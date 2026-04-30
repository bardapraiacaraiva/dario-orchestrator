---
name: diva-acoustics
description: Acoustic design and sound insulation for architecture and construction projects in Portugal. Covers RRAE compliance, airborne and impact sound insulation (DnT,w / L'nT,w), equipment noise (LAr,nT), acoustic classification, material specification, and pre-construction acoustic planning. Triggers on "acustica", "acoustics", "RRAE", "isolamento sonoro", "ruido", "som", "insonorizacao", "sound insulation", "barulho vizinhos".
license: MIT
---

# DIVA Skill — Acoustic Design & Sound Insulation (RRAE)

Comprehensive acoustic analysis and specification for Portuguese construction projects under the RRAE (Regulamento dos Requisitos Acusticos dos Edificios). Covers regulatory compliance assessment, sound insulation design for airborne and impact noise, equipment noise control, material specification with Portuguese suppliers, and coordination with other building systems (MEP, structure, partitions).

## When to activate

Invoke `/diva-acoustics` (or trigger automatically) when:
- User asks about sound insulation between apartments or rooms
- User mentions noise problems (neighbours, equipment, street noise)
- New construction or major renovation requiring RRAE compliance
- User needs acoustic specialty project documentation
- Architect needs to specify acoustic solutions for partitions, floors, or facades
- User asks about noise regulations in Portugal
- Mixed-use buildings (residential above commercial/restaurant)
- User mentions "regulamento acustica" or RRAE

Do NOT use when:
- Purely interior design aesthetics with no acoustic concern (use `diva-moodboard`)
- Room acoustics for professional studios/auditoriums (specialist domain)
- Environmental noise assessment (EIA) for urban planning

## Regulatory framework

### RRAE (DL 96/2008, updated by DL 129/2002 original)
The primary acoustic regulation for Portuguese buildings:

| Parameter | Symbol | What it measures |
|---|---|---|
| Airborne sound insulation (between dwellings) | DnT,w | dB reduction of voices, TV, music through walls/floors |
| Airborne sound insulation (facade) | D2m,nT,w | dB reduction of exterior noise (traffic, aircraft) |
| Impact sound insulation | L'nT,w | Impact noise level in receiving room (lower = better) |
| Equipment noise | LAr,nT | Noise from building equipment (elevators, HVAC, plumbing) |
| Reverberation time | T | Sound decay time in common areas |

### Minimum requirements (residential — habitacao)

| Element | Requirement | Notes |
|---|---|---|
| Partition between dwellings | DnT,w >= 50 dB | Wall or floor between different fractions |
| Partition dwelling/common areas | DnT,w >= 48 dB | Wall to stairwell, corridor, garage |
| Partition dwelling/commercial | DnT,w >= 58 dB | Residential above shops, restaurants |
| Facade (quiet zones, D < 55 dB Lden) | D2m,nT,w >= 28 dB | Rural, residential streets |
| Facade (moderate zones, 55-65 dB Lden) | D2m,nT,w >= 33 dB | Urban residential |
| Facade (noisy zones, >65 dB Lden) | D2m,nT,w >= 33 dB + correction | Near highways, airports |
| Impact sound (between dwellings) | L'nT,w <= 60 dB | Floor impact from upstairs |
| Equipment noise (continuous, HVAC) | LAr,nT <= 32 dB(A) | In receiving habitable room |
| Equipment noise (intermittent, elevator) | LAr,nT <= 40 dB(A) | In receiving habitable room |

### Classification system (NP 4499 — optional but adds value)

| Class | Quality | Typical application |
|---|---|---|
| Classe A | Excellent | Premium housing, >10 dB above RRAE |
| Classe B | Good | Quality housing, >5 dB above RRAE |
| Classe C | Standard | Meets RRAE minimum |
| Classe D | Below standard | Pre-existing, does not meet RRAE |

## Workflow

### 1. Gather acoustic inputs

From project documentation or site visit:
- **Building type:** residential, commercial, mixed, hotel, school
- **Location noise:** quiet street, busy avenue, near highway/airport/railway
- **Noise map data:** Lden and Ln values from municipal noise map (mapa de ruido)
- **Building structure:** concrete frame, steel, masonry, wood
- **Floor system:** solid slab, hollow-core, ribbed, composite
- **Existing conditions:** if renovation, what is the current construction
- **Critical adjacencies:** residential above restaurant? bedroom next to elevator shaft?
- **MEP systems:** HVAC type, elevator, plumbing risers, transformer
- **Client sensitivity:** standard compliance, enhanced comfort, or maximum isolation

If location noise data is missing, check the municipal noise map (mapa de ruido) at the Camara Municipal website.

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "RRAE acoustic insulation sound regulation Portugal DnT L'nT", limit: 5)
mcp__dario-rag__search_kb(query: "sound insulation materials partition floor ceiling Portugal", limit: 5)
mcp__dario-rag__search_kb(query: "acoustic design construction floating floor resilient layer", limit: 5)
```

### 3. Acoustic analysis by element

#### 3.1 Party walls (paredes entre fracoes)
Evaluate and specify:

| Solution | Approx. DnT,w | Cost EUR/m2 | Thickness mm |
|---|---|---|---|
| Double masonry 11+11 + air gap 4cm | 48-50 dB | 25-35 | 260 |
| Double masonry 11+11 + mineral wool 4cm | 52-54 dB | 30-40 | 260 |
| Double masonry 15+11 + mineral wool 5cm | 54-56 dB | 35-45 | 310 |
| Concrete 20cm + pladur + MW 5cm (one side) | 56-58 dB | 45-55 | 270 |
| Double pladur 2x13 + MW 7cm + pladur 2x13 (independent frames) | 58-62 dB | 50-70 | 200 |
| Concrete 20cm + independent pladur both sides | 62-65 dB | 60-80 | 320 |

Key principles:
- Mass-spring-mass is more efficient than mass alone
- Air gap or mineral wool decoupling is essential
- Avoid rigid connections between leaves (flanking paths)
- Seal all perimeter joints with acoustic sealant (no rigid contact)

#### 3.2 Floors (pavimentos entre pisos)

**Airborne insulation (DnT,w):**
Solid concrete slab provides good airborne insulation (typically 52-56 dB for 20-25cm):
- Additional mass (screed) improves further
- Suspended ceiling with mineral wool adds 5-10 dB

**Impact insulation (L'nT,w) — the critical challenge:**

| Solution | Approx. L'nT,w improvement | Cost EUR/m2 |
|---|---|---|
| Resilient underlay 5mm (PE foam) | 15-18 dB | 3-5 |
| Resilient underlay 10mm (crosslinked PE) | 18-22 dB | 5-8 |
| Mineral wool 20mm under screed (floating floor) | 22-28 dB | 8-15 |
| Rubber crumb mat 15mm under screed | 25-30 dB | 12-18 |
| Combination: resilient mat + floating screed + resilient underlay | 30-35 dB | 18-30 |
| Full floating floor system (Sylomer/Sylodyn) | 35-40 dB | 25-40 |

Critical floating floor rules:
- Screed must NOT touch any wall (banda resiliente perimetral obrigatoria)
- All penetrations (pipes, columns) wrapped with resilient material
- Minimum screed thickness over resilient layer: 5cm (recommended 6-7cm)
- Floor heating pipes IN the floating screed, not below resilient layer

#### 3.3 Facade (fachada)

Facade insulation depends on:
- Wall mass and insulation (ETICS helps acoustically too)
- Window acoustic class (the weakest link)
- Ventilation openings (biggest acoustic vulnerability)
- Rolling shutter boxes (caixas de estore — major flanking path in PT construction)

Window acoustic classes:

| Glass composition | Rw (dB) | Best for |
|---|---|---|
| 4/16/4 standard double | 29-31 | Quiet zones |
| 6/16/4 asymmetric double | 33-35 | Moderate zones |
| 8/16/6 asymmetric double | 35-37 | Urban zones |
| 6/16/44.2 laminated | 37-39 | Busy roads |
| 8/20/66.2 laminated acoustic | 40-44 | Highways, airports |
| Secondary glazing (double window system) | 45-50+ | Maximum insulation |

Caixa de estore acoustic treatment:
- Standard box: acoustic disaster (-8 to -12 dB penalty)
- Insulated box (EPS/XPS lining): -3 to -5 dB penalty
- Compact box (monoblock systems): -2 to -3 dB penalty
- Exterior blinds (no box penetration): 0 dB penalty (ideal)

#### 3.4 MEP noise control

| Source | Typical issue | Solution |
|---|---|---|
| HVAC units (splits) | Compressor vibration, airflow noise | Anti-vibration mounts, flex connections, silencers |
| Elevator | Motor room noise, guide rail impact | Floating motor room floor, resilient rail fixings |
| Plumbing risers | Water hammer, flow noise | Acoustic pipe clamps, lagging, low-velocity design |
| Waste water | Drain noise through floors | Acoustic pipe (dB+ systems), shaft infill |
| Ventilation ducts | Airflow noise, fan noise | Duct silencers, flexible connections, lined ducts |
| Transformer | Low-frequency hum | Isolated room, floating floor, resilient mounts |

### 4. Flanking transmission analysis

Even perfect partitions fail if flanking paths exist:

| Flanking path | Risk level | Mitigation |
|---|---|---|
| Continuous floor slab | High | Floating floor both sides of partition |
| Concrete frame (pillar/beam junction) | High | Resilient junction detail, pladur lining |
| Continuous ceiling void | Medium | Partition extends to structural slab above ceiling |
| Service penetrations (pipes, ducts, cables) | High | Seal with intumescent/acoustic sealant |
| Caixa de estore continuous between fractions | High | Separate boxes, acoustic break |
| Back-to-back electrical boxes | Medium | Offset boxes, acoustic putty pads |
| Door undercuts | Low-Medium | Acoustic door seals, drop seals |

### 5. Specification and material selection

Portuguese suppliers and products:

| Product type | Brands available in PT | Application |
|---|---|---|
| Mineral wool (acoustic grade) | Knauf Insulation, Isover, Rockwool | Cavity fill, ceiling, floating floor |
| Resilient underlays | Impactodan (Danosa), Fonodan, Sylomer (CDM) | Under screed, under flooring |
| Acoustic sealant | Sika Acoustic Seal, Mapei Mapesil AC | Perimeter joints, penetrations |
| Resilient channels/clips | Knauf UA, Gyproc GR | Ceiling and wall decoupling |
| Acoustic plasterboard | Knauf Silentboard, Gyproc AcoustiGips | Enhanced mass partitions |
| Acoustic pipe systems | Geberit dB20, Wavin AS+ | Waste water, risers |
| Banda resiliente | Knauf, Danosa, Imperalum | Floating floor perimeter strip |
| Acoustic doors | Vicaima (PT manufacturer), Jeldwen | Internal and entrance doors |
| Acoustic windows | Cortizo (PT), Reynaers, Schuco | Facade glazing |

### 6. Pre-construction acoustic specifications

Include in caderno de encargos:
1. **Party wall construction detail** — exact layers, materials, fixing method
2. **Floating floor specification** — resilient layer, screed type/thickness, banda resiliente
3. **Facade/window acoustic class** — minimum Rw per facade orientation
4. **Caixa de estore treatment** — insulation type, or specify exterior blinds
5. **MEP vibration isolation** — mount types, flexible connections
6. **Penetration sealing protocol** — every pipe/cable through acoustic partition sealed
7. **In-situ testing requirement** — post-construction verification to RRAE

### 7. Post-construction verification

RRAE compliance must be verified by acoustic testing:
- **Who tests:** Engenheiro acustico (LNEC or accredited laboratory)
- **When:** After construction, before autorizacao de utilizacao
- **Tests:** DnT,w, L'nT,w, D2m,nT,w, LAr,nT (as applicable)
- **Report:** Ensaio acustico report submitted to Camara Municipal
- **Cost:** 500-2,000 EUR depending on number of tests

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: diva-acoustics
building_type: <residential|commercial|mixed>
rrae_zone: <quiet|moderate|noisy>
target_class: <C-standard|B-enhanced|A-premium>
tags: [acustica, RRAE, isolamento, <project>]
---

# Projecto Acustico DIVA — <Project Name>

## Resumo
| Parametro | Valor |
|---|---|
| Tipo de edificio | <type> |
| Zona de ruido | <Lden dB> — <quiet/moderate/noisy> |
| Classe alvo | <C/B/A> |
| Regulamento aplicavel | RRAE (DL 96/2008) |

## Requisitos RRAE Aplicaveis
| Elemento | Parametro | Requisito minimo | Alvo projecto |
|---|---|---|---|
| Parede entre fracoes | DnT,w | >= 50 dB | >= <X> dB |
| Parede fracao/zonas comuns | DnT,w | >= 48 dB | >= <X> dB |
| Pavimento entre fracoes (impacto) | L'nT,w | <= 60 dB | <= <X> dB |
| Fachada | D2m,nT,w | >= <X> dB | >= <X> dB |
| Ruido equipamentos (continuo) | LAr,nT | <= 32 dB(A) | <= <X> dB(A) |
| Ruido equipamentos (intermitente) | LAr,nT | <= 40 dB(A) | <= <X> dB(A) |

## Solucoes Construtivas

### Paredes entre fracoes
| Camada | Material | Espessura | Funcao |
|---|---|---|---|
| ... | ... | ... | ... |
**DnT,w estimado:** <X> dB (margem: +<X> dB vs requisito)

### Pavimento flutuante
| Camada | Material | Espessura | Funcao |
|---|---|---|---|
| Laje estrutural | Betao armado | <X> cm | Massa |
| Camada resiliente | <product> | <X> mm | Desacoplamento |
| Banda resiliente perimetral | <product> | <X> mm | Isolamento lateral |
| Betonilha flutuante | Argamassa | <X> cm | Massa flutuante |
| Acabamento | <flooring> | <X> mm | Revestimento final |
**L'nT,w estimado:** <X> dB (margem: -<X> dB vs requisito)

### Fachada
| Elemento | Composicao | Rw estimado |
|---|---|---|
| Parede | <composition> | <X> dB |
| Vidro | <glass composition> | <X> dB |
| Caixa estore | <treatment> | <X> dB |
**D2m,nT,w estimado:** <X> dB

### Controlo de ruido MEP
| Equipamento | Fonte ruido | Solucao | LAr,nT estimado |
|---|---|---|---|
| ... | ... | ... | ... |

## Detalhes Construtivos Criticos
### Juncao parede-pavimento
### Juncao parede-teto
### Penetracoes (tubagens, cabos)
### Caixas electricas em paredes acusticas
### Caixas de estore

## Transmissoes Marginais (Flanking)
| Caminho | Risco | Mitigacao |
|---|---|---|
| ... | ... | ... |

## Materiais e Fornecedores
| Material | Referencia | Fornecedor PT | EUR/m2 ou unid |
|---|---|---|---|
| ... | ... | ... | ... |

## Estimativa de Custo Acustico
| Item | Area/Qtd | EUR/m2 | Total EUR |
|---|---|---|---|
| Isolamento paredes entre fracoes | ... | ... | ... |
| Pavimento flutuante | ... | ... | ... |
| Tratamento fachada (janelas acusticas) | ... | ... | ... |
| Tratamento caixas estore | ... | ... | ... |
| Isolamento MEP | ... | ... | ... |
| Ensaio acustico pos-obra | 1 | ... | ... |
| **Total** | | | **EUR X** |

## Ensaio Pos-Obra
- **Laboratorio:** <LNEC / accredited>
- **Ensaios requeridos:** DnT,w / L'nT,w / D2m,nT,w / LAr,nT
- **Custo estimado:** EUR <X>
- **Prazo:** agendar 2-3 semanas antes da vistoria CM

## Proximos Passos
- [ ] Incluir detalhes acusticos no projecto de especialidades
- [ ] Especificar solucoes nos mapas de trabalhos e caderno de encargos
- [ ] Coordenar com `diva-mep` para isolamento de equipamentos
- [ ] Verificar compatibilidade com `diva-energy` (isolamento termico e acustico partilham camadas)
- [ ] Agendar ensaio acustico pos-obra com laboratorio acreditado
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Projecto Acustico DIVA.md`

## Red flags -- don't do this
- Never ignore caixas de estore (rolling shutter boxes) -- they are the number one acoustic failure point in Portuguese residential construction, creating flanking paths that can reduce facade insulation by 8-12 dB
- Never specify a floating floor without banda resiliente perimetral -- if the screed touches any wall, the entire floating floor system is acoustically short-circuited and impact insulation drops to near zero
- Never assume a thick wall means good acoustic insulation -- a 30cm single-leaf masonry wall (DnT,w ~45 dB) performs worse than a properly decoupled 20cm double-leaf system (DnT,w ~55 dB) because mass alone cannot match mass-spring-mass
- Never forget flanking transmission analysis -- the best partition in the world fails if sound travels around it through the continuous floor slab, ceiling void, or service penetrations
- Never skip post-construction acoustic testing for new builds or major rehabilitations -- RRAE compliance is verified by in-situ measurement, and design estimates routinely differ from reality by 3-5 dB due to workmanship quality
- Never place back-to-back electrical boxes in acoustic partitions -- each unprotected box creates a ~5 dB penalty, and Portuguese electricians default to back-to-back unless explicitly instructed otherwise
- Never confuse thermal insulation with acoustic insulation -- EPS (esferovite) is excellent thermal but poor acoustic; mineral wool (la de rocha) provides both thermal and acoustic performance

## Interactions
- Coordinates with `diva-energy` -- thermal and acoustic insulation often share the same building layers (walls, roof, windows)
- Feeds into `diva-materials` -- acoustic material specifications become part of the material palette
- Feeds into `diva-budget` -- acoustic solutions add cost that must be included in the budget chapter breakdown
- Coordinates with `diva-mep` -- equipment noise control requires MEP coordination
- Referenced by `diva-licensing` -- RRAE is a mandatory specialty project for licenciamento
- Tested during `diva-inspection` -- Phase 3 (item 3.6) covers acoustic insulation checks
- Save via `diva-obsidian-save` to vault
