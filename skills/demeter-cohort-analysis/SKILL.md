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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-cohort-analysis** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-cohort-analysis:**

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
