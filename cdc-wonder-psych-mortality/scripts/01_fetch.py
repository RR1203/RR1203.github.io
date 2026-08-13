"""Step 1: fetch the pre-registered query plan from CDC WONDER (D76 + D158).

Workflow per query:
  1. Load the saved query-form HTML (fetched by 01a_fetch_docs.py) and enumerate the
     authoritative parameter names/picklists from it.
  2. Build request parameters = form defaults + per-query overrides; validate every
     override against the form; refuse to post anything that fails validation.
  3. POST to the database controller with accept_datause_restrictions=true; save the
     exact request XML (raw/queries/qNN.xml) and the untouched response
     (raw/responses/qNN.xml); append a row to raw/manifest.csv; refresh raw/SHA256SUMS.

Failure policy: an HTML/error response or a parse failure marks the query failed;
failed queries are retried by rerunning this script (already-successful queries are
skipped — raw/ is append-only). Exit code 0 only when every query in the plan has a
successful response on disk.
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wonder_client import PROJECT_ROOT, make_logger, request, sha256_file, utc_now_iso
import wonder_api as wa

RAW = PROJECT_ROOT / "raw"
QUERIES = RAW / "queries"
RESPONSES = RAW / "responses"
MANIFEST = RAW / "manifest.csv"
REF = PROJECT_ROOT / "references" / "sources"

MANIFEST_FIELDS = ["qid", "database", "series", "strata", "purpose", "rows_returned",
                   "timestamp_utc", "request_sha256", "response_sha256", "status"]

log = make_logger("01_fetch")


def load_manifest() -> dict[str, dict]:
    if not MANIFEST.exists():
        return {}
    with MANIFEST.open() as fh:
        return {row["qid"]: row for row in csv.DictReader(fh)}


def append_manifest(row: dict) -> None:
    new = not MANIFEST.exists()
    with MANIFEST.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def write_shasums() -> None:
    lines = []
    for path in sorted(RAW.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS":
            lines.append(f"{sha256_file(path)}  {path.relative_to(RAW)}")
    (RAW / "SHA256SUMS").write_text("\n".join(lines) + "\n")


def ensure_docs() -> None:
    needed = ["D76-form.html", "D158-form.html"]
    if not all((REF / f).exists() for f in needed):
        log.info("query-form HTML missing; running 01a_fetch_docs.py")
        rc = subprocess.run([sys.executable, str(Path(__file__).parent / "01a_fetch_docs.py")]).returncode
        if rc != 0 or not all((REF / f).exists() for f in needed):
            raise RuntimeError("could not obtain query-form HTML; cannot build validated queries")


def run_query(spec: wa.QuerySpec, defaults, options, form_html) -> bool:
    cfg = wa.DB_CONFIG[spec.db]
    over = wa.build_overrides(spec, cfg)
    optional = {v for v in wa.SERIES[spec.series].get("optional_icd", [])}
    over, problems = wa.validate_overrides(over, defaults, options, form_html, optional)
    for p in problems:
        log.warning("%s validation: %s", spec.qid, p)
    fatal = wa.fatal_problems(problems)
    if fatal:
        log.error("%s NOT POSTED — %d fatal validation problems", spec.qid, len(fatal))
        append_manifest({"qid": spec.qid, "database": spec.db, "series": spec.series,
                         "strata": spec.strata, "purpose": spec.purpose, "rows_returned": 0,
                         "timestamp_utc": utc_now_iso(), "request_sha256": "",
                         "response_sha256": "", "status": "validation_failed"})
        return False

    params = wa.merged_params(defaults, over)
    xml = wa.to_request_xml(params)
    qpath = QUERIES / f"{spec.qid}.xml"
    qpath.write_text(xml)

    resp = request("POST", cfg["url"], log,
                   data={"request_xml": xml, "accept_datause_restrictions": "true"})
    rpath = RESPONSES / f"{spec.qid}.xml"
    rpath.write_bytes(resp.content)

    parsed = wa.parse_response(resp.content, spec.n_groupby, spec.n_measures)
    status = "ok" if parsed.ok else "bad_response"
    if not parsed.ok:
        log.error("%s response not usable: %s", spec.qid, parsed.message[:400])
    else:
        log.info("%s ok: %d rows (%d totals rows skipped)", spec.qid, len(parsed.rows),
                 parsed.total_rows_skipped)
    append_manifest({"qid": spec.qid, "database": spec.db, "series": spec.series,
                     "strata": spec.strata, "purpose": spec.purpose,
                     "rows_returned": len(parsed.rows), "timestamp_utc": utc_now_iso(),
                     "request_sha256": sha256_file(qpath),
                     "response_sha256": sha256_file(rpath), "status": status})
    return parsed.ok


def main() -> int:
    QUERIES.mkdir(parents=True, exist_ok=True)
    RESPONSES.mkdir(parents=True, exist_ok=True)
    ensure_docs()

    forms: dict[str, tuple] = {}
    for db in ("D76", "D158"):
        html = (REF / f"{db}-form.html").read_text(errors="replace")
        defaults, options = wa.parse_form(html)
        if len(defaults) < 20:
            log.error("%s form parsed to only %d defaults — form HTML may not be the query page",
                      db, len(defaults))
            return 2
        log.info("%s form: %d parameters, %d selects", db, len(defaults), len(options))
        forms[db] = (defaults, options, html)

    done = {qid for qid, row in load_manifest().items() if row["status"] == "ok"}
    plan = wa.build_query_plan()
    failures = 0
    for spec in plan:
        if spec.qid in done:
            log.info("%s already fetched ok — skipping (raw/ is append-only)", spec.qid)
            continue
        try:
            if not run_query(spec, *forms[spec.db]):
                failures += 1
        except Exception as exc:  # noqa: BLE001
            log.error("%s failed: %s", spec.qid, exc)
            append_manifest({"qid": spec.qid, "database": spec.db, "series": spec.series,
                             "strata": spec.strata, "purpose": spec.purpose,
                             "rows_returned": 0, "timestamp_utc": utc_now_iso(),
                             "request_sha256": "", "response_sha256": "",
                             "status": f"error: {str(exc)[:120]}"})
            failures += 1
    write_shasums()
    log.info("fetch pass complete: %d/%d queries ok", len(plan) - failures, len(plan))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
