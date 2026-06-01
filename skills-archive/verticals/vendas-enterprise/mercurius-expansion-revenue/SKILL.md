---
name: mercurius-expansion-revenue
description: Expansion revenue — upsell, cross-sell, land-and-expand, NRR optimization. Triggers em "expansion revenue", "upsell", "cross-sell", "NRR", "net revenue retention", "land and expand".
license: MIT
parent_agent: mercurius-director
---

# MERCURIUS-EXPANSION-REVENUE

## Princípio
**NRR > 110% = top quartile SaaS.** Expansion 1.4-1.5x more efficient than new logo (Pacific Crest survey).

## Expansion playbook
- **Upsell:** same product, higher tier (seats, usage, premium features)
- **Cross-sell:** different product (DARIO LEX → DARIO MEDIK)
- **Land-and-expand:** start small, grow within org
- **Geographic expansion:** subsidiaries, regions

## Trigger events para expansion
- Usage hitting tier limits
- New hires in champion's team
- New funding round
- Leadership change (positive)
- Product roadmap delivery
- QBR action items completion

## NRR formula
```
NRR = (Starting MRR + Expansion - Churn - Downgrade) / Starting MRR × 100
```
- 100% = flat
- 110%+ = healthy
- 120%+ = top tier
- 130%+ = elite (Snowflake-tier)

## Templates
1. Upsell trigger playbook (10 triggers)
2. Cross-sell decision matrix (which product to which segment)
3. Land-and-expand 12-month plan
4. NRR calculation + cohort analysis
5. Expansion compensation design (% commission)
6. In-product upsell prompts (PLG)

## Cross-references
- [[mercurius-account-management]] · [[orion-pricing-strategy]] · [[orion-retention-engineering]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **mercurius-expansion-revenue** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in mercurius-expansion-revenue:**

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
