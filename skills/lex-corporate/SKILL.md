---
name: lex-corporate
description: Direito Societário e M&A Brasileiro. Lei 6.404/76 (S.A.), CC livro II, CVM, M&A operations, governance, acordos de acionistas. Triggers em "M&A", "fusão", "aquisição", "S.A.", "sociedade anônima", "acionistas", "governança", "due diligence", "estatuto social", "acordo de acionistas".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, privilege_marker, audit_oab]
legislation_primary:
  - "Lei 6.404/76 (S.A.)"
  - "CC livro II (sociedades empresárias)"
  - "Lei 11.638/07 (alterações contábeis)"
  - "Resoluções CVM (companhias abertas)"
  - "Lei 13.303/16 (Estatais)"
templates_count: 20
security_tier: 2
---

# LEX-CORPORATE — Societário & M&A

Skill especializada em direito societário, M&A e governança corporativa.

## Quando usar
- Constituição de S.A. ou LTDA
- Alterações estatutárias / contrato social
- Acordos de acionistas
- M&A: due diligence, term sheet, SPA, escrow
- Operações de fusão/cisão/incorporação
- Reestruturações societárias
- Governança corporativa (compliance Lei 13.303/16 para estatais)
- Operações CVM (companhias abertas)
- Drag-along, tag-along, right of first refusal

## Templates (20)

### Constituição & alteração (5)
1. Contrato social LTDA
2. Estatuto social S.A. fechada
3. Estatuto social S.A. aberta (CVM)
4. Alteração contratual LTDA
5. Reforma estatutária S.A.

### M&A operacional (8)
6. Memorando de entendimento (MOU) M&A
7. Carta de intenções (LOI)
8. Term sheet M&A
9. SPA (Stock Purchase Agreement)
10. APA (Asset Purchase Agreement)
11. Escrow agreement
12. Acordo de acionistas com drag-along/tag-along
13. Disclosure schedule

### Due diligence (4)
14. Checklist DD jurídica completa (multi-skill coordination)
15. Memorando DD trabalhista (coordenar com [[lex-trabalhista]])
16. Memorando DD tributário (coordenar com [[lex-tributario]])
17. Relatório issues consolidado

### Governance (3)
18. Política de governança corporativa
19. Regimento interno do conselho
20. Política de compliance anticorrupção (Lei 12.846/13)

## Compliance específico
- **Lei 12.846/13 (Anticorrupção):** programas de integridade obrigatórios
- **CVM:** companhias abertas seguem ICVMs específicas
- **LGPD:** transferência de dados em M&A (DPA específico)
- **CADE:** atos de concentração (notificação obrigatória se atingir thresholds)

## Output specials
- Outputs marcados como **estrategia_processual** ou **due_diligence_report** = privilege marker auto
- M&A docs sempre com ZDR active (dados sensíveis)

## Cross-references
- [[lex-trabalhista]] — DD trabalhista
- [[lex-tributario]] — DD fiscal
- [[lex-regulatorio]] — DD regulatório setorial
- [[lex-lgpd]] — transferência dados em M&A
- [[lex-commercial]] — contratos com cliente em DD


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-corporate** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-corporate:**

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
