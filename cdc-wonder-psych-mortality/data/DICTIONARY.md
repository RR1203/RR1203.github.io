# data/ dictionary

Tidy long-format CSVs produced by `scripts/02_clean.py` from `raw/responses/*.xml`
only. No cell is ever imputed; WONDER's markers become explicit boolean flags.

## Files

| File | Grain (one row per) | Source queries |
|------|---------------------|----------------|
| `rates_year.csv` | database × series × year | all `strata="year"` queries in `raw/manifest.csv` (incl. series `ALL` = all-cause benchmark rows) |
| `rates_year_sex.csv` | database × series × year × sex | `strata="year_sex"` queries |
| `rates_year_age.csv` | database × series × year × 10-year age group | `strata="year_age"` queries |

## Columns

| Column | Type | Meaning |
|--------|------|---------|
| `db` | str | WONDER database: `D76` (1999–2020, bridged race) or `D158` (2018–latest, single race). Never combine across `db` into one series. |
| `series` | str | Case definition key from `00_protocol.md` §3: `A` (F01–F99), `A1` (F10–F19), `A2` (non-substance F codes), `B` (intentional self-harm), `Aprime`/`Bprime` (sensitivity S1 definitions), `ALL` (all causes). |
| `qid` | str | Source query id — joins to `raw/manifest.csv`, `raw/queries/<qid>.xml`, `raw/responses/<qid>.xml`. |
| `year` | int | Calendar year of death. |
| `sex` | str | WONDER sex label (`Female`/`Male`); only in `rates_year_sex.csv`. |
| `age_group` | str | WONDER ten-year age group label; only in `rates_year_age.csv`. |
| `deaths` | float/empty | Death count. Empty iff a flag below is true. |
| `population` | float/empty | Population denominator (bridged-race for D76, single-race for D158). |
| `crude_rate` | float/empty | Deaths per 100,000 population, as computed by WONDER. |
| `age_adjusted_rate` | float/empty | Deaths per 100,000, age-adjusted to the 2000 U.S. standard population, as computed by WONDER. Absent in `rates_year_age.csv` (within an age stratum the age-specific crude rate is the rate measure). |
| `<measure>_suppressed` | bool | WONDER printed `Suppressed` (count 1–9, or a rate derived from one). |
| `<measure>_unreliable` | bool | WONDER printed `Unreliable` (rate based on < 20 deaths). |
| `<measure>_not_applicable` | bool | WONDER printed `Not Applicable` (e.g., population/rates for strata without denominators). |

Flag columns exist for every measure column (`deaths`, `population`, `crude_rate`,
`age_adjusted_rate`). Exactly one of: a numeric value, or one true flag, holds per
measure cell; `scripts/03_qc.py` verifies this invariant.
