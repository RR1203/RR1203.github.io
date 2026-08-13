# QC report

**STATUS: NOT RUN — BLOCKED AT FETCH.**

No CDC WONDER data exists in this checkout (the session's egress network policy denied
every connection to wonder.cdc.gov and www.cdc.gov across all scheduled retry cycles;
evidence in `logs/connectivity_probe.jsonl` and `DECISIONS.md` §4). Quality control is
implemented and tested in `scripts/03_qc.py`; running `./run_all.sh` on a network that
can reach CDC will regenerate this file with an explicit PASS/FAIL verdict per check:

1. Tidy row counts vs `raw/manifest.csv`.
2. External benchmark: all-cause deaths vs a figure published on www.cdc.gov, fetched
   and saved during the run (`references/sources/faststats-deaths.html`).
3. Internal consistency: stratum sums vs year totals, with the suppression-induced
   shortfall quantified (each suppressed cell holds 1–9 deaths).
4. D76 vs D158 overlap 2018–2020 for every study series (≤2% divergence threshold).
5. Suppressed/unreliable cell audit by query and stratum (table).
6. Denominator sanity: Census order-of-magnitude, no zero/negative populations,
   cross-series equality of national denominators.
7. Completeness of the year × stratum grid, duplicate detection, and the cell
   invariant (each measure cell is numeric XOR exactly one marker flag).

No check was executed against real data, so no PASS is claimed for any of them.
