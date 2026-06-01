---
name: atlas-briefing
description: Structured event briefing and requirements gathering for all event types. Captures event type, scale, objectives, audience profile, budget, dates, venue preferences, stakeholder mapping, success KPIs, brand alignment, and constraints. Triggers on "briefing evento", "novo evento", "planear evento", "event brief", "requisitos evento", "new event", "event planning".
license: MIT
---

# ATLAS Skill — Event Briefing & Requirements Gathering

Structured intake process that transforms a vague event idea into a comprehensive, actionable Event Brief Document. Captures every dimension needed to plan, budget, and execute an event — from strategic objectives to dietary requirements. The brief becomes the single source of truth for all downstream ATLAS skills.

## When to activate

Invoke `/atlas-briefing` (or trigger automatically) when:
- User is planning a new event of any type
- User says "tenho um evento" or "preciso de organizar..."
- User needs a structured template for client event intake
- User has scattered notes/emails about an event and needs structure
- User is preparing for an initial event planning meeting

Do NOT use when:
- Event already has a complete brief and needs execution (use `atlas-timeline`)
- User needs only venue search (use `atlas-venue`)
- User needs only a budget estimate (use `atlas-budget`)

## Workflow

### 1. Identify briefing mode
- **Interactive:** ATLAS asks questions section by section, adapts follow-ups based on event type
- **Template:** Generate a blank Event Brief Document for client self-completion
- **From notes:** User pastes emails, meeting notes, WhatsApp messages — ATLAS structures them into the brief format

Ask which mode the user prefers. Default to interactive if unclear.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "event planning briefing requirements gathering checklist", limit: 5)
mcp__dario-rag__search_kb(query: "corporate event objectives KPIs success metrics", limit: 5)
```

### 3. Section A — Event Identity
- **Event name/working title:** even if provisional
- **Event type:** corporate (conference, seminar, workshop, team building, product launch, gala dinner, awards ceremony, AGM), social (wedding, birthday, anniversary, graduation, baby shower), public (festival, fair, market, concert, exhibition, community event), hybrid (virtual + in-person)
- **Scale classification:** intimate (<50 pax), medium (50-200), large (200-1,000), massive (1,000+)
- **Edition:** first-time, recurring (which edition), annual
- **Date(s):** confirmed date, preferred dates, blackout dates, flexibility level
- **Duration:** single session, half-day, full day, multi-day, weekend

### 4. Section B — Strategic Objectives
- **Primary objective:** (choose max 2) brand awareness, lead generation, revenue, education, networking, celebration, team alignment, product launch, community building, fundraising
- **Secondary objectives:** up to 3 additional goals
- **Success KPIs with targets:**
  - Attendance: target number, minimum viable
  - NPS: target score (>50 good, >70 excellent)
  - Leads generated: quantity and quality criteria
  - Revenue: ticket sales, sponsorship, merchandise targets
  - Media coverage: publications, social reach, impressions
  - Engagement: session ratings, app interactions, Q&A participation
- **What does "success" look like?** One sentence from the stakeholder

### 5. Section C — Audience Profile
- **Primary audience:** demographics, job titles, industry, interests
- **Secondary audience:** media, sponsors, VIPs, speakers
- **Expected attendance:** confirmed, invited, realistic estimate
- **Audience journey:** how they hear about it, register, arrive, experience, leave, follow up
- **Accessibility needs:** mobility, hearing, visual, dietary, language (PT/EN/other)
- **Dress code:** black tie, business formal, smart casual, casual, themed

### 6. Section D — Stakeholder Map
| Stakeholder | Role | Decision Power | Contact | Notes |
|---|---|---|---|---|
| ... | Event Owner / Sponsor | Final approval | ... | Budget holder |
| ... | Project Manager | Day-to-day decisions | ... | Primary contact |
| ... | Marketing Lead | Brand approval | ... | Collateral sign-off |
| ... | Finance | Budget release | ... | PO/invoice process |
| ... | Operations | Logistics | ... | Internal resources |
| ... | External Agency | Execution partner | ... | Scope of work |

### 7. Section E — Budget Framework
- **Total budget:** confirmed amount or range (min-max)
- **Budget status:** approved, pending approval, indicative
- **Budget includes/excludes:** IVA, travel, accommodation, speaker fees
- **Revenue expected:** ticket sales, sponsorship, grants
- **Payment process:** PO required? invoice terms? advance payments?
- **Cost sensitivity:** where to invest vs. where to save
- **Contingency:** standard 10-15%, client awareness of need

### 8. Section F — Location & Logistics
- **Geographic preference:** city, region, specific area
- **Venue type preference:** hotel, convention center, quinta, outdoor, unique/unusual
- **Accommodation needed:** for how many, star rating, proximity
- **Transport:** airport transfers, parking, shuttle service
- **Catering style:** seated dinner, buffet, cocktail, food stations, food trucks
- **Dietary requirements known:** vegetarian, vegan, halal, kosher, allergies, celiac

### 9. Section G — Brand & Experience
- **Brand guidelines:** logo usage, colors, fonts, tone of voice
- **Visual identity:** existing event branding or create new
- **Tone:** formal, professional, relaxed, fun, inspirational, exclusive
- **Key messages:** what should attendees remember/feel after
- **Content/Program outline:** keynotes, panels, workshops, entertainment, networking
- **Technology:** event app, live streaming, polling, AR/VR, LED walls

### 10. Section H — Constraints & Risk
- **Non-negotiable requirements:** items that cannot be compromised
- **Hard constraints:** date, budget ceiling, venue already booked, specific vendors required
- **Regulatory:** IGAC license, Camara Municipal permits, ASAE food safety, DGS health protocols
- **Insurance:** event liability, cancellation insurance, equipment coverage
- **Risk appetite:** contingency budget %, backup venue, wet weather plan
- **Past event history:** what worked, what failed, lessons learned, attendee complaints

### 11. Consolidation and validation
- Summarize all captured information in structured format
- Highlight gaps requiring follow-up
- Flag contradictions (e.g., "intimate VIP experience" + "1,000 attendees")
- Flag unrealistic expectations (e.g., "gala dinner for 200" + "5,000 EUR budget")
- Confirm priority ranking with stakeholder

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-briefing
event_type: <corporate|social|public|hybrid>
scale: <intimate|medium|large|massive>
expected_attendance: <number>
budget_range: <min-max EUR>
event_date: <YYYY-MM-DD or TBC>
---

# Event Brief — <Event Name>

## A. Identidade do Evento
| Campo | Detalhe |
|---|---|
| Nome | ... |
| Tipo | ... |
| Escala | ... |
| Edicao | ... |
| Data(s) | ... |
| Duracao | ... |

## B. Objectivos Estrategicos
### Objectivo principal
### KPIs e metas
| KPI | Meta | Minimo viavel |
|---|---|---|
| Assistencia | ... | ... |
| NPS | ... | ... |
| Leads | ... | ... |
| Receita | ... | ... |

## C. Perfil do Publico
### Audiencia principal
### Audiencia secundaria
### Acessibilidade e necessidades especiais
### Dress code

## D. Mapa de Stakeholders
| Nome | Papel | Poder de decisao | Contacto |
|---|---|---|---|

## E. Enquadramento Orcamental
| Parametro | Valor |
|---|---|
| Budget total | ... |
| Status | Aprovado / Pendente |
| Receitas previstas | ... |
| Contingencia | ... |

## F. Localizacao e Logistica
### Preferencias de venue
### Alojamento
### Transporte
### Catering

## G. Marca e Experiencia
### Identidade visual
### Tom e mensagens-chave
### Programa/conteudo
### Tecnologia

## H. Condicionantes e Riscos
### Requisitos inegociaveis
### Restricoes
### Regulatorio (IGAC, CM, ASAE)
### Seguros
### Historico de eventos anteriores

## Sintese e Validacao
### Pontos fortes do briefing
### Gaps a esclarecer
### Contradicoes identificadas
### Expectativas a gerir

## Proximos Passos
- [ ] Stakeholder valida este briefing
- [ ] Seguir com `atlas-venue` para selecao de espaco
- [ ] Seguir com `atlas-budget` para orcamento detalhado
- [ ] Seguir com `atlas-timeline` para cronograma e run-of-show
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Event Brief ATLAS.md`

## Red flags — don't do this
- Never proceed with venue booking or vendor contracts without a validated briefing
- Never assume audience size without explicit confirmation — 50 vs 500 changes everything
- Never accept "no budget" as an answer — even a range is essential; without it every downstream decision is blind
- Never ignore the stakeholder map — events fail when the wrong person is making decisions or the real decision maker is absent
- Never skip the "non-negotiable requirements" question — discovering these mid-planning causes costly pivots
- Never let vague objectives stand — "a nice event" is not an objective; push for measurable KPIs
- Never forget to ask about past events — repeating known failures destroys client trust
- Never ignore accessibility needs — legal obligation under PT law and ethical imperative
- Never accept conflicting date/budget/scale without flagging — a 5,000 EUR gala for 300 is not viable; say so immediately

## Interactions
- First skill in the ATLAS workflow — everything starts with the brief
- Feeds into `atlas-venue` for venue selection aligned with requirements
- Feeds into `atlas-budget` for detailed financial planning
- Feeds into `atlas-timeline` for pre-event milestones and day-of run sheet
- Feeds into `atlas-checklist` for operational checklists
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-briefing** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-briefing:**

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
