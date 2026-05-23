---
name: diva-mep
description: MEP (Mechanical, Electrical, Plumbing) coordination and specification for architecture and construction projects in Portugal. Covers electrical design (RTIEBT/ITED), plumbing layout (water supply and drainage), HVAC system selection and sizing, gas installation, ventilation, fire safety systems (SCIE), and coordination between all building services. Triggers on "MEP", "instalacoes", "electricidade", "canalizacao", "AVAC", "ar condicionado", "ventilacao", "redes", "especialidades", "quadro electrico", "ITED", "plumbing", "heating", "aquecimento".
license: MIT
---

# DIVA Skill — MEP Coordination & Specification

Designs and coordinates Mechanical, Electrical, and Plumbing systems for Portuguese construction projects. Covers electrical distribution (RTIEBT compliance), telecommunications (ITED), water supply and drainage networks, HVAC system selection and sizing, gas installation, mechanical ventilation, fire safety (SCIE/RJSCIE), and cross-discipline coordination to prevent conflicts during construction.

## When to activate

Invoke `/diva-mep` (or trigger automatically) when:
- New construction or major renovation needs MEP design
- Client asks about electrical capacity, heating/cooling, or plumbing layout
- Architect needs MEP coordination for specialty projects (projectos de especialidades)
- Specifying HVAC systems (splits, VRV, floor heating, central)
- Kitchen or bathroom design requires plumbing coordination
- Electrical panel design or upgrade
- ITED telecommunications infrastructure planning
- Fire safety system specification (SCIE)
- Coordinating between MEP disciplines to avoid conflicts

Do NOT use when:
- Only need smart home automation (use `diva-smart-home`)
- Only need energy certification (use `diva-energy`)
- Only need construction inspection of MEP (use `diva-inspection` Phase 4)
- Engineering calculations requiring licensed engineer stamp (this skill provides specification and coordination, not structural/MEP engineering calculations)

## Regulatory framework

| Regulation | Scope | Key content |
|---|---|---|
| RTIEBT | Electrical installations | Rules for low-voltage installations |
| ITED 4a edicao | Telecommunications | In-building telecom infrastructure |
| RGSPPDADAR | Water supply and drainage | Water and wastewater network rules |
| DL 521/99 + Portarias | Gas installations | Natural gas and LPG rules |
| RJSCIE (DL 220/2008) | Fire safety | Active and passive fire protection |
| RSECE / RECS | HVAC systems | Ventilation and AC requirements |
| EN 12831 | Heating loads | Heating calculation method |
| EN 15243 | Cooling loads | Cooling calculation method |

## Workflow

### 1. Gather MEP inputs

- **Building type:** residential, commercial, hospitality, mixed
- **Area and number of floors:** total conditioned area
- **Floor plan:** from `diva-floor-plan` (room dimensions, wall positions)
- **Structural system:** from `diva-diagnose` (available ceiling voids, riser positions)
- **Number of dwellings/units:** for sizing
- **Existing infrastructure (if renovation):** electrical capacity, plumbing routes, gas availability
- **Client requirements:** specific equipment, heating preference, cooking fuel
- **Energy goals:** from `diva-energy` (target energy class, renewable integration)
- **Smart home:** from `diva-smart-home` (additional wiring, panel space)
- **Budget tier:** economico / recomendado / premium

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "MEP mechanical electrical plumbing coordination construction", limit: 5)
mcp__dario-rag__search_kb(query: "RTIEBT ITED electrical installation Portugal residential", limit: 5)
mcp__dario-rag__search_kb(query: "HVAC system selection heating cooling Portugal residential", limit: 5)
```

### 3. Electrical system design

#### 3.1 Power supply and distribution

**Residential supply levels (typical PT):**

| Type | Supply | Breaker | Typical use |
|---|---|---|---|
| Monofasico 3.45kVA | 1-phase, 15A | 1x15A | Small apartment, no AC |
| Monofasico 6.9kVA | 1-phase, 30A | 1x30A | Medium apartment |
| Monofasico 10.35kVA | 1-phase, 45A | 1x45A | Large apartment with AC |
| Trifasico 10.35kVA | 3-phase, 3x15A | 3x15A | Moradia small |
| Trifasico 13.8kVA | 3-phase, 3x20A | 3x20A | Moradia medium |
| Trifasico 20.7kVA | 3-phase, 3x30A | 3x30A | Moradia large, EV, heat pump |
| Trifasico 34.5kVA | 3-phase, 3x50A | 3x50A | Large moradia, pool, full AC |

**Electrical panel (quadro electrico) design:**
- Main switch (interruptor geral): sized to supply contract
- Differential switches (diferenciais): 30mA for personal protection, 300mA for fire
  - Minimum 2 differentials (circuits split to avoid total blackout)
  - Type A or AC depending on equipment (Type A for inverter loads: AC, EV)
- Circuit breakers (disjuntores): one per circuit, sized by cable and load
- Surge protection (SPD Type 2): recommended for all, mandatory with PV

**Circuit layout (typical residential):**

| Circuit | Breaker | Cable | Outlets/Points | Notes |
|---|---|---|---|---|
| Iluminacao sala/quartos | 10A | 1.5mm2 | All lights zone 1 | Max 8 points per circuit |
| Iluminacao cozinha/WC | 10A | 1.5mm2 | All lights zone 2 | Separate for wet zones |
| Tomadas gerais sala | 16A | 2.5mm2 | Max 8 tomadas | Ring or radial |
| Tomadas gerais quartos | 16A | 2.5mm2 | Max 8 tomadas | Separate circuit per zone |
| Tomadas cozinha (bancada) | 16A | 2.5mm2 | 4-6 tomadas bancada | High-load zone |
| Forno / placa | 20-32A | 4-6mm2 | 1 dedicado | Always dedicated circuit |
| Maquina lavar roupa | 16A | 2.5mm2 | 1 dedicado | Dedicated, near water |
| Maquina lavar louca | 16A | 2.5mm2 | 1 dedicado | Dedicated |
| Esquentador/caldeira | 16A | 2.5mm2 | 1 dedicado | Dedicated |
| Ar condicionado (por unidade) | 16-20A | 2.5-4mm2 | 1 por split | Dedicated per unit |
| Piso radiante | 16-20A | 2.5-4mm2 | 1 por zona | Via termostato |
| Bomba de calor | 20-32A | 4-6mm2 | 1 dedicado | Trifasico if >5kW |
| Carregador EV | 32A | 6mm2 | 1 dedicado | Trifasico recommended |
| Domotica/rede | 16A | 2.5mm2 | 1 dedicado | UPS recommended |
| Exterior (jardim, portao) | 16A | 2.5mm2 | Outdoor outlets | With differential 30mA |

**Point quantities per room (minimum recommended):**

| Room | Tomadas | Pontos luz | TV/dados | Especial |
|---|---|---|---|---|
| Sala | 8-12 | 3-5 | 2 | Ar condicionado |
| Cozinha | 6-10 (bancada) + 4 | 3-4 | 1 | Forno, placa, ML, MLL, exaustor |
| Suite | 6-8 | 3-4 | 1 | AC, USB cabeceira |
| Quarto | 4-6 | 2-3 | 1 | AC |
| WC | 2-3 | 2-3 | 0 | Toalheiro, espelho iluminado |
| Hall | 2-4 | 2-3 | 1 | Videoporteiro, alarme |
| Lavandaria | 3-4 | 1-2 | 0 | ML, secadora |
| Escritorio | 6-8 | 2-3 | 2 | UPS, dados |
| Exterior | 2-4 | 2-4 | 0 | IP65, PIR |

#### 3.2 ITED telecommunications

Mandatory for new builds and major renovations:

**ATI (Armario de Telecomunicacoes Individual):**
- Location: near electrical panel, accessible, ventilated
- Minimum size: 500x400x120mm (residential)
- Contains: patch panel, switch, fiber termination, coax distributor

**Cabling per room:**

| Room | Cat6A | Coax | Fibra | Notes |
|---|---|---|---|---|
| Sala | 2 | 1 | 1 | TV + internet + spare |
| Suite | 1 | 1 | 0 | Internet + TV |
| Quarto | 1 | 0 | 0 | Internet |
| Escritorio | 2 | 0 | 1 | Internet x2 + fiber |
| Cozinha | 1 | 0 | 0 | Smart appliances |
| Exterior/camara | 1 per camera | 0 | 0 | PoE for cameras |

### 4. Plumbing system design

#### 4.1 Water supply (abastecimento de agua)

**Pipe sizing principles:**
- Main entry: 25-32mm (depending on simultaneous use)
- Branch to kitchen: 20mm
- Branch to bathroom: 20mm (hot + cold)
- Individual fixtures: 16mm (taps), 20mm (bath/shower)

**Pipe materials (PT market):**

| Material | Use | Pros | Cons | Price range |
|---|---|---|---|---|
| Multicamada (PEX-Al-PEX) | Hot + cold supply | Easy install, flexible, no corrosion | UV-sensitive, fitting cost | EUR 2-5/ml |
| PPR (polipropileno) | Hot + cold supply | Welded joints (no leaks), cheap | Rigid, more space | EUR 1-3/ml |
| PEX | Hot + cold, floor heating | Flexible, oxygen barrier | Fittings expensive | EUR 2-4/ml |
| Copper | Hot + cold supply | Durable, antibacterial | Expensive, corrosion in acidic water | EUR 5-12/ml |
| Inox (AISI 316) | Premium installations | Premium finish, durable | Very expensive | EUR 8-15/ml |

**Hot water systems:**

| System | Efficiency | Cost | Best for |
|---|---|---|---|
| Esquentador (gas instantaneo) | 85-90% | EUR 300-800 | Small apartment, immediate |
| Caldeira mural (gas) | 90-95% | EUR 800-2,000 | Medium dwelling, heating combo |
| Caldeira condensacao | 95-108% | EUR 1,500-3,000 | Large dwelling, high efficiency |
| Bomba de calor AQS | COP 2.5-4.0 | EUR 1,500-3,500 | Energy-conscious, renewable |
| Termoacumulador electrico | 95-98% | EUR 200-600 | No gas, backup system |
| Solar termico + apoio | 50-70% solar | EUR 2,000-4,000 | Mandatory for new builds |

#### 4.2 Drainage (drenagem de aguas residuais)

**Pipe sizing:**
- Sanita: 100-110mm
- Base duche / banheira: 50-75mm
- Lavatorio: 40-50mm
- Lava-louca: 50mm
- Maquina lavar: 40-50mm
- Coluna principal (prumada): 100-110mm

**Slopes:** minimum 1% (recommended 2%) for horizontal runs

**Key rules:**
- Every fixture needs a sifao (trap) — minimum 50mm water seal
- Ventilation of drainage system (tubo de ventilacao or AAV — Admittance Air Valve)
- Avoid horizontal runs >4m without cleanout access
- WC should connect directly to main stack (shortest run)
- Kitchen grease trap recommended for restaurants (mandatory)

#### 4.3 Rainwater (aguas pluviais)

- Separate system from wastewater (sistema separativo — mandatory in most PT municipalities)
- Gutter sizing based on roof area and rainfall intensity
- Downpipes: minimum 75mm (90-100mm for large roofs)
- Ground drainage: to public network or infiltration (soakaway)
- Consider rainwater harvesting for irrigation (see `diva-landscape`)

### 5. HVAC system specification

#### 5.1 System selection guide

| System | Best for | Cost/m2 install | Running cost | Comfort |
|---|---|---|---|---|
| Split inverter (multi-split) | Apartments, zones | EUR 30-60 | Medium | Good |
| VRV/VRF | Large dwelling, commercial | EUR 60-120 | Low-Medium | Excellent |
| Floor heating (agua) + chiller | Premium, new build | EUR 80-150 | Low | Excellent |
| Floor heating (electrico) | Small zones, WC | EUR 40-70 | High | Good |
| Radiadores (agua) | Renovation, existing boiler | EUR 30-50 | Medium | Good |
| Central AVAC (dutos) | Large moradia, commercial | EUR 80-160 | Low-Medium | Excellent |
| Bomba calor aerotermia | New build, eco-conscious | EUR 60-100 | Low | Good-Excellent |

#### 5.2 Sizing guidelines (quick estimation)

**Heating load (residential PT):**
- Well-insulated (post-2013): 40-60 W/m2
- Medium insulation (1990-2013): 60-80 W/m2
- Poor insulation (pre-1990): 80-120 W/m2

**Cooling load (residential PT):**
- Standard: 80-100 W/m2
- Large glazing / west exposure: 100-130 W/m2
- With shading (estores, pergola): 60-80 W/m2

**Split AC sizing guide:**

| Room area | BTU needed | Split size |
|---|---|---|
| 10-15 m2 | 7,000-9,000 | 2.5kW (9000 BTU) |
| 15-22 m2 | 9,000-12,000 | 3.5kW (12000 BTU) |
| 22-30 m2 | 12,000-18,000 | 5.0kW (18000 BTU) |
| 30-40 m2 | 18,000-24,000 | 7.0kW (24000 BTU) |

**Multi-split systems:**
- 1 outdoor unit serving 2-5 indoor units
- Size outdoor unit at 80-90% of sum of indoor units (simultaneous diversity)
- Maximum pipe run: 50-75m (brand dependent)
- Maximum height difference: 15-30m

#### 5.3 Ventilation

**Natural ventilation (residential):**
- Cross-ventilation through operable windows
- Kitchen and WC require extraction (natural or mechanical)
- Air inlet: bedroom and living room windows (or ventilation grilles)
- Air outlet: kitchen hood + WC extraction

**Mechanical ventilation (when required):**
- Windowless WC or kitchen: mechanical extraction mandatory
- Commercial: RECS minimum ventilation rates per occupancy
- MVHR (recuperador de calor): recommended for energy-efficient homes
  - Efficiency: 75-95% heat recovery
  - Cost: EUR 3,000-8,000 installed
  - Requires duct network (ceiling void minimum 25cm)

### 6. Gas installation

| Item | Specification |
|---|---|
| Supply type | Natural gas (Goldenergy, EDP Gas, Galp) or GPL (garrafa/cisterna) |
| Entry point | Counter (natural gas) or regulator (GPL) |
| Internal pipe | Copper or steel (no plastic for gas) |
| Ventilation | Kitchen: low-level inlet (150cm2) + high-level outlet (if gas appliances) |
| Detector | CO detector recommended in kitchen (mandatory for some municipalities) |
| Appliances | Esquentador, fogao, caldeira — certified and with termo de responsabilidade |

### 7. Fire safety (SCIE)

Based on RJSCIE (DL 220/2008) and Portaria 1532/2008:

**Residential (utilizacao-tipo I):**

| Category | Criteria | Requirements |
|---|---|---|
| 1a categoria | <=9 pisos, <= 28m altura | Basic: extintores, sinaletica, iluminacao emergencia |
| 2a categoria | <=28 pisos, <= 50m | + detection in common areas, alarm, hydrants |
| 3a categoria | >28 pisos, >50m | + full SADI, sprinklers, pressurization |

**Basic fire safety (most residential):**
- Fire extinguishers: 1 per floor (common areas), ABC powder 6kg
- Emergency lighting: corridors, stairwells, exits
- Illuminated exit signs: at all exit doors
- Smoke detection: recommended in every bedroom and corridor (mandatory from 2a cat)
- Fire doors: to stairwell enclosures (EI30 or EI60)
- Fire resistance: party walls and floors EI60 minimum

### 8. MEP coordination

**Clash detection checklist:**
Cross-check all MEP routes against each other and against structure:

| Check | Common conflict | Resolution |
|---|---|---|
| Plumbing vs structure | Pipes through beams | Route around, use sleeves in slab |
| HVAC ducts vs ceiling height | Insufficient void | Reduce duct size, use flat ducts |
| Electrical vs plumbing | Cables near water pipes | Minimum 30cm separation, or protect |
| Drainage vs floor construction | Insufficient slope space | Raise floor level or use pump |
| AC outdoor units vs facade | Aesthetic impact, noise | Designate locations early, acoustic screen |
| Risers (prumadas) | Insufficient shaft size | Size shafts for all MEP from start |
| Floor heating vs door thresholds | Level differences | Plan build-up from start |
| Solar thermal vs roof structure | Panel weight, pipe routing | Structural check, pre-plan routes |

**Riser (prumada) sizing:**
For residential buildings, allocate shaft space:
- Minimum 60x60cm per dwelling stack (water + drainage + gas + electrical + telecom)
- Recommended 80x80cm for comfortable access and maintenance
- Fire-rate shaft walls (EI60)
- Access panels at every floor

### 9. Portuguese brands and suppliers

| System | Economico | Medio | Premium |
|---|---|---|---|
| Splits AC | Hisense, Midea | Daikin, Mitsubishi Electric | Daikin VRV, Toshiba |
| Bomba calor AQS | Ariston Nuos | Daikin Altherma, Vaillant | Daikin Altherma 3, NIBE |
| Caldeira gas | Vulcano | Vaillant, Junkers (Bosch) | Viessmann, Buderus |
| Piso radiante | Giacomini | Uponor, Rehau | Rehau, Watts |
| Radiadores | Baxi, Roca | Jaga, Runtal | Tubes, Vasco |
| Ventilacao MVHR | Vortice | Zehnder ComfoAir | Zehnder, Paul |
| Quadro electrico | Hager, Legrand | Schneider, ABB | ABB, Siemens |
| Tomadas/interruptores | Efapel (PT), Legrand Niloe | Schneider Unica | Jung LS990, BTicino |
| Louca sanitaria | Sanindusa (PT), Roca | Duravit, V&B | Laufen, Flaminia |
| Torneiras | Grohe Eurosmart | Grohe Essence, Hansgrohe | Axor, Dornbracht |

### 10. Cost estimation

**MEP as percentage of total construction:**

| Building type | MEP % of construction | Notes |
|---|---|---|
| Simple renovation | 20-25% | New wiring, plumbing, 2 splits |
| Medium renovation | 25-35% | Full rewire, replumb, multi-split, floor heating |
| New build residential | 30-40% | Complete MEP from scratch |
| Commercial/hospitality | 35-50% | Central HVAC, fire safety, complex |

**Individual system costs (installed, residential):**

| System | EUR range | Notes |
|---|---|---|
| Electrical rewire (apartment 100m2) | 5,000-12,000 | Panel + circuits + points |
| ITED (apartment) | 1,000-2,500 | ATI + cabling |
| Plumbing (kitchen + 2 WC) | 4,000-10,000 | Supply + drainage + fixtures |
| Split AC (per unit installed) | 800-2,500 | Depends on brand and capacity |
| Multi-split (1 outdoor + 4 indoor) | 4,000-8,000 | Installation + units |
| Floor heating (per m2 installed) | 40-80 | Water system, incl. manifold |
| Solar thermal (2 panels + deposito) | 2,000-4,000 | Mandatory for new builds |
| Bomba calor aerotermia | 5,000-15,000 | Heating + cooling + AQS |
| Fire safety (residential basic) | 500-2,000 | Extinguishers, signs, detection |

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: diva-mep
building_type: <residential|commercial|mixed>
area_m2: <number>
systems: [electrical, plumbing, hvac, gas, fire, ited]
tags: [MEP, instalacoes, especialidades, <project>]
---

# Especificacao MEP DIVA — <Project Name>

## 1. Resumo
- **Area:** <X> m2, <N> pisos
- **Tipo:** <building type>
- **Potencia contratada:** <X> kVA
- **Sistema AVAC:** <type>
- **AQS:** <type>
- **Gas:** <sim/nao, tipo>

## 2. Instalacao Electrica

### Potencia e alimentacao
- Contrato: <monofasico/trifasico>, <X> kVA
- Quadro geral: <N> modulos, <N> diferenciais

### Mapa de circuitos
| # | Circuito | Disjuntor | Cabo | Diferencial |
|---|---|---|---|---|
| 1 | Iluminacao zona 1 | 10A | 1.5mm2 | Dif. 1 |
| 2 | Tomadas sala | 16A | 2.5mm2 | Dif. 1 |
| ... | ... | ... | ... | ... |

### Pontos por divisao
| Divisao | Tomadas | Pontos luz | Dados | Especial |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## 3. ITED Telecomunicacoes
- ATI: <localizacao, dimensoes>
- Cabling: <Cat6A/Coax/Fibra por divisao>

## 4. Canalizacao

### Abastecimento agua
- Material tubagem: <tipo>
- Diametros: <entrada, ramos, pontos>

### AQS
- Sistema: <tipo>
- Capacidade: <litros ou kW>

### Drenagem
- Material: <PVC, PP>
- Diametros: <por equipamento>
- Ventilacao: <tipo>

## 5. AVAC

### Sistema seleccionado
- Tipo: <split/VRV/piso radiante/central>
- Marca/modelo: <spec>
- Capacidade: <heating kW / cooling kW>

### Por divisao
| Divisao | Area m2 | Carga termica W | Unidade | Capacidade |
|---|---|---|---|---|
| Sala | 30 | 3,000 | Split 3.5kW | 12,000 BTU |
| Suite | 15 | 1,500 | Split 2.5kW | 9,000 BTU |
| ... | ... | ... | ... | ... |

## 6. Gas (se aplicavel)
- Tipo: <natural/GPL>
- Equipamentos: <lista>
- Ventilacao: <spec>

## 7. Seguranca contra incendios
- Categoria: <1a/2a/3a>
- Extintores: <qtd, tipo, localizacao>
- Deteccao: <tipo>
- Iluminacao emergencia: <sim/nao>

## 8. Coordenacao MEP
| Conflito potencial | Solucao |
|---|---|
| ... | ... |

## 9. Orcamento MEP
| Sistema | EUR |
|---|---|
| Electricidade | ... |
| ITED | ... |
| Canalizacao (agua + esgoto) | ... |
| AVAC | ... |
| Gas | ... |
| Seguranca incendios | ... |
| **Total MEP** | **EUR X** |

## 10. Proximos Passos
- [ ] Contratar engenheiros de especialidades (electrotecnico, mecanico, civil)
- [ ] Projectos de especialidades para licenciamento
- [ ] Coordenar com `diva-acoustics` para isolamento de equipamentos
- [ ] Coordenar com `diva-energy` para eficiencia dos sistemas
- [ ] Coordenar com `diva-smart-home` para cablagem adicional
- [ ] Incluir custos MEP em `diva-budget`
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Especificacao MEP DIVA.md`

## Red flags — don't do this
- Never size the electrical panel without accounting for future loads (EV charger, heat pump, AC units) — upgrading the supply from EDP after construction is expensive (EUR 500-2,000+) and can take months of bureaucracy
- Never run plumbing drainage without proper slope testing (1-2% minimum) — Portuguese plumbers often eyeball slopes, and insufficient gradient causes recurring blockages that are extremely expensive to fix under tiled floors
- Never skip the pressure test (10 bar for 2 hours) before closing walls — a single missed joint in concealed plumbing becomes a EUR 5,000+ remediation once tiles and finishes are applied
- Never position AC outdoor units without considering noise impact (check `diva-acoustics`) and visual impact — municipalities can force removal of units that violate facade regulations or noise limits
- Never design MEP systems in isolation — HVAC ducts that conflict with structural beams, drainage that cannot reach the main stack, or electrical routes that cross plumbing without separation all result in costly site improvisation
- Never forget ITED compliance for new builds — ANACOM can block the autorizacao de utilizacao without a compliant ITED installation and certification
- Never undersize risers (prumadas) — Portuguese construction routinely makes shafts too small, forcing exposed pipes in finished spaces or impossible maintenance access

## Interactions
- Feeds into `diva-budget` (MEP is 20-40% of construction cost)
- Coordinates with `diva-floor-plan` for wet zone positions and riser locations
- Coordinates with `diva-acoustics` for equipment noise control and pipe insulation
- Coordinates with `diva-energy` for system efficiency and renewable integration
- Coordinates with `diva-smart-home` for additional cabling and panel space
- Referenced by `diva-licensing` for specialty project submissions
- Verified during `diva-inspection` Phase 4 (MEP rough-in)
- Save via `diva-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Regulamentação portuguesa citada correctamente
- [ ] Norma referenciada com designação completa (ex: RTIEBT, ITED 4.ª edição, RJSCIE DL 220/2008)
- [ ] Versão/edição vigente identificada, não genérica
- [ ] Aplicabilidade ao tipo de obra confirmada (residencial/comercial/hospitality)
- [ ] Sem referências a normas estrangeiras não homologadas em PT sem nota de equivalência
- ❌ NOT delivery-ready: "segundo as normas eléctricas aplicáveis..."
- ✅ Delivery-ready: "RTIEBT Artigo 4.3 — circuitos de tomadas com cabo 2,5mm² H07V-K, disjuntor 16A, diferencial 30mA Tipo A (obrigatório para cargas inversoras como ar condicionado e carregador EV)"

### Gate 2 — Potência eléctrica e dimensionamento do quadro com números reais
- [ ] Potência contratada especificada em kVA e amperagem (ex: trifásico 20,7kVA / 3×30A)
- [ ] Número de circuitos listado com breaker e secção de cabo por circuito
- [ ] Cargas dedicadas identificadas (forno, AC, bomba calor, EV) com amperagem própria
- [ ] Número de diferenciais e tipo (A vs AC) justificado
- ❌ NOT delivery-ready: "quadro eléctrico dimensionado para as necessidades da habitação"
- ✅ Delivery-ready: "Apartamento T3 Cuidai Porto: trifásico 13,8kVA (3×20A) — 14 circuitos, 2 diferenciais 30mA Tipo A; circuito dedicado placa de indução 32A / 6mm²; circuito EV 32A / 6mm² pré-instalação"

### Gate 3 — Sistema AVAC/aquecimento dimensionado para o espaço real
- [ ] Área condicionada em m² especificada por zona/divisão
- [ ] Carga de aquecimento ou arrefecimento estimada (kW ou BTU) com base em área e tipo de envolvente
- [ ] Sistema seleccionado justificado (split, VRV, bomba calor, piso radiante) com marca/modelo tier ou equivalente
- [ ] COP/EER ou classe energética do equipamento indicada
- ❌ NOT delivery-ready: "recomenda-se sistema de ar condicionado adequado"
- ✅ Delivery-ready: "Sala 42m² + cozinha 18m² = 60m² — carga estimada 6kW arrefecimento / 5kW aquecimento; Daikin Perfera 7kW (R32, SEER 8,74 / SCOP 5,1, classe A+++) — circuito dedicado 20A / 4mm²"

### Gate 4 — Redes de águas e drenagem com traçado e diâmetros
- [ ] Pontos de consumo listados por divisão (lavatório, sanita, duche, máquina, etc.)
- [ ] Diâmetros de alimentação indicados (ex: ½" ou ¾" para colectores principais)
- [ ] Sistema de drenagem descrito (colunas, ramais, pendentes mínimas 1%)
- [ ] Localização de contador, válvula de corte geral e esquentador/caldeira identificada
- ❌ NOT delivery-ready: "canalizações a instalar conforme projecto"
- ✅ Delivery-ready: "Moradia Vivenda Cascais: colector alimentação ¾" PEX-A entrada → 2 ramais ½" (IS social + cozinha); esquentador a gás 24kW no corredor técnico; drenagem coluna 110mm PVC com ramal sanita 90mm, pendente 2%"

### Gate 5 — Segurança contra incêndio (SCIE) referenciada se aplicável
- [ ] Categoria de risco SCIE identificada (Utilização-Tipo e Categoria 1-4)
- [ ] Medidas de autoprotecção ou sistemas activos listados se categoria ≥ 2
- [ ] Detectores de fumo, extintores e sinalização referenciados com localização
- [ ] Nota explícita se edifício isento de SCIE obrigatório (UT I Categoria 1)
- ❌ NOT delivery-ready: "verificar requisitos de segurança contra incêndio"
- ✅ Delivery-ready: "Edifício Tributario.AI Lisboa (UT IX — serviços, Categoria 2): 4 detectores iónicos corredor + sala técnica, extintor pó ABC 6kg por piso, bloco autónomo emergência em saídas — conforme RJSCIE DL 220/2008 Anexo III"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Nenhum `<nome_cliente>`, `<area>`, `<morada>` ou similar no output final
- [ ] Nome do projecto/cliente aparece pelo menos 2× no documento
- [ ] Morada ou localização real presente (bairro, cidade, rua se disponível)
- [ ] Datas e fases do projecto com referências temporais concretas se fornecidas
- ❌ NOT delivery-ready: "Para o projecto `<nome_projecto>` com área de `<X>`m²..."
- ✅ Delivery-ready: "Projecto Cuidai — Clínica Veterinária Matosinhos, 320m², Fase Especialidades Outubro 2025: quadro eléctrico trifásico 34,5kVA, 3 splits Mitsubishi Electric R32..."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output MEP deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via SKILL.md, regulamentação PT vigente, ou dados de projecto fornecidos pelo cliente
- 🟡 **assumed** — plausível para tipologia indicada, mas requer confirmação antes de entrega
- 🟢 **projection** — dimensionamento/estimativa por design (não verificável sem projecto executivo)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "Quadro eléctrico trifásico 20.7kVA, 3x30A, com 12 circuitos, AVAC tipo split 9000BTU por divisão, coluna de água DN25."
> *(reader assume tudo verificado — potência contratada, número de circuitos e dimensão da tubagem não têm fonte nem status)*

✅ Delivery-ready:
> - 🔵 **verified** — Fornecimento trifásico 20.7kVA (3x30A) compatível com moradia >200m² + bomba de calor, per RTIEBT tabela de níveis de potência
> - 🟡 **assumed** — 14 circuitos no quadro (estimativa para tipologia T4 + carregador EV); confirmar com cliente se existe pré-instalação solar ou jacuzzi
> - 🟢 **projection** — Carga total instalada estimada em 18.4kW em regime simultâneo; validação final requer cálculo por Engenheiro responsável

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — potência contratada actual, equipamentos previstos (EV, piscina, AC zonas), traçado de prumadas existentes
- [ ] All 🔵 citations added — artigos RTIEBT, ITED 4.ª edição, RGSPPDADAR e RJSCIE referenciados por número de artigo/tabela
- [ ] All 🟢 projections labeled ao cliente — deixar claro que dimensionamentos (AVAC, caudais, cargas) são estimativas de coordenação, não cálculos de projecto de execução com assinatura de técnico responsável

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# MEP Coordination — Apartamento T3 | LUSOconta HQ Lisboa
**Morada:** Rua Rodrigo da Fonseca 45, 2.º Esq., Lisboa
**Área total:** 138m² | **Tipo:** Renovação total | **Data:** Novembro 2025

---

## 1. Electrical System

**Alimentação:** Monofásico 10,35kVA (45A) — suficiente para T3 sem EV
**Quadro eléctrico:** 24 módulos DIN, 3 diferenciais 30mA (Tipo A circuitos AC + MW)

| Circuito | Disjuntor | Cabo | Notas |
|---|---|---|---|
| Iluminação zona 1 (sala/hall/quartos) | 10A | 1,5mm² H07V-K | 9 pontos |
| Iluminação zona 2 (cozinha/WC/lavandaria) | 10A | 1,5mm² H07V-K | 6 pontos |
| Tomadas sala + corredor | 16A | 2,5mm² | 6 tomadas |
| Tomadas quarto 1 + 2 | 16A | 2,5mm² | 8 tomadas |
| Tomadas quarto 3 + escritório | 16A | 2,5mm² | 6 tomadas |
| Tomadas bancada cozinha | 16A | 2,5mm² | 5 tomadas |
| Placa de indução Bosch 7,4kW | 32A | 6mm² | Dedicado |
| Forno encastrar | 20A | 4mm² | Dedicado |
| Máquina lavar roupa | 16A | 2,5mm² | Dedicado, lavandaria |
| Máquina lavar loiça | 16A | 2,5mm² | Dedicado, cozinha |
| Split sala 9.000BTU (Daikin Perfera) | 16A | 2,5mm² | Dedicado, Tipo A |
| Split quarto principal 7.000BTU | 16A | 2,5mm² | Dedicado, Tipo A |
| Pré-instalação EV (cave) | 32A | 6mm² | Para futuro EVSE |

**SPD Tipo 2:** instalado imediatamente após contador (preparação para PV futuro)
**ITED:** 2 caixas ATI (sala + escritório), cablagem CAT6A + coaxial RG6, riser 63mm

---

## 2. AVAC

**Método:** EN 15243 simplificado, orientação Sul, envolvente após isolamento ETICS 80mm

| Zona | Área | Carga Arref. | Carga Aquec. | Equipamento |
|---|---|---|---|---|
| Sala + cozinha aberta | 58m² | 5,8kW | 4,5kW | Daikin Perfera 7kW SEER 8,74 / SCOP 5,10 |
| Quarto principal | 22m² | 2,2kW | 1,8kW | Daikin Perfera 2,5kW |
| Quartos 2+3 | 28m² | — | — | Pré-instalação (canalização + circuito) |

**AQS:** Bomba de calor Ariston Nuos Evo 80L (COP 3,2) — lavandaria
**Ventilação:** VMC simples fluxo Aerauliqa QR80 — extracção WC + cozinha, 90m³/h total

---

## 3. Redes de Águas e Drenagem

**Alimentação geral:** ¾" PEX-A desde contador entrada → colector distribuição
**Ramais individuais:**
- Cozinha: ½" quente + fria, ponto máquina ¾" à rede
- IS social: ½" fria (sanita), ½" quente + fria (lavatório)
- IS suite: ½" quente + fria (duche + lavatório), sanita ½" fria
- IS quartos: ½" quente + fria, bidé ½" fria

**Drenagem:** coluna existente 110mm PVC mantida; ramais novos 50mm (lavatórios),
90mm (sanitas), pendente mínima 2%; sifão individual em todos os aparelhos

**Válvula de corte geral:** sob lava-loiça cozinha, acessível

---

## 4. SCIE

**Utilização-Tipo:** UT I (Habitacional) — **Categoria 1** (< 9m altura, < 9 fogos)
→ **Isento de medidas de autoprotecção obrigatórias** (RJSCIE DL 220/2008 Artigo 19.º)

Recomendado (boa prática): 2 detectores de fumo iónicos (hall + corredor quartos),
1 extintor pó ABC 1kg em cozinha — não obrigatório, incluído no caderno de encargos.

---

## 5. Coordenação entre Especialidades

- Riser técnico 30×60cm (parede cozinha/lavandaria): passa coluna AVAC + canalização AQS
- Tecto falso corredor 2,50m: reserva 15cm para condutas VMC (ø125mm)
- Quadro eléctrico: parede entrada, 40×60cm superfície, 24 módulos + espaço 30% expansão
- Conflito resolvido: condutas VMC cruzam com viga hall → desvio 20cm confirmado com
  diva-diagnose planta existente
```

---

## Output anti-patterns

- Citar "normas aplicáveis" sem nomear decreto-lei, edição ou artigo específico
- Dimensionar potência eléctrica sem listar os circuitos individuais com cabo e disjuntor
- Recomendar "sistema de ar condicionado adequado" sem área, kW estimado ou modelo tier
- Usar placeholders `<morada>`, `<área>`, `<cliente>` no output entregue ao cliente
- Descrever drenagem sem indicar diâmetros, materiais (PVC/PEX) ou pendentes mínimas
- Omitir a categoria de risco SCIE mesmo em habitações (a isenção deve ser declarada, não ignorada)
- Misturar specs de engenharia de cálculo certificadas com especificações de coordenação sem nota de disclaimer ("requere validação por engenheiro responsável")
- Copiar tabela de circuitos do template sem adaptar ao número de divisões e cargas reais do projecto
- Indicar COP/SEER de equipamento sem associar ao circuito eléctrico dedicado correspondente
