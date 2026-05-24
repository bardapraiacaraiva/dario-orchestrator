---
name: atlas-staging
description: Stage Design, Scenic & Set Build for events. Covers stage types, set design process, materials (truss, decks, draping, scenic flats), branding integration, scenic elements, load-bearing calculations, build schedule, technical drawings, strike plans. Portuguese specifics (historic venue restrictions, DGPC/IGESPAR, SCIE fire safety, stage licensing). Triggers on "palco", "cenografia", "set design", "stage", "scenic", "truss", "montagem", "desmontagem", "rigging", "backdrop", "set build", "cenario", "ground support", "fly system".
license: MIT
---

# ATLAS Skill — Stage Design, Scenic & Set Build

Definitive reference for designing, building, and striking stages, scenic elements, and set builds for events. Covers the full lifecycle from concept through technical drawings, load calculations, build schedule, and venue-compliant installation — with deep Portuguese regulatory knowledge for historic and modern venues.

## When to activate

Invoke `/atlas-staging` (or trigger automatically) when:
- User needs to design or specify a stage for any event
- User asks about set design, scenic elements, or backdrop construction
- User needs truss, rigging, or ground support specifications
- User asks about load-bearing, weight limits, or structural sign-off
- User needs a build schedule (load-in to strike)
- User asks about branding integration into stage/scenic design
- User mentions "cenografia", "montagem de palco", "estrutura", "truss"
- After `atlas-venue` confirms the space and before `atlas-av` designs the technical rig

Do NOT use when:
- User needs only AV/sound/lighting equipment (use `atlas-av`)
- User needs only decoration and theming (use `atlas-decor`)
- User needs only entertainment programming (use `atlas-entertainment`)
- Planning is at briefing stage without venue confirmation (use `atlas-briefing` first)

## Workflow

### 1. Gather staging requirements
From event briefing and venue data, determine:
- **Event type:** conference, gala, concert, festival, awards, fashion, corporate
- **Venue confirmed:** indoor/outdoor, dimensions, ceiling height, floor type, load limits
- **Content on stage:** speakers, performers, screens, scenic elements, presenter desk
- **Audience layout:** seated theatre, banquet, standing, mixed
- **Brand requirements:** logo placement, colours, themed entrance, photo walls
- **Budget tier:** basic (decks + drape) / mid (custom scenic) / premium (full set build)
- **Timeline:** load-in window, event duration, strike deadline

If no briefing exists, ask: event type, venue dimensions, what happens on stage, and budget range.

### 2. Stage type selection

| Type | Best for | Audience relation |
|---|---|---|
| Proscenium (end-on) | Conferences, galas, concerts | Audience faces one direction |
| Thrust | Fashion, awards, immersive | Audience on 3 sides, closer feel |
| In-the-round | Ceremonies, intimate concerts | Audience all around, maximum intimacy |
| Runway/catwalk | Fashion, product launch | Linear, movement-focused |
| Multi-level | Large galas, festivals | Visual depth, multiple performance areas |
| Rotating | TV, large shows | Dynamic reveals, scene changes |
| Hydraulic/lift | Premium productions | Dramatic entrances, multi-level transitions |

### 3. Set design process

#### Full design pipeline
1. **Concept brief** — gather theme, brand, objectives, references, mood board
2. **Sketch/storyboard** — hand or digital rough layout, key sightlines
3. **3D render** — SketchUp, Vectorworks, or Cinema4D — client approval required
4. **Technical drawing** — CAD ground plan with dimensions, section view with height clearances, rigging plot
5. **Material specification** — truss type, deck size, draping, scenic flats, finishes
6. **Build** — workshop prefabrication (scenic elements) + on-site assembly
7. **Install** — structure first, then scenic, then lighting focus, then AV
8. **Dress rehearsal** — full walk-through with all elements in place
9. **Strike** — reverse build order, packaging, load-out, venue restoration

#### Technical drawings required
- **Ground plan:** top-down, 1:50 or 1:100 scale, all dimensions, sightlines marked
- **Section view:** side elevation showing height clearances (min 3m head height for performers, more for screens)
- **Rigging plot:** all hanging points, weights, safety factors (minimum 10:1 for overhead rigging)
- **Electrical layout:** power drops, cable routes, dimmer positions
- **Format:** DWG/DXF for CAD, PDF for client approval

### 4. Materials and systems

#### Truss systems
| Type | Use | Load capacity (typical) |
|---|---|---|
| Box truss (aluminium) | Overhead lighting/PA hangs | 500-2,000 kg per span (depends on length) |
| Ground support | Free-standing tower + truss grid | Height limited by base weight/outrigger spread |
| Triangular truss | Lighter applications, decor | 200-500 kg per span |
| Circle/curved truss | Design feature, stage front | As per manufacturer spec |

- **Always reference manufacturer load tables** — never estimate truss capacity
- **Wind loading (outdoor):** reduces capacity significantly — structural engineer mandatory
- **Ground support height limit:** typically 8-12m without additional engineering

#### Staging decks
- Standard sizes: 2x1m (EU) or 8x4ft / 4x4ft (US standard)
- Height-adjustable legs: 40cm to 200cm in standard increments
- Load capacity: minimum 500 kg/m2 (check per manufacturer — Prolyte, Layher, Stagedex)
- Carpet/finish: black Molton default, branded carpet, vinyl print, wood-look laminate
- Accessories: stairs (1m wide min), ramp (1:12 gradient for accessibility), fascia, skirting

#### Draping
| Type | Use | Typical cost PT |
|---|---|---|
| Pipe and drape | Room division, backdrop | 15-30 EUR/linear metre |
| Swag/Austrian | Formal events, galas | 30-60 EUR/linear metre |
| Star cloth/LED cloth | Concert, awards backdrop | 50-100 EUR/m2 |
| Cyclorama (cyc) | Theatre, projection surface | 40-80 EUR/linear metre |
| Black Molton | Masking, wings, legs | 10-20 EUR/linear metre |

- All fabrics must be fire retardant (M1/B1 classification or DIN 4102-B1)
- Keep certificates on site — fire marshal will inspect

#### Scenic elements
- **Scenic flats:** lightweight timber or aluminium frame, faced with MDF/plywood, painted or wrapped
- **Hard scenery:** 3D constructed elements, columns, arches, custom builds
- **Soft scenery:** printed backdrops (dye-sub on polyester), banners, scrims
- **Modular systems:** reusable panel systems, branded fascia, quick-connect structures

### 5. Branding integration

- **Backdrop:** printed or LED — ensure logo is visible from last row (minimum 1m tall logo for 30m room)
- **Stage fascia:** branded panel across stage front, consistent with event brand
- **Lectern/podium:** branded wrap or custom build with integrated lighting
- **LED screens as scenic:** content-driven backgrounds, dynamic branding, sponsor rotation
- **Themed entrance:** archway, tunnel, branded corridor — first impression moment
- **Photo wall:** step-and-repeat or custom scenic — 3m wide minimum, well-lit (see `atlas-photo-video`)
- **Directional signage:** consistent with scenic design, not an afterthought

### 6. Scenic effects and special elements

| Element | Permits required (PT) | Notes |
|---|---|---|
| Florals/greenery walls | None | Coordinate with `atlas-decor` |
| Water features | Venue approval, floor protection | Pump noise, electrical safety |
| Fire effects (real) | IGAC + fire marshal + SCIE | Trained pyrotechnician required, insurance rider |
| Pyrotechnics (indoor) | IGAC + PSP + fire marshal | Licensed pyrotechnician mandatory |
| Projection mapping | None | Coordinate with `atlas-av` |
| Confetti/streamers | Venue approval | Cleanup plan required |
| Haze/fog | Fire alarm isolation | Notify fire panel operator, venue approval |
| CO2 jets/cryo | Venue approval, ventilation | Safety distance from audience |

### 7. Load-bearing and structural safety

#### Key calculations
- **Stage deck loading:** total weight on stage / area (kg/m2) — must not exceed deck rating
- **Point loads:** heavy items (piano, drum riser, LED wall) — check with deck manufacturer
- **Rigging loads:** equipment weight x safety factor (10:1 minimum for overhead, 8:1 for ground support)
- **Wind load (outdoor):** affects all structures — structural engineer calculation mandatory
- **Audience barriers:** minimum 1.1m high, withstand 3kN/m horizontal force

#### When structural engineer sign-off is mandatory
- Any overhead rigging (truss, flown PA, lighting)
- Outdoor structures exposed to wind
- Stages >1.5m high
- Multi-level or cantilevered structures
- Any structure in a heritage/listed building
- Audience capacity >500

### 8. Build schedule template

| Phase | Duration (typical 200-pax conference) | Notes |
|---|---|---|
| Load-in (trucks to venue) | 1-2h | Coordinate with venue loading dock |
| Structure (stage, truss) | 3-6h | Structural first, scenic second |
| Scenic (draping, flats, branding) | 2-4h | After structure is signed off |
| Lighting focus | 2-3h | After scenic is complete (coordinates with `atlas-av`) |
| Sound check | 1-2h | After lighting (coordinates with `atlas-av`) |
| Dress rehearsal | 1-2h | Full run-through |
| **Total load-in to ready** | **10-19h** | **Typically 1.5-2 days** |
| Strike | 4-8h | Reverse build order |
| Venue restoration | 1-2h | Return venue to original state |

For larger events (gala, festival), multiply by 2-3x.

### 9. Strike plan
- **Reverse build order:** scenic down first, then lighting, then truss, then stage
- **Packaging:** all elements labelled and packed in order of next use
- **Load-out:** coordinate truck sequence with venue loading dock schedule
- **Venue restoration:** remove all tape/marks, reset furniture, clean, photo-document return condition
- **Damage assessment:** compare with pre-event venue condition report

## Portuguese regulatory context

### Historic venue restrictions (DGPC/IGESPAR)
- **No drilling** into walls, ceilings, or floors of classified buildings (monumentos nacionais, imoveis de interesse publico)
- **No adhesives** on historic surfaces — free-standing structures only
- **Weight limits on marble/stone floors:** typically 200-400 kg/m2 — distribute with plywood base plates
- **Height restrictions:** no structures touching or approaching historic ceilings
- **Access routes:** must not block emergency exits or historic circulation paths
- **Pre-event condition survey** mandatory — photographic record, agreed with venue

### Fire safety (SCIE — Seguranca Contra Incendios em Edificios)
- All fabrics: fire retardant certification (M1 or equivalent), certificates on site
- Emergency exit routes: never blocked by scenic elements, minimum 1.2m clear width
- Fire extinguishers accessible at all times (never hidden behind draping)
- Haze/fog machines: coordinate with fire alarm system, venue engineer must isolate zones
- Pyrotechnics: licensed professional, fire marshal present, IGAC notification

### Stage licensing for public events
- Public events with temporary structures require Camara Municipal approval
- Outdoor stages: alvara de utilizacao for temporary structures
- Structural engineer certificate (termo de responsabilidade) for any stage >1m height in public venue
- Insurance: public liability minimum 250,000 EUR (higher for large events)

## Cost benchmarks (Portugal, 2025-2026)

| Staging package | Cost (EUR) | Includes |
|---|---|---|
| Basic stage (6x4m, 60cm) | 800-1,500 | Decks, legs, stairs, black skirting |
| Conference stage + scenic | 2,500-6,000 | Stage, backdrop, lectern, branding, basic draping |
| Gala scenic package | 6,000-15,000 | Custom scenic, entrance, photo wall, stage, draping |
| Concert/festival stage | 15,000-40,000 | Large stage, ground support, truss grid, wings, backstage |
| Full custom set build | 25,000-100,000+ | Workshop-built scenic, multi-level, special effects |

Crew rates: stage hand 120-200 EUR/day, scenic carpenter 180-300 EUR/day, structural rigger 250-400 EUR/day.

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: staging-scenic-spec
---

# Stage & Scenic Specification — <Event Name>

## Stage design
- Type: <proscenium/thrust/in-the-round>
- Dimensions: ... x ... m, height ... cm
- Decks: ... (type, quantity)
- Access: stairs / ramp / wings
- Load capacity: ... kg/m2

## Scenic elements
- Backdrop: ...
- Draping: ...
- Branding: ...
- Special elements: ...

## Structural requirements
- Truss: ... (type, span, load)
- Ground support: ... (height, footprint)
- Rigging points: ...
- Structural engineer required: yes/no

## Technical drawings
- [ ] Ground plan (1:50)
- [ ] Section view
- [ ] Rigging plot
- [ ] Electrical layout

## Build schedule
| Phase | Duration | Start | End |
|---|---|---|---|
| Load-in | ... | ... | ... |
| Structure | ... | ... | ... |
| Scenic | ... | ... | ... |
| Strike | ... | ... | ... |

## Materials list
| Item | Qty | Supplier | Cost (EUR) |
|---|---|---|---|
| ... | ... | ... | ... |

## Safety and compliance
- [ ] Fire retardant certificates for all fabrics
- [ ] Structural engineer sign-off (if required)
- [ ] Venue condition survey (before/after)
- [ ] Emergency exits clear
- [ ] Insurance confirmed

## Budget
| Line item | Cost (EUR) |
|---|---|
| Stage/decks | ... |
| Truss/rigging | ... |
| Scenic build | ... |
| Draping | ... |
| Branding/print | ... |
| Crew | ... |
| Transport | ... |
| **Total** | **...** |
```

## Red flags

- **No structural engineer sign-off for overhead rigging:** anything flown over people requires engineering certification — no exceptions, ever
- **No fire retardant certification on fabrics:** fire marshal will shut down the event on the spot; keep certificates physically on site
- **Load-in time insufficient:** a common cause of event failure; if the venue gives you 6h and the build needs 12h, push back before signing the contract
- **No strike plan:** failing to plan the strike leads to overtime charges, venue damage, and missed load-out windows
- **Historic venue not surveyed:** drilling into a classified monument incurs criminal liability under Portuguese heritage law
- **No pre-event venue condition report:** without it, you pay for any pre-existing damage the venue claims
- **Point loads on venue floor not checked:** a grand piano on a 15th-century marble floor can crack it — always distribute weight
- **Scenic elements blocking emergency exits:** fire marshal will require immediate removal, disrupting the event
- **No wind assessment for outdoor structures:** a truss grid in wind can become a sail — structural engineer calculation is mandatory

## Integration with other atlas-* skills

- **atlas-venue** — provides venue dimensions, ceiling height, floor type, load limits, rigging points, heritage restrictions
- **atlas-av** — lighting positions, speaker hangs, and screen placement depend on stage/truss design; coordinate simultaneously
- **atlas-decor** — scenic design and decoration must be visually coherent; agree on scenic vs. decor ownership early
- **atlas-timeline** — build schedule (load-in to strike) must be in the master timeline; typically the longest single block
- **atlas-budget** — staging/scenic is typically 10-20% of total event budget; provide itemized breakdown
- **atlas-risk** — structural failure, fire, wind (outdoor) are key risks; contingency plans required
- **atlas-compliance** — SCIE fire safety, DGPC heritage, stage licensing requirements overlap
- **atlas-entertainment** — performer requirements (drum riser, runway, reveal mechanisms) inform stage design
- **atlas-photo-video** — photo wall and branded backdrops are scenic elements that serve photography needs


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-staging** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-staging:**

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
