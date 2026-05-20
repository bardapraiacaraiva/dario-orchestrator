---
name: atlas-fin-foreign-exchange
description: FX management — câmbio BR (BCB), hedging, IOF, IRS, declaração CBE. Triggers em "câmbio", "FX management", "IOF câmbio", "DCE Bacen", "CBE", "remessa internacional", "Wise", "Remessa Online".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [bcb_compliance_gate, audit_immutable]
jurisdiction: Brasil + Global
---

# ATLAS-FIN-FOREIGN-EXCHANGE

## Marco BR
- **Lei 14.286/2021** — novo marco câmbio BR (substitui Decreto-Lei 4.595)
- **Resolução BCB 277/2022** + posteriores
- **IOF Câmbio** — alíquotas variáveis (0%-6.38%)
- **CBE (Capitais Brasileiros no Exterior)** — declaração Bacen quando >US$ 1M
- **DCE (Declaração Conjunta sobre Exportação)** — exportadores

## Operações típicas
- **Remessa internacional:** Wise, Remessa Online, BS2
- **Importação:** fechamento câmbio + DI
- **Exportação:** ACC/ACE financing
- **Hedge:** NDF (Non-Deliverable Forward), swap
- **Investimento exterior:** declaração CBE

## IOF Câmbio alíquotas (2026)
- **Aquisição moeda papel/cartão:** 3.5%
- **Importação:** 0.38%
- **Empréstimo externo curto prazo:** 6%
- **Remessa para residente exterior:** 0.38%
- **Transferência conta própria exterior:** 1.1%
- **Convergência tax reform:** progressive harmonization

## Templates
1. FX integration architecture (Bacen reporting)
2. Hedging strategy template (cash flow vs balance sheet)
3. IOF calculator (per operation type)
4. CBE annual declaration
5. ACC/ACE workflow (export financing)
6. NDF hedging playbook

## Cross-references
- [[atlas-fin-regulatory-reporting-bcb]] · [[nomos-mifid-ii-pt]] · [[zenith-sensitivity-analysis]]
