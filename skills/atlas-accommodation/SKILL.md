---
name: atlas-accommodation
description: Hotel Blocks & Travel Logistics for events — room block negotiation, attrition management, hotel selection, booking management, group rates, travel coordination, welcome packages, check-in/out, visa requirements. Portuguese hotel benchmarks and international guest support. Triggers on "hotel", "alojamento", "accommodation", "room block", "quartos", "hospedagem", "reservas hotel", "travel logistics", "voo", "flight", "visa", "rooming list", "welcome package", "check-in grupo".
license: MIT
---

# ATLAS Skill — Hotel Blocks & Travel Logistics

Complete accommodation and travel management for events: hotel block negotiation, rooming list management, group rate optimization, travel coordination for speakers/VIPs, welcome packages, and international guest support. Portuguese hotel market benchmarks and practical guidance for managing multi-hotel event bookings.

## When to activate

Invoke `/atlas-accommodation` (or trigger automatically) when:
- User needs to block hotel rooms for an event
- User needs to negotiate group rates with hotels
- User must manage a rooming list for conference/event guests
- User needs to coordinate flights/travel for speakers or VIP guests
- User asks about hotel options near an event venue
- User needs welcome package or check-in coordination
- User has international guests requiring visa or travel information

Do NOT use when:
- Guest transport between hotel and venue (use `atlas-transport`)
- Venue selection and assessment (use `atlas-venue`)
- General vendor negotiation (use `atlas-vendor` — though hotel-specific negotiation is covered here)

## Workflow

### 1. Gather accommodation requirements
- **Event name and dates** — including pre/post event dates for early arrivals/late departures
- **Guest count requiring accommodation** — typically 40-70% of total guests for conferences, 80-100% for destination events
- **Guest profile breakdown** — VIPs/speakers, corporate delegates, international guests, staff/crew
- **Budget per night** — or total accommodation budget
- **Hotel requirements** — star rating, amenities, meeting rooms, proximity to venue
- **Duration** — nights required (1, 2, 3+)
- **Special needs** — accessible rooms, connecting rooms, suites, early check-in, late check-out
- **Travel coordination** — flights to book? Visa letters needed?

### 2. Hotel selection criteria

| Criterion | Weight | Evaluation |
|---|---|---|
| Proximity to venue | 25% | Walking distance (<1km), shuttle distance (<15min), drive (<30min) |
| Star rating / quality | 20% | Matches event profile and guest expectations |
| Room availability | 15% | Can accommodate full block on event dates |
| Rate competitiveness | 15% | Within budget, good value vs. BAR |
| Amenities | 10% | Breakfast, WiFi, gym, pool, parking, meeting rooms |
| Meeting/event space | 5% | Breakout rooms, speaker prep room if needed |
| Accessibility | 5% | Accessible rooms, public areas, transport links |
| Track record | 5% | Group booking experience, references from other events |

**Hotel tier matching:**
| Event Type | Minimum Star | Recommended | VIP/Speaker |
|---|---|---|---|
| Corporate conference | 4* | 4*S / 5* | 5* or boutique |
| Association/NGO | 3* | 4* | 4*S |
| Wedding (destination) | 4* | 4*S / 5* | Suite upgrade |
| Festival / youth | 2* / hostel | 3* | 4* |
| Incentive / reward | 5* | 5*L | Presidential suite |

### 3. Room block negotiation

**Key terms to negotiate:**
| Term | Standard | Target | Notes |
|---|---|---|---|
| Group rate | BAR -10% to -30% | BAR -20% to -35% | Depends on block size and season |
| Attrition clause | 80% pickup required | 70-75% pickup | Below this, pay penalty on unsold rooms |
| Cut-off date | 30 days before event | 21-28 days before | After this, rooms released for public sale |
| Comp rooms | 1 per 50 booked | 1 per 40 booked | For event staff, speakers |
| Suite upgrade | None | 1-2 comp upgrades | For keynote speakers, VIPs |
| Breakfast | Per room extra | Included in rate | Significant value add |
| WiFi | Standard free | Premium free | Corporate guests need fast WiFi |
| Parking | Paid | Discounted or comped | Especially for drive-in events |
| Early check-in | Subject to availability | Guaranteed for VIPs | Critical for morning events |
| Late check-out | 12:00 standard | 14:00-16:00 for group | Especially for last-day events |
| Meeting room | Paid | Comped if F&B minimum met | For speaker prep, event office |
| F&B minimum | Required for comps | Reasonable, achievable | Breakfast + coffee breaks can count |
| Cancellation | Non-refundable | Sliding scale 90/60/30 days | Protect against force majeure |
| Force majeure | Limited | Comprehensive (pandemic, natural disaster) | Learned from COVID era |
| Commission | 0% | 8-10% to agency | Standard for event agencies |

**Attrition management:**
- Track pickup weekly from cut-off minus 60 days
- At 50% of cut-off: review and adjust block size if needed
- At cut-off: release unused rooms or negotiate extension
- Penalty calculation: (contracted rooms - picked up rooms) x rate x penalty % (typically 50-80%)

### 4. Portuguese hotel benchmarks 2026

**Lisboa (per room per night, B&B):**
| Category | Low Season (Nov-Feb) | Mid Season (Mar-Apr, Oct) | High Season (May-Sep) |
|---|---|---|---|
| 3* | 60-90 EUR | 80-120 EUR | 100-160 EUR |
| 4* | 90-140 EUR | 120-200 EUR | 160-280 EUR |
| 4*S | 130-180 EUR | 170-260 EUR | 220-350 EUR |
| 5* | 180-300 EUR | 250-400 EUR | 350-600 EUR |
| 5*L (Palace) | 300-500 EUR | 400-700 EUR | 600-1,200 EUR |

**Porto (per room per night, B&B):**
| Category | Low Season | Mid Season | High Season |
|---|---|---|---|
| 3* | 50-80 EUR | 70-100 EUR | 90-140 EUR |
| 4* | 80-120 EUR | 100-170 EUR | 140-240 EUR |
| 5* | 150-250 EUR | 220-350 EUR | 300-500 EUR |

**Algarve (per room per night, B&B):**
| Category | Low Season (Nov-Mar) | Mid Season (Apr-May, Oct) | High Season (Jun-Sep) |
|---|---|---|---|
| 4* Resort | 70-120 EUR | 120-200 EUR | 200-350 EUR |
| 5* Resort | 150-250 EUR | 250-400 EUR | 400-800 EUR |

**Rural / Countryside (Alentejo, Douro, Sintra):**
| Category | Range |
|---|---|
| Turismo Rural / Agroturismo | 60-120 EUR |
| Boutique Hotel | 100-200 EUR |
| Wine Estate / Quinta | 120-300 EUR |

**Group rate typical discounts:**
| Block Size | Expected Discount off BAR |
|---|---|
| 10-25 rooms/night | 10-15% |
| 25-50 rooms/night | 15-25% |
| 50-100 rooms/night | 20-30% |
| 100+ rooms/night | 25-35% + added value |

### 5. Rooming list management

**Rooming list template:**
| # | Guest Name | Company | Room Type | Check-in | Check-out | Nights | Special Requests | VIP | Payment | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Dr. Ana Costa | ABC Corp | Suite | 14/05 | 16/05 | 2 | High floor, quiet | Yes | Company | Confirmed |
| 2 | Joao Silva | XYZ Lda | Standard Twin | 14/05 | 15/05 | 1 | Connecting w/ #3 | No | Self-pay | Pending |

**Room type distribution (typical conference):**
| Room Type | % of Block | Notes |
|---|---|---|
| Standard double/twin | 65-75% | Bulk of delegates |
| Superior / executive | 15-20% | Senior delegates, sponsors |
| Junior suite | 5-10% | VIP speakers, board |
| Suite | 2-5% | Keynote, C-suite, event host |
| Accessible | 2-3% | Minimum, always available |

### 6. Travel coordination

**Flight booking for speakers/VIPs:**
| Field | Detail |
|---|---|
| Passenger name | As per passport |
| Origin city | Home airport |
| Preferred airline | Alliance, direct routes |
| Class | Economy+ / Business (per policy) |
| Preferred times | Arrive day before, depart day after |
| Frequent flyer | Number and alliance |
| Visa required | Check against nationality |
| Travel insurance | Included or separate |
| Ground transfer | From `atlas-transport` |

**Itinerary package for each traveler:**
- Flight confirmation
- Hotel confirmation
- Ground transport schedule
- Event program
- Emergency contacts
- Local information (weather, dress code, currency, plugs)
- Maps (airport to hotel, hotel to venue)

### 7. Welcome packages

**Standard welcome package contents:**
| Item | Purpose | Cost Range |
|---|---|---|
| Welcome letter | Personal greeting, event overview | Printed |
| Event program | Full schedule, map, contacts | Printed |
| Local guide | Restaurants, attractions, transport | Printed or QR |
| City map | Marked with venue, hotel, key locations | Printed |
| Name badge + lanyard | If pre-distributed | 2-5 EUR/pp |
| Event merch | Branded item (notebook, pen, bag) | 5-20 EUR/pp |
| Local product | Portuguese treat (pasteis, wine miniature, olive oil) | 5-15 EUR/pp |
| WiFi instructions | Hotel + venue network details | Printed |
| SIM card / eSIM | International guests | 10-20 EUR/pp |
| Room amenity | Water, fruit, chocolate | 5-15 EUR/room |

**VIP welcome upgrade:**
- Handwritten welcome note from event host
- Premium room amenity (Port wine + chocolates / flowers)
- Printed personal itinerary
- Private meet & greet arranged
- Dedicated contact person (phone number)

### 8. Check-in/out coordination

**Group check-in options:**
| Method | Best For | Setup |
|---|---|---|
| Pre-assigned rooms | VIP, known guests | Rooming list finalized 48h before, keys pre-prepared |
| Group check-in desk | Conferences, large groups | Dedicated desk in lobby, extra staff, signage |
| Self-service kiosk | Tech-savvy, large volume | Hotel kiosks + QR codes |
| In-room check-in | Premium, luxury | Keys delivered to car/lobby, paperwork in-room |

**Check-in timeline:**
| Time | Action |
|---|---|
| 48h before | Final rooming list to hotel |
| 24h before | Room assignments confirmed, keys prepared |
| Check-in day AM | Event team does room spot-check (VIP rooms) |
| Check-in day | Welcome packages placed in rooms |
| Check-in window | Group desk staffed, signage in place |
| Evening | Verify all arrivals checked in, follow up no-shows |

**Check-out coordination:**
- Express checkout option enabled for all rooms
- Luggage storage for guests with late departures
- Late check-out confirmed for VIPs (14:00-16:00)
- Transport schedule aligned with check-out times
- Final hotel bill review within 48h of check-out

### 9. International guest support

**Visa requirements for Portugal (non-EU guests):**
- Schengen visa required for most non-EU/EEA nationals
- Processing time: 15 business days minimum (apply 8-12 weeks before)
- Event organizer provides: invitation letter, event details, accommodation proof
- AIMA (Agencia para a Integracao, Migracoes e Asilo) is the Portuguese authority
- Business visa (type C): for conferences, meetings, events up to 90 days

**Invitation letter must include:**
- Event name, dates, venue
- Guest's full name, passport number, nationality
- Purpose of attendance (speaker, delegate, exhibitor)
- Confirmation that organizer covers costs (if applicable)
- Organizer's NIF and company details
- Signed by authorized representative

**Practical information for international guests:**
| Topic | Detail |
|---|---|
| Currency | EUR, cards widely accepted, MBWay for local payments |
| Language | Portuguese; English widely spoken in hospitality |
| Time zone | WET (UTC+0), WEST (UTC+1) summer |
| Electricity | Type F plugs, 230V/50Hz |
| Emergency | 112 (general), SOS AIMA for immigration issues |
| Tipping | Not mandatory, 5-10% appreciated in restaurants |
| Water | Safe to drink from tap in all cities |
| Mobile | EU roaming included for EU residents; prepaid SIM for others |

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-accommodation
event_date: <YYYY-MM-DD>
total_rooms_blocked: <number>
hotels: <number>
---

# Accommodation & Travel Plan — <Event Name>

## Overview
| Parameter | Value |
|---|---|
| Event dates | <dates> |
| Guests requiring accommodation | <number> |
| Total room nights | <number> |
| Hotels contracted | <number> |
| Total accommodation budget | EUR <X,XXX> |
| Cut-off date | <date> |

## Hotel Summary
| Hotel | Stars | Rooms Blocked | Rate/Night | Distance to Venue | Role |
|---|---|---|---|---|---|
| [Name] | 4* | 80 | EUR 140 | 1.2 km | Primary |
| [Name] | 5* | 20 | EUR 280 | 0.5 km | VIP / Speakers |
| [Name] | 3* | 30 | EUR 85 | 2.0 km | Overflow |

## Room Block Details
[Per hotel: room types, rates, attrition, cut-off, comp rooms]

## Rooming List
[Full rooming list table]

## VIP Accommodation
[Suite assignments, upgrades, special requests]

## Travel Coordination
[Flight bookings, visa letters, itineraries]

## Welcome Packages
[Contents, delivery schedule, VIP upgrades]

## Check-in/out Plan
[Group check-in setup, luggage storage, late check-out]

## International Guest Support
[Visa letters issued, practical information distributed]

## Attrition Tracker
| Hotel | Blocked | Picked Up | % Pickup | Cut-off | Status |
|---|---|---|---|---|---|
| [Name] | 80 | 62 | 78% | 14/04 | At risk |

## Budget Summary
| Component | Cost EUR |
|---|---|
| Room block (net) | X,XXX |
| VIP upgrades | X,XXX |
| Welcome packages | X,XXX |
| Speaker flights | X,XXX |
| Visa processing | X,XXX |
| Contingency (5%) | X,XXX |
| **Total** | **X,XXX** |

## Next Steps
- [ ] Finalize rooming list (deadline: <date>)
- [ ] Distribute welcome packages (<date>)
- [ ] Confirm VIP check-in arrangements
- [ ] Issue remaining visa invitation letters
- [ ] Coordinate airport transfers with `atlas-transport`
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Accommodation Plan.md`

## Red Flags
- Never sign a hotel contract without reviewing the attrition clause — an 80% pickup commitment on 100 rooms means paying for 80 rooms even if only 50 are used; negotiate down to 70% or add a review clause at cut-off minus 30 days
- Never set the cut-off date too early — a 60-day cut-off loses rooms back to the hotel when many delegates book 3-4 weeks before; negotiate 21-28 days for domestic events, 30-45 for international
- Never block rooms at a single hotel without identifying a backup — hotel overbooking, renovations, or labor disputes can leave guests without rooms; always have a secondary hotel agreement
- Never forget to block accessible rooms — minimum 2-3% of block, available from day one of booking; retrofitting accessibility at cut-off is impossible
- Never skip visa invitation letters for international events — Schengen visa processing takes 3-6 weeks; late letters mean absent speakers and wasted flights
- Never assume the hotel will place welcome packages correctly — do a spot-check of 5-10 rooms on arrival day; packages end up in wrong rooms or go missing routinely
- Never release the final rooming list later than 48h before check-in — hotels need time to pre-assign rooms, prepare keys, and brief reception staff; same-day lists create check-in chaos

## Interactions
- Hotel sourcing and contracting via `atlas-vendor`
- Airport and hotel-venue transfers via `atlas-transport`
- Guest data and dietary info from `atlas-guest`
- Budget allocation from `atlas-budget`
- Speaker/VIP program from `atlas-briefing`
- Event timeline for check-in/out windows from `atlas-timeline`
- International protocol guidance from `atlas-protocol`
- Save via `dario-obsidian-save` to vault
