---
name: euterpe-influencer-marketing
description: Influencer marketing — selection, contracts, ROI measurement, FTC/CONAR compliance. Triggers em "influencer marketing", "creator economy", "FTC disclosure", "CONAR PT", "Upfluence", "AspireIQ", "Grin".
license: MIT
parent_agent: euterpe-director
compliance: [audit_trail, no_dark_patterns]
---

# EUTERPE-INFLUENCER-MARKETING

## Categorias influencer
- **Nano:** <10K followers (1-3% engagement, high authenticity)
- **Micro:** 10K-100K (3-8% engagement, niche audiences)
- **Mid-tier:** 100K-1M (1-3% engagement)
- **Macro:** 1M-10M (broad reach, lower engagement)
- **Mega/Celebrity:** 10M+ (highest cost)

## Stack
- **Upfluence** — discovery + management
- **AspireIQ** — enterprise platform
- **Grin** — DTC-focused
- **Creator.co** — Shopify-focused
- **BR:** Squid, Airfluencers, Influre

## Compliance
- **FTC (US):** #ad #sponsored disclosure mandatory
- **CONAR (BR):** Resolução 168/2023 — disclosure obrigatório
- **ASA (UK):** similar
- **EU AVMSD:** product placement rules
- **Anti-fraud:** fake followers detection (HypeAuditor)

## ROI measurement
- **EMV (Earned Media Value):** equivalent paid spend
- **Engagement rate:** likes+comments+shares / followers
- **CPM (Cost per 1000 impressions):** comparable to paid media
- **Conversion attribution:** UTM, promo codes, affiliate links
- **Brand lift studies:** awareness pré/pós campanha

## Templates
1. Influencer brief template
2. Contract template (deliverables + exclusivity)
3. Disclosure compliance checklist
4. ROI measurement framework
5. Influencer audit (fake followers, fit)
6. Long-term ambassador program design

## Cross-references
- [[euterpe-brand-tracking]] · [[euterpe-affiliate-marketing]] · [[nomos-igac-events-pt]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-influencer-marketing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-influencer-marketing:**

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
