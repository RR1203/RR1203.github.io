**FLAG:** Power gate failed (MDE 25.2% > 20%), so per protocol the effect estimates below are exploratory and not evidence. Washington first stage (arrests) was not obtained. NFLIS fentanyl-share sensitivity was not run (site unreachable). `augsynth` could not be installed, so ridge-augmented SCM was implemented by hand.

### 1. What the code did

1. Downloaded CDC VSRR provisional overdose deaths (`xkb8-kh2a`, 88,182 rows). Kept total and synthetic-opioid (T40.4) 12-month-ending predicted counts for 50 states + DC → `vsrr` (7,038 rows, latest month June 2026).
2. Cut the window to Jan 2015–Dec 2025, because every state's 2026 rows are flagged "Underreported" → `vsrr`.
3. Joined Census July-1 populations (Vintage 2020 for 2015–19, Vintage 2025 for 2020–25; 0 missing) and computed rates per 100k → `df_clean` (6,732 rows × 13 columns, 51 units) → `clean_data.xlsx`.
4. Marked donor exclusions: OR, WA, CA, CO, NV. Flagged T40.4 completeness: 30 complete donors for 2019–2025, 15 for 2015–2022.
5. Extracted Oregon PCS-only arrests (CJC/LEDS, quarterly 2018Q1–2025Q4, n = 32 quarters) from the CJC HB 4002 equity report → `or_arrests_cjc`. FBI CDE arrests: all codes tried returned zeros or the rate limit → no usable FBI data.
6. G1 first stage: mean Oregon PCS-only arrests per quarter by period → `g1_cjc_summary`.
7. G2 power: ASCM in-space placebos (31 states incl. OR) at 4 fake start dates (Sept 2021, Jan 2022, Sept 2022, Jan 2023), estimand = event months 11–15 → `g2_mde`, plus a total-only sensitivity and a WA-design sensitivity.
8. H1 Oregon ASCM: start Sept 2024, pre-period Jan 2019–Aug 2024, matched on total + T40.4 trajectories, 30 donors → `h1_fit`, `h1_effect`, 30 placebos → `h1_p_pct`.
9. H1 robustness: in-time placebos (Sept 2022, Jan 2023); total-only matching with 46 donors; Western donors (8 states); leave-one-donor-out (AK, OK); T40.4 deaths as the outcome; TWFE DiD on log rate vs Western donors (`h1_did`).
10. H2 Washington ASCM: start July 2023, same setup → `h2_fit`, aligned effect (event 11–15) and all fully-post windows (event 11–29), 30 placebos. Robustness as in H1 (in-time placebo Jan 2022; total-only; West; LOO for AK, ME, OK; DiD).
11. H3 stacked: mean of the OR and WA % effects; placebo = each donor's mean across both designs → `h3_effect`, `h3_p`.
12. S1 decriminalization replication: start Feb 2021, pre-period 2015–Jan 2021, windows Jan–Dec 2022, OR and WA, each with total+T40.4 (15 donors) and total-only (46 donors) matching → `s1_*`, `s1_excess_2022`.
13. Figures 1–4 → `figures/`; all objects → `results.rds`.

**Unverified:** donor exclusions rely on legal changes not checked against a 50-state review [REF NEEDED]; the two 2026 working papers that touch recriminalization (Pourtaheri; Jones et al.) were not read in full.
**Not run:** NFLIS fentanyl-share sensitivity; Washington first stage; FBI arrests for either state.

### 2. Methods and Results

**Methods.** We used CDC VSRR provisional 12-month-ending drug overdose death counts (predicted values) for 50 states and DC, January 2015 to December 2025, divided by Census population. The policy dates were 1 September 2024 for Oregon (HB 4002) and 1 July 2023 for Washington (SB 5536). Because the outcome is a 12-month rolling sum, the primary estimand was the mean gap over event months 11–15, the first five windows made up entirely of post-policy months. We expressed this gap as a percent of the synthetic control. We estimated ridge-augmented synthetic control weights (simplex-constrained SCM plus a ridge bias correction, with λ chosen on the last 12 pre-period months). Matching used the 2019–pre-policy trajectories of total and synthetic-opioid (T40.4) death rates, each scaled by its SD. The donor pool was the 30 states with complete T40.4 data, excluding OR, WA, CA, CO and NV. We drew inference from in-space permutation (two-sided rank of |% gap|). We estimated power from in-space placebos at four fake pre-period start dates, defining the minimum detectable effect (MDE) as the 95th percentile of |placebo % gap|. The pre-set stop rule was MDE > 20%. Oregon PCS-only arrests came from the Oregon Criminal Justice Commission (LEDS). Analyses used R 4.3.3 with osqp and fixest.

**Results.** *First stage (Oregon):* PCS-only arrests averaged 1,044 per quarter before M110 (2018–2020) and 144 under M110 (2021Q2–2024Q2). Under HB 4002 (2024Q4–2025Q4) they averaged 676, which is 4.7 times the M110 level and 0.65 times the pre-M110 level. *Power:* the MDE was 25.2% (gate failed). It was 28.0% with total-only matching and 20.7% in the Washington design. *Exploratory estimates:* in Oregon (pre-RMSPE 0.63 per 100k; ASCM weights OK 0.71, AK 0.34), the gap over event months 11–15 was +1.21 per 100k (+4.1%, permutation p = 0.81, RMSPE-ratio p = 0.45, 30 placebos). In the calendar-2025 window it was −2.70 per 100k (−8.6%, about −115 deaths). The robustness checks did not agree with each other. In-time placebos at Sept 2022 and Jan 2023 gave +26.2% and +26.7%. The other specifications gave: total-only +2.9% (p = 0.91); Western donors −14.9%; leave-one-out +7.7% (no AK) and +8.7% (no OK); synthetic-opioid deaths as the outcome −4.2%. The DiD against Western donors gave +18.5% (log coefficient 0.170, 95% CI −0.005 to 0.344, p = 0.055). In Washington, the gap over event months 11–15 was +3.8% (p = 0.77) and over all fully-post windows +16.0% (p = 0.16). Calendar 2024 was +15.1% (about +418 deaths) and 2025 +18.8% (about +469). The robustness checks were: in-time placebo (Jan 2022) +18.1%; total-only +8.9%; Western donors −12.5%; leave-one-out +39.5% (no AK), +2.8% (no ME) and +4.7% (no OK); DiD +48.2% (log 0.393, 95% CI 0.205 to 0.581, p = 0.001). The stacked OR + WA estimate was +3.9% (p = 0.55). *Decriminalization replication (Feb 2021, windows Jan–Dec 2022):* matched on total + T40.4 with 15 donors, Oregon was +10.6% (p = 0.50) and Washington +5.3% (p = 0.69). Matched on total only with 46 donors, Oregon was +27.2% (p = 0.11) and Washington +3.1%. The implied calendar-2022 excess deaths were 218 for Oregon (403 total-only) and 374 for Washington (334 total-only). The first-year monthly-rate gaps were 0.21 per 100k for Oregon and 0.02 for Washington, against 0.268 and 0.112 in Joshi et al. These estimates fall inside the published range: a fentanyl-adjusted null (Zoorob et al.; Joshi et al.) at one end and sizeable increases (Hall, Hansen & Matsuzawa) at the other. As in that literature, the estimate shrinks when matching accounts for fentanyl.

### 3. Recap

- Built monthly 12-month-ending overdose panels (2015–2025) and an Oregon arrest first stage. Ran augmented SCM with permutation inference for OR and WA recriminalization, plus a decriminalization replication.
- Oregon arrests rose 4.7× after HB 4002, so the policy was enforced. But the design can only detect effects above about 25%, so the power gate failed. Exploratory estimates show no detectable effect (OR +4%, p = 0.81; WA +4%, p = 0.77), and the robustness checks swing by ±15–27 points.
- Decision: drop the project, or wait for 2026 final data (a longer post-period), a registered FBI API key (for the WA first stage) and NFLIS access, then re-run the power gate.

### Scorecard (0–10, based on what the data showed)

| Dimension | Score | Why |
|---|---|---|
| Novelty | 7 | No published estimate of the recriminalization effect found; two 2026 working papers touch it and were not read in full |
| First stage | 6 | OR: arrests 4.7× the M110 level (but 35% below pre-M110); WA: not obtained |
| Power | 2 | MDE 25% (gate failed); in-time placebos +26% |
| Big result | 1 | No detectable effect; estimates are sign-unstable across specifications |
| Rigor | 4 | Placebos, LOO, in-time, DiD and replication all run; but hand-coded ASCM, 2–3 donors carry the weight, λ at grid edge, 12-month smoothing, donor-law review incomplete |
| Feasibility | 5 | Outcome data are public and current to Dec 2025; arrests (WA/FBI) and NFLIS blocked in this environment |
