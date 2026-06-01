---
name: atlas-sustainability
description: Green events & sustainability — ISO 20121 event sustainability management, carbon footprint measurement (GHG Protocol), waste management (zero-waste target), sustainable catering (local sourcing, plant-forward), energy efficiency, sustainable materials, green transportation, venue selection (LEED/BREEAM), supplier sustainability criteria, measurement/reporting KPIs, and certifications. Portuguese specifics including Estrategia Nacional de Educacao Ambiental, Fundo Ambiental, Sociedade Ponto Verde, ADENE, and Turismo de Portugal sustainability criteria. Triggers on "evento sustentavel", "green event", "sustainability", "sustentabilidade", "carbon footprint", "pegada carbonica", "zero waste", "evento verde", "ISO 20121", "reciclagem evento", "plastico evento".
license: MIT
---

# ATLAS Skill — Green Events & Sustainability

Designs and measures event sustainability across all dimensions: carbon footprint, waste, energy, materials, catering, transport, and supply chain. Produces sustainability action plans with measurable KPIs, post-event impact reports, and certification roadmaps. Covers ISO 20121, GHG Protocol, and Portuguese environmental regulations and programs.

## When to activate

Invoke `/atlas-sustainability` (or trigger automatically) when:
- User wants to organize a "green event" or "evento sustentavel"
- User asks about carbon footprint of an event
- User needs a waste management plan for an event
- User asks about sustainable catering options
- User wants ISO 20121 certification or green event labeling
- User asks about reducing environmental impact of events
- User needs sustainability KPIs or reporting for an event
- Client/sponsor requires sustainability credentials or ESG reporting
- After `atlas-briefing` and `atlas-venue` define event scope and location

Do NOT use when:
- User needs general environmental compliance (permits, waste licensing) — use `atlas-compliance`
- User needs venue selection without sustainability focus — use `atlas-venue`
- User needs risk assessment for environmental hazards — use `atlas-risk`

## Trigger phrases (PT/EN)

- "evento sustentavel", "green event", "evento verde"
- "pegada carbonica do evento", "carbon footprint event"
- "zero waste", "zero residuos", "reciclagem no evento"
- "catering sustentavel", "sustainable catering", "comida local"
- "ISO 20121", "certificacao sustentabilidade evento"
- "reduzir plastico no evento", "single-use plastics"
- "compensacao carbono", "carbon offset"
- "relatorio sustentabilidade evento", "sustainability report"

## Workflow

### 1. Gather sustainability inputs

From `atlas-briefing`, `atlas-venue`, `atlas-catering`, and user input:
- **Event type and scale:** attendance, duration, indoor/outdoor
- **Venue:** existing sustainability features, certifications (Green Key, LEED, BREEAM)
- **Catering plan:** from `atlas-catering` or planned food/drink service
- **Transport profile:** attendee origins (local, national, international), venue accessibility by public transport
- **Materials planned:** print, signage, badges, merchandise, giveaways
- **Supplier list:** caterers, AV, decor, transport, accommodation
- **Client/sponsor requirements:** ESG reporting needs, sustainability commitments, certifications required
- **Budget for sustainability:** dedicated green budget or integrated
- **Baseline:** previous edition data if available (waste, energy, attendance origin)

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "ISO 20121 event sustainability management system", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "carbon footprint GHG Protocol scope 1 2 3 events", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "sustainable events waste management zero waste", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "green events Portugal sustainability certification", collection: "dario", limit: 5)
```

### 3. ISO 20121 — Event Sustainability Management System

**What it is:** International standard for event sustainability management (based on ISO 14001 structure). Provides a framework for integrating sustainability into all stages of event planning and delivery.

**Key requirements:**
1. **Sustainability policy:** written commitment from leadership, communicated to all stakeholders
2. **Scope definition:** boundaries of what the ESMS covers (which event aspects)
3. **Issue identification:** material sustainability issues (environmental, social, economic)
4. **Stakeholder engagement:** identify and engage key stakeholders (attendees, suppliers, community, sponsors)
5. **Objectives and targets:** measurable sustainability goals with timelines
6. **Operational planning:** sustainability integrated into procurement, logistics, operations
7. **Performance evaluation:** monitoring, measurement, internal audit
8. **Continual improvement:** management review, corrective actions, improvement planning

**Certification process:**
- Certification body: BSI, Bureau Veritas, SGS, LRQA (all operate in Portugal)
- Timeline: 6-12 months for first certification
- Cost: 5,000-15,000 EUR (depending on event size and complexity)
- Annual surveillance audits required
- Valid for 3 years before recertification

**Is it worth it?** Best suited for large recurring events (conferences, festivals) where the brand value of certification justifies the investment. For one-off events, implement ISO 20121 principles without formal certification.

### 4. Carbon footprint measurement

**GHG Protocol Scopes for events:**

| Scope | Description | Typical % of Event Footprint | Examples |
|---|---|---|---|
| **Scope 1** | Direct emissions (organizer-owned/controlled) | 5-10% | Generator fuel, company vehicles, refrigerant leaks |
| **Scope 2** | Indirect energy (purchased electricity, heating, cooling) | 10-15% | Venue electricity, HVAC, lighting |
| **Scope 3** | All other indirect (value chain) | 70-85% | Attendee travel, hotel stays, food production, materials, freight, waste |

**Carbon calculation methodology:**

| Source | Data Needed | Emission Factor (reference) |
|---|---|---|
| **Attendee flights** | Origin, destination, class | ICAO Carbon Calculator, DEFRA factors |
| **Attendee ground transport** | Mode, distance | DEFRA: car 0.17 kgCO2/km, train 0.04, bus 0.08 |
| **Accommodation** | Hotel nights, star rating | 20-30 kgCO2/night (3-4 star), 30-50 kgCO2/night (5 star) |
| **Venue energy** | kWh electricity, fuel (gas, oil) | Portugal grid: ~0.20 kgCO2/kWh (2025, high renewable mix) |
| **Catering** | Meals served, menu type | Meat meal: 5-8 kgCO2, vegetarian: 1.5-3 kgCO2, vegan: 1-2 kgCO2 |
| **Materials** | Weight by material type | Paper: 1.5 kgCO2/kg, plastic: 3.5 kgCO2/kg, aluminum: 8 kgCO2/kg |
| **Freight / shipping** | Weight, distance, mode | Truck: 0.06 kgCO2/tonne-km, air: 0.60 kgCO2/tonne-km |
| **Waste** | Weight by type, disposal method | Landfill: 0.5 kgCO2/kg, incineration: 0.02, recycling: negative |
| **Generator fuel** | Liters of diesel/petrol | Diesel: 2.68 kgCO2/liter, petrol: 2.31 kgCO2/liter |

**Key insight:** Attendee travel (especially flights) typically represents 70%+ of total event carbon footprint. Focus here for maximum impact.

**Carbon offset options (Portugal):**
- Portuguese carbon offset projects: reforestation (eucalyptus-free, native species preferred), renewable energy, marine conservation
- International platforms: Gold Standard, Verra VCS (verified projects)
- Cost: 15-30 EUR/tonne CO2 (voluntary market, 2026)
- Offset is NOT a substitute for reduction — always reduce first, offset the remainder
- Portuguese Fundo Ambiental: government fund supporting environmental projects (can be a co-funding partner)

### 5. Waste management (zero-waste approach)

**Zero-waste hierarchy for events:**
1. **Refuse:** eliminate unnecessary items (no single-use plastics, no unnecessary print, no disposable giveaways)
2. **Reduce:** minimize materials (digital-first, smaller portions to reduce food waste, concentrated products)
3. **Reuse:** reusable cups/plates, reusable signage (undated), reusable lanyards (collect at exit)
4. **Recycle:** proper separation stations, contract with recycling operator
5. **Compost:** organic waste composting (food scraps, compostable serviceware)
6. **Dispose:** only truly non-recyclable waste goes to landfill/incineration

**Waste station design:**
| Stream | Color (PT standard) | Examples |
|---|---|---|
| Papel/Cartao | Blue (azul) | Paper, cardboard, programs, napkins (unsoiled) |
| Plastico/Metal | Yellow (amarelo) | Plastic bottles, cans, tetra pak, film |
| Vidro | Green (verde) | Glass bottles, jars |
| Organico | Brown (castanho) | Food scraps, compostable items |
| Indiferenciado | Grey/Black (cinzento) | Non-recyclable, contaminated items |

**Best practices:**
- 1 waste station per 50-75 attendees in food areas, per 100-150 in general areas
- Station signage: pictorial (not text-only), multilingual if international event
- Waste ambassadors: 1 per 3-4 stations during peak times (guide sorting)
- Pre-event: brief all vendors on waste separation requirements
- Post-event: waste audit (weigh each stream, calculate diversion rate)
- Target: >70% diversion rate (recycling + composting vs. total waste)

**Portuguese waste infrastructure:**
- Sociedade Ponto Verde (SPV): national recycling coordination
- Valorsul (Lisboa), Lipor (Porto), AMARSUL (Setubal Peninsula): regional waste operators
- Composting: Re-Food and Banco Alimentar accept food surplus (not waste); composting via municipal or private operators
- Single-use plastics: EU Directive 2019/904 (transposed to Portuguese law) — ban on plates, cutlery, straws, stirrers, food containers (EPS)

### 6. Sustainable catering

**Local sourcing target:** >50% of ingredients sourced within 100km of event venue

| Category | Sustainable Approach | Portuguese Sources |
|---|---|---|
| **Produce** | Seasonal, local, organic when possible | AGROBIO (organic farming association), local farmers markets |
| **Protein** | Plant-forward menus (>50% plant-based options), sustainable seafood | MSC-certified fish, free-range Portuguese poultry |
| **Dairy** | Reduce dairy, offer plant-based alternatives | Portuguese plant milk producers, local artisan cheese (smaller footprint than industrial) |
| **Beverages** | Tap water (no bottled), local wine, Portuguese craft beer | Portuguese wine regions, Agua de nascente (filtered tap) |
| **Coffee/Tea** | Fair Trade, organic, Portuguese-roasted | Delta (Portuguese roaster with sustainability program), Nespresso recycling |

**Food waste reduction:**
- Accurate forecasting: use registration data to predict numbers (apply 10-15% no-show factor)
- Portion control: right-sized servings, allow seconds vs. over-portioning
- Buffet management: staggered replenishment, smaller containers at end of service
- Surplus donation: partner with Re-Food Portugal or Banco Alimentar Contra a Fome (legal protection for donors under "Lei do Bom Samaritano" — Lei 62/2017)
- Compost: remaining food waste to composting facility
- Target: <100g food waste per attendee

**Serviceware:**
- Priority: real/washable serviceware (plates, cutlery, glasses) — requires washing station
- Alternative: certified compostable (EN 13432) — not just "biodegradable" (which has no time standard)
- Ban: expanded polystyrene (EPS), single-use plastic cups, plastic straws, plastic cutlery (EU law)
- Reusable cup systems: deposit-return (2 EUR deposit, collected at exit) — reduces cup waste by 90%

### 7. Energy management

**Energy reduction strategies:**
| Area | Action | Savings |
|---|---|---|
| **Lighting** | LED fixtures (not halogen/incandescent) | 60-80% energy reduction |
| **HVAC** | Optimize set points (21-23C heating, 24-26C cooling), natural ventilation when possible | 20-40% |
| **AV equipment** | Energy-efficient projectors, LED screens vs. plasma | 30-50% |
| **Generators** | Grid power preferred; if generator needed, use battery storage hybrid, modern diesel with auto-shutoff | 20-40% fuel reduction |
| **Power management** | Timer-controlled lighting, motion sensors in low-traffic areas, power down overnight | 10-20% |
| **Stage production** | LED stage lighting, intelligent rigging (light only what's needed) | 50-70% |

**Portuguese energy context:**
- Portugal's electricity grid: >60% renewable (hydro, wind, solar) — one of the greenest in Europe
- Grid power = lower carbon than diesel generator (always prefer grid connection)
- ADENE (Agencia para a Energia): Portuguese energy agency, guidelines for efficient energy use
- Solar portable panels: feasible for small outdoor events (phone charging stations, signage lighting)
- Green energy contract: verify venue has renewable energy contract (tarifa verde)

### 8. Sustainable materials

| Item | Conventional | Sustainable Alternative | Notes |
|---|---|---|---|
| **Signage/banners** | PVC vinyl | Recyclable cardboard, fabric (reusable), bamboo | No PVC — it's non-recyclable and releases toxins |
| **Name badges** | PVC + lanyard | Recycled cardboard, seed paper, digital badge (QR on phone) | Collect lanyards at exit for reuse |
| **Programs/brochures** | Full-color print | Digital program (event app, QR to PDF), FSC-certified paper if print needed | Print only essential items |
| **Merchandise/gifts** | Plastic promotional items | Seeds, plantable pencils, reusable items (water bottles, tote bags), digital gifts | No "stuff for the sake of stuff" |
| **Registration** | Paper forms | Digital registration, paperless check-in (QR code) | Eliminates paper entirely |
| **Stage decoration** | New materials, single-use | Rented/borrowed decor, natural elements (plants, wood), reusable modular structures | Partner with rental companies |
| **Lanyards** | Polyester (new) | Recycled PET, bamboo fiber, cork (Portuguese specialty!) | Collect and reuse across events |
| **Event bags** | Non-woven PP | Organic cotton, recycled PET, cork (Portuguese) | Or no bag at all — attendees bring their own |

**Portuguese material innovation:**
- **Cork (cortica):** Portugal produces 50%+ of world's cork — sustainable, renewable, uniquely Portuguese. Use for badges, coasters, bags, signage, even flooring
- **Recycled paper:** Portugal has strong paper recycling infrastructure (Navigator, Altri)
- **Local artisan products:** Portuguese ceramics, textiles, natural soaps as sustainable gifts

### 9. Green transportation

**Priority hierarchy:**
1. **Venue near public transport** (metro, bus, train) — reduces car dependence
2. **Walking/cycling** — secure bike parking, pedestrian access from transport hubs
3. **Carpooling** — facilitate via event app or BlaBlaCar partnership
4. **EV charging** — at venue parking (or nearby)
5. **Shuttle service** — electric or hybrid buses from transport hubs / hotels
6. **Carbon offset** — for flights and unavoidable car travel

**Portuguese transport context:**
- Lisboa Metro + Carris + Fertagus: excellent coverage in Lisboa metropolitan area
- Metro do Porto + STCP: good coverage in Porto
- CP (Comboios de Portugal): inter-city rail, relatively low carbon
- Gira (Lisboa) + Bupi (Porto): bike-sharing systems
- MOBI.E: national EV charging network (growing fast)
- Carbon per passenger-km: car 0.17 kg, train 0.04 kg, metro 0.05 kg, bus 0.08 kg, flight (domestic) 0.25 kg

**Attendee communication:**
- Include public transport info in all event communications
- Provide exact directions from nearest metro/bus/train station
- Offer carpooling facilitation (rideshare board on event app)
- Include carbon comparison: "Taking the metro instead of driving saves X kg CO2"
- If parking is provided, consider pricing it (free parking subsidizes driving)

### 10. Supplier sustainability criteria

**Sustainability questionnaire for suppliers (include in RFP):**

| Question | Category | Weight |
|---|---|---|
| Do you have a written sustainability/environmental policy? | Policy | 10% |
| What waste management practices do you follow? | Waste | 15% |
| Do you source locally (>50% of inputs within 100km)? | Sourcing | 15% |
| Do you minimize single-use materials? How? | Materials | 10% |
| What is your energy management approach? | Energy | 10% |
| Do you hold any environmental certifications? (ISO 14001, B Corp, Green Key, etc.) | Certification | 10% |
| Do you track and report your carbon footprint? | Measurement | 10% |
| Can you provide sustainability documentation (policies, reports)? | Transparency | 10% |
| Do you employ fair labor practices? (contracts, fair pay, working conditions) | Social | 10% |

**Scoring:** Weight each question, score 0-5, total /100. Minimum threshold: 40/100 to qualify. Preference given to higher-scoring suppliers at equal price (up to 10% premium for sustainability).

**Portuguese certifications to look for:**
- **Green Key (Chave Verde):** hotels and venues with environmental management
- **EU Ecolabel (Rotulo Ecologico UE):** products and services meeting EU environmental criteria
- **B Corp:** companies meeting social and environmental performance standards
- **ISO 14001:** environmental management system
- **EMAS:** EU Eco-Management and Audit Scheme
- **Organic (Modo de Producao Biologico):** food certified organic (DGAV certification)
- **MSC (Marine Stewardship Council):** sustainable seafood
- **FSC (Forest Stewardship Council):** responsibly sourced paper/wood

### 11. Measurement, reporting & KPIs

**Core sustainability KPIs:**

| KPI | How to Measure | Target | Benchmark |
|---|---|---|---|
| **Total carbon footprint (tCO2e)** | GHG Protocol calculation (all scopes) | Reduce 10% YoY | 50-200 kgCO2 per attendee (varies hugely) |
| **Carbon per attendee (kgCO2)** | Total footprint / attendance | Reduce 10% YoY | <100 kg (local event), <500 kg (international) |
| **Waste diversion rate** | (Recycled + composted) / total waste | >70% | Industry avg: 30-50% |
| **Waste per attendee (kg)** | Total waste / attendance | <0.5 kg | Typical: 0.5-1.5 kg |
| **Food waste per attendee (g)** | Total food waste / attendance | <100g | Typical: 200-400g |
| **Local sourcing %** | Local spend / total F&B spend | >50% | Varies by region |
| **Plant-based meal uptake %** | Plant meals served / total meals | >30% | Growing trend, 15-25% typical |
| **Single-use plastic items** | Count of single-use plastic items | Zero | EU directive compliance baseline |
| **Public transport usage %** | Attendees using public transport / total | >40% | Depends on venue location |
| **Reusable cup return rate** | Cups returned / cups issued | >85% | With deposit: 90%+, without: 40-60% |
| **Renewable energy %** | Renewable energy / total energy consumed | >80% | Portugal grid already >60% |

**Post-event sustainability report structure:**
1. Executive summary with headline KPIs
2. Carbon footprint breakdown by scope and source (with pie chart)
3. Waste report: total, by stream, diversion rate (with comparison to last edition)
4. Energy consumption and source mix
5. Catering: local sourcing %, plant-based uptake, food waste, surplus donation
6. Materials: items avoided, recycled content used, items collected for reuse
7. Transport: modal split, EV charging usage, carbon from travel
8. Supplier sustainability scores
9. Year-over-year improvement (if recurring event)
10. Next edition targets and improvement commitments

### 12. Attendee communication

**Sustainability messaging principles:**
- **Inform, don't preach:** share what you're doing and why, without moralizing
- **Make it easy:** clear signage, convenient recycling, obvious sustainable choices
- **Make it visible:** sustainability corner/wall, impact numbers displayed, behind-the-scenes content
- **Make it participatory:** "You helped us divert X tonnes from landfill", attendee pledges
- **Make it positive:** frame as innovation and quality, not sacrifice

**Communication touchpoints:**
| When | What | How |
|---|---|---|
| Registration | Sustainability commitment, what attendees can do (bring water bottle, use public transport) | Website, confirmation email |
| Pre-event | Transport options, digital program announcement, "what we're doing" blog post | Email, social media |
| On-site | Recycling signage, reusable cup instructions, sustainability corner, food sourcing info | Signage, app, verbal |
| Post-event | Impact report, "together we achieved X", thank attendees for participation | Email, social media, website |

**Green certification display:**
- Display ISO 20121 or other certifications prominently on website and at event
- Include sustainability statement in program/app
- Social media: share sustainability milestones (content performs well — audiences engage with purpose)

### 13. Portuguese sustainability ecosystem

| Entity | Role | How to Engage |
|---|---|---|
| **Turismo de Portugal** | Sustainability criteria for events and tourism | Aligns with national sustainable tourism strategy; events can apply for support |
| **ADENE** (Agencia para a Energia) | Energy efficiency guidance and certification | Technical guidance on energy management, certified energy auditors |
| **Sociedade Ponto Verde** | Packaging recycling coordination | Partner for recycling stations, can provide branded bins and guidance |
| **Fundo Ambiental** | Government environmental fund | Funding opportunities for green event initiatives |
| **APA** (Agencia Portuguesa do Ambiente) | Environmental regulation and policy | Guidance on environmental compliance, climate reporting |
| **ERSAR** | Water regulation | Water quality and conservation guidance |
| **Re-Food** | Food surplus redistribution | Partner for food surplus donation (operates in many PT cities) |
| **Banco Alimentar** | Food bank (against hunger) | Alternative food surplus donation partner |
| **AGROBIO** | Organic farming association | Connects to local organic producers for sustainable catering |
| **QUERCUS** | Environmental NGO | Partnership for tree planting, environmental awareness |
| **Zero** (Associacao Sistema Terrestre Sustentavel) | Zero-waste advocacy | Guidance on waste reduction, can validate zero-waste claims |

## Output template

```markdown
---
project: <event-name>
date: <YYYY-MM-DD>
type: atlas-sustainability-plan
event_date: <YYYY-MM-DD>
expected_attendees: <number>
iso_20121: <pursuing/not pursuing>
---

# Plano de Sustentabilidade — <Event Name>

## Resumo Executivo
| Parametro | Valor |
|---|---|
| Evento | <name> |
| Data | <date> |
| Assistencia | <N> |
| Pegada carbonica estimada | <tCO2e> |
| Meta desvio residuos | >70% |
| Meta sourcing local | >50% |

## Compromisso de Sustentabilidade
<1-2 paragraph sustainability commitment statement>

## Pegada Carbonica
### Estimativa por Fonte
| Fonte | tCO2e | % do Total |
|---|---|---|
| Deslocacoes participantes | ... | ...% |
| Alojamento | ... | ...% |
| Energia venue | ... | ...% |
| Catering | ... | ...% |
| Materiais | ... | ...% |
| Residuos | ... | ...% |
| **Total** | **...** | **100%** |

### Reducao e Compensacao
- Reducao: <medidas, tCO2e evitadas>
- Compensacao: <projeto, tCO2e compensadas, custo>

## Gestao de Residuos
- Estacoes de reciclagem: <N>
- Streams: papel, plastico/metal, vidro, organico, indiferenciado
- Embaixadores residuos: <N>
- Parceiro reciclagem: <empresa>
- Parceiro compostagem: <empresa>
- Parceiro donacao alimentos: Re-Food / Banco Alimentar

## Catering Sustentavel
- Sourcing local (>100km): >X%
- Opcoes plant-based: >X% do menu
- Sistema reutilizavel: <copos deposito / louca lavavel>
- Previsao food waste: <Xg/participante>

## Energia
- Fonte: <rede / gerador / hibrido>
- Contrato energia verde: <sim/nao>
- LED: <X% iluminacao>
- Medidas eficiencia: ...

## Materiais
| Item | Convencional | Alternativa Sustentavel |
|---|---|---|
| Badges | PVC | <alternativa> |
| Sinalética | PVC vinilico | <alternativa> |
| ... | ... | ... |

## Transporte
- Transporte publico: <info detalhada>
- Bike parking: <N> lugares
- Carregamento EV: <N> postos
- Carpooling: <plataforma>

## Fornecedores
- Criterios sustentabilidade incluidos em RFP: ✅
- Score minimo: 40/100
- Fornecedores certificados: <lista>

## KPIs e Metas
| KPI | Meta | Medicao |
|---|---|---|
| Pegada CO2/participante | <X kgCO2> | Calculo GHG Protocol |
| Desvio residuos | >70% | Pesagem por stream |
| Food waste/pax | <100g | Pesagem |
| ... | ... | ... |

## Comunicacao
- Pagina sustentabilidade no website: ✅
- Sinalética evento: <descricao>
- Relatorio pos-evento: publicar em <prazo>

## Proximos Passos
- [ ] Calcular pegada carbonica estimada
- [ ] Contratar operador de residuos com reciclagem
- [ ] Implementar sistema copos reutilizaveis
- [ ] Incluir criterios sustentabilidade nos RFPs
- [ ] Confirmar parceria Re-Food / Banco Alimentar
- [ ] Preparar sinalética reciclagem
- [ ] Configurar tracking de KPIs
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Plano Sustentabilidade ATLAS.md`

## Red Flags

- Never claim "zero waste" or "carbon neutral" without measurement and verification — greenwashing destroys credibility faster than doing nothing; every claim must be backed by auditable data
- Never ignore attendee travel emissions (typically 70%+ of total footprint) — focusing only on waste and catering misses the dominant emission source; at minimum estimate and communicate it
- Never ban single-use without providing convenient alternatives — if you remove plastic cups but provide no reusable cup system, attendees use multiple paper cups (worse outcome); convenience drives adoption
- Never skip the post-event sustainability report for recurring events — without year-over-year data, you cannot demonstrate improvement, justify investment, or maintain stakeholder trust
- Never assume compostable = biodegradable in practice — "compostable" items (PLA, bagasse) require industrial composting facilities; verify your waste operator actually composts them, or they end up in landfill
- Never set sustainability targets without a measurement baseline — you cannot reduce what you don't measure; establish baseline KPIs at the first edition, then set reduction targets
- Never treat sustainability as a marketing gimmick — attendees, sponsors, and media are increasingly sophisticated; performative sustainability (one recycling bin + a green logo) generates backlash, not goodwill

## Interactions

- Follows `atlas-briefing` (event scope, sustainability ambition level)
- Follows `atlas-venue` (venue sustainability features, certifications)
- Coordinates with `atlas-catering` (sustainable menus, food waste, local sourcing)
- Coordinates with `atlas-compliance` (waste management regulations, environmental permits)
- Coordinates with `atlas-budget` (sustainability budget allocation, cost of offsets)
- Informs `atlas-marketing` (sustainability messaging, green credentials for promotion)
- Informs `atlas-sponsor` (sustainability partnership opportunities, ESG reporting)
- Post-event feeds `atlas-post-event` (sustainability report, KPI tracking)
- Pairs with `risco-esg` for broader ESG reporting context


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-sustainability** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-sustainability:**

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
