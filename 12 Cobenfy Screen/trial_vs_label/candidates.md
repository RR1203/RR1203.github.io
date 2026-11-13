# Candidates: trial AEs missing from the Cobenfy label

## Result of the pre-specified rule: **0 candidates**

Rule: pooled EMERGENT-1/2/3 Cobenfy rate > placebo, MH risk-difference lower 95% bound > 0 (available-case **and** unreported-as-zero), and label status "Missing" or "Mentioned elsewhere".

Every PT or grouped term with a lower bound > 0 is already in label Table 1: nausea, vomiting, dyspepsia, constipation, hypertension, dry mouth, GERD, vision blurred. Headache, the negative control, was not flagged: 10.9% vs 10.2%, RD 0.67 (−3.92 to 5.25). This is a clean negative screen, but its power is low. Public trial reports list only terms above 2% (EMERGENT-1/2) or 5% (EMERGENT-3), so rarer events cannot be tested. Source: `data/h3_screen_results.xlsx`, `analysis.Rmd` H3.

No grouped term met the "understated" rule (H3.2).

---

## Best near-miss (post hoc): Sweating / hyperhidrosis

It fails the trial rule, but it is the only event with all four of: trial signal, label gap, FAERS confirmation, and mechanism.

| Evidence | Numbers | Source |
|---|---|---|
| RCT, EMERGENT-1 | 2/89 (2.2%) vs 1/90 (1.1%); RD 1.14 (−2.63 to 4.90) | CT.gov NCT03697252; NEJM 2021 Table 3 (identical) |
| RCT, EMERGENT-2 | not reported, so ≤2% in each arm | CT.gov NCT04659161 (threshold 2%) |
| RCT, EMERGENT-3 / UNITE-001 / ARISE | not reported, so ≤5% in each arm | CT.gov (threshold 5%) |
| 52-week open-label EMERGENT-5 | 29/566 (5.1%; Wilson 3.6–7.3) | CT.gov NCT04820309; Kaul 2026 abstract (PMID 41506001) says 5.1% |
| Xanomeline alone vs combo (phase 1, healthy volunteers) | sweating 16/33 (48.5%) vs 7/35 (20.0%) | Breier 2023, PMC10102054, Table 3 |
| Xanomeline alone, Alzheimer's (Bodick 1997, 225 mg/d) | placebo-adjusted 71% | cited in PMC10102054 Table 5 |
| **US label** | **Section 10 (Overdosage) only**, "hyperhidrosis" as a cholinergic overdose sign; absent from 6.1 and 6.2; unchanged since v1 (2024-09-26) | DailyMed SPL v1–v6 |
| FAERS vs newer APs (main) | 99 vs 95 reports; ROR 3.79 (2.85–5.03); IC025 0.87 | `data/h4_faers_results.xlsx` |
| FAERS vs newer APs (HCP only) | 26 reports; ROR 2.34 (1.48–3.70) | same |
| FAERS vs all APs | ROR 4.49 (3.63–5.56); IC025 1.64; HCP lower bound 1.79 | same |
| FAERS grouped "Sweating" (hyperhidrosis, cold sweat, night sweats) | 118 reports; ROR 3.47 (2.69–4.48); HCP 2.44 (1.61–3.70) | same |
| Pilot replication (vs lumateperone alone) | 99 vs 41; ROR 3.47 (2.41–5.02) | `raw/pilot_check.txt` |

**FAERS status:** confirmed (lower bound > 1 in the main and the HCP analysis).
**Novelty: partly known.**
- Bao 2026 (Neurotherapeutics, PMC13234482, Table 3) reported hyperhidrosis, 46 cases, ROR 10.56 (7.89–14.14) against all of FAERS. It filed hyperhidrosis among events "aligned with AEs listed on the drug label" and flagged only cold sweat as unlabelled.
- Leppien 2026 (PMC13639622) reported 62 cases, ROR 11.72 (9.11–15.07).
- EMERGENT-5 reports 5.1%.
- Sweating is the classic xanomeline effect that trospium only partly blocks.
- **Not found in the literature:** that the US label lists hyperhidrosis only as an overdose sign, and the FAERS signal against active antipsychotic comparators with HCP-only confirmation.

## Second near-miss: Weight decreased / decreased appetite

| Evidence | Numbers | Source |
|---|---|---|
| EMERGENT-1 decreased appetite | 2/89 vs 0/90; RD 2.25 (−0.83 to 5.33) | CT.gov / NEJM |
| UNITE-001 (China) weight decreased | 21/102 vs 16/98 | CT.gov NCT05919823 |
| "Weight" group, EMERGENT-1 + UNITE-001 | RD 5.29 (−1.12 to 11.71) | `pooled_ae.csv` |
| EMERGENT-5 weight decreased | 32/566 (5.7%; 4.0–7.9) | CT.gov; abstract 5.7% |
| Label | **Missing** (only "loss of appetite" as a symptom of liver problems in the Medication Guide) | SPL v6 |
| FAERS weight decreased vs newer APs | 62 reports; ROR 2.18 (1.58–2.99); HCP 1.56 (0.86–2.83) | `h4_faers_results.xlsx` |

**FAERS status:** not confirmed at PT level (the HCP lower bound is below 1). The "Weight" group passes (HCP lower bound 1.03). **Novelty:** not found as a flagged signal in the retrieved FAERS papers. EMERGENT-5 reports it. Weak; treat as a lead only.

## Presentation note (not a candidate)
Drooling is in label Table 1 only inside the "EPS, non-akathisia" footnote, not with salivary hypersecretion. In FAERS, drooling (57 reports; ROR 6.04, 3.94–9.25) outnumbers salivary hypersecretion (41). Trial data cannot test this, because drooling was not reported above threshold in any trial.

## Events Cobenfy is *less* often reported for in FAERS (for context)
Akathisia ROR 0.11, mood group 0.30, headache 0.56 (vs newer APs).
