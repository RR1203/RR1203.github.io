"""Verify claims_map.csv: every numeric claim in the manuscript must trace to a saved
analysis/output file, its producing script, and raw query id(s).

For each claim row this checks:
  1. the referenced analysis/output file exists and contains the claimed value;
  2. manuscript.md contains the claimed value;
  3. the referenced script exists;
  4. every referenced raw query id has status=ok in raw/manifest.csv.
Exit 1 on any failure. With zero claim rows (Degraded Mode) it verifies the
manuscript contains no Results section and prints a notice.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wonder_client import PROJECT_ROOT, make_logger

log = make_logger("07_check_claims")


def norm(text: str) -> str:
    return text.replace(",", "").replace("−", "-").replace("–", "-").replace("−", "-")


def value_in(value: str, text: str) -> bool:
    return norm(value.strip()) in norm(text)


def main() -> int:
    claims_path = PROJECT_ROOT / "claims_map.csv"
    manuscript = (PROJECT_ROOT / "manuscript.md").read_text()
    with claims_path.open() as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        if re.search(r"^#+\s*Results\b", manuscript, flags=re.M):
            log.error("claims_map.csv has zero claims but manuscript.md has a Results section")
            return 1
        log.info("0 claims to check (Degraded Mode); manuscript has no Results section — OK")
        return 0

    manifest_ok = set()
    mpath = PROJECT_ROOT / "raw" / "manifest.csv"
    if mpath.exists():
        with mpath.open() as fh:
            manifest_ok = {r["qid"] for r in csv.DictReader(fh) if r["status"] == "ok"}

    failures = 0
    for row in rows:
        cid, value = row["claim_id"], row["value"]
        problems = []
        src = PROJECT_ROOT / row["analysis_file"]
        if not src.exists():
            problems.append(f"analysis file {row['analysis_file']} missing")
        elif not value_in(value, src.read_text()):
            problems.append(f"value {value!r} not found in {row['analysis_file']}")
        if not value_in(value, manuscript):
            problems.append(f"value {value!r} not found in manuscript.md")
        if not (PROJECT_ROOT / row["script"]).exists():
            problems.append(f"script {row['script']} missing")
        for qid in filter(None, row["raw_query_ids"].split(";")):
            if qid.strip() not in manifest_ok:
                problems.append(f"raw query {qid.strip()} not ok in manifest")
        if problems:
            failures += 1
            log.error("claim %s FAILS: %s", cid, "; ".join(problems))
    log.info("%d/%d claims verified", len(rows) - failures, len(rows))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
