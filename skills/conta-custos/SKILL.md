---
name: conta-custos
description: Cost accounting — cost centers, ABC costing, margins, break-even, profitability analysis
version: "1.0"
---

# CONTA-CUSTOS: Contabilidade Analítica e de Custos

## Activation Triggers

**PT:** contabilidade analítica, custos, centro de custo, margem, rentabilidade, ponto crítico, break-even, ABC, custeio, custo unitário, imputação
**EN:** cost accounting, cost center, margin, profitability, break-even, ABC costing, cost allocation, unit cost, management accounting

## Context

Cost accounting (contabilidade analítica) is not mandatory under SNC but is essential for management decision-making. It uses class 9 (internal/analytical accounts) or parallel tracking within the SNC chart. Portuguese entities, especially service companies and agencies, need cost accounting to understand project profitability, client margins, and service pricing.

## Workflow

### Step 1 — Cost Classification

| Classification | Categories |
|----------------|-----------|
| By nature (SNC) | CMVMC (61), FSE (62), Pessoal (63), Deprec. (64) |
| By behavior | Fixed, Variable, Semi-variable |
| By traceability | Direct, Indirect (overhead) |
| By function | Production, Admin, Commercial, Financial |
| By relevance | Relevant (for decisions), Sunk (ignore for decisions) |

### Step 2 — Cost Center Structure

| Level | Example | Purpose |
|-------|---------|---------|
| Division | DARIO / DIVA / LUCAS | P&L by business unit |
| Department | Marketing / Dev / Admin | Cost control |
| Project | Client-A-Website | Project profitability |
| Service line | SEO / Webdev / Consulting | Service margin analysis |
| Employee | Analyst-1 | Utilization and cost-per-hour |

**Chart of cost centers (example):**
```
CC-100  Administração Geral
CC-200  Comercial / Vendas
CC-300  Marketing
CC-400  Desenvolvimento Web
CC-410  SEO
CC-420  Design
CC-500  Suporte / Operações
CC-900  Imputação Geral (overhead pool)
```

### Step 3 — Cost Allocation Methods

**Direct allocation:** Costs directly traceable to a cost center (e.g., designer salary to CC-420).

**Indirect allocation (overhead):**

| Overhead | Allocation Base | Justification |
|----------|----------------|---------------|
| Rent | m2 per department | Space used |
| IT infrastructure | Headcount | Users served |
| Electricity | m2 or kWh metered | Consumption |
| Admin salaries | Revenue or headcount | Support provided |
| Depreciation (shared) | Usage hours or headcount | Asset usage |
| Insurance | Revenue or asset value | Risk basis |

### Step 4 — Activity-Based Costing (ABC)

```
Step 1: Identify activities
  → Client acquisition, project management, development, testing, support

Step 2: Assign costs to activities
  → Salaries, tools, overhead → activity pools

Step 3: Identify cost drivers
  → Hours worked, proposals sent, projects managed, tickets resolved

Step 4: Calculate cost per activity unit
  → Activity cost / Total driver units = Cost per unit

Step 5: Assign to cost objects (clients, projects)
  → Cost per unit × Units consumed = Total cost allocated
```

| Activity | Cost Pool | Driver | Rate |
|----------|-----------|--------|------|
| Proposal writing | €15,000/yr | Proposals | €300/proposal |
| Project management | €40,000/yr | Projects | €2,000/project |
| Development | €120,000/yr | Hours | €75/hour |
| Testing/QA | €30,000/yr | Hours | €50/hour |
| Client support | €25,000/yr | Tickets | €25/ticket |

### Step 5 — Margin Analysis

```
Revenue (project/client/service)        €XX,XXX
- Direct costs (materials, subcontracts) -€X,XXX
= Margem Bruta (Gross Margin)            €XX,XXX   (% = GM/Rev)

- Direct personnel (hours × rate)        -€X,XXX
= Margem Contribuição (Contrib. Margin)  €XX,XXX   (% = CM/Rev)

- Allocated overhead                     -€X,XXX
= Margem Líquida (Net Margin)            €X,XXX    (% = NM/Rev)
```

**Target margins for agencies (reference):**

| Metric | Healthy Range |
|--------|---------------|
| Gross margin (after directs) | 60-80% |
| Contribution margin (after labor) | 40-60% |
| Net margin (after overhead) | 15-25% |
| EBITDA margin | 15-20% |

### Step 6 — Break-Even Analysis

```
Break-Even Point (€) = Fixed Costs / Contribution Margin %

Example:
  Fixed Costs (annual): €180,000
  Avg. Contribution Margin: 55%
  Break-Even Revenue: €180,000 / 0.55 = €327,273

Break-Even Point (units):
  Fixed Costs / (Price - Variable Cost per Unit)
  €180,000 / (€5,000 - €2,250) = 65.5 projects/year
```

**Margin of Safety:**
```
Margin of Safety = (Actual Revenue - Break-Even Revenue) / Actual Revenue
  = (€500,000 - €327,273) / €500,000 = 34.5%
```

### Step 7 — Profitability Reports

| Report | Frequency | Audience |
|--------|-----------|---------|
| Project P&L | Per project close | PM + Finance |
| Client profitability | Quarterly | CEO + Sales |
| Service line margins | Monthly | Department heads |
| Cost center report | Monthly | CC managers |
| Break-even dashboard | Monthly | CEO + Finance |
| Employee utilization | Weekly/Monthly | Operations |

**Employee utilization (for service companies):**
```
Utilization Rate = Billable Hours / Available Hours
  Target: 70-80% (agencies)
  
Cost per Hour = (Salary + Encargos + Overhead allocation) / Available Hours
Revenue per Hour = Billable Revenue / Billable Hours
Margin per Hour = Revenue per Hour - Cost per Hour
```

## Commands

| Command | Description |
|---------|-------------|
| `conta-custos:cc <centro>` | Cost center report |
| `conta-custos:projeto <id>` | Project profitability |
| `conta-custos:cliente <id>` | Client profitability |
| `conta-custos:margem <servico>` | Service line margin |
| `conta-custos:breakeven` | Break-even analysis |
| `conta-custos:abc` | ABC costing calculation |
| `conta-custos:utilizacao <periodo>` | Employee utilization report |
| `conta-custos:imputar <periodo>` | Run overhead allocation |

## Output Template

```yaml
cost_analysis:
  period: "2026-Q1"
  by_service_line:
    web_development:
      revenue: 85000.00
      direct_costs: 12000.00
      labor_cost: 38000.00
      overhead: 15000.00
      net_margin: 20000.00
      margin_pct: 23.5%
    seo:
      revenue: 45000.00
      direct_costs: 5000.00
      labor_cost: 18000.00
      overhead: 8000.00
      net_margin: 14000.00
      margin_pct: 31.1%
  break_even:
    monthly_fixed: 15000.00
    avg_contribution_margin: 57.2%
    break_even_monthly: 26224.00
    margin_of_safety: 38.5%
  utilization:
    avg_rate: 72%
    cost_per_hour: 42.50
    revenue_per_hour: 85.00
    margin_per_hour: 42.50
```

## Red Flags

- No cost accounting despite having multiple service lines
- Overhead allocated using single arbitrary base
- Project closed without profitability analysis
- Break-even point above current revenue trajectory
- Utilization below 60% sustained (unprofitable team)
- Client with negative net margin retained without strategic justification
- Cost centers not aligned with organizational structure
- Subcontractor costs not tracked per project
- Pricing decisions made without cost data
- High-margin services underinvested while low-margin grow

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | Class 9 accounts or sub-account structure |
| **conta-lancamentos** | Cost allocation entries |
| **conta-relatorios** | DR by function (requires cost data) |
| **conta-orcamento** | Budget by cost center |
| **conta-payroll** | Personnel costs per cost center |
| **conta-ativos** | Depreciation allocation to cost centers |
| **conta-tesouraria** | Cash flow by business unit |
| **lucas-finance** | Agency profitability and pricing |
| **dario-pricing-calculator** | Service pricing based on cost data |
| **dario-financial-model** | Financial modelling with cost structure |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-custos** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-custos:**

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
