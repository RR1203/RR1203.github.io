**FLAG:** The positive control failed on the pre-specified window. Scotland 2007–2024 gave +1.6% (95% CI −10.0 to +14.6), against a published −13.4% (−18.4 to −8.3). A placebo test showed the 2007 pre-trend was misspecified (fake 2016 policy: +14.5%, p=0.005). All windows were therefore moved to start in 2012. This is a post-hoc change; see DECISIONS.md.
**FLAG:** After the fix, the gate passes only on the Wyper-matched window (2012–2020: −11.8%). On the extended primary window (2012–2024), Scotland's point estimate of −6.5% lies outside the published CI.
**FLAG:** Q2: the −13.0% monthly step at 65p cannot be attributed to the uprating. The same model puts a −11.3% step at a fake January 2024 date, and England's rate also fell 8.0% in 2024. England 2025 deaths are not yet published.
**FLAG:** Deviations from the brief:
- Wales admissions were unavailable (source failed twice).
- Welsh first-stage page references are [REF NEEDED].
- The Irish outcome is a 5-code proxy that covers 96–97% of UK alcohol-specific deaths.
- The NT floor price was repealed on 1 Mar 2025, so NT data stop at 2024.
- Placebo, leave-one-out and synthetic-control loops use `group_modify()`, which departs from house style.

**Positive control (Scotland 2018 vs England)**

| Specification | Effect (95% CI) |
|---|---|
| Wyper-matched window 2012–2020 | **−11.8% (−21.4 to −0.9), p=0.038, n=9 years.** Inside published CI; gate passes |
| Primary 2012–2024 | −6.5% (−21.5 to +11.3), p=0.41, n=13 |
| Trend fitted on pre-policy years only | −20.7% (−28.9 to −11.7) |
| Demeaned synthetic control | −17.7% (placebo rank p=0.18) |

**Scorecard (0–10)**

| Question | Novelty | First stage | Power | Big result | Rigor | Feasibility |
|---|---|---|---|---|---|---|
| Q1 Wales: deaths | 8 | 5 | 3 | 2 | 6 | 8 |
| Q1 Ireland: deaths | 9 | 3 | 2 | 2 | 3 | 7 |
| Q2 Scotland 65p | 10 | 6 | 5 | 2 | 3 | 4 now; 8 once England 2025 data are out (~May 2027) |
| Q3 Deprivation | 3 | 5 | 2 | 1 | 4 | 6 |

### 1. What the code did

1. Downloaded raw sources into `raw/`:
   - ONS alcohol-specific deaths, 2024 release
   - NRS alcohol-specific deaths 2025 and vital events chapter 6
   - CSO PxStat tables VSA35, VSA29, PEA01, MORT02, ASD01, ASD09
   - ABS Causes of Death 2025 Table 13.17
   - Fingertips indicators 92906, 91380, 93959, 94004
   - PHS ARHS and MESAS 2022 workbooks, plus the PHS 2026 report
2. Harvested these into one workbook with values unchanged (`scripts/01_harvest_raw.py`) → `03_mup_raw.xlsx` (24 sheets).
3. Built the Irish age-standardised rates (ASMR):
   - Deaths by 3-character ICD and age, 2007–2024; CSO nulls recoded to 0.
   - ASMR from ESP2013 weights and PEA01 population (×1000).
   - Outcomes: alcohol-specific proxy (F10+K70+X45+X65+Y15), K70, non-alcohol cancers (C00–C97 excluding C00–C15, C18–C22, C32, C50), all cancers, C15.
   - → `ireland`
4. Validated the ESP2013 weights: computed Irish cancer ASMR against CSO's published MORT02 gives a ratio of 0.991–1.016 (n=30) → `ireland_validation`.
5. Checked proxy coverage: the 5 codes cover 96.0–97.3% of UK alcohol-specific deaths in every year 2001–2024 (ONS Table 9).
6. Computed Scotland's cancer ASMR from NRS broad-age rates with collapsed ESP2013 weights.
   - Persons = mean of male and female rates, same rule as England → `scotland_cancer`, `cancer_persons`.
7. Combined North East + North West England as a ratio of sums, using deaths/ASMR as the standardised-population proxy → `ons_ne_nw`.
8. Collapsed England IMD2019 deciles to quintiles by averaging decile pairs (4/23 geography, 2006–2024) → `deprivation` (n=220).
9. Wrote `clean_data.xlsx` with 10 sheets:

   | Sheet | Rows |
   |---|---|
   | `panel` | 1,604 |
   | `scotland_monthly` | 312 |
   | `deprivation` | 220 |
   | `admissions` | 71 |
   | `sales_uk` | 56 |
   | `price_bands` | 150 |
   | `sales_ireland` | 32 |
   | `phs_2026_report` | 9 |
   | `australia` | 80 |
   | `ireland_validation` | 30 |

10. H0 positive control:
    - Model: CITS of log(Scotland/England ASMR) on a linear trend, a fraction-of-year MUP term (2018 = 8/12) and a 2020–21 COVID term, with Newey–West SE (lag 1).
    - Run on the Wyper window 2012–2020 (n=9, no COVID term) and on 2007–2024 (n=18) → `h0_gate`.
11. The gate failed on 2007–2024. Placebo 2016: +14.5%, p=0.005 on the 2007 window, +3.5%, p=0.26 on a 2012 window. Window start moved to 2012 for every analysis.
12. H0 robustness (2012–2024, n=13):
    - excluding 2020–21
    - placebo 2016
    - NE+NW control
    - by sex
    - placebo-in-space over 9 English regions
    - trend fitted on pre-policy years only
    - original 2007 window
    - demeaned synthetic control (10 donors, fitted 2012–2017), leave-one-donor-out, and RMSPE-ratio placebo
13. H1 first stage:
    - share of off-trade volume sold below 50p and below 65p, 2017–2021
    - Scotland vs England & Wales per-adult sales, CITS 2012–2021 (n=10)
    - PHS 2026 price-per-unit values (report pp. 3, 5)
    - Ireland per-capita sales ITS 2012–2025 (n=14), plus excluding COVID and a 2007 start
14. H2 power: MDE from the pre-period residual SD and the design-based SE of the MUP term → `h2_power`.
15. H3 Wales vs England:
    - primary model, 2012–2024, n=13, 2020 = 10/12 exposed
    - excluding 2020–21; placebo 2018; NE+NW control; by sex; 2007 window; trend from pre-policy years only
    - demeaned synthetic control with leave-one-donor-out and placebo
16. H4 Ireland:
    - primary vs Northern Ireland and vs England (2012–2024, n=13)
    - K70 vs NI; excluding 2020–21; placebo 2020; 2007 window; trend from pre-policy years only; by sex
17. H5 pooling: REML random-effects meta-analysis of the Scotland, Wales and Ireland (vs NI) primary log effects; also Wales + Ireland only, and fixed-effect → `h5_model_pooled`.
18. H6 Q2 (65p):
    - monthly ITS May 2018–Dec 2025 (n=92; 15 months after 65p): trend, month-of-year, COVID Mar 2020–Dec 2021, step at Oct 2024
    - MDE for that step
    - annual CITS vs England with 50p and 65p terms (2024 = 3/12 exposed)
    - long series 2012–2025 (n=168); COVID months excluded (n=70)
    - placebo steps at Oct 2022 (n=77) and Jan 2024 (data to Sep 2024)
    - year-on-year change table
19. H7 Q3: CITS per deprivation quintile (Scotland SIMD vs England IMD, 2012–2024, n=13 each), fixed-effect meta-regression of effect on quintile, Q1 and Q5 excluding COVID years. Wales WIMD: printed the year range only.
20. S1 negative and partly attributable controls:
    - Scotland all-cancer vs England
    - Ireland non-alcohol cancers vs England all-cancer
    - oesophageal cancer, Scotland and Ireland (own-trend ITS)
21. S2 admissions:
    - Scotland ARHS SMR01 vs England Fingertips 92906 (financial years 2016/17–2023/24, n=8, no trend term)
    - Ireland HIPE crude rate vs England (n=8)
    - own-trend ITS for Scotland (n=12) and Ireland (n=13)
22. S3 Northern Territory: log(NT ÷ other states' deaths) 2016–2024 (n=9; 2018 = 3/12 exposed), plus placebo-in-space over 8 states.
23. Saved `results.rds`. Wrote 6 figures to `figures/` via `figures_tables.Rmd`.

**Unverified:**
- Welsh Government evaluation purchase/price numbers and page references (gov.wales PDFs not retrieved).
- Ireland's commencement order number.
- NT dates (verified from peer-reviewed papers, not from nt.gov.au).

**Not run:**
- Wales admissions and Wales deprivation models (no pre-period data).
- Age-specific controlled estimates (England has no age-specific rates by nation).
- Synthetic control for Ireland (outside donors' convex hull).
- Wales negative control.
- Q2 admissions (ARHS ends 2023/24).

### 2. Methods and Results

**Methods.** We studied the introduction of minimum unit pricing (MUP) in Scotland (1 May 2018, 50p), Wales (2 Mar 2020, 50p) and Ireland (4 Jan 2022, €1.00 per 10 g). Northern Territory (NT; 1 Oct 2018, A$1.30) was a secondary, confounded case. We also studied Scotland's uprating to 65p (30 Sep 2024).

- **Outcome:** annual age-standardised (ESP2013) alcohol-specific mortality by year of registration (ONS 2024 release; NRS for Scotland 2025).
- **Ireland:** we computed rates from CSO deaths occurring by 3-character ICD-10 code, using F10, K70, X45, X65 and Y15. These codes accounted for 96–97% of UK alcohol-specific deaths in every year.
- **Main design:** a controlled interrupted time series (CITS) on the log rate ratio of the treated jurisdiction to its control. Controls were England for Scotland and Wales, and Northern Ireland (then England) for Ireland. The model had a linear trend, a level-change term equal to the fraction of each year under MUP, and a 2020–21 COVID indicator. We used Newey–West standard errors (lag 1) and t-based 95% confidence intervals over 2012–2024.
- **Window:** 2012 replaced a pre-specified 2007 start after the 2007 pre-trend failed a placebo test.
- **Robustness:**
  - demeaned synthetic control (donors: 9 English regions and Northern Ireland), with leave-one-donor-out and RMSPE-ratio placebo inference
  - placebo-in-space and placebo dates 2 years early
  - a North East + North West England control
  - exclusion of 2020–21
  - sex-specific models
  - a model with the trend estimated from pre-policy years only
- **Pooling:** effects were pooled by REML random-effects meta-analysis.
- **Dose (Q2):** a monthly interrupted time series of Scottish rates from May 2018 to Dec 2025, with month-of-year and COVID terms and a step at Oct 2024.
- **Deprivation (Q3):** CITS by quintile (SIMD vs IMD2019).
- **Power:** minimum detectable effects (80% power, α=0.05) from pre-period residual variance.
- **Software:** R 4.3.3, with sandwich 3.1.0, metafor 4.4.0, quadprog 1.5.8 and tidyverse 2.0.0.

**Results.**

*Positive control.* With the published window (2012–2020), Scotland's alcohol-specific mortality changed by −11.8% (95% CI −21.4 to −0.9; p=0.038; n=9 years), against a published −13.4% (−18.4 to −8.3). Over 2012–2024 (n=13) the estimate was:
- −6.5% (−21.5 to +11.3; p=0.41) in the primary model
- −20.7% (−28.9 to −11.7) with the trend fitted on pre-policy years only
- −17.7% with demeaned synthetic control (leave-one-out range −18.0 to −14.4; placebo rank p=0.18)
- placebo checks: placebo 2016 +3.5% (−4.3 to +11.9; p=0.26); placebo-in-space p=0.22

By sex, the effect was −16.1% in males (−27.7 to −2.5) and +14.0% in females (−8.5 to +42.1). With the North East + North West control it was −5.5% (−19.8 to +11.3).

*First stage.*
- **Scotland:** the share of off-trade alcohol sold below 50p fell from 45.1% (2017) to 6.7% (2019), against 43.5% to 38.0% in England & Wales. Per-adult sales fell by 4.4% relative to England & Wales (−5.1 to −3.7; n=10).
- **Scotland 65p:** average off-trade price per unit rose from 72p to 78p between 2024 and 2025, against 67p to 69p in England & Wales (PHS 2026, p. 5).
- **Ireland:** per-capita sales were 7.6% below trend (−15.0 to +0.5; p=0.062; n=14). With a 2007 start the estimate was −2.8% (−10.8 to +5.9).

*Power.* Minimum detectable effects, against the ~13% benchmark:

| Jurisdiction | MDE | Status |
|---|---|---|
| Scotland | 12.4% | powered |
| Wales | 21.8% | underpowered |
| Ireland (vs NI) | 31.4% | underpowered |

*Q1, Wales.* The change was +2.8% (−13.2 to +21.7; p=0.72; n=13). Every robustness check stayed between −3% and +4%:

| Check | Effect (95% CI) |
|---|---|
| Excluding 2020–21 | +2.7% (−11.0 to +18.5) |
| NE+NW control | +2.2% (−16.7 to +25.3) |
| Demeaned synthetic control | −3.0% (placebo rank p=0.82) |
| Trend from pre-policy years only | +1.3% (−10.8 to +15.0) |
| Placebo 2018 | +2.9% (−9.6 to +17.1) |

*Q1, Ireland.* The answer depended on the control:
- vs Northern Ireland: +39.6% (+7.8 to +80.7; p=0.017)
- vs England: −0.4% (−24.8 to +31.9; p=0.98)
- K70 vs NI: +50.3% (+15.5 to +95.6)
- placebo 2020: +14.4% (−2.4 to +34.0; p=0.085)
- 2007 window: +20.0% (+1.5 to +42.0)

*Pooled.* The random-effects estimate across Scotland, Wales and Ireland was +8.8% (−13.0 to +36.0; p=0.46; I²=81%; Q-test p=0.014). Wales and Ireland alone gave +18.3% (−12.3 to +59.6).

*Q2, Scotland 65p.* Scottish monthly rates showed a −13.0% step at Oct 2024 (−20.2 to −5.2; p=0.002; n=92; MDE 11.9%):
- long series: −12.2%
- excluding COVID months: −13.0%
- placebo Oct 2022: +0.6% (−11.5 to +14.4)
- placebo Jan 2024: −11.3% (−17.4 to −4.7; p=0.001)
- annual alcohol-specific rate, Scotland: −7.5% from 2023 to 2024, then −3.3% from 2024 to 2025
- annual alcohol-specific rate, England: −8.0% from 2023 to 2024
- annual CITS vs England (3 post months): −16.9% (−46.0 to +27.8; p=0.35)

*Q3, deprivation.* Effects by quintile, most to least deprived:

| Quintile | Effect (95% CI) |
|---|---|
| 1 (most deprived) | −6.5% (−20.2 to +9.6) |
| 2 | −3.7% (−20.2 to +16.3) |
| 3 | +2.1% (−16.4 to +24.8) |
| 4 | −5.2% (−34.6 to +37.5) |
| 5 (least deprived) | −9.2% (−17.7 to +0.3) |

There was no gradient (slope p=0.79).

*Negative and partly attributable controls.*
- Scotland all-cancer: +1.6% (−0.5 to +3.8)
- Ireland non-alcohol cancers: +1.0% (−1.9 to +4.1)
- Scotland oesophageal cancer: +3.6% (−2.9 to +10.5)
- Ireland oesophageal cancer, own trend: −8.6% (−14.5 to −2.2)

*Admissions.*
- Scotland vs England: −18.9% (−29.7 to −6.5; n=8; 2 pre-years). Scotland's own-trend ITS: +5.4% (−10.8 to +24.5).
- Ireland vs England: −14.8% (−29.6 to +3.1). Ireland's own-trend ITS: −15.8% (−25.2 to −5.1).

*NT.* Alcohol-induced deaths changed by −46.1% (−58.7 to −29.8; n=9) relative to the other states (placebo-in-space p=0.125). Co-policies (Banned Drinker Register, Police Auxiliary Liquor Inspectors) began at the same time.

### 3. Recap

- Built a harmonised panel of alcohol-specific deaths for 4 jurisdictions and ran CITS, synthetic control, a 65p monthly time series and deprivation splits. The pre-specified window failed the positive-control gate; moving to 2012 passed it on the published window.
- Scotland's effect reproduced on the published window (−11.8%) but is sensitive to specification. Wales showed no detectable effect (+2.8%, underpowered, MDE 22%). Ireland's estimate depends on the control (NI +40%, England −0.4%; MDE 31%) and is uninformative. The 65p decline started before the uprating (placebo −11%). No detectable deprivation gradient (underpowered).
- Next: rerun Q2 with ONS England 2025 deaths (~May 2027). Get Welsh first-stage page references from gov.wales. Decide whether the Ireland result goes in the paper only as an underpowered, control-sensitive null.
