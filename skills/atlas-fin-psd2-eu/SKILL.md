---
name: atlas-fin-psd2-eu
description: PSD2 EU implementation — SCA, XS2A, TPP, EBA RTS. Triggers em "PSD2", "PSD2 EU", "SCA EU", "XS2A", "Berlin Group", "STET", "Open Banking UK".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [ecb_compliance_gate, audit_immutable]
jurisdiction: EU
---

# ATLAS-FIN-PSD2-EU

(See also [[nomos-psd2-open-banking-pt]] for PT-specific transposição)

## Marco
- **Directive (EU) 2015/2366 (PSD2)**
- **RTS on SCA & CSC (EU 2018/389)**
- **Open Banking UK** (CMA standard, post-Brexit)
- **PSD3 + PSR proposals (2023)** — em discussão
- **eIDAS 2 + EU Digital Identity Wallet**

## TPP types
- **AISP** — read-only account info
- **PISP** — payment initiation
- **CBPII** — card-based payment instrument issuer
- **ASPSP** — Account Servicing Payment Service Provider (banks)

## XS2A interface options
- **Berlin Group NextGen PSD2** — most adopted EU
- **STET (France)** — alternative
- **Open Banking UK Standard** — UK-focused

## SCA exemptions
- Low-value < €30
- Recurring transactions
- Trusted beneficiaries (whitelist)
- Corporate payments via secure protocols
- TRA (Transaction Risk Analysis) ≤ €500

## Templates
1. TPP authorization application (national regulator)
2. XS2A API spec (Berlin Group)
3. SCA exemption decision tree
4. Consent management framework
5. Fallback mechanism (when bank API down)
6. PSD3 readiness assessment

## Cross-references
- [[nomos-psd2-open-banking-pt]] · [[atlas-fin-open-banking-br]] · [[aegis-iam-identity]]
