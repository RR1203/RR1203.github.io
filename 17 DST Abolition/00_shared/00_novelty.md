# Step 0.1: Novelty and literature check (DST abolition: Mexico 2022, Brazil 2019)

Date of search: 2026-11-14. Every source below was retrieved as a record (PubMed or Europe PMC record, OpenAlex record, RePEc page, or PDF) in this session. Effect sizes come from the abstract or full text as retrieved. Nothing here is cited from memory.

Access limits in this session: SciELO (search.scielo.org) and SSRN returned HTTP 403, and zenodo.org, pnas.org, doi.org, crossref and suicideinfo.ca were blocked by the network proxy. SciELO and SSRN were covered indirectly through OpenAlex (which indexes SciELO preprints and SSRN DOIs) and through site-restricted WebSearch. The RePEc full-text search did not parse, so RePEc was covered by WebSearch restricted to ideas.repec.org plus direct page reads.

## 1. Search log

| Database | Query (abridged) | Date | Hits returned / screened (titles) |
|---|---|---|---|
| Europe PMC | ("daylight saving" OR "summer time" OR "horario de verano" OR "horário de verão") AND (Brazil OR Brasil) | 2026-11-14 | 242 / 25 |
| Europe PMC | ("daylight saving" OR "horario de verano") AND (Mexico OR México) | 2026-11-14 | 60 / 25 |
| Europe PMC | "daylight saving" AND (abolition OR abolish* OR repeal OR "permanent standard time" OR elimination) | 2026-11-14 | 162 / 25 |
| Europe PMC | "horário de verão" ; "horario de verano" | 2026-11-14 | 2 / 2 ; 1 / 1 |
| Europe PMC | ("daylight saving" OR "summer time" OR "clock change") AND (suicide OR "self-harm" OR psychiatric) AND (Brazil OR Mexico OR "Latin America") | 2026-11-14 | 61 / 25 |
| Europe PMC | ("daylight saving" OR "clock change") AND ("myocardial infarction" OR mortality OR traffic) AND (Brazil OR Mexico) | 2026-11-14 | 51 / 25 |
| Europe PMC | ("end of daylight saving" OR "abolition of daylight saving" OR "suspension of daylight saving" OR "daylight saving time ended") AND (Brazil OR Mexico OR 2019 OR 2022) | 2026-11-14 | 17 / 17 |
| Europe PMC | ("horario de verano" OR "cambio de horario") AND (suicidio OR mortalidad OR infarto OR accidentes OR homicidio OR sueño) | 2026-11-14 | 5 / 5 |
| Europe PMC | ("horário de verão") AND (suicídio OR mortalidade OR infarto OR acidentes OR internações OR sono) | 2026-11-14 | 1 / 1 |
| OpenAlex | daylight saving time Brazil ; ... Mexico | 2026-11-14 | 4,291 / 25 ; 5,069 / 25 |
| OpenAlex | horário de verão ; horario de verano | 2026-11-14 | 19,827 / 25 ; 24,565 / 25 |
| OpenAlex | fim do horário de verão 2019 efeitos ; eliminación del horario de verano México 2022 | 2026-11-14 | 5,245 / 25 ; 348 / 25 |
| OpenAlex | daylight saving time abolition natural experiment ; Mexico abolished daylight saving time 2022 effect ; ... end Brazil 2019 health ; ... sleep Brazil end ; ... Mexico 2022 sleep | 2026-11-14 | 343 / 25 ; 42 / 25 ; 1,050 / 25 ; 821 / 25 ; 11 / 11 |
| OpenAlex | DST homicide Brazil ; crime Mexico ; suicide Mexico ; Quintana Roo ; horario de verano Sonora salud mental ; horário de verão homicídios Brasil | 2026-11-14 | 74 ; 964 ; 368 ; 31 ; 708 ; 381 (25 each screened) |
| OpenAlex | "daylight saving time is causing suicide" ; DST incidence of myocardial infarction regression discontinuity | 2026-11-14 | 1 / 1 ; 42 / 6 |
| PubMed (MCP) | daylight saving time myocardial infarction meta-analysis | 2026-11-14 | 2 / 2 |
| PubMed (MCP) | daylight saving time fatal motor vehicle crashes ; "daylight saving time"[Title] AND (traffic OR crash* OR accident*) | 2026-11-14 | 4 / 4 ; 54 / 20 |
| PubMed (MCP) | Janszky Ljung DST MI ; Fritz J / Carey RN DST traffic | 2026-11-14 | 2 / 2 ; 3 / 3 |
| NBER API | daylight saving | 2026-11-14 | 2,161 / 50 (no Brazil/Mexico/abolition paper) |
| RePEc (ideas) | direct page RePEc:amc:wpaper:02 ; site-restricted WebSearch on DST Brazil/Mexico abolition | 2026-11-14 | 1 ; 10 / 10 |
| WebSearch | Lins Menezes DST suicide IEPS ; Plöderl DST suicide ; PNAS Stanford time policy | 2026-11-14 | 10 / 10 each |
| WebSearch | end of DST Brazil 2019 study (EN) ; fim do horário de verão 2019 estudo (PT) ; eliminación horario de verano México 2022 estudio (ES) ; Mexico 2022 abolition natural experiment (EN) | 2026-11-14 | about 10 / 10 each |

## 2. Verified sources

### 2a. The three named claims

| Citation | Link (retrieved) | Country | Design | Outcome | Finding as stated in the source |
|---|---|---|---|---|---|
| Lins JGMG, Menezes TA. *Daylight Saving Time is causing suicide.* IEPS Working Paper (Texto para Discussão) No. 2, February 2020. A journal version is listed for Revista de Estudos Sociais (Cuiabá) 25(50):62-82, 2023 (PDF not retrievable, so unverified beyond the listing). | PDF read: https://ieps.org.br/wp-content/uploads/2021/11/WPS2.pdf ; RePEc:amc:wpaper:02 https://ideas.repec.org/p/amc/wpaper/02.html | Brazil (RS treated; PR and SC used as "untreated" comparison) | Sharp RDD at the **DST start** date (day before vs. first days after), about 10 years of SIM mortality data | Suicide deaths (daily rate) | Abstract: DST transition "in average increase the treated state suicide rate in about 57% (p-valo = 0.011), and this result is precisely zero in others untreated states"; about +2% per 1,000 km of latitude. Table 1: RS coefficient 1.33 (SE 0.53) and PR+SC −0.33 (SE 0.31). **The claim is confirmed: 57%, Rio Grande do Sul, 2020.** Caveats: PR and SC also observed DST but are labelled "untreated"; the paper studies DST onset, not abolition. |
| Plöderl M, Pichler EM, Westerlund J, Niederseer D, Fartacek C. *Daylight saving time was not associated with a change in suicide rates in Austria, Switzerland and Sweden.* Eur J Public Health 2024;34(4):717-722. | PMID 38561196; doi:10.1093/eurpub/ckae061; PMC11293815 | Austria, Switzerland, Sweden | Preregistered; 2 weeks before vs. after the transitions, 1980-2022; Poisson regression plus changepoint analysis | Suicide | After DST start: adjusted IRR 0.98 (95% CI 0.91-1.06), n = 13,362. After DST end: IRR 0.99 (0.91-1.07), n = 12,319. No subgroup (age, region) effects and no changepoints. **Claim confirmed** (null result). |
| Weed L, Zeitzer JM. *Circadian-informed modeling predicts regional variation in obesity and stroke outcomes under different permanent US time policies.* PNAS 2025;122(38). | doi:10.1073/pnas.2508293122; PMID 40953265 (Europe PMC record) | USA (contiguous) | Circadian light-exposure model by county, regressed on CDC PLACES county health data. **A modelling study, not observed outcomes.** | Obesity and stroke prevalence | Compared with current biannual shifting: permanent standard time gives obesity −0.78% (−0.06 to −1.49) and stroke −0.09% (−0.04 to −0.14); permanent DST gives obesity −0.51% and stroke −0.07%. The study supports ending biannual shifting. **Confirmed: Stanford (Zeitzer), PNAS 2025, published September 2025 per press coverage.** The "300,000 strokes / 2.6 million fewer obese" figures come from Stanford press coverage, not the abstract. |

### 2b. Brazil and Mexico DST studies (any outcome)

| Citation | Link | Country | Design | Outcome | Finding (as stated) | Uses abolition? |
|---|---|---|---|---|---|---|
| Watanabe K. *Abolishing Daylight Saving Time and the Clock-Hour Distribution of Road Crashes: Evidence from Brazil (2019) and Mexico (2022).* Zenodo preprint, 2026-11-05. | doi:10.5281/zenodo.23980727 (OpenAlex record; zenodo.org blocked) | Brazil, Mexico | Registered DiD comparing former-DST and never-DST states, before vs. after abolition; ln(evening/morning crash ratio) | Road crashes (clock-hour distribution). Not fatalities or health outcomes. | Brazil (federal highways): DiD −0.120 (−0.194 to −0.052), but the falsification estimate in June-August is the same size (−0.126). Mexico (urban crashes): 0.059 (−0.045 to 0.164). Abstract: "Neither country shows a detectable abolition-specific shift of crashes toward the evening." | **Yes** (the only abolition natural experiment found). Unrefereed preprint. |
| Goodwin MB, González F, Fontenla M. *The impact of daylight saving time in Mexico.* Appl Econ 2024;56(1):22-32 (online 2023). | doi:10.1080/00036846.2023.2166666 | Mexico | RDD at the transitions, 1998-2018 | Road-traffic, AMI and crime-related deaths | Road deaths +13-14% at both transitions. Crime deaths +16% (fall). AMI: only a small urban increase in spring. About 100 extra deaths per year. | No (pre-abolition) |
| Hancevic PI, Salas Rodríguez H. *The unexpected effects of daylight-saving time: Traffic accidents in Mexican municipalities.* EconoQuantum 2022;20(1). | doi:10.18381/eq.v20i1.7268 | Mexico | RDD plus DiD, hourly data | Traffic accidents | DST significantly reduces total accidents in metro areas; no clear effect on fatal accidents. | No |
| Poblano A, Téllez-Alanís B, Aldrete-Cortez V. *Cambio de horario, calidad de sueño y somnolencia excesiva diurna en universitarios.* Salud Publica Mex 2024;66(6):896-897. | PMID 39977165; doi:10.21149/15634 | Mexico | Letter (no abstract available) | Sleep quality, sleepiness | Content not retrieved: unverified whether it concerns the 2022 abolition. | Unverified |
| Toro W, Tigre R, Sampaio B. *Daylight Saving Time and incidence of myocardial infarction: Evidence from a regression discontinuity design.* Econ Lett 2015;136:1-4. | doi:10.1016/j.econlet.2015.08.005 (OpenAlex metadata only) | Brazil | RDD at DST onset | AMI | Abstract not retrieved. The "+7-8.5% AMI deaths" figure comes only from a secondary news snippet: **[REF NEEDED] to confirm.** | No |
| Franco C, Toro W, Sampaio B, Sampaio GR. *Daylight Saving Time and road accidents in Brazil.* SSRN 2021 and SciELO Preprints 2023 (PT version). | doi:10.2139/ssrn.3899538 ; doi:10.1590/scielopreprints.6458 | Brazil | RDD (onset) plus DiD, federal highways 2007-2013 | Road accidents | DST reduces accidents on federal highways (about 14% in the first weeks according to the SSRN snippet; the PT abstract says a reduction). | No |
| Ramos L, Tai SHT. *O impacto do horário de verão nos acidentes de trânsito em Porto Alegre.* Análise Econômica 2025. | doi:10.22456/2176-5456.110967 | Brazil (Porto Alegre) | Fixed effects, Jan 2010 to Dec 2019 | Traffic accidents | DST reduces traffic accidents by 7.4%. The data window includes 2019 but the abstract does not frame the study as an abolition analysis. | Unclear (not framed as abolition) |
| Cortes RX, Fochezatto A, Jacinto PA. *Daylight saving time and homicides: light effect in crimes of a Brazilian state.* Análise Econômica 2021. | doi:10.22456/2176-5456.80052 | Brazil (RS) | RDD, SIM 2006-2014 | Homicide | No significant effect of DST on homicide at start or end. | No |
| Toro W, Tigre R, Sampaio B. *Daylight Saving Lives: the effect of daylight saving time on homicides.* SSRN 2016. | doi:10.2139/ssrn.2786452 | Brazil (per authors and the thesis record; abstract not retrieved) | [details unverified] | Homicide | Unverified | No |
| Alencar JCN et al. *Self-reported discomfort associated with DST in Brazilian tropical and subtropical zones.* Ann Hum Biol 2017. | doi:10.1080/03014460.2017.1355982 | Brazil | Survey | Self-reported discomfort | Not extracted | No |
| Steponenaite A et al. *A systematic review of epidemiological studies into daylight-saving time & health.* Eur J Epidemiol 2026;41(4):419-433. | doi:10.1007/s10654-026-01372-8 | 36 countries, 157 studies | Systematic review (to June 2025) | Multiple | DST onset is associated with more AMI and fatal traffic accidents. Living with DST in summer is associated with lower all-cause mortality and fewer traffic accidents. | Review; no abolition study named in the abstract |
| Osborne-Christenson EJ. *Saving light, losing lives.* Health Econ 2022;31 Suppl 2:40-68. | PMID 36000150; doi:10.1002/hec.4581 | USA | RDD plus FE, 1979-1988 | Suicide, substance-related deaths | Spring transition: suicide +6.25%; no fall effect. | No |

### 2c. Positive-control references (transition effects on AMI and road traffic)

| Citation | Link | Design | Finding (as stated) |
|---|---|---|---|
| Hurst A, Morfeld P, Lewis P, Erren TC. *Daylight Saving Time Transitions and Risk of Heart Attack.* Dtsch Arztebl Int 2024;121(15):490-496. | PMID 38888468; doi:10.3238/arztebl.m2024.0078 | SR/MA, 12 studies from 10 countries | Spring: pooled RR 1.04 (1.02-1.07), I² 57%. Autumn: RR 1.02 (0.99-1.05). The authors call for RDD and comparisons with years or places without DST. |
| Manfredini R et al. *Daylight Saving Time and Acute Myocardial Infarction: A Meta-Analysis.* J Clin Med 2019;8(3):404. | PMID 30909587; doi:10.3390/jcm8030404 | MA, 7 studies, >115,000 subjects | Spring: OR 1.05 (1.02-1.07). Autumn: OR 1.01 (0.98-1.04). |
| Janszky I, Ljung R. *Shifts to and from daylight saving time and incidence of myocardial infarction.* N Engl J Med 2008;359(18):1966-8. | PMID 18971502; doi:10.1056/NEJMc0807104 | Swedish registry (letter) | No abstract in the record; effect size not extracted here. |
| Fritz J, VoPham T, Wright KP, Vetter C. *A Chronobiological Evaluation of the Acute Effects of Daylight Saving Time on Traffic Accident Risk.* Curr Biol 2020;30(4):729-735. | PMID 32008905; doi:10.1016/j.cub.2019.12.045 | US FARS, 732,835 fatal crashes, 1996-2017 | Spring DST increased fatal crash risk by 6%, more in the morning and in western parts of a time zone. No fall effect. |
| Carey RN, Sarma KM. *Impact of daylight saving time on road traffic collision risk: a systematic review.* BMJ Open 2017;7:e014319. | PMID 28674131; doi:10.1136/bmjopen-2016-014319 | SR, 24 studies | Short-term transition findings were inconsistent. Long-term findings suggested a benefit, but this could not be attributed solely to DST. |
| Woods AN, Weast RA, Monfort SS. *Daylight saving time and fatal crashes: the impact of changing light conditions.* J Safety Res 2025;93:200-205. | PMID 40483055; doi:10.1016/j.jsr.2025.02.010 | US, 2010-2019, 5 weeks before vs. after | Spring: motor-vehicle-occupant fatal crashes +12% and pedestrian/bicyclist −24%. Fall: occupants −7.1% and pedestrian/bicyclist +13%. |

## 3. Novelty matrix

| | Q1: transition excess disappears where clock changes stopped | Q2: chronic effect of year-round standard time (suicide, self-harm, psychiatric admissions, AMI, road deaths, homicide) |
|---|---|---|
| **Mexico** | **Not studied** using the abolition. Pre-abolition transition RDDs exist (Goodwin et al. 2024: road, AMI and crime deaths; Hancevic & Salas 2022: crashes), and they serve as baseline evidence. | **Partially studied (Watanabe 2026 preprint)**: abolition DiD on the evening/morning crash ratio only, null. No study of suicide, self-harm, psychiatric admissions, AMI, road deaths or homicide after 2022 was found. |
| **Brazil** | **Not studied** using the abolition. Pre-abolition onset RDDs exist (Lins & Menezes 2020: suicide; Toro et al. 2015: AMI; Franco et al.: crashes; Cortes et al. 2021: homicide). | **Partially studied (Watanabe 2026 preprint)**: abolition DiD on the crash clock-hour ratio, null and not distinguishable from a placebo-season divergence. Ramos & Tai 2025 (Porto Alegre crashes, 2010-2019) is not framed as an abolition study. No abolition study of suicide, self-harm, psychiatric admissions, AMI, road deaths or homicide was found. |

**Abolition as a natural experiment:** only one study was found, Watanabe 2026 (Zenodo, unrefereed, posted 2026-11-05). It covers both countries, but only for the timing distribution of road crashes. No study was found that uses the 2019 Brazilian or the 2022 Mexican abolition for mortality, hospital admissions, suicide, self-harm, AMI, homicide or sleep. The Poblano 2024 letter (Salud Publica Mex) could not be read and remains unverified.

## 4. Verdict per arm

- **Mexico arm:** Q1 not done; Q2 partly done (crash timing only). **Not stopped.** Proceed.
- **Brazil arm:** Q1 not done; Q2 partly done (crash timing only). **Not stopped.** Proceed.
- Implications: (i) the Q2 road-traffic outcome must cite Watanabe 2026 and position itself relative to it. Our outcomes are road-traffic *deaths* and health/crime outcomes, not the crash clock-hour ratio. Its placebo-season problem in Brazil (regional divergence in June-August) is a direct warning for our design. (ii) Lins & Menezes' 57% suicide estimate at RS DST onset is a fragile single-state working-paper estimate (PR and SC also had DST but showed nothing), and Plöderl et al. 2024 found nothing in Europe. Treat any suicide hypothesis as uncertain.
- Open items: re-check Zenodo, SciELO and SSRN directly when network access allows. Confirm the Toro et al. 2015 AMI effect size [REF NEEDED]. Read Poblano 2024.
