---
name: zenith-strategic-planning
description: Strategic planning — Playing to Win, 3 Horizons, Wardley Maps, Blue Ocean. Triggers em "strategic planning", "Playing to Win", "3 Horizons", "Wardley Maps", "Blue Ocean", "strategy".
license: SEE-LICENSE
parent_agent: zenith-director
compliance: [privilege_executive, audit_immutable]
---

# ZENITH-STRATEGIC-PLANNING

## Quando usar
- Annual strategic planning cycle
- Strategy refresh pós-pivot/disruption
- New market entry decision
- Multi-business unit prioritization
- Pre-board offsite

## Frameworks
- **Playing to Win (Lafley/Martin):** WTP/HTW/CTW/MS/MM
- **Good Strategy Bad Strategy (Rumelt):** diagnosis + guiding policy + actions
- **3 Horizons (McKinsey):** core/adjacent/transformational
- **Wardley Maps (Wardley):** value chain × evolution
- **Blue Ocean (Kim/Mauborgne):** ERRC + 6 paths framework
- **OGSM:** Objectives/Goals/Strategies/Measures

## Templates
1. Strategy on a page (executive 1-pager)
2. Playing to Win cascade (5 choices)
3. Wardley Map workshop
4. 3 Horizons portfolio review
5. Blue Ocean strategy canvas
6. Strategy → OKR cascade

## Cross-references
- [[zenith-okr-design]] · [[zenith-scenario-planning]] · [[zenith-capital-allocation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-strategic-planning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-strategic-planning:**

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
