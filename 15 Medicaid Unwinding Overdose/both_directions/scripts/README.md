# Re-creating the large raw inputs (not committed)

Run from `both_directions/`:

    curl -o inputs/vsrr_xkb8-kh2a.csv "https://data.cdc.gov/api/views/xkb8-kh2a/rows.csv?accessType=DOWNLOAD"
    mkdir -p inputs/fda && (cd inputs/fda && curl -O https://www.accessdata.fda.gov/cder/ndctext.zip && curl -O https://www.accessdata.fda.gov/cder/ndc_excluded.zip)
    python3 -I scripts/02_bup_ndc_lookup.py inputs/fda inputs/bup_ndc_lookup.csv
    python3 -I scripts/01_download_sdud.py inputs/sdud_bup_raw.csv   # all years 2018-2026 (slow, ~40 min)

The original run pulled 2018-2021 in one call and 2022-2026 in parallel per-year calls, then merged them
with scripts/03_merge_sdud.py; a single full call gives the same rows. Live CMS/CDC data are revised, so
compare against inputs/CHECKSUMS.md.
