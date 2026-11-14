# 00 Feasibility: Brazil school phone ban → youth self-harm

**FLAG: STOPPED AT STEP 0. Data access failed, not power. No data downloaded, no models run.**

## What was checked (2026-11-14, cloud container)

| Check | Result |
|---|---|
| `ftp://ftp.datasus.gov.br/dissemin/publicos/` | DNS fails (`Could not resolve host`). The container has no direct DNS, and FTP cannot pass through the HTTPS proxy. |
| `https://datasus.saude.gov.br`, `opendatasus.saude.gov.br` | Blocked by the environment's network policy (403 at proxy) |
| OpenDataSUS S3 mirror (`s3.sa-east-1.amazonaws.com/ckan.saude.gov.br`) | Host reachable, but guessed SIM/SINAN file paths return AccessDenied |
| Base dos Dados (BigQuery mirror of SIH/SIM/SINAN) | Website blocked; `bq` has no GCP credentials |
| R / CRAN | R is not installed; CRAN is blocked, so `microdatasus` / `read.dbc` can't be installed |

## Not answered (needs DATASUS access)
- Which 2025 files exist (SIH-RD, `VIOLBR25.dbc`, SIM-DO prelim) and the latest month covered
- Annual self-harm counts, ages 10–17, 2018–2025
- MDE of the age × school_day × post term

## To run it
Run the original prompt on a machine with open internet (your laptop). The FTP need alone rules out this cloud environment: even with hosts allowlisted, FTP doesn't go through the proxy.
