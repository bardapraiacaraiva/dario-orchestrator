---
name: lex-regulatorio
description: Direito Regulatório setorial brasileiro. BACEN, CVM, ANVISA, ANATEL, ANEEL, ANP, ANS, ANTT. Análise normativos, defesas, programas compliance setoriais. Triggers em "regulatório", "BACEN", "CVM", "ANVISA", "ANATEL", "ANEEL", "ANS", "compliance regulatório", "agência reguladora", "resolução", "instrução normativa".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "Lei 13.848/19 (Lei das Agências Reguladoras)"
  - "Lei 9.784/99 (Processo Administrativo Federal)"
  - "Setoriais: Lei 4.595/64 (BACEN), Lei 6.385/76 (CVM), Lei 6.360/76 (ANVISA), etc."
templates_count: 20
---

# LEX-REGULATORIO — Direito Regulatório Setorial

Análise normativos + defesas + compliance em sectores regulados.

## Agências cobertas
- **BACEN** — instituições financeiras, fintechs, PIX
- **CVM** — mercado de capitais, fundos, criptoativos
- **ANVISA** — medicamentos, alimentos, cosméticos, dispositivos médicos
- **ANATEL** — telecomunicações, internet, dados móveis
- **ANEEL** — energia elétrica, geração distribuída
- **ANP** — petróleo, gás, biocombustíveis
- **ANS** — planos de saúde, OPS
- **ANTT** — transporte terrestre

## Quando usar
- Análise de impacto de novo normativo (RG, IN, RDC)
- Defesa em processo administrativo sancionador
- Pedido de anuência prévia (M&A em sector regulado)
- Adequação a obrigação regulatória
- Compliance setorial (programas estruturados)
- Recursos administrativos
- Mandado de segurança contra ato regulatório
- Consulta pública (manifestação)

## Templates (20)

### Documentos por sector (12)
1. Defesa BACEN — processo sancionador
2. Pedido autorização BACEN (operação cambial / instituição financeira)
3. Defesa CVM — Inquérito Administrativo
4. Termo de compromisso CVM
5. Petição ANVISA — registro/manutenção produto
6. Defesa ANVISA — auto de infração
7. Recurso ANATEL — multa
8. Pedido ANATEL — uso de espectro
9. Defesa ANEEL — consumidor
10. Manifestação consulta pública (qualquer agência)
11. Recurso administrativo (genérico Lei 9.784/99)
12. Mandado de segurança contra ato regulatório

### Compliance estrutural (5)
13. Programa de compliance BACEN (Resolução 4.658/18)
14. Programa de compliance CVM
15. Programa LGPD setorial (combinar com [[lex-lgpd]])
16. Programa anticorrupção setorial (Lei 12.846/13)
17. Política de relacionamento com regulador

### Documentos consultivos (3)
18. Parecer impacto regulatório novo normativo
19. Análise risco regulatório (sector específico)
20. Memo treinamento equipa sobre nova norma

## Compliance específico
- **BACEN/CVM:** outputs sobre operações financeiras → ZDR + privilege markers
- **ANVISA:** dados clínicos → ZDR obrigatório
- **Audit trail:** todas defesas e recursos administrativos → audit log com prazo de protocolo

## Workflow típico
```
1. Upload do normativo (RDC, RG, IN, etc.)
2. /lex-regulatorio:analise_impacto
3. Output:
   - Obrigação principal
   - Prazo de adequação
   - Penalidades por descumprimento
   - Checklist de implementação
   - Responsáveis por área
4. Validação por advogado (OAB 205)
```

## Cross-references
- [[lex-administrativo]] — processo administrativo geral
- [[lex-corporate]] — anuência regulatória em M&A
- [[lex-ai-governance]] — futura regulação IA pela ANPD/Marco Legal


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-regulatorio** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-regulatorio:**

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
