# analysis/ — saved model outputs

**Currently empty except this note: the run was blocked at fetch** (no CDC data; see
`RUN_STATUS.md` and `DECISIONS.md` §4). Nothing here may be produced from anything but
real WONDER responses in `raw/` — synthetic fixtures live exclusively in
`tests/fixtures/` and are prohibited from producing analysis outputs.

When `scripts/04_analysis.py` runs on real data it writes one complete model-output
text file per pre-registered analysis (H1–H3, S1–S4, pre-specified descriptives) plus
`results_summary.json`. The rule enforced by `scripts/07_check_claims.py`: no number
may appear in the manuscript that is not present in a saved output file here.
Exploratory work (none planned) would live under `exploratory/`.
