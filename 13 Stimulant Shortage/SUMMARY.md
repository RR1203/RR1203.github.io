**FLAG:** Several inputs could not be downloaded: unemployment (BLS), cannabis legalization dates, and all CDC WONDER outcomes (suicide, injury, and the cancer placebo). After the first results I also added state × season fixed effects to every state-level model. Both are logged in `decisions_log.md`; the original specification is still reported.

### 1. What the code did

1. **Census population:** read the state single-year-of-age files (Vintage 2020 for 2017–2019, Vintage 2025 for 2020–2025), summed over race, and banded ages into 18–44, 45–54, 55–74 and 75+ → `pop_state_year` (51 states × 9 years).
2. **ARCOS:** parsed Report 02 from 9 DEA yearly PDFs (2017–2025) for amphetamine (1100), lisdexamfetamine (1205) and methylphenidate (1724), giving 51 × 36 state-quarters. Quarters sum to the reported totals (max error 0.01 g) → `arcos_state_quarter`.
3. **Daily doses:** converted grams to label-based daily doses (12.5 / 30 / 25 mg, from DailyMed labels, because WHO DDD was unreachable) per 1,000 residents aged 18–44 per day → `supply_state_quarter`.
4. **Expected supply:** fitted a log-linear trend plus season term for each state on 2017Q1–2022Q3 and predicted all quarters → `exp_amph_class`, `exp_amph`, `exp_mph`.
5. **Shortage intensity:** 1 − observed/expected over 2022Q4–2024Q4. Variants: to 2025, amphetamine only, acute phase (2022Q4–2023Q4), and net of methylphenidate substitution → `intensity_state` (n = 51).
6. **FARS:** read accident, person, vehicle, driver-factor and drug files for 2017–2024: 291,174 crashes and 445,556 drivers.
7. **Driver flags:** age band, speeding, driver error (text-label match), BAC ≥ 0.08, and drug results (2018–2024 only: tested, amphetamine-positive without methamphetamine, methamphetamine-positive) → `drivers`.
8. **Crash counts:** aggregated crash-level flags to state × quarter (young, older, oldest, by crash type, drug-positive, pedestrian deaths) → `fars_state_quarter` (1,632 rows).
9. **VMT:** read 108 monthly FHWA Traffic Volume Trends files (Table 5) and summed them to state-quarter VMT. Every quarter had 3 months → `vmt_state_quarter`.
10. **Panel:** merged into a state × quarter panel for 2017Q1–2024Q4, with 0 missing VMT → `panel` (1,632 rows, 51 states).
11. **CDC overdose:** read CDC VSRR provisional overdose deaths and kept the December 12-month-ending values for 2017–2025, giving 459 state-years with 50 states for psychostimulant deaths → `cdc_overdose`.
12. **Clean data:** wrote 7 sheets → `clean_data.xlsx`.
13. **Feasibility:** computed national observed vs expected supply by period, plus the spread of intensity across states → `f_national_gap`.
14. **Expected effect and power:** computed the expected effect and the MDE from pre-2020 placebo models (fake post = 2018Q3) → `e_expected`, `e_mde`. Saved to `expected_effect.md` at 16:00:03 UTC, before any outcome model. Updated the MDE with season FE afterwards → E.3.
15. **Age DiD (A2):** young (18–44) vs older (55–74), excluding 2020–2021, with state×quarter and state×age×season FE. Fitted the DiD, an event study, deaths, and robustness models (COVID dummies, age trend, excluding 2022) → `a2_model_*`.
16. **Dose-response (A3):** Poisson with population offset, state×season and quarter FE, and log VMT. Fitted the DiD, an event study, deaths, a VMT offset, and 10 robustness models → `a3_model_*`.
17. **Triple difference (A4):** intensity × post × young, with state×quarter, state×age×season and quarter×age FE. Fitted the DiD, an event study, deaths, excluding COVID, and excluding 2022 → `a4_model_*`.
18. **Reversal (A5):** split into acute (2022Q4–2023Q4), recovery (2024) and post-quota (2024Q4) phases, for both the dose-response and triple-difference designs → `a5_model_*`.
19. **Mechanism (A6):** dose-response by crash type (7 types), drug-positive drivers (4 models; 2018–2024; 1,423 state-quarters with a tested young driver), and age DiD by crash type (4 models) → `a6_model_*`.
20. **Secondary (S1):** state-year dose-response for psychostimulant overdose, all overdose and all-cause deaths → `s1_model_*`.
21. **Placebos (P):** driver 75+, driver 55–74 and pedestrian-death outcomes, plus placebo dates 2019Q4 (sample 2017Q1–2020Q1) and 2021Q4 (sample 2020Q1–2022Q3), each for the dose-response and age designs → `p_model_*`.
22. **Excess crashes and deaths (X):** observed × (1 − e^(−β·intensity)) summed over the 9 post quarters, from the dose-response and triple-difference models → `x_excess`.
23. **Figures:** 5 figures plus the mechanism table → `figures/` (`figures_tables.Rmd`).

**Not run:**
- unemployment control (BLS blocked)
- cannabis control and the exclusion of states that legalized in 2022–2024 (sources blocked)
- CDC WONDER suicide, unintentional injury and cancer at ages 18–44 (blocked)
- age-specific overdose (the VSRR file is all ages)
- Medicaid SDUD second exposure (skipped)
- FARS 2025 (not yet published)

**Unverified:**
- whether ARCOS grams for 1205 and 1724 are base or salt weight
- whether the FARS 2024 file is final or the annual-report version

---

### 2. Methods and Results

**Methods.**
- *Design:* the 2022 US amphetamine shortage was treated as a natural experiment.
- *Exposure:* quarterly retail distribution of amphetamine and lisdexamfetamine from DEA ARCOS (2017–2025), converted to label-based daily doses per 1,000 residents aged 18–44.
- *Shortage intensity:* each state's shortfall versus its own 2017Q1–2022Q3 log-linear trend with seasonality, over 2022Q4–2024Q4.
- *Outcomes:* from NHTSA FARS 2017–2024, the primary outcome was the number of fatal crashes involving at least one driver aged 18–44 per state-quarter. Deaths in those crashes were a secondary outcome.
- *Main design:* Poisson regression of crashes on intensity (per 10 percentage points) × post (2022Q4 onward), with a log population offset, state × season and quarter fixed effects, log vehicle-miles traveled (FHWA), and standard errors clustered by state (51 clusters).
- *Additional designs:*
  - an age comparison of drivers 18–44 vs 55–74, excluding 2020–2021, with state × quarter fixed effects
  - a triple difference (intensity × post × young) with state × quarter, state × age × season and quarter × age fixed effects
  - event-study versions of all three
- *Checks:* reversal by phase; mechanism outcomes (crash type and driver drug-test results, 2018–2024); secondary overdose outcomes (CDC VSRR, state-year, all ages); placebo outcomes and placebo dates.
- *Expected effect and power:* the expected effect (share on stimulants × supply drop × 38–58%) and the minimum detectable effect (2.80 × SE from pre-2020 placebo models) were recorded before outcome models were fitted.
- *Specification change:* state × season fixed effects were added after initial results showed a seasonal artifact; the original specification is reported as a robustness check.
- *Controls not available:* unemployment and cannabis legalization could not be retrieved. The age and triple-difference designs absorb them through state × quarter fixed effects.
- *Software:* R 4.3.3, fixest 0.14.2, tidyverse 2.0.0.

**Results.**

*Supply.*
- National amphetamine-class supply fell below trend by 5.4% in 2022Q4 and by 9.3% in 2023Q1. Over the acute phase (2022Q4–2023Q4) it averaged 5.65% below trend; over 2022Q4–2024Q4, 3.22% below.
- By 2024Q2 supply was at or above trend; in 2025 it was 1.9% above.
- State intensity ranged from −19.5% (SD) to +14.3% (FL): mean +1.0%, SD 6.2 pp, coefficient of variation 6.5.

*Expected effect and power.*
- The upper-bound daily share of 18–44-year-olds on an amphetamine-class stimulant was 5.66%.
- The expected rise in young-driver fatal crashes was 0.07–0.44%, or 38–237 crashes over 2022Q4–2024Q4.
- The minimum detectable effect was 3.6% for the age design and 4.7% for the dose-response design (87.5th vs 12.5th percentile state); with season FE, 4.0% per 10 pp.

*Primary result.*
- There were 53,968 young-driver fatal crashes and 59,426 deaths in the post period.
- In the dose-response model, each 10 pp of shortfall was associated with a rate ratio of 0.980 (95% CI 0.934–1.029; p = 0.42). For deaths: 0.983 (0.933–1.036).
- The triple difference gave 1.011 (0.972–1.051; p = 0.60). For deaths: 1.010 (0.970–1.052).
- These imply 215 excess young-driver crashes (95% CI −597 to 987) and 236 excess deaths (−657 to 1,085) from the triple difference. The dose-response model implies −417 crashes (−1,467 to 572) and −458 deaths (−1,614 to 629).

*Age comparison.*
- Young-driver crashes rose relative to older drivers after 2022Q4: rate ratio 1.036 (1.014–1.058; p = 0.001). For deaths: 1.038 (1.015–1.062).
- This difference disappeared with an age-specific linear trend: 0.991 (0.956–1.027).
- The event study showed the young–older gap was already at its post-shortage level in 2022Q1–Q3, and below it in 2017–2019 (leads jointly p = 1.1 × 10⁻⁵).
- The 2021Q4 placebo date was significant: 0.952 (0.925–0.980).
- The pre-period placebo was also significant: 0.973 (p = 0.03).

*Robustness of the dose-response estimate.* The estimate stayed null across:
- net-of-methylphenidate intensity: 0.983 (0.947–1.020)
- amphetamine-only intensity: 0.988 (0.947–1.030)
- acute-phase intensity: 0.982 (0.930–1.037)
- excluding 2020–2021: 0.987 (0.942–1.034)
- excluding 2022: 0.982 (0.930–1.037)
- time-varying gap: 0.981 (0.940–1.024)
- excluding FL and TX: 1.022 (0.986–1.060)
- VMT offset: 0.986 (0.945–1.029)
- no season FE: 0.974 (0.921–1.029)
- The exception was state linear trends, which gave a protective-direction 0.943 (0.908–0.978).

*Event studies.* The dose-response and triple-difference event studies showed no rise at 2022Q4. Leads versus the 2021Q4–2022Q3 reference were jointly non-zero:
- dose-response: p = 0.005 (2017–2019) and p = 6 × 10⁻⁴ (2020–2021)
- triple difference: p = 2.6 × 10⁻⁷ and p = 0.04

*Reversal.* Effects did not differ by phase:
- dose-response: acute 0.985 (0.938–1.033), recovery 0.979 (0.917–1.045); joint p = 0.81
- triple difference: acute 1.013 (0.982–1.045), recovery 1.019 (0.947–1.097)
- post-quota quarter: 1.007 (0.972–1.042)

*Mechanisms (dose-response per 10 pp).*
- Single-vehicle 0.989 (0.935–1.046); multi-vehicle 0.973 (0.926–1.022); daytime 0.979 (0.945–1.014); night 0.976 (0.918–1.037).
- Driver error 0.998 (0.911–1.093); speeding 1.052 (0.987–1.121); BAC ≥ 0.08 0.910 (0.807–1.025).
- Among tested crashes, amphetamine-positive (methamphetamine-negative) young drivers fell nationally after 2022Q4: 0.866 (0.755–0.991; p = 0.04). They fell more in harder-hit states: 0.818 per 10 pp (0.663–1.010; p = 0.06).
- Methamphetamine-positive drivers fell nationally, 0.746 (0.671–0.828), with no dose-response: 1.022 (0.909–1.148).
- In the age design, daytime crashes rose relative to older drivers, 1.030 (1.005–1.056). Single-vehicle (1.009), driver-error (1.030) and speeding (1.024) crashes did not differ significantly.

*Secondary outcomes (per 10 pp).*
- Psychostimulant overdose deaths 1.10 (0.97–1.25; p = 0.13)
- all overdose deaths 1.08 (0.89–1.31)
- all-cause deaths 0.990 (0.975–1.006)

*Placebos.*
- Crashes with drivers aged 75+: 0.946 (0.895–1.000; p = 0.049).
- Crashes with drivers aged 55–74: 0.970 (0.940–1.000; p = 0.053).
- Pedestrian deaths in older-driver crashes: 0.993 (0.926–1.066).
- Placebo dates for the dose-response design were null: 2019Q4 1.028 (0.991–1.065); 2021Q4 1.020 (0.952–1.092).

---

### 3. Recap

- **What was done:** tested whether the 2022–2024 amphetamine shortage raised fatal crashes with drivers aged 18–44, using a state dose-response design (ARCOS supply loss), an age comparison and a triple difference on FARS 2017–2024.
- **What was found:** no detectable crash harm. The best estimate (triple difference) is +215 excess crashes and +236 deaths nationally (95% CI −657 to +1,085 deaths). That matches the pre-registered expected effect (38–237 crashes), but the study had power only for effects 10–50 times larger. The national supply drop was small (5.7% in the acute phase), and a raw +3.6% young-vs-older rise is explained by a trend that predates the shortage. Amphetamine-positive crash drivers fell in harder-hit states, which suggests exposure did shift.
- **Decision needed:** write this up as a well-powered-for-large-effects null with a "first-stage" drug-test finding, or add individual-level exposure (Medicaid SDUD or claims) for a better-powered test.
