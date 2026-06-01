---
name: zenith-sensitivity-analysis
description: Sensitivity analysis — tornado, spider, what-if, two-way sensitivity. Triggers em "sensitivity analysis", "tornado", "what-if analysis", "two-way sensitivity", "data table Excel".
license: SEE-LICENSE
parent_agent: zenith-director
---

# ZENITH-SENSITIVITY-ANALYSIS

## Quando usar
- Financial model robustness check
- M&A valuation (what drives NPV?)
- Capital project decision
- Pricing change impact
- Budget assumptions stress test

## Métodos
- **One-way (Tornado):** vary 1 variable, hold others. Rank by impact
- **Two-way (data table):** 2 variables, matrix output
- **Spider chart:** multiple variables at % change
- **Scenario analysis:** discrete combinations (best/base/worst)
- **Monte Carlo:** probabilistic (see zenith-monte-carlo)

## Templates
1. Tornado chart template (Excel data table + waterfall)
2. Two-way sensitivity (NPV × discount rate × growth)
3. Spider chart (multiple drivers ±20%)
4. Scenario summary table (best/base/worst)
5. Decision criteria sob incerteza (NPV mean + std)

## Princípios
- **Identify what matters:** focus em high-impact variables
- **Realistic ranges:** ±10/20/30% baseado em historical
- **Document assumptions:** cada variable + source
- **Pair com Monte Carlo:** sensitivity = qualitative; MC = probabilistic

## Cross-references
- [[zenith-monte-carlo]] · [[zenith-ma-evaluation]] · [[zenith-capital-allocation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-sensitivity-analysis** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-sensitivity-analysis:**

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
