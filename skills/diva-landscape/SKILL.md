---
name: diva-landscape
description: Landscape and outdoor space design for Portuguese architecture projects. Covers garden design, terrace/patio layout, plant selection for PT climate zones, irrigation systems, outdoor living areas, pool integration, privacy screening, outdoor lighting, drainage, and hardscape specification. Triggers on "jardim", "garden", "paisagismo", "landscape", "terraco", "terrace", "outdoor", "patio", "piscina area", "espaco exterior", "varanda".
license: MIT
---

# DIVA Skill — Landscape & Outdoor Space Design

Designs comprehensive outdoor spaces for Portuguese residential and hospitality projects. Covers functional zoning of exterior areas, plant selection optimized for Portuguese climate zones and water constraints, hardscape material specification, irrigation system design, outdoor kitchen and living areas, pool integration, privacy solutions, lighting, drainage, and maintenance planning.

## When to activate

Invoke `/diva-landscape` (or trigger automatically) when:
- Project includes garden, terrace, patio, courtyard, or rooftop space
- Client asks about outdoor living, garden design, or landscaping
- Architect needs landscape plan for licensing submission
- Client wants pool area design and surrounding landscape
- Privacy screening or boundary treatment is needed
- Irrigation or drainage design for outdoor spaces
- Outdoor kitchen, lounge, or dining area specification
- Plant selection for Portuguese climate conditions

Do NOT use when:
- Project is purely interior with no outdoor component
- Agricultural landscape (orchards, vineyards — specialist domain)
- Public parks or municipal landscape (different regulatory framework)
- Only need terrace waterproofing (use `diva-inspection` Phase 3)

## Portuguese climate context

### Climate zones for plant selection

| Zone | Regions | Characteristics | Key constraints |
|---|---|---|---|
| Atlantic North | Minho, Douro Litoral | Cool winters, mild summers, high rainfall (1200-2000mm) | Shade tolerance, drainage |
| Atlantic Central | Lisboa, Estremadura | Mild winters, warm summers, moderate rain (600-800mm) | Summer drought tolerance |
| Mediterranean Interior | Alentejo, Tras-os-Montes | Cold winters, hot dry summers (<500mm) | Extreme drought tolerance |
| Mediterranean South | Algarve | Mild winters, hot summers, low rainfall (400-600mm) | Water scarcity, salt tolerance |
| Mountain | Serra da Estrela, Geres | Cold winters, cool summers | Frost resistance, altitude |

### Water context
- Portugal faces increasing drought — design for water efficiency
- Many municipalities restrict garden watering (especially Algarve, Alentejo)
- Prioritize Mediterranean/native species, mulching, drip irrigation
- Rainwater harvesting encouraged (sometimes mandatory for new builds)
- Well water (furo) common in rural areas — check water rights and quality

## Workflow

### 1. Gather landscape inputs

- **Property:** total outdoor area (m2), orientations, topography (flat/slope/terraced)
- **Climate zone:** region, microclimate (coastal, valley, hilltop, urban heat island)
- **Soil type:** clay, sandy, limestone, granite (affects drainage and planting)
- **Water source:** municipal, well (furo), borehole, rainwater tank
- **Existing vegetation:** trees to preserve (especially protected: sobreiro, azinheira)
- **Views:** to preserve, to frame, to block (neighbours, ugly wall)
- **Privacy needs:** from neighbours, from street, within garden zones
- **Functional requirements:** outdoor dining, children's play, pool, horta, parking, storage
- **Budget tier:** economico / recomendado / premium
- **Maintenance capacity:** DIY / occasional gardener / professional service
- **Style direction:** formal, informal, Mediterranean, tropical, contemporary, rustic, minimal

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "landscape design garden outdoor Portugal Mediterranean climate", limit: 5)
mcp__dario-rag__search_kb(query: "Portuguese plants garden drought tolerant native species", limit: 5)
mcp__dario-rag__search_kb(query: "outdoor living terrace patio pool design hardscape", limit: 5)
```

### 3. Functional zoning

Divide outdoor space into zones:

**Zone 1 — Transition (indoor-outdoor)**
- Covered terrace, pergola, or loggia
- Direct connection to living/dining room
- Level threshold or gentle step (accessibility — DL 163/2006 for commercial)
- Shade structure for summer protection (pergola, vela, toldo retratil)

**Zone 2 — Social (entertainment)**
- Outdoor dining (min 4x4m for 8-person table)
- Outdoor kitchen/BBQ (running water, electricity, worktop, storage)
- Lounge / seating area
- Pool deck / solarium
- Fire pit or outdoor fireplace

**Zone 3 — Active (recreation)**
- Children's play (soft surface, visible from kitchen/social)
- Lawn for play and pets
- Pool / spa
- Sports (padel court — growing trend in PT)

**Zone 4 — Productive**
- Vegetable garden / horta (min 2x3m for herbs + vegetables)
- Fruit trees (citrus, fig, olive)
- Compost area (screened from social zones)
- Clothesline (common in PT — screen with planting or structure)
- Storage shed / garden room

**Zone 5 — Contemplative**
- Stroll paths through planting
- Water feature (fonte, repuxo, tanque)
- Reading / meditation nook
- Ornamental beds

**Zone 6 — Service**
- Parking / driveway
- Waste bins (screened)
- Technical equipment (pool pump, irrigation controller, gas bottles)
- Service access

### 4. Plant palette

#### Trees (shade, structure, screening)

| Tree | Height | Water | Sun | Region | Notes |
|---|---|---|---|---|---|
| Olea europaea (Oliveira) | 8-12m | Low | Full | All | Iconic PT, evergreen, slow |
| Quercus suber (Sobreiro) | 10-15m | Low | Full | S/Central | PROTECTED (DL 169/2001) |
| Citrus spp. (limoeiro, laranjeira) | 4-8m | Medium | Full | Central/South | Fragrant, productive |
| Jacaranda mimosifolia | 8-12m | Medium | Full | Lisboa/South | Purple flowers May-Jun |
| Pinus pinea (Pinheiro manso) | 15-20m | Low | Full | Coastal | Umbrella canopy |
| Arbutus unedo (Medronheiro) | 5-8m | Low | Full/Part | All | Native, evergreen, fruit |
| Lagerstroemia indica | 5-8m | Medium | Full | All | Summer flowers, deciduous |
| Cercis siliquastrum (Olaia) | 5-8m | Low | Full | All | Pink spring flowers |
| Cupressus sempervirens | 10-20m | Low | Full | All | Vertical accent, screening |
| Celtis australis (Lodao) | 12-20m | Low | Full | Interior | Shade, drought-proof |

#### Shrubs (structure, hedging, colour)

| Shrub | Height | Water | Sun | Use |
|---|---|---|---|---|
| Lavandula spp. | 0.5-1m | Low | Full | Borders, fragrance, pollinator |
| Rosmarinus officinalis | 0.5-1.5m | Low | Full | Hedge, culinary, evergreen |
| Cistus spp. (Esteva) | 0.5-2m | Low | Full | Mass planting, native |
| Viburnum tinus | 2-4m | Low-Med | Part/Full | Screening hedge, evergreen |
| Pittosporum tobira | 2-4m | Low-Med | Full/Part | Dense screening |
| Nerium oleander | 2-4m | Low | Full | Screening, colour (TOXIC) |
| Bougainvillea spp. | 3-8m | Low | Full | Wall cover, dramatic colour |
| Myrtus communis (Murta) | 1-3m | Low | Full | Hedge, fragrance, native |
| Westringia fruticosa | 1-2m | Low | Full | Low hedge, grey foliage |
| Teucrium fruticans | 1-2m | Low | Full | Silver hedge, Mediterranean |

#### Groundcovers and perennials

| Plant | Height | Water | Sun | Use |
|---|---|---|---|---|
| Thymus serpyllum | 5-10cm | Low | Full | Path edges, lawn alternative |
| Dichondra repens | 3-5cm | Medium | Part | Lawn alternative (shade) |
| Gazania rigens | 15-30cm | Low | Full | Colour, slopes, banks |
| Agapanthus africanus | 60-80cm | Low-Med | Full/Part | Borders, pots |
| Strelitzia reginae | 1-1.5m | Medium | Full/Part | Tropical accent |
| Helichrysum italicum | 40-60cm | Low | Full | Silver, fragrant |
| Centranthus ruber | 60-80cm | Low | Full | Red/pink, walls, self-sowing |
| Erigeron karvinskianus | 20-30cm | Low | Full/Part | Cascading walls, charming |
| Convolvulus cneorum | 30-50cm | Low | Full | Silver evergreen, white flowers |

#### Climbers

| Climber | Reach | Water | Use | Support |
|---|---|---|---|---|
| Jasminum officinale | 3-6m | Low-Med | Fragrance, pergola | Wire/trellis |
| Wisteria sinensis | 10-15m | Medium | Spectacular spring flowers | Strong pergola |
| Bougainvillea | 5-10m | Low | Year-round colour | Wall/trellis |
| Trachelospermum jasminoides | 3-6m | Low-Med | Evergreen, fragrant | Wire/trellis |
| Parthenocissus tricuspidata | 10-15m | Low | Wall cover, autumn colour | Self-clinging |

### 5. Hardscape specification

**Paving options (PT market 2026 prices):**

| Material | EUR/m2 installed | Pros | Cons | Best for |
|---|---|---|---|---|
| Calcada portuguesa | 40-80 | Traditional, permeable | Uneven, weeds | Driveways, paths |
| Laje calcario/granito natural | 60-120 | Durable, elegant | Heavy, expensive | Terraces, pool decks |
| Porcelanico exterior 20mm | 50-90 | Low maintenance | Can be slippery wet | Contemporary terraces |
| Deck IPE/cumaru (madeira tropical) | 80-150 | Warm, natural | Annual oiling | Pool decks, terraces |
| Deck composito (Millboard, Fiberon) | 70-130 | Low maintenance | Less natural feel | Pool decks |
| Betonilha/microcimento exterior | 40-70 | Continuous, modern | Cracking risk, sealing | Contemporary terraces |
| Saibro compactado | 15-25 | Natural, permeable | Dusty, weed growth | Paths, rustic gardens |
| Gravilha decorativa | 10-20 | Permeable, economico | Displacement, weeds | Paths, mulch areas |
| Lajeta betao pre-fabricada | 25-45 | Economico, uniform | Basic aesthetic | Utility areas, paths |

**Boundary treatments:**

| Solution | EUR/ml | Height | Privacy | Maintenance |
|---|---|---|---|---|
| Muro rebocado + pintado | 80-200 | 1.5-2.5m | Total | Repaint 5-8 years |
| Muro pedra natural | 120-300 | 1-2m | Total | None |
| Grade metalica + trepadeira | 60-120 | 1.5-2m | Medium-High (2yr) | Annual pruning |
| Sebe Cupressocyparis/Loureiro | 20-40 | 2-4m | High (2-3 years) | Biannual trim |
| Paineis composito/madeira | 80-160 | 1.5-2m | Total | Low-Medium |
| Gabiao (stone-filled wire) | 100-180 | 1-2m | Medium | None |

**Outdoor structures:**

| Structure | EUR estimate | Notes |
|---|---|---|
| Pergola madeira (4x4m) | 2,000-5,000 | Pine treated / iroko |
| Pergola aluminio bioclimatica | 5,000-15,000 | Lamas orientaveis, motorizada |
| Churrasqueira alvenaria | 1,500-5,000 | Pré-fabricada ou custom |
| Outdoor kitchen (completa) | 5,000-25,000 | Bancada, forno, lava-louca, frigorífico |
| Cabanon / garden room | 3,000-15,000 | Arrumos, atelier, escritorio |
| Piscina (6x3m, fibra) | 15,000-25,000 | Incluindo equipamento |
| Piscina (betao, custom) | 25,000-60,000+ | Design livre, revestimento a escolher |

### 6. Irrigation system

**Design principles:**
- Hydrozoning: group plants by water needs (zones separadas)
- Drip irrigation for beds, trees, shrubs (90-95% efficient)
- Pop-up sprinklers only for lawn (70-80% efficient)
- Smart controller with rain sensor + soil moisture (Hunter, Rain Bird, Gardena)
- Schedule: early morning (6-8h) to minimize evaporation
- Rainwater tank: 1,000-5,000L (underground PE or surface)

**System specification per zone:**

| Zone | Method | Spacing | Frequency summer | Flow |
|---|---|---|---|---|
| Lawn (relvado) | Pop-up sprinklers | 4-5m | 3x/week, 20min | 15-20L/m2/week |
| Shrub beds | Drip line 16mm | 30-50cm emitters | 2x/week, 45min | 5-8L/m2/week |
| Trees (individual) | Ring drip / bubbler | 1 per tree | 1x/week, 60min | 30-50L/tree |
| Horta | Drip line 16mm | 30cm emitters | Daily, 20min | 8-10L/m2/week |
| Pots/vasos | Drip emitters | 1-2 per pot | Daily, 10min | Per pot size |

**Controller brands (PT available):** Hunter Pro-HC, Rain Bird ESP-ME3, Gardena Smart, Netafim

### 7. Outdoor lighting

| Layer | Purpose | Fixture type | IP rating | Colour temp |
|---|---|---|---|---|
| Pathway | Safety, wayfinding | Bollards, recessed ground | IP65+ | 2700-3000K |
| Feature | Trees, walls, sculpture | Spike spots, wall washers | IP65+ | 2700K |
| Social | Dining, lounge | String lights, pendants, lanterns | IP44+ | 2200-2700K |
| Security | Perimeter, entries | Floodlights + PIR | IP65+ | 4000K |
| Pool | Safety, ambiance | Underwater LED, deck recessed | IP68 | 3000K / RGB |
| Steps | Safety | Recessed wall, tread lights | IP65+ | 3000K |

All exterior: LED, IP65+ minimum (IP68 for pool/water), 12V for pool zones per RTIEBT.
Dark-sky friendly (downward-directed) fixtures recommended — increasingly required.

### 8. Drainage

- Surface fall: 1-2% away from building on all hardscape
- Channel drains: terrace-building junction, garage entries, low points
- French drains: perimeter of garden beds against building walls
- Soakaway / infiltration pit: for permeable surfaces and roof water overflow
- Rainwater collection: downpipes to storage tank before overflow to municipal system
- Retaining walls: drainage behind (geotextile + gravel + weep holes at 2m spacing)
- Pool backwash: to sewer (never to garden — chemicals)

### 9. Legal and regulatory

- **Protected trees:** Sobreiro and Azinheira require ICNF authorization before removal (DL 169/2001). Fines EUR 250-50,000 per tree
- **Pool:** some municipalities require comunicacao previa or licenciamento for pools >10m2
- **Boundary walls:** maximum height per PDM (typically 1.5-2.5m), verify with camara
- **Water features:** check municipal regulations for water usage
- **Outdoor lighting:** respect neighbour nuisance laws, dark-sky requirements
- **Terrace on apartment:** condominium rules, structural load limits, waterproofing responsibility

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: diva-landscape
area_exterior_m2: <number>
climate_zone: <atlantic|mediterranean|mountain>
style: <formal|informal|contemporary|mediterranean|rustic>
budget_tier: <economico|recomendado|premium>
tags: [paisagismo, jardim, exterior, <project>]
---

# Projecto de Paisagismo DIVA — <Project Name>

## 1. Contexto
- **Area exterior total:** <X> m2
- **Orientacao predominante:** <N/S/E/W>
- **Zona climatica:** <zone>
- **Solo:** <type>
- **Agua disponivel:** <municipal/furo/pluvial>
- **Vegetacao existente a preservar:** <list>

## 2. Zonamento Funcional
| Zona | Area (m2) | Funcao | Localizacao |
|---|---|---|---|
| Transicao | <X> | Terraco coberto | Junto a sala |
| Social | <X> | Refeicoes, lounge, BBQ | Sul/Poente |
| Activa | <X> | Piscina, relvado | Centro |
| Produtiva | <X> | Horta, fruteiras | Servico |
| Contemplativa | <X> | Passeio, fonte | Sombra |
| Servico | <X> | Estacionamento, tecnica | Entrada |

## 3. Paleta Vegetal

### Arvores
| Especie | Local | Qtd | Funcao |
|---|---|---|---|
| ... | ... | ... | Sombra/enquadramento/producao |

### Arbustos e sebes
| Especie | Local | Qtd/ml | Funcao |
|---|---|---|---|
| ... | ... | ... | Sebe/cor/fragancia |

### Herbaceas e revestimento
| Especie | Local | Area m2 | Funcao |
|---|---|---|---|
| ... | ... | ... | Cobertura/cor/aroma |

### Trepadeiras
| Especie | Suporte | Local | Funcao |
|---|---|---|---|
| ... | Pergola/muro | ... | Sombra/fragancia |

## 4. Pavimentos e Estruturas

### Pavimentos
| Zona | Material | Area m2 | EUR/m2 | Total EUR |
|---|---|---|---|---|
| Terraco principal | ... | ... | ... | ... |
| Caminhos | ... | ... | ... | ... |
| Pool deck | ... | ... | ... | ... |

### Estruturas
| Estrutura | Material | Dimensoes | EUR |
|---|---|---|---|
| Pergola | ... | ... | ... |
| Muro limite | ... | ... | ... |
| BBQ/outdoor kitchen | ... | ... | ... |

## 5. Sistema de Rega
| Zona | Metodo | Controlador | Frequencia verao |
|---|---|---|---|
| Relvado | Pop-up | Smart | 3x/semana |
| Canteiros | Gota-a-gota | Smart | 2x/semana |
| Arvores | Emissores | Smart | 1x/semana |
| Horta | Gota-a-gota | Smart | Diario |

### Deposito pluvial: <X> L, <tipo>

## 6. Iluminacao Exterior
| Zona | Luminaria | Qtd | IP | Controlo |
|---|---|---|---|---|
| Caminhos | Balizadores | <N> | IP65 | Crepuscular |
| Arvores | Projetores | <N> | IP65 | Crepuscular |
| Social | String/pendentes | <N> | IP44 | Dimmer |
| Seguranca | Projetores PIR | <N> | IP65 | Movimento |

## 7. Drenagem
- Pendentes hardscape: <spec>
- Caleiras: <locations>
- Deposito pluvial: <spec>

## 8. Orcamento Estimativo
| Componente | EUR |
|---|---|
| Pavimentos e estruturas | <X> |
| Plantacao (fornecimento + plantio) | <X> |
| Rega (sistema completo) | <X> |
| Iluminacao exterior | <X> |
| Drenagem | <X> |
| Mobiliario exterior | <X> |
| Piscina (se aplicavel) | <X> |
| **Total paisagismo** | **EUR X** |

## 9. Plano de Manutencao
| Tarefa | Frequencia | Epoca | Custo anual |
|---|---|---|---|
| Poda sebes | 2x/ano | Mar + Set | EUR X |
| Corte relvado | Semanal | Mar-Out | EUR X |
| Adubacao | 2-3x/ano | Mar, Jun, Set | EUR X |
| Manutencao rega | 1x/ano | Marco | EUR X |

## 10. Proximos Passos
- [ ] Cliente valida zonamento e paleta vegetal
- [ ] Solicitar orcamentos a paisagistas/viveiristas
- [ ] Coordenar com `diva-mep` para infra rega e electricidade exterior
- [ ] Coordenar com `diva-budget` para incluir no orcamento global
- [ ] Definir epoca de plantacao (Outono ideal em PT)
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Paisagismo DIVA.md`

## Red flags — don't do this
- Never specify a garden without considering summer drought — Portugal's Mediterranean climate means 3-5 months with minimal rainfall, and any planting plan without irrigation or drought-tolerant species will fail by August
- Never remove or damage sobreiro (Quercus suber) or azinheira (Quercus rotundifolia) without ICNF authorization — these are legally protected in Portugal (DL 169/2001), fines EUR 250-50,000 per tree
- Never design hardscape without drainage away from the building — water pooling against foundations is the number one cause of structural dampness in PT
- Never specify conventional lawn as primary ground cover in Algarve/Alentejo — it consumes 6-8 L/m2/day in summer and is unsustainable; use thyme, dichondra, or gravel alternatives
- Never ignore condominium rules for apartment terraces — load limits, waterproofing, drainage, and planting depth all apply
- Never forget pool equipment noise impact on neighbours — pumps and heat pumps are common dispute sources in Portugal
- Never plant invasive species (Acacia dealbata, Cortaderia selloana, Arundo donax) — they are prohibited under Portuguese law and spread aggressively

## Interactions
- Usually follows `diva-briefing` (outdoor preferences) and `diva-floor-plan` (indoor-outdoor flow)
- Feeds into `diva-budget` for landscape cost inclusion in total project budget
- Coordinates with `diva-mep` for outdoor electrical, water supply, and drainage infrastructure
- Coordinates with `diva-smart-home` for outdoor automation (irrigation, lighting, pool)
- References `diva-materials` for hardscape consistency with interior palette
- Save via `diva-obsidian-save` to vault
