---
name: dario-pitch
description: Investor or client pitch deck generator using Klaff STRONG framework + Duarte Sparkline + Campbell Hero's Journey. Outputs slide outline, speaker notes, and hook script. Triggers on "pitch deck", "investor pitch", "apresentação", "keynote", "story deck".
license: MIT
---

# DARIO Skill — Pitch Deck

Builds a narrative-first pitch deck (not a glorified feature list). Uses proven storytelling frameworks so the audience **feels** the pitch, not just understands it.

## When to activate

- Client needs an investor deck (VC, angels, family offices)
- Internal keynote / board presentation
- Client-facing proposal deck (high-ticket services)
- HNW / luxury client presentations (like Atrium Golden Visa to HNW investors)
- Conference talk structure

## Workflow

### 1. Gather inputs
- **Who** is the audience (decision makers, context, time available)
- **What** are they deciding (invest, buy, partner, approve)
- **Why** now (trigger event, timing, urgency)
- **Ask** (the specific action wanted)
- **Stakes** (what happens if they don't act)
- **Proof** (data, testimonials, track record)
- **Analogy** (metaphor that simplifies the idea)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "oren klaff pitch STRONG frame control", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "nancy duarte sparkline resonate presentation", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "joseph campbell heros journey narrative", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "dan harmon story circle", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "park howell abt and but therefore", collection: "dario", limit: 5)
```

### 3. Choose primary framework by context

| Situation | Framework |
|---|---|
| VC pitch, compressed time | **Klaff STRONG** (frame control + pattern interrupt) |
| Keynote, change narrative | **Duarte Sparkline** (what is ↔ what could be) |
| Origin story, purpose-driven | **Campbell Hero's Journey** (condensed) |
| Business narrative, simple | **Park Howell ABT** (And, But, Therefore) |

Most pitches benefit from combining: **Klaff for frames + Duarte for structure + ABT for clarity**.

### 4. Klaff STRONG framework

**S** — **S**et the frame (context control from minute 1)
**T** — **T**ell the story (not pitch, story)
**R** — **R**eveal the intrigue
**O** — **O**ffer the prize (why they should want IN, not you want them in)
**N** — **N**ail the hookpoint (emotional moment of decision)
**G** — **G**et the decision (clear ask)

**Frame control rules:**
- Never be needy
- Make scarcity real
- Position audience as worthy (they qualify for YOU)
- Control time (not them)
- Avoid "analyst frame" (getting quizzed)

### 5. Duarte Sparkline structure

Alternate between **what is** (current state) and **what could be** (better state):

```
Start: what is (status quo reality)
  ↓ contrast ↑
what could be (vision)
  ↓ contrast ↑
what is (new obstacles)
  ↓ contrast ↑
what could be (breakthrough)
  ...
End: New bliss (call to action)
```

Each cycle amplifies the gap between reality and vision. Audience stays engaged because of contrast.

### 6. ABT (And, But, Therefore) — one-sentence narrative

Template:
> **<Context> AND <context> BUT <problem> THEREFORE <solution>.**

Example (Atrium):
> American HNW investors seek diversification AND Portugal Golden Visa is the most efficient EU path, BUT 73% of applications fail because of mis-structured investments, THEREFORE we built an end-to-end compliance-first advisory specifically for Americans.

This is the elevator pitch that anchors the deck.

### 7. Deck structure (12-14 slides standard)

| # | Slide | Purpose | Duarte beat |
|---|---|---|---|
| 1 | **Cover** | Title + credibility hook | What is |
| 2 | **The world today** | Problem + stakes | What is (amplified) |
| 3 | **Trend / Opportunity** | Why now | What could be |
| 4 | **Your founder story** (optional) | Credibility | Personal sparkline |
| 5 | **The unique insight** | What you see that others don't | What could be |
| 6 | **Solution** | Your product/offer | Reality |
| 7 | **How it works** | Mechanism | What is |
| 8 | **Results / Proof** | Metrics, case studies, testimonials | What could be (for them) |
| 9 | **Market size** | TAM/SAM/SOM | What is |
| 10 | **Business model** | How you make money | — |
| 11 | **Competition** | Differentiation matrix | — |
| 12 | **Team** | Why you'll win | — |
| 13 | **Ask + Use of funds** | Specific number + allocation | Call to action |
| 14 | **Vision / Close** | What winning looks like | New bliss |

### 8. Hook script (first 90 seconds)

Open with ONE of these patterns (test 2-3):
- **Shock stat:** "73% of Portugal Golden Visa applications are rejected. Here's why."
- **Contrarian claim:** "Everything you've heard about Golden Visa is 10 years out of date."
- **Story:** "In 2019, Karen watched a $500K investment disappear because of a PFIC rule nobody told her client about."
- **Analogy:** "Think of Portugal Golden Visa like a stock — you're not buying a country, you're buying an option."
- **Question (Socratic):** "How many of you know what Form 8621 is? That's why this matters."

Avoid: "Hi my name is...", "Today I'll talk about...", "Let me show you some slides."

### 9. Speaker notes (per slide)
- **Main point** (1 sentence)
- **Transition** (link from previous)
- **Story / example** (if slide benefits from it)
- **Pause points** (where to let it sink)
- **Audience interaction** (optional Q, show of hands)

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: pitch-deck
audience: <VCs|clients|board>
framework: <STRONG|sparkline|ABT|combined>
---

# Pitch Deck — <Project>

## Strategic Context
- Audience: ...
- Ask: ...
- Stakes: ...

## ABT One-liner
<Context> AND <context> BUT <problem> THEREFORE <solution>.

## Hook (90s script)
<Verbatim opening>

## Slide Outline

### Slide 1 — Cover
**Headline:** ...
**Visual:** ...
**Speaker note:** ...

### Slide 2 — The world today
**Headline:** ...
**Key data:** ...
**Speaker note:** ...

(continua)

## Full Speaker Notes
[By slide number, with transitions and pauses]

## Q&A Preparation
### Likely questions + framed answers
1. ...

## Deliverables
- [ ] Deck in Keynote / Google Slides (this doc as source)
- [ ] 1-pager summary
- [ ] Executive brief (PDF)
- [ ] Dry run rehearsal schedule
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Pitch Deck.md`

## Red flags
- Starting with "About us" or "Company history" (loses audience in 30s)
- 40-slide monster (kills attention)
- Font size <20pt on slides (unreadable in room)
- Charts without a single takeaway highlighted
- No clear ask (audience doesn't know what to do)
- Feature-dumping (no story)
- Treating investor/client as rational-only (emotion drives decisions)

## Interactions
- Depends on `dario-brand` (voice, positioning)
- Pairs with `dario-sales-letter` (can share copy blocks)
- Project: Atrium Golden Visa is the canonical use case — HNW investors need this treatment

## Red Flags
- Never exceed 14 slides (12 is ideal) — every slide beyond that dilutes attention and signals that you cannot prioritize
- Never present a deck without at least one rehearsal with timer — unrehearsed presenters run over time, miss transitions, and lose frame control
- Always open with a hook (shock stat, contrarian claim, story) not credentials — leading with "About Us" loses the audience in the first 30 seconds
- Never feature-dump without a narrative thread — a deck without story structure is a glorified brochure that triggers the analyst frame instead of the buyer frame
- Always end with a specific, unambiguous ask — a deck without a clear call to action wastes the emotional momentum you built throughout the presentation

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1. GATE — Narrative arc completo e coeso
- [ ] ABT one-liner está presente e ancora todo o deck (Context AND context BUT problem THEREFORE solution)
- [ ] Duarte Sparkline alterna corretamente entre "what is" e "what could be" em pelo menos 3 ciclos
- [ ] Slides 1-3 criam tensão suficiente ANTES de apresentar a solução
- [ ] Slide final termina em "new bliss" — não em features nem em disclaimers
- [ ] Speaker notes incluem pause points e transição entre slides

❌ NOT delivery-ready: "Slide 2: O mercado é grande e tem oportunidade. Slide 3: A nossa solução resolve isso."
✅ Delivery-ready: "Slide 2 (What is): 67% das PME portuguesas perdem acesso a crédito nos primeiros 18 meses por falta de histórico financeiro estruturado — €2.3B em capital bloqueado. Slide 3 (What could be): E se qualquer PME pudesse construir esse histórico em 90 dias?"

---

### 2. GATE — TAM/SAM/SOM com metodologia explícita
- [ ] TAM definido com fonte (Euromonitor, INE, Statista, relatório setorial datado)
- [ ] SAM calculado com critério geográfico/demográfico claro (não "20% do TAM")
- [ ] SOM justificado por capacidade operacional real (team size, canais, runway)
- [ ] Os três números são consistentes entre si (SOM < SAM < TAM, sem saltos ilógicos)

❌ NOT delivery-ready: "TAM: €50B global. SAM: €5B Europa. SOM: €500M nos próximos 3 anos."
✅ Delivery-ready: "TAM: €4.1B — mercado europeu de compliance fiscal para não-residentes (Deloitte European Tax Report 2023). SAM: €380M — Portugal + Espanha, segmento HNW com ativos >$1M (BCE Wealth Statistics Q3 2023). SOM: €8.5M em 36 meses — baseado em 3 advisors × 40 clientes/ano × ticket médio €70K confirmado por pipeline atual."

---

### 3. GATE — Ask financeiro preciso + Use of funds milestones
- [ ] Valor do ask é número exato (não range)
- [ ] Use of funds divide-se em 3-5 categorias com percentagem E valor absoluto
- [ ] Cada categoria liga a um milestone mensurável com timeline
- [ ] Runway está calculado explicitamente (meses até break-even ou próxima ronda)
- [ ] Valuation ou deal terms estão presentes se deck é para equity

❌ NOT delivery-ready: "Procuramos €500K-€1M para crescimento e contratações."
✅ Delivery-ready: "Ask: €750K convertible note (10% discount, 18-month maturity). Use of funds: Produto 40% (€300K) → MVP v2 em Q2 2025; GTM 35% (€262K) → 3 mercados em Q3 2025; Equipa 25% (€188K) → 2 engenheiros + 1 CS. Runway: 22 meses até break-even projetado a €85K MRR."

---

### 4. GATE — Klaff frame control aplicado
- [ ] Deck nunca posiciona o fundador como suplicante — linguagem é de "convite qualificado"
- [ ] Existe pelo menos um elemento de scarcity real e verificável (não inventado)
- [ ] Slide de competição usa differentiation matrix (não lista de logos)
- [ ] Hook script dos primeiros 90 segundos está presente e evita as 3 aberturas proibidas ("Hi my name is", "Today I'll talk about", "Let me show you")
- [ ] Time constraint é controlado pelo deck (não pelo investidor)

❌ NOT delivery-ready: "Estamos à procura de investidores que nos possam ajudar a crescer. Gostaríamos muito de contar com o vosso apoio."
✅ Delivery-ready: "Estamos a fechar esta ronda com 3 dos 5 lugares preenchidos. Os critérios de entrada incluem network B2B relevante para o sector saúde — se isso vos descreve, faz sentido continuar esta conversa."

---

### 5. GATE — Proof layer validado e específico
- [ ] Métricas de tração têm data de referência (não "crescemos 3x")
- [ ] Testemunhos ou case studies identificam cliente real (ou "cliente anónimo, sector X, dimensão Y")
- [ ] Slide de Team liga cada membro a credencial relevante para o problema específico (não CV genérico)
- [ ] Se produto early-stage: LOIs, cartas de intenção ou waitlist com números reais substituem revenue

❌ NOT delivery-ready: "Temos clientes satisfeitos e grande tração no mercado."
✅ Delivery-ready: "ARR: €127K (Dezembro 2024, +340% YoY). NPS: 71 (n=43 clientes activos). Case study: Cuidai reduziu custo de aquisição de cuidadores de €180 para €47 em 90 dias usando o módulo de matching automático."

---

### 6. GATE — Output uses CLIENT NAME + REAL data throughout — no placeholder angle-brackets
- [ ] Nenhum campo `<client>`, `<date>`, `<audience>` por preencher no output final
- [ ] Nome do cliente aparece no título, no ABT, e no slide de cover
- [ ] Todos os números são reais ou claramente marcados como projeção com base explícita
- [ ] Framework escolhido está identificado no cabeçalho YAML do output

❌ NOT delivery-ready: "TAM: <inserir número aqui>. Fundador: <nome>. Ask: <valor a definir>."
✅ Delivery-ready: Deck completo para Tributario.AI com ABT, 14 slides populated, ask de €400K, TAM de €1.8B com fonte Eurostat 2023, hook script verbatim, speaker notes em todos os slides.

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados do cliente
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes da entrega
- 🟢 **projection** — forecast por design (não verificável no momento)

Output checklist upfront mostra ao leitor exactamente o que é trust-as-is vs o que precisa verificar. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "73% of applications fail. Market TAM is €4.2B. Our close rate is 3× industry average."
> *(reader não sabe se estes números são internos, estimados ou inventados — undermines credibility no investor room)*

✅ Delivery-ready:
> - 🔵 **verified** — "73% rejection rate" (sourced: SEF/AIMA 2023 report, confirmed last session)
> - 🟡 **assumed** — "TAM €4.2B" (baseado em benchmarks públicos — cliente deve confirmar com own research pré-pitch)
> - 🟢 **projection** — "3× close rate vs industry average por Year 2" (forecast by design; apresentar como target ao investidor, não como historical fact)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir market size estimates, fee assumptions e competitor positioning com actuals do cliente
- [ ] All 🔵 citations added — cada stat no deck tem fonte visível (slide footer ou appendix) pronta para due diligence
- [ ] All 🟢 projections labeled — investidor vê claramente o que é forecast vs track record (evita securities / credibility issues)
- [ ] ABT one-liner validado — números embutidos no "And / But / Therefore" passaram pelo checklist acima antes de entrar no hook script
- [ ] Hook stat confirmado — o shock stat dos primeiros 90 segundos é 🔵 verified; nunca abrir com 🟡 assumed em frente a VCs

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Tributario.AI
date: 2025-01-15
type: pitch-deck
audience: Business angels portugueses + family offices Lisboa
framework: STRONG + Sparkline + ABT combined
---

# Pitch Deck — Tributario.AI
## Ronda Seed €400K | Janeiro 2025

---

## Strategic Context
- Audience: 8 business angels, ticket médio €50-80K, sector fintech/legaltech familiar
- Ask: €400K convertible note, 12% discount, 24-month maturity
- Stakes: Sem funding → equipa reduz para 2 pessoas em Março, perde janela de lançamento de API B2B antes de concorrente espanhol entrar em Portugal
- Trigger event: Aprovação do OE2025 criou 3 novos regimes fiscais para nómadas digitais — janela de 18 meses

---

## ABT One-liner
Portugal tornou-se o país europeu com maior complexidade fiscal para trabalhadores remotos internacionais AND as empresas de contabilidade tradicionais facturaram €2.1B em 2023 apenas neste segmento, MAS 78% dos nómadas digitais reportam erros na sua declaração de IRS nos primeiros 2 anos (OCDE Digital Nomad Tax Report 2024), PORTANTO construímos um motor de IA que interpreta automaticamente os 4 regimes fiscais portugueses relevantes e gera declarações auditadas em 12 minutos.

---

## Hook Script (primeiros 90 segundos — verbatim)

"Levantem a mão quem já teve que explicar o regime NHR a um cliente estrangeiro.
[pausa 3 segundos]
Agora mantenham a mão levantada se esse cliente ainda cometeu um erro na declaração de qualquer forma.
[pausa]
Esse problema custa €340 milhões por ano em correcções, penalidades e honorários de revisão em Portugal.
Não é um problema de falta de contabilistas. É um problema de complexidade que escala mais rápido do que qualquer equipa humana consegue acompanhar.
Chamo-me Ana Ferreira. Em 2022 era fiscalista no Deloitte. Em 2023 perdi um cliente de €180K porque um colega interpretou mal a cláusula 16(3) do NHR.
Isso não devia ser possível em 2025. Hoje não é."

---

## Slide Outline

### Slide 1 — Cover
**Headline:** Tributario.AI — O primeiro motor fiscal inteligente para Portugal
**Sub:** Declarações auditadas por IA em 12 minutos. Zero erros de interpretação.
**Visual:** Split screen: pilha de documentação fiscal (what is) vs. dashboard limpo com check verde (what could be)
**Speaker notes:** Deixar o visual respirar 5 segundos antes de falar. Não ler o título.

---

### Slide 2 — O mundo hoje (What is — amplificado)
**Headline:** Portugal tem 4 regimes fiscais sobrepostos. Os contabilistas interpretam-nos de forma diferente.
**Conteúdo:**
- 214 páginas de legislação fiscal alterada no OE2025
- 4 regimes activos simultaneamente: NHR clássico, NHR 2.0, IFICI, RNH Transitório
- 78% taxa de erro em primeiras declarações (OCDE 2024)
- €340M em correcções e penalidades anuais (AT, dados públicos 2023)

**Visual:** Mapa de sobreposição dos 4 regimes com zonas de conflito assinaladas a vermelho
**Speaker notes:** "Este não é um problema de competência. É um problema de complexidade sistémica. Os melhores fiscalistas do país discordam entre si sobre casos borderline — temos 3 pareceres contraditórios de TOCs certificados para mostrar."

---

### Slide 3 — Tendência / Oportunidade (What could be)
**Headline:** 47.000 novos nómadas digitais registados em Portugal em 2024. O mercado triplicou em 18 meses.
**Conteúdo:**
- +47.000 registos NIF estrangeiros em 2024 (AT, Janeiro 2025)
- Ticket médio de consultoria fiscal: €1.800/ano por cliente
- Mercado endereçável em Portugal: €84M/ano e a crescer 34% YoY
- Nenhuma solução automatizada existe para regimes portugueses especificamente

**Visual:** Gráfico de barras crescimento 2021-2024 + mapa de origem dos nómadas (EUA 31%, UK 18%, Brasil 24%)
**Speaker notes:** "O OE2025 acaba de criar o IFICI — um regime novo que nenhum software legacy consegue processar. Temos uma janela de 12-18 meses antes de qualquer concorrente europeu adaptar os seus motores."

---

### Slide 4 — Insight único (What could be — profundo)
**Headline:** O problema não é falta de dados. É falta de raciocínio jurídico estruturado.
**Conteúdo:**
- LLMs genéricos erram em 43% dos casos fiscais edge-case (teste interno, n=200 casos reais anonimizados)
- Tributario.AI usa RAG sobre corpus legislativo actualizado + chain-of-thought jurídico
- Resultado: 97.3% accuracy em casos de teste auditados por TOC externo (Jan 2025)

**Visual:** Diagrama: Input (documentos cliente) → Motor RAG Legislativo → Chain-of-thought → Output auditado
**Speaker notes:** "A diferença não é o modelo de IA. É o corpus e a estrutura de raciocínio. Temos 4 anos de jurisprudência do CAAD indexada — nenhum concorrente tem isso."

---

### Slide 5 — Solução (Reality)
**Headline:** 12 minutos. 4 regimes. 1 declaração auditada.
**Conteúdo:**
- Upload de documentos → processamento automático → declaração XML pronta para AT
- Módulo de explicabilidade: cada linha da declaração tem citação legislativa
- Revisão humana integrada: TOC parceiro valida em <2h para casos complexos
- API B2B para integração em software de contabilidade (Sage, PHC, Moloni)

**Visual:** Screen recording do produto (3 passos em 45 segundos)
**Speaker notes:** "Demo ao vivo disponível após a sessão. O que vêem no ecrã é o produto real, não um mockup."

---

### Slide 6 — Como funciona (Mecanismo)
**Headline:** RAG legislativo + jurisprudência CAAD + validação TOC
**Conteúdo (técnico simplificado):**
1. Ingestão: OCR + extracção estruturada de 23 tipos de documento
2. Classificação de regime: árvore de decisão com 847 nós (construída com 3 TOCs seniores)
3. Cálculo: motor de regras + LLM para edge cases
4. Auditoria: log completo de cada decisão com referência legal
5. Output: XML AT-compatible + PDF explicativo para o cliente

**Visual:** Diagrama de arquitectura simplificado (não técnico — 5 boxes com setas)

---

### Slide 7 — Resultados / Proof (What could be — para eles)
**Headline:** 127 clientes activos. €127K ARR. NPS 71.
**Métricas (Dezembro 2024):**
- ARR: €127.000 (+340% YoY vs €29K Dezembro 2023)
- Clientes activos: 127 (82 B2C, 45 via parceiros contabilidade)
- Churn mensal: 1.2%
- Tempo médio de declaração: 11.4 minutos (vs. 4.2h processo manual)
- NPS: 71 (n=43 respostas, Janeiro 2025)

**Case study:** Contabilidade Matos & Associados (Porto) — integrou API em Outubro 2024, processou 34 declarações NHR 2.0 sem erros, reduziu tempo por cliente de 3.5h para 18 minutos.

**Visual:** Dashboard de métricas + quote do parceiro

---

### Slide 8 — Mercado (TAM/SAM/SOM)
**Headline:** €1.8B TAM. €84M SAM. €2.1M SOM (ano 1 pós-funding).
**TAM:** €1.8B — mercado europeu de compliance fiscal para não-residentes e nómadas digitais (Eurostat + Deloitte European Tax Services Report 2023)
**SAM:** €84M — Portugal, segmento nómadas digitais + expatriados activos com rendimento >€30K/ano (AT dados públicos + estimativa INE 2024)
**SOM:** €2.1M ARR em 12 meses pós-funding — baseado em: 45 parcerias contabilidade × 25 clientes médios × €1.800 ticket = €2.025M + crescimento B2C orgânico

**Visual:** Três círculos concêntricos com fonte para cada número

---

### Slide 9 — Modelo de negócio
**Headline:** SaaS B2C + API B2B. Receita recorrente 94%.
**Streams:**
- B2C: €149/declaração ou €299/ano (ilimitado) — margem 78%
- B2B API: €0.80/declaração processada + €199/mês base — margem 82%
- Enterprise (>500 declarações/mês): contrato anual €18K-€45K

**Unit economics actuais:**
- CAC B2C: €23 (SEO + referral)
- CAC B2B: €340 (outbound + demo)
- LTV B2C: €520 (vida média 3.5 anos)
- LTV/CAC: 22.6x

---

### Slide 10 — Competição
**Headline:** Nenhum concorrente processa os 4 regimes portugueses simultaneamente.

| | Tributario.AI | Sage Portugal | Recibo Verde | Contabilidade Tradicional |
|---|---|---|---|---|
| NHR 2.0 + IFICI | ✅ | ❌ | ❌ | ✅ (manual, 4h) |
| Explicabilidade legal | ✅ | ❌ | ❌ | Parcial |
| API B2B | ✅ | ✅ | ❌ | N/A |
| Tempo médio | 12 min | N/A | 45 min | 4.2h |
| Preço por declaração | €149 | €0 (bundle) | €9 | €180-€400 |

**Vantagem defensável:** corpus legislativo proprietário + 847-nó decision tree construída com TOCs seniores — 18 meses de vantagem técnica.

---

### Slide 11 — Equipa
**Headline:** Fiscalista + engenheiro de ML + operações. Exactamente quem este problema precisa.

- **Ana Ferreira (CEO):** 6 anos Deloitte Tax (Lisboa + Madrid), TOC certificada, autora de 2 pareceres publicados sobre NHR 2.0
- **Rui Baptista (CTO):** Ex-Unbabel, MSc NLP Carnegie Mellon, 4 patentes em extracção de informação legal
- **Mariana Costa (COO):** Ex-Revolut Portugal (operações), escalou equipa de 3 para 40 em 18 meses

**Advisors:** Prof. António Martins (Universidade do Porto, Direito Fiscal) + Pedro Alves (ex-AT, Director de Fiscalidade Internacional)

---

### Slide 12 — Ask + Use of Funds
**Headline:** €400K para atingir €1M ARR e fechar ronda Série A em Q1 2026.

**Ask:** €400.000 — convertible note, 12% discount, 24-month maturity, cap €4M

**Alocação:**
| Categoria | % | Valor | Milestone |
|---|---|---|---|
| Produto (API v2 + mobile) | 40% | €160K | Launch Q3 2025 |
| GTM (parcerias B2B) | 30% | €120K | 25 novos parceiros Q4 2025 |
| Equipa (1 eng. + 1 CS) | 20% | €80K | Contratações Q2 2025 |
| Operações + Legal | 10% | €40K | Compliance RGPD + ISO 27001 |

**Runway:** 22 meses → break-even a €85K MRR (projecto Q4 2025)
**Próxima ronda:** Série A €2M em Q1 2026, baseada em €1M ARR demonstrado

---

### Slide 13 — Visão / Close (New Bliss)
**Headline:** Em 2027, qualquer pessoa que chegue a Portugal sabe exactamente o que deve ao fisco — antes de aterrar.

"O nosso objectivo não é substituir contabilistas. É dar-lhes superpoderes para servir 10x mais clientes com zero erros.
Portugal está a tornar-se o hub fiscal mais complexo e mais atractivo da Europa simultaneamente.
Precisamos de infraestrutura inteligente para isso funcionar.
Esse é o Tributario.AI.
Temos 3 lugares disponíveis nesta ronda. Dois estão confirmados.
Se faz sentido para vós, a conversa continua esta semana."
```

---

## Output anti-patterns

- **TAM inventado sem fonte:** escrever "TAM: €50B" sem metodologia ou referência — invalida credibilidade imediata junto de qualquer investor sofisticado
- **Ask em range:** "procuramos entre €300K e €600K" sinaliza falta de planeamento financeiro — número exacto sempre
- **ABT genérico:** escrever "há um problema no mercado e nós resolvemos" em vez de uma frase ABT estruturada com dados específicos
- **Hook proibido:** começar o script com "Olá, sou X e hoje vou apresentar Y" — desperdiça os primeiros 30 segundos de atenção máxima
- **Proof sem data:** "crescemos muito" ou "temos grandes clientes" sem métricas datadas e verificáveis
- **Slides de features em vez de benefícios:** listar funcionalidades do produto sem ligar cada uma a um outcome mensurável para o cliente/investidor
- **Competição como lista de logos:** slide de competição sem differentiation matrix — não demonstra posicionamento,
