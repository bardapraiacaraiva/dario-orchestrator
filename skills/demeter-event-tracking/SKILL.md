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
