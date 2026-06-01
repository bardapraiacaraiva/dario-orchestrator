---
name: zenith-capital-allocation
description: Capital allocation — capital budgeting, portfolio decision, hurdle rates, NPV/IRR. Triggers em "capital allocation", "capital budgeting", "hurdle rate", "NPV", "IRR", "portfolio decision".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [privilege_executive, audit_immutable]
---

# ZENITH-CAPITAL-ALLOCATION

## Quando usar
- Annual budget cycle (where to deploy capital)
- Major investment decision (>R$ 1M)
- M&A vs organic vs buyback vs dividend decision
- PE/holding portfolio review
- R&D portfolio prioritization

## Frameworks
- **NPV (Net Present Value):** primary metric
- **IRR (Internal Rate of Return):** complementar
- **Payback period:** quando recupera
- **MIRR (Modified IRR):** corrige IRR assumptions
- **Real options:** quando há optionality
- **Buffett's framework:** intrinsic value, moat, management

## 5 destinos do capital
1. **Reinvest in business** (organic growth)
2. **M&A** (acquisitions)
3. **Pay down debt**
4. **Pay dividends**
5. **Share buybacks**

## Templates
1. Capital allocation framework (CEO/board memo)
2. Project NPV/IRR template (with sensitivity)
3. Portfolio review (projects ranked by NPV/$invested)
4. Hurdle rate setting (WACC + premium per risk class)
5. R&D portfolio matrix (probability × NPV)
6. Buyback vs dividend decision tree

## Princípios (Outsiders, Thorndike)
- **Best capital allocators são os melhores CEOs**
- **Compare honestly:** internal projects vs M&A vs buyback
- **Patient + decisive:** wait for fat pitches, then swing hard
- **Beware self-interested capex:** management instinct to grow

## Cross-references
- [[zenith-ma-evaluation]] · [[zenith-strategic-options]] · [[zenith-monte-carlo]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-capital-allocation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-capital-allocation:**

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
