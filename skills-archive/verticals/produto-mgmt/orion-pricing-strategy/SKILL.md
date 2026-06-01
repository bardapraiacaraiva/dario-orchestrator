---
name: orion-pricing-strategy
description: Pricing strategy — tiering, packaging, value metric, price localization, willingness-to-pay. Triggers em "pricing", "tiering", "packaging", "value metric", "willingness to pay", "Van Westendorp".
license: MIT
parent_agent: orion-director
compliance: [pricing_transparency, no_dark_patterns]
---

# ORION-PRICING-STRATEGY

## Quando usar
- Pricing inicial (greenfield SaaS)
- Pricing review (anual, ou pós-PMF)
- Add new tier (Enterprise tier criação)
- Value metric change (per-seat → usage-based)
- Geographic pricing (USD vs BRL vs EUR)

## Frameworks
- **Value-based pricing:** price = % of value created
- **Van Westendorp Price Sensitivity:** 4 questions, mapping price corridor
- **Conjoint analysis:** quantifica trade-offs feature vs price
- **JTBD-aligned pricing:** price = function of job importance
- **Patrick Campbell (ProfitWell):** willingness to pay surveys

## Tiering patterns
- **Good/Better/Best:** clássico, 3 tiers
- **Free + Paid + Enterprise:** freemium PLG
- **Usage-based:** per request/storage/seat
- **Hybrid:** base + usage overages
- **Land + expand:** low entry + expansion revenue

## Templates
1. Van Westendorp survey + analysis
2. Pricing page comparison (vs competitors)
3. Tier definition matrix (features × tiers)
4. Value metric workshop guide
5. Pricing change comm + grandfathering plan
6. Localized pricing matrix (USD/EUR/BRL/INR)

## Cross-references
- [[orion-product-strategy]] · [[dario-pricing-calculator]] · [[a360-oferta]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-pricing-strategy** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-pricing-strategy:**

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
