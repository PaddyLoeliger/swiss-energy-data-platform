# Phase 4: Azure storage and Terraform

**Status: planned, not implemented or validated.** This is an implementation brief, not an operational runbook. No runnable commands or completion claims are provided for absent infrastructure.

## Objective

Add an optional cloud raw-data layer provisioned with reviewable infrastructure code.

## Prerequisites

A working local pipeline, an explicitly selected Azure subscription/region and agreed spend limit are required. No Azure resources or Terraform configuration exist yet.

## Intended deliverables

- Define a minimal ADLS layout that retains original snapshots and SHA256 provenance.
- Provision storage and identity permissions with Terraform; isolate state and do not commit credentials or state files.
- Add cost visibility and alerts before workloads; document that alerts do not enforce a hard spending cap.
- Keep local operation available and document resource teardown and data-retention choices.

## Acceptance gate

- Review the Terraform plan, provision only the agreed resources and verify least-privilege access.
- Upload and retrieve a snapshot, verify its digest and demonstrate controlled replay.
- Demonstrate a clean deployment from documented configuration without embedded secrets.
- Record observed costs, deployment outputs, state recovery and verified teardown instructions.

## Decisions still open

Subscription, region, budget, naming, identity/authentication approach, remote-state location and retained data after teardown.

Before marking this phase complete, replace this brief with the actual architecture/configuration, copyable commands and expected output, failure/recovery steps, tests, cost/security limits where relevant, and links to observed validation evidence.

Return to the [documentation index](INDEX.md) or [roadmap](ROADMAP.md).
