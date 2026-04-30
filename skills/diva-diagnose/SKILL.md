---
name: diva-diagnose
description: DIVA's universal diagnostic for architecture, design, and construction projects. Structural assessment, design potential, regulatory compliance (RGEU/RJUE), budget feasibility, timeline estimation, and 4-milestone roadmap. Triggers on "diagnose", "diagnostico", "avaliar espaco", "analise projecto", "onde comecar", "roadmap obra".
license: MIT
---

# DIVA Skill — Project Diagnostic

The universal entry point for any architecture, interior design, or construction project. Produces a structured diagnosis covering structural condition, design potential, regulatory compliance, budget feasibility, and a phased roadmap before any specialized work begins.

## When to activate

Invoke `/diva-diagnose` (or trigger automatically) when:
- User brings a new space/property to evaluate (apartment, house, commercial)
- User asks "where do I start" with a renovation or construction project
- User shares photos, floor plans, or descriptions of a space
- User wants a roadmap for a remodeling or construction project
- User mentions regulatory concerns (licensing, RGEU, RJUE)
- Start of any architecture/design project workflow

Do NOT use when:
- User already has a diagnosis and needs a specific deliverable (use diva-floor-plan, diva-materials, diva-budget)
- Request is purely about material selection or budget without project context

## Workflow

### 1. Context gathering
Collect (or infer from input) the minimum viable context:
- **Property type:** apartment (T0-T5+), moradia, commercial, mixed-use
- **Location:** concelho, freguesia (affects CML/CMO/CM* regulations)
- **Current state:** original, already renovated, in ruins, new construction
- **Area:** total m2, useful m2 (if known)
- **Year of construction:** pre-1951 (no license needed for some work), 1951-1990, post-1990
- **Ownership situation:** own, buying, inherited, rented
- **What they want:** renovation level (cosmetic/structural/total gut), new build, expansion
- **Photos/plans available:** yes/no, quality

If critical context is missing (especially property type, location, and renovation scope), stop and ask.

### 2. RAG consult (mandatory)
```
mcp__dario-rag__search_kb(query: "RGEU regulamento geral edificacoes urbanas minimum areas", limit: 5)
mcp__dario-rag__search_kb(query: "RJUE licenciamento comunicacao previa obras", limit: 5)
mcp__dario-rag__search_kb(query: "<property type> <renovation type> portugal", limit: 5)
```

### 3. Structural assessment
Evaluate (from description/photos/plans):
- **Structural system:** masonry, concrete frame, mixed, wood (pre-1755, pombalino, gaioleiro, placa, modern)
- **Visible pathologies:** cracks (structural vs cosmetic), humidity, efflorescence, deformation
- **Floors/ceilings:** wood (soalho), concrete slab, mixed
- **Walls:** load-bearing identification (critical before any demolition)
- **Roof:** condition if applicable (telha, terraço, cobertura plana)
- **Infrastructure age:** electrical (pre/post RTIEBT), plumbing (chumbo/ferro/PPR/PEX), gas

Flag anything that requires structural engineering (projeto de estabilidade).

### 4. Design potential analysis
- **Natural light:** orientation (N/S/E/W), window count and size, obstructions
- **Ceiling height:** standard 2.70m, high ceilings (>3m = design opportunity), low (<2.40m = RGEU non-compliant)
- **Flow potential:** open plan viability, circulation optimization
- **Views/outdoor space:** balcony, terrace, garden, courtyard
- **Character elements worth preserving:** azulejos, moldings, soalho original, ironwork
- **Spatial constraints:** columns, shafts, structural walls that limit layout

### 5. Regulatory compliance check (RGEU/RJUE)
- **RGEU minimums:** room dimensions, ceiling heights, ventilation, natural light (1/8 of floor area)
- **RJUE classification:** what type of procedure is needed?
  - Isenta (exempt): interior works not affecting structure/facade
  - Comunicacao previa: minor exterior changes, some interior restructuring
  - Licenciamento: structural changes, use changes, facade alterations
  - Autorizacao de utilizacao: change of use (commercial to residential, etc.)
- **PDM/PMOT:** local zoning, max height, max density, heritage zones (ARU, ACRRU)
- **Heritage constraints:** DGPC classification, zona tampao, imovel de interesse
- **Condominium rules:** if apartment, what requires condominium approval
- **EAA/accessibility:** applicable if commercial or >4 units

### 6. Prioritization
Classify every finding into exactly one bucket:
- **CRITICO** — Structural safety, legal risk, blocks all other work (load-bearing wall issues, no license when needed, electrical danger, asbestos)
- **IMPORTANTE** — Affects project viability, must be addressed in planning (RGEU non-compliance, infrastructure replacement, waterproofing)
- **OPTIMIZACAO** — Enhances quality but not blocking (better materials, smart home, energy upgrade)

### 7. Roadmap — 4 milestones
| Milestone | Phase | Focus |
|---|---|---|
| **M1 — Projecto** | 4-8 weeks | Architecture project, engineering specialties, material selection |
| **M2 — Licenciamento** | 4-16 weeks | CM submission, approval wait, contractor selection |
| **M3 — Obra** | 8-24 weeks | Construction execution, site management, quality control |
| **M4 — Entrega** | 2-4 weeks | Snag list, final inspection, habitability license, handover |

Customize durations based on project scope and municipality (Lisbon CM is slower than smaller municipalities).

### 8. Budget feasibility range
Provide a rough cost/m2 range based on scope:
- **Cosmetic refresh:** 200-400 EUR/m2
- **Medium renovation:** 500-800 EUR/m2
- **Full gut renovation:** 800-1,200 EUR/m2
- **Premium renovation:** 1,200-2,000+ EUR/m2
- **New construction:** 1,200-2,500 EUR/m2

Flag if budget expectations are misaligned with scope.

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-diagnostic
property_type: <type>
location: <concelho>
area_m2: <number>
construction_year: <year/decade>
confidence: <green|yellow|red>
---

# Diagnostico DIVA — <Property/Client>

## Resumo Executivo
- **Espaco:** <type, area, location>
- **Estado atual:** <condition summary>
- **Ambicao:** <what the client wants>
- **Viabilidade:** <green/yellow/red + 1 line>
- **Estimativa custo:** <range EUR/m2 x area = total range>
- **Timeline estimada:** <months>

## Avaliacao Estrutural
### Sistema construtivo
### Patologias identificadas
### Infraestruturas (eletrica/hidrosanitaria/gas)
### Elementos a preservar

## Potencial de Design
### Luz natural e orientacao
### Pe-direito e volumetria
### Fluxo e circulacao
### Espaco exterior
### Elementos de caracter

## Conformidade Regulamentar
### RGEU — Areas minimas e pe-direito
### RJUE — Tipo de procedimento necessario
### PDM/Zonamento
### Condicionantes patrimoniais
### Condominio (se aplicavel)

## Priorizacao
### CRITICO (bloqueia projecto / risco seguranca)
1. ...
### IMPORTANTE (afeta viabilidade)
1. ...
### OPTIMIZACAO (melhoria de qualidade)
1. ...

## Roadmap
### M1 — Projecto (Sem 1-8)
- [ ] ...
### M2 — Licenciamento (Sem 9-24)
- [ ] ...
### M3 — Obra (Sem 25-48)
- [ ] ...
### M4 — Entrega (Sem 49-52)
- [ ] ...

## Estimativa Orcamental
| Categoria | Range EUR |
|---|---|
| Custo/m2 estimado | X - Y |
| Area util | Z m2 |
| **Total estimado** | **A - B** |
| Honorarios projecto (~10%) | ... |
| Licenciamento | ... |
| Contingencia (10-15%) | ... |

## Proximos Passos
- [ ] Seguir com `diva-briefing` para captar necessidades detalhadas
- [ ] Seguir com `diva-floor-plan` para analise de planta
- [ ] Seguir com `diva-budget` para orcamento detalhado

## Questoes Pendentes
- <information needed from client>
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Diagnostico DIVA.md`

## Red flags — don't do this
- Never recommend demolishing walls without confirming they are not load-bearing
- Never skip regulatory check for Portuguese projects (RGEU/RJUE always apply)
- Never provide a single-number budget estimate (always a range)
- Never assume pre-1951 buildings are exempt from licensing without checking scope
- Never ignore asbestos risk in buildings from 1960-1990 (fibrocimento)
- Never forget condominium approval requirements for apartment projects
- Never skip the structural assessment even for "cosmetic" renovations

## Interactions
- Follow up with `diva-briefing` for detailed client requirements
- Follow up with `diva-floor-plan` for layout analysis
- Follow up with `diva-materials` for material specification
- Follow up with `diva-budget` for detailed budget breakdown
- Save via `dario-obsidian-save` to vault
