"""End-to-end: SYNTHETIC tidy data -> 04_analysis -> 05_outputs, all inside tmp_path.

Verifies the drivers run the full pre-registered analysis and produce every figure,
table and caption — without touching the project's real data/, analysis/ or outputs/.
All values are invented (SYNTHETIC) and never leave pytest's tmp dirs.
"""
import importlib
import json

import numpy as np
import pandas as pd

FLAGS = ["_suppressed", "_unreliable", "_not_applicable"]


def _flags(rec, measures):
    for m in measures:
        for f in FLAGS:
            rec[m + f] = False
    return rec

SERIES_PARAMS = {  # base AAR at 2010, annual log growth
    "A": (8.0, 0.03), "A1": (2.0, 0.05), "A2": (6.0, 0.02),
    "Aprime": (4.0, 0.04), "ALL": (850.0, 0.0),
}


def _aar(series, y):
    if series in ("B", "Bprime"):     # built-in peak at 2018 for the H3 chain
        return 12.0 * np.exp(0.018 * (y - 2018)) if y <= 2018 \
            else 12.0 * np.exp(-0.03 * (y - 2018))
    base, growth = SERIES_PARAMS[series]
    return base * np.exp(growth * (y - 2010))


def synth_frames():
    yr_rows, sex_rows, age_rows = [], [], []
    for db, years in (("D76", range(1999, 2021)), ("D158", range(2018, 2025))):
        for series in ("A", "A1", "A2", "B", "Aprime", "Bprime", "ALL"):
            for y in years:
                pop = 300e6 * (1 + 0.007 * (y - 2010))
                aar = _aar(series, y)
                deaths = round(aar / 1e5 * pop)
                rec = {"db": db, "series": series, "qid": f"SYNTHETIC_{db}_{series}",
                       "year": y, "deaths": float(deaths), "population": pop,
                       "crude_rate": round(deaths / pop * 1e5, 1),
                       "age_adjusted_rate": round(aar, 1)}
                yr_rows.append(_flags(rec, ["deaths", "population", "crude_rate",
                                            "age_adjusted_rate"]))
                for sex, mult in (("Female", 0.8), ("Male", 1.2)):
                    srec = dict(rec, sex=sex, deaths=float(round(deaths * mult / 2)),
                                population=pop / 2,
                                age_adjusted_rate=round(aar * mult, 1))
                    sex_rows.append(_flags(srec, ["deaths", "population", "crude_rate",
                                                  "age_adjusted_rate"]))
                for age, mult in (("15-24", 0.5), ("25-34", 1.5), ("35-44", 1.2)):
                    arec = {"db": db, "series": series, "qid": rec["qid"], "year": y,
                            "age_group": age, "deaths": float(round(deaths * mult / 10)),
                            "population": pop / 10,
                            "crude_rate": round(aar * mult, 1)}
                    age_rows.append(_flags(arec, ["deaths", "population", "crude_rate"]))
    return (pd.DataFrame(yr_rows), pd.DataFrame(sex_rows), pd.DataFrame(age_rows))


def test_analysis_and_outputs_end_to_end(tmp_path, monkeypatch):
    data, analysis = tmp_path / "data", tmp_path / "analysis"
    fig, tab = tmp_path / "outputs" / "figures", tmp_path / "outputs" / "tables"
    data.mkdir()
    yr, yrsex, yrage = synth_frames()
    yr.to_csv(data / "rates_year.csv", index=False)
    yrsex.to_csv(data / "rates_year_sex.csv", index=False)
    yrage.to_csv(data / "rates_year_age.csv", index=False)

    ana = importlib.import_module("04_analysis")
    monkeypatch.setattr(ana, "DATA", data)
    monkeypatch.setattr(ana, "OUT", analysis)
    ana.summary.clear()
    assert ana.main() == 0
    summary = json.loads((analysis / "results_summary.json").read_text())
    # built-in synthetic truths must be recovered
    assert summary["h1_aapc_A1_D76"]["hypothesis_decision"] == "CONFIRMED"
    assert abs(summary["h1_aapc_A1_D76"]["aapc_pct"] - 100 * (np.exp(0.05) - 1)) < 0.2
    assert summary["h3_segmented_B_D76_knot2018"]["hypothesis_decision"] == "CONFIRMED"
    assert summary["h2_counts_A1_vs_A2_D76"]["primary_interaction"] > 0
    assert (analysis / "h1_aapc_A1_D76.txt").exists()
    assert summary["s3_overlap_D76_D158"]["n_pairs"] == 12
    assert summary["s3_overlap_D76_D158"]["max_deaths_pct_diff"] == 0.0

    out = importlib.import_module("05_outputs")
    monkeypatch.setattr(out, "DATA", data)
    monkeypatch.setattr(out, "ANALYSIS", analysis)
    monkeypatch.setattr(out, "FIG", fig)
    monkeypatch.setattr(out, "TAB", tab)
    assert out.main() == 0
    for name in ("fig1_series_A_trends", "fig2_selfharm_segmented",
                 "fig3_sex_stratified", "fig4_age_heatmap_A1"):
        assert (fig / f"{name}.png").exists(), name
        assert (fig / f"{name}.caption.txt").exists(), name
    for name in ("table1_annual_rates", "table2_model_results",
                 "table3_overlap_D76_D158", "table4_suppression_audit"):
        assert (tab / f"{name}.csv").exists(), name
        assert (tab / f"{name}.md").exists(), name
    t1 = pd.read_csv(tab / "table1_annual_rates.csv")
    assert set(t1["series"]) == {"A", "A1", "A2", "B"}
