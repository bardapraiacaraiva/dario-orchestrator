---
name: mercurius-customer-success-handoff
description: Sales → CS handoff — kickoff call, success criteria, onboarding plan. Triggers em "CS handoff", "customer success handoff", "onboarding plan", "kickoff call", "sales to CS transition".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-CUSTOMER-SUCCESS-HANDOFF

## Princípio
**Handoff é primeira impressão pós-venda.** Bad handoff = early churn risk.

## Handoff workflow
```
1. Internal handoff (Sales → CSM)
   - Account summary (decision drivers, expectations, risks)
   - Stakeholder map + sentiment
   - Commercial terms (contract specifics)
   - Promised commitments

2. External kickoff call (Sales + CSM + Customer)
   - Reintroduce team
   - Review success criteria
   - Define onboarding milestones
   - Communication cadence agreement
   - Success metrics baseline

3. 30-60-90 day onboarding plan
   - Day 30: initial value delivered
   - Day 60: adoption metrics
   - Day 90: ROI demonstrated
```

## Success criteria (define UPFRONT)
- Time to first value
- Activation milestones
- Usage metrics targets
- Business outcome KPIs
- Stakeholder satisfaction (NPS/CSAT)

## Anti-patterns
- ❌ Sales disappears post-close
- ❌ CSM hears about deal first time at kickoff
- ❌ Promised features not documented
- ❌ Champion not introduced to CSM
- ❌ No mutual success plan signed

## Templates
1. Internal handoff doc (Sales → CSM)
2. Kickoff call agenda + script
3. Mutual Success Plan (signed)
4. 30/60/90 onboarding milestones
5. CSM playbook by segment (SMB/MM/Enterprise)
6. Adoption tracker dashboard

## Cross-references
- [[mercurius-closing]] · [[client-onboard]] · [[client-journey]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-customer-success-handoff** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-customer-success-handoff:**

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
