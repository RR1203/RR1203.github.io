# 00 Data access (main gate)

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
