"""Step 5: figures (PNG) and tables (CSV + markdown) from cleaned data + saved analyses.

Every figure/table gets a caption file naming the producing script and input files.
Design follows the project's dataviz conventions: color is assigned to a series
(entity) in fixed slot order and never re-used; the database (D76 vs D158) is
carried by linestyle, never by a second axis; one y-axis per chart; recessive
grid/axes; direct labels plus a legend.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wonder_client import PROJECT_ROOT, make_logger

DATA = PROJECT_ROOT / "data"
ANALYSIS = PROJECT_ROOT / "analysis"
FIG = PROJECT_ROOT / "outputs" / "figures"
TAB = PROJECT_ROOT / "outputs" / "tables"

log = make_logger("05_outputs")

# Validated light-mode palette (dataviz reference instance), fixed slot order.
SLOT = {"A": "#2a78d6", "A1": "#eb6834", "A2": "#1baf7a", "B": "#2a78d6",
        "Female": "#2a78d6", "Male": "#eb6834"}
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
DB_STYLE = {"D76": "-", "D158": (0, (4, 2))}
SERIES_LABEL = {"A": "All mental & behavioural (F01–F99)",
                "A1": "Substance-induced (F10–F19)",
                "A2": "Non-substance (F01–F09, F20–F99)",
                "B": "Intentional self-harm"}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 1.0,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
    "axes.labelcolor": INK2, "font.size": 10.5,
    "font.family": "sans-serif", "axes.spines.top": False, "axes.spines.right": False,
})


def style_axes(ax):
    ax.grid(axis="x", visible=False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    ax.margins(x=0.02)


def save_fig(fig, name: str, caption: str, inputs: list[str]) -> None:
    path = FIG / f"{name}.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    (FIG / f"{name}.caption.txt").write_text(
        caption + f"\n\nProduced by scripts/05_outputs.py from: {', '.join(inputs)}.\n")
    log.info("wrote %s", path.name)


def save_table(df: pd.DataFrame, name: str, caption: str, inputs: list[str],
               floatfmt: str | None = "%.1f") -> None:
    df = df.copy()
    for col in df.columns:
        if "deaths" in col and pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].round().astype("Int64")
    df.to_csv(TAB / f"{name}.csv", index=False, float_format=floatfmt)
    md = df.to_markdown(index=False,
                        floatfmt=(floatfmt.replace("%", "") if floatfmt else "g"))
    (TAB / f"{name}.md").write_text(f"**{name}.** {caption}\n\n{md}\n")
    (TAB / f"{name}.caption.txt").write_text(
        caption + f"\n\nProduced by scripts/05_outputs.py from: {', '.join(inputs)}.\n")
    log.info("wrote %s.csv/.md", name)


def line_with_labels(ax, df, series_keys, label_fmt="{key}"):
    for key in series_keys:
        for db, style in DB_STYLE.items():
            g = df[(df["db"] == db) & (df["series"] == key)].sort_values("year")
            g = g[g["age_adjusted_rate"].notna()]
            if g.empty:
                continue
            ax.plot(g["year"], g["age_adjusted_rate"], linestyle=style,
                    color=SLOT[key], linewidth=2,
                    label=f"{SERIES_LABEL[key]} ({db})")
            if db == "D76":
                last = g.iloc[-1]
                ax.annotate(label_fmt.format(key=key), (last["year"], last["age_adjusted_rate"]),
                            xytext=(6, 0), textcoords="offset points",
                            color=SLOT[key], fontsize=9, va="center")


def fig1(yr):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    line_with_labels(ax, yr, ["A", "A1", "A2"])
    style_axes(ax)
    ax.set_ylabel("Age-adjusted deaths per 100,000")
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("Mortality with mental and behavioural disorders as underlying cause,\n"
                 "United States (solid: D76 bridged-race; dashed: D158 single-race)",
                 fontsize=11, loc="left", color=INK)
    save_fig(fig, "fig1_series_A_trends",
             "Age-adjusted death rates for ICD-10 F-chapter case definitions, by year and "
             "database. The two databases are separate series (different race methodology "
             "and denominators) and are deliberately not spliced.",
             ["data/rates_year.csv"])


def fig2(yr, summary):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    g76 = yr[(yr["db"] == "D76") & (yr["series"] == "B")].sort_values("year")
    ax.plot(g76["year"], g76["age_adjusted_rate"], "-", color=SLOT["B"], linewidth=2,
            label="Intentional self-harm (D76)")
    g158 = yr[(yr["db"] == "D158") & (yr["series"] == "B")].sort_values("year")
    if not g158.empty:
        ax.plot(g158["year"], g158["age_adjusted_rate"], linestyle=DB_STYLE["D158"],
                color=SLOT["B"], linewidth=2, label="Intentional self-harm (D158)")
    h3 = summary.get("h3_segmented_B_D76_knot2018")
    if h3:
        yrs = g76["year"].values.astype(float)
        knot = h3["knot"]
        # fitted values from the saved model coefficients (analysis output file)
        b0 = np.log(g76["age_adjusted_rate"]).values - (
            h3["b1_pre_slope"] * (yrs - knot) + h3["b2_slope_change"] * np.maximum(0, yrs - knot))
        fit = np.exp(b0.mean() + h3["b1_pre_slope"] * (yrs - knot)
                     + h3["b2_slope_change"] * np.maximum(0, yrs - knot))
        ax.plot(yrs, fit, linestyle=(0, (1, 2)), color=INK2, linewidth=1.6,
                label=f"Segmented fit (knot {knot}, a priori)")
        ax.axvline(knot, color=GRID, linewidth=1)
    style_axes(ax)
    ax.set_ylabel("Age-adjusted deaths per 100,000")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("Intentional self-harm mortality and the pre-registered 2018 breakpoint",
                 fontsize=11, loc="left", color=INK)
    save_fig(fig, "fig2_selfharm_segmented",
             "Age-adjusted intentional self-harm death rate with the pre-registered "
             "segmented (knot 2018) fit overlaid on the D76 series.",
             ["data/rates_year.csv", "analysis/results_summary.json"])


def fig3(yrsex):
    keys = ["A", "A1", "A2", "B"]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.4), sharex=True)
    for ax, key in zip(axes.flat, keys):
        for sex in ("Female", "Male"):
            for db, style in DB_STYLE.items():
                g = yrsex[(yrsex["db"] == db) & (yrsex["series"] == key)
                          & (yrsex["sex"] == sex)].sort_values("year")
                g = g[g["age_adjusted_rate"].notna()]
                if g.empty:
                    continue
                ax.plot(g["year"], g["age_adjusted_rate"], linestyle=style,
                        color=SLOT[sex], linewidth=1.8,
                        label=f"{sex} ({db})" if key == "A" else None)
        style_axes(ax)
        ax.set_ylim(bottom=0)
        ax.set_title(SERIES_LABEL[key], fontsize=9.5, loc="left", color=INK2)
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.supylabel("Age-adjusted deaths per 100,000", fontsize=10, color=INK2)
    fig.suptitle("Sex-stratified age-adjusted mortality by case definition",
                 fontsize=11.5, x=0.02, ha="left", color=INK)
    fig.tight_layout(rect=(0.015, 0, 1, 0.97))
    save_fig(fig, "fig3_sex_stratified",
             "Sex-stratified age-adjusted death rates for the four pre-registered case "
             "definitions (small multiples; blue = female, orange = male; solid = D76, "
             "dashed = D158).", ["data/rates_year_sex.csv"])


def fig4(yrage):
    g = yrage[(yrage["db"] == "D76") & (yrage["series"] == "A1")].copy()
    g = g[g["crude_rate"].notna() & ~g["age_group"].str.contains("Not Stated", na=False)]
    if g.empty:
        log.warning("fig4 skipped: no unsuppressed age-specific rates for D76 A1")
        return
    order = sorted(g["age_group"].unique(),
                   key=lambda a: int("".join(ch for ch in str(a).split("-")[0]
                                             .split("+")[0] if ch.isdigit()) or 0))
    pivot = g.pivot_table(index="age_group", columns="year", values="crude_rate",
                          aggfunc="first").reindex(order)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    mesh = ax.pcolormesh(pivot.columns, np.arange(len(pivot)), pivot.values,
                         cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
                             "seq_blue", ["#cde2fb", "#3987e5", "#0d366b"]),
                         shading="nearest")
    ax.set_yticks(np.arange(len(pivot)), pivot.index, fontsize=8.5)
    ax.tick_params(length=0)
    ax.grid(False)
    cb = fig.colorbar(mesh, ax=ax, shrink=0.9)
    cb.set_label("Deaths per 100,000 (age-specific)", color=INK2, fontsize=9)
    cb.outline.set_visible(False)
    ax.set_title("Substance-induced mental & behavioural mortality by age group "
                 "(D76, age-specific rates)", fontsize=11, loc="left", color=INK)
    save_fig(fig, "fig4_age_heatmap_A1",
             "Age-specific (crude within age group) death rates for substance-induced "
             "mental and behavioural disorders (F10–F19), D76. Suppressed/unreliable "
             "cells are blank.", ["data/rates_year_age.csv"])


def tables(yr, summary):
    study = yr[yr["series"].isin(["A", "A1", "A2", "B"])].copy()
    t1 = study[["db", "series", "year", "deaths", "crude_rate", "age_adjusted_rate"]].copy()
    t1 = t1.sort_values(["db", "series", "year"])
    save_table(t1, "table1_annual_rates",
               "Annual national deaths and rates per 100,000 by case definition and "
               "database (age-adjusted to the 2000 U.S. standard population).",
               ["data/rates_year.csv"])

    rows = []
    def aapc_row(name, key):
        r = summary[key]
        rows.append({"analysis": name,
                     "estimate": f"AAPC {r['aapc_pct']:.2f}%/yr",
                     "ci95": f"{r['aapc_ci_lo']:.2f} to {r['aapc_ci_hi']:.2f}",
                     "years": f"{r['year_min']}-{r['year_max']}",
                     "decision": r.get("hypothesis_decision", "-")})
    aapc_row("H1: A1 (F10-F19) age-adjusted trend, D76", "h1_aapc_A1_D76")
    h2 = summary["h2_counts_A1_vs_A2_D76"]
    rows.append({"analysis": "H2: extra annual growth, A1 vs A2 (count model)",
                 "estimate": f"ratio of annual rate-ratios {h2['primary_irr_ratio']:.4f}",
                 "ci95": f"{h2['primary_irr_ratio_ci'][0]:.4f} to {h2['primary_irr_ratio_ci'][1]:.4f}",
                 "years": "1999-2020",
                 "decision": h2.get("hypothesis_decision", "-")})
    h3 = summary["h3_segmented_B_D76_knot2018"]
    rows.append({"analysis": "H3: self-harm segmented trend (knot 2018)",
                 "estimate": (f"pre-slope APC {h3['pre_apc_pct']:.2f}%/yr; "
                              f"slope change b2 {h3['b2_slope_change']:.4f}"),
                 "ci95": (f"b1 {h3['b1_ci'][0]:.4f} to {h3['b1_ci'][1]:.4f}; "
                          f"b2 {h3['b2_ci'][0]:.4f} to {h3['b2_ci'][1]:.4f}"),
                 "years": "1999-2020", "decision": h3.get("hypothesis_decision", "-")})
    aapc_row("S1: chapter A (F01-F99)", "s1_aapc_A_D76")
    aapc_row("S1: chapter A' (F10-F99)", "s1_aapc_Aprime_D76")
    aapc_row("S2: H1 excluding 2020", "s2_h1_excl2020")
    for knot in (2017, 2019):
        k = summary[f"s4_segmented_B_D76_knot{knot}"]
        rows.append({"analysis": f"S4: H3 with knot {knot}",
                     "estimate": (f"pre-slope APC {k['pre_apc_pct']:.2f}%/yr; "
                                  f"slope change b2 {k['b2_slope_change']:.4f}"),
                     "ci95": (f"b1 {k['b1_ci'][0]:.4f} to {k['b1_ci'][1]:.4f}; "
                              f"b2 {k['b2_ci'][0]:.4f} to {k['b2_ci'][1]:.4f}"),
                     "years": "1999-2020", "decision": "-"})
    save_table(pd.DataFrame(rows), "table2_model_results",
               "Pre-registered hypothesis tests and sensitivity analyses; full model "
               "outputs in analysis/*.txt.",
               ["analysis/results_summary.json"], floatfmt="%s")

    s3 = summary.get("s3_overlap_D76_D158", {}).get("pairs", [])
    if s3:
        save_table(pd.DataFrame(s3), "table3_overlap_D76_D158",
                   "Cross-database consistency (protocol S3): identical underlying "
                   "certificates, different race methodology/denominators; counts should "
                   "agree within ~1%.", ["analysis/results_summary.json"], floatfmt="%.3f")


def suppression_table():
    rows = []
    for name in ("rates_year", "rates_year_sex", "rates_year_age"):
        df = pd.read_csv(DATA / f"{name}.csv")
        for (db, series), g in df.groupby(["db", "series"]):
            rows.append({"file": name, "db": db, "series": series, "cells": len(g),
                         "deaths_suppressed": int(g["deaths_suppressed"].sum()),
                         "rate_unreliable": int(g["crude_rate_unreliable"].sum())})
    save_table(pd.DataFrame(rows), "table4_suppression_audit",
               "Suppressed and unreliable cells by file, database and series (audit "
               "required by protocol §8; suppressed cells are excluded, never imputed).",
               ["data/*.csv"], floatfmt="%s")


def main() -> int:
    if not (DATA / "rates_year.csv").exists() or not (ANALYSIS / "results_summary.json").exists():
        log.error("BLOCKED: inputs missing (data/ or analysis/) — outputs not produced")
        return 3
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    yr = pd.read_csv(DATA / "rates_year.csv")
    yrsex = pd.read_csv(DATA / "rates_year_sex.csv")
    yrage = pd.read_csv(DATA / "rates_year_age.csv")
    summary = json.loads((ANALYSIS / "results_summary.json").read_text())
    fig1(yr)
    fig2(yr, summary)
    fig3(yrsex)
    fig4(yrage)
    tables(yr, summary)
    suppression_table()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
