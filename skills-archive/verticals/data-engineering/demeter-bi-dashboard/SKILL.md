---
name: demeter-bi-dashboard
description: BI dashboards profissionais — Looker, Metabase, Power BI, Grafana, Superset, Tableau. Design para decisores. KPIs accionáveis, sem vanity metrics. Triggers em "dashboard", "BI", "Looker", "Metabase", "Power BI", "Grafana", "KPI", "visualização de dados".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, access_control_per_role]
tools_supported:
  - "Looker / Looker Studio (Google)"
  - "Metabase (open-source)"
  - "Power BI (Microsoft)"
  - "Grafana (real-time + observability)"
  - "Apache Superset (open-source enterprise)"
  - "Tableau"
---

# DEMETER-BI-DASHBOARD — Dashboards que Geram Decisões

## Filosofia
**Vanity metrics morrem aqui.** Cada dashboard responde a uma pergunta de negócio e leva a uma ação.

## Quando usar
- Design de novo dashboard executive/operational
- Audit de dashboards existentes (qual é decisão? qual é acção?)
- Migração entre ferramentas BI
- Performance optimization (query time)
- Self-service BI strategy

## Princípios de design
- **5 metrics rule:** dashboard executive tem ≤ 5 metrics primárias
- **Comparable:** sempre vs período anterior, vs target, vs benchmark
- **Action-oriented:** cada gráfico responde "e agora?"
- **Single source of truth:** todas metrics vêm do metrics layer
- **Mobile-first:** executives veem no telemóvel

## Templates
1. Executive dashboard (5 KPIs + período anterior + target)
2. Operational dashboard (real-time, SLA, alerts)
3. Funnel/conversion dashboard (CRO)
4. Cohort retention dashboard
5. Financial P&L dashboard (com drill-down)

## Tipos de visualizações por cenário
- **Trend over time:** line chart (NUNCA bar para tempo contínuo)
- **Comparação categorias:** bar horizontal (NÃO vertical >5 cat)
- **Composição:** stacked bar (NÃO pie chart >5 fatias)
- **Distribuição:** histogram + boxplot (NÃO bar para distribuição)
- **Correlação:** scatter + regression line
- **Geográfico:** choropleth map (NÃO bubble se densidade matter)

## Compliance
- ✓ Row-level security por role/dept
- ✓ PII mascarada por default (CPF → ***.***.***-XX)
- ✓ Export logging (quem exportou que dashboard quando)

## Cross-references
- [[demeter-metrics-layer]] — fonte de truth
- [[demeter-data-storytelling]] — para apresentações
- [[demeter-cohort-analysis]] — embed cohort widgets


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-bi-dashboard** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-bi-dashboard:**

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
