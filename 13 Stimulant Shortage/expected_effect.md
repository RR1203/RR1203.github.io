# Expected effect (pre-specified)

Written: 2026-11-13 22:29:13 UTC, before any model used FARS data from 2022Q4 onward.
Inputs come from downloaded ARCOS (exposure), Census (population) and pre-shortage FARS (power only). Chang et al. 38-58% is from the task brief.

## Inputs

- Baseline amphetamine-class supply (amphetamine + lisdexamfetamine), 2022Q1-Q3: 46.3 DDD per 1,000 residents aged 18-44 per day.
- Implied share of 18-44-year-olds on amphetamine-class stimulants on a given day: upper bound 4.63% (all supply to ages 18-44, 1 DDD per user-day); half-of-supply scenario 2.32% (assumption, not data).
- National supply shortfall vs 2017-2022Q3 trend, 2022Q4-2023Q4: 3.9%.
- Crash reduction while on stimulants (Chang et al.): 38-58%.

## Expected national effect on young-driver fatal crash rate

- Prompt formula (share x drop x reduction): 0.034% to 0.105%.
- Alternative (risk increase when off treatment = 1/(1-r)-1, i.e. 61-138%): 0.056% to 0.251%.
- In expected excess crashes per quarter (baseline 6297 crashes with a driver 18-44 per quarter, 2022Q1-Q3): 2.2 to 15.8.

## Expected dose-response effect (per 10 percentage-point state shortfall)

- 0.088% to 0.269% increase in young-driver fatal crashes.

## Power (from pre-shortage data only)

Minimum detectable effect (80% power, 5% two-sided) = exp(2.8 x SE) - 1, with SE from the same model fitted to 2017Q1-2022Q3 with a placebo post period 2021Q4-2022Q3.

- State dose-response (per 10 pp shortfall): MDE = 10.0%.
- National young (18-44) vs older (55-74) comparison: MDE = 4.1%.

## Conclusion before looking at results

The expected effect (at most 0.25% nationally, 0.27% per 10 pp) is 16-fold smaller than the national MDE and 37-fold smaller than the dose-response MDE. The design cannot detect the effect that the Swedish within-person estimates imply. A significant crash increase would therefore be larger than the plausible pharmacological effect and should be treated with suspicion; a null result is the expected outcome and only rules out effects larger than the MDE.
