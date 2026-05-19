---
name: demeter-etl
description: ETL/ELT pipelines profissionais. Airflow, Prefect, Dagster, dbt orchestration. Ingestão de fontes heterogéneas, transformações idempotentes, deploy production-grade. Triggers em "ETL", "pipeline", "Airflow", "Prefect", "Dagster", "ingestão de dados", "data pipeline", "DAG".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, pii_detection, data_lineage]
stack_focus:
  - "Airflow 2.7+ (DAGs como Python)"
  - "Prefect 2.x (modern orchestration)"
  - "Dagster (asset-oriented)"
  - "dbt Cloud / dbt Core (transformations)"
  - "Singer/Meltano (ingestion)"
  - "Fivetran/Stitch (managed connectors)"
---

# DEMETER-ETL — Pipelines de Dados Production-Grade

Skill para desenhar, implementar e operar pipelines ETL/ELT robustos.

## Quando usar
- Desenhar arquitectura de pipeline (greenfield)
- Migrar pipeline legado para orquestrador moderno
- Diagnosticar falhas em DAGs existentes
- Implementar idempotency, backfill, retry strategies
- Validar performance + custo de pipelines
- Definir SLA + observabilidade

## Workflow
```
1. Source mapping (origens + frequência + schema)
2. Quality gates (Great Expectations / dbt tests pre-load)
3. Transformation logic (T em ELT, vs SQL puro)
4. Idempotency design (upsert/merge, not append)
5. Backfill strategy (historical reprocessing)
6. Monitoring (SLAs, alertas, lineage)
7. Cost optimization (warehouse credits, compute hours)
```

## Princípios chave aplicados
- **Idempotency:** mesmo input + mesma run = mesmo output (sem duplicados)
- **Atomicity:** transações garantem all-or-nothing
- **Determinism:** sem `now()` em transformations (usar `execution_date`)
- **Lineage:** cada tabela sabe de onde veio e quem consome
- **Cost-aware:** dimensionado por uso real (não over-provisioned)

## Compliance built-in
- ✓ **LGPD by design:** PII detectada e mascarada em staging
- ✓ **Data lineage:** todas transformações registadas (OpenLineage compatible)
- ✓ **Retention policies:** TTL por tabela conforme contrato
- ✓ **Audit:** quem acessou que dado, quando

## Templates incluídos
1. Airflow DAG production-grade (idempotent, retries, SLA, alerting)
2. dbt project skeleton (sources + staging + marts + tests)
3. Prefect flow com error handling completo
4. Backfill playbook (parameter sweep)
5. Migration plan: cron → Airflow

## Cross-references
- [[demeter-warehouse]] — destino dos pipelines
- [[demeter-data-quality]] — gates pré e pós-load
- [[demeter-dataops]] — CI/CD para pipelines
- [[demeter-dbt-workflows]] — transformations SQL-native
