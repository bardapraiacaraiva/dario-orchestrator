---
name: zenith-decision-intelligence
description: Decision intelligence — decision trees, multi-criteria, decision quality (DQ), DACI/RAPID. Triggers em "decision intelligence", "decision tree", "multi-criteria", "MCDA", "DACI", "RAPID", "decision quality".
license: SEE-LICENSE
parent_agent: zenith-director
---

# ZENITH-DECISION-INTELLIGENCE

## Quando usar
- High-stakes decision (M&A, market entry)
- Recurring decision quality issues
- Multi-stakeholder decision (procurement, hiring)
- Decision under uncertainty
- Post-decision review

## Frameworks
- **Decision Trees:** branches + probabilities + payoffs (EV calc)
- **MCDA (Multi-Criteria Decision Analysis):** criteria weighted
- **DACI:** Driver/Approver/Contributors/Informed
- **RAPID (Bain):** Recommend/Agree/Perform/Input/Decide
- **Decision Quality (Strategic Decisions Group):** 6 elements
- **Pre-mortem (Klein):** assume failure, work backwards
- **Pros/Cons + WRAP (Heath):** Widen/Reality-test/Attain-distance/Prepare

## Templates
1. Decision memo template (context + options + rec + risks + ask)
2. Decision tree (qualitative + EMV calc)
3. MCDA matrix (criteria × options, weighted)
4. DACI / RAPID assignment
5. Pre-mortem workshop (1h)
6. Decision log (track quality over time)

## Princípios DQ (Strategic Decisions Group)
1. Appropriate frame
2. Creative alternatives
3. Meaningful information
4. Clear values + trade-offs
5. Sound reasoning
6. Commitment to action

## Cross-references
- [[zenith-sensitivity-analysis]] · [[zenith-monte-carlo]] · [[zenith-strategic-options]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **zenith-decision-intelligence** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in zenith-decision-intelligence:**

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
