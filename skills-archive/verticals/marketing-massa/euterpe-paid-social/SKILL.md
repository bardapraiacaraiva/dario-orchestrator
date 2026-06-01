---
name: euterpe-paid-social
description: Paid social — Meta Ads, TikTok Ads, LinkedIn Ads, Pinterest, Snapchat. Triggers em "paid social", "Meta Ads", "Facebook Ads", "TikTok Ads", "LinkedIn Ads", "Advantage+", "lookalike audiences".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, gdpr_marketing]
---

# EUTERPE-PAID-SOCIAL

## Platforms + strengths
- **Meta (FB+IG):** broad reach, retargeting, e-commerce
- **TikTok Ads:** Gen Z, viral creative, mass discovery
- **LinkedIn Ads:** B2B premium, $$$, decision makers
- **Pinterest:** intent-driven, female-skewed, lifestyle
- **Snapchat:** Gen Z, ephemeral, AR
- **Reddit Ads:** niche communities
- **X (Twitter) Ads:** news, B2B niche
- **YouTube Ads:** video + Google integration

## Meta-specific
- **Advantage+ Shopping:** AI campaign optimization
- **Lookalike audiences:** seed audience → similar profiles
- **Custom audiences:** retargeting, customer lists
- **CAPI (Conversions API):** server-side tracking (post-iOS ATT)
- **Pixel + iOS 14.5+:** Aggregated Event Measurement (AEM)

## Compliance specifics
- **LGPD + Meta:** Data Processing Term BR
- **iOS ATT:** App Tracking Transparency degraded targeting
- **EU DSA:** Digital Services Act ads transparency
- **CAPI server-side:** mitigates browser tracking loss

## Performance benchmarks
- **CTR:** 0.9-2% (varies by platform)
- **CPM:** $5-15 (Meta), $15-30 (LinkedIn)
- **CPA:** varies wildly by industry
- **CPC:** $0.50-3 (Meta), $5-15 (LinkedIn)

## Templates
1. Campaign structure (CBO vs ABO)
2. Creative testing framework
3. CAPI implementation
4. Audience building strategy
5. iOS ATT mitigation playbook
6. Cross-platform attribution

## Cross-references
- [[euterpe-paid-search]] · [[euterpe-customer-data-platform]] · [[euterpe-attribution-multi-touch]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-paid-social** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-paid-social:**

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
