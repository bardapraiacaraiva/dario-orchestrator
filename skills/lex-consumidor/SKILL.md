---
name: lex-consumidor
description: Direito do Consumidor Brasileiro (CDC). Ações consumidoristas, defesa empresa, recall, e-commerce, vícios e defeitos. Triggers em "consumidor", "CDC", "Código de Defesa do Consumidor", "Procon", "vício produto", "defeito serviço", "recall", "e-commerce", "publicidade enganosa".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "CDC Lei 8.078/90"
  - "Decreto 7.962/13 (Comércio Eletrônico)"
  - "Lei 14.181/21 (Superendividamento)"
  - "Resoluções SENACON"
templates_count: 20
---

# LEX-CONSUMIDOR — Direito do Consumidor

## Quando usar
- Ações consumidoristas (consumidor)
- Defesa empresarial em ações CDC
- Análise de cláusulas abusivas (art. 51 CDC)
- Recall de produtos (procedimentos)
- Compliance e-commerce (Decreto 7.962/13)
- Superendividamento (Lei 14.181/21)
- Publicidade abusiva/enganosa (arts. 36-37 CDC)
- Vícios e defeitos (arts. 18-25 CDC)
- Responsabilidade objetiva fornecedor (art. 14 CDC)
- Inversão ônus prova (art. 6º VIII CDC)

## Templates (20)

### Consumidor (10)
1. PI — vício de produto durável
2. PI — defeito de serviço (responsabilidade objetiva)
3. PI — danos morais consumeristas
4. PI — cláusula abusiva (declaratória)
5. PI — publicidade enganosa
6. PI — superendividamento (Lei 14.181/21)
7. PI — chargeback indevido (e-commerce)
8. PI — produto com vício oculto
9. PI — falha na prestação serviço (telecom, energia, água)
10. PI — repactuação dívida (superendividamento)

### Empresa (defesas) (7)
11. Defesa — responsabilidade subjetiva (não objetiva)
12. Defesa — caso fortuito/força maior
13. Defesa — uso indevido pelo consumidor
14. Defesa — culpa exclusiva do consumidor
15. Defesa em ação coletiva consumerista
16. Defesa em ação MP (legitimação)
17. Defesa Procon

### Compliance & procedimentos (3)
18. Procedimento de recall
19. Política e-commerce (Decreto 7.962/13)
20. Programa compliance consumerista

## Princípios CDC aplicados
- **Vulnerabilidade do consumidor** (art. 4º I)
- **Boa-fé objetiva** (art. 4º III)
- **Equilíbrio nas relações** (art. 4º III)
- **Responsabilidade objetiva fornecedor** (arts. 12, 14)
- **Inversão do ônus da prova** (art. 6º VIII — quando hipossuficiência ou verossimilhança)

## Cross-references
- [[lex-civil]] — responsabilidade civil base
- [[lex-litigation]] — peças processuais
- [[lex-commercial]] — contratos B2B (não confundir B2C com B2B)
- [[lex-lgpd]] — dados do consumidor


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-consumidor** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-consumidor:**

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
