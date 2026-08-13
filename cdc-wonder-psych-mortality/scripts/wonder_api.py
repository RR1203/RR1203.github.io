"""CDC WONDER API machinery: query specs, form parsing, request XML, response parsing.

Design constraints (per protocol and operating contract):
  - Parameter names and picklist codes must be enumerated from the saved query-form
    HTML (references/sources/{DB}-form.html), not guessed: build_request_params()
    starts from the form's own default parameter set and applies per-query overrides;
    validate_overrides() then hard-fails with a named list of problems if any
    override key or picklist value is absent from the saved form. No query is posted
    unless validation passes.
  - Responses are XML; parse_response() understands the documented data-table format
    (label cells with rowspan compression, value cells, "Suppressed"/"Unreliable"/
    "Not Applicable" markers) and reports failure loudly rather than guessing.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

# --------------------------------------------------------------------------- #
# Study series (ICD-10 code selections, exactly as pre-registered in 00_protocol.md)
# --------------------------------------------------------------------------- #

F_CHAPTER_BLOCKS = ["F01-F09", "F10-F19", "F20-F29", "F30-F39", "F40-F48",
                    "F50-F59", "F60-F69", "F70-F79", "F80-F89", "F90-F98", "F99"]

SERIES: dict[str, dict] = {
    "A":  {"label": "All mental and behavioural disorders (F01-F99)",
           "icd": ["F01-F99"]},
    "A1": {"label": "Substance-induced mental and behavioural disorders (F10-F19)",
           "icd": ["F10-F19"]},
    "A2": {"label": "Non-substance mental and behavioural disorders (F01-F09, F20-F99)",
           "icd": [b for b in F_CHAPTER_BLOCKS if b != "F10-F19"]},
    "Aprime": {"label": "Sensitivity: F10-F99 (excl. organic F01-F09)",
               "icd": [b for b in F_CHAPTER_BLOCKS if b != "F01-F09"]},
    "B":  {"label": "Intentional self-harm (X60-X84, Y87.0, U03 if selectable)",
           "icd": ["X60-X84", "Y87.0", "U03"],
           "optional_icd": ["Y87.0", "U03"]},   # dropped with a logged warning if absent from picklist
    "Bprime": {"label": "Sensitivity: intentional self-harm X60-X84 only",
               "icd": ["X60-X84"]},
    "ALL": {"label": "All causes of death", "icd": None},
}

DB_CONFIG: dict[str, dict] = {
    "D76": {
        "url": "https://wonder.cdc.gov/controller/datarequest/D76",
        "entry_url": "https://wonder.cdc.gov/ucd-icd10.html",
        "years": (1999, 2020),
        "year_groupby": "D76.V1-level1",
        "sex_groupby": "D76.V7",
        "age_groupby": "D76.V5",
        "icd_var": "D76.V2",
        "age_var": "D76.V5",
        "prefix": "D76",
        "label": "Underlying Cause of Death, 1999-2020 (bridged race)",
    },
    "D158": {
        "url": "https://wonder.cdc.gov/controller/datarequest/D158",
        "entry_url": "https://wonder.cdc.gov/ucd-icd10-expanded.html",
        "years": (2018, None),  # through latest final year served; observed from data
        "year_groupby": "D158.V1-level1",
        "sex_groupby": "D158.V7",
        "age_groupby": "D158.V5",
        "icd_var": "D158.V2",
        "age_var": "D158.V5",
        "prefix": "D158",
        "label": "Underlying Cause of Death, 2018-latest, Single Race",
    },
}

STRATA_GROUPBYS = {  # strata key -> which group-by slots are used
    "year": ("year_groupby",),
    "year_sex": ("year_groupby", "sex_groupby"),
    "year_age": ("year_groupby", "age_groupby"),
}


@dataclass
class QuerySpec:
    qid: str
    db: str
    series: str
    strata: str          # "year" | "year_sex" | "year_age"
    aar: bool            # request age-adjusted rates
    purpose: str

    @property
    def n_groupby(self) -> int:
        return len(STRATA_GROUPBYS[self.strata])

    @property
    def n_measures(self) -> int:
        return 4 if self.aar else 3  # deaths, population, crude rate [, age-adjusted rate]


def build_query_plan() -> list[QuerySpec]:
    """The full pre-registered query plan (00_protocol.md §9)."""
    plan: list[QuerySpec] = []
    i = 1
    for db in ("D76", "D158"):
        for series in ("A", "A1", "A2", "B"):
            for strata, aar in (("year", True), ("year_sex", True), ("year_age", False)):
                plan.append(QuerySpec(f"q{i:02d}", db, series, strata, aar,
                                      f"{series} {strata} ({'AAR' if aar else 'age-specific'})"))
                i += 1
        for series in ("Aprime", "Bprime"):
            plan.append(QuerySpec(f"q{i:02d}", db, series, "year", True,
                                  f"sensitivity S1 series {series} annual totals"))
            i += 1
        plan.append(QuerySpec(f"q{i:02d}", db, "ALL", "year", True,
                              "all-cause annual totals (QC benchmark + denominators)"))
        i += 1
    return plan


# --------------------------------------------------------------------------- #
# Query-form HTML parsing (enumerates authoritative parameter names + picklists)
# --------------------------------------------------------------------------- #

class _FormParser(HTMLParser):
    """Collects form controls: defaults per parameter name, and per-select option values."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.defaults: dict[str, list[str]] = {}
        self.options: dict[str, list[str]] = {}
        self._select: str | None = None
        self._select_had_selected = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "input":
            name, itype = a.get("name"), (a.get("type") or "text").lower()
            if not name:
                return
            value = a.get("value", "")
            if itype in ("hidden", "text"):
                self.defaults.setdefault(name, []).append(value)
            elif itype in ("radio", "checkbox") and "checked" in a:
                self.defaults.setdefault(name, []).append(value)
        elif tag == "select":
            self._select = a.get("name")
            self._select_had_selected = False
            if self._select:
                self.options.setdefault(self._select, [])
        elif tag == "option" and self._select:
            value = a.get("value", "")
            self.options[self._select].append(value)
            if "selected" in a:
                self.defaults.setdefault(self._select, []).append(value)
                self._select_had_selected = True

    def handle_endtag(self, tag):
        if tag == "select" and self._select:
            if not self._select_had_selected and self.options.get(self._select):
                # browsers submit the first option of a single-select if none is marked
                self.defaults.setdefault(self._select, []).append(self.options[self._select][0])
            self._select = None


def parse_form(html_text: str) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Return (defaults, options) maps from a saved WONDER query-form HTML page."""
    p = _FormParser()
    p.feed(html_text)
    return p.defaults, p.options


# Control parameters that are part of the documented POST protocol rather than
# visible form fields; allowed as overrides even if absent from the parsed form.
PROTOCOL_PARAMS = {"accept_datause_restrictions", "stage", "action-Send", "saved_id"}


def build_overrides(spec: QuerySpec, cfg: dict) -> dict[str, list[str]]:
    gbs = [cfg[slot] for slot in STRATA_GROUPBYS[spec.strata]]
    over: dict[str, list[str]] = {}
    for i in range(1, 6):
        over[f"B_{i}"] = [gbs[i - 1]] if i <= len(gbs) else ["*None*"]
    p = cfg["prefix"]
    over["M_1"] = [f"{p}.M1"]   # Deaths
    over["M_2"] = [f"{p}.M2"]   # Population
    over["M_3"] = [f"{p}.M3"]   # Crude rate
    over["O_ucd"] = [cfg["icd_var"]]
    over["O_age"] = [cfg["age_var"]]
    over["O_rate_per"] = ["100000"]
    over["O_precision"] = ["1"]
    over["O_show_totals"] = ["false"]
    over["O_show_zeros"] = ["true"]
    over["O_timeout"] = ["300"]
    over["O_aar"] = ["aar_std" if spec.aar else "aar_none"]
    over["O_aar_pop"] = ["0000"]  # 2000 U.S. standard population
    icd = SERIES[spec.series]["icd"]
    fkey, ikey = f"F_{cfg['icd_var']}", f"I_{cfg['icd_var']}"
    if icd is None:
        over[fkey] = ["*All*"]
        over[ikey] = ["*All* (All Causes of Death)"]
    else:
        over[fkey] = list(icd)
        over[ikey] = list(icd)
        over[f"finder-stage-{cfg['icd_var']}"] = ["codeset"]
    over["accept_datause_restrictions"] = ["true"]
    over["stage"] = ["request"]
    over["action-Send"] = ["Send"]
    return over


def validate_overrides(over: dict[str, list[str]], defaults: dict[str, list[str]],
                       options: dict[str, list[str]], form_html: str,
                       optional_values: set[str] = frozenset()) -> tuple[dict[str, list[str]], list[str]]:
    """Check overrides against the authoritative saved form. Returns (possibly
    pruned overrides, problems). Values listed in optional_values are pruned with
    a problem note prefixed 'PRUNED' instead of failing the query."""
    problems: list[str] = []
    pruned = {k: list(v) for k, v in over.items()}
    known_names = set(defaults) | set(options) | PROTOCOL_PARAMS

    def code_in_form(code: str) -> bool:
        # boundary-aware: "F99" must not validate merely because "F01-F99" appears
        return re.search(rf"(?<![A-Za-z0-9.\-]){re.escape(code)}(?![A-Za-z0-9.\-])",
                         form_html) is not None
    for name, values in over.items():
        if name.startswith("finder-stage-"):
            # documented finder control: finder-stage-<variable>; valid iff the
            # variable itself is a form parameter (as F_<variable>)
            var = name.removeprefix("finder-stage-")
            if f"F_{var}" not in known_names:
                problems.append(f"finder control {name!r} has no matching F_{var} in saved form")
            continue
        if name not in known_names:
            problems.append(f"parameter name {name!r} not present in saved form")
            continue
        opts = options.get(name)
        for v in values:
            if v in PROTOCOL_SAFE_VALUES:
                continue
            if opts is not None:
                # select control: the value must be a listed <option>
                if v in opts:
                    continue
            elif name.startswith("F_"):
                # finder codes (e.g. ICD-10 picklist) are carried in the form's
                # javascript picklist data, not <option> elements: require the
                # exact code to appear (delimited) in the saved form HTML
                if code_in_form(v):
                    continue
            else:
                continue  # free-text/hidden non-finder parameter: override accepted
            if v in optional_values:
                pruned[name] = [x for x in pruned[name] if x != v]
                problems.append(f"PRUNED optional value {v!r} for {name} (absent from saved form)")
            else:
                problems.append(f"value {v!r} for {name} not found in saved form")
    # keep the informational I_ parameter in lockstep with its pruned F_ finder,
    # so a pruned code is never posted anywhere in the request
    for name in list(pruned):
        if name.startswith("F_"):
            ikey = "I_" + name[2:]
            if ikey in pruned:
                pruned[ikey] = [v for v in pruned[ikey]
                                if v in pruned[name] or v not in over.get(name, [])]
    return pruned, problems


def fatal_problems(problems: list[str]) -> list[str]:
    return [p for p in problems if not p.startswith("PRUNED")]


PROTOCOL_SAFE_VALUES = {"true", "request", "Send", "*None*", "*All*", "codeset",
                        "aar_std", "aar_none", "0000", "100000", "1", "false", "300"}


def merged_params(defaults: dict[str, list[str]], over: dict[str, list[str]]) -> dict[str, list[str]]:
    """Form defaults overlaid with per-query overrides; drops stray action buttons."""
    merged = {k: list(v) for k, v in defaults.items()
              if not (k.startswith("action-") and k != "action-Send")}
    merged.update({k: list(v) for k, v in over.items()})
    return merged


def to_request_xml(params: dict[str, list[str]]) -> str:
    root = ET.Element("request-parameters")
    for name in sorted(params):
        p = ET.SubElement(root, "parameter")
        ET.SubElement(p, "name").text = name
        for v in params[name]:
            ET.SubElement(p, "value").text = v
    return ET.tostring(root, encoding="unicode")


# --------------------------------------------------------------------------- #
# Response parsing
# --------------------------------------------------------------------------- #

MARKERS = {"Suppressed", "Unreliable", "Not Applicable"}


@dataclass
class ParsedResponse:
    ok: bool
    rows: list[list[str]] = field(default_factory=list)
    n_label_cols: int = 0
    message: str = ""
    total_rows_skipped: int = 0


def parse_response(xml_bytes: bytes, n_label_cols: int, n_value_cols: int) -> ParsedResponse:
    """Parse a WONDER XML response's data-table into fully expanded rows.

    Label cells carry attribute 'l' (with optional rowspan 'r'); value cells carry
    'v'. Rowspan compression is expanded so every returned row has exactly
    n_label_cols labels followed by n_value_cols values.
    """
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        return ParsedResponse(False, message=f"XML parse error: {exc}")

    messages = [" ".join(m.itertext()).strip() for m in root.iter("message")]
    table = next(iter(root.iter("data-table")), None)
    if table is None:
        return ParsedResponse(False, message="no <data-table> in response; messages: "
                              + " | ".join(messages[:5]))

    carry: list[tuple[str, int] | None] = [None] * n_label_cols
    rows: list[list[str]] = []
    skipped_totals = 0
    for r in table.iter("r"):
        cells = list(r.iter("c"))
        labels: list[str] = []
        ci = 0
        for col in range(n_label_cols):
            if carry[col] and carry[col][1] > 0:
                labels.append(carry[col][0])
                carry[col] = (carry[col][0], carry[col][1] - 1)
            else:
                if ci >= len(cells):
                    break
                cell = cells[ci]
                ci += 1
                lab = cell.get("l", cell.get("v", (cell.text or "")))
                labels.append(lab)
                span = int(cell.get("r", "1"))
                if span > 1:
                    carry[col] = (lab, span - 1)
        values = []
        for cell in cells[ci:]:
            values.append(cell.get("v", cell.get("l", (cell.text or ""))))
        if any(lab.strip().lower() == "total" for lab in labels):
            skipped_totals += 1
            continue
        if len(labels) == n_label_cols and len(values) == n_value_cols:
            rows.append(labels + values)
        elif len(labels) == n_label_cols and len(values) == n_value_cols + 1:
            # some WONDER exports append a trailing percent-of-total column
            rows.append(labels + values[:n_value_cols])
        elif cells:
            return ParsedResponse(False, message=(
                f"row shape mismatch: {len(labels)} labels / {len(values)} values, "
                f"expected {n_label_cols}/{n_value_cols}; first cells: "
                + ", ".join(ET.tostring(c, encoding='unicode')[:60] for c in cells[:4])))
    if not rows:
        return ParsedResponse(False, message="data-table parsed but yielded 0 rows; messages: "
                              + " | ".join(messages[:5]))
    return ParsedResponse(True, rows=rows, n_label_cols=n_label_cols,
                          total_rows_skipped=skipped_totals)


def numeric(cell: str) -> float | None:
    """Convert a WONDER value cell to float; None for markers/blank. Raises on junk."""
    s = cell.strip()
    if not s or s in MARKERS:
        return None
    s = s.replace(",", "")
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        return float(s)
    raise ValueError(f"unexpected non-numeric cell {cell!r}")
