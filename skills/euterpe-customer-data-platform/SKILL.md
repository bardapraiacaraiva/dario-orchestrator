---
name: euterpe-customer-data-platform
description: CDP architecture — Segment, RudderStack, Twilio, ActionIQ, mParticle. Unified customer profile. Triggers em "CDP", "Customer Data Platform", "Segment", "RudderStack", "ActionIQ", "mParticle", "unified profile", "identity graph".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, gdpr_marketing]
---

# EUTERPE-CUSTOMER-DATA-PLATFORM

## CDP categorias (Gartner)
- **Data CDP:** ingest + unify (Segment, RudderStack)
- **Analytics CDP:** + insights (Tealium)
- **Campaign CDP:** + activation (Salesforce CDP, Adobe AEP)
- **Delivery CDP:** + execution (Bloomreach)

## Stack
- **Segment (Twilio)** — líder dev-friendly
- **RudderStack** — Segment alternative, OSS-friendly
- **mParticle** — mobile-strong
- **Adobe Experience Platform**
- **Salesforce Data Cloud (ex-CDP)**
- **Bloomreach** — e-commerce focus
- **ActionIQ** — enterprise
- **Hightouch, Census** — reverse ETL (not CDP but adjacent)

## Identity graph
- Deterministic (login, email, phone)
- Probabilistic (device, fingerprint, behavioral)
- Identity stitching across devices
- Anonymous → known transition

## Use cases
- **Audience segmentation:** dynamic, real-time
- **Personalization:** product recs, content
- **Suppression:** don't show ads to recent buyers
- **Activation:** sync to Meta/Google/email
- **Compliance:** consent management central

## Templates
1. CDP requirements doc (selection)
2. Identity resolution rules
3. Audience taxonomy
4. Activation playbook (channel × audience)
5. Consent management integration (LGPD)
6. Data quality SLA

## Cross-references
- [[demeter-event-tracking]] · [[euterpe-attribution-multi-touch]] · [[obsidian-rag-corpus-engineering]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-customer-data-platform** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-customer-data-platform:**

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
