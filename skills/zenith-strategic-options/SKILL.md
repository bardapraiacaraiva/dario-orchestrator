---
name: zenith-strategic-options
description: Real options — strategic optionality, defer/expand/abandon/switch, ROV. Triggers em "real options", "strategic options", "optionality", "Black-Scholes strategy", "ROV", "real option valuation".
license: SEE-LICENSE
parent_agent: zenith-director
---

# ZENITH-STRATEGIC-OPTIONS

## Filosofia
**Strategy is creating + exercising options.** Não fica preso a 1 caminho; mantém optionality.

## Tipos
- **Option to defer:** wait + see
- **Option to expand:** scale up se sucesso
- **Option to abandon:** kill switch
- **Option to switch:** change tech/market/business
- **Option to learn:** invest pequeno para aprender

## Frameworks
- **Real Options Valuation (ROV):** Black-Scholes adaptation
- **Strategic Options Navigator (Trigeorgis):** sequential decisions
- **Discovery-Driven Planning (McGrath):** assumption-driven
- **Lean Startup (Ries):** build-measure-learn loops
- **Stage-Gate (Cooper):** R&D phased

## Templates
1. Option matrix (current + future options preserved)
2. Stage-gate template (R&D, M&A)
3. Real options valuation (Black-Scholes inputs)
4. Discovery-Driven Planning (assumptions + tests)
5. Decision tree with options (branches são options)

## Princípios
- **Pay para keep options:** small investment → big optionality
- **Time decay:** options expiram (urgency)
- **Volatility = value:** mais incerto → options vale mais
- **Don't fall in love:** kill switch real
- **Pair com sensitivity:** robust nas múltiplas paths

## Cross-references
- [[zenith-scenario-planning]] · [[zenith-decision-intelligence]] · [[zenith-capital-allocation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-strategic-options** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-strategic-options:**

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
