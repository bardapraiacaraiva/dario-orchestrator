---
name: conta-iva
description: IVA declarations — regime normal/simplificado, periodic returns, intra-EU, VIES, pro-rata, regularizations
version: "1.0"
---

# CONTA-IVA: Imposto sobre o Valor Acrescentado

## Activation Triggers

**PT:** IVA, imposto valor acrescentado, declaração periódica, regime normal, regime simplificado, IVA intracomunitário, VIES, pro-rata, isenção, liquidação, dedução, regularização
**EN:** VAT, value added tax, periodic return, VAT declaration, intra-community, reverse charge, VAT exemption, input VAT, output VAT, pro-rata, VIES

## Context

IVA (Value Added Tax) in Portugal is governed by the Código do IVA (CIVA), RITI (intra-EU regime), and CIRS/CIRC intersections. Entities must submit periodic declarations (monthly or quarterly) via Portal das Finanças. Key rates: 23% (normal), 13% (intermédia), 6% (reduzida). Azores and Madeira have lower rates.

## Workflow

### Step 1 — Determine IVA Regime

| Regime | Turnover Threshold | Filing | Payment |
|--------|-------------------|--------|---------|
| Normal mensal | > €650,000 annual | Monthly | By 10th of 2nd month after |
| Normal trimestral | ≤ €650,000 annual | Quarterly | By 15th of 2nd month after |
| Isenção Art.º 53.º | ≤ €15,000 annual (2025+) | No filing | No IVA charged |
| Regime forfetário (agriculture) | Special | Annual | Flat-rate compensation |

### Step 2 — IVA Account Flow (SNC)

```
2411 IVA Suportado          (Input VAT — all purchases)
  ↓ Classification
2412 IVA Dedutível          (Deductible portion)
2413 IVA Liquidado          (Output VAT — all sales)
  ↓ Apuramento
2415 IVA Apuramento         (Netting: 2413 - 2412)
  ↓ Result
2416 IVA a Pagar            (If output > input)
   or
2417 IVA a Recuperar        (If input > output)
2418 IVA Reembolsos Pedidos (Refund requested)
2414 IVA Regularizações     (Corrections, credit notes)
```

### Step 3 — IVA Rates Reference

| Rate | Continente | Açores | Madeira | Applies to |
|------|-----------|--------|---------|------------|
| Normal | 23% | 16% | 22% | Most goods/services |
| Intermédia | 13% | 9% | 12% | Restaurants, some food, agricultural inputs |
| Reduzida | 6% | 4% | 5% | Essential food, books, pharma, hotel, transport |
| Isenta | 0% | 0% | 0% | Art.º 9.º (health, education, finance, insurance) |

### Step 4 — Periodic Declaration (Declaração Periódica)

**Fields mapping to SNC accounts:**

| DP Field | Description | Source Account |
|----------|-------------|----------------|
| Campo 1-3 | Base tributável taxa normal | Sales at 23% |
| Campo 5-7 | Base tributável taxa intermédia | Sales at 13% |
| Campo 9-11 | Base tributável taxa reduzida | Sales at 6% |
| Campo 4/8/12 | IVA liquidado por taxa | 2413 sub-accounts |
| Campo 20-24 | IVA dedutível | 2412 sub-accounts |
| Campo 40 | IVA a pagar | 2416 |
| Campo 41 | IVA a recuperar / crédito | 2417 |

**Filing calendar:**

| Period | Deadline | Payment Deadline |
|--------|----------|-----------------|
| Monthly (Jan) | 10 Mar | 10 Mar |
| Monthly (Feb) | 10 Apr | 10 Apr |
| Quarterly (Q1) | 15 May | 15 May |
| Quarterly (Q2) | 15 Aug | 15 Aug |
| Quarterly (Q3) | 15 Nov | 15 Nov |
| Quarterly (Q4) | 15 Feb | 15 Feb |

### Step 5 — Intra-Community Operations (RITI)

**Aquisição Intracomunitária (purchase from EU):**
```
D  31xx/62xx  Compra           €10,000.00
D  2412      IVA Dedutível      €2,300.00  (auto-liquidação)
C  2413      IVA Liquidado      €2,300.00  (reverse charge)
C  221x      Fornecedor UE     €10,000.00
```

**Transmissão Intracomunitária (sale to EU with valid VIES):**
```
D  211x      Cliente UE        €10,000.00
C  71xx      Vendas            €10,000.00  (isenta Art.º 14.º RITI)
```
- Must validate buyer's VAT number on VIES before applying exemption
- Report in Declaração Recapitulativa (monthly if >€50,000/quarter)

### Step 6 — Special Situations

| Situation | Treatment |
|-----------|-----------|
| Pro-rata (mixed taxable/exempt) | Annual definitive %, provisional monthly |
| Autoconsumo | IVA liquidado on market value |
| Ofertas > €50 unit | IVA liquidado on cost |
| Créditos incobráveis | Regularize IVA after 24 months (Art.º 78.º-A) |
| Reverse charge (construction) | Art.º 2.º n.º 1 j) CIVA |
| Digital services B2C EU | OSS regime or local registration |

### Step 7 — Apuramento (Settlement)

Monthly/quarterly closing entry:
```
# Transfer deductible IVA
D  2415  IVA Apuramento       €X,XXX.XX
C  2412  IVA Dedutível        €X,XXX.XX

# Transfer output IVA
D  2413  IVA Liquidado        €Y,YYY.YY
C  2415  IVA Apuramento       €Y,YYY.YY

# If Y > X (IVA a pagar):
D  2415  IVA Apuramento       €Z,ZZZ.ZZ
C  2416  IVA a Pagar          €Z,ZZZ.ZZ

# If X > Y (IVA a recuperar):
D  2417  IVA a Recuperar      €Z,ZZZ.ZZ
C  2415  IVA Apuramento       €Z,ZZZ.ZZ
```

## Commands

| Command | Description |
|---------|-------------|
| `conta-iva:apurar <periodo>` | Calculate IVA for period |
| `conta-iva:dp <periodo>` | Generate Declaração Periódica data |
| `conta-iva:recapitulativa <periodo>` | Generate Declaração Recapitulativa |
| `conta-iva:vies <nif>` | Validate EU VAT number |
| `conta-iva:prorata <ano>` | Calculate definitive pro-rata |
| `conta-iva:regularizar <factura>` | Process IVA regularization |
| `conta-iva:calendario` | Show IVA filing/payment calendar |
| `conta-iva:saldo` | Current IVA position (pagar/recuperar) |

## Output Template

```yaml
iva_declaration:
  period: "2026-04"
  regime: "normal_mensal"
  filing_deadline: "2026-06-10"
  output_vat:
    normal_23: { base: 50000.00, iva: 11500.00 }
    intermedia_13: { base: 5000.00, iva: 650.00 }
    reduzida_6: { base: 2000.00, iva: 120.00 }
    total_liquidado: 12270.00
  input_vat:
    deductible: 8500.00
    non_deductible: 1200.00
    total_suportado: 9700.00
  intra_community:
    acquisitions: 3000.00
    transmissions: 7000.00
  settlement:
    iva_a_pagar: 3770.00
    previous_credit: 0.00
    net_payable: 3770.00
```

## Red Flags

- Declaração Periódica not submitted by deadline (fine: €150-€3,750)
- IVA deducted on non-deductible expenses (vehicles >€62,500, entertainment, personal)
- Intra-community sale without VIES validation
- Pro-rata not recalculated at year-end with definitive ratio
- Credit notes not reducing IVA liquidado in the correct period
- IVA suportado remaining in 2411 without classification to 2412
- Reverse charge not applied on construction subcontracts
- Art.º 53.º entity accidentally charging IVA
- Regularização of bad debts without meeting 24-month requirement
- OSS regime not activated for B2C digital services to EU consumers

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | IVA accounts (241x) structure |
| **conta-lancamentos** | Every entry with IVA generates 241x lines |
| **conta-facturacao** | Invoice IVA rates feed declarations |
| **conta-irc** | Non-deductible IVA impacts IRC computation |
| **conta-tesouraria** | IVA payment dates in cash flow forecast |
| **conta-encerramento** | Year-end IVA pro-rata adjustment |
| **conta-relatorios** | IVA balances in balance sheet |
| **lucas-finance** | Agency IVA compliance and calendar |
