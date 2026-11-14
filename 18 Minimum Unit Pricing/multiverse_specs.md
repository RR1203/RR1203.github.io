# Multiverse and cause-split specification list (FROZEN)

Frozen: 2026-11-14T01:25Z, before any H8 or H9 model was run and before any cause-specific death data were downloaded or inspected.
Any later change is logged in `DECISIONS.md` and marked **FLAG**.

## Base model (identical to H0)

- **Outcome:** `log(ASMR_Scotland) − log(ASMR_control)`.
- **Model:** `lm(log_gap ~ year_c + mup [+ covid])`.
  - `year_c = year − 2018`.
  - `mup` = fraction of the year under MUP: 0 before 2018, 8/12 in 2018, 1 from 2019.
- **Inference:** Newey–West SE (lag 1, no prewhitening), t-based 95% CI with residual df.
- **Effect:** `100 × (exp(b) − 1)`.

## H8. Multiverse, Scotland, all alcohol-specific deaths (persons)

### H8a. CITS grid: 8 × 5 × 2 × 2 × 2 = 320 specifications

| Dimension | Levels |
|---|---|
| Start year | 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014 |
| End year | 2020, 2021, 2022, 2023, 2024 |
| Trend | **full**: one linear trend fitted on all years (H0 primary). **pre-only**: adds `post_slope = max(0, year − 2018)`, so the trend comes from pre-policy years only |
| Control | **England**: ONS ASMR. **NE+NW**: North East + North West England, ratio of sums with deaths/ASMR as the standardised-population proxy (existing `Eng: NE+NW` rows) |
| COVID | **indicator**: `covid = 1` for years 2020–2021 that fall inside the window (if end = 2020, 2020 only). **exclude**: drop 2020–2021 years in the window, no COVID term |

**Pre-only effect:** the average over full post years 2019..end, `b_mup + b_post_slope × mean(year − 2018 for year in 2019..end)`. Its SE is the linear-combination SE from the Newey–West vcov.

**When a spec is dropped:** if any needed coefficient is NA (rank-deficient), or residual df < 1. Dropped specs are logged in `DECISIONS.md`.

**Summaries, overall and by each dimension level:**
- number of specs
- median effect (%)
- IQR of effect (%)
- % of specs with a negative point estimate
- % negative with p < 0.05

**Highlighted (Wyper-matched):** start 2012, end 2020, England, full trend. In the grid this appears as two specs, COVID indicator and COVID exclude; both are highlighted.

**Reference point outside the grid:** the existing H0 Wyper spec, which has no COVID term. It is shown on the figure but not counted in the summaries.

### H8b. Demeaned synthetic control: 8 × 5 = 40 specifications

- **Setup:** the existing H0 setup.
  - Outcome: log ASMR. Donors: 9 English regions + Northern Ireland.
  - Each unit is demeaned by its own mean over start..2017.
  - Weights from `solve.QP`: non-negative, sum to 1, fitted on start..2017.
- **Effect:** `100 × (exp(mean gap 2019..end − mean gap start..2017) − 1)`.
- **Inference:** placebo-in-space p = share of the 11 units whose post/pre RMSPE ratio is ≥ Scotland's. There is no CI.
- **Summaries:** median, IQR, % negative, % with placebo p < 0.05 (min attainable is 1/11 = 0.09, so this will be 0% by construction; reported anyway), overall and by start and by end.

## H9. Cause-specific split, Scotland vs England

### Causes (underlying cause, ICD-10)

1. Alcoholic liver disease: K70.
2. Mental and behavioural disorders due to alcohol: F10.
3. Acute alcohol poisoning: X45 + Y15, plus X65 if it is available for both nations. If X65 is available for only one nation, the outcome is X45 + Y15 for both.

### Data hierarchy (decided now; the first available level is used, per nation)

1. Published ASMR by cause (ESP2013).
2. ESP2013 ASMR computed from published counts by cause × 5-year age band plus population by age (existing method).
3. Crude rate = deaths / mid-year population × 100,000. **FLAG** if used.

Both nations must use the same level for a given cause. If they don't, the lower level is applied to both and **FLAG**ged.

### Analyses (per cause)

- **H9 primary:** 2012–2024 CITS, same model as H0 primary (full trend, COVID indicator 2020–21), control England.
- **Wyper-matched:** 2012–2020 CITS, no COVID term (as in H0 Wyper).
- **Multiverse:** cause as an extra dimension in the H8a CITS grid. That gives 3 × 320 = 960 specs if NE+NW cause-specific data exist.
  - If they don't, the control dimension is England only: 3 × 160 = 480. This is logged as unavoidable and **FLAG**ged.
- **MDE per cause:** existing H2 method.
  - sigma from `lm(log_gap ~ year_c)` on pre-policy years 2012–2017.
  - SE = sigma × sqrt([(X'X)^-1]_mup) for the primary design.
  - MDE = (1.96 + 0.84) × SE, reported as `100 × (1 − exp(−MDE))`.
  - A cause is labelled underpowered if its MDE exceeds 13%.
- **Multiplicity:** Holm adjustment across the 3 primary cause p-values.

### Pre-specified predictions

- **P1:** K70 falls relative to England. Primary estimate < 0, expected significant if powered.
- **P2:** F10 falls relative to England. Primary estimate < 0.
- **P3:** Acute poisoning shows a smaller or no effect. |effect| is smaller than both K70 and F10, or the 95% CI includes 0.
- **Assessment:** each prediction is reported as supported / not supported / uninformative (underpowered with CI including both 0 and −13%).

## Implementation note (style, not specification)

Iterating over 320, 960 and 40 specs needs `expand_grid()` + `pmap()`/`group_modify()`. This departs from the house-style "no map()" rule and is logged in `DECISIONS.md`. Each model formula is still written out explicitly.
