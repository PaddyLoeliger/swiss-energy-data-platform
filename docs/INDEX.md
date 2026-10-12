# Documentation index

Audited against the repository implementation on 12 October 2026. Phases 1 and 2 have operational guides; Phases 3-6 have planning briefs because their systems do not exist yet.

| Phase | Status | Guide and coverage |
|---|---|---|
| 1 - Local ingestion | Implemented, local + CI verified | [PHASE1](PHASE1.md): source, architecture, setup, all ingestion tasks, configuration, tables, persistence, recovery, tests and limits |
| 2 - SQL/dbt | Implemented, local + CI verified | [PHASE2](PHASE2.md): models/grain, formulas, completeness, commands, corrections, query plans, recovery and tests |
| 3 - Airflow | Planned only | [PHASE3](PHASE3.md): scheduling/recovery scope, prerequisites, open decisions and acceptance gate |
| 4 - Azure/Terraform | Planned only | [PHASE4](PHASE4.md): infrastructure, cost/access boundaries, prerequisites and acceptance gate |
| 5 - Databricks/Delta | Planned only | [PHASE5](PHASE5.md): cloud transformations, reconciliation, cost controls and acceptance gate |
| 6 - Delivery/portfolio | Planned only | [PHASE6](PHASE6.md): deployment, dashboard, demo and acceptance gate |

Start from [README](../README.md). Use [VALIDATION](VALIDATION.md) for dated evidence and [ROADMAP](ROADMAP.md) for sequencing. Do not interpret planned deliverables as existing capabilities.

## Command ownership

All commands are run as `.\tasks.ps1 <task>` from the repository root.

| Phase | Tasks | Notes |
|---|---|---|
| Foundation | `doctor`, `init`, `build`, `up`, `ingest`, `verify`, `test`, `down` | `build` now also builds the default analytics image; `test` runs the 15 ingestion tests |
| Analytics | `analytics`, `analytics-test`, `quality`, `explain` | `analytics-test` runs one multi-step scenario; `quality` and `explain` require an already running database |
| Future phases | None yet | Do not infer Airflow, Terraform or Databricks commands from the roadmap |

## Maintenance rule

When implementing a phase or changing a command, update its guide, this index/status, the roadmap and dated validation evidence in the same change. Record what was actually tested and link the relevant commit/CI run. Keep historical measurements dated; do not turn sample row counts or timings into promises. Pipeline test success and source-data quality are separate claims.

## Audit scope and remaining limits

The audit reconciled guides with task dispatch, Compose configuration, Python ingestion, dbt profiles/models/tests and CI. It corrected stale publication/location text, a README encoding error, unsupported PowerShell compatibility wording, missing Phase 1 configuration/schema/recovery detail and missing Phase 2 CI evidence. Local relative Markdown links and task references are checked before publication.

No executable behavior changed in this documentation audit. Pipeline/analytics results cited here are the earlier verified runs, not a newly performed live ingestion. Future-phase operational documentation remains deliberately pending implementation. A backup/restore procedure, production security design, scheduler runbook and cloud deployment runbooks do not exist yet and are not represented as complete.
