---
name: mercurius-territory-design
description: Territory design — carving (geo/vertical/account), quotas, equity. Triggers em "territory design", "sales territory", "quota assignment", "territory carving", "patch design".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-TERRITORY-DESIGN

## Carving dimensions
- **Geographic:** country, region, state (good for field sales)
- **Vertical:** healthcare, fintech, retail (deep expertise)
- **Account size:** SMB, mid-market, enterprise
- **Named accounts:** strategic accounts (top 100)
- **Product line:** legal sales vs healthcare sales
- **Hybrid:** combo of above

## Principles
- **Equity:** similar opportunity per rep
- **Balance:** mix of new + named + expansion
- **Specialization:** vertical or product expertise
- **Manageable scope:** 50-200 accounts max per AE
- **No overlap:** clear rules of engagement

## TAM mapping per territory
- Total accounts in TAM
- ICP-fit accounts
- Engaged accounts (last 12 months)
- Active opportunities
- Booked customers
- Expansion potential

## Quota setting
- Bottom-up: territory TAM × win rate × ACV
- Top-down: company target / # reps
- Adjustment for tenure, ramp, leverage

## Templates
1. Territory carve workshop (4h facilitation)
2. Quota model (top-down + bottom-up reconcile)
3. Account assignment rubric
4. Rules of engagement doc
5. Territory health scorecard
6. Annual territory review framework

## Cross-references
- [[mercurius-comp-plan]] · [[mercurius-sales-ops]] · [[demeter-cohort-analysis]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-territory-design** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-territory-design:**

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
