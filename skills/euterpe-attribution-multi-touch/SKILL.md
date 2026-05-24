---
name: euterpe-attribution-multi-touch
description: Multi-touch attribution — MTA, Shapley, Markov, position-based, ML-driven. Triggers em "multi-touch attribution", "MTA", "Shapley value", "Markov chain attribution", "data-driven attribution", "GA4 attribution".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing]
---

# EUTERPE-ATTRIBUTION-MULTI-TOUCH

## Models
- **First-click:** all credit to first touch (acquisition-focused)
- **Last-click:** all credit to last touch (default, conversion-biased)
- **Linear:** equal split all touchpoints
- **Time-decay:** more recent = more credit
- **Position-based (U-shaped):** 40% first + 40% last + 20% middle
- **Data-driven (Shapley/Markov):** ML-based fair allocation
- **Custom:** business logic per industry

## Stack
- **GA4 Data-Driven Attribution** — default Google
- **Adobe Analytics MTA**
- **Branch.io** — mobile attribution líder
- **AppsFlyer** — mobile
- **Northbeam, Triple Whale** — DTC e-commerce
- **Custom:** R + ChannelAttribution package

## MTA limitations 2026
- Cookie deprecation (Chrome 2025)
- iOS ATT (App Tracking Transparency) impact
- LGPD/GDPR consent requirements
- Mobile in-app vs web walls
- → **MMM growing as replacement**

## Templates
1. Attribution model selection rubric
2. Touchpoint taxonomy design
3. Shapley calculation methodology
4. Markov chain transition matrix
5. MTA + MMM reconciliation
6. Attribution change communication (when switching models)

## Cross-references
- [[euterpe-mmm-modeling]] · [[demeter-event-tracking]] · [[orion-product-analytics]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-attribution-multi-touch** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-attribution-multi-touch:**

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
