---
name: conta-ativos
description: Fixed assets — depreciation rates, register, acquisition, disposal, revaluation, impairment
version: "1.0"
---

# CONTA-ATIVOS: Ativos Fixos Tangíveis e Intangíveis

## Activation Triggers

**PT:** ativo fixo, imobilizado, depreciação, amortização, registo ativos, mapa depreciações, abate, alienação, reavaliação, imparidade, vida útil, DR 25/2009
**EN:** fixed asset, PP&E, depreciation, amortization, asset register, disposal, revaluation, impairment, useful life, capital expenditure

## Context

Fixed assets under SNC follow NCRF 7 (Ativos Fixos Tangíveis) and NCRF 6 (Ativos Intangíveis), aligned with IAS 16 and IAS 38. Tax depreciation rates are set by Decreto Regulamentar 25/2009. Assets must be recorded at cost, depreciated systematically, tested for impairment, and tracked in a formal register.

## Workflow

### Step 1 — Asset Classification (SNC Accounts)

| Account | Category | Example |
|---------|----------|---------|
| 431 | Terrenos e recursos naturais | Land |
| 432 | Edifícios e outras construções | Buildings, improvements |
| 433 | Equipamento básico | Machinery, production equipment |
| 434 | Equipamento de transporte | Vehicles |
| 435 | Equipamento administrativo | Computers, furniture, office equipment |
| 436 | Equipamentos biológicos | Livestock, plantations |
| 437 | Outros ativos fixos tangíveis | Other |
| 441 | Goodwill | Business combinations |
| 442 | Projetos de desenvolvimento | R&D (development phase) |
| 443 | Programas de computador | Software |
| 444 | Propriedade industrial | Patents, trademarks |
| 445 | Outros ativos intangíveis | Licenses, franchises |

### Step 2 — Recognition Criteria

An asset is recognized when:
1. It is probable that future economic benefits will flow to the entity
2. The cost can be reliably measured
3. Useful life > 1 year
4. Value above the entity's capitalization threshold (typically €250-€1,000)

**Initial cost includes:**
- Purchase price (net of discounts)
- Import duties and non-recoverable taxes
- Directly attributable costs (transport, installation, testing)
- Estimated dismantling/restoration costs

### Step 3 — Depreciation Rates (DR 25/2009)

| Asset Type | Tax Rate (straight-line) | Useful Life |
|------------|------------------------|-------------|
| Edifícios industriais | 5.00% | 20 years |
| Edifícios comerciais/serviços | 2.00% | 50 years |
| Equipamento básico (geral) | 12.50% | 8 years |
| Ferramentas e utensílios | 25.00% | 4 years |
| Equipamento de transporte ligeiro | 25.00% | 4 years |
| Equipamento transporte pesado | 20.00% | 5 years |
| Mobiliário e equipamento escritório | 12.50% | 8 years |
| Equipamento informático | 33.33% | 3 years |
| Software | 33.33% | 3 years |
| Equipamento administrativo diverso | 14.28% | 7 years |
| Patentes, marcas, licenças | 5.00-33.33% | Per contract/useful life |

**Note:** Tax rates are maximum rates. Entities may use lower rates (accounting rate can differ from tax rate).

### Step 4 — Depreciation Methods

| Method | Formula | When Used |
|--------|---------|-----------|
| Quotas constantes (straight-line) | Cost / Useful life | Default, most common |
| Quotas degressivas (declining balance) | NBV × (tax rate × 1.5/2/2.5) | Manufacturing equipment |
| Unidades de produção | (Cost / Total units) × Units used | Specific production assets |

**Declining balance coefficients:**
- Useful life < 5 years: × 1.5
- Useful life 5-6 years: × 2.0
- Useful life > 6 years: × 2.5

**Start of depreciation:** Month of entry into service (pro-rata first year).

### Step 5 — Vehicle Special Rules

| Limit | Applies to | Max Depreciable Cost |
|-------|-----------|---------------------|
| Viatura ligeira passageiros | Standard | €62,500 |
| Viatura ligeira passageiros GPL/GN | Gas | €62,500 |
| Viatura híbrida plug-in | Hybrid | €62,500 |
| Viatura elétrica | Electric | €62,500 |

Depreciation above the limit is non-deductible for IRC (added back in Modelo 22).

### Step 6 — Disposal and Retirement

**Sale entry:**
```
# Asset cost €10,000, accumulated depreciation €8,000, sold for €3,000+IVA
D  12xx  Bank               €3,690.00
D  438   Deprec. Acumuladas €8,000.00
C  43x   Ativo Fixo        €10,000.00
C  2413  IVA Liquidado        €690.00
C  7871  Ganho Alienação     €1,000.00
```

**Write-off (abate) entry:**
```
# Asset cost €5,000, fully depreciated, scrapped
D  438   Deprec. Acumuladas €5,000.00
C  43x   Ativo Fixo         €5,000.00
```

**Loss on disposal:**
```
D  438   Deprec. Acumuladas €6,000.00
D  6871  Perda Alienação    €2,000.00
C  43x   Ativo Fixo         €8,000.00
```

### Step 7 — Asset Register Requirements

| Field | Description |
|-------|-------------|
| Código ativo | Unique asset ID |
| Descrição | Asset description |
| Localização | Physical location |
| Data aquisição | Purchase date |
| Data entrada funcionamento | In-service date |
| Custo aquisição | Original cost |
| Método depreciação | Depreciation method |
| Taxa depreciação | Rate applied |
| Depreciação acumulada | Accumulated depreciation |
| Valor líquido contabilístico | Net book value (NBV) |
| Imparidade acumulada | Accumulated impairment |
| Data/valor alienação ou abate | Disposal date/amount |
| Estado | Active / Disposed / Idle |

### Step 8 — Impairment (NCRF 12)

Test for impairment when indicators exist:
- Market value decline
- Technological obsolescence
- Physical damage
- Change in use

```
# Impairment loss
D  655   Perdas Imparidade AFT  €5,000.00
C  439   Imparidades Acumul.    €5,000.00
```

## Commands

| Command | Description |
|---------|-------------|
| `conta-ativ:registar <ativo>` | Register new asset |
| `conta-ativ:depreciar <periodo>` | Calculate period depreciation |
| `conta-ativ:mapa <ano>` | Generate depreciation schedule |
| `conta-ativ:alienar <ativo>` | Process asset disposal |
| `conta-ativ:abater <ativo>` | Write off asset |
| `conta-ativ:imparidade <ativo>` | Test and record impairment |
| `conta-ativ:inventario` | Physical inventory checklist |
| `conta-ativ:relatorio` | Asset register summary report |

## Output Template

```yaml
asset_register:
  total_assets: 45
  active: 42
  disposed: 3
  summary:
    cost: 285000.00
    accumulated_depreciation: 142500.00
    impairment: 5000.00
    nbv: 137500.00
  by_class:
    buildings: { cost: 150000, nbv: 120000 }
    equipment: { cost: 80000, nbv: 12000 }
    vehicles: { cost: 35000, nbv: 3500 }
    it_equipment: { cost: 15000, nbv: 2000 }
    software: { cost: 5000, nbv: 0 }
  period_depreciation: 28500.00
  disposals_period: 1
  gain_loss_disposals: -2000.00
```

## Red Flags

- Assets in use but fully depreciated and not reviewed for useful life extension
- Depreciation rates exceeding DR 25/2009 maximums (non-deductible excess)
- Vehicle depreciation on cost above €62,500 limit
- No physical inventory of assets performed (at least every 2-3 years)
- Disposed assets still in register as active
- Impairment indicators present but no test performed
- Capital expenditure wrongly expensed (or vice versa)
- Depreciation not started in month of entry into service
- Assets without supporting purchase documentation
- Revaluation reserves not managed per NCRF 7
- Goodwill not tested for impairment annually

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-plano** | Accounts 43x, 44x, 438, 439 for assets |
| **conta-lancamentos** | Acquisition, depreciation, disposal entries |
| **conta-irc** | Tax depreciation limits and Modelo 22 adjustments |
| **conta-relatorios** | Asset values in balance sheet |
| **conta-auditoria** | Asset register as audit evidence |
| **conta-encerramento** | Year-end depreciation and impairment review |
| **conta-orcamento** | Capital expenditure budget |
| **conta-consolidacao** | Intercompany asset transfers |


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-ativos** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-ativos:**

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
