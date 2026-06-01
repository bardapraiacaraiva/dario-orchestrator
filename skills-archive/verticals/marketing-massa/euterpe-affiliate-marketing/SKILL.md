---
name: euterpe-affiliate-marketing
description: Affiliate programs — Impact, ShareASale, CJ, Hotmart (BR), fraud detection. Triggers em "affiliate marketing", "Impact Radius", "ShareASale", "CJ Affiliate", "Hotmart", "Eduzz", "Monetizze", "affiliate fraud".
license: MIT
parent_agent: euterpe-director
compliance: [audit_trail, no_dark_patterns]
---

# EUTERPE-AFFILIATE-MARKETING

## Stack global
- **Impact** — enterprise líder
- **CJ Affiliate (Commission Junction)** — long-established
- **ShareASale** — mid-market
- **Awin** — international
- **Rakuten Advertising** — enterprise
- **PartnerStack** — SaaS partnerships

## Stack BR
- **Hotmart** — infoprodutos líder
- **Eduzz** — concorrente direto
- **Monetizze** — alternativa
- **Lomadee** — e-commerce
- **Awin BR** — international + local
- **Magalu Pay Afiliados** — retail

## Tipos
- **Affiliate sites:** content + reviews (Wirecutter, NerdWallet)
- **Influencers:** social + content
- **Coupon sites:** RetailMeNot, Honey
- **Cashback:** Rakuten, Honey
- **Sub-affiliate networks:** Skimlinks, Sovrn
- **B2B partner program:** PartnerStack, Crossbeam

## Fraud detection
- **Cookie stuffing:** invisible iframe + cookie drop
- **Click fraud:** bot clicks
- **Order injection:** unauthorized last-click hijack
- **Toolbar fraud:** Honey-style overlap
- **Stack:** Impact Anti-Fraud, Forensiq, ClickGUARD

## Templates
1. Affiliate program structure (commission tiers)
2. T&Cs template (compliance + IP)
3. Affiliate onboarding
4. Performance tracking dashboard
5. Fraud detection rules
6. Compliance disclosure requirements

## Cross-references
- [[euterpe-influencer-marketing]] · [[euterpe-viral-marketing]] · [[atlas-fin-fraud-prevention]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-affiliate-marketing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-affiliate-marketing:**

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
