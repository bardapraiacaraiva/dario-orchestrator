---
name: atlas-sponsor
description: Sponsorship management — tier design, benefits menu, valuation methodology, sponsor CRM pipeline, activation strategies, fulfillment checklists, ROI reporting, and contract templates. Portuguese corporate sponsorship landscape, IVA on sponsorship (23%), mecenato fiscal benefits for cultural events. Triggers on "patrocinio", "sponsor", "sponsorship", "patrocinador", "sponsor deck", "sponsorship proposal", "sponsor tiers", "naming rights", "media partner".
license: MIT
---

# ATLAS Skill — Sponsorship Management

End-to-end sponsorship lifecycle management: from tier design and prospect pipeline through activation, fulfillment, ROI reporting, and renewal. Produces sponsor decks, contracts, benefit matrices, and post-event ROI reports. Covers Portuguese corporate sponsorship budgets, IVA implications, and Estatuto do Mecenato for cultural events.

## When to activate

Invoke `/atlas-sponsor` (or trigger automatically) when:
- User needs to define sponsorship tiers and pricing for an event
- User asks "how to get sponsors" or "como arranjar patrocinadores"
- User needs a sponsorship deck/proposal
- User wants to value sponsorship benefits (CPM, media value)
- User needs sponsor activation ideas (beyond logo placement)
- User asks about sponsor contracts, deliverables, or ROI reporting
- After `atlas-briefing` and `atlas-marketing` define audience and reach projections

Do NOT use when:
- User needs general event marketing (use `atlas-marketing`)
- User needs attendee relationship management (use `atlas-crm`)
- User needs overall event budget (use `atlas-budget`)

## Trigger phrases (PT/EN)

- "patrocinio para o evento", "sponsorship tiers", "niveis de patrocinio"
- "sponsor deck", "proposta de patrocinio", "sponsorship proposal"
- "como valorizar patrocinios", "sponsorship valuation"
- "activacao de patrocinadores", "sponsor activation"
- "contrato de patrocinio", "sponsor contract"
- "ROI do patrocinio", "sponsor ROI report"
- "media partner", "parceiro media", "naming rights"

## Workflow

### 1. Gather sponsorship inputs

From `atlas-briefing` and `atlas-marketing` or user input:
- **Event type:** conference, festival, gala, awards, community, corporate
- **Expected attendance:** total + breakdown (decision-makers, C-level, students)
- **Audience demographics:** industry, seniority, geography, company size
- **Marketing reach projections:** social media followers, email list size, website traffic
- **Media coverage expected:** press, TV, radio, online
- **Past sponsors (if recurring event):** who, how much, satisfaction, renewal status
- **Event budget gap:** how much revenue needed from sponsorship
- **Competitor events:** what they charge, who sponsors them
- **Event assets available:** stage, booths, content, data, naming, digital, print

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "sponsorship tiers pricing benefits valuation", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "sponsor activation engagement brand experience", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ROI sponsor reporting media value impressions", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "corporate sponsorship contract deliverables", collection: "dario", limit: 5)
```

### 3. Sponsorship tier design

**Standard tier structure (adapt to event size):**

| Tier | Price Range | # Available | Key Benefits |
|---|---|---|---|
| **Title / Naming** | 10,000-50,000+ EUR | 1 | Event name association ("Evento by Sponsor"), all channels, keynote slot, premium booth, VIP package, data access, exclusivity |
| **Platinum** | 7,500-20,000 EUR | 2-3 | Logo on stage backdrop + all materials, speaking slot, premium booth, 10+ tickets, social media feature, lead access |
| **Gold** | 5,000-12,000 EUR | 3-5 | Logo on key materials, panel seat or workshop, standard booth, 6-8 tickets, social mention, partial lead access |
| **Silver** | 2,500-7,000 EUR | 5-8 | Logo on digital materials + signage, booth (small), 4 tickets, social mention |
| **Bronze / Supporting** | 500-2,500 EUR | 10-15 | Logo on website + program, 2 tickets, social mention |
| **Media Partner** | VIK (value in kind) | 2-5 | Cross-promotion: media coverage in exchange for logo placement + tickets |
| **Category Sponsor** | 2,000-10,000 EUR | 1 per category | Exclusive association with specific element (coffee break, networking, Wi-Fi, lanyard, app) |

**Portuguese market calibration:**
- Small events (<200 pax): reduce all tiers by 40-60%
- Medium events (200-1,000 pax): use ranges as listed
- Large events (1,000-5,000 pax): increase top tiers by 50-100%
- Major festivals/events (5,000+ pax): Title sponsor can reach 100,000+ EUR
- Portuguese corporate budgets are generally conservative vs. UK/DE/FR — value relationships and multi-year partnerships over single large deals

### 4. Benefits menu (mix-and-match)

**Visibility:**
- Logo on stage backdrop / LED screen
- Logo on printed materials (program, badges, signage, banners)
- Logo on digital channels (website, email, social media)
- Logo on event app / virtual platform
- Branded area / lounge / zone naming
- Branded merchandise (lanyards, bags, pens, notebooks)
- Roll-up / banner placement in key areas
- Video/slide loop during breaks

**Content & speaking:**
- Keynote speaking slot (15-30 min)
- Panel participation
- Workshop hosting
- Branded content (blog post, interview, video)
- Social media takeover (1 day)
- Podcast/video interview with speakers

**Experience & activation:**
- Exhibition booth/stand (premium location priority)
- Product sampling / demonstration area
- Interactive installation or experience
- Contest / prize giveaway
- Branded networking activity
- VIP dinner / exclusive session hosting

**Data & access:**
- Attendee contact list (RGPD compliant, opt-in only)
- Lead capture at booth (badge scanning)
- Post-event survey question (1-2 branded questions)
- Analytics report (demographics, engagement)
- First right of refusal for next edition

**Hospitality:**
- Complimentary tickets (tiered quantity)
- VIP access / backstage
- Reserved seating / premium placement
- Speaker dinner / networking event access
- Accommodation (for multi-day events)

### 5. Sponsorship valuation methodology

**CPM (Cost Per Thousand Impressions):**
- Calculate total impressions across all channels (digital + physical)
- Apply market CPM rate (Portugal digital: 3-8 EUR CPM, physical event signage: 15-30 EUR CPM)
- Sum = equivalent media value

**Impression calculation template:**
| Touchpoint | Audience | Frequency | Total Impressions |
|---|---|---|---|
| Stage backdrop (live) | Attendees | All day | Attendance x hours |
| Website logo | Monthly visitors | Event period | Visitors x months |
| Email mentions | Subscribers | # emails | List size x emails |
| Social media posts | Followers | # posts | Reach per post x posts |
| Printed materials | Attendees | 1x | Attendance |
| Event app | App users | Multi-day | Users x sessions |
| Media coverage | Media reach | # articles | Article reach sum |
| **Total Impressions** | | | **Sum** |

**Value stacking:**
- Media value: impressions x CPM
- Lead value: # qualified leads x avg lead value (B2B: 50-200 EUR/lead)
- Brand association value: premium for category exclusivity (20-30% uplift)
- Networking access value: access to decision-makers, priced per comparable event ticket
- Content value: equivalent cost to produce branded content independently

**Pricing rule:** Sponsorship price = 25-40% of total calculated value (sponsors expect 2.5-4x ROI)

### 6. Sponsor CRM pipeline

**Pipeline stages:**
| Stage | Actions | Timeline |
|---|---|---|
| **1. Prospect** | Research companies, identify budget holders, align with event audience | 6-12 months before |
| **2. Contacted** | Initial outreach (email + call), send teaser, request meeting | 5-8 months before |
| **3. Proposal Sent** | Send full sponsor deck, customized to their objectives | 4-6 months before |
| **4. Negotiating** | Discuss tier, benefits, customization, pricing | 3-5 months before |
| **5. Confirmed** | Signed contract, first payment received | 2-4 months before |
| **6. Fulfilling** | Collect assets, deliver benefits, coordinate activation | Ongoing until event |
| **7. Fulfilled** | All deliverables completed, ROI report sent | 1-4 weeks after |
| **8. Renewal** | Renewal conversation, next edition offer, multi-year proposal | 2-8 weeks after |

**Follow-up cadence:**
- After initial contact: follow-up in 5 business days
- After proposal sent: follow-up in 7 business days
- During negotiation: weekly touchpoints
- After confirmation: bi-weekly updates until 4 weeks out, then weekly
- Post-event: ROI report within 2 weeks, renewal conversation within 4 weeks

**Portuguese corporate decision cycles:**
- Large corporates (EDP, Galp, BCP, NOS): 3-6 month decision cycles, start 9-12 months before
- Medium companies: 1-3 month cycles, start 6 months before
- Startups / SMEs: 2-4 weeks, can close 2-3 months before
- Government / institutional: public procurement rules may apply, very long cycles
- Budget seasons: most Portuguese companies finalize annual budgets in Q4 (Oct-Dec), approach in Q3

### 7. Sponsor activation (beyond logos)

**High-impact activations:**
- **Branded experience zone:** interactive area with brand integration (photo booth, VR, demo station)
- **Content collaboration:** co-created panel, report, or white paper presented at event
- **Networking facilitator:** sponsor hosts structured networking (speed networking, roundtable)
- **App integration:** sponsor featured in event app (push notifications, gamification, banner)
- **Sampling / gifting:** sponsor product in event bags, coffee break, or dedicated sampling moment
- **Social media takeover:** sponsor controls event social for 1 day/session
- **Sustainability partnership:** sponsor funds carbon offset, waste reduction, or green initiative
- **Data partnership:** co-branded survey, industry report, or trend analysis

**Activation quality criteria:**
- Adds value to attendee experience (not just brand exposure)
- Natural fit with event theme and audience
- Measurable engagement (not just passive visibility)
- Shareable on social media (attendees amplify)
- Memorable and differentiating (not generic logo wall)

### 8. Fulfillment checklist

**Pre-event (4+ weeks before):**
- [ ] Collect high-res logo (vector + PNG, light + dark backgrounds)
- [ ] Collect brand guidelines (colors, fonts, prohibited uses)
- [ ] Confirm speaker/panelist names and bios
- [ ] Collect booth requirements (power, internet, furniture, branding dimensions)
- [ ] Share event app access and digital asset specs
- [ ] Confirm ticket allocation and names
- [ ] Confirm activation logistics and space allocation
- [ ] Share attendee demographics preview (RGPD compliant aggregate data)
- [ ] Brief sponsor on schedule, load-in, contacts

**During event:**
- [ ] Verify all logo placements (stage, print, digital, signage)
- [ ] Ensure booth is set up and functioning
- [ ] Facilitate speaking slot (AV check, timing, introduction)
- [ ] Capture photo/video evidence of all deliverables
- [ ] VIP management (reserved seating, backstage, meals)
- [ ] Social media posts as committed (tag sponsor)
- [ ] Manage activation logistics
- [ ] Collect lead capture data

**Post-event (within 2 weeks):**
- [ ] Compile and send photo/video assets of sponsor visibility
- [ ] Deliver analytics report (impressions, engagement, leads)
- [ ] Send attendee data (RGPD opt-in contacts only)
- [ ] Share media coverage clips and social mentions
- [ ] Send satisfaction survey to sponsor contact
- [ ] Schedule renewal conversation

### 9. Contract essentials

**Key clauses for Portuguese sponsorship contracts:**

1. **Parties:** Full legal names, NIF, registered addresses
2. **Event details:** Name, date, venue, expected attendance (with "minimum guarantee" if applicable)
3. **Sponsorship tier and price:** Clear tier name, total amount, IVA treatment
4. **Benefits deliverables:** Exhaustive list with specifications (logo size, post count, booth sqm)
5. **Exclusivity:** Category exclusivity definition (e.g., "sole telecommunications sponsor"), competitor list
6. **Payment schedule:** 50% on contract signature, 50% 30 days before event (or 100% upfront for <5,000 EUR)
7. **Material deadlines:** Logo delivery, speaker confirmation, booth specs — with consequences for late delivery
8. **Cancellation terms:** 
   - Sponsor cancels >60 days before: 50% refund
   - Sponsor cancels 30-60 days: 25% refund
   - Sponsor cancels <30 days: no refund
   - Organizer cancels: full refund + notification
9. **Force majeure:** Pandemic, natural disaster, government order — mutual release, good faith rescheduling
10. **IP usage:** Rights to use sponsor logo in marketing, rights for sponsor to use event branding
11. **Data protection (RGPD):** How attendee data is collected, shared, and processed
12. **Liability:** Indemnification, insurance requirements
13. **Governing law:** Portuguese law, jurisdiction of Lisbon/Porto courts

**IVA on sponsorship in Portugal:**
- Standard rate: 23% IVA on sponsorship fees
- Sponsorship is treated as "prestacao de servicos" for IVA purposes
- Sponsor can deduct IVA if they are IVA-registered and it relates to their business activity
- VIK (value in kind): must be valued at market rate, IVA applies on the imputed value
- Invoicing: organizer issues fatura with 23% IVA to sponsor

**Mecenato (cultural events):**
- Estatuto do Mecenato (DL 74/99, updated) — fiscal benefits for cultural/social patronage
- Corporate donors can deduct 120-140% of donation value from IRC taxable income (cultural events qualify for 130%)
- Requirements: event must have "relevante interesse cultural", organizer must be registered with IGAC or Ministry of Culture
- Not applicable to pure commercial sponsorship — must be structured as "donativo" not "patrocinio"
- Consult fiscal advisor for structuring

### 10. ROI report template

**Post-event ROI report structure:**
1. **Executive summary:** Key metrics, highlights, thank you
2. **Audience delivered:** Attendance vs. projected, demographic breakdown
3. **Visibility metrics:** Total impressions by channel, photo evidence
4. **Engagement metrics:** Social mentions, content views, booth traffic, app engagement
5. **Lead data:** Number of qualified leads delivered (with opt-in contacts if applicable)
6. **Media coverage:** Press clips, online articles, social reach of coverage
7. **Sponsor satisfaction survey results:** Organizer asks 5-8 questions post-event
8. **ROI calculation:** Investment vs. value delivered (media value, leads, brand exposure)
9. **Improvement suggestions:** Based on sponsor feedback
10. **Renewal offer:** Next edition pricing, early commitment discount (10-15%), multi-year option

## Output template

```markdown
---
project: <event-name>
date: <YYYY-MM-DD>
type: atlas-sponsorship-plan
event_date: <YYYY-MM-DD>
target_sponsorship_revenue: <EUR>
---

# Plano de Patrocinios — <Event Name>

## Resumo Executivo
| Parametro | Valor |
|---|---|
| Evento | <name> |
| Data | <date> |
| Assistencia prevista | <N> participantes |
| Receita-alvo patrocinios | <EUR> |
| # Patrocinadores-alvo | <N> |

## Audiencia e Valor para Patrocinadores
- **Perfil:** <industry, seniority, geography>
- **Alcance total estimado:** <impressions across channels>
- **Valor medio por lead:** <EUR>

## Estrutura de Tiers
| Tier | Preco EUR | # Disponiveis | Beneficios-chave |
|---|---|---|---|
| Title | ... | 1 | ... |
| Platinum | ... | 2 | ... |
| Gold | ... | 4 | ... |
| Silver | ... | 6 | ... |
| Bronze | ... | 10 | ... |
| Media Partner | VIK | 3 | ... |
| Categoria | ... | varies | ... |

## Matriz de Beneficios Detalhada
| Beneficio | Title | Platinum | Gold | Silver | Bronze |
|---|---|---|---|---|---|
| Logo no palco | ★★★ | ★★ | ★ | — | — |
| Speaking slot | Keynote | Painel | Workshop | — | — |
| Booth (m2) | 12m2 | 9m2 | 6m2 | 3m2 | — |
| Bilhetes | 20 | 12 | 8 | 4 | 2 |
| Social posts | 10 | 6 | 4 | 2 | 1 |
| Lead access | Full | Full | Partial | — | — |
| ... | ... | ... | ... | ... | ... |

## Valorizacao (Media Value)
| Touchpoint | Impressoes | CPM | Valor EUR |
|---|---|---|---|
| Palco / venue | ... | ... | ... |
| Website | ... | ... | ... |
| Email | ... | ... | ... |
| Social media | ... | ... | ... |
| Imprensa | ... | ... | ... |
| **Total** | **...** | | **EUR** |

## Pipeline de Prospeccao
| Empresa | Sector | Tier-alvo | Contacto | Status |
|---|---|---|---|---|
| ... | ... | ... | ... | Prospect |
| ... | ... | ... | ... | Contactado |

## Calendario de Activacao
| Momento | Accao Patrocinador | Responsavel |
|---|---|---|
| -8 semanas | Entrega logos e assets | Sponsor |
| -4 semanas | Confirmacao booth/speaker | Organizer |
| -1 semana | Load-in e setup | Both |
| Dia do evento | Activacao ao vivo | Both |
| +2 semanas | Relatorio ROI | Organizer |
| +4 semanas | Conversa renovacao | Organizer |

## Template Contrato
[Clausulas essenciais conforme seccao 9 do skill]

## IVA e Fiscalidade
- IVA aplicavel: 23% sobre fees de patrocinio
- Mecenato: <elegivel/nao elegivel> — justificacao
- Faturacao: organizer emite fatura ao patrocinador

## Proximos Passos
- [ ] Finalizar sponsor deck (PDF e apresentacao)
- [ ] Identificar 20-30 prospects por tier
- [ ] Iniciar outreach (email + LinkedIn + telefone)
- [ ] Preparar template de contrato com advogado
- [ ] Definir deadlines para material collection
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Plano Patrocinios ATLAS.md`

## Red Flags

- Never over-promise deliverables in the sponsor deck — promising 1,000 attendees when you have 300 confirmed destroys trust and kills renewal; always use conservative projections with clear "projected" vs. "confirmed" labels
- Never accept competitor sponsors in the same exclusivity tier without explicit waiver — category exclusivity is the #1 sponsor concern; placing Vodafone and NOS in the same tier without disclosure creates contractual liability
- Never skip the ROI report after the event — sponsors who receive no post-event report renew at <20%, vs. >60% when a detailed ROI report is delivered within 2 weeks
- Never rely on verbal agreements for sponsorship — Portuguese commercial law requires written proof for amounts >2,500 EUR; always formalize with a signed contract before listing the sponsor
- Never collect sponsor logos and materials last-minute — set hard deadlines 4+ weeks before the event; late materials mean poor print quality, missing digital assets, and unfulfilled promises
- Never confuse sponsorship (commercial exchange) with mecenato (donation) in contracts — the IVA and IRC treatment are fundamentally different; misclassification creates fiscal risk for both parties
- Never present sponsorship tiers without a clear benefits matrix — vague "premium visibility" means nothing; sponsors need specific, countable deliverables (# posts, booth sqm, # tickets, logo size)

## Interactions

- Follows `atlas-briefing` (event scope, audience) and `atlas-marketing` (reach projections)
- Feeds into `atlas-budget` (sponsorship revenue projections)
- Coordinates with `atlas-compliance` (contracts, IVA, ASAE if applicable)
- Coordinates with `atlas-staging` and `atlas-decor` (booth/stand placement, branded areas)
- Post-event feeds `atlas-post-event` (ROI report, renewal conversations)
- Pairs with `dario-proposal` for commercial proposal formatting
