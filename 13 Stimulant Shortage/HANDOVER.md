# Handover: Did the US stimulant shortage increase fatal car crashes?

Project folder: `13 Stimulant Shortage/` · Branch: `claude/new-session-hgtgv1` · Run: 2026-11-13 (autonomous overnight run)

## Bottom line
- **No detectable increase in fatal crashes with drivers aged 18–44.**
  - Best estimate (triple difference): **+215 excess crashes** (95% CI −597 to 987) and **+236 deaths** (−657 to 1,085) over 2022Q4–2024Q4. There were 53,968 crashes and 59,426 deaths in that window.
- **This matches the expected effect.** Before looking at any crash results, I predicted a rise of only 0.07–0.44%, i.e. 38–237 crashes.
- **But the study is underpowered.** The smallest effect it can detect is 3.6–4.9%, 10–50× the expected effect. So it rules out large harm, not the expected small harm.
- **Why the expected effect is tiny:** the shortage was small in the supply data. National amphetamine-class supply was 5.7% below trend in the acute phase (2022Q4–2023Q4) and back on trend by mid-2024.
- **Signal that the shortage reached drivers:** among tested young crash drivers, amphetamine-positive (methamphetamine-negative) results fell 13% after 2022Q4 (p = 0.04). They fell more in harder-hit states (RR 0.82 per 10 pp, p = 0.06).

## Question and design
- **Question:** did fatal crashes with young drivers rise where stimulant supply fell most, and fall again after supply recovered?
- **Exposure:** each state's shortfall in amphetamine + lisdexamfetamine supply versus its own 2017Q1–2022Q3 trend, over 2022Q4–2024Q4. Source: DEA ARCOS.
- **Outcome:** fatal crashes involving at least one driver aged 18–44, per state-quarter. Source: NHTSA FARS 2017–2024.
- **Designs:**
  1. **Dose-response:** Poisson model; intensity × post; population offset; state × season and quarter fixed effects; log vehicle-miles traveled (VMT); standard errors clustered by state.
  2. **Age comparison:** drivers 18–44 vs 55–74, with 2020–2021 excluded and state × quarter fixed effects.
  3. **Triple difference:** intensity × post × young (the strongest single estimate).
  4. Event-study versions of all three, plus reversal, mechanism, secondary-outcome and placebo tests.

## Data
| Source | What | Status |
|---|---|---|
| DEA ARCOS Retail Drug Summary (Report 02), 2017–2025 | grams by state × quarter: amphetamine (1100), lisdexamfetamine (1205), methylphenidate (1724, includes dexmethylphenidate) | ✅ parsed from PDFs; quarters sum to reported totals |
| NHTSA FARS 2017–2024 | 291,174 fatal crashes, 445,556 drivers; drug tests 2018–2024 only | ✅ (2025 not yet published) |
| Census state single-year-of-age estimates (Vintage 2020 for 2017–19, Vintage 2025 for 2020–25) | population by age band | ✅ |
| FHWA Traffic Volume Trends | monthly state VMT, 2017–2025 | ✅ |
| CDC VSRR provisional overdose deaths | state × year, all ages | ✅ (substitute for WONDER) |
| Federal Register (via govinfo) | DEA quota increases | ✅ |
| DailyMed FDA labels | reference daily doses (WHO DDD site blocked) | ✅ |
| BLS unemployment | control | ❌ blocked |
| Cannabis legalization dates | control and state exclusion | ❌ all sources blocked |
| CDC WONDER (suicide, injury, cancer at ages 18–44) | secondary outcomes and cancer placebo | ❌ blocked |
| Medicaid SDUD | optional second exposure | ⏭ skipped |

The age and triple-difference designs use state × quarter fixed effects, which absorb any state-level shock (unemployment, cannabis policy). This only partly makes up for the missing controls.

## Key dates (from DEA Federal Register notices)
- **Shortage start:** 2022Q4 (FDA announcement, October 2022).
- **First amphetamine-class quota increase:** lisdexamfetamine + d-amphetamine (for conversion), effective **2024-09-05**; lisdexamfetamine aggregate production quota +6,236 kg (doc 2024-20114).
- **Later increases:**
  - methylphenidate: 2023-10-03
  - lisdexamfetamine and d-amphetamine: 2025-09-19 and 2025-10-02
  - d,l-amphetamine: 2026-11-10
- **ARCOS shows supply back at or above trend from 2024Q2.**

## Supply (feasibility)
- **National shortfall vs trend:**
  - 2022Q4: 5.4%
  - 2023Q1: 9.3%
  - acute average (2022Q4–2023Q4): 5.65%
  - 2022Q4–2024Q4: 3.22%
  - 2025: 1.9% *above* trend
- **State spread:** −19.5% (SD, supply above trend) to +14.3% (FL); mean +1.0%, SD 6.2 pp.
  - Hardest hit: FL, TX, UT, NH, AZ.
  - Coefficient of variation is 6.5, high only because the mean is near 0. The spread is real, so the dose-response design was kept as the main design.
- **Methylphenidate** ran above its own trend after 2022 (substitution).

## Results

### Primary
Rate ratios (RR) are per 10 percentage points of state shortfall.

| Model | RR (95% CI) | p |
|---|---|---|
| Dose-response, young-driver crashes | 0.980 (0.934–1.029) | 0.42 |
| Dose-response, deaths | 0.983 (0.933–1.036) | |
| Triple difference, crashes | 1.011 (0.972–1.051) | 0.60 |
| Triple difference, deaths | 1.010 (0.970–1.052) | |
| Age DiD (18–44 vs 55–74), crashes | 1.036 (1.014–1.058) | 0.001 |
| Age DiD + age-specific trend | 0.991 (0.956–1.027) | |

**The age DiD is not credible as a shortage effect:**
- The young/older gap was already at its post-2022 level in 2022Q1–Q3.
- A placebo date of 2021Q4 is significant (0.952).
- A pre-2020 placebo was significant (0.973, p = 0.03).
- The effect disappears once an age-specific trend is added.

### Robustness (dose-response, all null)
- **Exposure variants:**
  - net of methylphenidate: 0.983
  - amphetamine only: 0.988
  - acute-phase intensity: 0.982
  - time-varying quarterly gap: 0.981
- **Sample variants:**
  - excluding 2020–21: 0.987
  - excluding 2022: 0.982
  - excluding FL and TX: 1.022
- **Specification variants:**
  - VMT offset: 0.986
  - no seasonal fixed effects: 0.974
- **Exception:** state linear trends give 0.943 (0.908–0.978), in the *protective* direction.

### Event studies (`figures/fig3_event_studies.png`)
- No jump at 2022Q4 in the dose-response or triple-difference designs.
- Pre-period leads differ jointly from the reference year (2021Q4–2022Q3). The year just before the shortage was itself unusual. Post-period coefficients sit at the same level as the 2017–2019 leads.

### Reversal
- **Dose-response:** acute 0.985, recovery (2024) 0.979; joint p = 0.81.
- **Triple difference:** acute 1.013, recovery 1.019.
- **Post-quota quarter (2024Q4):** 1.007.
- No pattern of rise-then-fall. This test is weak because FARS ends in 2024.

### Mechanism (dose-response per 10 pp; `figures/fig5_mechanism_panel.png`)
- **Crash types:**
  - single-vehicle 0.989
  - multi-vehicle 0.973
  - daytime 0.979
  - night 0.976
  - driver-error 0.998
  - speeding 1.052 (0.987–1.121)
  - BAC ≥ 0.08: 0.910
- **Drug tests:**
  - Amphetamine+/meth−: national post 0.866 (0.755–0.991); dose-response 0.818 (0.663–1.010).
  - Methamphetamine+: national post 0.746 (0.671–0.828); no dose-response (1.022). No sign of a switch to street drugs.
- **Age DiD by crash type:** daytime 1.030 (1.005–1.056); others not significant.

### Secondary outcomes (CDC VSRR, state-year, all ages, per 10 pp)
- Psychostimulant overdose: 1.10 (0.97–1.25), p = 0.13
- All overdose: 1.08 (0.89–1.31)
- All-cause deaths: 0.990 (0.975–1.006)

### Placebos
- **Placebo outcomes:**
  - drivers 75+: 0.946 (0.895–1.000), p = 0.049
  - drivers 55–74: 0.970 (0.940–1.000), p = 0.053
  - pedestrian deaths in older-driver crashes: 0.993

  Hard-hit states saw slightly *fewer* crashes in all age groups. This state-level confounding is why the triple difference is preferred.
- **Placebo dates (dose-response):** 2019Q4 1.028; 2021Q4 1.020. Both null.

## Expected effect and power (`expected_effect.md`, timestamped 16:00:03 UTC, before outcome models)
- **Daily share of 18–44-year-olds on an amphetamine-class stimulant:** 5.66% (upper bound, all ARCOS doses assigned to this age group).
- **Expected rise:** share × drop (3.2–5.7%) × 38–58% (Chang) = **0.07–0.44%**.
- **Minimum detectable effect (80% power):**
  - age DiD: 3.6%
  - dose-response, 87.5th vs 12.5th percentile state: 4.7%
  - with seasonal fixed effects: 4.9%

## Decisions to know about (full list in `decisions_log.md`)
- **Post-hoc change:** state × season fixed effects were added to all state models after the first event study showed a seasonal artifact. High-shortage states (FL, TX, AZ) have different crash seasonality. The original model is reported as robustness; the estimate barely moved (0.974 → 0.980).
- **The 2019Q4 placebo sample** was shortened to end in 2020Q1, so it no longer includes the COVID lockdown quarters.
- **Reference daily doses come from FDA labels, not WHO DDD:**
  - amphetamine 12.5 mg base
  - lisdexamfetamine 30 mg
  - methylphenidate 25 mg

  They only scale the series. The amphetamine-only result is unit-free and agrees.
- **ARCOS covers all ages**, but the brief asked for doses per 1,000 residents aged 18–44. So the "share on stimulants" is an upper bound.
- **Drug-test models cover 2018–2024 only** (no drugs file in FARS 2017). "Amphetamine-positive" excludes methamphetamine-positive drivers, because amphetamine is a methamphetamine metabolite.
- **Driver-error and speeding flags** come from FARS text labels. The driver-factor file format changed in 2020; time fixed effects absorb this.
- **No multiple-testing correction.** Mechanism and placebo p-values are exploratory.

## Unverified
- Whether ARCOS grams for lisdexamfetamine and methylphenidate are base or salt weight.
- Whether the FARS 2024 file is the final release or the annual-report file.

## Files
| File | Contents |
|---|---|
| `analysis.Rmd` / `.html` | full analysis, house style: cleaning → feasibility → expected effect → national → dose-response → triple difference → reversal → mechanism → secondary → placebos → excess |
| `figures_tables.Rmd` / `.html` | refits models and saves the 5 figures |
| `clean_data.xlsx` | 7 sheets: state-quarter panel, supply by state and nationally, intensity, national series, CDC overdose, population |
| `figures/` | national series, intensity map, event studies, dose-response scatter, mechanism panel (+ CSV) |
| `expected_effect.md` | the timestamped expected effect and power calculation |
| `decisions_log.md` | every judgment call and data gap |
| `SUMMARY.md` | audit of every step + paper-ready Methods/Results |
| `raw/SOURCES.md` | download links for all raw data (3.2 GB, not committed) |

## To rerun
1. Re-download the raw data into `raw/` as listed in `raw/SOURCES.md`. This includes `pdftotext -layout` on the ARCOS PDFs and unzipping FARS into `raw/fars/x/{year}/`.
2. Install R 4.3+ with tidyverse, readxl, openxlsx and fixest.
3. Run `rmarkdown::render("analysis.Rmd")`, then `rmarkdown::render("figures_tables.Rmd")`. The full run takes about 3 minutes.

## Open decisions / next steps
1. **Framing.** Write it up as a null result that rules out large harm (crash harm >~5% per 10 pp of shortfall), with the drug-test result as evidence the shortage reached drivers. Or add individual-level exposure (Medicaid SDUD by state-quarter, or claims) to gain power.
2. **Missing data.** Fill the blocked inputs (BLS, cannabis dates, CDC WONDER) from a machine with open access. Then add those controls, the exclusion of states that legalized cannabis in 2022–2024, the age 18–44 secondary outcomes and the cancer placebo.
3. **Update when FARS 2025 is released.** This would give a real post-recovery window for the reversal test.
4. **Website repo.** This folder lives in the website repo; merging the branch may publish it on the site. Move it to a separate repo if that is not wanted.
