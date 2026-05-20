---
name: atlas-fin-fraud-prevention
description: Fraud prevention — ML rules, device fingerprinting, behavioral biometrics, network analysis. Triggers em "fraud prevention", "device fingerprinting", "behavioral biometrics", "Sift", "Forter", "Riskified", "Kount", "Signifyd".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [audit_immutable, sanctions_realtime]
---

# ATLAS-FIN-FRAUD-PREVENTION

## Quando usar
- E-commerce fraud rate >1%
- Account takeover (ATO) attacks
- Synthetic identity fraud
- Card-not-present (CNP) high-risk
- PIX-specific fraud BR

## Detection layers
1. **Device fingerprinting** (FingerprintJS, ThreatMetrix)
2. **Behavioral biometrics** (BioCatch, NuData)
3. **Network analysis** (graph-based, account linking)
4. **ML rules** (XGBoost on historical fraud)
5. **3DS 2.0** (issuer authentication shift)
6. **Negative lists** (devices, IPs, emails)

## Stack
- **Sift** — ML fraud platform
- **Forter** — guaranteed fraud
- **Signifyd** — e-commerce focus
- **Kount (Equifax)** — multi-purpose
- **Riskified** — chargeback guarantee
- **Stripe Radar** — bundled
- **BR-specific:** ClearSale, Konduto, Cyberbox

## Rules vs ML hybrid
- **Rules:** explainable, hard limits (BIN blocked, country blocked)
- **ML:** patterns subtle, continuous learning
- **Best practice:** rules for hard NO, ML for grey area

## Templates
1. Fraud rules library (30 starter rules)
2. ML model deployment workflow
3. Manual review queue UX
4. Fraud scorecard per merchant
5. Account Takeover (ATO) playbook
6. Synthetic identity detection patterns

## Cross-references
- [[atlas-fin-aml-monitoring]] · [[atlas-fin-sanctions-screening]] · [[demeter-predictive]]
