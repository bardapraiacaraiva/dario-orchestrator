---
name: atlas-fin-regulatory-reporting-bcb
description: Regulatory reporting Bacen — DCAD, SCR, RDR, IF.Data, GIN-SFN. Triggers em "Bacen reporting", "DCAD", "SCR", "RDR Bacen", "IF.Data", "GIN-SFN", "regulatory reporting BR".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# ATLAS-FIN-REGULATORY-REPORTING-BCB

## Reports Bacen principais
- **DCAD** — Documento Cadastral Análise de Disclosure
- **SCR** — Sistema Informações de Crédito (mensal)
- **RDR** — Risk Data Reporting
- **IF.Data** — IF.Data app (financial data)
- **GIN-SFN** — Gestor Informações Sistema Financeiro Nacional
- **DLO** — Demonstração Limites Operacionais
- **PROFIS** — Programa Fiscalização
- **Circular Letter** — ad-hoc requests

## Frequencies
- **Daily:** liquidity (LCR), large exposures
- **Monthly:** SCR credit, balance sheet
- **Quarterly:** ICAAP-related, stress test
- **Annual:** ICAAP, recovery plan, financial statements
- **Ad-hoc:** Circular Letters, on-site inspection

## Stack
- **Cloudera, SAS** — enterprise banks
- **Wolters Kluwer OneSumX** — global
- **AxiomSL (Adenza)** — risk + compliance reporting
- **BR-specific:** Senior Sistemas, Algar, custom internal

## Templates
1. Bacen reporting calendar (annual)
2. DLO calculation methodology
3. SCR mapping rules
4. RDR data architecture
5. ICAAP report structure
6. Reconciliation framework (general ledger ↔ reports)

## Cross-references
- [[nomos-bdp-banking-pt]] · [[atlas-fin-foreign-exchange]] · [[demeter-data-quality]]
