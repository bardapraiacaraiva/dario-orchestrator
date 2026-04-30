---
name: conta-plano
description: Chart of Accounts SNC — structure, NCRF mapping, IFRS alignment, account creation and validation
version: "1.0"
---

# CONTA-PLANO: Plano de Contas SNC

## Activation Triggers

**PT:** plano de contas, SNC, conta, criar conta, classe, NCRF, normalização, código de conta, plano contas
**EN:** chart of accounts, account code, SNC chart, NCRF mapping, IFRS alignment, account structure, ledger accounts

## Context

The Portuguese Chart of Accounts follows the **Sistema de Normalização Contabilística (SNC)**, regulated by Decreto-Lei 158/2009 and updated by DL 98/2015. It defines 8 classes (1-8) plus class 0 for off-balance-sheet items. Each entity must adopt the SNC code structure while customizing sub-accounts for its operations.

## Workflow

### Step 1 — Identify Entity Type and Applicable Framework

| Entity Type | Framework | Reference |
|-------------|-----------|-----------|
| General entities | SNC / NCRF | DL 158/2009 |
| Micro-entities | NC-ME | DL 36-A/2011 |
| Small entities | NCRF-PE | Portaria 220/2015 |
| Listed / large groups | IFRS (EU-adopted) | Reg. 1606/2002 |

### Step 2 — SNC Class Structure

| Class | Name (PT) | Name (EN) | Nature |
|-------|-----------|-----------|--------|
| 1 | Meios Financeiros Líquidos | Cash & Cash Equivalents | Asset |
| 2 | Contas a Receber e a Pagar | Receivables & Payables | Asset/Liability |
| 3 | Inventários e Activos Biológicos | Inventories & Biological Assets | Asset |
| 4 | Investimentos | Investments / Fixed Assets | Asset |
| 5 | Capital, Reservas e Resultados Transitados | Equity | Equity |
| 6 | Gastos | Expenses | Expense |
| 7 | Rendimentos | Revenue | Revenue |
| 8 | Resultados | Net Income | Result |
| 0 | Contas Extrapatrimoniais | Off-Balance Sheet | Memo |

### Step 3 — Account Code Convention

```
X.Y.Z.W.V
│ │ │ │ └─ 5th level: analytical detail (entity-specific)
│ │ │ └─── 4th level: sub-sub-account (entity-specific)
│ │ └───── 3rd level: sub-account (SNC standard)
│ └─────── 2nd level: account (SNC standard)
└───────── 1st level: class (SNC mandatory)
```

**Example:** 6.2.1.1.001 = Class 6 (Gastos) > 62 (FSE) > 621 (Subcontratos) > 6211 (Subcontratos nacionais) > 001 (Fornecedor X)

### Step 4 — Common Account Mappings

| SNC Code | SNC Name | IFRS Equivalent |
|----------|----------|-----------------|
| 11 | Caixa | Cash on hand |
| 12 | Depósitos à ordem | Bank deposits (current) |
| 21 | Clientes | Trade receivables (IFRS 15) |
| 22 | Fornecedores | Trade payables |
| 24 | Estado e Outros Entes Públicos | Tax assets/liabilities |
| 2411 | IVA Suportado | Input VAT |
| 2412 | IVA Dedutível | Deductible VAT |
| 2413 | IVA Liquidado | Output VAT |
| 2414 | IVA Regularizações | VAT adjustments |
| 2415 | IVA Apuramento | VAT settlement |
| 241x | IVA a Pagar / a Recuperar | VAT payable/receivable |
| 43 | Ativos Fixos Tangíveis | PP&E (IAS 16) |
| 44 | Ativos Intangíveis | Intangibles (IAS 38) |
| 51 | Capital | Share capital |
| 56 | Resultados Transitados | Retained earnings |
| 61 | CMVMC | Cost of goods sold |
| 62 | FSE | External services |
| 63 | Gastos com Pessoal | Employee costs |
| 71 | Vendas | Revenue from sales |
| 72 | Prestações de Serviços | Service revenue |

### Step 5 — Validate New Account

Before creating a new account, verify:

1. Does the account respect the SNC mandatory structure (1st-3rd levels)?
2. Is the account code unique within the entity?
3. Is the nature (debit/credit) consistent with the class?
4. Is there a corresponding NCRF for the transaction type?
5. Does the account have the correct IVA linkage (if applicable)?

## Commands

| Command | Description |
|---------|-------------|
| `conta-plano:listar [classe]` | List all accounts in a class |
| `conta-plano:criar <codigo> <nome>` | Create new sub-account |
| `conta-plano:mapear <snc> <ifrs>` | Map SNC code to IFRS |
| `conta-plano:validar <codigo>` | Validate account code structure |
| `conta-plano:pesquisar <termo>` | Search accounts by keyword |
| `conta-plano:exportar` | Export full chart to CSV/YAML |

## Output Template

```yaml
account:
  code: "62.1.1.001"
  name: "Subcontratos - Fornecedor X"
  class: 6 - Gastos
  nature: Debit
  ncrf: NCRF 1 - Estrutura e Conteúdo das DF
  ifrs_map: IAS 1 - External services expense
  iva_regime: Sujeito / Dedutível
  status: Active
  created: YYYY-MM-DD
  notes: ""
```

## Red Flags

- Account code does not follow SNC mandatory hierarchy (levels 1-3)
- Mixing debit-nature accounts in credit-nature classes (e.g., revenue in class 6)
- Creating accounts 2411-2418 without proper IVA flow configuration
- Using class 0 accounts in trial balance totals
- Micro-entity using full SNC chart instead of NC-ME simplified
- Missing conta 2415 (IVA Apuramento) in IVA flow setup
- Duplicate account codes at entity-specific levels (4th/5th)

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-lancamentos** | Uses account codes for journal entries |
| **conta-iva** | IVA sub-accounts (241x) feed IVA declarations |
| **conta-relatorios** | Chart structure defines financial statement layout |
| **conta-ativos** | Class 43/44 accounts for fixed asset register |
| **conta-consolidacao** | Group chart alignment for consolidation mapping |
| **conta-encerramento** | Year-end close validates all accounts balanced |
| **conta-custos** | Cost center sub-accounts under class 6/7 |
| **lucas-finance** | Agency-specific sub-accounts for client billing |
