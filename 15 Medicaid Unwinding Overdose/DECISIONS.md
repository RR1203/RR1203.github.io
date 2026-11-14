# DECISIONS.md — Medicaid unwinding → overdose deaths

Every judgment call made during the run, in the order made. "Pre-outcome" = decided before any 2023–2025 death data were modelled.

## Setup
1. **Location.** Only one repo is in scope for this session (`rr1203.github.io`, the personal website). Project lives in the folder `15 Medicaid Unwinding Overdose/` on branch `claude/new-session-u6tkjb`, not on `main`, so it is not published on the site.
2. **Software.** R 4.x from Ubuntu apt; packages from Ubuntu `r-cran-*` builds, `fixest` from CRAN source (binary repo blocked). Recorded in session info at the end of the knitted HTML.
3. **Blocked hosts.** `download.medicaid.gov` and `www.kff.org` were not reachable. All CMS tables were pulled through the `data.medicaid.gov` datastore API instead (same tables, same distribution IDs). The KFF tracker was not used.

## Step 0.1 Novelty
4. Searched PubMed, Europe PMC (includes preprints), and NBER/SSRN via web search. No study estimates unwinding → deaths. Gate passed. Details in `00_novelty.md`.

## Step 0.2 Exposure (pre-outcome)
5. **Source.** CMS Performance Indicator (PI) dataset, October 2026 release (data.medicaid.gov distribution `f4d1d0b1-…`). Where a state-month has both preliminary (P) and updated (U) rows, the updated row is used.
6. **Adult enrollment.** CMS's own `total_adult_medicaid_enrollment` only starts in late 2024, so adult enrollment = total Medicaid & CHIP enrollment − Medicaid & CHIP child enrollment. Check: in months where both exist (Dec 2024, Jun 2025) the derived and reported counts correlate at r > 0.9999 (median ratio 1.00).
7. **Zeros with "Unable to provide data" footnotes** are treated as missing, not zero.
8. **Arizona** reports no child enrollment before mid-2024, so its adult change cannot be computed from a March 2023 baseline. Fallback for any such state: % change in total Medicaid & CHIP enrollment. Flagged in `clean_data.xlsx` (`exposure_source`).
9. **Missing target month** (e.g., Rhode Island Dec 2024 reported as 0): use the nearest earlier valid month. Flagged.
10. **Main exposure** = % drop in adult enrollment from March 2023 to **June 2024** (most states had finished their unwinding renewals by mid-2024). Dec 2023 and Dec 2024 versions are computed and kept for robustness. Intensity = −(% change), so larger = more disenrollment, then standardized (z-score across the 51 jurisdictions).
11. **North Carolina (expanded Dec 2023) and South Dakota (expanded Jul 2023)** show adult enrollment *gains*. They are kept in the main exposure (their net coverage change is the true exposure) and dropped in a sensitivity check.
12. **Procedural share and ex parte share** come from the CMS "Medicaid and CHIP CAA Reporting Metrics" dataset (reporting months Mar 2023–Jul 2024): procedural share = Σ Metric 5c / Σ (5b + 5c); ex parte share = Σ 5a1 / Σ 5. The "Updated Renewal Outcomes" file only covers through Mar 2024, so it was downloaded but not used.
13. **Delayed unwinding** = first month with any reported termination later than June 2023. **Heavy ex parte** = top quartile of ex parte share. Both are data-derived rather than taken from KFF (blocked).
14. **Medicaid expansion** status and date from the PI dataset's monthly `state_expanded_medicaid` flag; yearly control = share of months in the year with expansion in effect.
15. The CMS T-MSIS eligibility-group file was downloaded but ends Dec 2022, so it cannot measure unwinding. Not used.

## Step 0.3 First stage (pre-outcome)
16. **Source.** State Drug Utilization Data (SDUD) 2018–2025 via datastore API; rows with product names starting BUPREN, SUBOX, SUBUT, ZUBSO, BUNAV, SUBLO, BRIXA.
17. **OUD vs pain formulations.** NDCs are matched to the FDA NDC Directory (current + excluded/discontinued files). OUD = sublingual, buccal/sublingual with naloxone, or subcutaneous extended-release (Sublocade, Brixadi). Pain = transdermal (Butrans and generics), buccal buprenorphine without naloxone (Belbuca), IM/IV (Buprenex). Pain formulations are excluded.
18. NDCs not found in the FDA files are classified by SDUD product name (brand → OUD; generic `BUPRENORPH` with no FDA match → see `analysis.Rmd`, decision logged after data review).
19. **National row** (`state == "XX"`) dropped. Fee-for-service and managed-care rows summed.
20. **Suppressed cells** (fewer than 11 prescriptions) set to 0 in the main count; the maximum they could add (10 × number of suppressed rows) is reported relative to the total.
21. **First-stage model.** State × quarter Poisson of Medicaid OUD-buprenorphine prescriptions, population offset, state and quarter FE, intensity × post (2023 Q2 onward), SE clustered by state, 2019 Q1 to latest quarter. **Pass rule:** coefficient negative with p < 0.05.

## Step 0.4 Power (pre-outcome)
22. **MDE.** 2018–2022 deaths only. Placebo design mirroring the main model: real intensity × fake post-years 2021 and 2022 (separate terms), state + year FE, population offset, state-clustered SE. MDE (80% power, two-sided α = 0.05) = 2.80 × SE, expressed as % change in deaths per 1 SD of intensity. Also a pooled version (one fake-post term for 2021–2022). **The gate uses the smallest of the three MDEs**, i.e. the one most favourable to continuing.
23. **Plausible effect.** (Lost Medicaid buprenorphine prescriptions per SD of intensity, from the first stage) × (30 days / 365, assuming each prescription = 30 days of treatment; this is generous, since many fills are shorter) × (excess overdose mortality off vs on buprenorphine: 4.6 − 1.4 = 3.2 per 1,000 person-years; Sordo et al., BMJ 2017, doi:10.1136/bmj.j1550), divided by mean state overdose deaths in 2022.
24. Generous alternative: all-cause mortality difference 9.5 − 4.3 = 5.2 per 1,000 PY (same source). Also a break-even figure: the excess mortality per 1,000 PY that would be needed for the plausible effect to reach MDE / 2.
25. **Stop rule** (from the brief): stop if MDE > 2 × plausible effect.
