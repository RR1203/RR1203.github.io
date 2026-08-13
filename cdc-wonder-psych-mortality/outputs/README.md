# outputs/ — figures and tables

**Currently empty except this note: the run was blocked at fetch** (no CDC data; see
`RUN_STATUS.md` and `DECISIONS.md` §4). Producing any figure or table from synthetic
data is prohibited by the operating contract, so none exists.

When `scripts/05_outputs.py` runs on real data it writes:
- `figures/figN_*.png` with a `figN_*.caption.txt` naming the producing script and
  input data files;
- `tables/tableN_*.csv` and `.md` with matching caption files.
