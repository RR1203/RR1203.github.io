# Expected effect and power (written before any outcome model)

**Timestamp:** 2026-11-13 16:00:03 UTC. At this point only supply data (ARCOS), population (Census) and pre-2020 FARS counts had been used. No post-2019 crash model had been run.

Source: `analysis.Rmd`, blocks F (feasibility) and E (expected effect and power). All inputs are from downloaded files except the 38–58% crash reduction (Chang et al., given in the task brief).

## Inputs
| Input | Value | Source |
|---|---|---|
| Share of residents 18–44 on an amphetamine-class stimulant on a given day (upper bound; all doses assigned to ages 18–44) | 5.66% | ARCOS 2021Q4–2022Q3, label-based daily doses / Census pop 18–44 |
| Supply shortfall vs own trend, 2022Q4–2024Q4 (population weighted) | 3.22% | ARCOS vs 2017Q1–2022Q3 state trends |
| Supply shortfall, acute phase 2022Q4–2023Q4 | 5.65% | same |
| Crash-risk reduction when on stimulants | 38–58% | Chang 2014/2017 (brief) |
| Baseline young-driver (18–44) fatal crashes per quarter, 2017–2019 | 5,418 (5,968 deaths) | FARS |

## Expected effect on young-driver fatal crashes
Formula from the brief: share × drop × crash reduction.

| Window | Chang | Expected % rise (brief formula) | Expected % rise (risk-ratio form, 1/(1−r)−1) |
|---|---|---|---|
| 2022Q4–2024Q4 | 38% | 0.07% | 0.11% |
| 2022Q4–2024Q4 | 58% | 0.11% | 0.25% |
| 2022Q4–2023Q4 | 38% | 0.12% | 0.20% |
| 2022Q4–2023Q4 | 58% | 0.19% | 0.44% |

So the expected rise is **about 0.1–0.4%**, i.e. roughly **4–24 extra fatal crashes per quarter nationally** (5,418 × 0.07–0.44%). Even taking the brief's 12% adult fill drop instead of the ARCOS gap: 5.66% × 12% × 58% = 0.39%.

## Minimum detectable effect (80% power, α = 0.05, MDE = 2.80 × SE)
SEs from placebo models fitted on 2017–2019 data only (fake post = 2018Q3), state-clustered, Poisson with population offset.

| Design | MDE |
|---|---|
| Dose-response, per 1.0 (100 pp) shortfall | +45% |
| Dose-response, 87.5th vs 12.5th percentile state (12.2 pp apart) | +4.7% |
| Age DiD, 18–44 vs 55–74 (national shock) | +3.6% |

## Verdict before looking at results
The expected effect (0.1–0.4%) is **10–50 times smaller** than the smallest effect these designs can detect (3.6–4.7%). The study cannot confirm the expected harm. A null result would rule out only large effects (several percent), not the size the Chang estimates imply. Any large significant effect would be implausible given the supply drop and should be treated as confounding until proven otherwise.

Also noted before results: the pre-period placebo age DiD was itself significant (−2.7%, p = 0.03), so young vs older crash trends were already diverging before the shortage.
