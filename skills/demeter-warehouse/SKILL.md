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
