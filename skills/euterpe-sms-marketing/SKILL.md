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
