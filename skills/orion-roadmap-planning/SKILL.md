---
name: orion-roadmap-planning
description: Roadmaps modernos — Now/Next/Later, outcome-based, no Gantt fiction. Triggers em "roadmap", "product roadmap", "now next later", "quarterly planning".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design]
---

# ORION-ROADMAP-PLANNING

## Filosofia
**Roadmaps são compromissos com outcomes, não com features+dates.** Datas em features não-shippadas são ficção; commit-se a outcomes mensuráveis.

## Quando usar
- Greenfield roadmap (greenfield product)
- Refactor de roadmaps "feature factory" → outcome-based
- Multi-team coordination (dependencies)
- Communicate roadmap to stakeholders (board, sales, customers)
- Re-planning pós-pivot

## Frameworks
- **Now/Next/Later (ProdPad):** sem datas, com confidence levels
- **GIST (Itamar Gilad):** Goals/Ideas/Steps/Tasks
- **OKR-aligned roadmap:** outcomes como swim lanes
- **Theme-based:** themes > features
- **Opportunity-based:** opportunities + bets

## Templates
1. Now/Next/Later roadmap (Notion/Productboard)
2. Quarterly roadmap com confidence + dependencies
3. Theme-based annual roadmap
4. Public-facing customer roadmap (sanitized)
5. Roadmap communication deck (sales, support)

## Cross-references
- [[orion-product-strategy]] · [[orion-prioritization]] · [[orion-prd-writing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-roadmap-planning** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-roadmap-planning:**

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
