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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Inputs recolhidos e validados antes de calcular
- [ ] `area_m2` confirmado (número concreto, não "um T2 grande")
- [ ] `scope` inferido ou confirmado — não assumir `completo` sem validação
- [ ] `localizacao` mapeada para um dos 4 enums válidos (`nacional / lisboa_porto / algarve / interior`)
- [ ] `ano_construcao` pedido quando `tipo == reabilitacao` (impacto directo no factor de ajuste e IVA)
- ❌ NOT delivery-ready: "Assumindo Lisboa e remodelação completa para o seu apartamento"
- ✅ Delivery-ready: "Confirmado: 80 m², remodelação completa, Lisboa/Porto, construção 1968 → factor de vetustez +10% aplicado"

### Gate 2 — Cálculo aritmético verificável linha a linha
- [ ] `adjusted_base = base × factors` explicitamente mostrado com números
- [ ] `subtotal = adjusted_base × area_m2` calculado e apresentado
- [ ] Cada chapter breakdown mostra `subtotal × pct = valor EUR` (não só percentagem)
- [ ] Add-ons (WC, cozinha, caixilharia, AVAC, domótica) apresentados como valores individuais, não fundidos
- ❌ NOT delivery-ready: "Instalações eléctricas: ~12 000 €" sem origem do número
- ✅ Delivery-ready: "Cap. 22 Electricidade: 92 800 € × 10% = 9 280 € + AVAC splits 80 m² × 30 = 2 400 €"

### Gate 3 — Tabela dos 3 cenários completa e coerente
- [ ] Três colunas: Económico (×0.75) / Recomendado (×1.00) / Premium (×1.40)
- [ ] Cada coluna inclui: custo/m², subtotal obra, honorários, contingência, IVA, **TOTAL**
- [ ] Multiplicadores aplicados ao `construction_total` — honorários e contingência recalculados proporcionalmente
- [ ] Diferença Económico→Premium indicada em EUR e em percentagem (contexto de decisão)
- ❌ NOT delivery-ready: Tabela com linha "Total" mas sem discriminar IVA ou contingência
- ✅ Delivery-ready: "Premium: 129 640 € obra + 18 150 € honor. + 25 928 € conting. + 10 424 € IVA 6% = **184 142 € total**"

### Gate 4 — Regime de IVA correctamente determinado e justificado
- [ ] Lógica `auto` aplicada: habitação própria + obra ≥2 anos → 6%; nova construção → 23%
- [ ] Regime indicado explicitamente com justificação (não apenas "IVA: 6%")
- [ ] Se IVA 6%, nota sobre condições de elegibilidade (afectação habitacional, requerimento AT)
- [ ] Honorários de projecto (arquitectura, engenharia) com IVA 23% separado se diferente da obra
- ❌ NOT delivery-ready: "IVA incluído nos valores acima" sem taxa nem base de cálculo
- ✅ Delivery-ready: "IVA 6% aplicável — remodelação hab. própria, imóvel 1968 (>2 anos). Base: 116 450 € → IVA: 6 987 €. Honorários projecto: IVA 23% separado = 2 875 €"

### Gate 5 — Contingência e honorários discriminados com lógica ProNIC
- [ ] Contingência calculada com `pct` correcto: 15% remodelação / 20% reabilitação / 10% nova
- [ ] Cinco linhas de honorários mostradas individualmente (arquitectura 8%, engenharia 3%, fiscal 3%, SCE 500 €, licenciamento área×10 €)
- [ ] Nota de contextualização: contingência para imóvel pré-1980 com possível amianto ou patologias
- [ ] Chapters ProNIC numerados (01, 03, 09… 28) — não renomeados nem fundidos
- ❌ NOT delivery-ready: "Honorários estimados: 15 000 €" como valor único sem discriminação
- ✅ Delivery-ready: "Arquitectura 8%: 7 416 € | Eng. 3%: 2 781 € | Fiscal 3%: 2 781 € | SCE: 500 € | Licenciamento 80×10: 800 € | **Total honor.: 14 278 €**"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets por preencher
- [ ] Título do orçamento tem nome do projecto/cliente real (não `[Projecto]`)
- [ ] Nenhum placeholder `<valor>`, `XX m²`, `X EUR` no output final
- [ ] Morada ou referência de localização concreta (ex.: "Avenida de Roma, Lisboa" não "Lisboa")
- [ ] Data da simulação indicada (validade de 60 dias — mercado de materiais volátil)
- ❌ NOT delivery-ready: "# Orçamento Estimado — [Projecto]" com área "XX m²"
- ✅ Delivery-ready: "# Orçamento Estimado — Remodelação Cuidai HQ, Rua Braamcamp 40, Lisboa · Simulação: Jun 2025 (válida 60 dias)"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Orçamento Estimado — Remodelação Apartamento Atrium T3, Av. da República 45, Lisboa
**Simulação:** 14 Jun 2025 · Válida 60 dias (índices de materiais voláteis)

---

## Dados de Entrada

| Parâmetro | Valor |
|---|---|
| Área | 95 m² |
| Tipo | Remodelação |
| Scope | Completo |
| Localização | Lisboa/Porto |
| Ano construção | 1971 |
| Tipologia | T3 |
| WCs | 2 |
| Cozinha nova | Sim |
| Caixilharia nova | Sim |
| AVAC | Splits |
| Domótica | Básico |
| Exterior | 0 m² |
| IVA | Auto → 6% (hab. própria, imóvel >2 anos) |

---

## Motor de Cálculo — Passo a Passo

**Base:** scope `completo` + `lisboa_porto` → **1 450 €/m²**

**Factores de ajuste:**
- Ano 1971 (1951–1980): × 1.10 → possível amianto, instalações obsoletas
- Localização Lisboa (acesso/estacionamento): × 1.05
- **Factor combinado: × 1.155**

**Base ajustada:** 1 450 × 1.155 = **1 674,75 €/m²**
**Subtotal base:** 1 674,75 × 95 m² = **159 011 €**

**Breakdown ProNIC — Scope Completo:**

| Cap. | Descrição | % | Valor (€) |
|---|---|---|---|
| 01 | Estaleiro | 2% | 3 180 |
| 03 | Demolição | 4% | 6 360 |
| 09 | Alvenaria | 4% | 6 360 |
| 12 | Impermeabilização | 3% | 4 770 |
| 13 | Isolamento | 4% | 6 360 |
| 14 | Revestimento paredes | 7% | 11 131 |
| 15 | Pavimentos | 10% | 15 901 |
| 16 | Tectos | 3% | 4 770 |
| 17 | Carpintaria | 8% | 12 721 |
| 18 | Caixilharia | 10% | 15 901 |
| 20 | Pintura | 4% | 6 360 |
| 21 | Canalização | 8% | 12 721 |
| 22 | Electricidade | 10% | 15 901 |
| 23 | AVAC | 7% | 11 131 |
| 27 | Cozinha | 10% | 15 901 |
| 28 | Sanitários | 6% | 9 541 |
| | **Subtotal chapters** | 100% | **159 011** |

**Add-ons:**

| Item | Cálculo | Valor (€) |
|---|---|---|
| WCs (2×) | 2 × 4 500 | 9 000 |
| Cozinha nova | fixo completo | 10 000 |
| Caixilharia | (95/10) × 700 | 6 650 |
| AVAC splits | 95 × 30 | 2 850 |
| Domótica básico | 95 × 40 | 3 800 |
| **Total add-ons** | | **32 300** |

**Construction total: 159 011 + 32 300 = 191 311 €**

**Honorários:**

| Item | Cálculo | Valor (€) |
|---|---|---|
| Arquitectura 8% | 191 311 × 0.08 | 15 305 |
| Engenharia 3% | 191 311 × 0.03 | 5 739 |
| Fiscal obra 3% | 191 311 × 0.03 | 5 739 |
| SCE | fixo | 500 |
| Licenciamento | 95 × 10 | 950 |
| **Total honorários** | | **28 233** |

**Contingência:** remodelação → 15% × 191 311 = **28 697 €**
*(Nota: imóvel 1971 — risco amianto em tectos/condutas; contingência pode ser insuficiente sem inspecção prévia)*

**Base IVA 6%:** 191 311 + 28 233 + 28 697 = 248 241 € → **IVA: 14 894 €**
*(Honorários de projecto sujeitos a IVA 23% separado: 28 233 × 0.23 = 6 494 €)*

---

## 3 Cenários

| | Económico (×0.75) | Recomendado (×1.00) | Premium (×1.40) |
|---|---|---|---|
| Custo/m² obra | 1 256 €/m² | 1 675 €/m² | 2 345 €/m² |
| Subtotal obra | 143 483 € | 191 311 € | 267 835 € |
| Honorários | 21 174 € | 28 233 € | 39 527 € |
| Contingência | 21 523 € | 28 697 € | 40 175 € |
| IVA 6% obra | 11 172 € | 14 894 € | 20 852 € |
| **TOTAL** | **197 352 €** | **263 135 €** | **368 389 €** |

Diferença Económico → Premium: **+171 037 € (+87%)**

---

## Notas e Próximos Passos

1. **Validade:** valores referência Jun 2025; aço +12% YoY, rever se obra iniciar após Set 2025
2. **IVA 6%:** confirmar elegibilidade com AT antes de adjudicar (afectação hab. própria obrigatória)
3. **Amianto:** imóvel 1971 — recomendar inspecção prévia (200–400 €); remoção pode adicionar 5 000–15 000 €
4. **Concurso:** orçamento para lançar concurso a 3 empreiteiros; desvio esperado ±15%
```

---

## Output anti-patterns

- Apresentar "Total: X €" sem discriminar obra / honorários / contingência / IVA — cliente não consegue negociar nem comparar propostas
- Usar `scope = completo` como default silencioso sem confirmar com o utilizador — infla orçamento e perde confiança
- Mostrar percentagens dos chapters sem os valores absolutos correspondentes — ilegível para cliente não-técnico
- Omitir o regime de IVA ou escrever apenas "IVA incluído" — erro fiscal com impacto de 17 pp na decisão
- Tabela de 3 cenários com só o total — sem custo/m² e sem breakdown, os cenários perdem poder de decisão
- Não mencionar validade do orçamento — mercado de materiais PT tem volatilidade 10–15%/ano; output desactualizado gera reclamações
- Placeholder `[Projecto]` ou `XX m²` no output final entregue ao cliente — sinal de output não revisto
- Ignorar factor de vetustez em imóveis pré-1980 — subestima obra em 10–20% e cria conflito com empreiteiro
- Apresentar add-ons (WC, cozinha, AVAC) já fundidos no subtotal sem linha separada — impede cliente de perceber onde pode cortar
- Omitir nota de risco (amianto, patologias estruturais, acesso centro histórico) em projetos de reabilitação — expõe DIVA a responsabilidade por surpresas em obra
