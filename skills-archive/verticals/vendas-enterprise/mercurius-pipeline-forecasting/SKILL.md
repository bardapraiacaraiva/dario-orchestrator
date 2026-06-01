---
name: mercurius-pipeline-forecasting
description: Pipeline forecasting — deal scoring, pipeline coverage, forecast accuracy, weighted vs committed. Triggers em "pipeline forecasting", "sales forecast", "deal scoring", "pipeline coverage", "weighted pipeline", "commit forecast".
license: MIT
parent_agent: mercurius-director
compliance: [audit_trail]
---

# MERCURIUS-PIPELINE-FORECASTING

## Métodos forecasting

| Método | Acurácia | Esforço |
|---|---|---|
| **Pipeline weighted** | 60-70% | Baixo |
| **Stage-based** | 70-80% | Médio |
| **Rep commit + sandbag** | 75-85% | Médio |
| **AI/ML based (Clari, Gong)** | 85-95% | Alto |
| **Custom multi-touch** | 80-90% | Médio-Alto |

## Pipeline coverage
- 3x pipeline coverage = healthy (need $3 in pipeline per $1 quota)
- 4x = comfortable
- <2x = red flag, prospecting need

## Deal scoring (MEDDIC-based)
- Metrics (quantified value)
- Economic buyer identified
- Decision criteria documented
- Decision process understood
- Identified pain (validated)
- Champion confirmed

Score 0-100 → confidence weighting

## Forecast cadence
- **Weekly:** rep self-commit
- **Bi-weekly:** manager review + adjustment
- **Monthly:** CRO/VP forecast (commit + best case)
- **Quarterly:** board forecast (high confidence only)

## Templates
1. Pipeline review template (weekly)
2. Deal scoring rubric (MEDDIC)
3. Forecast accuracy dashboard
4. Pipeline health metrics (coverage, age, slip)
5. Slippage analysis (why deals push)
6. Commit vs actual variance tracker

## Cross-references
- [[mercurius-sales-ops]] · [[zenith-sensitivity-analysis]] · [[demeter-predictive]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-pipeline-forecasting** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-pipeline-forecasting:**

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
