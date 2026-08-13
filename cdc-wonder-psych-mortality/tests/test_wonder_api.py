"""Tests for form parsing, override validation, request XML and response parsing.

All inputs are SYNTHETIC fixtures from tests/fixtures/ — never CDC data.
"""
import xml.etree.ElementTree as ET

import pytest

import wonder_api as wa
from conftest import FIXTURES

FORM_HTML = (FIXTURES / "SYNTHETIC_form.html").read_text()
RESP_XML = (FIXTURES / "SYNTHETIC_response_year_sex.xml").read_bytes()

SYNTH_CFG = {
    "url": "https://wonder.cdc.gov/controller/datarequest/D00",
    "years": (2001, 2003),
    "year_groupby": "D00.V1-level1",
    "sex_groupby": "D00.V7",
    "age_groupby": "D00.V5",
    "icd_var": "D00.V2",
    "age_var": "D00.V5",
    "prefix": "D00",
    "label": "SYNTHETIC database",
}


def test_parse_form_defaults_and_options():
    defaults, options = wa.parse_form(FORM_HTML)
    assert defaults["stage"] == ["request"]
    assert defaults["B_1"] == ["D00.V1-level1"]          # selected option
    assert defaults["B_2"] == ["*None*"]
    assert defaults["O_aar"] == ["aar_none"]             # checked radio only
    assert "D00.V7" in options["B_1"]
    assert defaults["O_aar_pop"] == ["0000"]


def test_overrides_validate_cleanly_and_prune_optional():
    defaults, options = wa.parse_form(FORM_HTML)
    spec = wa.QuerySpec("SYNTHETIC_q00", "D76", "B", "year_sex", True, "synthetic")
    over = wa.build_overrides(spec, SYNTH_CFG)
    over, problems = wa.validate_overrides(over, defaults, options, FORM_HTML,
                                           optional_values={"Y87.0", "U03"})
    assert wa.fatal_problems(problems) == []
    # U03 is absent from the synthetic form and must be pruned, not fatal
    assert any(p.startswith("PRUNED") and "U03" in p for p in problems)
    assert "U03" not in over["F_D00.V2"]
    assert "Y87.0" in over["F_D00.V2"]                   # present in form -> kept


def test_unknown_parameter_and_value_are_fatal():
    defaults, options = wa.parse_form(FORM_HTML)
    over = {"B_1": ["D00.V99-bogus"], "NOT_A_PARAM": ["x"]}
    _, problems = wa.validate_overrides(over, defaults, options, FORM_HTML)
    fatal = wa.fatal_problems(problems)
    assert any("NOT_A_PARAM" in p for p in fatal)
    assert any("D00.V99-bogus" in p for p in fatal)


def test_request_xml_roundtrip():
    xml = wa.to_request_xml({"F_D00.V2": ["F10-F19", "F99"], "B_1": ["D00.V1-level1"]})
    root = ET.fromstring(xml)
    params = {p.findtext("name"): [v.text for v in p.findall("value")]
              for p in root.findall("parameter")}
    assert params == {"B_1": ["D00.V1-level1"], "F_D00.V2": ["F10-F19", "F99"]}


def test_parse_response_rowspan_markers_totals():
    parsed = wa.parse_response(RESP_XML, n_label_cols=2, n_value_cols=4)
    assert parsed.ok
    assert parsed.total_rows_skipped == 1                # "Total" row skipped
    assert len(parsed.rows) == 6
    # rowspan expansion: year label repeats on the compressed second row
    assert parsed.rows[0][:2] == ["2001", "Female"]
    assert parsed.rows[1][:2] == ["2001", "Male"]
    assert parsed.rows[1][2] == "Suppressed"
    assert parsed.rows[2][4] == "Unreliable"
    assert parsed.rows[5][3] == "Not Applicable"


def test_parse_response_shape_mismatch_fails_loudly():
    parsed = wa.parse_response(RESP_XML, n_label_cols=3, n_value_cols=4)
    assert not parsed.ok
    assert "mismatch" in parsed.message


def test_numeric_conversion():
    assert wa.numeric("1,234") == 1234.0
    assert wa.numeric("2.7") == 2.7
    assert wa.numeric("Suppressed") is None
    assert wa.numeric(" ") is None
    with pytest.raises(ValueError):
        wa.numeric("12abc")


def test_query_plan_is_the_preregistered_30():
    plan = wa.build_query_plan()
    assert len(plan) == 30
    assert [s.qid for s in plan] == [f"q{i:02d}" for i in range(1, 31)]
    d76 = [s for s in plan if s.db == "D76"]
    assert len(d76) == 15
    assert {s.series for s in plan} == {"A", "A1", "A2", "B", "Aprime", "Bprime", "ALL"}
    # age-stratified queries must not request age-adjusted rates
    assert all(not s.aar for s in plan if s.strata == "year_age")
