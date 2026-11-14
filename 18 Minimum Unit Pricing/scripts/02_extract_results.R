# Print headline estimates from results.rds as % change with 95% CI (t-based, robust SE)
suppressMessages({library(tidyverse); library(lmtest); library(sandwich); library(metafor)})
r <- readRDS("results.rds")
pct <- function(m, v, term) {
  ci <- coefci(m, vcov = v, df = df.residual(m))[term, ]
  p <- coeftest(m, vcov = v)[term, 4]
  sprintf("%6.1f%% (95%% CI %6.1f to %6.1f), p=%.3f, n=%d", 100*(exp(coef(m)[term])-1), 100*(exp(ci[1])-1), 100*(exp(ci[2])-1), p, nobs(m))
}
rows <- list(
 c("H0 Scotland Wyper window", "h0_model_wyper","h0_vcov_wyper","mup"),
 c("H0 Scotland primary", "h0_model_main","h0_vcov_main","mup"),
 c("H0 excl 2020-21", "h0_model_nocovid","h0_vcov_nocovid","mup"),
 c("H0 placebo 2016", "h0_model_placebo","h0_vcov_placebo","mup_placebo"),
 c("H0 NE+NW control", "h0_model_nenw","h0_vcov_nenw","mup"),
 c("H0 males", "h0_model_males","h0_vcov_males","mup"),
 c("H0 females", "h0_model_females","h0_vcov_females","mup"),
 c("H1 Scot sales vs E&W", "h1_model_sales_scot","h1_vcov_sales_scot","mup"),
 c("H1 Ireland sales ITS", "h1_model_sales_ie","h1_vcov_sales_ie","mup"),
 c("H1 Ireland sales excl covid", "h1_model_sales_ie_nocovid","h1_vcov_sales_ie_nocovid","mup"),
 c("H1 Ireland sales from 2007", "h1_model_sales_ie_2013","h1_vcov_sales_ie_2013","mup"),
 c("H3 Wales primary", "h3_model_main","h3_vcov_main","mup"),
 c("H3 Wales excl 2020-21", "h3_model_nocovid","h3_vcov_nocovid","mup"),
 c("H3 Wales placebo 2018", "h3_model_placebo","h3_vcov_placebo","mup_placebo"),
 c("H3 Wales NE+NW", "h3_model_nenw","h3_vcov_nenw","mup"),
 c("H3 Wales males", "h3_model_males","h3_vcov_males","mup"),
 c("H3 Wales females", "h3_model_females","h3_vcov_females","mup"),
 c("H4 Ireland vs NI", "h4_model_ni","h4_vcov_ni","mup"),
 c("H4 Ireland vs England", "h4_model_eng","h4_vcov_eng","mup"),
 c("H4 Ireland K70 vs NI", "h4_model_k70","h4_vcov_k70","mup"),
 c("H4 Ireland excl 2020-21", "h4_model_nocovid","h4_vcov_nocovid","mup"),
 c("H4 Ireland placebo 2020", "h4_model_placebo","h4_vcov_placebo","mup_placebo"),
 c("H4 Ireland males", "h4_model_males","h4_vcov_males","mup"),
 c("H4 Ireland females", "h4_model_females","h4_vcov_females","mup"),
 c("H6 65p monthly ITS", "h6_model_monthly","h6_vcov_monthly","step_65p"),
 c("H6 65p annual vs Eng", "h6_model_annual","h6_vcov_annual","mup_65p"),
 c("H6 65p long series", "h6_model_long","h6_vcov_long","step_65p"),
 c("H6 65p excl covid", "h6_model_nocovid","h6_vcov_nocovid","step_65p"),
 c("H6 placebo Oct 2022", "h6_model_placebo","h6_vcov_placebo","step_placebo"),
 c("H7 Q1 excl covid", "h7_model_q1_nocovid","h7_vcov_q1_nocovid","mup"),
 c("H7 Q5 excl covid", "h7_model_q5_nocovid","h7_vcov_q5_nocovid","mup"),
 c("S1 Scot cancer (neg ctrl)", "s1_model_scot_cancer","s1_vcov_scot_cancer","mup"),
 c("S1 Ireland non-alc cancer", "s1_model_ie_cancer","s1_vcov_ie_cancer","mup"),
 c("S1 Scot oesophageal ITS", "s1_model_scot_oes","s1_vcov_scot_oes","mup"),
 c("S1 Ireland oesophageal ITS", "s1_model_ie_oes","s1_vcov_ie_oes","mup"),
 c("S2 Scot admissions vs Eng", "s2_model_scotland","s2_vcov_scotland","mup"),
 c("S2 Ireland admissions vs Eng", "s2_model_ireland","s2_vcov_ireland","mup"),
 c("S2 Scot admissions ITS", "s2_model_scot_its","s2_vcov_scot_its","mup"),
 c("S2 Ireland admissions ITS", "s2_model_ie_its","s2_vcov_ie_its","mup"),
 c("S3 NT vs other states", "s3_model_nt","s3_vcov_nt","mup"))
for (x in rows) cat(sprintf("%-30s %s\n", x[1], pct(r[[x[2]]], r[[x[3]]], x[4])))
cat("\nMDE 65p monthly:", round(r$h6_mde_pct,1), "%\n")
print(r$h2_power); print(r$h7_gradient); print(summary(r$h7_model_gradient)$beta); 
cat("\nPooled RE:", round(100*(exp(c(r$h5_model_pooled$b, r$h5_model_pooled$ci.lb, r$h5_model_pooled$ci.ub))-1),1), " I2=", round(r$h5_model_pooled$I2,1), " p=", signif(r$h5_model_pooled$pval,3), "\n")
cat("Replication RE (Wales+Ireland):", round(100*(exp(c(r$h5_model_replication$b, r$h5_model_replication$ci.lb, r$h5_model_replication$ci.ub))-1),1), "\n")
print(r$h1_price)
print(r$h0_sc_weights %>% filter(weight>0)); print(r$h0_sc_effect); print(range(r$h0_sc_loo$effect_pct)); print(r$h0_sc_placebo)
print(r$h3_sc_weights %>% filter(weight>0)); print(r$h3_sc_effect); print(range(r$h3_sc_loo$effect_pct)); print(r$h3_sc_placebo)
print(r$h0_placebo_space); print(r$s3_placebo)
cat("\n--- 2007-window and slope-change robustness ---\n")
for (x in list(c("H0 2007 window","h0_model_2007","h0_vcov_2007","mup"), c("H0 placebo 2016 on 2007 window","h0_model_placebo_2007","h0_vcov_placebo_2007","mup_placebo"),
               c("H3 2007 window","h3_model_2007","h3_vcov_2007","mup"), c("H4 2007 window","h4_model_2007","h4_vcov_2007","mup")))
  cat(sprintf("%-30s %s\n", x[1], pct(r[[x[2]]], r[[x[3]]], x[4])))
print(bind_rows(Scotland=r$h0_slope_avg, Wales=r$h3_slope_avg, Ireland=r$h4_slope_avg, .id="j"))
