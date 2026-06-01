---
name: atlas-transport
description: Transportation & Fleet Logistics for events -- guest transport, route planning, parking management, fleet coordination, airport logistics, load-in scheduling, equipment transport, shuttle services, accessibility. Portuguese specifics including Lisbon traffic, bridges, ferries, tuk-tuks. Triggers on "transporte", "transport", "shuttle", "transfer", "estacionamento", "parking", "load-in", "carga descarga", "fleet", "frota", "aeroporto", "airport transfer", "autocarros", "coaches".
license: MIT
---

# ATLAS Skill -- Transportation & Fleet Logistics

End-to-end transport planning for events: guest transfers, fleet coordination, route optimization, parking management, airport logistics, equipment delivery, and load-in scheduling. Covers all transport modes with deep Portuguese context including Lisbon/Porto traffic patterns, bridge timing, ferry options, and local fleet resources.

## When to activate

Invoke `/atlas-transport` (or trigger automatically) when:
- User needs to plan guest transportation (shuttles, transfers, coaches)
- User needs airport transfer logistics for speakers/VIPs/delegates
- User needs to plan equipment load-in and delivery scheduling
- User needs parking management for an event
- User asks about route planning or traffic considerations
- User needs fleet coordination for multiple vehicles
- User asks about transport options in Lisbon/Porto or other Portuguese cities

Do NOT use when:
- Booking accommodation (use `atlas-accommodation`)
- General vendor procurement for transport companies (use `atlas-vendor`)
- Event staging and technical load-in specs (use `atlas-staging`)

## Workflow

### 1. Gather transport requirements
- **Event location** -- full address, GPS coordinates, access routes
- **Guest count** -- total, plus breakdown by transport need
- **Guest origin points** -- hotels, airport, train station, city center, parking
- **VIP count** -- separate transport requirements
- **Event schedule** -- arrival window, departure time, multi-day considerations
- **Equipment/production** -- what needs to be delivered, dimensions, weight
- **Accessibility needs** -- wheelchair users, mobility assistance
- **Budget** -- transport allocation from `atlas-budget`
- **Venue constraints** -- vehicle size limits, loading dock specs, access hours

### 2. Guest transport modes

| Mode | Capacity | Best For | Cost Range PT 2026 | Notes |
|---|---|---|---|---|
| Executive car | 1-3 pax | VIP, speakers, C-suite | 50-150 EUR/transfer | Mercedes E-class or similar |
| Van (premium) | 5-7 pax | Small VIP groups | 80-200 EUR/transfer | Mercedes V-class |
| Minibus | 16-24 pax | Hotel-venue shuttle | 200-400 EUR/half day | With driver |
| Coach (standard) | 50-55 pax | Large group transfers | 400-800 EUR/half day | Autoestrada capable |
| Coach (premium) | 40-50 pax | Long distance, VIP groups | 600-1,200 EUR/half day | WC, Wi-Fi, recline |
| Tuk-tuk | 2-4 pax | Lisbon city tours, fun transfers | 30-80 EUR/trip | Iconic, not for luggage |
| River boat/ferry | 20-200 pax | Tagus crossing, scenic arrival | 500-5,000 EUR/charter | Weather dependent |
| Vintage car/classic | 1-3 pax | Wedding, CEO arrival | 200-500 EUR/event | Photo opportunity |
| Electric scooter fleet | Individual | Young/tech conferences | 5-10 EUR/pp/day | Partner with Lime/Bolt |
| Train charter | 50-200 pax | Inter-city, large delegations | Negotiated with CP | Porto-Lisboa groups |

### 3. Route planning

**Pre-event route analysis:**
- Primary route: fastest under normal conditions
- Secondary route: alternative avoiding known bottleneck
- Emergency route: fastest to nearest hospital
- All routes tested at same time-of-day as event

**Route documentation per vehicle:**
| Field | Detail |
|---|---|
| Origin | Address + GPS coordinates |
| Destination | Address + GPS coordinates |
| Primary route | Street-by-street or highway exits |
| Distance / time (normal) | X km / Y minutes |
| Distance / time (peak) | X km / Y minutes |
| Alternative route | Description + trigger conditions |
| Fuel/charging stops | If applicable for long routes |
| Waypoints | Pickup points if multi-stop |
| Speed restrictions | School zones, residential, construction |
| Vehicle restrictions | Weight limits, height limits, width limits |

### 4. Portuguese traffic specifics

**Lisbon critical patterns:**
| Factor | Detail | Recommendation |
|---|---|---|
| Ponte 25 de Abril | Heavy congestion 07:30-10:00 (south-north), 17:00-20:00 (north-south) | Avoid crossing during peaks; use Vasco da Gama if destination is east |
| Ponte Vasco da Gama | Less congested but longer route for west Lisbon venues | Best for Parque das Nacoes, Montijo, east bank venues |
| A1 (north) | Heavy Friday PM outbound, Sunday PM inbound | Schedule around weekend migration |
| A2 (south/Algarve) | Heavy holiday weekends, summer Fridays | Allow 2x normal time in July/August |
| Segunda Circular / Eixo N-S | Permanent congestion 08:00-10:00, 17:30-19:30 | Avoid for time-critical transfers |
| City center (Baixa/Chiado) | Narrow streets, tram lines, pedestrian zones | Minibus maximum, no coaches |
| Belem area | Tourist congestion, limited parking | Pre-book parking, arrive early |
| Parque das Nacoes | Good access, ample parking | Best logistics hub for large events |

**Porto critical patterns:**
| Factor | Detail |
|---|---|
| Ponte da Arrabida / D. Luis I | Peak hours 08:00-09:30, 17:30-19:00 |
| VCI (Via de Cintura Interna) | Congested most of the day |
| Ribeira / Centro Historico | Very narrow, coach access impossible |

**Inter-city transfer times (normal/peak):**
| Route | Distance | Normal | Peak/Holiday |
|---|---|---|---|
| Lisboa - Porto | 310 km | 3h00 | 3h30-4h00 |
| Lisboa - Cascais | 30 km | 30min | 45-60min |
| Lisboa - Sintra | 30 km | 35min | 50-75min |
| Lisboa - Arrabida/Setubal | 50 km | 40min | 60-90min |
| Lisboa Aeroporto - City center | 7 km | 15min | 30-45min |
| Porto Aeroporto - City center | 15 km | 20min | 35-50min |

### 5. Parking management

| Element | Standard | Notes |
|---|---|---|
| Capacity assessment | 1 space per 2.5-3 guests (car events) | Adjust for urban events with public transport |
| Accessible spots | Minimum 2% of total, near entrance | Portuguese law mandates accessible parking |
| VIP parking | Reserved, closest to entrance, signed | Cones + signage + marshal |
| Valet option | 1 valet per 15 cars/hour | Premium events, limited parking venues |
| Overflow parking | Identified + shuttle from overflow lot | Must be within 10min drive |
| Signage | Directional from 1km out, illuminated at night | Portuguese + English for international events |
| Marshals | 1 per 50 spaces during arrival peak | Hi-vis vests, radio, flashlights at night |
| EV charging | Identify charger locations nearby | Growing demand, especially corporate events |
| Cost | Free parking preferred, validated parking acceptable | Communicate parking cost upfront if paid |

### 6. Fleet coordination

**Vehicle manifest template:**
| Vehicle ID | Type | Capacity | Driver | Phone | Route | Departure | Arrival | Status |
|---|---|---|---|---|---|---|---|---|
| V-01 | Coach | 50 | Antonio S. | +351 9XX | Hotel A - Venue | 18:00 | 18:30 | Confirmed |
| V-02 | Van VIP | 7 | Maria L. | +351 9XX | Airport - Hotel B | 14:30 | 15:00 | Confirmed |

**Communication protocol:**
| Channel | Who | Purpose |
|---|---|---|
| Radio Ch. 1 | All drivers | Dispatch and status updates |
| WhatsApp group Transport | Drivers + transport manager | Non-urgent, photo updates |
| Direct phone | Transport manager to driver | Emergencies, schedule changes |
| Radio Ch. 5 | Production/staging vehicles | Load-in coordination |

**Staging areas:**
- Designated vehicle waiting area near venue
- Clear entry/exit flow (no reversing with passengers)
- Driver rest area with WC access and water
- Fuel/charging if multi-day event

### 7. Airport logistics

**Arrival manifest template:**
| Guest | Role | Flight | Arrival | Terminal | Transfer Type | Driver | Vehicle | Hotel |
|---|---|---|---|---|---|---|---|---|
| Dr. Ana Costa | Speaker | TP 1234 | 14:30 T1 | T1 | VIP car | Joao | V-03 | Hotel X |

**Airport protocol:**
- Track all flights in real-time (FlightRadar24, airline apps)
- Driver at arrivals 15min before landing (not scheduled arrival)
- Name board: clean, professional, event-branded
- Welcome kit in vehicle: water, itinerary, Wi-Fi password, local SIM if international
- Contingency for delays: driver waits up to 90min, then redeployable with 30min recall
- Lost luggage protocol: contact info for airline + hotel delivery arrangement

**Lisboa Airport (LIS) specifics:**
- Terminal 1: full-service carriers (TAP, Lufthansa, etc.)
- Terminal 2: low-cost (Ryanair, EasyJet) -- separate building, shuttle between terminals
- Pickup zone: arrivals level, lanes 1-2 for private vehicles, lane 3 for buses
- Kiss & fly: 15min free parking at departures
- Peak congestion: 06:00-08:00, 11:00-13:00 arrivals

### 8. Load-in / equipment transport

**Delivery schedule template:**
| Time | Vendor | Vehicle Type | Dimensions | Items | Loading Dock | Duration | Contact |
|---|---|---|---|---|---|---|---|
| 06:00 | Stage Co. | Truck 12m | 12x2.5x4m | Stage + truss | Dock A | 3h | Pedro +351 9XX |
| 08:00 | AV Tech | Van 3.5t | 6x2x2.5m | Sound + LED | Dock A | 2h | Ana +351 9XX |
| 09:00 | Caterer | Truck 7.5t + Van | Mixed | Kitchen + food | Dock B (cold) | 2h | Luis +351 9XX |
| 10:00 | Decor | Van 3.5t x2 | Standard | Flowers + decor | Main entrance | 1.5h | Sara +351 9XX |

**Load-in rules:**
- No two large vehicles at same dock simultaneously
- 30min buffer between slots for turnaround
- Venue access hours strictly observed (neighbors, noise)
- Fragile items: separate vehicle, hand-unloaded, climate-controlled if needed
- Cold chain items: refrigerated transport, temperature log required

### 9. Shuttle schedule design

| Departure | Route | Vehicle | Capacity | Frequency | Last Service |
|---|---|---|---|---|---|
| Hotel Zone A | Hotel A then Hotel B then Venue | Coach (50) | 50 | Every 30min | 19:30 |
| Hotel Zone B | Hotel C then Venue (direct) | Minibus (24) | 24 | Every 20min | 19:30 |
| Venue to Hotels | Venue then Hotel A then B then C | Coach (50) | 50 | Every 30min from 22:00 | 01:00 |
| VIP | On-demand | Van (7) | 7 | On call | 02:00 |

**Shuttle best practices:**
- Branded signage on vehicles (event logo, route name)
- Printed schedule in hotel lobby and event venue
- QR code to live shuttle tracker (Google Maps sharing or WhatsApp location)
- Last shuttle time prominently communicated at event
- Accessible vehicle in rotation (minimum 1 per route)

### 10. Accessibility transport

| Requirement | Solution |
|---|---|
| Wheelchair accessible vehicle | Minimum 1 per shuttle route, ramp or lift equipped |
| Assistance point | Designated pickup/dropoff closer to entrance |
| Companion policy | Companion travels free with accessible guest |
| Communication | Pre-event contact with guests requiring assistance |
| Driver training | Basic disability awareness, assistance protocol |
| Emergency | Accessible vehicle available for medical evacuation |

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-transport
event_date: <YYYY-MM-DD>
guest_count: <number>
vehicles_required: <number>
---

# Transport & Logistics Plan -- <Event Name>

## Overview
| Parameter | Value |
|---|---|
| Event venue | <name + address> |
| Guest count | <number> |
| Transport modes | <shuttles/VIP cars/coaches/etc.> |
| Total vehicles | <number> |
| Transport budget | EUR <X,XXX> |
| Transport manager | <name + phone> |

## Route Plan
[Primary and secondary routes with maps/GPS links]

## Guest Transport Schedule
[Shuttle and transfer timetables]

## VIP / Speaker Transfers
[Individual transfer manifest]

## Airport Logistics
[Arrival manifest + driver assignments]

## Fleet Manifest
[All vehicles, drivers, assignments]

## Load-In Schedule
[Delivery timeline by vendor]

## Parking Plan
[Capacity, zones, marshals, signage]

## Accessibility Plan
[Accessible vehicles, assistance points]

## Communication Protocol
[Radio channels, WhatsApp groups, emergency contacts]

## Contingency Plan
| Scenario | Response |
|---|---|
| Vehicle breakdown | Backup vehicle on standby within 30min |
| Severe traffic | Alternative route activated, guests notified |
| Flight delay >2h | Driver redeployed, replacement on 30min recall |
| Weather (rain/storm) | Covered drop-off zone, umbrellas at pickup |
| Medical emergency | Nearest hospital route for all vehicles |

## Cost Summary
| Component | Cost EUR |
|---|---|
| Guest shuttles | X,XXX |
| VIP transfers | X,XXX |
| Airport transfers | X,XXX |
| Load-in vehicles | X,XXX |
| Parking / marshals | X,XXX |
| Contingency (10%) | X,XXX |
| **Total** | **X,XXX** |

## Next Steps
- [ ] Confirm all vehicle bookings
- [ ] Test primary and secondary routes at event time
- [ ] Distribute driver packs (routes, contacts, schedule)
- [ ] Coordinate load-in with `atlas-timeline`
- [ ] Brief all drivers using `atlas-briefing` template
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Transport Plan.md`

## Red Flags
- Never plan transport with a single route to the venue -- one accident, roadwork, or closure strands all guests; always have a tested secondary route
- Never assume traffic will be normal -- test routes at the exact same day-of-week and time-of-day as the event, especially in Lisboa where 30min can become 90min
- Never operate without backup vehicles -- minimum 1 standby vehicle for every 5 active vehicles; breakdowns are common with rental coaches
- Never send drivers without GPS and tested routes -- paper directions fail, phone signal drops; pre-load routes on offline GPS before event day
- Never skip the load-in schedule -- two 12m trucks arriving simultaneously at a single loading dock creates a 2-hour cascade delay that compresses all setup time
- Never forget the last shuttle -- always communicate the last departure time clearly at the event; guests stranded at a venue with no transport is a reputation-destroying failure
- Never ignore accessibility -- Portuguese law requires accessible transport options; failing to provide them excludes guests and violates DL 163/2006

## Interactions
- Load-in schedule integrates with `atlas-timeline` for production coordination
- Vehicle fleet sourced via `atlas-vendor` procurement process
- Driver staffing coordinated with `atlas-staff`
- Guest arrival data from `atlas-guest` and `atlas-accommodation`
- Equipment manifests from `atlas-warehouse`
- Route to venue documented in `atlas-venue`
- Airport transfers linked to `atlas-accommodation` travel coordination
- Budget allocation from `atlas-budget`
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-transport** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-transport:**

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
