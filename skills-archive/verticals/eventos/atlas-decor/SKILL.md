---
name: atlas-decor
description: Decoration, Theming & Ambiance design for events. Covers theme development, centrepieces, floral design (Portuguese seasonal availability), lighting as decor, linen/textiles, signage/wayfinding, photo opportunities, props/furniture, Portuguese aesthetics (azulejos, cork, ceramics), sustainability. Triggers on "decoracao", "decoracao evento", "tema", "tematica", "centros de mesa", "flores", "ambiance", "theming", "centrepieces", "florals", "table decor", "uplighting", "photo wall", "step and repeat", "azulejos", "styling".
license: MIT
---

# ATLAS Skill — Decoration, Theming & Ambiance

Definitive reference for designing cohesive event decoration, theming, and ambiance — from initial mood board through execution. Covers every decorative element from table centrepieces to photo opportunities, with deep knowledge of Portuguese aesthetics, seasonal floral availability, and sustainable practices.

## When to activate

Invoke `/atlas-decor` (or trigger automatically) when:
- User needs to design the look and feel of an event
- User asks about themes, colour palettes, or mood boards
- User needs centrepiece design, floral specifications, or table styling
- User asks about decorative lighting (candles, fairy lights, uplighting)
- User needs signage, wayfinding, or branded decor elements
- User asks about photo opportunities (photo wall, booth, backdrop)
- User mentions "decoracao", "tema do evento", "centros de mesa", "flores"
- After `atlas-venue` and `atlas-staging` confirm the physical space

Do NOT use when:
- User needs stage/scenic construction (use `atlas-staging`)
- User needs technical/production lighting (use `atlas-av`)
- User needs catering/food presentation only (use `atlas-catering`)
- User needs photography/videography planning (use `atlas-photo-video`)

## Workflow

### 1. Gather decoration context
From event briefing, determine:
- **Event type:** wedding, gala, corporate, conference, launch, party, ceremony
- **Theme/concept:** specific theme, brand colours, era/style, cultural reference
- **Venue:** indoor/outdoor, architectural style, existing decor to work with or hide
- **Guest count:** affects centrepiece quantity, signage needs, scale
- **Budget tier:** essential / enhanced / luxury
- **Season:** affects floral availability and colour palette
- **Client references:** Pinterest boards, mood images, "love/hate" examples
- **Restrictions:** venue rules (no real candles, no confetti, no adhesives)

If no briefing exists, ask: event type, theme direction, venue, guest count, and budget range.

### 2. Theme development

#### Mood board creation
1. **Colour palette:** primary (1-2 colours), secondary (1-2), accent (1), neutral base
2. **Material palette:** textures and finishes (matte/gloss, rough/smooth, organic/industrial)
3. **Era/style reference:** modern minimalist, classic elegance, rustic, tropical, art deco, industrial, bohemian, Mediterranean
4. **Inspirational images:** 8-12 images capturing the desired atmosphere
5. **Typography direction:** for signage and stationery — serif/sans-serif, formal/casual

#### Theme coherence checklist
- Does the theme work across ALL event spaces (entrance, ceremony, reception, bar, lounge, WC)?
- Does it complement the venue architecture (not fight it)?
- Is it achievable within budget?
- Does it photograph well (both daylight and artificial light)?
- Is it culturally appropriate for the audience?

### 3. Centrepiece design

#### Dining table centrepieces
| Table type | Centrepiece height rule | Width guidance |
|---|---|---|
| Round (10-12 pax) | Below 35cm OR above 60cm (eye-line gap) | Max 1/3 of table diameter |
| Rectangular (banquet) | Same height rule | Max 1/4 of table width, repeated every 80-100cm |
| Cocktail/standing | Compact or tall dramatic | Must not obstruct drink service |

- **Below eye-line:** low arrangements, candle clusters, object collections — guests see each other
- **Above eye-line:** tall vases, candelabra, hanging installations — dramatic but must not block sightlines to stage
- **Never:** centrepieces at eye level (40-60cm) that block conversation

#### Other centrepiece locations
- **Cocktail tables:** single stem or compact arrangement, weighted base (wind if outdoor)
- **Buffet stations:** anchor arrangement at end or centre, scaled to table length (40-60cm tall)
- **Entrance feature:** large statement piece, sets the tone, first photo moment
- **Bar back:** decorative elements integrated with bottles/glassware, lit from behind

### 4. Floral design

#### Portuguese seasonal availability
| Season | Key flowers available | Notes |
|---|---|---|
| Jan-Mar | Mimosa, camellia, tulip, ranunculus, anemone | Mimosa iconic in PT (Feb-Mar) |
| Apr-Jun | Peony (May-Jun), rose, sweet pea, wisteria, iris | Peony: short season, premium price |
| Jul-Sep | Sunflower, dahlia, lavender, protea, delphinium | Lavender from Alentejo |
| Oct-Dec | Hydrangea (until Oct), chrysanthemum, amaryllis, winter berry | Chrysanthemum = Dia de Todos os Santos (avoid for weddings) |
| Year-round | Eucalyptus, olive branch, rose (greenhouse), orchid, greenery | Eucalyptus and olive: quintessentially Portuguese |

#### Arrangement styles
- **Loose/garden-style:** organic, asymmetric, movement — trending, works for rustic/boho
- **Structured/compact:** dome, sphere, formal — classic elegance, corporate
- **Cascading:** trailing over table/structure edge — dramatic, romantic
- **Minimal/ikebana:** single stems, sculptural — modern, clean
- **Garland/runner:** along table length — banquet style, abundant feel

#### Floral logistics
- **Order timeline:** 4-6 weeks for standard, 8-12 weeks for peak season (June weddings) or imported varieties
- **Setup timing:** flowers last in, first out — arrange on site 2-4h before guests arrive
- **Preservation:** water tubes for arrangements, cool storage (not cold), mist foliage
- **Allergy awareness:** lilies (strong scent, pollen stains), eucalyptus (scent), tuberose (strong scent) — flag in plan

### 5. Lighting as decor

| Element | Best for | Venue considerations |
|---|---|---|
| Real candles | Warm intimacy, gala, wedding | Many PT venues prohibit — check policy |
| LED candles | Alternative where real banned | Increasingly realistic, flickering options |
| Fairy lights/string lights | Ceiling draping, outdoor, garden | 3000K warm white preferred, waterproof outdoor |
| Uplighting (LED par cans) | Wall wash, mood colour | 12-16 units for medium room, wireless battery preferred |
| Pin spots | Centrepiece highlighting | 1 per table, mounted on truss or ceiling rig |
| Festoon lights | Outdoor, rustic, garden party | 5-10m spacing between supports, IP65 for outdoor |
| Neon signs | Modern, photo opportunity | Custom LED neon (not glass), 2-3 week lead time |
| Lanterns | Pathway, entrance, garden | Real candle or LED, weighted for wind |
| Projection | Logo, patterns on walls/floor | Coordinate with `atlas-av` |
| Chandeliers (rental) | Dramatic focal point | Structural support required, coordinate with `atlas-staging` |

#### Lighting design principles for decor
- **Warm colour temperature (2700-3000K)** for social/dining events — never cold white
- **Layer lighting:** ambient (general fill) + task (reading menus) + accent (centrepieces, features)
- **Dim the house lights:** venue fluorescents OFF — all decorative/event lighting instead
- **Light the perimeter:** dark corners make rooms feel smaller and uninviting
- **Test at actual event time:** daylight changes everything — always do a lighting check at the correct hour

### 6. Linen and textiles

#### Tablecloths
| Fabric | Use | Cost tier |
|---|---|---|
| Polyester | Budget events, outdoor (easy clean) | Low |
| Cotton/cotton blend | Mid-range, natural feel | Medium |
| Satin/duchess | Formal events, galas | Medium-high |
| Organza overlay | Layering for texture | Medium |
| Velvet | Winter, luxury, awards | High |
| Sequin/metallic | Party, awards, NYE | High |

- **Drop length:** floor-length (preferred for formal), mid-drop (casual), to-the-knee (minimum)
- **Pressing:** all linens pressed/steamed on site before setting — non-negotiable for formal events
- **Napkins:** matching or contrasting, folded (3-4 styles: classic, fan, pocket), linen preferred over paper

#### Chair covers and accessories
- Chair covers: universal stretch (budget) vs. tailored (formal)
- Sashes: organza, satin, or velvet — tied in back, bow, or knot
- Chiavari/cross-back chairs: no covers needed — decorative in themselves (premium rental)
- Cushion pads: for ceremony chairs or long events — comfort matters

### 7. Signage and wayfinding

#### Essential event signage
| Sign | Purpose | Typical size | Material |
|---|---|---|---|
| Welcome sign | Entrance, brand/theme statement | A1-A0 (60x84cm - 84x119cm) | Acrylic, wood, mirror, foam board |
| Seating chart | Guest table assignments | A0 or larger | Printed board, digital screen, mirror |
| Table numbers | Table identification | 15x20cm | Acrylic, wood, ceramic, printed card |
| Menu cards | Dining | A5 per table or individual | Card stock, printed |
| Bar menu | Drink options | A2-A1 | Chalkboard, acrylic, printed |
| Directional signs | Wayfinding (WC, bar, ceremony) | A3-A2 | Consistent with theme |
| Order of ceremony | Programme | A4 individual or A1 display | Card stock, printed |

#### Material and style options
- **Acrylic (perspex):** modern, clean, transparent or frosted — popular for weddings
- **Wood:** rustic, laser-cut or printed — olive wood for Portuguese touch
- **Mirror:** glamorous, hand-lettered calligraphy — classic formal
- **Digital screens:** corporate, dynamic content, sponsor logos — coordinate with `atlas-av`
- **Chalkboard:** casual, bistro, farm-to-table — hand-lettered or vinyl decal

### 8. Photo opportunities

| Feature | Space needed | Typical cost PT | Notes |
|---|---|---|---|
| Branded step-and-repeat | 3x2.5m backdrop + 2m depth | 300-800 EUR | Logo grid, well-lit, carpet |
| Flower wall | 2.5x2.5m minimum | 500-2,000 EUR | Real (premium) or silk |
| Neon sign backdrop | 1-2m sign + neutral backdrop | 400-1,200 EUR | Custom text, 2-3 week lead |
| 360 photo booth | 4x4m clear area | 800-2,000 EUR | Flat floor required |
| Mirror booth | 2x2m | 600-1,500 EUR | Instant prints, props |
| Selfie frame | Handheld | 50-150 EUR | Branded, simple |
| GIF/slow-mo booth | 2x3m | 700-1,800 EUR | Digital sharing |
| Themed set/vignette | Variable | 500-5,000 EUR | Custom scenic build |

- Position near entrance or between spaces (natural traffic flow)
- Lighting is critical — dedicated lights, never rely on ambient
- Brand/hashtag visible in every photo
- Props box: themed items, brand elements, fun accessories
- Digital sharing: QR code to instant gallery, social media integration

### 9. Props and furniture

#### Lounge areas
- Sofas, armchairs, coffee tables — create conversation clusters
- 1 lounge area per 50-80 guests at cocktail events
- Consistent with theme (industrial, boho, classic, modern)
- Lighting: floor lamp, table lamp, or overhead pendant — warm and intimate

#### Specialty furniture
- **Ceremony arch/structure:** timber, metal, floral — 2.5-3m wide, 2.8-3.2m high
- **Dance floor:** portable parquet or branded vinyl wrap — 0.5m2 per dancing guest
- **Bar/counter:** custom built or rental — 1.2m height, 60cm depth, bar-back shelving
- **Cake table:** dedicated, lit, backdrop — centred or visible from main room
- **Gift/guest book table:** entrance area, styled to theme

### 10. Portuguese aesthetics

| Element | Application | Notes |
|---|---|---|
| Azulejo-inspired | Table runners, signage, printed napkins, tiles as charger plates | Blue-and-white traditional, or modern colour |
| Cork | Place cards, coasters, table accents, welcome bags | Alentejo origin, sustainable, textural |
| Traditional ceramics | Swallow (andorinha), rooster (galo), bordado embroidery | Carefully — can feel touristy if overdone |
| Mediterranean botanicals | Olive branch, fig, lemon, citrus, rosemary, lavender | Quintessentially Portuguese garden feel |
| Nautical themes | Maritime rope, shells, maritime blue, fishing net | Coastal events, Algarve, Cascais, Azores |
| Fado ambiance | Dim lighting, guitarra portuguesa as decor, shawl draping | Evening events, intimate, Lisbon atmosphere |
| Sardine motifs | Festas populares, arraial | Santos Populares (June), casual outdoor events |
| Pasteis de nata display | Food as decor, branded boxes | Welcome moment, departure gift |

**Cultural sensitivity note:** Portuguese aesthetic elements work beautifully for local and international audiences who appreciate authenticity. For corporate events, use subtly. For tourism-sector events, use proudly.

### 11. Sustainability practices

- **Rent over buy:** all furniture, props, linens — reduces waste, amortizes cost
- **Potted plants over cut flowers:** reuse, replant, donate after event
- **Minimal single-use:** avoid foam board signage — use digital, acrylic (reusable), or recycled card
- **Local sourcing:** Portuguese flowers in season, local artisans for props, reduce transport
- **Donation plan:** flowers to hospitals/care homes (Cruz Vermelha), furniture back to rental
- **Compostable confetti:** if confetti is used, biodegradable only (dried flower petals)
- **LED candles and fairy lights:** rechargeable, reusable across events

## Cost benchmarks (Portugal, 2025-2026)

| Decoration package | Cost (EUR) | Includes |
|---|---|---|
| Essential (corporate) | 1,000-3,000 | Centrepieces (basic), signage, linen upgrade, uplighting |
| Enhanced (social/gala) | 3,000-8,000 | Themed centrepieces, florals, photo wall, lounge area, full linen |
| Premium (wedding/luxury gala) | 8,000-20,000 | Custom florals, full theming, scenic entrance, props, premium linen |
| Bespoke/luxury | 20,000-50,000+ | Full immersive theming, custom builds, premium florals throughout |

Individual items: floral centrepiece 30-80 EUR (simple) to 150-400 EUR (premium), uplighting package 400-1,200 EUR, lounge set 300-800 EUR, photo wall 500-2,000 EUR.

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: decoration-theming-spec
---

# Decoration & Theming Specification — <Event Name>

## Theme concept
- Theme: ...
- Colour palette: primary, secondary, accent, neutral
- Material palette: ...
- Style reference: ...
- Mood board: [link or description]

## Spaces to decorate
### Entrance/welcome
- ...

### Ceremony/main event
- ...

### Reception/dining
- Centrepieces: ... (description, height, quantity)
- Linen: tablecloths, napkins, colour
- Table numbers and menus: ...

### Bar/lounge
- ...

### Photo opportunities
- Type: ...
- Location: ...
- Branding: ...

## Floral specification
| Arrangement | Flowers | Style | Qty | Unit cost |
|---|---|---|---|---|
| Table centrepiece | ... | ... | ... | ... |
| Entrance feature | ... | ... | 1 | ... |

## Lighting (decorative)
- Uplighting: ... units, colour
- Candles: real/LED, quantity
- Fairy lights: ... metres
- Pin spots: ...

## Signage
| Sign | Content | Material | Size |
|---|---|---|---|
| Welcome | ... | ... | ... |
| Seating chart | ... | ... | ... |

## Props and furniture
- Lounge: ...
- Specialty: ...

## Setup schedule
| Task | Duration | When |
|---|---|---|
| Linen and table setup | ... | ... |
| Florals delivered and placed | ... | ... |
| Signage and props | ... | ... |
| Lighting check | ... | ... |

## Budget
| Category | Cost (EUR) |
|---|---|
| Florals | ... |
| Linen/textiles | ... |
| Lighting (decorative) | ... |
| Signage | ... |
| Props/furniture rental | ... |
| Photo opportunities | ... |
| Setup crew | ... |
| **Total** | **...** |

## Sustainability notes
- ...
```

## Red flags

- **Theme inconsistency between spaces:** entrance says "modern minimalist" but dining room says "rustic farmhouse" — guests notice the disconnect immediately
- **Centrepieces blocking sightlines:** anything at eye level (40-60cm) on a dining table blocks conversation and frustrates guests — go low or go high
- **Fire hazard decorations:** real candles near draping, dried flowers near heat sources, non-fire-retardant fabrics — fire marshal will intervene or worse
- **Allergen flowers without disclosure:** lilies, eucalyptus, tuberose — strong scent or pollen can cause reactions; flag in advance
- **No setup/strike time in master timeline:** decoration setup takes 2-6h; if the timeline does not account for this, everything runs late
- **Outdoor decor without wind plan:** lightweight centrepieces, tall candles, and signage become projectiles — weight everything, plan for gusts
- **Photo wall poorly lit:** a beautiful backdrop in shadow produces terrible photos — dedicate lights to this
- **Using chrysanthemums at celebratory events in Portugal:** culturally associated with Dia de Todos os Santos (cemetery visits) — avoid for weddings and parties
- **Signage as afterthought:** inconsistent fonts, colours, and materials across signs undermine the entire theme
- **No damage prevention plan for venue:** protect floors (carpet/plywood under heavy items), walls (no tape/nails on painted surfaces), surfaces (protective cloths under arrangements)

## Integration with other atlas-* skills

- **atlas-venue** — venue architecture, existing decor, restrictions (no candles, no adhesives, listed building rules) define decoration possibilities
- **atlas-staging** — scenic design and decoration must be visually coherent; define boundary between scenic (structural) and decor (finishing) early
- **atlas-av** — ambient/decorative lighting overlaps with production lighting; agree on fixture ownership, control, and timing
- **atlas-catering** — food presentation, table setup, buffet styling, and bar design must align with theme
- **atlas-photo-video** — photo opportunities, backdrop lighting, and Instagram-worthy moments are decoration deliverables that serve content capture
- **atlas-timeline** — decoration setup and strike must be in the master timeline; usually the last setup task before doors
- **atlas-budget** — decoration is typically 5-15% of total event budget; provide itemized breakdown
- **atlas-sustainability** — sustainable choices (potted plants, reusable signage, local sourcing) align with event sustainability goals
- **atlas-entertainment** — themed entertainment must visually match decor (a jazz trio needs different ambiance than a DJ)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-decor** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-decor:**

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
