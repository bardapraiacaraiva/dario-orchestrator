---
name: mercurius-sales-enablement
description: Sales enablement — battle cards, competitive intel, sales collateral, onboarding curriculum. Triggers em "sales enablement", "battle cards", "competitive intel sales", "sales collateral", "playbook sales".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-SALES-ENABLEMENT

## Quando usar
- Sales team scaling (10 → 50+ reps)
- New product launch enablement
- Competitive battle cards
- Onboarding rep curriculum (30/60/90)
- Pitch deck standardization

## Battle card structure
1. **Competitor overview** — pricing, target, recent moves
2. **Our advantages** — 3-5 differentiators
3. **Their advantages** — be honest
4. **Common objections** — vs this competitor
5. **Trap-setting questions** — to expose competitor weakness
6. **Proof points** — wins vs this competitor

## Onboarding 30/60/90 plan
- **Week 1-2:** product training + persona deep dive
- **Week 3-4:** shadow calls + demo certification
- **Day 30:** first deal in pipeline
- **Day 60:** first close + ramping
- **Day 90:** full quota carrying

## Stack
- **Highspot, Seismic** — enterprise sales content
- **Showpad** — sales enablement platform
- **Gong, Chorus** — call recording + intel
- **MindTickle** — sales onboarding + readiness
- **Notion, Confluence** — knowledge base (cheaper)

## Templates
1. Battle card template (per top 5 competitors)
2. Onboarding curriculum (30/60/90 days)
3. Pitch deck library (intro, demo, ROI, executive)
4. Sales talking points by persona
5. Competitive trap questions
6. Content audit framework (what's used vs ignored)

## Cross-references
- [[mercurius-sales-methodology]] · [[zenith-competitive-intelligence]] · [[mercurius-discovery-call]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-sales-enablement** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-sales-enablement:**

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
