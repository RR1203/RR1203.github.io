# Raw data sources (not committed: 3.2 GB)

Re-download into these folders to rerun `analysis.Rmd`:

- `raw/fars/FARS{2017..2024}NationalCSV.zip`: https://static.nhtsa.gov/nhtsa/downloads/FARS/{year}/National/FARS{year}NationalCSV.zip, unzipped flat into `raw/fars/x/{year}/` (`unzip -j`).
- `raw/arcos/report_yr_{2017..2025}.pdf`: https://www.deadiversion.usdoj.gov/arcos/retail_drug_summary/report_yr_{year}.pdf, then `pdftotext -layout report_yr_{year}.pdf txt/{year}.txt`.
- `raw/census/SC-EST2020-ALLDATA6.csv`: https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/state/asrh/
- `raw/census/sc-est2025-alldata6.csv`: https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/state/asrh/
- `raw/other/tvt/{yy}{mon}tvt.xls(x)`: https://www.fhwa.dot.gov/policyinformation/travel_monitoring/{yy}{mon}tvt/{yy}{mon}tvt.xlsx (or .xls for older months), 2017-01 to 2025-12.
- `raw/other/cdc_vsrr_overdose.csv`: https://data.cdc.gov/api/views/xkb8-kh2a/rows.csv?accessType=DOWNLOAD
- `raw/other/fr_*.htm`: DEA Federal Register notices via https://www.govinfo.gov/content/pkg/FR-{date}/html/{doc}.htm (docs 2022-26351, 2023-22059, 2023-28962, 2024-20114, 2024-30019, 2024-30023, 2025-18110, 2025-19335, 2025-24277, 2026-22842).
- `raw/other/dailymed/`: FDA labels via https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml (Adderall XR aff45863-ffe1-4d4f-8acf-c7081512a6c0; Vyvanse 704e4378-ca83-445c-8b45-3cfa51c1ecad; Ritalin d6fb2750-cdab-4749-ba0d-7534840a5892).

Downloaded 2026-11-13.
