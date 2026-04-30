---
name: atlas-warehouse
description: Storage, Inventory & Asset Management for events — equipment inventory, storage management, asset tracking (barcode/QR), pick-pack-ship, post-event return, consumables, cross-event sharing, kit standardization, rent vs buy analysis. Portuguese warehouse zones and costs. Triggers on "armazem", "warehouse", "inventario", "inventory", "equipamento", "stock", "asset tracking", "pick list", "kit evento", "material evento", "rent vs buy", "alugar comprar", "storage", "armazenamento".
license: MIT
---

# ATLAS Skill — Storage, Inventory & Asset Management

Complete event equipment and asset management: inventory tracking, warehouse operations, pre-event picking and packing, post-event returns, consumables management, cross-event scheduling, and rent-vs-buy analysis. Designed for event companies managing their own equipment pool alongside vendor-rented items. Portuguese warehouse market context included.

## When to activate

Invoke `/atlas-warehouse` (or trigger automatically) when:
- User needs to track event equipment inventory
- User needs to prepare a pick list for an event
- User needs to manage post-event returns and condition checks
- User asks about consumables stock levels (candles, batteries, tape, etc.)
- User needs to coordinate equipment across multiple events
- User asks about rent vs. buy decisions for event equipment
- User needs to set up or optimize warehouse/storage operations
- User needs standard event kits defined and maintained

Do NOT use when:
- Vendor equipment that stays with the vendor (managed via `atlas-vendor`)
- Load-in transport logistics (use `atlas-transport`)
- Venue-owned equipment and facilities (use `atlas-venue`)
- Budget decisions without inventory context (use `atlas-budget`)

## Workflow

### 1. Gather inventory requirements
- **Event portfolio** — how many events per month/year
- **Event types** — what categories of equipment are needed
- **Existing inventory** — what is already owned
- **Storage available** — warehouse, office storage, third-party
- **Budget for equipment** — capital expenditure allocation
- **Team** — who manages the warehouse
- **Vehicle access** — loading dock, van/truck for transport

### 2. Equipment inventory structure

**Asset register template:**
| Field | Description | Example |
|---|---|---|
| Asset ID | Unique barcode/QR code | AST-TBL-001 |
| Category | Equipment type | Tables |
| Sub-category | Specific type | Round 180cm |
| Description | Full description | Round banquet table, 180cm diameter, folding legs, white top |
| Brand / Model | Manufacturer | Mity-Lite RT-72 |
| Serial number | Manufacturer serial | ML-2024-78901 |
| Purchase date | When acquired | 2024-06-15 |
| Purchase price | Original cost | 185 EUR |
| Current value | Depreciated value | 130 EUR |
| Condition | Excellent/Good/Fair/Poor | Good |
| Location | Current storage | Warehouse Bay A3 |
| Status | Available/Deployed/Repair/Retired | Available |
| Last inspection | Date of condition check | 2026-03-20 |
| Next maintenance | Scheduled service | 2026-09-20 |
| Insurance | Covered under policy X | Policy #INV-2026-001 |
| Photo | Current condition photo | [link] |
| Notes | Special handling, known issues | Slight scratch on top, cosmetic only |

**Equipment categories for events:**
| Category | Typical Items | Tracking Level |
|---|---|---|
| Tables | Round, rectangular, cocktail, buffet, registration | Per unit |
| Chairs | Banquet, chiavari, folding, barstool, lounge | Per batch (10s) |
| Linens | Tablecloths, napkins, chair covers, runners | Per batch (10s) |
| AV Equipment | Projectors, screens, speakers, mics, mixers | Per unit |
| Lighting | Uplights, wash lights, spots, LED bars, festoon | Per unit |
| Staging | Stage decks, risers, steps, railings, skirting | Per unit |
| Signage | Banners, rollups, directional signs, A-frames | Per unit |
| Decor | Vases, candelabras, mirror bases, arches | Per unit |
| Registration | Badge printers, scanners, laptops, lanyards | Per unit |
| Power/Electrical | Extension cables, distribution boards, generators | Per unit |
| Safety | Fire extinguishers, first aid kits, cones, tape | Per kit |
| Cases/Transport | Flight cases, trolleys, packing blankets | Per unit |

### 3. Storage management

**Warehouse layout principles:**
| Zone | Contents | Requirements |
|---|---|---|
| Zone A — High frequency | Tables, chairs, linens | Easy access, ground level, near loading dock |
| Zone B — Medium frequency | AV, lighting, staging | Racking, organized by category |
| Zone C — Low frequency | Seasonal decor, specialty items | Upper racking, clearly labeled |
| Zone D — Consumables | Candles, batteries, tape, stationery | Shelving, FIFO rotation |
| Zone E — Returns/inspection | Incoming returns, damage assessment | Workspace, cleaning station |
| Zone F — Repair | Items awaiting repair or parts | Separate, does not mix with available stock |
| Zone G — Climate controlled | Electronics, delicate fabrics, printed materials | Temperature 18-24C, humidity 40-60% |
| Staging area | Pre-picked event loads, ready for transport | Near loading dock, per-event bays |

**Storage specifications:**
| Requirement | Standard |
|---|---|
| Security | Alarm system, access control (key card or code), CCTV |
| Insurance | Contents insurance covering full replacement value |
| Access hours | 06:00-22:00 minimum for event operations |
| Loading dock | Minimum 1 dock for van/truck, ground-level access for smaller loads |
| Lighting | Full warehouse lighting, task lighting in inspection area |
| Fire safety | Extinguishers, smoke detection, sprinklers (if required by size) |
| Pest control | Quarterly treatment, especially for linens/fabrics |
| Cleaning | Weekly sweep, monthly deep clean |

**Portuguese warehouse market 2026:**
| Location | Cost/sqm/month | Distance to Lisboa Center | Notes |
|---|---|---|---|
| Alverca / Vila Franca | 5-8 EUR | 25 km (20min) | Good highway access (A1), industrial zone |
| Montijo / Alcochete | 4-7 EUR | 20 km (25min via V. Gama) | Growing area, newer units |
| Sintra / Mem Martins | 5-8 EUR | 25 km (30min) | Western events (Sintra, Cascais, Ericeira) |
| Prior Velho / Sacavem | 7-10 EUR | 8 km (15min) | Close to city and airport, premium |
| Loures / Frielas | 6-9 EUR | 15 km (20min) | Balanced location and price |
| Porto — Maia / Matosinhos | 4-7 EUR | 10 km | Porto metro area |

**Recommended sizes:**
| Event Volume | Warehouse Size | Annual Cost (approx.) |
|---|---|---|
| 1-3 events/month | 100-200 sqm | 6,000-18,000 EUR |
| 3-8 events/month | 200-500 sqm | 12,000-45,000 EUR |
| 8+ events/month | 500-1,000 sqm | 30,000-90,000 EUR |

### 4. Asset tracking system

**Barcode/QR implementation:**
- Generate unique QR code per asset (or per batch for low-value items)
- Label placement: durable, visible, not customer-facing during events
- Scanning: smartphone app (Sortly, Asset Panda, or custom Google Sheet + QR)
- Each scan logs: asset ID, action (check-out/check-in), event, date, person, condition

**Check-out / check-in workflow:**
```
CHECK-OUT (pre-event):
1. Pull list generated from event requirements
2. Pick items from warehouse locations
3. Scan each item QR → status changes to "Deployed"
4. Record: event name, expected return date, responsible person
5. Load onto transport vehicle (loading order = reverse unload order)
6. Final count verification before vehicle departs

CHECK-IN (post-event):
1. Unload at warehouse returns zone (Zone E)
2. Scan each item QR → status changes to "Returned - Pending Inspection"
3. Condition check: compare to pre-event condition, note any damage
4. Clean/repair as needed
5. Status update: "Available" or "Repair"
6. Re-shelve to correct warehouse location
7. Damage report filed if applicable (photo + description)
```

### 5. Pre-event pick/pack process

**Pick list template:**
| Asset ID | Item | Qty | Location | Picked | Condition | Notes |
|---|---|---|---|---|---|---|
| AST-TBL-001-020 | Round table 180cm | 20 | Bay A3 | [ ] | - | Check legs fold correctly |
| AST-CHR-001-200 | Chiavari gold | 200 | Bay A1 | [ ] | - | Include 10 spares |
| AST-LIN-001-025 | White tablecloth 300cm | 25 | Bay A5 | [ ] | - | Freshly laundered |
| AST-AV-PRJ-001 | Projector Epson 5000 | 1 | Bay B2 | [ ] | - | Include spare lamp |
| AST-SGN-REG-001 | Registration banner | 1 | Bay B4 | [ ] | - | Check for event branding |
| KIT-REG-001 | Registration kit | 1 | Bay D1 | [ ] | - | Standard kit, verify contents |

**Loading order (reverse of unload):**
1. Last to unload = first to load: tables, chairs (heaviest, base of load)
2. Mid-load: AV equipment in flight cases, staging elements
3. Top/last loaded = first unloaded: signage, linens, fragile decor, consumables

**Confirmation checklist before departure:**
- [ ] All pick list items verified and counted
- [ ] Spare items included (10% extra for chairs, linens)
- [ ] Consumables kit complete (see Section 7)
- [ ] Tools kit included (screwdrivers, gaffer tape, cable ties, level)
- [ ] Load secured (straps, blankets between items)
- [ ] Vehicle dimensions confirmed for venue access
- [ ] Driver has venue address, GPS, contact, and load-in time

### 6. Post-event return process

**Return inspection checklist:**
| Check | Action |
|---|---|
| Count | Verify all items returned vs. pick list |
| Condition | Compare each item to pre-event condition |
| Damage | Photograph and document any damage |
| Cleaning | Linens to laundry, tables/chairs wiped, AV dusted |
| Consumables | Count remaining, return to Zone D stock |
| Missing items | Report immediately, trace to venue or transport |
| Vendor items | Separate vendor-owned items for return to vendor |
| Re-shelve | Return to correct warehouse location |
| Update system | All items scanned back in, status updated |

**Damage reporting:**
| Field | Detail |
|---|---|
| Asset ID | QR code / asset number |
| Event | Where damage occurred |
| Damage description | Clear text + photo |
| Cause | Known or suspected |
| Repairable | Yes (cost estimate) / No (write off) |
| Responsible party | Internal / vendor / guest / unknown |
| Action | Repair / Replace / Insurance claim |

### 7. Consumables management

**Standard consumables stock list:**
| Item | Unit | Reorder Point | Reorder Qty | Cost/Unit | Supplier |
|---|---|---|---|---|---|
| Gaffer tape (black) | Roll | 5 rolls | 20 rolls | 8 EUR | Thomann |
| Gaffer tape (white) | Roll | 3 rolls | 10 rolls | 8 EUR | Thomann |
| Cable ties (assorted) | Pack 100 | 3 packs | 10 packs | 4 EUR | AKI |
| Batteries AA | Pack 24 | 5 packs | 20 packs | 8 EUR | Amazon |
| Batteries AAA | Pack 24 | 3 packs | 10 packs | 8 EUR | Amazon |
| Candles (tea light) | Box 100 | 3 boxes | 10 boxes | 12 EUR | IKEA |
| Candles (taper) | Box 12 | 5 boxes | 20 boxes | 8 EUR | Decor supplier |
| Safety pins | Box 100 | 2 boxes | 10 boxes | 3 EUR | Retrosaria |
| Sewing kit | Kit | 2 kits | 5 kits | 5 EUR | Various |
| First aid supplies | Kit | 2 kits | 5 kits | 25 EUR | Pharmacy |
| Stain remover spray | Bottle | 3 bottles | 10 bottles | 6 EUR | Supermarket |
| Lint roller | Each | 5 | 15 | 3 EUR | Supermarket |
| Extension cables (5m) | Each | 5 | 10 | 12 EUR | AKI |
| Power strips | Each | 5 | 10 | 8 EUR | AKI |
| Marker pens (assorted) | Box | 3 boxes | 10 boxes | 6 EUR | Staples |
| Pens (black, branded) | Box 50 | 2 boxes | 10 boxes | 15 EUR | Branded supplier |
| Paper A4 | Ream | 5 reams | 20 reams | 4 EUR | Staples |
| Lanyards (blank) | Pack 100 | 2 packs | 5 packs | 35 EUR | Badge supplier |
| Badge holders | Pack 100 | 2 packs | 5 packs | 20 EUR | Badge supplier |

**FIFO rotation:** always use oldest stock first, check expiry on first aid and batteries.

### 8. Standard event kits

**Registration Kit (KIT-REG):**
- 2x badge printers (1 primary + 1 backup)
- 500x blank badges + holders + lanyards
- 2x barcode/QR scanners
- 1x laptop with registration software
- 1x printer (A4, for ad-hoc prints)
- Extension cables, power strip, cable management
- Stationery: pens, markers, scissors, tape, paper
- Signage: "Registration", directional arrows, "Help Desk"
- Alphabetical dividers for pre-printed badges

**Emergency Kit (KIT-EMG):**
- First aid kit (EN 13157 compliant)
- Emergency contact list (laminated)
- Venue floor plan with exits (laminated)
- High-vis vests (x5)
- Flashlights + batteries (x5)
- Megaphone (x1)
- Fire blanket (x1)
- Emergency blankets (x5)
- Phone charger (universal)
- Cash (200 EUR, various denominations)

**AV Basic Kit (KIT-AV):**
- HDMI cables (2m, 5m, 10m, 2 each)
- USB-C to HDMI adapters (x5, various types)
- Presentation clicker (x2)
- Extension power (x4)
- Gaffer tape (x2 rolls)
- Cable ties and velcro straps
- Spare batteries (AA, AAA)
- Timer/countdown display
- Laptop (backup presentation machine)

**Signage Kit (KIT-SGN):**
- A-frame signs (x6, insert-based)
- Directional arrow inserts (x10)
- Blank inserts for custom printing (x20)
- Easels for welcome signs (x2)
- Tape/adhesive strips (non-damaging)
- Cable/stanchion for queue management (x6 posts)

### 9. Cross-event asset sharing

**Calendar conflict management:**
- Master equipment calendar: Gantt view showing all assets deployed per event
- Minimum turnaround: 24h between events for cleaning and inspection
- Express turnaround: 4h possible for tables/chairs (clean and re-deploy), not for linens or AV
- Conflict resolution: first-booked event has priority, second event sources alternatives

**Transport between events:**
- Back-to-back events at different venues: plan dedicated vehicle
- Cleaning in transit: not possible for linens, possible for hard goods
- Driver briefing: pickup from Event A load-out, deliver to Event B load-in
- Risk: if Event A runs late, Event B setup is delayed — build buffer

### 10. Rent vs. buy analysis

**Decision framework:**
| Factor | Buy | Rent |
|---|---|---|
| Usage frequency | >8 times/year | <8 times/year |
| ROI breakeven | Typically 6-10 uses | N/A |
| Storage available | Yes, appropriate space | No storage or temporary |
| Capital available | Yes, or financing | Cash flow preferred |
| Maintenance | You handle (cost + time) | Vendor handles |
| Latest models | Replace every 3-5 years | Always current |
| Insurance | You cover | Vendor covers |
| Depreciation | Tax deductible | Expense deductible |

**ROI calculation:**
```
Buy cost: Purchase price + Storage (per year) + Maintenance + Insurance
Rent cost: Rental rate x Number of uses per year

Breakeven uses = Purchase price / (Rental rate - Incremental storage/maintenance cost per use)

Example: LED uplight
- Buy: 120 EUR + 2 EUR/month storage + 10 EUR/year maintenance = 144 EUR/year
- Rent: 25 EUR/use
- Breakeven: 120 / (25 - 3) = 5.5 uses → Buy if used 6+ times/year
```

## Output template

```markdown
---
project: <event name or general>
date: <YYYY-MM-DD>
type: atlas-warehouse
---

# Inventory & Asset Plan — <Event Name / Warehouse Setup>

## Equipment Summary
| Category | Items Owned | Items to Rent | Cost (Owned) | Cost (Rental) |
|---|---|---|---|---|
| Tables | X | X | - | EUR X,XXX |
| Chairs | X | X | - | EUR X,XXX |
| AV | X | X | - | EUR X,XXX |
| Signage | X | 0 | - | - |
| Kits | X | 0 | - | - |

## Pick List
[Full pick list for this event]

## Kit Assignments
| Kit | Contents Verified | Assigned To | Notes |
|---|---|---|---|
| KIT-REG-001 | Yes | Registration Lead | Includes 300 pre-printed badges |
| KIT-EMG-001 | Yes | Security Lead | Full, checked DD/MM |
| KIT-AV-001 | Yes | AV Lead | All adapters present |

## Rental Orders
[Items to rent, vendor, cost, delivery/return dates]

## Loading Plan
[Vehicle assignment, loading order, departure time]

## Return Schedule
[Expected return date, inspection assignment, re-shelving deadline]

## Consumables Check
| Item | Stock Level | Needed for Event | Reorder? |
|---|---|---|---|
| Gaffer tape | 12 rolls | 4 rolls | No |
| Batteries AA | 3 packs | 2 packs | Yes (below reorder point) |

## Next Steps
- [ ] Complete pick list (2 days before event)
- [ ] Verify all kit contents
- [ ] Order rental items (1 week before)
- [ ] Schedule return inspection (day after event)
- [ ] Reorder consumables below reorder point
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Warehouse Plan.md`

## Red Flags
- Never skip the pre-event inventory count — discovering missing or damaged items on-site with 200 guests arriving is an unrecoverable failure; count and inspect everything 48h before
- Never store event electronics without climate control — humidity, heat, and cold damage projectors, LED panels, and sound equipment; replacement costs dwarf climate control costs
- Never skip the post-event condition check — damage discovered weeks later cannot be attributed to a specific event, making insurance claims and vendor accountability impossible
- Never operate without insurance on stored assets — a warehouse fire, flood, or theft without contents insurance destroys the business; coverage should equal full replacement value
- Never rely on memory for inventory — every item must be in the asset register with a unique ID; "I think we have 15 round tables" becomes "we actually have 12" when the event needs 15
- Never skip the loading order plan — equipment loaded randomly means fragile items crushed, heaviest items on top, and unloading takes 3x longer with everything in the wrong order
- Never ignore consumables reorder points — running out of gaffer tape, batteries, or cable ties on event day creates small problems that cascade into large ones; automate reorder alerts

## Interactions
- Equipment transport coordinated with `atlas-transport` for load-in/load-out scheduling
- Rental equipment sourced via `atlas-vendor` procurement
- Equipment costs feed into `atlas-budget`
- AV and staging equipment specs shared with `atlas-av` and `atlas-staging`
- Registration kits support `atlas-guest` check-in operations
- Staff uniforms and branded items tracked here for `atlas-staff`
- Signage and decor items coordinated with `atlas-decor`
- Cross-event calendar aligned with `atlas-timeline`
- Save via `dario-obsidian-save` to vault
