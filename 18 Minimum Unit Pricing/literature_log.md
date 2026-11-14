# Literature search log: MUP novelty and verification

All searches were run on **2026-11-14**. "Hits" is the database total count. For WebSearch, which returns no count, it is the number of results returned.

## PubMed

| # | Interface | Query | Hits |
|---|---|---|---|
| 1 | PubMed MCP | `Wyper minimum unit pricing alcohol deaths hospitalisations Scotland` | 1 |
| 2 | PubMed MCP | `minimum unit pricing Wales` | 66 |
| 3 | PubMed MCP | `minimum unit pricing Ireland alcohol` | 11 |
| 4 | PubMed MCP | `"floor price" alcohol "Northern Territory"` | 4 |
| 5 | E-utilities | `(minimum unit pric*[tiab] OR minimum pric*[tiab]) AND Wales[tiab] AND (death*[tiab] OR mortality[tiab] OR hospital*[tiab] OR admission*[tiab])` | 4 |
| 6 | E-utilities | `(minimum unit pric*[tiab] OR minimum pric*[tiab]) AND Ireland[tiab] AND (death*[tiab] OR mortality[tiab] OR hospital*[tiab] OR admission*[tiab])` | 4 |
| 7 | E-utilities | `(minimum unit pric*[tiab] OR minimum pric*[tiab]) AND Ireland[tiab] AND (purchas*[tiab] OR sales[tiab] OR household*[tiab])` | 4 |
| 8 | E-utilities | `(minimum unit pric*[tiab]) AND Scotland[tiab] AND (65p[tiab] OR 65 pence[tiab] OR uprat*[tiab] OR increase*[tiab]) AND 2024:2026[dp]` | 8 |
| 9 | E-utilities | `(minimum unit pric*[tiab] OR floor price[tiab] OR minimum pric*[tiab]) AND Northern Territory[tiab]` | 20 |
| 10 | E-utilities | `minimum unit pric*[tiab] AND alcohol AND 2025:2026[dp]` | 32 |
| 11 | E-utilities | `Robinson M[au] AND minimum unit pricing[tiab] AND sales[tiab] AND Scotland` | 3 |

## Europe PMC REST

| # | Query | Hits |
|---|---|---|
| 12 | `("minimum unit price" OR "minimum unit pricing" OR "minimum pricing") AND Wales AND (deaths OR mortality OR hospital OR admissions)` | 167 |
| 13 | `("minimum unit price" OR "minimum unit pricing") AND Ireland AND (purchas* OR sales OR Kantar OR Worldpanel)` | 119 |
| 14 | `("minimum unit price" OR "minimum unit pricing") AND Ireland AND (deaths OR mortality OR "hospital" OR admissions)` | 130 |
| 15 | `("minimum unit price" OR "minimum unit pricing") AND Scotland AND ("65p" OR "65 pence" OR "£0.65" OR uprating OR uprated)` | 38 |
| 16 | `("minimum unit price" OR "floor price") AND "Northern Territory" AND (deaths OR mortality OR hospitalisations OR admissions)` | 28 |
| 17 | `("minimum unit price" OR "minimum unit pricing" OR "minimum pricing" OR "floor price") AND alcohol AND (SRC:PPR) AND (PUB_YEAR:[2022 TO 2026])` (preprints) | 15 |

I screened the top 25 results of each query by title.

## OpenAlex (`/works?search=`, filter from_publication_date:2022-01-01)

| # | Query | Hits |
|---|---|---|
| 18 | `minimum unit pricing alcohol Wales deaths hospital admissions` | 375 |
| 19 | `minimum unit pricing Ireland alcohol purchases evaluation` | 1562 |
| 20 | `minimum unit pricing Ireland alcohol harms hospital deaths` | 818 |
| 21 | `Scotland minimum unit price 65p increase evaluation` | 8 |
| 22 | `Northern Territory minimum unit price alcohol deaths` | 1519 |

I screened the top 15 results of each query by title (relevance-ranked).

## Web search (grey literature)

| # | Query | Results returned |
|---|---|---|
| 23 | `Public Health (Alcohol) Act 2018 section 11 minimum price commencement order 4 January 2022 €1 10 grams` | 18 |
| 24 | `Ireland minimum unit pricing evaluation alcohol purchases Kantar Worldpanel impact study 2024 2025` | 10 |
| 25 | `"minimum unit pricing" Ireland impact evaluation "Public Health Alcohol Research Group" OR O'Dwyer alcohol sales after MUP 2022` | 10 |
| 26 | `gov.wales minimum pricing for alcohol evaluation final report 2025` | 19 |
| 27 | `Wales minimum pricing alcohol evaluation retailers quantitative analysis Kantar purchases ... below 50p` (extended) | 9 |
| 28 | `Public Health Scotland "Evaluating the impact of minimum unit pricing for alcohol in Scotland: A synthesis of the evidence" June 2023 final report` | 10 |
| 29 | `Public Health Scotland 65p minimum unit price impact alcohol sales MESAS 2025 2026 after increase September 2024` | 10 |
| 30 | `Northern Territory minimum unit price alcohol repealed 1 March 2025 ... floor price commenced 1 October 2018 $1.30` | 19 |
| 31 | `Northern Ireland minimum unit pricing alcohol Department of Health consultation 2026 legislation update` | 19 |
| 32 | `England minimum unit pricing alcohol government position 2026` | 19 |

## Official sources and site searches

| # | Source | Query / URL | Result |
|---|---|---|---|
| 33 | legislation.gov.uk feed | title=`Minimum Price per Unit` | 3 (SSI 2018/135, 2020/81, 2024/128) |
| 34 | legislation.gov.uk feed | title=`Minimum Unit Price for Alcohol` | 5 (adds WSI 2019/1472, 2026/34) |
| 35 | legislation.gov.uk feed | title=`Minimum Price for Alcohol` | 11 (adds anaw/2018/5, WSI 2026/30, SSI 2024/127, etc.) |
| 36 | legislation.gov.uk | made texts of SSI 2018/135, 2020/81, 2024/128; WSI 2019/1472, 2026/30, 2026/34; revised WSI 2019/1472 reg.2 | retrieved |
| 37 | hrb.ie site search | `minimum unit pricing` | HRB news/blog pages; no MUP impact evaluation |
| 38 | publichealthscotland.scot site search | `minimum unit pricing 65p`; `MESAS monitoring report 2026` | 3 news items and the dashboard release of 30 Jun 2026; no 65p evaluation |
| 39 | publichealthscotland.scot | MUP final report PDF and "at a glance" PDF | retrieved |

## Sources that failed (each tried twice, or blocked by the proxy)

- **gov.wales / www.gov.wales**: curl returned 403 (CloudFront); WebFetch could not resolve the host. The Welsh final evaluation PDFs were not read.
- **irishstatutebook.ie**, **oireachtas.ie**, **drugsandalcohol.ie**: proxy 403.
- **gov.ie**: host could not be resolved.
- **legislation.nt.gov.au**, **nt.gov.au**, **alcoholreform.nt.gov.au**: proxy refused.
- **research.senedd.wales**, **laiddocuments.senedd.wales**: proxy 403.
- **health-ni.gov.uk**, **derrynow.com**: proxy 403 or no content.
- **publichealthscotland.scot**: two guessed URLs gave 404. The correct page was found through search.
