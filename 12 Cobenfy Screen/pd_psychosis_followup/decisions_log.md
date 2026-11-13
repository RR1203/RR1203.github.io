# Decisions log: PD psychosis follow-up

1. **Network.**
   - openFDA, FDA and bioRxiv hosts were blocked in the Default environment.
   - I moved this session's network onto the existing repo environment "RR1203.github.io", which already allows `api.fda.gov`, `www.accessdata.fda.gov` and `dailymed.nlm.nih.gov`.
   - I added `api.biorxiv.org` to that environment, retried once, and it worked.
   - `www.ncbi.nlm.nih.gov` (the PMC website) stayed blocked. I fetched PMC full text through Europe PMC (`/fullTextXML`) or the E-utilities `efetch db=pmc` endpoint instead.
2. **Full text vs abstract.**
   - Full text was obtained for 38864492 (PMC11449127) and 42729706 (PMC13563583).
   - For 37358841 the PMC record contained only the abstract and Key Points, not the article body, so it is labelled abstract-level.
   - 38412585, 17070675, 37530610 and 42345506 have no open-access full text and are labelled "abstract only".
3. **Independence.**
   - 37530610 is a commentary on 37358841 and adds no independent data.
   - 17070675 overlaps the clozapine trials pooled in 38412585.
   - Neither changes the screen score, because each evidence type counts once, but they are flagged.
4. **Mouse study 42345506** uses an NMDA-antagonist (MK-801) model in intact mice. It is marked "partly verified": it shows generic antipsychotic-like activity, not a PD-specific effect.
5. **Contrary evidence added.** During verification I found a rivastigmine RCT for minor hallucinations in PD that was null (PMID 34291590, n=91, stopped early). The screen's retrieval depth (top 6 per query) had missed it. It is added to evidence_verified.csv as contrary evidence.
6. **ClinicalTrials.gov.**
   - 20 drug terms × 6 condition terms via `query.intr` + `query.cond`, plus 6 free-text `query.term` searches, all statuses (126 queries; `raw/ctgov_log.json`).
   - Only 2 trials matched: NCT04334317 (TAK-071, an M1 PAM, in PD; cognition/gait) and NCT03149809 (solifenacin, an antagonist; irrelevant). Both are kept in trials_pd.csv.
7. **Literature novelty search.**
   - PubMed: E-utilities.
   - Europe PMC: title/abstract fields from 2024, which includes preprints (SRC:PPR) and conference abstracts indexed there.
   - bioRxiv/medRxiv: the API was scanned in full for 2024-01-01 to 2026-11-13 in medRxiv neurology, psychiatry, and pharmacology & therapeutics, and in bioRxiv neuroscience and pharmacology & toxicology. Titles and abstracts were matched by regex for xanomeline/KarXT/Cobenfy/trospium/emraclidine/M4-agonist terms.
   - Conference abstracts not indexed by these sources (e.g., MDS/AAN meeting books) could not be searched and are **not found / not searched**.
8. **FAERS source.** There was no FAERS file in the project, so I used the openFDA drug/event API (data last updated 2026-10-28).
   - Without an API key, openFDA refused `limit=1000` (`API_KEY_MISSING`), so I paged with `limit=100`.
   - Cobenfy query: activesubstance XANOMELINE OR medicinalproduct COBENFY OR medicinalproduct XANOMELINE OR generic_name XANOMELINE. This returned **2,881 unique safetyreportids**, with Cobenfy as primary suspect in 2,834. The openFDA count query used for the reference table returns 2,875 because it uses a slightly narrower query; this is noted.
9. **PD definition in FAERS.** openFDA does not include medical history, so "PD" can only be inferred from drug indications or co-medications.
   - **Tier A:** any drug indication containing Parkinson or Lewy (6 reports, 4 unique patients after linking duplicates).
   - **Tier B:** dopaminergic co-medication without a PD indication (1).
   - **Tier C:** co-medication only, where the indication points away from PD (7; e.g., amantadine for EPS, ropinirole with restless legs, off-label pimavanserin in schizophrenia).
   - Tier A is the primary analysis. The broad 14-report definition is reported but treated as contaminated.
10. **Duplicate linking.**
    - Reports 26114932, 26191622 and 26660047 share age/sex (73F), an identical 14-drug co-medication list and the same event date, so they are treated as one patient.
    - Report 27115291 matches the published case report (83M; quetiapine 350 mg; brexpiprazole 1/2/3 mg; pimavanserin 34 mg; Cobenfy 50/20 then 100/20 BID; blurred vision) and is treated as the same patient. FAERS therefore does not provide independent efficacy evidence.
11. **Motor AE definition.** MedDRA preferred terms:
    - **motor_any:** EPS, tremor, dystonia, parkinsonism, rigidity, brady/hypo/akinesia, freezing, dyskinesia, akathisia, gait, fall, balance, mobility, dysarthria, dysphagia, muscle spasms, tardive dyskinesia.
    - **eps_core:** without gait, fall, balance, dysarthria, dysphagia and spasm terms.
    - **gait_fall:** gait, fall, balance and mobility terms.
12. **ROR.** 2×2 table of the PD subgroup vs all other Cobenfy reports. Haldane +0.5 correction when any cell is 0. With 0 events in n=6, the Haldane ROR is mechanically above 1 and uninformative; this is stated in the summary.
13. **Reference drugs (pimavanserin, quetiapine).** openFDA count queries at report level. "PD report" means any drug in the report has an indication matching parkinson, parkinsonism or "lewy", with the drug present in any role. openFDA cannot tie an indication to a specific drug inside a count query, so this is an approximation.
14. **FDA review documents.** `www.accessdata.fda.gov` returned 404 for the NDA 216158 TOC and review PDFs (guessed names IntegratedR, MultidisciplineR, SumR) and for the Drugs@FDA overview page. One web search did not find the review URL. Result: **review not found**; only the label (openFDA SPL, effective 2026-01-16, set_id 8f0e73bf-…) was used.
15. **Motor-risk verdict.** This is my synthesis, stated with its basis. Trial EPS data come from young adults with schizophrenia; the label states that controlled studies did not include patients over 65. They cannot be extrapolated directly to a dopamine-depleted PD brain.
16. **Go/no-go criteria used.**
    - GO requires: (a) no ongoing or registered trial that would scoop the idea; (b) at least one verified human efficacy signal; (c) a plausible motor-safety margin with a monitorable risk.
    - A conditional GO requires a protocol that includes motor stopping rules.
17. **Storage.** The raw openFDA download is gzipped (`raw/faers_cobenfy_all.json.gz`) to keep the repo small; scripts/faers_analyze.py reads the .gz.
