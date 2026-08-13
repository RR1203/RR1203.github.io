"""Shared HTTP client for CDC WONDER with rate limiting, timeouts and backoff.

Network contract for this project:
  - Only wonder.cdc.gov and www.cdc.gov may be contacted by this module.
  - >= 3 seconds between any two requests (module-global, enforced here).
  - Every request has a timeout; failures retry with exponential backoff.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import logging
import os
import time
from pathlib import Path

import requests

ALLOWED_HOSTS = {"wonder.cdc.gov", "www.cdc.gov"}
MIN_INTERVAL_S = 3.0
TIMEOUT_S = 120
BACKOFF_S = [5, 15, 45, 120]  # in-script retries; the fetch driver adds longer cycles

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"

_last_request_time = 0.0
_session = requests.Session()
_session.headers.update(
    {"User-Agent": "cdc-wonder-psych-mortality-research/1.0 (autonomous overnight run; contact: repository owner)"}
)


def make_logger(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(LOG_DIR / f"{name}_{ts}.log")
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        logger.addHandler(sh)
    return logger


def _throttle() -> None:
    global _last_request_time
    wait = MIN_INTERVAL_S - (time.time() - _last_request_time)
    if wait > 0:
        time.sleep(wait)
    _last_request_time = time.time()


def _check_host(url: str) -> None:
    host = url.split("/")[2]
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"host {host!r} is outside the allowed set {sorted(ALLOWED_HOSTS)}")


def request(method: str, url: str, logger: logging.Logger, *, data=None, max_tries: int = len(BACKOFF_S) + 1) -> requests.Response:
    """One rate-limited request with backoff. Raises after max_tries failures."""
    _check_host(url)
    last_exc: Exception | None = None
    for attempt in range(max_tries):
        _throttle()
        try:
            resp = _session.request(method, url, data=data, timeout=TIMEOUT_S)
            logger.info("%s %s -> HTTP %s (%d bytes)", method, url, resp.status_code, len(resp.content))
            if resp.status_code == 200:
                return resp
            last_exc = RuntimeError(f"HTTP {resp.status_code} for {url}: {resp.text[:500]!r}")
        except requests.RequestException as exc:
            logger.warning("%s %s attempt %d failed: %s", method, url, attempt + 1, exc)
            last_exc = exc
        if attempt < max_tries - 1:
            time.sleep(BACKOFF_S[min(attempt, len(BACKOFF_S) - 1)])
    raise RuntimeError(f"request failed after {max_tries} tries: {url}") from last_exc


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
