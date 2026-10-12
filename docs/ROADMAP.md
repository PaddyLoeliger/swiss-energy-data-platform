# Incremental roadmap

Each phase must leave a demonstrable working system. Add tools to meet an engineering or learning objective, not solely to list them on a CV.

| Phase | Status | Exit gate |
|---|---|---|
| [1 - Local foundation](PHASE1.md) | Complete for defined local scope | Live ingestion and replay, SQL verification, 15 tests and remote CI passed |
| [2 - SQL/dbt analytics](PHASE2.md) | Complete for defined local scope | Models and quality rules verified, historical corrections tested, actual plans explained, remote CI passed |
| [3 - Airflow operations](PHASE3.md) | Planned | Scheduled execution, concurrency limits, durable failure audit and demonstrated recovery |
| [4 - Azure storage/Terraform](PHASE4.md) | Planned | Reviewed provisioning, identity access, replayable snapshots, cost evidence and teardown |
| [5 - Databricks/PySpark/Delta](PHASE5.md) | Planned | Local/cloud reconciliation, corrections/schema tests and compute-cost evidence |
| [6 - Delivery/portfolio](PHASE6.md) | Planned | Reproducible demo, tested deployment/rollback, visible data quality and credible portfolio claims |

[Validation evidence](VALIDATION.md) supports completed-phase status. Planned-phase guides contain prerequisites, deliverables, open decisions and acceptance checks; executable runbooks will be written alongside implementation.

Before claiming current energy monitoring, resolve the stale-source limitation or explicitly constrain the use case to historical analysis. Before production use, address migrations, backups and tested restore, least-privilege database roles, image/transitive-dependency locks, failure audit, retention, deletion reconciliation and concurrent execution. Existing dbt builds are not atomic across the entire graph.

Kafka and Kubernetes are not justified by the present batch workload. The next implementation phase is Airflow, subject to the choices in its planning brief.
