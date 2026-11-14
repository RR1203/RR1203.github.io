# 00 Novelty check: recriminalization of drug possession and overdose deaths (OR, WA)

Search date: 2026-11-14.

## Where we searched
- PubMed (MCP): `(Oregon OR Washington) AND (recriminalization OR recriminalize OR "HB 4002" OR "Measure 110" OR Blake OR 5536) AND overdose`, 2023 onward → 5 hits, none estimate a recriminalization effect.
- Europe PMC REST API: `(recriminalization OR recriminalisation OR "HB 4002" OR "SB 5536" OR "House Bill 4002") AND (overdose OR "drug deaths") AND (Oregon OR Washington)` → 8 hits, none on OR/WA recriminalization.
- OpenAlex (researchfasttrack connector), recriminalization + Oregon/Washington + overdose, 2023 onward → 12 hits.
- Web search (covers NBER, SSRN, medRxiv, university working-paper pages).

## What exists

### Decriminalization (the setting we build on)
| Paper | Design | Result (as stated in abstract) |
|---|---|---|
| Joshi et al., JAMA Psychiatry 2023;80(12):1277-83, doi:10.1001/jamapsychiatry.2023.3416 | SCM, monthly rates, post to Mar 2022 | OR: mean diff 0.268 per 100k per month, p = 0.26; WA: 0.112, p = 0.06. "No evidence of an association." |
| Zoorob et al., JAMA Netw Open 2024, doi:10.1001/jamanetworkopen.2024.31612 | Matrix-completion SCM, half-year rates, NFLIS fentanyl share | Crude 1.83 (SE 0.47) per 100k per half-year; adjusted for fentanyl −0.51 (SE 0.61), p = 0.41. |
| Hall, Hansen & Matsuzawa, NBER w35427 (2026), doi:10.3386/w35427 | SCM | Arrests fell sharply; ~1,186 excess deaths OR and ~1,895 WA, 2021–2023. |
| Pourtaheri, "The Social Cost of Drug Decriminalization", UW job-market paper / SSRN 7608641 (Oct 2026) | Synthetic DiD, FBI arrests + CDC deaths | Per search snippet: user arrests −68%, overdose deaths +34%. **Full text not read** (host blocked). |
| Jones, Mitchell, Thomas & Thorley, "Decriminalization and Death…", SSRN 7416340 (2026) | DiD, Multnomah County | Per search snippet: M110 raised deaths 2.197 per 100k per month in Multnomah; "higher overdose deaths have persisted during the recriminalization period". **Full text not read.** |
| PSU/NIJ final report on M110 (2025) | Mixed | Per press coverage: no evidence M110 drove overdoses or crime. [REF NEEDED: exact report citation] |

### Recriminalization
- **No peer-reviewed estimate of the effect of OR HB 4002 (Sept 2024) or WA SB 5536 (July 2023) on overdose deaths was found.**
- Two 2026 working papers (Pourtaheri; Jones et al.) mention the recriminalization period, from snippets apparently descriptively (WA: "after recriminalization both series rise again"; Multnomah: elevated deaths "persisted"). Neither appears to report a state-level causal estimate of recriminalization with OR + WA and permutation inference, but **we could not read either full text**, so this is not certain. [REF NEEDED: verify both full texts]
- A search snippet attributed to a medRxiv preprint says WA's trend "substantially accelerated after the state recriminalized"; we could not identify or verify the source. [REF NEEDED]
- Closest analogue: Gaudreault et al., CMAJ 2026, doi:10.1503/cmaj.260038 — British Columbia decriminalization (2023) and partial recriminalization (May 2024), controlled ITS. Possession incidents rose after recriminalization (IRR 1.68, 95% CI 1.13–2.51); no change in drug toxicity deaths vs Alberta (RRR 1.14, 0.79–1.66).
- Oregon CJC, "Examining Equity in the Recriminalization of Drug Possession in Oregon" (Feb 2026) — descriptive arrests and overdose series; no causal estimate.

## Verdict
Gate **passed (with caveat)**. A state-level synthetic-control estimate of recriminalization for both OR and WA, with permutation inference and a decriminalization replication in the same setup, appears new. Two working papers touch the recriminalization period and must be read before any write-up.
