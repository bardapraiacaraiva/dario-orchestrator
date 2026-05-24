---
name: conta-payroll
description: Payroll processing — salaries, subsidios alimentacao/ferias/natal, overtime, termination, DMR
version: "1.0"
---

# CONTA-PAYROLL: Processamento Salarial

## Activation Triggers

**PT:** salário, vencimento, recibo de vencimento, processamento salarial, subsídio natal, subsídio férias, subsídio alimentação, horas extra, rescisão, indemnização, férias, DMR
**EN:** payroll, salary, wages, pay slip, Christmas bonus, holiday pay, meal allowance, overtime, termination, severance, DMR

## Context

Portuguese payroll is governed by the Código do Trabalho (CT), CIRS, and Código Contributivo. Employers must process monthly salaries including mandatory components (sub. alimentação, sub. férias, sub. natal), withhold IRS and SS, submit DMR by the 10th, and pay SS by the 20th. Minimum wage (RMMG) for 2025: €870/month (14 payments).

## Workflow

### Step 1 — Salary Components

| Component | Mandatory | Frequency | Taxable IRS | SS Base |
|-----------|-----------|-----------|-------------|---------|
| Remuneração base | Yes | Monthly (×14) | Yes | Yes |
| Subsídio alimentação | Yes (if in CIT/practice) | Monthly (per working day) | No (up to €6.00 cash / €10.20 card) | No (up to limit) |
| Subsídio de Natal | Yes | Nov/Dec (or proportional) | Yes (separate table) | Yes |
| Subsídio de Férias | Yes | Before holiday period | Yes (separate table) | Yes |
| Diuturnidades | If CIT provides | Monthly | Yes | Yes |
| Horas extraordinárias | When worked | Monthly | Yes | Yes |
| Comissões | If applicable | Monthly/quarterly | Yes | Yes |
| Abono para falhas | If applicable | Monthly | No (up to 5% base) | No (up to 5% base) |
| Prémios | If applicable | Per occurrence | Yes | Yes |

### Step 2 — Overtime Rates (Código do Trabalho)

| Type | First Hour | Subsequent | Rest Day / Holiday |
|------|-----------|------------|-------------------|
| Dia útil | +25% | +37.5% | +50% |
| Dia de descanso | +50% | +50% | +50% |
| Feriado | +50% | +50% | +50% |

**Maximum overtime:** 150 hours/year (general), 175 hours (companies <50 employees).

### Step 3 — Monthly Payroll Calculation

```
Employee: João Santos
Category: Administrativo | Contract: Sem Termo | Full-time

Remuneração base:                €1,500.00
Subsídio alimentação (22 days):  €   132.00  (€6.00/day, cash)
Horas extra (5h × 25%):         €    64.37
Duodécimos sub. férias:         €   125.00  (1/12 of base)
Duodécimos sub. natal:          €   125.00  (1/12 of base)
──────────────────────────────────────────────
BRUTO:                           €1,946.37

Deduções:
  IRS (tabela 2026, solteiro, 0 dep.): €  232.50  (on €1,689.37)
  SS trabalhador (11%):                €  189.37  (on €1,714.37*)
──────────────────────────────────────────────
Deduções totais:                        €  421.87
──────────────────────────────────────────────
LÍQUIDO:                                €1,524.50

Encargos patronais:
  SS empregador (23.75%):              €  407.16  (on €1,714.37*)
  Seguro AT:                           €   17.14  (~1%)
  FCT/FGCT:                            €   17.14  (1% each)
──────────────────────────────────────────────
CUSTO TOTAL EMPRESA:                    €2,387.67
```

*SS base = bruto - sub. alimentação isento

### Step 4 — Subsídio de Natal

| Option | When Paid | Amount |
|--------|-----------|--------|
| Full payment | Until 15 December | 1× remuneração base |
| Duodécimos | Monthly (1/12 each) | Requires written agreement |
| Proportional | Entry/exit mid-year | Pro-rata by months worked |

### Step 5 — Subsídio de Férias

| Option | When Paid | Amount |
|--------|-----------|--------|
| Full payment | Before holiday start | 1× remuneração base |
| Duodécimos | Monthly (1/12 each) | Requires written agreement |
| Proportional | First year / exit | 2 days per month worked |

**Holiday entitlement:** 22 working days per year (accrued in prior year).

### Step 6 — Termination / Severance

| Type | Notice Period | Compensation |
|------|--------------|-------------|
| Mútuo acordo | Agreed | Negotiated |
| Despedimento com justa causa | None | None |
| Despedimento colectivo | 15-75 days | 14 days base salary per year of service |
| Extinção posto trabalho | 15-75 days | 14 days base salary per year of service |
| Caducidade (termo certo) | 15 days | 24 days per year (first 3yr) + 18 days thereafter |
| Denúncia pelo trabalhador | 30-60 days | None |

**Severance calculation (post-2013):** 14 days × base salary ÷ 30 × years of service (or fraction)
**Cap:** 20× RMMG per severance, 12× monthly base per year.

**Exit payment includes:**
- Remunerações em atraso
- Subsídio férias e natal proporcionais
- Férias não gozadas (year + proportional)
- Indemnização/compensação (if applicable)

### Step 7 — DMR and Reporting

| Report | Deadline | Content |
|--------|----------|---------|
| DMR (Declaração Mensal Remunerações) | 10th of following month | AT + SS combined |
| Recibo de vencimento | With salary payment | Mandatory detailed payslip |
| Relatório Único (Anexo A) | By 15 April (prior year) | Annual employment report |
| Mapa de férias | Until 15 April | Holiday schedule |
| Quadros de pessoal | Part of Relatório Único | Workforce structure |

## Commands

| Command | Description |
|---------|-------------|
| `conta-pay:processar <periodo>` | Process monthly payroll |
| `conta-pay:recibo <trabalhador>` | Generate payslip |
| `conta-pay:dmr <periodo>` | Generate DMR data |
| `conta-pay:ferias <trabalhador>` | Calculate holiday entitlement |
| `conta-pay:natal <ano>` | Calculate Christmas bonus |
| `conta-pay:rescisao <trabalhador>` | Calculate termination package |
| `conta-pay:horas-extra <trabalhador>` | Process overtime |
| `conta-pay:custo <trabalhador>` | Full employer cost breakdown |
| `conta-pay:simulacao <bruto>` | Simulate net from gross |

## Output Template

```yaml
payroll:
  period: "2026-04"
  employees: 5
  summary:
    gross_salaries: 9500.00
    meal_allowance: 660.00
    overtime: 320.00
    total_gross: 10480.00
  deductions:
    irs_withholding: 1580.00
    ss_employee: 1045.00
    total_deductions: 2625.00
  net_pay: 7855.00
  employer_costs:
    ss_employer: 2256.25
    insurance_at: 95.00
    fct_fgct: 190.00
    total_employer: 2541.25
  total_cost: 13021.25
  deadlines:
    salary_payment: "2026-04-30"
    dmr_submission: "2026-05-10"
    ss_payment: "2026-05-20"
    irs_payment: "2026-05-20"
```

## Red Flags

- Salary below RMMG (€870/month in 2025, 14 payments)
- Sub. alimentação above exempt limit without taxation
- Overtime exceeding annual legal maximum (150h/175h)
- Sub. Natal not paid by 15 December
- DMR not submitted by 10th
- Termination compensation incorrectly calculated
- Missing seguro de acidentes de trabalho (mandatory)
- FCT/FGCT contributions not processed
- Holiday entitlement not accruing correctly
- Duodécimos paid without employee written agreement
- IRS withholding using wrong table (single vs married, dependents)

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-irs** | IRS withholding tables and DMR |
| **conta-ss** | SS contributions and DRI |
| **conta-lancamentos** | Payroll journal entries (631/635/2312/2421/245) |
| **conta-tesouraria** | Payroll payment in cash flow forecast |
| **conta-irc** | Personnel costs deductible for IRC |
| **conta-relatorios** | Gastos com pessoal in DR |
| **conta-encerramento** | Holiday/bonus accruals at year-end |
| **conta-orcamento** | Payroll budget and headcount planning |
| **lucas-finance** | Agency team costs and capacity planning |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-payroll** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-payroll:**

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
