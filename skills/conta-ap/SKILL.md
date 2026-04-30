---
name: conta-ap
description: Accounts payable — 3-way match, payment scheduling, aging analysis, supplier management
version: "1.0"
---

# CONTA-AP: Contas a Pagar (Accounts Payable)

## Activation Triggers

**PT:** contas a pagar, fornecedores, pagamento, vencimento, aging, dívida, factura fornecedor, aprovação pagamento, conta 22
**EN:** accounts payable, AP, supplier payment, vendor invoice, 3-way match, payment run, aging report, payables

## Context

Accounts payable in the SNC framework uses conta 22 (Fornecedores) and sub-accounts. Portuguese AP processes must ensure proper IVA deduction (only deductible IVA from correctly issued invoices), comply with late payment legislation (DL 62/2013 — max 60 days for commercial transactions), and maintain auditable approval workflows.

## Workflow

### Step 1 — Invoice Receipt and Registration

| Check | Requirement |
|-------|-------------|
| NIF emitente | Valid and active supplier NIF |
| ATCUD + QR | Present on invoice |
| Description | Matches order/contract |
| Amounts | Arithmetically correct |
| IVA | Correct rate, correctly calculated |
| Date | Within acceptable period |

**Registration entry:**
```
D  62xx  FSE / 61xx CMVMC    €1,000.00
D  2411  IVA Suportado         €230.00
C  221x  Fornecedor          €1,230.00
```

### Step 2 — 3-Way Match

| Document | Source | Matches |
|----------|--------|---------|
| Purchase Order (PO) | Internal system | Description, quantities, prices |
| Goods Receipt (GR) | Warehouse / service confirmation | Quantities received |
| Invoice (FT) | Supplier | Amounts match PO and GR |

**Match outcomes:**
- **Full match:** Approve for payment
- **Partial match:** Flag discrepancy, hold for resolution
- **No match:** Reject, return to supplier or investigate

### Step 3 — Approval Workflow

| Amount Range | Approver |
|-------------|----------|
| ≤ €500 | Department manager |
| €501 - €5,000 | Finance director |
| > €5,000 | CEO / Board |
| Recurring (rent, utilities) | Pre-approved standing authority |

### Step 4 — Payment Scheduling

**Payment terms common in Portugal:**

| Term | Description |
|------|-------------|
| Pronto pagamento | Immediate / on receipt |
| 30 dias | Net 30 from invoice date |
| 30 dias fim do mês | End of month + 30 days |
| 60 dias | Net 60 (legal max for commercial) |
| Prestações | Installment plan |

**Payment methods:**
- Transferência bancária (bank transfer) — most common
- Débito direto (direct debit)
- Cheque (declining usage)
- MBWay / Multibanco (smaller amounts)
- Letra / Livrança (bills of exchange — larger amounts)

### Step 5 — Payment Execution

```
# Payment to supplier
D  221x  Fornecedor          €1,230.00
C  12xx  Depósitos à Ordem   €1,230.00
```

**Early payment discount:**
```
D  221x  Fornecedor          €1,230.00
C  12xx  Depósitos à Ordem   €1,205.40
C  785   Descontos Obtidos      €24.60  (2% discount)
```

### Step 6 — Aging Analysis

| Bucket | Days | Status |
|--------|------|--------|
| Current | 0-30 | Normal |
| 30 days | 31-60 | Monitor |
| 60 days | 61-90 | Overdue (exceeds legal limit) |
| 90 days | 91-120 | Escalation |
| 120+ days | >120 | Dispute / legal action |

**Late payment interest:** ECB reference rate + 8% (commercial, per DL 62/2013)

### Step 7 — Period-End Procedures

1. Accrue for goods/services received but not yet invoiced
2. Review aging — escalate overdue items
3. Confirm supplier balances (circularização)
4. Ensure all IVA suportado is correctly classified (dedutível vs não dedutível)

```
# Accrual for uninvoiced receipt
D  62xx  FSE               €2,000.00
D  2411  IVA Suportado       €460.00
C  2722  Credores Acrésc.  €2,460.00
```

## Commands

| Command | Description |
|---------|-------------|
| `conta-ap:registar <factura>` | Register supplier invoice |
| `conta-ap:match <po> <gr> <ft>` | Run 3-way match |
| `conta-ap:aprovar <factura_id>` | Approve for payment |
| `conta-ap:agendar <periodo>` | Generate payment schedule |
| `conta-ap:pagar <fornecedor>` | Execute payment run |
| `conta-ap:aging [data]` | Generate aging report |
| `conta-ap:saldo <fornecedor>` | Check supplier balance |
| `conta-ap:circularizar` | Generate balance confirmation letters |

## Output Template

```yaml
ap_aging:
  date: "2026-04-30"
  currency: EUR
  suppliers:
    - nif: "123456789"
      name: "Fornecedor ABC"
      current: 3500.00
      days_30: 1200.00
      days_60: 0.00
      days_90: 0.00
      days_120_plus: 0.00
      total: 4700.00
  totals:
    current: 45000.00
    days_30: 12000.00
    days_60: 3500.00
    days_90: 800.00
    days_120_plus: 200.00
    grand_total: 61500.00
  overdue_percentage: 7.3
  avg_days_to_pay: 34
```

## Red Flags

- Invoices exceeding 60-day payment term (DL 62/2013 violation)
- IVA deducted from invoices without valid ATCUD
- 3-way match override without documented justification
- Duplicate invoice registration (same supplier + number + date)
- Supplier NIF inactive or non-existent at AT
- Payments to suppliers not matching registered invoices
- Growing aging over 90 days without dispute resolution
- Accruals not reversed when actual invoice arrives
- Missing withholding tax on services from non-residents (Art.º 94.º CIRC)
- Payments above €1,000 in cash (legal restriction)

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-lancamentos** | AP entries posted to ledger |
| **conta-conciliacao** | Payments reconciled with bank |
| **conta-facturacao** | Supplier invoices validated |
| **conta-iva** | IVA suportado feeds IVA declaration |
| **conta-tesouraria** | Payment schedule feeds cash flow forecast |
| **conta-irc** | Expenses feed IRC deductibility analysis |
| **conta-encerramento** | AP accruals and confirmations at year-end |
| **lucas-finance** | Agency supplier and freelancer payments |
