---
name: atlas-checklist
description: Day-of event checklists and operational run sheets. Master checklist by category (venue, AV, catering, registration, VIP, H&S, contingency), pre-event/day-of/during/closing checklists, emergency procedures, staff assignment matrix, Go/No-Go framework, and printable templates. Triggers on "checklist evento", "day-of checklist", "lista verificacao", "preparacao evento", "event checklist", "go no go", "emergency plan evento".
license: MIT
---

# ATLAS Skill — Day-of Checklists & Operational Run Sheets

The operational backbone of event execution. Produces category-specific checklists for every phase of event day — from crew arrival through venue handback. Includes emergency procedures, staff assignments, communication protocols, and the critical Go/No-Go decision framework. Designed to be printed on A4, laminated, and carried by every team lead.

## When to activate

Invoke `/atlas-checklist` (or trigger automatically) when:
- User is preparing for an upcoming event (1-2 weeks before)
- User needs a day-of operational plan
- User asks "o que nao posso esquecer" or "checklist para o dia"
- User needs emergency/contingency procedures for an event
- User needs to brief event staff on roles and responsibilities
- After `atlas-timeline` defines the run-of-show

Do NOT use when:
- User is in early planning phase (use `atlas-briefing`)
- User needs a budget (use `atlas-budget`)
- User needs post-event analysis (use `atlas-post-event`)

## Workflow

### 1. Gather checklist inputs
From `atlas-timeline` and `atlas-venue` or directly:
- **Event type and scale:** determines checklist depth
- **Venue specifics:** access times, curfew, emergency exits, venue contact
- **Team size:** how many staff, volunteers, vendors
- **Program complexity:** single track vs. multi-track, entertainment, VIP program
- **Risk factors:** outdoor, large-scale, alcohol served, high-profile guests
- **Communication tools:** radios, WhatsApp group, walkie-talkie channels

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "event day checklist operations run sheet", limit: 5)
mcp__dario-rag__search_kb(query: "event emergency procedures evacuation health safety", limit: 5)
```

### 3. Master checklist categories

#### A. Venue Checklist
- [ ] Venue contact on-site confirmed and mobile number saved
- [ ] All rooms unlocked and accessible as contracted
- [ ] Climate control set to correct temperature (20-22C winter, 22-24C summer)
- [ ] Lighting preset configured (or manual settings confirmed)
- [ ] Toilets clean, stocked, and signposted (including accessible WC)
- [ ] Parking arrangements confirmed, signage placed
- [ ] Loading dock clear for vendor arrivals
- [ ] Venue damage pre-inspection completed and photographed
- [ ] Smoking area identified and signposted
- [ ] Cloakroom ready (hangers, tickets, staff assigned)
- [ ] Venue cleaning schedule confirmed for during-event touch-ups

#### B. AV / Production Checklist
- [ ] All equipment arrived and inventory checked against spec sheet
- [ ] Main PA system tested at event volume levels
- [ ] All microphones tested (handheld, lapel, headset — backup mics ready)
- [ ] Projector/LED wall tested with actual presentations
- [ ] Confidence monitor operational and positioned for speakers
- [ ] Presentation laptop configured (no screensaver, no updates, airplane mode)
- [ ] All presentations loaded, tested, and backed up on USB
- [ ] Video playback tested (including sound through PA)
- [ ] Lighting programmed and cued (house lights, stage, ambient)
- [ ] Recording equipment operational (if recording sessions)
- [ ] Live stream tested end-to-end including audio (if streaming)
- [ ] WiFi tested under load (speed test, attendee network vs. production network)
- [ ] Backup equipment identified and accessible (spare projector, cables, mics)
- [ ] AV technician briefed on run-of-show and cue points

#### C. Catering Checklist
- [ ] Final headcount communicated and confirmed in writing
- [ ] Menu confirmed including all dietary alternatives
- [ ] Dietary flags system confirmed (how to identify special meals)
- [ ] Service times confirmed and aligned with run-of-show
- [ ] Table layout matches floor plan (table numbers, seating chart if assigned)
- [ ] Bar setup complete with correct stock levels
- [ ] Non-alcoholic options prominently available
- [ ] Water stations positioned and stocked (refill schedule confirmed)
- [ ] Allergen information displayed at food stations (EU Regulation 1169/2011)
- [ ] Kitchen/service area clean and health-safety compliant
- [ ] Waste disposal plan confirmed (recycling, organic, general)
- [ ] Catering manager introduced to event director, radio channel assigned

#### D. Registration & Guest Services Checklist
- [ ] Registration desk set up with signage visible from entrance
- [ ] Registration system online and tested (scan, search, manual check-in)
- [ ] Badge printer operational with spare ribbons/cards
- [ ] Pre-printed badges organized alphabetically and by category
- [ ] Walk-in/on-site registration process defined
- [ ] Guest list printed as backup (battery/WiFi failure contingency)
- [ ] Welcome packs/bags ready and organized
- [ ] Information desk staffed (program, WiFi password, facilities map)
- [ ] Attendee WiFi credentials posted/shared
- [ ] Event app push notification tested (if applicable)
- [ ] Lost and found box/area designated

#### E. VIP Management Checklist
- [ ] VIP list confirmed with photos for recognition
- [ ] VIP welcome protocol defined (who greets, where, what they receive)
- [ ] VIP lounge/area set up and stocked
- [ ] VIP seating reserved and marked
- [ ] VIP parking arranged with clear directions
- [ ] VIP gifts/packs prepared and personalized
- [ ] VIP hosts assigned (1 host per 3-5 VIPs for high-touch events)
- [ ] Speaker green room stocked (water, snacks, chargers, mirror)
- [ ] Speaker/VIP transport confirmed (arrivals and departures)
- [ ] Press/media credentialing ready (if media attend)

#### F. Signage & Wayfinding Checklist
- [ ] Exterior directional signage placed (from parking/street to entrance)
- [ ] Welcome/entrance signage branded and visible
- [ ] Room/session signage installed at each location
- [ ] Registration desk signage (A-L, M-Z, VIP, Press, etc.)
- [ ] Restroom directional signs
- [ ] Emergency exit signs visible and unobstructed
- [ ] Sponsor signage placed per contractual agreements
- [ ] Schedule board/digital display showing program
- [ ] WiFi password displayed at key locations

#### G. Health & Safety Checklist
- [ ] Emergency exits identified, unobstructed, and illuminated
- [ ] Evacuation plan posted at all exits
- [ ] Fire extinguishers accessible and within inspection date
- [ ] First aid kit stocked and location known to all team leads
- [ ] AED (defibrillator) location identified and accessible
- [ ] First aid trained person on-site identified
- [ ] Nearest hospital identified with address and route (share with team)
- [ ] Emergency contact numbers printed and distributed:
  - INEM/112
  - Nearest hospital
  - Venue security
  - Event director mobile
  - Event owner mobile
- [ ] Trip hazards eliminated (cables taped/ramped, no loose carpets)
- [ ] Maximum capacity not exceeded (Protecao Civil limits)
- [ ] Food safety compliance verified (ASAE standards, temperature logs)
- [ ] COVID/health protocols if applicable (ventilation, sanitation stations)

### 4. Phase-specific checklists

#### Pre-Event (Day Before)
| Time | Task | Responsible | Done |
|---|---|---|---|
| AM | Venue walkthrough with team leads | Event Director | [ ] |
| AM | AV install begins | AV Lead | [ ] |
| PM | Signage placement | Operations | [ ] |
| PM | Registration desk setup and system test | Registration Lead | [ ] |
| PM | Catering walk-through (service flow, timing) | Catering Manager | [ ] |
| PM | Emergency briefing with venue and security | Event Director + Venue | [ ] |
| PM | Rehearsal (speakers, MC, award presenters) | Event Director | [ ] |
| EVE | Team briefing: roles, radios, run-of-show review | Event Director | [ ] |
| EVE | Vendor confirmations (all reconfirmed for tomorrow) | Event Coordinator | [ ] |

#### Day-of Opening (Crew Call to Doors Open)
| Time | Task | Responsible | Done |
|---|---|---|---|
| Crew call | Team arrives, signs in, collects radio | All | [ ] |
| +15min | Team briefing: weather, changes, priorities | Event Director | [ ] |
| +15min | Communications test (all radios, channels) | Operations | [ ] |
| +30min | AV final check (presentations, sound, lights) | AV Lead | [ ] |
| +30min | Registration final check (system, badges, backup list) | Registration Lead | [ ] |
| +45min | Catering confirm (service ready, dietary flagged) | Catering Manager | [ ] |
| +45min | VIP area final check | VIP Host | [ ] |
| +50min | Photographer/videographer arrives, briefed on key shots | Event Coordinator | [ ] |
| +55min | Final walk-through: all areas | Event Director | [ ] |
| +60min | **DOORS OPEN** | All | [ ] |

#### During Event Monitoring
- [ ] Attendance counts (registration numbers at 30min intervals)
- [ ] Session attendance (room counts for each session)
- [ ] F&B consumption tracking (reorder triggers, running out alerts)
- [ ] Social media monitoring (hashtag, mentions, sentiment)
- [ ] Issue log maintained (real-time log of problems and resolutions)
- [ ] Speaker management (next speaker in green room 15min before slot)
- [ ] Temperature monitoring (rooms, outdoor areas)
- [ ] Noise level monitoring (if restrictions apply)
- [ ] VIP satisfaction check (discreet check-in with key guests)
- [ ] Sponsor deliverables tracking (are all sponsor commitments being met)

#### Closing Checklist
| Time | Task | Responsible | Done |
|---|---|---|---|
| -30min | Final session warning to AV and MC | Event Director | [ ] |
| -15min | Bar last orders announced | Catering Manager | [ ] |
| Event end | Closing remarks, thank-yous by MC/host | MC + Event Owner | [ ] |
| +5min | House lights up, closing music | AV Lead | [ ] |
| +10min | VIP departure coordination (cars, coats) | VIP Host | [ ] |
| +15min | Guest departure managed (exits, taxis, transport) | Operations | [ ] |
| +30min | Venue sweep: lost and found, personal items | Operations | [ ] |
| +30min | Sponsor materials return / collection | Event Coordinator | [ ] |
| +45min | Teardown begins (when last guests depart) | Production Manager | [ ] |
| +60min | Catering breakdown and kitchen handback | Catering Manager | [ ] |
| +90min | AV and production load-out | AV Lead | [ ] |
| +120min | Final venue inspection with venue manager | Event Director + Venue | [ ] |
| +120min | Venue handback: condition check, keys, damage report | Event Director | [ ] |
| +120min | Damage deposit release process initiated | Event Coordinator | [ ] |

### 5. Staff assignment matrix

| Role | Person | Radio Channel | Mobile | Backup |
|---|---|---|---|---|
| Event Director | ... | Ch 1 (Command) | ... | ... |
| Production Manager | ... | Ch 1 (Command) | ... | ... |
| AV Lead | ... | Ch 2 (Production) | ... | ... |
| Registration Lead | ... | Ch 3 (Front of House) | ... | ... |
| Catering Manager | ... | Ch 4 (Catering) | ... | ... |
| VIP Host | ... | Ch 1 (Command) | ... | ... |
| Security Lead | ... | Ch 5 (Security) | ... | ... |
| Event Coordinator(s) | ... | Ch 3 (Front of House) | ... | ... |

**Escalation path:** Team Member -> Team Lead -> Event Coordinator -> Event Director -> Event Owner

**Radio discipline:** Channel 1 = command only, other channels for operational chatter. Switch to channel 1 for emergencies only.

### 6. Emergency procedures

#### Fire / Evacuation
1. Alert Event Director on Channel 1: "CODE RED — [location]"
2. AV cuts music, house lights full, MC announces calm evacuation
3. Staff guide guests to nearest emergency exits (know your exit assignment)
4. Assembly point: [pre-defined location outside venue]
5. Team leads do headcount of their zones
6. Call 112 if not already done
7. No one re-enters until all-clear from fire brigade

#### Medical Emergency
1. Alert Event Director: "CODE BLUE — [location]"
2. First-aider responds immediately
3. Clear area around patient, maintain privacy
4. Call 112 / INEM if serious
5. Guide ambulance to venue entrance — assign one person as ambulance guide
6. Event continues in other areas unless impractical

#### Weather Emergency (outdoor events)
1. Monitor weather radar from 48h before (IPMA.pt)
2. **Go/No-Go** decision: 4 hours before if severe weather forecast
3. If weather turns during event: move to indoor backup or covered area
4. Lightning protocol: stop immediately, move indoors, wait 30min after last strike
5. Heavy rain: activate drainage plan, non-slip mats at entrances

#### Security Incident
1. Alert Security Lead and Event Director: "CODE ORANGE — [location]"
2. Isolate the area, do not confront
3. Security handles, police called if needed (PSP/GNR)
4. Protect guests and staff first, property second
5. Document incident for report

### 7. Go/No-Go decision framework
At T-4 hours, Event Director evaluates:

| Criterion | Go | No-Go | Status |
|---|---|---|---|
| Venue accessible and ready | Yes | Critical failure | [ ] |
| AV/Production operational | Yes, or acceptable backup | Total failure, no backup | [ ] |
| Catering confirmed | Yes | Caterer no-show, no alternative | [ ] |
| Weather (outdoor) | Acceptable or backup available | Severe weather, no indoor option | [ ] |
| Minimum attendance viable | >50% of target | <25% of target (cost/reputation) | [ ] |
| Safety compliance | All checks passed | Critical safety failure | [ ] |
| Key personnel present | Event Director + 2 leads | Event Director absent, no delegate | [ ] |
| Communications working | Radios + mobile | No communication system | [ ] |

**Decision authority:** Event Director, with Event Owner consulted on cancellation.
**Postponement:** preferred over cancellation. Refund only as last resort.

### 8. Event emergency kit (physical kit to carry)
Pack in a clearly labeled bag/box:
- Printed Run-of-Show (5 copies)
- Printed guest list (backup)
- Printed staff contact list
- Printed emergency procedures
- Radio batteries (spare set)
- Phone charger / power bank
- Gaffer tape (black + white)
- Cable ties (assorted)
- Scissors, box cutter
- Pens, markers (Sharpie), notepads
- Safety pins, sewing kit
- Painkillers (paracetamol, ibuprofen)
- Plasters / first aid basics
- Stain remover pen
- Breath mints
- Umbrella (compact)
- Torch/flashlight
- Cash (100 EUR in small notes — emergency tips, taxis, small purchases)

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-checklist
event_date: <YYYY-MM-DD>
team_size: <N>
---

# Day-of Checklists — <Event Name>

## Staff Assignment Matrix
| Papel | Nome | Radio | Telemovel | Backup |
|---|---|---|---|---|

## Go/No-Go (T-4 horas)
| Criterio | Status |
|---|---|

## Checklists por Categoria
### A. Venue [ /11 ]
### B. AV/Producao [ /14 ]
### C. Catering [ /12 ]
### D. Registo/Acolhimento [ /11 ]
### E. VIP [ /10 ]
### F. Sinalctica [ /9 ]
### G. Saude e Seguranca [ /14 ]

## Checklists por Fase
### Vespera
### Abertura (Crew Call -> Portas Abertas)
### Durante o Evento
### Encerramento e Desmontagem

## Procedimentos de Emergencia
### Incendio/Evacuacao
### Emergencia Medica
### Meteorologia (outdoor)
### Incidente de Seguranca

## Kit de Emergencia
[Packed items checklist]

## Proximos Passos
- [ ] Imprimir todos os checklists em A4
- [ ] Distribuir a team leads 48h antes
- [ ] Briefing final com toda a equipa na vespera
- [ ] Seguir com `atlas-post-event` apos o evento
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Day-of Checklists ATLAS.md`

## Red flags — don't do this
- Never operate without a printed emergency procedure — digital fails when you need it most (dead battery, no signal)
- Never have a single point of failure on any critical role — every lead needs a named backup who knows the role
- Never skip the communications test — discovering radio dead zones during the event is too late
- Never assume the venue's emergency plan covers your event — your event layout changes exits, capacities, and flows
- Never let the Go/No-Go decision default to "go" without explicitly checking all criteria — cancellation costs less than a disaster
- Never forget the venue handback inspection — undocumented damage becomes your liability and your damage deposit
- Never serve food without visible allergen information — anaphylaxis is a life-threatening emergency and a legal liability under EU Regulation 1169/2011
- Never rely solely on digital check-in — always have a printed guest list backup

## Interactions
- Follows `atlas-timeline` for run-of-show integration
- Follows `atlas-venue` for venue-specific safety and operational requirements
- Links to `atlas-budget` for day-of vendor payment settlements
- Feeds into `atlas-post-event` for debrief on what worked and what failed
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-checklist** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-checklist:**

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
