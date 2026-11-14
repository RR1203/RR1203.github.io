# Harvest cause-specific alcohol deaths (K70, F10, X45, X65, Y15) by age and populations by age
# into 03_mup_raw_cause.xlsx. Values copied unchanged; reshaped to long format only.
# Run with: python3 -I scripts/03_harvest_cause.py
from pathlib import Path
import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
OUT = ROOT / "03_mup_raw_cause.xlsx"
CODES = ["F10", "K70", "X45", "X65", "Y15"]
AGES = ["<1", "01-04", "05-09", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49",
        "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"]
rows = []

# ONS 'deaths by individual cause' 2001-2021: England (Table 2), Scotland (Table 4), persons by age
wb = openpyxl.load_workbook(RAW / "ons_deathsbyindividualcause_2022.xlsx", read_only=True)
for table, area in [("Table 2", "England"), ("Table 4", "Scotland")]:
    for r in wb[table].iter_rows(min_row=6, values_only=True):
        if isinstance(r[0], int) and r[1] == "Persons" and r[2] in CODES:
            for a, v in zip(AGES, r[4:24]):
                rows.append(dict(area=area, year=r[0], icd10=r[2], age_group=a, deaths=v, source="ONS individual cause 2022"))

# ONS adhoc 11797: North East (Table 1), North West (Table 2), 2001-2018, persons by age (year forward-filled)
wb = openpyxl.load_workbook(RAW / "ons_adhoc11797_regions_cause.xlsx", read_only=True)
for table, area in [("Table 1", "North East"), ("Table 2", "North West")]:
    year = None
    for r in wb[table].iter_rows(min_row=14, values_only=True):
        if isinstance(r[0], int):
            year = r[0]
        if year and r[1] in CODES:
            for a, v in zip(AGES, r[3:23]):
                rows.append(dict(area=area, year=year, icd10=r[1], age_group=a, deaths=v, source="ONS adhoc 11797"))

# Nomis NM_161_1: England, North East, North West 2013-2024, deaths by age
nomis_age = {"Aged under 1": "<1", "Aged 1 to 4": "01-04", "Aged 5 to 9": "05-09", "Aged 10-14": "10-14",
             "Aged 15-19": "15-19", "Aged 20-24": "20-24", "Aged 25-29": "25-29", "Aged 30-34": "30-34",
             "Aged 35-39": "35-39", "Aged 40-44": "40-44", "Aged 45-49": "45-49", "Aged 50-54": "50-54",
             "Aged 55-59": "55-59", "Aged 60-64": "60-64", "Aged 65-69": "65-69", "Aged 70-74": "70-74",
             "Aged 75-79": "75-79", "Aged 80-84": "80-84", "Aged 85-89": "85-89", "Aged 90 and over": "90+"}
d = pd.read_csv(RAW / "nomis" / "nomis_nm161_alcohol_causes.csv")
d = d[(d.MEASURE_NAME == "Deaths") & d.AGE_NAME.isin(nomis_age.keys())]
for _, r in d.iterrows():
    rows.append(dict(area=r.GEOGRAPHY_NAME, year=int(r.DATE_NAME), icd10=r.CAUSE_OF_DEATH_NAME[:3],
                     age_group=nomis_age[r.AGE_NAME], deaths=r.OBS_VALUE, source="Nomis NM_161_1"))
nomis_asmr = pd.read_csv(RAW / "nomis" / "nomis_nm161_alcohol_causes.csv")
nomis_asmr = nomis_asmr[(nomis_asmr.MEASURE_NAME == "Age-standardised mortality rate") &
                        (nomis_asmr.AGE_NAME == "total (all ages)")]
nomis_asmr = pd.DataFrame(dict(area=nomis_asmr.GEOGRAPHY_NAME, year=nomis_asmr.DATE_NAME.astype(int),
                               icd10=nomis_asmr.CAUSE_OF_DEATH_NAME.str[:3], asmr_published=nomis_asmr.OBS_VALUE))

# NRS vital events table 6.04: Scotland 2023 and 2024, persons by age (Y15 row absent = 0 deaths)
vert_age_cols = AGES
for f, sheet, year, persons in [("nrs_vert_2023_all.xlsx", "6.04", 2023, (None, ("M", "F"))),
                                ("nrs_vital_events_2024_ch6.xlsx", "table_6.04", 2024, (None, ("Males", "Females")))]:
    wb = openpyxl.load_workbook(RAW / f, read_only=True)
    acc = {}
    for r in wb[sheet].iter_rows(min_row=4, values_only=True):
        code = str(r[2])[:3] if r[2] else None
        if code not in CODES:
            continue
        if persons[0] and r[3] == persons[0]:
            acc[code] = [v or 0 for v in r[5:25]]
        if persons[1] and r[3] in persons[1]:
            prev = acc.get(code, [0] * 20)
            acc[code] = [p + (v or 0) for p, v in zip(prev, r[5:25])]
    for code in CODES:
        vals = acc.get(code, [0] * 20)
        for a, v in zip(AGES, vals):
            rows.append(dict(area="Scotland", year=year, icd10=code, age_group=a, deaths=v, source=f"NRS VERT {year} 6.04"))

deaths_age = pd.DataFrame(rows)
deaths_age["deaths"] = deaths_age["deaths"].fillna(0)

# NRS alcohol-specific deaths 2025, Table 8: Scotland counts by cause 2000-2025 (all ages)
nrs_t8 = pd.read_excel(ROOT / "03_mup_raw.xlsx", sheet_name="nrs_cause")
nrs_t8 = nrs_t8[nrs_t8.icd10.isin(CODES)][["icd10", "year", "deaths"]].assign(area="Scotland", source="NRS 2025 Table 8")

# Nomis NM_31_1 populations by 5-year age (85+ top band), 2007-2024
p = pd.read_csv(RAW / "nomis" / "nomis_nm31_population.csv")
pop = pd.DataFrame(dict(area=p.GEOGRAPHY_NAME, year=p.DATE_NAME.astype(int), age_label=p.AGE_NAME, population=p.OBS_VALUE))

with pd.ExcelWriter(OUT) as xw:
    deaths_age.to_excel(xw, sheet_name="deaths_cause_age", index=False)
    nrs_t8.to_excel(xw, sheet_name="nrs_cause_total", index=False)
    nomis_asmr.to_excel(xw, sheet_name="nomis_asmr_published", index=False)
    pop.to_excel(xw, sheet_name="population_age", index=False)
print(deaths_age.groupby(["area", "source"]).year.agg(["min", "max", "count"]))
print(len(nrs_t8), len(nomis_asmr), len(pop))
