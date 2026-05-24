---
name: lex-imobiliario
description: Direito Imobiliário Brasileiro. Lei 8.245/91 (locação), 4.591/64 (condomínio + incorporação), 6.766/79 (parcelamento solo), Registro de Imóveis. Triggers em "locação", "aluguel", "condomínio", "incorporação", "compra e venda imóvel", "registro de imóvel", "due diligence imobiliária", "regularização", "loteamento".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "Lei 8.245/91 (Locação)"
  - "Lei 4.591/64 (Condomínio em Edificações + Incorporações)"
  - "Lei 6.766/79 (Parcelamento do Solo Urbano)"
  - "Lei 6.015/73 (Registros Públicos)"
  - "CC/2002 (livros relevantes — propriedade, posse)"
templates_count: 15
---

# LEX-IMOBILIARIO — Direito Imobiliário

## Quando usar
- Contratos de locação (residencial, comercial, temporada)
- Compra e venda de imóveis
- Incorporação imobiliária (memorial + registro)
- Análise de matrícula imobiliária
- Due diligence imobiliária (DD)
- Regularização fundiária urbana (REURB)
- Loteamento e desmembramento
- Despejo (ações)
- Cobrança de aluguel
- Condomínio (regimento, IPTU, taxas)

## Templates (15)

### Contratos (6)
1. Contrato locação residencial (Lei 8.245/91)
2. Contrato locação comercial (com garantia)
3. Contrato compra e venda (CCV) com escritura
4. Compromisso compra e venda (CCV — alienação fiduciária)
5. Contrato built to suit
6. Contrato de cessão de direitos hereditários sobre imóvel

### Ações imobiliárias (5)
7. Ação de despejo (falta de pagamento)
8. Ação renovatória
9. Ação revisional de aluguel
10. Ação de adjudicação compulsória
11. Ação de imissão na posse

### Documentos especializados (4)
12. Memorial de incorporação (Lei 4.591/64)
13. Due diligence imobiliária (checklist + relatório)
14. Pedido de regularização REURB
15. Análise de matrícula imobiliária

## Pontos críticos
- **Locação:** prazo mínimo 30 meses para resgate antecipado sem multa proporcional (art. 4º)
- **Compra/venda:** escritura pública obrigatória para valores > 30 salários mínimos (art. 108 CC)
- **Registro:** princípio da continuidade — cadeia dominial sem furos
- **Alienação fiduciária:** Lei 9.514/97 — procedimento extrajudicial de retomada (mais rápido)
- **Direito de preferência:** locatário tem (art. 27 Lei 8.245)

## Cross-references
- [[lex-civil]] — propriedade, posse (CC livros relevantes)
- [[lex-tributario]] — ITBI, ITCMD, IPTU
- [[lex-corporate]] — operações imobiliárias societárias (REIT/FII)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-imobiliario** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-imobiliario:**

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
