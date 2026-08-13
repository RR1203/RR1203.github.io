DRAFT — machine-generated overnight; requires author verification before any use.

# Psychiatric-cause mortality in the United States, 1999 to the latest available year: trends in underlying-cause death certificates from CDC WONDER

## Plain-language summary

We planned a national study of deaths in the United States for which a psychiatric
condition — a mental or behavioural disorder, or intentional self-harm — was recorded
as the underlying cause on the death certificate. Using two public CDC WONDER
databases, the study asks whether such deaths became more common between 1999 and the
most recent available year, whether deaths tied to alcohol and drugs (substance-induced
disorders) rose faster than other psychiatric deaths, and whether the long rise in
suicide mortality reversed in the late 2010s. **In this overnight run the analysis
could not be executed: the computing environment's network policy blocked all access
to CDC servers, so no data could be obtained. This document therefore contains the
study's introduction and methods only — no results. Every part of the analysis
pipeline is written, tested, and ready to run the moment CDC WONDER is reachable.**

## Introduction

Deaths assigned to mental and behavioural disorders (ICD-10 chapter F) or to
intentional self-harm sit at the intersection of two major public-health narratives of
the past quarter-century in the United States: the rise of drug- and alcohol-related
mortality [REF NEEDED: prior literature on US drug/alcohol mortality trends], and the
long increase — and recent inflection — of suicide mortality [REF NEEDED: NCHS or
peer-reviewed reports on US suicide trends through the 2010s and their post-2018
decline]. Within the F chapter itself, recorded mortality is heterogeneous: deaths
attributed to substance-induced disorders (F10–F19) concentrate in working-age adults,
while the non-substance remainder is dominated by organic disorders — chiefly dementia
(F01, F03) — in the elderly, whose recorded mortality is known to be sensitive to
secular changes in death-certification practice [REF NEEDED: studies of dementia
coding changes on US death certificates].

Aggregate death-certificate series cannot support causal or individual-level
inference, but they are the only national, complete-coverage record of mortality
assigned to psychiatric causes, and they are publicly queryable through CDC WONDER
[CDC WONDER API documentation; see Data availability]. This brief report pre-registered
three falsifiable hypotheses about these series — before any data were requested — and
tests them with simple, fully scripted models: that substance-induced psychiatric
mortality rose on average over 1999–2020 (H1); that it rose faster than non-substance
psychiatric mortality (H2); and that the intentional self-harm trend broke downward at
a pre-specified 2018 breakpoint (H3).

## Methods

### Design and data sources

National-level ecological (aggregate) study of underlying-cause-of-death data for the
United States, from two CDC WONDER databases: D76 (Underlying Cause of Death,
1999–2020, bridged-race population denominators) as the primary series, and D158
(Underlying Cause of Death, 2018 through the latest available final year, single-race
denominators) as an extension series. Because the two databases use different race
methodologies and different population denominator series, they are never spliced into
a single series; all analyses treat them as two series, and their 2018–2020 overlap is
used as a built-in cross-database consistency check. The WONDER public API serves
national data only; no sub-national analyses were planned.

The complete study protocol (`00_protocol.md`) was written and committed to version
control before the first data request, and the analysis tests nothing that is not in
it. All data handling is scripted end-to-end (fetch → clean → quality control →
analysis → figures/tables), with every query's exact request and untouched response
retained under `raw/` and indexed with SHA-256 checksums.

### Case definitions (underlying cause, ICD-10)

- **Series A** — all mental and behavioural disorders: F01–F99.
- **Series A1** — substance-induced mental and behavioural disorders: F10–F19.
- **Series A2** — non-substance mental and behavioural disorders: F01–F09 and F20–F99.
- **Series B** — intentional self-harm: X60–X84 plus Y87.0 (and U03 where selectable),
  following the NCHS injury-mortality definition of suicide.

Pre-specified alternative definitions for sensitivity analysis: A′ = F10–F99
(excluding organic disorders F01–F09, the dementia-dominated block), and
B′ = X60–X84 only.

### Measures and strata

Deaths, population, crude rates, and age-adjusted rates per 100,000 (2000 U.S.
standard population; rates as computed by WONDER) by calendar year, sex, and 10-year
age group. Within age groups the age-specific (crude) rate is the rate measure.
Race/ethnicity was not part of the confirmatory design. WONDER suppresses counts of
1–9 and flags rates based on fewer than 20 deaths as unreliable; suppressed cells are
parsed into explicit flags, audited, excluded from analysis, and never imputed.

### Statistical analysis

All models were pre-registered with exact decision rules (protocol §5). Trend
magnitude: ordinary least squares regression of the natural log of the age-adjusted
rate on calendar year; the average annual percent change (AAPC) is 100·(exp(β)−1),
with 95% confidence intervals from OLS (Newey–West lag-1 intervals also reported).
H1 applies this to Series A1 (D76, 1999–2020) and is confirmed if the AAPC's 95% CI
lies entirely above zero. H2 fits a Poisson regression of annual death counts on
year × category (A1 vs A2) with log-population offset, replaced by negative binomial
(NB2) if the Pearson dispersion statistic exceeds 2; it is confirmed if the
interaction — the difference in annual log-rate growth — is positive with 95% CI
excluding zero. H3 fits a continuous piecewise-linear ("segmented") regression of the
log age-adjusted self-harm rate with a single breakpoint fixed a priori at 2018 (from
the pre-specified candidate set {2017, 2018, 2019}); it is confirmed if the pre-break
slope is positive and the slope change negative, each with 95% CI excluding zero.
Pre-specified sensitivity analyses: the alternative case definitions (S1); exclusion
of data year 2020 onward, for COVID-era certification effects (S2); the D76 vs D158
overlap comparison, with divergence in death counts above 2% treated as a flag for
investigation (S3); and the alternative breakpoints (S4). Two-sided α = 0.05
throughout; no multiplicity adjustment across the three-hypothesis family. Analyses
use Python 3.11 with statsmodels; exact package versions are pinned in
`requirements.txt`.

### Data integrity and reproducibility

Every number in this report must be traceable, via `claims_map.csv`, from the
manuscript to a produced table or figure, to a saved model-output file, to the
generating script, and to the raw query id of the CDC WONDER response it derives from.
A single command (`./run_all.sh --skip-fetch`) rebuilds all data products, analyses,
figures and tables from the committed raw responses without network access.

### Status of this run

No data section, results, discussion, figures, or tables appear in this draft because
none could be produced: at execution time (2026-08-13, 05:52–08:52 UTC) the
environment's egress network policy refused all connections to wonder.cdc.gov and
www.cdc.gov (HTTP CONNECT rejected with 403 by the managed proxy, verified across
repeated scheduled retry cycles; evidence in `logs/connectivity_probe.jsonl` and
`DECISIONS.md` §4). Per the pre-committed operating contract, no number may be
estimated, simulated, or filled in from any source other than CDC WONDER responses
fetched during the run — so this draft stops at Methods. The pipeline was validated
end-to-end against clearly labeled synthetic fixtures (which never enter the data or
output directories); `MORNING_README.md` documents the single command that completes
the study once CDC servers are reachable.

## Limitations (of the planned design)

This is an ecological, aggregate design: it supports no individual-level or causal
inference. Underlying-cause certification captures only deaths where the psychiatric
condition was judged the underlying cause; psychiatric conditions as contributing
causes are not counted, and certification practices — including dementia coding and
drug-intoxication attribution — changed secularly over 1999–2024 [REF NEEDED:
certification-practice change literature]. Small-cell suppression removes counts of
1–9 (and flags rates under 20 deaths), which biases finely stratified series and is
why analysis strata were kept coarse. The bridged-race (D76) and single-race (D158)
databases are incompatible in race methodology and denominators; they are reported as
separate series, and race-stratified estimates were excluded from the confirmatory
design. If data year 2020 and later are included, COVID-era certification effects may
distort trends, which the pre-specified S2 sensitivity analysis addresses. Finally,
with D76 ending in 2020, the pre-registered 2018 breakpoint for H3 leaves only two
post-break years in the primary series, limiting the precision of the post-break
slope.

## Data availability

All raw API requests and untouched responses are retained under `raw/` (empty in this
blocked run), with SHA-256 checksums. CDC WONDER technical documentation could not be
fetched during this run (network blocked); citations to it are therefore given as
placeholders: [REF NEEDED: CDC WONDER API documentation page, wonder.cdc.gov/wonder/help/WONDER-API.html,
with access date] and [REF NEEDED: D76/D158 database documentation pages with access
dates]. No literature citations appear in this draft except as [REF NEEDED]
placeholders for the author to fill.
