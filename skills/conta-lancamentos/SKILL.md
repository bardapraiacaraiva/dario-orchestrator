---
name: conta-lancamentos
description: Journal entries — double-entry bookkeeping, recurring entries, accruals, adjustments, reversals
version: "1.0"
---

# CONTA-LANCAMENTOS: Lançamentos Contabilísticos

## Activation Triggers

**PT:** lançamento, diário, razão, débito, crédito, partida dobrada, acréscimo, diferimento, regularização, estorno, lançamento recorrente
**EN:** journal entry, double entry, debit, credit, accrual, deferral, adjustment, reversal, recurring entry, posting

## Context

All journal entries in Portugal must follow the double-entry principle under SNC. Each entry must be supported by a valid document (factura, recibo, extracto bancário, etc.), properly dated, and traceable to source. The AT (Autoridade Tributária) requires entries to be stored in certified software for entities above the micro threshold.

## Workflow

### Step 1 — Classify the Transaction

| Transaction Type | Journal | Frequency |
|-----------------|---------|-----------|
| Sales / Revenue | Diário de Vendas | Per invoice |
| Purchases / Expenses | Diário de Compras | Per invoice |
| Bank movements | Diário de Bancos | Per statement |
| Cash movements | Diário de Caixa | Daily/per event |
| Payroll | Diário de Pessoal | Monthly |
| Adjustments | Diário de Operações Diversas | As needed |
| Opening/Closing | Diário de Abertura/Encerramento | Annual |

### Step 2 — Construct the Entry

Every entry MUST satisfy: **Total Debits = Total Credits**

```
Date: YYYY-MM-DD
Journal: [Diário]
Document: [Tipo + Número]
Description: [Natureza da operação]

  Debit   Account    Amount     Description
  ─────   ───────    ──────     ───────────
  D       XXXX       €XXX.XX    [line detail]
  D       XXXX       €XXX.XX    [line detail]
  C       XXXX       €XXX.XX    [line detail]
  C       XXXX       €XXX.XX    [line detail]
```

### Step 3 — Common Entry Patterns

**Sale with IVA (23%):**
```
D  211x  Cliente         €1,230.00
C  721   Prest. Serviços €1,000.00
C  2413  IVA Liquidado     €230.00
```

**Purchase with IVA (23%):**
```
D  62xx  FSE             €1,000.00
D  2411  IVA Suportado     €230.00
C  221x  Fornecedor      €1,230.00
```

**Payroll (simplified):**
```
D  631   Remunerações    €2,000.00
D  635   Encargos s/ Rem   €475.00  (23.75% SS patronal)
C  2451  Pessoal - Rem.   €1,560.00 (líquido)
C  2421  Retenção IRS       €220.00
C  245   SS a Pagar         €695.00 (11% + 23.75%)
```

**Depreciation:**
```
D  642   Gastos Deprec.    €500.00
C  438   Deprec. Acumul.   €500.00
```

**Accrual (revenue earned, not yet invoiced):**
```
D  2721  Devedores Acrésc. €5,000.00
C  72xx  Prestações Serv.  €5,000.00
```

**Deferral (expense paid, not yet consumed):**
```
D  281   Gastos Diferidos   €1,200.00
C  12xx  Depósitos à Ordem  €1,200.00
```

**Monthly reversal of deferral:**
```
D  62xx  FSE                  €100.00
C  281   Gastos Diferidos     €100.00
```

### Step 4 — Validate the Entry

| Check | Rule |
|-------|------|
| Balance | Sum(Debit) = Sum(Credit) |
| Date | Within the fiscal period |
| Document | Valid reference attached |
| Account | Exists in chart, correct nature |
| IVA | Correct rate applied, correct IVA accounts |
| Period | Not posting to closed period |
| Sequence | Document numbering sequential |

### Step 5 — Post and Lock

1. Save entry in draft status
2. Review for accuracy
3. Post to general ledger (razão)
4. Lock period when all entries reviewed

## Commands

| Command | Description |
|---------|-------------|
| `conta-lanc:criar` | Create new journal entry |
| `conta-lanc:modelo <tipo>` | Generate template for entry type |
| `conta-lanc:validar <entry>` | Validate debit=credit and accounts |
| `conta-lanc:recorrente <entry> <freq>` | Set up recurring entry |
| `conta-lanc:estornar <entry_id>` | Reverse an entry |
| `conta-lanc:acrescimo <tipo>` | Create accrual entry |
| `conta-lanc:diferimento <tipo>` | Create deferral entry |
| `conta-lanc:pesquisar <filtro>` | Search entries by account/date/amount |

## Output Template

```yaml
journal_entry:
  id: "OD-2026-0042"
  date: "2026-04-27"
  journal: "Operações Diversas"
  document_ref: "FT 2026/123"
  description: "Venda de serviços de consultoria"
  lines:
    - type: D
      account: "211"
      amount: 1230.00
      description: "Cliente XYZ"
    - type: C
      account: "721"
      amount: 1000.00
      description: "Prestação de serviços"
    - type: C
      account: "24131"
      amount: 230.00
      description: "IVA 23%"
  total_debit: 1230.00
  total_credit: 1230.00
  balanced: true
  status: posted
  period: "2026-04"
```

## Red Flags

- Entry not balanced (debits != credits)
- Posting to a closed period without reopening authorization
- Missing document reference (violates AT requirements)
- IVA account used without corresponding base amount
- Accruals not reversed in the correct subsequent period
- Recurring entries duplicated (double posting)
- Using conta 12 (bank) without matching bank statement line
- Adjustment entries without written justification
- Sequential numbering gaps in document series

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | Validates account codes exist and have correct nature |
| **conta-conciliacao** | Bank entries reconciled against statement |
| **conta-facturacao** | Invoice generates automatic sale entry |
| **conta-iva** | IVA lines feed periodic IVA declarations |
| **conta-payroll** | Payroll processing generates personnel entries |
| **conta-ativos** | Asset purchase/depreciation entries |
| **conta-encerramento** | Year-end adjustments and closing entries |
| **conta-relatorios** | Ledger balances feed financial statements |
