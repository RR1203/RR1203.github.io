"""Pre-registered statistical methods (00_protocol.md §5-§7) as pure functions.

Each function returns (result_dict, full_text_output). The text output is the
complete statsmodels summary (with volatile Date/Time lines stripped so re-runs are
byte-identical); the dict carries the headline numbers used downstream. Every number
that reaches the manuscript must exist inside one of these saved text outputs.
"""
from __future__ import annotations

import math
import re

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def _strip_volatile(text: str) -> str:
    return "\n".join(l for l in text.splitlines()
                     if not re.search(r"\b(Date|Time):", l))


def aapc_loglinear(years: np.ndarray, rates: np.ndarray) -> tuple[dict, str]:
    """H1 method: OLS of ln(rate) on year; AAPC with OLS CI (primary) + HAC lag-1 CI."""
    years = np.asarray(years, dtype=float)
    rates = np.asarray(rates, dtype=float)
    if np.any(rates <= 0) or np.any(~np.isfinite(rates)):
        raise ValueError("rates must be positive and finite for log-linear AAPC")
    X = sm.add_constant(years - years.mean())
    ols = sm.OLS(np.log(rates), X).fit()
    hac = sm.OLS(np.log(rates), X).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
    b, (lo, hi) = ols.params[1], ols.conf_int()[1]
    hlo, hhi = hac.conf_int()[1]
    res = {
        "n_years": int(len(years)),
        "year_min": int(years.min()), "year_max": int(years.max()),
        "beta_year": float(b),
        "aapc_pct": 100 * (math.exp(b) - 1),
        "aapc_ci_lo": 100 * (math.exp(lo) - 1),
        "aapc_ci_hi": 100 * (math.exp(hi) - 1),
        "aapc_hac_ci_lo": 100 * (math.exp(hlo) - 1),
        "aapc_hac_ci_hi": 100 * (math.exp(hhi) - 1),
        "r2": float(ols.rsquared),
    }
    text = (f"Log-linear trend, ln(rate) ~ year (centered), {res['year_min']}-{res['year_max']}\n"
            f"AAPC = {res['aapc_pct']:.2f}% per year "
            f"(95% CI {res['aapc_ci_lo']:.2f} to {res['aapc_ci_hi']:.2f}; "
            f"HAC lag-1 CI {res['aapc_hac_ci_lo']:.2f} to {res['aapc_hac_ci_hi']:.2f})\n\n"
            "== OLS ==\n" + _strip_volatile(str(ols.summary())) +
            "\n\n== OLS with HAC (Newey-West, lag 1) standard errors ==\n"
            + _strip_volatile(str(hac.summary())))
    return res, text


def h2_count_interaction(df: pd.DataFrame) -> tuple[dict, str]:
    """H2 method: deaths ~ year_c * category with ln(population) offset.

    df columns: year, category (exactly 2 levels; the level of interest sorts LAST so
    the interaction reads 'extra annual log-growth of that level'), deaths, population.
    Poisson first; Pearson chi2/df reported; NB2 (MLE alpha) is primary if it exceeds 2.
    """
    df = df.copy()
    levels = sorted(df["category"].unique())
    if len(levels) != 2:
        raise ValueError(f"need exactly 2 categories, got {levels}")
    df["year_c"] = df["year"] - df["year"].mean()
    df["cat"] = (df["category"] == levels[1]).astype(float)
    df["inter"] = df["year_c"] * df["cat"]
    X = sm.add_constant(df[["year_c", "cat", "inter"]])
    off = np.log(df["population"].astype(float))
    pois = sm.GLM(df["deaths"], X, family=sm.families.Poisson(), offset=off).fit()
    disp = float(pois.pearson_chi2 / pois.df_resid)
    res = {
        "levels": levels, "reference": levels[0], "interest": levels[1],
        "n_obs": int(len(df)),
        "poisson_interaction": float(pois.params["inter"]),
        "poisson_inter_ci": [float(x) for x in pois.conf_int().loc["inter"]],
        "pearson_dispersion": disp,
        "overdispersed_gt2": disp > 2,
    }
    text = [f"H2 count model: deaths ~ year_c * category(={levels[1]} vs {levels[0]}) "
            f"+ offset(ln population)\n"
            f"Pearson chi2/df dispersion = {disp:.2f} "
            f"({'> 2 -> negative binomial (NB2) is primary' if disp > 2 else '<= 2 -> Poisson is primary'})\n",
            "== Poisson ==", _strip_volatile(str(pois.summary()))]
    if disp > 2:
        import statsmodels.discrete.count_model  # noqa: F401  (register NB)
        from statsmodels.discrete.discrete_model import NegativeBinomial
        nb = NegativeBinomial(df["deaths"], X, offset=off, loglike_method="nb2").fit(
            disp=False, maxiter=200)
        ci = nb.conf_int()
        res.update({
            "nb2_interaction": float(nb.params["inter"]),
            "nb2_inter_ci": [float(ci.loc["inter"][0]), float(ci.loc["inter"][1])],
            "nb2_alpha": float(nb.params.get("alpha", float("nan"))),
        })
        text += ["", "== Negative binomial (NB2, MLE alpha) — PRIMARY ==",
                 _strip_volatile(str(nb.summary()))]
        prim, ci_ = res["nb2_interaction"], res["nb2_inter_ci"]
    else:
        prim, ci_ = res["poisson_interaction"], res["poisson_inter_ci"]
    res["primary_interaction"] = prim
    res["primary_inter_ci"] = list(ci_)
    res["primary_irr_ratio"] = math.exp(prim)
    res["primary_irr_ratio_ci"] = [math.exp(ci_[0]), math.exp(ci_[1])]
    text.insert(1, f"PRIMARY interaction (extra annual log-rate growth of {levels[1]}): "
                   f"{prim:.4f} (95% CI {ci_[0]:.4f} to {ci_[1]:.4f}); "
                   f"ratio of annual rate-ratios {res['primary_irr_ratio']:.4f} "
                   f"(95% CI {res['primary_irr_ratio_ci'][0]:.4f} to "
                   f"{res['primary_irr_ratio_ci'][1]:.4f})\n")
    return res, "\n".join(text)


def segmented_loglinear(years: np.ndarray, rates: np.ndarray, knot: int) -> tuple[dict, str]:
    """H3 method: ln(rate) = b0 + b1*(year-knot) + b2*max(0, year-knot); knot fixed a priori."""
    years = np.asarray(years, dtype=float)
    rates = np.asarray(rates, dtype=float)
    x1 = years - knot
    x2 = np.maximum(0.0, years - knot)
    X = sm.add_constant(np.column_stack([x1, x2]))
    fit = sm.OLS(np.log(rates), X).fit()
    ci = fit.conf_int()
    res = {
        "knot": int(knot),
        "n_pre": int((years <= knot).sum()), "n_post": int((years > knot).sum()),
        "b1_pre_slope": float(fit.params[1]),
        "b1_ci": [float(ci[1][0]), float(ci[1][1])],
        "b2_slope_change": float(fit.params[2]),
        "b2_ci": [float(ci[2][0]), float(ci[2][1])],
        "pre_apc_pct": 100 * (math.exp(fit.params[1]) - 1),
        "post_slope": float(fit.params[1] + fit.params[2]),
        "post_apc_pct": 100 * (math.exp(fit.params[1] + fit.params[2]) - 1),
        "r2": float(fit.rsquared),
    }
    text = (f"Segmented log-linear trend, knot fixed a priori at {knot} "
            f"({res['n_pre']} years ≤ knot, {res['n_post']} after)\n"
            f"pre-break slope b1 = {res['b1_pre_slope']:.4f} "
            f"(95% CI {res['b1_ci'][0]:.4f} to {res['b1_ci'][1]:.4f}) "
            f"= APC {res['pre_apc_pct']:.2f}%/yr\n"
            f"slope change b2 = {res['b2_slope_change']:.4f} "
            f"(95% CI {res['b2_ci'][0]:.4f} to {res['b2_ci'][1]:.4f}); "
            f"post-break APC {res['post_apc_pct']:.2f}%/yr\n\n"
            + _strip_volatile(str(fit.summary())))
    return res, text


def decide_h1(res: dict) -> str:
    if res["aapc_ci_lo"] > 0:
        return "CONFIRMED"
    if res["aapc_ci_hi"] < 0:
        return "REFUTED"
    return "INCONCLUSIVE"


def decide_h2(res: dict) -> str:
    lo, hi = res["primary_inter_ci"]
    if lo > 0:
        return "CONFIRMED"
    if hi < 0:
        return "REFUTED"
    return "INCONCLUSIVE"


def decide_h3(res: dict) -> str:
    b1_pos = res["b1_ci"][0] > 0
    b2_neg = res["b2_ci"][1] < 0
    if b1_pos and b2_neg:
        return "CONFIRMED"
    if res["b1_ci"][1] < 0 or res["b2_ci"][0] > 0:
        return "REFUTED"
    return "INCONCLUSIVE"
