**FLAG:** The pre-specified screen found **0 candidates**. Public trial reports list only terms above 2% (EMERGENT-1/2) or 5% (EMERGENT-3), and the FDA review could not be retrieved. So events below those thresholds could not be tested in the trials.

# 1. What the code did

**Sources retrieved**
1. ClinicalTrials.gov API v2 search — xanomeline / KarXT / Cobenfy → 54 studies, 9 with posted results; full records saved → `raw/ctgov/*.json`
2. Parsed `adverseEventsModule` (serious + other, every term, every arm) — 9 studies → `raw/ctgov_ae_long.csv` (407 rows)
3. Europe PMC / PubMed search and open-access full texts — EMERGENT-1 NEJM (PMC7610870), EMERGENT-1 safety (PMC9719488), EMERGENT-3 JAMA Psychiatry + supplement (PMC11063924), phase 1 xanomeline vs combo (PMC10102054), FAERS papers (PMC13234482, PMC13639622), NMA (PMC13435969); abstracts of 18 non-open papers → `raw/europepmc/`, `raw/pubmed/`
4. DailyMed label — current SPL v6 (2026-08-21) and every version (v1, v3, v4, v5, v6) → `raw/label/`
5. FAERS quarterly ASCII files — 2024Q3–2026Q3 (9 quarters) → scratchpad (≈2 GB, not in repo)
6. **Not retrieved:** Drugs@FDA review and label PDFs (site returned a bot-block page); full texts of EMERGENT-2 (Lancet), pooled safety (J Clin Psychiatry), EMERGENT-4/5 papers, and Bodick 1997 (abstracts only).

**Processing** (scripts in `scripts/`, analysis in `analysis.Rmd`)

7. Built long table — CT.gov + journal tables (EMERGENT-1 Table 3, EMERGENT-3 Table 2, phase 1 Table 3, Bodick via Table 5) + label Table 1 + EMERGENT-5 abstract → `trial_ae_long.csv` (520 rows)
8. Defined grouped terms — 17 clinical groups + 5 label-footnote groups, 81 PT rows → `term_groups.csv`
9. Classified label status for 135 PTs, with each cited wording checked against the label text (0 failures) and first label version recorded → `label_status.csv` (42 listed, 18 mentioned elsewhere, 75 missing; all labelled content present since v1)
10. Pooled EMERGENT-1/2/3 — MH risk difference, Sato variance, no continuity correction, available-case; also unreported-as-zero, EMERGENT-1/2/3 + UNITE-001, label pool EMERGENT-2+3, ARISE, and largest-member group count → `pooled_ae.csv` (401 rows), `data/h2_pooled_results.xlsx`; Python and R implementations agree to ≤0.005 pp
11. Positive controls — EMERGENT-2+3 crude % vs label Table 1 → H1 tables
12. Candidate screen — lower bound > 0 in both missingness methods + label status Missing/Mentioned elsewhere → `data/h3_screen_results.xlsx`
13. FAERS extraction — antipsychotic-containing reports per quarter → `scripts/07_faers_extract.py`
14. FAERS dedup — latest caseversion per caseid (3,674,893 DEMO rows → 3,238,161 caseids), 14,555 deleted caseids removed → 3,223,606 cases; 130,953 with an antipsychotic → `data/faers_cases.csv.gz`, `data/faers_case_pt.csv.gz`
15. FAERS disproportionality — 153 events (PTs + groups); Cobenfy PS/SS (n = 2,841) vs newer APs (n = 10,060) and vs all APs (n = 99,237); HCP-only (1,203 vs 6,952 / 54,731); ROR (Woolf) and IC025 → `data/h4_faers_results.xlsx`
16. Long-term incidence — EMERGENT-4 (n = 152), EMERGENT-5 (n = 566), Wilson CI → `data/s1_longterm.xlsx`
17. Source agreement — journal tables vs CT.gov (52 count pairs, all identical); EMERGENT-5 abstract vs CT.gov (12 terms) → S2 tables
18. Audits — independent recount of FAERS from raw files (identical: 2,841 cases, hyperhidrosis 99); pilot replication vs lumateperone → `raw/pilot_check.txt`; novelty searches → `raw/novelty/`
19. Figures → `figures/forest_grouped_terms_trials.png`, `figures/forest_grouped_terms_faers.png`

**Not run:** incidence per 100 patient-years and time patterns (no exposure data in retrieved sources); urinary-retention positive control (below public reporting thresholds); extraction of FDA-review AE tables (not retrievable).

# 2. Methods and Results

**Methods.** We extracted adverse events from all 9 xanomeline-trospium studies with results on ClinicalTrials.gov, cross-checked them against published trial tables, and harmonised terms to MedDRA preferred terms. Synonyms were merged into 17 pre-specified clinical groups. For the three 5-week placebo-controlled trials (EMERGENT-1, -2, -3; 340 xanomeline-trospium, 343 placebo), we estimated Mantel-Haenszel risk differences stratified by trial, with Sato variance and no continuity correction. Registry reporting thresholds (2% in EMERGENT-1/2, 5% in EMERGENT-3) meant a term absent from a trial could not be counted. Analyses therefore used the trials reporting each term, and a sensitivity analysis set unreported terms to zero. An event was a candidate if the lower 95% bound exceeded zero in both analyses and the term was absent from the US label or appeared only outside Section 6.1 (DailyMed SPL versions 1–6). FAERS reports from 2024Q3–2026Q3 were deduplicated: we kept the latest case version and removed FDA-deleted cases. We then compared reports naming xanomeline-trospium as suspect drug with reports naming lumateperone, brexpiprazole or cariprazine (and, separately, any antipsychotic) without xanomeline-trospium. The measures were reporting odds ratios with 95% CIs and the information component (IC025), overall and in health-professional reports. Analyses used Python 3.13 and R with tidyverse.

**Results.** The pipeline reproduced label Table 1 within 1 percentage point for nausea (19.1% vs 3.6%; label 19% vs 4%), constipation (17.1% vs 7.1%; 17% vs 7%), dyspepsia (17.5% vs 4.7%; 18% vs 5%) and vomiting (15.1% vs 0.8%; 15% vs 1%). Urinary retention could not be checked because it fell below the reporting thresholds. Journal and registry counts agreed for all 52 matched pairs. In the pooled 5-week trials, eight preferred terms had a lower 95% bound above zero, and all eight are in label Table 1: nausea (RD 14.7 points, 10.1 to 19.3), vomiting (11.8, 7.9 to 15.7), constipation (10.9, 6.2 to 15.6), dyspepsia (10.6, 6.2 to 15.0), hypertension (6.8, 3.2 to 10.4), dry mouth (5.1, 1.5 to 8.8), vision blurred (4.8, 1.0 to 8.5) and gastroesophageal reflux disease (3.6, 1.3 to 5.8). No event met the candidate rule, and no grouped term met the understated rule. Headache, the negative control, did not differ (10.9% vs 10.2%; RD 0.7, −3.9 to 5.3). The strongest unlabelled near-miss was hyperhidrosis. In EMERGENT-1 it occurred in 2.2% vs 1.1% (RD 1.1, −2.6 to 4.9), it was not reported above threshold in the other trials, and it occurred in 5.1% (3.6 to 7.3) of 566 patients in the 52-week open-label EMERGENT-5. The label mentions it only as an overdose sign. In FAERS, the 2,841 xanomeline-trospium reports showed disproportionate hyperhidrosis compared with newer antipsychotics (99 reports; ROR 3.79, 2.85 to 5.03; IC025 0.87). This held in health-professional reports (ROR 2.34, 1.48 to 3.70) and against all antipsychotics (ROR 4.49, 3.63 to 5.56). Weight decreased, absent from the label, occurred in 5.7% in EMERGENT-5 and was disproportionate in FAERS (ROR 2.18, 1.58 to 2.99), but not in health-professional reports (1.56, 0.86 to 2.83). All five labelled positive controls were disproportionate in FAERS. Headache (ROR 0.56) and akathisia (0.11) were reported less often than with the comparators.

# 3. Recap

- I screened 9 trials, 6 label versions and 2,841 deduplicated FAERS reports. No trial adverse event met the pre-specified "missing from label" rule, so this is a clean negative screen, limited by the 2–5% registry reporting thresholds.
- The best unlabelled event is sweating/hyperhidrosis. In the RCTs it is weak (2.2% vs 1.1%, CI crosses 0), it reaches 5.1% in the 52-week study, and FAERS confirms it (ROR 3.79, 2.85–5.03; HCP 2.34, 1.48–3.70). The label lists it only under overdose. Novelty is partial: FAERS papers report the signal but treat it as labelled.
- Decision needed: whether to get the FDA multidisciplinary review by hand (the site blocks scripts), since its <2% tables are the only way to test rarer events.
