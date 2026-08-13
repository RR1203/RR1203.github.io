# ENVIRONMENT

| Item | Value |
|------|-------|
| Run start (UTC) | 2026-08-13T05:47:17Z |
| Run end (UTC) | _(recorded at final commit)_ |
| OS | Linux 6.18.5-fc-v20 x86_64 (managed remote container) |
| Python | 3.11.15 (`/usr/local/bin/python3`), project venv in `venv/` |
| Package installs | pip from PyPI only (requests, pandas, statsmodels, scipy, matplotlib, pytest); pinned in `requirements.txt` |
| Network | Outbound HTTPS via session-managed proxy (`HTTPS_PROXY`, CA bundle `/root/.ccr/ca-bundle.crt`, exposed as `REQUESTS_CA_BUNDLE`). Contact restricted to wonder.cdc.gov, www.cdc.gov, pypi.org, files.pythonhosted.org. |
| Git | Existing repository RR1203/RR1203.github.io, branch `claude/cdc-wonder-psych-mortality-8lnoj3`; per-step commits; final tag `overnight-final` (see DECISIONS.md #1–#2) |
| Working directory | `cdc-wonder-psych-mortality/` inside the repository (see DECISIONS.md #3) |
