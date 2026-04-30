---
name: diva-floor-plan
description: Floor plan analysis and optimization for architecture and interior design projects. Analyzes circulation flow, functional zones, RGEU dimensional compliance, natural light, ventilation, and privacy gradient. Proposes 2-3 layout alternatives with pros/cons. Triggers on "planta", "floor plan", "layout", "circulacao", "optimizar espaco", "distribuicao".
license: MIT
---

# DIVA Skill — Floor Plan Analysis & Optimization

Analyzes existing floor plans and proposes optimized layout alternatives. Evaluates circulation flow, functional zoning, dimensional compliance with Portuguese regulations (RGEU), natural light distribution, ventilation paths, and privacy gradients. Produces 2-3 layout alternatives with comparative analysis.

## When to activate

Invoke `/diva-floor-plan` (or trigger automatically) when:
- User shares a floor plan (image, description, or dimensions)
- User asks to optimize a layout or redistribute spaces
- User wants to evaluate if a space works for their program
- User is deciding between layout options
- User mentions circulation problems, wasted space, or poor flow
- After `diva-briefing` defines the functional program

Do NOT use when:
- No floor plan or dimensional information is available (do `diva-diagnose` first)
- User only needs material or budget information
- The project is purely exterior/facade work

## Workflow

### 1. Capture existing plan data
From image, description, or measurements:
- **External dimensions:** total footprint
- **Structural elements:** load-bearing walls (mark as IMMOVABLE), columns, shafts
- **Fixed points:** risers (prumadas), wet areas stack, stairwell, elevator
- **Window positions:** size, orientation (N/S/E/W), height from floor
- **Door positions:** entry door(s), interior doors
- **Ceiling height:** uniform or variable
- **Current room layout:** with approximate dimensions

If a floor plan image is provided, extract dimensions. If dimensions are missing, ask for key measurements.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "RGEU minimum areas rooms apartment residential", limit: 5)
mcp__dario-rag__search_kb(query: "floor plan circulation flow functional zoning", limit: 5)
mcp__dario-rag__search_kb(query: "natural light ventilation apartment layout", limit: 5)
```

### 3. RGEU dimensional compliance audit
Check every space against Portuguese minimums:

**Minimum areas (RGEU Art. 65-67):**
| Space | Min area (m2) | Min dimension (m) |
|---|---|---|
| Sala (T0-T1) | 10 | 2.10 |
| Sala (T2+) | 12 | 2.70 |
| Quarto casal | 10.50 | 2.60 |
| Quarto individual | 6.50 | 2.10 |
| Cozinha | 6 | 1.70 |
| WC | 3.50 | 1.30 |
| Despensa | - | 0.80 |
| Corredor | - | 0.90 (1.10 recommended) |

**Minimum ceiling height:** 2.40m (habitavel), 2.20m (WC, arrumos, garagem)

**Natural light:** each habitable room must have window area >= 1/8 of floor area

**Ventilation:** cross-ventilation path, kitchen and WC must have extraction

Flag every non-compliance as CRITICO (if new work) or EXISTENTE (if pre-existing and grandfathered).

### 4. Circulation flow analysis
- **Entry sequence:** from front door, what do you see/access first
- **Public-private gradient:** entry > social zones > private zones (ideal flow)
- **Kitchen triangle:** sink-stove-fridge distances (ideal: 3.6-7.9m perimeter)
- **Corridor efficiency:** percentage of total area used for circulation (target: <15%)
- **Dead-end spaces:** rooms accessible only through other rooms (avoid for bedrooms)
- **Service flow:** laundry path, garbage path, grocery unloading
- **Emergency egress:** code-compliant exit routes

### 5. Functional zone mapping
Divide the plan into zones:
- **Social zone:** sala, dining, kitchen (ideally connected, near entry)
- **Private zone:** bedrooms, suites (ideally away from entry, quieter side)
- **Service zone:** laundry, storage, technical (can be windowless)
- **Wet zone:** bathrooms, kitchen (stack vertically for plumbing efficiency)
- **Transition zone:** corridors, hall (minimize but don't eliminate)

Evaluate adjacency quality:
- Kitchen near dining (essential)
- Suite bathroom accessible from bedroom (essential)
- Guest WC accessible from social zone without crossing private zone
- Laundry near bedrooms OR kitchen (cultural: PT traditionally near kitchen)

### 6. Natural light and orientation analysis
- **South-facing rooms:** prioritize living areas (maximum winter sun)
- **North-facing rooms:** suitable for offices, storage, service areas
- **East-facing rooms:** good for bedrooms (morning light)
- **West-facing rooms:** afternoon sun, can overheat in summer (consider shading)
- **Light penetration depth:** max ~6m from window without borrowed light
- **Borrowed light strategies:** interior windows, glass partitions, clerestories
- **Light well/saguao:** if present, maximize its use

### 7. Generate layout alternatives
Produce 2-3 options:

**Option A — Conservative:**
- Minimal structural changes
- Respects existing plumbing positions
- Lower cost, faster execution
- Best for: budget constraints, rental properties

**Option B — Optimized:**
- Strategic wall removals (non-structural only)
- May relocate some wet areas within reason
- Better flow and space utilization
- Best for: medium renovations, most clients

**Option C — Transformative:**
- Maximum structural intervention (within regulatory limits)
- Possible plumbing relocation, new openings in structural walls (with engineering)
- Completely reimagined layout
- Best for: full gut renovations, high budgets

For each option provide:
- Textual floor plan description with dimensions
- Walls removed (with load-bearing confirmation)
- Walls added
- Plumbing moves (and cost implications)
- Pros and cons
- Estimated cost tier impact
- RGEU compliance status

### 8. Comparative analysis
| Criteria | Option A | Option B | Option C |
|---|---|---|---|
| Circulation efficiency | ... | ... | ... |
| Natural light | ... | ... | ... |
| Privacy gradient | ... | ... | ... |
| RGEU compliance | ... | ... | ... |
| Structural impact | ... | ... | ... |
| Plumbing impact | ... | ... | ... |
| Cost impact | ... | ... | ... |
| WOW factor | ... | ... | ... |

### 9. Recommendation
State the recommended option with rationale tied to the client's briefing priorities.

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-floor-plan
area_total_m2: <number>
area_util_m2: <number>
typology_current: <T0-T5>
typology_proposed: <T0-T5>
options_count: <2-3>
---

# Analise de Planta DIVA — <Property/Client>

## Planta Existente
### Dimensoes gerais
### Elementos estruturais (imoveis)
### Pontos fixos (prumadas, shafts)
### Programa atual

## Auditoria RGEU
| Espaco | Area atual | Min RGEU | Conforme? |
|---|---|---|---|
| Sala | ... | 12 m2 | ... |
| Quarto 1 | ... | 10.5 m2 | ... |
| Cozinha | ... | 6 m2 | ... |
| WC | ... | 3.5 m2 | ... |

### Nao-conformidades identificadas

## Analise de Circulacao
### Fluxo entrada-social-privado
### Eficiencia de corredor (% da area)
### Triangulo de cozinha
### Fluxos de servico

## Mapa de Zonas Funcionais
### Zona social
### Zona privada
### Zona de servico
### Zona humida

## Luz Natural e Orientacao
### Orientacao por fachada
### Profundidade de penetracao
### Espacos deficitarios

## Opcao A — Conservadora
### Descricao do layout
### Alteracoes estruturais: nenhuma/minimas
### Pros
### Contras
### Impacto custo: baixo

## Opcao B — Optimizada
### Descricao do layout
### Alteracoes estruturais
### Pros
### Contras
### Impacto custo: medio

## Opcao C — Transformadora
### Descricao do layout
### Alteracoes estruturais
### Pros
### Contras
### Impacto custo: alto

## Comparacao
| Criterio | Opcao A | Opcao B | Opcao C |
|---|---|---|---|
| Circulacao | ... | ... | ... |
| Luz natural | ... | ... | ... |
| Privacidade | ... | ... | ... |
| RGEU | ... | ... | ... |
| Custo | ... | ... | ... |

## Recomendacao
<Recommended option + rationale>

## Proximos Passos
- [ ] Cliente escolhe opcao preferida
- [ ] Seguir com `diva-materials` para especificacao de materiais
- [ ] Seguir com `diva-budget` para orcamento da opcao escolhida
- [ ] Projeto de especialidades (estabilidade, redes)
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Analise Planta DIVA.md`

## Red flags — don't do this
- Never propose removing a wall without confirming it is NOT load-bearing
- Never ignore RGEU minimum dimensions for new layouts
- Never forget to check plumbing stack positions before moving wet areas
- Never propose a layout where a bedroom is only accessible through another bedroom
- Never ignore the kitchen work triangle
- Never place a WC door opening directly onto the kitchen or dining area
- Never forget cross-ventilation requirements
- Never assume window positions can be moved (structural + facade implications)
- Never propose more than 3 options (decision paralysis)
- Never skip the comparative table (clients need side-by-side to decide)

## Interactions
- Usually follows `diva-diagnose` + `diva-briefing`
- Feeds into `diva-materials` for material specification per chosen layout
- Feeds into `diva-budget` for cost estimation of chosen option
- May trigger engineering consultation if structural changes are proposed
- Save via `dario-obsidian-save` to vault
