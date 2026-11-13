**FLAG:** The main shortage window is 2022Q4–2023Q4, not the specified "Q4 2022–latest". In ARCOS, amphetamine-class supply was back above trend from 2024Q2, so the specified window has a mean surplus of 4.0%. CDC WONDER (ages 18–44, cancer placebo, unintentional injury) was not retrieved.

### 1. What the code did

1. **Network and tools.** Added the data hosts to the environment and installed R 4.3.3 and fixest. Blocked: BLS direct download (scripted clients refused; the same LAUS series came via FRED), the CDC WONDER API (needs a data-use agreement only you can accept) and NIAAA APIS (403) → `raw/`
2. **ARCOS download.** Retail Drug Summary PDFs, 2017–2025, parsed with `scripts/parse_arcos.py`. Report 2 gives grams by state × quarter for codes 1100, 1205, 1724 and 1105; quarter sums match totals within 0.02 g → `raw/arcos/arcos_report2_parsed.csv` (1,953 rows)
3. **FARS download.** National CSV files for 2017–2024. No 2025 file exists (404) → `raw/fars/`
4. **Other downloads.**
   - Census Vintage 2020 and Vintage 2025 state single-year-of-age files.
   - FHWA VM-2 for 2017–2024.
   - FRED `<ST>UR` series for 51 jurisdictions.
   - Cannabis effective dates (Wikipedia table).
   - WHO DDDs: amfetamine 15 mg, lisdexamfetamine 30 mg, methylphenidate 30 mg, dexmethylphenidate 15 mg.
   - Ten Federal Register notices (GPO copies).
   - Three data.cdc.gov files.
5. **Population.** Ages 18–44, 55–74 and 75+ by state × year, summing the 5 race groups (SEX 0, ORIGIN 0) → `pop` (51 states, 2017–2025)
6. **ARCOS to DDDs.** Amphetamine class = codes 1100 + 1205; methylphenidate = 1724 (includes dexmethylphenidate, at a 30 mg DDD). Converted to DDD per 1,000 residents aged 18–44 per day → `arcos` (51 × 36 quarters)
7. **Shortage intensity.** Each state's own linear trend plus season, fitted on 2017Q1–2022Q3; shortfall = mean % below expected → `intensity`, with these variants:
   - Main window, 2022Q4–2023Q4.
   - Net of methylphenidate.
   - To the quota increase (2022Q4–2024Q3).
   - To latest ARCOS (2022Q4–2025Q4).
   - No-extrapolation change versus 2022Q1–Q3.
   - Fake window 2021Q4–2022Q3.
8. **Controls.** VMT (FHWA VM-2 totals; header row located, footnote marks stripped), quarterly unemployment, and a recreational cannabis indicator (effective date ≤ quarter end) → `vmt` (408 rows), `unemp`, `cannabis`
9. **FARS driver file.**
   - Drivers (PER_TYP 1) joined to accident, vehicle, driver-factor and drug results.
   - Drugs matched by label name, because codes changed in 2022.
   - amph_rx = amphetamine-positive and methamphetamine-negative.
   - → `drivers` (445,556 driver records)
10. **Crash counts.** By state × quarter × driver-age group, with a crash counted for a group if it has ≥ 1 driver in that group. Subtypes counted: single/multi-vehicle, day/night, driver factor, speeding, BAC ≥ 0.08, drug results, and pedestrian deaths → `panel` (4,896 rows = 51 × 32 × 3; 187,553 crashes with a driver aged 18–44, 86,486 with a driver aged 55–74, 25,526 with a driver aged 75+)
11. **CDC secondary outcomes** (all ages):
    - Suicide and drug overdose, state × year 2019–2024.
    - Psychostimulant overdose (T43.6), 12-month-ending December, 2017–2025, 50 states (one missing).
    - → `secondary`
12. **Expected effect and power.** Written by `scripts/expected_effect.R` using ARCOS and pre-2022Q4 FARS only → `expected_effect.md` (2026-11-13 22:29 UTC)
13. **Feasibility.** National supply versus trend, spread across states, fake-window correlation, recovery dates from the Federal Register → `nat_arcos`, `spread`, `recovery`, figures 01 and 02
14. **National comparison.** Drivers 18–44 vs 55–74 (Poisson, state × age-group FE + quarter FE, population offset, state-clustered SE). COVID quarters are excluded (n = 2,448); variants use a COVID dummy, deaths as the outcome, and seasonal FE. Event study uses state × age × season FE → `nat_res`, `es_nat`, figure 03a
15. **Dose-response.** Crashes with a driver aged 18–44 ~ intensity × post + intensity × 2024 + log VMT + unemployment + cannabis | state + quarter (n = 1,632), plus 12 variants. Event study uses state × season FE → `dose_rob`, `es_dose`, figures 03b and 04
16. **Triple difference.** Intensity × post × young, with state × group, state × quarter and group × quarter FE (n = 3,264), plus 3 variants → `ddd_res`, `es_ddd`, figure 03c
17. **Reversal.** 2024 (ARCOS recovery) and 2024Q4 (DEA quota date) terms → `rev_res`, `rev_diff`
18. **Mechanism.** 11 crash types in both designs; drug results per tested driver; placebo dates for the amphetamine-positive finding → `mech`, `drug_share`, `amph_placebo`, figure 05
19. **Secondary outcomes.** State × year Poisson, intensity × 2023 and × 2024–25, with state and year FE → `sec_res`
20. **Placebos.**
    - Outcomes: drivers 75+, pedestrian deaths in crashes with a driver 75+, drivers 55–74, and 75+ vs 55–74.
    - Dates: fake shortage starts in 2019Q4 and 2021Q4.
    - → `plac_out`, `plac_dates`
21. **Excess crashes and deaths** during the shortage, from the dose-response and national models → `excess`
22. **Saved outputs.** 22 sheets in `clean_data.xlsx`, `results.rds`, `analysis.html` (knitted without errors)

**Unverified:**
- The share of 18–44-year-olds on stimulants (an upper bound plus a 50% scenario, not data).
- Whether the FARS 2024 file is the Final or the Annual Report File.
- Cannabis dates come from a secondary source.

**Not run:**
- CDC WONDER age 18–44 outcomes, the cancer-death placebo and unintentional-injury deaths.
- Medicaid SDUD exposure.
- FARS 2025.
- A reversal test with more than one quarter after the DEA date.

---

### 2. Methods and Results

**Methods.**

*Exposure.* We used DEA ARCOS retail distribution (grams by state and quarter, 2017–2025), converted to WHO defined daily doses per 1,000 residents aged 18–44 per day. Shortage intensity was each state's mean percentage shortfall in amphetamine-class supply (amphetamine plus lisdexamfetamine) between 2022Q4 and 2023Q4, relative to its own 2017Q1–2022Q3 linear trend with seasonal terms.

*Outcomes.* From NHTSA FARS 2017–2024 we counted fatal crashes involving at least one driver aged 18–44, and, as comparators, aged 55–74 or 75+, by state and quarter (51 jurisdictions, 32 quarters).

*Models.* All models were Poisson with a log-population offset and standard errors clustered by state.
- National comparison: crashes of drivers aged 18–44 vs 55–74, excluding 2020–2021.
- Dose-response: intensity × shortage period, with state and quarter fixed effects, log VMT, unemployment and recreational cannabis status.
- Triple difference: intensity × period × age group, with state-by-quarter fixed effects.

Shortage and recovery periods were 2022Q4–2023Q4 and 2024. We verified the first amphetamine-class quota increase in the Federal Register: 5 September 2024 (89 FR 72424).

*Checks.* Mechanism outcomes were crash subtypes and driver drug results within state. Secondary outcomes were state-year suicide, drug-overdose and psychostimulant-overdose deaths at all ages (CDC). Placebos were older drivers and fake start dates (2019Q4, 2021Q4).

*Pre-specification and software.* Expected effect and power were saved before analysis. We used R 4.3.3 with fixest 0.14.2, tidyverse 2.0.0 and data.table 1.14.10.

*Limitation from a coding decision.* State intensity correlated 0.73 with the same measure computed for a fake pre-shortage window, so much of its cross-state variation reflects pre-existing trend breaks.

**Results.**

*Supply.* National amphetamine-class supply was 3.9% below trend over 2022Q4–2023Q4 (peak 7.4% in 2023Q1). Net of methylphenidate it was 1.6% below trend. Supply was above trend from 2024Q2. State shortfalls ranged from −12.7% to 13.4% (SD 5.3; CV 2.56).

*Pre-specified expectation.* We expected an effect of at most 0.25% nationally and 0.27% per 10 percentage points (pp). The minimum detectable effects were 4.1% and 10.0%.

*Dose-response.* Crashes with a driver aged 18–44 did not rise with state shortfall: −0.8% per 10 pp (95% CI −5.3 to 3.9; p = 0.73; n = 1,632). Deaths: −0.6% (−5.5 to 4.6). The estimate stayed between −3.6% and −0.2% with every CI including zero across all 12 variants:
- per-VMT rates;
- net of methylphenidate;
- alternative windows;
- no-extrapolation intensity;
- excluding COVID quarters;
- state trends;
- excluding the six states that legalised cannabis in 2022–2024;
- excluding 2022;
- seasonal fixed effects.

*Triple difference.* +1.2% per 10 pp (−2.2 to 4.8; p = 0.49; n = 3,264).

*Event studies.* Pre-trend Wald tests rejected parallel leads (dose-response p = 4×10⁻¹⁰; triple difference p = 2×10⁻¹⁰). The shortage-period coefficients lay at the same level as those for 2017–2020.

*Reversal.* No reversal was seen:
- 2024 (ARCOS recovery): −1.6% per 10 pp (−7.6 to 4.8).
- 2024Q4 (DEA quota date): +1.9% (−5.4 to 9.8).

*National comparison.* Crashes with drivers aged 18–44 rose 3.6% relative to drivers aged 55–74 during the shortage (1.7 to 5.5; n = 2,448). Deaths rose 3.9%. But this design failed both placebo-date tests:
- +9.4% at a fake 2019Q4 start (7.2 to 11.7).
- +7.9% at a fake 2021Q4 start (4.9 to 11.0).

Its pre-trend test rejected (p = 7×10⁻⁵), and drivers aged 75+ also diverged from drivers aged 55–74 (−5.1%, −8.9 to −1.1).

*Mechanism (dose-response).* No crash subtype moved:
- single-vehicle −1.0%;
- daytime −0.8%;
- driver factor +1.1%;
- speeding +5.2% (−1.4 to 12.3).

Amphetamine-positive (methamphetamine-negative) drivers fell 36.4% per 10 pp (−48.7 to −21.2), or 33.0% per tested driver (−45.1 to −18.1). The same model gave increases at fake start dates (+40.8% at 2019Q4, +26.2% at 2021Q4), so this decline is not attributable to the shortage. Methamphetamine-positive drivers did not change (−5.0%, −22.7 to 16.6).

*Secondary outcomes (per 10 pp).* No association:
- suicide −0.3% (−2.3 to 1.6);
- drug overdose +3.3% (−9.0 to 17.3);
- psychostimulant overdose +4.7% (−4.8 to 15.1).

*Placebo outcomes.* Crashes with a driver aged 75+ were null (−4.7%, −11.4 to 2.6). Pedestrian deaths in crashes with a driver aged 75+ were borderline (−15.2%, −27.9 to −0.2; p = 0.047).

*Excess burden.* The dose-response model gives −116 excess crashes (−794 to 530) and −86 excess deaths (−898 to 685) during the shortage. The shortage period had 30,792 crashes with a driver aged 18–44 and 33,969 deaths in those crashes.

---

### 3. Recap

- **Done:** We linked DEA supply data (51 states, 2017–2025) to 187,553 fatal crashes with a driver aged 18–44 (FARS 2017–2024) in national, dose-response and triple-difference designs, with pre-specified power, 12 dose-response sensitivity variants and placebo tests.
- **Found:** No excess fatal crashes are attributable to the shortage: −116 crashes (95% CI −794 to 530) and −86 deaths (−898 to 685). The dose-response result is robust across all variants. The 3.6% national young-vs-older rise fails both placebo-date tests. The expected effect (≤ 0.25%) was 16–37 times below the minimum detectable effect, so this null rules out only effects larger than about 4–10%, consistent with the small 3.9% supply drop.
- **Decide:** Whether to obtain CDC WONDER data (needs your data-use agreement) for the age 18–44 secondary outcomes and the cancer placebo, and whether to frame the paper as "the shortage was too small in supply data to cause detectable crash harm".
