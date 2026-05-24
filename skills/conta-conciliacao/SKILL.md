---
name: conta-conciliacao
description: Bank reconciliation — multi-bank, auto-matching, discrepancy resolution, periodic close
version: "1.0"
---

# CONTA-CONCILIACAO: Conciliação Bancária

## Activation Triggers

**PT:** conciliação, conciliação bancária, reconciliação, extracto bancário, banco, diferenças, pendentes, saldo bancário
**EN:** bank reconciliation, bank statement, reconcile, discrepancy, unmatched, clearing, multi-bank, bank balance

## Context

Bank reconciliation ensures that the accounting ledger (conta 12 sub-accounts) matches the bank statement. In Portugal, entities must reconcile at least monthly. With multiple banks, each conta 12x sub-account must be reconciled independently. Discrepancies may arise from timing differences, bank fees, interest, or errors.

## Workflow

### Step 1 — Gather Inputs

| Source | Content | Format |
|--------|---------|--------|
| Bank statement | Movements + final balance | PDF, OFX, CSV, SEPA XML |
| Accounting ledger | Conta 12x movements + balance | Trial balance extract |
| Previous reconciliation | Outstanding items carried forward | Reconciliation report |

### Step 2 — Match Transactions

**Auto-match rules (in priority order):**

1. **Exact match:** Same date, same amount, same reference
2. **Amount match:** Same amount within ±3 days tolerance
3. **Reference match:** Same document/reference number, any date
4. **Aggregate match:** Sum of ledger entries = single bank line (or vice versa)
5. **Manual match:** Remaining items reviewed manually

**Match status codes:**

| Status | Meaning |
|--------|---------|
| `MATCHED` | Ledger line = Bank line, confirmed |
| `PENDING_BANK` | In ledger, not yet on statement (e.g., cheque emitido) |
| `PENDING_LEDGER` | On statement, not yet in ledger (e.g., bank fee, interest) |
| `DISCREPANCY` | Amount differs, needs investigation |
| `DUPLICATE` | Possible double entry |

### Step 3 — Reconciliation Calculation

```
Saldo Contabilístico (Ledger Balance)           €XX,XXX.XX
+ Movimentos no extracto não registados           +€X,XXX.XX
  (bank fees, interest, direct debits)
- Movimentos registados não no extracto           -€X,XXX.XX
  (cheques pendentes, transferências em trânsito)
= Saldo do Extracto Bancário (Bank Balance)     €XX,XXX.XX
```

If the result does not equal the bank statement balance, there is an **unresolved discrepancy**.

### Step 4 — Resolve Discrepancies

| Issue | Resolution |
|-------|------------|
| Bank fee not recorded | Create entry: D 6817 / C 12x |
| Interest received not recorded | Create entry: D 12x / C 7881 |
| Direct debit not recorded | Create entry: D 22x or 62x / C 12x |
| Cheque not yet cashed | Mark as PENDING_BANK, carry forward |
| Transfer in transit | Mark as PENDING_BANK, carry forward |
| Amount difference | Investigate, correct ledger or flag bank error |
| Duplicate entry | Reverse the duplicate |
| Unidentified bank movement | Request clarification, park in conta 2689 |

### Step 5 — Process Unrecorded Items

For each PENDING_LEDGER item, create the journal entry:

```
# Bank fee
D  6817  Gastos Bancários    €15.00
C  12xx  Depósitos à Ordem   €15.00

# Interest earned
D  12xx  Depósitos à Ordem    €8.50
C  7881  Juros Obtidos        €8.50

# Imposto de Selo on interest (4%)
D  6812  Imposto de Selo      €0.34
C  12xx  Depósitos à Ordem    €0.34
```

### Step 6 — Sign Off and Archive

1. Generate reconciliation report
2. Sign off by responsible person
3. Archive with bank statement copy
4. Carry forward outstanding items to next period

## Commands

| Command | Description |
|---------|-------------|
| `conta-conc:importar <banco> <ficheiro>` | Import bank statement |
| `conta-conc:reconciliar <banco> <periodo>` | Run auto-reconciliation |
| `conta-conc:pendentes <banco>` | List unmatched items |
| `conta-conc:resolver <item_id> <accao>` | Resolve a discrepancy |
| `conta-conc:relatorio <banco> <periodo>` | Generate reconciliation report |
| `conta-conc:multi` | Reconcile all banks for period |
| `conta-conc:historico <banco>` | View reconciliation history |

## Output Template

```yaml
reconciliation:
  bank: "Millennium BCP"
  account: "121 - BCP Conta Corrente"
  period: "2026-04"
  statement_date: "2026-04-30"
  ledger_balance: 45230.50
  adjustments:
    pending_bank:
      - ref: "CHQ-4521"
        amount: -1500.00
        description: "Cheque pendente"
    pending_ledger:
      - ref: "COMISS-ABR"
        amount: -22.50
        description: "Comissão manutenção conta"
  adjusted_ledger: 43708.00
  bank_balance: 43708.00
  reconciled: true
  items_matched: 142
  items_pending: 3
  discrepancies: 0
  signed_by: ""
  date_signed: ""
```

## Red Flags

- Reconciliation not performed for 2+ months
- Growing list of unresolved PENDING items month over month
- Bank balance differs from ledger by round amounts (potential missing entry)
- Unidentified movements parked in 2689 for over 30 days
- Duplicate entries inflating both sides equally (hidden error)
- Cheques outstanding for more than 6 months (may need write-off)
- Imposto de Selo on bank interest not recorded
- Foreign currency accounts not reconciled at month-end exchange rate
- Reconciliation signed off without resolving all discrepancies

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-lancamentos** | Creates entries for unrecorded bank items |
| **conta-plano** | Uses conta 12x sub-accounts per bank |
| **conta-tesouraria** | Reconciled balances feed cash flow analysis |
| **conta-ap** | Payment confirmations matched to supplier payments |
| **conta-facturacao** | Customer payments matched to invoices |
| **conta-encerramento** | All banks must be reconciled before year-end close |
| **lucas-finance** | Agency bank accounts reconciled monthly |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-conciliacao** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-conciliacao:**

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
