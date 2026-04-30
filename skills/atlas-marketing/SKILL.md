---
name: atlas-marketing
description: Event marketing & promotion — multi-channel strategy, email sequences, social media calendar, pricing tiers, landing page optimization, and ticketing platform selection. Full 12-week marketing timeline from strategy to post-event recap. Portuguese market specifics including ASAE compliance, dominant channels, and local influencer landscape. Triggers on "marketing evento", "promover evento", "event marketing", "ticket sales", "bilhetes", "early bird", "divulgacao", "promocao evento", "campanha evento", "social media evento".
license: MIT
---

# ATLAS Skill — Event Marketing & Promotion

Produces a comprehensive event marketing plan covering the full promotional lifecycle: from 12 weeks pre-event through post-event recap. Designs channel strategy, email sequences, social media calendar, pricing tiers, and landing page structure optimized for conversion. Calculates marketing budget allocation and defines measurable KPIs for every phase.

## When to activate

Invoke `/atlas-marketing` (or trigger automatically) when:
- Planning promotion for a new event (conference, festival, gala, workshop)
- User asks "how do we sell more tickets" or "como promover o evento"
- User needs an email marketing sequence for an event
- User wants a social media content calendar for event promotion
- User needs pricing strategy (early bird, VIP, group discounts)
- User asks about ticketing platforms for Portugal
- After `atlas-briefing` defines the event scope and target audience

Do NOT use when:
- Event is internal with no external promotion needed
- User needs sponsor acquisition (use `atlas-sponsor`)
- User needs CRM/attendee management (use `atlas-crm`)

## Trigger phrases (PT/EN)

- "marketing do evento", "promover o evento", "campanha de divulgacao"
- "event marketing plan", "promote the event", "ticket sales strategy"
- "early bird pricing", "preco de lancamento", "bilhetes antecipados"
- "social media para o evento", "calendario de conteudo", "content calendar"
- "landing page do evento", "pagina de inscricao"
- "como vender mais bilhetes", "how to sell more tickets"

## Workflow

### 1. Gather marketing inputs

From `atlas-briefing` or user input:
- **Event type:** conference, festival, workshop, gala, corporate, community
- **Target audience:** demographics, psychographics, industry, geography
- **Capacity:** total seats/tickets available
- **Date:** event date (determines marketing timeline)
- **Budget:** total marketing budget (recommended 15-25% of total event budget)
- **Past data:** previous edition attendance, conversion rates, channel performance
- **Unique selling points:** speakers, venue, exclusivity, content, networking
- **Competitors:** similar events in the same market/period

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "event marketing promotion strategy launch timeline", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "email sequence event ticket sales conversion", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "social media content calendar event promotion", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "pricing strategy early bird urgency scarcity", collection: "dario", limit: 5)
```

### 3. Marketing timeline (12-week framework)

| Phase | Weeks Out | Focus | Key Actions |
|---|---|---|---|
| **Strategy & Branding** | 12-10 | Foundation | Brand identity, key messaging, visual assets, website/landing page build, ticketing setup, media kit |
| **Launch & Early Bird** | 8-6 | Awareness + First sales | Public announcement, early bird pricing live, email launch, PR outreach, social media campaign start, paid ads test |
| **Momentum & Social Proof** | 6-4 | Credibility + FOMO | Speaker announcements, testimonials, behind-the-scenes, partnership activations, retargeting ads, ambassador program |
| **Urgency** | 4-2 | Conversion push | Early bird deadline, scarcity messaging ("70% sold"), countdown content, final speaker reveals, group discount push |
| **Last Chance** | 2-1 | Final push | Last chance emails (3-5 in final week), urgency ads, influencer pushes, direct outreach to undecided leads |
| **Day-Of** | 0 | Live engagement | Live social coverage, Instagram Stories/Reels, LinkedIn posts, press coverage, attendee UGC encouragement |
| **Post-Event** | +1 to +4 | Retention + Next | Thank-you emails, highlight reel, survey, testimonial collection, content repurposing, save-the-date for next edition |

### 4. Channel strategy matrix

| Channel | Best For | Event Types | Budget % | Portuguese Notes |
|---|---|---|---|---|
| **Email marketing** | Highest ROI, segmented | All | 10-15% | Brevo/Mailchimp popular in PT, typical open rates 18-25% |
| **Instagram** | Visual, lifestyle, B2C | Festivals, galas, lifestyle | 15-20% | Dominant platform in PT for events, Reels outperform posts 3:1 |
| **LinkedIn** | Professional, B2B | Conferences, corporate, tech | 10-15% | Strong for PT corporate events, sponsored InMail for C-level |
| **Facebook** | Community, 35+ demographic | Community, cultural, local | 10-15% | Still strong in PT for 35+, Facebook Events drive discovery |
| **TikTok** | Gen Z, viral potential | Festivals, music, youth | 5-10% | Growing fast in PT, ideal for music/cultural events |
| **Google Ads** | Intent-based search | All (brand + category) | 15-20% | "eventos em Lisboa", "conferencia tecnologia Portugal" |
| **Meta Ads** | Targeting, retargeting | B2C events | 15-20% | Combine Instagram + Facebook, lookalike audiences from past attendees |
| **PR / Media** | Credibility, reach | Major events, launches | 5-10% | NIT, Time Out, Observador, Publico, Sapo Lifestyle, sector media |
| **Partnerships** | Cross-promotion, credibility | All | 0-5% (VIK) | Co-promotion with venues, associations, universities |
| **Influencers** | Awareness, trust | B2C, lifestyle, festivals | 5-15% | PT micro-influencers (5-50K): 150-500 EUR/post, macro (50-500K): 500-3,000 EUR |
| **Content marketing** | SEO, authority | Conferences, recurring | 5-10% | Blog posts, speaker interviews, industry insights |

### 5. Email sequence design

**Sequence 1 — Pre-launch nurture:**
1. Save-the-date (12 weeks) — date, city, 1-line teaser, "be the first to know" CTA
2. Early access invitation (10 weeks) — exclusive pre-sale for past attendees/subscribers

**Sequence 2 — Launch & early bird:**
3. Official launch (8 weeks) — full announcement, early bird pricing, keynote reveal
4. Speaker spotlight #1 (7 weeks) — feature keynote/headliner, value of their session
5. Agenda reveal (6 weeks) — full program, track highlights, "build your schedule"

**Sequence 3 — Social proof & momentum:**
6. Testimonial email (5 weeks) — past attendee stories, numbers ("87% rated 9+/10")
7. Speaker spotlight #2 (4 weeks) — panel/workshop leaders, new additions
8. Sponsor/partner announcement (4 weeks) — credibility through association

**Sequence 4 — Urgency & scarcity:**
9. Early bird deadline warning (3 weeks) — "Price increases in 7 days"
10. Early bird last call (2.5 weeks) — "48 hours left at this price"
11. Regular price + scarcity (2 weeks) — "Only 30% of tickets remaining"

**Sequence 5 — Final push:**
12. Last chance #1 (1 week) — final pricing, complete lineup, full value stack
13. Last chance #2 (3 days) — "Doors close soon", social proof recap
14. Final reminder (1 day) — "Tomorrow is the day. Are you in?"

**Sequence 6 — Logistics:**
15. Pre-event logistics (3 days) — venue, schedule, what to bring, parking, dress code

**Sequence 7 — Post-event:**
16. Thank-you + survey (24h after) — gratitude, feedback link, "your opinion shapes next year"
17. Content access (1 week after) — recordings, slides, photos, highlight reel
18. Save-the-date next edition (2-4 weeks after) — alumni pricing, early commitment

### 6. Social media content calendar structure

**Weekly cadence (active campaign phase):**
| Day | Instagram | LinkedIn | Facebook | TikTok |
|---|---|---|---|---|
| Mon | Speaker spotlight (carousel) | Industry insight post | Event update in groups | Behind-the-scenes clip |
| Tue | Behind-the-scenes (Story) | Speaker article share | — | — |
| Wed | Countdown/stat graphic | Agenda highlight | Community poll | Speaker intro (short) |
| Thu | Attendee testimonial | Networking value post | Event share/boost | Trending audio + event |
| Fri | Reel (venue/vibe teaser) | Week recap + CTA | — | — |
| Sat | UGC repost / poll (Story) | — | Community engagement | — |
| Sun | Countdown reminder | — | — | — |

**Hashtag strategy:**
- Event-specific: #NomeDoEvento2026 #NomeDoEventoLisboa
- Category: #EventosLisboa #ConferenciasPortugal #FestivaisPortugal
- Industry: #TechPortugal #MarketingDigitalPT (adapt to sector)
- Trending: leverage relevant trending hashtags when organic fit exists

### 7. Pricing strategy

| Tier | Timing | Discount | Purpose | Capacity Allocation |
|---|---|---|---|---|
| **Super Early Bird** | First 48-72h (flash) | 30-40% off | Reward loyal/fast movers, generate buzz | 5-10% of capacity |
| **Early Bird** | Weeks 8-3 before | 20-30% off | Build base attendance, cash flow | 15-20% of capacity |
| **Regular** | Weeks 3-1 before | Standard price | Main revenue tier | 40-50% of capacity |
| **Late / Door** | Final week + door | +10-20% premium | Urgency revenue, discourage waiting | 10-15% of capacity |
| **Group (10+)** | Anytime | 10-15% off regular | Corporate blocks, associations | No cap |
| **VIP / Premium** | Anytime | +50-100% over regular | Premium experience, higher margin | 10-15% of capacity |
| **Student / NGO** | Anytime | 40-60% off regular | Accessibility, goodwill | 5-10% of capacity |
| **Speaker / Media / Sponsor** | Comps | Free | Earned access | 5-10% of capacity |

**Portuguese pricing benchmarks (2026):**
- Workshop (half-day): 25-75 EUR
- Conference (full-day): 50-200 EUR
- Premium conference (2 days): 150-500 EUR
- Gala/dinner event: 75-250 EUR
- Festival (multi-day): 30-120 EUR/day
- Corporate summit: 200-1,000 EUR (often sponsor-subsidized)

### 8. Landing page structure (conversion-optimized)

1. **Hero section:** Event name, date, location, 1-line value prop, primary CTA ("Garantir Lugar" / "Get Tickets")
2. **Social proof bar:** "500+ attendees in 2025", sponsor logos, media mentions
3. **Speakers / Lineup:** Photos, names, titles, companies — top 4-6 above fold
4. **Value proposition:** 3-4 bullet points answering "Why attend?"
5. **Agenda overview:** Day structure, track highlights, key sessions
6. **Testimonials:** 3-4 past attendee quotes with photos and roles
7. **Venue:** Photo, map, transport info, nearby hotels
8. **Pricing table:** All tiers side-by-side, recommended tier highlighted
9. **FAQ:** 8-12 common questions (cancellation, dress code, parking, accessibility)
10. **Sponsors:** Logo grid with tier labels
11. **Final CTA:** Repeat pricing + urgency ("Only X spots remaining")
12. **Footer:** Organizer info, contact, social links, legal (RGPD, terms)

**Conversion optimization:**
- Sticky CTA button on mobile
- Countdown timer for early bird deadline
- Exit-intent popup with discount or lead magnet
- UTM tracking on all external links
- Pixel (Meta, Google) installed from day 1

### 9. Ticketing platforms (Portugal)

| Platform | Best For | Fees | Payout | Portuguese Notes |
|---|---|---|---|---|
| **Eventbrite** | General events, international | 6.95% + 0.79 EUR | 5-7 business days | Well known in PT, MBWay integration |
| **Bilhetica** | Portuguese events, local | 5-8% negotiable | Weekly payouts | PT-native, ASAE compliant, Multibanco/MBWay |
| **Ticketline** | Concerts, festivals, theatre | 10-15% (includes distribution) | Monthly | PT market leader for entertainment, physical POS network |
| **BOL (Bilheteira Online)** | Cultural events, venues | 8-12% | Monthly | Integrated with FNAC stores, strong PT brand |
| **Weezevent** | Free/low-cost events | Free for free events, 1.5% paid | 2-3 days | Good for association/community events |
| **Custom (WooCommerce/Stripe)** | Full control, brand | Stripe: 1.4% + 0.25 EUR | 2-7 days | Lower fees, requires development, ASAE compliance manual |

**ASAE requirements for ticket sales in Portugal:**
- Bilhetes must include: event name, date, time, venue, organizer, price (with IVA), unique serial number
- Reclamation book (Livro de Reclamacoes) must be available
- Consumer rights compliance (cancellation policy, refund terms)
- If selling food/drink: additional ASAE licensing required

### 10. Marketing budget allocation

| Category | % of Marketing Budget | Notes |
|---|---|---|
| Paid advertising (Meta + Google) | 30-40% | Highest variable, scale based on ROI |
| Content creation (design, video, copy) | 15-20% | Invest early, reuse across channels |
| Email platform & tools | 5-8% | Brevo/Mailchimp/HubSpot + landing page tool |
| PR & media outreach | 5-10% | Press releases, media partnerships |
| Influencer partnerships | 5-15% | Varies by event type, higher for B2C |
| Print materials (if applicable) | 3-5% | Flyers, posters, banners — decreasing importance |
| Ticketing platform fees | 5-10% | Factor into ticket pricing, not separate budget |
| Contingency | 5-10% | For opportunistic buys or underperforming channels |

**Rule of thumb:** Marketing budget = 15-25% of total event budget for ticketed events, 5-10% for sponsored/corporate events.

### 11. Metrics & KPIs

| Metric | Target | Measurement |
|---|---|---|
| Total registrations vs. capacity | >80% | Ticketing platform dashboard |
| Email open rate | >20% (PT average: 18%) | Email platform |
| Email click-through rate | >3% | Email platform |
| Landing page conversion rate | >5% (cold), >15% (warm) | Google Analytics / UTM |
| Cost per registration (paid) | <15% of ticket price | Ad platforms + ticketing |
| Social media engagement rate | >3% (Instagram), >1% (LinkedIn) | Native analytics |
| Early bird uptake | 20-30% of total sales | Ticketing platform |
| Referral/word-of-mouth % | >15% of registrations | "How did you hear" field |
| Day-of no-show rate | <15% (paid), <30% (free) | Check-in system |

## Output template

```markdown
---
project: <event-name>
date: <YYYY-MM-DD>
type: atlas-marketing-plan
event_date: <YYYY-MM-DD>
capacity: <number>
marketing_budget: <EUR>
---

# Plano de Marketing — <Event Name>

## Resumo Executivo
| Parametro | Valor |
|---|---|
| Evento | <name> |
| Data | <date> |
| Local | <venue, city> |
| Capacidade | <N> lugares |
| Budget marketing | <EUR> |
| Objectivo registos | <N> (<% da capacidade>) |

## Publico-Alvo
- **Primario:** <demographics + psychographics>
- **Secundario:** <demographics + psychographics>
- **Terciario:** <demographics + psychographics>

## Timeline de Marketing (12 semanas)
| Fase | Semanas | Acoes-chave | Responsavel |
|---|---|---|---|
| Estrategia | 12-10 | ... | ... |
| Lancamento | 8-6 | ... | ... |
| Momentum | 6-4 | ... | ... |
| Urgencia | 4-2 | ... | ... |
| Last chance | 2-0 | ... | ... |
| Pos-evento | +1 a +4 | ... | ... |

## Estrategia de Canais
| Canal | Objectivo | Budget | KPI |
|---|---|---|---|
| Email | ... | EUR | Open rate >20% |
| Instagram | ... | EUR | Engagement >3% |
| LinkedIn | ... | EUR | CTR >1% |
| Meta Ads | ... | EUR | CPA <X EUR |
| Google Ads | ... | EUR | CPA <X EUR |
| PR/Media | ... | EUR | X mencoes |

## Sequencia de Emails
| # | Assunto | Timing | Objectivo |
|---|---|---|---|
| 1 | Save the date | 12 sem | Awareness |
| ... | ... | ... | ... |

## Calendario Social Media (semana-tipo)
| Dia | Instagram | LinkedIn | Facebook |
|---|---|---|---|
| Seg | ... | ... | ... |
| ... | ... | ... | ... |

## Estrategia de Precos
| Tier | Preco | Desconto | Periodo | Alocacao |
|---|---|---|---|---|
| Super Early Bird | EUR | -35% | Primeiras 48h | 5% |
| Early Bird | EUR | -25% | Sem 8-3 | 20% |
| Regular | EUR | — | Sem 3-1 | 45% |
| Late/Porta | EUR | +15% | Ultima semana | 10% |
| VIP | EUR | +75% | Sempre | 10% |
| Grupo 10+ | EUR | -12% | Sempre | — |
| Estudante | EUR | -50% | Sempre | 5% |

## Plataforma de Ticketing
- **Recomendacao:** <platform>
- **Justificacao:** <why>
- **Metodos pagamento:** Multibanco, MBWay, Visa/MC, PayPal

## Landing Page — Wireframe
1. Hero: ...
2. Social proof: ...
3. Speakers: ...
...

## KPIs e Metricas
| Metrica | Target | Ferramenta |
|---|---|---|
| Registos totais | X | Ticketing |
| Taxa conversao LP | >X% | GA4 |
| ... | ... | ... |

## Orcamento Marketing Detalhado
| Rubrica | Valor EUR | % do total |
|---|---|---|
| Paid ads | ... | ...% |
| Conteudo | ... | ...% |
| ... | ... | ... |
| **Total** | **EUR** | **100%** |

## Proximos Passos
- [ ] Finalizar branding e assets visuais
- [ ] Configurar plataforma de ticketing
- [ ] Construir landing page
- [ ] Configurar pixels e tracking (Meta, Google, UTM)
- [ ] Preparar sequencia de emails
- [ ] Lancar campanha Early Bird
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Plano Marketing ATLAS.md`

## Red Flags

- Never launch marketing less than 4 weeks before the event — the promotional cycle needs time to build awareness, create urgency, and convert; compressing it means relying on luck instead of strategy
- Never rely on a single marketing channel — if Instagram goes down, ads get rejected, or email deliverability drops, you lose 100% of your pipeline; always maintain 3+ active channels
- Never skip UTM tracking on external links — without attribution data, you cannot measure channel ROI, optimize spend, or learn for the next edition
- Never launch without content assets ready (photos, copy, videos) — starting promotion with placeholder content signals amateur production and kills first impressions
- Never ignore ASAE ticket sale requirements in Portugal — non-compliance can result in fines up to 44,000 EUR and event shutdown
- Never set early bird pricing without a firm deadline and capacity cap — "early bird forever" destroys urgency and trains the audience to never pay full price
- Never send undifferentiated email blasts to your entire list — segment by past attendance, engagement level, and ticket tier for 2-3x higher conversion

## Interactions

- Follows `atlas-briefing` (event scope, audience, objectives)
- Feeds into `atlas-sponsor` (marketing reach data for sponsor decks)
- Feeds into `atlas-crm` (attendee data from registration)
- Coordinates with `atlas-budget` (marketing spend allocation)
- Coordinates with `atlas-timeline` (marketing milestones in master timeline)
- Post-event data feeds `atlas-post-event` (survey, recap content)
