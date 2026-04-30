---
name: atlas-av
description: Audio/Visual & Technical Production planning for events. Covers PA sizing, speaker placement, lighting design, video/projection, streaming, power calculations, stage design, technical riders, comms systems. Portuguese regulations (IGAC, noise limits), venue power constraints, cost benchmarks PT. Triggers on "AV", "audio visual", "som", "iluminacao", "luzes", "projecao", "streaming", "palco", "sound", "lighting", "video", "projection", "technical production", "rider tecnico", "LED wall", "microfones".
license: MIT
---

# ATLAS Skill — Audio/Visual & Technical Production

Definitive reference for planning, specifying, and managing all AV and technical production elements for events — from intimate corporate presentations to large-scale festivals. Produces technical specifications, equipment lists, power calculations, and crew requirements aligned with Portuguese regulations and venue constraints.

## When to activate

Invoke `/atlas-av` (or trigger automatically) when:
- User needs to plan AV for any event type
- User asks about sound, lighting, video, projection, or streaming
- User needs to read or create a technical rider
- User asks about power requirements or generator sizing
- User needs stage dimensions or design specifications
- User asks about live streaming or recording setup
- User mentions "rider tecnico", "producao tecnica", "equipamento AV"
- After `atlas-venue` confirms the venue and before `atlas-timeline` locks the schedule

Do NOT use when:
- User needs only decoration/ambiance lighting (use `atlas-decor`)
- User needs stage scenic/set design only (use `atlas-staging`)
- User needs entertainment booking (use `atlas-entertainment`)
- Event is purely online/virtual with no physical AV (use `atlas-hybrid`)

## Workflow

### 1. Gather AV requirements
From event briefing and venue data, determine:
- **Event type:** conference, gala, concert, corporate, festival, wedding
- **Venue:** indoor/outdoor, dimensions, ceiling height, power available, acoustic properties
- **Audience size:** seated/standing, expected capacity
- **Content type:** speeches, panels, live music, DJ, video playback, presentations
- **Streaming:** yes/no, platform, expected viewers, recording requirements
- **Budget tier:** basic / mid-range / premium / broadcast-grade
- **Special requirements:** simultaneous interpretation, hearing loop, accessibility

If no briefing exists, ask: event type, venue, audience size, and content type.

### 2. Sound system design

#### PA sizing (watts per person rule)
| Event type | Watts/person | Example: 300 pax |
|---|---|---|
| Speech/conference | 3-5W | 900-1,500W |
| Background music | 5-8W | 1,500-2,400W |
| DJ/dance | 8-12W | 2,400-3,600W |
| Live band (indoor) | 10-15W | 3,000-4,500W |
| Live band (outdoor) | 15-25W | 4,500-7,500W |
| Festival/concert | 25-50W | 7,500-15,000W |

#### Speaker placement
- **Conference:** L/R main PA + front fills + delays (every 15-20m)
- **Gala/dinner:** distributed system (speakers every 8-10m), no hot spots
- **Concert:** main PA arrays (L/R), subs (ground stacked or flown), front fills, delays
- **Outdoor:** add 6dB for lack of room gain, consider wind direction

#### Wireless microphone management
- **Frequency coordination:** scan venue, avoid TV broadcast frequencies, coordinate all wireless (mics + IEMs + comms)
- **Portugal UHF bands:** 470-694 MHz (post digital dividend), license via ANACOM for events >50 units
- **Rule of thumb:** max 12-16 wireless channels in clean environment, fewer in urban venues
- **Backup:** 1 wired mic per 4 wireless as fallback
- **Battery protocol:** fresh batteries for every session, labelled spares

#### Sound check protocol
1. System power-up and line check (1h before doors minimum)
2. Walk the room — check coverage, dead spots, feedback points
3. Ring out monitors (if stage monitors, not IEMs)
4. Sound check performers in reverse order of appearance
5. Run full cue-to-cue with MC/host
6. Final walk — confirm levels at FOH, last row, VIP area

### 3. Lighting design

#### Core lighting positions
- **Front wash:** even face lighting, colour temperature 3200K (warm) or 5600K (daylight)
- **Back light:** separation from background, colour for mood
- **Key light:** follow spot or focused profile for keynote/VIP
- **Specials:** gobos (logo projection), pin spots, effect lights
- **Ambient/architectural:** uplighting walls, table pin spots, entrance feature

#### Fixture categories
| Category | Use | Example fixtures |
|---|---|---|
| Wash | Even coverage | LED par, fresnel, cyc light |
| Spot/Profile | Focused beam, gobos | ETC Source Four, moving head spot |
| Moving head | Dynamic effects | Robe, Clay Paky, Martin |
| LED strip/bar | Accent, architectural | Astera Titan, PixelBar |
| Follow spot | VIP tracking | Robert Juliat, Lycian |
| Blinder/strobe | Effect, audience | Atomic, Sunstrip |

#### Lighting levels by event type
- **Conference/presentation:** 300-500 lux on stage, 100-200 lux in audience
- **Gala dinner:** 50-100 lux ambient, 200 lux on stage, pin spots on tables
- **Concert:** 0 lux house, full show lighting on stage
- **Wedding ceremony:** soft, warm, 150-200 lux

### 4. Video and projection

#### Screen sizing — the 1:6 rule
Screen width = maximum viewing distance / 6
- 30m deep room: 5m wide screen minimum
- Dual screens: each 4m wide for rooms >20m
- LED wall: pixel pitch determines min viewing distance (min distance in metres equals pixel pitch in mm)

#### Projection brightness
| Environment | Lumens per m2 of screen |
|---|---|
| Dark room | 500-800 lm/m2 |
| Dimmed room | 1,000-1,500 lm/m2 |
| Ambient light | 2,000-3,000 lm/m2 |
| Daylight/outdoor | 5,000+ lm/m2 (use LED wall instead) |

- **Rear projection:** needs 2-3m depth behind screen, better contrast, blocks rear access
- **Front projection:** more affordable, watch for shadows and speaker walk path
- **LED wall:** best for daylight, pixel pitch 2.6-3.9mm (indoor), 4.8-6mm (outdoor)
- **Confidence monitors:** 1-2 screens at stage front facing speaker (slides + timer)
- **IMAG:** required for audiences >300 or rooms deeper than 25m

### 5. Presentation technology
- **Format compatibility:** accept PPT, PPTX, PDF, Keynote — test all on show laptop 24h before
- **Backup laptop:** identical spec, all presentations loaded and tested
- **Clickers:** Logitech Spotlight or R500, spare batteries, test range in venue
- **Timers:** visible countdown for speakers via confidence monitor or dedicated display
- **Teleprompter:** for formal keynotes — presidential glass style or monitor-based

### 6. Streaming and recording

#### Multi-camera setup
| Event type | Cameras | Notes |
|---|---|---|
| Single speaker | 2 | Wide + close-up |
| Panel/roundtable | 3 | Wide + 2 singles |
| Conference (multi-room) | 2-3 per room | + roaming |
| Gala/show | 4-6 | + jib/crane |
| Concert | 5-8 | + steadicam + drone |

#### Bandwidth requirements
- 720p stream: 2.5-4 Mbps upload
- 1080p stream: 5-8 Mbps upload
- 4K stream: 15-25 Mbps upload
- Rule: dedicated wired line, 2x required bandwidth minimum, never rely on venue Wi-Fi
- Backup: 4G/5G bonding unit as failover

#### Recording protocol
- ISO recording of every camera (not just program feed)
- Redundant recording (2 recorders minimum for critical events)
- Audio: board feed + room mic + backup recorder at FOH

### 7. Power requirements

#### Amperage calculation
Total amps = total watts / 230V (Portugal) — add 20% safety margin always.

#### Portuguese power specifics
- **Mains:** 230V / 50Hz, Schuko (Type F) plugs
- **3-phase:** 400V between phases, common in larger venues
- **Historic venues:** often limited to 32A or 63A single phase — confirm in writing
- **Generator:** diesel, silenced (<75dB at 7m), positioned downwind, separate earth rod
- **Clean power:** UPS for LED walls, computers, streaming; isolating transformers for audio
- **PAT testing:** all portable equipment tested and labelled (insurance requirement)
- **Cable management:** covered cable ramps on public walkways, gaffer tape on stage only

### 8. Stage design specifications

| Event type | Minimum stage | Ideal stage | Height |
|---|---|---|---|
| Keynote/speech | 6x3m | 8x4m | 60-80cm |
| Panel (4-5 people) | 8x3m | 10x4m | 40-60cm |
| Live band | 8x4m | 12x6m | 80-120cm |
| Orchestra | 12x8m | 16x10m | 40-60cm |
| Fashion/catwalk | 2x15m+ | 2x20m+ | 80-100cm |
| Awards/gala | 10x6m | 14x8m | 80-100cm |

- **Access:** stairs both sides (min 1m wide), ramp for accessibility (1:12 gradient max)
- **Wings:** minimum 2m each side for entries/exits
- **Backstage:** separate from audience, green room with mirror, water, snacks
- **Load capacity:** minimum 500 kg/m2 for staging decks — confirm with manufacturer

### 9. Technical rider management
A complete technical rider includes:
- **Stage plot:** top-down view of all performer/equipment positions
- **Input list:** every channel — instrument, mic/DI type, stand, phantom power
- **Monitor requirements:** number of mixes, IEM or wedge, specific needs per performer
- **Backline:** what artist brings vs. what production provides
- **Power requirements:** total load, number of dedicated circuits
- **Lighting requirements:** minimum rig, specials, follow spots, programmed cues
- **Hospitality:** green room, food, transport (non-AV but always in the rider)
- **Schedule:** load-in time, sound check duration, set time, curfew

### 10. Communications
- **Intercom/ClearCom:** wired for fixed positions (FOH, lighting op, stage manager, follow spot)
- **Radio:** UHF 2-way for mobile crew (production manager, floor manager, security)
- **Channels:** minimum 3 — Production, Security, Catering/Logistics
- **Cue system:** cue lights for performers, or Q-Lab software triggers for complex shows
- **Show caller:** stage manager calls all cues via intercom — single point of authority

## Portuguese regulatory context

### IGAC requirements
- Required for public shows with >1,000 capacity or any ticketed cultural event
- Application 15-30 days before event
- Fire safety plan (plano de seguranca) mandatory
- Venue must hold valid IGAC licence (recinto de espetaculos)

### Noise regulations
- Regulamento Geral do Ruido (DL 9/2007)
- Night (23h-07h): max 45 dB(A) at nearest residential facade
- Day: max 55 dB(A) at nearest residential facade
- Camara Municipal may impose stricter limits — always confirm per venue
- Sound limiter may be required — install and calibrate before event

### Historic venues
- Palacios, conventos, igrejas: severely limited power (often 32A single phase max)
- No rigging from historic ceilings — ground support truss only
- Weight limits on stone/marble floors — structural engineer sign-off required
- DGPC may restrict equipment placement and cable routes

## Cost benchmarks (Portugal, 2025-2026)

| AV package | Cost (EUR) | Includes |
|---|---|---|
| Basic presentation | 1,500-3,000 | PA, 2 mics, projector+screen, basic lighting |
| Conference (1 room) | 3,000-8,000 | Full PA, 6-8 mics, projection, stage lighting, recording |
| Gala/awards show | 8,000-25,000 | Show lighting, LED wall, multi-mic, video, IMAG |
| Concert/festival stage | 25,000-80,000+ | Line array, full rig, LED wall, multi-cam, streaming |

Crew day rates: AV tech 150-300, FOH engineer 250-500, lighting 250-500, video director 300-600 EUR/day.

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: av-technical-spec
---

# AV Technical Specification — <Event Name>

## Event overview
- Type / Venue / Capacity / Date / Key content

## Sound system
- PA spec (model, qty, placement, total watts)
- Microphone list (type, use, wireless/wired)
- Monitor system (IEM/wedge, mixes)

## Lighting
- Rig summary table (position, fixture, qty, purpose)
- Control (console, operator)

## Video and projection
- Screens (size, type), projector (lumens), confidence monitors, IMAG

## Streaming/recording
- Platform, cameras, bandwidth, backup

## Power calculation
| System | Watts | Amps @230V |
- Total + 20% margin, source (venue/generator/hybrid), UPS

## Stage
- Dimensions, height, access, backstage

## Comms
- Intercom positions, radio channels

## Crew and schedule
- Roles, quantities, load-in through strike timeline

## Budget
- Line items with costs

## Compliance
- [ ] IGAC / Noise / PAT / Fire safety / Insurance
```

## Red flags

- No sound check time in timeline — minimum 1h speeches, 2-3h live music
- Power capacity unverified — never assume, get written confirmation
- No backup equipment on critical path — single points of failure will fail
- Uncoordinated wireless frequencies across vendors — appoint one coordinator
- No tech rehearsal for complex cued shows — non-negotiable
- LED wall pixel pitch too coarse for viewing distance
- Relying on venue Wi-Fi for streaming — will fail under attendee load
- Historic venue power overload — always survey before specifying
- No cable management plan — trip hazard and insurance liability

## Integration with other atlas-* skills

- **atlas-venue** — power specs, dimensions, rigging points feed AV design
- **atlas-staging** — stage dimensions and scenic elements affect AV placement
- **atlas-timeline** — sound check and load-in times must be in master schedule
- **atlas-entertainment** — performer riders feed input lists and monitor specs
- **atlas-budget** — AV is 15-30% of event budget; provide itemized breakdown
- **atlas-risk** — power/equipment failure contingencies
- **atlas-compliance** — IGAC, noise, PAT testing, fire safety overlap
- **atlas-photo-video** — shared video infrastructure (cameras, IMAG, streaming)
- **atlas-decor** — ambient lighting design overlap; agree ownership early
