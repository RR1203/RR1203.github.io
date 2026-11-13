# Novelty / scoop check: Cobenfy (xanomeline-trospium) for PD psychosis

## Verdict: already being tested? **NO**
- No registered trial in any status, withdrawn included.
- No published trial.
- No preprint of a PD clinical study.
- No company program found.
- The only clinical PD evidence is one published case report (PMID 42729706, 2026).

## 1. ClinicalTrials.gov (API v2, all statuses; `raw/ctgov_log.json`, `trials_pd.csv`)
- **Interventions (20):** xanomeline, KarXT, Cobenfy, "xanomeline trospium", emraclidine, CVL-231, NBI-1117568, NBI-1117567, "muscarinic agonist", muscarinic, "M4 positive allosteric modulator", "M1 positive allosteric modulator", TAK-071, MK-7622, HTL0016878, VU319, ML-007, KarX-EC, ANAVEX3-71, cevimeline.
- **Conditions (6):** Parkinson Disease, Parkinson Disease Psychosis, Lewy Body Disease, Dementia with Lewy Bodies, Parkinsonism, Parkinson Disease Dementia.
- **Also run:** 6 free-text queries (`xanomeline AND parkinson`, `KarXT AND parkinson`, `cobenfy AND parkinson`, `xanomeline AND lewy`, `cobenfy AND lewy`, `muscarinic AND parkinson psychosis`).
- **Result:** 126 queries returned **2 trials, neither relevant**:
  - **NCT04334317:** TAK-071, an M1 PAM, in PD. Phase 2, completed. Endpoints were cognition and gait, not psychosis. It is not an M1/M4 agonist.
  - **NCT03149809:** solifenacin, a muscarinic *antagonist*, for overactive bladder in PD. Irrelevant.
- **Nearest Cobenfy programs (from the earlier screen's `trials.csv`):** Alzheimer's psychosis/agitation (ADEPT: NCT05511363, NCT06126224, NCT06937229 and others), bipolar mania, autism irritability, and cocaine use disorder.

## 2. Literature, 2024 to now
| Source | Query | Hits | PD-relevant result |
|---|---|---|---|
| PubMed | `(xanomeline OR KarXT OR cobenfy OR "xanomeline-trospium") AND (parkinson* OR lewy OR parkinsonism)` (all years) | 6 | **42729706** (case report); 42345506 (mouse MK-801; not a PD model); 40056428 (review); 28422371, 30856192, 31299348 (preclinical, not PD clinical) |
| PubMed | xanomeline/KarXT/Cobenfy + motor/EPS/PD terms, 2024–2026 `[dp]` | 34 | Only 42729706 is PD clinical. The rest are schizophrenia trials, reviews and FAERS studies. |
| Europe PMC | title/abstract: (xanomeline OR KarXT OR Cobenfy OR trospium) AND (parkinson* OR lewy OR parkinsonism OR extrapyramidal OR dystonia OR tremor OR motor), first published 2024–2026 | 30 (29 mention xanomeline/Cobenfy) | 3 also mention Parkinson/Lewy: 42729706, 40056428, 42345506 |
| Europe PMC preprints (SRC:PPR) | (xanomeline/KarXT/Cobenfy) AND (parkinson* OR lewy) | 1 | PPR61639 (2018, TAK-071 qEEG in monkeys). Not relevant. |
| bioRxiv + medRxiv API, full scan 2024-01-01 to 2026-11-13 | medRxiv neurology (4,574), psychiatry (3,306), pharmacology (405); bioRxiv neuroscience (38,750), pharmacology/toxicology (2,230) = **49,265 preprints**, regex on title/abstract | 7 keyword hits (6 unique) | 1 PD-related: **10.1101/2024.04.16.589785**, M4 PAM infused in pedunculopontine nucleus *augmented* L-DOPA motor effect in 6-OHDA rats with no change in dyskinesia (preclinical, not clinical). No clinical Cobenfy-in-PD preprint. |
| Conference abstracts | MDS / AAN / ACNP abstract books | **not searched** | Not indexed by the sources above; not found. |

## 3. Company pipeline and news (1 web search)
- **Query:** "Bristol Myers Squibb Cobenfy Parkinson's disease psychosis Lewy body trial news".
- **Result:** **no PD or Lewy body program found.** The results covered ADEPT (Alzheimer's psychosis), where secondary news sources describe a delayed readout and site irregularities, and the failed adjunctive schizophrenia trial ARISE.
- **Sources:** [BioSpace: Future of BMS' Cobenfy still in limbo after Phase III fail](https://www.biospace.com/business/future-of-bms-cobenfy-still-in-limbo-after-phase-iii-fail); [Yahoo/news: BMS delays Alzheimer's readout for Cobenfy](https://www.yahoo.com/news/articles/bms-delays-alzheimer-readout-cobenfy-170531776.html); [BioPharma Dive: ARISE](https://biopharmadive.com/news/cobenfy-bristol-myers-trial-failure-schizophrenia-adjuvant-wall-street/746073).

## 4. Scoop risk
- **Main risk:** an investigator-initiated study following the 2026 case report, or a BMS extension of ADEPT to Lewy body disease. Neither is registered as of 2026-11-13.
- **Ongoing check:** re-run `scripts/ctgov.py` before committing resources.
