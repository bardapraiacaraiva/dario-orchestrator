---
name: conta-orcamento
description: Budgeting — annual budget, variance analysis, rolling forecasts, departmental budgets, KPIs
version: "1.0"
---

# CONTA-ORCAMENTO: Orçamento e Controlo Orçamental

## Activation Triggers

**PT:** orçamento, budget, previsão, forecast, desvio orçamental, variância, planeamento financeiro, rolling forecast, centro de custo, objetivo orçamental
**EN:** budget, budgeting, forecast, variance analysis, financial planning, rolling forecast, cost center budget, budget control, KPI

## Context

Budgeting is the financial planning and control process linking strategy to operations. While not legally mandated for private entities in Portugal, it is essential for management control. Portuguese entities often align budgets with the fiscal year (Jan-Dec), SNC account structure, and tax calendar for IVA/IRC/SS obligations.

## Workflow

### Step 1 — Budget Framework

| Budget Type | Scope | Period |
|-------------|-------|--------|
| Orçamento anual (master) | Full P&L + Balance + Cash Flow | 12 months |
| Orçamento departamental | Per cost center / department | 12 months |
| Orçamento de vendas | Revenue by product/service/client | 12 months |
| Orçamento de investimento (capex) | Fixed asset acquisitions | 12-36 months |
| Orçamento de tesouraria | Cash flow forecast | 12-52 weeks |
| Rolling forecast | Continuous re-forecast | 12-18 months rolling |

### Step 2 — Budget Construction (Bottom-Up)

**Revenue budget:**
```
Revenue = Volume × Price
  By client / segment / service line
  Consider: seasonality, pipeline, contracts, churn
```

**Cost budget (aligned to SNC):**

| SNC Account | Budget Category | Method |
|-------------|----------------|--------|
| 61 - CMVMC | Direct costs | % of revenue or per-unit |
| 62 - FSE | Operating expenses | Line-by-line (fixed + variable) |
| 63 - Pessoal | Personnel | Headcount × cost-per-person |
| 64 - Depreciações | Depreciation | From asset register + planned capex |
| 65 - Imparidades | Impairment | Estimated loss provisions |
| 67 - Provisões | Provisions | Risk-based estimate |
| 68 - Outros gastos | Other expenses | Historical + known changes |
| 69 - Financeiros | Financial costs | Loan schedules + working capital |

**Tax budget:**

| Tax | Budget Method |
|-----|--------------|
| IVA (payment/refund) | Based on revenue/cost IVA rates |
| IRC | Estimated effective rate × budgeted profit |
| SS | 23.75% of budgeted payroll |
| IRS (withholding) | Based on payroll budget |

### Step 3 — Budget Approval Process

| Step | Action | Timeline |
|------|--------|----------|
| 1 | Strategic objectives defined (board/CEO) | Sep-Oct |
| 2 | Department managers prepare proposals | Oct-Nov |
| 3 | Finance consolidates and challenges | Nov |
| 4 | Iterations and negotiation | Nov-Dec |
| 5 | Board approval | Dec |
| 6 | Communication to all managers | Jan |

### Step 4 — Variance Analysis

```
Variance = Actual - Budget

If Positive (revenue): Favorable
If Positive (cost): Unfavorable
If Negative (revenue): Unfavorable
If Negative (cost): Favorable
```

**Variance decomposition:**

| Type | Formula |
|------|---------|
| Price variance | (Actual Price - Budget Price) × Actual Volume |
| Volume variance | (Actual Volume - Budget Volume) × Budget Price |
| Mix variance | Change due to product/service mix shift |
| Efficiency variance | (Actual hours - Standard hours) × Standard rate |

**Threshold for investigation:** Typically >5% or >€X,XXX absolute deviation.

### Step 5 — Monthly Budget Review

| Report | Content |
|--------|---------|
| P&L Real vs Orçamento | Line-by-line variance, MTD and YTD |
| Desvios significativos | Items exceeding threshold, with explanation |
| Re-forecast | Updated full-year estimate based on actuals |
| KPIs dashboard | Key metrics vs targets |
| Cash position vs forecast | Liquidity variance |

**Monthly review template:**

```
╔════════════════════════════════════════════════════════╗
║  RELATÓRIO ORÇAMENTAL — ABRIL 2026                    ║
╠════════════════╦═══════╦═══════╦═══════╦══════════════╣
║ Rubrica        ║ Orçam ║ Real  ║ Desvio║ Desvio %     ║
╠════════════════╬═══════╬═══════╬═══════╬══════════════╣
║ Vendas         ║ 40,000║ 42,500║ +2,500║ +6.3% (F)    ║
║ FSE            ║ 8,000 ║ 9,200 ║ +1,200║ +15.0% (U)   ║
║ Pessoal        ║ 15,000║ 14,800║   -200║ -1.3% (F)    ║
║ EBITDA         ║ 12,000║ 13,500║ +1,500║ +12.5% (F)   ║
╚════════════════╩═══════╩═══════╩═══════╩══════════════╝
```

### Step 6 — Rolling Forecast

| Feature | Annual Budget | Rolling Forecast |
|---------|--------------|-----------------|
| Period | Fixed 12 months | Always 12-18 months ahead |
| Update frequency | Once/year | Monthly or quarterly |
| Detail level | Full line-by-line | Key drivers only |
| Purpose | Target setting, accountability | Decision support, agility |
| Effort | High (2-3 months) | Low (1-2 weeks per update) |

### Step 7 — Budget KPIs

| KPI | Formula | Target Setting |
|-----|---------|---------------|
| Revenue growth | (Revenue_t / Revenue_t-1) - 1 | vs market growth |
| Gross margin | (Revenue - CMVMC) / Revenue | vs industry |
| EBITDA margin | EBITDA / Revenue | vs strategic target |
| Payroll ratio | Personnel / Revenue | < 30-40% services |
| FSE ratio | FSE / Revenue | Benchmark by industry |
| Capex ratio | Capex / Revenue | Investment strategy |
| Budget accuracy | Actual / Budget | 95-105% range |
| Cash conversion | Operating CF / EBITDA | > 80% |

## Commands

| Command | Description |
|---------|-------------|
| `conta-orc:criar <ano>` | Create annual budget template |
| `conta-orc:departamento <dept>` | Departmental budget template |
| `conta-orc:variancia <periodo>` | Variance analysis report |
| `conta-orc:forecast <periodo>` | Update rolling forecast |
| `conta-orc:kpis <periodo>` | KPI dashboard |
| `conta-orc:cenario <nome>` | Create budget scenario |
| `conta-orc:comparar <cenario1> <cenario2>` | Compare scenarios |
| `conta-orc:mensal <periodo>` | Monthly budget review report |

## Output Template

```yaml
budget_review:
  period: "2026-04"
  ytd_months: 4
  income_statement:
    revenue:
      budget: 160000.00
      actual: 168000.00
      variance: 8000.00
      variance_pct: 5.0%
      status: favorable
    total_costs:
      budget: 128000.00
      actual: 131000.00
      variance: 3000.00
      variance_pct: 2.3%
      status: unfavorable
    ebitda:
      budget: 32000.00
      actual: 37000.00
      variance: 5000.00
      variance_pct: 15.6%
      status: favorable
  re_forecast:
    full_year_revenue: 510000.00
    full_year_ebitda: 115000.00
    vs_original_budget: "+4.5%"
  alerts:
    - item: "FSE"
      variance: "+15%"
      action: "Investigate subcontractor costs"
```

## Red Flags

- No budget approved before fiscal year starts
- Variance analysis not performed monthly
- Budget prepared without input from operational managers
- Revenue budget unrealistically optimistic (>20% growth without justification)
- Tax obligations (IVA, IRC, SS) not included in cash budget
- Rolling forecast not updated for 3+ months
- No scenario analysis (only single-point forecast)
- Budget not aligned with SNC account structure (makes comparison difficult)
- Capex budget not linked to depreciation forecast
- Payroll budget missing sub. natal, sub. ferias, SS employer costs

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-relatorios** | Actual vs budget comparison |
| **conta-tesouraria** | Cash flow forecast from budget |
| **conta-custos** | Cost center budgets |
| **conta-payroll** | Personnel cost budget |
| **conta-ativos** | Capex budget and depreciation forecast |
| **conta-irc** | Tax budget from budgeted profit |
| **conta-iva** | IVA cash impact in treasury budget |
| **conta-encerramento** | Year-end actual vs budget final report |
| **lucas-finance** | Agency P&L budget and KPI targets |
| **dario-financial-model** | Strategic financial modelling |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-orcamento** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-orcamento:**

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
