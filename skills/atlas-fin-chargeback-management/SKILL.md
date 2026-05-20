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
