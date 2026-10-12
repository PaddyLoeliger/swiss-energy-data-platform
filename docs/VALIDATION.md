# Validation record

This file records dated observations, not a promise of current source freshness or machine state.

## Phase 1

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

The test database was stopped after testing. The project database was left available locally at the end of that validation. Existing unrelated containers were not changed.

GitHub Actions passed for implementation commit `fe7d1ea361095ec5f3acec5e815cfb6480486775`: [verified run](https://github.com/PaddyLoeliger/swiss-energy-data-platform/actions/runs/38270109079). The workflow built the image and ran the PostgreSQL-backed test suite on GitHub. Local verification was also rerun successfully after relocating the repository to `C:\Projects\Swiss Energy Platform`.

## Phase 2

Validated on 12 October 2026. Implementation commit: `22d2153353aa7889ce9557d3357ec5fc6f1f30b5`. [Successful GitHub Actions run](https://github.com/PaddyLoeliger/swiss-energy-data-platform/actions/runs/38274342924); its success and commit were rechecked during this documentation audit.

| Check | Observed result |
|---|---|
| dbt/container versions | dbt Core 1.12.5, dbt-postgres 1.11.0, PostgreSQL 16 |
| Ingestion regression suite | 15 passed |
| Analytics integration scenario | 1 passed: three builds plus deliberate unknown-category rejection |
| Real dbt build | Five models and one seed built; 26 data tests: 24 passed, two warnings, zero errors/skips |
| Analytics rows | 4,183 daily rows, 4,183 rolling rows, 25,098 mix rows |
| Quality status | Zero incomplete days, one negative-value day, source age 120 days |
| Historical correction | Daily total 60 -> 67; affected seven-day average 60 -> 61; out-of-window average unchanged |
| Query plans | Broad sequential scan/hash aggregate; selective bitmap index/heap scan |

The 32 dbt build nodes include six model/seed nodes and 26 tests; `PASS=30` in its summary does not mean 30 data tests. The pytest scenario is one test with multiple assertions, not an additional 26 pytest tests. Detailed measurements and caveats are in [PHASE2](PHASE2.md).

## Phases 3-6

Planned only. No implementation, deployment, cost measurement or acceptance test has been performed. Their guides are planning briefs linked from [INDEX](INDEX.md).

## Documentation audit

The 12 October 2026 audit checked documentation against current source/configuration and verified the Phase 2 CI evidence. Only Markdown files changed. It did not repeat live ingestion, claim a newer data snapshot or reclassify known source warnings as passes. Relative links and task references were checked locally; the documentation commit also triggers the existing CI workflow.
