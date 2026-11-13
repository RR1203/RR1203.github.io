# Decisions log

Choices made without asking, as instructed. Each line: decision, and why.

## Sources
1. **Drugs@FDA (NDA 216158) review and label PDFs not retrieved.** `www.accessdata.fda.gov` returned an "abuse-detection / excessive requests" page (HTTP 404) to scripted downloads; the web-fetch tool could not resolve the host. I did not try to bypass the bot block. All label versions were taken from DailyMed instead (SPL versions 1, 3, 4, 5, 6; setid 8f0e73bf-6025-44f6-ab64-0983322de0df). DailyMed has no SPL version 2.
2. **EMERGENT-2 Lancet paper, pooled safety paper (Kaul 2025 J Clin Psychiatry), EMERGENT-4/5 full papers: not open access.** Only PubMed abstracts used (EMERGENT-5 abstract gives % for TEAEs ≥5%).
3. **Bodick 1997 (xanomeline alone, Alzheimer's): full text not accessible.** Used the abstract plus the placebo-adjusted rates that Breier 2023 (PMC10102054, Table 5) cites from Bodick. Marked "secondary citation" in `trial_ae_long.csv`.
4. Network access to FDA, DailyMed and FAERS hosts required a new personal cloud environment (approved at the session start); no credentials were used.

## Trial data
5. **ClinicalTrials.gov is the primary count source.** It is the only source with full per-arm counts for all trials. Journal tables were used for cross-checks.
6. **'Other' + 'serious' counts summed per PT.** CT.gov lists serious events separately from non-serious ones. Summing can double-count a patient who had both. In EMERGENT-5 this over-counted dizziness and dyspepsia by 1 patient each, compared with the paper abstract (S2).
7. **Reporting thresholds differ:** EMERGENT-1 and -2 used 2%, EMERGENT-3, UNITE-001, ARISE and EMERGENT-4/5 used 5%. A term missing from a trial is "below threshold in both arms", not zero. **Primary pool = available-case** (a trial contributes only to terms it reports). **Sensitivity = unreported treated as 0 in both arms.** A candidate must have a lower bound > 0 in **both**.
8. **Pools:** primary = EMERGENT-1/2/3 (as specified). Label positive controls use EMERGENT-2+3, because label Table 1 is the pool of these two trials (N = 251/253 = 126+125 / 125+128). Sensitivity: EMERGENT-1/2/3 + UNITE-001 (China, 5-week, placebo-controlled). ARISE (adjunctive) is pooled only in `pooled_ae.csv`, not in the main screen.
9. **Grouped-term count = sum of member PTs within a trial arm, capped at n.** Patient-level overlap is unknown. Sensitivity: largest single member.
10. **Term groups:** the prompt's lists were mapped to MedDRA PTs. A few direct synonyms were added (sinus tachycardia, BP orthostatic decreased, sedation, dystonia); these are marked "added" in `term_groups.csv`. Label-footnote groups (a–f) were added to reproduce label Table 1.
11. **MH risk difference:** MH weights n1·n0/(n1+n0), Sato/Greenland–Robins variance, no continuity correction (RevMan / metafor `rma.mh` formula). Implemented twice: Python (`scripts/05_pool.py`) and R (`analysis.Rmd`). The two agree to ≤0.005 percentage points, which is rounding.
12. **Long-term studies:** exposure time (patient-years) is not in any retrieved source, so incidence per 100 patient-years could **not** be computed. Crude cumulative incidence with Wilson CI is reported instead. Time pattern is also not available.

## Label
13. **Label status categories:** "Listed (6.1 Table 1)" includes footnote member terms. "Listed (6.1 text, not Table 1)" covers the 6.1 narrative (liver enzymes, urinary retention). "Mentioned elsewhere" covers 5.x, 6.2 and 10. The candidate rule treats 6.1 narrative as inside 6.1 (not a candidate).
14. A group's label status is the best status among its members.
15. **"Understated" rule:** group % ≥ 1.5× and ≥ 2 percentage points above the largest Table 1-listed member, with at least one member that is not itself a Table 1 term. Groups made only of listed PTs (e.g. "Cholinergic GI") are not flagged.
16. Every label mapping is checked automatically. `scripts/06_label_status.py` confirms each cited wording appears in the cited section; there were 0 failures.

## FAERS
17. Quarters 2024Q3–2026Q3 (9 files, latest available on 2026-11-13). Dedup: latest `caseversion` per `caseid` across all quarters (ties: latest `fda_dt`, then highest `primaryid`). Then caseids on any quarterly DELETE list are dropped.
18. **Exposure:** Cobenfy as primary or secondary suspect (PS/SS). **Comparator:** a comparator antipsychotic as PS/SS, and Cobenfy absent in any role. A Cobenfy case that also names a comparator stays in the Cobenfy group.
19. "All antipsychotics" = ATC N05A agents excluding lithium and antiemetic-only agents (prochlorperazine, promethazine, droperidol, metoclopramide). Pimavanserin is included (N05AX17).
20. Health professionals = `occp_cod` MD, PH, OT or HP.
21. ROR (Woolf CI) is set to NA when a cell is 0. IC uses Norén's shrinkage: log2((a+0.5)/(E+0.5)), and IC025 = IC − 3.3(a+0.5)^−½ − 2(a+0.5)^−3/2. E is computed within each Cobenfy-plus-comparator dataset.
22. **No trial candidate qualified, so FAERS was run on every PT and grouped term** (153 events). This shows how the near-misses behave in FAERS and checks the controls. The FAERS rule ("confirmed" = ROR lower bound > 1 in the main and the health-professional analysis vs newer antipsychotics) was applied unchanged.

## Code
23. House-style questions (robustness choices, figures, ANOVA) were not asked, per "do not ask". Decisions: robustness = items 7–9; figures = two forest plots; ANOVA not applicable.
24. FAERS clean data are saved as `.csv.gz`, not Excel (>500k rows). Raw FAERS quarterly files (~2 GB unzipped) are not in the repo; scripts 07–08 rebuild the extracts.
25. Bugs found and fixed during the run: a footnote-stripping regex removed real final letters ("Nausea" → "Nause"); "6.1 text, not Table 1" matched a "Table 1" test; a GGT term failed to map in S2; infinite RORs were written to Excel as text. All are fixed, and the outputs were re-knitted.
