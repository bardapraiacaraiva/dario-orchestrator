---
name: atlas-crm
description: Attendee CRM & follow-up — database design, segmentation, pre-event nurture, during-event engagement tracking, post-event follow-up sequences, retention/loyalty programs, win-back campaigns, automation workflows, RGPD compliance, and Portuguese data protection (CNPD). Full attendee lifecycle from first touchpoint to repeat attendance. Triggers on "CRM evento", "attendee management", "follow-up", "participantes", "base de dados evento", "retencao participantes", "RGPD evento", "email pos-evento", "survey evento", "loyalty evento".
license: MIT
---

# ATLAS Skill — Attendee CRM & Follow-Up

Manages the complete attendee lifecycle: from first registration through post-event follow-up, retention, and re-engagement for future editions. Designs CRM database architecture, segmentation strategies, automated email workflows, engagement scoring, and RGPD-compliant data management. Optimized for the Portuguese market with CNPD requirements and local communication preferences.

## When to activate

Invoke `/atlas-crm` (or trigger automatically) when:
- User needs to design an attendee database or CRM structure
- User asks "how to follow up after the event" or "como contactar participantes"
- User needs post-event email sequences (thank-you, survey, content)
- User wants attendee segmentation for targeted communication
- User needs a loyalty/retention program for recurring events
- User asks about RGPD compliance for event attendee data
- User needs to re-engage lapsed attendees from previous editions
- After registration data starts flowing from `atlas-marketing`

Do NOT use when:
- User needs sponsor relationship management (use `atlas-sponsor`)
- User needs general event marketing (use `atlas-marketing`)
- User needs guest protocol/VIP management (use `atlas-guest`)

## Trigger phrases (PT/EN)

- "CRM para o evento", "base de dados participantes", "attendee database"
- "follow-up pos-evento", "post-event follow-up", "email de agradecimento"
- "segmentacao participantes", "attendee segmentation"
- "retencao de participantes", "retention rate", "loyalty program"
- "RGPD evento", "protecao dados evento", "data protection event"
- "survey pos-evento", "inquerito de satisfacao", "NPS evento"
- "re-engagement", "win-back", "participantes inativos"
- "automacao emails evento", "email automation workflows"

## Workflow

### 1. Gather CRM inputs

From `atlas-briefing`, `atlas-marketing`, and registration data:
- **Event type:** one-off vs. recurring (series), public vs. corporate, free vs. paid
- **Expected volume:** number of attendees (determines tool selection)
- **Data sources:** registration platform, event app, check-in system, social media
- **Existing data:** past edition attendee lists, newsletter subscribers, CRM contacts
- **Communication channels:** email, WhatsApp, SMS, app push, social DM
- **Team capacity:** who manages communications (dedicated person vs. organizer)
- **Goals:** retention rate target, NPS target, repeat attendance rate

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "CRM attendee lifecycle segmentation engagement", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "email automation workflow post-event follow-up", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "RGPD GDPR event data consent management Portugal", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "customer retention loyalty NPS survey", collection: "dario", limit: 5)
```

### 3. CRM database architecture

**Core attendee profile fields:**

| Category | Fields | Source |
|---|---|---|
| **Identity** | Name, email, phone, company, title, NIF (if B2B) | Registration form |
| **Demographics** | Age range, gender, location, language, industry | Registration + survey |
| **Event history** | Events attended (list), dates, ticket tiers, spend total | Transaction records |
| **Engagement** | Sessions attended, networking connections, app usage, survey responses | Event app + check-in |
| **Communication** | Email opens, clicks, unsubscribes, preferred channel, timezone | Email platform |
| **Scores** | Engagement score (0-100), NPS (0-10), lifetime value (EUR), churn risk (low/med/high) | Calculated |
| **Consent** | RGPD consent date, consent type (marketing, data sharing, profiling), opt-out date | Consent management |
| **Preferences** | Topics of interest, dietary restrictions, accessibility needs, networking preferences | Registration + survey |
| **Tags** | VIP, speaker, sponsor guest, media, student, alumni, first-timer | Manual + automated |

**Engagement score formula (0-100):**
- Events attended in last 24 months: 0-20 pts (5 pts per event, max 20)
- Email engagement (opens + clicks): 0-15 pts
- Session attendance rate (attended/available): 0-15 pts
- Social media engagement with event: 0-10 pts
- Survey completion: 0-10 pts
- Networking activity (app connections, meetings): 0-10 pts
- Referrals (brought others): 0-10 pts
- Recency (months since last event): 0-10 pts (10 = <3 months, 5 = 3-12 months, 0 = >12 months)

### 4. Segmentation strategy

**Primary segments:**

| Segment | Definition | Communication Strategy |
|---|---|---|
| **VIP / High-Value** | Engagement score >80, attended 3+ events, or premium ticket holders | Personalized outreach, early access, exclusive content, phone/WhatsApp |
| **Regulars** | Attended 2+ events, engagement 50-80 | Loyalty recognition, segment-specific content, early bird priority |
| **First-Timers** | Attended 1 event, engagement <50 | Welcome nurture, highlight community, remove friction for return |
| **Prospects** | Registered but never attended (no-shows) or newsletter-only | Re-engagement, social proof, low-barrier offers |
| **Lapsed** | Attended previously but not in last 12+ months | Win-back campaign, "we miss you", what's changed |
| **Corporate Groups** | Company sent 3+ employees | Account-based approach, corporate packages, decision-maker relationship |
| **Speakers / Contributors** | Past/current speakers, moderators, workshop leaders | Community cultivation, co-creation, advisory board |
| **Sponsor Guests** | Attendees who came via sponsor | Share with sponsor (RGPD compliant), nurture to organic next time |

**Secondary segmentation dimensions:**
- By industry (tech, finance, health, creative, etc.)
- By geography (Lisboa, Porto, other PT, international)
- By ticket tier (free, standard, premium, VIP)
- By topic interest (tagged from session attendance)
- By feedback score (promoters NPS 9-10, passives 7-8, detractors 0-6)

### 5. Pre-event nurture sequence

**For registered attendees (after ticket purchase/registration):**

| # | Email | Timing | Content | Goal |
|---|---|---|---|---|
| 1 | Welcome & confirmation | Immediate | Ticket confirmation, what to expect, save calendar, share on social | Confirmation + excitement |
| 2 | Community invitation | +2 days | WhatsApp group / LinkedIn group / event app download | Community building |
| 3 | Speaker spotlight | -3 weeks | Featured speakers, session previews, "build your schedule" | Value reinforcement |
| 4 | Networking prep | -2 weeks | Attendee list preview (opt-in), networking tips, meeting booking tool | Networking value |
| 5 | Logistics email | -3 days | Venue map, schedule, transport, parking, dress code, what to bring | Reduce friction |
| 6 | Eve-of reminder | -1 day | "See you tomorrow!", final schedule, check-in instructions, excitement | Reduce no-shows |

**For free events (no-show reduction — critical):**
- Add SMS/WhatsApp reminder at -1 day and morning-of
- Include social commitment device ("tell a friend you're going")
- Emphasize limited capacity to create accountability

### 6. During-event engagement tracking

**Touchpoints to capture:**
| Touchpoint | How to Track | Data Captured |
|---|---|---|
| Check-in | QR code scan, badge scan, manual | Arrival time, attendance confirmed |
| Session attendance | Room sensors, app check-in, manual count | Which sessions, duration |
| Networking | App connections, badge scan exchanges | Who connected with whom |
| Booth visits | Badge scan at sponsor booths | Sponsor interest |
| F&B preferences | Meal selection, dietary requests | Dietary profile |
| Live polls / Q&A | Event app, Slido, Mentimeter | Topic engagement |
| Social media | Hashtag monitoring, UGC | Social amplification |
| Feedback (real-time) | NPS pulse mid-event, emoji reactions | Real-time sentiment |

**Tools for during-event tracking:**
- Event app: Whova, Swapcard, Grip, Brella (all popular in PT corporate events)
- Check-in: Eventbrite check-in, custom QR system, Bizzabo
- Engagement: Slido (polls, Q&A), Mentimeter, Pigeonhole Live
- Badge scanning: Boomset, vFairs Lead Capture, Zuant

### 7. Post-event follow-up sequence

**Critical timing — the 48-hour rule: first follow-up must go within 24-48h while memory is fresh.**

| # | Email | Timing | Content | Goal |
|---|---|---|---|---|
| 1 | Thank you | +24h | Gratitude, event highlights, 1 great photo, survey link, "save the date" hint | Warm feeling + survey |
| 2 | Survey + NPS | +48h | Dedicated survey email (5-8 min, not longer), incentive (early access next edition, raffle) | Feedback collection |
| 3 | Content access | +1 week | Recordings, slides, photos, speaker decks (if applicable) | Extended value |
| 4 | Highlight reel | +2 weeks | Best photos, video recap, social media highlights, attendee testimonials | Social proof for next |
| 5 | Community invitation | +3 weeks | Year-round community (newsletter, WhatsApp, meetups, online events) | Retain connection |
| 6 | Next edition save-the-date | +4-6 weeks | Date announcement, alumni pricing (10-15% off), "lock in your spot" | Early commitment |

**Survey design (Portuguese context):**
- Keep under 8 minutes (Portuguese respondents drop off sharply after 5 min)
- Incentivize: prize draw (iPad, event tickets), exclusive content, alumni discount
- NPS question first: "De 0 a 10, qual a probabilidade de recomendar este evento a um colega?"
- Include: overall satisfaction, specific session ratings, logistics, networking value, suggestions
- Open-ended: "O que mais gostou?" and "O que melhoraria?" (exactly 2 open questions, no more)
- Expected response rate in Portugal: 15-25% (vs 30-40% in Northern Europe) — incentivize aggressively
- Send reminder to non-respondents after 5 days

### 8. Retention & loyalty strategy

**For recurring events (series, annual, quarterly):**

**Loyalty tiers:**
| Tier | Criteria | Benefits |
|---|---|---|
| **Alumnus** | Attended 1 event | 10% early bird discount, content access |
| **Regular** | Attended 2-3 events | 15% discount, priority registration, alumni networking group |
| **Ambassador** | Attended 4+ events OR referred 3+ people | 20% discount, free upgrade to VIP, speaker consideration, advisory input |
| **Lifetime** | Attended 6+ events OR exceptional contribution | Permanent VIP, complimentary ticket, brand ambassador partnership |

**Year-round engagement (between events):**
- Monthly newsletter with industry insights (not just event promotion)
- Quarterly online webinars/meetups (maintain community)
- Exclusive content (interviews with past speakers, trend reports)
- Community platform (WhatsApp group, LinkedIn group, Slack/Discord)
- Early access to speaker/agenda announcements
- Birthday/anniversary touches (automate via CRM)

### 9. Win-back campaigns (lapsed attendees)

**Trigger:** Attended a previous edition but did not register for the latest or next.

**Win-back sequence (3 emails + 1 alternative channel):**

| # | Subject (PT example) | Content | Timing |
|---|---|---|---|
| 1 | "Sentimos a sua falta no [Evento]" | Recap of what they missed, highlights, testimonials from the edition they skipped | 2 weeks after event they missed |
| 2 | "O que mudou desde a ultima vez" | New features, speakers, format improvements based on feedback, personal invitation | +2 weeks |
| 3 | "Oferta especial para alumni" | Exclusive discount (15-20%), limited time, "last chance to re-join the community" | +2 weeks |
| 4 | WhatsApp/LinkedIn DM | Personal message from organizer (for high-value lapsed) | +1 week after email 3 |

**Win-back analysis:**
- If lapsed gave negative feedback: address specific issues in win-back messaging
- If lapsed had scheduling conflict: offer flexible options (recordings, virtual attendance)
- If lapsed chose competitor event: analyze differentiators, highlight improvements

### 10. Automation workflows

**Recommended tools (Portugal-compatible):**

| Tool | Best For | Price Range | Portuguese Notes |
|---|---|---|---|
| **Brevo (ex-Sendinblue)** | SMEs, multi-channel (email+SMS+WhatsApp) | Free-49 EUR/mo | EU-based (France), RGPD native, WhatsApp API, Portuguese UI |
| **Mailchimp** | Small events, simple automation | Free-350 EUR/mo | Well known, limited automation on free tier |
| **ActiveCampaign** | Advanced automation, CRM integration | 29-259 EUR/mo | Powerful automations, good for complex sequences |
| **HubSpot** | Full CRM + marketing, B2B events | Free-800 EUR/mo | Overkill for small events, excellent for conference series |
| **ConvertKit** | Creator/community events | 29-79 EUR/mo | Simple, tag-based, good for newsletter-driven events |

**Key automation triggers:**
- Registration completed → Welcome sequence starts
- No email open in 3 emails → Switch to secondary channel (WhatsApp/SMS)
- Survey completed with NPS 9-10 → Trigger referral request
- Survey completed with NPS 0-6 → Trigger personal follow-up from organizer
- 30 days before event → Logistics email sequence starts
- No check-in on event day → No-show follow-up (send recording access)
- Engagement score drops below 30 → Win-back sequence triggers
- Attendee refers 3+ people → Upgrade to Ambassador tier

### 11. Analytics & KPIs

| Metric | Definition | Target | Frequency |
|---|---|---|---|
| **NPS (Net Promoter Score)** | % Promoters - % Detractors | >50 (good), >70 (excellent) | Per event |
| **Retention rate** | % attendees who return for next edition | >40% (annual), >60% (quarterly) | Per edition |
| **Attendee Lifetime Value (ALV)** | Total spend per attendee across all events | Growing YoY | Annually |
| **Email open rate** | Unique opens / delivered | >20% | Per campaign |
| **Survey response rate** | Surveys completed / surveys sent | >20% (with incentive) | Per event |
| **No-show rate** | Registered but didn't attend / total registered | <15% (paid), <30% (free) | Per event |
| **Referral rate** | % registrations from referrals | >15% | Per event |
| **Churn rate** | % of past attendees who don't return | <60% (annual), <40% (quarterly) | Per edition |
| **Cost per attendee (marketing)** | Total marketing spend / attendees acquired | Decreasing over editions | Per event |
| **First-timer conversion** | % first-timers who return for second event | >30% | Per edition pair |

### 12. RGPD compliance (critical for Portugal)

**Legal basis for processing:**
| Data Use | Legal Basis | Notes |
|---|---|---|
| Event registration | Contract execution (Art. 6(1)(b)) | Necessary to deliver the service they purchased |
| Post-event survey | Legitimate interest (Art. 6(1)(f)) | Document in DPIA, provide opt-out |
| Marketing emails (future events) | Consent (Art. 6(1)(a)) | Explicit opt-in at registration, easy unsubscribe |
| Sharing data with sponsors | Consent (Art. 6(1)(a)) | Separate, explicit consent — NEVER bundle with registration |
| Photography/video at event | Legitimate interest + signage | Post visible signs, provide opt-out wristband option |
| Badge scanning (lead capture) | Consent (Art. 6(1)(a)) | Attendee must actively participate (scan badge) |

**RGPD checklist for events:**
- [ ] Privacy policy on registration page (link, not just checkbox)
- [ ] Separate consent checkboxes: (1) event communications, (2) partner/sponsor communications, (3) profiling
- [ ] Cookie consent banner on event website (Cookiebot, OneTrust, or similar)
- [ ] Data retention policy: delete personal data 24 months after last interaction (or shorter)
- [ ] Right to erasure workflow: process within 30 days, document procedure
- [ ] Data portability: ability to export attendee's data in machine-readable format
- [ ] Breach notification: 72h notification to CNPD (Comissao Nacional de Protecao de Dados)
- [ ] DPO designation: required if processing data of >5,000 attendees regularly
- [ ] DPIA (Data Protection Impact Assessment): required for large-scale events with profiling
- [ ] Subprocessor agreements: with email platform, ticketing platform, event app vendor
- [ ] CCTV signage at venue (if applicable)
- [ ] Photo/video consent: visible signage at entry, optional "no photo" wristbands

**Portuguese specifics (CNPD):**
- CNPD (Comissao Nacional de Protecao de Dados) is the Portuguese supervisory authority
- Lei 58/2019 implements RGPD in Portuguese law with some national specifics
- Direct marketing via electronic means requires prior explicit consent (Lei 41/2004 — e-Privacy)
- CNPD fines can reach 20M EUR or 4% of global turnover (as per RGPD)
- Portuguese consumers are increasingly RGPD-aware — transparent data practices build trust
- WhatsApp for business communications requires opt-in (WhatsApp Business API terms + RGPD)

### 13. Data integration architecture

**Data flow between systems:**
```
Registration Platform (Eventbrite/custom)
    ↓ [webhook / API sync]
CRM (HubSpot/ActiveCampaign/Brevo)
    ↓ [automation triggers]
Email Platform (if separate)
    ↓ [engagement data]
Event App (Whova/Swapcard)
    ↓ [session + networking data]
Survey Tool (Typeform/Google Forms)
    ↓ [feedback data]
Analytics Dashboard (Google Sheets / Looker Studio / Power BI)
```

**Integration best practices:**
- Single source of truth: CRM holds the master attendee record
- Real-time sync: webhooks for registration, daily batch for engagement data
- Deduplication: match on email address (primary key), merge duplicates
- Data enrichment: LinkedIn profile, company data (for B2B events)
- Export-ready: all systems must support CSV/API export for portability

## Output template

```markdown
---
project: <event-name>
date: <YYYY-MM-DD>
type: atlas-crm-plan
event_date: <YYYY-MM-DD>
expected_attendees: <number>
---

# Plano CRM & Follow-Up — <Event Name>

## Resumo
| Parametro | Valor |
|---|---|
| Evento | <name> |
| Participantes esperados | <N> |
| Edicoes anteriores | <N> (se aplicavel) |
| Taxa retencao actual | <X%> (se aplicavel) |
| NPS objectivo | >X |

## Arquitectura CRM
- **Ferramenta:** <Brevo/HubSpot/ActiveCampaign>
- **Campos core:** [lista dos campos essenciais]
- **Integracao:** Registration ↔ CRM ↔ Email ↔ Event App

## Segmentacao
| Segmento | Criterio | Tamanho estimado | Estrategia |
|---|---|---|---|
| VIP | Engagement >80 | X | Outreach pessoal |
| Regulars | 2+ eventos | X | Loyalty program |
| First-timers | 1 evento | X | Nurture + welcome |
| Lapsed | >12m sem evento | X | Win-back |

## Sequencia Pre-Evento
| # | Email | Timing | Objectivo |
|---|---|---|---|
| 1 | Welcome | Imediato | Confirmacao |
| ... | ... | ... | ... |

## Sequencia Pos-Evento
| # | Email | Timing | Objectivo |
|---|---|---|---|
| 1 | Obrigado + survey | +24h | Feedback |
| ... | ... | ... | ... |

## Programa de Fidelizacao
| Tier | Criterio | Beneficios |
|---|---|---|
| Alumnus | 1 evento | 10% desconto |
| ... | ... | ... |

## Campanha Win-Back
| # | Mensagem | Timing | Canal |
|---|---|---|---|
| 1 | Sentimos a sua falta | +2 sem | Email |
| ... | ... | ... | ... |

## Automacoes
| Trigger | Accao | Ferramenta |
|---|---|---|
| Registo completo | Welcome sequence | Brevo |
| NPS 9-10 | Pedido referral | Brevo |
| ... | ... | ... |

## KPIs
| Metrica | Target | Medicao |
|---|---|---|
| NPS | >50 | Survey |
| Retencao | >40% | CRM |
| ... | ... | ... |

## RGPD Compliance
- [ ] Politica privacidade na pagina de registo
- [ ] Consentimentos separados (evento, marketing, parceiros)
- [ ] Processo de eliminacao de dados (<30 dias)
- [ ] Acordo subprocessadores com todas as plataformas
- [ ] Sinalética CCTV e fotografia no evento

## Proximos Passos
- [ ] Selecionar e configurar CRM
- [ ] Importar dados de edicoes anteriores
- [ ] Criar templates de email (welcome, follow-up, survey)
- [ ] Configurar automacoes
- [ ] Definir processo RGPD com DPO
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Plano CRM ATLAS.md`

## Red Flags

- Never send the first post-event follow-up more than 48h after the event — after 48 hours, attendee memory fades, emotional peak is lost, and survey response rates drop by 50%+
- Never share attendee data with sponsors without separate, explicit RGPD consent — bundling data-sharing consent with registration violates RGPD and exposes the organizer to CNPD fines
- Never send undifferentiated bulk emails to the entire attendee list — first-timers, VIPs, and lapsed attendees need fundamentally different messages; one-size-fits-all feels impersonal and increases unsubscribes
- Never manage attendee data in spreadsheets for events with >200 participants — manual processes create RGPD compliance gaps, data duplication, and make automation impossible
- Never skip the NPS question in the post-event survey — without NPS trending, you cannot measure event health over time or identify declining satisfaction before it becomes churn
- Never ignore no-show data — high no-show rates (>20% for paid, >40% for free) indicate a funnel problem, pricing problem, or communication failure that must be diagnosed
- Never retain attendee personal data indefinitely — Portuguese RGPD implementation (Lei 58/2019) requires defined retention periods; 24 months after last interaction is a reasonable maximum for event CRM data

## Interactions

- Follows `atlas-marketing` (registration data flows into CRM)
- Follows `atlas-briefing` (event audience definition)
- Coordinates with `atlas-sponsor` (RGPD-compliant lead sharing with sponsors)
- Coordinates with `atlas-compliance` (RGPD, CNPD requirements)
- Feeds into `atlas-post-event` (survey data, NPS, retention metrics)
- Pairs with `dario-email-seq` for advanced email copywriting
- Pairs with `dario-support` for attendee communication templates


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-crm** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-crm:**

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
