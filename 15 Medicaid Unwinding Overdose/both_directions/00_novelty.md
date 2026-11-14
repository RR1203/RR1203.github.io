# 00 Novelty check: Medicaid coverage gains vs losses (SD/NC expansion vs unwinding), buprenorphine and overdose

- **Search date:** 2026-11-14
- **Claimed contribution:** one state-panel model using both directions of coverage change in 2023–2024 (unwinding losses in most states; expansion gains in SD from 1 Jul 2023 and NC from 1 Dec 2023), a piecewise-linear dose-response with a kink at 0 net enrollment change, and a formal **symmetry test**: is the effect per pp gained on Medicaid buprenorphine fills (SDUD) and overdose deaths (CDC VSRR) equal to the effect per pp lost?

## Sources not reachable
- The network proxy blocked (HTTP 403, CONNECT tunnel failed) www.ncdhhs.gov, medicaid.ncdhhs.gov, kff.org, dss.sd.gov, sdlegislature.gov and medicaid.gov. No statute, CMS approval letter or state press release was read directly. The dates below rest on indexed peer-reviewed literature only.

## Databases, exact queries, hit counts

**PubMed (MCP `search_articles`)**
| Group | Query | Filter | Hits |
|---|---|---|---|
| a | `"North Carolina" AND Medicaid expansion AND (buprenorphine OR "opioid use disorder" OR overdose OR MOUD)` | 2023– | 14 |
| b | `"South Dakota" AND Medicaid AND expansion` | 2022– | 12 |
| c | `(Medicaid unwinding OR "continuous enrollment" OR disenrollment) AND (buprenorphine OR "opioid use disorder" OR overdose OR MOUD)` | 2023– | 53 (all 53 screened by title; most hits are "continuous enrollment" used as a claims-cohort inclusion criterion) |
| c | `Medicaid unwinding buprenorphine` | none | 5 |
| d | `Medicaid AND (coverage loss OR disenrollment) AND (coverage gain OR expansion) AND (asymmetr* OR symmetr*)` | none | 1 |
| a/b/d | `Medicaid unwinding AND Medicaid expansion AND (South Dakota OR North Carolina)` | none | 5 |
| check | `Medicaid Expansion and Buprenorphine Dispensing in Early vs Recent Expansion States` (title lookup) | none | 1 |

**Europe PMC REST (`/search`, format=json; indexes MED + PPR preprints incl. medRxiv/SSRN/Research Square)**
| Group | Query | Hits |
|---|---|---|
| a | `"North Carolina" AND "Medicaid expansion" AND (buprenorphine OR "opioid use disorder" OR overdose OR MOUD) AND PUB_YEAR:[2023 TO 2026]` | 127 (top 25 screened) |
| b | `"South Dakota" AND "Medicaid expansion" AND (buprenorphine OR opioid OR overdose OR MOUD OR substance)` | 158 (top 25 screened; none SD-specific on OUD) |
| c | `("Medicaid unwinding" OR "continuous enrollment provision" OR "end of continuous enrollment") AND (buprenorphine OR "opioid use disorder" OR overdose OR MOUD)` | 25 |
| c | `("Medicaid unwinding" OR "Medicaid disenrollment") AND ("overdose death*" OR "overdose mortality")` | 10 (no unwinding-to-overdose-death study) |
| d | `("Medicaid unwinding" OR disenrollment) AND "Medicaid expansion" AND (asymmetr* OR symmetr* OR "coverage gains and losses" OR "gains and losses")` | 19 (mostly conference abstract books) |
| d | `(Medicaid) AND ("asymmetric" OR "asymmetry") AND ("coverage loss" OR "losing coverage" OR disenrollment) AND ("coverage gain*" OR expansion)` | 46 (top 15 screened) |
| d | `(TennCare OR "Missouri Medicaid") AND disenrollment AND (mortality OR "health outcomes" OR "access to care")` | 26 (top 15 screened; no Missouri disenrollment outcome study surfaced) |
| c (preprints) | `SRC:PPR AND (unwinding OR "continuous enrollment") AND Medicaid` | 22 (none relevant) |
| a/b (preprints) | `SRC:PPR AND "Medicaid expansion" AND (buprenorphine OR overdose) AND PUB_YEAR:[2023 TO 2026]` | 4 (none relevant to 2023 expansions) |
| d | `Medicaid AND ("net enrollment change" OR "enrollment change") AND (buprenorphine OR overdose) AND PUB_YEAR:[2023 TO 2026]` | 0 |
| NC infra | `"North Carolina" AND ("opioid settlement" OR "abatement fund*")` | 39 |

**researchfasttrack (OpenAlex; for NBER/SSRN-type working papers)**
- `Medicaid unwinding and Medicaid expansion symmetric effects of coverage gains and losses on opioid use disorder treatment and overdose` (year ≥2023): 1 hit (NBER w34642, on SUD treatment facilities and intimate partner violence; not relevant).

**Consensus**
- `Medicaid unwinding coverage loss versus Medicaid expansion coverage gain buprenorphine overdose deaths`: 10 hits. All relevant hits were already found in PubMed (Constantin 2025 ×2, Gupta 2025, Landis 2025, Crystal 2025), plus Siegal 2026 (added below).

## Relevant papers

| Author year | Title | Journal | PMID / DOI | Group | One-line finding | Overlap with combined symmetry test? |
|---|---|---|---|---|---|---|
| Constantin, Chua, McCullough 2025 | Buprenorphine Dispensing Following Medicaid Expansion Amid Unwinding in North Carolina | JAMA Netw Open | 41370080 / 10.1001/jamanetworkopen.2025.47933 | a, c, d | NC vs SC DiD (IQVIA): after both states lost ~11 pp in active buprenorphine during unwinding, NC expansion (1 Dec 2023) gave a +1.6 pp differential increase and +7.4 pp in Medicaid-paid fills, i.e., expansion partly offset unwinding losses | **Partial (closest).** Same setting and both directions in one state, but a single-state DiD with no per-pp dose-response, no kink, no formal gain-vs-loss symmetry test, no SD, no overdose deaths |
| Constantin, Kenney, Simon, Chua 2025 | Medicaid Unwinding and Changes in Buprenorphine Dispensing | JAMA Netw Open | 40314954 / 10.1001/jamanetworkopen.2025.8469 | c | States in the top vs bottom quartile of adult enrollment decline: −3.9 buprenorphine days, +1.8 pp with no active Rx | Partial (losses only, binary quartile exposure) |
| Landis, Sheng, Stein 2025 | Medicaid Unwinding: Association With New and Ending Buprenorphine Treatment Episodes | J Addict Med | 40838627 / 10.1097/ADM.0000000000001573 | c | Medicaid buprenorphine episodes ending rose and new episodes fell, most in states with the largest disenrollment (graded by magnitude) | Partial (loss-side dose gradient only) |
| Gupta, James, Miles, et al. 2025 | Trends in Access to Medications for Opioid Use Disorder | JAMA Health Forum | 40184057 / 10.1001/jamahealthforum.2025.0393 | c | ITS: 12.7% drop in Medicaid-paid buprenorphine patients 8 months after unwinding began, partly offset by commercial and self-pay fills; nonexpansion states had smaller offsets | Partial (losses only) |
| Landis, Kapinos, et al. 2026 | Association of Coverage-Promoting Policies With Initiation and Discontinuation of Buprenorphine Treatment During Medicaid Unwinding | J Addict Med | 41980697 / 10.1097/ADM.0000000000001695 | c | Ex parte renewal and follow-up policies were linked to smaller disruptions in buprenorphine treatment | No |
| Rome, Han, McIntyre, Kesselheim, Sommers 2026 | Changes in Medication Use During Medicaid Continuous Enrollment and Unwinding | JAMA Health Forum | 41481327 / 10.1001/jamahealthforum.2025.5890 | c, d | Gain phase (continuous enrollment): enrollment +2.42%/qtr and Rx +1.85%/qtr. Loss phase (unwinding): enrollment −4.92%/qtr and Rx −3.94%/qtr. Rx changed less than enrollment in both phases; stratified by net enrollment change | **Partial.** Compares gains and losses in Medicaid Rx across states, but not OUD-specific, no expansion states, no overdose deaths, no formal per-pp symmetry test |
| Elani, Sommers, Kawachi, Tipirneni 2026 | Fluctuating State Medicaid Dental Coverage: Asymmetric Impact Of Benefit Cuts And Expansions, 2010-21 | Health Aff | 41628380 / 10.1377/hlthaff.2025.00454 | d | Removing adult dental benefits had larger and different effects than adding them (asymmetry) | Partial (methodological precedent for a gain-vs-loss asymmetry test; dental, not OUD) |
| Siegal, Gupta, Miles, et al. 2026 | Medicaid Expansion and Buprenorphine Dispensing in Early vs Recent Expansion States | JAMA Netw Open | 41706449 / 10.1001/jamanetworkopen.2025.59803 | a, b | Staggered DiD 2013–2024: expansions from 2019 on raised all-payer buprenorphine treatment by 21% | No (gains only) |
| Crystal, Xie, Samples, et al. 2025 | States With Substantial Increases In Buprenorphine Uptake Did So With Increased Medicaid Prescribing, 2018-24 | Health Aff | 40893074 / 10.1377/hlthaff.2025.00343 | a, b | States expanding in 2018–24 raised all-payer buprenorphine by 27.3% vs −2.1% in nonexpansion states | No |
| Nguyen, Binswanger, et al. 2026 | Health Plan Disenrollment and Mortality After Initiation of Medications for Opioid Use Disorder | JAMA Psychiatry | 41779402 / 10.1001/jamapsychiatry.2026.0021 | c (bg) | Individual disenrollment after MOUD start was linked to higher overdose mortality (HR 1.56), 2012–2022 | No (individual-level, pre-unwinding) |
| Johnson, Mein, Marinacci, Liu 2025 | Insurance coverage and employment after Medicaid expansion with work requirements | BMJ | 41027709 / 10.1136/bmj-2025-086792 | b | SD (expanded at the same time as GA, 1 Jul 2023) low-income Medicaid coverage rose from 36.6% to 44.6% | No (coverage only) |
| Nicolet, Bender, Guymon, Kroboth 2025 | Medicaid in South Dakota Since Expansion | S D Med | 40878023 / no DOI shown | b | Narrative: about 29,500 newly covered; start date 1 Jul 2023; rollout overlapped with unwinding | No |
| Lu 2026 | Late Medicaid expansion was associated with higher Medicaid coverage: … Oklahoma, Missouri, and North Carolina | Front Public Health | 42922905 / 10.3389/fpubh.2026.1942538 | a | ACS DiD: NC Medicaid coverage +3.3 pp after the 2023 expansion | No (first-stage coverage only) |
| Berghammer, Adams, Khan, Bobashev 2024 | Simulating the effects of medicaid expansion on the opioid epidemic in North Carolina | Drug Alcohol Depend Rep | 39139778 / 10.1016/j.dadr.2024.100262 | a | Simulation: NC expansion could avert 213–332 overdose deaths in year 1 | No (simulation) |
| Barbosa, Dowd, et al. 2024 | Simulated impact of medicaid expansion on the economic burden of opioid use disorder in North Carolina | Int J Drug Policy | 38733650 / 10.1016/j.drugpo.2024.104449 | a | Simulated reductions in NC state costs of OUD after expansion "adopted in December 2023" | No |
| Tarazi, Green, Sabik 2017 | Medicaid Disenrollment and Disparities in Access to Care: Evidence from Tennessee | Health Serv Res | 27256968 / 10.1111/1475-6773.12515 | d (bg) | 2005 TennCare disenrollment reduced access to care | No (background) |
| Rahman 2026 | Medicaid and health resilience: Evidence from TennCare disenrollment | Econ Hum Biol | 42612417 / 10.1016/j.ehb.2026.101640 | d (bg) | TennCare 2005 disenrollment raised uninsurance and reported poor health | No (background) |

- No Missouri disenrollment outcome study surfaced in these searches. Cite one as [REF NEEDED] if wanted.
- No study surfaced that links unwinding (or the 2023 expansions) to **overdose deaths** at the state level.
- No South Dakota-specific study on buprenorphine, MOUD or overdose after the 2023 expansion was found.

## Expansion date verification
- **South Dakota, 1 July 2023: confirmed (secondary peer-reviewed sources).**
  - Nicolet et al. 2025, S D Med, PMID 40878023: "the Medicaid expansion start date of July 1, 2023"; passed by ballot Amendment D (2022).
  - Johnson et al. 2025, BMJ, PMID 41027709 / 10.1136/bmj-2025-086792: Georgia expanded on 1 July 2023, "and South Dakota, which simultaneously expanded Medicaid."
  - Not read: primary sources (SD Constitution Art. XXIX / Amendment D text, CMS SPA approval, dss.sd.gov). These sites were blocked. [REF NEEDED] for a primary citation.
- **North Carolina, 1 December 2023: confirmed (secondary peer-reviewed sources).**
  - Constantin et al. 2025, JAMA Netw Open, PMID 41370080 / 10.1001/jamanetworkopen.2025.47933: "On December 1, 2023, North Carolina expanded Medicaid."
  - Barbosa et al. 2024, Int J Drug Policy, PMID 38733650: "Medicaid expansion in North Carolina (adopted in December 2023)."
  - Not read: primary sources (Session Law 2023-7 / HB 76, CMS approval, NCDHHS press release). ncdhhs.gov and medicaid.ncdhhs.gov were blocked. [REF NEEDED] for a primary citation.

## NC addiction-treatment infrastructure / opioid settlement note
- Mange 2024, "The North Carolina Model for Opioid Settlement Funds," N C Med J, PMID 39495957 / 10.18043/001c.123268. NC expects about $1.4 billion over 18 years from opioid settlements.
- Gonzales, Gora Combs, Sibley, Marshall 2025, "How North Carolina is Using Opioid Settlement Funds to Reduce Overdose Deaths," N C Med J, PMID 41804117 / 10.18043/001c.146070. Describes settlement-funded overdose prevention in NC.
- Implication: settlement spending in NC ran at the same time as expansion. It is a co-intervention that could confound the gain-side slope and should be handled as a sensitivity check. Relevant background: Shi & Wen 2026, Health Serv Res, 10.1111/1475-6773.70173 (abatement funds and MOUD).

## Verdict
- Closest overlaps are Constantin 2025 (NC expansion amid unwinding, buprenorphine; single-state DiD, no symmetry test, no overdose outcome) and Rome 2026 (gain vs loss phases in all Medicaid Rx; not OUD, no formal symmetry test). Neither, nor any other paper found, estimates a per-pp dose-response across states with a kink at zero and formally tests gain/loss symmetry for buprenorphine fills or overdose deaths.
- These two papers must be cited and the contribution framed against them. The novelty claim is narrow: the formal both-directions symmetry test plus the overdose outcome.

**GATE: PASS**
