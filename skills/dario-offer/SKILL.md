---
name: dario-offer
description: Build an irresistible Grand Slam Offer using Hormozi's value equation, 4-part formula, pricing tiers, bonuses, guarantees and urgency. Triggers on "oferta", "grand slam offer", "construir oferta", "pricing", "value equation", "bundle".
license: MIT
---

# DARIO Skill — Grand Slam Offer Builder

Turns a raw product/service into an offer that's hard to say no to, using Alex Hormozi's `$100M Offers` framework. Used before writing sales copy (`dario-sales-letter`) and for pricing/relaunch decisions.

## When to activate

- User asks for help "constructing an offer"
- New service launch
- Pricing discussion
- Conversion is failing but the product is solid → the problem is the offer
- Before Facebook/Google Ads campaign (ads are only as good as the offer)

## Workflow

### 1. Gather inputs
- **Product / service** — what it is
- **Dream outcome** — what the customer wants in their own words
- **Target avatar** — who specifically
- **Current price + packaging** (if exists)
- **Competitor offers** (who else, at what price, with what)
- **Customer objections** (top 5 "but what if..." fears)
- **Proof points** (results, testimonials, case studies)

If any of these are missing, stop and ask.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "hormozi grand slam offer value equation", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hormozi pricing tiers value-based", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hormozi guarantees conditional unconditional", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hormozi bonus stack naming offer", collection: "dario", limit: 5)
```

### 3. Apply the Value Equation

```
          (Dream Outcome × Perceived Likelihood of Achievement)
Value  =  ────────────────────────────────────────────────────
          (Time Delay × Effort & Sacrifice)
```

Iterate each lever to **maximize value**:
- **Dream outcome:** is it vivid, specific, tangible? ("Lose 20 pounds" > "get healthier")
- **Likelihood of achievement:** add proof, guarantees, frameworks
- **Time delay:** how fast will they see results? Accelerate it.
- **Effort & sacrifice:** how much do they have to do? Reduce it. "Done-for-you" > "Done-with-you" > "DIY".

### 4. Apply the 5-step Grand Slam formula

#### Step 1: Identify the dream outcome (1 sentence)
"<Target>, get <dream outcome> in <timeframe> without <pain>."

#### Step 2: List every problem that stands in the way
Brainstorm 15-20 problems. These become the bonuses that eliminate each.

#### Step 3: Turn problems into solutions
Each problem → a specific deliverable that solves it.

#### Step 4: Stack the value
Create "Bonus stack":
- **Bonus 1:** Solves [problem 1]. Value: $X
- **Bonus 2:** Solves [problem 2]. Value: $Y
- ...
Total perceived value: $ZZZZZ

The offer price should be 10-20% of the perceived stacked value.

#### Step 5: Name it and frame it
- **Magnetic name:** benefit-driven, specific, memorable
  - Bad: "Consulting Package Premium"
  - Good: "The 90-Day Lisbon Listing Dominator"
- **Frame:** context that positions the offer as different/unique

### 5. Design the guarantee
Choose one (or stack multiple):
- **Unconditional** — 100% money back, no questions
- **Conditional** — "if you do X, we guarantee Y"
- **Anti-guarantee** — "we don't refund but we promise X" (works when trust is high)
- **Implied** — case studies + pay-for-results
- **Performance** — "we hit KPI or work free until we do"
- **Service** — "we redo the work"

### 6. Add urgency + scarcity (real, never fake)
- Cohort-based (next cohort starts X)
- Seat-limited (20 clients per quarter)
- Price-escalating (price goes up every N sales)
- Bonus-expiring (bonuses available until X date)

### 7. Stack pricing tiers (optional)
- **Good:** entry (DIY)
- **Better:** managed (done-with-you)
- **Best:** full-service (done-for-you) — highest margin, highest ticket
Price gap between tiers: 2.5-5x (anchor the Best)

## Output template

```markdown
---
project: <client or product>
date: <YYYY-MM-DD>
type: grand-slam-offer
hormozi_framework: yes
---

# Grand Slam Offer — <Offer Name>

## One-liner
> <Target>, <dream outcome> in <timeframe> without <pain>.

## Avatar
- Who: ...
- What they want: ...
- What they fear: ...

## Value Equation Analysis
| Lever | Current | After Offer |
|---|---|---|
| Dream Outcome | ... | ... |
| Likelihood | ... | ... |
| Time Delay | ... | ... |
| Effort | ... | ... |

## Core Offer
<What they get, in plain language>

## Bonus Stack
| # | Bonus | Solves Problem | Value |
|---|---|---|---|
| 1 | ... | ... | $X |
| 2 | ... | ... | $Y |
| N | ... | ... | $Z |
| **Total** | | | **$TTTT** |

## Guarantee
<Specific guarantee language>

## Urgency / Scarcity
<Real, not fake>

## Pricing Tiers
| Tier | Price | Delivery | Who it's for |
|---|---|---|---|
| Good | $X | DIY | ... |
| Better | $XX | DWY | ... |
| Best | $XXX | DFY | ... |

## Objection → Reframe
| Objection | Response |
|---|---|
| "Too expensive" | ... |
| "I don't have time" | ... |
| "Not sure it'll work for me" | ... |

## Next Steps
- [ ] Pair with `dario-sales-letter` for copy
- [ ] Pair with `dario-ads-blueprint` for traffic
- [ ] Test price on 10 calls before public launch
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Grand Slam Offer.md`

## Red flags to avoid
- Fake scarcity ("only 2 left!" when there are 200)
- Vague dream outcome ("better life")
- Bonuses that duplicate the core (not new problems solved)
- No guarantee — implies no confidence
- Price too low (implies low value)
- Too many tiers (>3) — paralysis

## Interactions
- Follow up with `dario-sales-letter` to write the long-form copy
- Follow up with `dario-ads-blueprint` to drive traffic
- Save via `dario-obsidian-save` to vault

## Red Flags
- Never build an offer without brand positioning completed first (`dario-brand`) — an offer disconnected from brand voice and values feels generic and erodes trust
- Never use the value equation with vague or generic terms ("better results", "more success") — each lever must be specific and measurable or the equation produces meaningless output
- Always include a guarantee in the final offer — an offer without risk reversal signals low confidence and leaves the biggest conversion objection unaddressed
- Never create fake scarcity or urgency — fabricated deadlines and phantom limits destroy credibility when discovered, and they always get discovered
- Always validate the offer with 5-10 real conversations before public launch — an untested offer at scale wastes ad budget and poisons the market's first impression

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

### 1. VALUE EQUATION — todos os 4 levers estão quantificados
- [ ] Dream Outcome é específico e mensurável ("fechar 3 clientes enterprise em 90 dias" — não "crescer o negócio")
- [ ] Likelihood of Achievement tem prova concreta (case study, testimonial, framework nomeado)
- [ ] Time Delay está declarado em dias/semanas — não "rapidamente"
- [ ] Effort & Sacrifice está reduzido com linguagem DFY/DWY explícita

❌ NOT delivery-ready: "Aumentar a probabilidade de sucesso do cliente com o nosso método comprovado."
✅ Delivery-ready: "Taxa de fecho de 73% nos primeiros 60 dias — comprovado em 12 PMEs portuguesas (ver caso Cuidai, Q1 2024)."

### 2. BONUS STACK — cada bonus resolve um problema distinto com valor âncora
- [ ] Mínimo 4 bonuses listados na tabela, cada um com problema mapeado
- [ ] Cada bonus tem valor âncora em € (calculado por tempo/mercado — não inventado)
- [ ] Valor total stacked é 5-10× o preço do tier "Better"
- [ ] Nenhum bonus duplica o core offer (elimina problema novo, não repete entrega principal)
- [ ] Nomes dos bonuses são benefit-driven ("O Guia de Objeções de Preço" > "Documento de Apoio 3")

❌ NOT delivery-ready: "Bonus 1: Suporte extra. Valor: $500" (vago, sem problema mapeado)
✅ Delivery-ready: "Bonus 2: 'Script de Recuperação de Leads Frios' — resolve o problema de pipeline parado após 14 dias. Valor âncora: €380 (2h consultoria de vendas a €190/h)."

### 3. GARANTIA — linguagem específica, condições claras, sem ambiguidade
- [ ] Tipo de garantia está explicitamente nomeado (incondicional / condicional / performance)
- [ ] Se condicional: as condições do cliente estão escritas em plain language (o que ele tem de fazer)
- [ ] Se performance: o KPI alvo e o prazo estão fixados em números
- [ ] A garantia está escrita como o cliente a vai LER — não como nota interna

❌ NOT delivery-ready: "Garantimos resultados ou devolvemos o dinheiro."
✅ Delivery-ready: "Se completares os 3 módulos e não fechares pelo menos 1 cliente novo em 60 dias, devolvemos 100% — sem perguntas, por transferência em 5 dias úteis."

### 4. URGÊNCIA/ESCASSEZ — real, verificável, não fabricada
- [ ] Mecanismo de urgência está explicado (cohort, lugares, price-escalation, bonus expiry)
- [ ] A data ou limite está fixado com número concreto (não "em breve" ou "vagas limitadas")
- [ ] Existe lógica de negócio que justifica o limite (não é decorativa)
- [ ] Urgência não contradiz outros elementos da oferta (ex: "só 5 lugares" + "equipa de 1 pessoa" = credível; "só 5 lugares" + "produto digital" = fake)

❌ NOT delivery-ready: "Oferta por tempo limitado! Aproveita já!"
✅ Delivery-ready: "Próxima cohort: 3 de Fevereiro. Máximo 8 clientes (limite de capacidade de onboarding). 3 lugares preenchidos. Preço sobe €500 na cohort de Março."

### 5. PRICING TIERS — âncora clara, gap de 2.5-5× entre tiers, avatar correto por tier
- [ ] Máximo 3 tiers (Good / Better / Best) — sem sub-opções dentro de tiers
- [ ] Gap de preço entre Better e Best é 2.5–5× (âncora o Best para tornar o Better óbvio)
- [ ] Cada tier tem avatar descrito ("para quem quer X mas prefere Y")
- [ ] Tier "Best" (DFY) tem margem mais alta que "Good" — verificar que não está invertido

❌ NOT delivery-ready: "Pack A: €200 | Pack B: €350 | Pack C: €500" (gap insuficiente, sem diferenciação)
✅ Delivery-ready: "Good: €490 (DIY, para fundadores com tempo) | Better: €1.490 (DWY, sessões semanais) | Best: €5.900 (DFY, entregamos tudo, para quem quer resultado sem trabalho)."

### 6. OUTPUT usa NOME DO CLIENTE + dados reais — zero placeholders com angle-brackets
- [ ] `<client or product>`, `<Target>`, `<dream outcome>` estão todos substituídos por dados reais
- [ ] Tabelas de valor equation têm dados antes/depois preenchidos (não "...")
- [ ] Objection → Reframe tem objeções reais deste avatar (não genéricas de template)
- [ ] Save location tem data real + nome do cliente

❌ NOT delivery-ready: "One-liner: `<Target>`, alcança `<dream outcome>` em `<timeframe>`."
✅ Delivery-ready: "One-liner: PMEs portuguesas de serviços B2B, fecham os primeiros 3 contratos recorrentes em 90 dias sem contratar uma equipa de vendas."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Atrium — Sales Acceleration Program
date: 2025-01-15
type: grand-slam-offer
hormozi_framework: yes
---

# Grand Slam Offer — O Acelerador de Pipeline Atrium 90

## One-liner
> PMEs de SaaS B2B em Portugal, fecham os primeiros 3 contratos enterprise
> em 90 dias sem contratar um head of sales a tempo inteiro.

## Avatar
- **Quem:** Fundador de SaaS B2B, 5-20 colaboradores, MRR entre €8k–€40k
- **O que quer:** pipeline previsível, sair do ciclo "só cresce quando eu vendo"
- **O que teme:** gastar €5k+ em consultoria e ficar igual; equipa não adotar o processo;
  perder tempo em demos que nunca fecham

## Value Equation Analysis
| Lever | Situação Atual | Depois da Oferta |
|---|---|---|
| Dream Outcome | "Quero mais clientes" (vago) | 3 contratos enterprise assinados, MRR +€9.000 |
| Likelihood | Sem processo, depende do humor do fundador | Framework BANT + script testado em 12 PMEs portuguesas, taxa fecho 67% |
| Time Delay | 6-12 meses para sistematizar sozinho | Primeiros 2 closes em 45 dias (milestone garantido) |
| Effort | Fundador faz tudo: prospeção, demo, follow-up, proposta | DFY nas primeiras 4 semanas; DWY nas restantes 8 |

## Core Offer
Programa de 90 dias onde a equipa Atrium co-executa o processo de vendas
B2B do cliente: constrói a sequência de prospeção, treina o fundador no
framework de qualificação, escreve as propostas comerciais das primeiras
3 deals, e entrega um Sales Playbook pronto a passar à primeira contratação.

## Bonus Stack
| # | Bonus | Resolve Problema | Valor Âncora |
|---|---|---|---|
| 1 | Script de Cold Email (3 variantes A/B/C testadas no mercado PT) | "Não sei como abordar empresas frias" | €420 |
| 2 | Template de Proposta Comercial Atrium (Notion + PDF) | "As minhas propostas perdem para as da concorrência" | €350 |
| 3 | Biblioteca de 40 Objeções B2B com Reframe (PT/EN) | "Travo quando o prospect diz 'está caro'" | €280 |
| 4 | Sessão de Role-Play de Demo (gravada + feedback escrito) | "Não sei se o meu pitch está a funcionar" | €380 |
| 5 | Acesso à comunidade Atrium Alumni (12 meses) | "Depois do programa fico isolado outra vez" | €600 |
| **Total** | | | **€2.030** |

**Preço do programa: €1.490 (tier Better) — 73% do valor stacked em bonuses.**

## Garantia
**Garantia de Pipeline em 45 Dias (Condicional)**

Se completares as 4 sessões de onboarding, enviares mínimo 80 cold emails
com os nossos templates e participares nos 2 role-plays, e não tiveres pelo
menos 2 demos qualificadas agendadas ao fim de 45 dias — trabalhamos
contigo gratuitamente até atingires esse número, sem custo adicional.

Condições do cliente: assiduidade às sessões, envio mínimo documentado
no CRM partilhado, feedback em 48h nos drafts de proposta.

## Urgência / Scarcity
- Próxima cohort arranca **3 de Fevereiro de 2025** (data fixa — alinhada com
  calendário de onboarding da equipa Atrium)
- **Máximo 6 clientes por cohort** (cada cliente tem 2 sessões semanais com
  sénior; 6 × 2h = 12h/semana — capacidade máxima do programa)
- **2 lugares já preenchidos** (Tributario.AI + SAQUEI — confirmados a 10 Jan)
- Preço sobe para €1.790 na cohort de Abril (price-escalation documentada
  na página de vendas desde Outubro 2024)

## Pricing Tiers
| Tier | Preço | Entrega | Para quem |
|---|---|---|---|
| Good — Playbook Solo | €490 | DIY: acesso ao Sales Playbook Atrium + 1 sessão de setup de 90 min | Fundador com tempo, quer o processo mas prefere executar sozinho |
| Better — Acelerador 90 ⭐ | €1.490 | DWY: 8 sessões ao longo de 90 dias + co-execução das primeiras 3 propostas + todos os bonuses | Fundador que quer resultado rápido e quer aprender fazendo |
| Best — Pipeline DFY | €5.900 | DFY: equipa Atrium executa prospeção, qualificação e primeiras demos; fundador aprova apenas | Fundador sem tempo, prefere delegar completamente as primeiras 10 deals |

## Objection → Reframe
| Objeção | Resposta |
|---|---|
| "€1.490 está caro para mim agora" | "Precisas de fechar 1 deal de €500/mês para ter ROI em 3 meses. A maioria dos nossos clientes fecha a primeira deal antes do programa terminar." |
| "Não tenho tempo para mais um programa" | "O Better foi desenhado para fundadores com <5h/semana disponíveis. Nós executamos; tu approvas. Nas primeiras 4 semanas o teu esforço é 2h." |
| "Já tentei consultoria de vendas e não funcionou" | "A diferença: nós não ensinamos teoria — co-executamos contigo. Vês as primeiras deals fecharem antes de receberes o playbook." |
| "O meu produto é diferente, será que funciona?" | "O framework foi aplicado em 12 sectores B2B diferentes em Portugal, incluindo SaaS jurídico (Tributario.AI) e fintech (SAQUEI). Mostramos os casos antes de decidires." |

## Next Steps
- [ ] Pair com `dario-sales-letter` para escrever a página de vendas longa
- [ ] Pair com `dario-ads-blueprint` para LinkedIn Ads targeting fundadores SaaS PT
- [ ] Testar preço do tier Best (€5.900) em 5 calls antes de publicar
- [ ] Salvar via `dario-obsidian-save`
```

---

## Output anti-patterns

- **Placeholders não substituídos** — entregar output com `<Target>` ou `<dream outcome>` por preencher; o cliente recebe lixo de template, não uma oferta
- **Dream outcome vago** — "melhorar o negócio", "crescer as vendas", "ter mais sucesso"; se não cabe num KPI com número, reescreve
- **Bonuses que duplicam o core** — se o core é "construímos o teu funil", um bonus "sessão de funil" não é novo valor; resolve um problema diferente ou não existe
- **Valores âncora inventados** — "Bonus 1: valor €2.000" sem cálculo; usar sempre tempo × tarifa de mercado ou preço de produto equivalente real
- **Scarcity decorativa** — "apenas 5 lugares" num produto digital infinitamente replicável; ou "oferta expira domingo" sem lógica de negócio; destrói confiança instantaneamente
- **Garantia sem condições** — "garantimos resultados" é vazio juridicamente e comercialmente; especificar o que o cliente tem de fazer E o que a empresa entrega se falhar
- **Gap de preço insuficiente entre tiers** — Good €200 / Better €300 / Best €400 não ancora nada; o Best tem de ser 2.5–5× o Better para tornar o Better a escolha óbvia
- **Mais de 3 tiers** — 4+ opções criam paralisia de decisão; se o cliente quer sub-opções dentro de um tier, criar add-ons nomeados, não novos tiers
- **Objeções genéricas** — "está caro" sem contexto do avatar real; as objeções devem vir do Step 1 (inputs do cliente) — se não há inputs, parar e perguntar antes de gerar
- **Oferta sem brand check** — gerar Grand Slam Offer antes de confirmar que existe `dario-brand` completed; oferta desalinhada com voz da marca dilui confiança e parece comprada num template
