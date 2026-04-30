---
name: diva-calc
description: "Interactive construction budget calculator for Portugal. Takes inputs (area, type, location, quality, rooms) and computes detailed budget by ProNIC chapter with IVA, fees, contingency, and 3 scenarios (economico/recomendado/premium). Triggers on \"calcula orcamento\", \"quanto custa esta obra\", \"simula orcamento\", \"calculadora\", \"calcula budget\", \"simular custos\", \"3 cenarios\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Calc — Interactive Budget Calculator

Compute detailed construction budgets from inputs. Not just reference tables — actual calculations with formulas, adjustments, and scenario simulation.

## When to activate

Invoke `/diva-calc` when:
- User provides area + type + location and wants a budget
- User wants to compare 3 price scenarios
- User asks "quanto custa remodelar um T2 em Lisboa?"
- User needs detailed breakdown by chapter
- User wants to simulate different quality levels

## Input Parameters

Collect from user (or infer from context):

| Parameter | Type | Example | Default |
|---|---|---|---|
| `area_m2` | number | 75 | REQUIRED |
| `tipo` | enum | remodelacao / nova / reabilitacao | remodelacao |
| `scope` | enum | cosmetico / medio / completo / estrutural / luxo | completo |
| `localizacao` | enum | nacional / lisboa_porto / algarve / interior | nacional |
| `ano_construcao` | number | 1960 | null |
| `n_wc` | number | 2 | from tipologia |
| `tipologia` | enum | T0/T1/T2/T3/T4/T5 | from area |
| `cozinha_nova` | bool | true | true if completo |
| `caixilharia_nova` | bool | true | true if completo |
| `avac` | enum | nenhum / splits / piso_radiante / vrf | splits |
| `domotica` | enum | nenhum / basico / medio / premium | nenhum |
| `exterior_m2` | number | 0 | 0 |
| `iva_regime` | enum | 6 / 23 / auto | auto |

## Calculation Engine

### Step 1: Base Cost per m2

```
BASE_COSTS = {
  "cosmetico": {"nacional": 250, "lisboa_porto": 300, "algarve": 300},
  "medio": {"nacional": 700, "lisboa_porto": 850, "algarve": 800},
  "completo": {"nacional": 1200, "lisboa_porto": 1450, "algarve": 1300},
  "estrutural": {"nacional": 1700, "lisboa_porto": 2000, "algarve": 1650},
  "luxo": {"nacional": 2650, "lisboa_porto": 3000, "algarve": 2750}
}

base = BASE_COSTS[scope][localizacao]
```

### Step 2: Adjustment Factors

```
factors = 1.0

# Age factor
if ano_construcao and ano_construcao < 1951:
    factors *= 1.20  # Pre-RGEU, patologias provaveis
elif ano_construcao and ano_construcao < 1980:
    factors *= 1.10  # Possivel amianto, instalacoes antigas

# Access factor (infer from location)
if localizacao == "lisboa_porto":
    factors *= 1.05  # Centro historico, estacionamento, elevadores

# Season (if obra inverno)
# factors *= 1.07  # Nov-Fev

adjusted_base = base * factors
```

### Step 3: Chapter Breakdown

```
CHAPTER_PERCENTAGES = {
  "completo": {
    "01_estaleiro": 0.02,
    "03_demolicao": 0.04,
    "09_alvenaria": 0.04,
    "12_impermeabilizacao": 0.03,
    "13_isolamento": 0.04,
    "14_revestimento_paredes": 0.07,
    "15_pavimentos": 0.10,
    "16_tectos": 0.03,
    "17_carpintaria": 0.08,
    "18_caixilharia": 0.10,
    "20_pintura": 0.04,
    "21_canalizacao": 0.08,
    "22_electricidade": 0.10,
    "23_avac": 0.07,
    "27_cozinha": 0.10,
    "28_sanitarios": 0.06,
  }
}

subtotal = adjusted_base * area_m2
for chapter, pct in CHAPTER_PERCENTAGES[scope].items():
    chapter_value = subtotal * pct
```

### Step 4: Add-ons (items calculated separately)

```
# WC: each WC has fixed cost beyond base
wc_addon = n_wc * {"cosmetico": 800, "medio": 2500, "completo": 4500, "luxo": 8000}[scope]

# Cozinha: if new kitchen
cozinha_addon = {"cosmetico": 0, "medio": 5000, "completo": 10000, "luxo": 25000}[scope] if cozinha_nova else 0

# Caixilharia: per window unit average
caixilharia_addon = (area_m2 / 10) * {"basico": 400, "aluminio": 700, "premium": 1200}[quality] if caixilharia_nova else 0

# AVAC
avac_addon = {
  "nenhum": 0,
  "splits": area_m2 * 30,
  "piso_radiante": area_m2 * 75,
  "vrf": area_m2 * 120
}[avac]

# Domotica
domotica_addon = {
  "nenhum": 0,
  "basico": area_m2 * 40,
  "medio": area_m2 * 115,
  "premium": area_m2 * 350
}[domotica]

# Exterior
exterior_addon = exterior_m2 * 150 if exterior_m2 > 0 else 0
```

### Step 5: Fees & Extras

```
construction_total = subtotal + wc_addon + cozinha_addon + caixilharia_addon + avac_addon + domotica_addon + exterior_addon

fees = {
  "arquitectura": construction_total * 0.08,     # 8% medio
  "engenharia": construction_total * 0.03,        # 3% (estruturas + MEP)
  "fiscal": construction_total * 0.03,            # 3%
  "sce": 500,                                      # fixo
  "licenciamento": area_m2 * 10,                   # estimativa media
}

contingencia_pct = 0.15 if tipo == "remodelacao" else 0.20 if tipo == "reabilitacao" else 0.10
contingencia = construction_total * contingencia_pct
```

### Step 6: IVA

```
if iva_regime == "auto":
    if tipo in ["remodelacao", "reabilitacao"] and (not ano_construcao or ano_construcao <= 2024):
        iva_rate = 0.06  # Habitacao propria >2 anos
    else:
        iva_rate = 0.23
else:
    iva_rate = int(iva_regime) / 100

iva = (construction_total + sum(fees.values()) + contingencia) * iva_rate
```

### Step 7: 3 Scenarios

Run the entire calculation 3 times with multipliers:
```
SCENARIOS = {
  "economico": 0.75,      # 75% do valor recomendado
  "recomendado": 1.00,     # valor calculado
  "premium": 1.40,         # 140% do valor recomendado
}
```

## Output Template

```markdown
# Orcamento Estimado — [Projecto]

## Dados de Entrada
- **Area:** XX m2 | **Tipo:** remodelacao | **Scope:** completo
- **Localizacao:** Lisboa | **Ano construcao:** 1965
- **WCs:** 2 | **Cozinha nova:** Sim | **Caixilharia:** Sim
- **AVAC:** Piso radiante | **Domotica:** Medio

## 3 Cenarios

| | Economico | Recomendado | Premium |
|---|---|---|---|
| **Custo/m2** | X EUR | X EUR | X EUR |
| **Construcao** | X EUR | X EUR | X EUR |
| **Honorarios** | X EUR | X EUR | X EUR |
| **Contingencia** | X EUR | X EUR | X EUR |
| **Subtotal** | X EUR | X EUR | X EUR |
| **IVA (X%)** | X EUR | X EUR | X EUR |
| **TOTAL** | **X EUR** | **X EUR** | **X EUR** |

## Breakdown Detalhado (Cenario Recomendado)

| Cap. | Descricao | % | Valor EUR |
|---|---|---|---|
| 01 | Estaleiro | 2% | X |
| 03 | Demolicao | 4% | X |
| 09 | Alvenaria | 4% | X |
| 12 | Impermeabilizacao | 3% | X |
| 13 | Isolamento | 4% | X |
| 14 | Revestimentos paredes | 7% | X |
| 15 | Pavimentos | 10% | X |
| 16 | Tectos | 3% | X |
| 17 | Carpintaria | 8% | X |
| 18 | Caixilharia | 10% | X |
| 20 | Pintura | 4% | X |
| 21 | Canalizacao | 8% | X |
| 22 | Electricidade | 10% | X |
| 23 | AVAC | 7% | X |
| 27 | Cozinha | 10% | X |
| 28 | Sanitarios | 6% | X |
| | **Subtotal obra** | 100% | **X** |

## Add-ons
| Item | Valor EUR |
|---|---|
| WC (X unidades) | X |
| Cozinha nova | X |
| Caixilharia | X |
| AVAC (tipo) | X |
| Domotica (nivel) | X |
| Exterior (X m2) | X |
| **Total add-ons** | **X** |

## Honorarios e Extras
| Item | Valor EUR |
|---|---|
| Arquitectura (8%) | X |
| Engenharia (3%) | X |
| Fiscalizacao (3%) | X |
| Certificacao energetica | 500 |
| Licenciamento camara | X |
| **Total honorarios** | **X** |

## Resumo Final (Recomendado)
| | Valor EUR |
|---|---|
| Construcao | X |
| Add-ons | X |
| Honorarios | X |
| Contingencia (15%) | X |
| **Subtotal sem IVA** | **X** |
| IVA (X%) | X |
| **TOTAL COM IVA** | **X** |

## Regime IVA
- Regime aplicado: X% — [justificacao]
- Poupanca vs 23%: X EUR (se aplicavel)

## Plano de Pagamentos Sugerido
| Milestone | % | Valor EUR |
|---|---|---|
| Sinal (contrato) | 10% | X |
| Inicio obra | 25% | X |
| MEP concluido | 25% | X |
| Acabamentos | 20% | X |
| Recepcao | 15% | X |
| Retencao (12 meses) | 5% | X |

## Notas
- Precos de referencia Abril 2026, mercado portugues
- Valores estimados — pedir SEMPRE 3 orcamentos a empreiteiros
- Contingencia: {contingencia_pct*100}% incluida
- Materiais: nivel {scope} — fornecedores PT
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - Orcamento Calculado.md`

## Red Flags
- Never present a single scenario — always include 3 tiers (economico/recomendado/premium) so the client understands the cost-quality spectrum
- Always include the 3-tier comparison table even for quick estimates — a single number creates false precision and kills trust when the real quote differs
- Never skip IVA in the final total — presenting values sem IVA misleads clients who budget in cash-out-of-pocket terms (6% vs 23% can shift the total by tens of thousands)
- Always caveat that all prices are estimates based on 2026 market averages — real contractor quotes will vary by availability, season, and site conditions
- Never drop contingency below 10% even in the economico tier — Portuguese renovation surprises (hidden structures, outdated wiring, asbestos) are the norm, not the exception
- Always recommend the client obtain at least 3 real contractor quotes — the calculator is a planning tool, not a substitute for competitive tendering
