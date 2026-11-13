# Decisions log

Choices made without asking, in the order they came up. Run date: 2026-11-13.

## Environment and data access
1. **Network.** The default cloud environment blocked every data host. I moved the session to the repository's saved environment and added the hosts NHTSA, DEA, Census, BLS, CDC, FHWA, Federal Register/GovInfo, FRED, Wikipedia and WHO ATC/DDD (each approved in the app).
2. **R.** R wasn't installed, so I installed R 4.3.3 from Ubuntu packages, plus `fixest` from CRAN.
3. **BLS unemployment.** download.bls.gov rejects scripted clients without contact details, and I didn't send a spoofed browser identity or your email. I used the same BLS LAUS series (`<ST>UR`, seasonally adjusted, monthly) via FRED instead.
4. **CDC WONDER was not used.** Its API requires accepting a data-use agreement, which is yours to accept, so I didn't accept it for you. As substitutes I used three public data.cdc.gov files:
   - "Mapping Injury, Overdose, and Violence – State" (suicide and drug overdose, state × year 2019–2024, **all ages**).
   - "VSRR Provisional Drug Overdose Death Counts" (psychostimulant T43.6, 12-month-ending December values, state × year 2017–2025, **all ages**).
   - "VSRR Quarterly provisional estimates" was downloaded, but it only covers 2023Q1–2025Q3. With no pre-period it wasn't used for inference.

   **Not done:** outcomes restricted to ages 18–44, all unintentional-injury deaths by state, and cancer deaths in ages 18–44 (placebo). All of these need WONDER.
5. **Cannabis dates.** The official NIAAA APIS site returned 403 (bot block). I used the effective dates from the Wikipedia table "Legalization of non-medical cannabis in the United States" (saved in `raw/cannabis/`). This source is secondary.
6. **Medicaid SDUD** (optional second exposure) was not downloaded, for time and scope reasons.
7. **FARS early-release 2025** is not published as person-level files (the 2025 national CSV returned 404). FARS ends at 2024Q4. The 2024 file is used as downloaded on 2026-11-13 and may be the Annual Report File rather than the Final file.

## Exposure (ARCOS)
8. **Source.** ARCOS Retail Drug Summary, Report 2 (grams by state × quarter × drug code), 2017–2025. It was parsed from the PDFs with `scripts/parse_arcos.py`. Quarter sums match the reported totals within 0.02 g.
9. **Drug codes.** 1100 amphetamine (d-, l-, dl- salts), 1205 lisdexamfetamine, 1724 methylphenidate. DEA code 1724 covers all methylphenidate isomers, so dexmethylphenidate is included and was not separated.
10. **Defined daily doses.** WHO ATC/DDD index, downloaded: amfetamine 15 mg, lisdexamfetamine 30 mg, methylphenidate 30 mg. I applied the methylphenidate DDD to dexmethylphenidate as well (the WHO dexmethylphenidate DDD is 15 mg), which understates dexmethylphenidate DDDs. ARCOS grams were treated as reported.
11. **Denominator.** DDD per 1,000 residents aged 18–44 per day, as specified. ARCOS covers all ages, so this is a supply intensity, not an adult-use rate.
12. **Expected supply.** Each state's own linear trend plus quarter-of-year dummies, fitted on 2017Q1–2022Q3.
13. **Shortage window changed from "Q4 2022–latest".** In ARCOS, national amphetamine-class supply was below trend only from 2022Q4 to 2023Q4:
    - 4.4%, 7.4%, 1.4%, 2.7% and 3.6% below trend in those five quarters (mean 3.9%).
    - Nearly back in 2024Q1 (1.9% below trend; at trend net of methylphenidate), above trend from 2024Q2, and 3.8–8.0% **above** trend in 2025.

    "Q4 2022–latest" would average the shortage together with the later surplus; its mean shortfall is −4.0%, meaning a surplus. So:
    - **Main window: 2022Q4–2023Q4.**
    - Sensitivities: the specified "to latest" window, and 2022Q4–2024Q3 (up to the quota increase).
14. **Feasibility rule.** The coefficient of variation of state intensity is 2.56 (mean 2.07%, SD 5.30%), far above 0.1, so the state design was kept. The CV is inflated because the mean is near zero, though, and that matters for the next point.
15. **Noise benchmark.** I computed the same shortfall for a fake window (2021Q4–2022Q3, trend fitted to 2017Q1–2021Q3). It correlates **0.73** with the real intensity. Much of the cross-state "intensity" therefore reflects state-specific trend breaks that predate the shortage (trend-extrapolation error), not the shortage itself. As a sensitivity, I added a no-extrapolation intensity: the fall versus each state's 2022Q1–Q3 level.
16. **Recovery date (Federal Register, GPO copies).**

    | Drug | Quota change | Published | Citation |
    |---|---|---|---|
    | Methylphenidate (for sale) | +27.5% | 3 Oct 2023 | 88 FR 68147 |
    | Lisdexamfetamine | +23.5% | 5 Sep 2024 | 89 FR 72424 |
    | d-Amphetamine (for conversion) | +18.4% | 5 Sep 2024 | 89 FR 72424 |
    | d-Amphetamine (for sale) | +24.8% | 2 Oct 2025 | 90 FR 47825 |
    | d,l-Amphetamine | +30.6% | 10 Nov 2026 | 91 FR 72564 |

    - The first amphetamine-class increase is **2024Q4**, which I used as the DEA recovery date.
    - ARCOS shows supply recovering earlier (nearly back in 2024Q1, above trend from 2024Q2). So "recovery" is tested two ways: 2024Q1–Q4 (ARCOS) and 2024Q4 (DEA).
    - FARS ends at 2024Q4, so the DEA-dated recovery has only one quarter of data.

## Outcomes (FARS)
17. **Crash unit.** A crash counts for an age group if at least one driver (PER_TYP = 1) is in that group, so a crash can count for both 18–44 and 55–74. "Deaths" = all deaths in those crashes (FATALS), not only driver deaths. Unknown ages (998/999) are excluded.
18. **Crash definitions.**
    - Single-vehicle: VE_FORMS = 1.
    - Daytime: hours 06–17. Night: hours 18–23 and 00–05. Unknown hour (99) is in neither.
    - Speeding: SPEEDREL 2–5.
    - Alcohol: BAC ≥ 0.08 (ALC_RES 80–940).
19. **"Driver at fault"** is approximated by "any driver-related factor recorded". FARS has no fault variable.
    - 2017–2019: DR_SF1–4 in the vehicle file.
    - 2020+: the driverrf file.
    - Codes 1–98 count; 0 (none) and 99 (unknown) don't.
20. **Drug coding changed in 2022** (for example, amphetamine went from 401 to 3019). Drugs were matched by the label columns in the files (AMPHETAMINE, AMPHETAMINE SULFATE, DEXTROAMPHETAMINE, METHAMPHETAMINE, METHYLPHENIDATE), not by codes.
    - 2017 uses the three DRUGRES fields in the person file; 2018+ use the drugs file.
    - Methamphetamine is metabolised to amphetamine, so "prescription amphetamine" = amphetamine-positive **and** methamphetamine-negative.
    - "Tested" = any result other than not given, not reported, or unknown if tested.
21. **Older-driver placebo.** "Pedestrian deaths caused by older drivers" = pedestrians killed (PER_TYP 5, INJ_SEV 4) in crashes involving a driver aged 75+. FARS does not assign causation.

## Population and controls
22. **Census population.** Vintage 2020 (SC-EST2020-ALLDATA5) for 2017–2019 and Vintage 2025 (sc-est2025-alldata5) for 2020–2025. The five race groups were summed (SEX = 0, ORIGIN = 0). Annual populations are applied to every quarter of the year.
23. **VMT.** FHWA VM-2 annual totals; quarterly VMT = annual / 4. This VMT is a control, and the offset in the per-VMT model.
24. **Controls.** The main dose-response model uses log VMT, the unemployment rate, and an indicator for recreational cannabis legal (effective date ≤ quarter end). The alcohol-impaired crash *trend* was not added as a control, because it is a crash outcome on the same causal path. State-specific linear trends are a sensitivity instead.

## Models
25. **Estimation.** Poisson (`fixest::fepois`) with a log-population offset and SEs clustered by state (51 clusters). Exposure is scaled per 10 percentage points of shortfall.
26. **Periods.**
    - post = 2022Q4–2023Q4.
    - rec24 = 2024Q1–Q4.
    - Both are in the same model, so each is compared with the pre-period.
27. **National comparison.** COVID quarters (2020Q1–2021Q4) are excluded. The alternative keeps them with a young × COVID dummy.
28. **Event studies.**
    - The models include state × quarter-of-year fixed effects, because high-shortfall states (FL, TX, CA, AZ) have different crash seasonality. The version without them is also reported.
    - With seasonal fixed effects one reference quarter per season is needed: 2021Q4–2022Q3. The national model drops 2021Q4 as a COVID quarter, so it uses 2019Q4 for season 4.
    - The pre-trend test is a joint Wald test of all non-reference leads. With 11–22 restrictions and 51 clusters it probably over-rejects, but the results are reported as they are.
29. **Placebo dates.** Fake starts at 2019Q4 (data to 2020Q4) and 2021Q4 (data to 2022Q3), with the same five-quarter post length as the real shortage.
30. **Power and expected effect** were written to `expected_effect.md` (timestamp 2026-11-13 22:29 UTC) by `scripts/expected_effect.R` before any model touched FARS data from 2022Q4 on.
    - The share of 18–44-year-olds on stimulants is not in any downloaded data. I used an upper bound (all amphetamine-class supply to ages 18–44, 1 DDD per user per day) and a labelled 50% scenario.
    - The MDE uses the SE from a pre-period placebo model.
31. **Excess crashes and deaths.**
    - Dose-response: Σ over states and shortage quarters of observed × (1 − exp(−β × intensity)).
    - National: observed × (1 − exp(−β)).
    - The 95% CIs plug in the coefficient CI bounds.
    - The national figure is shown but not endorsed, because that design fails its placebo-date tests.

## Bugs caught during the run (fixed before final results)
- The placebo-date function had arguments named `start` and `end`, which dplyr confused with the panel's date columns of the same names. Renamed to `t0` and `t1`.
- A coefficient-name mismatch (`I10:young:rec24`) would have silently returned NA. The `pc()` helper now stops if a term is missing.
- The dose-response scatter divided the rate by the number of quarters twice. Fixed; the scatter now shows annualised rates.
- The seasonal event study silently dropped three 2024 coefficients. Fixed with explicit per-season references.

## Repository
- The large raw files are not committed: FARS zips and extracted files (~3 GB) and ARCOS PDFs (123 MB). `scripts/download_raw.sh` re-downloads them, and the parsed ARCOS CSV is committed. Everything else in `raw/` is committed.
