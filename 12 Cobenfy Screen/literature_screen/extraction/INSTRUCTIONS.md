# Extraction instructions (identical for every batch)

Input: extraction/batch_N.json — a JSON list of PubMed records. Each record has pmid, title, abstract, pubtypes and `screen_for`: the condition(s) whose search retrieved it.

Task: READ EACH ABSTRACT IN FULL (never judge from the title). For every (record × condition in screen_for) write ONE JSON object per line to extraction/out_N.jsonl with these keys:

- pmid (string), condition (the condition key from screen_for)
- relevant (true/false): true only if the abstract itself reports data (or a systematic review/meta-analysis of data) linking cholinergic / muscarinic signalling to THIS condition. Narrative reviews, protocols with no results, and abstracts about a different disease = false.
- evidence_type: one of
  "1_human_pharm" (human trial/study of a muscarinic agonist, cholinesterase inhibitor, scopolamine challenge, or anticholinergic DRUG TRIAL used as treatment),
  "2_anticholinergic_burden" (observational: anticholinergic burden/exposure vs risk/severity of the condition),
  "3_genetics" (CHRM1-5 variants, expression QTL, Mendelian randomization),
  "4_postmortem_imaging" (human postmortem/PET/SPECT receptor binding, ChAT, VAChT, basal forebrain),
  "5_animal" (non-human in vivo or in vitro),
  "6_clinical_obs" (case report/series, or any clinical data with xanomeline / KarXT / Cobenfy specifically)
  Assign by what the study actually is, not by the query bucket. Any human trial of xanomeline/KarXT/Cobenfy → "1_human_pharm" AND set xanomeline_tested=true.
- direction: from the perspective "would MORE brain M1/M4 cholinergic signalling help this condition?"
  "helps" = increasing cholinergic/muscarinic signalling improves the condition, OR reducing it (anticholinergic burden, scopolamine, receptor/ChAT loss, loss-of-function variant) worsens, causes or associates with it.
  "harms" = increasing cholinergic signalling worsens the condition (e.g. ChEI or agonist causes/worsens it), OR anticholinergics improve it, OR more cholinergic tone is pathogenic.
  "null" = properly tested, no effect / no association.
  "unclear" = relevant but direction cannot be determined.
  For irrelevant rows use "na".
- drug_or_exposure: short (e.g. "donepezil", "xanomeline", "ACB score", "CHRM2 rs...")
- study_type: RCT / open-label / crossover / cohort / case-control / cross-sectional / case report / case series / meta-analysis / postmortem / PET / GWAS / MR / animal / in vitro / other
- n: integer human sample size if stated, else null (animals: null)
- xanomeline_tested: true if xanomeline, KarXT, Cobenfy or xanomeline-trospium was given for THIS condition (or its symptoms) in humans
- peripheral: true if the effect is mainly peripheral (gut, bladder, salivary, airway, heart) rather than brain
- finding: ONE line, ≤25 words, factual, from the abstract (include effect direction and key number if present)

Rules: Do not use outside knowledge to fill in results. If the abstract is missing, mark relevant=false and finding "no abstract". Output must be valid JSONL (one object per line, no comments). Check the line count equals the number of (record × screen_for) pairs before finishing.
