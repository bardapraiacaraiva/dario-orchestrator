---
name: lex-litigation
description: Contencioso Cível Brasileiro. CPC/2015, peças processuais (petições iniciais, contestações, réplicas, embargos, recursos). Estratégia processual. Triggers em "petição inicial", "contestação", "recurso", "apelação", "embargos", "agravo", "STJ", "TJ", "CPC", "processo civil", "estratégia processual".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, privilege_marker, audit_oab]
legislation_primary:
  - "CPC/2015 (Lei 13.105/15)"
  - "Súmulas STJ (mais de 660)"
  - "Súmulas STF (incluindo vinculantes)"
  - "Regimentos Internos STF/STJ"
templates_count: 50
priority: critical_volume
---

# LEX-LITIGATION — Contencioso Cível

Skill core para peças processuais civis. Volume alto em escritórios.

## Quando usar
- Petição inicial (qualquer matéria civil/empresarial)
- Contestação
- Réplica
- Embargos de declaração
- Recursos (apelação, especial, extraordinário)
- Agravo de instrumento
- Mandado de segurança cível
- Habeas data
- Tutela provisória (urgência ou evidência)
- Cumprimento de sentença
- Embargos do devedor
- Estratégia processual (timing + provas + recursos)

## Templates (50)

### Petições iniciais (15)
1. PI — ação de cobrança
2. PI — ação revisional contrato
3. PI — ação de obrigação de fazer/não fazer
4. PI — ação rescisória
5. PI — ação monitória
6. PI — ação declaratória
7. PI — ação anulatória
8. PI — ação consignatória
9. PI — ação de prestação de contas
10. PI — ação reivindicatória
11. PI — ação cautelar (com tutela urgência)
12. PI — mandado de segurança individual
13. PI — habeas data
14. PI — ação civil pública (legitimação)
15. PI — ação popular

### Defesas (10)
16. Contestação genérica
17. Contestação com reconvenção
18. Contestação com denunciação à lide
19. Contestação com chamamento ao processo
20. Exceção de incompetência
21. Exceção de pré-executividade
22. Embargos do devedor (execução)
23. Embargos de terceiro
24. Impugnação ao cumprimento de sentença
25. Impugnação à assistência judiciária gratuita

### Recursos (15)
26. Apelação cível
27. Embargos de declaração
28. Embargos infringentes
29. Agravo de instrumento
30. Agravo interno
31. Recurso especial (STJ)
32. Recurso extraordinário (STF)
33. Recurso ordinário em MS
34. Recurso adesivo
35. Agravo em recurso especial
36. Embargos de divergência (STJ)
37. Agravo regimental
38. Reclamação constitucional
39. Recurso de revisão criminal (coordenar [[lex-criminal]])
40. Recurso eleitoral (TSE)

### Outros (10)
41. Pedido de tutela de urgência
42. Pedido de tutela de evidência
43. Impugnação ao valor da causa
44. Impugnação à gratuidade
45. Sustentação oral (memorial)
46. Petição interlocutória (manifestação)
47. Réplica
48. Tréplica
49. Memoriais finais
50. Petição de desistência

## Princípios processuais aplicados
- **Devido processo legal** (art. 5º LIV CF)
- **Contraditório e ampla defesa** (art. 5º LV CF)
- **Cooperação** (art. 6º CPC)
- **Boa-fé processual** (art. 5º CPC)
- **Primazia do julgamento de mérito** (art. 6º CPC)
- **Razoável duração do processo** (art. 5º LXXVIII CF)

## Súmulas STJ mais aplicadas (auto-aplicadas)
- **Súmula 7 STJ:** revisão de prova em REsp
- **Súmula 83 STJ:** divergência jurisprudencial
- **Súmula 130 STJ:** prescrição em ação rescisória
- **Súmula 211 STJ:** prequestionamento em REsp
- **Súmula 282/356 STF + Súmula 211 STJ:** prequestionamento

## Estratégia processual
- **Ordem de defesas:** preliminares → mérito → pedidos
- **Provas:** documental → testemunhal → pericial → inspeção
- **Recursos:** sempre considerar custo-benefício (depósito, sucumbência)
- **Timing:** ações urgentes → tutela; comuns → procedimento ordinário

## Compliance específico
- **Estratégia processual** = privilege marker auto
- **Memoriais a juízes** = revisão humana obrigatória (OAB 205 — bloqueado sem flag)
- **Cite check** obrigatório (Súmulas + leis citadas)
- **Prazos** validados via mcp-cnj-datajud (futuro) ou cálculo CPC (atualmente)

## Cross-references
- [[lex-civil]] — fundamentos materiais civis
- [[lex-trabalhista]] — peças específicas trabalhistas (CLT + CPC subsidiário)
- [[lex-tributario]] — peças tributárias (LEF + CPC)
- [[lex-administrativo]] — peças contra Fazenda Pública
- [[lex-criminal]] — peças criminais (CPP)
