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
- Secondary hypotheses (H2, H3): Holm correction across the secondary key-term p-values
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

### Exploratory [PROPOSED]
- E1. Prevalence of each of the 6 categories, overall and by area
- E2. Blanket vs qualified exclusions: share of psychiatric exclusion bullets that also mention compliance/consent/"interfere"
- E3. Trials with US sites vs without

## Deviations from plan
- 2026-11-13: All [PROPOSED] items were set by Claude without Hannes's review, before any outcome data were analysed. They still need confirmation.
- 2026-11-13: H2 was fitted with a 0/1 industry indicator (industry vs government + other) instead of the 3-level sponsor_class. Reason: the key term must be a single contrast.
- 2026-11-13: The classifier was not tuned after validation. Missed phrasings ("psychological, familial, sociological or geographical condition", "toxicomania") are reported as a limitation. Tuning on the validation set would bias the accuracy estimates.
