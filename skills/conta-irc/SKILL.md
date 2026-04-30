---
name: conta-irc
description: IRC computation — Modelo 22, derrama, PEC, tributação autónoma, tax planning, deductions
version: "1.0"
---

# CONTA-IRC: Imposto sobre o Rendimento das Pessoas Colectivas

## Activation Triggers

**PT:** IRC, imposto rendimento, modelo 22, derrama, PEC, pagamento especial por conta, tributação autónoma, lucro tributável, prejuízos fiscais, benefícios fiscais, RFAI, SIFIDE
**EN:** corporate tax, CIT, model 22, surcharge, advance payment, autonomous taxation, taxable profit, tax losses, tax benefits, R&D credit

## Context

IRC is the Portuguese corporate income tax, governed by the Código do IRC (CIRC). Standard rate: 21%. Entities must compute taxable profit from accounting profit via tax adjustments, file Modelo 22 annually (by 31 May for Dec year-end), and make advance payments (PPC) throughout the year.

## Workflow

### Step 1 — IRC Rate Structure

| Component | Rate | Applies to |
|-----------|------|------------|
| IRC base | 21% | Taxable profit (general) |
| IRC PME | 17% | First €50,000 (SME qualifying) |
| Derrama municipal | 0-1.5% | Taxable profit (municipality rate) |
| Derrama estadual | 3% | €1.5M - €7.5M |
| Derrama estadual | 5% | €7.5M - €35M |
| Derrama estadual | 9% | > €35M |

**Effective rate for SME (first €50,000):** 17% + derrama ≈ 18-18.5%
**Effective rate general:** 21% + derrama ≈ 22-22.5%

### Step 2 — Taxable Profit Computation

```
Resultado Líquido do Período (Accounting Profit)    €XXX,XXX
+ Variações patrimoniais positivas                   +€XX,XXX
- Variações patrimoniais negativas                   -€XX,XXX
+ Acréscimos (add-backs)                             +€XX,XXX
- Deduções (deductions)                              -€XX,XXX
= Lucro Tributável (antes de prejuízos)              €XXX,XXX
- Prejuízos fiscais deduzidos (max 70% LT)           -€XX,XXX
= Matéria Colectável                                 €XXX,XXX
```

### Step 3 — Common Tax Adjustments

**Acréscimos (add-backs / increases):**

| Item | CIRC Reference | Typical |
|------|---------------|---------|
| Multas e coimas | Art.º 23.º-A n.º 1 e) | 100% add-back |
| Despesas não documentadas | Art.º 23.º-A n.º 1 b) | 100% + TA 50% |
| Depreciações acima limites | Art.º 34.º | Excess add-back |
| Provisões não aceites | Art.º 39.º | Non-tax provisions |
| Realizações de utilidade social excess | Art.º 43.º | Above limits |
| Viaturas acima €62,500 (TA) | Art.º 34.º n.º 1 e) | Excess depreciation |
| IVA não dedutível (certos casos) | | Per analysis |

**Deduções (deductions):**

| Item | CIRC Reference | Typical |
|------|---------------|---------|
| Dividendos recebidos (participation exemption) | Art.º 51.º | 100% if >10% held 1yr |
| Mais-valias reinvestidas | Art.º 48.º | 50% if reinvested |
| Benefícios fiscais (RFAI, SIFIDE, DLRR) | EBF | Per scheme |
| Donativos (mecenato) | Art.º 62.º EBF | 120-140% |

### Step 4 — Tributação Autónoma (Autonomous Taxation)

| Expense | Rate | Condition |
|---------|------|-----------|
| Despesas não documentadas | 50% (70% if exempt) | Art.º 88.º n.º 1 |
| Despesas representação | 10% | Art.º 88.º n.º 7 |
| Ajudas de custo + km não facturadas | 5% | Art.º 88.º n.º 9 |
| Viaturas ligeiras (custo <€27,500) | 10% | Art.º 88.º n.º 3 |
| Viaturas ligeiras (€27,500-€35,000) | 27.5% | Art.º 88.º n.º 3 |
| Viaturas ligeiras (>€35,000) | 35% | Art.º 88.º n.º 3 |
| Viaturas híbridas plug-in | 5% / 10% / 17.5% | 50% reduction |
| Viaturas elétricas | 0% / 10% | Exempt or reduced |
| Bónus e prémios gestores (>€27,500) | 35% | Art.º 88.º n.º 13 |
| Lucros distribuídos a entidades isentas | 23% | Art.º 88.º n.º 11 |

**All TA rates increase by 10pp if entity has prejuízo fiscal.**

### Step 5 — Advance Payments

| Payment | Calculation | Deadline |
|---------|-------------|----------|
| PPC (Pagamento por Conta) | Based on prior year IRC | Jul, Sep, Dec (15th) |
| PEC (Pagamento Especial por Conta) | 1% of turnover (min €850, max €70,000) | Mar (31st) or Mar+Oct split |
| Retenções na fonte (withholding received) | 25% on services to entities | As withheld |

**PPC formula:** (IRC prior year - withholdings) × 80% (if turnover ≤€500K) or 95% / 3 installments

### Step 6 — Modelo 22 Filing

| Field Group | Content |
|-------------|---------|
| Quadro 07 | Taxable profit computation (adjustments) |
| Quadro 09 | Matéria colectável |
| Quadro 10 | IRC calculation |
| Quadro 11 | Tributação autónoma |
| Quadro 12 | Tax credits and deductions |
| Quadro 13 | IRC payable/refundable |

**Deadline:** 31 May (for Dec year-end entities) or 5th month after year-end.

### Step 7 — Tax Planning Opportunities

| Strategy | Benefit | Reference |
|----------|---------|-----------|
| RFAI (invest. productive) | 10-25% tax credit | Art.º 22.º EBF |
| SIFIDE II (R&D) | 32.5-50% tax credit | Art.º 35.º-41.º CFI |
| DLRR (retained earnings) | 10% tax credit | Art.º 27.º-34.º CFI |
| Mecenato (donations) | 120-140% deduction | Art.º 62.º EBF |
| Interior regime | IRC 12.5% first €50K | Art.º 41.º-B EBF |
| Regime PME | 17% first €50K | Art.º 87.º n.º 2 CIRC |

## Commands

| Command | Description |
|---------|-------------|
| `conta-irc:calcular <ano>` | Compute IRC for fiscal year |
| `conta-irc:modelo22 <ano>` | Generate Modelo 22 data |
| `conta-irc:ta <ano>` | Calculate tributação autónoma |
| `conta-irc:ppc <ano>` | Calculate advance payments |
| `conta-irc:pec <ano>` | Calculate PEC |
| `conta-irc:prejuizos` | Track fiscal loss carryforward |
| `conta-irc:beneficios <tipo>` | Simulate tax benefit |
| `conta-irc:calendario` | IRC filing/payment calendar |

## Output Template

```yaml
irc_computation:
  fiscal_year: 2025
  accounting_profit: 150000.00
  adjustments:
    add_backs: 18500.00
    deductions: 5000.00
  taxable_profit: 163500.00
  loss_deduction: 0.00
  taxable_base: 163500.00
  irc:
    sme_rate: { base: 50000, rate: 0.17, tax: 8500.00 }
    general_rate: { base: 113500, rate: 0.21, tax: 23835.00 }
    derrama_municipal: { rate: 0.015, tax: 2452.50 }
    total_irc: 34787.50
  autonomous_tax: 2800.00
  total_tax: 37587.50
  advance_payments:
    ppc_paid: 28000.00
    withholdings: 3500.00
    pec_paid: 850.00
  net_payable: 5237.50
  effective_rate: 25.1%
  filing_deadline: "2026-05-31"
```

## Red Flags

- Modelo 22 not filed by 31 May (fine: €150-€3,750)
- Tributação autónoma not calculated (often forgotten, always due)
- PPC payments missed (interest + penalties)
- Fiscal losses not tracked or exceeding 70% deduction limit
- Despesas não documentadas not identified (50% TA + non-deductible)
- Vehicle costs above thresholds without correct TA rate
- RFAI/SIFIDE benefits claimed without proper documentation
- Participation exemption applied without meeting holding requirements
- Transfer pricing adjustments needed for related-party transactions
- Derrama municipal rate not verified for entity's municipality

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | Tax accounts (241x, 2621, 8121) |
| **conta-lancamentos** | Tax provision and payment entries |
| **conta-iva** | Non-deductible IVA impacts IRC base |
| **conta-relatorios** | Tax expense in DR, tax liability in balance |
| **conta-ativos** | Depreciation limits affect taxable profit |
| **conta-encerramento** | IRC computation is part of year-end close |
| **conta-tesouraria** | Tax payment dates in cash flow |
| **conta-orcamento** | Tax budget and effective rate planning |
| **lucas-finance** | Agency IRC computation and planning |
