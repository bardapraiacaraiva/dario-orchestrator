---
name: orion-product-launch
description: Product launches — internal alignment, GTM, press, customer comms, post-launch monitoring. Triggers em "launch", "GTM", "go-to-market", "product launch", "release", "lancamento produto".
license: MIT
parent_agent: orion-director
compliance: [data_privacy_by_design]
---

# ORION-PRODUCT-LAUNCH

## Quando usar
- Major feature launch (X.0 release)
- New product line launch
- Re-launch (rebranded/repositioned)
- Geographic expansion (novo país)
- Tier launch (new pricing tier)

## Launch tiers
- **Tier 1 (major):** all-hands, press, customer comms, social media, ads
- **Tier 2 (medium):** customer comms + in-app + blog
- **Tier 3 (small):** changelog + in-app announcement

## Templates
1. Launch plan template (8 weeks pre → 4 weeks post)
2. Internal alignment doc (sales, support, success know what's coming)
3. Press kit (press release + screenshots + exec quotes)
4. Customer comm sequence (announcement + how-to + FAQ)
5. Sales enablement kit (battle cards + objection handling)
6. Post-launch monitoring dashboard (adoption + support tickets + NPS)

## Anti-patterns
- ❌ Launch sem internal alignment (sales descobre pelo Twitter)
- ❌ No metrics defined pre-launch
- ❌ No rollback plan
- ❌ Big-bang sem progressive rollout

## Cross-references
- [[orion-feature-flags]] · [[orion-beta-program]] · [[a360-lancamento]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-product-launch** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-product-launch:**

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
