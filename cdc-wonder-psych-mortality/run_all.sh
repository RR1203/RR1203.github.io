#!/usr/bin/env bash
# Rebuild the whole study from a clean checkout: venv, fetch (unless --skip-fetch),
# clean, QC, analysis, outputs, claims check. With --skip-fetch everything is rebuilt
# from the committed raw/ with no network access.
set -uo pipefail
cd "$(dirname "$0")"

SKIP_FETCH=0
[ "${1:-}" = "--skip-fetch" ] && SKIP_FETCH=1

if [ ! -x venv/bin/python ]; then
  echo "== creating venv =="
  python3 -m venv venv
fi
./venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt
PY=./venv/bin/python

if [ "$SKIP_FETCH" -eq 0 ]; then
  echo "== step 1a: reference/documentation pages =="
  $PY scripts/01a_fetch_docs.py || echo "WARN: documentation fetch failed"
  echo "== step 1: WONDER queries =="
  $PY scripts/01_fetch.py || echo "WARN: fetch pass incomplete (rerun to retry failed queries)"
fi

if [ ! -s raw/manifest.csv ]; then
  echo "=============================================================="
  echo "BLOCKED AT FETCH: raw/manifest.csv is absent or empty — no CDC"
  echo "data exists in this checkout. Nothing downstream can run on real"
  echo "data. Running the synthetic-fixture test suite instead (fixtures"
  echo "live only in tests/fixtures/ and never enter data/ or outputs/)."
  echo "=============================================================="
  exec $PY -m pytest tests/ -q
fi

echo "== step 2: clean ==";    $PY scripts/02_clean.py    || exit $?
echo "== step 3: QC ==";       $PY scripts/03_qc.py;      QC=$?
[ "$QC" -eq 3 ] && exit 3
[ "$QC" -ne 0 ] && echo "WARNING: QC has FAIL checks — see qc/qc_report.md before trusting results"
echo "== step 4: analysis =="; $PY scripts/04_analysis.py || exit $?
echo "== step 5: outputs ==";  $PY scripts/05_outputs.py  || exit $?
if [ -f claims_map.csv ]; then
  echo "== claims check =="
  $PY scripts/07_check_claims.py || exit $?
fi
echo "== reproducibility digest (data/ analysis/ outputs/) =="
bash scripts/hash_outputs.sh
