---
name: lex-criminal
description: Direito Penal e Processual Penal Brasileiro. CP, CPP, Lei 13.964/19 (Anticrime), Lei 9.099/95 (Juizados Especiais), HC, defesa criminal. Triggers em "criminal", "penal", "habeas corpus", "denúncia", "defesa criminal", "júri", "tráfico", "anticrime", "JECRIM", "processo penal".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, privilege_marker, audit_oab]
legislation_primary:
  - "Código Penal (Decreto-Lei 2.848/40)"
  - "Código de Processo Penal (Decreto-Lei 3.689/41)"
  - "Lei 13.964/19 (Pacote Anticrime)"
  - "Lei 9.099/95 (Juizados Especiais Criminais)"
  - "Lei 11.343/06 (Drogas)"
  - "Lei 9.503/97 (Código de Trânsito Brasileiro — crimes de trânsito)"
templates_count: 25
security_tier: 1
priority: high_sensitivity
---

# LEX-CRIMINAL — Direito Criminal

Skill de **alta sensibilidade** — security_tier 1, privilege marker auto em quase tudo.

## Quando usar
- Defesa criminal em geral
- Habeas Corpus (preventivo, liberatório)
- Resposta à acusação (art. 396-A CPP)
- Alegações finais
- Recurso em sentido estrito
- Apelação criminal
- Júri (Tribunal do Júri — dolo contra a vida)
- Crime de trânsito
- Tráfico (Lei 11.343/06)
- ANPP (Acordo de Não Persecução Penal)
- Colaboração premiada (Lei 12.850/13)
- Crimes empresariais (Lei 12.846/13 + CP)
- Compliance criminal corporativo

## Templates (25)

### Defesa criminal (12)
1. Resposta à acusação
2. Defesa preliminar (júri)
3. Alegações finais (procedimento ordinário)
4. Memoriais (júri)
5. Pedido de revogação prisão preventiva
6. Pedido de liberdade provisória
7. HC liberatório
8. HC preventivo
9. Pedido de relaxamento de prisão
10. Pedido de revisão criminal
11. Pedido ANPP (Acordo Não Persecução Penal)
12. Manifestação em delação premiada

### Recursos criminais (5)
13. Recurso em sentido estrito (RESE)
14. Apelação criminal
15. Embargos infringentes (júri)
16. Recurso especial criminal
17. Recurso extraordinário criminal

### Acusação (advocacia assistente) (3)
18. Queixa-crime (ação privada)
19. Habilitação como assistente de acusação
20. Petição em ação penal pública (assistente)

### Crimes específicos (5)
21. Defesa — tráfico de drogas (Lei 11.343/06)
22. Defesa — crime de trânsito (homicídio culposo)
23. Defesa — Lei Maria da Penha (cumulação)
24. Defesa — crimes empresariais (sonegação fiscal, lavagem)
25. Defesa — crimes contra honra (calúnia, difamação, injúria)

## Pontos críticos
- **Princípio da presunção de inocência** (art. 5º LVII CF)
- **Princípio do contraditório** (art. 5º LV CF)
- **In dubio pro reo**
- **Devido processo legal**
- **Vedação prova ilícita** (art. 5º LVI CF + art. 157 CPP)

## Pacote Anticrime (Lei 13.964/19)
- **ANPP** (Acordo Não Persecução Penal): para crimes sem violência, pena < 4 anos
- **Juiz das Garantias** (em implementação progressiva)
- **Banco de DNA criminal**
- **Confisco alargado de bens** (crime organizado)
- **Cadeia de custódia da prova**
- **Audiência de custódia em 24h**

## Lei 9.099/95 (JECRIM) — Infração de menor potencial ofensivo
- Pena máxima ≤ 2 anos
- Composição civil (extingue punibilidade)
- Transação penal
- Suspensão condicional do processo (art. 89 — pena mínima ≤ 1 ano)

## Compliance específico
- **PRIVILEGE MARKER AUTO em TUDO** — defesa criminal = sigilo máximo
- **Audit log expandido** — cada output registado com timestamp + advogado responsável
- **OAB 205 strict** — defesa criminal nunca sai sem revisão humana confirmada
- **ZDR obrigatório** — todos dados (CPF, RG, número processo) são sensíveis
- Tratamento de **vítima vs réu** com proteção dual de identidade

## Cross-references
- [[lex-litigation]] — peças genéricas (subsidiariamente)
- [[lex-corporate]] — crimes empresariais
- [[lex-tributario]] — crimes tributários (interface CP + CTN)
- [[lex-familia]] — Maria da Penha
- [[lex-ai-governance]] — crimes cibernéticos envolvendo IA


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-criminal** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-criminal:**

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
