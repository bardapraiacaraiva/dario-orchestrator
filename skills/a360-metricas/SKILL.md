---
name: "A360 Business Metrics Dashboard"
description: "Comprehensive business metrics tracking — CAC, LTV, MRR, churn, conversion rates, runway, burn rate, break-even timeline, unit economics health check. The financial pulse of the business."
version: "1.0"
agent: "A360 — Accelera 360"
category: "Phase 5 — Scale"
license: SEE-LICENSE
parent_agent: a360-director
compliance: [audit_immutable]
---

# A360 Business Metrics Dashboard

## Triggers

Activate this skill when the user says any of:
- "metrics", "metricas", "KPIs", "dashboard"
- "CAC", "LTV", "MRR", "churn", "burn rate"
- "how is my business doing?", "como esta o negocio?"
- "unit economics", "economia unitaria"
- "runway", "break-even", "ponto de equilibrio"
- "conversion rates", "taxas de conversao"
- "business health check", "saude do negocio"
- Any request to track, analyze, or report on business performance

## Frameworks & References

- **David Skok** (forEntrepreneurs) — SaaS metrics, CAC payback, LTV:CAC, Rule of 40
- **Alex Hormozi** ($100M Offers) — revenue per employee, enterprise value drivers
- **Eric Ries** (Lean Startup) — innovation accounting, actionable vs vanity metrics
- **Sean Ellis** (Hacking Growth) — North Star Metric, AARRR framework
- **Jason Lemkin** (SaaStr) — SaaS benchmarks, T2D3 growth, magic number
- **Tomasz Tunguz** — SaaS benchmarks, cohort analysis, unit economics

## Workflow

### Step 1: Business Type Classification

Metrics vary by model. Identify which applies:

| Model | Primary Metrics | Revenue Pattern |
|-------|----------------|-----------------|
| **SaaS / Subscription** | MRR, ARR, churn, NRR, CAC payback | Recurring |
| **E-commerce** | AOV, purchase frequency, COGS, inventory turns | Transactional |
| **Service / Agency** | Utilization rate, client LTV, project margin | Project-based |
| **Marketplace** | GMV, take rate, liquidity, supply/demand ratio | Commission |
| **Info Products / Courses** | Launch revenue, refund rate, completion rate | Launch/evergreen |
| **Hybrid** | Combine relevant metrics from above | Mixed |

### Step 2: Core Financial Metrics

| Metric | Formula | Your Number | Health |
|--------|---------|-------------|--------|
| **Monthly Revenue** | Total revenue this month | $X | |
| **MRR** (if recurring) | Sum of all monthly subscriptions | $X | |
| **ARR** | MRR x 12 | $X | |
| **Revenue Growth** (MoM) | (This month - Last month) / Last month | X% | >10% MoM early stage |
| **Gross Revenue** | Total before refunds/discounts | $X | |
| **Net Revenue** | After refunds, chargebacks, discounts | $X | |
| **Gross Margin** | (Revenue - COGS) / Revenue | X% | >60% SaaS, >40% services |
| **Net Profit Margin** | Net profit / Revenue | X% | >15% healthy |

### Step 3: Customer Acquisition Metrics

| Metric | Formula | Your Number | Benchmark |
|--------|---------|-------------|-----------|
| **CAC** | Total marketing + sales spend / New customers | $X | <1/3 of LTV |
| **Blended CAC** | All costs / All new customers (paid + organic) | $X | |
| **Paid CAC** | Paid marketing spend / Paid-acquired customers | $X | |
| **Organic CAC** | Organic marketing cost / Organic-acquired customers | $X | |
| **CAC Payback** | CAC / Monthly gross profit per customer | X months | <12 months |
| **Leads Generated** | Total new leads this month | X | |
| **Lead-to-Customer Rate** | New customers / New leads | X% | >2% |
| **Cost Per Lead (CPL)** | Marketing spend / Leads generated | $X | |
| **Traffic Sources** | Channel breakdown | | |

**CAC by Channel:**

| Channel | Spend | Customers | CAC | LTV:CAC |
|---------|-------|-----------|-----|---------|
| Facebook Ads | $X | X | $X | X:1 |
| Google Ads | $X | X | $X | X:1 |
| Organic/SEO | $X | X | $X | X:1 |
| Referral | $X | X | $X | X:1 |
| Email | $X | X | $X | X:1 |
| **Total** | **$X** | **X** | **$X** | **X:1** |

### Step 4: Customer Lifetime Value

| Metric | Formula | Your Number | Benchmark |
|--------|---------|-------------|-----------|
| **LTV (simple)** | ARPU x Avg. customer lifespan (months) | $X | >3x CAC |
| **LTV (with margin)** | ARPU x Gross margin % x Lifespan | $X | |
| **ARPU** | Monthly revenue / Active customers | $X | |
| **Avg. Lifespan** | 1 / Monthly churn rate | X months | |
| **LTV:CAC Ratio** | LTV / CAC | X:1 | >3:1 (ideal 5:1) |
| **Purchase Frequency** | Purchases / Customers (per year) | X | |
| **Avg. Order Value (AOV)** | Revenue / Number of orders | $X | |

**LTV Health Assessment:**
- LTV:CAC > 5:1 = Excellent (consider investing more in growth)
- LTV:CAC 3-5:1 = Healthy
- LTV:CAC 1-3:1 = Warning (optimize retention or reduce CAC)
- LTV:CAC < 1:1 = Critical (losing money on every customer)

### Step 5: Retention & Churn Metrics

| Metric | Formula | Your Number | Benchmark |
|--------|---------|-------------|-----------|
| **Monthly Churn Rate** | Lost customers / Start-of-month customers | X% | <5% |
| **Annual Churn** | 1 - (1 - monthly churn)^12 | X% | <30% |
| **Net Revenue Retention (NRR)** | (Start MRR + expansion - contraction - churn) / Start MRR | X% | >100% |
| **Gross Revenue Retention (GRR)** | (Start MRR - contraction - churn) / Start MRR | X% | >85% |
| **Logo Retention** | 1 - (Lost customers / Start customers) | X% | >90% |
| **Reactivation Rate** | Returned customers / Total churned | X% | |
| **Time to Churn** | Avg. months before customer leaves | X months | |

**Cohort Analysis:**
Track retention by signup month to spot trends.

| Cohort | Month 1 | Month 2 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|---------|----------|
| Jan | 100% | X% | X% | X% | X% |
| Feb | 100% | X% | X% | X% | |
| Mar | 100% | X% | X% | | |

### Step 6: Funnel Conversion Metrics

| Stage | Visitors/Leads | Converted | Rate | Benchmark |
|-------|---------------|-----------|------|-----------|
| **Website → Lead** | X | X | X% | 2-5% |
| **Lead → MQL** | X | X | X% | 15-30% |
| **MQL → SQL** | X | X | X% | 30-50% |
| **SQL → Customer** | X | X | X% | 20-30% |
| **Customer → Repeat** | X | X | X% | 30%+ |
| **Customer → Referral** | X | X | X% | 15%+ |

### Step 7: Cash & Runway Metrics

| Metric | Formula | Your Number | Health |
|--------|---------|-------------|--------|
| **Cash on Hand** | Bank balance | $X | |
| **Monthly Burn Rate** | Total monthly expenses | $X | |
| **Revenue** | Monthly income | $X | |
| **Net Burn** | Burn rate - Revenue | $X | (negative = profitable) |
| **Runway** | Cash / Net burn | X months | >6 months |
| **Break-even Revenue** | Fixed costs / Gross margin % | $X/mo | |
| **Months to Break-even** | (Break-even - Current revenue) / Monthly growth | X months | |
| **Cash Conversion Score** | Free cash flow / Net income | X% | >80% |

**Runway Traffic Light:**
- GREEN: >12 months runway or profitable
- YELLOW: 6-12 months runway
- ORANGE: 3-6 months runway (start fundraising or cutting)
- RED: <3 months runway (emergency mode)

### Step 8: Growth Health Indicators

| Indicator | Formula | Your Number | Benchmark |
|-----------|---------|-------------|-----------|
| **Rule of 40** (SaaS) | Revenue growth % + Profit margin % | X | >40 = excellent |
| **Magic Number** (SaaS) | Net new ARR / Prior quarter S&M spend | X | >0.75 = efficient |
| **Quick Ratio** (SaaS) | (New MRR + Expansion) / (Contraction + Churn) | X | >4 = healthy |
| **Burn Multiple** | Net burn / Net new ARR | X | <2 = efficient |
| **Revenue per Employee** | Annual revenue / Full-time headcount | $X | >$100K |
| **Payback Period** | CAC / Monthly gross profit per customer | X months | <12 |

### Step 9: Unit Economics Summary Card

```
┌─────────────────────────────────────────────┐
│            UNIT ECONOMICS CARD              │
├─────────────────────────────────────────────┤
│  CAC:  $____    LTV:  $____    Ratio: __:1 │
│  ARPU: $____    Churn: ____%   NRR:  ____% │
│  Margin: ____%  Payback: ___ months         │
│  Burn:  $____   Runway: ___ months          │
│  Break-even: $____/mo   ETA: ___ months     │
├─────────────────────────────────────────────┤
│  Overall Health: [HEALTHY / WARNING / CRITICAL] │
└─────────────────────────────────────────────┘
```

### Step 10: Monthly Review Cadence

**Weekly check (5 min):**
- Revenue this week vs target
- New leads and customers
- Any churn events

**Monthly deep dive (1 hour):**
- Full dashboard update (all metrics)
- Cohort analysis update
- Funnel conversion review
- CAC by channel comparison
- Cash position and runway
- Growth experiment results

**Quarterly strategic review:**
- LTV:CAC trend
- Revenue growth trajectory
- Unit economics vs plan
- Competitive positioning
- Adjust targets for next quarter

## Output Template

```markdown
# A360 Metrics Dashboard
## Business: [NAME]
## Period: [MONTH YYYY]

### Revenue Summary
| Metric | This Month | Last Month | Change |
|--------|-----------|------------|--------|
| Revenue | $X | $X | +X% |
| Customers | X | X | +X |
| ARPU | $X | $X | +X% |

### Unit Economics
| Metric | Value | Status |
|--------|-------|--------|
| CAC | $X | [status] |
| LTV | $X | [status] |
| LTV:CAC | X:1 | [status] |
| Churn | X% | [status] |
| Gross Margin | X% | [status] |

### Cash Position
- Cash: $X | Burn: $X/mo | Runway: X months
- Break-even: $X/mo | ETA: X months

### Funnel Performance
[Stage-by-stage conversion rates]

### Health Score: [HEALTHY/WARNING/CRITICAL]

### Top 3 Actions This Month
1. [Action 1 — addresses biggest metric gap]
2. [Action 2]
3. [Action 3]
```

## Red Flags

Stop and warn the user if:
- LTV:CAC below 1:1 (losing money on every customer acquired)
- Monthly churn above 10% (business is a leaky bucket)
- Runway below 3 months with no funding plan
- CAC increasing month-over-month with no strategy change
- Revenue growth negative for 3+ consecutive months
- Gross margin below 30% (structural problem)
- Net Revenue Retention below 80% (not enough value delivered)
- Zero tracking in place (flying blind)
- Focusing on vanity metrics (followers, page views) instead of revenue metrics

## Handoff

After metrics review:
- Route to `a360-growth` if acquisition metrics need improvement
- Route to `a360-modelo` if unit economics need restructuring
- Route to `a360-scale` when metrics show readiness for next milestone
- Route to `a360-pitch` with metrics for investor conversations
- Feed to `dario-saas-metrics` for SaaS-specific deep dive
- Save output to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - A360 - Metrics - [BusinessName].md`

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Business model classification está explícito e coerente

- [ ] O modelo foi identificado (SaaS / E-commerce / Service / Marketplace / Info Product / Hybrid)
- [ ] As métricas selecionadas são as corretas para esse modelo (não apresentar MRR para e-commerce puro)
- [ ] A tabela Step 1 tem a linha correta realçada ou indicada
- [ ] Não há métricas irrelevantes ocupando espaço (ex: GMV para SaaS)

❌ NOT delivery-ready: "O negócio é de tipo X, vamos ver as métricas."
✅ Delivery-ready: "Cuidai opera modelo **Subscription (SaaS-like)** — foco em MRR, NRR, churn mensal e CAC payback. Métricas de AOV e GMV não aplicáveis."

---

### Gate 2 — Todas as métricas core têm número real ou flag explícito de "dado em falta"

- [ ] Nenhuma célula da tabela contém "$X" ou "X%" sem substituição ou nota
- [ ] Onde dados não foram fornecidos, aparece "⚠️ Dado não fornecido — necessário para calcular"
- [ ] MRR, CAC, LTV e Gross Margin estão sempre preenchidos ou flagged
- [ ] Unidade monetária está consistente (€ ou R$ — nunca misturar)

❌ NOT delivery-ready: "CAC: $X | LTV: $X | LTV:CAC: X:1"
✅ Delivery-ready: "CAC: €43 | LTV: €312 | LTV:CAC: **7,3:1** ✅ Excellent"

---

### Gate 3 — Health assessment tem veredito claro com benchmark comparado

- [ ] Cada métrica crítica tem símbolo de saúde: ✅ Healthy / ⚠️ Warning / ❌ Critical
- [ ] O benchmark de referência está citado (ex: "<5% churn mensal — SaaStr)
- [ ] LTV:CAC tem o tier explícito (Excellent / Healthy / Warning / Critical)
- [ ] CAC Payback tem interpretação em linguagem de negócio, não só o número

❌ NOT delivery-ready: "Churn: 8% — acima do ideal."
✅ Delivery-ready: "Churn mensal: **8%** ❌ Critical (benchmark SaaStr: <5%). Ao ritmo atual, perdes ~65% da base em 12 meses — prioridade #1."

---

### Gate 4 — CAC por canal está desagregado com ROI relativo

- [ ] Tabela de CAC por canal tem pelo menos 2 canais com dados reais
- [ ] Coluna LTV:CAC por canal está calculada (não genérica)
- [ ] Canal mais eficiente está identificado e recomendação de alocação de budget feita
- [ ] Canais com LTV:CAC < 1:1 têm recomendação explícita (pausar / otimizar)

❌ NOT delivery-ready: "Facebook Ads: $X spend, X customers, CAC $X"
✅ Delivery-ready: "Facebook Ads: €1.200 spend, 14 clientes, CAC €86, LTV:CAC 3,6:1 ⚠️ | Referral: €0 spend, 9 clientes, CAC €0, LTV:CAC ∞ ✅ → escalar programa de referral"

---

### Gate 5 — Runway e burn rate têm timeline concreta e trigger de ação

- [ ] Runway calculado em meses com data de esgotamento projetada
- [ ] Burn rate mensal (gross e net) está especificado
- [ ] Break-even calculado com data estimada baseada em crescimento atual
- [ ] "Default alive vs default dead" (Paul Graham) está avaliado explicitamente

❌ NOT delivery-ready: "Runway: X meses. Precisas de mais receita."
✅ Delivery-ready: "Burn rate net: €4.200/mês | Caixa: €38.000 | Runway: **9,0 meses** → esgotamento ~Fevereiro 2026. Break-even projetado: mês 11 (se crescimento MoM ≥8%). **Default dead** — janela crítica."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders com angle-brackets

- [ ] Nome do cliente aparece no título ou header do dashboard
- [ ] Zero ocorrências de `<client>`, `[nome]`, `$X`, `X%` no output final
- [ ] Período de análise está explícito (ex: "Junho 2025" ou "Q2 2025")
- [ ] Fonte dos dados está indicada (ex: "dados fornecidos pelo cliente via chat, 18 Jun 2025")

❌ NOT delivery-ready: "Dashboard para `<client_name>` — período `<month>`"
✅ Delivery-ready: "**ARRECADA.GOV — Business Metrics Dashboard | Junho 2025** (dados fornecidos pelo cliente, 18 Jun 2025)"

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no dashboard deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / dados reais do cliente (ex: extracto bancário, CRM, ad account)
- 🟡 **assumed** — plausível com base no contexto, mas precisa de confirmação do cliente antes de entrega
- 🟢 **projection** — forecast por design (não verificável hoje — benchmark ou modelo calculado)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verify. **Honest transparency > dashboard inflado.**

---

❌ NOT delivery-ready:
> "CAC: $42 | LTV: $310 | LTV:CAC: 7.4:1 | Runway: 8 meses"
> *(reader assume que todos os números são factuais — nenhum label, nenhuma fonte, CAC pode incluir ou não salários)*

✅ Delivery-ready:
> - 🔵 **verified** — MRR: R$28.400 (exportado do Stripe, Março 2025)
> - 🔵 **verified** — Churn mensal: 3,2% (calculado de 94 clientes início → 91 fim do mês)
> - 🟡 **assumed** — CAC blended: ~R$190 (baseado em spend declarado de R$4.800; excluí salário do SDR — confirmar se deve entrar)
> - 🟡 **assumed** — Gross margin: ~68% (cliente mencionou "produto digital, custo baixo" — sem P&L formal partilhado)
> - 🟢 **projection** — Runway: 11 meses (burn rate médio dos últimos 3 meses × saldo declarado; assume burn estável)
> - 🟢 **projection** — Break-even timeline: Mês 7 (modelo linear sobre crescimento MoM actual de 9%)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — CAC recalculado com custos de headcount incluídos; gross margin validada contra COGS real
- [ ] All 🔵 citations added — fonte de cada número (Stripe export, CRM report, ad account screenshot, data range)
- [ ] All 🟢 projections labeled como tal ao cliente — expectativas claras: "este runway assume burn constante; qualquer contratação altera o número"

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SAQUEI — Business Metrics Dashboard | Junho 2025
*Dados fornecidos pelo cliente via A360, 18 Jun 2025 | Modelo: SaaS / Subscription*

---

## 📊 Core Financial Metrics

| Métrica | Valor | Saúde | Benchmark |
|---------|-------|-------|-----------|
| MRR | €18.400 | ✅ | — |
| ARR | €220.800 | ✅ | — |
| Crescimento MoM | +11,3% | ✅ | >10% early-stage |
| Gross Margin | 71% | ✅ | >60% SaaS (Skok) |
| Net Profit Margin | 18% | ✅ | >15% |

---

## 🎯 Customer Acquisition

| Métrica | Valor | Saúde |
|---------|-------|-------|
| CAC blended | €52 | ✅ |
| CAC payback | 4,1 meses | ✅ (<12 meses) |
| Lead-to-Customer | 3,8% | ✅ (>2%) |
| CPL (Facebook) | €4,20 | ✅ |

**CAC por canal — Junho 2025:**

| Canal | Spend | Clientes | CAC | LTV:CAC |
|-------|-------|----------|-----|---------|
| Facebook Ads | €1.800 | 22 | €82 | 5,1:1 ✅ |
| Google Ads | €900 | 8 | €113 | 3,7:1 ⚠️ |
| Referral | €0 | 14 | €0 | ∞ ✅ |
| Email nurture | €120 | 6 | €20 | 20,9:1 ✅ |
| **Total** | **€2.820** | **50** | **€56** | **7,4:1 ✅** |

→ **Recomendação:** Escalar Referral (custo zero, 14 aquisições). Google Ads abaixo de threshold — testar otimização de keywords por 30 dias ou realocar budget para Facebook.

---

## 💰 LTV & Unit Economics

| Métrica | Valor | Saúde |
|---------|-------|-------|
| ARPU | €214/mês | — |
| Avg. lifespan | 19,4 meses | — |
| LTV (com margin) | €2.975 | — |
| LTV:CAC | **57,2:1** | ✅ Excellent |

→ LTV:CAC > 5:1: considerar aumentar agressividade de aquisição — cada €1 em marketing retorna €57 de valor.

---

## 🔄 Retenção & Churn

| Métrica | Valor | Saúde | Benchmark |
|---------|-------|-------|-----------|
| Churn mensal | 3,1% | ✅ | <5% (SaaStr) |
| Churn anual | 32% | ⚠️ | <30% |
| NRR | 108% | ✅ | >100% |
| GRR | 96,9% | ✅ | >85% |
| Logo Retention | 96,9% | ✅ | >90% |

→ **Atenção:** Churn anual em 32% — 2pp acima do benchmark. Cohort de Janeiro mostra queda acentuada no mês 10. Investigar motivo de saída nesse período (pricing? onboarding? concorrência?).

---

## 💸 Runway & Burn Rate

| Métrica | Valor |
|---------|-------|
| Burn rate gross | €14.200/mês |
| Burn rate net | €2.800/mês |
| Caixa disponível | €61.500 |
| Runway | **21,9 meses** ✅ |
| Break-even projetado | Já atingido (Março 2025) ✅ |

→ **Default Alive** ✅ — ao crescimento atual (11,3% MoM), SAQUEI não precisa de capital externo para sobreviver. Runway de quase 2 anos dá flexibilidade para escalar sem pressão de fundraising.

---

## 🔺 Funil de Conversão (Junho 2025)

| Etapa | Volume | Taxa | Saúde |
|-------|--------|------|-------|
| Website → Lead | 4.200 → 182 | 4,3% | ✅ |
| Lead → MQL | 182 → 71 | 39% | ✅ |
| MQL → SQL | 71 → 58 | 82% | ✅ |
| SQL → Cliente | 58 → 50 | 86% | ✅ |

---

## 🏆 North Star Summary

**Métrica North Star: MRR** — €18.400 (+11,3% MoM)

Top 3 prioridades para Julho 2025:
1. **Reduzir churn anual de 32% → <30%** — investigar cohort mês 10
2. **Escalar programa de referral** — 14 clientes a custo zero em Junho
3. **Monitorizar Google Ads** — 30 dias para otimizar ou pausar (CAC €113 borderline)
```

---

## Output anti-patterns

- **Placeholders não substituídos** — entregar dashboard com "$X", "X%", ou `<client>` ainda no output
- **Modelo errado de métricas** — apresentar MRR e churn a um negócio de e-commerce transacional puro
- **Health sem veredito** — listar métricas sem símbolo ✅/⚠️/❌ e sem comparação com benchmark
- **CAC agregado sem desagregação por canal** — esconder ineficiências de canais caros num blended number
- **Runway sem data concreta** — dizer "9 meses de runway" sem indicar mês de esgotamento projetado
- **LTV:CAC calculado mas sem implicação de decisão** — o número existe mas não gera recomendação de ação
- **Churn em % sem tradução para impacto real** — "8% churn" sem dizer "perdes 65% da base em 12 meses"
- **North Star ausente** — dashboard extenso mas sem priorização clara do que mover primeiro
- **Período de análise omitido** — dashboard sem indicar a que mês/trimestre os dados se referem
- **Mistura de moedas** — alternar € e R$ no mesmo output sem aviso explícito de contexto
