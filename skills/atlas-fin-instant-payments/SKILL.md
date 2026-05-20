---
name: atlas-fin-instant-payments
description: Instant payments — PIX BR, SEPA Instant EU, FedNow US, RTP networks. Triggers em "instant payments", "PIX integration", "SEPA Instant", "FedNow", "RTP", "real-time payments", "MIR".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, ecb_compliance_gate, audit_immutable]
---

# ATLAS-FIN-INSTANT-PAYMENTS

## Networks globais
- **PIX (BR)** — 24/7, R$ 26 trilhões/ano, líder global per capita
- **SEPA Instant (EU)** — 10 sec, ≤€100K
- **FedNow (US)** — launched Jul 2023, growing
- **RTP (US)** — The Clearing House, alternative to FedNow
- **UK Faster Payments** — desde 2008
- **MIR (Russia)** — geopolitical context
- **PromptPay (Thailand)** — RTP líder ASEAN

## PIX BR específico
- **Volume diário:** ~250M transações
- **Custo:** zero p/ PF, baixo p/ PJ
- **Crescimento:** 130%+ YoY
- **PIX por aproximação (NFC):** 2026 rollout
- **PIX Internacional:** 2026 launch (BR ↔ países selecionados)

## Integration patterns
- **PSP direct** — fintechs como Pagar.me, Stone integração direta Bacen
- **Indirect via BaaS** — Dock, QI Tech, Swap
- **White-label** — banco parceiro empresta charter

## Templates
1. PIX integration roadmap
2. SEPA Instant API spec
3. Instant payment UX best practices
4. Reconciliation real-time
5. Failed payment retry logic
6. Cross-border instant strategy

## Cross-references
- [[atlas-fin-pix-rules-bcb]] · [[atlas-fin-open-banking-br]] · [[atlas-fin-banking-as-a-service]]
