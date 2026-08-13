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

ok_queries() { [ -f raw/manifest.csv ] && awk -F, 'NR>1 && $NF=="ok"' raw/manifest.csv | wc -l || echo 0; }

if [ "$SKIP_FETCH" -eq 0 ]; then
  echo "== step 1a: reference/documentation pages =="
  $PY scripts/01a_fetch_docs.py || echo "WARN: documentation fetch failed"
  echo "== step 1: WONDER queries (contract backoff: 1/5/15/30/60 min between passes) =="
  for pause in 0 60 300 900 1800 3600; do
    [ "$pause" -gt 0 ] && { echo "…retrying failed queries in ${pause}s"; sleep "$pause"; }
    $PY scripts/01_fetch.py && break
    if [ "$(ok_queries)" -eq 0 ]; then
      echo "No query has ever succeeded — systemic block (network policy?), not a"
      echo "transient failure. Abandoning retry cycles; see logs/01_fetch_*.log."
      break
    fi
  done
fi

if [ "$(ok_queries)" -eq 0 ]; then
  echo "=============================================================="
  echo "BLOCKED AT FETCH: no successful query in raw/manifest.csv — no CDC"
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
