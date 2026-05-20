---
name: euterpe-email-marketing-mass
description: Mass email — list hygiene, deliverability, segmentation, automation. Triggers em "email marketing", "deliverability", "Mailchimp", "Klaviyo", "Iterable", "Sendgrid", "Postmark", "DMARC", "SPF DKIM".
license: MIT
parent_agent: euterpe-director
compliance: [lgpd_marketing, gdpr_marketing, no_dark_patterns]
---

# EUTERPE-EMAIL-MARKETING-MASS

## Stack
- **Klaviyo** — e-commerce líder
- **Mailchimp** — SMB líder
- **Iterable** — cross-channel
- **Customer.io** — automation
- **Braze** — enterprise multi-channel
- **MailerLite, ConvertKit** — creators
- **SendGrid, Postmark** — transactional
- **AWS SES** — bulk transactional cheap

## Deliverability essentials
- **SPF, DKIM, DMARC:** authentication trio
- **BIMI:** Brand Indicators (logo na inbox)
- **List hygiene:** remove invalid, bounces, complaints
- **Engagement segmentation:** ignore non-openers gradually
- **Warm-up:** new IP/domain gradual ramp
- **Reputation monitoring:** Sender Score, Postmaster Tools

## Performance benchmarks
- **Open rate:** 15-25% B2B, 18-30% B2C
- **CTR:** 2-5% típico
- **Conversion:** 1-3% transactional
- **Unsubscribe:** <0.5% (alarm at 1%+)
- **Bounce rate:** <2% (alarm at 5%+)
- **Spam complaints:** <0.1% (Gmail flag at 0.3%)

## Templates
1. Welcome sequence (5-7 emails)
2. Abandoned cart flow (3 emails)
3. Win-back campaign (3 emails)
4. RFM segmentation
5. Deliverability audit checklist
6. Re-engagement before sunset

## Cross-references
- [[dario-email-seq]] · [[euterpe-customer-data-platform]] · [[orion-retention-engineering]]
