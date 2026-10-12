# Phase 3: Airflow operations

**Status: planned, not implemented or validated.** This is an implementation brief, not an operational runbook. No runnable commands or completion claims are provided for absent infrastructure.

## Objective

Make ingestion and analytics a scheduled, observable workflow with reliable recovery.

## Prerequisites

Phases 1 and 2 must pass. Resolve or explicitly accept the source freshness limitation before claiming monitoring. Select and verify an Airflow version and executor at implementation time.

## Intended deliverables

- Sequence ingestion, raw verification, dbt build and quality reporting in a DAG.
- Set bounded retries, timeouts and one active pipeline run; prevent test/production connection confusion.
- Persist success/failure audit details and define freshness alerts with an owner and destination.
- Define backfill semantics explicitly: the current source is a full snapshot and the ingestion CLI has no date-range option. Do not pretend scheduler dates filter the input.

## Acceptance gate

- Induce a download or database failure and show a successful rerun with no duplicate observations.
- Show a historical correction reaching dbt outputs after scheduled execution.
- Demonstrate concurrency limits, stale-source handling and durable failure records.
- Add the actual startup, UI/access, pause, recovery, test and cleanup commands to this guide.

## Decisions still open

Executor/resource requirements, DAG schedule/time zone, persisted metadata volumes, alert destination and whether real date-bounded backfills are required.

Before marking this phase complete, replace this brief with the actual architecture/configuration, copyable commands and expected output, failure/recovery steps, tests, cost/security limits where relevant, and links to observed validation evidence.

Return to the [documentation index](INDEX.md) or [roadmap](ROADMAP.md).
