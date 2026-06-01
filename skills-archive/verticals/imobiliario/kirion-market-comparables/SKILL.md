---
name: kirion-market-comparables
description: Comparable sales analysis (CMA), hedonic pricing, GIS-based. Triggers em "CMA", "comparable analysis", "hedonic pricing", "GIS real estate", "Imovirtual", "ZAP Imóveis", "Idealista".
license: SEE-LICENSE
parent_agent: kirion-director
---

# KIRION-MARKET-COMPARABLES

## Sources data
- **PT:** Idealista, Imovirtual, Casa Sapo, Confidencial Imobiliário, INE
- **BR:** ZAP, Vivareal, ImovelWeb, FGV-IBRE, IGV índice
- **Global:** Zillow, Redfin (US), Rightmove (UK)
- **Off-market:** broker network, transaction databases

## Hedonic pricing variables
- **Location:** lat/lng, neighbourhood, school district, transit
- **Property:** size, bedrooms, age, condition
- **Quality:** finishings, view, floor
- **Amenities:** parking, garden, pool, elevator
- **Macro:** crime, demographics, employment

## Adjustments típicas
- **Time:** appreciation since comp transaction (% per month)
- **Location:** premium/discount per neighborhood
- **Size:** $ per m² regression
- **Condition:** renovation cost adjustment
- **Features:** parking + R$ 30K, view + 5%, etc.

## Templates
1. CMA worksheet (8-12 comparables)
2. Hedonic regression model
3. Adjustment matrix (10 dimensions)
4. GIS heat map visualization
5. Confidential Imobiliário data integration
6. Time series adjustment factor

## Cross-references
- [[kirion-real-estate-valuation]] · [[kirion-dcf-property]] · [[demeter-predictive]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **kirion-market-comparables** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in kirion-market-comparables:**

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
