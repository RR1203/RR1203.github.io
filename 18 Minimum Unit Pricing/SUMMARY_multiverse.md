**FLAG:** The cause split uses crude rates (data level 3), not age-standardised rates. Scotland's 2022 deaths by cause and age exist only on the NRS web archive, which served a browser-verification page twice and was not bypassed. The frozen hierarchy then requires crude rates for both nations. An exploratory age-standardised version with 2022 omitted gives nearly the same estimates.

**FLAG:** The 2011 ICD-10 coding change moved acute alcohol intoxication from F10.0 to X45 in both nations, but by different amounts:

| | X45 before 2011 → 2011 | F10 2010 → 2011 |
|---|---|---|
| Scotland | 0–1/yr → 61 | — |
| England | 173 → 360 | 628 → 427 |

- Cause-multiverse specs starting before 2011 cross this break for F10 and poisoning.
- The 80 poisoning specs that include 2007–2008 were dropped: Scotland recorded 0 deaths in those years, so the rate is unidentifiable.
- A start ≥ 2011 summary was added after seeing the data and is labelled post-hoc.
- The primary and Wyper windows (2012+) are unaffected.

**FLAG:** Two hosts were added to the cloud environment with your approval: `www.nomisweb.co.uk` (England cause × age data, 2022–2024) and `webarchive.nrscotland.gov.uk`, which is unusable because of the browser-verification page.

**FLAG:** The multiverse grid uses `expand_grid()` + `pmap()`, which departs from house style. The model formulas are written out explicitly inside.

**FLAG:** Every pre-specified prediction (P1–P3) is *uninformative*. All three causes are underpowered: minimum detectable effects (MDE) are K70 15.4%, F10 57.3% and poisoning 32.7%, and each CI spans both 0 and −13%.

### 1. What the code did

1. **Froze the plan.** `multiverse_specs.md` (320 CITS specs, 40 synthetic-control specs, cause split, predictions P1–P3, Holm adjustment) was committed as `3a13287` before any data were downloaded or models run. Logged in DECISIONS.md.
2. **Downloaded and harvested** these sources into `03_mup_raw_cause.xlsx` (`scripts/03_harvest_cause.py`) → sheets `deaths_cause_age`, `nrs_cause_total`, `nomis_asmr_published`, `population_age`:
   - Nomis NM_161_1: England, North East and North West deaths by cause × age, 2013–2024.
   - Nomis NM_31_1: population by 5-year age band, 2007–2024.
   - ONS individual-cause dataset (England, Scotland; 2001–2021).
   - ONS ad hoc 11797 (North East, North West; 2001–2018).
   - NRS vital-events table 6.04 for 2023 and 2024.
3. **Checked that sources agree where they overlap:**
   - ONS vs Nomis: 2013–2021 for England, 2013–2018 for the regions.
   - Every Scotland source vs NRS Table 8.
   - Agreement ratio = 1.000 for every ICD code.
4. **Spliced the series:**
   - England: ONS up to 2021, Nomis from 2022.
   - NE+NW: ad hoc table up to 2018, Nomis from 2019.
   - Scotland: by-age counts for ages; NRS Table 8 for totals.
   - Ages 85–89 and 90+ merged into 85+. Causes: k70 = K70; f10 = F10; poisoning = X45+X65+Y15.
5. **Built the rate tables:**
   - Crude rates = deaths / Nomis population × 100,000 → `cause_crude` (n=162).
   - ESP2013 rates → `cause_asmr` (n=159; Scotland 2022 missing).
   - Validation: computed England rates vs Nomis published rates differ by a ratio of 0.997–1.004 → `cause_validation` (n=24).
6. **H8a, CITS multiverse:** the H0 model run over start 2007–2014 × end 2020–2024 × trend (full / pre-only) × control (England / NE+NW) × COVID (indicator / exclude). 320 specs ran, none dropped → `h8_cits`, plus summaries overall and by dimension → `h8_summary`.
7. **H8b, synthetic control:** demeaned synthetic control (10 donors) over start × end, 40 specs. Inference by placebo-in-space using the post/pre RMSPE ratio → `h8_sc`, `h8_sc_summary`. Saved together as `h8_multiverse`.
8. **H9, cause split:**
   - Primary CITS 2012–2024 (n=13) and Wyper-window CITS 2012–2020 (n=9, no COVID term) for each cause.
   - Holm adjustment across the 3 primary tests, MDE per cause, prediction verdicts → `h9_table`, `h9_mde`, `h9_predictions`.
9. **H9 multiverse:** cause × the 320-spec grid = 960 specs. 880 ran and 80 poisoning specs were dropped (non-finite log gap). Summaries were made, plus the post-hoc start ≥ 2011 summary.
10. **H9 exploratory age-standardised check:** primary model per cause on ESP2013 rates, with 2022 omitted → `h9_asmr_table`. Everything saved as `h9_cause`.
11. **Figures and tables:** `figures_tables.Rmd` produced:
    - `fig6_multiverse_specification_curve.png`
    - `fig7_cause_specific.png`
    - tables `table6`, `table6b`, `table7`, `table7b` (CSV)

**Unverified:**
- Why NRS's archive serves a browser check to automated access.
- Whether a Scotland 2022 cause × age table exists anywhere other than that archive.

**Not run:**
- Age-standardised rates as the H9 primary (blocked by the missing 2022 Scottish age data).
- Synthetic control by cause (not specified).

### 2. Methods and Results

**Methods.**
- **Plan:** all specifications and predictions were fixed in advance (`multiverse_specs.md`, committed before any analysis).
- **Model:** the H0 controlled interrupted time series (CITS) on log(Scotland/control rate), with a linear trend, a fraction-of-year MUP term (2018 = 8/12) and a 2020–21 COVID term; Newey–West SE (lag 1) and t-based 95% CIs.
- **Multiverse:** the model was refitted over:
  - start year 2007–2014
  - end year 2020–2024
  - trend estimated on all years, or on pre-policy years only (adding a post-policy slope; effect averaged over full post-policy years)
  - control England or North East + North West England
  - COVID years modelled with an indicator or excluded
- **Synthetic control:** a demeaned synthetic control (donors: 9 English regions and Northern Ireland) was run over start × end, with inference by placebo-in-space.
- **Cause-specific outcomes:**
  - Sources: underlying-cause counts for K70, F10 and acute poisoning (X45+X65+Y15) from ONS, Nomis and NRS; populations from Nomis mid-year estimates.
  - Rates: crude, because Scottish deaths by cause and age were unavailable for 2022.
  - Coding: the 2011 ICD-10 update moved acute intoxication from F10.0 to X45, so cause-specific windows starting before 2011 cross a coding break.
  - Inference: Holm-adjusted across the three primary cause tests. MDE used the H2 method.

**Results.**

*All alcohol-specific deaths (H8).* Across 320 CITS specifications, the median effect was −6.0% (IQR −14.0 to −0.2). 78.4% of estimates were negative, and 26.6% were negative with p < 0.05. Start year and trend method decide most of the result:

| Choice | Median effect (IQR) | % negative |
|---|---|---|
| Start 2007 | +2.7% (−0.1 to +4.6) | 30% |
| Start 2012 | −13.1% (−19.1 to −8.2) | 100% |
| Start 2014 | −15.6% (−22.9 to −4.7) | 100% |
| Trend from pre-policy years only | −13.4% | 91.2% (53.1% with p < 0.05) |
| Trend from all years | −2.3% | 65.6% (0% with p < 0.05) |
| Control England | −6.7% | — |
| Control NE+NW | −4.8% | — |
| End 2020 | −8.9% | — |
| End 2024 | −3.5% | — |

- The COVID choice barely mattered: −6.4% excluding those years, −5.7% with an indicator.
- The Wyper-matched grid specs gave −9.5% (95% CI −21.0 to +3.7; p = 0.12). The original H0 Wyper spec, which keeps 2020 as an ordinary year, gave −11.8% (−21.4 to −0.9).
- All 40 demeaned synthetic-control specs were negative: median −15.5% (IQR −17.2 to −14.2), range by end year −14.2% to −17.7%. Placebo p ranged from 0.09 to 0.36; none was below 0.05, and the smallest possible is 1/11.

*Cause-specific (H9; crude rates; n = 13 years; Holm-adjusted p = 1.0 for all):*

| Cause | Primary 2012–2024 (95% CI), p | Wyper window 2012–2020 (95% CI), p | MDE |
|---|---|---|---|
| K70 | −5.3% (−17.7 to +9.0), p = 0.40 | −8.7% (−15.3 to −1.5), p = 0.026 | 15.4% |
| F10 | −23.3% (−57.9 to +39.8), p = 0.34 | −33.5% (−63.0 to +19.7), p = 0.14 | 57.3% |
| Poisoning | +13.0% (−16.3 to +52.6), p = 0.38 | +6.0% (−16.1 to +33.9), p = 0.56 | 32.7% |

- The point estimates point the way P1–P3 predicted, but every prediction is uninformative under the pre-specified rule.
- The age-standardised check (2022 omitted) gave similar results: K70 −3.7% (−14.1 to +8.0), F10 −22.1% (−58.3 to +45.4), poisoning +12.5% (−19.2 to +56.7).

Cause multiverse medians:

| Cause | All specs: median (IQR), % negative | Post-hoc, start ≥ 2011 |
|---|---|---|
| K70 (n=320) | −3.4% (−9.6 to +5.3); 60.9% negative | −8.9%; 100% negative, 35% with p < 0.05 |
| F10 (n=320) | −35.3% (−44.0 to −26.5); 99.1% negative | −36.6% |
| Poisoning (n=240) | −1.9% (−72.1 to +15.0) | +9.4%; 30.6% negative |

For K70 the start year drives the sign: start 2007 gives +8.6% and start 2014 gives −17.9%.

### 3. Recap

- Ran a pre-registered 320-spec CITS multiverse, a 40-spec synthetic-control multiverse and a 960-spec cause split for Scotland's 2018 MUP against England.
- All-deaths effect: −6% median, negative in 78% of CITS specs and all 40 synthetic-control specs. Its size depends mainly on start year (2007 starts ≈ 0; 2011+ starts ≈ −13%) and on trend method. By cause, K70 and F10 lean negative and poisoning does not, but all three are underpowered; the cause split runs on crude rates and crosses a 2011 coding break.
- Decision: either report the start-year sensitivity as the main finding, or justify a 2011+ window a priori. To lift the crude-rate FLAG, ask NRS for the 2022 cause × age table.
