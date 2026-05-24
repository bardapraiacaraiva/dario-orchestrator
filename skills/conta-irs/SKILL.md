---
name: conta-irs
description: IRS withholding — categories A/B/E/F/G, freelancer retention, annual obligations, non-residents
version: "1.0"
---

# CONTA-IRS: Retenções na Fonte de IRS

## Activation Triggers

**PT:** IRS, retenção na fonte, categoria A, categoria B, trabalhador independente, recibos verdes, tabelas retenção, rendimentos, declaração modelo 10
**EN:** IRS withholding, personal income tax, category A, category B, freelancer, green receipts, withholding tables, income tax, non-resident withholding

## Context

Entities paying income to individuals must withhold IRS (Imposto sobre o Rendimento das Pessoas Singulares) at source. The withholding rate depends on the income category, amount, and taxpayer situation. Governed by CIRS (Código do IRS) and annual withholding tables published by Despacho ministerial.

## Workflow

### Step 1 — Income Categories and Withholding

| Category | Income Type | Withholding Method |
|----------|------------|-------------------|
| A | Dependent employment (salários) | Monthly tables (progressive) |
| B | Independent/freelance (recibos verdes) | Flat rate on gross |
| E | Capital income (dividendos, juros) | Flat rate 28% |
| F | Property income (rendas) | Flat rate 25% |
| G | Capital gains (mais-valias) | At source or declaration |
| H | Pensions | Monthly tables (specific) |

### Step 2 — Category A (Employment) Withholding

**Annual withholding tables** (published each year):

| Factor | Impact on Rate |
|--------|---------------|
| Gross monthly salary | Higher salary = higher marginal rate |
| Marital status (casado/solteiro) | Married = lower rate |
| Number of dependents | More dependents = lower rate |
| Holder type (único/dois titulares) | Single earner household = lower rate |
| Deficiência ≥ 60% | Reduced rate |

**Withholding entry (simplified):**
```
# Salary €2,000 gross, IRS 14.5%, SS 11%
D  631   Remunerações        €2,000.00
C  2421  Retenção IRS          €290.00
C  245   Contrib. SS           €220.00
C  2312  Pessoal - Rem. Líq  €1,490.00
```

**Subsidio de alimentação:** Exempt up to €6.00/day (cash) or €10.20/day (card). Excess is taxed as Cat. A.

### Step 3 — Category B (Freelancer) Withholding

**Standard rates (services to entities with contabilidade organizada):**

| Activity | Rate | Notes |
|----------|------|-------|
| Professional services (Art.º 151.º CIRS listed) | 25% | Default |
| Professional services (not listed) | 20% | Since 2024 |
| Comercial/industrial income | 11.5% | Specific activities |
| Services > €14,500/year by payer | Mandatory retention | Even if normally exempt |
| First year of activity | 50% reduction available | Optional |

**Exemption from withholding:** Freelancer earning ≤ €14,500 previous year AND not expecting more in current year can request exemption (Art.º 101.º-B n.º 1 a) CIRS).

**Entry for freelancer payment:**
```
# Service €1,000, retention 25%
D  62xx  FSE               €1,000.00
D  2411  IVA Suportado       €230.00  (if subject to IVA)
C  2421  Retenção IRS        €250.00
C  221x  Fornecedor          €980.00  (net + IVA - retention)
```

### Step 4 — Category E (Capital Income)

| Income | Rate | Notes |
|--------|------|-------|
| Dividendos (residentes) | 28% | On gross amount |
| Juros depósitos | 28% | Bank withholds |
| Royalties | 25% | At source |
| Non-resident dividends | 25% (or treaty rate) | Reduced by DTA |

### Step 5 — Category F (Property)

| Income | Rate | Notes |
|--------|------|-------|
| Rendas (tenant is entity) | 25% | Entity withholds |
| Rendas (tenant is individual) | No withholding | Landlord declares |
| Sublocação | 25% | On the sub-rent portion |

### Step 6 — Non-Resident Withholding

| Income | Rate | DTA Reduction |
|--------|------|---------------|
| Services (Cat. B) | 25% | Treaty rate |
| Dividends | 25% | Typically 10-15% |
| Interest | 25% | Typically 10-15% |
| Royalties | 25% | Typically 10% |
| Employment income | Tables Cat. A | Per treaty |

**Require:** NIF português or fiscal representative, proof of residence, DTA form (if applicable).

### Step 7 — Reporting Obligations

| Obligation | Frequency | Deadline |
|------------|-----------|----------|
| Guia de Retenções (payment to AT) | Monthly | By 20th of following month |
| DMR (Declaração Mensal de Remunerações) | Monthly | By 10th of following month |
| Modelo 10 (annual withholding summary) | Annual | By 25 February |
| Modelo 39 (capital income) | Annual | By end of February |
| Declaração de rendimentos pagos NR | Annual | Part of Modelo 30 |

## Commands

| Command | Description |
|---------|-------------|
| `conta-irs:retencao <categ> <montante>` | Calculate withholding |
| `conta-irs:tabela <ano>` | Show current withholding tables |
| `conta-irs:freelancer <nif> <montante>` | Process freelancer payment |
| `conta-irs:dmr <periodo>` | Generate DMR data |
| `conta-irs:modelo10 <ano>` | Generate Modelo 10 data |
| `conta-irs:nao-residente <tipo> <pais>` | Non-resident withholding |
| `conta-irs:guia <periodo>` | Generate payment guide |
| `conta-irs:calendario` | IRS obligations calendar |

## Output Template

```yaml
irs_withholding:
  period: "2026-04"
  category_a:
    employees: 5
    gross_salaries: 12500.00
    withholding_total: 2150.00
  category_b:
    freelancers: 3
    gross_services: 4500.00
    withholding_total: 1125.00
  category_e:
    capital_income: 0.00
    withholding_total: 0.00
  category_f:
    rent_paid: 1200.00
    withholding_total: 300.00
  total_withholding: 3575.00
  payment_deadline: "2026-05-20"
  dmr_deadline: "2026-05-10"
  guia_ref: "2026-04-IRS"
```

## Red Flags

- Retenção na fonte not delivered to AT by 20th (daily interest)
- DMR not submitted by 10th of following month
- Freelancer withholding at wrong rate (25% vs 20% vs 11.5%)
- Non-resident payment without checking DTA applicability
- Subsidio alimentação above exempt threshold not taxed
- Category B exemption applied without valid requirements
- Modelo 10 values not matching sum of monthly DMRs
- Withholding on dividends at incorrect rate
- Missing fiscal representative for non-resident payees
- Rent withholding not applied when tenant is entity

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-payroll** | Category A withholding from salary processing |
| **conta-ap** | Freelancer payments with withholding |
| **conta-lancamentos** | Withholding entries (2421 credit) |
| **conta-tesouraria** | Monthly withholding payment in cash flow |
| **conta-ss** | DMR includes both IRS and SS data |
| **conta-encerramento** | Year-end reconciliation of withholdings |
| **conta-irc** | Withholdings received reduce IRC payable |
| **lucas-finance** | Agency freelancer payment processing |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-irs** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-irs:**

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
