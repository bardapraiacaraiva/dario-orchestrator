---
name: dario-data
description: Data squad — analytics, customer science, and growth hacking. Avinash Kaushik (See-Think-Do-Care, 10/90 rule), Peter Fader (CLV, Pareto/NBD), Sean Ellis (PMF, North Star Metric, AARRR, ICE). Triggers on "data", "analytics", "metrics", "CLV", "LTV", "churn", "cohort", "PMF", "north star metric", "AARRR", "pirate metrics", "growth", "activation", "retention", "ICE score", "dashboard".
version: 1.0.0
license: MIT
---

# DARIO Skill — Data Squad

Three minds, one mission: turn data into decisions. Combines Avinash Kaushik's digital analytics philosophy, Peter Fader's customer-centric CLV science, and Sean Ellis's growth hacking methodology into a single skill that answers "what should we measure, what does it mean, and what do we do about it?"

## Squad Agents

| Agent | Mindset | Core Philosophy | Superpower |
|-------|---------|----------------|------------|
| **Chief Data (Kaushik)** | "Fail faster, succeed sooner" | 10/90 rule: spend 10% on tools, 90% on people who analyze. See-Think-Do-Care framework for audience intent. | Cutting through vanity metrics to find actionable insights |
| **Customer Data Scientist (Fader)** | "Not all customers are created equal" | CLV models, customer-centricity, probability models (Pareto/NBD, BG/NBD). Future value > past revenue. | Predicting which customers matter most and why |
| **Growth Hacker (Ellis)** | "If you're not growing, you're dying" | Product-market fit test, North Star Metric, AARRR pirate metrics, ICE scoring for experiment prioritization. | Systematic experimentation for compounding growth |
| **Analytics Engineer** | "Garbage in, garbage out" | Data pipeline quality, warehouse design, metric definitions, dashboard architecture. The infrastructure that makes insights possible. | Building the measurement foundation everyone else depends on |

## When to activate

- "What should we be measuring?" — metric framework design
- "We have data but don't know what it means" — analysis and interpretation
- "How do we know if we have product-market fit?" — PMF assessment
- "Which customers should we focus on?" — CLV segmentation
- "Our growth is flat/declining" — growth audit and experiment design
- "We need a dashboard" — dashboard specification with the right metrics
- New product/feature launch — measurement plan before launch
- Fundraising preparation — metrics narrative for investors
- SaaS metrics deep-dive (MRR, churn, NRR, CAC payback)
- Cohort analysis request — retention curves, revenue cohorts
- Before any paid campaign — baseline metrics + attribution model
- User mentions LUSOconta, Atelier AI, or any SaaS project — data-driven product decisions

## Workflow

### 1. Gather context

- **Business model:** SaaS, e-commerce, marketplace, agency, services?
- **Stage:** pre-PMF, post-PMF, growth, scale?
- **Current data:** what's tracked, what tools exist (GA4, Mixpanel, Amplitude, Stripe, custom)?
- **Team:** who looks at data? How often? What decisions do they make with it?
- **Burning question:** what do they actually want to know?
- **Historical data:** how much history is available? (Months? Years?)

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "avinash kaushik see think do care framework analytics", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "peter fader CLV customer lifetime value pareto NBD", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "sean ellis product market fit north star metric AARRR", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "growth hacking ICE scoring experiment prioritization", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "cohort analysis retention churn SaaS metrics", collection: "dario", limit: 5)
```

### 3. Apply frameworks

#### Kaushik: See-Think-Do-Care

Map every metric and content piece to an audience intent stage:

| Stage | Audience | Intent | Key Metrics | Content Type |
|-------|----------|--------|-------------|-------------|
| **See** | Largest addressable qualified audience | Awareness, no intent to buy | Impressions, reach, brand search volume, new visitors | Blog, video, social, PR |
| **Think** | Audience with some commercial intent | Considering, researching | Engagement rate, time on site, pages/session, email signups | Comparison guides, webinars, case studies |
| **Do** | Audience with clear intent to buy | Ready to transact | Conversion rate, add-to-cart, sign-ups, trials, revenue | Product pages, pricing, demos, offers |
| **Care** | Existing customers (2+ purchases) | Loyalty, expansion | NPS, repeat purchase rate, CLV, upsell rate, referral rate | Onboarding, support, community, loyalty programs |

**Kaushik's 10/90 rule:** If the analytics budget is $100, spend $10 on tools and $90 on analysts who can extract insights. Tools without human interpretation produce dashboards no one reads.

#### Fader: Customer Lifetime Value (CLV)

**CLV = Average Revenue per Period x Customer Lifetime (periods) x Gross Margin**

For more sophisticated modeling:
- **Pareto/NBD model:** Predicts future purchasing behavior based on recency and frequency
- **BG/NBD model:** Simplified version, better for contractual settings (SaaS)
- **Gamma-Gamma model:** Predicts monetary value conditional on purchase frequency

**Key CLV insights:**
- Top 20% of customers typically generate 60-80% of revenue (Pareto principle)
- Acquiring a new customer costs 5-25x more than retaining an existing one
- A 5% increase in retention can increase profits by 25-95%
- CLV should guide: marketing spend allocation, feature prioritization, support investment

**CLV segmentation matrix:**

| Segment | CLV | Recency | Strategy |
|---------|-----|---------|----------|
| **Champions** | High | Recent | Reward, upsell, ask for referrals |
| **Loyal** | High | Moderate | Engage, prevent churn, deepen relationship |
| **At Risk** | High | Lapsed | Win-back campaign, personal outreach, understand why |
| **New High-Potential** | Low (so far) | Very recent | Activate quickly, onboard well, nurture toward champion |
| **Low Value** | Low | Any | Automate, self-serve, don't over-invest |

#### Ellis: Product-Market Fit & Growth

**PMF Test (Sean Ellis Test):**
Ask existing users: "How would you feel if you could no longer use [product]?"
- **Very disappointed** → PMF signal
- **Somewhat disappointed** → Weak signal
- **Not disappointed** → No PMF

**Threshold:** If 40%+ say "very disappointed," you have PMF. Below 40%, iterate on the product before scaling.

**North Star Metric (NSM):**
The single metric that best captures the core value your product delivers to customers.

| Business Type | NSM Example |
|---------------|-------------|
| SaaS | Weekly active users, or features used per session |
| E-commerce | Purchase frequency per customer |
| Marketplace | Transactions completed per week |
| Content/Media | Time spent reading/watching per session |
| Agency | Recurring retainer revenue |

**Rules for a good NSM:**
- Reflects customer value received (not just company revenue)
- Leading indicator of revenue (not lagging)
- Measurable weekly
- Actionable by the team
- One metric, not a composite

#### AARRR Pirate Metrics

| Stage | Metric | Benchmark (SaaS) | Diagnostic Question |
|-------|--------|-------------------|-------------------|
| **Acquisition** | Visitors, signups by channel | CAC varies by channel | "Where do our best customers come from?" |
| **Activation** | % completing key action within X days | 20-40% typical | "Do new users experience the aha moment?" |
| **Retention** | Day 1, Day 7, Day 30 retention | D1: 40%, D7: 20%, D30: 10% | "Do users come back after first use?" |
| **Revenue** | Conversion to paid, ARPU, MRR | Trial→paid: 2-5% (freemium), 15-25% (free trial) | "Do retained users pay?" |
| **Referral** | Viral coefficient, NPS, referral rate | K-factor > 0.5 is strong | "Do users tell others?" |

**Diagnosis priority:** Fix from the bottom up. Referral without retention is a leaky bucket. Revenue without activation means you're charging before delivering value. Always fix retention first.

#### ICE Scoring for Experiment Prioritization

For every growth experiment, score 1-10 on three dimensions:

| Dimension | Question | 1 (Low) | 10 (High) |
|-----------|----------|---------|-----------|
| **Impact** | If this works, how big is the effect? | Marginal improvement | 2x or more on target metric |
| **Confidence** | How sure are we this will work? | Pure guess | Strong data/precedent |
| **Ease** | How easy is this to implement? | Months of engineering | Ship in a day |

**ICE Score = (Impact + Confidence + Ease) / 3**

Run experiments in ICE score order. Review scores weekly. Kill experiments that don't move the metric within the test period.

### 4. Core metrics reference

#### SaaS Metrics (for LUSOconta, Atelier AI, and future SaaS)

| Metric | Formula | Healthy Range | Red Flag |
|--------|---------|---------------|----------|
| **MRR** | Sum of all monthly recurring revenue | Growing month-over-month | Flat or declining for 2+ months |
| **ARR** | MRR x 12 | Aligns with growth targets | Diverges from fundraise projections |
| **Net Revenue Retention (NRR)** | (Starting MRR + expansion - contraction - churn) / Starting MRR | > 100% (ideally > 110%) | < 90% means shrinking without new customers |
| **Gross Churn** | Lost MRR / Starting MRR | < 3% monthly (< 5% for SMB) | > 5% monthly — product or market problem |
| **CAC** | Total sales+marketing spend / New customers | Varies by ACV | CAC > 12 months of revenue |
| **LTV** | ARPU x (1 / Monthly Churn Rate) x Gross Margin | LTV:CAC > 3:1 | LTV:CAC < 1:1 — losing money on every customer |
| **CAC Payback** | CAC / Monthly Gross Margin per Customer | < 12 months | > 18 months — cash flow risk |
| **Activation Rate** | % of signups completing key action | > 25% | < 10% — onboarding is broken |
| **Trial-to-Paid** | % of trial users converting to paid | 15-25% (free trial), 2-5% (freemium) | < 1% — value proposition unclear |

#### E-commerce / Agency Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **CAC** | Marketing spend / New customers | Track by channel |
| **AOV** | Revenue / Orders | Increase with bundles, upsells |
| **Purchase Frequency** | Orders / Unique customers | Per year |
| **Customer Retention Rate** | Customers at end / Customers at start | Excludes new acquisitions |
| **NPS** | % Promoters - % Detractors | > 50 is excellent |
| **Revenue per Employee** | Total revenue / FTE count | Agency benchmark: 100-200K EUR/year |

### 5. Dashboard specification

Every dashboard must answer: "What happened, why, and what should we do about it?"

**Structure:**
1. **Header:** NSM trend (current vs previous period vs target)
2. **AARRR funnel:** Each stage with trend arrows
3. **Cohort retention grid:** Monthly cohorts, retention by week/month
4. **Revenue breakdown:** By plan, by channel, by segment
5. **Experiment tracker:** Active experiments, results, next actions
6. **Alerts:** Metrics outside normal range

## Commands

| Command | Description |
|---------|-------------|
| `/pmf-test` | Design and analyze a Sean Ellis PMF survey — question design, distribution, scoring, interpretation |
| `/nsm-define` | Define the North Star Metric for a product — candidates, evaluation criteria, selection, input metrics |
| `/aarrr-audit` | Full AARRR pirate metrics audit — measure each stage, identify the weakest link, prioritize fixes |
| `/ice-backlog` | Create ICE-scored experiment backlog — brainstorm experiments, score each, rank by ICE, plan sprints |
| `/activation-optimize` | Activation rate deep-dive — map the activation funnel, find drop-off points, design experiments |
| `/clv-model` | Build CLV model — RFM segmentation, CLV calculation, segment strategies, marketing budget allocation |
| `/cohort-analysis` | Cohort retention analysis — build retention curves, identify healthy vs leaky cohorts, find patterns |
| `/dashboard-spec` | Design executive dashboard — metric selection, layout, data sources, update cadence, alert thresholds |
| `/metric-define` | Define a specific metric precisely — formula, data source, filters, frequency, owner, target |
| `/growth-audit` | Full growth audit — current state, bottlenecks, experiment history, recommended growth model |
| `/data-quality` | Data quality assessment — coverage, accuracy, freshness, consistency, gaps, remediation plan |
| `/attribution` | Marketing attribution model — channel performance, attribution methodology, budget reallocation |

## Output template

```markdown
---
project: <client or product>
date: <YYYY-MM-DD>
type: data-analysis
framework: <kaushik|fader|ellis|combined>
---

# Data Analysis — <Topic>

## Context
- Business: ...
- Model: SaaS / E-commerce / Agency / ...
- Stage: Pre-PMF / Post-PMF / Growth / Scale
- Data available: ...
- Burning question: ...

## Current State
### Key Metrics Snapshot
| Metric | Current | Previous Period | Trend | Target | Status |
|--------|---------|----------------|-------|--------|--------|
| ... | ... | ... | ... | ... | OK / Warning / Critical |

### See-Think-Do-Care Mapping
| Stage | Current Activity | Metrics | Gap |
|-------|-----------------|---------|-----|
| See | ... | ... | ... |
| Think | ... | ... | ... |
| Do | ... | ... | ... |
| Care | ... | ... | ... |

## Analysis

### PMF Assessment (if applicable)
- Ellis Test result: ...% "very disappointed"
- PMF status: Achieved / Approaching / Not yet
- Key signal: ...

### CLV Segmentation
| Segment | % of Customers | % of Revenue | Strategy |
|---------|---------------|-------------|----------|
| Champions | ... | ... | ... |
| Loyal | ... | ... | ... |
| At Risk | ... | ... | ... |
| Low Value | ... | ... | ... |

### AARRR Funnel
| Stage | Volume | Rate | Benchmark | Verdict |
|-------|--------|------|-----------|---------|
| Acquisition | ... | ... | ... | ... |
| Activation | ... | ... | ... | ... |
| Retention | ... | ... | ... | ... |
| Revenue | ... | ... | ... | ... |
| Referral | ... | ... | ... | ... |

**Weakest stage:** ...
**Recommended focus:** ...

### Cohort Retention
| Cohort | M0 | M1 | M2 | M3 | M6 | M12 |
|--------|----|----|----|----|----|----|
| ... | ... | ... | ... | ... | ... | ... |

## Recommendations

### North Star Metric
**Proposed NSM:** ...
**Rationale:** ...
**Input metrics:** ...

### Experiment Backlog (ICE-ranked)
| # | Experiment | Impact | Confidence | Ease | ICE | Status |
|---|-----------|--------|-----------|------|-----|--------|
| 1 | ... | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... | ... |

### Quick Wins (this week)
1. ...
2. ...
3. ...

### Strategic Moves (this quarter)
1. ...
2. ...

## Dashboard Specification
### Metrics to track
- ...
### Update cadence
- ...
### Alert thresholds
- ...

## Next Steps
- [ ] ...
```

## Save location

- Analytics reports → `05 - Claude - IA/Outputs/YYYY-MM-DD - Data - <Topic>.md`
- CLV models → `05 - Claude - IA/Outputs/YYYY-MM-DD - CLV Model - <Client>.md`
- Dashboard specs → `05 - Claude - IA/Outputs/YYYY-MM-DD - Dashboard Spec - <Client>.md`
- Growth audits → `05 - Claude - IA/Outputs/YYYY-MM-DD - Growth Audit - <Client>.md`

## Integration points

| Skill | Relationship |
|-------|-------------|
| `dario-c-level` | Data squad feeds metrics to CEO/CMO/COO for strategic decisions |
| `dario-saas-metrics` | Overlapping domain — use `dario-saas-metrics` for SaaS-specific deep dives, this skill for broader analytics |
| `dario-financial-model` | CLV and revenue metrics feed financial projections |
| `dario-pipeline` | Pipeline math uses data squad's conversion rate analysis |
| `dario-ads-blueprint` | Attribution and ROAS analysis for paid campaigns |
| `dario-product` | Product metrics (activation, retention) inform feature prioritization |
| `dario-product-mgmt` | NSM, AARRR, and ICE scoring shared with product management workflow |
| `dario-ai-engineering` | Data quality and pipeline design for AI systems |
| `dario-funnel` | Funnel conversion metrics and optimization |
| `dario-diagnose` | Diagnostic uses data squad for quantitative assessment |
| `dario-wp-audit` | Analytics audit as part of WordPress evaluation |
| `dario-obsidian-save` | All outputs saved to vault |

## Red flags / anti-patterns

- **Vanity metrics worship** — page views, total signups, social followers without context are vanity metrics. They go up and to the right but don't correlate with business outcomes. Always tie metrics to revenue or retention.
- **Dashboard without decisions** — a dashboard that no one looks at or that doesn't change behavior is wasted effort. Every metric on a dashboard must have an owner, a target, and a documented "if X happens, we do Y" response.
- **Premature optimization** — optimizing conversion rate when you have 50 visitors/month is statistical noise. You need volume before optimization makes sense. Focus on acquisition first, then optimize.
- **Measuring everything, analyzing nothing** — Kaushik's 10/90 rule. A team with 15 analytics tools and no analyst is worse off than a team with a spreadsheet and someone who thinks. Invest in people, not tools.
- **CLV without action** — calculating CLV and then treating all customers the same defeats the purpose. CLV must drive differentiated strategies: more investment in high-CLV segments, automated/self-serve for low-CLV.
- **Ignoring retention to chase acquisition** — a product with 5% monthly churn loses half its customers in a year. No amount of acquisition can outrun bad retention. Fix retention before scaling acquisition.
- **ICE scores without data** — assigning ICE scores based on gut feeling, then treating them as objective rankings. The scores are heuristics to structure debate, not truth. Update them as you learn.
- **Cohort analysis without segmentation** — aggregate retention curves hide segment-level insights. A flat retention curve might be the average of one segment with 80% retention and another with 10%. Always segment.
- **North Star Metric that the team can't influence** — an NSM that depends on external factors (market growth, competitor actions) rather than product/team actions is useless for decision-making. The team must be able to move the NSM through their work.
- **Attribution certainty** — no attribution model is perfect. Last-click, first-click, linear, and data-driven all have biases. Acknowledge the limitations, use directional guidance, and never make absolute claims about channel ROI.

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Metric Framework tem North Star + métricas de apoio definidas

- [ ] North Star Metric nomeada com fórmula explícita (não só "engagement")
- [ ] 3–5 supporting metrics mapeadas ao funil AARRR correto
- [ ] Vanity metrics excluídas ou explicitamente marcadas como tal
- [ ] Cada métrica tem owner, frequência de reporte, e threshold de alerta

❌ NOT delivery-ready: "Deves medir engagement e retenção para perceber o crescimento."
✅ Delivery-ready: "North Star da LUSOconta: Transações conciliadas por utilizador ativo/mês (meta: ≥8 até Q3-2025). Supporting: DAU/MAU ratio (target 0.35), % utilizadores que conciliam no D3 pós-onboarding (target 62%), involuntary churn rate (target <1.2%/mês)."

---

### Gate 2 — CLV/Segmentação com dados reais do cliente

- [ ] CLV calculado com fórmula explícita e valores preenchidos (ARPU, margem, lifetime)
- [ ] Pelo menos 3 segmentos Fader (Champions / At Risk / New High-Potential) com critérios mensuráveis
- [ ] Estratégia diferenciada por segmento (não genérica)
- [ ] Pareto validado ou estimado: % clientes top → % receita

❌ NOT delivery-ready: "Os teus melhores clientes merecem atenção especial e campanhas de retenção."
✅ Delivery-ready: "Atelier AI — CLV médio: €47/mês × 11 meses × 72% margem = €372. Top 18% dos clientes (planos Team+) geram 71% da MRR. Champions (recência <30 dias + ≥3 projetos ativos): estratégia de upsell para API credits. At Risk (recência 61–90 dias, plano Solo): win-back sequence 3 emails com oferta de onboarding 1:1."

---

### Gate 3 — See-Think-Do-Care mapeado ao modelo de negócio específico

- [ ] Cada estágio tem métricas concretas, não placeholder
- [ ] Conteúdo recomendado por estágio é específico ao produto/mercado
- [ ] Budget/esforço alocado reflete 10/90 rule (não propor 5 ferramentas sem analista)
- [ ] "Care" stage não está vazio — tem métricas de expansão e NPS definidos

❌ NOT delivery-ready: "No estágio See deves focar em awareness. No Do foca em conversão."
✅ Delivery-ready: "SAQUEI — See: impressões LinkedIn Posts sobre 'crédito para empresas' (baseline 12k/mês); Think: tempo médio em /como-funciona ≥2m30s, taxa de download do guia PDF >4%; Do: submissões de pedido de crédito (target 38/semana, atual 21); Care: NPS pós-desembolso (target 52), taxa de segundo empréstimo em 6 meses (target 29%)."

---

### Gate 4 — PMF Assessment com score e próximos passos

- [ ] Sean Ellis test aplicado (% "muito desapontado" calculada ou estimada com método)
- [ ] Threshold 40% explicado e contextualizado para o estágio do produto
- [ ] Se pré-PMF: recomendações de retenção qualitativas + quantitativas
- [ ] Se pós-PMF: North Star e experimentos ICE priorizados, não só "escalar"

❌ NOT delivery-ready: "Ainda não tens product-market fit. Fala com os utilizadores e itera."
✅ Delivery-ready: "Pupli — Survey a 87 utilizadores ativos: 34% 'muito desapontado' (abaixo dos 40%). Segmento que passa o threshold: treinadores independentes com carteira ≥8 cães (52% neste sub-grupo). Próximo passo: redesenhar onboarding para este ICP, parar growth spend até D30-retention ≥35% neste segmento."

---

### Gate 5 — ICE Scoring com experimentos ranqueados

- [ ] Mínimo 4 experimentos propostos com ICE (Impact 1–10, Confidence 1–10, Ease 1–10)
- [ ] ICE Score = média das 3 dimensões, não apenas soma
- [ ] Hipótese de cada experimento formulada como "Se X então Y porque Z"
- [ ] Quick win (ICE ≥7, tempo <2 semanas) identificado explicitamente

❌ NOT delivery-ready: "Testa diferentes CTAs e melhora o onboarding. Prioriza o que for mais fácil."
✅ Delivery-ready: "Cuidai — Experimento #1 (ICE 8.3): 'Se adicionarmos progress bar no onboarding (4 passos visíveis), a taxa de activação D1 sobe de 41% para 55%, porque utilizadores sabem quanto falta.' Impact 9, Confidence 8, Ease 8. Quick win — implementar em 5 dias. Experimento #2 (ICE 6.7): email de re-activação ao D7 para utilizadores sem 1ª consulta agendada. Impact 8, Confidence 7, Ease 5."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero angle-brackets

- [ ] Nenhum `<client_name>`, `<insert metric>`, `<your product>` no output final
- [ ] Todos os números são reais (fornecidos pelo cliente) ou estimativas explicitamente marcadas como `[estimativa — validar]`
- [ ] Nome do produto/empresa aparece pelo menos 3x no output
- [ ] Datas e períodos concretos (ex: "Q2-2025", "últimos 90 dias") em vez de "recentemente" ou "em breve"

❌ NOT delivery-ready: "A <empresa> deve focar em melhorar o <metric principal> no próximo trimestre."
✅ Delivery-ready: "A LUSOconta deve focar em aumentar a taxa de conciliação D3 de 38% para 55% até 30-Jun-2025, através dos 3 experimentos ICE priorizados abaixo."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmed from prior session/memory/cliente data
- 🟡 **assumed** — plausible but needs cliente confirm pre-delivery
- 🟢 **projection** — forecast by design (not verifiable)

Output checklist upfront mostra reader exactly o que é trust-as-is vs precisa verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready: análise CLV entregue sem labels — "o teu CAC payback é 8 meses, NRR está em 104%, os top 20% de clientes geram 68% da receita" — reader assume que todos os números são verified quando podem ser assumptions baseadas em benchmarks de sector, não nos dados reais do cliente.

✅ Delivery-ready:
- 🔵 **verified** — CAC payback = 8 meses (calculado a partir dos dados Stripe + spend Google Ads fornecidos)
- 🟡 **assumed** — NRR ~104% (estimado via churn rate declarado; confirmar com MRR expansion real)
- 🟢 **projection** — top 20% clientes → 68% receita em 12 meses (modelo Pareto/NBD aplicado à cohort actual; não é histórico)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir benchmarks/sector assumptions com actuals do cliente (ex: churn rate real, ARPU por segmento, histórico de cohorts disponível)
- [ ] All 🔵 citations added — fonte explícita por cada métrica verified (ex: "Stripe export 2024-Q1", "GA4 funnel report", "Mixpanel retention dashboard")
- [ ] All 🟢 projections labeled as such ao cliente — CLV forecasts, North Star Metric targets e ICE score outcomes comunicados como modelos/projecções, não como resultados garantidos

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Data Squad Report — Atelier AI
**Data:** 14-Mai-2025 | **Modelo:** SaaS B2B | **Estágio:** Post-PMF inicial

---

## North Star Metric

**Projetos AI publicados por workspace ativo/mês**
- Fórmula: (Projetos publicados totais) ÷ (Workspaces com ≥1 login nos últimos 30 dias)
- Baseline atual: 2.1 projetos/workspace/mês
- Target Q3-2025: 4.0 projetos/workspace/mês
- Porquê: correlaciona 0.81 com expansão de receita a 90 dias (dado de coorte Jan–Mar 2025)

---

## AARRR — Atelier AI

| Estágio | Métrica | Atual | Target | Owner |
|---------|---------|-------|--------|-------|
| Acquisition | Signups orgânicos/semana | 47 | 80 | Marketing |
| Activation | % workspaces com 1º projeto publicado em D7 | 38% | 58% | Product |
| Retention | D30 retention (workspaces ativos) | 44% | 60% | Product |
| Revenue | MRR expansion rate (upsell/cross-sell) | 6%/mês | 11%/mês | CS |
| Referral | % novos signups via link de referral | 9% | 18% | Growth |

---

## CLV Segmentação — Fader Model

**CLV médio calculado:** €41/mês ARPU × 13.2 meses lifetime × 69% margem = **€374**

| Segmento | Critério | N Clientes | % MRR | Estratégia |
|----------|----------|------------|-------|------------|
| Champions | Recência ≤21 dias + ≥5 projetos/mês | 89 | 58% | Upsell API credits; programa beta features |
| Loyals | Recência ≤45 dias + 2–4 projetos/mês | 143 | 27% | Nurture com templates; webinar mensal |
| At Risk | Recência 46–75 dias, plano pago | 61 | 11% | Win-back: email pessoal do founder + oferta 1 mês |
| Churned High-Value | Recência >75 dias, ex-plano Team | 29 | 0% | Outreach manual; entender motivo; produto roadmap |

**Pareto observado:** 18% dos clientes (Champions + topo dos Loyals) → 72% do MRR.

---

## PMF Assessment — Sean Ellis

**Survey enviado:** 12-Mai-2025, n=134 respostas (utilizadores ativos últimos 60 dias)

- "Muito desapontado" se Atelier AI desaparecesse: **46%** ✅ Acima do threshold 40%
- Segmento mais forte: Product Managers em equipas 5–20 pessoas (61% "muito desapontado")
- Segmento fraco: Freelancers solo (28% — abaixo do threshold)

**Conclusão:** PMF confirmado para ICP B2B mid-market. Não escalar aquisição freelancer até reengenharia do onboarding para este segmento.

---

## See-Think-Do-Care — Atelier AI

| Estágio | Audiência | Métricas-Chave | Ação Prioritária |
|---------|-----------|----------------|-----------------|
| See | PMs e tech leads em empresas 10–200 pessoas PT/BR | LinkedIn impressions (atual 28k/mês), brand search "atelier AI" (atual 340/mês) | 2 posts/semana sobre "AI workflows para produto" |
| Think | Visitantes /features e /pricing com >1m30s | Páginas/sessão (atual 2.1, target 3.2), demo request rate (atual 1.8%) | Caso de estudo Cuidai publicado em blog |
| Do | Trial signups | Conversão trial→pago (atual 22%, target 31%), TTV 1º projeto <D3 | Redesign onboarding: 4 passos com progress bar |
| Care | Clientes ativos (Champions + Loyals) | NPS (atual 51), expansion MRR (atual 6%/mês) | Programa "AI Builder" — templates exclusivos mensais |

---

## ICE Experiments — Sprint Mai–Jun 2025

| # | Hipótese | I | C | E | ICE | Prazo |
|---|----------|---|---|---|-----|-------|
| 1 | Progress bar onboarding → activação D7 38%→55% | 9 | 8 | 8 | **8.3** | 1 semana |
| 2 | Email D7 para workspaces sem projeto publicado → reactivação +18% | 8 | 7 | 6 | **7.0** | 10 dias |
| 3 | Caso de estudo Cuidai em /pricing → trial CVR +4pp | 7 | 6 | 7 | **6.7** | 2 semanas |
| 4 | Referral program (créditos por convite aceite) → referral 9%→16% | 8 | 5 | 5 | **6.0** | 3 semanas |

**Quick win imediato:** Experimento #1 — impacto alto, 5 dias de eng., zero risco de regressão.

---

**Próxima revisão de métricas:** 11-Jun-2025 | **Owner:** Diogo (Product) + Ana (Growth)
```

---

## Output anti-patterns

- Listar "métricas importantes" sem fórmulas, owners, ou baselines reais — transforma dashboards em decoração
- Recomendar ferramentas (Mixpanel, Amplitude, Looker) sem verificar se o cliente tem o analista para as operar — viola a 10/90 rule de Kaushik
- Apresentar CLV sem segmentar: um CLV médio único esconde os Champions e deixa a estratégia cega
- Fazer ICE scoring com todos os experimentos no mesmo intervalo (6.5–7.2) — não prioriza nada, é lista de desejos com números
- Concluir "tens PMF" ou "não tens PMF" sem mostrar a percentagem "muito desapontado" e o n amostral do survey
- Colocar "Care" no See-Think-Do-Care como afterthought ou vazio — é onde está 70%+ do CLV incremental
- Usar "churn está alto" sem definir a taxa, o tipo (voluntário vs. involuntário), e o segmento afetado
- Propor North Star Metric sem validar correlação com receita — um NSM desalinhado otimiza a métrica errada
- Entregar coortes de retenção sem explicar o eixo X (semanas? meses?) nem o denominador (instalações? primeiros pagamentos?)
- Misturar métricas See e Do no mesmo "dashboard principal" — cria ruído para o CEO e paralisa decisões de produto
