---
name: atlas-timeline
description: Event timeline and run-of-show generator. Pre-event milestones (12-month to day-before), minute-by-minute day-of run sheet, setup/teardown timelines, vendor coordination, buffer management, and critical path analysis. Triggers on "timeline evento", "run of show", "cronograma evento", "run sheet", "horario evento", "agenda evento", "event schedule", "programa evento".
license: MIT
---

# ATLAS Skill — Event Timeline & Run-of-Show

Generates two complementary deliverables: (1) a pre-event planning timeline with milestones from kickoff to day-before, and (2) a minute-by-minute day-of Run-of-Show (ROS) that serves as the master operational document. Every person involved in the event should be able to look at the ROS and know exactly what happens, where, when, and who is responsible.

## When to activate

Invoke `/atlas-timeline` (or trigger automatically) when:
- User is planning a new event and needs a planning schedule
- User needs a day-of run sheet for an upcoming event
- User asks "quando comecamos a preparar" or "como organizar o dia"
- User needs to coordinate multiple vendors for event day
- After `atlas-briefing` and `atlas-venue` are complete
- User has a confirmed event date and needs reverse-planning milestones

Do NOT use when:
- User needs only a budget (use `atlas-budget`)
- User needs post-event analysis (use `atlas-post-event`)
- Event is fully virtual with no physical logistics

## Workflow

### 1. Gather timeline inputs
From `atlas-briefing` and `atlas-venue` or directly:
- **Event date(s):** confirmed date, setup days, teardown days
- **Event type:** determines milestone complexity
- **Scale:** intimate (<50) vs massive (1,000+) changes lead times
- **Venue confirmed:** setup/teardown windows, curfew, load-in access hours
- **Key components:** speakers, entertainment, catering, AV production, registration
- **Vendor count:** how many external vendors to coordinate
- **Rehearsal needed:** yes/no (complex events with speakers, performances, cues)

If event date is not confirmed, flag this as blocker.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "event planning timeline milestones pre-event checklist", limit: 5)
mcp__dario-rag__search_kb(query: "run of show run sheet event day schedule template", limit: 5)
```

### 3. Pre-event planning timeline
Adapt milestones based on event scale and complexity:

#### 12 months before (large/complex events only)
- [ ] Define event objectives and KPIs (`atlas-briefing`)
- [ ] Set preliminary budget (`atlas-budget`)
- [ ] Research and shortlist venues (`atlas-venue`)
- [ ] Book venue (popular venues book 12+ months ahead in PT)
- [ ] Identify key speakers/entertainment (high-profile: 6-12 months lead)
- [ ] Establish event committee / working group
- [ ] Create event brand identity if new event

#### 6 months before
- [ ] Confirm venue contract and deposit paid
- [ ] Finalize event program structure (sessions, breaks, entertainment)
- [ ] Confirm keynote speakers / entertainment and contracts signed
- [ ] Begin sponsorship outreach (if applicable)
- [ ] Select and brief AV/production company
- [ ] Select and brief caterer (menu development begins)
- [ ] Launch event website / registration page
- [ ] Begin marketing campaign (save-the-date)
- [ ] Obtain necessary licenses (IGAC: 30 dias, CM permits: 30-60 dias)

#### 3 months before
- [ ] Finalize program with all session details
- [ ] Confirm all vendors and contracts signed
- [ ] Open ticket sales / registration (if applicable)
- [ ] Finalize sponsorship packages and deliverables
- [ ] Brief photographer/videographer
- [ ] Order branded materials (signage, badges, programs, gifts)
- [ ] Confirm accommodation blocks for speakers/VIPs
- [ ] Plan transport logistics (shuttles, transfers)
- [ ] Develop contingency plans (weather, no-show speakers, technical failure)
- [ ] Begin attendee communications (program highlights, logistics info)

#### 1 month before
- [ ] Production schedule finalized with AV company
- [ ] Menu finalized with caterer, dietary requirements collected
- [ ] Confirm all speaker presentations received
- [ ] Seating plan draft (if seated event)
- [ ] Registration system tested end-to-end
- [ ] Signage and print materials in production
- [ ] Event app configured and tested (if applicable)
- [ ] Confirm staffing plan and brief event team
- [ ] Final venue site visit with production team
- [ ] Distribute Run-of-Show v1 to all stakeholders

#### 2 weeks before
- [ ] Final headcount to venue and caterer (check final numbers deadline)
- [ ] Run-of-Show v2 distributed (refined after production meeting)
- [ ] All print materials delivered and checked
- [ ] Confirm all vendor arrival times and contact numbers
- [ ] Brief all staff on roles, radio channels, escalation paths
- [ ] Test all technology (AV, WiFi, registration, streaming)
- [ ] Confirm emergency procedures with venue
- [ ] Send final attendee communications (logistics, parking, dress code)

#### 1 week before
- [ ] Final Run-of-Show v3 (locked version) distributed
- [ ] All presentations loaded and tested on venue system
- [ ] Confirm weather forecast (outdoor events: Go/No-Go decision)
- [ ] Reconfirm all vendors (arrival time, contact, requirements)
- [ ] Pack event kit (supplies, emergency kit, printed ROS, contacts list)
- [ ] Final team briefing
- [ ] Social media content scheduled

#### Day before
- [ ] Venue walkthrough with full team
- [ ] Stage/set build begins (if multi-day setup)
- [ ] AV install and sound check
- [ ] Signage placement
- [ ] Registration desk setup and test
- [ ] Catering walk-through (confirm timings, service points, dietary)
- [ ] Rehearsal (speakers, MCs, award presenters, performers)
- [ ] Emergency briefing with venue and security
- [ ] Team dinner / final alignment
- [ ] Charge all devices, radios, batteries

### 4. Day-of Run-of-Show (ROS)
The master operational document. Format as minute-by-minute with these columns:

| Time | Duration | Activity | Location | Responsible | Equipment/AV | Cue/Notes |
|---|---|---|---|---|---|---|
| 06:00 | 60min | Crew call, load-in | Loading dock | Production Manager | Truck access, trolleys | Security opens dock |
| 07:00 | 120min | AV setup & test | Main hall | AV Lead | PA, projector, screens | Power on by 07:00 |
| 07:00 | 120min | Catering setup | Kitchen + service areas | Catering Manager | Tables, linens, service | Parallel with AV |
| 08:00 | 60min | Registration setup | Foyer | Registration Lead | iPads, badges, signage | WiFi test |
| 08:30 | 30min | Sound check speakers | Main hall | AV Lead + Speakers | Mics, presentation | Speakers arrive 08:15 |
| 09:00 | 30min | Team briefing | Backstage | Event Director | Radios distributed | Final ROS review |
| 09:00 | 30min | Final walk-through | All areas | Event Director | Checklist | Fix any issues |
| 09:30 | - | **Doors open** | Main entrance | Registration team | Badge scanning | Music: ambient |
| 09:30 | 30min | Welcome coffee | Foyer | Catering | Coffee, pastries | Service until 10:00 |
| 10:00 | 5min | **Event start** — Welcome | Main stage | MC / Host | Mic, confidence monitor | Cue: lights dim |
| 10:05 | 45min | Keynote 1 | Main stage | Speaker A | Presentation, clicker | Q&A: 10min |
| 11:00 | 30min | **Coffee break** | Foyer | Catering | Coffee, snacks | Networking time |
| ... | ... | ... | ... | ... | ... | ... |
| 22:00 | - | **Event end** | All | Event Director | - | Final announcement |
| 22:00 | 30min | Guest departure | Main entrance | Security + team | Lighting, signage | Taxi queue managed |
| 22:30 | 120min | Teardown begins | All areas | Production Manager | - | Venue handback by 00:30 |

### 5. Buffer management rules
- **Minimum 15-minute buffer** between back-to-back sessions
- **30-minute buffer** before doors open (after final walk-through)
- **Sound check ALWAYS before doors** — never after attendees arrive
- **Catering buffers:** 15min before service for final prep, 15min transition between courses
- **Speaker transition:** 5-10min for mic swap, presentation load, stage reset
- **Contingency slot:** build one 15-30min flexible slot into the program for overruns
- **Hard stops:** curfew, transport departures, venue handback — these are immovable

### 6. Vendor coordination timeline
For each vendor, specify:

| Vendor | Arrival | Setup complete by | Test/check | During event | Teardown starts | Departs by |
|---|---|---|---|---|---|---|
| AV/Production | 06:00 | 08:30 | 08:30-09:00 | Continuous | 22:00 | 00:30 |
| Catering | 07:00 | 09:30 | 09:00 (walk-through) | Continuous | 22:30 | 01:00 |
| Florist/Decor | 07:00 | 09:00 | - | - | 22:30 | 23:30 |
| Photographer | 09:00 | - | - | 09:00-22:00 | - | 22:00 |
| Entertainment/DJ | 18:00 | 19:00 | 19:00-19:30 | 20:00-22:00 | 22:00 | 23:00 |
| Security | 08:00 | - | 08:30 (briefing) | 08:00-23:00 | - | 23:00 |

### 7. Critical path analysis
Identify the longest sequential chain that determines minimum event setup time:
```
Venue access -> Load-in -> AV install -> AV test -> Sound check -> Doors open -> Event start
```
Any delay in this chain directly delays the event. Parallel activities (catering setup, decor, registration) have float unless they also depend on the critical path.

Flag activities with zero float — these are the ones that need backup plans.

### 8. Portuguese calendar considerations
- **August:** many vendors on holiday, reduced availability, premium pricing
- **Christmas/New Year (20 Dec - 6 Jan):** limited availability, higher costs
- **Santos Populares (June):** Lisbon (Santo Antonio 12-13 Jun), Porto (Sao Joao 23-24 Jun) — street closures, noise competition
- **Easter week:** reduced vendor availability
- **Feriados nacionais:** 10 public holidays — check against event date
- **Football/major events:** check Selecao schedule, UEFA/FIFA events — attendance impact
- **Academic calendar:** June exams, September back-to-school — affects some venues and audiences

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-timeline
event_date: <YYYY-MM-DD>
setup_days: <N>
total_vendors: <N>
---

# Event Timeline & Run-of-Show — <Event Name>

## Resumo
| Parametro | Valor |
|---|---|
| Evento | ... |
| Data | ... |
| Local | ... |
| Duracao | ... |
| Setup | ... |
| Teardown | ... |
| Vendors | ... |

## Pre-Event Planning Timeline
### 6 meses antes — [date range]
- [ ] ...
### 3 meses antes — [date range]
- [ ] ...
### 1 mes antes — [date range]
- [ ] ...
### 2 semanas antes — [date range]
- [ ] ...
### 1 semana antes — [date range]
- [ ] ...
### Vespera — [date]
- [ ] ...

## Run-of-Show (Dia do Evento)
| Hora | Dur. | Actividade | Local | Responsavel | Equipamento | Notas/Cue |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

## Coordenacao de Vendors
| Vendor | Chegada | Setup pronto | Teste | Durante | Desmontagem | Saida |
|---|---|---|---|---|---|---|

## Caminho Critico
[Sequential chain with zero float]

## Buffers e Contingencia
| Buffer | Duracao | Localizacao no programa |
|---|---|---|

## Riscos de Timeline
| Risco | Impacto | Mitigacao |
|---|---|---|

## Proximos Passos
- [ ] Distribuir ROS a todos os stakeholders
- [ ] Agendar production meeting com vendors
- [ ] Confirmar horarios de acesso ao venue
- [ ] Preparar `atlas-checklist` para dia do evento
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Timeline & ROS ATLAS.md`

## Red flags — don't do this
- Never schedule sound check after doors open — attendees arriving to screeching feedback is unprofessional and ruins first impressions
- Never eliminate buffers to "fit more in" — events without buffers cascade into chaos; a single 10-minute overrun destroys the rest of the day
- Never have vendor arrival times that conflict with each other at the loading dock — stagger arrivals or confirm multiple access points
- Never skip rehearsal for complex events (award ceremonies, multi-speaker, live entertainment) — "we'll figure it out on the day" is the recipe for disaster
- Never lock the ROS without input from all key vendors — the AV company, caterer, and venue each have constraints that must be integrated
- Never forget the teardown timeline — venue handback is contractual and overtime fees in PT can be 500-2,000 EUR/hour
- Never plan critical outdoor activities during Portuguese rain season (Oct-Mar) without a weather contingency in the ROS
- Never assume vendors know the ROS — distribute, walk through, confirm receipt, and carry printed copies on event day

## Interactions
- Follows `atlas-briefing` (objectives, format) and `atlas-venue` (space constraints, curfew)
- Feeds into `atlas-checklist` for day-of operational checklists
- Feeds into `atlas-budget` for cost phasing aligned with timeline milestones
- Links to `atlas-post-event` for debrief on timeline adherence
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-timeline** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-timeline:**

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
