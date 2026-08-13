#!/usr/bin/env bash
# One digest over every regenerable artifact (data/, analysis/, outputs/).
# Two runs of `run_all.sh --skip-fetch` from the same raw/ must print the same digest.
cd "$(dirname "$0")/.."
find data analysis outputs -type f 2>/dev/null | LC_ALL=C sort | xargs -r sha256sum | sha256sum | cut -d' ' -f1
