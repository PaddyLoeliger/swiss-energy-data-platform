# Phase 6: Delivery and portfolio evidence

**Status: planned, not implemented or validated.** This is an implementation brief, not an operational runbook. No runnable commands or completion claims are provided for absent infrastructure.

## Objective

Make the complete project reviewable, deployable and easy to demonstrate without overstating its maturity.

## Prerequisites

Earlier phases need recorded acceptance results. Current CI already covers local Python/PostgreSQL/dbt tests; this phase extends it rather than claiming CI is absent.

## Intended deliverables

- Separate environments and add identity-based CI/CD authentication where cloud deployment exists.
- Define migration/deployment/rollback checks and an image/dependency update process.
- Add a SQL dashboard that exposes data freshness and flags alongside metrics.
- Prepare architecture decisions and a short incident/recovery demonstration backed by repository evidence.

## Acceptance gate

- A new reviewer follows the documentation to reproduce the supported demo.
- A deliberate failure and recovery are demonstrated without duplicated data or hidden quality warnings.
- Deployment and rollback are exercised for the actual selected environments.
- Portfolio claims distinguish personal project work from employment experience; costs and limitations remain visible.

## Decisions still open

Dashboard tool, deployment environments, promotion rules, rollback strategy, artifact retention and intended demo audience.

Before marking this phase complete, replace this brief with the actual architecture/configuration, copyable commands and expected output, failure/recovery steps, tests, cost/security limits where relevant, and links to observed validation evidence.

Return to the [documentation index](INDEX.md) or [roadmap](ROADMAP.md).
