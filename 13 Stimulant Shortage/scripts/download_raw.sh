#!/usr/bin/env bash
# Re-download the large raw files that are not committed (run from the project folder).
set -euo pipefail
mkdir -p raw/fars/x raw/arcos

# NHTSA FARS national CSV, 2017-2024
for y in 2017 2018 2019 2020 2021 2022 2023 2024; do
  curl -sS -o raw/fars/FARS${y}NationalCSV.zip \
    https://static.nhtsa.gov/nhtsa/downloads/FARS/$y/National/FARS${y}NationalCSV.zip
  unzip -o -q raw/fars/FARS${y}NationalCSV.zip -d raw/fars/x/$y
done

# DEA ARCOS Retail Drug Summary (annual PDFs, Report 2 is parsed by parse_arcos.py)
for y in 2017 2018 2019 2020 2021 2022 2023 2024 2025; do
  curl -sS -o raw/arcos/report_yr_$y.pdf \
    https://www.deadiversion.usdoj.gov/arcos/retail_drug_summary/report_yr_$y.pdf
done

# Rebuild the parsed ARCOS CSV (needs poppler-utils)
mkdir -p /tmp/arcos_txt
for y in 2017 2018 2019 2020 2021 2022 2023 2024 2025; do
  pdftotext -layout raw/arcos/report_yr_$y.pdf /tmp/arcos_txt/$y.txt
done
python3 -I scripts/parse_arcos.py /tmp/arcos_txt raw/arcos/arcos_report2_parsed.csv

# Other sources (already committed in raw/):
#  Census:  www2.census.gov/programs-surveys/popest/datasets/{2010-2020,2020-2025}/state/asrh/
#  FHWA:    www.fhwa.dot.gov/policyinformation/statistics/<year>/xls/vm2.xls(x)
#  FRED:    fred.stlouisfed.org/graph/fredgraph.csv?id=<ST>UR
#  FR/GPO:  www.govinfo.gov/content/pkg/FR-<date>/html/<doc>.htm
#  CDC:     data.cdc.gov views fpsi-y8tj, xkb8-kh2a, 489q-934x
#  WHO DDD: atcddd.fhi.no/atc_ddd_index/?code=N06BA01|02|04|11|12
#  Cannabis: en.wikipedia.org/wiki/Legalization_of_non-medical_cannabis_in_the_United_States
