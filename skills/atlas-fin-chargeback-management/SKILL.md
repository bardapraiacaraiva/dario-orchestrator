---
name: atlas-fin-chargeback-management
description: Chargeback dispute, evidence collection, win-rate optimization, friendly fraud. Triggers em "chargeback", "chargeback dispute", "friendly fraud", "RDR Visa", "CDRN Mastercard", "Verifi", "Ethoca".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [audit_immutable]
---

# ATLAS-FIN-CHARGEBACK-MANAGEMENT

## Tipos de chargeback
- **Friendly fraud (genuine):** consumer claims didn't recognize charge
- **True fraud:** stolen card used
- **Service failure:** product not delivered, defective
- **Authorization:** technical issue with auth
- **Processing error:** double charge, wrong amount

## Card brand reason codes
- **Visa:** 30 reason codes (10.4 fraud-CP, 13.1 missing product)
- **Mastercard:** 4837 (no authorization), 4853 (cancelled recurring)
- **Amex:** F30 fraud, P05 credit not processed
- **Discover:** AT (NOT-AUTH), CR (CREDIT)

## Pre-dispute alerts
- **Verifi (Visa CDRN):** Cardholder Dispute Resolution Network
- **Ethoca Alerts (Mastercard):** early warning
- **RDR (Visa Rapid Dispute Resolution):** auto-refund pre-chargeback

## Win-rate optimization
- Quick response (<5 days)
- Evidence pack templates per reason code
- Customer service receipts
- Delivery confirmation (signature, photo)
- IP geolocation match
- Device fingerprint match
- Customer communication history

## Templates
1. Chargeback dispute response templates (per reason code)
2. Evidence collection checklist
3. RDR/CDRN integration setup
4. Chargeback ratio monitoring dashboard
5. Merchant fraud monitoring program
6. Customer service receipt template

## Cross-references
- [[atlas-fin-fraud-prevention]] · [[atlas-fin-payment-orchestration]] · [[lex-consumidor]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-fin-chargeback-management** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-fin-chargeback-management:**

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
