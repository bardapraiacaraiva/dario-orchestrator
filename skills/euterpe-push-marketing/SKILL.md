---
name: euterpe-push-marketing
description: Push notifications — mobile + web, segmentation, frequency caps. Triggers em "push notification", "web push", "mobile push", "OneSignal", "Braze push", "Iterable push", "FCM".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, no_dark_patterns]
---

# EUTERPE-PUSH-MARKETING

## Tipos
- **Mobile push (iOS APNs, Android FCM)**
- **Web push (Push API browsers)**
- **In-app:** when user is active in app
- **Rich push:** images, videos, action buttons

## Stack
- **OneSignal** — líder mid-market
- **Braze, Iterable, Customer.io** — enterprise
- **Airship** — enterprise legacy
- **Firebase Cloud Messaging (FCM):** free Google
- **Apple Push Notification service (APNs):** iOS

## Compliance + UX
- **Permission ask timing:** AFTER user value moment, not on landing
- **Frequency caps:** max 1-3/day mobile
- **Quiet hours:** local timezone respect
- **Personalization:** name + behavioral
- **Deep linking:** open specific screen
- **A/B testing:** copy + image + CTA

## Use cases
- **Re-engagement:** 7-day churn risk
- **Order updates:** transactional
- **Flash sales:** time-sensitive
- **Content updates:** news, articles
- **Geo-targeting:** location-based offers
- **Behavioral triggers:** abandoned X, completed Y

## Templates
1. Permission ask flow design
2. Push notification taxonomy
3. Frequency cap rules
4. Localization checklist
5. Deep link strategy
6. Push + email + SMS orchestration

## Cross-references
- [[euterpe-customer-data-platform]] · [[euterpe-sms-marketing]] · [[orion-product-analytics]]
