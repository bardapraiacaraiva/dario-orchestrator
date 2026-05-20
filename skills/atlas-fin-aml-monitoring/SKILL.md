---
name: atlas-fin-aml-monitoring
description: AML transaction monitoring — rules, ML detection, SARs to COAF (BR) + UIF (PT). Triggers em "AML monitoring", "transaction monitoring", "COAF", "UIF Portugal", "SAR", "suspicious activity", "AMLD6".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable, sanctions_realtime]
---

# ATLAS-FIN-AML-MONITORING

## Marco
- **BR:** Lei 9.613/1998 + Circular Bacen 3978/2020 + COAF
- **PT:** Lei 83/2017 + UIF Portugal
- **EU:** AMLD6 (Directive 2024/1640) — applicable Jul 2027
- **FATF Recommendations** (40+9)

## Stack
- **NICE Actimize** — enterprise líder
- **SAS AML** — banking traditional
- **Hummingbird (now ComplyAdvantage)** — modern
- **Trapets** — Nordics
- **Quantexa** — graph-based, network analysis
- **BR-specific:** Spline, Avantia, IDtech

## Detection rules (típicas)
- **Structuring:** múltiplas transações just below threshold
- **Unusual velocity:** spike inexplicado
- **High-risk countries:** transferências OFAC, FATF blacklist
- **PEP transactions:** politicamente exposto + alto valor
- **Round numbers:** R$ 10.000, R$ 50.000 (money laundering signals)
- **New account, large transaction:** D-7 risk
- **Dormant → active:** account "wake up" pattern

## Workflow
```
1. Real-time monitoring (rules + ML)
2. Alert triage (level 1)
3. Investigation (level 2)
4. SAR filing decision
5. Submit COAF (BR) / UIF (PT)
6. Recordkeeping (5 years BR, 7 EU)
```

## Templates
1. AML monitoring rules library (50+ rules)
2. Alert triage workflow
3. SAR template COAF + UIF
4. Investigation case file structure
5. Annual independent review framework
6. Training curriculum AML staff

## Cross-references
- [[atlas-fin-sanctions-screening]] · [[atlas-fin-kyc-onboarding]] · [[nomos-kyc-aml-pt]]
