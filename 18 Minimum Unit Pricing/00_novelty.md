# 00 Novelty and policy-fact check: minimum unit pricing (MUP)

Searched 2026-11-14 in PubMed, Europe PMC (including preprints), OpenAlex, legislation.gov.uk, PHS and HRB sites, and the web. The full query log is in `literature_log.md`.
I could not reach gov.wales, irishstatutebook.ie, gov.ie, oireachtas.ie, nt.gov.au, senedd.wales or health-ni.gov.uk; each was blocked or failed twice. Facts from those sites are marked as secondary or [REF NEEDED].

## 1. Novelty table (jurisdiction × outcome)

| Jurisdiction | Deaths | Hospital admissions | Sales / purchases / first stage |
|---|---|---|---|
| **Scotland, 50p (2018)** (positive control) | **Evaluated.** Wyper et al. *Lancet* 2023;401:1361-70. PMID 36963415, doi:10.1016/S0140-6736(23)00497-X | **Evaluated.** Same paper. Self-harm admissions: J Public Health 2026, doi:10.1093/pubmed/fdag058 (PMID 42544395) | **Evaluated.** Giles et al. *Addiction* 2024 (PMID 38685192, doi:10.1111/add.16492). Robinson et al. *Addiction* 2021 (PMID 33723866, doi:10.1111/add.15478). O'Donnell et al. *BMJ* 2019 (PMID 31554617, doi:10.1136/bmj.l5274) |
| **Scotland, 65p uprating (30 Sep 2024)** | **Not evaluated** (empirical). Modelled only: PLoS Med 2026 (PMID 41505661, doi:10.1371/journal.pmed.1004792) | **Not evaluated** (empirical). Modelled only: same paper | **Not evaluated** (causal). PHS Alcohol Consumption and Harms Dashboard release of 30 Jun 2026 reports sales for 2017–2025 descriptively; it does not mention 65p ([PHS](https://publichealthscotland.scot/publications/alcohol-consumption-and-harms-dashboard/alcohol-consumption-and-harms-dashboard-30-june-2026/)) |
| **Wales, 50p (2 Mar 2020)** | **Not evaluated.** No study found | **Not evaluated.** No study found. The Welsh Government final evaluation reports (Jan 2025) could not be opened to confirm they leave harms out of scope [REF NEEDED: gov.wales blocked] | **Evaluated.** Billan, Angus, Collins. *Public Health* 2025;240:71-79 (Kantar CITS vs England; PMID 39874916, doi:10.1016/j.puhe.2024.12.051). Welsh Government retailer/quantitative final report (Kantar 2016–2023) [figures and pages REF NEEDED]. Qualitative: Holloway et al. 2024 (PMID 38356791) |
| **Wales, 65p (1 Oct 2026)** | Not evaluated (6 weeks old) | Not evaluated | Not evaluated |
| **Ireland, €1.00/10 g (4 Jan 2022)** | **Not evaluated.** No study found | **Not evaluated at population level.** Single-hospital before/after audits only: Maharaj et al. *Public Health* 2024 (Beaumont ED, PMID 38103275, doi:10.1016/j.puhe.2023.11.016). McKenna-Barry & O'Regan, *Ir J Med Sci* 2023 (Tipperary, PMID 35851670, doi:10.1007/s11845-022-03100-z). Both are uncontrolled and do not draw causal conclusions | **Not evaluated** (peer-reviewed). Only trade press: NielsenIQ off-trade volume via drinksindustryireland.ie (not a causal design). No Kantar/Worldpanel or HRB evaluation found. Note: Mohan 2025 (PMID 39581582) is an Irish author but evaluates **Scotland**, not Ireland |
| **Northern Territory, A$1.30/std drink (1 Oct 2018; repealed 1 Mar 2025)** | **Not evaluated.** No study found | **Partly evaluated, confounded by co-policies.** Critical-care admissions: *Addiction* 2021 (PMID 33891373). Injury hospitalisations, joinpoint: *DAR* 2025 (PMID 39656527). DFV hospital admissions: *DAR* 2026 (PMID 42152233). ED: *EMA* 2023 (PMID 36428244). The PALI/BDR overlap is stated in these papers | **Evaluated.** Wholesale supply: *ANZJPH* 2021 (PMID 33559964). Wastewater: *Addiction* 2022 (PMID 34184809). Expenditure: *ANZJPH* 2023 (PMID 37202337). Repeal price effects: Miller et al. *Addiction* 2026 (PMID 42299053) |
| England | No MUP (control) | — | — |
| Northern Ireland | No MUP (control candidate) | — | — |

**What remains open:** no one has evaluated deaths or hospital admissions after MUP in Wales or Ireland at population level, or after Scotland's 65p uprating. NT deaths are also unevaluated.

## 2. Verified key numbers

- **Wyper 2023** (abstract, PMID 36963415). The study compared Scotland with England using a controlled interrupted time series, with data from Jan 2012 to Dec 2020 (32 months post-policy).
  - Deaths wholly attributable to alcohol: **−13.4% (95% CI −18.4 to −8.3; p=0.0004)**.
  - Hospitalisations wholly attributable to alcohol: **−4.1% (95% CI −8.3 to +0.3; p=0.064)**.
  - The effects were driven by chronic outcomes, especially alcoholic liver disease.
  - Deaths and hospitalisations fell in the **four most socioeconomically deprived deciles**, and the greatest improvements were there.
  - The PHS final report (p.35) adds that the largest death reductions were among men, people aged 65 and over, and the 40% most deprived areas.
- **PHS final MUP evaluation** (*Evaluating the impact of MUP for alcohol in Scotland: Final report – a synthesis of the evidence*, 27 June 2023; [page](https://publichealthscotland.scot/publications/evaluating-the-impact-of-minimum-unit-pricing-for-alcohol-in-scotland-a-synthesis-of-the-evidence/), [PDF](https://publichealthscotland.scot/media/20366/evaluating-the-impact-of-minimum-unit-pricing-for-alcohol-in-scotland-final-report.pdf)).
  - It reports deaths −13.4% and admissions −4.1% (PDF p.35).
  - Estimated wholly attributable **deaths prevented: 156 per year (69 to 243)**, Table 5, PDF p.92.
  - Estimated **admissions averted: 411 per year (−86 to 908)**, Table 6, PDF p.94.
  - The ["Findings at a glance"](https://publichealthscotland.scot/media/21240/minimum-unit-pricing-mup-for-alcohol-evaluation-findings-at-a-glance-updated-august-2023.pdf) (Aug 2023) summary gives sales −3%.
- **Sales (MESAS), Giles et al. 2024** (*Addiction* 119:1378-86, PMID 38685192).
  - Total per-adult sales: **−3.0% (95% CI 1.8–4.2%)** versus England & Wales after 3 years.
  - This is a 1.1% fall in Scotland against a 2.4% rise in England & Wales.
  - The fall was driven by the off-trade; there was no on-trade change.
  - Earlier off-trade estimate: Robinson 2021, −3.5% (2.2–4.9%).
- **Wales first stage.** Billan 2025 (abstract) reports that under-28s cut cider purchasing by 50% relative to England and spent 33% more on lager. Lower socioeconomic groups showed a 1.33 percentage-point rise in wine purchasing.
  - **Welsh Government report figures (change in purchased units, price per unit, share of units sold below 50p) and their page numbers: [REF NEEDED].** The PDFs could not be retrieved.
  - [Retailers & quantitative final report (Report 81/2024)](https://www.gov.wales/sites/default/files/statistics-and-research/2025-01/evaluation-of-the-minimum-price-for-alcohol-in-wales--final-report-on-research-with-retailers-and-quantitative-analysis.pdf)
  - [Contribution-analysis final report (Report 80/2024)](https://www.gov.wales/sites/default/files/statistics-and-research/2025-01/final-report-review-of-the-introduction-of-minimum-pricing-for-alcohol-in-wales_0.pdf)
  - A web-search snippet of the retailer report says Wales had a smaller COVID-era purchase surge than England and a faster decline afterwards (Kantar 2016–2023). It is unverified and has no page number.
- **NT repeal** (Miller 2026, PMID 42299053). One month after the repeal, 5.1% of wine and 2.5% of cider were available below A$1.30 per standard drink. This included 67.6% of the 37 wine products sold in vessels of 1 L or more.

## 3. Policy dates verified

| Fact | Verified value | Source (official unless noted) | Status |
|---|---|---|---|
| Scotland MUP start | 1 May 2018, 50 pence/unit | SSI 2018/135 art.2: https://www.legislation.gov.uk/ssi/2018/135/made | ✔ matches |
| Scotland uprating | 65 pence from 30 Sep 2024 (made 23 Apr 2024) | SSI 2024/128: https://www.legislation.gov.uk/ssi/2024/128/made. Continuation: SSI 2024/127 | ✔ matches |
| Wales MUP start | 2 Mar 2020, £0.50 | WSI 2019/1472 (W.260) reg.1(2), 2: https://www.legislation.gov.uk/wsi/2019/1472/made | ✔ matches |
| Wales rise to 65p | **Legislated and in force**: £0.65 from 1 Oct 2026 (made 6 Feb 2026) | WSI 2026/34: https://www.legislation.gov.uk/wsi/2026/34/made. The revised reg.2 shows £0.65 from 2026-10-01. The sunset was removed by the Continuation Regs, WSI 2026/30 (in force 9 Feb 2026): https://www.legislation.gov.uk/wsi/2026/30/made | ✔ happened |
| Ireland MUP start | 4 Jan 2022; €0.10 per gram (= €1.00 per 10 g standard drink); s.11 Public Health (Alcohol) Act 2018 | irishstatutebook.ie and gov.ie **not reachable**. Date confirmed only secondarily: HRB blog 13 May 2021 (announced for "January 2022": https://www.hrb.ie/blog/drug-and-alcohol-evidence-blog/alcohol-the-evidence-and-minimum-unit-pricing/), plus Dáil PQ and law-firm summaries via web search. Commencement S.I. number: [REF NEEDED] | ◐ secondary only |
| NT floor price | 1 Oct 2018, A$1.30/standard drink | nt.gov.au not reachable. Peer-reviewed: Taylor et al. JSAD 2023 (PMID 37014647, "From October 1, 2018 … AU$1.30 per standard drink") | ◐ peer-reviewed, not official |
| **NT repeal (new)** | Repealed **1 Mar 2025**: Liquor Legislation Amendment (Repeal of Minimum Pricing) Act 2025 (No. 2 of 2025) | NT Gazette S9, 28 Feb 2025 (via web search): https://nt.gov.au/__data/assets/pdf_file/0006/1485825/S9-28-February-2025.pdf. Miller et al. Addiction 2026 (PMID 42299053) | ⚠ not in brief |
| NT co-policy: BDR | Reintroduced Sept 2017 | LEARNT protocol, BMJ Open 2022 (PMID 35365540). DAR 2026 (PMID 42152233) | ✔ (peer-reviewed) |
| NT co-policy: PALIs | PALIs introduced in Alice Springs 1 Oct 2018 (Darwin/Palmerston had MUP only); NT-wide PALI start dates/other towns [REF NEEDED] | Taylor et al. JSAD 2023 (PMID 37014647); Addiction 2021 (PMID 33891373) | ✔ (peer-reviewed) |
| England | No MUP. Only Scottish and Welsh MUP instruments on legislation.gov.uk. July 2025 DHSC: "not something the government has chosen to proceed with at this time" (press reports) | legislation.gov.uk title search; press via web search | ✔ |
| Northern Ireland | No MUP. DoH consultation launched Feb 2022 ([health-ni.gov.uk](https://www.health-ni.gov.uk/news/swann-seeks-views-minimum-unit-pricing-alcohol)). Mar 2026: Health Minister said MUP won't be introduced this Assembly term because there is no Executive agreement (press: derrynow.com, British Liver Trust) | health-ni.gov.uk not reachable; secondary only | ✔ (secondary) |
