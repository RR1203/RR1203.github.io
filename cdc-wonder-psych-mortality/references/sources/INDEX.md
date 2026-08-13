# references/sources — fetched during this run

| file | url | method | accessed (UTC) | sha256 |
|------|-----|--------|----------------|--------|

**No reference page could be fetched during this run.** Every request to
wonder.cdc.gov and www.cdc.gov was refused by the session's egress network policy
(HTTP CONNECT rejected with 403 by the managed proxy) across all scheduled retry
cycles — see `logs/connectivity_probe.jsonl`, `logs/01a_fetch_docs_*.log`, and
`DECISIONS.md` §4. Re-running `scripts/01a_fetch_docs.py` on a network that can reach
CDC populates this directory and appends rows to this index automatically.

Planned contents (fetched automatically by `scripts/01a_fetch_docs.py`):
WONDER API help page, D76/D158 database documentation, D76/D158 entry pages and
query-form HTML (the authoritative parameter enumeration used by `scripts/01_fetch.py`
for validation), and the NCHS FastStats deaths page (external QC benchmark).
