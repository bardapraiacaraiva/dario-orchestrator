---
name: atlas-compliance
description: Permits, licenses, health & safety for Portuguese events — Camara Municipal, IGAC, PSP/GNR, ASAE, ANAC, SCIE fire safety, noise regulations, food safety/HACCP, accessibility (DL 163/2006), RGPD, temporary structures, alcohol licensing, capacity certification, and environmental compliance. Full regulatory checklist with timelines, costs, and responsible entities. Triggers on "licenca evento", "event permit", "alvara", "IGAC", "ASAE", "licenciamento", "regulamentacao", "saude e seguranca evento", "fire safety event", "plano de evacuacao", "licenca de ruido", "food safety event", "acessibilidade evento".
license: MIT
---

# ATLAS Skill — Permits, Licenses, Health & Safety

Comprehensive Portuguese event compliance guide covering every permit, license, and regulatory requirement for public and private events. From Camara Municipal occupacao de via publica through IGAC espetaculos, PSP/GNR policiamento, ASAE food safety, SCIE fire safety, noise regulations, accessibility, RGPD, and environmental requirements. Includes timelines, costs, forms, responsible entities, and penalty consequences.

## When to activate

Invoke `/atlas-compliance` (or trigger automatically) when:
- User is organizing any public event in Portugal (even small ones have requirements)
- User asks "what permits do I need" or "que licencas preciso"
- User asks about fire safety, noise regulations, food safety, or accessibility for events
- User needs to understand IGAC registration or Camara Municipal process
- User asks about temporary structures (tents, stages, marquees)
- User needs alcohol licensing or food handling requirements
- User asks about RGPD compliance for event data
- After `atlas-risk` identifies regulatory risk areas

Do NOT use when:
- User needs risk assessment methodology (use `atlas-risk`)
- User needs marketing compliance (ASAE ticket rules are covered here, but marketing strategy is `atlas-marketing`)
- User needs data protection strategy (high-level RGPD covered here, deep CRM compliance in `atlas-crm`)

## Trigger phrases (PT/EN)

- "licencas para o evento", "event permits Portugal", "que autorizacoes preciso"
- "IGAC", "espetaculos e divertimentos publicos", "Camara Municipal evento"
- "licenca de ruido", "noise permit", "regulamento geral do ruido"
- "HACCP evento", "seguranca alimentar", "food safety event"
- "seguranca contra incendios", "fire safety", "SCIE", "plano de evacuacao"
- "acessibilidade evento", "accessibility compliance", "DL 163/2006"
- "estruturas temporarias", "temporary structures", "tendas licenciamento"
- "alvara do evento", "capacity license", "lotacao maxima"

## Workflow

### 1. Gather compliance inputs

From `atlas-briefing`, `atlas-venue`, `atlas-risk`, and user input:
- **Event type:** concert, festival, conference, feira, sporting event, private corporate
- **Location type:** venue with alvara, public space, private property, temporary site
- **Municipality:** which Camara Municipal has jurisdiction
- **Expected attendance:** determines threshold requirements
- **Activities:** music/performance, food/drink service, alcohol, pyrotechnics, drones, temporary structures
- **Duration:** single day, multi-day, overnight
- **Noise profile:** amplified music, PA system, time of day
- **Food service:** catering, food trucks, market stalls, bar
- **Structures:** stages, tents, marquees, temporary fencing, barriers

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "Portuguese event permits IGAC Camara Municipal licensing", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "fire safety SCIE DL 220/2008 plano evacuacao", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "HACCP food safety ASAE event regulations Portugal", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "noise regulations Portugal DL 9/2007 ruido evento", collection: "dario", limit: 5)
```

### 3. Master permit checklist (Portuguese events)

**Tier 1 — Always required (any public event):**

| Permit/License | Entity | Timeline | Cost | Notes |
|---|---|---|---|---|
| **Comunicacao previa / licenca** | Camara Municipal | 30+ days before | 50-500 EUR (varies by CM) | Occupacao de via publica if on public land; even private venues may need CM notification |
| **Registo IGAC** | IGAC (Inspecao-Geral das Atividades Culturais) | 15+ days before (recommended 30+) | Variable (50-300 EUR) | Required for espetaculos e divertimentos publicos (DL 23/2014); exceptions for private/corporate-only events |
| **Seguro de responsabilidade civil** | Insurance company | Before event | 500-3,000 EUR/year | Mandatory for public events; minimum 1M EUR coverage recommended |
| **RGPD compliance** | Self-assessment + CNPD if needed | Before registration opens | Internal cost | Privacy policy, consent management, data processing records |
| **Livro de reclamacoes** | ASAE compliance | Available at event | 20-30 EUR (book) + online registration | Mandatory for all economic activities open to public (DL 156/2005) |

**Tier 2 — Conditional requirements:**

| Requirement | Trigger | Entity | Timeline | Cost |
|---|---|---|---|---|
| **Policiamento** | >1,000 attendees in public spaces | PSP (urban) / GNR (rural) | 30+ days before | 25-50 EUR/officer/hour |
| **Plano de seguranca** | >1,000 attendees OR high-risk activities | PSP/GNR + ANPC | 30+ days before | Internal + consultant |
| **HACCP compliance** | Any food/drink service | ASAE | Ongoing (vendor responsibility) | Vendor cost (verify) |
| **Licenca de ruido** | Amplified music, outdoor events | Camara Municipal | 15-30 days before | 50-200 EUR |
| **Estruturas temporarias** | Tents/marquees >50 sqm, stages >2m height | Camara Municipal | 30+ days before | 100-500 EUR + engineer report |
| **Licenca de bebidas alcoolicas** | Alcohol service | Camara Municipal + ASAE | 15-30 days before | 50-200 EUR |
| **Autorizacao ANAC** | Drone photography/videography | ANAC (Autoridade Nacional de Aviacao Civil) | 15+ days before | 25-100 EUR |
| **Plano de transito** | Road closures, significant traffic impact | Camara Municipal + PSP | 30-60 days before | Variable |
| **Licenca pirotecnia** | Fireworks, pyrotechnics | PSP + Camara Municipal | 30+ days before | 100-300 EUR |
| **Autorizacao ICNF** | Events near forest/protected areas | ICNF | 30+ days before | Variable |
| **Licenciamento DGS** | Events with health implications (sports, pools) | DGS (Direcao-Geral de Saude) | Variable | Variable |

### 4. Fire safety (SCIE — Seguranca Contra Incendios em Edificios)

**Legal framework:** DL 220/2008 (Regime Juridico da SCIE) + Portaria 1532/2008 (Regulamento Tecnico)

**Risk categories for events:**
| Category | Criteria | Requirements |
|---|---|---|
| **1a categoria** (low risk) | <100 occupants, ground floor | Basic fire safety measures, extintores |
| **2a categoria** | 100-500 occupants, up to 2 floors | Fire safety plan, trained staff, extintores + carreteis |
| **3a categoria** | 500-5,000 occupants | Full medidas de autoproteacao, fire warden team, simulacro |
| **4a categoria** (high risk) | >5,000 occupants or complex buildings | Comprehensive fire safety management, ANPC approval, dedicated fire team |

**Fire safety checklist for events:**
- [ ] **Extintores:** 1 per 200 sqm, visible, accessible, inspected (ABC powder or CO2)
- [ ] **Saidas de emergencia:** minimum 2, clearly marked, unobstructed, illuminated (sinalética fotoluminescente)
- [ ] **Sinalética:** emergency exit signs (green/white, EN ISO 7010), fire equipment signs, evacuation route signs
- [ ] **Plano de evacuacao:** displayed at key points, all staff trained
- [ ] **Simulacro:** dry-run evacuation (mandatory for 3a/4a categoria)
- [ ] **Iluminacao de emergencia:** autonomous lighting on evacuation routes (minimum 1 lux)
- [ ] **Detecao de incendio:** smoke detectors in enclosed spaces (SADI system for large venues)
- [ ] **Materiais:** stage curtains, decorations must be fire-retardant (certificado M1/M2)
- [ ] **Acessos bombeiros:** clear access for fire vehicles, hydrant locations identified
- [ ] **Plano de seguranca interno:** documented, staff trained, fire warden designated
- [ ] **Coordenacao bombeiros:** notify local corporacao de bombeiros for large events

**Exit width calculation:**
- Minimum 1 unidade de passagem (UP) = 0.9m
- 1 UP per 120 persons for normal risk
- 1 UP per 100 persons for high risk (alcohol events, standing audiences)
- Minimum 2 independent exits per zone
- Emergency evacuation: full venue emptied within 8 minutes (3 minutes for rooms)

### 5. Food safety (HACCP / ASAE)

**Legal framework:** Regulamento (CE) 852/2004, DL 113/2006, enforced by ASAE

**Requirements for food service at events:**
- [ ] **HACCP plan:** every food vendor must have a documented HACCP system
- [ ] **Food handler training:** all food handlers must have formacao em higiene alimentar (valid certificate)
- [ ] **Temperature control:** cold food <5C, hot food >65C, documented temperature logs
- [ ] **Allergen labeling:** 14 EU allergens displayed (Regulamento 1169/2011) — cereais c/ gluten, crustaceos, ovos, peixe, amendoim, soja, leite, frutos casca rija, aipo, mostarda, sesamo, dioxido enxofre, tremoco, moluscos
- [ ] **Water supply:** potable water must be available, tested if from private supply
- [ ] **Waste management:** food waste separation, grease traps if applicable
- [ ] **Handwashing:** facilities available for all food handlers (soap, paper towels, warm water)
- [ ] **Pest control:** measures in place for multi-day events
- [ ] **Vendor documentation:** collect from each vendor: HACCP certificate, food handler training certificates, insurance, NIF, licenca de atividade
- [ ] **ASAE inspection readiness:** ASAE can inspect without notice during event

**ASAE penalties for non-compliance:**
- Minor infractions: 250-3,740 EUR
- Serious infractions: 3,740-44,890 EUR
- Very serious infractions: 44,890-140,000 EUR
- Repeated offenses can result in event shutdown and activity suspension

### 6. Noise regulations (Regulamento Geral do Ruido)

**Legal framework:** DL 9/2007 (Regulamento Geral do Ruido)

**Key rules:**
| Parameter | Limit | Notes |
|---|---|---|
| **Periodo diurno** (07:00-20:00) | LAeq <= 65 dB(A) at facade of nearest habitation | In mixed zones (zonas mistas) |
| **Periodo entardecer** (20:00-23:00) | LAeq <= 60 dB(A) at facade | In mixed zones |
| **Periodo noturno** (23:00-07:00) | LAeq <= 55 dB(A) at facade | In mixed zones; events after 23h need special licenca |
| **Emergence** | Evento sonoro nao pode exceder ruido de fundo em >5 dB(A) noturno, >3 dB(A) diurno | Measured at nearest sensitive receptor |

**Noise license process:**
1. Request licenca especial de ruido from Camara Municipal (15-30 days before)
2. Submit: event details, noise mitigation measures, expected sound levels, duration
3. CM may require acoustic study (medicao acustica) by certified acoustician
4. Typical conditions: maximum dB level, end time, sound orientation away from habitation
5. Exceptions: festividades tradicionais (festas populares, Santos Populares) — municipalities can grant broader exceptions

**Noise mitigation measures:**
- Directional speaker arrays (point away from residential areas)
- Sound limiters on mixing desk (hard limit at permitted dB)
- Bass frequency management (low frequencies travel further)
- Sound barriers / walls if feasible
- Communication with neighbors (advance notice, complaint hotline)
- Noise monitoring during event (dB meter at perimeter, continuous logging)

### 7. Accessibility (DL 163/2006)

**Legal framework:** DL 163/2006 (Acessibilidade) + Convencao ONU sobre os Direitos das Pessoas com Deficiencia

**Event accessibility checklist:**
- [ ] **Wheelchair access:** ramps (max 6% gradient, 8% for short ramps), accessible pathways (min 1.2m wide), no steps without alternative
- [ ] **Accessible WC:** minimum 1 per event (1.5m x 2.2m minimum, grab bars, accessible lock)
- [ ] **Hearing assistance:** hearing loop or FM system for main stage/conference area, sign language interpreter (Lingua Gestual Portuguesa — LGP) if requested
- [ ] **Visual aids:** large print program, accessible website (WCAG 2.1 AA), screen reader compatible event app
- [ ] **Service animals:** permitted in all areas (no exceptions)
- [ ] **Accessible parking:** designated spaces near entrance (1 per 25 total, minimum 1)
- [ ] **Accessible seating:** wheelchair positions in all seating areas (not segregated), companion seats
- [ ] **Sensory considerations:** quiet room/zone for neurodivergent attendees, visual alerts for deaf attendees
- [ ] **Communication:** accessibility information published on website, contact for accessibility requests
- [ ] **Staff training:** event staff trained on accessibility assistance, disability awareness

**Portuguese note:** DL 163/2006 applies to all edificios e espacos publicos, including event venues. Non-compliance is an infraction; Camara Municipal or IGAS (Inspeccao-Geral das Atividades em Saude) can enforce.

### 8. Environmental compliance

**Waste management plan (mandatory for large events):**
- [ ] Recycling stations: separate bins for papel/cartao, plastico/metal, vidro, organico, indiferenciado
- [ ] Operator: contract with licensed waste operator (Sociedade Ponto Verde system)
- [ ] Cleaning team: during and post-event, area left clean within 24h
- [ ] Hazardous waste: cooking oil, batteries, electronic waste — separate collection
- [ ] Single-use reduction: ban on single-use plastics where feasible (EU Directive 2019/904)

**Traffic and transport:**
- Traffic management plan for >500 attendees in urban areas
- Coordination with Camara Municipal for road closures or traffic diversions
- Parking plan with capacity limits
- Public transport information provided to attendees
- Shuttle service if venue is remote

**Environmental impact assessment:**
- Not typically required for standard events unless in protected areas
- Events in Rede Natura 2000 or Parque Natural: ICNF assessment required
- Events near water courses: APA (Agencia Portuguesa do Ambiente) consultation

### 9. Temporary structures

**Licensing for temporary structures:**
| Structure | Requirement | Notes |
|---|---|---|
| Tents/marquees <50 sqm | No special license | Must comply with SCIE fire safety |
| Tents/marquees >50 sqm | Camara Municipal license + structural engineer report | Wind/load calculations, anchorage, emergency exits |
| Stages >2m height | Structural engineer sign-off | Load capacity for equipment + performers + weather |
| Fencing/barriers >2m | Camara Municipal notification | Crowd management barriers may need engineer review |
| Inflatables | Insurance + operator certification | Mandatory insurance, wind speed limits (usually 25-35 km/h) |
| Temporary grandstands | Camara Municipal + structural engineer | EN 13200-6 compliance, regular inspection during event |

**Structural engineer requirements:**
- Registered with Ordem dos Engenheiros (OE) or Ordem dos Engenheiros Tecnicos (OET)
- Must provide termo de responsabilidade (liability declaration)
- Inspection: before public access, daily for multi-day events
- Documentation: structural calculations, material certifications, installation records

### 10. Alcohol licensing

**Portuguese alcohol service requirements:**
- Age verification: 18+ (Lei 106/2015 — venda e consumo de bebidas alcoolicas a menores)
- ID check: mandatory for anyone appearing under 25
- Responsible service: staff trained on signs of intoxication, right to refuse service
- Late-night restrictions: vary by municipality — some limit alcohol sales after 02:00 or 04:00
- ASAE compliance: alcohol vendors need licenca, proper storage, temperature control
- Separate licensing may be needed for spirits (bebidas espirituosas) vs. beer/wine in some municipalities
- No alcohol service near schools, hospitals, or religious sites (proximity restrictions)

### 11. Capacity certification

**Venue capacity (lotacao):**
- All venues have a maximum capacity in their alvara de funcionamento
- This number is legally binding — exceeding it is a contraordenacao grave
- Capacity considers: floor area, exit width, fire safety category, structural load
- For temporary venues: capacity must be calculated and certified by engineer
- Occupancy monitoring: organizer must track entries/exits in real-time for events >500

**Capacity calculation reference (standing events):**
- Stage area: 2 persons/sqm (front), 3-4 persons/sqm (back)
- Circulation: 40% of floor area reserved for circulation (not counted in capacity)
- Bar/food areas: 1 person/sqm
- Seated: per seat count (fire safety exits sized accordingly)

### 12. Licensing timeline (consolidated)

| Weeks Before | Action | Entity | Notes |
|---|---|---|---|
| **16-12** | Initial consultation with CM | Camara Municipal | Understand local requirements, book slots |
| **12-8** | Submit CM license application | Camara Municipal | Occupacao de via publica, licenca de ruido, temporary structures |
| **12-8** | Submit IGAC registration | IGAC | Espetaculos e divertimentos publicos |
| **8-6** | Request policiamento | PSP/GNR | For events >1,000 or public space |
| **8-6** | Contract insurance | Insurer | RC publica, cancelamento, acidentes trabalho |
| **8-4** | Fire safety plan submission | Bombeiros / ANPC | For 3a/4a categoria risk |
| **6-4** | ANAC drone authorization | ANAC | If drone filming planned |
| **6-4** | Vendor HACCP verification | ASAE compliance | Collect all vendor documentation |
| **4-2** | Structural engineer inspection | Registered engineer | Temporary structures, stages, tents >50 sqm |
| **2-1** | Final safety inspection | CM / Bombeiros | On-site verification |
| **1-0** | Pre-event checklist sign-off | Event manager | All permits obtained, filed, copies on-site |
| **0** | Permits available on-site | — | All permits must be physically present at event |

## Output template

```markdown
---
project: <event-name>
date: <YYYY-MM-DD>
type: atlas-compliance-checklist
event_date: <YYYY-MM-DD>
municipality: <Camara Municipal>
expected_attendance: <number>
---

# Checklist de Licenciamento e Compliance — <Event Name>

## Resumo
| Parametro | Valor |
|---|---|
| Evento | <name> |
| Data | <date> |
| Local | <venue> |
| Municipio | <CM> |
| Assistencia | <N> |
| Tipo | <espetaculo/feira/conferencia/festival> |

## Licencas Obrigatorias
| Licenca | Entidade | Deadline | Status | Custo | Responsavel |
|---|---|---|---|---|---|
| CM — ocupacao via publica | CM <municipio> | <date> | ⬜ | EUR | ... |
| IGAC — registo espetaculo | IGAC | <date> | ⬜ | EUR | ... |
| PSP — policiamento | PSP <esquadra> | <date> | ⬜ | EUR | ... |
| Seguro RC | <seguradora> | <date> | ⬜ | EUR | ... |
| Licenca ruido | CM <municipio> | <date> | ⬜ | EUR | ... |
| ... | ... | ... | ⬜ | ... | ... |

## Seguranca Contra Incendios (SCIE)
- Categoria de risco: <1a/2a/3a/4a>
- [ ] Extintores: <N> unidades
- [ ] Saidas de emergencia: <N> (largura total: Xm)
- [ ] Sinaletica fotoluminescente
- [ ] Plano de evacuacao afixado
- [ ] Iluminacao de emergencia
- [ ] Materiais ignifugos (decoracao, cortinas)
- [ ] Coordenacao com bombeiros

## Seguranca Alimentar (HACCP)
- [ ] Todos os vendedores com plano HACCP
- [ ] Certificados de formacao higiene alimentar
- [ ] Controlo de temperaturas documentado
- [ ] Alergénios sinalizados (14 alergénios UE)
- [ ] Fornecimento de agua potavel
- [ ] Gestao de residuos alimentares

## Ruido
- Licenca especial de ruido: ⬜ Obtida / ⬜ Pendente
- Limite: <dB(A)> ate as <hora>
- Medicao acústica: <sim/nao>
- Mitigacao: <medidas>

## Acessibilidade (DL 163/2006)
- [ ] Acesso cadeira de rodas
- [ ] WC acessivel
- [ ] Lugares reservados/acessiveis
- [ ] Parking acessivel
- [ ] Informacao de acessibilidade publicada

## Estruturas Temporarias
| Estrutura | Licenca CM | Eng. Estrutural | Status |
|---|---|---|---|
| Palco (<dim>) | ⬜ | ⬜ | ... |
| Tenda (<dim>) | ⬜ | ⬜ | ... |

## RGPD
- [ ] Politica de privacidade no website
- [ ] Consentimentos na inscricao
- [ ] Sinaletica CCTV/fotografia
- [ ] Acordo com subprocessadores

## Ambiente
- [ ] Plano de gestao de residuos
- [ ] Estacoes de reciclagem
- [ ] Plano de transito (se aplicavel)

## Documentos no Local (dia do evento)
- [ ] Copia de todas as licencas
- [ ] Livro de reclamacoes
- [ ] Plano de emergencia
- [ ] Contactos de emergencia
- [ ] Seguro (copia apolice)

## Proximos Passos
- [ ] <next license to apply for, with deadline>
- [ ] <next inspection to schedule>
- [ ] <vendor documentation to collect>
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Compliance Checklist ATLAS.md`

## Red Flags

- Never organize a public event without Camara Municipal notification/license — even "small" events in public spaces require CM authorization; operating without it can result in event shutdown by PSP/CM on the day
- Never skip IGAC registration for events with paid admission or public performance — DL 23/2014 requires it; IGAC inspectors can close an unregistered event and issue fines
- Never allow food service without verified HACCP documentation from every vendor — ASAE inspections are unannounced; a single non-compliant vendor can shut down all food service at the event
- Never exceed the venue's licensed capacity (alvara lotacao) — it is a legal offense in Portugal, and in case of incident, the organizer bears full criminal and civil liability
- Never schedule amplified music events past the licensed noise hours without a licenca especial de ruido — DL 9/2007 penalties plus neighbor complaints to CM can shut down the event
- Never install temporary structures >50 sqm without structural engineer sign-off and CM license — a collapsed tent or stage is catastrophic; the engineer's termo de responsabilidade is legally required
- Never assume a private venue handles all compliance — the event organizer is jointly responsible for all compliance, not just the venue; verify independently

## Interactions

- Follows `atlas-risk` (risk assessment identifies regulatory requirements)
- Follows `atlas-briefing` (event type and scope determine permit needs)
- Follows `atlas-venue` (venue type determines applicable regulations)
- Coordinates with `atlas-catering` (HACCP, ASAE, alcohol licensing)
- Coordinates with `atlas-sustainability` (environmental compliance, waste management)
- Coordinates with `atlas-crm` (RGPD compliance for attendee data)
- Informs `atlas-budget` (permit costs, insurance costs, security costs)
- Informs `atlas-timeline` (permit deadlines in master timeline)
- Pairs with `dario-legal` for contract and liability review


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-compliance** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-compliance:**

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
