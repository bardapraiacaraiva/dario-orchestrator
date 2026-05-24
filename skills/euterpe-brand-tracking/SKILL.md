---
name: euterpe-brand-tracking
description: Brand health metrics — awareness, consideration, NPS, share of voice, sentiment. Triggers em "brand tracking", "brand health", "awareness", "consideration", "share of voice", "Net Promoter Score", "brand sentiment".
license: MIT
parent_agent: euterpe-director
---

# EUTERPE-BRAND-TRACKING

## Métricas chave
- **Aided awareness:** "have you heard of X?" (%)
- **Unaided awareness:** "name brands em category Y" (%)
- **Top-of-mind:** first brand mentioned
- **Consideration:** "would consider buying"
- **Preference:** "favorite brand"
- **NPS:** Net Promoter Score (0-10 → promoter/passive/detractor)
- **CSAT:** Customer Satisfaction (1-5 ou 1-10)
- **Share of Voice (SOV):** % brand mentions in category
- **Brand sentiment:** positive/neutral/negative

## Stack
- **YouGov BrandIndex** — continuous tracking
- **Kantar Millward Brown** — full-service
- **Brandwatch, Sprinklr** — social listening
- **Talkwalker** — social + traditional media
- **Qualtrics** — survey platform
- **SurveyMonkey** — SMB-friendly
- **GWI** — global web index (audience)

## Funnel framework
```
Awareness → Familiarity → Consideration → Preference → Purchase → Loyalty → Advocacy
```

## Templates
1. Brand health tracker design (quarterly)
2. NPS survey template + analysis
3. Social listening keyword library
4. SOV competitive analysis
5. Brand crisis monitoring dashboard
6. CMO brand health monthly report

## Cross-references
- [[dario-brand]] · [[euterpe-influencer-marketing]] · [[orion-product-analytics]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-brand-tracking** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-brand-tracking:**

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
