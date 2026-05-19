---
name: demeter-metrics-layer
description: Metrics layer / semantic layer — Cube, dbt Semantic Layer, Transform, MetricFlow. Single source of truth para KPIs. Triggers em "metrics layer", "semantic layer", "Cube", "dbt Semantic", "MetricFlow", "single source of truth", "KPI definition".
license: MIT
parent_agent: demeter-director
compliance: [metric_governance, single_source_of_truth]
---

# DEMETER-METRICS-LAYER — Single Source of Truth para KPIs

## Problema que resolve
**"Revenue" no Looker = R$ 1M. Mesma "revenue" no Power BI = R$ 1.2M. Qual é o real?**
Metrics layer define métricas UMA VEZ. Todos os tools consomem da mesma definição.

## Quando usar
- Multi-tool BI environment (Looker + Tableau + custom apps)
- Conflitos persistentes de métricas
- Audit de definições de KPI (CFO ≠ CMO ≠ COO)
- Self-service BI com governance
- Embedded analytics

## Stack
- **Cube** (open-source, mais maduro)
- **dbt Semantic Layer** (dbt Cloud Enterprise)
- **MetricFlow** (Transform — agora dbt Labs)
- **Looker LookML** (proprietary, Looker-only)
- **Lightdash** (open-source dbt-based BI)
- **Malloy** (Google, modern language)

## Princípios
- **Definir uma vez:** Cube/dbt semantic model
- **Consumir N vezes:** API, SQL, BI tools
- **Versionar:** semver para metrics
- **Test:** cada metric tem test (current_revenue > 0)
- **Document:** dono, definição business, fonte técnica

## Templates
1. Cube data model (cubes + measures + dimensions + joins)
2. dbt Semantic Layer (semantic_models.yml + metrics.yml)
3. Metric governance RACI (DPO + Owners + Approvers)
4. Migration: ad-hoc SQL → semantic layer

## Métricas típicas a definir
```
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- NRR (Net Revenue Retention)
- LTV (Customer Lifetime Value)
- CAC (Customer Acquisition Cost)
- CAC payback period
- Churn rate (logo + revenue)
- Activation rate
- Time to value
- NPS / CSAT
- Bookings vs revenue (saas)
```

## Cross-references
- [[demeter-bi-dashboard]] — consumer do semantic layer
- [[demeter-dbt-workflows]] — semantic models em dbt
- [[demeter-data-storytelling]] — apresentação executiva
