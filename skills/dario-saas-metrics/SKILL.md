---
name: dario-saas-metrics
description: SaaS metrics dashboard — MRR, ARR, NRR, churn, CAC, LTV, CAC payback, Rule of 40. Uses CFO Squad (Skok, Tunguz, Janz). Triggers on "saas metrics", "mrr", "arr", "churn rate", "ltv cac", "nrr", "unit economics".
license: MIT
---

# DARIO Skill — SaaS Metrics

## Workflow
1. RAG: `search_kb("saas metrics mrr nrr cac ltv skok tunguz", collection: "dario")`
2. Gather: pricing tiers, customer counts, churn data, acquisition costs
3. Calculate all SaaS metrics with benchmarks
4. Flag red/yellow/green per metric
5. Recommendations for improvement

## Metrics calculated
- MRR/ARR (total, new, expansion, contraction, churn)
- Net Revenue Retention (NRR) — target >110%
- Gross churn vs Net churn
- CAC (by channel if possible)
- LTV = ARPU × (1/churn rate)
- LTV:CAC ratio — target ≥3:1
- CAC payback months — target <12
- Rule of 40 = Growth% + Margin% — target ≥40
- Magic Number = Net new ARR / S&M spend

## Metrics Dashboard Template

| Metric | Formula | Current | Benchmark | Status |
|---|---|---|---|---|
| **MRR** | Sum of all recurring revenue | ___ EUR | >10K seed, >50K growth | 🟢🟡🔴 |
| **ARR** | MRR x 12 | ___ EUR | >120K seed, >600K growth | 🟢🟡🔴 |
| **MRR Growth Rate** | (MRR_current - MRR_prev) / MRR_prev | ___% | >15% m/m seed, >10% growth | 🟢🟡🔴 |
| **Net New MRR** | New + Expansion - Contraction - Churn | ___ EUR | Positive and growing | 🟢🟡🔴 |
| **NRR (Net Revenue Retention)** | (MRR_start + expansion - contraction - churn) / MRR_start | ___% | >100% min, >110% good, >130% elite | 🟢🟡🔴 |
| **Gross Revenue Retention** | (MRR_start - contraction - churn) / MRR_start | ___% | >85% acceptable, >90% good, >95% elite | 🟢🟡🔴 |
| **Logo Churn (monthly)** | Lost customers / Start customers | ___% | <5% seed, <3% growth, <1% mature | 🟢🟡🔴 |
| **Revenue Churn (monthly)** | Lost MRR / Start MRR | ___% | <3% seed, <2% growth, <0.5% mature | 🟢🟡🔴 |
| **CAC** | (Sales + Marketing spend) / New customers | ___ EUR | Varies by ACV — see benchmarks | 🟢🟡🔴 |
| **LTV** | ARPU x (1 / monthly churn rate) | ___ EUR | >3x CAC minimum | 🟢🟡🔴 |
| **LTV:CAC Ratio** | LTV / CAC | ___:1 | 3:1 min, 5:1 ideal, >8:1 under-investing | 🟢🟡🔴 |
| **CAC Payback** | CAC / (ARPU x Gross Margin %) | ___ meses | <18 seed, <12 growth, <6 mature | 🟢🟡🔴 |
| **ARPU** | MRR / Total customers | ___ EUR | Growing or stable | 🟢🟡🔴 |
| **Rule of 40** | YoY Revenue Growth % + EBITDA Margin % | ___% | >40% good, >60% elite | 🟢🟡🔴 |
| **Magic Number** | Net New ARR / Prior quarter S&M spend | ___ | >0.75 efficient, >1.0 excellent | 🟢🟡🔴 |
| **Burn Multiple** | Net Burn / Net New ARR | ___ | <1x excellent, 1-2x good, >2x alarming | 🟢🟡🔴 |
| **Quick Ratio** | (New MRR + Expansion) / (Contraction + Churn) | ___ | >4 excellent, 2-4 healthy, <1 shrinking | 🟢🟡🔴 |

### Status Criteria
- 🟢 **Green:** At or above benchmark for the company's stage
- 🟡 **Yellow:** Within 20% below benchmark — needs attention
- 🔴 **Red:** More than 20% below benchmark — requires immediate action

## Benchmark Ranges

| Metric | Seed (pre-PMF) | Growth (1-10M ARR) | Mature (>10M ARR) |
|---|---|---|---|
| MRR Growth (m/m) | 15-25% | 8-15% | 3-8% |
| Logo Churn (monthly) | 3-7% | 2-4% | 0.5-2% |
| Revenue Churn (monthly) | 2-5% | 1-3% | 0.3-1% |
| NRR (annual) | 90-110% | 105-125% | 110-140% |
| GRR (annual) | 70-85% | 80-92% | 90-98% |
| LTV:CAC | 2-4:1 | 3-6:1 | 5-10:1 |
| CAC Payback | 12-24 meses | 6-18 meses | 3-12 meses |
| ARPU trend | Volatile | Growing 5-10%/q | Stable +2-5%/q |
| Rule of 40 | N/A (growth focus) | 30-50 | 40-70 |
| Magic Number | 0.3-0.7 | 0.5-1.0 | 0.7-1.5 |
| Burn Multiple | 2-5x | 1-3x | <1.5x |
| Quick Ratio | 2-4 | 3-5 | 4-8 |
| Gross Margin | 60-75% | 70-85% | 80-90% |

> **Fonte:** Compilado de Skok (Matrix Partners), Tunguz (Tomasz Tunguz), Janz (Christoph Janz), Bessemer Cloud Index, OpenView Partners.

## MRR Waterfall

O MRR Waterfall decompoe a variacao mensal de MRR nas suas componentes:

```
MRR Waterfall (Mes X → Mes Y)
============================================
MRR Inicial (Mes X)                    €___

(+) New MRR          — novos clientes   €___
(+) Expansion MRR    — upgrades/upsell  €___
(-) Contraction MRR  — downgrades       €___
(-) Churned MRR      — cancelamentos    €___
(+) Reactivation MRR — clientes voltam  €___

= Net New MRR                           €___

MRR Final (Mes Y)                      €___
============================================
```

### Exemplo Trabalhado (LUSOconta SaaS)

| Componente | Jan | Fev | Mar | Abr |
|---|---|---|---|---|
| MRR Inicial | 4.200 | 5.050 | 5.830 | 6.910 |
| + New MRR | 600 | 500 | 750 | 400 |
| + Expansion | 350 | 400 | 500 | 300 |
| - Contraction | -50 | -70 | -60 | -80 |
| - Churn | -50 | -50 | -110 | -30 |
| + Reactivation | 0 | 0 | 0 | 50 |
| **Net New MRR** | **850** | **780** | **1.080** | **640** |
| **MRR Final** | **5.050** | **5.830** | **6.910** | **7.550** |

### Rácios derivados do Waterfall
- **Expansion Rate** = Expansion MRR / MRR Inicial = indica capacidade de upsell
- **Contraction Rate** = Contraction MRR / MRR Inicial = pressão descendente de preço
- **Net Churn Rate** = (Churn + Contraction - Expansion) / MRR Inicial
- **Net Negative Churn** = quando Expansion > Churn + Contraction (o santo graal do SaaS)

## Cohort Analysis Template

Tabela de retenção por cohort mensal (% de clientes que permanecem activos):

| Cohort | M0 | M1 | M2 | M3 | M4 | M5 | M6 | M9 | M12 |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2025 (n=30) | 100% | 87% | 80% | 77% | 73% | 70% | 67% | 60% | 55% |
| Fev 2025 (n=25) | 100% | 88% | 84% | 80% | 76% | 72% | 68% | 62% | — |
| Mar 2025 (n=40) | 100% | 90% | 85% | 82% | 78% | 75% | 71% | — | — |
| Abr 2025 (n=35) | 100% | 91% | 86% | 83% | 79% | 76% | — | — | — |
| Mai 2025 (n=28) | 100% | 89% | 82% | 78% | 74% | — | — | — | — |
| Jun 2025 (n=32) | 100% | 91% | 87% | 84% | — | — | — | — | — |

### Como ler a tabela
- **Diagonal para baixo-direita:** cada cohort novo deve reter MELHOR que o anterior (sinal de product-market fit)
- **M1 drop:** se >15%, o onboarding precisa de trabalho urgente
- **M3 stabilization:** a curva deve achatar por volta de M3-M6 ("smile curve")
- **M12 retention:** alvo minimo 50% para seed, 65% growth, 80% mature

### Revenue Cohort (alternativa)
Em vez de % clientes, medir % da receita retida por cohort — mais relevante se ARPU varia entre clientes. NRR por cohort revela se os que ficam compensam os que saem.

## Unit Economics Deep Dive

### Variante 1 — LTV Simples
```
LTV = ARPU / Monthly Churn Rate
```
Exemplo: ARPU = 89 EUR, Churn = 3% mensal
LTV = 89 / 0,03 = **2.967 EUR**

### Variante 2 — LTV Ajustado por Margem (recomendado)
```
LTV = (ARPU x Gross Margin %) / Monthly Churn Rate
```
Exemplo: ARPU = 89 EUR, GM = 80%, Churn = 3%
LTV = (89 x 0,80) / 0,03 = **2.373 EUR**

### Variante 3 — LTV com Desconto DCF (mais preciso para investidores)
```
LTV = ARPU x Gross Margin % x [1 / (Churn Rate + Discount Rate)]
```
Exemplo: ARPU = 89 EUR, GM = 80%, Churn = 3%, Discount = 1% (12%/ano)
LTV = 89 x 0,80 x [1 / (0,03 + 0,01)] = 89 x 0,80 x 25 = **1.780 EUR**

### Variante 4 — LTV Segmentado
Calcular LTV separadamente por segmento e ponderar pelo mix:

| Segmento | % Clientes | ARPU | Churn | GM | LTV | LTV Ponderado |
|---|---|---|---|---|---|---|
| Starter (29 EUR) | 50% | 29 | 5% | 75% | 435 | 218 |
| Professional (89 EUR) | 35% | 89 | 2,5% | 82% | 2.920 | 1.022 |
| Enterprise (249 EUR) | 15% | 249 | 1% | 88% | 21.912 | 3.287 |
| **Blended** | **100%** | **79** | **3,2%** | **80%** | — | **4.526** |

> O LTV blended (ponderado) e sempre mais preciso que calcular LTV sobre medias. Segmentos com churn baixo dominam o LTV real.

### Unit Economics Health Check
| Racio | Calculo | Alvo | Accao se fora |
|---|---|---|---|
| LTV:CAC | LTV / CAC | 3:1 a 5:1 | <3:1 reduzir CAC ou aumentar retenção |
| CAC Payback | CAC / (ARPU x GM%) | <12 meses | >12m: problema de eficiencia de aquisição |
| Margem Contribuição | ARPU - COGS per user - S&M per user | >0 EUR | Negativa = queimar dinheiro por cliente |

## Recommendations Engine

Quando uma metrica esta 🔴, recomendar acoes especificas:

| Metrica em 🔴 | Diagnóstico Provável | Recomendações |
|---|---|---|
| **Logo Churn > 5%** | Produto não resolve problema core; onboarding fraco; support deficiente | 1. Entrevistar 10 churned users esta semana 2. Implementar NPS in-app 3. Rever onboarding flow (time-to-value) 4. Criar health score por cliente |
| **Revenue Churn > 3%** | Preço desalinhado com valor; funcionalidades premium não justificam upgrade | 1. Analisar feature usage por tier 2. Ajustar packaging/bundling 3. Criar expansion triggers automaticos 4. Rever pricing vs concorrencia |
| **NRR < 100%** | Sem upsell/cross-sell; contraction supera expansion | 1. Implementar usage-based upsell triggers 2. Criar tier intermedio se gap grande 3. Lançar add-ons/modulos 4. Account management proactivo |
| **LTV:CAC < 3:1** | CAC demasiado alto OU retenção/ARPU demasiado baixos | 1. Focar em canais organicos (SEO, content, referral) 2. Optimizar conversion rate do funil 3. Aumentar ARPU (preços ou packaging) 4. Melhorar retenção M1-M3 |
| **CAC Payback > 18 meses** | Ciclo de venda longo; trial-to-paid baixo; canais pagos ineficientes | 1. Encurtar trial (14 para 7 dias) ou freemium 2. Rever attribution por canal 3. Automatizar nurturing 4. Self-serve checkout |
| **MRR Growth < 5% m/m** | Saturação do canal; product-market fit fraco; capacidade vendas limitada | 1. Testar novo canal de aquisição 2. Lançar referral program 3. Expandir para segmento adjacente 4. Partnerships/integrações |
| **Rule of 40 < 30** | Crescimento lento sem rentabilidade | 1. Se growth-stage: investir mais em aquisição 2. Se mature: cortar custos para margem 3. Rever unit economics por segmento 4. Considerar pivot se consistentemente abaixo |
| **Quick Ratio < 2** | MRR a encolher; churn domina nova receita | 1. PARAR de investir em aquisição até resolver churn 2. Implementar churn prediction (usage drops) 3. Win-back campaign 4. Product intervention nos first 30 days |
| **Burn Multiple > 3x** | Gastar muito mais do que cresce; ineficiencia capital | 1. Reduzir headcount nao essencial 2. Focar em top 2 canais de aquisição 3. Automatizar onde possivel 4. Rever se modelo de negocio e viavel |
| **Gross Margin < 70%** | Infraestrutura cara; support intensivo; COGS não escala | 1. Migrar para infra mais eficiente 2. Self-service support (docs, chatbot) 3. Automatizar provisioning 4. Renegociar contratos fornecedores |

## Save Location

```
Obsidian: C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs\YYYY-MM-DD - SaaS Metrics - [Produto/SaaS].md
```

Guardar automaticamente quando o dashboard for gerado. Incluir frontmatter:
```yaml
---
type: saas-metrics
product: "[nome do SaaS]"
date: YYYY-MM-DD
mrr: "[valor]"
nrr: "[valor]%"
ltv_cac: "[ratio]"
rule_of_40: "[valor]"
stage: seed | growth | mature
status: healthy | attention | critical
---
```

## Red Flags

Alertar SEMPRE que qualquer destas situacoes for detectada:

| Red Flag | Limiar | Accao |
|---|---|---|
| Logo churn > 7% mensal | Mais de 7 em 100 clientes saem por mes | CRITICO — produto ou onboarding com problema fundamental |
| NRR < 90% anual | Receita de clientes existentes a encolher 10%+ | CRITICO — sem expansion, o negocio morre em 2-3 anos |
| LTV:CAC < 1:1 | Cada cliente custa mais do que gera | PARAR aquisicao imediatamente — rever modelo |
| CAC Payback > 24 meses | 2 anos para recuperar custo de aquisicao | Insustentavel — rever pricing ou canais |
| Quick Ratio < 1 | MRR a encolher activamente | EMERGENCIA — churn supera nova receita |
| Burn Multiple > 5x | Queimar 5 EUR por cada 1 EUR de ARR novo | Runway em risco — cortar custos drasticamente |
| MRR flat 3+ meses | Sem crescimento por trimestre | Produto pode ter atingido tecto; rever estrategia |
| Gross Margin < 60% | COGS a comer margens | Modelo nao escala — rever infraestrutura e support |
| ARPU em queda 3+ meses | Clientes a fazer downgrade consistentemente | Pricing ou packaging desalinhado com valor percebido |
| Top 3 clientes > 30% MRR | Concentracao perigosa | Risco de revenue cliff — diversificar base urgente |
