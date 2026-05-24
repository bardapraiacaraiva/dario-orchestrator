---
name: lex-familia
description: Direito de Família e Sucessões Brasileiro. CC livro IV, Lei do Divórcio, alimentos, guarda, união estável, partilha, inventários. Triggers em "divórcio", "guarda", "alimentos", "partilha", "inventário", "união estável", "pensão alimentícia", "casamento", "regime de bens", "tutela", "curatela".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, privilege_marker, audit_oab]
legislation_primary:
  - "CC livro IV (Família, arts. 1.511-1.783)"
  - "CC livro V (Sucessões, arts. 1.784-2.027)"
  - "Lei 5.478/68 (Alimentos)"
  - "Lei 11.340/06 (Maria da Penha)"
  - "Lei 13.058/14 (Guarda Compartilhada)"
templates_count: 20
security_tier: 2
---

# LEX-FAMILIA — Família e Sucessões

Skill com alta sensibilidade — outputs frequentemente privilege marked.

## Quando usar
- Divórcio (consensual ou litigioso)
- Partilha de bens (com ou sem filhos)
- Pensão alimentícia (fixação, revisão, exoneração)
- Guarda (unilateral, compartilhada, alternada)
- Reconhecimento/dissolução união estável
- Investigação de paternidade
- Adoção
- Tutela/curatela
- Violência doméstica (Maria da Penha)
- Inventário (judicial ou extrajudicial)
- Testamento (público, particular, cerrado)
- Planejamento sucessório (com [[lex-tributario]] para impactos fiscais)

## Templates (20)

### Divórcio & união (6)
1. PI — divórcio consensual com partilha
2. PI — divórcio litigioso
3. PI — dissolução de união estável
4. Escritura pública de divórcio (extrajudicial)
5. Pacto antenupcial
6. Contrato de namoro (delimitação união estável)

### Alimentos (4)
7. PI — alimentos provisórios + definitivos
8. PI — revisão de alimentos
9. PI — exoneração de alimentos
10. Execução de alimentos (com prisão civil)

### Guarda & filiação (4)
11. PI — guarda unilateral
12. PI — guarda compartilhada (preferencial Lei 13.058/14)
13. PI — investigação de paternidade
14. PI — adoção (consensual ou litigiosa)

### Sucessões (4)
15. PI — inventário judicial
16. Escritura pública de inventário extrajudicial
17. Testamento público
18. Sobrepartilha

### Outros (2)
19. Medida protetiva Maria da Penha
20. Pedido de interdição (curatela)

## Princípios aplicados
- **Melhor interesse da criança** (CDC + ECA)
- **Igualdade entre cônjuges** (art. 226 §5º CF)
- **Convivência familiar** (ECA)
- **Função social da família**
- **Reconhecimento da união estável** (art. 1.723 CC)

## Regimes de bens
- **Comunhão parcial** (default desde 1977)
- **Comunhão universal**
- **Separação total**
- **Separação obrigatória** (art. 1.641 CC — > 70 anos)
- **Participação final nos aquestos** (raro)

## Maria da Penha (Lei 11.340/06)
- Medidas protetivas (urgência)
- Suspensão de posse/guarda armas
- Distanciamento (mínimo varia)
- Acompanhamento policial (mudança de residência)

## Compliance específico
- **Casos de família** = privilege marker AUTO (sensibilidade alta)
- **Dados de menores** = ZDR obrigatório
- **Outputs envolvendo violência doméstica** = privilege + audit reforçado
- Termos como "vítima", "agressor" usados conforme proteção da privacidade

## Cross-references
- [[lex-civil]] — sucessões + CC livro IV/V
- [[lex-criminal]] — violência doméstica (interface com Lei Maria da Penha)
- [[lex-tributario]] — ITCMD em planejamento sucessório
- [[lex-imobiliario]] — partilha de imóveis


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-familia** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-familia:**

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
