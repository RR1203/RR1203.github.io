# psyexcl — Analysis plan

**Preregistered:** no
**Target journal:** [PROPOSED] JAMA Psychiatry (research letter) / Lancet Psychiatry / BMJ Mental Health

## Question
How often do non-psychiatric clinical trials exclude people with mental illness, and has this changed from 2010 to 2025?

## Data
- Raw file: 03_psyexcl_raw.xlsx (ClinicalTrials.gov API v2, downloaded 2026-11-13; all interventional phase 2–4 trials with start date 2010–2025)
- Data status: existing public data; nothing analysed before this plan
- Study-wide exclusions:
  - trials with any condition in MeSH "Mental Disorders" or "Nervous System Diseases" (psychiatric/neurological trials)
  - trials without MeSH condition terms (area cannot be assigned)
  - trials whose eligibility text has no separable "Exclusion criteria" section
- Therapeutic area [PROPOSED]: from MeSH condition terms + ancestors, priority order Oncology (Neoplasms) > Cardiovascular > Metabolic/endocrine > Infectious > Respiratory > Other
- Outcome [PROPOSED]: rule-based (regex) classification of the exclusion section into 6 categories: general psychiatric/mental illness; depression; suicidality; psychosis/schizophrenia/bipolar; substance use; other (anxiety, PTSD, eating, personality, OCD). `any_psych` = any of the 6.
- Classifier validation [PROPOSED]: random sample of 200 exclusion sections labelled blind by an independent LLM reader; report sensitivity, specificity, PPV, NPV, κ for `any_psych`
- Outliers: not applicable (binary outcome)

## Inference
- H1: α = .05, two-sided
- H4 (co-primary, added later): α = .05, two-sided
- Secondary hypotheses (H2, H3, H5, H6, H7): Holm correction across the secondary key-term p-values
- Exploratory analyses: no correction; always labelled exploratory

## Hypotheses

### H1. Time trend (primary)
- Hypothesis: [PROPOSED] the proportion of non-psychiatric trials with a psychiatric exclusion decreases with start year
- Model: glm(any_psych ~ start_year + area + phase + sponsor_class, family = binomial), sample: analytic sample
- Key term: start_year (OR per year)

### H2. Industry sponsorship (secondary)
- Hypothesis: [PROPOSED] industry-sponsored trials exclude people with psychiatric conditions more often than non-industry trials
- Model: same model as H1, sponsor_class = industry vs non-industry
- Key term: sponsor_industry

### H3. Therapeutic area (secondary)
- Hypothesis: [PROPOSED] the proportion of trials with psychiatric exclusions differs between therapeutic areas
- Model: same model as H1; likelihood-ratio test of area (full vs model without area)
- Key term: area (LR χ², 5 df)

## Part B — Impact on psychiatric patients (added 2026-11-13, after H1–H3 were analysed; main question per Hannes)

- Extra raw files: 03_psyexcl_status_raw.xlsx, 03_psyexcl_results_*_raw.xlsx (ClinicalTrials.gov posted results, via 03_psyexcl_download_results.py)
- Harm sample [PROPOSED]: analytic-sample trials that are randomized, post adverse-event results, and have exactly 2 adverse-event groups: 1 experimental arm + 1 inactive control (placebo, sham or no intervention; matched to registered arm type, fallback on group title)
- Psychiatric AE per arm [PROPOSED]: participants with any adverse event in MedDRA organ system "Psychiatric disorders" (serious + other), counted as the maximum over terms (lower bound of people affected)
- Effect size: log risk ratio (RR) experimental vs control, 0.5 continuity correction; trials with zero events in both arms dropped

### H4. Psychiatric harm and exclusion (co-primary)
- Hypothesis: [PROPOSED] the psychiatric-harm RR (drug vs control) is larger in trials that did not exclude psychiatric patients than in trials that did, i.e. exclusion hides psychiatric harm
- Model: rma(log_rr, var_log_rr, mods = ~ any_psych + area + phase + sponsor_class + start_year, method = "REML"), sample: harm sample
- Key term: any_psych (ratio of RRs)

### H5. Psychiatric safety data gap (secondary)
- Hypothesis: [PROPOSED] trials that exclude psychiatric patients are less likely to report any psychiatric adverse event
- Model: glm(any_psych_ae_reported ~ any_psych + area + phase + sponsor_class + start_year + log1p(enrollment), binomial), sample: analytic-sample trials with posted adverse-event results
- Key term: any_psych

### H6. Recruitment failure (secondary)
- Hypothesis: [PROPOSED] excluding psychiatric patients does not lower the risk of stopping for poor accrual
- Model: glm(stopped_low_accrual ~ any_psych + area + phase + sponsor_class + start_year, binomial), sample: analytic sample
- Key term: any_psych

### H7. Drop-out (secondary)
- Hypothesis: [PROPOSED] drop-out is not lower in trials that exclude psychiatric patients
- Model: glm(cbind(flow_dropped, flow_completed) ~ any_psych + area + phase + sponsor_class + start_year, quasibinomial), sample: trials with participant flow
- Key term: any_psych

### Exploratory [PROPOSED]
- E1. Prevalence of each of the 6 categories, overall and by area
- E2. Blanket vs qualified exclusions: share of psychiatric exclusion bullets that also mention compliance/consent/"interfere"
- E3. Trials with US sites vs without
- E4. H4 repeated for serious adverse events (any organ system) and deaths
- E5. H4 robustness: active comparators included; sum over terms instead of max; trials with zero events in both arms kept (continuity correction)

## Deviations from plan
- 2026-11-13: All [PROPOSED] items were set by Claude without Hannes's review, before any outcome data were analysed. They still need confirmation.
- 2026-11-13: H2 was fitted with a 0/1 industry indicator (industry vs government + other) instead of the 3-level sponsor_class. Reason: the key term must be a single contrast.
- 2026-11-13: The classifier was not tuned after validation. Missed phrasings ("psychological, familial, sociological or geographical condition", "toxicomania") are reported as a limitation. Tuning on the validation set would bias the accuracy estimates.
- 2026-11-13: Part B (H4–H7, E4–E5) was added after H1–H3 had been analysed, at Hannes's request. The main question moved to the impact on psychiatric patients (H4). None of the Part B outcome data had been looked at when it was added.
