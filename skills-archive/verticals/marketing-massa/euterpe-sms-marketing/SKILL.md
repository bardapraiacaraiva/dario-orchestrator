---
name: euterpe-sms-marketing
description: SMS marketing — opt-in, compliance TCPA/LGPD, short codes, RCS. Triggers em "SMS marketing", "RCS", "short code", "TCPA", "opt-in SMS", "Attentive", "Postscript".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, no_dark_patterns]
---

# EUTERPE-SMS-MARKETING

## Stack
- **Attentive** — líder e-commerce
- **Postscript** — Shopify-focused
- **Klaviyo SMS** — bundled
- **Twilio SMS** — API/CPaaS
- **Vonage, Sinch** — global
- **Zenvia, TotalVoice** — BR-focused

## Compliance
- **TCPA (US):** opt-in required, fines até $1,500/SMS
- **LGPD BR:** Lei 8.078 (CDC) + LGPD consentimento
- **STOP keyword:** mandatory opt-out
- **Quiet hours:** typically 9pm-9am (varies state)
- **CTIA guidelines (US):** carrier compliance

## Use cases
- **Abandoned cart recovery:** SMS 1h pós-abandono
- **Order confirmation:** transactional always-allowed
- **Shipping updates:** transactional
- **Flash sales:** marketing requires opt-in
- **Back-in-stock:** marketing
- **Birthday/anniversary:** automated

## Performance benchmarks
- **CTR:** 19-25% (vs email 2-5%)
- **Conversion:** 20-30% short-window
- **Opt-out:** <2% target
- **Cost:** $0.02-0.10/SMS BR; $0.0075-0.05 US

## Templates
1. Opt-in flow (post-purchase, popup, checkout)
2. SMS sequence library (welcome, cart, win-back)
3. Compliance checklist (per country)
4. SMS + email integration playbook
5. RCS upgrade strategy (rich media)
6. Carrier registration short codes

## Cross-references
- [[euterpe-email-marketing-mass]] · [[atlas-fin-instant-payments]] · [[orion-retention-engineering]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-sms-marketing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-sms-marketing:**

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
