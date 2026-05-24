---
name: conta-tesouraria
description: Treasury management — cash flow forecast, working capital, liquidity ratios, bank relationships
version: "1.0"
---

# CONTA-TESOURARIA: Gestão de Tesouraria

## Activation Triggers

**PT:** tesouraria, cash flow, fluxo de caixa, liquidez, fundo de maneio, previsão tesouraria, working capital, saldo disponível
**EN:** treasury, cash flow, liquidity, working capital, cash forecast, cash management, bank balance, float

## Context

Treasury management ensures the entity has sufficient liquidity to meet obligations while optimizing idle cash. In Portugal, SMEs face particular challenges with payment delays (average DSO ~65 days) and seasonal cash flow variations. Effective treasury management integrates receivables, payables, and bank positions into a rolling forecast.

## Workflow

### Step 1 — Cash Position Dashboard

```
┌─────────────────────────────────────────┐
│ POSIÇÃO DE TESOURARIA — 2026-04-27      │
├─────────────────────────────────────────┤
│ Banco BCP (121)        €  45,230.50     │
│ Banco CGD (122)        €  28,100.00     │
│ Banco BPI (123)        €  12,800.00     │
│ Caixa (111)            €     850.00     │
├─────────────────────────────────────────┤
│ TOTAL DISPONÍVEL       €  86,980.50     │
│                                         │
│ Recebimentos previstos (7d)  +€15,200   │
│ Pagamentos previstos (7d)    -€22,400   │
│ Saldo previsto (7d)          €79,780.50 │
└─────────────────────────────────────────┘
```

### Step 2 — Cash Flow Forecast (13-Week Rolling)

| Week | Saldo Inicial | Recebimentos | Pagamentos | Saldo Final |
|------|--------------|-------------|-----------|-------------|
| Sem 1 | 86,980 | 15,200 | 22,400 | 79,780 |
| Sem 2 | 79,780 | 18,500 | 12,300 | 85,980 |
| Sem 3 | 85,980 | 8,200 | 35,600 | 58,580 |
| ... | ... | ... | ... | ... |

**Sources of forecast data:**

| Inflows | Source |
|---------|--------|
| Client invoices due | AR aging (conta 21) |
| Contracted recurring revenue | Service contracts |
| Expected new sales | Pipeline / CRM |
| VAT refunds | IVA a recuperar (conta 2418) |
| Other receivables | Conta 26/27 |

| Outflows | Source |
|----------|--------|
| Supplier invoices due | AP aging (conta 22) |
| Payroll + SS | Monthly fixed (conta 63 budget) |
| Tax payments | IVA, IRC, IRS calendar |
| Loan repayments | Financing schedule (conta 25) |
| Rent, utilities, insurance | Recurring fixed costs |
| Capex | Investment budget |

### Step 3 — Working Capital Analysis

```
Working Capital = Current Assets - Current Liabilities

Current Assets:
  + Conta 11/12 (Cash)
  + Conta 21 (Clientes)
  + Conta 3x (Inventários)
  + Conta 281 (Diferimentos activos)

Current Liabilities:
  - Conta 22 (Fornecedores)
  - Conta 24 (Estado — IVA, IRC, IRS, SS a pagar)
  - Conta 25 (Financiamentos curto prazo)
  - Conta 282 (Diferimentos passivos)
```

**Key ratios:**

| Ratio | Formula | Healthy Range |
|-------|---------|---------------|
| Current Ratio | CA / CL | > 1.2 |
| Quick Ratio | (CA - Inventários) / CL | > 1.0 |
| Cash Ratio | Cash / CL | > 0.3 |
| DSO (Days Sales Outstanding) | (Clientes / Vendas) × 365 | < 60 days |
| DPO (Days Payable Outstanding) | (Fornecedores / Compras) × 365 | 30-60 days |
| Cash Conversion Cycle | DSO + DIO - DPO | < 60 days |

### Step 4 — Liquidity Stress Test

| Scenario | Impact | Action |
|----------|--------|--------|
| Top client delays 30 days | -€X,XXX | Draw credit line |
| Tax payment spike (Q estimate) | -€X,XXX | Defer non-essential capex |
| Seasonal revenue dip | -XX% | Pre-arrange overdraft |
| Emergency expense | -€X,XXX | Access reserve fund |

### Step 5 — Cash Optimization

| Strategy | Benefit |
|----------|---------|
| Negotiate longer DPO with suppliers | Free cash buffer |
| Offer early payment discounts to clients | Reduce DSO |
| Sweep excess cash to term deposit | Earn interest |
| Consolidate bank accounts | Reduce fees, simplify |
| Set up cash pooling (group) | Optimize group liquidity |
| Review and cancel unused credit lines | Save commitment fees |

### Step 6 — Bank Relationship Management

| Item | Track |
|------|-------|
| Credit lines (available vs used) | Monthly |
| Bank fees (comissões) | Quarterly benchmark |
| Interest rates on loans | Vs ECB reference |
| Guarantees outstanding | Quarterly review |
| Covenants compliance | Per agreement |

## Commands

| Command | Description |
|---------|-------------|
| `conta-tes:posicao` | Current cash position across all banks |
| `conta-tes:previsao <semanas>` | Rolling cash flow forecast |
| `conta-tes:wc` | Working capital analysis |
| `conta-tes:rácios` | Liquidity ratios dashboard |
| `conta-tes:stress <cenario>` | Run liquidity stress test |
| `conta-tes:calendario` | Payment/receipt calendar |
| `conta-tes:alertas` | Low balance and overdue alerts |

## Output Template

```yaml
treasury:
  date: "2026-04-27"
  cash_position:
    total: 86980.50
    by_bank:
      BCP: 45230.50
      CGD: 28100.00
      BPI: 12800.00
      caixa: 850.00
  forecast_7d:
    inflows: 15200.00
    outflows: 22400.00
    projected_balance: 79780.50
  working_capital:
    current_assets: 185000.00
    current_liabilities: 120000.00
    net_wc: 65000.00
  ratios:
    current: 1.54
    quick: 1.22
    dso: 52
    dpo: 38
    ccc: 44
  alerts:
    - type: "LOW_BALANCE"
      bank: "BPI"
      threshold: 10000
      current: 12800
      severity: "warning"
```

## Red Flags

- Cash position below minimum operating threshold
- DSO increasing trend (clients paying slower)
- Cash conversion cycle exceeding 90 days
- Overdraft usage above 80% of limit
- Tax payments missed due to insufficient funds
- Working capital negative for 2+ consecutive months
- No 13-week rolling forecast maintained
- Single bank concentration >70% of total cash
- Payroll date approaching with insufficient balance
- Covenant breach risk on bank facilities

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-conciliacao** | Reconciled balances feed cash position |
| **conta-ap** | AP aging feeds payment forecast |
| **conta-facturacao** | AR aging feeds receipt forecast |
| **conta-iva** | IVA payment/refund dates in calendar |
| **conta-irc** | IRC payment schedule in forecast |
| **conta-ss** | SS monthly payment in forecast |
| **conta-payroll** | Payroll dates and amounts in forecast |
| **conta-orcamento** | Budget vs actual cash flow variance |
| **conta-relatorios** | Cash flow statement preparation |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-tesouraria** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-tesouraria:**

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
