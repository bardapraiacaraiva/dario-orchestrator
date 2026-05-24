---
name: lex-administrativo
description: Direito Administrativo Brasileiro. Lei 14.133/21 (NLLC), Lei 9.784/99, contratos públicos, licitações, TCU, processo administrativo. Triggers em "licitação", "contrato administrativo", "NLLC", "Lei 14133", "TCU", "concessão", "PPP", "processo administrativo", "improbidade", "Fazenda Pública".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "Lei 14.133/21 (Nova Lei de Licitações e Contratos — NLLC)"
  - "Lei 8.987/95 (Concessões)"
  - "Lei 11.079/04 (PPPs)"
  - "Lei 9.784/99 (Processo Administrativo Federal)"
  - "Lei 8.429/92 (Improbidade Administrativa)"
  - "Lei 12.846/13 (Anticorrupção)"
templates_count: 25
---

# LEX-ADMINISTRATIVO — Direito Administrativo

## Quando usar
- Participação em licitações (NLLC Lei 14.133/21)
- Impugnações + recursos administrativos
- Contratos administrativos
- Concessões e PPPs
- Processo administrativo sancionador
- Ações de improbidade (defesa ou propositura)
- Mandado de segurança contra autoridade pública
- Recursos administrativos (Lei 9.784/99)
- Anti-corrupção (Lei 12.846/13)
- Pareceres jurídicos para Fazenda Pública (CGU, AGU, PGE, PGM)

## Templates (25)

### Licitações & contratos (10)
1. Impugnação a edital de licitação
2. Recurso administrativo em licitação
3. Mandado de segurança contra licitação
4. Defesa em processo sancionador administrativo
5. Contrato administrativo (modelo NLLC)
6. Aditivo contratual (objeto, valor, prazo)
7. Termo de rescisão administrativa
8. Análise de equilíbrio econômico-financeiro
9. Pedido de reequilíbrio contratual
10. Recurso ao TCU

### Improbidade & anticorrupção (8)
11. Defesa em ação de improbidade
12. Acordo de não-persecução cível
13. Acordo de leniência (Lei 12.846/13)
14. Programa de integridade (compliance Lei 12.846)
15. Defesa em PAR (Processo Administrativo de Responsabilização)
16. Investigação interna anti-corrupção (privilege marker auto)
17. Whistleblowing channel — política
18. Due diligence integridade (parceiros)

### Concessões & PPPs (3)
19. Contrato de concessão comum
20. Contrato de PPP (patrocinada/administrativa)
21. Pedido de equilíbrio econômico-financeiro em concessão

### Processo administrativo (4)
22. Recurso administrativo (Lei 9.784/99)
23. Reclamação ao TCU
24. Representação ao MP
25. Defesa em consulta pública (manifestação)

## NLLC Lei 14.133/21 — Mudanças críticas (vs Lei 8.666/93 revogada)
- **Modalidades:** pregão (preferencial), concorrência, concurso, leilão, diálogo competitivo
- **Tipos:** menor preço, melhor técnica, técnica e preço, maior desconto, maior retorno econômico
- **Critérios:** sustentabilidade, inovação, equilíbrio
- **Sistema de Registro de Preços (SRP):** ampliado
- **Diálogo competitivo:** novidade para contratações complexas
- **Compliance:** programa de integridade obrigatório em obras > R$ 200M
- **Vigência plena:** abr/2024 (transição gradual)

## Cross-references
- [[lex-litigation]] — peças processuais
- [[lex-tributario]] — execução fiscal (Fazenda Pública)
- [[lex-regulatorio]] — concessões em sectores regulados
- [[lex-corporate]] — compliance Lei 12.846 corporativo


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-administrativo** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-administrativo:**

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
