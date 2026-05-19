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
