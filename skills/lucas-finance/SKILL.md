---
name: lucas-finance
description: "Internal agency accounting — invoicing, IVA/IRC, cash flow tracking, AT/e-Fatura compliance, monthly P&L, expense categorization, freelancer payments, client receivables, tax calendar PT. Triggers on: 'factura', 'invoice', 'IVA', 'IRC', 'cash flow', 'financas', 'AT', 'e-fatura', 'recibos verdes', 'contabilidade', 'quanto faturei', 'despesas', 'impostos'."
license: MIT
---

# LUCAS Finance — Internal Agency Accounting

Not for clients — for the AGENCY itself. Tracks money in, money out, tax obligations, and financial health.

## When to activate

- "Quanto faturei este mes?"
- "Preciso de emitir factura para [cliente]"
- "Quando e o proximo pagamento de IVA?"
- "Qual e o meu cash flow actual?"
- "Despesas do mes"
- "P&L da agencia"
- Tax calendar reminders

## Workflow

### 1. Regime Fiscal Detection

| Regime | Quem | Obrigacoes |
|---|---|---|
| **Regime Simplificado (Cat B IRS)** | Freelancer/ENI, <200K receitas | IRS trimestral (Modelo 3), IVA trimestral, sem IRC |
| **Lda (IRC)** | Sociedade por quotas | IRC (Modelo 22), IVA mensal/trimestral, IES, contabilidade organizada |
| **Unipessoal Lda** | 1 socio | Igual a Lda mas 1 pessoa |

### 2. Tax Calendar PT (automatico)

| Data | Obrigacao | Regime |
|---|---|---|
| Ate dia 20 cada mes | IVA mensal (se volume >650K) | Lda |
| Ate 15 Fev/Mai/Ago/Nov | IVA trimestral | Simplificado / Lda <650K |
| Ate 15 Fev/Mai/Ago/Nov | Pagamento por conta IRC | Lda |
| Ate 31 Mar | IRS Modelo 3 (ano anterior) | Simplificado |
| Ate 31 Mai | IRC Modelo 22 (ano anterior) | Lda |
| Ate 15 Jul | IES (Informacao Empresarial Simplificada) | Lda |
| Ate 31 Jan | Comunicacao inventarios (se aplicavel) | Lda |
| Continuo | Comunicacao facturas a AT (SAFT) | Todos |

### 3. Invoice Generator

Template de factura PT conforme:

```
FACTURA N.o [SERIE]/[NUMERO]
Data: YYYY-MM-DD

EMITENTE:
[Nome/Empresa]
NIF: [XXX XXX XXX]
Morada: [completa]
IBAN: [PTXX XXXX XXXX XXXX XXXX XXXXX]

CLIENTE:
[Nome/Empresa]
NIF: [XXX XXX XXX]
Morada: [completa]

DESCRICAO DOS SERVICOS:
| Descricao | Qtd | Preco Unit. | Total |
|---|---|---|---|
| Estrategia de marca (Mar & Brasa) | 1 | 1.500,00 | 1.500,00 |
| Auditoria SEO completa | 1 | 800,00 | 800,00 |
| Gestao redes sociais (Abril 2026) | 1 | 600,00 | 600,00 |

Subtotal: 2.900,00 EUR
IVA 23%: 667,00 EUR
TOTAL: 3.567,00 EUR

Condicoes: Pagamento a 30 dias via transferencia bancaria.
Isencao IVA: [se aplicavel — Art. 53 CIVA para <15K/ano]

Processado por programa certificado n.o [XXXX] — AT
```

**Notas:**
- Facturas DEVEM ser emitidas por software certificado AT (InvoiceXpress, Moloni, PHC, etc.)
- Este template e para REFERENCIA — a factura real sai do software
- SAFT-PT deve ser comunicado mensalmente a AT

### 4. Monthly P&L Template

```markdown
## P&L — [Mes] [Ano]

### RECEITA
| Cliente | Servico | Valor | Estado |
|---|---|---|---|
| Mar & Brasa | Estrategia digital | 1.500 | Pago |
| Atrium | SEO mensal | 2.500 | Pendente (vence 15/05) |
| Vivenda | Manutencao WP | 300 | Pago |

**Total Receita Bruta:** 4.300 EUR
**Receita Cobrada:** 1.800 EUR
**Receita Pendente:** 2.500 EUR

### DESPESAS
| Categoria | Descricao | Valor |
|---|---|---|
| Software | Claude Code Pro | 100 |
| Software | Hosting (Hetzner) | 25 |
| Software | DataForSEO | 50 |
| Servicos | Contabilista | 150 |
| Marketing | Dominio .pt | 15 |

**Total Despesas:** 340 EUR

### RESULTADO
| Metrica | Valor |
|---|---|
| Receita bruta | 4.300 EUR |
| Despesas | -340 EUR |
| Resultado antes impostos | 3.960 EUR |
| Estimativa IVA a entregar | -667 EUR |
| Estimativa IRC/IRS (~25%) | -990 EUR |
| Resultado liquido estimado | ~2.303 EUR |
| Margem liquida | ~53.5% |
```

### 5. Cash Flow Tracker

```markdown
## Cash Flow — [Mes] [Ano]

### Entradas
| Data | Origem | Valor | Acumulado |
|---|---|---|---|
| 02/04 | Vivenda (Mar) | 300 | 300 |
| 10/04 | Mar & Brasa (setup) | 1.500 | 1.800 |

### Saidas
| Data | Destino | Valor | Acumulado |
|---|---|---|---|
| 01/04 | Hosting | 25 | -25 |
| 05/04 | Claude Code | 100 | -125 |

### Previsao
| Esperado | Quando | Valor |
|---|---|---|
| Atrium (Abril) | 15/05 | 2.500 |

### Posicao
| Metrica | Valor |
|---|---|
| Saldo actual | 1.675 EUR |
| A receber (30d) | 2.500 EUR |
| Despesas previstas (30d) | -340 EUR |
| Saldo projectado (30d) | 3.835 EUR |
```

### 6. Client Receivables Tracking

```yaml
# ~/.claude/orchestrator/finance/receivables.yaml
clients:
  mar-brasa:
    invoices:
      - number: "F/2026/001"
        amount: 1500.00
        issued: "2026-04-10"
        due: "2026-05-10"
        status: "pending"  # pending | paid | overdue | disputed
    total_outstanding: 1500.00

  atrium:
    invoices:
      - number: "F/2026/002"
        amount: 2500.00
        issued: "2026-04-01"
        due: "2026-05-01"
        status: "pending"
    total_outstanding: 2500.00

summary:
  total_outstanding: 4000.00
  overdue: 0.00
  avg_days_to_pay: 28
```

## Integration Points

- **dario-proposal** → Valor do contrato → lucas-finance regista receivable
- **dario-legal** → Contrato assinado → lucas-finance inicia tracking
- **lucas-analytics** → Revenue attribution por skill → lucas-finance confirma valores reais
- **Obsidian** → P&L mensal guardado em `05 - Claude - IA/Outputs/`

## Red Flags (Legacy — see Pro version below)

- NUNCA substituir contabilista certificado — este e um auxiliar de gestao
- NUNCA emitir facturas por este sistema — usar software certificado AT
- NUNCA aconselhar optimizacao fiscal sem qualificacao — indicar contabilista
- Sempre lembrar prazos fiscais com antecedencia (7 dias)
- Sempre separar IVA do resultado (nao e receita, e imposto a entregar)

---

## Repositioning: Decision Support, Not Accounting

This skill does NOT replace a certified accountant (contabilista certificado).
It DOES:
- Help you understand your numbers before the accountant meeting
- Simulate scenarios before committing
- Track receivables and cash position in real-time
- Generate reports for internal decision-making
- Alert you to tax deadlines and obligations

Think of it as your CFO brain — the accountant is the executor.

The distinction:
- **Accountant**: submits declarations, signs Modelo 22, certifies SAFT, handles AT audits
- **This skill**: tells you WHERE you stand, WHAT to prepare, WHEN to act, and HOW MUCH you can spend

You walk into the accountant meeting KNOWING your numbers. No surprises. No "ah, nao sabia que tinha de pagar isso."

---

## Invoice Tracker

Operational invoice tracking system for the agency. This is the single source of truth for money owed to you.

### Data Structure

```yaml
# ~/.claude/orchestrator/finance/receivables.yaml
invoices:
  - id: "INV-001"
    client: "Mar & Brasa"
    amount: 5000
    currency: "EUR"
    issued: "2026-04-15"
    due: "2026-05-15"
    status: "pending"  # pending | paid | overdue | cancelled
    project: "mar-brasa"
    skills_used: ["dario-brand", "seo-local", "seo-plan"]
    certified_invoice: "F/2026/001"  # reference from InvoiceXpress/Moloni
    payment_method: "transferencia"
    notes: ""

  - id: "INV-002"
    client: "Atrium Golden Visa"
    amount: 8000
    currency: "EUR"
    issued: "2026-04-01"
    due: "2026-05-01"
    status: "pending"
    project: "atrium-golden-visa"
    skills_used: ["seo-audit", "seo-technical", "dario-content"]
    certified_invoice: "F/2026/002"
    payment_method: "transferencia"
    notes: "HNW client — always pays on time"

  - id: "INV-003"
    client: "Vivenda Creative Home"
    amount: 3000
    currency: "EUR"
    issued: "2026-03-20"
    due: "2026-04-20"
    status: "overdue"
    project: "vivenda-creative-home"
    skills_used: ["dario-wp-audit", "seo-page"]
    certified_invoice: "F/2026/003"
    payment_method: "transferencia"
    notes: "7 days overdue — send reminder"
```

### Commands

**Add invoice:**
```bash
# Append to receivables.yaml
# Required: id, client, amount, issued, due, project
# Auto-sets: status=pending, currency=EUR
```

**Mark paid:**
```bash
# Update status: "pending" → "paid"
# Add: paid_date, payment_reference
# Trigger: update monthly revenue totals
```

**Aging report (overdue analysis):**
```markdown
## Aging Report — 2026-04-27

| Client | Invoice | Amount | Days Overdue | Risk |
|--------|---------|--------|--------------|------|
| Vivenda | INV-003 | €3,000 | 7 | LOW |

### Thresholds
- 1-30 days: Send polite reminder (email)
- 31-60 days: Phone call + formal notice
- 61-90 days: Registered letter (carta registada com AR)
- 90+ days: Write-off risk — consider legal action or debt recovery

Total overdue: €3,000
Total at risk (>60d): €0
```

**Monthly revenue (sum paid invoices):**
```markdown
## Revenue — April 2026

| Status | Count | Amount |
|--------|-------|--------|
| Paid | 2 | €7,000 |
| Pending | 3 | €16,000 |
| Overdue | 1 | €3,000 |
| **Total billed** | **6** | **€26,000** |
| **Total received** | **2** | **€7,000** |

YTD Revenue (paid): €28,500
YTD Revenue (billed): €45,000
Collection rate: 63.3%
```

---

## Cash Flow Dashboard

Operational monthly dashboard — the most important view for agency survival.

```markdown
## Cash Flow — April 2026

### Income
| Source | Expected | Received | Delta |
|--------|----------|----------|-------|
| Mar & Brasa (brand + SEO) | €5,000 | €5,000 | ✓ |
| Atrium (SEO retainer) | €3,000 | €0 | ⚠ overdue 15d |
| Vivenda (maintenance) | €2,000 | €2,000 | ✓ |
| **Total** | **€10,000** | **€7,000** | **-€3,000** |

### Expenses (fixed)
| Item | Amount | Notes |
|------|--------|-------|
| Hosting (Hetzner + Vercel) | €200 | Monthly |
| Software licenses (Claude, DataForSEO, InvoiceXpress) | €150 | Monthly |
| Contabilista | €100 | Monthly retainer |
| Office / co-working | €300 | Monthly |
| **Total fixed** | **€750** | |

### Expenses (variable)
| Item | Amount | Notes |
|------|--------|-------|
| Freelancer — Designer X | €800 | Mar & Brasa project |
| Freelancer — Dev Y | €400 | Atrium fixes |
| Ads (client reimbursed) | €500 | Pass-through |
| **Total variable** | **€1,700** | |

### Summary
| Metric | Amount |
|--------|--------|
| Gross income (received) | €7,000 |
| Total expenses | €2,450 |
| **Net income** | **€4,550** |
| Runway (if no new sales) | 4,550 / 2,450 = **1.9 months** |
| Target margin (45%) | Need €4,455 net minimum → ✓ Met |
| IVA liability estimate | €7,000 × 23% = €1,610 (to reserve) |
| Available after IVA reserve | €4,550 - €1,610 = **€2,940** |

### Health Indicators
- ✓ Margin above 45% target
- ⚠ Runway below 3-month safety threshold
- ⚠ €3,000 overdue — chase immediately
- ✓ Fixed costs stable month-over-month
```

### How to generate

Run monthly on the 1st:
1. Pull all paid invoices for the month from receivables.yaml
2. Pull all expenses from expenses.yaml
3. Calculate IVA reserve (received × 23% unless Art. 53 exempt)
4. Generate dashboard markdown
5. Save to Obsidian: `05 - Claude - IA/Outputs/YYYY-MM-DD - Finance - Cash Flow.md`

---

## Tax Calendar — Operational Alerts

Not just dates — actionable alerts with what to prepare, who does what, and penalties for missing.

```
MAY 2026 — Tax Obligations:
├── May 10: IRS/IRC retencao na fonte (entregar guia)
│   WHO: Contabilista submits via Portal das Financas
│   YOUR ACTION: Check if any freelancer payments last month
│   → If yes, confirm contabilista submitted Modelo 10
│   PREPARE: List of payments, NIFs, amounts, tax withheld (25% if >€12,500/yr)
│   PENALTY IF MISSED: Coima €150-€3,750 + juros de mora
│   
├── May 20: Seguranca Social
│   WHO: Auto-debit if configured. If not, pay via SS Direta
│   YOUR ACTION: Verify amount matches expected
│   AMOUNT: Salario bruto × 23.75% (patronal) + 11% (trabalhador)
│   → ENI sem trabalhadores: 21.4% sobre rendimento relevante (70% do lucro)
│   PENALTY IF MISSED: Coima + suspensao de beneficios
│   
├── May 20: IVA mensal (if regime mensal — volume >€650K)
│   WHO: Contabilista submits declaracao periodica
│   YOUR ACTION: Ensure all invoices for April are in SAFT
│   PREPARE: Export SAFT-PT from InvoiceXpress/Moloni, verify all invoices included
│   VERIFY: IVA dedutivel (compras) vs IVA liquidado (vendas)
│   PENALTY IF MISSED: Portal closes → automatic coima €150+ per day
│   
├── May 15: IVA trimestral (if applicable — Q1 Jan-Mar)
│   WHO: Contabilista submits
│   YOUR ACTION: Reconcile Q1 invoices vs SAFT export
│   AMOUNT: IVA liquidado (vendas) - IVA dedutivel (compras com factura)
│   
└── May 31: Pagamento por conta IRC (1st installment — Lda only)
    WHO: Pay via Portal das Financas or multibanco ref
    YOUR ACTION: Confirm with contabilista the calculation
    FORMULA: (IRC colecta anterior - retencoes na fonte) × coeficiente
    → 1st payment: 1/3 of total
    → Coeficiente varies: usually (colecta - retencoes) / volume negocios anterior
    NOTE: If last year IRC was zero → no pagamento por conta
```

### Full Year Calendar (Critical Dates)

| Month | Day | Obligation | Regime | Priority |
|-------|-----|-----------|--------|----------|
| Jan | 31 | Comunicacao inventarios | Lda | LOW (services) |
| Feb | 15 | IVA trimestral (Q4) | Todos | HIGH |
| Feb | 15 | Pagamento por conta IRC (3rd) | Lda | HIGH |
| Mar | 31 | IRS Modelo 3 (ano anterior) | ENI/Cat B | CRITICAL |
| Mai | 15 | IVA trimestral (Q1) | Todos | HIGH |
| Mai | 31 | IRC Modelo 22 (ano anterior) | Lda | CRITICAL |
| Mai | 31 | Pagamento por conta IRC (1st) | Lda | HIGH |
| Jun | 30 | IRS (se Lda paga dividendos) | Lda | MEDIUM |
| Jul | 15 | IES | Lda | HIGH |
| Ago | 15 | IVA trimestral (Q2) | Todos | HIGH |
| Set | 15 | Pagamento por conta IRC (2nd) | Lda | HIGH |
| Nov | 15 | IVA trimestral (Q3) | Todos | HIGH |
| Dez | 15 | Pagamento especial por conta | Lda | MEDIUM |

### Alert Automation

7 days before each deadline:
1. Check if obligation applies to current regime
2. Generate prep checklist
3. Flag to user: "Deadline em 7 dias: [obligation]. Preparar: [list]"
4. Verify contabilista has necessary documents

---

## Profitability per Client

Track profit per client to know where to focus, where to raise prices, and where to fire clients.

```markdown
## Client Profitability — Q1 2026

| Client | Revenue | Hours | Tokens | Direct Cost | Profit | Margin |
|--------|---------|-------|--------|-------------|--------|--------|
| Mar & Brasa | €5,000 | 40h | 35K | €2,000 | €3,000 | 60% |
| Atrium Golden Visa | €8,000 | 60h | 45K | €3,500 | €4,500 | 56% |
| Vivenda Creative Home | €3,000 | 25h | 30K | €1,200 | €1,800 | 60% |
| Lisbon Dog Care | €1,500 | 20h | 25K | €800 | €700 | 47% |

### Rankings
- Top client by margin: Mar & Brasa + Vivenda (60%)
- Top client by absolute profit: Atrium (€4,500)
- Bottom client by margin: Lisbon Dog Care (47%)

### Alerts
- ⚠ If any client margin < 30% → REVIEW scope or RAISE price immediately
- ⚠ If hours > estimate by 20% → scope creep detected → renegotiate
- ✓ If margin > 55% → healthy, maintain

### Direct Cost Calculation
Direct cost per client includes:
- Your time: hours × internal rate (e.g., €50/h for planning, free for AI execution)
- Freelancer costs allocated to that project
- Tool costs directly attributable (e.g., DataForSEO credits used)
- AI token costs (from orchestrator budget_tracker)

### Quarterly Action
1. Sort clients by margin (ascending)
2. Bottom 20%: raise prices or reduce scope
3. Top 20%: upsell with new services
4. Middle: maintain, look for efficiency gains
```

---

## Freelancer Payment Tracker

Critical for tax compliance — Portugal requires retencao na fonte IRS on payments to freelancers above €12,500/year.

```yaml
# ~/.claude/orchestrator/finance/freelancers.yaml
freelancers:
  - name: "Designer X"
    nif: "123456789"
    regime: "recibos_verdes"
    irs_retention_rate: 0.25  # 25% mandatory if YTD > €12,500
    payments:
      - date: "2026-01-15"
        amount: 800
        project: "vivenda-creative-home"
        retencao_irs: 0  # below threshold at this point
        retencao_ss: 0
        recibo_verde_ref: "RV/2026/001"
      - date: "2026-02-10"
        amount: 1200
        project: "mar-brasa"
        retencao_irs: 0
        retencao_ss: 0
        recibo_verde_ref: "RV/2026/015"
      - date: "2026-03-12"
        amount: 800
        project: "mar-brasa"
        retencao_irs: 0
        retencao_ss: 0
        recibo_verde_ref: "RV/2026/028"
      - date: "2026-04-10"
        amount: 800
        project: "atrium-golden-visa"
        retencao_irs: 0
        retencao_ss: 0
        recibo_verde_ref: "RV/2026/042"
    ytd_total: 3600
    annual_threshold_alert: false  # becomes TRUE if approaching €12,500
    projected_annual: 10800  # ytd × (12/months_elapsed)

  - name: "Dev Y"
    nif: "987654321"
    regime: "recibos_verdes"
    irs_retention_rate: 0.25
    payments:
      - date: "2026-04-05"
        amount: 400
        project: "atrium-golden-visa"
        retencao_irs: 0
        retencao_ss: 0
        recibo_verde_ref: "RV/2026/039"
    ytd_total: 1600
    annual_threshold_alert: false
    projected_annual: 4800
```

### Retention Rules (IRS)

| YTD Payment to Freelancer | Retencao IRS | Action |
|---------------------------|-------------|--------|
| < €12,500/year | 0% (exempt) | Freelancer can request dispensa |
| >= €12,500/year | 25% mandatory | YOU must withhold and deliver to AT |

### Alert System

- When `projected_annual` > €10,000 → WARNING: approaching threshold
- When `ytd_total` > €12,500 → MANDATORY: apply 25% retencao on ALL subsequent payments
- Monthly: verify all recibos verdes received match payments made
- January: report total payments per freelancer for Modelo 10

### Compliance Checklist (Monthly)

1. Verify each freelancer emitted recibo verde for the payment
2. Confirm NIF matches between recibo and your records
3. If retencao applied: confirm guia de pagamento submitted by day 20
4. Archive recibos verdes digitally (7 year retention requirement)

---

## Integration with Orchestrator

How finance connects to the rest of the DARIO + LUCAS ecosystem.

### Automatic Triggers

| Event | Source | Finance Action |
|-------|--------|---------------|
| Task completes | orchestrator taskboard | budget_tracker.py updates token spend |
| Project completes | dario-orchestrator | Prompt user: "Create invoice for [client]?" |
| Proposal accepted | dario-proposal | Create receivable entry with payment terms |
| Contract signed | dario-legal | Activate payment tracking, set due dates |
| Freelancer assigned | dario-hr | Add to freelancer tracker, estimate cost |
| Month end | lucas-heartbeat | Auto-generate P&L + Cash Flow dashboard |
| Quarter end | lucas-heartbeat | IVA calculation reminder + prep checklist |
| Budget > 80% | lucas-autopilot | Finance alert: "Token spend approaching limit" |

### Data Flow

```
dario-proposal (contract value)
    → lucas-finance (receivable created)
        → invoice issued (certified software)
            → payment received
                → lucas-analytics (revenue attribution by skill)
                    → client profitability updated

orchestrator budget_tracker (token costs)
    → lucas-finance (expense categorized)
        → P&L monthly (cost of delivery)
            → margin per client calculated
```

### Monthly Automation Sequence (1st of each month)

1. Export SAFT-PT from billing software
2. Reconcile: invoices issued vs receivables.yaml
3. Mark paid invoices (check bank statement)
4. Generate aging report for overdue
5. Pull expenses from bank/tools
6. Calculate: revenue - expenses - IVA reserve = net
7. Generate P&L + Cash Flow dashboards
8. Save to Obsidian vault
9. Flag upcoming tax deadlines (next 30 days)
10. Update client profitability if quarter end

---

## Output Template — Monthly Financial Report

Full template for the monthly finance deliverable.

```markdown
# Financial Report — [Month] [Year]
## Agency: DARIO Digital

### Executive Summary
- Revenue (received): €X,XXX
- Revenue (billed, pending): €X,XXX  
- Total expenses: €X,XXX
- Net result: €X,XXX
- Margin: XX%
- Runway: X.X months
- Health: [GREEN | YELLOW | RED]

---

### 1. Revenue Breakdown
| Client | Service | Billed | Received | Status |
|--------|---------|--------|----------|--------|
| ... | ... | ... | ... | ... |

### 2. Expense Breakdown
#### Fixed
| Item | Amount |
|------|--------|
| ... | ... |

#### Variable
| Item | Amount | Project |
|------|--------|---------|
| ... | ... | ... |

### 3. Cash Flow Position
| Metric | Amount |
|--------|--------|
| Bank balance (start of month) | €X,XXX |
| + Received | €X,XXX |
| - Paid out | €X,XXX |
| = Bank balance (end of month) | €X,XXX |
| Pending receivables (30d) | €X,XXX |
| IVA reserve | €X,XXX |
| Available cash | €X,XXX |

### 4. Aging Report
| Client | Amount | Days Overdue | Action |
|--------|--------|--------------|--------|
| ... | ... | ... | ... |

### 5. Tax Obligations (Next 30 Days)
| Date | Obligation | Amount Est. | Status |
|------|-----------|-------------|--------|
| ... | ... | ... | Prepared / Pending |

### 6. Client Profitability (if quarter end)
| Client | Revenue | Cost | Margin |
|--------|---------|------|--------|
| ... | ... | ... | ... |

### 7. KPIs
| KPI | This Month | Last Month | Trend |
|-----|-----------|-----------|-------|
| Collection rate | XX% | XX% | ↑/↓ |
| Avg days to pay | XX | XX | ↑/↓ |
| Margin | XX% | XX% | ↑/↓ |
| Runway | X.X mo | X.X mo | ↑/↓ |
| Overdue amount | €X,XXX | €X,XXX | ↑/↓ |

### 8. Actions Required
- [ ] Chase: [client] — €X,XXX overdue Xd
- [ ] Prepare: [tax obligation] by [date]
- [ ] Review: [client] margin below 30%
- [ ] Invoice: [client] for [completed work]

---
Generated: YYYY-MM-DD by lucas-finance
```

---

## Save Location

All finance outputs go to Obsidian for permanent record:

| Report Type | Path |
|-------------|------|
| Monthly P&L | `05 - Claude - IA/Outputs/YYYY-MM-DD - Finance - P&L [Month].md` |
| Cash Flow | `05 - Claude - IA/Outputs/YYYY-MM-DD - Finance - Cash Flow [Month].md` |
| Full Monthly Report | `05 - Claude - IA/Outputs/YYYY-MM-DD - Finance - Monthly Report [Month].md` |
| Tax Prep Checklist | `05 - Claude - IA/Outputs/YYYY-MM-DD - Finance - Tax Prep [Obligation].md` |
| Client Profitability | `05 - Claude - IA/Outputs/YYYY-MM-DD - Finance - Client Profitability Q[N].md` |
| Aging Report | `05 - Claude - IA/Outputs/YYYY-MM-DD - Finance - Aging Report.md` |

Vault: `C:\Users\barda\OneDrive\Documents\D.A.R.I.O`

---

## Red Flags (Pro)

Eight specific operational warnings that protect the agency from real financial damage.

1. **Never issue invoice without certified software (InvoiceXpress, Moloni, PHC)**
   - AT requires software certificado com numero de certificacao
   - Invoices issued outside certified software = invalid = coima €750-€37,500
   - This skill generates REFERENCES only — the real invoice comes from the software

2. **Never miss IVA deadline (portal closes, penalties immediate)**
   - Portal das Financas closes submission after deadline
   - Automatic coima: €150 minimum, escalates with delay
   - Late payment: juros de mora 4%/year + juros compensatorios
   - If >90 days late: AT can initiate execucao fiscal (asset seizure)

3. **Never pay freelancer >€12,500/year without retencao IRS 25%**
   - Legal obligation is on the PAYER (you), not the freelancer
   - If you fail to withhold: YOU pay the tax + coima
   - Track cumulative payments per NIF across the calendar year
   - When in doubt, apply retencao — freelancer claims back via IRS declaration

4. **Always reconcile receivables monthly — overdue >60 days = write-off risk**
   - Portuguese statute of limitations for services: 2 years (Art. 317 CC)
   - But practical recovery drops to <20% after 90 days
   - Monthly reconciliation catches issues early
   - Formal demand letter (carta registada com AR) preserves legal rights

5. **Always keep 3 months runway minimum — below = emergency mode**
   - Runway = available cash / monthly fixed expenses
   - Below 3 months: stop all non-essential spending, accelerate collections
   - Below 1.5 months: emergency — consider credit line, defer supplier payments
   - Target: 6 months runway for seasonal stability

6. **Never mix personal and business expenses — AT audits specifically for this**
   - AT cross-references: lifestyle vs declared income
   - Separate bank accounts mandatory for Lda, recommended for ENI
   - Personal expenses in business = IVA indevidamente deduzido = devolver + coima
   - Rule: if the expense has no business invoice with your NIF, it is personal

7. **Always export SAFT-PT monthly — required for AT compliance**
   - SAFT (Standard Audit File for Tax) must be communicated monthly to AT
   - Deadline: until day 12 of following month (automatic in most software)
   - If manual: export from billing software → upload to Portal das Financas
   - Missing SAFT = AT assumes revenue is HIGHER than declared

8. **Never calculate IRC without including derrama municipal — varies by concelho**
   - IRC rate: 21% (standard) or 17% (PME on first €50K)
   - Derrama municipal: 0% to 1.5% depending on concelho
   - Derrama estadual: +3% on profit >€1.5M, +5% on >€7.5M, +9% on >€35M
   - Lisboa: 1.5% derrama. Porto: 1.5%. Some concelhos: 0%
   - Total effective rate (PME, Lisboa): 17% + 1.5% = 18.5% on first €50K, then 21% + 1.5% = 22.5%
   - Always ask contabilista for the exact derrama of your sede fiscal

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Regime fiscal correctamente identificado

- [ ] Output identifica explicitamente o regime do utilizador (Simplificado / Lda / Unipessoal)
- [ ] Obrigações listadas correspondem ao regime detectado (ex: sem IRC para Cat B)
- [ ] Se regime ambíguo, output pede clarificação antes de calcular

❌ NOT delivery-ready: "Tens obrigações de IVA trimestrais e possivelmente IRC."
✅ Delivery-ready: "Estás em **Regime Simplificado (Cat B IRS)** → IVA trimestral até 15 Ago 2026, **sem IRC**, IRS Modelo 3 até 31 Mar 2027."

---

### Gate 2 — Tax calendar com datas reais e próximo prazo destacado

- [ ] Pelo menos 3 datas concretas listadas com DD/MM/AAAA
- [ ] Prazo mais próximo marcado explicitamente ("⚠️ Próximo em X dias")
- [ ] Regime fiscal do utilizador filtra quais datas são aplicáveis (não dump genérico)
- [ ] Alerta antecipado se prazo < 7 dias

❌ NOT delivery-ready: "O IVA é entregue trimestralmente. Verifica as datas na AT."
✅ Delivery-ready: "⚠️ **IVA Q2 vence em 15 Ago 2026 (18 dias).** Valor estimado: 1.081 EUR. Próximas: IRC Pagamento por conta 15 Nov 2026, IES 15 Jul 2026 ✓ já passou."

---

### Gate 3 — Invoice / factura com todos os campos obrigatórios AT preenchidos

- [ ] Número de série sequencial presente (ex: F/2026/004)
- [ ] NIF emitente + NIF cliente + moradas completas
- [ ] IVA calculado correctamente (23% / 6% / 0% com justificação legal)
- [ ] IBAN e condições de pagamento incluídas
- [ ] Nota de software certificado AT presente (nunca emitir via DARIO)

❌ NOT delivery-ready: "Factura para o cliente com total de 3.500 EUR + IVA."
✅ Delivery-ready: "**F/2026/004** — Atrium Hospitality, NIF 501 234 567, SEO mensal Mai 2026: 2.500,00 + IVA 23% (575,00) = **3.075,00 EUR** — vence 01/Jun/2026 — emitir no InvoiceXpress/Moloni."

---

### Gate 4 — P&L com separação explícita IVA ≠ receita

- [ ] IVA liquidado listado separadamente das receitas (nunca somado ao resultado)
- [ ] Receita cobrada vs. pendente discriminadas
- [ ] Resultado líquido estimado com taxa IRC/IRS aplicada correctamente ao regime
- [ ] Margem líquida calculada sobre receita bruta (não sobre cobrada)

❌ NOT delivery-ready: "Resultado do mês: 4.300 EUR de receitas menos 340 EUR de despesas = 3.960 EUR."
✅ Delivery-ready: "Receita bruta: 4.300 EUR | IVA a entregar (não é teu): −667 EUR | Despesas: −340 EUR | Base tributável: 3.293 EUR | IRS est. 25%: −823 EUR | **Resultado líquido: ~2.470 EUR (57.4% margem)**."

---

### Gate 5 — Cash flow com saldo actual + previsão 30 dias

- [ ] Entradas e saídas reais com datas DD/MM listadas
- [ ] Saldo actual calculado (entradas − saídas verificadas)
- [ ] Previsão 30 dias inclui receivables pendentes + despesas recorrentes conhecidas
- [ ] Receivables em overdue (vencimento passado + não pago) assinalados com ❗

❌ NOT delivery-ready: "O teu saldo está positivo e tens alguns pagamentos pendentes."
✅ Delivery-ready: "Saldo actual: **1.675 EUR** | A receber ≤30d: +2.500 EUR (Atrium, vence 01/Jun) | Despesas previstas: −340 EUR | **Saldo projectado 30d: 3.835 EUR** | ❗ Mar & Brasa F/2026/001 venceu há 3 dias — sem pagamento registado."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders entre `< >`

- [ ] Nenhum `[NOME]`, `[VALOR]`, `[DATA]`, `[NIF]` ou `<angle-bracket>` no output final
- [ ] Cliente nomeado (ex: Atrium, Mar & Brasa, Vivenda) ou pedida clarificação explícita
- [ ] Valores numéricos concretos presentes — nunca "X EUR" ou "valor acordado"
- [ ] Se dados em falta, output lista exactamente o que precisa: "Para continuar preciso do NIF do cliente e valor do serviço"

❌ NOT delivery-ready: "Factura para `<cliente>` no valor de `<total>` EUR com IVA de `<taxa>`%."
✅ Delivery-ready: "Factura F/2026/005 — **Vivenda**, NIF 509 876 543, Manutenção WP Mai 2026: **300,00 EUR** + IVA 23% = **369,00 EUR**."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados reais do cliente
- 🟡 **assumed** — plausível mas precisa confirmação do Lucas antes de entregar
- 🟢 **projection** — previsão por design (não verificável no momento)

Output checklist upfront mostra ao leitor exactamente o que é trust-as-is vs o que precisa de verify. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
```
Receita Abril: 4.300 EUR | Resultado líquido: ~2.303 EUR | IVA a entregar: 667 EUR
Atrium paga a 30 dias. Margem líquida: 53.5%
```
*(reader assume tudo verified — mas IVA, prazo Atrium e margem podem ser estimates não confirmados)*

✅ Delivery-ready:
```
🔵 verified   — Factura F/2026/002 Atrium: 2.500 EUR (emitida 01/04, due 01/05)
🔵 verified   — Despesas fixas Abril: 340 EUR (Claude Code 100 + Hosting 25 + DataForSEO 50 + Contabilista 150 + Domínio 15)
🟡 assumed    — Regime IVA trimestral (não mensal) — confirmar se volume 2025 ficou <650K
🟡 assumed    — Taxa IRC efectiva ~25% usada no P&L — confirmar com contabilista se há deduções
🟢 projection — Saldo projectado 30d: 3.835 EUR (depende de Atrium pagar em 15/05)
🟢 projection — Resultado líquido estimado: ~2.303 EUR (pré-apuramento fiscal real)
```

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir assumptions com actuals (regime IVA, taxa IRC real, NIFs, IBANs)
- [ ] Todas as facturas 🔵 cruzadas com software AT certificado (InvoiceXpress / Moloni / PHC) antes de comunicar SAFT
- [ ] Todas as 🟢 projecções de cash flow e resultado líquido apresentadas ao Lucas com label "estimativa" — expectativas claras antes de decisões de tesouraria

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## P&L + Cash Flow — Abril 2026
**Regime:** Lda (IRC) | **Software facturação:** InvoiceXpress

---

### RECEITA — Abril 2026

| Cliente         | Serviço                        | Factura      | Valor      | Estado                        |
|-----------------|-------------------------------|--------------|------------|-------------------------------|
| Atrium          | SEO mensal Abr                | F/2026/002   | 2.500,00   | ⚠️ Pendente (vence 01/Mai)    |
| Mar & Brasa     | Estratégia digital + setup    | F/2026/003   | 1.500,00   | ✅ Pago (10/04)                |
| Vivenda         | Manutenção WP Abr             | F/2026/004   | 300,00     | ✅ Pago (02/04)                |

**Receita Bruta:** 4.300,00 EUR
**Cobrada (Abril):** 1.800,00 EUR
**Pendente:** 2.500,00 EUR (Atrium — vence 01/Mai/2026)

> ⚠️ IVA liquidado nas facturas: 989,00 EUR — **não é receita tua, é imposto a entregar à AT.**

---

### DESPESAS — Abril 2026

| Categoria   | Descrição              | Valor    | Dedutível IRC |
|-------------|------------------------|----------|---------------|
| Software    | Claude Code Pro        | 100,00   | ✅ Sim         |
| Software    | Hosting Hetzner        | 25,00    | ✅ Sim         |
| Software    | DataForSEO             | 50,00    | ✅ Sim         |
| Serviços    | Contabilista (mensal)  | 150,00   | ✅ Sim         |
| Marketing   | Domínio .pt (anual/12) | 15,00    | ✅ Sim         |

**Total Despesas:** 340,00 EUR

---

### RESULTADO — Abril 2026

| Métrica                          | Valor         |
|----------------------------------|---------------|
| Receita bruta                    | 4.300,00 EUR  |
| IVA liquidado (entregar AT)      | −989,00 EUR   |
| Receita líquida de IVA           | 3.311,00 EUR  |
| Despesas dedutíveis              | −340,00 EUR   |
| Resultado antes impostos         | 2.971,00 EUR  |
| Estimativa IRC (21% taxa normal) | −623,91 EUR   |
| **Resultado líquido estimado**   | **2.347,09 EUR** |
| Margem líquida                   | **54,6%**     |

---

### CASH FLOW — Abril 2026

**Entradas**
| Data  | Origem            | Valor    | Acumulado  |
|-------|-------------------|----------|------------|
| 02/04 | Vivenda (Mar→Abr) | 300,00   | 300,00     |
| 10/04 | Mar & Brasa       | 1.500,00 | 1.800,00   |

**Saídas**
| Data  | Destino        | Valor   | Acumulado |
|-------|----------------|---------|-----------|
| 01/04 | Hetzner        | 25,00   | −25,00    |
| 05/04 | Claude Code    | 100,00  | −125,00   |
| 15/04 | Contabilista   | 150,00  | −275,00   |
| 20/04 | DataForSEO     | 50,00   | −325,00   |

**Saldo actual (30 Abr):** 1.475,00 EUR

**Previsão Maio 2026**
| Esperado              | Quando  | Valor     |
|-----------------------|---------|-----------|
| Atrium F/2026/002     | 01/Mai  | 2.500,00  |
| Despesas recorrentes  | Mai     | −340,00   |
| IVA Q1 entregue ✓     | —       | —         |

**Saldo projectado 31 Mai:** 3.635,00 EUR

---

### 📅 Próximos prazos fiscais (Lda)

| Prazo      | Obrigação                           | Urgência              |
|------------|-------------------------------------|----------------------|
| 20/Mai/2026 | IVA mensal Abril → AT (SAFT)       | ⚠️ 20 dias          |
| 31/Mai/2026 | IRC Modelo 22 (ano 2025)           | ⚠️ 31 dias          |
| 15/Jul/2026 | IES                                | 🟡 76 dias          |
| 15/Ago/2026 | IVA Q2 (se trimestral)             | 🟢 107 dias         |

> 🔴 **Acção imediata:** IRC Modelo 22 vence 31 Mai — confirma com contabilista
> esta semana se valores de 2025 estão fechados.

---

*Este output é auxiliar de gestão — não substitui contabilista certificado (OCC).
Facturas emitidas exclusivamente via InvoiceXpress (software certificado AT n.º 1234).*
```

---

## Output anti-patterns

- Incluir IVA no resultado líquido como se fosse receita da agência ("ganhei 4.989 EUR")
- Listar datas fiscais genéricas sem filtrar pelo regime do utilizador detectado
- Gerar template de factura com campos `[NIF]` / `[CLIENTE]` por preencher, sem pedir os dados em falta
- Dar estimativa de IRC/IRS sem especificar a taxa aplicada e porquê (21% IRC normal vs. 17% PME vs. 25% IRS Cat B)
- Omitir separação entre receita cobrada e receita pendente no P&L (distorce percepção de liquidez)
- Recomendar optimização fiscal concreta (ex: "deduz X como despesa") sem remeter para contabilista — fora de âmbito deste skill
- Calcular margem líquida sobre receita cobrada em vez de receita bruta (favorece artificialmente meses com pagamentos atrasados)
- Apresentar saldo de cash flow sem distinguir saldo actual (verificado) de saldo projectado (estimado)
- Esquecer alerta de 7 dias para prazos iminentes — output entregue sem ⚠️ quando vencimento < 7 dias
- Tratar SAFT-PT como opcional — comunicação à AT é obrigatória e contínua, não periódica
