# SUMMARY: Cobenfy (xanomeline-trospium) for Parkinson's disease psychosis: follow-up

Run 2026-11-13. Every number below traces to a PMID, NCT ID, FAERS safetyreportid or a file in this folder.

## Bottom line (3 lines)
1. **Still untested and unscooped.** No registered trial of any M1/M4 agonist or PAM exists for PD psychosis, PD or Lewy body disease. The only exception is TAK-071, an M1 PAM tested for cognition and gait, not psychosis (NCT04334317). The published human evidence is one case report (PMID 42729706).
2. **The efficacy chain holds but is thin.** 5 of 7 sources verified fully, 1 partly, and 1 is not independent. The human signal rests on clozapine data (a proxy), small cholinesterase-inhibitor effects (SMD −0.08 to −0.14) and one uncontrolled case.
3. **Motor risk is real but monitorable.** Tremor worsening and blunting of levodopa are the plausible harms. Trial EPS rates are low (3.2% vs 0.9%), but those come from young schizophrenia patients. **Recommendation: conditional GO** for the 6-week open-label pilot, with motor safety as a co-primary endpoint and pre-set stopping rules.

---

## 1. Evidence verification (details in `evidence_verified.csv`)

| PMID | Evidence | Read | Verified? | Confirmed effect / note |
|---|---|---|---|---|
| 38412585 | Clozapine NMA in PDP | abstract only | **Verified** | SMD −1.31 (−1.73 to −0.89), 16 RCTs, N=1,252; quetiapine inferior (SMD 0.47). This is a proxy, not M1/M4 evidence. |
| 17070675 | Neuroleptics in PD psychosis | abstract only | **Verified, not independent** | Clozapine beat placebo; quetiapine and olanzapine failed; olanzapine worsened EPS. Overlaps 38412585. |
| 37358841 | ChEI IPD meta-analysis | abstract + key points (PMC) | **Verified** | PD delusions −0.14 (−0.26 to −0.01); PD hallucinations −0.08 (−0.13 to −0.03); 5 PD RCTs. Effects are small. |
| 37530610 | Commentary on the IPD meta-analysis | abstract only | **Flagged: not independent** | Same data as 37358841. Says only PD delusions survive multiplicity correction ("questionably significant"). |
| 38864492 | FEOBV-PET cholinergic deficit with hallucinations | **full text** | **Verified** | VH+ (n=13) had lower uptake in the left ventral visual stream than VH− (n=20); 38 PD + 10 controls. Confound: VH+ were at more advanced Hoehn & Yahr (P=0.033). |
| 42345506 | Xanomeline in MK-801 mice | abstract only | **Partly. Does not support a PD claim** | Hyperlocomotion attenuated at 1–10 mg/kg, PPI deficit at 10 mg/kg. This is not a PD model, so it counts only as generic antipsychotic-like activity. |
| 42729706 | Cobenfy case report | **full text** | **Verified** | See below. |
| 34291590 (added) | Rivastigmine for minor VH in PD | abstract only | Contrary evidence | Null for progression to psychosis; n=91; stopped early and underpowered. The screen had missed this trial. |

**Case report PMID 42729706 (full text, PMC13563583):**
- **Patient:** 83-year-old man with a 10-year history of PD. No dementia on clinical exam.
- **PD stage:** **not reported** (no Hoehn & Yahr, no UPDRS).
- **Prior treatment:** failed quetiapine 350 mg/d, brexpiprazole up to 3 mg/d, and pimavanserin 34 mg/d for 3 months. Clozapine was declined.
- **Dose and response:**
  - On **50/20 mg BID**, nighttime hallucinations resolved within **2 weeks**.
  - The dose was raised to **100/20 mg BID**. Near-complete resolution came by **day 19** at that dose and was **sustained >6 months**.
- **Motor course:** "no worsening of parkinsonian motor symptoms". This was a clinical impression only; **no rating scale** was used.
- **Adverse effects:** blurred vision, resolved by dosing with food. Constipation was pre-existing and managed. No other clinically significant AEs.
- **Note:** the same patient almost certainly appears in FAERS as case 27115291, so FAERS adds no independent efficacy evidence.

**Effect on the screen score:** it stays at 8.0 by the screen's rules, since every evidence type is still present. Quality is lower than the score suggests. The animal type is not PD-specific, the ChEI type rests on one meta-analysis with small effects, and the clinical type is n=1.

---

## 2. Novelty verdict: **NOT already being tested (No)**
See `novelty_check.md` for the queries.
- **ClinicalTrials.gov:** 126 queries, all statuses including withdrawn. They found 0 trials of xanomeline, KarXT, Cobenfy, emraclidine, NBI-1117568/-567, HTL0016878, MK-7622, VU319, ML-007 or KarX-EC in PD, PD psychosis, Lewy body disease or parkinsonism. The only hit is NCT04334317 (TAK-071, an M1 PAM, PD cognition/gait; completed).
- **Literature, 2024–now:**
  - PubMed: 6 hits for xanomeline/KarXT/Cobenfy + Parkinson/Lewy, all-time.
  - Europe PMC: title/abstract search, including preprints.
  - bioRxiv/medRxiv: full API scan.
  - The only PD clinical report is PMID 42729706. There is one non-PD mouse study (42345506) and reviews.
- **Web/news:** 1 search found no BMS program in PD or Lewy body disease. The nearest program is ADEPT (Alzheimer's psychosis), with readout delayed to end-2026/2027 per news reports.

---

## 3. FAERS PD subgroup (openFDA, data to 2026-10-28; `faers_pd_reports.csv`)
- **Cobenfy reports:** 2,881 (primary suspect in 2,834).
- **PD/Lewy indication (Tier A):** 6 reports, which come from **4 unique patients**.
  - Reports 26114932, 26191622 and 26660047 are one patient. 27115291 is the published case.
- **Breadth of the PD flag:** a broader flag that also counts dopaminergic or pimavanserin co-medication gives 14 reports. Most of the extra reports are not PD, e.g., amantadine for EPS or ropinirole with restless legs.

**n<5 unique patients. Do not over-interpret.**

| Patient (reports) | Cobenfy role | Psychosis outcome | Motor AEs |
|---|---|---|---|
| P1: 73F, PDP on pimavanserin (26114932, 26191622, 26660047) | interacting / concomitant | Visual hallucinations **aggravated**; "drug ineffective" (pimavanserin was the suspect drug); cardiac disorder; drug interaction | none coded |
| P2: 70, DLB (26421590) | suspect, 50/20 → 100/20 mg | Agitation; also anuria, hyperhidrosis | none coded |
| P3: 66F, PD on carbidopa/levodopa (26927134) | suspect, 50/20 mg, withdrawn | not reported | none coded (dyspnoea, hypertension) |
| P4: 83M, PDP (27115291) = published case | suspect, 50/20 → 100/20 BID | "Drug ineffective" + visual hallucination, which cannot be attributed between pimavanserin and Cobenfy; the publication reports response | none coded (blurred vision) |
| Tier B: 75F schizoaffective on carbidopa/levodopa + quetiapine (26458557) | suspect, 50/20 mg | not applicable | **tremor ×2** |

**Motor-AE disproportionality** (`raw/faers_cobenfy_ror_tiers.json`, `raw/faers_reference.json`):

| Group | Motor AE (any), n/N (%) | ROR vs reference (95% CI) |
|---|---|---|
| Cobenfy, all non-PD reports (reference) | 164/2,867 (5.7%) | – |
| Cobenfy, PD Tier A reports | 0/6 (0%) | 1.26 (0.07–22.5)*, uninformative |
| Cobenfy, Tier A + B reports | 1/7 (14%) | 2.75 (0.33–23.0) |
| Cobenfy, broad 14-report flag | 3/14 (21%) | 4.50 (1.24–16.3); driven by akathisia in non-PD (ropinirole/RLS) cases |
| Pimavanserin, PD reports vs non-PD | 9,244/53,449 (17.3%) vs 510/4,244 (12.0%) | 1.53 (1.39–1.68) |
| Quetiapine, PD reports vs non-PD | 3,089/10,158 (30.4%) vs 25,468/184,222 (13.8%) | 2.72 (2.61–2.85) |

\*Haldane-corrected because there were 0 events. Any ROR with 0 events in 6 reports is mechanically above 1 and carries no information.

**Reading:**
- PD reports carry more motor AEs for every drug (ROR 1.5–2.7), because PD itself produces motor events (confounding by indication).
- Cobenfy's PD sample is far too small to compare against that baseline.
- The one usable signal is that **tremor is already the most frequent motor PT** for Cobenfy overall (46/2,881 reports). It was also flagged as an "unexpected signal" in a published FAERS study (PMID 42202430).

---

## 4. Motor-safety evidence

**Trials and label (schizophrenia, mostly <65 years):**
- **Pooled EMERGENT-1/2/3** (n=683; PMID 43010316): EPS-related TEAEs 3.2% vs 0.9% placebo. Akathisia 2.4% vs 0.9%; only 0.6% vs 0.3% was judged drug-related. Dystonia, dyskinesia and extrapyramidal disorder occurred in 1 patient each (0.3%). SAS, BARS and AIMS were unchanged.
- **EMERGENT-2** (PMID 38104575): EPS 0% vs 0%; akathisia 1% vs 1%. **EMERGENT-1** (33626254) and **EMERGENT-3** (38691387): EPS "similar" to placebo.
- **Cumulative review** (PMID 41825117): EPS TEAEs 3.8% in double-blind studies and 2.6% in open-label studies. Pre-existing EPS attenuated.
- **52-week EMERGENT-4** (PMID 41634905, n=152): "not associated with clinically meaningful motor symptoms".
- **FDA label** (openFDA SPL, effective 2026-01-16):
  - EPS (non-akathisia) 2% vs <1% placebo (N=251 vs 253).
  - Dizziness 5% vs 2%; orthostatic hypotension 2% vs 1%.
  - **"Controlled clinical studies… did not include patients older than 65"**, so slower titration is advised in older patients.
  - Warning 5.9: trospium can cause CNS anticholinergic effects **including hallucinations**. This matters for a PDP endpoint.
- **FDA review documents:** not found (accessdata.fda.gov returned 404).

**PD-relevant pharmacology (animal and other human data):**

| Finding | Direction for PD motor | Source |
|---|---|---|
| Xanomeline blocked dopamine-agonist rotation in 6-OHDA rats, like haloperidol, without catalepsy. It inhibited A10 but not A9 dopamine neurons. | Could **blunt levodopa/agonist effect**; spares nigrostriatal firing | PMID 10785583 |
| Muscarinic agonists (M2/M4) inhibited D1/D2-agonist rotation in 6-OHDA rats | Same concern | PMID 9855303 |
| Cholinomimetic "tremulous jaw movements" (a rodent PD-tremor model) are M4-mediated; M4 knockout reduces them | **Tremor risk** | PMID 9920179, 11392629 |
| Antipsychotic catalepsy is attenuated in M4-knockout mice | M4 activation may favour parkinsonism | PMID 21269601 |
| M1 and M4 antagonists relieve akinesia in 6-OHDA mice | M4 agonism may **worsen akinesia** | PMID 27581457 |
| **Counterpoint:** M4 PAM reduced levodopa-induced dyskinesia in mouse and primate | **Benefit** for dyskinesia | PMID 26590347 |
| **Counterpoint:** M4 signalling is reduced after dopamine loss; restoring it partly alleviated parkinsonian deficits | Possible **benefit** | PMID 39565858 |
| Xanomeline 4 mg/kg caused dystonia in 2/3 EPS-sensitised monkeys (none at 0.5–3 mg/kg) | Dystonia at high dose | PMID 12700711 |
| ChEIs in PD dementia: new or worse tremor 10.2% vs 3.9% (n=541), with UPDRS-III unchanged | **Tremor** is the realistic clinical effect | PMID 18095748; meta-analysis PMID 25224676 |
| Donepezil in DLB: EPS AEs 6.5% vs 3.8% (ns), UPDRS-III unchanged over 52 weeks | Reassuring | PMID 26226884 |

**Motor-risk verdict: moderate and monitorable.**
- **Most likely harm:** tremor worsening. The analogy is ChEIs in PD, with roughly 6 percentage points excess tremor and no UPDRS-III change, combined with Cobenfy's own FAERS tremor signal.
- **Plausible, untested harm:** partial blunting of levodopa response, based on 6-OHDA rotation data.
- **Possible benefit:** reduced dyskinesia via M4.
- **Unknown:** severe parkinsonism or dystonia at clinical doses in PD has never been measured. The trial EPS data do not transfer to a dopamine-depleted brain or to patients over 65.
- **Additional caveats:** dizziness and orthostatic hypotension (fall risk), and the label warning that trospium can cause hallucinations.

---

## 5. Go/no-go for the pilot (6-week open-label, n≈15–20, NPI-hallucinations + MDS-UPDRS-III)

**Recommendation: CONDITIONAL GO.**
- **Why go:** the idea is unscooped; the mechanism avoids D2 blockade; there is a verified human case with a durable response; and the motor risk can be detected within 6 weeks with MDS-UPDRS-III.
- **Conditions:**
  1. **Make motor safety a co-primary outcome.** Measure MDS-UPDRS-III in the ON state at the same time relative to levodopa at baseline and weeks 1, 2, 4 and 6. Add tremor items (3.15–3.18) and a falls diary.
  2. **Pre-specify stopping rules.** Stop for MDS-UPDRS-III worsening of ≥5 points confirmed at a repeat visit, new freezing or falls, or dystonia.
  3. **Titrate slowly for older patients:** 50/20 mg BID for at least 2 weeks before 100/20 mg BID; no 125/30 step. Keep the levodopa-equivalent daily dose fixed.
  4. **Exclusions** (label): urinary retention, gastric retention, moderate or severe hepatic impairment, untreated narrow-angle glaucoma, moderate or severe renal impairment, and symptomatic orthostatic hypotension. Record baseline heart rate and orthostatic blood pressure.
  5. **Psychosis outcome:** NPI hallucinations/delusions plus SAPS-PD, with caregiver input. Be aware that trospium can itself cause hallucinations (label 5.9).
- **Before or alongside the pilot:** run the institutional records check, because FAERS is too small (4 patients) to replace it.
- **No-go triggers:** a registered competing trial appears; or the records check shows motor worsening in ≥2 PD patients on Cobenfy.

**Files:** `evidence_verified.csv`, `faers_pd_reports.csv`, `trials_pd.csv`, `novelty_check.md`, `decisions_log.md`, plus `raw/` and `scripts/`.
