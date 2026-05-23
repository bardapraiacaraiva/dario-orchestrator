---
name: dario-cro
description: CRO & experimentation squad — runs ResearchXL audits, LIFT scoring, emotional targeting, attention ratio analysis, form optimization, trust audits, PXL prioritization, and A/B test planning. Triggers on "cro", "conversion rate", "a/b test", "split test", "landing page audit", "form optimization", "trust audit", "experimentation", "taxa de conversao", "otimizar conversao".
version: 1.0.0
license: MIT
---

# DARIO Skill -- CRO & Experimentation

Full-stack conversion rate optimization: diagnose why pages underperform, audit using six expert lenses, prioritize a test backlog, design statistically valid experiments, and implement winning variants. Built on the combined frameworks of Peep Laja, Chris Goward, Talia Wolf, Oli Gardner, Karl Gilis, and Andre Morys.

## When to activate

- Landing page not converting (below industry benchmark)
- Homepage trying to do everything at once
- "People visit but don't buy/sign up/contact"
- Form abandonment is high
- Client asks for "A/B testing" or "conversion optimization"
- After `dario-funnel` (funnel exists, now optimize each step)
- After `dario-sales-letter` (copy exists, now test variants)
- E-commerce checkout drop-off investigation
- Before paid traffic scale-up (fix the bucket before pouring more water)

## Squad roster

| Agent | Framework | Focus |
|---|---|---|
| **ResearchXL** (Peep Laja) | 6-layer research model | Heuristic, technical, analytics, mouse tracking, qualitative, quantitative |
| **LIFT Model** (Chris Goward) | 6-factor scoring | Value prop, relevance, clarity, anxiety, distraction, urgency |
| **Emotional Targeting** (Talia Wolf) | Emotional conversion | Emotional triggers, color psychology, persuasion hierarchy |
| **Attention Ratio** (Oli Gardner) | 1:1 ratio rule | Single CTA focus, page congruence, information scent |
| **Form Optimization** (Karl Gilis) | Form UX | Field reduction, microcopy, progressive disclosure, error handling |
| **Trust Signals** (Andre Morys) | Conversion trust | Social proof, authority, risk reversal, credibility markers |

## Workflow

### 1. Gather inputs

- **Page URL** (live page or staging)
- **Page purpose** (lead gen, purchase, signup, download, booking)
- **Traffic source** (paid, organic, email, social, direct)
- **Current metrics** (conversion rate, bounce rate, sessions, AOV if e-commerce)
- **Analytics access** (GA4 or equivalent data)
- **Heatmap data** (Hotjar/Clarity if available)
- **Business context** (industry, ticket size, sales cycle)

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "peep laja researchxl conversion optimization heuristic", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "chris goward lift model value proposition clarity", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "talia wolf emotional targeting conversion", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "oli gardner attention ratio unbounce landing page", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "karl gilis form optimization usability", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "andre morys trust signals conversion psychology", collection: "dario", limit: 5)
```

### 3. Diagnose -- ResearchXL 6-layer analysis

Run each layer sequentially:

**Layer 1 -- Heuristic analysis**
Walk the page as a first-time visitor. Score each element:
- Does the headline communicate value in under 5 seconds?
- Is the primary CTA immediately visible above the fold?
- Is the visual hierarchy guiding the eye toward conversion?
- Are trust signals present and credible?
- Is the copy benefit-oriented (not feature-oriented)?

**Layer 2 -- Technical analysis**
- Page load time (target: < 3s)
- Mobile responsiveness and tap targets
- Cross-browser rendering
- Core Web Vitals (LCP, INP, CLS)
- JavaScript errors blocking interactions
- Form submission errors

**Layer 3 -- Analytics deep-dive**
- Traffic segmentation (device, source, geo, new vs returning)
- Funnel visualization (where do users drop off?)
- Exit pages vs bounce pages (different problems)
- Event tracking gaps (what is NOT being measured?)
- Segment comparison (converters vs non-converters behavior)

**Layer 4 -- Mouse tracking / heatmaps**
- Click maps: are users clicking non-clickable elements?
- Scroll maps: what percentage see below-the-fold content?
- Attention maps: is the CTA in a heat zone?
- Rage clicks: frustrated interactions
- Session recordings: 10-20 random non-converting sessions

**Layer 5 -- Qualitative research**
- On-page surveys ("What almost stopped you from completing?")
- Exit-intent survey ("Why are you leaving?")
- Customer interviews (5-10 recent converters)
- Customer support ticket analysis (recurring objections)
- Review mining (competitor reviews for objection patterns)

**Layer 6 -- Quantitative validation**
- A/B test hypotheses ranked by impact x effort
- Sample size calculations before launching tests
- Statistical significance thresholds (95% confidence minimum)
- Test duration planning (minimum 2 full business cycles)

### 4. Audit -- LIFT Model scoring

Score each factor 1-10 and compute overall LIFT score:

| Factor | Question | Score (1-10) | Notes |
|---|---|---|---|
| **Value Proposition** | Is the offer compelling and clearly communicated? | | |
| **Relevance** | Does the page match visitor intent and ad/referral promise? | | |
| **Clarity** | Is the message and next step immediately obvious? | | |
| **Anxiety** | Are there elements creating doubt or hesitation? | | |
| **Distraction** | Are there elements pulling attention away from conversion? | | |
| **Urgency** | Is there a reason to act now vs later? | | |

**LIFT Score** = (Value + Relevance + Clarity - Anxiety - Distraction + Urgency) / 6

- Score 8-10: High conversion potential, fine-tune only
- Score 5-7: Significant issues, structured testing needed
- Score 1-4: Fundamental problems, redesign before testing

### 5. Specialized audits

#### *emotional-audit (Talia Wolf)

Map the emotional conversion path:
1. **Identify dominant buyer emotion** (fear, aspiration, belonging, status, guilt, curiosity)
2. **Audit visual triggers** -- do colors, images, and layout reinforce the emotion?
3. **Audit copy triggers** -- does the language amplify the emotion?
4. **Audit persuasion sequence** -- emotion first, then logic, then action
5. **Emotional gap analysis** -- where does the emotional thread break?

#### *attention-ratio (Oli Gardner)

Calculate the attention ratio:
```
Attention Ratio = Number of links on page : Number of conversion goals
Target: 1:1 (one page, one goal)
```

Audit:
- Count every clickable element (nav links, footer links, social icons, secondary CTAs)
- Identify the single conversion goal
- Flag violations: nav bar on LP, social links, "learn more" links, footer navigation
- Information scent check: does every element point toward the CTA?

#### *form-audit (Karl Gilis)

For every form on the page:
- **Field count** -- target: absolute minimum needed (every field removed = conversion lift)
- **Field labels** -- clear, above the field, not inside (placeholder-as-label is an anti-pattern)
- **Field order** -- easy first (name, email), hard last (phone, budget)
- **Microcopy** -- helper text explaining WHY you need each field
- **Error handling** -- inline validation, specific error messages (not "invalid input")
- **CTA button text** -- specific verb + value ("Get My Free Audit" not "Submit")
- **Progressive disclosure** -- multi-step vs single long form
- **Mobile UX** -- correct keyboard types (email, tel, number), autofill support

#### *trust-audit (Andre Morys)

Inventory and score trust signals:
- **Social proof**: testimonials (with photos/names), review counts, client logos, case studies
- **Authority**: certifications, awards, press mentions, expert endorsements, years in business
- **Risk reversal**: guarantees, free trials, return policies, "no commitment" language
- **Security**: SSL badge, payment security icons, privacy assurances
- **Specificity**: exact numbers beat vague claims ("1,247 clients" vs "thousands of clients")
- **Proximity**: trust signals placed near the CTA, not buried in footer

### 6. Prioritize -- PXL framework

Rank all identified issues using PXL (Peep Laja):

| # | Hypothesis | Page/element | Is it above the fold? (2pt) | Based on user data? (2pt) | Addresses a known problem? (2pt) | Running on high-traffic page? (2pt) | Noticeable in < 5s? (2pt) | Adding/removing? (1pt) | PXL Score | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |

Sort by PXL score descending. Top 3 become the test roadmap.

### 7. Design A/B test plan

For each prioritized hypothesis:

```
Test ID:       CRO-<NNN>
Hypothesis:    If we [change], then [metric] will [improve] because [reason]
Variable:      [specific element being changed]
Control:       [current version description]
Variant:       [new version description]
Primary KPI:   [conversion rate / form completion / AOV / RPV]
Secondary KPI: [bounce rate / time on page / scroll depth]
Sample size:   [calculated — use formula below]
Duration:      [minimum days based on traffic]
Segment:       [all traffic / specific source / device]
Tool:          [Google Optimize successor / VWO / Convert / Optimizely]
```

**Sample size formula:**
```
n = (Z_alpha/2 + Z_beta)^2 * 2 * p * (1-p) / MDE^2

Where:
- Z_alpha/2 = 1.96 (for 95% confidence)
- Z_beta = 0.84 (for 80% power)
- p = baseline conversion rate
- MDE = minimum detectable effect (typically 10-20% relative lift)
```

**Duration rule:**
```
Minimum days = Required sample size / Daily visitors
Never less than 14 days (capture weekly cycles)
Preferably 28 days (capture monthly cycles)
```

### 8. Implement winning changes

After a test reaches significance:
- Document the winner with exact lift percentage and confidence interval
- Implement permanently via code (not just the testing tool)
- Update the page template / component library
- Feed insights back into `dario-sales-letter` and `dario-funnel` for systemic improvement
- Log in test archive for institutional knowledge

## Commands

| Command | Description | Output |
|---|---|---|
| `*cro-research` | Full ResearchXL 6-layer diagnostic | Prioritized issue list with evidence |
| `*lift-audit` | LIFT Model scoring (6 factors) | Score card + recommendations |
| `*emotional-audit` | Talia Wolf emotional targeting analysis | Emotional gap map + fixes |
| `*attention-ratio` | Oli Gardner 1:1 attention ratio check | Ratio score + distraction inventory |
| `*form-audit` | Karl Gilis form optimization review | Field-by-field recommendations |
| `*trust-audit` | Andre Morys trust signal inventory | Trust score + placement map |
| `*pxl-rank` | PXL prioritization of test backlog | Ranked hypothesis table |
| `*test-plan` | Design a statistically valid A/B test | Full test spec document |
| `*teardown` | Oli-style landing page teardown/critique | Page-by-page annotated critique |
| `*ab-sample-size` | Calculate sample size for a test | Sample size + duration estimate |

## CRO audit scoring rubric

Overall CRO Health Score (0-100):

| Dimension | Weight | Score range | Assessment |
|---|---|---|---|
| **Value Proposition Clarity** | 20% | 0-20 | Is the offer immediately understood? |
| **Page Focus & Attention** | 15% | 0-15 | Single goal, no distractions? |
| **Trust & Credibility** | 20% | 0-20 | Social proof, authority, risk reversal? |
| **Form / CTA Optimization** | 15% | 0-15 | Frictionless path to conversion? |
| **Emotional Resonance** | 15% | 0-15 | Does the page connect emotionally? |
| **Technical Performance** | 15% | 0-15 | Fast, functional, mobile-ready? |

**Grading:**
- 85-100: Optimized -- fine-tuning and incremental testing
- 70-84: Good foundation -- targeted tests will yield lifts
- 50-69: Significant issues -- structured optimization program needed
- Below 50: Fundamental problems -- redesign before testing

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: cro-audit
page: <URL>
lift_score: <X/10>
cro_health: <X/100>
---

# CRO Audit -- <Client> -- <Page Name>

## Executive Summary
- Current conversion rate: X%
- Industry benchmark: Y%
- Gap: Z percentage points
- Top 3 issues identified: ...
- Estimated lift potential: X-Y%

## ResearchXL Findings
### Layer 1 -- Heuristic
...
### Layer 2 -- Technical
...
### Layer 3 -- Analytics
...
### Layer 4 -- Mouse tracking
...
### Layer 5 -- Qualitative
...
### Layer 6 -- Quantitative validation plan
...

## LIFT Score Card
| Factor | Score | Key finding |
|---|---|---|
| Value Proposition | /10 | ... |
| Relevance | /10 | ... |
| Clarity | /10 | ... |
| Anxiety | /10 | ... |
| Distraction | /10 | ... |
| Urgency | /10 | ... |

## Specialized Audits
### Emotional Targeting
...
### Attention Ratio
Current: X:1 | Target: 1:1
Distractions: ...

### Form Audit
Fields: X (recommend: Y)
Issues: ...

### Trust Signals
Present: ...
Missing: ...

## PXL Prioritized Test Backlog
| # | Hypothesis | PXL Score | Priority |
|---|---|---|---|
| 1 | ... | ... | HIGH |
| 2 | ... | ... | HIGH |
| 3 | ... | ... | MEDIUM |

## Test Plan -- Top Priority
### Test CRO-001
- Hypothesis: ...
- Variable: ...
- Sample size: ...
- Duration: ...
- Expected lift: ...

## Red Flags Detected
- [ ] ...

## Next Steps
1. ...
2. ...
3. ...
```

## Red flags / anti-patterns

- Homepage trying to be everything (about us + services + blog + testimonials + pricing on one page)
- Hero copy focused on features, not transformation ("We have 20 years of experience" vs "Double your leads in 90 days")
- Multiple competing CTAs on a single landing page (attention ratio > 5:1)
- Forms with 8+ fields when 3-4 would suffice
- Zero social proof anywhere on the page
- Testimonials without names, photos, or specifics ("Great service!" -- Anonymous)
- A/B tests ended before reaching statistical significance
- Testing button colors instead of value propositions (low-impact vanity tests)
- No urgency or scarcity element (no reason to act today vs next month)
- Mobile experience is an afterthought (desktop-designed page squeezed into mobile)
- CTA below the fold with no visual path leading to it
- "Submit" as button text on any form
- Trust signals buried in the footer where nobody scrolls
- Running experiments without a documented hypothesis
- Declaring a winner based on a few days of data (Simpson's paradox risk)

## Metrics to track

| Metric | Definition | Benchmark context |
|---|---|---|
| **Conversion Rate** | Completions / unique visitors | Varies by industry (SaaS trial: 3-8%, e-commerce: 1-4%, lead gen: 5-15%) |
| **Bounce Rate** | Single-page sessions / total sessions | Landing pages: 60-90% is normal; below 40% investigate tracking issues |
| **Form Abandonment** | Started but did not complete form / started | Target: < 30% |
| **Time on Page** | Median time before conversion or exit | Longer is not always better -- depends on page purpose |
| **Scroll Depth** | % of page viewed | 75%+ should see the CTA |
| **Click-Through Rate** | CTA clicks / page views | Depends on placement and copy |
| **Average Order Value** | Revenue / orders | Track lift from upsell/cross-sell tests |
| **Revenue Per Visitor** | Revenue / unique visitors | Ultimate e-commerce CRO metric |

## Integration with other DARIO skills

| Skill | Integration point |
|---|---|
| `dario-funnel` | CRO audits each funnel step; funnel provides the conversion flow to optimize |
| `dario-sales-letter` | Copy variants for A/B tests come from sales-letter frameworks; winning copy feeds back |
| `dario-brand` | Brand voice and positioning constrain what CRO changes are on-brand |
| `dario-offer` | A weak offer cannot be fixed by CRO -- if the value equation is broken, fix the offer first |
| `dario-ads-blueprint` | Ad-to-page congruence (message match) is a critical LIFT factor; ad copy must align with LP |
| `dario-wp-audit` | Technical CRO issues often surface in WP audit (speed, mobile, plugin conflicts) |
| `dario-cwv-fix` | Core Web Vitals directly impact bounce rate and conversion; fix CWV before CRO testing |
| `dario-content` | Content pages that should convert (pillar pages, comparison pages) need CRO lens |

## Save location

`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - CRO Audit.md`

## Critical rules

- Never run A/B tests without calculating required sample size first -- underpowered tests produce false positives that waste development resources and sometimes make conversion worse
- Never skip the ResearchXL diagnostic and jump straight to testing -- testing random ideas without research is guessing with extra steps
- Always check ad-to-page message match (LIFT relevance factor) before blaming the landing page -- if the ad promises X and the page delivers Y, no amount of page optimization will fix the disconnect
- Never optimize a page with broken Core Web Vitals -- a 6-second load time kills conversion before any copy or design change can help; run `dario-cwv-fix` first
- Always separate mobile and desktop analysis -- a page that converts at 5% on desktop and 0.5% on mobile is two different problems, not one
- Never declare a test winner without 95% statistical confidence AND a minimum of 14 days runtime -- weekly and daily traffic patterns can create false patterns that reverse after a full cycle
- Never test cosmetic changes (button color, font size) before structural changes (value proposition, offer, CTA copy) -- optimize the biggest levers first

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — ResearchXL 6 layers foram executados (não apenas mencionados)

- [ ] Cada uma das 6 layers tem findings concretos documentados (não "análise pendente")
- [ ] Layer 3 inclui métricas reais: CR atual, bounce rate, sessions/mês com números
- [ ] Layer 5 inclui pelo menos uma fonte qualitativa citada (survey, entrevista, review mining)
- [ ] Layer 6 inclui cálculo de sample size com poder estatístico definido

❌ NOT delivery-ready: "Análise heurística sugere que o headline pode ser melhorado e o CTA não está visível."  
✅ Delivery-ready: "Layer 1 — Heuristic: headline 'Gestão Financeira para PMEs' falha o teste dos 5 segundos (valor não está no headline, está no parágrafo 3). CTA 'Saiba Mais' abaixo do fold em 1280px. Layer 3 — Analytics: CR atual 1,2% (benchmark SaaS B2B PT: 3,1%). Bounce rate 74% mobile vs 48% desktop. Exit concentrada na página de pricing (67% dos non-converters)."

---

### Gate 2 — LIFT Score calculado com números reais, não estimativas vagas

- [ ] Cada um dos 6 factores tem score numérico 1-10 com justificação de 1 linha
- [ ] LIFT Score final calculado pela fórmula correta: (Value + Relevance + Clarity − Anxiety − Distraction + Urgency) / 6
- [ ] Diagnóstico de tier (8-10 / 5-7 / 1-4) explicitado com implicação prática
- [ ] Anxiety e Distraction têm exemplos concretos da página (não abstratos)

❌ NOT delivery-ready: "Score de Ansiedade é médio porque faltam elementos de confiança."  
✅ Delivery-ready: "Anxiety: 7/10 — formulário pede NIF + cartão antes de mostrar preço; 3 campos de segurança ausentes. Distraction: 6/10 — menu de navegação com 9 itens numa landing page, 4 links externos above the fold. LIFT Score = (6+7+5−7−6+4)/6 = **3,17 → tier 1-4: redesign antes de qualquer teste**."

---

### Gate 3 — PXL Backlog priorizado com ICE/PXL scores e hipóteses testáveis

- [ ] Mínimo 5 hipóteses de teste formuladas no formato "Se [mudança], então [métrica] aumenta X% porque [razão baseada em evidência]"
- [ ] Cada hipótese tem score PXL ou ICE (Impact × Confidence × Ease) numérico
- [ ] Sequência de testes ordenada com justificação (quick wins primeiro ou highest impact?)
- [ ] Cada teste tem página-alvo, variante clara, e métrica primária de sucesso definida

❌ NOT delivery-ready: "Recomendamos testar o headline e simplificar o formulário. Prioridade: alta."  
✅ Delivery-ready: "H1 — Reformular headline para incluir número concreto: 'Poupe 3h/semana em contabilidade'. ICE: I=9, C=8, E=9 → Score 72. Teste A/B: controlo vs variante, métrica primária: CTR para signup, secundária: time-on-page. Sample size necessário: 1.847 visitas por variante (poder 80%, α=0,05, MDE=15%)."

---

### Gate 4 — Plano de A/B test estatisticamente válido (não "vamos ver o que acontece")

- [ ] Sample size calculado explicitamente para cada teste prioritário (ferramenta ou fórmula citada)
- [ ] Duração mínima definida em semanas/ciclos de negócio (nunca "2-3 dias")
- [ ] Threshold de significância estatística declarado (mín. 95% confidence)
- [ ] Critérios de paragem antecipada (stopping rules) definidos para evitar peeking

❌ NOT delivery-ready: "O teste deve correr até ter resultados significativos. Recomendamos pelo menos 100 conversões."  
✅ Delivery-ready: "Sample size: 2.240 visitas/variante (baseline CR 1,2%, MDE 20%, α=0,05, poder 80% — calculado via Evan Miller). Com tráfego atual de 4.800 visitas/mês, duração mínima: 3,5 semanas = 2 ciclos de negócio completos. Stopping rules: não avaliar antes de 80% do sample size atingido; parar imediatamente se CR variante < 0,5% após 500 visitas/variante (dano activo)."

---

### Gate 5 — Trust audit com evidência específica, não checklist genérica

- [ ] Trust signals presentes identificados por nome e posição na página (não "faltam depoimentos")
- [ ] Trust signals em falta categorizados: social proof / authority / risk reversal / credibility markers
- [ ] Anxiety triggers específicos da indústria/ticket identificados (ex: RGPD para SaaS, garantia para e-commerce, credenciais para serviços profissionais)
- [ ] Quick wins de trust implementáveis sem A/B test identificados separadamente

❌ NOT delivery-ready: "A página precisa de mais provas sociais e deve transmitir mais confiança ao utilizador."  
✅ Delivery-ready: "Trust presente: logo 'Certificado pela CMVM' (posição: footer, invisível). Trust ausente: (1) zero depoimentos above the fold — sector fintech PT: benchmark 3+ reviews visíveis; (2) sem menção a RGPD no formulário — obrigatório para leads B2B PT; (3) preço ausente gera ansiedade de ticket (serviço €2.400/ano). Quick win sem teste: adicionar 'Sem compromisso. Cancelamento a qualquer momento.' sob o CTA → implementável em 30 min, impacto histórico: +8-12% CR em SaaS europeu."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets ou placeholders

- [ ] Zero ocorrências de `[CLIENT NAME]`, `[URL]`, `[METRIC]`, `[INSERT HERE]` ou equivalentes
- [ ] Nome da empresa aparece no título do audit e nas hipóteses de teste
- [ ] Todas as métricas têm fonte declarada (GA4, Hotjar, dados fornecidos pelo cliente)
- [ ] Recomendações referem páginas específicas por URL ou nome de secção real

❌ NOT delivery-ready: "Para [Nome da Empresa], recomendamos testar [variante] na página [URL da landing page]."  
✅ Delivery-ready: "Para LUSOconta — Audit CRO · landing page lusoconta.pt/abrir-conta (dados GA4 exportados 2024-11-01 a 2025-01-31): CR actual 1,2%, 4.800 sessões/mês, bounce 74% mobile. Hipótese H1: reformular headline para 'Abra a sua conta empresarial em 7 minutos — sem deslocações' aumenta CR ≥ 15% porque…"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# CRO Audit — LUSOconta · lusoconta.pt/abrir-conta
**Data:** 2025-01-31 | **Analista:** DARIO CRO Squad | **Tráfego base:** Jan 2025 (GA4)

---

## ResearchXL — 6-Layer Findings

**Layer 1 — Heuristic**
- Headline: "A conta que trabalha para si" — falha teste dos 5 segundos (sem número, sem diferenciador)
- CTA "Abrir Conta" visível above the fold em desktop, abaixo do fold em mobile (375px)
- Visual hierarchy: 3 CTAs concorrentes no header (Login / Tarifas / Abrir Conta) — distração activa
- Trust: selo "Banco de Portugal supervisionado" em footer cinzento, tamanho 10px — invisível

**Layer 2 — Técnica**
- LCP: 4,1s mobile (target < 2,5s) — imagem hero 1,8MB não comprimida
- CLS: 0,18 (threshold: < 0,1) — banner de cookies empurra conteúdo ao carregar
- Formulário: erro de validação NIF sem mensagem explicativa ("Campo inválido")

**Layer 3 — Analytics (GA4, Jan 2025)**
- Sessões: 4.847 | Conversões (conta aberta): 58 | **CR: 1,20%**
- Benchmark fintech PT abertura de conta digital: 3,5–5% (fonte: Fintech Portugal 2024)
- Mobile: 67% do tráfego, CR mobile 0,61% vs desktop 2,31%
- Exit rate formulário step 2 (dados fiscais): 71%

**Layer 4 — Heatmap (Hotjar, Jan 2025, n=1.240 sessões)**
- Scroll: apenas 34% dos visitantes chegam à secção de benefícios (below the fold 800px)
- Rage clicks: botão "Ver Tarifas" no header recebe 18% dos cliques — utilizadores procuram preço
- Click map: "Supervisionado pelo Banco de Portugal" (footer) tem 0 cliques — não comunica

**Layer 5 — Qualitativo**
- Exit survey (n=47): 38% "Não percebi o que estava incluído na conta"; 29% "Fiquei preso no passo do NIF"
- Review mining Trustpilot LUSOconta (n=312 reviews): objecção #1 "Não sabia se era grátis" (41 menções)

**Layer 6 — Quantitativo**
- MDE alvo: 20% uplift relativo (CR 1,20% → 1,44%)
- Sample size: 2.240 visitas/variante (α=0,05, poder 80%)
- Duração estimada: 3,7 semanas com tráfego actual

---

## LIFT Score — lusoconta.pt/abrir-conta

| Factor | Score | Justificação |
|---|---|---|
| Value Proposition | 4/10 | Headline genérico, sem menção a "grátis", "sem mensalidade" ou tempo de abertura |
| Relevance | 6/10 | Página alinhada com pesquisas "abrir conta empresa online" mas sem personalização por segmento |
| Clarity | 4/10 | 3 CTAs concorrentes; passo 2 do formulário sem instrução para o NIF |
| Anxiety | 7/10 | Preço não visível above the fold; NIF pedido antes de mostrar benefícios |
| Distraction | 7/10 | Menu completo + 4 links de saída na landing page |
| Urgency | 2/10 | Zero urgência — sem oferta limitada, sem "abertura hoje = X" |

**LIFT Score = (4+6+4−7−7+2)/6 = 0,33 → Tier 1-4: resolver problemas fundamentais antes de A/B tests pontuais**

---

## PXL Backlog — Top 5 Hipóteses

| # | Hipótese | ICE Score | Sample Size | Duração |
|---|---|---|---|---|
| H1 | Headline "Abra a sua conta em 7 min — sem custos de manutenção" aumenta CR ≥20% porque resolve objecção #1 (38% exit survey) | I=9 C=8 E=9 → **72** | 2.240/var | 3,7 sem |
| H2 | Remover menu de navegação da landing aumenta CR ≥15% (attention ratio 1:1) | I=8 C=9 E=8 → **64** | 2.612/var | 4,3 sem |
| H3 | Adicionar barra de progresso no formulário reduz abandono step 2 ≥25% | I=8 C=7 E=7 → **56** | 3.110/var | 5,2 sem |
| H4 | Mover selo "Banco de Portugal" para junto do CTA aumenta CR ≥10% | I=6 C=8 E=9 → **54** | 4.490/var | 7,4 sem |
| H5 | Adicionar urgência ("247 contas abertas hoje") aumenta CR ≥12% | I=7 C=6 E=7 → **42** | 3.640/var | 6,0 sem |

**Quick wins sem A/B test (implementar imediatamente):**
- Comprimir imagem hero: LCP 4,1s → ~2,1s (impacto estimado CR mobile: +0,3-0,5pp)
- Adicionar "Sem custos de manutenção. Cancelamento a qualquer momento." sob CTA
- Corrigir mensagem de erro NIF: "O NIF deve ter 9 dígitos — ex: 123456789"

---

## Plano A/B Test — H1 (Prioritário)

**Teste:** Headline controlo vs variante  
**Controlo (A):** "A conta que trabalha para si"  
**Variante (B):** "Abra a sua conta empresarial em 7 minutos — sem custos de manutenção"  
**Ferramenta:** VWO / Google Optimize  
**Métrica primária:** CR (conta aberta) | **Métrica secundária:** CTR para step 1 do formulário  
**Sample size:** 2.240 visitas/variante | **Duração mínima:** 3,7 semanas (2 ciclos completos)  
**Threshold:** 95% confidence (p < 0,05) | **Stopping rules:** não avaliar antes de 80% do sample; parar se CR variante < 0,6% após 500 visitas
```

---

## Output anti-patterns

- **Audit sem números**: escrever "a taxa de conversão está baixa" sem o valor actual e benchmark do sector
- **LIFT Score sem fórmula aplicada**: listar os 6 factores mas não calcular o score final nem determinar o tier de acção
- **Hipóteses não falsificáveis**: "testar headline diferente" em vez de "Se headline X, então CR aumenta ≥Y% porque evidência Z"
- **Sample size em falta ou inventado**: dizer "precisamos de 1.000 visitas" sem cálculo baseado em baseline CR, MDE e poder estatístico
- **Trust audit genérico**: "adicionar depoimentos e selos de segurança" sem especificar posição na página, formato e urgência relativa
- **Recomendações de redesign disfarçadas de A/B test**: propor redesign completo como "variante B" invalida o teste — uma variável de cada vez
- **Ignorar mobile vs desktop split**: apresentar CR agregado quando split mobile/desktop revela problema isolado (e.g. 0,61% vs 2,31%)
- **Ausência de stopping rules**: plano de teste sem critérios de paragem antecipada leva a peeking e falsos positivos
- **Quick wins misturados com testes**: implementar quick wins como variante num A/B test contamina os resultados — separar sempre
- **Placeholders no output final**: entregar documento com `[inserir URL]`, `[nome do cliente]` ou `[métrica a confirmar]`
