---
name: atlas-fin-banking-as-a-service
description: BaaS architecture — white-label banking, embedded accounts, card issuing, Dock, QI Tech, Swap. Triggers em "BaaS", "Banking as a Service", "white-label banking", "Dock", "QI Tech", "Swap fintech", "card issuing".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
---

# ATLAS-FIN-BANKING-AS-A-SERVICE

## Quando usar
- Non-financial company quer oferecer financial products (super-app)
- Fintech sem charter (não autorizada Bacen)
- Time-to-market reduzir 18 meses → 2 meses
- Marketplace que quer wallet/escrow
- Vertical SaaS adding embedded finance

## Stack BR
- **Dock** — líder BR, processadora + emissora
- **QI Tech** — credit + payments BaaS
- **Swap** — cards + payments
- **Pismo** — banking core
- **CloudWalk (InfinitePay)** — payments BaaS
- **Conductor (Pague Veloz)** — emissor cartões

## Stack global
- **Unit** — US líder
- **Synapse** (turbulent 2024)
- **Treasury Prime** — embedded banking US
- **Solaris (DE)** — European líder (em recovery)
- **ClearBank (UK)** — UK BaaS líder

## Products típicos BaaS
- **Conta digital** — checking equivalent
- **Cartão pré-pago / débito** — Visa/Mastercard rails
- **Cartão crédito** — emissor white-label
- **PIX integration** — accept + send
- **Empréstimos** — credit-as-a-service
- **Seguros** — insurance-as-a-service

## Templates
1. BaaS provider selection scorecard
2. Charter vs BaaS decision framework
3. Integration architecture (BaaS APIs)
4. Compliance responsibility matrix
5. Cost modeling (per-transaction, monthly fees)
6. Exit strategy planning (migration to own charter)

## Cross-references
- [[atlas-fin-embedded-finance]] · [[atlas-fin-instant-payments]] · [[nomos-bdp-banking-pt]]
