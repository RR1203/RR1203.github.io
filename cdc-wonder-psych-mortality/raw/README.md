# raw/ — append-only archive of CDC WONDER requests and responses

**Currently empty: the run was blocked at fetch** (egress network policy denied all
access to CDC hosts; evidence in `logs/connectivity_probe.jsonl` and `DECISIONS.md`
§4). No raw data means no data products anywhere downstream — by design, nothing in
`data/`, `analysis/` or `outputs/` may exist unless it derives from files here.

When `scripts/01_fetch.py` runs successfully it creates:

- `queries/qNN.xml` — the exact request XML posted for each query
- `responses/qNN.xml` — the untouched response
- `manifest.csv` — query id, database, series, strata, purpose, rows returned,
  timestamp, request/response SHA-256, status
- `SHA256SUMS` — checksums of every file in this directory

This directory is append-only forever after: already-successful queries are never
re-posted or overwritten (the fetch script skips them on re-runs).
