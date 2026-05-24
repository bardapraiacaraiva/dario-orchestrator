---
name: lex-ai-governance
description: Governança de IA e Marco Legal de Inteligência Artificial Brasileiro. PL 2338/2023, LGPD + IA, compliance algorítmico. Triggers em "Marco Legal IA", "PL 2338", "governança IA", "viés algorítmico", "IA generativa compliance", "deepfake", "AI governance".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "PL 2338/2023 (Marco Legal IA) — em tramitação"
  - "Lei 13.709/18 (LGPD) — art. 20 (decisão automatizada)"
  - "Resolução CNJ 332/2020 (IA no Judiciário)"
  - "AI Act EU 2024/1689 (comparativo)"
templates_count: 10
priority: emerging_demand
---

# LEX-AI-GOVERNANCE — Governança de IA

Compliance + framework para IA generativa, automatizada e algorítmica.

## Quando usar
- Análise risco regulatório uso de IA pelo cliente
- Implementação framework governança IA
- Resposta a DSR sobre decisão automatizada (art. 20 LGPD)
- Compliance Resolução CNJ 332/2020 (escritórios)
- Análise impacto PL 2338/2023 (quando aprovado)
- Cláusulas contratuais IA (em contratos com fornecedores AI)
- Política de uso de IA interno (do próprio escritório)
- Análise viés algorítmico (audit)
- Deepfake e direitos de imagem
- Direitos autorais output IA generativa

## Templates (10)
1. Política de uso de IA (corporativa)
2. Cláusulas contratuais IA (fornecedor)
3. RIPD específico para sistema IA
4. Framework de governança IA
5. Procedimento para resposta DSR art. 20 (decisão automatizada)
6. Checklist compliance Resolução CNJ 332/20
7. Análise de impacto algorítmico
8. Termo de uso de ferramenta IA (clientes/usuários)
9. Política interna anti-deepfake
10. Análise direitos autorais output IA

## PL 2338/2023 — Pontos-chave (em tramitação)
- Categorias de risco (inaceitável, alto, médio, baixo)
- Sistemas de **risco inaceitável:** social scoring, manipulação, vigilância em massa
- Sistemas de **alto risco:** decisões judiciais, contratação, crédito, saúde
- Obrigações para sistemas alto risco: documentação, supervisão humana, auditoria
- Sanções: até 2% do faturamento (similar LGPD)
- ANPD como autoridade competente (provisória)

## Art. 20 LGPD — Decisão automatizada
- Direito à **revisão humana** de decisões automatizadas
- Direito à **explicação** dos critérios da decisão
- Aplicável a: crédito, contratação, perfil, etc.

## Resolução CNJ 332/2020 — IA no Judiciário (relevante para escritórios)
- Modelos de IA usados pelo judiciário devem ser auditáveis
- Vedação a vieses discriminatórios
- Supervisão obrigatória de juiz
- Transparência sobre uso de IA em sentenças

## Cross-references
- [[lex-lgpd]] — art. 20 LGPD (decisão automatizada)
- [[lex-regulatorio]] — futura regulação ANPD sobre IA
- [[lex-ip]] — direitos autorais output IA
- [[lex-criminal]] — crimes envolvendo IA (deepfake, fraude algorítmica)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-ai-governance** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-ai-governance:**

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
