---
name: mercurius-closing
description: Closing techniques — 12 techniques + when to use each, mutual close plans, urgency creation. Triggers em "closing", "close deal", "ABC always be closing", "assumptive close", "summary close", "mutual close plan".
license: MIT
parent_agent: mercurius-director
compliance: [no_dark_patterns]
---

# MERCURIUS-CLOSING

## 12 closing techniques

| # | Technique | When |
|---|---|---|
| 1 | Assumptive | High confidence, soft buyer |
| 2 | Summary | After complex evaluation |
| 3 | Now-or-never (urgency) | End of quarter, real promo |
| 4 | Trial close | Mid-process check |
| 5 | Sharp angle | Buyer asks for concession |
| 6 | Question close | "What's stopping us?" |
| 7 | Take-away | Confident buyer hesitating |
| 8 | Hard close | Late stage, clear signals |
| 9 | Soft close | Relationship-driven |
| 10 | Empathy close | Pain validated |
| 11 | Visual close | Show vs tell |
| 12 | Doorknob close | Last resort exit |

## Mutual Close Plan (recommended)
- Joint document defining:
  - Decision date target
  - Stakeholders involved (theirs + ours)
  - Steps required (technical eval, legal, procurement)
  - Trigger events (board approval, etc.)
- Signed by champion (verbal or formal)

## Anti-patterns
- ❌ Fake urgency
- ❌ "Special discount expiring today" (when false)
- ❌ Bait-and-switch terms
- ❌ Ignoring "no" (respect autonomy)

## Templates
1. Mutual Close Plan template
2. 12 closing scripts by technique
3. Urgency creation ethical guide
4. Champion validation checklist
5. Deal momentum tracker

## Cross-references
- [[mercurius-negotiation-prep]] · [[mercurius-customer-success-handoff]] · [[orion-product-launch]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-closing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-closing:**

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
