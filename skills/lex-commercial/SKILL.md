---
name: lex-commercial
description: Direito Empresarial Brasileiro. Contratos B2B, distribuição, agência, franquia, representação comercial, Lei da Liberdade Econômica. Triggers em "contrato comercial", "B2B", "distribuição", "franquia", "agência", "representação comercial", "liberdade econômica".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "CC livro II (Direito de Empresa, arts. 966-1195)"
  - "Lei 8.955/94 (Franquia Empresarial)"
  - "Lei 4.886/65 (Representação Comercial)"
  - "Lei 13.874/19 (Liberdade Econômica)"
  - "Lei 6.404/76 (S.A. — coordenar com lex-corporate)"
templates_count: 25
---

# LEX-COMMERCIAL — Direito Empresarial

Skill especializada em contratos e operações empresariais BR. Análise + redação + revisão sob CC livro II + leis especiais.

## Quando usar
- Contratos B2B (fornecimento, distribuição, agência, representação)
- Contratos de franquia (Lei 8.955/94)
- Acordos de confidencialidade (NDA) empresariais
- Cláusulas de não-concorrência (validade + enforceability)
- Contratos de software/SaaS empresarial
- Cláusulas de change of control
- Acordos de exclusividade territorial
- Joint ventures (não-societárias)
- Operações regidas pela Lei 13.874/19 (Liberdade Econômica)

## Templates (25)

### Contratos comerciais core (10)
1. Contrato de fornecimento
2. Contrato de distribuição
3. Contrato de representação comercial (Lei 4.886/65)
4. Contrato de franquia (com COF — Circular de Oferta)
5. Contrato de licenciamento comercial
6. NDA empresarial
7. Acordo de exclusividade
8. Contrato de software/SaaS B2B
9. Contrato de prestação de serviços empresariais
10. Acordo de não-concorrência (com análise validade)

### Operacional (8)
11. Memorando de entendimento (MOU)
12. Carta de intenções (LOI)
13. Term sheet comercial
14. Contrato de joint venture (não-societária)
15. Contrato de transferência de tecnologia
16. Contrato de agência
17. Cláusulas de hardship
18. Cláusulas de force majeure

### Análises (7)
19. Análise de risco contratual
20. Parecer sobre cláusula de não-concorrência
21. Análise change of control
22. Parecer sobre cláusula penal (validade + razoabilidade)
23. Análise de cláusula compromissória (arbitragem)
24. Parecer Liberdade Econômica (atos abusivos)
25. Due diligence contratual

## Compliance built-in
✓ OAB 205 ✓ LGPD ✓ cite_check ✓ privilege_marker ✓ audit_oab

## Cross-references
- [[lex-corporate]] — para questões societárias (S.A./LTDA)
- [[lex-civil]] — para fundamentos obrigações
- [[lex-lgpd]] — para cláusulas LGPD em B2B
- [[lex-ip]] — para licenciamento IP

## Workflow típico

```
Input: contrato draft ou descrição da operação
→ Análise: legalidade + boa-fé + função social
→ Output: red-line revision + parecer + recomendações
→ Compliance: cite_check + OAB 205 + LGPD marker
```


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-commercial** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-commercial:**

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
