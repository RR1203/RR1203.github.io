"""Step 3: quality control. Writes qc/qc_report.md with explicit PASS/FAIL per check.

Checks (00_protocol.md §8, §10 and the operating contract):
  1. Tidy row counts match raw/manifest.csv.
  2. External benchmark: all-cause deaths vs a figure on a www.cdc.gov page saved
     during this run (references/sources/faststats-deaths.html).
  3. Internal consistency: stratum sums vs year totals, suppression shortfall
     quantified (each suppressed cell holds 1-9 deaths).
  4. D76 vs D158 overlap (2018-2020) for every study series.
  5. Suppressed/unreliable audit table by query and stratum.
  6. Denominator sanity (population magnitude, no zero/negative, cross-series equality).
  7. Completeness: full year x stratum grid; duplicates; cell invariant
     (numeric XOR exactly one flag).
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wonder_client import PROJECT_ROOT, make_logger

DATA = PROJECT_ROOT / "data"
RAW = PROJECT_ROOT / "raw"
QC = PROJECT_ROOT / "qc"
REF = PROJECT_ROOT / "references" / "sources"

log = make_logger("03_qc")

EXPECTED_SEXES = {"Female", "Male"}
STUDY_SERIES = ["A", "A1", "A2", "B"]


def load() -> dict[str, pd.DataFrame]:
    dfs = {}
    for name in ("rates_year", "rates_year_sex", "rates_year_age"):
        dfs[name] = pd.read_csv(DATA / f"{name}.csv")
    return dfs


def check1_rowcounts(dfs) -> tuple[str, str]:
    with (RAW / "manifest.csv").open() as fh:
        manifest = [r for r in csv.DictReader(fh) if r["status"] == "ok"]
    lines, ok = [], True
    tidy_counts = pd.concat([df.groupby("qid").size() for df in dfs.values()])
    for row in manifest:
        expect = int(row["rows_returned"])
        got = int(tidy_counts.get(row["qid"], 0))
        if expect != got:
            ok = False
            lines.append(f"- **{row['qid']}**: manifest says {expect} rows, tidy data has {got}")
    detail = "All tidy row counts equal `rows_returned` in raw/manifest.csv." if ok \
        else "\n".join(lines)
    return ("PASS" if ok else "FAIL", detail)


def check2_external_benchmark(dfs) -> tuple[str, str]:
    page = REF / "faststats-deaths.html"
    if not page.exists():
        return ("FAIL", "Benchmark page references/sources/faststats-deaths.html was not "
                        "fetched during this run; no external comparison possible.")
    html = page.read_text(errors="replace")
    text = re.sub(r"<[^>]+>", " ", html)
    m = re.search(r"Number of deaths[^0-9]{0,80}([\d,]{7,})", text)
    ym = re.search(r"[Dd]ata are for\D{0,20}(20\d\d)", text)
    if not m or not ym:
        return ("FAIL", "Could not parse a total-deaths figure and data year from the saved "
                        "FastStats page; inspect references/sources/faststats-deaths.html "
                        "manually. No number is assumed.")
    bench, year = int(m.group(1).replace(",", "")), int(ym.group(1))
    ally = dfs["rates_year"].query("series == 'ALL' and year == @year")
    if ally.empty:
        return ("FAIL", f"FastStats figure is for {year}, but no all-cause WONDER row for "
                        f"{year} exists in the fetched data.")
    lines = [f"FastStats (saved page): **{bench:,}** deaths in **{year}**.", ""]
    ok = False
    for _, r in ally.iterrows():
        diff = abs(r["deaths"] - bench) / bench * 100
        lines.append(f"- {r['db']} all-cause {year}: {int(r['deaths']):,} "
                     f"({diff:.3f}% difference)")
        ok = ok or diff <= 2.0
    return ("PASS" if ok else "FAIL", "\n".join(lines))


def check3_internal_consistency(dfs) -> tuple[str, str]:
    totals = dfs["rates_year"].set_index(["db", "series", "year"])["deaths"]
    lines, ok = [], True
    for name, key in (("rates_year_sex", "sex"), ("rates_year_age", "age_group")):
        df = dfs[name][dfs[name]["series"].isin(STUDY_SERIES)]
        g = df.groupby(["db", "series", "year"])
        agg = g.agg(sum_deaths=("deaths", "sum"),
                    n_supp=("deaths_suppressed", "sum"),
                    n=("deaths", "size"))
        mism = 0
        for idx, row in agg.iterrows():
            if idx not in totals.index or pd.isna(totals.loc[idx]):
                continue
            total = totals.loc[idx]
            shortfall = total - row["sum_deaths"]
            if row["n_supp"] == 0 and shortfall != 0:
                ok = False
                mism += 1
                if mism <= 8:
                    lines.append(f"- **{name}** {idx}: stratum sum {int(row['sum_deaths']):,} "
                                 f"≠ total {int(total):,} with no suppression")
            elif row["n_supp"] > 0 and not (0 < shortfall <= 9 * row["n_supp"]):
                ok = False
                mism += 1
                if mism <= 8:
                    lines.append(f"- **{name}** {idx}: shortfall {shortfall:,.0f} outside "
                                 f"(0, 9x{int(row['n_supp'])}] for {int(row['n_supp'])} suppressed cells")
        supp_tot = int(agg["n_supp"].sum())
        with_supp = agg[agg["n_supp"] > 0]
        short_sum = float((totals.reindex(with_supp.index) - with_supp["sum_deaths"]).sum()) \
            if len(with_supp) else 0.0
        lines.append(f"- {name}: {len(agg)} db×series×year groups checked, {mism} mismatches; "
                     f"{supp_tot} suppressed cells inducing a total shortfall of "
                     f"{short_sum:,.0f} deaths across {len(with_supp)} groups")
    return ("PASS" if ok else "FAIL", "\n".join(lines))


def check4_overlap(dfs) -> tuple[str, str]:
    df = dfs["rates_year"]
    lines = ["| series | year | D76 deaths | D158 deaths | Δ% deaths | D76 AAR | D158 AAR | Δ% AAR |",
             "|--------|------|-----------:|------------:|----------:|--------:|---------:|-------:|"]
    ok, found = True, False
    for series in STUDY_SERIES:
        for year in (2018, 2019, 2020):
            a = df.query("db=='D76' and series==@series and year==@year")
            b = df.query("db=='D158' and series==@series and year==@year")
            if a.empty or b.empty:
                continue
            found = True
            d76, d158 = a.iloc[0], b.iloc[0]
            dd = abs(d76["deaths"] - d158["deaths"]) / d158["deaths"] * 100
            da = abs(d76["age_adjusted_rate"] - d158["age_adjusted_rate"]) / d158["age_adjusted_rate"] * 100
            ok = ok and dd <= 2.0 and da <= 2.0
            lines.append(f"| {series} | {year} | {int(d76['deaths']):,} | {int(d158['deaths']):,} "
                         f"| {dd:.3f}% | {d76['age_adjusted_rate']:.1f} | "
                         f"{d158['age_adjusted_rate']:.1f} | {da:.3f}% |")
    if not found:
        return ("FAIL", "No overlapping 2018-2020 rows present in both databases.")
    return ("PASS" if ok else "FAIL",
            "\n".join(lines) + "\n\nThreshold: ≤2% (protocol S3); counts expected to agree ≈1%.")


def check5_suppression_audit(dfs) -> tuple[str, str]:
    lines = ["| file | db | series | cells | suppressed | % | unreliable rates | % |",
             "|------|----|--------|------:|-----------:|--:|-----------------:|--:|"]
    for name, df in dfs.items():
        for (db, series), g in df.groupby(["db", "series"]):
            n = len(g)
            ns = int(g["deaths_suppressed"].sum())
            nu = int(g["crude_rate_unreliable"].sum())
            lines.append(f"| {name} | {db} | {series} | {n} | {ns} | {ns/n*100:.1f}% "
                         f"| {nu} | {nu/n*100:.1f}% |")
    lines.append("")
    lines.append("Suppressed cells are excluded from analysis, never imputed "
                 "(protocol §8). This check reports; it cannot fail.")
    return ("PASS", "\n".join(lines))


def check6_denominators(dfs) -> tuple[str, str]:
    lines, ok = [], True
    y = dfs["rates_year"]
    pops = y[y["population"].notna() & (y["population"] != "")]
    bad = pops[pd.to_numeric(pops["population"]) <= 0]
    if len(bad):
        ok = False
        lines.append(f"- {len(bad)} rows with population ≤ 0")
    nat = pops[pops["series"] == "ALL"]
    for _, r in nat.iterrows():
        p = float(r["population"])
        if not (2.5e8 <= p <= 4.0e8):
            ok = False
            lines.append(f"- {r['db']} {r['year']}: national population {p:,.0f} outside "
                         f"[250M, 400M] (Census order of magnitude)")
    # same-year national denominators must be identical across series within a db
    for (db, year), g in pops.groupby(["db", "year"]):
        vals = set(pd.to_numeric(g["population"]))
        if len(vals) > 1:
            ok = False
            lines.append(f"- {db} {year}: population differs across series: {sorted(vals)[:4]}")
    lines.append(f"- {len(pops)} populated rows checked "
                 f"({len(nat)} national all-cause denominators against Census magnitude)")
    return ("PASS" if ok else "FAIL", "\n".join(lines))


def check7_completeness(dfs) -> tuple[str, str]:
    lines, ok = [], True
    for name, df in dfs.items():
        keys = ["db", "series", "year"] + (["sex"] if "sex" in df else []) \
               + (["age_group"] if "age_group" in df else [])
        dups = df.duplicated(subset=keys).sum()
        if dups:
            ok = False
            lines.append(f"- {name}: {dups} duplicate key rows")
        for db, g in df.groupby("db"):
            lo, hi = int(g["year"].min()), int(g["year"].max())
            expect_lo, expect_hi = (1999, 2020) if db == "D76" else (2018, max(hi, 2023))
            span = set(range(expect_lo, expect_hi + 1))
            for series, gs in g.groupby("series"):
                missing = span - set(gs["year"])
                # a fully suppressed year is absent only if WONDER returned no row; report it
                if missing:
                    ok = False
                    lines.append(f"- {name} {db} series {series}: missing years {sorted(missing)}")
            lines.append(f"- {name} {db}: years {lo}-{hi} present")
        if "sex" in df:
            bad_sex = set(df["sex"]) - EXPECTED_SEXES
            if bad_sex:
                lines.append(f"- {name}: unexpected sex labels {bad_sex} (reported, not fatal)")
    # cell invariant: numeric XOR exactly one flag
    viol = 0
    for name, df in dfs.items():
        for m in ("deaths", "population", "crude_rate", "age_adjusted_rate"):
            if m not in df:
                continue
            flags = df[[m + "_suppressed", m + "_unreliable", m + "_not_applicable"]].sum(axis=1)
            has_val = df[m].notna()
            viol += int(((flags == 0) & ~has_val).sum() + ((flags > 0) & has_val).sum()
                        + (flags > 1).sum())
    if viol:
        ok = False
        lines.append(f"- cell invariant violated in {viol} cells (numeric XOR one flag)")
    else:
        lines.append("- cell invariant holds: every measure cell is numeric XOR exactly one flag")
    return ("PASS" if ok else "FAIL", "\n".join(lines))


def main() -> int:
    if not (DATA / "rates_year.csv").exists():
        log.error("BLOCKED: data/ CSVs missing — cleaning has not run")
        return 3
    dfs = load()
    checks = [
        ("1. Tidy row counts vs raw/manifest.csv", check1_rowcounts),
        ("2. External benchmark (saved cdc.gov page)", check2_external_benchmark),
        ("3. Internal consistency: stratum sums vs totals (suppression shortfall)",
         check3_internal_consistency),
        ("4. D76 vs D158 overlap 2018-2020", check4_overlap),
        ("5. Suppressed/unreliable audit", check5_suppression_audit),
        ("6. Denominator sanity", check6_denominators),
        ("7. Completeness, duplicates, cell invariant", check7_completeness),
    ]
    out = ["# QC report", "",
           "Generated by `scripts/03_qc.py` from `data/*.csv`, `raw/manifest.csv` and "
           "saved reference pages. Every check states PASS or FAIL explicitly.", ""]
    n_fail = 0
    for title, fn in checks:
        try:
            status, detail = fn(dfs)
        except Exception as exc:  # noqa: BLE001 — a crashing check is a failing check
            status, detail = "FAIL", f"check crashed: {exc!r}"
        n_fail += status == "FAIL"
        log.info("%s: %s", title, status)
        out += [f"## {title} — **{status}**", "", detail, ""]
    out.append(f"**Summary: {len(checks) - n_fail}/{len(checks)} checks PASS.**")
    QC.mkdir(exist_ok=True)
    (QC / "qc_report.md").write_text("\n".join(out) + "\n")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
