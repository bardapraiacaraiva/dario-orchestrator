---
name: atlas-venue
description: Venue selection, scoring, site inspection, and management for events in Portugal. Weighted scoring matrix, 40+ item site inspection checklist, contract negotiation points, layout optimization with capacity calculators, outdoor considerations, and Portuguese venue specifics (Quintas, Palacios, Herdades, Espacos Municipais). Triggers on "venue", "espaco", "local evento", "quinta", "sala", "selecao espaco", "site visit", "visita ao local".
license: MIT
---

# ATLAS Skill — Venue Selection & Management

Systematic venue evaluation, comparison, and management process. From initial shortlist through contract negotiation to handover, this skill ensures the right space for the right event at the right price — with no surprises on event day. Calibrated for the Portuguese market with specific knowledge of venue types, licensing, and local regulations.

## When to activate

Invoke `/atlas-venue` (or trigger automatically) when:
- User needs to find or evaluate venues for an event
- User has venue options and needs a structured comparison
- User is preparing for a site inspection visit
- User needs to negotiate or review a venue contract
- User asks about capacity, layout options, or venue logistics
- After `atlas-briefing` defines event requirements

Do NOT use when:
- Venue is already booked and user needs day-of logistics (use `atlas-checklist`)
- User needs only a timeline (use `atlas-timeline`)
- Event is fully virtual with no physical venue

## Workflow

### 1. Define venue requirements from brief
Extract from `atlas-briefing` or gather directly:
- **Event type and format:** conference, gala, wedding, workshop, festival
- **Capacity needed:** seated, standing, mixed — with format-specific numbers
- **Date(s) and duration:** including setup/teardown time needed
- **Location constraints:** city/region, max travel time for attendees, proximity to hotels/airport
- **Budget for venue:** percentage of total budget allocated (typically 25-35%)
- **AV/production needs:** built-in vs. bring-your-own, power requirements
- **Catering model:** in-house mandatory, external allowed, own kitchen
- **Ambiance/brand fit:** formal, rustic, modern, historic, unique

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "event venue selection criteria scoring matrix", limit: 5)
mcp__dario-rag__search_kb(query: "Portugal venue types quintas palacios espacos municipais licensing", limit: 5)
```

### 3. Portuguese venue categories
| Category | Description | Best for | Price range (2026) | Licensing |
|---|---|---|---|---|
| **Quintas** | Rural estates with gardens, chapel, manor house | Weddings, corporate retreats, gala dinners | 3,000-15,000 EUR/day | Camara Municipal + IGAC |
| **Palacios/Solares** | Historic palaces, stately homes | Gala dinners, launches, awards, exclusive events | 5,000-25,000+ EUR/day | DGPC if classified + IGAC |
| **Herdades** | Alentejo estates, large outdoor spaces | Festivals, large corporate, team building | 2,000-12,000 EUR/day | CM + IGAC if music/entertainment |
| **Hoteis (salas)** | Hotel conference/banquet rooms | Conferences, seminars, corporate events | 1,500-8,000 EUR/day | Usually pre-licensed |
| **Centros de Congressos** | CCB, FIL, Altice Arena, CNEMA | Large conferences, trade shows, expos | 5,000-50,000+ EUR/day | Pre-licensed, union labor rules |
| **Espacos Municipais** | Camara-owned venues, cultural centers | Community events, workshops, public events | 200-3,000 EUR/day | CM approval, may be free for local events |
| **Rooftops/Terracos** | Urban terraces, panoramic venues | Cocktail receptions, launches, summer events | 2,000-10,000 EUR/day | Noise restrictions, capacity limits |
| **Museus/Galerias** | Museums, art galleries | Premium receptions, cultural events, launches | 3,000-20,000 EUR/day | Institutional approval, restrictions |
| **Espacos industriais** | Warehouses, factories, LX Factory type | Creative events, festivals, tech events | 1,500-8,000 EUR/day | Safety inspection, temporary license |
| **Outdoor (jardins, parques)** | Public parks, private gardens, beaches | Festivals, markets, summer events | 500-5,000 EUR + permits | CM permit, IGAC, environmental |

### 4. Venue scoring matrix (weighted)
Score each venue 1-5 on each criterion, multiply by weight:

| Criterion | Weight | Venue A | Venue B | Venue C |
|---|---|---|---|---|
| Capacity fit (right size, not too big/small) | 15% | /5 | /5 | /5 |
| Location & accessibility (transport, parking) | 12% | /5 | /5 | /5 |
| Cost vs. budget | 12% | /5 | /5 | /5 |
| AV/production capabilities | 10% | /5 | /5 | /5 |
| Catering quality/flexibility | 10% | /5 | /5 | /5 |
| Ambiance & brand alignment | 10% | /5 | /5 | /5 |
| Availability on required dates | 8% | /5 | /5 | /5 |
| Setup/teardown time allowed | 5% | /5 | /5 | /5 |
| Accommodation nearby/on-site | 5% | /5 | /5 | /5 |
| Exclusivity (sole use vs. shared) | 5% | /5 | /5 | /5 |
| Insurance & liability | 4% | /5 | /5 | /5 |
| Wet weather backup (if outdoor) | 4% | /5 | /5 | /5 |
| **Weighted total** | **100%** | **/5** | **/5** | **/5** |

### 5. Site inspection checklist (40+ items)

#### Access & Logistics
- [ ] Load-in access: dimensions (height, width), weight limits, ramp/level access
- [ ] Loading dock: availability, time restrictions, vehicle size limits
- [ ] Parking: attendee capacity, VIP parking, supplier/crew parking
- [ ] Public transport: nearest metro/bus, taxi rank, ride-share drop-off
- [ ] Disabled access: ramps, elevators, accessible WC, wheelchair seating positions
- [ ] Signage permissions: exterior banners, directional signs, branded entry

#### Space & Dimensions
- [ ] Main room dimensions: L x W x H (ceiling height critical for production)
- [ ] Pillar/column locations: obstruction map for sightlines
- [ ] Stage area: built-in or need to build, dimensions, weight load
- [ ] Breakout rooms: number, capacity, AV in each
- [ ] Registration/foyer area: size, flow, weather protection
- [ ] Green room/dressing rooms: for speakers, performers, VIPs
- [ ] Storage: secure storage for equipment, gifts, merchandise
- [ ] Cloakroom: capacity, staffed or self-service

#### Technical
- [ ] Power supply: total kVA available, distribution board locations, 3-phase availability
- [ ] Power outlets: locations, quantity, dedicated circuits for AV
- [ ] WiFi: capacity (simultaneous users), speed (upload/download), dedicated SSID possible
- [ ] Mobile signal: coverage inside venue (test all major operators: MEO, NOS, Vodafone)
- [ ] Built-in AV: projectors, screens, sound system, confidence monitors, recording
- [ ] Rigging points: ceiling load capacity for lighting/PA, truss mounting
- [ ] Blackout capability: can room be fully darkened for projections
- [ ] Climate control: HVAC capacity, independent zones, outdoor heating/cooling

#### Catering & Services
- [ ] Kitchen: commercial kitchen on-site, prep kitchen only, or none
- [ ] Catering model: exclusive caterer, approved list, or any external allowed
- [ ] Corkage policy: BYO beverages allowed, corkage fee per bottle
- [ ] Bar: fixed bars, mobile bar positions, license type (full, beer/wine only)
- [ ] Service areas: waiter stations, dishwashing, waste disposal
- [ ] Dining configurations: max seated dinner, max cocktail, max theater

#### Safety & Compliance
- [ ] Emergency exits: number, locations, signage, illuminated
- [ ] Fire safety: extinguishers, sprinklers, fire alarm, evacuation plan
- [ ] Maximum capacity: legal limit per room (Protecao Civil certificate)
- [ ] First aid: kit location, nearest hospital, AED defibrillator
- [ ] Security: in-house security, additional needed, CCTV
- [ ] Noise restrictions: decibel limits, curfew time, neighbor sensitivity
- [ ] Insurance: venue liability insurance, additional event insurance required

#### Operational
- [ ] Setup time: how many hours/days before event
- [ ] Teardown time: how many hours after event ends
- [ ] Curfew: hard stop time for music/event, latest departure
- [ ] Overnight: can setup remain overnight if multi-day build
- [ ] Exclusivity: sole use of venue or shared with other events
- [ ] Venue staff: included staff (reception, cleaning, security), additional cost
- [ ] Cleaning: included or additional charge, post-event cleaning expectations

### 6. Contract negotiation points
Key terms to negotiate/verify in Portuguese venue contracts:
- **Minimum spend:** is F&B minimum spend reasonable vs. event size
- **Corkage fees:** per-bottle rate for BYO (typically 5-15 EUR/bottle PT market)
- **Overtime rates:** cost per additional hour beyond contracted time
- **Force majeure clause:** what qualifies, refund vs. credit vs. reschedule
- **Cancellation policy:** sliding scale (100% refund >6mo, 50% 3-6mo, 0% <3mo is standard)
- **Deposit structure:** typically 25-50% on booking, balance 30 days before
- **Setup/teardown:** confirm hours included in price, additional hour rate
- **Exclusive vendor requirements:** must-use caterer, AV company, florist
- **Damage deposit:** amount, inspection process, return timeline
- **Weather clause (outdoor):** move-inside option, marquee permission, cancellation terms
- **Noise/curfew penalties:** fines for exceeding limits
- **Final numbers deadline:** when final headcount is due (usually 7-10 days before)

### 7. Layout configurations & capacity calculator
Standard capacity by format (per 100m2 usable space):

| Format | Capacity/100m2 | Best for | Setup time |
|---|---|---|---|
| Theater (rows, no tables) | 80-100 pax | Keynotes, presentations, ceremonies | 2h |
| Classroom (rows with tables) | 40-50 pax | Training, workshops, seminars | 3h |
| Banquet (round tables of 8-10) | 50-60 pax | Gala dinners, weddings, award ceremonies | 4h |
| Cocktail (standing, high tables) | 100-120 pax | Receptions, networking, launches | 2h |
| U-shape (single table) | 20-25 pax | Board meetings, workshops | 1h |
| Boardroom (single table) | 18-22 pax | Executive meetings, press conferences | 1h |
| Hollow square | 24-30 pax | Panel discussions, round tables | 2h |
| Cabaret (half-round tables) | 40-50 pax | Interactive workshops, team building | 3h |
| Exhibition (3x3m stands) | 8-10 stands | Trade shows, fairs, expos | 8h+ |

### 8. Outdoor venue additional considerations
- **Permits:** Camara Municipal outdoor event license (aplicar 30-60 dias antes)
- **IGAC license:** mandatory if music/entertainment (aplicar 30 dias antes)
- **Noise study:** may be required for residential areas (medicao acustica)
- **Weather contingency:** mandatory Plan B — marquee, indoor backup, postponement clause
- **Power supply:** generator rental (diesel, calculate kVA needs), cable routing, safety
- **Water supply:** portable water, WC facilities (1 unit per 50 pax minimum)
- **Shade/cover:** tents, sails, pergolas for sun/rain protection
- **Ground conditions:** level surface, grass vs. gravel, wheelchair accessible paths
- **Lighting:** event ends after sunset? full lighting plan needed
- **Environmental:** waste management plan, noise impact, protected areas

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-venue
venues_evaluated: <number>
recommended: <venue name>
---

# Venue Selection Report — <Event Name>

## Requisitos do Evento
| Parametro | Valor |
|---|---|
| Tipo de evento | ... |
| Capacidade necessaria | ... pax |
| Formato(s) | ... |
| Data(s) | ... |
| Localizacao preferida | ... |
| Budget venue | ... EUR |

## Venues Avaliados

### Venue A — <Name>
- **Localizacao:** ...
- **Capacidade:** ... (sentados) / ... (cocktail)
- **Preco:** ... EUR
- **Pontos fortes:** ...
- **Pontos fracos:** ...
- **Site visit realizada:** Sim/Nao

### Venue B — <Name>
[same structure]

### Venue C — <Name>
[same structure]

## Matriz de Scoring
| Criterio | Peso | Venue A | Venue B | Venue C |
|---|---|---|---|---|
| Capacidade | 15% | X | X | X |
| Localizacao | 12% | X | X | X |
| Custo | 12% | X | X | X |
| AV/Producao | 10% | X | X | X |
| Catering | 10% | X | X | X |
| Ambiente | 10% | X | X | X |
| [... all criteria] | | | | |
| **Total ponderado** | **100%** | **X.X** | **X.X** | **X.X** |

## Recomendacao
**Venue recomendado:** <name>
**Justificacao:** <2-3 sentences>

## Site Inspection Checklist (<Venue Name>)
[Completed checklist with findings]

## Pontos de Negociacao Contratual
| Ponto | Posicao do venue | Nossa posicao | Resultado |
|---|---|---|---|

## Layout Proposto
- **Formato:** ...
- **Capacidade neste formato:** ...
- **Planta esquematica:** [description]

## Proximos Passos
- [ ] Confirmar disponibilidade e bloquear data
- [ ] Negociar contrato com pontos identificados
- [ ] Agendar site visit tecnica com equipa AV
- [ ] Verificar licenciamento (IGAC/CM) se necessario
- [ ] Seguir com `atlas-budget` para orcamento completo
- [ ] Seguir com `atlas-timeline` para run-of-show adaptado ao espaco
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Venue Selection ATLAS.md`

## Red flags — don't do this
- Never book a venue without a physical site visit — photos lie about dimensions, columns, access, and ambiance
- Never ignore noise restrictions and curfew — Portuguese municipalities enforce these strictly and fines can reach 10,000+ EUR
- Never accept a venue without confirming setup/teardown time in writing — "you can set up from 8am" means nothing without a contract clause
- Never skip the outdoor weather contingency — Portugal's weather is generally good but a single rain day without a Plan B ruins the entire event
- Never assume WiFi capacity from the venue's claim — always test with concurrent device load; "high-speed WiFi" often means 20 Mbps shared among 300 people
- Never overlook exclusive vendor requirements — discovering the venue mandates their 80 EUR/head caterer when your budget is 35 EUR/head is a deal-breaker
- Never sign without a clear force majeure and cancellation clause — post-COVID, this is non-negotiable
- Never forget to check IGAC licensing requirements for events with music or entertainment — operating without it risks shutdown and fines

## Interactions
- Follows `atlas-briefing` for event requirements
- Feeds into `atlas-budget` with confirmed venue costs
- Feeds into `atlas-timeline` with setup/teardown windows and curfew constraints
- Feeds into `atlas-checklist` with venue-specific operational requirements
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-venue** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-venue:**

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
