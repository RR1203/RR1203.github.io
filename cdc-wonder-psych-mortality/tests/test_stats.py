"""Tests that the pre-registered statistical methods recover known SYNTHETIC truths."""
import numpy as np
import pandas as pd
import pytest

import stats_lib as sl

SYNTHETIC_YEARS = np.arange(1999, 2021)


def test_aapc_recovers_exact_exponential_growth():
    rates = 100.0 * np.exp(0.02 * (SYNTHETIC_YEARS - 2000))
    res, text = sl.aapc_loglinear(SYNTHETIC_YEARS, rates)
    assert res["aapc_pct"] == pytest.approx(100 * (np.exp(0.02) - 1), abs=1e-9)
    assert res["n_years"] == 22
    assert "AAPC" in text and "OLS" in text
    assert "Date:" not in text and "Time:" not in text   # deterministic output
    assert sl.decide_h1({"aapc_ci_lo": 1.0, "aapc_ci_hi": 3.0}) == "CONFIRMED"
    assert sl.decide_h1({"aapc_ci_lo": -1.0, "aapc_ci_hi": 3.0}) == "INCONCLUSIVE"
    assert sl.decide_h1({"aapc_ci_lo": -3.0, "aapc_ci_hi": -1.0}) == "REFUTED"


def test_segmented_recovers_known_breakpoint_slopes():
    knot = 2010
    pre, post = 0.03, -0.05
    ln = np.where(SYNTHETIC_YEARS <= knot,
                  5 + pre * (SYNTHETIC_YEARS - knot),
                  5 + post * (SYNTHETIC_YEARS - knot))
    res, _ = sl.segmented_loglinear(SYNTHETIC_YEARS, np.exp(ln), knot)
    assert res["b1_pre_slope"] == pytest.approx(pre, abs=1e-9)
    assert res["b2_slope_change"] == pytest.approx(post - pre, abs=1e-9)
    assert res["n_pre"] == 12 and res["n_post"] == 10
    assert sl.decide_h3({"b1_ci": [0.01, 0.05], "b2_ci": [-0.1, -0.01]}) == "CONFIRMED"
    assert sl.decide_h3({"b1_ci": [-0.05, -0.01], "b2_ci": [-0.1, -0.01]}) == "REFUTED"
    assert sl.decide_h3({"b1_ci": [0.01, 0.05], "b2_ci": [-0.1, 0.01]}) == "INCONCLUSIVE"


def test_h2_interaction_recovers_growth_difference():
    pop = 1e7
    rows = []
    for cat, base, growth in (("0_SYNTH_ref", -9.0, 0.01), ("1_SYNTH_interest", -9.5, 0.06)):
        for y in SYNTHETIC_YEARS:
            mu = pop * np.exp(base + growth * (y - 2009.5))
            rows.append({"year": y, "category": cat, "deaths": round(mu), "population": pop})
    res, text = sl.h2_count_interaction(pd.DataFrame(rows))
    assert res["interest"] == "1_SYNTH_interest"
    assert res["primary_interaction"] == pytest.approx(0.05, abs=1e-3)
    assert res["primary_irr_ratio"] == pytest.approx(np.exp(0.05), abs=1e-3)
    assert "Poisson" in text
    assert sl.decide_h2({"primary_inter_ci": [0.01, 0.09]}) == "CONFIRMED"
    assert sl.decide_h2({"primary_inter_ci": [-0.09, -0.01]}) == "REFUTED"
    assert sl.decide_h2({"primary_inter_ci": [-0.01, 0.09]}) == "INCONCLUSIVE"


def test_aapc_rejects_nonpositive_rates():
    with pytest.raises(ValueError):
        sl.aapc_loglinear(SYNTHETIC_YEARS, np.zeros_like(SYNTHETIC_YEARS, dtype=float))
