---
name: lex-ip
description: Propriedade Intelectual Brasileira. Marcas, patentes, software, direitos autorais. INPI, Lei 9.279/96 (propriedade industrial), Lei 9.609/98 (software), Lei 9.610/98 (direitos autorais). Triggers em "marca", "patente", "INPI", "direito autoral", "software", "trade secret", "concorrência desleal", "registro de marca", "violação IP".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "Lei 9.279/96 (Propriedade Industrial — marcas, patentes, desenho industrial)"
  - "Lei 9.609/98 (Software)"
  - "Lei 9.610/98 (Direitos Autorais)"
  - "Lei 10.973/04 (Inovação)"
templates_count: 15
---

# LEX-IP — Propriedade Intelectual

Skill para marcas, patentes, software, direitos autorais e segredos comerciais.

## Quando usar
- Registro de marca (INPI)
- Defesa em oposição/processo administrativo INPI
- Depósito de patente
- Análise de viabilidade patentária
- Contratos de licenciamento (marca, patente, software, obra)
- Cessão de direitos IP
- Trade secret protection
- Defesa contra violação de IP
- Concorrência desleal
- Direitos autorais sobre código, design, conteúdo

## Templates (15)

### INPI procedimental (6)
1. Pedido de registro de marca
2. Manifestação em oposição (defesa do depositante)
3. Recurso ao Presidente do INPI
4. Pedido de depósito de patente (modelo de utilidade)
5. Manifestação em exigência INPI
6. Pedido de registro de desenho industrial

### Contratos IP (5)
7. Contrato de licenciamento de marca (royalty)
8. Contrato de licenciamento de software (SaaS)
9. Cessão de direitos autorais
10. Contrato de desenvolvimento de software (work for hire vs licença)
11. Acordo de trade secret + NDA reforçado

### Defesa & contencioso IP (4)
12. Notificação extrajudicial — violação de marca
13. Ação de busca e apreensão (Lei 9.279/96 art. 200)
14. Ação anulatória de registro
15. Ação por concorrência desleal (art. 195 Lei 9.279/96)

## Pontos-chave Lei 9.279/96 (Marcas)
- **Princípio da especialidade:** marca protege apenas no segmento registrado
- **Princípio do registro:** quem registra primeiro tem prioridade
- **Marca de alto renome:** proteção em todos os segmentos (art. 125)
- **Marca notória:** protegida em segmento próprio mesmo sem registro BR (art. 126)
- **Prazo:** 10 anos renováveis indefinidamente
- **Procedimento:** depósito → publicação RPI → 60 dias oposição → exame → decisão → recurso

## Software (Lei 9.609/98)
- Registro no INPI (opcional mas recomendável — facilita prova)
- Prazo: 50 anos
- Direitos morais NÃO inalienáveis (diferente da Lei 9.610/98)
- Engenharia reversa permitida em casos específicos
- **Output de IA** — debate atual sobre autoria (aguardando PL 2338)

## Direitos Autorais (Lei 9.610/98)
- **Direitos morais (inalienáveis):** paternidade, integridade, ineditismo, retirada
- **Direitos patrimoniais (alienáveis):** reprodução, distribuição, etc.
- **Prazo:** vida + 70 anos (heríderos)
- **Obra coletiva:** organizador detém direitos
- **Obra encomendada:** depende de cessão expressa (default = autor mantém)

## Cross-references
- [[lex-commercial]] — licenciamento comercial
- [[lex-corporate]] — IP em M&A (valuation + transferência)
- [[lex-ai-governance]] — output IA (autoria)
- [[lex-criminal]] — crime de violação IP (art. 184 CP)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-ip** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-ip:**

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
