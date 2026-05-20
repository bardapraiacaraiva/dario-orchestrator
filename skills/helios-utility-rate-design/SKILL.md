---
name: helios-utility-rate-design
description: Utility rate design — tariff structure, ToU, demand charges, social tariffs, dynamic pricing. Triggers em "utility rate design", "tariff design", "ToU", "demand charge", "social tariff", "dynamic pricing", "Reforma Tarifária".
license: SEE-LICENSE
parent_agent: helios-director
compliance: [aneel_compliance_gate]
---

# HELIOS-UTILITY-RATE-DESIGN

## Componentes tarifários BR
- **TUSD (Tarifa Uso Sistema Distribuição):** fio
- **TE (Tarifa Energia):** energia consumida
- **Bandeira tarifária:** verde/amarela/vermelha 1/vermelha 2
- **Encargos setoriais:** CDE, CCRBT, PROINFA
- **Tributos:** ICMS, PIS/COFINS

## Tipos tarifa
- **Convencional B1/B2/B3:** residencial/rural/commercial pequeno
- **Branca:** ToU residencial (3 períodos)
- **Verde:** opção horária A (industrial)
- **Azul:** demanda + energia (industrial alta)
- **Tarifa social:** baixa renda subsidiada

## Reforma Tarifária 2026
- Em implementação ANEEL
- Subsídios cruzados reduction
- TUSD demand mais alocada para grandes
- Adoption de tarifas dinâmicas (real-time)

## Dynamic pricing models
- **ToU (Time-of-Use):** fixed bands (peak/off-peak)
- **CPP (Critical Peak Pricing):** spike eventos críticos
- **RTP (Real-Time Pricing):** wholesale-linked
- **Tiered:** consumption-based blocks

## Templates
1. Tariff structure analysis (per cliente)
2. Class cross-subsidy quantification
3. ToU design (3-period vs hourly)
4. Reforma Tarifária impact por cliente
5. Social tariff eligibility framework
6. Dynamic pricing rollout plan

## Cross-references
- [[helios-aneel-compliance]] · [[helios-mercado-livre-br]] · [[helios-demand-response]]
