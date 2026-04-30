---
name: atlas-risk
description: Risk assessment & contingency planning — risk matrix (likelihood x impact), weather contingency, medical/health protocols, security planning, crowd management, crisis communication, insurance requirements, business continuity, and force majeure. Portuguese specifics including Protecao Civil, PSP/GNR, INEM, ANPC, SCIE fire safety, and summer fire risk. Triggers on "risco evento", "event risk", "contingency", "contingencia", "plano emergencia", "emergency plan", "seguranca evento", "crisis management", "cancelamento evento", "insurance evento", "seguro evento", "crowd management", "gestao multidoes".
license: MIT
---

# ATLAS Skill — Risk Assessment & Contingency Planning

Produces comprehensive event risk assessments with risk matrices, contingency plans for every major risk category, crisis communication protocols, and insurance guidance. Covers weather, health, security, technical, financial, reputational, vendor, and natural disaster risks. Deep Portuguese regulatory context including Protecao Civil, PSP/GNR liaison, INEM, and ANPC requirements.

## When to activate

Invoke `/atlas-risk` (or trigger automatically) when:
- User is planning any event with 100+ attendees
- User asks about event safety, emergency plans, or "what could go wrong"
- User asks "do I need insurance for the event" or "preciso de seguro"
- User needs a weather contingency plan for outdoor events
- User needs crowd management or security planning
- User asks about crisis communication or PR risk
- User needs to assess financial risk (low ticket sales, sponsor withdrawal)
- Before `atlas-compliance` (risk assessment informs permit requirements)

Do NOT use when:
- User needs routine logistics planning (use `atlas-timeline`, `atlas-checklist`)
- User needs venue selection (use `atlas-venue`)
- User needs permits/licensing details (use `atlas-compliance` — but risk assessment feeds into it)

## Trigger phrases (PT/EN)

- "risco do evento", "event risk assessment", "avaliacao de riscos"
- "plano de contingencia", "contingency plan", "plano B"
- "plano de emergencia", "emergency plan", "seguranca do evento"
- "e se chover", "what if it rains", "weather backup"
- "crowd management", "gestao de multidoes", "controlo de acessos"
- "crisis communication", "comunicacao de crise"
- "seguro do evento", "event insurance", "cancelamento"
- "first aid", "primeiros socorros", "equipa medica"

## Workflow

### 1. Gather risk inputs

From `atlas-briefing`, `atlas-venue`, and user input:
- **Event type:** indoor/outdoor/hybrid, single-day/multi-day
- **Expected attendance:** total and peak concurrent
- **Venue type:** purpose-built, temporary structure, public space, heritage building
- **Date/season:** summer fire risk, winter weather, holiday proximity
- **Audience profile:** age range, alcohol service, physical activity level
- **Activities:** pyrotechnics, water, heights, food service, alcohol, physical sports
- **Location:** urban/rural, proximity to emergency services, transport links
- **Duration:** day event, overnight, multi-day camping
- **Budget:** insurance budget, safety infrastructure budget
- **History:** incidents at previous editions, near-misses, complaints

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "event risk assessment matrix contingency planning", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "crowd management safety security event planning", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "crisis communication plan stakeholder management", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "event insurance cancellation force majeure", collection: "dario", limit: 5)
```

### 3. Risk identification by category

**Category 1 — Weather:**
| Risk | Likelihood (outdoor) | Impact | Contingency |
|---|---|---|---|
| Rain / storm | 3-4 (varies by season) | 3-4 | Indoor backup venue, tents/marquees, rain kits (ponchos, umbrellas), drainage plan |
| Extreme heat (>35C) | 4 (PT summer) | 3-4 | Water stations every 50m, shade structures, misting fans, shortened outdoor exposure, medical team for heat stroke |
| High wind (>40km/h) | 2-3 | 4-5 | Secure temporary structures, threshold for dismantling tents/stages, IPMA monitoring, cancellation protocol at 60km/h |
| Lightning | 2 | 5 | Evacuation to indoor spaces, 30-min rule (no outdoor activity until 30 min after last strike), IPMA alerts |
| Cold / frost | 2-3 (winter) | 2 | Heating, hot beverages, blankets, shorten outdoor exposure |
| Fog | 2 | 2 | Enhanced signage, lighting, adjust start time |

**IPMA monitoring:** Set up IPMA (Instituto Portugues do Mar e da Atmosfera) alerts for the event location. Check daily from 1 week before, hourly on event day.

**Category 2 — Medical & Health:**
| Risk | Likelihood | Impact | Contingency |
|---|---|---|---|
| Minor injuries (trips, falls) | 4 | 1-2 | First aid posts, trained first aiders (1 per 250 attendees), clear signage |
| Serious medical emergency | 2 | 5 | AED (defibrillator) on site, ambulance on standby (mandatory >1,000 pax in PT), INEM 112 protocol |
| Food poisoning | 2 | 4 | HACCP compliance, temperature monitoring, allergen labeling, food vendor vetting |
| Pandemic / infectious disease | 1-2 | 5 | Ventilation plan, hand sanitizer stations, isolation room, rapid test capability, virtual pivot plan |
| Alcohol-related incidents | 3 (events with bar) | 3 | Responsible service training, ID checks (18+ in PT), water available free, taxi/transport info |
| Allergic reactions | 2 | 4 | Allergen labeling (14 EU allergens per Reg. 1169/2011), epi-pen in first aid kit, medical team briefed |
| Heat stroke / dehydration | 3 (PT summer) | 4 | Free water, shade, medical team trained for heat emergencies, cooling stations |

**Portuguese medical requirements:**
- Events >1,000 attendees: ambulance on standby + medical team (INEM coordination)
- Events >5,000: INEM Posto Medico Avancado (advanced medical post)
- AED (defibrillador): not yet legally mandatory at all events but strongly recommended; mandatory in sports events
- First aid: minimum 1 first aider per 250 attendees, more for active/outdoor events
- INEM contact: Numero Europeu de Emergencia 112, or direct INEM CODU coordination for large events

**Category 3 — Security:**
| Risk | Likelihood | Impact | Contingency |
|---|---|---|---|
| Unauthorized access | 3 | 2-3 | Perimeter control, credentialing system, security at all entry points |
| Theft | 3 | 2 | Cloakroom service, "secure your belongings" signage, CCTV, security patrols |
| Assault / violence | 2 | 4 | Security team sizing (1 per 100 for standard, 1 per 50 for alcohol events), conflict de-escalation training |
| Terrorism threat | 1 | 5 | PSP/GNR liaison, access control, bag checks, vehicle barriers, suspicious package protocol |
| VIP security incident | 1-2 | 4-5 | Dedicated close protection, secure rooms, separate entrance/exit, advance team |
| Protest / disruption | 2 | 3 | PSP/GNR coordination, designated protest area, media management, speaker briefing |

**Portuguese security force liaison:**
- **PSP** (Policia de Seguranca Publica): urban areas, mandatory coordination for events >1,000 in public spaces
- **GNR** (Guarda Nacional Republicana): rural areas, same threshold
- Request policiamento (paid police presence) at least 30 days before — costs 25-50 EUR/officer/hour
- Private security (vigilancia privada): must be licensed by PSP (Alvara de seguranca privada), DL 34/2013
- Security staff must carry cartao profissional MAI (Ministerio da Administracao Interna)

**Category 4 — Crowd Management:**
| Parameter | Guideline | Source |
|---|---|---|
| Maximum density | 4 persons/sqm (standing), 2 persons/sqm (seated) | ANPC / EU best practices |
| Emergency egress time | Full evacuation within 8 minutes (enclosed venue) | SCIE / DL 220/2008 |
| Exit width | Minimum 1m per 120 persons | SCIE regulations |
| Crush barriers | Required for >2,000 standing audience, max 3,000 between barriers | EN 13200-1 |
| Ingress flow rate | 40-60 persons/min per 1m entry width (with bag check) | Industry standard |
| Capacity monitoring | Real-time headcount at entries/exits, never exceed alvara capacity | Legal requirement |

**Crowd management plan elements:**
- Entry/exit flow design (separate ingress from egress where possible)
- Queue management (serpentine, estimated wait time signage)
- Crowd density monitoring (visual, sensors, or manual counting)
- Barrier placement (front of stage, separation zones)
- Emergency evacuation routes (minimum 2 independent routes per zone)
- Steward/marshal deployment (1 per 250 for general, 1 per 100 for dense areas)
- Communication system (radios for all key personnel, PA system for announcements)

**Category 5 — Technical:**
| Risk | Likelihood | Impact | Contingency |
|---|---|---|---|
| Power failure | 2 | 4-5 | UPS for critical systems, backup generator, electrician on standby |
| AV equipment failure | 3 | 3-4 | Backup projector, spare microphones, backup laptop, tech crew on site |
| Internet failure | 3 | 3 | Backup 4G/5G hotspot, offline mode for critical systems, backup ISP |
| Ticketing/check-in system crash | 2 | 3 | Offline attendee list (printed + USB), manual check-in procedure |
| Event app failure | 2 | 2 | Printed program as fallback, WhatsApp group for updates |
| Stage/structure failure | 1 | 5 | Structural engineer sign-off, load testing, weather monitoring, inspection schedule |

**Category 6 — Financial:**
| Risk | Likelihood | Impact | Contingency |
|---|---|---|---|
| Low ticket sales (<60% capacity) | 3 | 4 | Trigger marketing escalation at -6 weeks, pivot pricing, partner promotions |
| Major sponsor withdrawal | 2 | 4-5 | Sponsor contracts with cancellation fees, diversified sponsor base (no single sponsor >30% of revenue), reserve fund |
| Cost overrun | 3 | 3 | 10-15% contingency in budget, regular budget reviews, change order approval process |
| Vendor bankruptcy / no-show | 2 | 4 | Backup vendor list for every critical service, advance payments limited to 30%, escrow for large amounts |
| Currency fluctuation (international) | 1-2 | 2 | Fix rates in contracts, hedge if >10% of budget is foreign |

**Category 7 — Reputational:**
| Risk | Likelihood | Impact | Contingency |
|---|---|---|---|
| Negative social media incident | 3 | 3-4 | Social media monitoring (real-time), response protocol, designated spokesperson |
| Speaker controversy | 2 | 3-4 | Speaker vetting, code of conduct, prepared holding statement |
| Accessibility complaint | 2 | 3 | DL 163/2006 compliance, accessibility audit, proactive communication |
| Data breach (attendee data) | 1-2 | 5 | RGPD compliance, encryption, breach notification protocol (72h to CNPD) |
| Media negative coverage | 2 | 3-4 | Media relations plan, press spokesperson, proactive positive storytelling |

### 4. Risk matrix template

**Scoring: Likelihood (1-5) x Impact (1-5) = Risk Score**

| Score | Risk Level | Action Required |
|---|---|---|
| 1-4 | **LOW** (Green) | Accept risk, monitor, basic mitigation |
| 5-9 | **MEDIUM** (Amber) | Active mitigation plan, assign owner, review regularly |
| 10-15 | **HIGH** (Red) | Comprehensive contingency plan, escalation protocol, dedicated resource |
| 16-25 | **CRITICAL** (Black) | Event viability question, board/leadership decision, consider cancellation |

**Risk register format:**
| ID | Risk | Category | Likelihood (1-5) | Impact (1-5) | Score | Level | Owner | Mitigation | Contingency | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Heavy rain during outdoor event | Weather | 3 | 4 | 12 | HIGH | Event Manager | IPMA monitoring, tent coverage | Move to indoor backup venue | Active |
| R02 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 5. Crisis communication protocol

**Crisis communication hierarchy:**
1. **Incident Commander** (Event Director): overall decision authority
2. **Communications Lead**: all external communications
3. **Operations Lead**: manages on-ground response
4. **Medical Lead**: health/safety incidents
5. **Legal Advisor**: contractual and liability guidance (on-call)

**Communication protocol by scenario:**

| Scenario | Internal Response | External Message | Channel | Timing |
|---|---|---|---|---|
| Weather cancellation | All-hands briefing, vendor notification | "Event postponed due to weather" + refund/reschedule info | Email + social + website + PA | ASAP, <30 min |
| Medical emergency | Isolate area, medical response, incident log | No public statement unless media inquires; prepared holding statement | Spokesperson only | Only if asked |
| Security incident | Lockdown/evacuation, PSP/GNR coordination | "Event paused for safety. Follow steward instructions." | PA + social + text | Immediate |
| Technical failure | Tech crew fix, backup activation | "Brief pause. We'll be back in X minutes." | PA + social | Within 5 min |
| PR/social media crisis | Assess severity, prepare response, legal review | Acknowledge, empathize, state actions | Social media + email | Within 1 hour |

**Holding statement template (Portuguese):**
> "Estamos cientes da situacao e estamos a trabalhar para a resolver o mais rapidamente possivel. A seguranca e bem-estar dos nossos participantes e a nossa prioridade absoluta. Atualizaremos assim que tivermos mais informacao. Obrigado pela compreensao."

**Holding statement template (English):**
> "We are aware of the situation and are working to resolve it as quickly as possible. The safety and wellbeing of our attendees is our absolute priority. We will provide updates as more information becomes available. Thank you for your understanding."

### 6. Insurance requirements

**Essential event insurance (Portugal):**

| Type | Coverage | Minimum Recommended | Portuguese Notes |
|---|---|---|---|
| **Seguro de responsabilidade civil** (Public liability) | Third-party injury/damage | 1,000,000 EUR (2M for >1,000 pax) | Mandatory for public events, Fidelidade/Tranquilidade/Generali |
| **Seguro de cancelamento** (Event cancellation) | Financial loss from cancellation | Full event budget | Check exclusions (pandemic, pre-existing conditions) |
| **Seguro de acidentes de trabalho** (Workers comp) | Employee/contractor injuries | Legal minimum per DL 159/99 | Mandatory for all workers, including temporary staff |
| **Seguro de equipamento** | Equipment loss/damage/theft | Replacement value | For rented AV, staging, structures |
| **Seguro de responsabilidade civil profissional** | Professional errors/omissions | 500,000 EUR | For event organizers as professionals |
| **Weather insurance** | Specific weather trigger | Revenue at risk | Available from specialist insurers (parametric policies) |

**Portuguese insurance market:**
- Major event insurers: Fidelidade, Tranquilidade, Generali, Zurich, Allianz
- Event cancellation: typically 3-8% of insured sum as premium
- Public liability: 500-3,000 EUR/year depending on event size and type
- Get quotes at least 8 weeks before event
- Broker recommendation: use an insurance broker specializing in events (corretor de seguros)

### 7. Business continuity

**Backup plans for critical dependencies:**
| Critical Element | Primary | Backup | Activation Trigger |
|---|---|---|---|
| Venue | Primary venue | Pre-negotiated backup venue (same capacity, nearby) | Venue becomes unavailable >48h before |
| Date | Planned date | Rain date or postponement date (in contracts) | Weather/emergency cancellation |
| Keynote speaker | Confirmed speaker | Backup speaker briefed, video presentation ready | Speaker cancels <7 days before |
| Catering | Primary caterer | Backup caterer on standby agreement | Caterer fails to deliver or quality failure |
| AV/Tech | Primary AV company | Backup AV inventory, local rental contacts | Equipment failure or vendor no-show |
| Power | Mains | Generator (tested 24h before) | Mains failure |
| Internet | Primary ISP | 4G/5G hotspot backup | Primary connection drops |
| Format | In-person | Hybrid/virtual pivot plan | Pandemic, severe weather, major crisis |

**Virtual pivot checklist (if event must go fully online):**
- [ ] Streaming platform ready (Zoom, Hopin, StreamYard)
- [ ] Speakers briefed on virtual format
- [ ] Attendees notified with new access links
- [ ] Ticketing platform configured for refund/credit/virtual tier
- [ ] Virtual networking solution activated
- [ ] Recording and content delivery plan
- [ ] Sponsor digital visibility plan activated

### 8. Force majeure

**Contract clause elements:**
- **Definition:** events beyond reasonable control — including but not limited to: pandemic, epidemic, natural disaster, war, terrorism, government order, severe weather, strike, fire
- **Notification:** party affected must notify in writing within 48h of the force majeure event
- **Obligations:** both parties suspended during the force majeure period
- **Rescheduling:** good faith effort to reschedule within 6 months
- **Cost sharing:** sunk costs shared proportionally or as defined per contract
- **Termination:** if force majeure exceeds 60 days, either party may terminate with mutual release
- **Insurance:** force majeure does not override insurance obligations; parties should maintain event cancellation insurance

### 9. Portuguese emergency entities

| Entity | Role | Contact | When to Engage |
|---|---|---|---|
| **INEM** (Inst. Nacional de Emergencia Medica) | Emergency medical | 112 (CODU) | Medical emergencies, pre-event coordination for >1,000 pax |
| **PSP** (Policia de Seguranca Publica) | Urban police | Local esquadra | Events >1,000 in urban public spaces, security coordination |
| **GNR** (Guarda Nacional Republicana) | Rural police | Local posto | Events in rural areas, same thresholds |
| **ANPC** (Autoridade Nacional de Protecao Civil) | Civil protection | District command | Large-scale events, multi-day, camping, pyrotechnics |
| **IPMA** (Inst. Portugues do Mar e Atmosfera) | Weather | ipma.pt | Weather monitoring, severe weather alerts |
| **Bombeiros** (Fire service) | Fire + rescue | Local corporacao | Fire safety approval, standby for pyrotechnics/large events |
| **ASAE** | Food safety, economic inspection | Regional ASAE office | Food service compliance, ticket sales compliance |
| **CNPD** | Data protection | cnpd.pt | Data breach notification (72h) |
| **Camara Municipal** | Local authority | Relevant CM | Permits, noise, public space occupation |

**Summer fire risk (July-September):**
- Portugal has extreme wildfire risk in summer, especially central/northern regions
- Outdoor events near forest: coordinate with ICNF (Inst. Conservacao Natureza e Florestas)
- No pyrotechnics during fire risk periods (ICNF prohibition)
- Fire truck on standby for rural/forest-adjacent events
- Clear vegetation around event perimeter (zone defensavel)
- Monitor daily fire risk level at ICNF/IPMA

## Output template

```markdown
---
project: <event-name>
date: <YYYY-MM-DD>
type: atlas-risk-assessment
event_date: <YYYY-MM-DD>
event_type: <indoor|outdoor|hybrid>
expected_attendance: <number>
---

# Avaliacao de Riscos — <Event Name>

## Resumo Executivo
| Parametro | Valor |
|---|---|
| Evento | <name> |
| Data | <date> |
| Local | <venue> |
| Tipo | <indoor/outdoor/hybrid> |
| Assistencia | <N> |
| Riscos criticos (16-25) | <N> |
| Riscos altos (10-15) | <N> |
| Riscos medios (5-9) | <N> |
| Riscos baixos (1-4) | <N> |

## Matriz de Riscos
| ID | Risco | Categoria | Prob | Imp | Score | Nivel | Responsavel | Mitigacao | Contingencia |
|---|---|---|---|---|---|---|---|---|---|
| R01 | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Plano de Contingencia — Meteorologia
- **Cenario chuva:** ...
- **Cenario calor extremo:** ...
- **Cenario vento forte:** ...

## Plano Medico e Saude
- **Postos de primeiros socorros:** <N> (localizacao)
- **Equipa medica:** <N> socorristas, <N> enfermeiros, <N> medicos
- **Ambulancia:** <sim/nao> (obrigatoria se >1,000 pax)
- **AED:** <N> desfibrilhadores
- **Coordenacao INEM:** <sim/nao>

## Plano de Seguranca
- **Seguranca privada:** <N> elementos (empresa: <nome>)
- **PSP/GNR:** <coordenacao feita sim/nao>
- **Controlo de acessos:** <metodo>
- **CCTV:** <sim/nao>

## Gestao de Multidoes
- **Capacidade maxima:** <N> (alvara)
- **Tempo de evacuacao:** <min>
- **Saidas de emergencia:** <N>
- **Monitorizacao densidade:** <metodo>

## Comunicacao de Crise
- **Incident Commander:** <nome, contacto>
- **Porta-voz:** <nome, contacto>
- **Holding statement:** [preparado]
- **Cadeia de notificacao:** [hierarquia]

## Seguros
| Tipo | Seguradora | Cobertura | Apolice |
|---|---|---|---|
| RC publica | ... | ... EUR | ... |
| Cancelamento | ... | ... EUR | ... |
| Acidentes trabalho | ... | Legal | ... |

## Continuidade de Negocio
| Elemento critico | Backup | Trigger |
|---|---|---|
| Venue | <backup venue> | Indisponibilidade >48h antes |
| ... | ... | ... |

## Contactos de Emergencia
| Entidade | Contacto | Responsavel |
|---|---|---|
| INEM | 112 | — |
| PSP/GNR local | <tel> | <nome> |
| Bombeiros | <tel> | — |
| ANPC | <tel> | — |
| Seguradora | <tel> | <gestor conta> |

## Proximos Passos
- [ ] Submeter plano de seguranca a PSP/GNR
- [ ] Contratar seguranca privada licenciada
- [ ] Contratar seguro RC e cancelamento
- [ ] Coordenar com INEM (se >1,000 pax)
- [ ] Instalar AED e formar equipa
- [ ] Testar plano de evacuacao
- [ ] Briefing equipa dia do evento
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Avaliacao Riscos ATLAS.md`

## Red Flags

- Never organize an event for 500+ people without a formal risk assessment — informal "we'll figure it out" approaches fail catastrophically when an incident occurs; a documented risk register is also required by Portuguese authorities for public events
- Never skip insurance (seguro de responsabilidade civil) for any public event — a single slip-and-fall injury can generate liability claims exceeding the entire event budget; it is legally mandatory for public events in Portugal
- Never hold an outdoor event in Portugal without a weather contingency plan — Portuguese weather is generally mild but summer heat waves (>40C) and winter storms are real risks; IPMA monitoring should start 1 week before
- Never exceed the venue's licensed capacity (alvara) — exceeding capacity is a criminal offense in Portugal, and in case of incident, all liability falls on the organizer with no insurance protection
- Never skip PSP/GNR liaison for events with 500+ attendees in public spaces — Portuguese law requires coordination; failure to notify can result in event shutdown on the day
- Never have a single point of failure for any critical system (power, AV, internet, catering) — Murphy's Law applies doubly to events; every critical system needs a tested backup
- Never operate without a crisis communication plan — the first hour of a crisis defines the narrative; without a prepared holding statement and designated spokesperson, social media fills the vacuum with rumors

## Interactions

- Feeds directly into `atlas-compliance` (risk assessment informs permit requirements)
- Follows `atlas-briefing` (event scope and audience)
- Follows `atlas-venue` (venue-specific risks and capacity)
- Coordinates with `atlas-staff` (security team, medical team sizing)
- Coordinates with `atlas-catering` (food safety, HACCP)
- Informs `atlas-budget` (insurance costs, contingency allocation, security costs)
- Pairs with `dario-pr` for crisis communication planning
