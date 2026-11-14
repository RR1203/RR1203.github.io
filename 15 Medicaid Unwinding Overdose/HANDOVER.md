# Handoff: Medicaid unwinding → overdose deaths (project 15)
2026-11-14 · Overnight autonomous run of the brief `addiction_1_medicaid_unwinding_overdose_prompt.md`. It stopped at the Step 0 gates.

## Objective
Test whether states with larger Medicaid disenrollment from April 2023 ("unwinding") had more overdose deaths in 2023–2025 than they otherwise would have. The brief requires passing four gates first: novelty, exposure data, first stage, power. **Stop if a gate fails.** "No detectable effect" is an acceptable result.

## Current state
- **The run stopped at Step 0.4 (power).** The first-stage gate also failed. No 2023–2025 death models were run.
- **Gate 1, novelty: passed.** No study estimates unwinding → deaths. The closest is Constantin et al., JAMA Netw Open 2025, doi 10.1001/jamanetworkopen.2025.8469, which covers buprenorphine only.
- **Gate 2, exposure: built for all 51 jurisdictions.** Mean adult enrollment drop Mar 2023→Jun 2024 was 19.1% (SD 12.8). The range runs from −31.7% (NC, which expanded) to 38.6% (CO).
- **Gate 3, first stage: failed** by the rule set before seeing results.
  - Pooled effect: −3.2% Medicaid buprenorphine Rx per SD of disenrollment (95% CI −10.7% to +4.9%, p = 0.42).
  - Event study vs 2022: 2023 +0.1%, 2024 −6.1% (p = 0.009), 2025 −9.4% (p = 0.003).
  - The pre-period slopes from −6.6% in 2019 to 0 in 2022 (joint p = 0.45).
  - Quartiles show no gradient.
  - Dropping NC and SD flips the sign (+1.4%, p = 0.87).
- **Gate 4, power: failed.**
  - The minimum detectable effect (MDE, 80% power) is 5.2% per SD.
  - The plausible effect is 0.07% (overdose excess), 0.12% (all-cause), or 0.39% (all-cause × first-stage CI bound). That makes the MDE 73×, 45× and 14× larger, against a 2× limit.
  - Break-even: excess mortality would need to be ~117 per 1,000 person-years, vs 3.2–5.2 in Sordo 2017.
- Everything is committed and pushed to branch `claude/new-session-u6tkjb` in `rr1203/rr1203.github.io` (last commit `1b22483`).

## Decisions (and why)
Full log: `DECISIONS.md` (33 entries). The key ones:
- **Project location:** folder in the website repo on a branch, not `main`. This was the only repo in scope, and keeping it off `main` keeps it off the public site.
- **CMS data via the data.medicaid.gov datastore API:** `download.medicaid.gov` and `kff.org` were blocked.
- **Adult enrollment = total Medicaid & CHIP − child enrollment:** CMS's own adult field only starts in late 2024. The derived count matches it at r = 1.00.
- **AZ uses total enrollment** (no child counts before mid-2024). **RI Dec 2024 uses Nov 2024** (Dec reported as 0).
- **Main exposure is Mar 2023 → Jun 2024**, because most renewals were done by mid-2024. Dec 2023 and Dec 2024 versions are kept for robustness. Exposure is standardized (z).
- **NC and SD stay in the main exposure**, since their enrollment gains are real net exposure. They are dropped in a sensitivity check.
- **Procedural share, ex parte share and start month come from CMS CAA Reporting Metrics** (Mar 2023–Jul 2024). The "Updated Renewal Outcomes" file only runs to Mar 2024.
- **Delayed unwinding and heavy ex parte are data-derived** because KFF was blocked:
  - Delayed = first termination after Jun 2023. Only OR qualifies.
  - Heavy ex parte = top quartile of ex parte share (≥ 0.53). 13 states qualify.
- **OUD buprenorphine:** NDCs are classified with the FDA NDC Directory route. Transdermal, Belbuca and Buprenex are excluded as pain products.
  - Fallback for NDCs not in the FDA directory: product name first, then units per Rx (≥ 7 counts as OUD).
  - Suppressed cells are set to 0. Setting them to the 10-Rx upper bound adds only 0.6%.
- **First-stage pass rule** (pre-specified): pooled term negative with p < 0.05. The significant 2024–2025 year estimates were **not** swapped in as the gate after seeing them.
- **Power method:**
  - MDE comes from placebo models on 2018–2022 deaths, and the gate uses the smallest of the three MDEs (the most lenient).
  - Plausible effect = lost Rx × 30/365 × excess mortality off buprenorphine (Sordo et al., BMJ 2017, doi 10.1136/bmj.j1550: overdose 4.6 vs 1.4, all-cause 9.5 vs 4.3 per 1,000 PY).
  - The 30-day supply per Rx is an assumption, chosen to be generous.

## Dead ends — do not retry
- `download.medicaid.gov` and `www.kff.org` are blocked from the cloud environment. Use the data.medicaid.gov API instead (`/api/1/datastore/query/{distribution_id}`, POST, limit 5000).
- The CMS T-MSIS eligibility-group file ends Dec 2022, so it cannot measure unwinding.
- The binary R repo (p3m.dev) is blocked. Use Ubuntu `r-cran-*` packages and install fixest from CRAN source.
- NBER w21580 and w32227 are about the 2005 TennCare disenrollment, not unwinding. Don't cite them as unwinding evidence.

## Artifacts (all in `15 Medicaid Unwinding Overdose/`, final unless noted)
- `SUMMARY.md`: FLAG line, scorecard, step audit, Methods/Results, recap
- `DECISIONS.md`: 33 numbered decisions
- `00_novelty.md`: search log and closest papers
- `analysis.Rmd` / `analysis.html`: cleaning (01.1–01.8), F1 first stage, P1 power, gate decision
- `figures_tables.Rmd` / `figures_tables.html`, plus `figures/`:
  - exposure dot plot
  - buprenorphine trends by quartile
  - buprenorphine event study
  - MDE vs plausible effect chart
  - CSV tables
- `clean_data.xlsx`, with sheets:
  - `state_year` (408 rows; deaths all/opioid/synthetic/stimulant, population, unemployment, expansion share, exposures)
  - `state` (51)
  - `state_quarter` (1,632)
  - `reporting_log`
  - `ndc_lookup`
- `results.rds`: all F1/P1 models and gate objects
- `raw/`: CDC VSRR, CMS PI, CAA, renewal outcomes, T-MSIS (unused), Census V2020 and V2025, FRED (51 files), SDUD buprenorphine extract (132,832 rows), FDA buprenorphine NDC extract. The FDA zips are git-ignored and can be downloaded again from accessdata.fda.gov.

## Verbatim essentials
- Stop rule from the brief: "Stop if the MDE is more than twice the plausible effect; report it as a feasibility result."
- Outcome: CDC VSRR dataset `xkb8-kh2a`, 12-month-ending December values. NY = NY + YC (NYC is reported separately). Data run through Dec 2025.
- CMS PI distribution `f4d1d0b1-d27d-53aa-9902-b4425dbad6b3` (Oct 2026 release). SDUD covers 2018 Q1–2025 Q4.
- Software: R 4.3.3, fixest 0.14.2, tidyverse 2.0.0.

## Working preferences
- House style is hannes-04-analysis: one Rmd, raw → clean Excel, self-contained blocks, small chunks, `print()` on every output, no loops or helper functions for models.
- Log every decision in `DECISIONS.md`. Never invent numbers or citations; write [REF NEEDED].
- Summaries use the hannes-code-summary format with a FLAG line and a 0–10 scorecard.
- Concise, bullet-style communication. Run autonomously without asking questions.

## Open items
- **Next step (your decision):** accept the stop as a feasibility result, or override it and run the outcome models as an explicitly labelled, underpowered reduced form.
- If you override, these models from the brief are not yet written:
  - main Poisson with intensity × 2023/2024/2025
  - event study 2018–latest, reference 2022, with a pre-trend test
  - quartile dose-response
  - 2SLS (exploratory)
  - placebo timing 2020/2021
  - psychostimulant placebo outcome
  - drop the 5 largest states one at a time
  - exclude delayed (OR) and heavy ex parte states
  - control for pre-2022 state trends
- Not done: `00_PIPELINE.md` tick (no file exists) and a PR (none requested).

## Suggested opening prompt
> Read `15 Medicaid Unwinding Overdose/HANDOVER.md`, `SUMMARY.md` and `DECISIONS.md` on branch `claude/new-session-u6tkjb` of rr1203/rr1203.github.io. The run stopped at the first-stage and power gates. I want to [accept the stop and draft a short feasibility note | override the gate and add the outcome models from the brief as an explicitly underpowered reduced form, in the same Rmd and house style]. Keep logging every decision in DECISIONS.md.
