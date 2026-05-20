---
name: nomos-bdp-banking-pt
description: Banco de Portugal — supervisão prudencial, AML, capital requirements, RGICSF. Triggers em "Banco de Portugal", "BdP", "supervisão bancária PT", "RGICSF", "capital requirements", "Aviso BdP", "Carta Circular BdP".
license: SEE-LICENSE
parent_agent: nomos-director
compliance: [bdp_regulatory_reporting_gate, audit_immutable]
jurisdiction: Portugal
---

# NOMOS-BDP-BANKING-PT

## Marco
- **RGICSF (Regime Geral das IC e SF)** — DL 298/92 (multi-amended)
- **CRD V/CRR 2** — Capital Requirements (EU 2019/878, 2019/876)
- **BRRD II** — Bank Recovery and Resolution Directive
- **PSD2 + DL 91/2018** — Payment Services
- **Aviso BdP 2/2018** — Continuidade negócio
- **Aviso BdP 3/2020** — Cybersec
- **Circulares BdP** — interpretação prática

## Quando usar
- IC (Instituição de Crédito) authorization request
- Anti-money laundering program setup
- ICAAP/ILAAP submission
- Recovery plan + resolution plan
- Operational resilience (DORA combined)
- Stress testing EBA/BdP

## Pillars (Basel III/IV)
- **Pillar 1:** minimum capital requirements (CET1 ≥ 4.5%, T1 ≥ 6%, total ≥ 8%)
- **Pillar 2:** SREP (Supervisory Review) + ICAAP
- **Pillar 3:** market discipline + disclosures

## Templates
1. ICAAP documentation structure
2. ILAAP (liquidity) framework
3. Recovery plan template (8 sections RGICSF)
4. Operational risk loss data collection
5. AML/CFT policy (Lei 83/2017)
6. Suspicious Transaction Report (UIF)
7. RAS (Risk Appetite Statement) board-approved

## Compliance gates
- CET1 ratio monitoring (auto-alert if < buffer)
- ICAAP annual deadline (31 March)
- Liquidity coverage ratio (LCR ≥ 100%)
- NSFR (Net Stable Funding Ratio ≥ 100%)
- Large exposures monitoring

## Cross-references
- [[nomos-dora-resilience]] · [[nomos-kyc-aml-pt]] · [[nomos-mifid-ii-pt]] · [[atlas-fin-regulatory-reporting-bcb]]
