"""Step 1a: fetch CDC WONDER API documentation and query-form HTML into references/.

Saves (with access dates in references/sources/INDEX.md):
  - WONDER API help page
  - D76 / D158 database documentation pages
  - D76 / D158 entry pages, and the query-form HTML obtained after agreeing to the
    data-use restrictions (the form HTML enumerates the exact parameter codes).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wonder_client import PROJECT_ROOT, make_logger, request, sha256_file, utc_now_iso

REF = PROJECT_ROOT / "references" / "sources"
log = make_logger("01a_fetch_docs")

DOC_PAGES = {
    "WONDER-API.html": "https://wonder.cdc.gov/wonder/help/WONDER-API.html",
    "ucd-help.html": "https://wonder.cdc.gov/wonder/help/ucd.html",
    "ucd-expanded-help.html": "https://wonder.cdc.gov/wonder/help/ucd-expanded.html",
    "ucd-icd10-entry.html": "https://wonder.cdc.gov/ucd-icd10.html",
    "ucd-icd10-expanded-entry.html": "https://wonder.cdc.gov/ucd-icd10-expanded.html",
    # External QC benchmark (protocol §10): NCHS FastStats total U.S. deaths
    "faststats-deaths.html": "https://www.cdc.gov/nchs/fastats/deaths.htm",
}

FORM_POSTS = {
    # Agreeing to the data-use restrictions returns the query form HTML, which
    # contains every parameter name and picklist value code.
    "D76-form.html": (
        "https://wonder.cdc.gov/controller/datarequest/D76",
        {"stage": "about", "saved_id": "", "action-I Agree": "I Agree"},
    ),
    "D158-form.html": (
        "https://wonder.cdc.gov/controller/datarequest/D158",
        {"stage": "about", "saved_id": "", "action-I Agree": "I Agree"},
    ),
}


def main() -> int:
    REF.mkdir(parents=True, exist_ok=True)
    index_rows = []
    ok = True
    for fname, url in DOC_PAGES.items():
        try:
            resp = request("GET", url, log)
            path = REF / fname
            path.write_bytes(resp.content)
            index_rows.append((fname, url, "GET", utc_now_iso(), sha256_file(path)))
        except Exception as exc:  # noqa: BLE001 - log-and-continue by design
            log.error("FAILED %s: %s", url, exc)
            ok = False
    for fname, (url, data) in FORM_POSTS.items():
        try:
            resp = request("POST", url, log, data=data)
            path = REF / fname
            path.write_bytes(resp.content)
            index_rows.append((fname, url, "POST (I Agree)", utc_now_iso(), sha256_file(path)))
        except Exception as exc:  # noqa: BLE001
            log.error("FAILED %s: %s", url, exc)
            ok = False

    index = REF / "INDEX.md"
    lines = ["# references/sources — fetched during this run", "",
             "| file | url | method | accessed (UTC) | sha256 |",
             "|------|-----|--------|----------------|--------|"]
    if index.exists():
        lines = index.read_text().splitlines()
    for fname, url, method, ts, digest in index_rows:
        lines.append(f"| {fname} | {url} | {method} | {ts} | {digest} |")
    index.write_text("\n".join(lines) + "\n")
    log.info("wrote %s (%d new rows)", index, len(index_rows))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
