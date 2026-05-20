---
name: atlas-fin-payment-orchestration
description: Payment orchestration — multi-acquirer routing, retry logic, decline recovery, smart routing. Triggers em "payment orchestration", "smart routing", "multi-acquirer", "payment routing", "decline recovery", "ProcessOut", "Primer".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [pci_dss_scope, audit_immutable]
---

# ATLAS-FIN-PAYMENT-ORCHESTRATION

## Princípio
**1 acquirer = single point of failure.** Multi-acquirer + smart routing = approval rate +5-15%.

## Quando usar
- E-commerce com >€1M/ano payment volume
- Marketplace (multi-merchant, multi-currency)
- LATAM expansion (acquirers locais)
- Decline rate >10%
- Conversion optimization checkout

## Smart routing logic
- **BIN-based:** rotear por country/issuer do cartão
- **Performance-based:** auto-route ao acquirer com melhor approval rate
- **Cost-based:** menor MDR (Merchant Discount Rate)
- **Currency-based:** local acquirer para evitar FX
- **Retry logic:** falhou? tentar outro acquirer com delay

## Stack
- **Primer** — payment orchestration líder
- **ProcessOut** — open-source-friendly
- **Spreedly** — vault + orchestration
- **Adyen** — built-in orchestration
- **Gr4vy** — payment ops
- **BR-specific:** Pagar.me, Pagseguro, Stone (cada um próprio rail)

## Templates
1. Payment orchestration architecture
2. Smart routing rules matrix
3. Decline reason analysis + remediation
4. PCI-DSS scope reduction strategy
5. Acquirer scorecard (cost, approval, latency)
6. A/B testing payment flows

## Cross-references
- [[atlas-fin-fraud-prevention]] · [[atlas-fin-chargeback-management]] · [[atlas-fin-foreign-exchange]]
