**FLAG:** The data-access gate failed. No source with monthly × province × ICD-10 admissions after June 2025 could be reached: HDC and NHSO refuse non-Thai IPs, THIP needs ethics approval, and data.go.th and the Royal Gazette sit behind Cloudflare. H1–H3, the DiD, event studies and all checks were therefore **not run**. Other deviations: run in the cloud rather than on a Mac. The network allowlist was widened by 19 exact hosts, not set to Full. Primary SEs are model-based NB rather than Newey-West, because the power simulation showed NW was anti-conservative. Appendicitis was added as a negative control. One helper function and replicate() were used for the power simulation.

**Scorecard (0–10, based on what the data showed)**

| Novelty | First stage | Power | Big result | Rigor | Feasibility |
|---|---|---|---|---|---|
| 9 | 6 | 6 | n/a (not run) | 7 | 3 |

- Novelty: no study of the 2025 reversal found in PubMed, Europe PMC or Thai/English web searches. One unread 2026 J Cannabis Res surveillance paper still needs checking.
- First stage: the fall is documented (84.5% of 2025-expiring licences not renewed). The rise from 2022 to mid-2025 has no verified counts, and there is no province time series.
- Power: national F12.5 and F12.2 can detect a 15–20% drop if overdispersion is low (theta 100), but only 30–40% if it is high (theta 25).
- Feasibility: it depends on a Thai collaborator or Thai IP.

**Is cannabis harm reversible after re-regulation?** Not answerable yet. The admissions data after June 2025 exist (HDC, THIP) but could not be reached from this run, so no estimate was made.

---

### 1. What the code did

1. Read the sourced first-stage values — `raw_first_stage.csv`, 28 hand-entered rows, each with source URL and verification status → `raw_first_stage`
2. Read the outcome definitions — `outcome_codes.csv`, 9 outcomes (F12, F12.5, F20–F29, T40.7, F10, F15, K35–K37, all IP, F chapter) → `codes`
3. Split the rows by table — shops n = 14, survey n = 5, HDC/Addiction context means n = 9 → `shop_panel`, `survey_prevalence`, `hdc_context`
4. Built the admissions panel — `raw_admissions.csv` absent, so an empty template (0 rows) → `admissions_panel`
5. Wrote the clean workbook — 5 sheets → `clean_data.xlsx`
6. Computed licence non-renewal — 8,636 expired, 1,339 renewed, 7,297 not renewed (84.5%); 7,297 / 18,433 = 39.6% of all establishments → printed
7. Plotted shop counts — national points Dec 2025 – Nov 2026 only → `figures/first_stage_shops.png`
8. Plotted CADS past-year use — 2019–2021 → `figures/first_stage_survey.png`
9. Built the simulation grid — monthly Jan 2017 – Oct 2026, 118 months, 65 before June 2022 → `p1_grid`
10. Simulated power for the 2025 level drop — NB data (theta 25 / 100), segmented glm.nb (trend, month FE, COVID Mar 2020 – Dec 2021, level and slope at Jun 2022 and Jul 2025), model-based Wald test, 200 replicates × 7 drop sizes × 4 outcomes × 2 theta × 2 follow-ups (12 / 16 post months) → `p1_power`
11. Derived the MDE at 80% power and labelled it (powered if MDE ≤ 20%) → `p1_mde`, `figures/power_mde.png`
12. Saved the status, first stage and power results → `results.rds`

**Unverified:** All shop counts and the ONCB/PeerJ survey figures come from search-engine excerpts; the pages were not opened. The HDC means come from an advocacy open letter. Royal Gazette volume and page numbers are unknown. The 2022 jump size, the +8%/yr pre-trend, the 5% seasonality and theta are assumed. F20–F29, F10 and F15 have no baseline counts, so they were not simulated.
**Not run:** H1 (symmetry, event studies, DiD vs F10/F15, age split, placebo Jun 2020 / Jun 2024, anticipation May 2024 / May 2025, coding check), H2 (dose, tourism provinces, leave-one-province-out), H3 (F12.5, F20–F29, T40.7). The code is written and was smoke-tested on a simulated panel only (scratchpad, not saved): it recovered a symmetry level ratio of −0.98 (95% CI −1.11 to −0.86) against a truth of −1.

---

### 2. Methods and Results

**Methods.** The planned design was a monthly segmented negative-binomial time series of national and provincial admissions, January 2017 to the latest available month. It has breakpoints in June 2022 (delisting effective 9 June 2022) and July 2025 (controlled-herb notification effective 26 June 2025), with month-of-year fixed effects, a COVID-19 indicator (March 2020 – December 2021), and a population offset. The primary outcome was any-diagnosis F12, with F12.5, F20–F29 (principal diagnosis) and T40.7 as key secondary outcomes, and F10, F15 and appendicitis (K35–K37) as comparison outcomes. Symmetry was defined as the ratio of the 2025 to the 2022 log level change, with a 2,000-draw parametric bootstrap CI. Because no post-June-2025 admissions data could be obtained, only the first stage and an approximate power analysis were run. Power for the 2025 level change was estimated by simulation (200 replicates per scenario) under a negative-binomial data-generating process. Inputs were national monthly means from Health Data Center reports quoted in a June 2026 open letter (F12.5: 85 before 2022, 556 in year 3; F12.2: 130 and 830; T40.7: 35, 115 and 60) and from Puetpaiboon et al. 2026 (cannabis admissions age 10–19: about 27 and 150 per month). Model-based standard errors replaced Newey-West SEs after the simulation showed Newey-West type I error of 0.06–0.25 with 12–16 post-reversal months. Analyses used R 4.3.3 with MASS, sandwich and lmtest.

**Results.** Of 8,636 cannabis-shop licences that expired in 2025, 1,339 were renewed and 7,297 (84.5%) were not, which is 39.6% of the 18,433 establishments licensed by 28 December 2025. In November 2026, 12,279 outlets were licensed nationally, including 1,726 in Bangkok, 1,046 in Phuket, 900 in Chon Buri, 717 in Surat Thani and 482 in Chiang Mai. Past-year cannabis use among adults aged 18–65 rose from 2.2% (2019) to 2.5% (2020) and 4.2% (2021); no comparable 2022–2025 survey waves were found. With 16 post-reversal months, the minimum detectable level drop at 80% power was 15% for F12.5 and F12.2 at theta 100, and 30% at theta 25. For cannabis admissions age 10–19 it was 20% and 30%, and for T40.7 30% and 40%. Empirical type I error ranged from 0.020 to 0.085. With 12 post months, the MDEs were 20–30% (theta 100) and 30–40% (theta 25). A 40% drop, the largest simulated, was detected with power 0.93–1.00 in all 16 scenarios. A fully symmetric reversal (F12.5 back from about 556 towards 85 per month) would be a far larger drop than any simulated.

---

### 3. Recap

- Completed the novelty search, policy timeline, data-access audit, first stage and power analysis. Wrote the full two-breakpoint analysis code, but the main analysis did not run because the data-access gate failed.
- The reversal is unstudied. The shop fall is real (84.5% of expiring licences not renewed). National F12/F12.5 are powered for drops of 15–30% or more. Admissions data after June 2025 exist in HDC and THIP but cannot be reached from outside Thailand.
- Decide: (a) pull HDC province × month reports by hand on the Mac, or (b) send `draft_email.md` (not sent) to the PSU/THIP group. Then drop `raw_admissions.csv` into the folder and re-knit.
