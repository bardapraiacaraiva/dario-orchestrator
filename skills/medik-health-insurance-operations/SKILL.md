---
name: medik-health-insurance-operations
description: Operadoras de saúde — autorização, gestão de rede, regulação assistencial, sinistralidade. Triggers em "operadora saúde", "autorização", "gestão rede", "regulação assistencial", "sinistralidade".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, lgpd_healthcare_marker, audit_cfm]
jurisdiction: Brasil
---

# MEDIK-HEALTH-INSURANCE-OPERATIONS

## Quando usar
- Setup operadora pequena/média
- Autorização prévia + auditoria médica
- Gestão de rede credenciada
- Análise de sinistralidade
- Programa de gestão de crônicos
- Verticalização vs network management

## Operações chave
- **Cadastro de beneficiários** (Datasus + ANS upload)
- **Autorização prévia** (médico auditor + protocolo ANS)
- **Gerenciamento de rede** (credenciamento + descredenciamento)
- **Faturamento + Repasse** (TUSS + TISS)
- **Auditoria médica** (revisão prontuário pós-procedimento)
- **Regulação:** porta de entrada, central regulação

## Templates
1. Protocolo de autorização prévia (decision tree)
2. Auditoria médica concorrente vs retrospectiva
3. Scorecard prestador (qualidade + custo)
4. Programa gestão crônicos (DM, HAS, insuficiência cardíaca)
5. Análise de sinistralidade + projeção atuarial

## Métricas
- **Sinistralidade:** custo assistencial / receita
- **Frequência:** eventos/beneficiário/ano
- **Custo médio:** R$/evento
- **Auditoria denial rate:** % autorizações negadas
- **NPS beneficiário**

## Cross-references
- [[medik-ans-compliance]] · [[medik-claim-management]] · [[medik-rcm-revenue-cycle]]
