# Decisions log

Run date: 2026-11-13 (overnight, no questions asked). Each entry: what was unclear or blocked → what I did.

## Data access
- **FARS:** 2017–2024 national CSVs downloaded from static.nhtsa.gov. 2025 not posted (404), so no early-release data. The 2024 file is the version NHTSA currently posts; I did not verify whether it is the final or the annual-report file.
- **ARCOS:** DEA Retail Drug Summary yearly PDFs 2017–2025 (`raw/arcos/`). Converted with `pdftotext -layout` and parsed Report 02 (grams by state × quarter × drug). The quarters sum to the reported totals (max error 0.01 g). ARCOS drug codes used: 1100 amphetamine (d- and l- combined; ARCOS does not split them), 1205 lisdexamfetamine, 1724 methylphenidate. Code 1724 includes dexmethylphenidate ("DL; D; L isomers"), so there is no separate dexmethylphenidate series.
- **WHO ATC/DDD:** host blocked by the network policy. DDDs were not available, so I used **label-based reference daily doses** from FDA labels on DailyMed (`raw/other/dailymed/`):
  - amphetamine 12.5 mg base (Adderall XR adult recommended 20 mg/day = 12.5 mg total amphetamine base, from the label table)
  - lisdexamfetamine 30 mg (Vyvanse adult starting dose)
  - methylphenidate 25 mg (Ritalin adult "average 20 to 30 mg daily", midpoint)
  - These constants only scale the series and weight amphetamine vs lisdexamfetamine within the "amphetamine class". The single-drug intensity (1100 only) is unit-free and gives the same answer.
  - ARCOS gram units (base vs salt) for 1205 and 1724 are not stated in the reports.
- **Population:** Census state single-year-of-age files: Vintage 2020 for 2017–2019 and Vintage 2025 for 2020–2025. Summed over race. Mixing vintages creates a small break at 2020, which year/quarter fixed effects absorb.
- **BLS LAUS (unemployment):** download.bls.gov and api.bls.gov refused automated requests (403/blocked). I did not try to get around this. **No unemployment control.** Mitigation: the age-comparison and triple-difference models include state × quarter fixed effects, which absorb every state-level economic shock.
- **Cannabis legalization dates:** every source I tried (NCSL, Wikipedia, NIAAA APIS, PDAPS) was blocked. **No cannabis control, and the planned exclusion of states that legalized in 2022–2024 was not possible.** Same mitigation (state × quarter FE in the age and triple-difference designs).
- **FHWA VMT:** monthly Traffic Volume Trends spreadsheets 2017-01 to 2025-12, Table 5 ("ALL roads by state"), current-month preliminary vehicle-miles, summed to quarters.
- **CDC WONDER:** blocked (403). **Not available: suicide, all unintentional-injury deaths, and cancer deaths at ages 18–44 (the cancer placebo).** Replacement: the CDC VSRR provisional overdose file on data.cdc.gov (state × month, 12-month-ending counts). I used the December value as the calendar-year count. It covers all ages only (no age 18–44 split) and is suppressed in some state-years (4 missing in 2022–2024).
- **Medicaid SDUD (optional second exposure):** skipped for time.
- **DEA quota documents:** Federal Register API for the document list; the text came from govinfo.gov because federalregister.gov full text redirected to a bot check. Key documents:
  - 2023-22059: methylphenidate APQ increase, effective 2023-10-03
  - 2024-20114: lisdexamfetamine and d-amphetamine (for conversion) APQ increase, effective **2024-09-05**; lisdexamfetamine APQ +6,236 kg
  - 2025-18110 and 2025-19335: further lisdexamfetamine, d-amphetamine (for sale) and methylphenidate increases, effective 2025-09-19 and 2025-10-02
  - 2026-22842: d,l-amphetamine increase, effective 2026-11-10

## Definitions
- **Shortage start:** 2022Q4.
- **Recovery date:** first amphetamine-class quota increase, effective 2024-09-05, so 2024Q4 is the first post-quota quarter. ARCOS itself shows national supply back at or above trend from 2024Q2.
  - Because FARS ends in 2024Q4, the reversal test has only 4 "recovery" quarters (2024) and 1 post-quota quarter. It is weak by design.
- **Shortage intensity:**
  - Fit one log-linear trend plus quarter-of-year seasonality per state on 2017Q1–2022Q3. Intensity = 1 − Σobserved/Σexpected over 2022Q4–2024Q4 (the outcome window).
  - Variants: to 2025Q4; amphetamine (1100) only; acute phase 2022Q4–2023Q4; net of methylphenidate (the methylphenidate surplus above its own trend is subtracted, in reference-daily-dose units).
  - All ARCOS doses are divided by residents aged 18–44 as the brief asked, even though ARCOS covers all ages.
- **CV rule:** the CV is 6.5, but only because the mean intensity is close to 0 (+1%). The spread is real: SD 6.2 pp, range −19.5% (SD) to +14.3% (FL). I did not switch to age-only, and ran the dose-response as the main design.
- **Primary outcome:** fatal crashes involving ≥1 driver aged 18–44 (PER_TYP = driver), assigned to crash state and quarter (from MONTH). Deaths = FATALS in those crashes. Older comparison: ≥1 driver aged 55–74. Placebo: ≥1 driver aged 75+.
- **Driver error:** any driver-related factor whose text label matches a driving-behaviour pattern (careless, yield, lane, erratic/reckless, obey, overcorrect, wrong side, following, aggressive, racing, speed, improper, passing, turning, fail).
  - Source: vehicle DR_SF1–4 for 2017–2019 and driverrf.csv for 2020–2024 (format change in 2020, absorbed by time FE).
  - I used the NAME label columns that FARS ships, not code numbers from memory.
- **Speeding:** SPEEDREL coded "Yes" (racing, exceeded the limit, too fast for conditions, specifics unknown).
- **Daytime:** HOUR 6–17.
- **Single-vehicle:** VE_FORMS = 1.
- **Drug tests:** only the drugs.csv file, which exists from 2018 (2017 has no drugs file), so drug models cover 2018–2024.
  - "Amphetamine+" = amphetamine, amphetamine sulfate, dextroamphetamine or lisdexamfetamine AND not methamphetamine-positive. This is because amphetamine is a metabolite of methamphetamine.
  - Tested = any result other than not given, unknown or not reported.
  - Modeled per crash with a tested young driver (log offset), within state.
- **Pedestrian placebo:** pedestrians killed in crashes with a 55–74 driver and no 18–44 driver.
- **COVID:** the age comparison drops 2020–2021 (main) or adds young × COVID-year dummies (robustness). The state designs keep all quarters with quarter FE; dropping 2020–2021 is a robustness check.

## Post-hoc changes (made after seeing first results; reported both ways)
1. **State × quarter-of-year fixed effects added to all state-level models.**
   - The first event study showed a strong seasonal saw-tooth: Q1 coefficients high, Q3 low, relative to a 2022Q3 reference.
   - Cause: high-intensity states (FL, TX, AZ, CA) have different crash seasonality from northern states. This is a specification error, not a finding.
   - Primary estimates now use state^quarter-of-year + quarter FE. The original state + quarter FE model is kept as robustness `a3_model_noseason`.
   - Point estimates barely moved: −2.6% → −2.0% per 10 pp.
   - Event studies now use one reference quarter per season (2021Q4–2022Q3; for the age model, 2019Q4 + 2022Q1–Q3, because 2020–2021 are excluded). Seasonal FE absorb one level per season, which makes a single reference quarter not identified.
2. **Placebo date 2019Q4 sample** changed from 2017Q1–2020Q3 to 2017Q1–2020Q1. The first version put the 2020 lockdown quarters inside the "post" period.
3. **Expected effect and power** (`expected_effect.md`, timestamp 2026-11-13 16:00:03 UTC) were written before any post-2019 crash model was run and were not changed. Block E.3 adds an updated MDE using the seasonal-FE specification, labelled as added later.

## Style
- House style is followed (one cleaning section that writes `clean_data.xlsx`, self-contained blocks, banner comments, every output wrapped in `print()`). Three deviations:
  - `map()` is used in data cleaning, to read files whose columns differ across years. It is not used for models, except one `map_dbl` to extract coefficients for the mechanism figure.
  - The brief asked for `analysis.Rmd` plus `figures/`. Following the house style, figures live in a separate `figures_tables.Rmd`, which refits the models and saves the PNGs.
  - No Holm correction was pre-specified. Mechanism and placebo p-values are unadjusted and should be read as exploratory.
