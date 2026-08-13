# Protocol — Psychiatric-cause mortality in the United States, 1999–latest available year

**Status:** Pre-registration. Written and committed **before any data request** in this
run. Step 4 (analysis) may test nothing that is not specified here; any analysis not in
this file is exploratory and must be labeled as such wherever it appears.

Date of pre-registration: 2026-08-13 (UTC). Author of record: overnight autonomous run
on behalf of the project owner; requires author verification before any use.

---

## 1. Research question

How has mortality from psychiatric conditions recorded as the **underlying cause of
death** changed in the United States from 1999 to the latest available final data year,
overall and by sex and age — and, specifically:

- Did mortality from **substance-induced mental and behavioural disorders (F10–F19)**
  and from **non-substance mental and behavioural disorders** follow different trends?
- How did **intentional self-harm** mortality (a pre-specified, separate series — not
  part of the ICD-10 F chapter) evolve over the same period, and did its long rise
  reverse in the late 2010s?

This is a national-level ecological (aggregate) study of death-certificate data. It
supports no individual-level or causal inference.

## 2. Data sources

| Series | Database | Years | Race methodology |
|--------|----------|-------|------------------|
| Primary | CDC WONDER **D76**, Underlying Cause of Death, 1999–2020 | 1999–2020 | Bridged race |
| Extension | CDC WONDER **D158**, Underlying Cause of Death, 2018–latest, Single Race | 2018 through latest final year served (expected 2024) | Single race |

The two databases use different race methodologies and different population
denominators. They are **never spliced into one series**. All results present them as
two separate series; the 2018–2020 overlap serves as a built-in cross-database QC
check (§7, sensitivity S3). National level only — the WONDER API does not serve
state/county mortality queries. If the actual year coverage of D158 differs from the
expectation above, the actual coverage is used and the discrepancy logged in
DECISIONS.md (no protocol change required — "latest final year served" is the
specification).

## 3. Case definitions (exact ICD-10 codes, underlying cause of death)

| Series | Name | ICD-10 codes |
|--------|------|--------------|
| A | All mental and behavioural disorders | F01–F99 (the WONDER "Mental and behavioural disorders" chapter selection) |
| A1 | Substance-induced mental and behavioural disorders | F10–F19 |
| A2 | Non-substance mental and behavioural disorders | F01–F09 and F20–F99 (i.e., A minus A1) |
| B | Intentional self-harm (suicide) | X60–X84 and Y87.0; plus U03 if selectable in the database's code list |

**Justification.** Series A is the standard chapter-level definition of psychiatric
mortality. The A1/A2 split separates substance-related deaths (concentrated in
working-age adults and plausibly driven by the alcohol/drug epidemics) from the
non-substance remainder, which at chapter level is dominated by organic disorders —
chiefly dementia codes F01 and F03 in the elderly — whose recorded mortality is known
to be strongly affected by secular changes in death-certificate coding practice.
Series B follows the NCHS injury-mortality definition of suicide (X60–X84, Y87.0, U03).
If a component code (Y87.0 or U03) is not selectable in a database's picklist, the
closest available selection is used and the deviation logged in DECISIONS.md with its
expected magnitude (both codes contribute very few deaths relative to X60–X84).

**Alternative definitions (pre-specified, used only in sensitivity S1):**

- A′: F10–F99 — Series A excluding organic mental disorders (F01–F09), testing whether
  chapter-level conclusions are robust to removing the dementia-dominated block.
- B′: X60–X84 only — Series B without sequelae/terrorism codes.

## 4. Years, strata, and measures

- **Years:** D76: all years 1999–2020. D158: all years served (expected 2018–2024).
- **Strata (pre-specified):** calendar year; sex (female, male); 10-year age groups
  (WONDER standard ten-year groups). Queries request at most year × one other
  stratifier; combined tables are assembled in the cleaning step, not in the request.
- **Race/ethnicity:** not part of the confirmatory design. If examined at all, it is
  exploratory only (`analysis/exploratory/`), one database at a time (bridged-race and
  single-race series are incompatible), and labeled exploratory wherever mentioned.
- **Measures:** deaths; population; crude rate per 100,000; age-adjusted rate per
  100,000 standardized to the 2000 U.S. standard population (WONDER's computation).
  Age-adjusted rates are used for totals and sex strata; within 10-year age groups the
  age-specific (crude) rate is the rate measure.

## 5. Hypotheses (falsifiable, with exact tests)

Statistical conventions for all hypotheses: two-sided α = 0.05; 95% confidence
intervals; estimation in Python/statsmodels; the full model output for every fitted
model is saved as a text file under `analysis/`. Primary analysis years for D76 models:
**1999–2020** (full range); sensitivity S2 excludes 2020 (COVID-era certification
effects). No multiplicity adjustment across the three hypotheses (small pre-specified
family; acknowledged as a limitation).

### H1 — Rising substance-induced psychiatric mortality

**Claim.** The national age-adjusted death rate for Series A1 (F10–F19) increased on
average over 1999–2020.

**Test.** Ordinary least squares regression of ln(age-adjusted rate) on calendar year,
D76 national totals, 1999–2020. Average annual percent change
AAPC = 100·(exp(β̂_year) − 1), 95% CI from the OLS standard error.
Serial correlation is addressed by also reporting Newey–West (HAC, lag 1) standard
errors; the OLS CI is primary.

**Decision rule.** Confirmed if the 95% CI for AAPC lies entirely above 0. Refuted if
it lies entirely below 0. Inconclusive if it spans 0.

### H2 — Divergence between substance-induced and non-substance trends

**Claim.** Over 1999–2020, the death rate for Series A1 (F10–F19) grew faster
(proportionally, per year) than the rate for Series A2 (non-substance F codes).

**Test.** Poisson regression of annual national death counts on
year (continuous, centered) × category (A1 vs A2), with ln(population) offset, D76
1999–2020 (44 observations: 22 years × 2 categories). Overdispersion assessed by the
Pearson χ²/df dispersion statistic (reported in all cases); if it exceeds 2, a
negative binomial model (NB2, statsmodels default estimation) replaces the Poisson as
the primary model. The estimand is the interaction coefficient: the difference in
annual log-rate growth between A1 and A2.

**Decision rule.** Confirmed if the interaction (A1 vs A2 per-year log-rate-ratio
difference) is positive with 95% CI excluding 0. Refuted if negative with 95% CI
excluding 0. Inconclusive otherwise.

### H3 — Reversal of the intentional self-harm trend in the late 2010s

**Claim.** The national age-adjusted rate for Series B rose from 1999 to the late
2010s, then the trend broke downward.

**Test.** Segmented (piecewise-linear, continuous) regression of ln(age-adjusted rate)
on year, D76 1999–2020, with a single breakpoint fixed **a priori at 2018**. The
pre-specified candidate breakpoint set is {2017, 2018, 2019}; 2018 is primary (the
published NCHS peak year for the age-adjusted suicide rate); 2017 and 2019 are
sensitivity S4. The breakpoint is never fitted freely. Model:
ln(rate) = β₀ + β₁·(year − 2018) + β₂·max(0, year − 2018) + ε.

**Decision rule.** Confirmed if BOTH: β₁ (pre-break slope) is positive with 95% CI
excluding 0, AND β₂ (slope change) is negative with 95% CI excluding 0. Refuted if
β₁'s CI lies below 0 or β₂'s CI lies above 0. Inconclusive otherwise. (Only 2 data
points lie after the 2018 break in D76; the post-break slope is therefore imprecise —
acknowledged as a limitation. The D158 series (2018 onward) is presented descriptively
alongside as an external consistency check, never spliced.)

### Descriptive (pre-specified, not hypothesis tests)

Sex-specific and 10-year-age-group-specific rates for Series A, A1, A2, B by year,
both databases; sex-specific AAPCs (same method as H1) reported with CIs as
descriptive estimates.

## 6. Statistical toolkit (defaults; deviations require logged rationale)

- Trend magnitude: log-linear OLS on age-adjusted rates → AAPC with 95% CI (as H1).
- Count models: Poisson with population offset; negative binomial if Pearson χ²/df > 2
  (dispersion statistic reported either way).
- Trend change: segmented regression, breakpoint a priori (as H3).
- All models' complete outputs saved as text files in `analysis/`. **No number may
  appear in the manuscript that is not present in a saved output file.**

## 7. Pre-specified sensitivity analyses

| ID | Analysis |
|----|----------|
| S1 | Alternative case definitions: repeat H1 with A′ replacing the A-family series it concerns (A1 is unchanged in A′; therefore S1 for H1 applies the H1 method to Series A and A′ to test chapter-level robustness); repeat H3 with B′. |
| S2 | Exclude 2020 onward (COVID-era certification effects): refit H1, H2, H3 on 1999–2019. For H3 this leaves one post-break year (2019); the slope-change term is then estimable only degenerately and is reported with that caveat. |
| S3 | Cross-database consistency: for 2018–2020, compare D76 vs D158 national deaths and age-adjusted rates for Series A, A1, A2, B (all-race totals only). Report absolute and percentage differences. Expectation: death counts agree to within ~1% (same underlying certificates); rates may differ slightly more (different denominator series). Material divergence (>2% in counts) triggers investigation and is reported prominently. |
| S4 | H3 with breakpoints 2017 and 2019 (the rest of the candidate set). |

## 8. Suppression and reliability plan

WONDER suppresses death counts 1–9 (and corresponding rates) and flags rates based on
counts < 20 as "Unreliable". Plan:

1. Queries are designed at coarse aggregation (national; year × sex or year × 10-year
   age at most; chapter/block-level code groups) precisely to keep suppression
   minimal.
2. Cleaning parses "Suppressed"/"Unreliable"/"Not Applicable" markers into explicit
   boolean flag columns — never into missing values or zeros.
3. QC audits **every** suppressed or unreliable cell: counts and percentages by query
   and stratum, reported as a table in `qc/qc_report.md` and summarized in the
   manuscript.
4. Suppressed cells are never imputed, estimated, or hand-patched. Analyses use only
   unsuppressed cells; any stratum excluded for suppression is named in DECISIONS.md.
   The shortfall that suppression induces in stratum sums vs published totals is
   quantified in QC.

## 9. Planned queries (assembled tables come from cleaning, not from the requests)

Per database (D76; D158 analogously for its year range): for each of Series A, A1,
A2, B — (i) year totals with deaths, population, crude and age-adjusted rate;
(ii) year × sex, same measures; (iii) year × 10-year age groups with deaths,
population, crude rate. Plus, per database: all-cause deaths by year (QC benchmark
and denominator check), and Series A and A′ year totals for S1. Exact request XML for
every query is stored verbatim in `raw/queries/`, responses in `raw/responses/`,
indexed in `raw/manifest.csv`; `raw/` is append-only.

## 10. External QC benchmark

Total U.S. deaths for at least one year cross-checked against a figure published on
www.cdc.gov (page fetched and saved to `references/sources/` during this run).

## 11. Integrity rules binding the analysis

- Every number in every output must be traceable to a raw file fetched from CDC WONDER
  during this run (claims_map.csv provides the trace).
- Nothing outside §5 is confirmatory. Anything else is exploratory and labeled so.
- If data cannot be fetched, the run enters Degraded Mode (no results, no figures, no
  numbers; protocol + pipeline + Methods-only manuscript), per the operating contract.
