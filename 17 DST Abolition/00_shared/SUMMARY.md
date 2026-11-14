**FLAG:** Brazil arm STOPPED (DATASUS FTP unreachable from the cloud; see `BR/BRAZIL_TODO.md`), so no MX+BR pooling or replication test was possible. Hospital-admission outcomes NOT ANALYSED (DGIS server has a self-signed TLS certificate; see `MX/HOSPITAL_TODO.md`). Positive-control gate FAILED for Q1: no pre-abolition spring-forward spike in AMI (IRR 0.985) and only a non-significant one in road deaths (IRR 1.043). The A-vs-B comparisons fail the neoplasm negative control. CONAPO population was blocked, so 2020 Census population is held fixed.

### 1. What the code did

(`MX/analysis.Rmd`, knitted to `MX/analysis.html`; all decisions are timestamped in `DECISIONS.md`)

1. Novelty search: PubMed, Europe PMC, OpenAlex, NBER, RePEc and web, in EN/ES/PT → `00_shared/00_novelty.md`. Q1 not studied in either country. Q2 partly studied: Watanabe 2026, a Zenodo preprint, crash timing only. Gate passed for both arms.
2. Read 2020 Census localities (ITER, 195,662 rows) → population-weighted centroids and population for 2,469 municipalities (0 missing coordinates) → `mun_df`.
3. Coded clock regimes from the law texts in `MX/raw/law/` (Ley de los Husos Horarios, DOF 28-10-2022 and 29-11-2022; the abrogated Ley del Sistema de Horario and Decreto de Horario Estacional). Groups:
   - A, abolished: 2,291 municipalities, 111.3 M people
   - A2, Chihuahua non-border, moved to permanent UTC-6: 59, 2.16 M
   - B, kept US-aligned DST: 33, 7.72 M
   - C, never DST (Sonora, plus Quintana Roo from 2016): 83, 4.80 M
   - Ambiguous (Ojinaga, Coyame del Sotol, Manuel Benavides): 3, excluded

   Municipalities whose centroid is within 50 km of a centroid in another group were flagged "near": 8 in A, 5 in B, 3 in A2, 2 in C.
4. Built a calendar: national DST rule (1st Sun Apr – last Sun Oct), US rule (2nd Sun Mar – 1st Sun Nov), holidays, Holy Week, Easter (computed) → `cal_df`. This gave 52 transition events for 2012–2024 → `events_df`. Events within the COVID window (Mar 2020 – Dec 2021) are flagged.
5. Read the INEGI EDR registration files for 2012–2024 (10,050,739 records). Dropped 10,866 with no valid date of death, then restricted to deaths occurring 2012–2024 (10,014,079 left). Kept the five study outcomes by ICD-10 underlying cause (3,277,558 deaths). San Felipe (02007) was mapped to Mexicali → `deaths_df`.
   - 56,759 deaths have no residence municipality and 535 have a code not in the 2020 Census; 57,054 deaths in total could not be assigned a residence group.
6. Aggregated counts:
   - daily counts by state × group × date, residence- and occurrence-based (208,956 rows) → `daily_counts`
   - municipality-month counts (385,164 rows) → `muni_month`
   - residence totals: AMI 1,388,669; neoplasm 1,183,588; homicide 354,190; road 202,365; suicide 91,692
7. Sun-clock exposure (suncalc): sunrise, sunset and solar noon for each municipality and day from Nov 2021 to Dec 2024, under the actual and counterfactual (old-rule) clock. Doses are the change in morning light before 07:00, evening light after 19:00, and the clock shift → `sun_dose_month`. Wrote `MX/clean_data.xlsx` (8 sheets).
8. Step 0 figures → `figures/fig1`–`fig3`: regime map, dose map, and first stage for 10 example cities.
   - The clock moved −60 min in A in Apr–Oct and +60 min in A2 in Nov–Mar. B and C did not change.
9. Power: placebo SEs from pre-2020 data; MDE = exp(2.80·SE) − 1; "powered" means MDE ≤ 10% → `s0_power_table`.
10. Q1 (spring and fall): days 0–7 after each transition vs days −21 to −8 and +14 to +27, at group-day level; Poisson with event × group and day-of-week FE, holiday controls, SE clustered by event. A2 was pooled into A, since its switching also stopped. Models:
    - pre-period excess (positive-control check)
    - excess by group and period
    - DiD A vs B (main), DiD A vs C (placebo group)
    - within-A pre vs post change
    - phantom dates only
    - fall DiD
11. Q1 robustness: occurrence-based counts; excluding boundary municipalities; ambiguous municipalities counted in B; including COVID events; placebo abolition in Oct 2020; negative binomial; leave-one-state-out (29 fits).
12. Q2: municipality-month Poisson triple difference (Apr–Oct × post Nov 2022 × A). FE: municipality, month × group, year. Population offset; SE clustered by state; COVID months excluded. Fitted vs C (main), vs B, and vs B+C. Also: dose-response on morning and evening light, and an event study by year (ref 2019).
13. Q2 robustness: occurrence-based counts; excluding boundary municipalities; Sonora only as control; including COVID; follow-up to 2023 only; placebo abolition in Oct 2020; leave-one-state-out (28 fits).
14. Results → `MX/results.rds`, `MX/results_tables.xlsx`, `figures/fig4`–`fig6`: Q1 event plot, Q2 event study, and the forest plot (Brazil and pooled rows empty).

**Not run:** Brazil arm; all admission outcomes (self-harm, F00–F99, F30–F39); MX+BR pooling.

**Unverified:**
- Pre-2022 border DST applied to a 20-km strip, not whole municipalities; whole municipalities were assigned.
- Deaths from 2024 registered in 2025 are missing.
- Clustering by state leaves the A-vs-C contrast resting on 2 control states.

### 2. Methods and Results

**Methods.** We used Mexico's 30 Oct 2022 abolition of daylight saving time (DST) as a natural experiment. Municipal clock regimes were coded from the Ley de los Husos Horarios (DOF 28-10-2022, reformed 29-11-2022) and the abrogated 2001 law and 2002 seasonal-time decree. Groups:
- A: abolished DST (2,291 municipalities)
- B: kept US-aligned DST (33 border municipalities and all of Baja California)
- C: never DST (Sonora, and Quintana Roo from 2016)
- A2: Chihuahua outside the border strip, which moved to permanent UTC-6 and was analysed separately
- Excluded as ambiguous: Ojinaga, Coyame del Sotol and Manuel Benavides

Deaths came from INEGI death registrations (EDR) 2012–2024, assigned to the municipality of residence by date of death. Outcomes were defined by ICD-10 underlying cause: suicide (X60–X84), acute myocardial infarction (AMI; I21–I22), transport deaths (V01–V89), homicide (X85–Y09) and neoplasms (C00–D48, negative control). Hospital admissions could not be obtained.

- **Q1 (transition effect):** we compared deaths in days 0–7 after each clock change with the same weekdays 2–3 weeks before and after. We used Poisson models with event-by-group and day-of-week fixed effects, holiday and Holy Week indicators, and SEs clustered by event. Group A after abolition was assessed on "phantom" dates (2023–2024).
- **Q2 (chronic clock effect):** we fitted a triple difference on municipality-months: former-DST months (Apr–Oct) × post-abolition × group A. The models had municipality, month-of-year × group and year fixed effects, a log 2020-population offset, and SEs clustered by state.
- **Dose:** the change in daily minutes of clock-time light before 07:00 and after 19:00, from suncalc at population-weighted centroids.
- **Shared rules:** both questions excluded Mar 2020–Dec 2021. Minimum detectable effects (80% power, α = 0.05) came from placebo SEs in pre-abolition data. Software: R 4.3.3, fixest 0.14.2, suncalc.

**Results.**
- **Q1 positive-control gate failed.** Before abolition, the spring-forward week in A+B (648 group-days) showed:

  | Outcome | IRR | 95% CI | p |
  |---|---|---|---|
  | AMI | 0.985 | 0.956–1.014 | 0.30 |
  | Road deaths | 1.043 | 0.992–1.098 | 0.10 |
  | Suicide | 1.071 | 0.996–1.153 | 0.065 |
  | Homicide | 1.031 | 1.006–1.057 | 0.015 |
  | Neoplasm | 0.998 | 0.983–1.014 | 0.83 |

  No outcome showed a fall-back excess (all p ≥ 0.11).
- **Q1 main DiD (A vs B, 792 group-days) did not separate signal from noise.** Suicide: IRR 0.965 (0.650–1.433, p = 0.86). AMI: 0.947 (0.831–1.080, p = 0.42). But the neoplasm negative control was significant (1.162, 1.074–1.258, p < 0.001), as were road deaths (1.326) and homicide (1.439). The placebo for an Oct 2020 abolition was also significant for suicide (1.752) and neoplasm (1.260). The design is not valid, and MDEs were 13–59% (all underpowered).
- **Q1 placebo-group DiD (A vs C):** nothing was significant (suicide 0.694, 0.287–1.678).
- **Q1 within group A:**
  - The spring-week suicide excess fell after abolition: IRR 0.831 (0.713–0.969, p = 0.018). The pre-period placebo was null (1.011, 0.869–1.176), but this test's MDE was 24% (underpowered).
  - AMI did not change (1.032, 0.991–1.075), but its within-A placebo was itself significant (1.102, p < 0.001).
  - On phantom dates, no outcome spiked except neoplasm (1.037, 1.005–1.069).
- **Q2 main triple difference (A vs C, about 277,000–318,000 municipality-months per outcome):**

  | Outcome | IRR | 95% CI | p | Power |
  |---|---|---|---|---|
  | Suicide | 1.074 | 0.939–1.229 | 0.30 | underpowered, MDE 21% |
  | AMI | 1.163 | 1.013–1.336 | 0.033 | powered |
  | Road deaths | 0.985 | 0.586–1.657 | 0.96 | underpowered, MDE 15% |
  | Homicide | 0.879 | 0.746–1.036 | 0.12 | underpowered, MDE 35% |
  | Neoplasm | 1.018 | 0.907–1.142 | 0.76 | powered |
- **The AMI estimate did not hold up:**
  - vs B: 1.033 (0.897–1.190)
  - vs B+C: 1.066 (0.956–1.188)
  - with follow-up ending in 2023: 1.154 (0.962–1.385)
  - The event study showed significant pre-2019 coefficients for AMI, suicide and road deaths.
  - It held under occurrence-based counts (1.157), excluding boundary municipalities (1.168), and in 27 of 28 leave-one-state-out fits.
- **Q2 vs B failed the negative control:** neoplasm 0.932 (0.895–0.972).
- **Dose-response models also failed the neoplasm control:** per +1 h of morning light, neoplasm 1.022 (p = 0.023); per +1 h of evening light, 0.974 (p < 0.001). They gave suicide 1.089 (1.006–1.179) per +1 h morning light and 0.922 (0.870–0.977) per +1 h evening light. Because the negative control failed, these are not interpretable as causal.
- **Q2 placebo (Oct 2020):** significant for road deaths (0.784) and homicide (1.164). Including the COVID months did not change the direction of any estimate.

### 3. Recap

- Built a municipality-level clock-regime map and sun-clock dose for Mexico from the law texts. Tested Q1 and Q2 on 3.28 M deaths from 2012–2024; Brazil and hospital admissions were not run.
- No robust effect of abolishing DST on any outcome. The transition design failed its positive control, A-vs-B comparisons failed the negative control, and the only signals (Q1 within-A suicide −17%; Q2 AMI +16% vs C) are fragile.
- Decide whether to run Brazil and DGIS admissions on the Mac (scripts ready). Q2 needs a better control group than 2 states before any claim.

---

#### Scorecard (0–10, based on what the data showed)

| Arm | Novelty | First stage | Power | Big result | Rigor | Feasibility |
|---|---|---|---|---|---|---|
| Mexico | 8 | 9 | 3 | 1 | 6 | 7 |
| Brazil | 8 | n/a (not run) | n/a | n/a | n/a | 4 (FTP blocked in cloud; Mac needed) |

- **Mexico, first stage (9):** the clock shift is mechanical and verified from the law.
- **Mexico, power (3):** only the AMI and neoplasm Q2 tests and the single-group Q1 tests were powered.
- **Mexico, big result (1):** no robust effect.
- **Mexico, rigor (6):** many checks ran, but the control groups are small.

#### What this means for the photoperiod study

Mexico shifted the clock by 60 minutes against the sun for about 111 M people without changing the amount of daylight. Two years later this left no detectable, robust change in suicide, homicide, road deaths or AMI deaths. So clock–sun misalignment of this size is unlikely to drive large population-level mortality effects (≥ 15–35% for the rarer outcomes; ≥ 9% for AMI). Effects of photoperiod itself, meaning daylight amount, are therefore not obviously confounded by clock policy. One limit: the dose varied almost only by group, not by longitude, so this run cannot separate sun-clock misalignment from other differences between A and the 2-state controls. Brazil's larger North/South split and the admission data would be the better test.
