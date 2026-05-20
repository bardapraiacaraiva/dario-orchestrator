---
name: helios-ev-charging-strategy
description: EV charging — infrastructure, fast charging, V2G, fleet electrification, charge points. Triggers em "EV charging", "estações carregamento", "fast charging", "V2G", "vehicle to grid", "fleet electrification", "ChargePoint", "EVgo".
license: SEE-LICENSE
parent_agent: helios-director
---

# HELIOS-EV-CHARGING-STRATEGY

## Charging levels
- **Level 1 (slow):** AC 1.4-1.9 kW, 8-20h full charge
- **Level 2 (medium):** AC 3.3-19.2 kW, 4-8h full
- **DC Fast (Level 3):** 25-150 kW, 30-60min 80%
- **Ultra-Fast (XFC):** 150-350 kW, 15-30min 80%
- **Tesla Supercharger V4:** up to 350 kW

## Connector standards
- **Type 2 (Mennekes):** EU AC standard
- **CCS Combo 2:** EU DC fast
- **CHAdeMO:** Japan DC fast (declining)
- **GB/T:** China standard
- **NACS (Tesla, now SAE J3400):** becoming US standard

## Business models
- **CPO (Charge Point Operator):** own + operate stations
- **eMSP (e-Mobility Service Provider):** customer-facing app/billing
- **Roaming:** cross-network access
- **Workplace:** employer-provided
- **Fleet:** depot charging private
- **Public:** highway + urban DC fast

## V2G (Vehicle-to-Grid)
- EV battery sells back to grid
- Pilots Nissan, Ford, Hyundai
- Regulatory + warranty challenges
- DERMS integration required

## Templates
1. Charging infrastructure site selection
2. CPO business model
3. Fleet electrification roadmap
4. V2G pilot framework
5. Charging tariff design
6. Roaming agreement template

## Cross-references
- [[helios-grid-integration]] · [[helios-demand-response]] · [[helios-microgrid-design]]
