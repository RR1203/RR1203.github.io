# MORNING README

## Run status: BLOCKED AT FETCH — pipeline complete and tested, zero data, zero fabricated numbers

The environment's egress network policy refused every connection to **wonder.cdc.gov**
and **www.cdc.gov** (HTTP CONNECT → 403 from the managed proxy — a per-destination
policy denial, while PyPI worked). Per your contract I retried on the prescribed
1/5/15/30/60-minute schedule (evidence: `logs/connectivity_probe.jsonl`), and entered
Degraded Mode when the cycles were exhausted. **No number anywhere in this project
came from anywhere.** The manuscript stops at Methods by design.

## What exists (all committed on branch `claude/cdc-wonder-psych-mortality-8lnoj3`, tag `overnight-final`)

- `00_protocol.md` — full pre-registration (hypotheses H1–H3 with decision rules,
  sensitivity S1–S4, suppression plan), committed before any data request.
- Complete scripted pipeline: `scripts/01a` (docs) → `01` (30 validated queries,
  append-only `raw/`) → `02` (tidy CSVs with explicit suppression flags) → `03`
  (7-check QC with PASS/FAIL) → `04` (pre-registered models only) → `05` (figures +
  tables + captions) → `07` (claims-map verifier), orchestrated by `run_all.sh`.
- 17 passing tests (`./venv/bin/python -m pytest tests/ -q`) covering the pipeline
  end-to-end against `SYNTHETIC`-labeled fixtures that never touch `data/`/`outputs/`.
- `manuscript.md` — Introduction + Methods only; `[REF NEEDED: …]` for every
  literature claim; zero numbers. `claims_map.csv` — header, zero rows.
- `VERIFY.md` (audit path), `DECISIONS.md` (every judgment call), `RUN_STATUS.md`,
  `ENVIRONMENT.md`, per-script logs in `logs/`.

## To complete the study (one command once CDC is reachable)

1. **Fix reachability first.** Easiest: in the Claude Code environment settings for
   this repository, add `wonder.cdc.gov` and `www.cdc.gov` to the network allowlist.
   Or run on any machine that can reach CDC:
   `git clone <repo> && cd RR1203.github.io/cdc-wonder-psych-mortality`.
2. Run `./run_all.sh` (≈10–15 min; ~30 queries ≥3 s apart). It fetches the API docs
   and both query forms, **validates every parameter against the saved form HTML
   before posting anything** (see caveat 1 below), then rebuilds
   data → QC → analysis → figures/tables and prints a reproducibility digest.
3. Read `qc/qc_report.md` — any FAIL must be resolved (or the affected stratum
   excluded and logged) before trusting results.
4. Write Results + Discussion into `manuscript.md` from `analysis/*.txt` and
   `outputs/`, adding one `claims_map.csv` row per numeric claim; then
   `./venv/bin/python scripts/07_check_claims.py` must exit 0.
5. Re-run `./run_all.sh --skip-fetch` twice and confirm identical digests, then
   follow `VERIFY.md` end to end.

## The three weakest points, in my judgment

1. **The WONDER request vocabulary was written blind.** The contract says enumerate
   parameter codes from the fetched form HTML — unfetchable tonight — so
   `scripts/wonder_api.py` encodes the documented conventions (`B_1`, `M_1`,
   `F_D76.V2`, `O_aar`, …) from prior knowledge, and `01_fetch.py` validates every
   name and picklist code against the *actually saved* form at runtime, refusing to
   post anything that doesn't validate. First-run failure mode is therefore a loud
   validation error, not a wrong query — but expect possibly one round of parameter
   fixes on first contact with the real API.
2. **H3's post-break precision.** The pre-registered 2018 breakpoint leaves two
   post-break years in D76 (one in the S2 sensitivity). This was accepted at
   pre-registration to avoid post-hoc breakpoint fitting; the D158 series (2018–latest)
   is the descriptive check. Treat the post-2018 slope as fragile.
3. **Chapter-level interpretation risk.** Series A (F01–F99) is dominated by dementia
   coding in the elderly, whose secular certification changes are large; conclusions
   should lean on the pre-specified A1/A2 split and the A′ (F10–F99) sensitivity, not
   on the chapter total.

## Questions I would have asked, and the defaults chosen instead

| Question | Default chosen (details in DECISIONS.md) |
|----------|------------------------------------------|
| CDC hosts are policy-blocked — abort, or build everything for a one-command morning run? | Built + tested the full pipeline; Degraded Mode per contract (§4) |
| "Never push" vs an ephemeral container that would destroy all work? | Push only to the session's designated branch on your own repo (§2) |
| Deliverables at repo root of your website, or a subdirectory? | Subdirectory `cdc-wonder-psych-mortality/` (§3) |
| If Y87.0/U03 are not selectable in a database's picklist? | Auto-prune with a logged warning; X60–X84 carries the series (protocol §3) |
| D158 actual year coverage (2024 final yet?) | Whatever the database serves; observed at fetch, logged |

## Recommended next steps

1. Unblock the network, run `./run_all.sh`, and triage any parameter-validation
   errors (each names the offending parameter and the saved form file to inspect).
2. After a green run: complete manuscript Results/Discussion + `claims_map.csv`
   (step 4 above) — this part was deliberately not automatable tonight because no
   real numbers exist.
3. Consider registering the protocol (e.g., OSF) before looking at results, since it
   is genuinely pre-data.

### Handoff notes — NSDUH mechanism companion paper

- **Role split:** this project gives national outcome trends (deaths); NSDUH
  (SAMHSA's National Survey on Drug Use and Health) supplies candidate mechanisms:
  past-year SUD prevalence, unmet treatment need, MH service receipt, by the same
  sex × 10-year-age strata and years (2002 onward).
- **Comparability discipline transfers directly:** NSDUH has known series breaks
  (2015 questionnaire redesign; 2020–2021 methodology change) — treat them like
  D76/D158 here: separate series, never spliced, with overlap-style consistency
  checks where possible.
- **Network scope to request up front:** samhsa.gov / datafiles.samhsa.gov (public-use
  files + codebooks) — tonight's failure shows the allowlist must be verified with a
  probe *before* the run is scheduled (`scripts/01b_connectivity_probe.py` is
  reusable as-is).
- **Design linkage is ecological only:** align NSDUH prevalence series against these
  mortality series by year/stratum for coherence-of-trends arguments; no individual
  linkage exists, and the companion paper should pre-register that limitation the
  same way this protocol does.
