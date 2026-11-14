# Harvest downloaded source files into one raw workbook (03_mup_raw.xlsx).
# Values are copied unchanged; only reshaped to long format. Run with: python3 -I scripts/01_harvest_raw.py
import json, itertools, sys
from pathlib import Path
import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
OUT = ROOT / "03_mup_raw.xlsx"
sheets = {}

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

# ---- ONS alcohol-specific deaths, nations (Tables 1-5) -----------------------
wb = openpyxl.load_workbook(RAW / "ons_alcoholspecificdeaths2024.xlsx", read_only=True)
rows = []
for t in ["Table_1", "Table_2", "Table_3", "Table_4", "Table_5"]:
    for r in wb[t].iter_rows(min_row=6, values_only=True):
        if r[0] is None or not isinstance(r[2], int):
            continue
        for i, sex in enumerate(["Persons", "Males", "Females"]):
            b = 3 + 4 * i
            rows.append(dict(area_code=r[0], area=r[1], year=r[2], sex=sex, deaths=num(r[b]),
                             asmr=num(r[b + 1]), lcl=num(r[b + 2]), ucl=num(r[b + 3])))
sheets["ons_nation"] = pd.DataFrame(rows)

# ---- ONS regions of England (Table 6) ----------------------------------------
rows = []
for r in wb["Table_6"].iter_rows(min_row=6, values_only=True):
    if isinstance(r[0], int):
        rows.append(dict(year=r[0], sex=r[1], area_code=r[2], area=r[3], deaths=num(r[4]),
                         asmr=num(r[5]), lcl=num(r[6]), ucl=num(r[7])))
sheets["ons_region"] = pd.DataFrame(rows)

# ---- ONS deprivation England / Wales (Tables 11-12) --------------------------
rows = []
for t, nation in [("Table_11", "England"), ("Table_12", "Wales")]:
    for r in wb[t].iter_rows(min_row=5, values_only=True):
        if isinstance(r[0], int):
            for i, sex in enumerate(["Males", "Females"]):
                b = 2 + 4 * i
                rows.append(dict(nation=nation, year=r[0], quintile=r[1], sex=sex, deaths=num(r[b]),
                                 asmr=num(r[b + 1]), lcl=num(r[b + 2]), ucl=num(r[b + 3])))
sheets["ons_deprivation"] = pd.DataFrame(rows)

# ---- ONS UK deaths by individual cause (Table 9, all ages) -------------------
ws = wb["Table_9"]
hdr = None
rows = []
for r in ws.iter_rows(min_row=4, values_only=True):
    if r[0] == "Area code \n[note 2]" or (isinstance(r[0], str) and r[0].startswith("Area code")):
        hdr = list(r)
        continue
    if hdr and isinstance(r[2], int) and r[3] == "Persons":
        total = sum(num(v) or 0 for v in r[6:] if v is not None)
        rows.append(dict(year=r[2], icd10=r[4], cause=r[5], deaths=total))
sheets["ons_uk_cause"] = pd.DataFrame(rows)

# ---- NRS Scotland 2025 release ------------------------------------------------
wb = openpyxl.load_workbook(RAW / "nrs_alcohol_specific_deaths_2025_all_tables.xlsx", read_only=True)
rows = [dict(year=r[0], sex=r[1], deaths=num(r[2]), asmr=num(r[3]), lcl=num(r[4]), ucl=num(r[5]))
        for r in wb["Table_1"].iter_rows(min_row=7, values_only=True) if isinstance(r[0], int)]
sheets["nrs_annual"] = pd.DataFrame(rows)
rows = [dict(year=r[0], month=r[1], sex=r[2], deaths=num(r[3]), asmr=num(r[4]), lcl=num(r[5]), ucl=num(r[6]))
        for r in wb["Table_7"].iter_rows(min_row=6, values_only=True) if isinstance(r[0], int)]
sheets["nrs_monthly"] = pd.DataFrame(rows)
rows = [dict(year=r[0], quintile=r[1], quintile_label=r[2], sex=r[3], deaths=num(r[4]), asmr=num(r[5]),
             lcl=num(r[6]), ucl=num(r[7]))
        for r in wb["Table_5"].iter_rows(min_row=7, values_only=True) if isinstance(r[0], int)]
sheets["nrs_simd"] = pd.DataFrame(rows)
ws = wb["Table_8"]
allr = list(ws.iter_rows(min_row=5, values_only=True))
years = [int(y) for y in allr[0][2:] if y is not None]
rows = []
for r in allr[1:]:
    if r[0] is None:
        continue
    for y, v in zip(years, r[2:]):
        rows.append(dict(icd10=r[0], cause=r[1], year=y, deaths=num(v)))
sheets["nrs_cause"] = pd.DataFrame(rows)

# ---- NRS cancer death rates by age (Table 6.06) -------------------------------
wb = openpyxl.load_workbook(RAW / "nrs_vital_events_2024_ch6.xlsx", read_only=True)
ages = ["Under 25", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "65 to 74", "75 to 84", "85 to 89", "90 and over"]
rows = []
for r in wb["table_6.06"].iter_rows(min_row=7, values_only=True):
    if r[0] in ("C00-C97", "C15") and str(r[2]).isdigit():
        for a, v in zip(ages, r[5:14]):
            rows.append(dict(icd10=r[0], year=int(r[2]), sex=r[3], age_group=a, rate=num(v)))
sheets["nrs_cancer_age"] = pd.DataFrame(rows)

# ---- CSO PxStat JSON-stat tables ----------------------------------------------
def jsonstat(path, keep):
    d = json.load(open(path))
    ids = d["id"]
    labs = [list(d["dimension"][k]["category"]["label"].items()) for k in ids]
    out = []
    for i, combo in enumerate(itertools.product(*labs)):
        rec = {d["dimension"][k]["label"]: lab for k, (code, lab) in zip(ids, combo)}
        rec["code_" + d["dimension"][ids[3]]["label"] if len(ids) > 3 else "code"] = combo[3][0] if len(ids) > 3 else None
        rec["value"] = d["value"][i] if isinstance(d["value"], list) else d["value"].get(str(i))
        if keep(rec, combo):
            out.append(rec)
    return pd.DataFrame(out)

codes_keep = {"F10", "K70", "X45", "X65", "Y15", "80005"} | {f"C{n:02d}" for n in range(0, 98)}
for m, first, last in [("VSA35", 2007, 2018), ("VSA29", 2019, 2024)]:
    df = jsonstat(RAW / f"cso_{m}.json", lambda rec, combo: combo[3][0] in codes_keep)
    df.columns = ["statistic", "year", "sex", "cause", "age_group", "icd10", "deaths"]
    df["year"] = df["year"].astype(int)
    df["source_table"] = m
    sheets[f"cso_{m.lower()}"] = df[(df.year >= first) & (df.year <= last)]

d = json.load(open(RAW / "cso_PEA01.json"))
labs = [list(d["dimension"][k]["category"]["label"].values()) for k in d["id"]]
rows = [dict(year=int(c[1]), age_group=c[2], sex=c[3], population=d["value"][i])
        for i, c in enumerate(itertools.product(*labs)) if 2005 <= int(c[1]) <= 2026]
sheets["cso_population"] = pd.DataFrame(rows)

d = json.load(open(RAW / "cso_MORT02.json"))
labs = [list(d["dimension"][k]["category"]["label"].values()) for k in d["id"]]
rows = []
for i, c in enumerate(itertools.product(*labs)):
    if c[3] == "Ireland" and c[4] == "All ages" and c[5] in ("All causes of death", "Selected alcohol related causes",
                                                           "Alcohol abuse (including alcoholic psychosis)", "Chronic liver disease",
                                                           "Malignant neoplasms"):
        rows.append(dict(statistic=c[0], year=int(c[1]), sex=c[2], cause=c[5], value=d["value"][i]))
sheets["cso_mort02"] = pd.DataFrame(rows)

for m, name in [("ASD01", "cso_asd01_percapita"), ("ASD09", "cso_asd09_hipe")]:
    d = json.load(open(RAW / f"cso_{m}.json"))
    labs = [list(d["dimension"][k]["category"]["label"].values()) for k in d["id"]]
    rows = [dict(statistic=c[0], year=int(c[1]), group=c[2], value=d["value"][i])
            for i, c in enumerate(itertools.product(*labs))]
    sheets[name] = pd.DataFrame(rows)

# ---- ABS alcohol-induced deaths by state (Table 13.17) ------------------------
wb = openpyxl.load_workbook(RAW / "abs" / "2025_13 Drug and alcohol-induced deaths (Australia).xlsx", read_only=True)
rows, block, sex = [], None, None
yrs = list(range(2016, 2026))
for r in wb["Table 13.17"].iter_rows(min_row=5, values_only=True):
    if r[0] is None:
        continue
    s = str(r[0])
    if s.startswith("Drug-induced"):
        block = "drug"
    elif s.startswith("Alcohol-induced"):
        block = "alcohol"
    elif s in ("Males", "Females", "Persons"):
        sex = s
    elif r[1] == "no." and block == "alcohol":
        for y, v in zip(yrs, r[2:12]):
            rows.append(dict(state=s, sex=sex, year=y, deaths=num(v)))
sheets["abs_state_alcohol"] = pd.DataFrame(rows)

# ---- Fingertips (England) ------------------------------------------------------
cols = ["Indicator ID", "Indicator Name", "Area Code", "Area Name", "Area Type", "Sex", "Age", "Category Type",
        "Category", "Time period", "Value", "Lower CI 95.0 limit", "Upper CI 95.0 limit", "Count", "Denominator"]
for i, name, filt in [(92906, "ft_admissions", lambda d: d["Area Type"].isin(["England", "Regions (statistical)"])),
                      (91380, "ft_mortality_imd", lambda d: d["Area Type"].isin(["England"])),
                      (93959, "ft_cancer", lambda d: d["Area Type"].isin(["England"])),
                      (94004, "ft_oesophageal", lambda d: d["Area Type"].isin(["England"]))]:
    d = pd.read_csv(RAW / f"fingertips_{i}.csv", low_memory=False)
    d = d[filt(d)][cols]
    d = d.drop_duplicates(subset=["Area Code", "Sex", "Category Type", "Category", "Time period"])
    sheets[name] = d

# ---- PHS ARHS Scotland admissions --------------------------------------------
d = pd.read_csv(RAW / "phs_arhs_hbr.csv")
sheets["phs_arhs"] = d[(d.HBR == "S92000003") & (d.Condition == "All alcohol conditions")]

# ---- PHS MESAS 2022 sales per adult & price bands ----------------------------
wb = openpyxl.load_workbook(RAW / "phs_mesas-monitoring-report-2022-alcohol-sales.xlsx", read_only=True, data_only=True)
allr = list(wb["Data for charts"].iter_rows(min_row=1, max_row=40, values_only=True))
yrs = [int(y) for y in allr[1][3:] if isinstance(y, (int, float))]
rows = []
for idx, country in [(14, "Scotland"), (32, "England & Wales")]:
    for y, v in zip(yrs, allr[idx][3:]):
        rows.append(dict(country=country, year=y, litres_per_adult_16plus=num(v)))
sheets["mesas_sales"] = pd.DataFrame(rows)

wb = openpyxl.load_workbook(RAW / "phs_mesas-monitoring-report-2022-alcohol-price-and-affordability.xlsx", read_only=True, data_only=True)
allr = list(wb["Data for charts"].iter_rows(min_row=27, max_row=37, values_only=True))
bands = [str(b).replace("\n", "") for b in allr[0][3:18]]
rows, country = [], None
for r in allr[1:]:
    country = r[1].strip() if r[1] else country
    for b, v in zip(bands, r[3:18]):
        rows.append(dict(country=country, year=int(r[2]), price_band_ppu=b, pct_offtrade_volume=num(v)))
sheets["mesas_price_bands"] = pd.DataFrame(rows)

# ---- PHS 2026 report text values (page refs) ----------------------------------
sheets["phs2026_report_values"] = pd.DataFrame([
    dict(measure="litres pure alcohol per adult (16+), Scotland", year=2024, value=9.1, page=3),
    dict(measure="litres pure alcohol per adult (16+), Scotland", year=2025, value=8.6, page=3),
    dict(measure="litres pure alcohol per adult (16+), England & Wales (comparison year not stated in text; E&W series runs to 2024)", year=2025, value=7.8, page=3),
    dict(measure="average off-trade price per unit (p), Scotland", year=2024, value=72, page=5),
    dict(measure="average off-trade price per unit (p), Scotland", year=2025, value=78, page=5),
    dict(measure="average off-trade price per unit (p), England & Wales", year=2024, value=67, page=5),
    dict(measure="average off-trade price per unit (p), England & Wales", year=2025, value=69, page=5),
    dict(measure="% change per-adult sales 2017-2025, Scotland", year=2025, value=-18.9, page=3),
    dict(measure="% change per-adult sales 2017-2025, England & Wales", year=2025, value=-16.0, page=3),
])

with pd.ExcelWriter(OUT) as xw:
    pd.DataFrame([dict(sheet=k, rows=len(v)) for k, v in sheets.items()]).to_excel(xw, sheet_name="index", index=False)
    for k, v in sheets.items():
        v.to_excel(xw, sheet_name=k[:31], index=False)
print({k: len(v) for k, v in sheets.items()})
