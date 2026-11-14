# BRAZIL arm — not run in the cloud (TODO on the Mac)

**Why stopped:** `ftp.datasus.gov.br` could not be reached from the cloud container (curl exit 6, "Could not resolve host", tried twice on 2026-11-14). Per the run prompt §0, the Brazil arm stops when FTP fails.

**What is ready to reuse**
- Novelty check covers Brazil: `../00_shared/00_novelty.md` (Q1 not studied; Q2 only via Watanabe 2026 preprint on crash timing).
- Outcome code lists: `../00_shared/outcome_codes.csv` (same ICD-10 definitions).
- Design and code: copy `../MX/analysis.Rmd` and swap the data section. Q1/Q2/power code works on any `unit × date` count table with columns `group`, `date`, `outcome`, `n`, `pop`.

**Steps on the Mac**
1. `remotes::install_github("rfsaldanha/microdatasus")`
2. SIM-DO: `fetch_datasus(year_start = 2010, year_end = <latest>, information_system = "SIM-DO")`, all UFs (DO only, not fetal deaths). Check whether preliminary years are picked up; if not, fetch them separately.
3. SIH-RD: `fetch_datasus(year_start = 2010, month_start = 1, year_end = <latest>, month_end = 12, information_system = "SIH-RD")`. Large: keep only `DT_INTER`, `MUNIC_RES`, `MUNIC_MOV`, `DIAG_PRINC`, `DIAG_SECUN`, `CID_MORTE`, `IDADE`, `SEXO`. Self-harm admissions: external cause X60–X84 is coded in `DIAG_SECUN` (S/T primary). Verify.
4. Regime map: DST states 2010–2018 = RS, SC, PR, SP, RJ, ES, MG, GO, DF, MS, MT (Tocantins only in 2012/13 season; Bahia only 2011/12 season). [Verify each season's decree before coding; log ambiguous ones.]
5. DST dates 2010–2018 seasons: from the federal decrees (Decreto 6.558/2008 and amendments; Decreto 9.242/2017; end via Decreto 9.772/2019). [Verify dates from decree text — do not copy from memory.]
6. Population: IBGE municipal estimates (`apisidra.ibge.gov.br`, table 6579).
7. Phantom dates after abolition: the first Sunday of November (2019–) per Decreto 9.242/2017 rule. [Verify.]
8. Q2 former-DST months = Nov–Feb; post = Nov 2019 onward; COVID exclusion Mar 2020–Dec 2021 (this removes most of the early post period — flag).

**Alternative if FTP keeps failing on the Mac too:** OpenDataSUS publishes SIM as CSV over HTTPS (`opendatasus.saude.gov.br`, "SIM" dataset). SIH has no full HTTPS equivalent that I verified.
