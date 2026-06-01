---
name: demeter-data-quality
description: Data quality testing automatizado. Great Expectations, dbt tests, Soda, Monte Carlo, Anomalo. Detecta data drift, freshness, completeness, uniqueness. Triggers em "data quality", "Great Expectations", "dbt tests", "Soda", "data drift", "anomaly detection".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_by_design, pii_detection]
---

# DEMETER-DATA-QUALITY — Garbage In, Garbage Out (Stop It Here)

## Quando usar
- Bootstrap de programa de data quality
- Auditoria de pipelines existentes (que tests faltam?)
- Investigação de incidents (data foi corrompida quando?)
- Setup de alerting automatic
- Definir SLA de qualidade

## 7 dimensões de data quality
1. **Completeness:** não-nulos onde esperado
2. **Uniqueness:** duplicates detectados
3. **Validity:** formato correto (CPF, email, dates)
4. **Consistency:** referential integrity preservada
5. **Accuracy:** valores fazem sentido (idade não negativa)
6. **Freshness:** data não-stale (idade dos registos)
7. **Drift:** distribuição muda ao longo do tempo

## Templates
1. Great Expectations suite completa para pipeline ETL
2. dbt schema.yml com tests (unique, not_null, accepted_values, relationships)
3. Soda Cloud monitors para production tables
4. Anomaly detection com ML (Prophet, Isolation Forest)
5. Data quality dashboard (Soda + Grafana)

## SLA de qualidade
| Métrica | SLA típico |
|---|---|
| Freshness | 99% < 4h delay |
| Completeness | 99.5% non-null em colunas críticas |
| Uniqueness | 0 duplicados em PKs |
| Validity | 99.9% formato válido (emails, CPFs) |
| Drift | < 5% population shift sem alert |

## Compliance
- ✓ PII detection automatic (regex CPF/CNPJ/email)
- ✓ Anomalias flagged não bloqueiam pipeline mas requerem review

## Cross-references
- [[demeter-etl]] — gates pre/post load
- [[demeter-dataops]] — testing como CI gate


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-data-quality** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-data-quality:**

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
