---
name: euterpe-paid-search
description: Paid search — Google Ads advanced, Quality Score, Smart Bidding, Performance Max. Triggers em "paid search", "Google Ads", "PPC", "Quality Score", "Smart Bidding", "Performance Max", "Microsoft Advertising".
license: MIT
parent_agent: euterpe-director
---

# EUTERPE-PAID-SEARCH

## Quando usar
- High-intent traffic capture
- Branded protection
- Competitor bidding
- Local services
- E-commerce shopping

## Campaign types Google Ads
- **Search:** keyword-based
- **Performance Max (PMax):** AI cross-channel
- **Shopping:** product feed-based
- **Display:** banner ads GDN
- **Video (YouTube):** TrueView, Bumpers, in-stream
- **App campaigns:** install + engagement
- **Discovery / Demand Gen:** YouTube + Gmail + Discover

## Optimization levers
- **Quality Score (1-10):** Ad Relevance + Expected CTR + Landing Page
- **Smart Bidding:** Target ROAS, Target CPA, Max Conversions
- **Audience signals:** add to PMax campaigns
- **Negative keywords:** prevent waste
- **Ad extensions:** sitelinks, callouts, structured snippets

## Métricas chave
- **CTR:** clicks / impressions
- **CPC:** average cost per click
- **Conv rate:** conversions / clicks
- **ROAS:** revenue / spend
- **CPA:** cost per acquisition
- **Impression share:** impressions / total available

## Templates
1. Account structure (campaign/ad group/ad)
2. Keyword research process
3. Negative keyword library
4. Quality Score optimization checklist
5. PMax asset group structure
6. Conversion tracking setup (enhanced conversions)

## Cross-references
- [[seo-plan]] · [[euterpe-paid-social]] · [[demeter-ab-testing]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-paid-search** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-paid-search:**

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
