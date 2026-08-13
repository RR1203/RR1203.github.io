"""Step 2: parse raw WONDER responses into tidy long-format CSVs in data/.

Outputs (schema documented in data/DICTIONARY.md):
  data/rates_year.csv       one row per db x series x year          (AAR queries)
  data/rates_year_sex.csv   one row per db x series x year x sex    (AAR queries)
  data/rates_year_age.csv   one row per db x series x year x age    (age-specific)
Suppression/reliability markers become explicit boolean flag columns — never
silently missing values or zeros. Every transformation is logged with before/after
row counts.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wonder_client import PROJECT_ROOT, make_logger
import wonder_api as wa

RAW = PROJECT_ROOT / "raw"
DATA = PROJECT_ROOT / "data"

log = make_logger("02_clean")

BASE_COLS = ["db", "series", "qid"]
MEASURES_AAR = ["deaths", "population", "crude_rate", "age_adjusted_rate"]
MEASURES_CRUDE = ["deaths", "population", "crude_rate"]
FLAG_SUFFIXES = ["_suppressed", "_unreliable", "_not_applicable"]


def cell_to_columns(prefix: str, cell: str) -> dict:
    """One WONDER value cell -> numeric column + three explicit flag columns."""
    s = cell.strip()
    return {
        prefix: "" if s in wa.MARKERS or s == "" else wa.numeric(s),
        prefix + "_suppressed": s == "Suppressed",
        prefix + "_unreliable": s == "Unreliable",
        prefix + "_not_applicable": s == "Not Applicable",
    }


def year_from_label(label: str) -> int:
    parts = label.strip().split()
    if not parts or not (parts[0].isdigit() and 1990 <= int(parts[0]) <= 2035):
        raise ValueError(f"unparseable year label {label!r}")
    return int(parts[0])


def clean_query(spec: wa.QuerySpec, xml_bytes: bytes) -> list[dict]:
    parsed = wa.parse_response(xml_bytes, spec.n_groupby, spec.n_measures)
    if not parsed.ok:
        raise RuntimeError(f"{spec.qid}: raw response does not parse: {parsed.message}")
    measures = MEASURES_AAR if spec.aar else MEASURES_CRUDE
    out = []
    for row in parsed.rows:
        labels, values = row[: spec.n_groupby], row[spec.n_groupby:]
        rec: dict = {"db": spec.db, "series": spec.series, "qid": spec.qid,
                     "year": year_from_label(labels[0])}
        if spec.strata == "year_sex":
            rec["sex"] = labels[1]
        elif spec.strata == "year_age":
            rec["age_group"] = labels[1]
        for m, v in zip(measures, values):
            rec.update(cell_to_columns(m, v))
        out.append(rec)
    log.info("%s: %d raw rows -> %d tidy rows (%d totals rows skipped at parse)",
             spec.qid, len(parsed.rows), len(out), parsed.total_rows_skipped)
    return out


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["db"], r["series"], r["year"],
                                             str(r.get("sex", "")), str(r.get("age_group", "")))):
            w.writerow(r)
    log.info("wrote %s: %d rows", path.name, len(rows))


def measure_columns(measures: list[str]) -> list[str]:
    cols = []
    for m in measures:
        cols.append(m)
        cols.extend(m + s for s in FLAG_SUFFIXES)
    return cols


def main() -> int:
    if not (RAW / "manifest.csv").exists():
        log.error("BLOCKED: raw/manifest.csv does not exist — fetch has not produced data")
        return 3
    with (RAW / "manifest.csv").open() as fh:
        manifest = {r["qid"]: r for r in csv.DictReader(fh) if r["status"] == "ok"}
    plan = {s.qid: s for s in wa.build_query_plan()}
    missing = [q for q in plan if q not in manifest]
    if missing:
        log.warning("queries without successful responses (excluded): %s", ", ".join(missing))

    buckets: dict[str, list[dict]] = {"year": [], "year_sex": [], "year_age": []}
    for qid, spec in plan.items():
        if qid not in manifest:
            continue
        xml_bytes = (RAW / "responses" / f"{qid}.xml").read_bytes()
        buckets[spec.strata].extend(clean_query(spec, xml_bytes))

    if not any(buckets.values()):
        log.error("BLOCKED: no successful responses to clean")
        return 3

    DATA.mkdir(exist_ok=True)
    write_csv(DATA / "rates_year.csv", buckets["year"],
              BASE_COLS + ["year"] + measure_columns(MEASURES_AAR))
    write_csv(DATA / "rates_year_sex.csv", buckets["year_sex"],
              BASE_COLS + ["year", "sex"] + measure_columns(MEASURES_AAR))
    write_csv(DATA / "rates_year_age.csv", buckets["year_age"],
              BASE_COLS + ["year", "age_group"] + measure_columns(MEASURES_CRUDE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
