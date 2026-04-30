---
name: conta-consolidacao
description: Group consolidation — intercompany elimination, currency translation, minorities, equity method
version: "1.0"
---

# CONTA-CONSOLIDACAO: Consolidação de Contas de Grupo

## Activation Triggers

**PT:** consolidação, contas consolidadas, grupo, eliminações, intercompany, participações, subsidiária, associada, minority, método integral, método equivalência patrimonial
**EN:** consolidation, group accounts, intercompany elimination, subsidiary, associate, minority interest, equity method, full consolidation, currency translation

## Context

Group consolidation in Portugal follows NCRF 15 (Investimentos em Subsidiárias e Consolidação) and NCRF 13 (Investimentos em Associadas), aligned with IFRS 10, IAS 27, and IAS 28. Groups must consolidate when a parent controls (>50% voting rights or de facto control) one or more subsidiaries. Exemptions exist for small groups under SNC.

## Workflow

### Step 1 — Determine Consolidation Scope

| Participation | Level | Method |
|---------------|-------|--------|
| > 50% (control) | Subsidiary | Full consolidation (método integral) |
| 20-50% (significant influence) | Associate | Equity method (método equivalência patrimonial) |
| Joint control | Joint venture | Proportional or equity method |
| < 20% (no influence) | Financial investment | Cost or fair value |

**Exemptions from consolidation (NCRF 15):**
- Small groups (2 of 3: assets ≤€7.5M, revenue ≤€15M, employees ≤250 — on consolidated basis)
- Intermediate parent exempted if ultimate parent consolidates

### Step 2 — Consolidation Preparation

| Task | Description |
|------|-------------|
| Unify accounting policies | All entities must use same policies |
| Unify reporting dates | Max 3-month difference from parent |
| Translate foreign currencies | Closing rate for balance, avg rate for DR |
| Identify intercompany | All intra-group transactions and balances |
| Determine goodwill/gain | At acquisition date |

### Step 3 — Full Consolidation Process

```
1. Aggregate: Add all parent + subsidiary assets, liabilities, revenue, expenses
2. Eliminate investment vs equity:
   D  51   Capital (subsidiary)          €XXX,XXX
   D  55   Reservas (subsidiary)          €XX,XXX
   D  56   Res. Transitados (subs.)       €XX,XXX
   D  441  Goodwill (if positive)         €XX,XXX
   C  41x  Investimento financeiro       €XXX,XXX
   C  5x   Interesses minoritários        €XX,XXX

3. Eliminate intercompany balances:
   D  22x  Fornecedores (subs.)          €XX,XXX
   C  21x  Clientes (parent)             €XX,XXX

4. Eliminate intercompany revenue/expense:
   D  71x  Vendas (parent)               €XX,XXX
   C  61x  CMVMC (subsidiary)            €XX,XXX

5. Eliminate unrealized profits:
   D  71x  Vendas intra-grupo             €X,XXX
   C  3xx  Inventários (buyer)             €X,XXX
   (margin on unsold inventory)

6. Eliminate intercompany dividends:
   D  78x  Rendimentos participações       €X,XXX
   C  56   Res. Transitados (subs.)        €X,XXX

7. Calculate and allocate minority interests
8. Test goodwill for impairment
```

### Step 4 — Equity Method (Associates)

```
# Initial recognition
D  411   Investimentos Associadas     €100,000
C  12xx  Bank                         €100,000

# Share of profit (30% associate with €50,000 profit)
D  411   Investimentos Associadas      €15,000
C  785   Rendim. Equivalência Patrim.  €15,000

# Share of dividend received
D  12xx  Bank                          €6,000
C  411   Investimentos Associadas      €6,000
```

### Step 5 — Foreign Currency Translation (IAS 21 / NCRF 23)

| Item | Rate | Where Difference Goes |
|------|------|----------------------|
| Assets and liabilities | Closing rate (year-end) | Equity (reservas conversão) |
| Revenue and expenses | Average rate (period) | Equity (reservas conversão) |
| Equity items | Historical rate | n/a |
| Goodwill | Closing rate | Equity (reservas conversão) |

```
# Translation difference
D/C  5xx  Reservas de Conversão   €XX,XXX
C/D  Various accounts             €XX,XXX
```

### Step 6 — Consolidation Adjustments Schedule

| Adjustment | Reference | Recurring |
|------------|-----------|-----------|
| Investment elimination | Step 3.2 | Annual (updated) |
| Intercompany balances | Step 3.3 | Every period |
| Intercompany P&L | Step 3.4 | Every period |
| Unrealized profit stock | Step 3.5 | Every period |
| Unrealized profit assets | Similar to 3.5 | Until asset sold/depreciated |
| Dividends | Step 3.6 | When declared |
| Goodwill impairment | Step 3.8 | Annual test |
| Currency translation | Step 5 | Every period |
| Minority interests | Step 3.7 | Every period |

### Step 7 — Consolidated Financial Statements

Must present:
- Balanço consolidado
- DR consolidada
- DACP consolidada
- Demonstração fluxos caixa consolidada
- Anexo consolidado (including basis of consolidation, entity list, policies)

## Commands

| Command | Description |
|---------|-------------|
| `conta-cons:perimetro` | Define consolidation perimeter |
| `conta-cons:intercompany <periodo>` | Identify intercompany transactions |
| `conta-cons:eliminar <tipo>` | Process elimination entries |
| `conta-cons:goodwill <subsidiaria>` | Calculate/test goodwill |
| `conta-cons:mep <associada>` | Apply equity method |
| `conta-cons:cambio <moeda> <periodo>` | Currency translation |
| `conta-cons:consolidar <periodo>` | Full consolidation run |
| `conta-cons:minoritarios` | Calculate minority interests |

## Output Template

```yaml
consolidation:
  parent: "Grupo XYZ, SGPS"
  period: "2025-12"
  perimeter:
    subsidiaries:
      - name: "ABC, Lda"
        participation: 80%
        method: full
      - name: "DEF, S.A."
        participation: 100%
        method: full
    associates:
      - name: "GHI, Lda"
        participation: 30%
        method: equity
  eliminations:
    intercompany_balances: 125000.00
    intercompany_revenue: 340000.00
    unrealized_profit: 15000.00
    dividends: 20000.00
  goodwill:
    gross: 50000.00
    impairment: 5000.00
    net: 45000.00
  minority_interests:
    equity: 35000.00
    profit: 8000.00
  consolidated_result: 185000.00
```

## Red Flags

- Subsidiary omitted from consolidation without valid exemption
- Intercompany balances not fully eliminating (difference indicates error)
- Unrealized profit on intra-group inventory not eliminated
- Goodwill not tested for impairment annually
- Different accounting policies across group entities
- Reporting dates misaligned beyond 3 months
- Minority interests incorrectly calculated
- Currency translation differences not going to equity
- Equity method not updated for associate's current year result
- Transfer pricing not at arm's length within group

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | Group chart of accounts alignment |
| **conta-relatorios** | Consolidated financial statements |
| **conta-ativos** | Intercompany asset transfers and unrealized profit |
| **conta-irc** | Group tax considerations, transfer pricing |
| **conta-auditoria** | Consolidated audit requirements |
| **conta-encerramento** | Group year-end close procedures |
| **conta-orcamento** | Consolidated budget |
| **conta-lancamentos** | Consolidation adjustment entries |
