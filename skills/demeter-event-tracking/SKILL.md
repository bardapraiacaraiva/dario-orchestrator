---
name: demeter-event-tracking
description: Event tracking & product analytics — Segment, RudderStack, Snowplow, PostHog. Event taxonomy, schema design, identity resolution. Triggers em "event tracking", "product analytics", "Segment", "RudderStack", "Snowplow", "PostHog", "Mixpanel", "Amplitude", "event schema".
license: MIT
parent_agent: demeter-director
compliance: [lgpd_consent, pii_handling, identity_resolution]
---

# DEMETER-EVENT-TRACKING — Front-end → Warehouse

## Quando usar
- Greenfield event tracking strategy
- Auditoria de eventos existentes (qual é qualidade?)
- Setup de Segment / RudderStack como CDP
- Migration: Google Analytics 4 → eventos próprios
- Identity resolution (anonymous → logged-in)
- Event taxonomy definition

## Stack
- **Segment** (proprietary, líder de mercado)
- **RudderStack** (open-source Segment alternative)
- **Snowplow** (open-source, mais flexível)
- **PostHog** (open-source product analytics)
- **Mixpanel / Amplitude** (managed product analytics)
- **GA4** (Google Analytics — não substitui CDP)

## Event taxonomy (princípio)
- **Object-Action:** "Cart_Item_Added" (não "addedToCart")
- **Consistent verb:** Past tense para histórico ("Order_Placed")
- **Required properties:** sempre user_id (or anonymous_id) + timestamp
- **Optional properties:** context, payload, source

## Identity resolution
```
Anonymous user (cookie/device) → Logged-in user
                              ↓
        anonymous_id ←→ user_id mapping
                              ↓
        Histórico unificado (pre + post login)
```

## Templates
1. Event taxonomy spec (Google Doc-style)
2. Segment tracking plan (CSV with events × properties)
3. CDP setup (Segment Connections + Destinations)
4. Identity resolution rules
5. Server-side tracking (better than client-side)
6. Consent mode (LGPD/GDPR compliance)

## Compliance
- ✓ **Consent before tracking:** opt-in obrigatório (LGPD)
- ✓ **PII handling:** email/CPF não em event properties (use user_id)
- ✓ **Right to be forgotten:** event deletion pipeline
- ✓ **Sensitive data exclusion:** healthcare, biometrics

## Cross-references
- [[demeter-ab-testing]] — exposure events
- [[demeter-cohort-analysis]] — eventos definem cohorts
- [[demeter-warehouse]] — destino dos eventos
- [[risco-rgpd]] — compliance consent


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **demeter-event-tracking** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in demeter-event-tracking:**

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
