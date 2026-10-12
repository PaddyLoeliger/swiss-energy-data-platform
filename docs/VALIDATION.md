# Validation record

Local validation performed on 12 October 2026 on Windows (reported NT build 26300).

| Check | Observed result |
|---|---|
| Git | 2.52.0.windows.1 |
| VS Code | 1.139.1 |
| Docker server | 20.10.21, Linux containers |
| Compose | v2.13.0 |
| GitHub CLI | 2.101.0, authenticated |
| Host Python | No standalone installation confirmed; Docker supplies Python 3.12 |
| Container build | Passed |
| pytest including real PostgreSQL integration | 15 passed, no skips |
| Live ingestion | 25,098 rows, six carriers |
| Live replay | Same checksum and 25,098 observations; second audit run created |
| SQL verification | 4,183 rows per carrier; latest run count reconciled |
| Local secret | Random .env password; .env confirmed ignored by Git |

Source range: 2015-01-01 through 2026-06-14. Source SHA256:
`7f7afbab454a644eb3462cecfb104bbd657f9abcf38d2ac833bf5b5c8a2e2b73`.

The first live attempt correctly failed the original non-negative check. Inspection found one reported value of -1.5 GWh for Speicherkraft on 2026-06-14. The final implementation preserves this value and flags it for review; it does not assert whether it is a source error or a valid net measure. Validation also reports source age: 120 days on the check date. This alternate endpoint is suitable for demonstrating historical ingestion, not current monitoring without further source investigation.

The test database was stopped after testing. The project database remains available locally. Existing unrelated containers were not changed.

GitHub Actions passed for implementation commit `fe7d1ea361095ec5f3acec5e815cfb6480486775`: [verified run](https://github.com/PaddyLoeliger/swiss-energy-data-platform/actions/runs/38270109079). The workflow built the image and ran the PostgreSQL-backed test suite on GitHub. Local verification was also rerun successfully after relocating the repository to `C:\Projects\Swiss Energy Platform`.
