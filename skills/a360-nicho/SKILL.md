---
name: "A360 Niche Research & Validation"
description: "Deep niche research and market validation — TAM/SAM/SOM sizing, competition mapping, demand signals, viability scoring. Takes a business idea and determines if the market is worth entering."
version: "1.0"
agent: "A360 — Accelera 360"
category: "Phase 1 — Discovery"
license: SEE-LICENSE
parent_agent: a360-director
compliance: [audit_immutable]
---

# A360 Niche Research & Validation

## Triggers

Activate this skill when the user says any of:
- "niche research", "pesquisa de nicho", "market research"
- "TAM SAM SOM", "market size", "tamanho de mercado"
- "competition analysis", "analise concorrencia"
- "demand signals", "sinais de procura"
- "is this niche viable?", "este nicho vale a pena?"
- "validate this market", "validar mercado"
- Any request to evaluate whether a business idea has market potential

## Frameworks & References

- **Eric Ries** (Lean Startup) — validated learning, build-measure-learn
- **Alex Hormozi** ($100M Offers) — market selection criteria: growing, has pain, can afford to pay, easy to target
- **Russell Brunson** (DotCom Secrets) — dream customer identification, market sophistication levels (Eugene Schwartz)
- **Sean Ellis** (Hacking Growth) — growth experiments, North Star Metric
- **Peter Thiel** (Zero to One) — monopoly vs competition, 10x better test

## Workflow

### Step 1: Niche Definition
Capture from the user:
- Business idea / product concept (1-2 sentences)
- Target geography (local, national, global)
- Initial target audience hypothesis
- Budget range for validation (if any)
- Timeline pressure (how fast to revenue?)

### Step 2: Market Sizing (TAM/SAM/SOM)
Calculate using top-down AND bottom-up approaches:

**Top-Down:**
- TAM (Total Addressable Market): entire global market for the category
- SAM (Serviceable Addressable Market): segment you CAN reach with your business model
- SOM (Serviceable Obtainable Market): realistic capture in 12-24 months

**Bottom-Up:**
- Number of potential customers in target segment
- Average revenue per customer (ARPC)
- Purchase frequency per year
- SOM = customers x ARPC x frequency x realistic penetration rate (1-5%)

### Step 3: Demand Signal Analysis
Research and document each signal:

| Signal | Source | Method |
|--------|--------|--------|
| Search volume | Google Trends | Trend direction (rising/stable/declining), seasonality |
| Keyword volume | SEO tools | Monthly searches for core terms, CPC as proxy for commercial intent |
| Forum activity | Reddit, Quora, Facebook Groups | Number of posts, engagement, sentiment |
| Social mentions | Twitter/X, Instagram, TikTok | Hashtag volume, creator activity |
| Competitor funding | Crunchbase, AngelList | Recent raises in the space = investor validation |
| Job postings | LinkedIn, Indeed | Companies hiring in this niche = growth signal |
| Amazon/marketplace | Amazon BSR, Etsy trends | Product demand, review volume, pricing |
| Paid ads | Facebook Ad Library, SpyFu | Active advertisers = proven monetization |

### Step 4: Competition Mapping
Create a competitive landscape matrix:

**Direct Competitors** (same product, same market):
- Name, URL, estimated revenue/traffic
- Positioning statement
- Pricing model and price points
- Key differentiators
- Weaknesses / gaps / complaints (review mining)

**Indirect Competitors** (different product, same problem):
- Alternative solutions the customer uses today
- DIY / status quo alternatives

**Market Sophistication Level** (Eugene Schwartz scale):
1. Unaware — nobody knows the problem exists
2. Problem-aware — know the problem, no solutions yet
3. Solution-aware — solutions exist, yours must differentiate
4. Product-aware — market is crowded, need unique mechanism
5. Most-aware — market is saturated, need identity/brand play

### Step 5: Hormozi Market Selection Criteria
Score the niche on Alex Hormozi's 4 criteria (1-10 each):

| Criterion | Score | Evidence |
|-----------|-------|----------|
| **Growing market** (tailwind) | /10 | Google Trends direction, industry reports |
| **Has massive pain** (desperate buyers) | /10 | Forum posts, complaint volume, urgency signals |
| **Can afford to pay** (purchasing power) | /10 | Average income, B2B budget, existing spend |
| **Easy to target** (reachable audience) | /10 | Congregations, media, associations, lists |

**Minimum viable score: 28/40**. Below this, recommend pivoting.

### Step 6: Blue Ocean Opportunity Scan
Identify potential differentiation angles:
- Underserved sub-segments within the niche
- Feature gaps in competitor offerings
- Pricing model innovation opportunities
- Distribution channel gaps
- Geographic whitespace
- Audience segments competitors ignore

### Step 7: Viability Scorecard

Score each dimension 1-10:

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Market size (SOM > $1M) | 15% | /10 | |
| Growth trajectory | 15% | /10 | |
| Pain intensity | 15% | /10 | |
| Willingness to pay | 15% | /10 | |
| Competition gap | 10% | /10 | |
| Reachability | 10% | /10 | |
| Personal fit / expertise | 10% | /10 | |
| Speed to revenue | 10% | /10 | |
| **TOTAL** | 100% | | **/100** |

**Decision Thresholds:**
- 80-100: GREEN — Strong niche, proceed to Avatar (a360-avatar)
- 60-79: YELLOW — Viable with adjustments, refine positioning
- 40-59: ORANGE — High risk, consider pivot or sub-niche
- 0-39: RED — Do not proceed, find a different niche

## Commands

```bash
# Research Google Trends for niche terms
rtk curl "https://trends.google.com/trends/explore?q=TERM"

# Check keyword volume (if DataForSEO available)
# Use seo-dataforseo skill for live keyword data

# Search Reddit for pain points
rtk curl "https://www.reddit.com/search.json?q=TOPIC&sort=relevance&limit=25"
```

## Output Template

```markdown
# A360 Niche Research Report
## Niche: [NICHE NAME]
## Date: YYYY-MM-DD

### 1. Market Sizing
- **TAM**: $X (global category)
- **SAM**: $X (reachable segment)
- **SOM**: $X (12-month realistic capture)
- **Method**: [top-down / bottom-up / hybrid]

### 2. Demand Signals
| Signal | Finding | Strength |
|--------|---------|----------|
| Google Trends | [direction] | Strong/Medium/Weak |
| Keyword Volume | [X/mo] | Strong/Medium/Weak |
| Forum Activity | [description] | Strong/Medium/Weak |
| Competitor Activity | [description] | Strong/Medium/Weak |
| Paid Ads | [description] | Strong/Medium/Weak |

### 3. Competition Landscape
| Competitor | Revenue Est. | Positioning | Weakness |
|------------|-------------|-------------|----------|
| [Name] | $X | [statement] | [gap] |

**Market Sophistication**: Level X — [description]

### 4. Hormozi Criteria: X/40
| Criterion | Score | Evidence |
|-----------|-------|----------|
| Growing | /10 | [evidence] |
| Pain | /10 | [evidence] |
| Purchasing Power | /10 | [evidence] |
| Targetability | /10 | [evidence] |

### 5. Blue Ocean Opportunities
1. [Opportunity 1]
2. [Opportunity 2]
3. [Opportunity 3]

### 6. Viability Score: X/100
**Verdict**: [GREEN/YELLOW/ORANGE/RED]
**Recommendation**: [proceed / refine / pivot / abandon]

### 7. Next Steps
- [ ] Proceed to a360-avatar for customer profiling
- [ ] Proceed to a360-validacao for smoke testing
- [ ] [Other specific actions]
```

## Red Flags

Stop and warn the user if:
- SOM is below $100K (too small to build a business)
- Google Trends shows consistent decline over 5 years
- Zero active paid advertisers in the space (nobody can monetize)
- All competitors are VC-funded with deep moats (Thiel's competition trap)
- Market sophistication is Level 5 with no differentiation angle
- Hormozi score below 20/40
- User has zero expertise AND zero passion for the niche (personal fit = 0)
- The niche requires regulatory licenses the user does not have
- Customer acquisition cost appears higher than lifetime value at first glance

## Handoff

After completing niche research:
- **If GREEN**: Route to `a360-avatar` to build ideal customer profile
- **If YELLOW**: Refine niche parameters and re-run, or route to `a360-avatar` with caveats
- **If ORANGE/RED**: Brainstorm alternative niches and re-run this skill
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - A360 - Niche Research - [NicheName].md`

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Market Sizing tem três camadas calculadas (não estimadas ao calhas)
- [ ] TAM, SAM e SOM estão todos presentes com valor monetário explícito
- [ ] Bottom-up E top-down foram aplicados (pelo menos uma equação visível: Nº clientes × ARPC × frequência × penetration rate)
- [ ] SOM é ≥ $1M ou justificação explícita de por que < $1M ainda é viável
- [ ] Números têm fonte identificada (relatório, Statista, IBGE, INE, Crunchbase, etc.)

❌ NOT delivery-ready: `TAM: mercado grande, estimado em biliões. SOM: depende da execução.`
✅ Delivery-ready: `TAM: €2.1B (pet care Portugal + Espanha, Euromonitor 2023). SAM: €340M (cuidadores premium Lisboa/Porto/Madrid com app). SOM: €1.7M (12 meses, 850 clientes × €165 ARPC × 12× ano × 1%). Bottom-up confirma: 34.000 donos de cão em Lisboa com gasto médio de €80/mês em serviços.`

---

### Gate 2 — Demand Signals têm dados observáveis (não "provavelmente há procura")
- [ ] Google Trends: direção declarada (rising / stable / declining) + screenshot ou URL do termo exato pesquisado
- [ ] Volume de keyword com número concreto de pesquisas mensais + CPC como proxy de intenção comercial
- [ ] Pelo menos 2 sinais adicionais da tabela (Reddit/fóruns, Facebook Ads Library, Amazon BSR, job postings, etc.)
- [ ] Sazonalidade identificada quando relevante (ex: "pico em Dezembro, queda em Fevereiro")

❌ NOT delivery-ready: `Reddit mostra interesse no tema. Google Trends parece positivo.`
✅ Delivery-ready: `"dog care Lisboa" — 1.900 pesquisas/mês, CPC €1.40 (alta intenção). Google Trends: tendência +34% YoY (Jan 2022→Jan 2024). Reddit r/portugal: 47 posts sobre cuidadores de animais nos últimos 90 dias, sentimento 82% frustração com opções existentes. Facebook Ads Library: 12 anunciantes ativos em PT com copy sobre pet sitting = monetização provada.`

---

### Gate 3 — Competition Mapping tem nomes reais, não categorias abstratas
- [ ] Mínimo 3 concorrentes diretos com: nome, URL, modelo de preço, estimativa de tráfego ou receita
- [ ] Gaps/reclamações identificados via review mining (G2, Trustpilot, Google Reviews, Reddit complaints)
- [ ] Nível de sofisticação de mercado (Schwartz 1-5) declarado e justificado
- [ ] Concorrentes indiretos (status quo, DIY) identificados

❌ NOT delivery-ready: `Existem vários players no mercado. A concorrência é fragmentada.`
✅ Delivery-ready: `Diretos: Rover.com (€15-35/sessão, 8K reviews PT, fraqueza: sem seguro veterinário incluído), DogHero.com.br (BR, 120K utilizadores, reclamação recorrente: "sem validação de antecedentes"). Indiretos: vizinhos/família (gratuito, 67% dos utilizadores atuais). Schwartz Level 3 — soluções existem mas sem trust mechanism. Gap crítico: nenhum player PT oferece verificação de antecedentes criminais do cuidador.`

---

### Gate 4 — Hormozi Score tem evidências por critério (não scores subjetivos)
- [ ] Cada um dos 4 critérios tem score 1-10 E pelo menos 1 evidência concreta que justifica o score
- [ ] Score total calculado com soma explícita
- [ ] Se score < 28/40, recomendação de pivot está presente com alternativa específica
- [ ] Se score ≥ 28/40, próximo passo (ex: "avançar para A360 Avatar") está indicado

❌ NOT delivery-ready: `Growing: 7/10. Pain: 8/10. Can pay: 6/10. Targetable: 7/10. Total: 28/40 — ok.`
✅ Delivery-ready: `Growing: 8/10 (Google Trends +34% YoY, mercado pet PT cresceu 19% pós-COVID per Euromonitor). Massive pain: 9/10 (47 posts Reddit, tema #1 = "não confio em estranhos com o meu cão"). Can pay: 7/10 (donos de cão PT gastam €960/ano em média, APAP 2023). Targetable: 8/10 (grupos FB "Donos de cão Lisboa" 23K membros, 4 eventos anuais, IG hashtag #caesdeLisboa 180K posts). Total: 32/40 → GREEN, avançar.`

---

### Gate 5 — Viability Scorecard está completo e a decisão está declarada
- [ ] Todos os 8 critérios têm score numérico E weighted score calculado
- [ ] Total final em /100 com threshold declarado (GREEN/YELLOW/ORANGE/RED)
- [ ] Blue Ocean: pelo menos 2 oportunidades de diferenciação concretas identificadas (não genéricas)
- [ ] Recomendação final é uma frase de ação (não "depende")

❌ NOT delivery-ready: `Score total: ~65. Niche é viável mas tem riscos. Recomendamos continuar com cautela.`
✅ Delivery-ready: `Score total: 71/100 → YELLOW. Ajuste recomendado: sub-niche "pet sitting premium com verificação criminal" em vez de mercado geral. Blue Ocean: (1) modelo de subscrição mensal €49 vs pay-per-use dos concorrentes; (2) segmento ignorado — donos de cão sénior (65+) sem filhos, Lisboa, poder de compra elevado, zero ofertas adaptadas. Próximo passo: A360 Avatar para perfil "Dona de cão, 58 anos, Lisboa, rendimento >€3K/mês."`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero angle-brackets
- [ ] `[NICHE NAME]`, `[CLIENT]`, `$X`, `YYYY-MM-DD` substituídos por valores reais
- [ ] Data do relatório é a data atual (não placeholder)
- [ ] Todos os URLs de pesquisa referenciados são termos reais (não `TERM` ou `TOPIC`)
- [ ] Nenhum campo da tabela está vazio ou contém `TBD` / `a preencher`

❌ NOT delivery-ready: `Niche: [INSERIR NICHO]. TAM: $X. Data: YYYY-MM-DD. Score: /10.`
✅ Delivery-ready: `# A360 Niche Research Report — Cuidai. Niche: Pet Sitting Premium — Lisboa & Porto. Data: 2024-06-12. TAM: €2.1B. SOM: €1.7M (12M). Score: 71/100 — YELLOW.`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via fontes reais (Google Trends, Crunchbase, SEO tools, Amazon BSR, Ad Library)
- 🟡 **assumed** — plausível com base em proxies disponíveis, precisa de confirmação do cliente pré-entrega
- 🟢 **projection** — forecast calculado por design (SOM, penetration rate, revenue potential) — não verificável, comunicar como tal

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. o que precisa de sync antes de decidir entrar num mercado. **Honest transparency > inflated market research.**

❌ NOT delivery-ready:
> "TAM €2.3B, SOM €46M em 24 meses, mercado a crescer 18% YoY, 3 concorrentes fracos, Hormozi score 34/40."
> *(Sem labels — o cliente não sabe se o TAM veio de um relatório pago, de um cálculo bottom-up estimado, ou de uma projecção otimista. Decisões de investimento tomadas sobre dados sem proveniência.)*

✅ Delivery-ready:
> - 🔵 **verified** — TAM €2.3B (fonte: Statista 2024, European EdTech Report)
> - 🔵 **verified** — 3 concorrentes diretos identificados (Udemy PT, Aprender.pt, CourseHero) — tráfego via SimilarWeb
> - 🟡 **assumed** — ARPC €297/ano (baseado em pricing público dos concorrentes; cliente deve confirmar se o seu modelo difere)
> - 🟡 **assumed** — Hormozi "Can Afford to Pay" score 7/10 (proxy: rendimento médio do segmento 25-45 anos PT — INE 2023; validar se B2B ou B2C muda este número)
> - 🟢 **projection** — SOM €46M em 24 meses (bottom-up: 12.400 clientes × €297 × 1.25 freq × 1% penetration rate — modelo por design, comunicar ao cliente como cenário base)
> - 🟢 **projection** — Hormozi total score 34/40 (crescimento e dor validados 🔵; targeting e poder de compra são 🟡 — score final pode descer se assumptions não confirmados)

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir ARPC estimado, segmentação e poder de compra com dados reais do cliente ou pesquisa primária
- [ ] Todas as citações 🔵 linkadas no entregável final (relatório/fonte/data de acesso)
- [ ] Todos os itens 🟢 (SOM, Hormozi score composto, revenue projections) comunicados explicitamente ao cliente como modelos de forecast — não como factos de mercado

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# A360 Niche Research Report — Cuidai
## Niche: Pet Sitting Premium com Verificação de Antecedentes — Portugal (Lisboa & Porto)
## Data: 2024-06-12
## Preparado por: A360 — Accelera 360

---

### 1. Market Sizing

**Top-Down:**
- TAM: €2.1B (mercado pet care Portugal + Espanha combinado, Euromonitor 2023)
- SAM: €340M (serviços de cuidado ativo — sitting, walking, grooming — Lisboa/Porto, donos premium)
- SOM: €1.7M (projeção 12 meses)

**Bottom-Up (validação):**
- 34.000 donos de cão em Lisboa com gasto >€80/mês em serviços
- ARPC estimado: €165/mês (3 sessões × €55)
- Frequência: 12× ano
- Penetration rate: 0.9% (conservador, ano 1)
- **SOM = 34.000 × €165 × 12 × 0.009 = €608K Lisboa alone → +Porto: ~€1.7M**

---

### 2. Demand Signal Analysis

| Signal | Fonte | Dados |
|--------|-------|-------|
| Google Trends | trends.google.pt | "dog sitter Lisboa" +34% YoY (Jan 2022→Jan 2024), pico Julho–Agosto |
| Keyword volume | SEMrush Jan 2024 | "dog sitter lisboa" 1.900/mês, CPC €1.40; "pet sitting porto" 880/mês, CPC €1.10 |
| Reddit | r/portugal | 47 posts sobre cuidadores de animais (últimos 90 dias), 82% tom de frustração/desconfiança |
| Facebook Groups | "Donos de Cão Lisboa" | 23.000 membros, 3-5 posts/semana sobre recomendações — nenhuma solução com rating consistente |
| Facebook Ads Library | Meta (PT) | 12 anunciantes ativos, orçamento médio estimado €800-2.000/mês = monetização provada |
| Job Postings | LinkedIn PT | 0 vagas "pet sitter" com seguro incluído — gap de profissionalização visível |

**Sazonalidade:** pico claro Junho–Setembro (férias), queda Novembro–Janeiro. Oportunidade: pacotes de subscrição anual para suavizar.

---

### 3. Competition Mapping

**Diretos:**
| Concorrente | URL | Preço | Tráfego Est. | Fraqueza crítica |
|-------------|-----|-------|--------------|-----------------|
| Rover.com | rover.com/pt | €15–35/sessão | 42K visitas/mês PT | Sem verificação criminal; suporte em inglês |
| DogHero | doghero.com.br | R$50–120 | BR only | Não opera PT; modelo de avaliação fraco |
| Gudog | gudog.com | €12–28/sessão | 18K visitas/mês PT | Interface desatualizada; cuidadores não verificados |

**Indiretos:**
- Vizinhos/família: gratuito, 67% dos utilizadores atuais (APAP survey 2023)
- Canis/hotéis para cães: €25–45/noite — alternativa para viagens longas

**Schwartz Sophistication Level: 3 — Solution-Aware**
Mercado sabe que soluções existem (Rover, Gudog), mas não confia nelas. Diferenciação não pode ser "somos um marketplace de pet sitters" — tem de ser um mecanismo único (verificação criminal + seguro + garantia de satisfação).

**Review Mining (Google + Trustpilot):**
- Rover PT: reclamação #1 — "cuidador não apareceu, sem compensação" (34 reviews negativas em 6 meses)
- Gudog: reclamação #1 — "não sei quem é a pessoa que vai ficar com o meu cão" (tom de desconfiança)

---

### 4. Hormozi Market Selection Criteria

| Critério | Score | Evidência |
|----------|-------|-----------|
| Growing market | 8/10 | +34% Google Trends YoY; mercado pet PT cresceu 19% pós-COVID (Euromonitor) |
| Massive pain | 9/10 | 47 posts Reddit com sentimento de frustração; review mining confirma desconfiança sistemática |
| Can afford to pay | 7/10 | Donos de cão PT gastam €960/ano em média em serviços (APAP 2023); segmento alvo rende >€2.500/mês |
| Easy to target | 8/10 | Grupos FB (23K membros), hashtag #caesdeLisboa (180K posts IG), 4 eventos anuais em Lisboa |
| **TOTAL** | **32/40** | **GREEN — acima do threshold mínimo de 28/40** |

---

### 5. Blue Ocean Opportunity Scan

1. **Verificação criminal como produto** — nenhum player PT oferece; transforma trust em feature vendável ("Cuidadores Certificados Cuidai")
2. **Modelo de subscrição mensal €49** vs pay-per-use dos concorrentes — previsibilidade para o cliente, LTV superior para Cuidai
3. **Segmento ignorado: donos sénior (58–72 anos, Lisboa)** — sem filhos em casa, cão como companhia principal, poder de compra elevado, zero ofertas adaptadas (interface simples, contacto telefónico, confiança reforçada)
4. **Canal: clínicas veterinárias** — parceria B2B com 120 clínicas em Lisboa/Porto para referenciação cruzada; concorrentes ignoram canal offline

---

### 6. Viability Scorecard

| Dimensão | Peso | Score | Weighted |
|----------|------|-------|----------|
| Market size (SOM >€1M) | 15% | 7/10 | 1.05 |
| Growth trajectory | 15% | 8/10 | 1.20 |
| Pain intensity | 15% | 9/10 | 1.35 |
| Willingness to pay | 15% | 7/10 | 1.05 |
| Competition gap | 10% | 8/10 | 0.80 |
| Reachability | 10% | 8/10 | 0.80 |
| Personal fit / expertise | 10% | 6/10 | 0.60 |
| Speed to revenue | 10% | 7/10 | 0.70 |
| **TOTAL** | 100% | | **7.55/10 → 75/100** |

**Decisão: YELLOW (60-79) — Viável com ajuste de posicionamento.**
Recomendação: não atacar mercado geral; lançar como "Pet Sitting Premium Verificado" com foco em Lisboa (Avenidas Novas, Príncipe Real, Cascais) nos primeiros 6 meses.

**Próximo passo:** → Avançar para **A360 Avatar** com perfil prioritário: "Marta, 42 anos, Lisboa, rende €3.200/mês, 1 Golden Retriever, viaja 4× ano por trabalho."
```

---

## Output anti-patterns

- **Números sem fonte** — "TAM de €5B" sem citar relatório, data ou metodologia; o cliente não pode verificar nem usar em pitch
- **Schwartz level omitido** — entregar competitive map sem declarar nível de sofisticação torna a recomendação de posicionamento arbitrária
- **Hormozi scores sem evidência** — preencher tabela com scores intuitivos (Pain: 8/10 porque "parece urgente") invalida o framework inteiro
- **Blue Ocean genérico** — "melhor UX" e "preço mais baixo" não são oportunidades de diferenciação; requerem mecanismo específico
- **SOM irrealista** — usar penetration rate >5% em ano 1 sem benchmark comparável infla projeções e perde credibilidade
- **Decision threshold não declarado** — entregar scorecard sem dizer GREEN/YELLOW/ORANGE/RED e sem próximo passo concreto
- **Concorrentes sem fraqueza acionável** — listar nomes e URLs sem review mining não gera insight diferenciador
- **Placeholders no output final** — qualquer `[NICHE]`, `$X`, `YYYY-MM-DD` ou célula de tabela vazia é falha de entrega imediata
- **Demand signals sem direção** — "Google Trends mostra interesse" sem tendência (rising/stable/declining) e período específico é sinal vazio
