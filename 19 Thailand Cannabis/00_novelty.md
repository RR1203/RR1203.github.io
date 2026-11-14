# 00 Novelty and policy timeline

Searched 14 Nov 2026.

## Verdict

**Novel.** I found no peer-reviewed paper or preprint that tests whether hospital admissions, psychosis or poisoning changed after the June 2025 re-regulation. The "on" phase is published. The "off" phase is not.

## Searches run

| Database | Query (short form) | Hits screened | Relevant to the 2025 reversal × health outcomes |
|---|---|---|---|
| PubMed (E-utilities, from 2022) | Thailand AND cannabis AND (2025 OR recriminali* OR relist* OR reversal) | 111 unique PMIDs across 2 queries | 0 |
| PubMed | Thailand AND cannabis AND (psychosis OR admission* OR hospitali* OR poisoning OR emergency) | (in the 111 above) | 0 |
| Europe PMC (includes preprints, 2023–2026) | (Thailand AND cannabis) AND (2025 OR relisting OR "re-regulation" OR "controlled herb") AND (hospital* OR psychosis OR poisoning) | about 60 | 0 |
| Europe PMC | Thailand cannabis legalisation hospitalisation / Thailand cannabis psychosis | about 80 | 0 |
| Web (Google-type), English | Thailand cannabis 2025 re-regulation admissions psychosis; medRxiv/SSRN interrupted time series | 2 searches | 0 (news and advocacy figures only) |
| Web, Thai (ThaiJO) | กัญชา ผู้ป่วยจิตเวช หลังควบคุม 2568 ThaiJO ผู้ป่วยใน | 1 search | 0 (single-hospital and pre-2025 studies) |

I did not search Google Scholar directly; the web search tool stood in for it. ThaiJO was reached only through web search, not its own search engine.

## Closest prior work

| Study | What it covers | Why it is not the "off" study |
|---|---|---|
| Puetpaiboon S, …, Chongsuvivatwong V. *Addiction* 2026;121(10):2768–79. doi:10.1111/add.70484 | Interrupted time series of weekly substance-related admissions, age 10–19, THIP, Oct 2016 – Sep 2023. Cannabis: +25.5 admissions/week (95% PI 23.5–27.2), 1,762 excess, +303%. | "On" phase only. Ends Sep 2023. |
| Freeman TP et al. *Lancet Psychiatry* 2026;13(7):615–26. doi:10.1016/S2215-0366(26)00087-8 | International review of cannabis policy and psychiatric outcomes. A co-author (Kalayasiri) is Thai. | Review. No new Thai data. |
| Kitcharoen P et al. *J Cannabis Res* 2026;8:97. doi:10.1186/s42238-026-00462-4 | Qualitative: 13 Bangkok operators during the shift to medical-only. Estimates tourists at about 60% of the market. | No health outcomes. |
| Chumchuen K et al. *PLoS One* 2024;19:e0312139. doi:10.1371/journal.pone.0312139 | Cannabis-related admissions × TB, monthly × province, 2017–2022 (national inpatient databank). | Shows that monthly × province cannabis admissions exist in the PSU group's data. Ends 2022. |
| Kalayasiri R, Boonthae S. *BMC Public Health* 2023;23:911. doi:10.1186/s12889-023-15883-6 | CADS surveys: past-year use 2.2% (2019), 2.5% (2020), 4.2% (2021). | Use prevalence, not admissions. |
| *J Cannabis Res* 2026, doi:10.1186/s42238-026-00495-9, "Surveillance of healthcare utilisation related to cannabis following the introduction of medical cannabis in Thailand" | Surveillance after medical cannabis (2019 onward). | Full text not reachable (blocked, then not re-tried). Whether it covers months after June 2025 is unknown [REF NEEDED]. **Check this paper first; it is the most likely overlap.** |
| Ramathibodi Poison Center, *Clin Toxicol* 2025 (PMID 40905855) | Cannabis exposures 2018–2022. | Ends 2022. |

Grey literature: an open letter from an anti-drug network of doctors, academics and civil society (9 Jun 2026, hosted on hfocus.org) cites national monthly HDC inpatient counts. Cannabis-induced psychosis (F12.5) went from about 85 to 556 per month by year 3, dependence (F12.2) from about 130 to 830, and poisoning (T40.7) from 30–40 to 115 (year 1), then 83 and 60. The series ends around mid-2025. This is an advocacy source. Its numbers are used here only as context and as power inputs.

## Methods of the "on" study, for comparable outcome definitions

From the full text (PMC13578852):
- Source: THIP, an inpatient data warehouse run by NHSO, PSU and NSTDA. It includes all hospital admissions, both residents and non-residents. It has no outpatient or ED visits. Access is through the THIP gateway after ethics approval.
- Unit: hospitalisation events. Same-day admissions and transfers are merged into one event, then aggregated to **weekly national** counts.
- Outcomes: 8 substance categories built from ICD-10 codes, using **any diagnosis** ("all diagnoses affecting patient care are coded"). The exact code list is in Supplementary Table S1, which I did not retrieve [REF NEEDED].
- Model: GLM counterfactual (Poisson or NB, with or without zero inflation). Predictor sets: linear trend plus AR(1), then seasonality, then holidays. COVID level and slope terms from 18 Jul 2021. Selection by residual diagnostics, AICc and rolling-origin cross-validation. Results: excess cases from 1,000 parametric-bootstrap trajectories (95% PI).
- Negative control: appendicitis K35–K37.
- Population offset: Bureau of Registration Administration mid-year counts by age and sex.

How this project differs: monthly rather than weekly, national **and province**, two breakpoints in one model (segmented NB) rather than a pre-period-only counterfactual, all ages with an under-20 / 20+ split, and F10/F15 used as comparison outcomes in a DiD. The ICD rule ("any diagnosis") matches theirs for F12.

## Policy timeline (verified as far as possible)

The Royal Gazette site (ratchakitcha.soc.go.th) was behind a Cloudflare challenge and could not be opened. Gazette volume and page numbers are [REF NEEDED]. Everything below comes from news and law-firm sources, read as search excerpts.

| Date | Event | Source |
|---|---|---|
| 19 Feb 2019 | Narcotics Act (No. 7): medical cannabis legal | Addiction 2026 intro |
| 8 Feb 2022 | Ministry of Public Health Notification "Specifying Category 5 Narcotics B.E. 2565" signed by Anutin. Cannabis/hemp plant removed; extracts >0.2% THC stay narcotic. | https://www.thaipost.net/hi-light/82204/ ; https://www.thansettakij.com/general-news/513395 |
| 9 Feb 2022 | Published in the Royal Gazette | thaipost (above) |
| **9 Jun 2022** | **Notification takes effect ("on")** | https://assets.kpmg.com/content/dam/kpmg/th/pdf/2022/03/legal-news-flash-issue-11.pdf ; Reuters via https://www.inkl.com/news/thailand-legalises-growing-consumption-of-marijuana |
| 8 May 2024 | PM Srettha says he has asked MoPH to relist cannabis as a narcotic (first anticipation date) | https://www.scmp.com/news/asia/southeast-asia/article/3261912/thailand-pm-srettha-outlaw-cannabis-end-2024-stunning-u-turn-just-2-years-after-it-was |
| mid/late 2024 | Relisting plan dropped in favour of a Cannabis Act (exact date [REF NEEDED]) | https://www.thaipbsworld.com/health/thai-government-to-reclassify-cannabis-as-narcotic |
| 22 May – 15 Jun 2025 | DTAM public consultation on the draft notice (second anticipation date) | Thai search results [REF NEEDED for primary URL] |
| 23 Jun 2025 | Health Minister Somsak signs MoPH Notification "Controlled Herbs (Cannabis) B.E. 2568" (under the Thai Traditional Medicine Wisdom Act) | https://thethaiger.com/hot-news/cannabis_news/thailands-cannabis-recriminalisation-whats-the-damage |
| 25 Jun 2025 | Published in the Royal Gazette | https://www.bangkokbiznews.com/health/public-health/1186954 (excerpt) |
| **26 Jun 2025** | **Takes effect ("off")**: flower is a controlled herb. Sale needs a DTAM licence. Sale only on prescription from listed professions, max 30-day supply. Online sale banned. | https://www.thaipbs.or.th/news/content/353622 ; AP via https://www.news4jax.com/news/world/2025/06/27/thailand-starts-banning-the-sale-of-cannabis-without-a-prescription/ ; https://www.tilleke.com/insights/new-developments-in-thailands-cannabis-law/22/ |
| 17 Mar 2026 (effective 26 Apr 2026) | Ministerial regulation allowing medical use of extracts >0.2% THC (still Category 5) | hfocus open letter, 9 Jun 2026 |
| 22 Sep 2026 | Cabinet approves draft Cannabis Control Bill (medical-only) | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/09/22/thailand-moves-to-rein-in-cannabis-industry-reverse-decriminalisation-policy |

The prompt's dates (9 Jun 2022, 26 Jun 2025) agree with these sources. One correction: the 2025 change is a "controlled herb" notification under traditional-medicine law, **not** relisting as a narcotic. As of Nov 2026, cannabis flower is still not a narcotic.
