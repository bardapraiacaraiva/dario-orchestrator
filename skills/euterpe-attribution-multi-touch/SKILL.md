---
name: euterpe-attribution-multi-touch
description: Multi-touch attribution — MTA, Shapley, Markov, position-based, ML-driven. Triggers em "multi-touch attribution", "MTA", "Shapley value", "Markov chain attribution", "data-driven attribution", "GA4 attribution".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing]
---

# EUTERPE-ATTRIBUTION-MULTI-TOUCH

## Models
- **First-click:** all credit to first touch (acquisition-focused)
- **Last-click:** all credit to last touch (default, conversion-biased)
- **Linear:** equal split all touchpoints
- **Time-decay:** more recent = more credit
- **Position-based (U-shaped):** 40% first + 40% last + 20% middle
- **Data-driven (Shapley/Markov):** ML-based fair allocation
- **Custom:** business logic per industry

## Stack
- **GA4 Data-Driven Attribution** — default Google
- **Adobe Analytics MTA**
- **Branch.io** — mobile attribution líder
- **AppsFlyer** — mobile
- **Northbeam, Triple Whale** — DTC e-commerce
- **Custom:** R + ChannelAttribution package

## MTA limitations 2026
- Cookie deprecation (Chrome 2025)
- iOS ATT (App Tracking Transparency) impact
- LGPD/GDPR consent requirements
- Mobile in-app vs web walls
- → **MMM growing as replacement**

## Templates
1. Attribution model selection rubric
2. Touchpoint taxonomy design
3. Shapley calculation methodology
4. Markov chain transition matrix
5. MTA + MMM reconciliation
6. Attribution change communication (when switching models)

## Cross-references
- [[euterpe-mmm-modeling]] · [[demeter-event-tracking]] · [[orion-product-analytics]]
