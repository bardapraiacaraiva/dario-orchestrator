---
name: conta-relatorios
description: Financial statements SNC — balancete, demonstração resultados, balanço, fluxos de caixa, anexo
version: "1.0"
---

# CONTA-RELATORIOS: Demonstrações Financeiras SNC

## Activation Triggers

**PT:** demonstrações financeiras, balancete, balanço, demonstração de resultados, DR, fluxos de caixa, anexo, IES, relatório gestão, NCRF, rácios financeiros
**EN:** financial statements, trial balance, balance sheet, income statement, P&L, cash flow statement, notes, financial ratios, annual accounts

## Context

Under SNC, entities must prepare annual financial statements per NCRF 1 (Estrutura e Conteúdo das Demonstrações Financeiras). The full set includes: Balanço, DR (por naturezas ou funções), DACP, Demonstração de Fluxos de Caixa, and Anexo. These feed into the IES (Informação Empresarial Simplificada) filed annually. Micro-entities and small entities have reduced requirements.

## Workflow

### Step 1 — Statement Requirements by Entity Type

| Entity Type | Balanço | DR | Fluxos Caixa | DACP | Anexo |
|-------------|---------|----|-----------|----|------|
| General (SNC full) | Full | Full (naturezas + funções) | Full | Full | Full |
| Pequena entidade (NCRF-PE) | Reduced | Reduced (naturezas) | Optional | Optional | Reduced |
| Micro-entidade (NC-ME) | Simplified | Simplified | Not required | Not required | Simplified |

### Step 2 — Balancete (Trial Balance)

The balancete is the working document from which all statements derive.

| Column | Content |
|--------|---------|
| Código | Account code |
| Descrição | Account name |
| Saldo anterior | Opening balance |
| Débitos período | Period debits |
| Créditos período | Period credits |
| Saldo final | Closing balance |
| Saldo devedor | Debit balance |
| Saldo credor | Credit balance |

**Validation:** Total debit balances = Total credit balances

### Step 3 — Demonstração de Resultados (por Naturezas)

```
Vendas e serviços prestados (71+72)          €XXX,XXX
Subsídios à exploração (751)                  +€XX,XXX
Ganhos/perdas subsidiárias (78/68)            ±€XX,XXX
Variação inventários produção (73)            ±€XX,XXX
Trabalhos para a própria entidade (74)        +€XX,XXX
────────────────────────────────────────────
CMVMC (61)                                    -€XX,XXX
FSE (62)                                      -€XX,XXX
Gastos com pessoal (63)                       -€XX,XXX
Imparidades (65)                              -€XX,XXX
Provisões (67)                                -€XX,XXX
Outros gastos (68)                            -€XX,XXX
────────────────────────────────────────────
EBITDA                                         €XX,XXX
Depreciações e amortizações (64)              -€XX,XXX
────────────────────────────────────────────
EBIT (Resultado Operacional)                   €XX,XXX
Juros suportados (6911)                       -€X,XXX
Juros obtidos (7911)                          +€X,XXX
────────────────────────────────────────────
RAI (Resultado Antes de Impostos)              €XX,XXX
Imposto sobre o rendimento (8121)             -€X,XXX
────────────────────────────────────────────
Resultado Líquido do Período (RLP)             €XX,XXX
```

### Step 4 — Balanço (Balance Sheet)

```
ATIVO
  Ativo não corrente:
    Ativos fixos tangíveis (43)             €XXX,XXX
    Ativos intangíveis (44)                  €XX,XXX
    Investimentos financeiros (41)           €XX,XXX
    Goodwill (44)                            €XX,XXX
  Ativo corrente:
    Inventários (3x)                         €XX,XXX
    Clientes (21)                           €XXX,XXX
    Estado (24 - a receber)                  €XX,XXX
    Outras contas a receber (26/27)          €XX,XXX
    Diferimentos (281)                       €XX,XXX
    Caixa e depósitos (11/12)               €XX,XXX
────────────────────────────────────────────
TOTAL ATIVO                                €XXX,XXX

CAPITAL PRÓPRIO
    Capital (51)                             €XX,XXX
    Reservas legais (551)                    €XX,XXX
    Outras reservas (552)                    €XX,XXX
    Resultados transitados (56)             ±€XX,XXX
    Resultado líquido período (818)         ±€XX,XXX
────────────────────────────────────────────
TOTAL CAPITAL PRÓPRIO                       €XX,XXX

PASSIVO
  Passivo não corrente:
    Financiamentos obtidos LP (25)          €XX,XXX
    Provisões (29)                           €XX,XXX
  Passivo corrente:
    Fornecedores (22)                       €XX,XXX
    Estado (24 - a pagar)                    €XX,XXX
    Financiamentos CP (25)                   €XX,XXX
    Outras contas a pagar (26/27)            €XX,XXX
    Diferimentos (282)                       €XX,XXX
────────────────────────────────────────────
TOTAL PASSIVO                              €XXX,XXX
────────────────────────────────────────────
TOTAL CP + PASSIVO                         €XXX,XXX  (= TOTAL ATIVO)
```

### Step 5 — Key Financial Ratios

| Ratio | Formula | Benchmark |
|-------|---------|-----------|
| Liquidez geral | AC / PC | > 1.2 |
| Liquidez reduzida | (AC - Inv) / PC | > 1.0 |
| Autonomia financeira | CP / Ativo | > 30% |
| Solvabilidade | CP / Passivo | > 50% |
| Endividamento | Passivo / Ativo | < 70% |
| ROE | RLP / CP | > 15% |
| ROA | RLP / Ativo | > 5% |
| Margem líquida | RLP / Vendas | Industry-dependent |
| EBITDA margin | EBITDA / Vendas | > 10% |
| Prazo médio recebimento | (Clientes / Vendas) × 365 | < 60 days |
| Prazo médio pagamento | (Fornecedores / Compras) × 365 | 30-60 days |

### Step 6 — IES Filing

| Component | Content |
|-----------|---------|
| Anexo A | Balanço + DR + DACP |
| Anexo I | Fluxos de Caixa |
| Anexo L | IVA (operations) |
| Anexo Q | Informação estatística |
| Anexo R | Rendimentos / IRC |

**Deadline:** 15 July (for Dec year-end entities).

## Commands

| Command | Description |
|---------|-------------|
| `conta-rel:balancete <periodo>` | Generate trial balance |
| `conta-rel:dr <periodo>` | Generate income statement |
| `conta-rel:balanco <data>` | Generate balance sheet |
| `conta-rel:fluxos <periodo>` | Generate cash flow statement |
| `conta-rel:racios <periodo>` | Calculate financial ratios |
| `conta-rel:ies <ano>` | Prepare IES data |
| `conta-rel:comparativo <p1> <p2>` | Period comparison |
| `conta-rel:consolidado` | Consolidated statements |

## Output Template

```yaml
financial_statements:
  entity: "D.A.R.I.O. Lda"
  period: "2025-01 to 2025-12"
  income_statement:
    revenue: 450000.00
    cogs: 120000.00
    gross_margin: 330000.00
    fse: 85000.00
    personnel: 150000.00
    ebitda: 95000.00
    depreciation: 15000.00
    ebit: 80000.00
    financial_result: -5000.00
    rai: 75000.00
    irc: 16500.00
    net_income: 58500.00
  balance_sheet:
    total_assets: 380000.00
    equity: 175000.00
    total_liabilities: 205000.00
    balanced: true
  ratios:
    current_ratio: 1.45
    financial_autonomy: 46.1%
    roe: 33.4%
    ebitda_margin: 21.1%
  ies_deadline: "2026-07-15"
```

## Red Flags

- Balance sheet not balanced (Ativo != CP + Passivo)
- Trial balance with debit != credit totals
- Negative equity (capital próprio negativo) — potential insolvency
- IES not filed by 15 July
- DR showing CMVMC > Revenue (negative gross margin)
- Missing impairment tests on receivables
- Depreciation not charged for the period
- Period-end accruals and deferrals missing
- Comparative figures not presented
- Micro-entity using full NCRF statements unnecessarily

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | Account structure defines statement layout |
| **conta-lancamentos** | All entries feed into trial balance |
| **conta-encerramento** | Year-end entries finalize statements |
| **conta-irc** | Tax expense line in DR |
| **conta-iva** | IVA data for IES Anexo L |
| **conta-consolidacao** | Group-level statements |
| **conta-orcamento** | Budget vs actual comparison |
| **conta-custos** | Cost analysis by function |
| **conta-tesouraria** | Cash flow statement data |
| **lucas-finance** | Agency monthly P&L and reporting |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-relatorios** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-relatorios:**

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
