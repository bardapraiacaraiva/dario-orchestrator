---
name: diva-budget
description: Construction budget estimation for architecture and renovation projects in Portugal. Uses ProNIC/LNEC reference prices. Breakdown by demolition, structure, masonry, MEP, finishes, carpentry, equipment, fees, and contingency. Includes IVA analysis (6% rehab vs 23%). Cost/m2 ranges for 2026. Triggers on "orcamento", "budget", "quanto custa", "custo obra", "preco remodelacao", "custo m2".
license: MIT
---

# DIVA Skill — Construction Budget Estimation

Produces detailed construction budget estimates for Portuguese projects using ProNIC/LNEC reference pricing, real market rates for 2026, and proper IVA tax analysis. Breaks down costs by work chapter, identifies cost drivers, and flags budget-scope misalignments before they become problems on site.

## When to activate

Invoke `/diva-budget` (or trigger automatically) when:
- User asks "how much will this cost" for any construction/renovation
- User needs a budget estimate before engaging a contractor
- User wants to validate a contractor's quote
- User asks about cost per m2 for renovation types
- User needs to understand IVA implications (6% vs 23%)
- After `diva-floor-plan` and `diva-materials` define scope and specs

Do NOT use when:
- User needs engineering calculations (structural, MEP sizing)
- User wants contractor recommendations (not a budget skill)
- Project has no defined scope (do `diva-diagnose` first)

## Workflow

### 1. Gather budget inputs
From previous DIVA skills or user input:
- **Project scope:** from `diva-diagnose` or description
- **Area:** total m2 and useful m2
- **Layout changes:** from `diva-floor-plan` (walls to demolish/build, plumbing moves)
- **Material tier:** from `diva-materials` (economico/recomendado/premium)
- **Property age:** affects demolition complexity and surprises
- **Location:** Lisbon/Porto premium vs rest of country
- **Access conditions:** elevator? stairs? narrow streets? (affects labor cost)
- **Timeline:** rush premium if compressed schedule

If key inputs are missing, request them before estimating.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "construction costs portugal 2026 renovation price m2", limit: 5)
mcp__dario-rag__search_kb(query: "ProNIC LNEC reference prices construction chapters", limit: 5)
mcp__dario-rag__search_kb(query: "IVA 6% reabilitacao urbana ARU portugal", limit: 5)
```

### 3. Cost/m2 reference ranges (2026 Portugal)
Base reference ranges (all-in construction cost, excluding fees and furniture):

**Renovation:**
| Scope | EUR/m2 (national) | EUR/m2 (Lisboa/Porto) |
|---|---|---|
| Cosmetic refresh (pintura, pavimento, louca) | 200-400 | 250-500 |
| Medium renovation (+ cozinha, WC, eletrica parcial) | 500-800 | 600-1,000 |
| Full gut (tudo novo, redistribuicao) | 800-1,200 | 1,000-1,500 |
| Premium gut (materiais topo, domonica) | 1,200-2,000 | 1,500-2,500 |
| Heritage/restoration (pombalino, patrimonio) | 1,500-3,000 | 1,800-3,500 |

**New construction:**
| Type | EUR/m2 |
|---|---|
| Standard moradia | 1,200-1,800 |
| Premium moradia | 1,800-2,800 |
| Luxury/architect | 2,500-4,000+ |

Adjust for:
- +10-15% if poor access (centro historico, sem elevador, ruas estreitas)
- +10-20% if compressed timeline (<3 months for medium renovation)
- +15-25% for buildings pre-1940 (surprises, complexity)
- -5-10% for larger areas (>150m2, economies of scale)

### 4. Chapter-by-chapter breakdown (ProNIC structure)
Estimate each chapter as percentage of total AND absolute value:

| Cap | Capitulo | % Typical | Notes |
|---|---|---|---|
| 1 | Estaleiro e trabalhos preparatorios | 3-5% | Containers, protecoes, licencas camararias |
| 2 | Demolicoes e remocoes | 5-10% | Depends on scope, asbestos adds 30-50% to this chapter |
| 3 | Estrutura e fundacoes | 0-15% | 0% if no structural work, 15%+ if reinforcement needed |
| 4 | Alvenarias e divisorias | 5-8% | Tijolo, gesso cartonado (pladur), isolamento |
| 5 | Impermeabilizacoes e isolamentos | 3-5% | WC, cobertura, fachada |
| 6 | Revestimentos exteriores | 0-8% | Facade work if applicable |
| 7 | Revestimentos interiores — paredes | 8-12% | Ceramica, pintura, papel, paineis |
| 8 | Revestimentos interiores — pavimentos | 8-12% | Madeira, ceramica, pedra, betonilhas |
| 9 | Revestimentos interiores — tetos | 3-5% | Teto falso, pintura, estucagem |
| 10 | Caixilharia exterior | 5-10% | Janelas, portas exteriores, estores |
| 11 | Caixilharia interior | 3-5% | Portas interiores, armarios embutidos |
| 12 | Instalacoes eletricas | 8-12% | Quadro, cablagem, pontos de luz, tomadas, dados |
| 13 | Instalacoes hidrosanitarias | 6-10% | Agua, esgotos, louca, torneiras |
| 14 | AVAC | 3-8% | Ar condicionado, ventilacao, aquecimento |
| 15 | Instalacao de gas | 1-2% | Se aplicavel |
| 16 | Carpintarias e marcenarias | 5-10% | Cozinha, roupeiros, movel WC |
| 17 | Equipamentos sanitarios | 3-5% | Louca, cabine duche, banheira |
| 18 | Diversos | 2-3% | Limpeza final, testes, certificacoes |

### 5. Additional costs beyond construction
Always include these in the total project budget:

| Item | % or Value | Notes |
|---|---|---|
| Projeto de arquitectura | 5-10% of construction | Depends on complexity, min ~3,000-5,000 EUR |
| Projetos de especialidades | 3-5% of construction | Estabilidade, redes (agua, esgoto, gas, eletrica, telecom, AVAC) |
| Fiscalizacao de obra | 2-4% of construction | Optional but recommended |
| Licenciamento CM | 500-3,000 EUR | Varies by municipality and scope |
| Certificado energetico | 200-500 EUR | Mandatory for venda/arrendamento |
| Mobiliario e decoracao | Variable | Can equal construction cost in premium projects |
| Contingencia | 10-15% | MANDATORY — never present budget without it |
| IVA | 6% or 23% | See IVA analysis below |

### 6. IVA analysis (critical for Portugal)
**IVA a 6% — when applicable:**
- Property located in ARU (Area de Reabilitacao Urbana)
- Construction >30 years old
- Work classified as "reabilitacao" (not just maintenance)
- Empreiteiro fatura com IVA 6% (verba 2.23/2.24 da Lista I do CIVA)
- Applies to: mao-de-obra + materiais incorporados
- Does NOT apply to: materiais comprados separadamente, mobiliario, eletrodomesticos

**IVA a 23% — standard rate:**
- New construction
- Properties outside ARU or <30 years old
- Separate material purchases
- Furniture and appliances
- Professional fees (arquitecto, engenheiro)

**Impact calculation:**
For a 100,000 EUR renovation:
- With IVA 6%: 106,000 EUR total
- With IVA 23%: 123,000 EUR total
- **Savings: 17,000 EUR (17%)**

Always check ARU status at the relevant Camara Municipal.

### 7. Payment schedule (typical PT market)
Standard construction payment milestones:
| Fase | % | Momento |
|---|---|---|
| Adiantamento | 10-15% | Assinatura do contrato |
| Demolicoes concluidas | 15-20% | Apos demolicoes e remocoes |
| Infraestruturas (1a fix) | 20-25% | Eletrica, canalização, AVAC embutidos |
| Acabamentos (2a fix) | 25-30% | Revestimentos, louca, carpintarias |
| Conclusao | 10-15% | Apos snag list e correcoes |
| Retencao | 5% | 6-12 meses apos conclusao (garantia) |

### 8. Budget validation checks
Before presenting:
- Total aligns with cost/m2 reference range for this scope?
- Individual chapters within normal percentage ranges?
- Contingency included (10-15%)?
- IVA correctly applied?
- Fees and licensing included?
- No major scope items missing?
- Budget-scope-quality triangle is realistic?

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-budget
area_m2: <number>
scope: <cosmetic|medium|full-gut|premium|new-build>
material_tier: <economico|recomendado|premium>
iva_rate: <6%|23%|mixed>
---

# Orcamento Estimativo DIVA — <Client/Property>

## Resumo
| Parametro | Valor |
|---|---|
| Area util | X m2 |
| Ambito | <scope> |
| Custo/m2 estimado | X - Y EUR |
| Tier de materiais | <tier> |
| IVA aplicavel | X% |
| **Custo total estimado** | **X - Y EUR** |

## Premissas
- <key assumptions that affect the estimate>
- <material tier selected>
- <access conditions>
- <timeline assumptions>

## Mapa de Quantidades por Capitulo

### Construcao
| Cap | Descricao | % | Valor estimado EUR |
|---|---|---|---|
| 1 | Estaleiro e preparatorios | X% | X,XXX |
| 2 | Demolicoes e remocoes | X% | X,XXX |
| 3 | Estrutura e fundacoes | X% | X,XXX |
| 4 | Alvenarias e divisorias | X% | X,XXX |
| 5 | Impermeabilizacoes | X% | X,XXX |
| 6 | Revestimentos exteriores | X% | X,XXX |
| 7 | Revestimentos paredes | X% | X,XXX |
| 8 | Revestimentos pavimentos | X% | X,XXX |
| 9 | Tetos | X% | X,XXX |
| 10 | Caixilharia exterior | X% | X,XXX |
| 11 | Caixilharia interior | X% | X,XXX |
| 12 | Instalacoes eletricas | X% | X,XXX |
| 13 | Instalacoes hidrosanitarias | X% | X,XXX |
| 14 | AVAC | X% | X,XXX |
| 15 | Gas | X% | X,XXX |
| 16 | Carpintarias | X% | X,XXX |
| 17 | Equipamentos sanitarios | X% | X,XXX |
| 18 | Diversos | X% | X,XXX |
| | **Subtotal construcao** | **100%** | **XX,XXX** |

### Custos adicionais
| Item | Valor EUR |
|---|---|
| Projeto de arquitectura | X,XXX |
| Especialidades | X,XXX |
| Fiscalizacao | X,XXX |
| Licenciamento | X,XXX |
| Certificado energetico | XXX |
| **Subtotal adicional** | **X,XXX** |

### Contingencia
| Item | % | Valor EUR |
|---|---|---|
| Contingencia (imprevistos) | 10-15% | X,XXX |

### IVA
| Base | Taxa | Valor EUR |
|---|---|---|
| Construcao (se ARU) | 6% | X,XXX |
| Honorarios | 23% | X,XXX |
| Materiais avulso | 23% | X,XXX |
| **Total IVA** | | **X,XXX** |

## Total do Investimento
| Componente | Min EUR | Max EUR |
|---|---|---|
| Construcao | ... | ... |
| Custos adicionais | ... | ... |
| Contingencia | ... | ... |
| IVA | ... | ... |
| **TOTAL** | **XX,XXX** | **XX,XXX** |

### Exclusoes
- Mobiliario solto e decoracao
- Eletrodomesticos (exceto encastre se incluido)
- Jardim e paisagismo (se aplicavel)
- <other exclusions>

## Analise IVA
### Elegibilidade IVA 6%
- ARU: <sim/nao — verificar na CM>
- Idade do imovel: <anos>
- Tipo de obra: <reabilitacao/manutencao/nova>
- **Poupanca estimada com IVA 6%:** X,XXX EUR

## Calendario de Pagamentos
| Fase | % | Valor EUR | Momento |
|---|---|---|---|
| Adiantamento | 10% | X,XXX | Assinatura contrato |
| Demolicoes | 20% | X,XXX | Conclusao demolicoes |
| 1a fix | 25% | X,XXX | Infraestruturas embutidas |
| 2a fix | 25% | X,XXX | Acabamentos |
| Conclusao | 15% | X,XXX | Snag list resolvida |
| Retencao | 5% | X,XXX | 6-12 meses apos |

## Riscos Orcamentais
| Risco | Impacto potencial | Mitigacao |
|---|---|---|
| Surpresas estruturais | +10-30% cap. 3 | Inspecao previa detalhada |
| Aumento preco materiais | +5-10% total | Comprar/reservar cedo |
| Atrasos licenciamento | Custo tempo | Submeter cedo, expediente |
| Alteracoes em obra | +15-25% total | Briefing robusto, decisoes antes |

## Proximos Passos
- [ ] Verificar elegibilidade IVA 6% na Camara Municipal
- [ ] Solicitar 3 orcamentos a empreiteiros com base neste mapa
- [ ] Definir materiais finais com `diva-materials` se ainda nao feito
- [ ] Assegurar contingencia no financiamento
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Orcamento DIVA.md`

## Red Flags
- Never skip ProNIC reference codes when itemizing chapters — without ProNIC the budget cannot be cross-checked against contractor quotes or LNEC benchmarks
- Never forget the IVA split analysis (6% rehabilitation vs 23% standard) — the 17-point difference on a 100k obra is 17,000 EUR the client either saves or loses
- Always include a contingency line of 10-15% (15-20% for pre-1940 buildings) — Portuguese renovation sites routinely uncover hidden structural issues, asbestos, or outdated wiring
- Never produce a budget estimate without a floor plan or measured survey — area guesses can swing costs by 30-50% and destroy credibility
- Always present min-max ranges, never a single number — Portuguese construction prices vary widely by region, season, and contractor availability
- Never omit professional fees (arquitecto, engenheiro, fiscalizacao, licenciamento) from the total — clients who only see the construction line get blindsided by 15-20% in additional costs

## Interactions
- Usually follows `diva-diagnose` (scope) + `diva-floor-plan` (layout) + `diva-materials` (specs)
- Can be used standalone for quick "quanto custa" estimates
- Feeds into `dario-proposal` for commercial proposals to clients
- Save via `dario-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Inputs capturados antes de estimar

- [ ] Área em m2 confirmada (útil + bruta) — não estimada vagamente
- [ ] Scope categorizado num dos 5 níveis da tabela (cosmetic/medium/full gut/premium/heritage)
- [ ] Localização definida (Lisboa/Porto premium vs resto do país)
- [ ] Tier de materiais identificado (económico/recomendado/premium)
- [ ] Condições de acesso avaliadas (elevador, ruas estreitas, andar)

❌ NOT delivery-ready: "Apartamento em Lisboa, remodelação completa, cerca de 80m2"
✅ Delivery-ready: "Apartamento T2, 78m2 úteis, Mouraria (ARU), pré-1940, acesso por escadas estreitas, sem elevador, materiais recomendados, full gut com redistribuição de paredes"

---

### Gate 2 — Breakdown por capítulo ProNIC preenchido

- [ ] Todos os capítulos aplicáveis têm % E valor absoluto em EUR
- [ ] Capítulos a 0% estão explicados ("Cap. 3 — Estrutura: 0% — sem trabalhos estruturais previstos")
- [ ] Percentagens somam 100% da componente construção
- [ ] Capítulos com risco elevado estão sinalizados (e.g., asbestos em Cap. 2, reforço estrutural em Cap. 3)

❌ NOT delivery-ready: "Instalações eléctricas: ~10%, canalizações: ~8%"
✅ Delivery-ready: "Cap. 12 — Instalações eléctricas: 10% → 7.800 EUR (quadro novo, 18 circuitos, 42 pontos de luz/tomadas, dados CAT6)"

---

### Gate 3 — Custos adicionais além da construção incluídos

- [ ] Projeto de arquitectura cotado (% ou valor mínimo 3.000-5.000 EUR)
- [ ] Projetos de especialidades incluídos (estabilidade, redes, AVAC)
- [ ] Contingência de 10-15% presente e visível como linha separada
- [ ] Licenciamento CM com valor estimado (500-3.000 EUR conforme município)
- [ ] Certificado energético incluído se relevante (200-500 EUR)

❌ NOT delivery-ready: "A estes valores acresce IVA e outros custos."
✅ Delivery-ready: "Contingência (12%): 9.360 EUR | Projeto arq. + especialidades: 6.500 EUR | Licenciamento CML: 1.200 EUR | Cert. energético: 350 EUR"

---

### Gate 4 — Análise IVA correcta e fundamentada

- [ ] IVA a 6% só aplicado se ARU confirmada E imóvel >30 anos E empreiteiro certificado
- [ ] IVA a 23% aplicado a mobiliário, equipamentos e honorários (mesmo em ARU)
- [ ] Impacto financeiro calculado em valor absoluto (diferença 6% vs 23%)
- [ ] Recomendação explícita ao cliente: confirmar elegibilidade ARU na CM antes de adjudicar

❌ NOT delivery-ready: "Se estiver em ARU aplica-se IVA reduzido de 6%."
✅ Delivery-ready: "Morada em ARU Lisboa (Mouraria, Resolução CM nº X/2021): IVA construção 6% → 4.680 EUR. A 23% seriam 17.940 EUR. Poupança potencial: 13.260 EUR. Confirmar elegibilidade com empreiteiro certificado INCI antes de contrato."

---

### Gate 5 — Ajustes e flags de risco explícitos

- [ ] Ajuste de localização aplicado e justificado (+10-15% acesso difícil, +15-25% pré-1940)
- [ ] Pelo menos 1 flag de risco orçamental identificado (asbestos, surpresas estruturais, prazo comprimido)
- [ ] Range apresentado (mínimo–máximo) com justificação dos extremos
- [ ] Alinhamento scope/budget verificado — se budget insuficiente para scope, dito claramente

❌ NOT delivery-ready: "Pode haver custos imprevistos. O orçamento é indicativo."
✅ Delivery-ready: "⚠️ RISCO: Edifício 1923 → probabilidade de asbestos em soalho/estuques. Se confirmado: +3.500-6.000 EUR (Cap. 2 demolições +35%). Reservar na contingência. Recomendar peritagem prévia."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem placeholders entre `< >`

- [ ] Nome do cliente/projecto no cabeçalho do orçamento
- [ ] Morada real ou referência de localização concreta
- [ ] Valores em EUR com casas decimais ou arredondamento consistente (não "~€X")
- [ ] Zero instâncias de `[INSERIR]`, `<endereço>`, `TBD`, `XX m2`, `N/A`
- [ ] Data de referência de preços indicada (e.g., "Preços de referência: Março 2026")

❌ NOT delivery-ready: "Orçamento para [NOME CLIENTE], apartamento em <localização>, área de XX m2."
✅ Delivery-ready: "Orçamento indicativo — Projecto Mouraria T2 | Cliente: Mariana Fonseca | Rua do Capelão 14, 3º Esq., Lisboa | 78 m2 úteis | Referência: ProNIC/LNEC, Março 2026"

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via ProNIC/LNEC, RAG KB, ou dados reais do projecto
- 🟡 **assumed** — plausível pelo contexto mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — estimativa por design (range calculado, não valor real verificável)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs o que precisa de verify antes de agir.  
**Honest transparency > orçamento inflado ou falsa precisão.**

---

❌ NOT delivery-ready:
> "Custo total estimado: €87.500. IVA a 6%. Demolições: €6.200. Caixilharia: €9.100."
→ Sem labels: cliente não sabe se os valores são ProNIC verified, se a área foi assumida, ou se IVA 6% se aplica mesmo ao projecto deles.

✅ Delivery-ready:
> - 🟢 **Custo total estimado: €82.000–€96.000** — projection baseada em 110m2 × €750–€875/m2 (full gut, Lisboa)
> - 🟡 **Área útil: 110m2** — assumed pela planta enviada; cliente deve confirmar com medição real
> - 🔵 **IVA 6%** — verified: imóvel em ARU Lisboa segundo Portaria 277/2020; aplica-se a reabilitação urbana
> - 🟡 **Acesso normal (sem agravamento)** — assumed; cliente deve confirmar se há restrições de rua ou sem elevador
> - 🔵 **Range demolições: 5–10% do total** — verified via estrutura ProNIC Cap. 2
> - 🟢 **Capítulo estrutura: €0** — projection assumindo sem alterações estruturais; reverter se diva-diagnose identificar reforços

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — área real medida, condições de acesso validadas, presença de amianto verificada
- [ ] All 🔵 citations adicionadas — número ARU, referência ProNIC/LNEC, portaria IVA aplicável
- [ ] All 🟢 projections comunicadas ao cliente como ranges (não valores fixos) com disclaimer de contingência 10–15%

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Orçamento Indicativo de Remodelação
**Projecto:** Atrium — Apartamento Chiado T3
**Morada:** Rua Nova do Almada 62, 2º Dto, Lisboa (ARU Chiado)
**Cliente:** Atrium Real Estate Development
**Área:** 112 m2 úteis | 124 m2 brutos
**Scope:** Full gut renovation — redistribuição parcial, cozinha nova, 2 WC novos
**Tier materiais:** Recomendado (mid-high)
**Imóvel:** 1928 (pré-1940, edifício pombalino)
**Acesso:** Escadas, sem elevador, rua pedonal estreita
**Data referência:** Março 2026

---

## COMPONENTE 1 — Construção (ProNIC)

| Cap | Capítulo | % | EUR |
|---|---|---|---|
| 1 | Estaleiro e trabalhos preparatórios | 4% | 5.376 |
| 2 | Demolições e remoções | 9% | 12.096 |
| 3 | Estrutura e fundações | 5% | 6.720 |
| 4 | Alvenarias e divisórias | 7% | 9.408 |
| 5 | Impermeabilizações e isolamentos | 4% | 5.376 |
| 6 | Revestimentos exteriores | 0% | 0 *(fora de scope)* |
| 7 | Revestimentos interiores — paredes | 10% | 13.440 |
| 8 | Revestimentos interiores — pavimentos | 11% | 14.784 |
| 9 | Revestimentos interiores — tetos | 4% | 5.376 |
| 10 | Caixilharia exterior | 8% | 10.752 |
| 11 | Caixilharia interior | 4% | 5.376 |
| 12 | Instalações eléctricas | 10% | 13.440 |
| 13 | Instalações hidrosanitárias | 8% | 10.752 |
| 14 | AVAC | 6% | 8.064 |
| 15 | Instalação de gás | 1% | 1.344 |
| 16 | Carpintarias e marcenarias | 7% | 9.408 |
| 17 | Equipamentos sanitários | 4% | 5.376 |
| 18 | Diversos (limpeza, testes, cert.) | 2% | 2.688 |
| **TOTAL CONSTRUÇÃO** | | **100%** | **134.400** |

*Base: 1.200 EUR/m2 (Lisboa, full gut, tier recomendado)*
*Ajuste aplicado: +15% acesso difícil + pré-1940 → 1.200 × 1,15 = 1.380 EUR/m2 efectivo*

---

## COMPONENTE 2 — Honorários e custos de projecto

| Item | Valor EUR |
|---|---|
| Projeto de arquitectura (6% construção) | 8.064 |
| Projetos de especialidades (estabilidade + redes) | 4.700 |
| Fiscalização de obra (3% construção) | 4.032 |
| Licenciamento CML (full gut, ARU Chiado) | 1.850 |
| Certificado energético (pós-obra) | 380 |
| **Subtotal honorários** | **19.026** |

---

## COMPONENTE 3 — Contingência e IVA

| Item | Valor EUR |
|---|---|
| Contingência 12% sobre construção | 16.128 |
| *(pré-1940: risco asbestos, surpresas estruturais)* | |

**IVA — Análise ARU:**
- Construção elegível (ARU Chiado confirmada, imóvel 1928): **IVA 6%**
- IVA construção (6% × 134.400): **8.064 EUR**
- Honorários e equipamentos: IVA 23% → 4.376 EUR
- **Total IVA:** 12.440 EUR
- *Poupança vs. IVA 23% integral: 22.284 EUR*

---

## TOTAL PROJECTO

| | EUR |
|---|---|
| Construção | 134.400 |
| Honorários e licenças | 19.026 |
| Contingência | 16.128 |
| IVA | 12.440 |
| **TOTAL ESTIMADO** | **181.994** |
| **Range (mín–máx)** | **168.000 – 205.000** |

*Mínimo: sem surpresas estruturais, prazo normal 5 meses*
*Máximo: asbestos confirmado (+5.000), reforço pombalino necessário (+9.000)*

---

## ⚠️ Flags de risco

1. **Asbestos** — Soalhos e estuques 1928: probabilidade média-alta.
   Recomendar peritagem prévia (350 EUR). Se positivo: +4.500-6.000 EUR Cap. 2.
2. **Estrutura pombalina** — Gaiola pode requerer reforço. Aguardar relatório estrutural.
3. **IVA 6%** — Confirmar elegibilidade com empreiteiro certificado INCI e CM Lisboa
   antes de assinar contrato. Erro aqui = +22.284 EUR não orçamentados.
4. **Prazo** — Acesso pedonal: rotação de materiais limitada. Prever 5-6 meses.
   Rush (<3 meses): +15% mão-de-obra = +20.160 EUR.
```

---

## Output anti-patterns

- Apresentar custo total sem breakdown por capítulo ProNIC — o cliente não consegue validar nem comparar com proposta de empreiteiro
- Omitir contingência ou enterrá-la num rodapé — deve ser linha visível e obrigatória
- Aplicar IVA 6% sem confirmar ARU e age do imóvel — erro financeiro potencialmente superior a 20.000 EUR
- Usar ranges demasiado largos sem justificar os extremos ("100.000 a 300.000 EUR") — é ruído, não informação
- Apresentar percentagens por capítulo sem valores absolutos — percentagens sozinhas são inúteis para decisão
- Não ajustar EUR/m2 base para localização, acesso e idade do imóvel — subestima sistematicamente projectos Lisboa/Porto pré-1940
- Incluir mobiliário e decoração dentro do custo de construção sem separar — distorce benchmarks e comparação com empreiteiros
- Não identificar nenhum flag de risco — qualquer projecto em Portugal tem pelo menos 2 riscos materiais identificáveis
- Apresentar orçamento sem data de referência de preços — valores de 2024 vs 2026 diferem 12-18%
