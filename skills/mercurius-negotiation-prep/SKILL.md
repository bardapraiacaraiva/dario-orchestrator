---
name: mercurius-negotiation-prep
description: Negotiation — BATNA, ZOPA, concession ladder, pricing power dynamics. Triggers em "negotiation", "BATNA", "ZOPA", "concession", "deal terms", "discount strategy".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-NEGOTIATION-PREP

## Frameworks
- **BATNA:** Best Alternative To Negotiated Agreement
- **ZOPA:** Zone of Possible Agreement (your floor vs their ceiling)
- **Anchor high:** start higher than target
- **Concession ladder:** plan 4-5 concessions decreasing magnitude
- **Quid pro quo:** never concede without ask back
- **Walk-away criteria:** define before, not during

## Pre-negotiation checklist
- [ ] My BATNA (next best customer this quarter?)
- [ ] Their BATNA (competitors evaluating?)
- [ ] My walk-away price
- [ ] Their walk-away (estimated)
- [ ] ZOPA mapped
- [ ] Concession ladder defined
- [ ] Trade-offs identified (term length, payment, features)
- [ ] Decision authority confirmed (mine + theirs)

## Concession tactics
- **Term length:** 12 → 24 → 36 months for discount
- **Payment terms:** net 30 → annual upfront for 10% discount
- **Volume commitment:** higher tier for committed seats
- **Reference customer:** logo + case study for discount
- **Beta features:** early access vs pricing

## Templates
1. Pre-call negotiation strategy doc
2. Concession ladder template (5 steps)
3. Discount approval matrix (level × approval needed)
4. Term sheet comparison
5. Walk-away decision criteria

## Cross-references
- [[mercurius-objection-handling]] · [[mercurius-closing]] · [[zenith-decision-intelligence]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-negotiation-prep** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-negotiation-prep:**

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
