# Pre-specified expected effect + power. Uses ARCOS (exposure) and ONLY pre-shortage FARS data (2017Q1-2022Q3).
suppressMessages({library(tidyverse); library(fixest)})
load("/tmp/claude-0/clean.RData")
nat <- arcos %>% group_by(t, q, days) %>%
  summarise(ddd = sum(ddd_amph), p = sum(p18_44), .groups = "drop") %>% mutate(rate = ddd / (p / 1000) / days)
fit <- lm(rate ~ t + factor(q), data = filter(nat, t < T_SHORT))
base_rate <- mean(nat$rate[nat$t %in% qid(2022, 1:3)])               # DDD/1000 residents 18-44/day
nat_gap <- nat %>% filter(t %in% W_MAIN) %>% mutate(e = predict(fit, .)) %>% summarise(g = mean((e - rate) / e)) %>% pull(g)
share_upper <- base_rate / 1000                                        # all supply to 18-44, 1 DDD = 1 person-day
share_half  <- share_upper / 2                                         # assumption: half of supply to 18-44
red <- c(0.38, 0.58)                                                   # Chang et al. crash reduction on stimulants
exp_formula <- outer(c(share_upper, share_half) * nat_gap, red)        # prompt formula: share x drop x reduction
exp_rr      <- outer(c(share_upper, share_half) * nat_gap, 1 / (1 - red) - 1)  # risk increase when off treatment
per10_formula <- outer(c(share_upper, share_half) * 0.10, red)          # per 10 pp state shortfall

pre <- filter(young_panel, t < T_SHORT) %>% mutate(fake = as.integer(t >= qid(2021, 4)))
m_dose <- fepois(crashes ~ I10:fake + log_vmt + unemp + cannabis_legal | fips + t, offset = ~log(pop), data = pre, cluster = ~fips)
pre3 <- filter(panel, t < T_SHORT, group %in% c("18-44", "55-74")) %>% mutate(fake = as.integer(t >= qid(2021, 4)))
m_nat <- fepois(crashes ~ young:fake | state_group + t, offset = ~log(pop), data = filter(pre3, covid == 0 | t >= qid(2021,4)), cluster = ~fips)
se_dose <- se(m_dose)["I10:fake"]; se_nat <- se(m_nat)["young:fake"]
mde_dose <- exp(2.8 * se_dose) - 1; mde_nat <- exp(2.8 * se_nat) - 1
base_q <- mean(filter(young_panel, t %in% qid(2022, 1:3)) %>% group_by(t) %>% summarise(n = sum(crashes)) %>% pull(n))

pct <- function(x, d = 2) paste0(formatC(100 * x, format = "f", digits = d), "%")
txt <- c(
"# Expected effect (pre-specified)", "",
paste0("Written: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z"), ", before any model used FARS data from 2022Q4 onward."),
"Inputs come from downloaded ARCOS (exposure), Census (population) and pre-shortage FARS (power only). Chang et al. 38-58% is from the task brief.", "",
"## Inputs", "",
paste0("- Baseline amphetamine-class supply (amphetamine + lisdexamfetamine), 2022Q1-Q3: ", round(base_rate, 1), " DDD per 1,000 residents aged 18-44 per day."),
paste0("- Implied share of 18-44-year-olds on amphetamine-class stimulants on a given day: upper bound ", pct(share_upper), " (all supply to ages 18-44, 1 DDD per user-day); half-of-supply scenario ", pct(share_half), " (assumption, not data)."),
paste0("- National supply shortfall vs 2017-2022Q3 trend, 2022Q4-2023Q4: ", pct(nat_gap, 1), "."),
"- Crash reduction while on stimulants (Chang et al.): 38-58%.", "",
"## Expected national effect on young-driver fatal crash rate", "",
paste0("- Prompt formula (share x drop x reduction): ", pct(min(exp_formula), 3), " to ", pct(max(exp_formula), 3), "."),
paste0("- Alternative (risk increase when off treatment = 1/(1-r)-1, i.e. 61-138%): ", pct(min(exp_rr), 3), " to ", pct(max(exp_rr), 3), "."),
paste0("- In expected excess crashes per quarter (baseline ", round(base_q), " crashes with a driver 18-44 per quarter, 2022Q1-Q3): ",
       round(min(exp_formula) * base_q, 1), " to ", round(max(exp_rr) * base_q, 1), "."), "",
"## Expected dose-response effect (per 10 percentage-point state shortfall)", "",
paste0("- ", pct(min(per10_formula), 3), " to ", pct(max(per10_formula), 3), " increase in young-driver fatal crashes."), "",
"## Power (from pre-shortage data only)", "",
"Minimum detectable effect (80% power, 5% two-sided) = exp(2.8 x SE) - 1, with SE from the same model fitted to 2017Q1-2022Q3 with a placebo post period 2021Q4-2022Q3.", "",
paste0("- State dose-response (per 10 pp shortfall): MDE = ", pct(mde_dose, 1), "."),
paste0("- National young (18-44) vs older (55-74) comparison: MDE = ", pct(mde_nat, 1), "."), "",
"## Conclusion before looking at results", "",
paste0("The expected effect (at most ", pct(max(exp_rr), 2), " nationally, ", pct(max(per10_formula), 2), " per 10 pp) is ",
       round(mde_nat / max(exp_rr)), "-fold smaller than the national MDE and ", round(mde_dose / max(per10_formula)), "-fold smaller than the dose-response MDE. ",
       "The design cannot detect the effect that the Swedish within-person estimates imply. A significant crash increase would therefore be larger than the plausible pharmacological effect and should be treated with suspicion; a null result is the expected outcome and only rules out effects larger than the MDE.")
)
writeLines(txt, "expected_effect.md")
cat(txt, sep = "\n")
