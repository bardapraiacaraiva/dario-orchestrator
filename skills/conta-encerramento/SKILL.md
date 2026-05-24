---
name: conta-encerramento
description: Year-end close — closing checklist, provisions, adjustments, statutory filings, deadlines
version: "1.0"
---

# CONTA-ENCERRAMENTO: Encerramento de Contas

## Activation Triggers

**PT:** encerramento, fecho de contas, encerramento anual, fim de exercício, provisões, ajustamentos, prestação de contas, aprovação de contas, acréscimos, diferimentos, inventário
**EN:** year-end close, closing, annual close, financial close, provisions, adjustments, year-end entries, statutory filing, closing checklist

## Context

Year-end close is the most critical accounting process, transforming the ongoing ledger into final financial statements. In Portugal, entities must close accounts, prepare financial statements per SNC, file IES by July 15, approve accounts in Assembleia Geral by March 31 (or within 5 months of year-end), and have the dossier fiscal organized. Every adjustment, accrual, provision, and reclassification must be documented and reversible.

## Workflow

### Step 1 — Year-End Close Calendar (Dec Year-End)

| Date | Obligation |
|------|------------|
| Dec 31 | Cut-off date — all transactions attributed to correct period |
| Jan 31 | Physical inventory count completed |
| Feb 28 | Draft financial statements ready |
| Mar 15 | PEC payment (if not split) |
| Mar 31 | Assembleia Geral — approve accounts (5-month rule) |
| Apr 15 | Relatório Único (labor report) |
| May 31 | Modelo 22 (IRC return) filing |
| Jun 30 | Modelo 3 IRS (if applicable) |
| Jul 15 | IES (Informação Empresarial Simplificada) filing |
| Jul 15 | Dossier fiscal assembled |

### Step 2 — Closing Checklist

**Phase 1: Pre-Close (December)**

| # | Task | Status |
|---|------|--------|
| 1 | Reconcile all bank accounts (conta 12) | [ ] |
| 2 | Confirm client balances (circularização clientes) | [ ] |
| 3 | Confirm supplier balances (circularização fornecedores) | [ ] |
| 4 | Physical inventory count (existências) | [ ] |
| 5 | Review fixed asset register, verify physical existence | [ ] |
| 6 | Confirm loan balances with banks | [ ] |
| 7 | Review open purchase orders and commitments | [ ] |
| 8 | Ensure all December invoices issued | [ ] |
| 9 | Ensure all December supplier invoices received/accrued | [ ] |
| 10 | Review intercompany balances (if group) | [ ] |

**Phase 2: Adjustments (January-February)**

| # | Task | Account Impact |
|---|------|---------------|
| 11 | Calculate depreciation (full year) | D 642 / C 438 |
| 12 | Test receivables for impairment | D 651 / C 219 |
| 13 | Value inventory (lower of cost/NRV) | D 652 / C 3x9 |
| 14 | Accrue sub. férias and sub. natal (proportional) | D 632 / C 2722 |
| 15 | Accrue unused holiday days | D 632 / C 2722 |
| 16 | Record deferred revenue (rendimentos diferidos) | D 72x / C 282 |
| 17 | Record deferred expenses (gastos diferidos) | D 281 / C 62x |
| 18 | Calculate provisions (guarantees, litigation, etc.) | D 67x / C 29x |
| 19 | Record accrued revenue (acréscimos de rendimentos) | D 2721 / C 72x |
| 20 | Record accrued expenses (acréscimos de gastos) | D 62x / C 2722 |
| 21 | Foreign currency revaluation | D/C 692-693 / 782-783 |
| 22 | Review related party transactions | Disclosure |
| 23 | Review contingent liabilities | Disclosure or provision |
| 24 | Subsequent events review (until CLC date) | Adjust or disclose |

**Phase 3: Tax Adjustments (February-March)**

| # | Task |
|---|------|
| 25 | IVA annual apuramento and pro-rata adjustment |
| 26 | IRC computation (taxable profit) |
| 27 | Tributação autónoma calculation |
| 28 | Deferred tax calculation (if applicable) |
| 29 | IRC provision entry: D 8121 / C 2413x |
| 30 | Review tax loss carryforward position |

**Phase 4: Close and Report (March)**

| # | Task |
|---|------|
| 31 | Generate final balancete (after all adjustments) |
| 32 | Prepare DR (Demonstração de Resultados) |
| 33 | Prepare Balanço |
| 34 | Prepare DACP |
| 35 | Prepare Demonstração Fluxos de Caixa |
| 36 | Prepare Anexo (notes) |
| 37 | Prepare Relatório de Gestão |
| 38 | Close period 13 (closing entries) |
| 39 | Transfer resultado líquido to conta 818 |
| 40 | Open new year (opening balances) |

### Step 3 — Key Closing Entries

**Close revenue and expense to results:**
```
# Close revenue accounts (class 7)
D  71x   Vendas            €XXX,XXX
D  72x   Prestações Serv.  €XXX,XXX
C  811   Resultado Líquido €XXX,XXX

# Close expense accounts (class 6)
D  811   Resultado Líquido €XXX,XXX
C  61x   CMVMC             €XXX,XXX
C  62x   FSE               €XXX,XXX
C  63x   Pessoal           €XXX,XXX
C  64x   Depreciações      €XX,XXX
...

# Transfer to resultado líquido do período
D  811   Resultado Líquido  €XX,XXX  (profit)
C  818   Resultado Líquido Período  €XX,XXX
```

**IRC provision:**
```
D  8121  Imposto s/ Rendimento  €XX,XXX
C  2413  IRC Estimado           €XX,XXX
```

**Holiday accrual (unconsumed):**
```
D  632   Remunerações a Pagar    €XX,XXX
D  635   Encargos sobre Rem.      €X,XXX  (23.75% SS)
C  2722  Credores Acrésc.        €XX,XXX
```

### Step 4 — Statutory Filings Summary

| Filing | Portal | Deadline | Penalty if Late |
|--------|--------|----------|----------------|
| IVA Declaração Periódica (Dec) | Portal Finanças | Feb 10/May 15 | €150-€3,750 |
| Modelo 22 (IRC) | Portal Finanças | May 31 | €150-€3,750 |
| IES/DA | Portal Finanças | Jul 15 | €150-€3,750 |
| Relatório Único | GEP/MTSSS | Apr 15 | €2,040-€61,200 |
| Registo Central Benef. Efetivo | IRN/RCBE | Keep updated | €1,000-€50,000 |
| Comunicação inventários | E-Fatura (AT) | Jan 31 | €200-€2,500 |
| Registos contabilísticos (SAF-T) | Portal Finanças | Jul 15 (with IES) | Per AT |
| Aprovação contas (AG) | Registo Comercial | Mar 31 (+15 days) | Administrative sanction |

### Step 5 — Profit Distribution

After AG approval:

```
# Transfer result to retained earnings
D  818   Resultado Líquido Período  €XX,XXX
C  56    Resultados Transitados     €XX,XXX

# Legal reserve (5% until 20% of capital)
D  56    Resultados Transitados      €X,XXX
C  551   Reserva Legal               €X,XXX

# Dividend distribution
D  56    Resultados Transitados     €XX,XXX
C  264   Resultados Atribuídos      €XX,XXX

# Dividend payment (with 28% IRS withholding if individual)
D  264   Resultados Atribuídos      €XX,XXX
C  2421  Retenção IRS                €X,XXX  (28%)
C  12xx  Bank                       €XX,XXX
```

## Commands

| Command | Description |
|---------|-------------|
| `conta-enc:checklist <ano>` | Generate closing checklist with status |
| `conta-enc:calendario <ano>` | Year-end filing calendar |
| `conta-enc:ajustamentos <ano>` | List required adjustments |
| `conta-enc:fechar <periodo>` | Close accounting period |
| `conta-enc:abrir <ano>` | Open new year with balances |
| `conta-enc:distribuir <resultado>` | Profit distribution entries |
| `conta-enc:dossier <ano>` | Dossier fiscal completeness check |
| `conta-enc:status` | Overall closing status dashboard |

## Output Template

```yaml
year_end_close:
  fiscal_year: 2025
  status: "in_progress"
  checklist:
    total_items: 40
    completed: 28
    pending: 12
    blocked: 0
  key_figures:
    revenue: 450000.00
    net_income: 58500.00
    total_assets: 380000.00
    equity: 175000.00
  adjustments_posted:
    depreciation: true
    impairment_receivables: true
    holiday_accrual: true
    irc_provision: true
    inventory_valuation: false
    deferred_items: false
  filings:
    modelo22: { status: "pending", deadline: "2026-05-31" }
    ies: { status: "pending", deadline: "2026-07-15" }
    relatorio_unico: { status: "submitted", date: "2026-04-10" }
    assembleia_geral: { status: "scheduled", date: "2026-03-28" }
  dossier_fiscal:
    complete: false
    missing: ["mapa depreciações", "circularização fornecedores"]
  profit_distribution:
    net_income: 58500.00
    legal_reserve: 2925.00
    dividends: 30000.00
    retained: 25575.00
```

## Red Flags

- Year-end close not started by February
- Physical inventory not counted or count not supervised
- Receivables not tested for impairment (overstate assets)
- Holiday and bonus accruals missing (understate liabilities)
- IRC provision not calculated (tax liability not recognized)
- Assembleia Geral not held by March 31
- IES not filed by July 15 (blocks issuing new certificates)
- Resultado not transferred to resultados transitados
- Legal reserve below minimum (5% of profit until 20% of capital)
- Opening balances not matching prior year closing
- Subsequent events not considered between Dec 31 and AG date
- SAF-T annual file not validated before IES submission

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | All account balances must be reviewed |
| **conta-lancamentos** | Closing entries and period 13 adjustments |
| **conta-conciliacao** | All banks reconciled at Dec 31 |
| **conta-facturacao** | All invoices issued, cutoff verified |
| **conta-ap** | Supplier accruals and confirmations |
| **conta-iva** | Annual IVA apuramento and pro-rata |
| **conta-irc** | IRC computation and Modelo 22 |
| **conta-irs** | Modelo 10 preparation |
| **conta-ss** | Annual SS reconciliation |
| **conta-payroll** | Holiday/bonus accruals |
| **conta-ativos** | Depreciation schedule and impairment |
| **conta-relatorios** | Final financial statements |
| **conta-auditoria** | Dossier fiscal and audit coordination |
| **conta-consolidacao** | Group close and elimination entries |
| **conta-orcamento** | Final actual vs budget report |
| **lucas-finance** | Agency year-end close |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-encerramento** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-encerramento:**

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
