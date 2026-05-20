---
name: nomos-kyc-aml-pt
description: KYC/AML PT — UIF Portugal, Lei 83/2017, beneficial ownership, SARs, sanctions screening. Triggers em "KYC", "AML PT", "UIF", "Lei 83/2017", "beneficiário efectivo", "RCBE", "branqueamento capitais", "AMLD6".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [audit_immutable]
jurisdiction: Portugal + EU
---

# NOMOS-KYC-AML-PT

## Marco
- **Lei 83/2017** — Prevenção BC/FT (transposição AMLD4/5)
- **DL 27/2024** — actualização AMLD5
- **Lei 89/2017** — RCBE (Registo Central Beneficiário Efectivo)
- **AMLD6 (Directive (EU) 2024/1640)** — applicable July 2027
- **AML Package (Regulation 2024/1624)** — directly applicable
- **EU AML Authority (AMLA)** — operational 2025+, based in Frankfurt

## Entidades obrigadas (Art. 3 Lei 83/2017)
- Instituições financeiras (bancos, seguradoras, fundos)
- Sociedades fiduciárias e gestoras de fundos
- Notários, advogados, contabilistas (atividades específicas)
- Empresas leilões, antiguidades, alta gama
- Casinos + apostas online
- VASPs (Virtual Asset Service Providers — crypto)
- Imobiliárias (transações > €10K cash)

## Workflow KYC
```
1. Customer identification (ID, address, beneficial owners)
2. Risk classification (low/medium/high)
3. Customer Due Diligence (CDD) ou Enhanced (EDD)
4. Sanctions screening (UN, EU, OFAC, BdP lists)
5. PEP screening
6. Ongoing monitoring + transaction monitoring
7. SAR (Suspicious Activity Report) → UIF if needed
8. Recordkeeping (7 years)
```

## RCBE obrigatório
- Pessoas colectivas portuguesas
- Inscrição RCBE até 30 dias após constituição
- Atualização sempre que muda beneficiário efectivo
- Sanção falta inscrição: até €50.000

## Templates
1. KYC/CDD onboarding form (PF + PJ)
2. EDD high-risk + PEP procedures
3. Sanctions screening workflow (OFAC + EU + UN)
4. Transaction monitoring scenarios (typical 30-50 rules)
5. SAR template UIF
6. RCBE submission template
7. AML training curriculum (annual)
8. AML risk assessment institutional

## Cross-references
- [[nomos-anti-fraude-pt]] · [[nomos-bdp-banking-pt]] · [[atlas-fin-kyc-onboarding]] · [[atlas-fin-aml-monitoring]]
