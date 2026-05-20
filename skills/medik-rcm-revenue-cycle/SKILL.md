---
name: medik-rcm-revenue-cycle
description: Revenue Cycle Management — autorização → produção → faturamento → recebimento. Triggers em "RCM", "revenue cycle", "ciclo receita hospitalar", "gestão financeira hospital", "DSO healthcare".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, audit_trail]
jurisdiction: Brasil
---

# MEDIK-RCM-REVENUE-CYCLE

## Quando usar
- Diagnóstico de ciclo de receita (DSO alto? glosa alta?)
- Setup RCM em greenfield (hospital novo)
- Automação de faturamento (TISS)
- Negociação de tabela com operadora
- Programa de redução de glosas

## Stages
```
1. Pre-service:    autorização + elegibilidade + estimativa
2. Service:        captura clínica + codificação
3. Faturamento:    TUSS/TISS submission
4. Adjudication:   operadora análise + glosa
5. Recurso:        re-submission + auditoria
6. Recebimento:    payment posting + reconciliation
```

## Métricas
- **DSO (Days Sales Outstanding):** dias para receber
- **Glosa rate:** % faturado glosado
- **Net collection rate:** % recebido / faturado líquido
- **Denied claim rate:** % primária negada
- **A/R aging:** distribuição idade contas a receber

## Templates
1. RCM workflow end-to-end (BPMN)
2. Glosa root cause analysis
3. Programa de redução de glosas (causas top-10)
4. DSO improvement playbook
5. KPI dashboard RCM

## Cross-references
- [[medik-medical-billing-tuss]] · [[medik-claim-management]] · [[demeter-bi-dashboard]]
