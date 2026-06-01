---
name: atlas-staff
description: Event Staffing & Team Management — staffing ratios, role definitions, briefing templates, communication plans, uniforms, volunteer management, Portuguese labor law, agency vs direct hire, staff welfare. Triggers on "staff", "equipa", "staffing", "pessoal evento", "team management", "briefing equipa", "voluntarios", "volunteers", "seguranca evento", "security staff", "hostesses", "runners", "crew", "staff ratio", "escalas", "turnos".
license: MIT
---

# ATLAS Skill — Event Staffing & Team Management

Complete event staffing lifecycle: calculating staffing needs, defining roles, recruiting and briefing teams, managing communication on event day, and ensuring compliance with Portuguese labor law. Covers paid staff, agency workers, and volunteers with practical ratios, briefing templates, and welfare requirements.

## When to activate

Invoke `/atlas-staff` (or trigger automatically) when:
- User needs to calculate staffing requirements for an event
- User needs to define event roles and responsibilities
- User needs to create staff briefings or communication plans
- User asks about staff-to-guest ratios for any event function
- User needs to manage volunteers
- User asks about Portuguese labor law for event staff (temporary workers, hours, breaks)
- User needs to decide between agency staff and direct hire

Do NOT use when:
- Hiring permanent employees (use `pessoa-recrutamento`)
- F&B service staff numbers only (covered in `atlas-catering`, but referenced here)
- Security company procurement (use `atlas-vendor` for sourcing, this skill for ratios and management)

## Workflow

### 1. Gather staffing requirements
- **Event type** — conference, gala, wedding, festival, corporate, exhibition
- **Guest count** — confirmed and projected
- **Venue layout** — number of rooms, entrances, stages, floors
- **Event duration** — including setup and teardown
- **Service level** — standard, premium, luxury
- **Functions needed** — registration, hospitality, security, catering, AV, production, VIP
- **Shift structure** — single shift, split shift, overnight
- **Existing team** — how many permanent staff available?
- **Budget** — staff allocation from `atlas-budget`

### 2. Staffing ratios by function

| Function | Ratio (Staff:Guests) | Notes |
|---|---|---|
| **Registration / Check-in** | 1:50 | Peak arrival: 1:30, add queue management |
| **Catering — Plated service** | 1:20 | Servers only, excludes kitchen |
| **Catering — Buffet** | 1:30 | Replenishment + clearing |
| **Catering — Cocktail (butler pass)** | 1:25 | Per tray circuit |
| **Bar — Cocktails** | 1:50 | Experienced bartenders |
| **Bar — Beer/wine only** | 1:75 | Simpler service |
| **Security — Indoor** | 1:100 | Increases for high-profile events |
| **Security — Door/access** | 2-4 per entrance | Minimum 2 per access point |
| **Security — VIP close protection** | 1:1 to 1:3 | Per VIP risk assessment |
| **Coat check** | 1:75 | Winter events: 1:50 |
| **Parking / Valet** | 1:100 (marshal), 1:15/hr (valet) | Peak arrival/departure |
| **VIP liaison** | 1:10-15 VIPs | Dedicated VIP host |
| **Stage manager** | 1 per stage | Plus 1 assistant for main stage |
| **AV technician** | 1-3 per room | Depends on complexity |
| **Runner** | 1 per 100 guests | Minimum 2 for any event |
| **First aid** | 1 per 500 guests | Minimum 1 for any event, licensed |
| **Cleaning** | 1 per 150 guests | Continuous during event |
| **Photographer** | 1 per 150 guests | For event coverage, not portraits |
| **MC / Host** | 1 per stage | Professional, bilingual for international |
| **Production manager** | 1 per event | Overall coordination |

### 3. Role definitions

**Core event team:**

| Role | Responsibilities | Reports To | Skills Required |
|---|---|---|---|
| Event Director | Overall event delivery, client liaison, final decisions | Client/Agency | 5+ years events, leadership, crisis management |
| Production Manager | Technical production, vendor coordination, timeline | Event Director | Technical knowledge, multi-tasking, calm under pressure |
| Stage Manager | Stage schedule, speaker management, cues | Production Manager | Precision, communication, AV knowledge |
| Registration Lead | Check-in flow, badge printing, guest queries | Event Director | Organization, guest-facing, tech-savvy |
| Hospitality Manager | Guest experience, VIP handling, F&B coordination | Event Director | Hospitality background, languages, composure |
| Catering Manager | F&B service, kitchen liaison, dietary compliance | Event Director | F&B experience, HACCP awareness |
| Security Lead | Access control, emergency response, incident management | Event Director | Security certification (MAI), crisis training |
| AV Lead | Sound, lighting, video, streaming, presentations | Production Manager | Technical AV, troubleshooting |
| VIP Liaison | VIP arrivals, green room, speaker needs, protocol | Hospitality Manager | Discretion, languages, protocol awareness |
| Head Runner | Staff coordination, problem-solving, supply runs | Production Manager | Initiative, venue knowledge, stamina |
| MC / Host | Stage presence, program flow, audience engagement | Stage Manager | Public speaking, bilingual, event experience |

### 4. Staff briefing template

```markdown
# Event Staff Briefing — <Event Name>

## Event Overview
- **Event:** <name>
- **Client:** <organization>
- **Date:** <DD/MM/YYYY>
- **Venue:** <name + address>
- **Guests expected:** <number>
- **Event type:** <conference / gala / wedding / etc.>

## YOUR Role
- **Position:** <specific role>
- **Reporting to:** <name + radio channel>
- **Location:** <where you will be based>
- **Shift:** <start time — end time>

## Timeline (Key Moments)
| Time | What Happens | Your Action |
|---|---|---|
| HH:MM | Doors open | [specific instruction] |
| HH:MM | VIP arrival | [specific instruction] |
| HH:MM | Program starts | [specific instruction] |
| HH:MM | Dinner service | [specific instruction] |
| HH:MM | Event ends | [specific instruction] |

## Dress Code
- [Specific uniform/dress code]
- [Footwear requirements]
- [Branded elements to wear]
- [Weather-appropriate additions]

## Communication
- **Radio channel:** [channel number]
- **WhatsApp group:** [group name]
- **Emergency only:** [phone number]
- **Code words:**
  - "Code Green" = medical emergency
  - "Code Orange" = security incident
  - "Code Blue" = VIP arrival/departure
  - "Code Red" = evacuation

## Meal Breaks
- **Break time:** [scheduled time]
- **Break duration:** [minutes]
- **Break location:** [where]
- **Cover:** [who covers during break]

## Emergency Procedures
- **First aid location:** [where]
- **First aider on duty:** [name]
- **Nearest hospital:** [name + address]
- **Fire exits:** [locations]
- **Assembly point:** [where]
- **Evacuation procedure:** [brief steps]

## Escalation
| Issue | Contact | How |
|---|---|---|
| Guest complaint | Hospitality Manager | Radio Ch. X |
| Technical problem | AV Lead | Radio Ch. X |
| Security concern | Security Lead | Radio Ch. X |
| Medical emergency | First Aid + 112 | Radio Ch. X + phone |
| Any other issue | Production Manager | Radio Ch. X |

## Key Rules
- No personal phones visible during event
- No eating/drinking in guest areas
- Always smile and greet guests
- "I don't know" is never the answer — escalate instead
- Stay at your post until relieved
```

### 5. Communication plan

| Channel | Equipment | Who | Purpose |
|---|---|---|---|
| Radio Ch. 1 | Two-way radios | All team leads | General coordination |
| Radio Ch. 2 | Two-way radios | Security team | Security-specific |
| Radio Ch. 3 | Two-way radios | Production/AV | Technical cues |
| Radio Ch. 4 | Two-way radios | Catering team | F&B service |
| Radio Ch. 5 | Two-way radios | Transport/logistics | Vehicle movements |
| WhatsApp "Event Team" | Personal phones | All staff | Non-urgent updates, photos |
| WhatsApp "Event Leads" | Personal phones | Leads only | Sensitive issues |
| Direct phone | Personal phones | Emergency only | Event Director + Security Lead |

**Radio discipline:**
- Keep transmissions short (under 10 seconds)
- Identify yourself: "Registration Lead to Production, over"
- Wait for acknowledgment before speaking
- Never discuss sensitive issues on open channel
- Code words for emergencies (see briefing)
- Spare batteries and backup radios at production office

### 6. Uniform and dress code

| Role | Standard | Premium | Notes |
|---|---|---|---|
| Event team | Black trousers, polo (branded) | Black trousers, dress shirt | Comfortable shoes mandatory |
| Registration | Smart casual, branded lanyard | Business casual | Seated most of shift |
| Hospitality / VIP | Business dress, event branded | Cocktail/formal | Languages badge |
| Security | Dark suit or uniform | Dark suit + earpiece | Discreet for premium events |
| Runners | All black, trainers OK | All black, smart trainers | Comfort and mobility priority |
| Catering | White shirt, black apron | Formal service uniform | Caterer provides |
| Cleaning | Branded overalls or all black | Branded, discreet | Never visible to guests |

### 7. Volunteer management

| Phase | Action |
|---|---|
| Recruitment | Event listing, university partnerships, social media, NGO partnerships |
| Application | Form: name, availability, skills, languages, dietary, T-shirt size |
| Selection | Match skills to roles, check availability, confirm commitment |
| Training | 2-hour session 1 week before, or 1 hour on morning of event |
| Incentives | Certificate, event access, meals, T-shirt, networking, reference letter |
| Day-of | Buddy system (1 experienced per 5 volunteers), clear supervision |
| Recognition | Thank-you email, social media shout-out, LinkedIn recommendation |

**Volunteer vs. paid staff guidelines:**
- Volunteers: registration, wayfinding, welcome, bag stuffing, general assistance
- Paid staff only: security, AV operation, catering service, driving, first aid
- Never use volunteers for roles requiring certification or insurance
- Portuguese law: volunteers are covered under DL 389/99 (voluntariado social) but event volunteering may require additional accident insurance

### 8. Portuguese labor law for event staff

| Requirement | Detail | Reference |
|---|---|---|
| Maximum daily hours | 8 hours normal; 10 hours with overtime | Codigo do Trabalho Art. 203-211 |
| Overtime rate | +25% first hour, +37.5% additional, +50% rest days | CT Art. 268 |
| Mandatory meal break | 1 hour if shift >6 hours (can negotiate 30min minimum) | CT Art. 213 |
| Night work premium | +25% for hours between 22:00-07:00 | CT Art. 266 |
| Rest between shifts | Minimum 11 hours between end and start of next shift | CT Art. 214 |
| Minimum wage 2026 | 870 EUR/month (approximately 5.03 EUR/hour) | Updated annually |
| Temporary work | Must use licensed agency (IEFP registered) or fixed-term contract | CT Art. 175-192 |
| Insurance | Seguro de Acidentes de Trabalho mandatory for all staff | Lei 100/97 |
| Social Security | Employer contributes 23.75%, employee 11% | Even for temporary staff |
| Under 18 | Maximum 8h/day, no night work, parental consent required | CT Art. 66-83 |

**Typical event staff costs PT 2026:**
| Role | Hourly Rate (gross) | Agency Rate (billed) | Notes |
|---|---|---|---|
| General staff / runner | 7-10 EUR | 12-18 EUR | Agency adds 40-80% margin |
| Registration / hostess | 8-12 EUR | 15-22 EUR | Languages add premium |
| Head waiter | 10-15 EUR | 18-25 EUR | Experience premium |
| Security guard | 8-12 EUR | 15-25 EUR | Must be licensed (MAI) |
| AV technician | 15-25 EUR | 25-45 EUR | Specialized skill |
| Stage manager | 20-35 EUR | 35-55 EUR | Senior role |
| Event coordinator | 15-25 EUR | 25-40 EUR | Mid-level management |
| Production manager | 25-45 EUR | 40-70 EUR | Senior management |
| MC / Host | 300-1,500 EUR/event | Direct booking | Flat fee typical |
| Photographer | 150-400 EUR/event | Direct booking | 4-8 hour coverage |

### 9. Agency vs. direct hire

| Factor | Agency | Direct Hire |
|---|---|---|
| Cost | Higher (40-80% markup) | Lower hourly, but admin overhead |
| Reliability | Backup staff if no-show | No automatic replacement |
| Training | Generic, may not know your event | You train, full control |
| Insurance | Agency covers (verify) | You must arrange |
| Social Security | Agency handles | You handle declarations |
| Contracts | Agency manages | You draft fixed-term contracts |
| Best for | Large teams, one-off events, specialized roles | Regular events, core team, long-term |

### 10. Staff welfare

| Requirement | Standard | Notes |
|---|---|---|
| Meal breaks | 30min paid or 1h unpaid per 6h+ shift | Hot meal preferred, dietary options |
| Staff meals | Provided by caterer or separate | Different from guest meals acceptable |
| Hydration | Water stations accessible throughout | Especially summer outdoor events |
| Shade/shelter | For outdoor events | Covered rest area mandatory |
| Secure storage | Lockers or secure room for personal belongings | Valuables responsibility disclaimer |
| Restrooms | Dedicated staff WC if possible | Not sharing with guests |
| Rest area | Separate from guest areas | Seating, chargers available |
| First aid | Staff covered under same first aid plan | Brief all staff on location |
| Transport | Staff parking or late-night transport | If event ends after midnight |

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-staff
event_date: <YYYY-MM-DD>
guest_count: <number>
total_staff: <number>
---

# Staffing Plan — <Event Name>

## Overview
| Parameter | Value |
|---|---|
| Event date | <date> |
| Guest count | <number> |
| Total staff | <number> |
| Paid staff | <number> |
| Volunteers | <number> |
| Shifts | <number and times> |
| Staff budget | EUR <X,XXX> |

## Staffing Matrix
| Function | Ratio | Staff Required | Source | Cost/Person | Total Cost |
|---|---|---|---|---|---|
| Registration | 1:50 | X | Agency | EUR X | EUR X,XXX |
| Catering | 1:20 | X | Caterer | Included | - |
| Security | 1:100 | X | Security firm | EUR X | EUR X,XXX |
| Bar | 1:50 | X | Caterer | Included | - |
| Runners | 1:100 | X | Direct hire | EUR X | EUR X,XXX |
| VIP Liaison | 1:15 VIP | X | Direct hire | EUR X | EUR X,XXX |
| AV Tech | per room | X | AV vendor | Included | - |
| First Aid | 1 minimum | X | Licensed | EUR X | EUR X,XXX |
| **Total** | | **XX** | | | **EUR X,XXX** |

## Org Chart
[Event Director → Production Manager → Team Leads → Staff]

## Role Briefs
[Summary per role — detailed briefs distributed separately]

## Shift Schedule
| Shift | Time | Roles Covered | Break Schedule |
|---|---|---|---|
| Setup | 06:00-14:00 | Production, staging, AV | 10:00-10:30 |
| Event | 14:00-23:00 | All front-of-house | Rotating, 30min each |
| Teardown | 23:00-02:00 | Production, cleaning | None (short shift) |

## Communication Plan
[Radio channels, WhatsApp groups, code words]

## Uniform Specification
[Per role with supplier/distribution plan]

## Staff Welfare
[Meals, breaks, rest area, transport, storage]

## Volunteer Plan (if applicable)
[Recruitment, training, supervision, recognition]

## Cost Summary
| Category | Amount EUR |
|---|---|
| Direct hire staff | X,XXX |
| Agency staff | X,XXX |
| Volunteer costs (meals, T-shirts) | X,XXX |
| Radios rental | X,XXX |
| Uniforms/branded items | X,XXX |
| Staff meals | X,XXX |
| Overtime contingency (15%) | X,XXX |
| **Total** | **X,XXX** |

## Next Steps
- [ ] Confirm agency booking (deadline: <date>)
- [ ] Distribute briefing packs (<date>)
- [ ] Schedule rehearsal/walkthrough (<date>)
- [ ] Confirm radio equipment rental
- [ ] Prepare staff check-in and sign-off sheets
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Staffing Plan.md`

## Red Flags
- Never run an event without a pre-event briefing or rehearsal — unbriefed staff make mistakes, miss cues, and cannot handle emergencies; minimum 30min briefing on event morning, ideally a walkthrough the day before
- Never operate below minimum staffing ratios — understaffing is the number one cause of poor guest experience; it is cheaper to have 2 extra staff than to lose a client over slow service
- Never assign emergency response roles informally — first aid, evacuation lead, and security lead must be named, trained, and briefed; "everyone helps" means nobody leads
- Never skip overtime budgeting — Portuguese events routinely run 1-2 hours over schedule; unbudgeted overtime at +37.5% rate on 30 staff creates a significant unplanned cost
- Never hire security staff without MAI (Ministerio da Administracao Interna) licensing verification — unlicensed security is illegal in Portugal and invalidates insurance
- Never assume backup staff are available last-minute — for events over 200 guests, contract 10% more staff than calculated and have 2-3 on-call reserves confirmed
- Never forget staff transport for late-night events — if the event ends after midnight and public transport has stopped, the organizer has a duty of care to get staff home safely

## Interactions
- Staffing sourced via `atlas-vendor` (agencies) or direct recruitment
- Catering staff ratios aligned with `atlas-catering`
- Security plan integrated with `atlas-risk` and `atlas-compliance`
- Staff schedule part of `atlas-timeline` master production schedule
- Briefing template linked to `atlas-briefing` event-day documents
- VIP staff roles coordinated with `atlas-protocol`
- Staff uniforms/equipment tracked in `atlas-warehouse`
- Budget allocation from `atlas-budget`
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-staff** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-staff:**

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
