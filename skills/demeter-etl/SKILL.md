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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-etl** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-etl:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
