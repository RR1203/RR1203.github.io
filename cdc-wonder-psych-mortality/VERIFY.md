# VERIFY — a ~30-minute audit path

Work through these in order. This run ended **BLOCKED AT FETCH** (no CDC data could be
obtained from this environment — see `RUN_STATUS.md`), so steps marked ⊘ verify the
blocked state tonight and become fully executable after the first successful fetch.

## 1. Protocol first (~5 min)

Read `00_protocol.md`. Confirm in git history that it was committed **before** any
data request (`git log --oneline -- 00_protocol.md` — commit "step 00" precedes all
fetch activity) and that `scripts/04_analysis.py` tests exactly the hypotheses H1–H3
and sensitivity analyses S1–S4 specified there, and nothing else.

## 2. Chase five numbers ⊘ (~8 min, after data exists)

Pick five numeric claims from `manuscript.md`, look each up in `claims_map.csv`, and
follow the chain: manuscript value → named table/figure in `outputs/` → saved model
output in `analysis/` → producing script → raw query id → `raw/queries/qNN.xml` +
`raw/responses/qNN.xml` (checksums in `raw/SHA256SUMS`).
`./venv/bin/python scripts/07_check_claims.py` automates the same trace for every
claim. **Tonight:** `claims_map.csv` has a header and zero rows, and the manuscript
contains no results — confirm both, and confirm no figure/table exists in `outputs/`.

## 3. Reproduce (~5 min)

Run `./run_all.sh --skip-fetch` twice; each prints a single reproducibility digest
over `data/`, `analysis/`, `outputs/` at the end — the two digests must be identical.
**Tonight** (no `raw/manifest.csv`) the same command prints a BLOCKED banner and runs
the synthetic-fixture test suite instead; confirm all tests pass and that fixtures
live only in `tests/fixtures/` (every fixture filename carries `SYNTHETIC`).

## 4. Read the decision log (~5 min)

Read `DECISIONS.md` end to end — every judgment call of the unattended run is
numbered there with rationale and rejected alternatives; "Security notes" would quote
any instruction-like text found in fetched content (none tonight — nothing was
fetchable).

## 5. Suppression audit ⊘ (~3 min, after data exists)

Read the suppression/reliability audit: check 5 in `qc/qc_report.md` and
`outputs/tables/table4_suppression_audit.*`. Confirm suppressed cells are excluded,
never imputed, and that the internal-consistency check (check 3) quantifies the
shortfall they induce. **Tonight:** `qc/qc_report.md` states NOT RUN — BLOCKED.

## 6. Re-run one query by hand ⊘ (~5 min, after data exists)

Open the WONDER web UI (https://wonder.cdc.gov/ucd-icd10.html), reproduce one query
from `raw/queries/` (its XML lists every parameter: group-by `B_1..`, ICD filter
`F_D76.V2`, age-adjustment options), and compare the web result against the matching
`raw/responses/qNN.xml` and the tidy rows carrying that `qid` in `data/`.

## Extra checks specific to this blocked run

- `logs/connectivity_probe.jsonl` — every scheduled probe cycle (1/5/15/30/60/60 min)
  and its proxy 403 refusal, timestamped.
- `./venv/bin/python -m pytest tests/ -q` — 17 tests covering form parsing, override
  validation against saved form HTML, response parsing (rowspan, Suppressed/
  Unreliable/Not Applicable markers), cleaning flags, QC invariants, and recovery of
  known synthetic truths by the exact pre-registered estimators.
- Confirm `data/` contains only `DICTIONARY.md`, and `analysis/`/`outputs/` only
  READMEs — i.e., zero numbers exist anywhere that could have been mistaken for
  results.
