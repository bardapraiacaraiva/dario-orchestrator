---
name: kirion-real-estate-valuation
description: Real estate valuation — métodos comparativo, custo, renda. NBR 14.653 BR + RICS PT. Triggers em "RE valuation", "avaliação imóvel", "NBR 14653", "RICS Red Book", "cap rate", "DCF imóvel".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [audit_immutable]
---

# KIRION-REAL-ESTATE-VALUATION

## Métodos
- **Comparativo (CM):** sales comparables (residencial líder)
- **Custo (CR):** terreno + benfeitorias - depreciação (industrial)
- **Renda (R):** capitalização da renda potencial (income property)
- **Resíduo (R-RD):** desenvolvimento terreno (greenfield)
- **DCF:** flujos descontados (commercial RE)

## Normas
- **NBR 14.653 (BR):** Avaliação de Bens — partes 1-7
- **RICS Red Book (PT/Global):** Royal Institution Chartered Surveyors
- **IVS (International Valuation Standards)**
- **Lei 7.018/2010 PT:** profissão avaliador imobiliário

## Métricas
- **Cap rate:** NOI / Property value (5-12% típico)
- **GIM:** Gross Income Multiplier = Price / Annual rent
- **DCF:** WACC discount, terminal value, exit cap
- **Price per m²:** unit comparison

## Templates
1. NBR 14.653 laudo template
2. RICS Red Book report
3. Comparable analysis matrix (CMA)
4. DCF model commercial RE
5. Cap rate benchmarking by sub-market
6. Sensitivity analysis (rents, vacancy, exit cap)

## Cross-references
- [[kirion-dcf-property]] · [[kirion-market-comparables]] · [[kirion-reit-analysis]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-real-estate-valuation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-real-estate-valuation:**

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
