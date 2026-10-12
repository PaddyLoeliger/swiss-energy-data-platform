# Incremental roadmap

Each phase must leave a demonstrable working system. Avoid adding a tool solely to list it on a CV.

1. **Local foundation (completed):** real SFOE ingestion, PostgreSQL, Docker, tests, CI definition, raw provenance and repeatable commands. Exit: successful real load and replay, SQL verification, all unit/integration tests passed. Local end-to-end and remote CI checks passed; see validation record.
2. **SQL/dbt analytics (local validation complete):** staging models, daily generation mix, rolling aggregates and documented source completeness rules. Add dbt uniqueness/not-null/relationship tests and late-correction scenarios. Exit: reproducible models plus explained query plans.
3. **Airflow operations:** schedule the existing ingestion entry point, bounded retries, concurrency control, backfills, durable failed-run audit and freshness alerts. Exit: demonstrate recovery from a failed run without duplicates.
4. **Azure storage and Terraform:** budget alerts first; provision a minimal ADLS layout and identity-based access. Keep cloud infrastructure optional and document teardown. Exit: raw snapshots replayable from storage with no embedded credentials.
5. **Databricks/PySpark and Delta:** move validated data into bronze/silver/gold layers, demonstrate merge semantics and schema evolution. This small dataset does not require Spark for scale; explain that the purpose is cloud implementation practice. Exit: local/cloud reconciliation tests and cost evidence.
6. **Delivery and portfolio evidence:** environment-specific CI/CD, OIDC, image/dependency updates, SQL dashboard, architecture decisions and an incident/recovery walkthrough. Exit: a reviewer can reproduce the demo, understand trade-offs and distinguish personal project skills from employment experience.

Later Phase 1 hardening: database migrations, image digest locks, persisted failure audit, bounded raw retention, deletion reconciliation and richer completeness checks. Kafka and Kubernetes are not justified by this batch workload.
