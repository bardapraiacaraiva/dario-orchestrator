---
name: medik-claim-management
description: Claim management — glosas, recursos, denials management, root cause analysis. Triggers em "glosa", "recurso glosa", "denial management", "auditoria operadora", "claim management".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [ans_regulatory, audit_trail]
jurisdiction: Brasil
---

# MEDIK-CLAIM-MANAGEMENT

## Quando usar
- Glosa rate alto (>10%)
- Recursos administrativos sistemáticos
- Auditoria de operadora pós-faturamento
- Disputa judicial procedimento negado
- Programa de redução de denials

## Tipos de glosa
- **Glosa técnica:** procedimento sem código TUSS válido
- **Glosa administrativa:** sem autorização, fora prazo
- **Glosa clínica:** auditor médico questiona indicação
- **Glosa contratual:** valor diferente do contratado

## Workflow recurso
```
1. Glosa recebida (operadora)
2. Análise root cause
3. Recurso documentado (laudo médico, prontuário, protocolo)
4. Re-submission via TISS
5. Decisão operadora
6. Se mantida: NIP ANS ou jurídico
```

## Templates
1. Recurso administrativo template (por tipo de glosa)
2. Root cause analysis 5-why
3. Programa preventivo de glosas (top-10 causas)
4. NIP ANS template
5. Petição inicial vs operadora (com lex-civil + lex-consumidor cross)

## Métricas
- **Glosa primária:** %
- **Recuperação após recurso:** %
- **Time to recovery:** dias
- **Net denial rate:** glosa - recovery

## Cross-references
- [[medik-rcm-revenue-cycle]] · [[medik-medical-billing-tuss]] · [[lex-consumidor]]
