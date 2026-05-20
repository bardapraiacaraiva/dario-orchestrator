---
name: orion-product-analytics
description: Product analytics — Mixpanel, Amplitude, PostHog instrumentation. Funnel, cohort, retention, feature adoption. Triggers em "product analytics", "Mixpanel", "Amplitude", "PostHog", "funnel", "activation".
license: MIT
parent_agent: orion-director
compliance: [lgpd_consent, pii_handling]
---

# ORION-PRODUCT-ANALYTICS

## Quando usar
- Instrumentation greenfield (event taxonomy + tracking plan)
- Audit de analytics existente (data trust score)
- Migration entre platforms (Mixpanel → Amplitude)
- Self-service analytics setup
- Activation funnel optimization

## Stack
- **Mixpanel** (event-based, líder histórico)
- **Amplitude** (cohort + behavioral)
- **PostHog** (open-source, full stack)
- **Heap** (auto-capture)
- **GA4** (web-focused, free)

## Métricas core
- **Activation rate:** % users que completam "aha moment" em N dias
- **Engagement (DAU/MAU):** stickiness ratio
- **Retention curves:** D1/D7/D30/D90
- **Feature adoption:** % users que usam feature X em 30 dias
- **Time to value:** mediana entre signup e first value

## Templates
1. Event taxonomy + tracking plan (CSV)
2. Activation funnel definition (5-7 steps max)
3. Retention dashboard (cohort heatmap)
4. Feature adoption dashboard
5. North Star + input metrics tree

## Cross-references
- [[orion-product-discovery]] · [[demeter-event-tracking]] · [[demeter-cohort-analysis]]
