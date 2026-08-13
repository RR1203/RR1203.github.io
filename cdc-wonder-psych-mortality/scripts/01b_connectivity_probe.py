"""Step 1b: scheduled connectivity probes to CDC hosts per the contract's backoff plan.

The session's egress proxy answered 403 (policy denial) to CONNECT for both
wonder.cdc.gov and www.cdc.gov at run start. The operating contract prescribes retry
cycles at 1, 5, 15, 30, 60 minutes before declaring Degraded Mode. Each cycle sends
one lightweight GET per host (>=3 s apart, 30 s timeout). Probes that are rejected by
the local proxy never reach CDC servers at all.

Exit codes: 0 = a probe succeeded (CDC reachable); 3 = all cycles exhausted.
State is appended to logs/ as JSON lines for evidence.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG = PROJECT_ROOT / "logs" / "connectivity_probe.jsonl"

PROBE_URLS = [
    "https://wonder.cdc.gov/wonder/help/WONDER-API.html",
    "https://www.cdc.gov/nchs/index.htm",
]
# Contract schedule: retries at 1, 5, 15, 30, 60 minutes (+1 extra 60-min cycle ≈ 6 cycles).
DELAYS_S = [0, 60, 300, 900, 1800, 3600, 3600]


def probe(url: str) -> tuple[bool, str]:
    try:
        r = requests.get(url, timeout=30)
        return (r.status_code == 200, f"HTTP {r.status_code}")
    except requests.RequestException as exc:
        return (False, f"{type(exc).__name__}: {str(exc)[:300]}")


def main() -> int:
    LOG.parent.mkdir(exist_ok=True)
    for cycle, delay in enumerate(DELAYS_S):
        if delay:
            time.sleep(delay)
        for url in PROBE_URLS:
            ok, detail = probe(url)
            rec = {
                "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "cycle": cycle,
                "url": url,
                "ok": ok,
                "detail": detail,
            }
            with LOG.open("a") as fh:
                fh.write(json.dumps(rec) + "\n")
            print(json.dumps(rec), flush=True)
            if ok:
                print("REACHABLE", flush=True)
                return 0
            time.sleep(3)
    print("EXHAUSTED", flush=True)
    return 3


if __name__ == "__main__":
    sys.exit(main())
