---
name: nomos-psd2-open-banking-pt
description: PSD2 + Open Banking PT — Strong Customer Authentication (SCA), TPP authorization, account info services, payment initiation. Triggers em "PSD2", "Open Banking PT", "SCA", "Strong Customer Authentication", "TPP", "AIS", "PIS", "PSD3".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [bdp_regulatory_reporting_gate, audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-PSD2-OPEN-BANKING-PT

## Marco
- **Directive (EU) 2015/2366 (PSD2)** — Payment Services Directive 2
- **DL 91/2018** — transposição PT
- **RTS on SCA & CSC** (Regulation 2018/389)
- **PSD3 + PSR proposals (2023)** — under discussion, applicable 2026-2027
- **eIDAS 2** + **Digital Identity Wallet** — convergence
- **PT Open Banking** — implementação BdP

## TPP types (Third-Party Providers)
- **AISP (Account Info Service Provider):** read access, no payments
- **PISP (Payment Initiation Service Provider):** initiate payments from user account
- **CBPII (Card-Based Payment Instrument Issuer):** confirm funds availability

## SCA (Strong Customer Authentication)
- **Two factors required:** knowledge + possession + inherence
- **Exemptions:** low-value (<€30), recurring, MOTO, trusted beneficiaries, TRA (Transaction Risk Analysis)

## Quando usar
- TPP authorization BdP (AISP/PISP/CBPII)
- Bank API setup (PSD2 compliant XS2A interface)
- SCA implementation + UX optimization
- Open Banking commercial APIs (Premium APIs beyond PSD2)
- PSD3 readiness assessment

## Templates
1. TPP authorization application BdP
2. XS2A API specification (Berlin Group / STET / Open Banking UK)
3. SCA exemption decision tree
4. Consent management framework
5. Fallback mechanism for API outages
6. Premium API pricing model (beyond regulated)
7. PSD3 gap analysis (vs current PSD2)

## Cross-references
- [[nomos-bdp-banking-pt]] · [[atlas-fin-open-banking-br]] · [[atlas-fin-psd2-eu]] · [[aegis-iam-identity]]
