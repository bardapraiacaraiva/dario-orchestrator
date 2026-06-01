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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-metrics-layer** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-metrics-layer:**

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
