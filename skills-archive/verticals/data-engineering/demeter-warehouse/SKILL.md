---
name: demeter-warehouse
description: Data warehousing arquitectura e operação. BigQuery, Snowflake, Redshift, Postgres analytics. Modelagem Kimball/Inmon/Data Vault. Performance tuning, custos optimizados. Triggers em "data warehouse", "BigQuery", "Snowflake", "Redshift", "modelagem dimensional", "fact table", "dimension table", "schema design".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, retention_policies, access_control]
warehouses_supported:
  - "BigQuery (GCP) — serverless, pay-per-query"
  - "Snowflake — multi-cloud, separation compute/storage"
  - "Redshift (AWS) — node-based, RA3 instances"
  - "Postgres analytics (TimescaleDB, Citus)"
  - "DuckDB (local analytics)"
  - "ClickHouse (real-time OLAP)"
---

# DEMETER-WAREHOUSE — Data Warehouse Architecture

## Quando usar
- Escolher warehouse adequado (BigQuery vs Snowflake vs Redshift)
- Desenhar schema dimensional (star/snowflake/data vault)
- Tuning de performance (partitioning, clustering, indexes)
- Optimizar custos (slot allocation, warehouse sizing)
- Migration entre warehouses
- Storage strategies (hot/cold/archive tiers)

## Modelagem
- **Star schema (Kimball):** fact + dimensions desnormalizadas — bom para BI
- **Data Vault:** hubs + links + satellites — bom para auditability
- **One Big Table (OBT):** desnormalizado total — bom para Looker/BI moderno
- **3NF (Inmon):** normalizado — bom para data lake → warehouse

## Templates
1. Star schema completo (fact_orders + dim_customer + dim_product + dim_date)
2. Snowflake setup com roles, warehouses, RBAC
3. BigQuery cost optimization (partitioning, clustering, materialized views)
4. Redshift WLM queue configuration
5. Migration plan: Postgres → BigQuery

## Compliance
- ✓ Row-level security (RLS) por tenant
- ✓ Column-level masking para PII
- ✓ Retention policies por tabela
- ✓ Audit logging (BigQuery audit logs, Snowflake QUERY_HISTORY)

## Cross-references
- [[demeter-etl]] — pipelines que populam
- [[demeter-dbt-workflows]] — transformations
- [[demeter-metrics-layer]] — semantic layer em cima


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-warehouse** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-warehouse:**

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
