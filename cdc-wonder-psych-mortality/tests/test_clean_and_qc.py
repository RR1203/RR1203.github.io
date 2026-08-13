"""End-to-end tests of cleaning (and targeted QC checks) on SYNTHETIC fixtures only.

The cleaner runs against a synthetic raw/ tree assembled under pytest's tmp_path;
nothing is ever written into the project's real raw/, data/ or outputs/.
"""
import csv
import importlib

import pandas as pd

import wonder_api as wa
from conftest import FIXTURES

RESP_XML = (FIXTURES / "SYNTHETIC_response_year_sex.xml").read_bytes()
SPEC = wa.QuerySpec("SYNTHETIC_q00", "D76", "A", "year_sex", True, "synthetic test")


def test_clean_query_flags_and_types():
    clean = importlib.import_module("02_clean")
    recs = clean.clean_query(SPEC, RESP_XML)
    assert len(recs) == 6
    r_supp = next(r for r in recs if r["year"] == 2001 and r["sex"] == "Male")
    assert r_supp["deaths"] == "" and r_supp["deaths_suppressed"] is True
    assert r_supp["age_adjusted_rate_suppressed"] is True
    r_unrel = next(r for r in recs if r["year"] == 2002 and r["sex"] == "Female")
    assert r_unrel["crude_rate"] == "" and r_unrel["crude_rate_unreliable"] is True
    assert r_unrel["deaths"] == 15.0
    r_na = next(r for r in recs if r["year"] == 2003 and r["sex"] == "Male")
    assert r_na["population_not_applicable"] is True and r_na["deaths"] == 41.0


def test_clean_main_end_to_end(tmp_path, monkeypatch):
    clean = importlib.import_module("02_clean")
    raw = tmp_path / "raw"
    (raw / "responses").mkdir(parents=True)
    data = tmp_path / "data"
    # q02 is the D76 Series A year_sex query in the pre-registered plan
    (raw / "responses" / "q02.xml").write_bytes(RESP_XML)
    with (raw / "manifest.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["qid", "database", "series", "strata", "purpose",
                                           "rows_returned", "timestamp_utc",
                                           "request_sha256", "response_sha256", "status"])
        w.writeheader()
        w.writerow({"qid": "q02", "database": "D76", "series": "A", "strata": "year_sex",
                    "purpose": "SYNTHETIC test", "rows_returned": 6,
                    "timestamp_utc": "2026-01-01T00:00:00Z",
                    "request_sha256": "x", "response_sha256": "y", "status": "ok"})
    monkeypatch.setattr(clean, "RAW", raw)
    monkeypatch.setattr(clean, "DATA", data)
    assert clean.main() == 0
    df = pd.read_csv(data / "rates_year_sex.csv")
    assert len(df) == 6
    assert df["qid"].unique().tolist() == ["q02"]
    assert bool(df.query("year==2001 and sex=='Male'")["deaths_suppressed"].iloc[0]) is True
    assert df.query("year==2003 and sex=='Female'")["deaths"].iloc[0] == 22.0
    # header-only files for strata with no successful queries
    assert (data / "rates_year.csv").exists()
    assert len(pd.read_csv(data / "rates_year.csv")) == 0


def _dfs_from_fixture():
    clean = importlib.import_module("02_clean")
    recs = clean.clean_query(SPEC, RESP_XML)
    df = pd.DataFrame(recs).replace({"": None})
    for m in ("deaths", "population", "crude_rate", "age_adjusted_rate"):
        df[m] = pd.to_numeric(df[m])
    empty_year = df.iloc[0:0].drop(columns=["sex"])
    empty_age = df.iloc[0:0].rename(columns={"sex": "age_group"}).drop(
        columns=["age_adjusted_rate", "age_adjusted_rate_suppressed",
                 "age_adjusted_rate_unreliable", "age_adjusted_rate_not_applicable"])
    return {"rates_year": empty_year, "rates_year_sex": df, "rates_year_age": empty_age}


def test_qc_suppression_audit_and_cell_invariant():
    qc = importlib.import_module("03_qc")
    dfs = _dfs_from_fixture()
    status, detail = qc.check5_suppression_audit(dfs)
    assert status == "PASS"
    assert "rates_year_sex | D76 | A | 6 | 1" in detail.replace("| D76", "| D76")
    status7, detail7 = qc.check7_completeness(dfs)
    # synthetic 2001-2003 slice must FAIL the 1999-2020 completeness expectation
    assert status7 == "FAIL"
    assert "missing years" in detail7
    assert "cell invariant holds" in detail7


def test_qc_check1_fails_on_missing_preregistered_queries(tmp_path, monkeypatch):
    """A wholly-failed query must FAIL QC loudly, not vanish (review finding)."""
    qc = importlib.import_module("03_qc")
    clean = importlib.import_module("02_clean")
    raw = tmp_path / "raw"
    raw.mkdir()
    with (raw / "manifest.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["qid", "database", "series", "strata", "purpose",
                                           "rows_returned", "timestamp_utc",
                                           "request_sha256", "response_sha256", "status"])
        w.writeheader()
        w.writerow({"qid": "q02", "database": "D76", "series": "A", "strata": "year_sex",
                    "purpose": "SYNTHETIC test", "rows_returned": 6,
                    "timestamp_utc": "2026-01-01T00:00:00Z",
                    "request_sha256": "x", "response_sha256": "y", "status": "ok"})
    monkeypatch.setattr(qc, "RAW", raw)
    recs = clean.clean_query(wa.QuerySpec("q02", "D76", "A", "year_sex", True, "t"), RESP_XML)
    df = pd.DataFrame(recs)
    dfs = {"rates_year": df.iloc[0:0], "rates_year_sex": df, "rates_year_age": df.iloc[0:0]}
    status, detail = qc.check1_rowcounts(dfs)
    assert status == "FAIL"
    assert "missing pre-registered queries" in detail
    assert "q01" in detail and "q30" in detail


def test_qc_cell_invariant_detects_violation():
    qc = importlib.import_module("03_qc")
    dfs = _dfs_from_fixture()
    bad = dfs["rates_year_sex"].copy()
    bad.loc[bad.index[0], "deaths"] = None          # numeric removed, no flag set
    dfs["rates_year_sex"] = bad
    status, detail = qc.check7_completeness(dfs)
    assert status == "FAIL"
    assert "cell invariant violated" in detail
