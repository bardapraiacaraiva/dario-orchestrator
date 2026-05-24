---
name: conta-ss
description: Social Security — employer/employee contributions, DRI, independent workers, special regimes
version: "1.0"
---

# CONTA-SS: Segurança Social

## Activation Triggers

**PT:** segurança social, SS, contribuições, TSU, taxa social única, DRI, trabalhador independente, entidade empregadora, enquadramento, base incidência
**EN:** social security, contributions, employer contributions, employee contributions, independent worker, DRI, social insurance

## Context

The Portuguese Social Security system is governed by the Código Contributivo (Lei 110/2009). Entities must register workers, calculate monthly contributions, submit declarations (DRI — Declaração de Remunerações por Internet), and pay by the 20th of the following month. Rates differ by worker category and regime.

## Workflow

### Step 1 — Contribution Rates

**Regime Geral (Dependent Workers):**

| Component | Rate |
|-----------|------|
| Entidade Empregadora (employer) | 23.75% |
| Trabalhador (employee) | 11.00% |
| Total TSU | 34.75% |

**Special Rates:**

| Category | Employer | Employee | Total |
|----------|----------|----------|-------|
| Membros órgãos estatutários (MOE) | 20.30% | 9.30% | 29.60% |
| Trabalhadores domésticos | 18.90% | 9.40% | 28.30% |
| Primeiro emprego | 23.75% | 11.00% | 34.75% (incentivos possíveis) |
| Estágios IEFP | 0% | 0% | Isento |
| Contratos muito curto prazo | 26.10% | 11.00% | 37.10% |

**Trabalhadores Independentes (Freelancers):**

| Situation | Rate |
|-----------|------|
| TI sem contabilidade organizada | 21.4% (on rendimento relevante) |
| TI com contabilidade organizada | 25.2% (on rendimento relevante) |
| Entidade contratante (>50% rendimento) | 7% (on valor serviços) |
| Entidade contratante (≥80% rendimento) | 10% (on valor serviços) |

### Step 2 — Base de Incidência (Contribution Base)

**Dependent workers — what's included:**

| Component | Included? |
|-----------|-----------|
| Remuneração base | Yes |
| Subsídio de Natal | Yes |
| Subsídio de férias | Yes |
| Diuturnidades | Yes |
| Comissões | Yes |
| Prémios regulares | Yes |
| Subsídio de alimentação (até limite) | No (exempt up to €6.00/day cash, €10.20 card) |
| Subsídio alimentação (excesso) | Yes |
| Ajudas de custo (dentro limites) | No |
| Horas extraordinárias | Yes |
| Abono para falhas | No (up to 5% base salary) |

**Cap:** There is no general contribution cap in Portugal (unlike some EU countries).

### Step 3 — Monthly Calculation

```
Employee: Maria Silva
Base salary:                    €1,500.00
Subsídio alimentação (22 days): €132.00 (€6.00/day, exempt)
Overtime:                       €150.00
─────────────────────────────────────────
Contribution base:              €1,650.00 (salary + overtime)

Employee SS (11%):              €181.50
Employer SS (23.75%):           €391.88
Total SS:                       €573.38
```

### Step 4 — Independent Workers (Regime TI)

**Rendimento relevante calculation (quarterly):**

```
Rendimento Relevante = Rendimento Bruto × Coeficiente
  - Prestação serviços: × 70%
  - Produção/venda bens: × 20%
  - Restauração/alojamento: × 20%

Base mensal = Rendimento Relevante / 3

Mínimo: 1 IAS = €522.50 (2025)
Máximo: 12 IAS = €6,270.00
```

**Quarterly declaration:** TI must declare income to SS quarterly (Jan/Apr/Jul/Oct).

### Step 5 — DRI (Declaração de Remunerações)

| Field | Content |
|-------|---------|
| NISS trabalhador | SS number |
| NIF trabalhador | Tax number |
| Remuneração base | Monthly base |
| Dias de trabalho | Days worked |
| Modalidade | Full-time / part-time |
| Taxa aplicável | Applicable rate |

**Deadline:** By 10th of the following month (same as DMR for IRS).

### Step 6 — Payment

| Obligation | Deadline | Method |
|------------|----------|--------|
| DRI submission | 10th of following month | Portal SS Directa |
| SS payment (employer share) | 20th of following month | MB/Transfer/DD |
| SS payment (employee share) | 20th of following month | Withheld and paid by employer |
| TI quarterly declaration | Jan 31, Apr 30, Jul 31, Oct 31 | Portal SS Directa |
| TI monthly payment | 20th of following month | MB/Transfer |

### Step 7 — Journal Entries

```
# Monthly payroll SS booking
D  635   Encargos sobre Remunerações  €391.88  (employer 23.75%)
C  245   Contrib. SS a Pagar          €573.38  (employer + employee)
# Employee portion already withheld from salary (contra 2312)

# Payment to SS
D  245   Contrib. SS a Pagar          €573.38
C  12xx  Depósitos à Ordem            €573.38
```

## Commands

| Command | Description |
|---------|-------------|
| `conta-ss:calcular <trabalhador>` | Calculate SS for worker |
| `conta-ss:dri <periodo>` | Generate DRI data |
| `conta-ss:ti <rendimento>` | Calculate independent worker SS |
| `conta-ss:contratante <fornecedor>` | Check if entity is "entidade contratante" |
| `conta-ss:base <componentes>` | Determine contribution base |
| `conta-ss:calendario` | SS obligations calendar |
| `conta-ss:incentivos` | List available SS exemptions/reductions |
| `conta-ss:saldo` | Current SS balance (payable) |

## Output Template

```yaml
social_security:
  period: "2026-04"
  dependent_workers:
    headcount: 5
    total_base: 9500.00
    employer_rate: 23.75%
    employee_rate: 11.00%
    employer_contribution: 2256.25
    employee_contribution: 1045.00
    total_contribution: 3301.25
  moe:
    headcount: 1
    total_base: 3000.00
    employer_contribution: 609.00
    employee_contribution: 279.00
  independent_workers:
    contratante_7: 0.00
    contratante_10: 0.00
  totals:
    total_payable: 4189.25
    dri_deadline: "2026-05-10"
    payment_deadline: "2026-05-20"
```

## Red Flags

- DRI not submitted by 10th (fines apply)
- SS payment after 20th (daily interest 3% + penalty)
- Employer 23.75% not applied (using wrong rate)
- MOE at general rate instead of 20.30%/9.30%
- Subsidio alimentação excess not included in base
- Independent worker quarterly declaration missed
- "Entidade contratante" obligation not identified (>50% of TI income)
- Worker not registered (enquadramento) before start date
- Base de incidência not including all mandatory components
- SS contributions not reconciled with DRI submitted values
- Contratos muito curto prazo at standard rate instead of 26.10%

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-payroll** | SS calculated as part of payroll processing |
| **conta-lancamentos** | SS entries (635/245) posted to ledger |
| **conta-irs** | DMR includes both IRS and SS data |
| **conta-tesouraria** | SS payment date in cash flow forecast |
| **conta-irc** | SS costs are deductible for IRC |
| **conta-relatorios** | Personnel costs in DR, SS payable in balance |
| **conta-encerramento** | Year-end SS reconciliation |
| **lucas-finance** | Agency SS for employees and freelancer obligations |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-ss** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-ss:**

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
