---
name: helios-climate-pricing
description: Climate-adjusted pricing, weather derivatives, internal carbon price. Triggers em "climate pricing", "weather derivatives", "internal carbon price", "shadow carbon price", "climate hedge".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-CLIMATE-PRICING

## Internal carbon price
- **Shadow price:** internal accounting only (investment decisions)
- **Internal tax:** actual cross-charge between BUs
- **Implicit price:** efficiency improvement targets

## Climate-adjusted pricing
- **Carbon-adjusted gross margin:** subtract carbon cost
- **Climate alpha:** premium for low-carbon products
- **Green premium (Bill Gates):** cost of low-carbon vs fossil baseline

## Weather derivatives
- **HDD (Heating Degree Days):** colder = more demand
- **CDD (Cooling Degree Days):** hotter = more demand
- **Rainfall futures:** agriculture, hydro
- **CME weather contracts:** standardized hedging

## Stack
- **MSCI Climate:** climate analytics enterprise
- **S&P Global Sustainable1:** climate data
- **Trucost** (now S&P):** environmental costing
- **Speedwell:** weather derivatives

## Templates
1. Internal carbon price design ($30-150/tCO₂ range)
2. Climate-adjusted investment NPV
3. Green premium analysis (per product)
4. Weather derivative hedging strategy
5. Climate scenario pricing (1.5°C vs 3°C+)
6. Climate risk-adjusted P&L

## Cross-references
- [[gaia-climate-risk-tcfd]] · [[helios-renewable-financing]] · [[zenith-sensitivity-analysis]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **helios-climate-pricing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in helios-climate-pricing:**

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
