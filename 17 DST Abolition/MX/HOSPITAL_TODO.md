# Hospital discharges (DGIS egresos) — TODO

Not obtained in the cloud run (see DECISIONS.md). On the Mac:
1. Download DGIS "Egresos hospitalarios" open data 2012–latest from
   http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_egresoshosp_gobmx.html (Secretaría de Salud units only; sectoral version from 2022 only).
2. Keep: admission date (INGRE), municipality of residence (ENTIDAD/MUNIC of residence), AFECPRIN (principal diagnosis), CAUSAEXT (external cause).
3. Outcomes (see ../00_shared/outcome_codes.csv): self-harm = CAUSAEXT X60–X84; psychiatric = AFECPRIN F00–F99; mood = F30–F39.
4. Build the same `daily_group_counts` / `muni_month_counts` tables and rerun the H1/H2 blocks of analysis.Rmd with `outcome %in% c("selfharm_adm", "psych_adm", "mood_adm")`.
