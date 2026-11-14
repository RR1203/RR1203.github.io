**FLAG:** Run STOPPED at Step 0. The first-stage gate failed (pre-specified pooled test p = 0.42) and the power gate failed (MDE 5.2% vs plausible effect ≤ 0.39%, ratio 14–73× against a 2× limit). No 2023–2025 death models were run. Other deviations: `download.medicaid.gov` and KFF were blocked, so CMS data came via the data.medicaid.gov API. Adult enrollment is derived as total − child.

## Scorecard (0–10, based on what the data showed)
| Dimension | Score | Why |
|---|---|---|
| Novelty | 8 | No published study links unwinding to deaths (`00_novelty.md`). |
| First stage | 3 | Pre-specified pooled test null. Event study shows Medicaid buprenorphine down 6–9% per SD in 2024–2025, but the pre-trend slopes and quartile dose-response is flat. |
| Power | 1 | MDE is 14–73× the plausible effect. |
| Big result | 1 | None possible with state-year deaths at this effect size. |
| Rigor | 7 | Gates pre-specified and honoured, all decisions logged. Exposure derived (not KFF), ex parte/delay classifications data-driven. |
| Feasibility | 1 | State-level death design cannot detect a buprenorphine-mediated effect. Would need individual-level linked data. |

### 1. What the code did

1. Read CDC VSRR provisional overdose file — 88,182 rows → `deaths_raw`
2. Kept 12-month-ending-December values, 2018–2025, 50 states + DC (NYC summed into NY, PR/US dropped), 4 indicators → `deaths_wide` (408 state-years)
3. Logged incomplete reporting — all-drug deaths complete except AK 2025 (99.5% complete); opioid/synthetic/stimulant counts suppressed in 14–16 state-years in 2018 falling to 2 in 2025 → `deaths_reporting_log`
4. Built population — Census Vintage 2020 (2018–19) + Vintage 2025 (2020–25) → `population` (408 rows)
5. Built unemployment — FRED monthly state rates, annual mean 2018–2025 → `unemployment` (408 rows)
6. Cleaned CMS PI enrollment — updated over preliminary rows, zeros with "unable to provide" set missing; adult = total − child (vs CMS-reported adult in 1,274 state-months: r = 1.00, median ratio 1.00) → `pi_clean`
7. Derived expansion — share of months flagged expanded per state-year → `expansion`, `expansion_date`
8. Built exposure — % drop in adult enrollment Mar 2023 → Jun 2024 (main), Dec 2023, Dec 2024; AZ uses total enrollment; RI Dec 2024 uses Nov 2024; z-scored and quartiled (n = 51; mean drop 19.1%, SD 12.8; range −31.7 NC to 38.6 CO) → `exposure`
9. Built renewal measures from CAA metrics (Mar 2023–Jul 2024) — procedural share (median 0.73), ex parte share (median 0.40), delayed = first termination after Jun 2023 (1 state: OR), heavy ex parte = top quartile (13 states) → `renewals`
10. Built FDA buprenorphine NDC lookup — 523 NDCs, route-based OUD (354) / pain (62) / unknown (107) → `fda_ndc`
11. Read SDUD buprenorphine extract 2018–2025 — 132,832 rows; dropped national XX row and duplicates → 125,909 rows → `sdud`
12. Classified formulations — FDA route, then product name, then units/Rx ≥ 7; OUD 66.7M Rx, pain 0.22M Rx, 194 unclassified rows (all suppressed, 0 Rx) → `sdud`
13. Aggregated OUD buprenorphine to state-quarter — suppressed cells = 0 (upper bound adds 0.6%) → `bup_state_quarter` (1,632 rows, 51 states × 32 quarters)
14. Wrote `clean_data.xlsx` — sheets state_year (408), state (51), state_quarter (1,632), reporting_log, ndc_lookup
15. F1 first stage — Poisson Rx ~ intensity_z × post (2023 Q2+), state + quarter FE, population offset, clustered by state, 2019 Q1–2025 Q4, n = 1,428 → `f1_model_main`
16. F1 event study — intensity_z × year, reference 2022 → `f1_model_event`; Wald pre-trend test 2019–2021
17. F1 robustness — suppressed at upper bound → `f1_model_upper`; without NC/SD (n = 1,372) → `f1_model_no_expanders`; quartiles × post → `f1_model_quartile`
18. P1 placebo models on 2018–2022 deaths (n = 255) — intensity_z × fake 2021 and 2022 terms → `p1_model_years`; pooled 2021–22 → `p1_model_pooled`; MDE = 2.80 × SE → `p1_mde`
19. P1 plausible effect — first stage × mean 2022 state Rx (181,015) × 30/365 × excess mortality (Sordo 2017), ÷ mean 2022 state deaths (2,145) → `p1_plausible`, `p1_breakeven_per_1000py`
20. Gate decision — both gates FALSE → STOP; saved `results.rds`
21. figures_tables.Rmd — exposure dot plot, first-stage trends by quartile, first-stage event study, MDE vs plausible chart → `figures/*.png`, `figures/*.csv`

**Unverified:** The 30-day supply per prescription is an assumption (SDUD has no days supply), chosen to be generous. The excess-mortality inputs come from pre-fentanyl-era cohorts.
**Not run:** Main Poisson death model, death event study, dose-response, 2SLS mechanism, placebo timing 2020/2021, psychostimulant placebo outcome, drop-5-largest, exclusion of delayed/ex parte states, pre-2022 state-trend control. All were stopped by the power gate.

### 2. Methods and Results

**Methods.** We built a panel of 50 states and DC. Adult Medicaid disenrollment intensity was the percentage drop in adult Medicaid enrollment (total minus child Medicaid and CHIP enrollment, CMS Performance Indicator data) from March 2023 to June 2024, standardized across states. Medicaid buprenorphine for opioid use disorder came from the State Drug Utilization Data, 2019–2025: sublingual, buccal-naloxone, and extended-release injectable products, identified through the FDA NDC Directory, with pain formulations excluded and suppressed cells set to zero. The first stage was a state-quarter Poisson model of prescriptions with a population offset, state and quarter fixed effects, and an intensity × post-April-2023 term, with standard errors clustered by state. It passed if that term was negative with p < 0.05. Power was assessed on 2018–2022 CDC provisional overdose deaths (12 months ending December), using placebo intensity × year terms in a state-year Poisson model. The minimum detectable effect (MDE) at 80% power and α = 0.05 was compared with a plausible effect: lost prescriptions × 30 days × excess mortality off versus on buprenorphine (overdose 3.2 and all-cause 5.2 per 1,000 person-years; Sordo et al., BMJ 2017). The stop rule was MDE > 2 × plausible effect. Analyses used R 4.3.3, fixest 0.14.2, and tidyverse 2.0.0.

**Results.** Adult enrollment fell by a mean of 19.1% (SD 12.8) across states. It rose in North Carolina and South Dakota, which expanded Medicaid during unwinding. In the pre-specified first stage (n = 1,428 state-quarters), each 1 SD more disenrollment was associated with 3.2% fewer Medicaid buprenorphine prescriptions after April 2023 (95% CI −10.7% to +4.9%; p = 0.42), so the gate failed. In the event study, the 2023 estimate was +0.1% (−3.3% to +3.5%; p = 0.97). The 2024 estimate was −6.1% (−10.4% to −1.5%; p = 0.009) and the 2025 estimate was −9.4% (−15.0% to −3.3%; p = 0.003). Pre-period coefficients were not jointly different from zero (p = 0.45), but ran from −6.6% in 2019 to −1.4% in 2021. The estimate held with suppressed cells at their upper bound (−3.2%, p = 0.42). It reversed sign without NC and SD (+1.4%, −14.7% to +20.5%; p = 0.87). Disenrollment quartiles 2–4 versus 1 showed no gradient (−6.2%, −0.9%, +6.2%; all p ≥ 0.66). For power (n = 255 state-years), the placebo death terms were −2.6% for 2021 (p = 0.15) and −3.9% for 2022 (p = 0.065), and the smallest MDE was 5.2% per SD (5.6% pooled, 6.3% for 2022). The plausible effect on state overdose deaths was 0.07% per SD (1.5 excess deaths per state-year) with the overdose input and 0.12% with the all-cause input. It was 0.39% even with the first-stage lower confidence bound. The MDE was 73×, 45× and 14× these values, so the gate failed. Reaching half the MDE would require ~117 excess deaths per 1,000 person-years off buprenorphine.

### 3. Recap
- Checked novelty, built a 51-state exposure and Medicaid buprenorphine panel, and ran the pre-specified first-stage and power gates.
- The question is novel, but the pooled first stage was null (a 6–9% drop appeared only in 2024–2025), and the death design is 14–73× underpowered for any buprenorphine-mediated effect.
- Your decision: accept the stop, or override and run the outcome models as an explicitly underpowered reduced form. The clean panel is ready (`clean_data.xlsx`, sheet `state_year`).
