---
name: conta-facturacao
description: Invoicing — e-Fatura AT, ATCUD, QR code, SAF-T, credit notes, series management
version: "1.0"
---

# CONTA-FACTURACAO: Facturação e Documentos Fiscais

## Activation Triggers

**PT:** factura, fatura, facturação, e-fatura, ATCUD, SAF-T, nota de crédito, série, QR code, recibo, documento fiscal, auto-facturação
**EN:** invoice, invoicing, e-fatura, ATCUD, SAF-T, credit note, receipt, tax document, billing, self-billing, QR code

## Context

Portuguese invoicing is governed by the Código do IVA and DL 28/2019. All invoices must be issued through AT-certified software, include ATCUD (unique document code), QR code, and be reported via SAF-T (PT) monthly or communicated in real-time. Non-compliance carries fines from €375 to €18,750.

## Workflow

### Step 1 — Document Types

| Code | Type (PT) | Type (EN) | When Used |
|------|-----------|-----------|-----------|
| FT | Factura | Invoice | Standard sale |
| FS | Factura Simplificada | Simplified Invoice | Sale ≤ €100 (goods) or ≤ €1000 (services to non-taxable) |
| FR | Factura-Recibo | Invoice-Receipt | Invoice + immediate payment |
| NC | Nota de Crédito | Credit Note | Correction, return, discount |
| ND | Nota de Débito | Debit Note | Additional charges |
| RC | Recibo | Receipt | Payment confirmation |
| GT | Guia de Transporte | Transport Document | Goods in transit |
| OR | Orçamento | Quotation | Non-fiscal, informational |
| FP | Factura Proforma | Proforma Invoice | Non-fiscal, informational |

### Step 2 — Mandatory Invoice Fields

Every FT/FS/FR must include:

| Field | Requirement |
|-------|-------------|
| NIF emitente | Issuer tax number |
| NIF adquirente | Buyer tax number (mandatory if B2B or >€1000) |
| Nome e morada | Name and address of both parties |
| Data de emissão | Issue date |
| Tipo e série | Document type + series (e.g., FT 2026/A) |
| ATCUD | Unique code: [validation_code]-[sequential_number] |
| QR Code | Machine-readable fiscal data |
| Descrição | Description of goods/services |
| Quantidade e preço | Quantity and unit price |
| Taxa IVA | VAT rate(s) applied |
| Base tributável | Taxable base per rate |
| Motivo isenção | If exempt: legal basis (e.g., Art.º 9.º CIVA) |
| Total IVA | Total VAT amount |
| Total documento | Grand total |

### Step 3 — ATCUD Generation

```
ATCUD = [Código de Validação AT]-[Número Sequencial]
```

1. Register document series at Portal das Finanças
2. AT returns a validation code per series
3. Each document gets: validation_code + "-" + sequential_number
4. Example: `ABCD1234-42` (42nd document in this series)

**Series format:** `[TYPE] [YEAR]/[SERIES_LETTER]` → e.g., `FT 2026/A`

### Step 4 — QR Code Content

The QR code encodes (separated by `*`):

```
A:[NIF emitente]*B:[NIF adquirente]*C:[País]*D:[Tipo]*
E:[Estado]*F:[Data]*G:[ID documento]*H:[ATCUD]*
I1:[Base isenta]*I2:[Base reduzida]*I3:[IVA reduzida]*
I4:[Base intermédia]*I5:[IVA intermédia]*
I6:[Base normal]*I7:[IVA normal]*I8:[Imposto selo]*
N:[Total IVA]*O:[Total documento]*Q:[4 chars hash]*R:[Certificado SW]
```

### Step 5 — SAF-T (PT) Reporting

| Obligation | Frequency | Deadline |
|-----------|-----------|----------|
| SAF-T mensal (comunicação facturas) | Monthly | 5th of following month |
| SAF-T anual (contabilidade) | Annual | With IES (15 July) |
| SAF-T on demand | AT inspection | Immediate |

**SAF-T file validation:** Use AT's validation tool before submission.

### Step 6 — Credit Note Rules

A credit note (NC) must:
1. Reference the original invoice (FT number and date)
2. State the reason for correction
3. Use the same IVA rate as the original
4. Be issued in the same series type (NC series)
5. Reduce IVA liquidado proportionally

```
# Credit note entry
D  721   Prestações Serviços  €500.00
D  2413  IVA Liquidado        €115.00
C  211x  Cliente              €615.00
```

### Step 7 — IVA Rates on Invoices

| Rate | Name | Applies to |
|------|------|------------|
| 23% | Normal | Most goods and services |
| 13% | Intermédia | Food/bev (restaurants), agricultural inputs |
| 6% | Reduzida | Essential food, books, pharma, hotel stays |
| 0% | Isenta | Exports, health, education, financial services (Art.º 9.º) |

**Azores/Madeira reduced rates:** 16%/9%/4% and 22%/12%/5% respectively.

## Commands

| Command | Description |
|---------|-------------|
| `conta-fact:criar <tipo>` | Create invoice/credit note |
| `conta-fact:serie <tipo> <ano>` | Register new document series |
| `conta-fact:atcud <serie>` | Generate ATCUD for next document |
| `conta-fact:qr <factura_id>` | Generate QR code data |
| `conta-fact:saft <periodo>` | Generate SAF-T monthly extract |
| `conta-fact:validar <factura>` | Validate invoice compliance |
| `conta-fact:nc <factura_ref>` | Create credit note for invoice |
| `conta-fact:listar <filtro>` | List documents by period/client |

## Output Template

```yaml
invoice:
  type: "FT"
  series: "FT 2026/A"
  number: 42
  atcud: "ABCD1234-42"
  date: "2026-04-27"
  issuer:
    nif: "123456789"
    name: "D.A.R.I.O. Lda"
  buyer:
    nif: "987654321"
    name: "Cliente XYZ, S.A."
  lines:
    - description: "Desenvolvimento website"
      quantity: 1
      unit_price: 5000.00
      vat_rate: 23
      vat_amount: 1150.00
      total: 6150.00
  totals:
    taxable_base: 5000.00
    total_vat: 1150.00
    grand_total: 6150.00
  qr_code: "A:123456789*B:987654321*..."
  saft_status: "communicated"
```

## Red Flags

- Invoice without ATCUD (mandatory since Jan 2023)
- Missing QR code on fiscal documents
- SAF-T not submitted by 5th of month (fine: €200-€2,500)
- Credit note without reference to original invoice
- Incorrect IVA rate for the goods/services sold
- Missing exemption reason when IVA = 0%
- Sequential numbering gap in a series (AT audit trigger)
- NIF not validated (non-existent or inactive taxpayer)
- Factura simplificada issued above €100 threshold for goods
- Auto-facturação without prior written agreement

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-lancamentos** | Each invoice generates a journal entry |
| **conta-iva** | Invoice IVA feeds periodic declarations |
| **conta-conciliacao** | Payments matched to invoices |
| **conta-ap** | Supplier invoices enter AP workflow |
| **conta-irc** | Revenue from invoices feeds IRC computation |
| **conta-relatorios** | Invoice totals in financial statements |
| **conta-encerramento** | All invoices must be issued before year-end close |
| **lucas-finance** | Agency invoicing with correct fiscal compliance |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-facturacao** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-facturacao:**

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
