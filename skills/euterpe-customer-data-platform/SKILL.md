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
