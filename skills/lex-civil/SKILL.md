---
name: lex-civil
description: Análise e redação em Direito Civil Brasileiro. Contratos civis, responsabilidade civil (subjetiva e objetiva), obrigações, sucessões, posse e propriedade. Base CC/2002 (Lei 10.406/02). Triggers em "direito civil", "responsabilidade civil", "danos morais", "contrato civil", "sucessão", "inventário", "usucapião", "obrigação", "indenização", "código civil".
license: MIT
jurisdiction: Brasil
language: pt-br-formal
parent_agent: lex-br-director
compliance: [oab_205, lgpd, cite_check, audit_oab]
legislation_primary:
  - "CC/2002 (Lei 10.406/2002)"
  - "Lei 8.078/1990 (CDC, para relações de consumo)"
  - "Lei 11.340/2006 (Maria da Penha, para violência doméstica)"
  - "Lei 6.515/1977 (Divórcio)"
templates_count: 30
---

# LEX-CIVIL — Skill Direito Civil Brasileiro

Skill especializada em Direito Civil Brasileiro para o agente LEX-BR. Analisa, redige e revisa peças e documentos sob o Código Civil/2002 e leis civis especiais.

## Quando usar

- Análise de contratos civis (compra e venda, prestação de serviço, doação, etc.)
- Redação de pareceres sobre responsabilidade civil
- Cálculo e fundamentação de danos morais/materiais
- Questões sucessórias (inventários, partilhas, testamentos)
- Posse, propriedade, usucapião
- Obrigações em geral (mora, juros, multa)
- Casos envolvendo art. 186, 187 e 927 CC (responsabilidade)

## Output structure (padrão peça)

```
1. QUALIFICAÇÃO DAS PARTES
2. SÍNTESE DOS FATOS
3. FUNDAMENTAÇÃO JURÍDICA
   3.1 Dispositivos legais aplicáveis (CC + leis especiais)
   3.2 Jurisprudência relevante (STJ + TJs — via mcp-jusbrasil quando disponível)
   3.3 Doutrina (citações de autores consolidados)
4. CONCLUSÃO
5. PEDIDOS (se aplicável)
6. PROVAS (rol)
```

## Princípios civis-chave aplicados

- **Função social do contrato** (art. 421 CC)
- **Boa-fé objetiva** (art. 422 CC)
- **Vedação ao enriquecimento sem causa** (art. 884 CC)
- **Responsabilidade objetiva em atividades de risco** (art. 927, parágrafo único CC)
- **Lesão e estado de perigo** (arts. 156, 157 CC)
- **Proteção ao consumidor** (CDC quando aplicável — encaminhar para [[lex-consumidor]])

## Templates incluídos (30)

### Contratos (10)
1. Contrato de compra e venda (móvel)
2. Contrato de compra e venda (imóvel — coordenar com [[lex-imobiliario]])
3. Contrato de prestação de serviços
4. Contrato de mútuo
5. Contrato de comodato
6. Contrato de depósito
7. Contrato de transporte
8. Contrato de doação
9. Contrato de mandato
10. Contrato de gestão de negócios

### Responsabilidade civil (8)
11. Petição inicial — danos morais (acidente)
12. Petição inicial — danos morais (calúnia/injúria/difamação online)
13. Petição inicial — danos materiais (defeito de produto/serviço)
14. Petição inicial — responsabilidade civil estado (art. 37 §6º CF)
15. Defesa em ação de responsabilidade civil
16. Réplica em ação de responsabilidade civil
17. Parecer sobre responsabilidade objetiva
18. Cálculo de indenização (parâmetros Súmula 387 STJ)

### Sucessões (6)
19. Petição inicial de inventário judicial
20. Inventário extrajudicial (escritura pública)
21. Testamento público
22. Testamento particular
23. Sobrepartilha
24. Renúncia à herança

### Outros (6)
25. Ação de usucapião (extraordinária — art. 1238 CC)
26. Ação possessória (reintegração de posse)
27. Ação reivindicatória
28. Notificação extrajudicial (constituição em mora)
29. Parecer sobre obrigação solidária
30. Acordo extrajudicial

## Workflow

```
1. Input: descrição do caso + documentos relevantes
2. Análise:
   a) Identificar institutos civis aplicáveis
   b) Verificar prescrição (art. 205-206 CC)
   c) Validar capacidade das partes (art. 3-5 CC)
   d) Avaliar boa-fé objetiva
3. Output:
   a) Peça/parecer redigido em PT-BR formal
   b) Citações validadas via cite_checker
   c) Compliance OAB 205 + LGPD aplicados
   d) Marcação de privilege quando aplicável
4. Audit log automático em compliance_log/
```

## Compliance built-in

- ✓ **OAB Provimento 205/2021** — outputs externos requerem revisão humana
- ✓ **LGPD** — rodapé operador automático
- ✓ **Cite checker** — valida todas as citações de art./lei
- ✓ **Privilege marker** — pareceres marcam sigilo cliente-advogado
- ✓ **ZDR** — dados sensíveis (CPF, processos) requerem ZDR active
- ✓ **Audit trail** — log imutável de cada uso

## Limitações

- **Jurisprudência STJ/TJs** requer mcp-jusbrasil (status: planned). Enquanto não disponível, advogado faz upload manual de acórdãos relevantes.
- **Análise de provas técnicas** (perícias) requer especialista — LEX-CIVIL identifica a necessidade mas não substitui o perito.
- **Direito de família** específico → encaminhar para [[lex-familia]]
- **Direito do consumidor** específico → encaminhar para [[lex-consumidor]]
- **Direito imobiliário** específico → encaminhar para [[lex-imobiliario]]

## Cross-references

- [[lex-litigation]] — para peças processuais civis (CPC/2015)
- [[lex-commercial]] — para contratos empresariais
- [[lex-consumidor]] — para relações de consumo
- [[lex-familia]] — para direito de família/sucessões
- [[lex-imobiliario]] — para questões imobiliárias

## Modelo de invocação

```
/lex-civil:analise_contrato <upload do contrato>
/lex-civil:redige_peticao_inicial <descrição do caso>
/lex-civil:parecer_responsabilidade_civil <fatos>
/lex-civil:calcula_indenizacao <natureza do dano + base de cálculo>
```

## Standards de qualidade

- Score mínimo de release: **75/100** (calibrado adaptive_rubric)
- σ máximo nas dimensões: **0.20**
- Confidence level: **HIGH ou MEDIUM** (LOW automaticamente vira REVIEW)
- Cite check: **PASS obrigatório** (nenhuma citação inválida)
- Linguagem: PT-BR formal, sem anglicismos, sem coloquialismos


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **lex-civil** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in lex-civil:**

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
