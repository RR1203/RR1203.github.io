# HANDOVER — Thailand cannabis on/off (decriminalised Jun 2022, re-regulated Jun 2025)

Single handover file. It brings together SUMMARY.md, 00_novelty.md, 00_data_access.md, draft_email.md, outcome_codes.csv, the first-stage data and DECISIONS.md. The original files are unchanged.

**Status (14 Nov 2026):** The data-access gate failed, so the main analysis was not run. First stage and power are done. The analysis code is ready and starts automatically once `raw_admissions.csv` is added.

**Next decision:** (a) pull HDC province × month reports by hand from the Mac, or (b) send the email in section 4 to the PSU/THIP group. Then put `raw_admissions.csv` (month, province, age_group, outcome_id, admissions, population) in this folder and run `Rscript -e 'rmarkdown::render("analysis.Rmd")'`.

## Contents
1. Summary (audit, Methods/Results, recap, scorecard)
2. Novelty and policy timeline
3. Data access and access plan
4. Draft collaboration email (NOT sent)
5. Outcome codes
6. First-stage and context data (with sources)
7. Decision log
8. File index

---

# 1. Summary

**FLAG:** The data-access gate failed. No source with monthly × province × ICD-10 admissions after June 2025 could be reached: HDC and NHSO refuse non-Thai IPs, THIP needs ethics approval, and data.go.th and the Royal Gazette sit behind Cloudflare. H1–H3, the DiD, event studies and all checks were therefore **not run**. Other deviations: run in the cloud rather than on a Mac. The network allowlist was widened by 19 exact hosts, not set to Full. Primary SEs are model-based NB rather than Newey-West, because the power simulation showed NW was anti-conservative. Appendicitis was added as a negative control. One helper function and replicate() were used for the power simulation.

**Scorecard (0–10, based on what the data showed)**

| Novelty | First stage | Power | Big result | Rigor | Feasibility |
|---|---|---|---|---|---|
| 9 | 6 | 6 | n/a (not run) | 7 | 3 |

- Novelty: no study of the 2025 reversal found in PubMed, Europe PMC or Thai/English web searches. One unread 2026 J Cannabis Res surveillance paper still needs checking.
- First stage: the fall is documented (84.5% of 2025-expiring licences not renewed). The rise from 2022 to mid-2025 has no verified counts, and there is no province time series.
- Power: national F12.5 and F12.2 can detect a 15–20% drop if overdispersion is low (theta 100), but only 30–40% if it is high (theta 25).
- Feasibility: it depends on a Thai collaborator or Thai IP.

**Is cannabis harm reversible after re-regulation?** Not answerable yet. The admissions data after June 2025 exist (HDC, THIP) but could not be reached from this run, so no estimate was made.

---

### 1. What the code did

1. Read the sourced first-stage values — `raw_first_stage.csv`, 28 hand-entered rows, each with source URL and verification status → `raw_first_stage`
2. Read the outcome definitions — `outcome_codes.csv`, 9 outcomes (F12, F12.5, F20–F29, T40.7, F10, F15, K35–K37, all IP, F chapter) → `codes`
3. Split the rows by table — shops n = 14, survey n = 5, HDC/Addiction context means n = 9 → `shop_panel`, `survey_prevalence`, `hdc_context`
4. Built the admissions panel — `raw_admissions.csv` absent, so an empty template (0 rows) → `admissions_panel`
5. Wrote the clean workbook — 5 sheets → `clean_data.xlsx`
6. Computed licence non-renewal — 8,636 expired, 1,339 renewed, 7,297 not renewed (84.5%); 7,297 / 18,433 = 39.6% of all establishments → printed
7. Plotted shop counts — national points Dec 2025 – Nov 2026 only → `figures/first_stage_shops.png`
8. Plotted CADS past-year use — 2019–2021 → `figures/first_stage_survey.png`
9. Built the simulation grid — monthly Jan 2017 – Oct 2026, 118 months, 65 before June 2022 → `p1_grid`
10. Simulated power for the 2025 level drop — NB data (theta 25 / 100), segmented glm.nb (trend, month FE, COVID Mar 2020 – Dec 2021, level and slope at Jun 2022 and Jul 2025), model-based Wald test, 200 replicates × 7 drop sizes × 4 outcomes × 2 theta × 2 follow-ups (12 / 16 post months) → `p1_power`
11. Derived the MDE at 80% power and labelled it (powered if MDE ≤ 20%) → `p1_mde`, `figures/power_mde.png`
12. Saved the status, first stage and power results → `results.rds`

**Unverified:** All shop counts and the ONCB/PeerJ survey figures come from search-engine excerpts; the pages were not opened. The HDC means come from an advocacy open letter. Royal Gazette volume and page numbers are unknown. The 2022 jump size, the +8%/yr pre-trend, the 5% seasonality and theta are assumed. F20–F29, F10 and F15 have no baseline counts, so they were not simulated.
**Not run:** H1 (symmetry, event studies, DiD vs F10/F15, age split, placebo Jun 2020 / Jun 2024, anticipation May 2024 / May 2025, coding check), H2 (dose, tourism provinces, leave-one-province-out), H3 (F12.5, F20–F29, T40.7). The code is written and was smoke-tested on a simulated panel only (scratchpad, not saved): it recovered a symmetry level ratio of −0.98 (95% CI −1.11 to −0.86) against a truth of −1.

---

### 2. Methods and Results

**Methods.** The planned design was a monthly segmented negative-binomial time series of national and provincial admissions, January 2017 to the latest available month. It has breakpoints in June 2022 (delisting effective 9 June 2022) and July 2025 (controlled-herb notification effective 26 June 2025), with month-of-year fixed effects, a COVID-19 indicator (March 2020 – December 2021), and a population offset. The primary outcome was any-diagnosis F12, with F12.5, F20–F29 (principal diagnosis) and T40.7 as key secondary outcomes, and F10, F15 and appendicitis (K35–K37) as comparison outcomes. Symmetry was defined as the ratio of the 2025 to the 2022 log level change, with a 2,000-draw parametric bootstrap CI. Because no post-June-2025 admissions data could be obtained, only the first stage and an approximate power analysis were run. Power for the 2025 level change was estimated by simulation (200 replicates per scenario) under a negative-binomial data-generating process. Inputs were national monthly means from Health Data Center reports quoted in a June 2026 open letter (F12.5: 85 before 2022, 556 in year 3; F12.2: 130 and 830; T40.7: 35, 115 and 60) and from Puetpaiboon et al. 2026 (cannabis admissions age 10–19: about 27 and 150 per month). Model-based standard errors replaced Newey-West SEs after the simulation showed Newey-West type I error of 0.06–0.25 with 12–16 post-reversal months. Analyses used R 4.3.3 with MASS, sandwich and lmtest.

**Results.** Of 8,636 cannabis-shop licences that expired in 2025, 1,339 were renewed and 7,297 (84.5%) were not, which is 39.6% of the 18,433 establishments licensed by 28 December 2025. In November 2026, 12,279 outlets were licensed nationally, including 1,726 in Bangkok, 1,046 in Phuket, 900 in Chon Buri, 717 in Surat Thani and 482 in Chiang Mai. Past-year cannabis use among adults aged 18–65 rose from 2.2% (2019) to 2.5% (2020) and 4.2% (2021); no comparable 2022–2025 survey waves were found. With 16 post-reversal months, the minimum detectable level drop at 80% power was 15% for F12.5 and F12.2 at theta 100, and 30% at theta 25. For cannabis admissions age 10–19 it was 20% and 30%, and for T40.7 30% and 40%. Empirical type I error ranged from 0.020 to 0.085. With 12 post months, the MDEs were 20–30% (theta 100) and 30–40% (theta 25). A 40% drop, the largest simulated, was detected with power 0.93–1.00 in all 16 scenarios. A fully symmetric reversal (F12.5 back from about 556 towards 85 per month) would be a far larger drop than any simulated.

---

### 3. Recap

- Completed the novelty search, policy timeline, data-access audit, first stage and power analysis. Wrote the full two-breakpoint analysis code, but the main analysis did not run because the data-access gate failed.
- The reversal is unstudied. The shop fall is real (84.5% of expiring licences not renewed). National F12/F12.5 are powered for drops of 15–30% or more. Admissions data after June 2025 exist in HDC and THIP but cannot be reached from outside Thailand.
- Decide: (a) pull HDC province × month reports by hand on the Mac, or (b) send `draft_email.md` (not sent) to the PSU/THIP group. Then drop `raw_admissions.csv` into the folder and re-knit.

---

# 2. Novelty and policy timeline

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

---

# 3. Data access and access plan

**Result: GATE FAILED.** From this cloud session I could not find or reach any source with monthly × province × ICD-10 admissions that runs past June 2025. Under the protocol, the analysis stops here. The access plan is below, and `draft_email.md` holds the email (not sent).

## What each source offers

| Source | Public download? | Level | Time | ICD detail | Age | Latest | Status from this session |
|---|---|---|---|---|---|---|---|
| **HDC, MoPH** (hdcservice.moph.go.th) | Standard reports usually public; record-level data needs a login | Country → region → province → district | Fiscal year with monthly view | IPD reports by **4-character** code exist (the open letter quotes "IPD-F12.2", "IPD-F12.5", "IPD-T40.7" monthly, Oct 2019 – mid-2025) | Varies by report | Unknown; probably near real time | **Connection reset by peer** (×2, plus earlier ×2). Fits geo-blocking of non-Thai IPs. **Best candidate.** |
| **THIP** (PSU / NHSO / NSTDA), used by Addiction 2026 | **No.** Gateway access after ethics approval | Record level, national | Admission date | Any ICD-10, all diagnoses | Yes | Published use ends Sep 2023; warehouse coverage now unknown | Not public |
| NHSO UC info / data.go.th "IP services" (dataset-p_21_011) | Yes (CSV) | Probably national/region | Probably annual | **No diagnosis codes** in description | Not confirmed | Updated Sep 2026 (snippet) | data.go.th: Cloudflare 403. ucinfo.nhso.go.th: connection reset |
| data.go.th "Inpatients by disease group" (moph_20250210_05) | Yes (CSV) | "By area" | Probably annual | 298 disease groups, **not** 3/4-character codes | Not confirmed | 2019–2026 | Cloudflare 403 |
| Provincial HDC extracts on gdcc.data.go.th | Yes | One province | Annual | Total or 298 groups | No | Up to 2026 for some provinces | Not fetched |
| Department of Mental Health (dmh.go.th) | Annual statistics and press releases only | National / DMH hospitals | Annual | Top disease groups | No | 2023 | Homepage reachable; no monthly cannabis-psychosis series found |
| Strategy & Planning Division / NSO "Public Health Statistics" | Yes (PDF/XLS) | National | Annual | 298 groups, top 10 | No | 2023 | Not fetched |
| Health Region 8 cannabis dashboard (cloud1-r8way.moph.go.th) | Was public | 7 provinces, by hospital | Unknown | F12 subcodes | Unknown | "Data as of 15 May 2026" (snippet) | URL now serves an unrelated app. **Lost.** |
| Thai FDA "report-safety-cannabis" (catalog.fda.moph.go.th) | Yes | National | Unknown | Adverse-event reports, not admissions | Unknown | Unknown | Homepage 200; CKAN API reset |

## Blockers, in order of importance

1. **HDC and NHSO refuse connections from outside Thailand.** This needs a Thai IP or a person in Thailand.
2. **THIP is restricted.** It needs an application, ethics approval and a PSU collaborator.
3. data.go.th, opendata.moph.go.th and the Royal Gazette use a Cloudflare challenge. A headless-browser workaround was not allowed in this session. A normal browser on a Mac should get through.

## One-page access plan

**Goal:** monthly admissions, Jan 2017 – latest (≥ Dec 2025, ideally Oct 2026), by province (77) × age group (<20 / 20+), for F12 (any), F12.5, F20–F29, T40.7, F10, F15, K35–K37, all admissions, and the F chapter. Counts only, so no individual data is needed.

**Route A, fastest (1–2 weeks): HDC standard reports, by hand.**
- Who: Hannes, on a Mac in a normal browser. If the site is geo-blocked from Germany too, a Thai collaborator or a Thai VPN exit.
- Where: hdcservice.moph.go.th, report groups for in-patients (ผู้ป่วยใน), drugs (ยาเสพติด), mental health (สุขภาพจิตและจิตเวช), and cannabis (กัญชา).
- What: for each code, the province × month table per fiscal year 2017–2026, exported to Excel. Save the files untouched in `raw_downloads/hdc/`.
- Limits: HDC covers MoPH facilities, so university, military and private hospitals are under-represented. Age bands may not split at 20. The diagnosis-position rule (principal vs any) depends on the report.

**Route B, best quality (2–4 months): collaborate with the THIP / PSU group.**
- Who: Prof. Virasakdi Chongsuvivatwong and Dr Songyos Rajborirug (Dept. of Epidemiology, Faculty of Medicine, Prince of Songkla University), the Addiction 2026 team. Chumchuen et al. 2024 shows the same group already builds monthly × province cannabis admissions.
- Ask: aggregated counts only (province × month × age band × outcome, small cells suppressed), Oct 2016 – latest, using their exact Supplementary Table S1 cannabis code list so the "on" and "off" phases match. They run the code, so no record-level data leaves PSU.
- Needs: a short protocol (this repo's `analysis.Rmd` plus `outcome_codes.csv`), a co-authorship offer, and whatever ethics amendment PSU requires.

**Route C, first-stage data:** DTAM licence registry by province × month (issue, expiry and renewal dates). Ask DTAM (Department of Thai Traditional and Alternative Medicine) for an export of the "ปลูกกัญ" / shop-map database, or ask the PSU collaborator to request it. Without it, H2 (dose) cannot run. Only a single Nov 2026 snapshot for 5 provinces is public.

**Decision rule once data arrive:** drop `raw_admissions.csv` (columns: month YYYY-MM, province, age_group, outcome_id, admissions, population) and, optionally, `raw_shops_province_month.csv` into the project folder and re-knit `analysis.Rmd`. All hypothesis blocks switch on automatically.

---

# 4. Draft collaboration email (NOT sent)


**To:** Prof. Virasakdi Chongsuvivatwong; Dr Songyos Rajborirug (Department of Epidemiology, Faculty of Medicine, Prince of Songkla University). Email addresses: [REF NEEDED]
**Cc:** Dr Sirada Puetpaiboon (first author)
**Subject:** Collaboration: substance-related admissions after Thailand's June 2025 cannabis re-regulation

Dear Professor Chongsuvivatwong, dear Dr Rajborirug,

I read your *Addiction* paper on adolescent substance-related hospitalisations after the 2022 cannabis delisting (Puetpaiboon et al., 2026; doi:10.1111/add.70484) with great interest. I am writing to propose a follow-up together.

The June 2025 notification, which made cannabis flower a controlled herb sold only on prescription, offers a rare reverse experiment. As far as I can tell, no one has yet studied whether cannabis-related admissions fell after it. Shop licences make a clear first stage: of the 8,636 licences that expired in 2025, only 1,339 were renewed.

My plan is a monthly segmented time series with breakpoints in June 2022 and June 2025. The main measure is the ratio of the 2025 change to the 2022 change. F10 and F15 serve as comparison outcomes, and the analysis is split by age (<20 vs 20+) and province. Outcomes are F12, F12.5, F20–F29 and T40.7, using your published code definitions so that both phases match. The analysis code and outcome definitions are written and ready.

Would you be open to running a short extraction of **aggregated counts only** (province × month × age band × outcome, October 2016 to the latest month) from THIP? No record-level data would need to leave PSU. I would gladly offer co-authorship and fit in with any ethics amendment you need.

I would be happy to send the protocol and code, or to talk at a time that suits you.

With best regards,
Hannes Meilicke
[affiliation] [REF NEEDED]

---

# 5. Outcome codes

| outcome_id | role | label | icd10_codes | match_rule | diagnosis_position | notes |
|---|---|---|---|---|---|---|
| f12_any | primary | Mental and behavioural disorders due to use of cannabinoids | F12 (F12.0-F12.9) | code starts with F12 | any diagnosis | Matches protocol. Comparability with Addiction 2026 cannabis category: their full code list is in Supplementary Table S1 (not retrieved) [REF NEEDED] |
| f12_5 | key secondary | Cannabis-induced psychotic disorder | F12.5 | code starts with F125 | any diagnosis | 4-character code needed; HDC IPD reports use 4-character (IPD-F12.5 per hfocus 2026 letter) |
| f20_f29 | key secondary | Schizophrenia schizotypal and delusional disorders (psychosis overall) | F20-F29 | code starts with F20..F29 | principal diagnosis (primary) and any (sensitivity) | Principal-diagnosis rule chosen to avoid counting chronic patients admitted for other reasons |
| t40_7 | key secondary | Poisoning by cannabis (derivatives) | T40.7 | code starts with T407 | any diagnosis | Mostly unintentional edible exposures in children; low counts |
| f10_any | comparison | Mental and behavioural disorders due to use of alcohol | F10 (F10.0-F10.9) | code starts with F10 | any diagnosis | Should not respond to cannabis law |
| f15_any | comparison | Mental and behavioural disorders due to use of other stimulants incl. caffeine (methamphetamine) | F15 (F15.0-F15.9) | code starts with F15 | any diagnosis | Should not respond to cannabis law; note Addiction 2026 found a post-2022 rise in youth stimulant admissions (possible COVID rebound) |
| k35_k37 | negative control (added) | Acute appendicitis | K35-K37 | code starts with K35/K36/K37 | principal diagnosis | Added to mirror the Addiction 2026 negative control (deviation from protocol: addition only) |
| all_ip | coding check | All inpatient admissions | all codes | all records | n/a | Denominator for coding check |
| f_chapter | coding check | Chapter V mental and behavioural disorders | F00-F99 | code starts with F | principal diagnosis | F-chapter share = f_chapter / all_ip |

---

# 6. First-stage and context data (with sources)

Hand-entered from the cited sources (`raw_first_stage.csv`). The verification column shows how far each value was checked.

| table | date | geography | measure | value | unit | source_url | verification |
|---|---|---|---|---|---|---|---|
| shops | 2025-12-28 | Thailand | licensed cannabis establishments (cumulative) | 18433 | count | https://e.vnexpress.net/news/news/over-7-000-cannabis-shops-shut-as-tighter-laws-reshape-thailand-s-marijuana-market-5013599.html | search snippet (2 independent searches); page not opened |
| shops | 2025-12-31 | Thailand | licences expired in calendar 2025 | 8636 | count | https://thethaiger.com/news/national/thailand-cannabis-shop-closures-2025 | search snippet; page not opened |
| shops | 2025-12-31 | Thailand | licences renewed in calendar 2025 | 1339 | count | https://thethaiger.com/news/national/thailand-cannabis-shop-closures-2025 | search snippet; page not opened |
| shops | 2025-12-31 | Thailand | licences not renewed in calendar 2025 | 7297 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/02/01/over-7000-cannabis-shops-close-in-thailand-due-to-stricter-regulations-and-new-law | search snippet; page not opened |
| shops | 2025-12-31 | Thailand | establishments remaining after non-renewal | 11136 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/02/01/over-7000-cannabis-shops-close-in-thailand-due-to-stricter-regulations-and-new-law | search snippet; arithmetic 18433-7297=11136 checks |
| shops | 2026-04-22 | Thailand | establishments on DTAM shop map (cumulative) | 18517 | count | https://www.khaosodenglish.com/news/2026/04/22/thailand-maps-cannabis-shops-limits-use-to-medical/ | search snippet; page not opened |
| shops | 2026-04-22 | Thailand | closed after failing to renew | 7131 | count | https://thethaiger.com/news/national/thailand-launches-cannabis-shop-tracker | search snippet; page not opened |
| shops | 2026-04-22 | Thailand | establishments remaining | 11386 | count | https://thethaiger.com/news/national/thailand-launches-cannabis-shop-tracker | search snippet; page not opened |
| shops | 2026-11-07 | Thailand | licensed cannabis outlets | 12279 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/11/07/thailand-steps-up-cannabis-crackdown-repeat-offenders-face-licence-revocation | search snippet; page not opened; rise vs April unexplained |
| shops | 2026-11-07 | Bangkok | licensed cannabis outlets | 1726 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/11/07/thailand-steps-up-cannabis-crackdown-repeat-offenders-face-licence-revocation | search snippet; page not opened |
| shops | 2026-11-07 | Phuket | licensed cannabis outlets | 1046 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/11/07/thailand-steps-up-cannabis-crackdown-repeat-offenders-face-licence-revocation | search snippet; page not opened |
| shops | 2026-11-07 | Chon Buri | licensed cannabis outlets | 900 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/11/07/thailand-steps-up-cannabis-crackdown-repeat-offenders-face-licence-revocation | search snippet; page not opened |
| shops | 2026-11-07 | Surat Thani | licensed cannabis outlets | 717 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/11/07/thailand-steps-up-cannabis-crackdown-repeat-offenders-face-licence-revocation | search snippet; page not opened |
| shops | 2026-11-07 | Chiang Mai | licensed cannabis outlets | 482 | count | https://www.thestar.com.my/aseanplus/aseanplus-news/2026/11/07/thailand-steps-up-cannabis-crackdown-repeat-offenders-face-licence-revocation | search snippet; page not opened |
| survey | 2019-12-31 | Thailand age 18-65 | past-year cannabis use | 2.2 | percent | https://doi.org/10.1186/s12889-023-15883-6 | PubMed abstract read |
| survey | 2020-12-31 | Thailand age 18-65 | past-year cannabis use | 2.5 | percent | https://doi.org/10.1186/s12889-023-15883-6 | PubMed abstract read |
| survey | 2021-12-31 | Thailand age 18-65 | past-year cannabis use | 4.2 | percent | https://doi.org/10.1186/s12889-023-15883-6 | PubMed abstract read; Addiction 2026 cites the same 4.2% as '2022' |
| survey | 2023-05-31 | Thailand adults (n=2191) | current (past-12-month) cannabis use | 15 | percent | https://peerj.com/articles/17317/ | search snippet; different survey design - not comparable with CADS series |
| survey | 2024-12-31 | Thailand age 12-65 | past-year cannabis users (ONCB household survey) | 1500000 | persons | https://www.dailynews.co.th/news/4778457/ | search snippet; original report not found |
| hdc_context | 2019-10-01/2022-06-08 | Thailand | IPD T40.7 mean monthly admissions pre-2022 (range of period means) | 35 | admissions per month | https://www.hfocus.org/sites/default/files/files_upload/cm.thueng-rmw-kaychaesriikhrbsiipii_v2_june6-2026.pdf | PDF read; text says '30-40'; midpoint used |
| hdc_context | year 1 after 2022-06-09 | Thailand | IPD T40.7 mean monthly admissions | 115 | admissions per month | https://www.hfocus.org/sites/default/files/files_upload/cm.thueng-rmw-kaychaesriikhrbsiipii_v2_june6-2026.pdf | PDF read |
| hdc_context | year 3 after 2022-06-09 | Thailand | IPD T40.7 mean monthly admissions | 60 | admissions per month | https://www.hfocus.org/sites/default/files/files_upload/cm.thueng-rmw-kaychaesriikhrbsiipii_v2_june6-2026.pdf | PDF read |
| hdc_context | 2019-10-01/2022-06-08 | Thailand | IPD F12.2 mean monthly admissions pre-2022 | 130 | admissions per month | https://www.hfocus.org/sites/default/files/files_upload/cm.thueng-rmw-kaychaesriikhrbsiipii_v2_june6-2026.pdf | PDF read ('about 130') |
| hdc_context | year 3 after 2022-06-09 | Thailand | IPD F12.2 mean monthly admissions | 830 | admissions per month | https://www.hfocus.org/sites/default/files/files_upload/cm.thueng-rmw-kaychaesriikhrbsiipii_v2_june6-2026.pdf | PDF read ('more than 830') |
| hdc_context | 2019-10-01/2022-06-08 | Thailand | IPD F12.5 mean monthly admissions pre-2022 | 85 | admissions per month | https://www.hfocus.org/sites/default/files/files_upload/cm.thueng-rmw-kaychaesriikhrbsiipii_v2_june6-2026.pdf | PDF read |
| hdc_context | year 3 after 2022-06-09 | Thailand | IPD F12.5 mean monthly admissions | 556 | admissions per month | https://www.hfocus.org/sites/default/files/files_upload/cm.thueng-rmw-kaychaesriikhrbsiipii_v2_june6-2026.pdf | PDF read |
| hdc_context | 2016-10-01/2022-06-08 | Thailand age 10-19 | cannabis-related admissions (all cannabis codes) total | 1854 | admissions | https://doi.org/10.1111/add.70484 | full text read; 5.69 years -> ~27 per month |
| hdc_context | 2022-06-09/2023-09-30 | Thailand age 10-19 | cannabis-related admissions (all cannabis codes) total | 2343 | admissions | https://doi.org/10.1111/add.70484 | full text read; 68 weeks -> ~150 per month |

---

# 7. Decision log


- 2026-11-14T00:57:30Z Started run in cloud session (not Mac). Folder created inside repo working dir `19 Thailand Cannabis/` on branch claude/new-session-qbw1zs. House style hannes-04-analysis loaded.
- 2026-11-14T00:57:30Z R not installed in container; attempting apt install of r-base + packages (background).
- 2026-11-14T01:02:10Z R 4.x installed via apt (r-cran-fixest unavailable → use MASS::glm.nb / glm + sandwich/lmtest instead of fixest).
- 2026-11-14T01:02:10Z Novelty: PubMed (eutils, 2 queries, 111 unique PMIDs), Europe PMC (3 queries incl. preprints), Thai-language ThaiJO web search, English web search. No study of the June 2025 re-regulation × admissions/psychosis/poisoning found. Closest: Puetpaiboon et al., Addiction 2026 (doi:10.1111/add.70484, PMC13578852; "on" phase only, to Sep 2023).
- 2026-11-14T01:02:10Z Cloud network was limited; all .go.th hosts refused (403). Requested and got approval to add 19 exact hosts (HDC, data.go.th, NHSO, DMH, Royal Gazette, DTAM, Thai FDA catalog, hfocus, crossref, springer, cads). Did not switch to unrestricted.
- 2026-11-14T01:02:10Z Addiction study data source = THIP (Thai Health Information Portal), PSU custodian, ethics approval required → not public.
- 2026-11-14T01:05:16Z Portal probes after allowlist: hdcservice.moph.go.th and ucinfo.nhso.go.th → TCP "connection reset by peer" (×2 each; consistent with geo-blocking of non-Thai IPs). data.go.th, opendata.moph.go.th, ratchakitcha.soc.go.th → Cloudflare 403 / JS challenge (×2). catalog.fda.moph.go.th: homepage 200 but CKAN API reset. dmh.go.th: 200 (homepage only). hfocus.org: 200.
- 2026-11-14T01:05:16Z Tried headless Chromium to pass Cloudflare challenge; action denied by session permission policy. Not retried; respected. Logged as access failure.
- 2026-11-14T01:05:16Z Region 8 cannabis dashboard URL (cloud1-r8way.moph.go.th/r8eoc/dashboard-ganja-r8.html) now serves an unrelated app (IAAI ageing platform); no cannabis data endpoint found. Fallback failed.
- 2026-11-14T01:05:16Z hfocus.org PDF (open letter, 9 Jun 2026, anti-drug network) downloaded: cites HDC national monthly IPD counts for T40.7, F12.2, F12.5, Oct 2019 to ~mid-2025, reported only as period averages in chart labels. Advocacy source; used only as context/power inputs, flagged as such. No chart digitising (would create unverified numbers).
- 2026-11-14T01:05:16Z GATE DECISION: data-access gate FAILED (no accessible monthly × province × ICD-10 admissions after June 2025; THIP requires ethics approval; HDC geo-blocked from cloud). Per protocol: analysis stopped. Producing 00_novelty.md, 00_data_access.md, access plan, draft_email.md (NOT sent), first-stage table, outcome_codes.csv, approximate power analysis, analysis.Rmd scaffold (not run on real data), SUMMARY.md.
- 2026-11-14T01:05:16Z Legal dates: Royal Gazette pages unreachable (Cloudflare). Best fallback = Thai and international news + law-firm notes (URLs in 00_legal_timeline in 00_novelty.md). Gazette volume/page numbers = [REF NEEDED].
- 2026-11-14T01:09:08Z Wrote outcome_codes.csv before any analysis (F12 any; F12.5; F20-F29 principal dx; T40.7; F10; F15; plus K35-K37 negative control added to mirror Addiction 2026; all_ip and F-chapter for coding check). Addiction 2026 Supplementary Table S1 code list not retrieved → comparability [REF NEEDED].
- 2026-11-14T01:09:08Z Breakpoint coding: Jun 2022 = first "on" month (9 Jun, 22/30 days exposed); Jul 2025 = first "off" month (effective 26 Jun 2025, only 5 June days exposed). Anticipation breakpoints: May 2024 (PM relisting announcement, 8 May 2024) and May 2025 (DTAM consultation from 22 May 2025).
- 2026-11-14T01:09:08Z Models: NB GLM with population offset, month-of-year FE, COVID indicator Mar 2020-Dec 2021, Newey-West SE (lag 3). fixest unavailable → DiD/dose models use glm.nb with FE dummies and cluster-robust SE (sandwich::vcovCL).
- 2026-11-14T01:09:08Z Power: approximate simulation (Poisson GLM + Newey-West, 300 reps, NB data-generating process, theta 25/100, 12 or 16 post months). Inputs = period means from HDC (advocacy letter) and Addiction 2026; trend (+8%/yr pre, from Addiction cannabis model), 5% seasonal amplitude, and 2022 jump size (2x for F12.2/F12.5) are ASSUMPTIONS. F20-F29, F10, F15 not simulated: no baseline counts found [REF NEEDED]. Pre-specified label: "powered" if 80%-power MDE <= 20% level drop.
- 2026-11-14T01:09:08Z Deviation from house style: one helper function + replicate() for the power simulation, and a rowwise loop for leave-one-province-out (77 refits). All substantive models written out explicitly. Figures saved from analysis.Rmd rather than a separate figures_tables.Rmd (most blocks cannot run yet).
- 2026-11-14T01:09:08Z Smoke test of H1-H3 + checks on a SIMULATED panel (scratchpad only, not in project): all chunks ran; symmetry level ratio recovered (-0.98, 95% CI -1.11 to -0.86 vs truth -1). Slope ratio unstable when 2022 slope ~0 → level ratio pre-specified as primary symmetry metric, slope ratio secondary/descriptive.
- 2026-11-14T01:11:19Z First power run (Poisson + Newey-West lag 3): empirical type I error at true effect 0 = 0.06-0.25 (anti-conservative with 12-16 post months). DECISION: primary inference switched to model-based SE (glm.nb in H blocks; quasi-Poisson in power sim); Newey-West kept as sensitivity in H1.3 plus residual ACF check. Power re-run.
- 2026-11-14T01:13:14Z Second power run (quasi-Poisson): size still ~0.17 for F12.2/F12.5 (variance not proportional to mean when counts rise ~6-fold). DECISION: power sim now fits glm.nb, the same model as H1 primary; nsim 200 per cell. Re-run.
- 2026-11-14T01:18:01Z Third power run: size ~0.05 at theta 25, but 0.10-0.18 at theta 100. Cause = simulation artefact (DGP 2022 slope stopped at Jun 2025, one month before the model's Jul 2025 breakpoint → spurious ~3% level shift). Fixed DGP (slope runs to the breakpoint). Re-run; previous runs superseded.
- 2026-11-14T01:23:23Z Final power run done (glm.nb, fixed DGP): type I error 0.020-0.085; 40% drop power 0.93-1.00 in all scenarios. SUMMARY.md written (hannes-code-summary format + FLAG + scorecard + one-sentence answer). draft_email.md NOT sent. Run complete.

---

# 8. File index

| File | What it is |
|---|---|
| `HANDOVER.md` | This file |
| `SUMMARY.md` | Audit, Methods/Results, recap, scorecard |
| `00_novelty.md` | Literature search and policy timeline |
| `00_data_access.md` | Source-by-source access audit and access plan |
| `draft_email.md` | Collaboration email to the THIP/PSU authors (not sent) |
| `DECISIONS.md` | Timestamped decision log |
| `outcome_codes.csv` | ICD-10 outcome definitions |
| `raw_first_stage.csv` | Sourced shop, survey and context values |
| `analysis.Rmd` / `analysis.html` | Full analysis. First stage and power run now; H1–H3 run once data arrive |
| `clean_data.xlsx` | Sheets: admissions_panel (empty), shop_panel, survey_prevalence, hdc_context, codes |
| `results.rds` | Status, first stage, power grid, MDE table |
| `figures/first_stage_shops.png` | Licensed establishments, Dec 2025 – Nov 2026 |
| `figures/first_stage_survey.png` | CADS past-year use, 2019–2021 |
| `figures/power_mde.png` | Power curves for the 2025 level drop |
| `raw_downloads/hfocus/hfocus_june6_2026.pdf` | Open letter (9 Jun 2026) citing HDC monthly IPD counts |
| `raw_downloads/r8_dashboard/` | Region 8 dashboard snapshot (now an unrelated app) |
