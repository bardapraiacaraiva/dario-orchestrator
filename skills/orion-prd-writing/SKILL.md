---
name: orion-prd-writing
description: PRDs production-grade. Problem, solution, success metrics, edge cases, rollout. Triggers em "PRD", "product requirements", "spec", "feature spec", "product brief".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design]
---

# ORION-PRD-WRITING

## Quando usar
- Escrever PRD para nova feature
- Refactor PRDs legados (sem success metrics? sem edge cases?)
- Template de PRD para a empresa toda
- One-pager vs full PRD decision
- RFC technical para mudanças arquiteturais

## Estrutura PRD (production-grade)
```
1. Problem statement (the WHY)
2. Target users + JTBD
3. Success metrics (leading + lagging)
4. Solution overview
5. User stories + acceptance criteria
6. Edge cases + error states
7. Out of scope (explicit)
8. Dependencies + risks
9. Rollout plan (flag, %, segments)
10. Launch checklist
```

## Princípios
- **WHY antes de WHAT:** problem clarity > solution detail
- **Success metrics explícitas:** "ship it when X = Y"
- **Edge cases listados:** ambiguity = bugs
- **Out of scope explícito:** previne scope creep
- **Single owner:** nome do PM no top

## Templates
1. PRD full (Notion/Confluence)
2. One-pager (RFC-style)
3. Mini-PRD para experiments
4. PRD template específico para growth experiments
5. RFC técnico para arquitetura

## Cross-references
- [[orion-product-discovery]] · [[orion-prioritization]] · [[builder-prd-complete]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-prd-writing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-prd-writing:**

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
