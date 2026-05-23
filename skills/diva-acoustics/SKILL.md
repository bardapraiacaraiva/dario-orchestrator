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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Parâmetros RRAE identificados e quantificados

- [ ] Output especifica os parâmetros relevantes ao projeto (DnT,w, L'nT,w, D2m,nT,w, LAr,nT) com valores numéricos, não apenas "cumpre o regulamento"
- [ ] Cada parâmetro comparado com o mínimo RRAE aplicável (ex: DnT,w >= 50 dB entre frações)
- [ ] Indica se o projeto está em Classe C (mínimo), B ou A (NP 4499) quando aplicável
- [ ] Gap entre solução proposta e mínimo legal está explícito (ex: "+4 dB de margem")

❌ NOT delivery-ready: *"A parede cumpre os requisitos acústicos do RRAE."*
✅ Delivery-ready: *"Parede dupla tijolo 11+11 + MW 5cm → DnT,w estimado 54 dB. Requisito RRAE: 50 dB. Margem: +4 dB (Classe B per NP 4499)."*

---

### Gate 2 — Localização e ruído exterior contextualizado

- [ ] Zona de ruído identificada (quieta / moderada / ruidosa) com Lden estimado ou consultado no mapa de ruído municipal
- [ ] Requisito de fachada D2m,nT,w correto para a zona (28 dB / 33 dB / 33 dB + correção)
- [ ] Se localização é junto a eixo viário, ferrovia ou aeroporto, isso está explicitamente mencionado
- [ ] Fonte do dado de ruído indicada (ex: "Mapa de Ruído CM Lisboa, 2022 — Lden 63 dB")

❌ NOT delivery-ready: *"A fachada deve cumprir os requisitos do RRAE conforme a localização do edifício."*
✅ Delivery-ready: *"Localização: Av. Almirante Reis, Lisboa. Lden estimado: 68 dB (zona ruidosa, mapa CM Lisboa). Requisito fachada: D2m,nT,w >= 33 dB + correção. Solução: janela PVC vidro duplo 4/16/6 → D2m,nT,w ≈ 36 dB. ✅ Cumpre."*

---

### Gate 3 — Soluções construtivas especificadas com materiais reais

- [ ] Cada solução tem espessura total (mm), composição por camadas (da interior para exterior), e DnT,w ou L'nT,w estimado
- [ ] Custo indicativo EUR/m² presente para pelo menos a solução recomendada
- [ ] Materiais mencionam fornecedores ou produtos disponíveis em Portugal (ex: Isover, Knauf, Weber, Mapei, Saint-Gobain)
- [ ] Princípio construtivo crítico verificado: ausência de ligações rígidas entre panos, selagem perimetral com mastique acústico

❌ NOT delivery-ready: *"Recomenda-se piso flutuante com material resiliente para redução de ruído de impacto."*
✅ Delivery-ready: *"Piso flutuante: betonilha 6cm + lã mineral resiliente Isover Floorrock SE 30mm (Rw 38 dB, rigidez dinâmica s' ≤ 10 MN/m³) + laje maciça 20cm → L'nT,w ≈ 52 dB. Requisito: ≤ 60 dB. Custo aprox. 28-35 €/m²."*

---

### Gate 4 — Ruído de equipamentos (LAr,nT) endereçado se relevante

- [ ] Se o edifício tem AVAC, elevador, bombas, ou tubagens de queda, output verifica LAr,nT
- [ ] Distingue equipamento contínuo (limite 32 dB(A)) vs. intermitente/elevador (limite 40 dB(A))
- [ ] Medidas de isolamento de equipamentos especificadas quando LAr,nT previsto excede limite (anti-vibráticos, caixa técnica flutuante, shafts com lã mineral)
- [ ] Adjacências críticas identificadas (ex: quarto de dormir junto a shaft de elevador)

❌ NOT delivery-ready: *"Os equipamentos mecânicos devem ser instalados de forma a não causar incómodo acústico."*
✅ Delivery-ready: *"Elevador previsto adjacente a quarto T2. Limite LAr,nT ≤ 40 dB(A). Medidas: revestimento shaft com pladur 2×15mm + MW 5cm; silentblocks no grupo motor; porta casa de máquinas com DnT,w ≥ 38 dB. LAr,nT estimado pós-medidas: 36 dB(A). ✅ Cumpre."*

---

### Gate 5 — Percursos de flanking e pontos críticos identificados

- [ ] Output menciona pelo menos 1 percurso de flanking relevante ao projeto (laje contínua, pilar, condutas partilhadas, rodapé rígido)
- [ ] Solução de descontinuidade proposta para percurso identificado (junta elástica, dessolidarização, sleeve resiliente)
- [ ] Zonas de interface especiais tratadas: caixa de escada, garagem, zona comercial no piso 0
- [ ] Para mistos residencial/comercial: parâmetro 58 dB aplicado (não 50 dB) e confirmado

❌ NOT delivery-ready: *"Cuidado com as pontes acústicas na construção."*
✅ Delivery-ready: *"Laje contínua entre fração A (piso 1) e restaurante (piso 0, Cuidai Lisboa). Flanking path via laje + parede estrutural. Solução: perfis Regupol 5010 sob parede divisória + junta perimetral betonilha com Knauf Trennfix 5mm. DnT,w necessário: 58 dB (residencial/comercial). Solução estimada: 60 dB. ✅ Margem +2 dB."*

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais do projeto, sem placeholders entre ângulos

- [ ] Nenhum `<client_name>`, `<project_address>`, `<floor_type>`, `<insert_value>` presente no output
- [ ] Morada ou localização do projeto aparece em pelo menos 1 ponto do output
- [ ] Tipologia do edifício e ano de projeto/licença referenciados (ex: "Edificio novo, licença 2024, CM Porto")
- [ ] Valores de desempenho são do projeto específico, não genéricos de tabela

❌ NOT delivery-ready: *"Para o projeto em `<localização>`, o requisito de `<parametro>` é de `<valor>` dB."*
✅ Delivery-ready: *"Vivenda — Edifício Almada Nova, Rua Prior do Crato 12, Almada. Licença 2024. Paredes entre frações T3: DnT,w 56 dB (solução: betão 20cm + Pladur F47 independente). Pavimentos: L'nT,w 54 dB (piso flutuante Floorrock 30mm). Todos os parâmetros RRAE cumpridos com Classe B."*

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Projeto Acústico — Vivenda Almada Nova
**Cliente:** Vivenda — Promoção Imobiliária  
**Obra:** Edifício Residencial + Comércio R/C, Rua Prior do Crato 12, Almada  
**Tipologia:** 3 pisos residenciais (T2/T3) + loja R/C  
**Licença de construção:** CM Almada, 2024  
**Data análise:** Junho 2025

---

## 1. Contexto de ruído exterior

Localização: arruamento urbano de tráfego moderado.  
Lden estimado: 61 dB (Mapa de Ruído CM Almada, zona moderada 55–65 dB).  
**Requisito fachada: D2m,nT,w ≥ 33 dB.**

---

## 2. Requisitos RRAE aplicáveis

| Elemento | Parâmetro | Requisito mínimo | Classe-alvo |
|---|---|---|---|
| Parede entre frações (residencial) | DnT,w | ≥ 50 dB | Classe B (≥ 55 dB) |
| Parede fração / loja R/C | DnT,w | ≥ 58 dB | Classe B (≥ 63 dB) |
| Pavimento entre pisos | L'nT,w | ≤ 60 dB | Classe B (≤ 53 dB) |
| Fachada | D2m,nT,w | ≥ 33 dB | ≥ 36 dB |
| Elevador (junto a quarto) | LAr,nT | ≤ 40 dB(A) | ≤ 36 dB(A) |
| AVAC (unidade interior) | LAr,nT | ≤ 32 dB(A) | ≤ 28 dB(A) |

---

## 3. Soluções construtivas especificadas

### 3.1 Parede entre frações T2/T3 (pisos 1–3)
**Solução:** Betão armado 20cm + perfis Knauf F47 independentes 
(distância 3cm ao betão) + lã mineral Isover Façade 034 5cm + 
Pladur N 2×13mm  
**Espessura total:** 290mm  
**DnT,w estimado:** 62 dB  ✅ Classe B (requisito 50 dB, meta 55 dB)  
**Custo:** ~55 €/m²  
**Atenção:** Perfis F47 NÃO podem ter contacto rígido com laje — 
selar com Knauf Trennfix 5mm na base e topo.

### 3.2 Parede fração / loja R/C (separação residencial-comercial)
**Solução:** Laje BA 25cm (pré-existente) + piso flutuante face 
superior (ver 3.3) + tecto falso suspenso face inferior com 
Isover Calibel 13+45mm  
**DnT,w estimado:** 61 dB  ✅ (requisito 58 dB)  
**L'nT,w estimado:** 51 dB  ✅ Classe B (requisito 60 dB)  
**Custo tecto falso:** ~38 €/m²

### 3.3 Pavimento entre pisos (laje 20cm BA)
**Solução piso flutuante:**  
Laje BA 20cm + lã mineral resiliente Isover Floorrock SE 30mm  
(s' ≤ 10 MN/m³, Rw 38 dB) + betonilha 6cm (120 kg/m²)  
+ junta perimetral Knauf Trennfix 5mm (dessolidarização total)  
**L'nT,w estimado:** 52 dB  ✅ Classe B  
**DnT,w estimado:** 58 dB  ✅  
**Custo:** 30–38 €/m²  
**Crítico:** rodapé colado apenas à betonilha, nunca à parede.

### 3.4 Fachada (janelas, Rua Prior do Crato)
**Caixilharia:** PVC Deceuninck Elegant 82 MD, vidro duplo 6/16Ar/6  
**D2m,nT,w janela:** ≈ 35 dB  ✅ (requisito 33 dB)  
**Parede exterior:** ETICS + pano tijolo 11cm — contribuição ≥ 48 dB  
**Sistema global fachada:** D2m,nT,w ≈ 36 dB  ✅

---

## 4. Equipamentos — controlo LAr,nT

**Elevador** (shaft adjacente a quarto T3, piso 2):  
- Revestimento shaft: Pladur 2×15mm + Isover Acoustic 5cm  
- Silentblocks Farrat TF25 no grupo motor  
- Porta casa de máquinas: porta acústica DnT,w ≥ 40 dB  
- **LAr,nT estimado: 37 dB(A)**  ✅ (limite 40 dB(A))

**AVAC** (unidades split Mitsubishi Electric MSZ-LN — 3 frações):  
- Unidades interiores sobre suportes anti-vibráticos  
- Tubagens com manga resiliente Armacell AF/ArmaFlex nos 
  atravessamentos de laje  
- **LAr,nT estimado: 29 dB(A)**  ✅ (limite 32 dB(A))

---

## 5. Percursos de flanking identificados

| Ponto crítico | Risco | Solução |
|---|---|---|
| Laje contínua piso 1 → loja R/C | Alto — flanking via laje | Junta Regupol 5010 sob parede divisória |
| Pilar BA entre fração A e B | Médio — transmissão lateral | Pladur independente não solidário ao pilar |
| Tubagem queda (PVC 110mm) | Médio — ruído plumbing | Manga Rockwool Pipe 40mm + braçadeiras resilientes |
| Caixa de escada comum | Baixo | DnT,w ≥ 48 dB (parede tijolo 15 + reboco duplo) |

---

## 6. Classificação acústica final (NP 4499)

| Elemento | Valor estimado | Classe |
|---|---|---|
| Paredes entre frações | DnT,w 62 dB | **Classe B** |
| Pavimentos impacto | L'nT,w 52 dB | **Classe B** |
| Fachada | D2m,nT,w 36 dB | **Classe B** |
| Elevador | LAr,nT 37 dB(A) | **Classe C** |

**Classificação global do edifício: Classe B** — adequado a 
posicionamento de mercado premium-médio (Vivenda).

---

*Análise baseada em RRAE (DL 96/2008) e NP 4499. Valores estimados 
por cálculo — confirmação por medição in-situ após construção 
recomendada (RRAE Art. 11º).*
```

---

## Output anti-patterns

- Citar apenas "cumpre o RRAE" sem valores de DnT,w ou L'nT,w — compliance sem número não é verificável
- Especificar "isolamento acústico adequado" sem indicar a camada resiliente, espessura e fornecedor concreto
- Ignorar o percurso de flanking pela laje ou pilares (o ponto mais frequente de falha real em obra)
- Tratar DnT,w e Rw como equivalentes — Rw é de laboratório, DnT,w é in-situ com correção de tempo de reverberação
- Omitir distinção residencial/comercial (58 dB) vs. residencial/residencial (50 dB) — erro de 8 dB com impacto legal
- Recomendar piso flutuante sem especificar rigidez dinâmica (s') do material resiliente — propriedade crítica para L'nT,w
- Output genérico sem localização: "verifique o mapa de ruído municipal" sem indicar qual município, URL ou valor Lden
- Listar soluções construtivas sem custo indicativo €/m² — impede tomada de decisão por promotor ou arquitecto
- Confundir LAr,nT contínuo (32 dB(A)) com intermitente/elevador (40 dB(A)) — requisitos diferentes, não intercambiáveis
- Produzir output sem identificar o cliente ou edifício específico — relatório sem cabeçalho não é documento de projeto
