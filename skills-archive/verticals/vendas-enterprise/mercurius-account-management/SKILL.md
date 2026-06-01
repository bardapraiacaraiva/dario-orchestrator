---
name: mercurius-account-management
description: Strategic account management — QBR, account plans, multi-threading, expansion mapping. Triggers em "account management", "QBR", "account plan", "multi-threading", "strategic account", "key account".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-ACCOUNT-MANAGEMENT

## Quando usar
- Post-close account ownership
- Strategic account program (top 20% revenue)
- QBR (Quarterly Business Review) cadence
- Multi-threading (8+ relationships per account)
- Expansion mapping

## Account plan components
1. **Account overview** — company, key metrics, our footprint
2. **Stakeholder map** — who/role/sentiment (red-yellow-green)
3. **Current state** — what we sell, MRR, usage
4. **Future state** — total addressable wallet, expansion opportunities
5. **Action plan** — 90-day, quarterly milestones
6. **Risks** — competitive threats, sentiment risks

## QBR structure (60-90 min)
- Wins + metrics (what we delivered)
- Adoption review (usage, gaps)
- Roadmap preview (what's coming)
- Mutual planning next quarter
- Asks (references, expansion, renewal)

## Multi-threading targets
- Economic buyer + champion (minimum 2)
- Technical + business stakeholders
- Multiple departments using product
- VP/C-level relationships (especially for renewal)

## Templates
1. Account plan template (Salesforce/Notion)
2. QBR deck template (15 slides)
3. Stakeholder map (org chart + sentiment)
4. Expansion opportunity matrix
5. Account scoring (health + opportunity)
6. Risk mitigation playbook

## Cross-references
- [[mercurius-expansion-revenue]] · [[mercurius-customer-success-handoff]] · [[client-qbr]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-account-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-account-management:**

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
