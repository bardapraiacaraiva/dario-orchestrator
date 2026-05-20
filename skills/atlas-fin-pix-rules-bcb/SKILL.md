---
name: atlas-fin-pix-rules-bcb
description: PIX rules BCB — limites, fraude, MED, MED-PIX, PIX Internacional, PIX Saque/Troco. Triggers em "PIX", "PIX Bacen", "MED PIX", "PIX Internacional", "PIX Saque", "PIX por aproximação", "Bacen PIX".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# ATLAS-FIN-PIX-RULES-BCB

## Marco
- **Resolução BCB 1/2020** — instituição arranjo PIX
- **Resolução BCB 19/2020** — funcionamento PIX
- **Circular BCB 4.027/2020** + posteriores
- **Resolução BCB 103/2021** — MED (Mecanismo Especial Devolução)
- **PIX Internacional 2026** — em implementação

## Quando usar
- Fintech integração PIX
- PSP (Provedor Serviços Pagamento) autorização
- Fraud rules PIX-specific
- MED (chargeback PIX equivalente) workflow
- PIX por aproximação (NFC) 2026
- PIX Cobrança (boleto-substitute)

## Modalidades PIX
- **PIX comum** — entre pessoas
- **PIX Cobrança** — substituto boleto, recorrência
- **PIX Saque/Troco** — saque em estabelecimentos
- **PIX por aproximação** — NFC contactless 2026
- **PIX Internacional** — cross-border 2026+

## Limites + fraude
- Conta PF: ≤ R$ 1.000/transação noturno (20h-6h)
- Limite mensal noturno: R$ 1.000 ajustável
- MED ≤ R$ 70.000 → 80 dias para iniciar
- Fraude marker → bloqueio cautelar

## Templates
1. PIX integration architecture
2. Fraud detection rules PIX
3. MED workflow (chargeback equivalent)
4. PIX QR Code generation (estático + dinâmico)
5. Pix Cobrança recorrência integration
6. Customer dispute UI

## Cross-references
- [[atlas-fin-fraud-prevention]] · [[atlas-fin-chargeback-management]] · [[atlas-fin-instant-payments]]
