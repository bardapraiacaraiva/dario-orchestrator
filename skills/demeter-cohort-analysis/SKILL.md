---
name: demeter-cohort-analysis
description: Cohort analysis — retention curves, LTV cohorts, funnel analysis, behavioral segmentation. Mostra padrões que medias escondem. Triggers em "cohort", "retention", "LTV", "funnel", "churn cohort", "user segmentation", "behavioral analysis", "Mixpanel", "Amplitude".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, pii_aggregation]
---

# DEMETER-COHORT-ANALYSIS — Padrões Por Trás das Médias

## Filosofia
**Medias mentem.** ARR cresce mas qual cohort está a sustentar? Conversion sobe mas é canal X ou Y? Cohort analysis quebra "all users" em grupos coerentes.

## Quando usar
- Análise de retention (D1, D7, D30, M12)
- LTV por cohort de acquisition
- Funnel analysis por segmento
- Behavioral segmentation (RFM, K-Means)
- Diagnóstico de churn (qual cohort está a sair)

## Tipos de cohort
- **Acquisition cohort:** users por mês de signup
- **Behavioral cohort:** users que fizeram acção X
- **Demographic cohort:** users por país/idade/segmento
- **Time-based cohort:** users com 0-30, 31-90, 91+ dias

## Métricas chave
- **Retention curve:** % users active em D1/7/30 por cohort
- **Cohort LTV:** Σ revenue até day N por cohort
- **Funnel conversion:** % que avança em cada step
- **Churn cohort:** quando cohort X começou a churn-ar

## Templates
1. SQL cohort retention (date_trunc + window functions)
2. Mixpanel/Amplitude cohort setup
3. LTV cohort dashboard (Looker/Metabase)
4. Funnel analysis com drop-off por step
5. RFM segmentation (Recency, Frequency, Monetary)
6. K-Means behavioral segmentation

## Insights típicos
- "Cohort de Out/2025 retém 40% em D30. Cohort de Jan/2026 retém só 22%. O que mudou?"
- "Channel X traz users com LTV 3x maior do que channel Y, mas custa 5x. CAC pay-back > 12 meses."
- "Segmento power-user gera 80% revenue mas é 5% users. Estratégia: protect them."

## Cross-references
- [[demeter-predictive]] — churn prediction baseado em cohort
- [[demeter-ab-testing]] — segmentation em experiments
- [[demeter-bi-dashboard]] — visualização cohort
