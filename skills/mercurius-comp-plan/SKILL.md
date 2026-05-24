---
name: mercurius-comp-plan
description: Comp plan design — base/variable/SPIFs/accelerators/clawbacks. Triggers em "comp plan", "compensation plan sales", "OTE", "SPIF", "accelerators", "clawback".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-COMP-PLAN

## Components
- **Base salary:** 50-60% OTE (Total Earnings)
- **Variable (commission):** 40-50% OTE
- **OTE (On-Target Earnings):** total at quota
- **Accelerators:** higher % above quota
- **Decelerators:** lower % below threshold
- **SPIFs:** Special Performance Incentive Funds (one-off)
- **Clawback:** reversal if cancellation

## Comp ratios típicos
- **SDR:** 70/30 (base/variable), OTE $60-80k
- **AE inside:** 50/50, OTE $100-150k
- **AE field enterprise:** 50/50, OTE $200-300k+
- **AM (Account Manager):** 70/30, OTE $120-180k
- **Sales Manager:** 70/30, OTE $200-280k
- **VP Sales:** 60/40, OTE $300-500k

## Quota multipliers (accelerators)
- 0-80%: 50% commission rate
- 80-100%: 100% rate
- 100-150%: 150% rate
- 150%+: 200% rate (encourage overachievement)

## Anti-patterns
- ❌ Complexity > 1 page (reps need to calculate own check)
- ❌ Capping commissions (kills motivation)
- ❌ Misaligned incentives (e.g., MRR without retention)
- ❌ Changing mid-year (trust killer)

## Templates
1. Comp plan 1-pager per role
2. Commission calculator (Excel)
3. Plan launch document + FAQ
4. Quarterly comp review framework
5. Clawback policy + exceptions
6. SPIF design rubric (when/how/budget)

## Cross-references
- [[mercurius-territory-design]] · [[mercurius-pipeline-forecasting]] · [[zenith-capital-allocation]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-comp-plan** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-comp-plan:**

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
