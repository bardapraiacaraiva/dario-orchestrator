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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **euterpe-email-marketing-mass** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in euterpe-email-marketing-mass:**

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
