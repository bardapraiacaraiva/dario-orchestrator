---
name: diva-accessibility
description: Accessibility and universal design for Portuguese construction projects. Covers DL 163/2006 compliance, mobility-impaired access, wheelchair dimensions, accessible bathrooms, ramps, elevators, signage, and universal design principles for residential, commercial, and public buildings. Triggers on "acessibilidade", "accessibility", "mobilidade reduzida", "cadeira de rodas", "wheelchair", "DL 163/2006", "universal design", "design inclusivo", "barreiras arquitectonicas".
license: MIT
---

# DIVA Skill — Accessibility & Universal Design (DL 163/2006)

Comprehensive accessibility analysis and specification for Portuguese construction projects. Ensures compliance with DL 163/2006 (accessibility regulations), applies universal design principles, and creates inclusive spaces that work for all users regardless of mobility, vision, hearing, or cognitive abilities. Covers residential, commercial, public, and hospitality buildings.

## When to activate

Invoke `/diva-accessibility` (or trigger automatically) when:
- New construction or major renovation requiring DL 163/2006 compliance
- Commercial, public, or hospitality building design (mandatory compliance)
- Client requests aging-in-place design (envelhecimento em casa)
- Client or household member has mobility, visual, or hearing impairment
- Licensing requires accessibility specialty project compliance
- User asks about wheelchair access, ramps, accessible WCs
- Tourism accommodation (AL, hotel) requiring accessible rooms
- Workplace design requiring inclusive access

Do NOT use when:
- Purely cosmetic renovation with no spatial or access changes
- Project exempt under RERU (pre-existing in ARU — but still recommend improvements)
- Industrial facilities with separate accessibility frameworks

## Regulatory framework

### DL 163/2006 — Accessibility of buildings
The primary Portuguese accessibility regulation, implementing EU Directive requirements:

| Scope | Requirement |
|---|---|
| New public buildings | Full compliance mandatory |
| New residential (>4 dwellings) | Common areas + adaptable dwellings |
| New commercial/services | Full compliance mandatory |
| Existing buildings (renovation >25% value) | Reasonable adjustments required |
| Tourism accommodation | Minimum accessible rooms per capacity |
| Heritage buildings | Reasonable adjustments (case-by-case) |

### Key standards referenced
- EN 81-70: Elevator accessibility
- ISO 21542: Building accessibility
- EN 12182: Assistive products
- CEN/TS 17959: Universal design

### Exemptions and flexibility
- RERU (rehabilitation) may exempt from strict compliance for pre-existing buildings
- Heritage buildings: reasonable adjustments only (DGPC consultation)
- Existing dwellings: no mandatory retrofit, but recommended for aging-in-place
- Small commercial (<150m2, no public access): limited requirements

## Workflow

### 1. Gather accessibility inputs

- **Building type:** residential, commercial, public, hospitality, mixed
- **New build vs renovation:** determines compliance level
- **Number of dwellings/units:** triggers threshold for common area requirements
- **Users with specific needs:** wheelchair, walker, visual, hearing, cognitive
- **Aging-in-place requirement:** current or future adaptability
- **Floor count:** determines elevator/lift requirement
- **Existing barriers:** steps, narrow doors, inaccessible WC
- **Tourism accommodation:** number of rooms, AL or hotel classification
- **Public access:** yes/no, expected visitors

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "acessibilidade DL 163/2006 mobilidade reduzida Portugal", limit: 5)
mcp__dario-rag__search_kb(query: "universal design aging in place wheelchair accessible bathroom", limit: 5)
mcp__dario-rag__search_kb(query: "ramp elevator accessible building regulations dimensions", limit: 5)
```

### 3. Access route analysis (percurso acessivel)

An accessible route must exist from the public way to every accessible space:

**Exterior access (from street to building entrance):**
- Path width: minimum 1.20m (recommended 1.50m)
- Maximum slope: 6% for ramps up to 6m long (8% up to 2m)
- Cross slope: maximum 2%
- Surface: firm, stable, slip-resistant (avoid loose gravel, cobblestone)
- Ramp requirements (if level change):
  - Width: minimum 1.20m between handrails
  - Landing at top and bottom: minimum 1.50m x 1.50m
  - Intermediate landing every 6m (at 6%) or 10m (at 5%)
  - Handrails both sides: 0.90m height (double rail: 0.70m + 0.90m)
  - Edge protection: minimum 0.05m kerb or solid barrier
  - Non-slip surface (R11 minimum)
- Steps/stairs (if also provided):
  - Rise: 0.15-0.175m, going: 0.28-0.32m
  - Handrails both sides, extending 0.30m beyond top and bottom
  - Tactile warning strip before top step (0.40m deep)
  - Contrasting nosings

**Interior access:**
- Corridor width: minimum 1.20m (1.50m recommended)
- Passing space: 1.80m wide every 15m maximum
- Door width (clear opening): minimum 0.77m (recommended 0.90m)
- Door handle: lever type, 0.80-1.10m height
- Threshold: maximum 0.02m (ideally flush)
- Floor level changes >0.02m: ramp or platform lift required
- Turning circle: minimum 1.50m diameter (for wheelchair 180 turn)

### 4. Vertical access (elevators and lifts)

**When mandatory:**
- Buildings >1 floor with public access
- Residential buildings >4 floors (or >3 + ground floor parking)
- Any building where accessible route requires level change >0.40m

**Elevator dimensions (minimum per DL 163/2006):**

| Type | Cabin LxW (m) | Door width (m) | Use |
|---|---|---|---|
| Standard accessible | 1.10 x 1.40 | 0.80 | Basic wheelchair access |
| Recommended | 1.40 x 1.60 | 0.90 | Comfortable wheelchair + companion |
| Stretcher-compatible | 1.10 x 2.10 | 0.90 | Emergency + wheelchair |

**Controls:**
- Button height: 0.90-1.20m from floor
- Braille and tactile buttons
- Audible floor announcement
- Visual floor indicator
- Emergency communication at accessible height
- Mirror on rear wall (for wheelchair user to see when reversing)

**Platform lifts (plataformas elevatórias):**
- For level changes up to 2m (exterior) or 4m (interior)
- Minimum platform: 0.90 x 1.20m
- Maximum speed: 0.15m/s
- Lower cost alternative to full elevator
- EN 81-41 compliance

### 5. Accessible sanitary facilities (WC acessivel)

**Minimum dimensions:**

| Configuration | Minimum dimensions | Notes |
|---|---|---|
| Independent WC (only toilet + basin) | 1.60 x 1.80m | Side transfer |
| WC with frontal transfer | 1.80 x 2.20m | Frontal approach |
| Full accessible WC (toilet + basin + shower) | 2.20 x 2.50m | Recommended |
| Adapted suite bathroom | 2.50 x 3.00m | Luxury/hotel |

**Toilet (sanita):**
- Height: 0.45-0.50m (higher than standard 0.40m)
- Flush: large button or lever, reachable
- Grab bars: one fixed (wall side), one folding (transfer side)
  - Height: 0.70-0.75m from floor
  - Distance between bars: 0.70-0.75m
  - Support weight: minimum 150kg

**Basin (lavatorio):**
- Height: 0.80m top surface
- Knee clearance below: minimum 0.65m high, 0.50m deep
- No pedestal (wheelchair access underneath)
- Lever or sensor tap
- Mirror: bottom edge at 0.90m, tilting preferred

**Shower (duche acessivel):**
- Level access (zero threshold, flush with floor)
- Minimum area: 0.90 x 0.90m (recommended 1.00 x 1.20m)
- Folding seat: 0.45-0.50m height, 150kg capacity
- Grab bars: L-shaped or combination, 0.70-0.75m height
- Handheld shower on adjustable rail (0.60-2.00m range)
- Thermostatic mixer with anti-scald (max 38C)
- Non-slip floor (R11 minimum)
- Linear drain (for flush floor)

**Door:**
- Sliding or outward-opening (never inward in accessible WC)
- Emergency unlockable from outside
- Contrasting colour vs wall
- Clear opening: minimum 0.80m

### 6. Residential accessibility (habitacao adaptavel)

For new residential buildings with >4 units, DL 163/2006 requires "adaptable" dwellings:

**Adaptable dwelling concept:**
A standard dwelling designed so it CAN be converted to fully accessible with minimal work:

| Element | As-built (adaptable) | Converted (accessible) |
|---|---|---|
| Entrance | Level or max 0.02m threshold | Same |
| Corridor | 1.10m minimum (1.20m recommended) | Same |
| Doors | 0.80m clear opening, lever handles | Same |
| WC | Reinforced walls for future grab bars | Bars installed, shower modified |
| Kitchen | Standard | Lower worktop zones, accessible appliances |
| Bedroom | Standard, 1.50m on one side of bed | Same |
| Balcony | Level or max 0.02m threshold | Same |

**Wall reinforcement specification:**
In all WC and bedroom walls adjacent to bed position, install:
- 18mm marine plywood or OSB behind plasterboard/tiles
- Area: 1.00m wide x 0.60m high at grab bar zones (0.60-0.90m from floor)
- Cost: negligible if done during construction (~EUR 5-10/m2 extra)
- Retrofitting without reinforcement: requires wall demolition

### 7. Commercial and public spaces

**Reception / counter:**
- Lowered section: 0.75-0.85m height, minimum 0.80m wide
- Knee clearance: 0.65m height, 0.50m depth

**Seating areas (restaurants, waiting rooms):**
- Wheelchair spaces: minimum 0.90m x 1.20m
- Table height: 0.70-0.80m with knee clearance
- Accessible route to all seating zones

**Changing rooms / fitting rooms:**
- Minimum one accessible: 1.50m x 1.50m
- Bench: 0.45-0.50m height, grab bar adjacent
- Mirror: full-length, bottom at floor level

**Parking:**
- Accessible spaces: minimum 1 per 20 (or fraction)
- Dimensions: 3.50m wide (2.50m + 1.00m side access zone)
- Maximum distance to accessible entrance: 25m
- Level surface, covered route preferred
- Signage: ISA symbol (vertical and ground)
- Height: minimum 2.40m clear (for adapted vehicles)

### 8. Signage and wayfinding

**Tactile:**
- Tactile ground surface indicators (pisos tacteis):
  - Warning (botoneiras): before steps, ramps, hazards
  - Directional (caneluras): guide paths in large open areas
- Braille signage at room doors (1.40-1.60m height)

**Visual:**
- Contrasting colors: door frames vs walls, stairs vs landings
- Large, high-contrast text (sans-serif, minimum 15mm at reading distance)
- ISA (International Symbol of Access) for accessible routes and facilities
- Room numbers: tactile and visual, consistent placement

**Audible:**
- Audible signals at crossings, elevators, emergency
- Hearing loops (anel magnetico) at reception desks and auditoriums

### 9. Aging-in-place considerations (envelhecimento em casa)

Design features for homes that age with the occupant:

| Feature | Implementation | Cost impact |
|---|---|---|
| Step-free entrance | Level threshold or gentle ramp | Low |
| Wider doors (0.90m) | Specify at design phase | Negligible |
| Reinforced WC walls | Plywood behind tiles | EUR 200-400 |
| Walk-in shower | Level-access instead of step-over | EUR 500-1,000 premium |
| Lever taps and handles | Specify at procurement | Negligible |
| Good lighting | 300+ lux in circulation, task areas | Low |
| Non-slip floors | Specify R10-R11 for wet areas | Negligible |
| Smart home (voice control) | Basic automation for lights, locks | EUR 1,000-3,000 |
| Stairlift provision | Electrical point, clear width 0.90m | EUR 50 prep, EUR 3,000-8,000 install later |
| Elevator shaft provision | Structural provision in new build | EUR 5,000-10,000 prep vs EUR 30,000+ retrofit |

### 10. Cost impact of accessibility

| Measure | Cost impact (new build) | Cost impact (retrofit) |
|---|---|---|
| Wider doors and corridors | +1-2% | +5-15% (wall moves) |
| Level-access shower | +EUR 500-1,000 per WC | +EUR 2,000-5,000 per WC |
| Elevator (new shaft) | EUR 25,000-60,000 | EUR 40,000-80,000 |
| Platform lift | EUR 8,000-20,000 | EUR 10,000-25,000 |
| Ramp (exterior) | EUR 200-500/ml | EUR 300-800/ml |
| Accessible WC fitout | EUR 3,000-6,000 | EUR 5,000-10,000 |
| Wall reinforcement | EUR 5-10/m2 | EUR 50-100/m2 (demolish + rebuild) |
| Tactile flooring | EUR 40-80/m2 | EUR 60-100/m2 |

**Key insight:** Accessibility in new construction adds only 1-3% to total cost. Retrofit costs 5-20x more. Always design for accessibility from the start.

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: diva-accessibility
building_type: <residential|commercial|public|hospitality|mixed>
regulation: DL 163/2006
compliance_level: <full|adaptable|reasonable-adjustment|voluntary>
tags: [acessibilidade, DL163, universal-design, <project>]
---

# Analise de Acessibilidade DIVA — <Project Name>

## 1. Contexto
- **Tipo de edificio:** <type>
- **Obra nova / reabilitacao:** <new/renovation>
- **N. fracoes/unidades:** <N>
- **Pisos:** <N>
- **Publico:** <sim/nao>
- **Nivel de conformidade requerido:** <full/adaptable/reasonable>

## 2. Auditoria do Percurso Acessivel

### Via publica ate entrada
| Elemento | Existente/Proposto | Conforme DL 163? | Accao necessaria |
|---|---|---|---|
| Passeio/caminho | ... | Sim/Nao | ... |
| Rampa entrada | ... | Sim/Nao | ... |
| Porta entrada | ... | Sim/Nao | ... |
| Campainha/intercomunicador | ... | Sim/Nao | ... |

### Circulacao interior
| Elemento | Existente/Proposto | Conforme DL 163? | Accao necessaria |
|---|---|---|---|
| Corredores | ... | Sim/Nao | ... |
| Portas interiores | ... | Sim/Nao | ... |
| Escadas | ... | Sim/Nao | ... |
| Elevador | ... | Sim/Nao | ... |

### Instalacoes sanitarias
| WC | Dimensoes | Conforme DL 163? | Accao necessaria |
|---|---|---|---|
| WC publico/comum | ... | Sim/Nao | ... |
| WC suite | ... | Adaptavel? | ... |

## 3. Solucoes Propostas

### Acesso exterior
- Rampa: <especificacao>
- Porta: <especificacao>

### Acesso vertical
- Elevador/plataforma: <especificacao>

### WC acessivel
- Dimensoes: <LxW>
- Equipamento: <sanita, lavatório, duche, barras>
- Porta: <tipo, largura>

### Habitacao adaptavel (se residencial)
- Reforcos paredes: <localizacao>
- Portas: <larguras>
- Duche: <tipo>

## 4. Sinaletica e Orientacao
- Pisos tacteis: <localizacao>
- Sinaletica Braille: <localizacao>
- Contraste visual: <especificacao>

## 5. Estimativa de Custo
| Medida | EUR |
|---|---|
| Rampa exterior | ... |
| Elevador/plataforma | ... |
| WC acessivel | ... |
| Reforcos paredes | ... |
| Sinaletica | ... |
| **Total acessibilidade** | **EUR X** |

## 6. Conformidade Regulamentar
| Requisito DL 163/2006 | Artigo | Conforme? | Observacao |
|---|---|---|---|
| Percurso acessivel exterior | Art. 2-5 | ... | ... |
| Percurso acessivel interior | Art. 6-12 | ... | ... |
| Instalacoes sanitarias | Art. 13-17 | ... | ... |
| Elevadores | Art. 18-20 | ... | ... |
| Estacionamento | Art. 21-23 | ... | ... |
| Sinaletica | Art. 24-26 | ... | ... |

## 7. Proximos Passos
- [ ] Incluir especificacao acessibilidade no projecto de arquitectura
- [ ] Coordenar com `diva-floor-plan` para dimensoes de corredores e portas
- [ ] Coordenar com `diva-mep` para elevador/plataforma
- [ ] Verificar conformidade com camara municipal antes de submissao
- [ ] Solicitar parecer ACAPO (se relevante para deficiencia visual)
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Acessibilidade DIVA.md`

## Red flags — don't do this
- Never design a new public or commercial building without full DL 163/2006 compliance — non-compliance blocks the autorizacao de utilizacao and exposes the owner to discrimination claims under Portuguese equality law
- Never assume "we'll add accessibility later" — retrofitting costs 5-20x more than designing it in from the start, and many elements (wider corridors, elevator shafts, reinforced walls) are impossible or prohibitively expensive to add after construction
- Never forget wall reinforcement in WC zones during construction — installing grab bars later without plywood backing behind tiles requires demolishing the tile, adding backing, and retiling, turning a EUR 200 job into a EUR 2,000+ one
- Never specify a ramp steeper than 6% (1:16.7) for lengths over 6m — steeper ramps are dangerous for wheelchair users and non-compliant; a ramp at 8% is only acceptable for runs under 2m
- Never design an accessible WC with an inward-opening door — if a user falls against the door, rescuers cannot open it; always use outward-opening or sliding doors
- Never skip the turning circle check (1.50m diameter) — a wheelchair that can enter a room but cannot turn around is trapped, not accommodated
- Never forget that accessibility benefits everyone — parents with strollers, delivery workers, elderly visitors, and temporarily injured people all benefit from accessible design

## Interactions
- Feeds into `diva-floor-plan` for corridor widths, door dimensions, turning circles
- Feeds into `diva-budget` for accessibility cost line items
- Coordinates with `diva-mep` for elevator/lift specification and electrical for platform lifts
- Referenced by `diva-licensing` as mandatory specialty project component
- Coordinates with `diva-materials` for slip-resistant and tactile floor specifications
- Informs `diva-smart-home` for voice-control and assistive technology integration
- Save via `diva-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Percurso acessível completamente especificado
- [ ] Largura de corredor indicada com valor real (ex: "corredor de 1.35m → upgrade para 1.50m")
- [ ] Inclinação de rampa calculada com comprimento e desnível reais do projeto
- [ ] Revestimento de piso especificado com classificação antiderrapante (R10, R11, R12)
- [ ] Faixa tátil de aviso indicada com dimensão e cor contrastante
- ❌ NOT delivery-ready: "A rampa deve ter uma inclinação adequada e superfície antiderrapante."
- ✅ Delivery-ready: "Rampa de acesso (desnível 0.42m, comprimento 5.25m): inclinação resultante 8.0% — excede limite de 6% para >2m. Solução: comprimento mínimo 7.00m ou rampa em dois lanços com patamar intermédio 1.50m×1.50m. Revestimento R11 exigido."

### Gate 2 — Conformidade DL 163/2006 explicitamente classificada
- [ ] Tipo de edifício cruzado com tabela de âmbito (novo/reabilitação, nº fogos, acesso público)
- [ ] Isenções RERU ou patrimônio indicadas se aplicáveis, com fundamentação
- [ ] Elementos obrigatórios vs. recomendados claramente distinguidos
- [ ] Referência ao artigo ou anexo do DL 163/2006 quando se cita dimensão normativa
- ❌ NOT delivery-ready: "O projeto deve cumprir as normas de acessibilidade aplicáveis."
- ✅ Delivery-ready: "Edifício comercial novo, 320m², acesso público → conformidade total DL 163/2006 obrigatória (Artigo 10º). Elevador não exigido (piso único). WC acessível obrigatório: mínimo 1 por estabelecimento (Anexo, §4.3)."

### Gate 3 — Instalações sanitárias acessíveis dimensionadas
- [ ] Dimensões reais da IS existente ou proposta indicadas (LxC em metros)
- [ ] Espaço de manobra de cadeira de rodas verificado (círculo 1.50m ou transfer 0.90m lateral)
- [ ] Barras de apoio especificadas: posição, comprimento, altura, rebatível ou fixo
- [ ] Lavatório sem coluna, torneira de alavanca ou sensor indicados
- ❌ NOT delivery-ready: "A instalação sanitária deve ter barras de apoio e espaço suficiente para cadeira de rodas."
- ✅ Delivery-ready: "IS proposta 1.80m×2.20m (3.96m²): espaço de manobra 1.50m×1.50m disponível lateral à sanita ✓. Barra rebatível: lado esquerdo (transfer), 0.85m altura, comprimento 0.80m. Barra fixa: parede posterior, 0.85m altura. Lavatório suspenso regulável 0.70–0.85m, sem coluna, torneira monocomando."

### Gate 4 — Elevador ou solução de acesso vertical avaliada
- [ ] Número de pisos e condição de acesso público verificados para determinar obrigatoriedade
- [ ] Dimensão de cabine especificada em LxC com largura de porta (se elevador obrigatório ou recomendado)
- [ ] Alternativa justificada se elevador não viável (plataforma elevatória, salva-escadas), com dimensões
- [ ] Controlos: altura de botões, braile, anúncio sonoro, indicados
- ❌ NOT delivery-ready: "Prever elevador acessível conforme legislação."
- ✅ Delivery-ready: "Edifício Cuidai — sede Porto, 4 pisos + r/c, acesso público: elevador obrigatório (DL 163/2006, Artigo 11º). Cabine mínima 1.10×1.40m, porta 0.80m → recomendado 1.40×1.60m, porta 0.90m para conforto cadeira + acompanhante. Botoneiras: 0.90–1.20m altura, braile + relevo, anúncio sonoro por piso."

### Gate 5 — Sinalética e orientação inclusiva especificada
- [ ] Sinalização tátil/podoguia indicada nos percursos principais
- [ ] Contraste visual (≥70% LRV) verificado para portas, degraus, mudanças de nível
- [ ] Sinalética em braile ou pictograma nas IS acessíveis e elevadores
- [ ] Iluminação mínima nos percursos acessíveis indicada (lux)
- ❌ NOT delivery-ready: "Prever sinalética acessível nos espaços comuns."
- ✅ Delivery-ready: "Piso podoguia (cor amarela, contraste ≥70% LRV sobre pavimento cinza claro) no hall de entrada até elevador e IS acessível. Placa IS: pictograma cadeira de rodas + braile, altura 1.40–1.60m (centro). Iluminação percurso acessível: mínimo 200 lux ao nível do piso."

### Gate 6 — Output usa NOME DO CLIENTE + dados reais do projeto, sem angle-brackets
- [ ] Nome do cliente ou projeto real mencionado (ex: "Vivenda Cascais — Fam. Rodrigues", "Atrium Lisboa Piso 3")
- [ ] Endereço ou localização real indicada onde relevante para contexto regulatório
- [ ] Zero ocorrências de `<nome>`, `[CLIENT]`, `[ADDRESS]`, `[INSERT]` ou equivalentes
- [ ] Todas as dimensões são valores calculados para o projeto em questão, não ranges genéricos copiados da norma

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Análise de Acessibilidade — Cuidai Centro de Dia Braga
**Projeto:** Adaptação de edifício existente (1980), 3 pisos, uso misto saúde/serviços
**Endereço:** Rua do Castelo 47, Braga | **Data:** Junho 2025
**Compliance:** DL 163/2006 — reabilitação >25% valor → ajustes razoáveis obrigatórios

---

## 1. Percurso acessível exterior

**Situação existente:** 4 degraus (desnível total 0.68m) entre passeio e entrada principal.
**Solução proposta:** Rampa lateral a sul, aproveitando recuo de 6.20m disponível.

| Parâmetro | Valor calculado | Requisito DL 163/2006 | Estado |
|---|---|---|---|
| Desnível | 0.68m | — | — |
| Comprimento rampa | 8.50m (incl. patamares) | mínimo livre | ✓ |
| Inclinação | 6.0% | ≤6% para >2m | ✓ |
| Largura entre corrimãos | 1.30m | mínimo 1.20m | ✓ |
| Patamar inicial (passeio) | 1.50×1.60m | mínimo 1.50×1.50m | ✓ |
| Patamar intermédio | 1.50×1.50m (a 5.50m) | obrigatório a cada 6m | ✓ |
| Patamar superior (entrada) | 1.80×1.80m | mínimo 1.50×1.50m | ✓ |

**Corrimãos:** Duplo (0.70m + 0.90m), ambos os lados, extensão 0.30m além do topo e base.
**Revestimento:** Betão com acabamento estriado transversal, classificação R11.
**Guarda lateral:** Bordão de 0.07m altura nas duas faces longitudinais.

---

## 2. Acesso vertical interno

**Situação:** Edifício 3 pisos + cave técnica. Acesso público ao piso 1 (consultas) e piso 2 (fisioterapia).

**Conclusão de obrigatoriedade:** Acesso público em múltiplos pisos → elevador obrigatório (Artigo 11º).

**Especificação elevador proposto (shaft existente 1.80×2.10m útil):**
- Cabine: 1.40×1.60m — conforto cadeira de rodas + acompanhante ✓
- Porta: 0.90m largura, automática, proteção de bordo sensível
- Botoneiras: 0.95m–1.15m do piso (centro botão)
- Braile + relevo em todos os botões
- Anúncio sonoro: "Piso zero — entrada", "Piso um — consultas", "Piso dois — fisioterapia"
- Indicador visual: display digital exterior por piso
- Dimensões de espera exterior: 1.60×1.60m disponíveis em todos os pisos ✓
- Norma aplicável: EN 81-70 Categoria 2

---

## 3. Instalação sanitária acessível — Piso 0

**Dimensões propostas** (reconfiguração de IS existente 2.20×2.60m = 5.72m²):

```
┌─────────────────────────┐ 2.20m
│  [LAV]     [↑BARRA 0.80]│
│                          │
│ ○ 1.50m    [SANITA]     │
│                          │
│  [PORTA 0.90m →]        │
└─────────────────────────┘ 2.60m
```

- **Sanita:** Altura assento 0.46m, espaço transfer lateral esquerdo 0.90m ✓
- **Barra rebatível esquerda:** altura 0.85m, comprimento 0.80m, carga 100kg
- **Barra fixa posterior:** altura 0.85m, comprimento 0.60m
- **Lavatório:** Suspenso, regulável 0.70–0.85m, espaço inferior livre 0.65m (para aproximação frontal cadeira)
- **Torneira:** Monocomando alavanca longa, acessível a 0.40m da borda frontal
- **Espelho:** Inclinado 10° ou regulável, borda inferior a 0.90m
- **Círculo de manobra 1.50m:** disponível com porta aberta ✓
- **Porta:** Abertura para o exterior (ou painéis removíveis), puxador barra horizontal 0.90–1.10m

---

## 4. Sinalética e orientação

| Elemento | Especificação | Localização |
|---|---|---|
| Piso podoguia | Amarelo RAL 1018, relevo 5mm, contraste ≥70% LRV | Hall → elevador → IS acessível |
| Placa IS acessível | Pictograma ISo 7001 + braile "WC ACESSIVEL", altura 1.50m centro | Exterior porta IS |
| Degraus escada | Nosing contraste RAL 9016 sobre degrau cinza, faixa tátil 0.40m no patamar superior | Todas as escadas |
| Iluminação percurso | Mínimo 200 lux ao nível do piso, sensor movimento | Corredor piso 0, hall elevador |
| Planta tátil | Mapa em relevo da planta do piso 0, a 1.20m do chão | Entrada principal |

---

## 5. Checklist de entrega — Cuidai Braga

- [x] Percurso acessível exterior: rampa 6.0%, R11, corrimãos duplos ✓
- [x] Elevador EN 81-70 Cat.2, cabine 1.40×1.60m, botoneiras braile ✓
- [x] IS acessível 5.72m², transfer 0.90m, barras especificadas ✓
- [x] Sinalética tátil + visual + braile em todos os pontos críticos ✓
- [x] DL 163/2006 Artigos 10º, 11º e Anexo §§ 3.1, 4.3 verificados ✓
```

---

## Output anti-patterns

- **Dimensões sem contexto do projeto:** citar "mínimo 1.20m" sem calcular ou comparar com a dimensão real existente ou proposta
- **"Cumprir DL 163/2006" sem classificar o tipo de edifício:** a obrigatoriedade varia radicalmente — novo vs. reabilitação, nº de fogos, acesso público
- **IS acessível sem diagrama ou layout:** barras de apoio sem posição (esquerda/direita do transfer) são inúteis para o projetista
- **Elevador "conforme norma" sem especificar cabine:** omitir dimensão LxC e largura de porta impede verificação do shaft disponível
- **Isenções ignoradas:** não mencionar RERU ou estatuto de patrimônio quando aplicável é um erro de compliance, não apenas de qualidade
- **Sinalética tratada como cosmética:** omitir contraste LRV, braile, piso podoguia faz o output falhar na perspetiva do utilizador com deficiência visual
- **Recomendações sem priorização:** misturar requisitos obrigatórios com melhorias voluntárias sem distinção clara induz o cliente a erro na tomada de decisão orçamental
- **Aging-in-place genérico:** "preparar casa para o futuro" sem especificar reforços estruturais para barras, larguras de porta mínimas futuras, ou pré-instalação de plataforma elevatória
