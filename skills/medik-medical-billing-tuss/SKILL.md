---
name: medik-medical-billing-tuss
description: TUSS billing — Tabela Única de Saúde Suplementar, CBHPM, AMB. Codificação para operadoras. Triggers em "TUSS", "CBHPM", "AMB", "faturamento médico", "código procedimento", "tabela operadora".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, audit_trail]
jurisdiction: Brasil
---

# MEDIK-MEDICAL-BILLING-TUSS

## Quando usar
- Setup faturamento ANS-compliant
- Codificação TUSS de procedimentos
- Negociação tabela com operadora
- Glosas e recursos
- Migration AMB → CBHPM → TUSS

## Tabelas
- **TUSS (ANS)** — Tabela Única, padrão obrigatório operadoras
- **CBHPM 2022** — Classificação Brasileira Hierarquizada
- **AMB 92** — legada, ainda referenciada
- **SUS SIGTAP** — público (referência para precificação)

## Templates
1. Mapeamento procedimento → TUSS
2. Tabela negociação operadora (CH + valor) com benchmarks
3. Workflow glosa → recurso administrativo
4. Auditoria de faturamento (% recuperação)
5. Análise sinistralidade

## Compliance
- ✓ ANS RN 305/2012 (TISS — troca info operadora)
- ✓ Padrão TISS comunicação
- ✓ Auditoria CFC

## Cross-references
- [[medik-claim-management]] · [[medik-rcm-revenue-cycle]] · [[medik-ans-compliance]]
