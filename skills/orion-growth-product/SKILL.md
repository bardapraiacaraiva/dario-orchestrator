---
name: orion-growth-product
description: Product-Led Growth (PLG) loops, activation, virality, expansion. Triggers em "PLG", "product-led growth", "activation", "viral loop", "growth", "expansion revenue".
license: MIT
parent_agent: orion-director
compliance: [user_consent_explicit, no_dark_patterns]
---

# ORION-GROWTH-PRODUCT

## Quando usar
- Migrar sales-led → PLG
- Activation funnel optimization
- Viral loops design (invite/share)
- Expansion revenue (upsell in-product)
- Self-serve onboarding

## Frameworks
- **AARRR Pirate Metrics:** Acquisition, Activation, Retention, Referral, Revenue
- **Reforge Growth Loops:** loop > funnel (each user pulls in more)
- **OpenView PLG Framework:** product as growth engine
- **Hooked (Eyal):** trigger → action → reward → investment
- **Fogg Behavior Model:** B = MAT (motivation × ability × trigger)

## Tipos de loop
- **Viral loop:** user → invite → user (Slack, Calendly)
- **Content loop:** user → content → SEO → user (Notion, Pinterest)
- **Paid loop:** revenue → ads → user → revenue (most B2C)
- **Sales-assisted PLG:** PLG bottom-up + sales top-down (Datadog)

## Templates
1. Activation funnel analysis (5-7 steps)
2. Viral loop design + measurement (k-factor)
3. Onboarding sequence (in-product + email)
4. Aha moment definition workshop
5. Expansion revenue playbook (in-product upsells)

## Anti-patterns
- ❌ Dark patterns (forced continuity, hidden costs)
- ❌ Growth hacks que destroem retention
- ❌ Vanity metrics (signups vs activated users)

## Cross-references
- [[orion-retention-engineering]] · [[orion-pricing-strategy]] · [[dario-funnel]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **orion-growth-product** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in orion-growth-product:**

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
