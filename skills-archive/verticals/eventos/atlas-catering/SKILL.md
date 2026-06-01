---
name: atlas-catering
description: F&B Planning & Management for events -- menu planning, dietary management, beverage programs, service styles, quantity calculations, HACCP compliance, Portuguese menus and wines, cost benchmarks, sustainability. Triggers on "catering", "menu", "comida", "bebidas", "food and beverage", "F&B", "cocktail", "jantar de gala", "buffet", "bar", "vinhos", "wine", "allergens", "alergenos", "HACCP".
license: MIT
---

# ATLAS Skill -- F&B Planning & Management

Complete food and beverage planning for events: menu design, dietary management, beverage programs, service style selection, quantity calculations, HACCP compliance, and vendor coordination. Deep Portuguese context including regional cuisine, wine regions, pastelaria, and local cost benchmarks for 2026.

## When to activate

Invoke `/atlas-catering` (or trigger automatically) when:
- User needs to plan food and/or beverage for an event
- User needs menu recommendations for a specific event type
- User must manage dietary restrictions and allergens
- User needs to calculate F&B quantities and costs
- User wants to select a service style (buffet, plated, cocktail, etc.)
- User needs HACCP compliance guidance for an event
- User asks about Portuguese wines, regional menus, or traditional F&B

Do NOT use when:
- Sourcing and contracting the caterer (use `atlas-vendor`)
- Kitchen/venue technical requirements only (use `atlas-venue`)
- General staffing for service (use `atlas-staff` -- though staffing ratios are covered here)

## Workflow

### 1. Gather F&B inputs
- **Event type** -- corporate conference, gala dinner, wedding, cocktail, festival, product launch
- **Guest count** -- confirmed + estimated, plus staff/crew meals
- **Event duration** -- affects quantity calculations significantly
- **Time of day** -- breakfast, lunch, afternoon, dinner, late night
- **Budget per person** -- or total F&B budget
- **Guest profile** -- corporate, international, families, millennials, luxury HNW
- **Venue kitchen** -- full kitchen, prep kitchen only, no kitchen (all brought in)
- **Dietary data** -- % vegetarian, vegan, gluten-free, halal, kosher, allergies
- **Service preference** -- sit-down, buffet, cocktail, stations, food trucks
- **Alcohol policy** -- open bar, limited, drink tickets, per consumption, dry event
- **Theme/concept** -- Portuguese traditional, Mediterranean, fusion, international

If dietary data is unavailable, use defaults: 10% vegetarian, 5% vegan, 5% gluten-free, 2% other allergies.

### 2. Service styles -- pros, cons, cost

| Style | Best For | Guests | Cost/pp Range (PT 2026) | Staff Ratio |
|---|---|---|---|---|
| Sit-down plated | Galas, weddings, formal corporate | 50-300 | 45-90 EUR | 1:20 |
| Silver service | Ultra-premium, protocol events | 20-150 | 90-150 EUR | 1:10 |
| Butler pass | Cocktail receptions, networking | 50-500 | 25-45 EUR | 1:25 |
| Buffet | Conferences, casual corporate | 80-500+ | 35-65 EUR | 1:30 |
| Food stations | Themed events, interactive | 80-400 | 40-75 EUR | 1:25 per station |
| Family style | Intimate dinners, team events | 20-100 | 45-70 EUR | 1:20 |
| Food trucks | Festivals, outdoor, casual | 100-2000+ | 15-30 EUR | Per truck |
| Live cooking | Premium, interactive, show-cooking | 50-300 | 50-100 EUR | 1 chef per station |
| Box/packed | Hybrid, takeaway, COVID-era | Any | 15-35 EUR | Minimal |

### 3. Menu planning by event type

**Cocktail reception (1.5-2h):**
- 8-12 canapes per person per hour
- Mix: 60% savory, 40% sweet
- 3-4 cold items, 3-4 warm items per round
- 1-2 substantial items if no dinner follows

**Sit-down dinner (corporate/gala):**
- Welcome drink + 2-3 canapes
- Starter (or soup)
- Fish course (optional, adds formality)
- Main course + sides
- Pre-dessert (sorbet intermezzo for premium)
- Dessert
- Coffee/tea + petit fours
- Portuguese addition: queijos e doces conventuais

**Wedding (Portuguese traditional):**
- Cocktail hour: 10-12 canapes/pp
- Starter: choice of 2
- Fish course: bacalhau or seafood
- Main: meat (vitela, leitao, borrego)
- Dessert: wedding cake + doces finos
- Open bar: champagne toast + wine + spirits
- Late night: soup station (canja) + sandwiches

**Conference/all-day:**
- Welcome coffee + pastries
- Mid-morning break: coffee + healthy snacks
- Lunch: buffet or boxed
- Afternoon break: coffee + sweet/savory mix
- Optional: networking cocktail at close

### 4. Quantity calculation formulas

**Food quantities:**
| Item | Quantity per Person | Notes |
|---|---|---|
| Canapes (cocktail only) | 8-12 pieces/hour | First hour heavier |
| Canapes (pre-dinner) | 4-6 pieces total | Lighter if meal follows |
| Starter | 1 portion | 120-150g plated |
| Main course | 1.2x headcount | 20% buffer for plating issues |
| Buffet mains | 2-3 options, 250-300g total/pp | Always over-prep by 10% |
| Bread | 2-3 pieces/pp | Artisanal adds perceived value |
| Cheese | 50-80g/pp | If cheese course included |
| Dessert | 1 portion + petit fours | 120-150g plated |
| Coffee | 1.5-2 cups/pp | Espresso and filter options |

**Beverage quantities:**
| Item | Calculation | Notes |
|---|---|---|
| Welcome drink | 1 glass/pp | Champagne, prosecco, or cocktail |
| Wine (dinner) | 0.5 bottle/pp | Half white, half red (adjust to menu) |
| Water | 0.5L still + 0.25L sparkling/pp | Minimum, more in summer |
| Soft drinks | 0.3L/pp | For non-drinkers, 10-15% of guests |
| Cocktail hour drinks | 2 drinks first hour | +1 drink per additional hour |
| After-dinner spirits | 0.5 drink/pp | Digestivos: Porto, Ginja, whisky |
| Coffee/tea | 1.5 cups/pp post-dinner | Espresso dominant in Portugal |

**Staff-to-guest ratios for F&B:**
| Service | Ratio | Notes |
|---|---|---|
| Plated service | 1:20 | Servers only, excludes kitchen |
| Silver service | 1:10 | Higher skill, slower pace |
| Buffet | 1:30 | Replenishment + clearing |
| Butler pass | 1:25 | Per tray circuit |
| Bar (cocktails) | 1:50 | Experienced bartenders |
| Bar (beer/wine only) | 1:75 | Simpler service |
| Live cooking station | 1 chef + 1 assistant | Per station |

### 5. Dietary management -- EU 14 allergens

**Mandatory allergen tracking (EU Regulation 1169/2011):**
1. Cereals containing gluten
2. Crustaceans
3. Eggs
4. Fish
5. Peanuts
6. Soybeans
7. Milk (including lactose)
8. Nuts (almonds, hazelnuts, walnuts, cashews, pecans, Brazil nuts, pistachios, macadamias)
9. Celery
10. Mustard
11. Sesame seeds
12. Sulphur dioxide and sulphites (>10mg/kg)
13. Lupin
14. Molluscs

**Dietary management protocol:**
- Collect dietary requirements during registration (mandatory field)
- Deadline: 1 week before event (2 weeks for 200+ guests)
- Assign unique identifiers to special meals
- Plated: dietary meals served with discreet marker (colored napkin ring, small flag)
- Buffet: label every item with allergen icons and dietary suitability (V, VG, GF)
- Kitchen: separate preparation area, dedicated utensils, allergen-free zones
- Staff: brief all servers on allergen identification and emergency protocol

### 6. Beverage programs -- cost models

| Model | How It Works | Best For | Cost Control |
|---|---|---|---|
| Open bar | All drinks included, unlimited | Galas, weddings, premium | Low (highest cost) |
| Limited bar | Selected spirits/wines only | Corporate, budget-conscious | Medium |
| Drink tickets | X tickets per guest (e.g., 4) | Conferences, casual | High |
| Per consumption | Tab tracked, pay actual | Private dinners, VIP | Variable |
| Wine pairing | Pre-selected wine per course | Formal dinners | Medium (fixed cost) |
| Cash bar | Guests pay for drinks | Festivals, large events | Full (minimal cost) |
| Dry event | No alcohol | Cultural, religious | N/A |

**Portuguese wine regions for event menus:**
| Region | Character | Best For | Price Range/bottle (event wholesale) |
|---|---|---|---|
| Douro | Bold reds, complex whites | Galas, red meat menus | 8-25 EUR |
| Alentejo | Fruit-forward reds, easy drinking | Buffets, casual events | 6-18 EUR |
| Dao | Elegant reds, mineral whites | Formal dinners | 8-20 EUR |
| Vinho Verde | Light, crisp, refreshing | Welcome drinks, seafood, summer | 4-12 EUR |
| Lisboa | Versatile, value | Large events, volume | 4-10 EUR |
| Setubal | Moscatel dessert wine | Dessert course, after-dinner | 8-15 EUR |
| Bairrada | Espumante (sparkling) | Toasts, reception | 6-15 EUR |

### 7. Portuguese F&B specifics

**Traditional menu elements:**
- Entradas: queijo da Serra, presunto, azeitonas, pao alentejano
- Sopa: caldo verde, acorda, sopa de peixe
- Peixe: bacalhau (200+ recipes), polvo, robalo, dourada, ameijoas
- Carne: leitao da Bairrada, vitela, borrego, cabrito, secretos de porco preto
- Regional stations: francesinha station (Porto), bifanas, prego
- Doces: pasteis de nata, doces conventuais (ovos moles, toucinho do ceu), bolo de bolacha
- Queijos: Serra da Estrela, Azeitao, Sao Jorge, Nisa, Serpa

**Cost benchmarks PT 2026 (per person, excluding IVA):**
| Type | Budget | Mid-Range | Premium |
|---|---|---|---|
| Cocktail (2h) | 25-35 EUR | 35-55 EUR | 55-80 EUR |
| Buffet lunch | 25-35 EUR | 35-50 EUR | 50-70 EUR |
| Sit-down dinner | 45-60 EUR | 60-90 EUR | 90-150 EUR |
| Wedding (full) | 80-110 EUR | 110-150 EUR | 150-250 EUR |
| Coffee break | 8-12 EUR | 12-18 EUR | 18-25 EUR |
| Open bar (3h) | 20-30 EUR | 30-45 EUR | 45-70 EUR |

### 8. HACCP compliance for events

| Requirement | Standard | Verification |
|---|---|---|
| Temperature control (cold) | Below 5C at all times | Probe thermometer check on arrival |
| Temperature control (hot) | Above 65C during service | Check before and during service |
| Transport temperature | Cold chain documented | Caterer provides transport log |
| Allergen labeling | All 14 EU allergens marked | Verify labels on every item |
| Food handler certificates | All staff handling food | Caterer provides copies |
| Kitchen inspection | Clean, separated zones | Site visit 2-4 weeks before |
| Preparation timing | Made within safe windows | Caterer provides prep schedule |
| Waste management | Separated, removed promptly | Bins provided, collection arranged |
| Traceability | Ingredient origins documented | Available on request |

### 9. Sustainability practices

- **Local sourcing:** prioritize suppliers within 100km, seasonal produce
- **Seasonal menus:** reduce cost and environmental impact
- **Food waste management:** accurate quantity planning, donation partnerships (Refood, Zero Desperdicio)
- **Service materials:** avoid single-use plastics, real crockery preferred, compostable if disposable needed
- **Leftover protocol:** staff meals first, donation second, composting third
- **Carbon offset:** calculate F&B carbon footprint, offset options

### 10. Timeline for F&B planning

| When | Action |
|---|---|
| 12-16 weeks before | Select caterer via `atlas-vendor`, sign contract |
| 8-12 weeks before | Menu tasting (mandatory for 200+ or premium events) |
| 6-8 weeks before | Beverage program finalized, wine selection |
| 4 weeks before | Dietary requirement collection opens (via registration) |
| 2 weeks before | Final menu confirmed, print menu cards |
| 1 week before | Final guest count and dietary confirmations to caterer |
| 3 days before | Final adjustments (+/- 5% typically allowed) |
| Day before | Kitchen/venue setup, equipment delivery check |
| Event day | Morning walkthrough, temp checks, allergen briefing |
| Post-event | Waste report, feedback, invoice reconciliation |

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-catering
event_date: <YYYY-MM-DD>
guest_count: <number>
service_style: <plated|buffet|cocktail|stations|mixed>
budget_pp: <EUR>
---

# F&B Plan -- <Event Name>

## Overview
| Parameter | Value |
|---|---|
| Event type | <type> |
| Guest count | <confirmed + buffer> |
| Service style | <style> |
| Meal periods | <breakfast/lunch/dinner/cocktail> |
| Budget per person | EUR <X> |
| Total F&B budget | EUR <X,XXX> |
| Caterer | <name> (contracted via atlas-vendor) |

## Menu
[Full menu with allergen markers per item]

## Dietary Matrix
| Restriction | Count | Menu Solution |
|---|---|---|
| Vegetarian | X | [specific dishes] |
| Vegan | X | [specific dishes] |
| Gluten-free | X | [specific dishes] |
| Halal | X | [specific dishes] |
| Allergies | X | [individual handling] |

## Beverage Program
| Service | Details | Cost Model |
|---|---|---|
| Welcome drink | [specification] | Included |
| Dinner wines | [selection] | Wine pairing |
| Bar | [scope] | Open / Limited / Tickets |
| Non-alcoholic | [options] | Included |

## Quantity Calculations
| Item | Per Person | Total | Buffer |
|---|---|---|---|
| [item] | X | Y | +Z% |

## HACCP Checklist
- [ ] Caterer HACCP certification verified
- [ ] Temperature monitoring protocol confirmed
- [ ] Allergen labeling for all items
- [ ] Food handler certificates on file
- [ ] Transport cold chain documented
- [ ] Kitchen site visit completed
- [ ] Waste management plan confirmed

## Service Staff
| Role | Count | Ratio | Source |
|---|---|---|---|
| Head waiter | 1 | - | Caterer |
| Servers | X | 1:20 | Caterer |
| Bartenders | X | 1:50 | Caterer |
| Kitchen staff | X | - | Caterer |

## Cost Summary
| Component | Per Person | Total |
|---|---|---|
| Food | EUR X | EUR X,XXX |
| Beverage | EUR X | EUR X,XXX |
| Service staff | EUR X | EUR X,XXX |
| Equipment rental | EUR X | EUR X,XXX |
| **Subtotal** | **EUR X** | **EUR X,XXX** |
| IVA (23%) | EUR X | EUR X,XXX |
| **Total** | **EUR X** | **EUR X,XXX** |

## Next Steps
- [ ] Confirm menu tasting date
- [ ] Collect dietary requirements via registration (`atlas-guest`)
- [ ] Finalize wine selection with sommelier
- [ ] Confirm service staff count with `atlas-staff`
- [ ] Coordinate kitchen load-in with `atlas-timeline`
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - F&B Plan.md`

## Red Flags
- Never skip allergen tracking -- a single unmanaged allergen can cause anaphylaxis, hospitalization, and legal liability under EU Regulation 1169/2011
- Never host a 200+ person event without a prior menu tasting -- what reads well on paper may fail in execution, temperature, presentation, or taste at scale
- Never allow last-minute menu changes (under 1 week) -- the caterer cannot guarantee ingredient sourcing, staff training, or allergen safety with insufficient lead time
- Never accept a staff-to-guest ratio below 1:25 for plated service -- under-staffed service creates cold food, long waits, and a perception of poor quality regardless of food quality
- Never assume dietary data from a previous event -- always collect fresh dietary requirements for every event; guests change, attendees differ, and allergies develop
- Never skip HACCP temperature checks on arrival -- if hot food arrives below 65C or cold food above 5C, it must be refused; serving it is a health violation
- Never present an F&B budget without IVA clearly separated -- 23% IVA on a 50,000 EUR catering bill is 11,500 EUR that surprises clients who budgeted net amounts

## Interactions
- Caterer sourcing and contracting via `atlas-vendor`
- Dietary data collected through `atlas-guest` registration
- Service staff coordination with `atlas-staff`
- Kitchen/service timeline integrated into `atlas-timeline`
- Budget allocation from `atlas-budget`
- Venue kitchen specifications from `atlas-venue`
- Sustainability alignment with `atlas-sustainability`
- Equipment (tables, linens, crockery) tracked via `atlas-warehouse`
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-catering** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-catering:**

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
