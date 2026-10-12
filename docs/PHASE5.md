# Phase 5: Databricks, PySpark and Delta

**Status: planned, not implemented or validated.** This is an implementation brief, not an operational runbook. No runnable commands or completion claims are provided for absent infrastructure.

## Objective

Implement a cloud transformation path and compare its results with the tested local SQL baseline.

## Prerequisites

Phase 2 metric definitions and quality fixtures are the reference. Confirm the Phase 4 storage/access setup and a bounded compute budget. No Databricks workspace or Spark/Delta pipeline is implemented.

## Intended deliverables

- Implement bronze/silver/gold layers with source provenance and reviewed schemas.
- Use Delta merge semantics for replay and historical corrections; test deletion policy separately.
- Port date-spine, completeness, share and rolling-window rules without silently changing NULL handling.
- Explain that this small dataset is for learning cloud implementation, not evidence that distributed compute is needed.

## Acceptance gate

- Reconcile local and cloud row counts, keys and numeric outputs within documented tolerances.
- Exercise duplicate replay, late corrections, missing days, negatives and schema changes.
- Measure runtime and actual cost; verify idle-resource shutdown.
- Document tested runtime versions, execution, diagnostics, permissions and cleanup commands.

## Decisions still open

Workspace/runtime, compute type and limits, metastore/catalog layout, dbt integration and numeric precision policy.

Before marking this phase complete, replace this brief with the actual architecture/configuration, copyable commands and expected output, failure/recovery steps, tests, cost/security limits where relevant, and links to observed validation evidence.

Return to the [documentation index](INDEX.md) or [roadmap](ROADMAP.md).
