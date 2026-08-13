"""Step 4: pre-registered analysis. Tests ONLY the hypotheses in 00_protocol.md §5,
plus the pre-specified sensitivity analyses §7 and pre-specified descriptives.

Every fitted model's complete output is saved as a text file under analysis/; headline
numbers additionally land in analysis/results_summary.json (machine-readable, used by
Step 5/6 and claims_map.csv). No number may appear in the manuscript that is not
present in a saved output file. Exploratory work would live in analysis/exploratory/
(none is planned).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wonder_client import PROJECT_ROOT, make_logger
import stats_lib as sl

DATA = PROJECT_ROOT / "data"
OUT = PROJECT_ROOT / "analysis"

log = make_logger("04_analysis")
summary: dict = {}


def save(name: str, res: dict, text: str) -> None:
    (OUT / f"{name}.txt").write_text(text + "\n")
    summary[name] = res
    log.info("saved analysis/%s.txt", name)


def series_year(df: pd.DataFrame, db: str, series: str, y0: int | None = None,
                y1: int | None = None) -> pd.DataFrame:
    g = df[(df["db"] == db) & (df["series"] == series)].sort_values("year")
    if y0 is not None:
        g = g[g["year"] >= y0]
    if y1 is not None:
        g = g[g["year"] <= y1]
    g = g[g["age_adjusted_rate"].notna()]
    return g


def main() -> int:
    if not (DATA / "rates_year.csv").exists():
        log.error("BLOCKED: data/rates_year.csv missing — nothing to analyze")
        return 3
    OUT.mkdir(exist_ok=True)
    (OUT / "exploratory").mkdir(exist_ok=True)
    yr = pd.read_csv(DATA / "rates_year.csv")
    yrsex = pd.read_csv(DATA / "rates_year_sex.csv")

    # ------------------------------------------------------------------ H1
    g = series_year(yr, "D76", "A1", 1999, 2020)
    res, text = sl.aapc_loglinear(g["year"].values, g["age_adjusted_rate"].values)
    res["hypothesis_decision"] = sl.decide_h1(res)
    save("h1_aapc_A1_D76", res, "H1 — Series A1 (F10-F19), D76 1999-2020, age-adjusted rate\n"
         f"Decision per protocol rule: {res['hypothesis_decision']}\n\n" + text)

    # ------------------------------------------------------------------ H2
    counts = yr[(yr["db"] == "D76") & (yr["series"].isin(["A1", "A2"]))
                & yr["deaths"].notna() & yr["population"].notna()]
    h2df = counts.rename(columns={"series": "category"})[
        ["year", "category", "deaths", "population"]]
    # Protocol estimand: A1's extra growth relative to A2. Recode so A1 sorts last
    # (stats_lib treats the last-sorting level as the level of interest).
    h2df2 = h2df.assign(category=h2df["category"].map({"A2": "0_A2_nonsubstance",
                                                       "A1": "1_A1_substance"}))
    res, text = sl.h2_count_interaction(h2df2)
    res["hypothesis_decision"] = sl.decide_h2(res)
    save("h2_counts_A1_vs_A2_D76", res,
         "H2 — D76 1999-2020, A1 (substance) vs A2 (non-substance), interaction = extra "
         "annual log-rate growth of A1\n"
         f"Decision per protocol rule: {res['hypothesis_decision']}\n\n" + text)

    # ------------------------------------------------------------------ H3
    g = series_year(yr, "D76", "B", 1999, 2020)
    res, text = sl.segmented_loglinear(g["year"].values, g["age_adjusted_rate"].values, 2018)
    res["hypothesis_decision"] = sl.decide_h3(res)
    save("h3_segmented_B_D76_knot2018", res,
         "H3 — Series B (intentional self-harm), D76 1999-2020, knot 2018 (a priori)\n"
         f"Decision per protocol rule: {res['hypothesis_decision']}\n\n" + text)

    # ------------------------------------------------------------------ S1 alternative definitions
    for series in ("A", "Aprime"):
        g = series_year(yr, "D76", series, 1999, 2020)
        res, text = sl.aapc_loglinear(g["year"].values, g["age_adjusted_rate"].values)
        save(f"s1_aapc_{series}_D76", res,
             f"S1 — chapter-level robustness: series {series}, D76 1999-2020\n\n" + text)
    g = series_year(yr, "D76", "Bprime", 1999, 2020)
    res, text = sl.segmented_loglinear(g["year"].values, g["age_adjusted_rate"].values, 2018)
    save("s1_segmented_Bprime_D76_knot2018", res,
         "S1 — Series B' (X60-X84 only), D76 1999-2020, knot 2018\n\n" + text)

    # ------------------------------------------------------------------ S2 exclude 2020
    g = series_year(yr, "D76", "A1", 1999, 2019)
    res, text = sl.aapc_loglinear(g["year"].values, g["age_adjusted_rate"].values)
    save("s2_h1_excl2020", res, "S2 — H1 refit on 1999-2019 (COVID-era certification "
         "sensitivity)\n\n" + text)
    h2df3 = h2df2[h2df2["year"] <= 2019]
    res, text = sl.h2_count_interaction(h2df3)
    save("s2_h2_excl2020", res, "S2 — H2 refit on 1999-2019\n\n" + text)
    g = series_year(yr, "D76", "B", 1999, 2019)
    res, text = sl.segmented_loglinear(g["year"].values, g["age_adjusted_rate"].values, 2018)
    save("s2_h3_excl2020", res, "S2 — H3 refit on 1999-2019 (one post-break year; the "
         "slope-change term is estimable only degenerately — protocol caveat applies)\n\n" + text)

    # ------------------------------------------------------------------ S3 cross-database overlap
    rows = []
    for series in ("A", "A1", "A2", "B"):
        for year in (2018, 2019, 2020):
            a = series_year(yr, "D76", series, year, year)
            b = series_year(yr, "D158", series, year, year)
            if a.empty or b.empty:
                continue
            d76, d158 = a.iloc[0], b.iloc[0]
            rows.append({
                "series": series, "year": year,
                "d76_deaths": float(d76["deaths"]), "d158_deaths": float(d158["deaths"]),
                "deaths_pct_diff": abs(d76["deaths"] - d158["deaths"]) / d158["deaths"] * 100,
                "d76_aar": float(d76["age_adjusted_rate"]),
                "d158_aar": float(d158["age_adjusted_rate"]),
                "aar_pct_diff": abs(d76["age_adjusted_rate"] - d158["age_adjusted_rate"])
                                / d158["age_adjusted_rate"] * 100,
            })
    s3 = pd.DataFrame(rows)
    res = {"n_pairs": len(s3),
           "max_deaths_pct_diff": float(s3["deaths_pct_diff"].max()) if len(s3) else None,
           "max_aar_pct_diff": float(s3["aar_pct_diff"].max()) if len(s3) else None,
           "pairs": rows}
    save("s3_overlap_D76_D158", res,
         "S3 — D76 vs D158 overlap 2018-2020 (never spliced; QC cross-check)\n\n"
         + (s3.to_string(index=False) if len(s3) else "NO OVERLAP ROWS AVAILABLE"))

    # ------------------------------------------------------------------ S4 alternative knots
    for knot in (2017, 2019):
        g = series_year(yr, "D76", "B", 1999, 2020)
        res, text = sl.segmented_loglinear(g["year"].values, g["age_adjusted_rate"].values, knot)
        save(f"s4_segmented_B_D76_knot{knot}", res,
             f"S4 — H3 with alternative a-priori candidate knot {knot}\n\n" + text)

    # ------------------------------------------------------------------ pre-specified descriptives
    desc: dict = {}
    for db in ("D76", "D158"):
        for series in ("A", "A1", "A2", "B"):
            g = series_year(yr, db, series)
            if g.empty:
                continue
            first, last = g.iloc[0], g.iloc[-1]
            desc[f"{db}_{series}"] = {
                "first_year": int(first["year"]), "first_deaths": float(first["deaths"]),
                "first_aar": float(first["age_adjusted_rate"]),
                "last_year": int(last["year"]), "last_deaths": float(last["deaths"]),
                "last_aar": float(last["age_adjusted_rate"]),
                "peak_year": int(g.loc[g["age_adjusted_rate"].idxmax(), "year"]),
                "peak_aar": float(g["age_adjusted_rate"].max()),
            }
    lines = ["Pre-specified descriptives: first/last/peak age-adjusted rates by db x series", ""]
    for k, v in desc.items():
        lines.append(f"{k}: {v['first_year']} deaths={v['first_deaths']:.0f} "
                     f"AAR={v['first_aar']}; {v['last_year']} deaths={v['last_deaths']:.0f} "
                     f"AAR={v['last_aar']}; peak {v['peak_year']} AAR={v['peak_aar']}")
    sexres = {}
    for db in ("D76", "D158"):
        for series in ("A", "A1", "A2", "B"):
            for sex in ("Female", "Male"):
                g = yrsex[(yrsex["db"] == db) & (yrsex["series"] == series)
                          & (yrsex["sex"] == sex) & yrsex["age_adjusted_rate"].notna()]
                if len(g) < 5:
                    continue
                r, t = sl.aapc_loglinear(g["year"].values, g["age_adjusted_rate"].values)
                sexres[f"{db}_{series}_{sex}"] = r
                lines += ["", f"== AAPC {db} {series} {sex} ==", t.split("\n\n")[0]]
    save("descriptive_first_last_peak_and_sex_aapc",
         {"first_last_peak": desc, "sex_aapc": sexres}, "\n".join(lines))

    with (OUT / "results_summary.json").open("w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True, default=str)
    log.info("wrote analysis/results_summary.json with %d entries", len(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
