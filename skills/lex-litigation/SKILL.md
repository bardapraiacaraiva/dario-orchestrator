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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-litigation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-litigation:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
