---
name: atlas-post-event
description: Post-event analysis, debrief, and reporting. Structured debrief (went well / didn't / improve), attendee survey design (NPS, CSAT), metrics dashboard, ROI report, vendor scorecard, photo/video asset management, thank-you communications, knowledge base update, and stakeholder executive summary. Triggers on "pos-evento", "debrief evento", "post-event", "avaliacao evento", "relatorio evento", "event report", "what went well", "vendor review", "survey evento".
license: MIT
---

# ATLAS Skill — Post-Event Analysis & Debrief

Transforms event outcomes into structured insights, measurable results, and actionable improvements. Covers the full post-event cycle from immediate thank-yous through financial reconciliation to the final stakeholder report. Every event should leave the organization smarter — this skill ensures learnings are captured, documented, and applied to future events.

## When to activate

Invoke `/atlas-post-event` (or trigger automatically) when:
- User says "o evento acabou, e agora?" or "preciso do relatorio"
- User needs to send post-event surveys
- User needs to debrief with the team
- User needs a financial reconciliation (budget vs. actual)
- User wants to evaluate vendor performance
- User needs a stakeholder/board report on event results
- Within 24-48 hours of event conclusion (time-sensitive)

Do NOT use when:
- Event has not happened yet (use `atlas-timeline` or `atlas-checklist`)
- User is planning a new event (use `atlas-briefing`)

## Workflow

### 1. Post-event timeline (critical — time-sensitive actions)

| Timeframe | Action | Priority | Owner |
|---|---|---|---|
| **Day 0 (event day)** | Issue log compiled, initial team debrief (15min hot wash) | Critical | Event Director |
| **Within 24 hours** | Thank-you emails: speakers, VIPs, sponsors | Critical | Event Director |
| **Within 24 hours** | Social media: thank-you posts, best photos, key stats | High | Marketing |
| **Within 48 hours** | Attendee survey sent (NPS + feedback) | Critical | Event Coordinator |
| **Within 48 hours** | Vendor thank-yous sent | High | Event Coordinator |
| **Within 72 hours** | Speaker/sponsor thank-yous with photos/highlights | High | Event Director |
| **Within 1 week** | Full team debrief meeting (60-90 min structured) | Critical | Event Director |
| **Within 1 week** | Photo delivery from photographer (preview set) | High | Event Coordinator |
| **Within 2 weeks** | Survey results compiled and analyzed | High | Event Coordinator |
| **Within 2 weeks** | Financial reconciliation (budget vs. actual) | Critical | Finance/Event Dir |
| **Within 2 weeks** | Full photo delivery + video rough cut | Medium | Event Coordinator |
| **Within 3 weeks** | Vendor scorecards completed | High | Event Coordinator |
| **Within 1 month** | Final stakeholder report with ROI | Critical | Event Director |
| **Within 1 month** | Final edited video / aftermovie delivered | Medium | Event Coordinator |
| **Within 1 month** | Knowledge base updated (templates, checklists, lessons) | High | Event Director |

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "post-event analysis debrief report template", limit: 5)
mcp__dario-rag__search_kb(query: "event NPS survey questions feedback attendee satisfaction", limit: 5)
```

### 3. Structured debrief framework
Use this 5-section framework for the team debrief meeting:

#### Section 1: What went well (Celebrate)
- Top 3-5 successes with specific examples
- Staff/vendor who went above and beyond (name them)
- Attendee compliments received (verbatim quotes)
- Moments that exceeded expectations
- Systems/processes that worked flawlessly

#### Section 2: What didn't go well (Acknowledge)
- Issues that occurred and their impact (severity: low/medium/high)
- Root cause for each issue (not blame — systemic analysis)
- Was the issue foreseeable? Was it in the risk register?
- Impact on attendee experience (visible to guests or internal only?)

#### Section 3: What to improve (Action)
- Specific, actionable improvements for each issue identified
- Process changes needed (update checklists, timelines, contracts)
- Training needs identified (staff skills gaps)
- Vendor changes needed (replace, renegotiate, add backup)
- Technology improvements (registration, AV, communications)

#### Section 4: Key metrics review (Measure)
- Compare every KPI from `atlas-briefing` against actual results
- Budget variance analysis from `atlas-budget`
- Timeline adherence: did run-of-show hold? Where did it slip?
- Attendance: registered vs. showed vs. target

#### Section 5: Recommendations (Forward-looking)
- Should this event be repeated? With what changes?
- Optimal date/venue for next edition
- Budget recommendation for next edition (same, more, less, and why)
- Scale recommendation (grow, maintain, focus)

### 4. Attendee survey design
Send within 48 hours while the experience is fresh. Keep to 5 minutes max completion time.

#### Core questions (always include)
1. **NPS:** "On a scale of 0-10, how likely are you to recommend this event to a colleague/friend?" (0-10 scale)
2. **Overall satisfaction:** "How satisfied were you with the event overall?" (1-5 stars)
3. **Content quality:** "How would you rate the quality of the content/program?" (1-5 stars)
4. **Logistics:** "How would you rate the venue, catering, and organization?" (1-5 stars)
5. **Value for money:** "Did the event deliver good value?" (if ticketed) (1-5 stars)
6. **Return intent:** "Would you attend this event again?" (Definitely yes / Probably yes / Unsure / Probably no / Definitely no)
7. **Best part:** "What was the best part of the event?" (open text)
8. **Improvement:** "What one thing would you improve?" (open text)

#### Optional questions (by event type)
- **Conference:** Rate each speaker/session (1-5), "Which topic would you like to see next time?"
- **Networking:** "Did you make valuable connections?" (yes/no), "How many new contacts?"
- **Product launch:** "Are you more likely to purchase after attending?" (1-5)
- **Workshop:** "Can you apply what you learned?" (1-5), "What skills would you like next?"
- **Social/Wedding:** "What was the highlight of the evening?" "Rate: food, music, atmosphere" (1-5 each)

#### Survey tools (Portuguese market)
- Google Forms (free, simple, integrates with Sheets)
- Typeform (premium UX, conditional logic, 25 EUR/mo)
- SurveyMonkey (robust analysis, 30 EUR/mo)
- Eventbrite post-event survey (if ticketed via Eventbrite)
- Custom email with embedded 1-click NPS

### 5. Metrics dashboard

| Metric | Target | Actual | % Achievement | RAG |
|---|---|---|---|---|
| **Attendance** | | | | |
| Registered | X | X | X% | G/A/R |
| Showed up (show rate) | X (80%+) | X | X% | G/A/R |
| No-show rate | <20% | X% | | G/A/R |
| **Engagement** | | | | |
| NPS score | >50 | X | | G/A/R |
| Overall satisfaction (CSAT) | >4.0/5 | X | | G/A/R |
| Content rating | >4.0/5 | X | | G/A/R |
| Logistics rating | >4.0/5 | X | | G/A/R |
| Survey response rate | >30% | X% | | G/A/R |
| **Financial** | | | | |
| Total revenue | X EUR | X EUR | X% | G/A/R |
| Total cost | X EUR | X EUR | X% | G/A/R |
| Net result | X EUR | X EUR | | G/A/R |
| Cost per attendee | X EUR | X EUR | | G/A/R |
| **Marketing/Reach** | | | | |
| Social media reach | X | X | X% | G/A/R |
| Social media engagement | X | X | X% | G/A/R |
| Media coverage (articles) | X | X | X% | G/A/R |
| Event hashtag mentions | X | X | X% | G/A/R |
| **Business** | | | | |
| Leads generated | X | X | X% | G/A/R |
| Qualified leads (MQL) | X | X | X% | G/A/R |
| Deals influenced | X | X | | G/A/R |
| Sponsorship renewed | X | X | X% | G/A/R |

### 6. ROI report

| Component | Value EUR |
|---|---|
| **Direct Revenue** | |
| Ticket sales | ... |
| Sponsorship received | ... |
| Exhibition fees | ... |
| Other revenue | ... |
| **Total Direct Revenue** | **...** |
| | |
| **Total Cost** | **...** |
| | |
| **Direct ROI** | **(Revenue - Cost) / Cost x 100 = X%** |
| | |
| **Indirect Value (estimated)** | |
| Media coverage equivalent value | ... |
| Lead pipeline value (leads x avg deal size x conversion rate) | ... |
| Brand awareness lift (survey-measured) | ... |
| Employee engagement / team building value | ... |
| **Total Value (direct + indirect)** | **...** |
| **Full ROI** | **X%** |

### 7. Vendor scorecard
Rate each vendor on these dimensions (1-5 scale):

| Criterion | Weight | Vendor A | Vendor B | Vendor C |
|---|---|---|---|---|
| Quality of deliverable | 25% | /5 | /5 | /5 |
| Punctuality (arrival, deadlines) | 20% | /5 | /5 | /5 |
| Communication (responsiveness, clarity) | 20% | /5 | /5 | /5 |
| Problem-solving (when issues arose) | 15% | /5 | /5 | /5 |
| Value for money | 15% | /5 | /5 | /5 |
| Professionalism (attitude, appearance) | 5% | /5 | /5 | /5 |
| **Weighted score** | **100%** | **/5** | **/5** | **/5** |
| **Recommendation** | | Rehire / Consider / Replace | | |

Notes per vendor: specific feedback, contract issues, pricing concerns, relationship status.

### 8. Photo/video asset management

| Asset | Vendor | Delivery date | Format | Usage rights | Archive location |
|---|---|---|---|---|---|
| Event photos (full set) | ... | +2 weeks | High-res JPEG | Unlimited / 1 year / credit required | ... |
| Preview photos (20-30) | ... | +24-48h | Web-res JPEG | Social media immediate use | ... |
| Highlight video (2-3 min) | ... | +3-4 weeks | MP4 1080p/4K | ... | ... |
| Full session recordings | ... | +2 weeks | MP4 | ... | ... |
| Aftermovie | ... | +4-6 weeks | MP4 | ... | ... |
| Social media clips | ... | +1 week | MP4 vertical | ... | ... |

**Usage rights checklist:**
- [ ] Attendee photo consent obtained (RGPD — via registration T&C or signage)
- [ ] Speaker/performer release forms signed
- [ ] Venue photography permission confirmed
- [ ] Sponsor logo usage approved for post-event materials
- [ ] Copyright and credit requirements documented

### 9. Thank-you communications

#### Template: Attendee thank-you (email, within 24h)
Subject: Obrigado por estar connosco no [Event Name]

Content framework:
- Thank for attending (personal, warm)
- 1-2 highlight moments or key takeaways
- Survey link (this is the primary CTA)
- Save the date for next edition (if applicable)
- Photo gallery link
- Social media: "Share your experience with #[hashtag]"

#### Template: Speaker/VIP thank-you (personalized email, within 24h)
- Personal thank-you referencing their specific contribution
- 1-2 photos of them at the event attached
- Offer to share their session recording/slides
- Express interest in future collaboration

#### Template: Sponsor thank-you (email + formal letter, within 72h)
- Thank for partnership and investment
- Preliminary metrics relevant to their sponsorship (logo views, lead scans, etc.)
- Promise of full post-event report with detailed deliverables
- Express interest in continued partnership

#### Template: Vendor thank-you (email, within 48h)
- Thank for professional service
- Specific praise for what went well
- Constructive feedback if relevant (diplomatically)
- Indicate interest in working together again (or not, gracefully)

### 10. Knowledge base update
After every event, update the organization's event knowledge base:
- [ ] Updated checklists with new items discovered
- [ ] Updated vendor database with scores and notes
- [ ] Updated budget templates with actual costs (for future estimation)
- [ ] Updated timeline templates with actual durations
- [ ] Lessons learned document filed
- [ ] Photos archived with proper naming and metadata
- [ ] Event case study drafted (if showcase-worthy)

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-post-event
event_date: <YYYY-MM-DD>
attendance: <actual>
nps: <score>
total_cost: <EUR>
total_revenue: <EUR>
---

# Post-Event Report — <Event Name>

## Resumo Executivo
| Parametro | Target | Resultado | Avaliacao |
|---|---|---|---|
| Assistencia | X | X | [above/below target] |
| NPS | X | X | [excellent/good/needs work] |
| Receita | X EUR | X EUR | [+/-X%] |
| Custo total | X EUR | X EUR | [+/-X%] |
| Resultado liquido | X EUR | X EUR | |
| ROI | X% | X% | |

## Debrief
### O que correu bem
### O que nao correu bem
### O que melhorar
### Recomendacoes para proxima edicao

## Dashboard de Metricas
[Full metrics table with RAG status]

## Reconciliacao Financeira
### Budget vs. Real
| Categoria | Orcamento | Real | Variancia | RAG |
|---|---|---|---|---|

### Receitas vs. Previsto
| Fonte | Previsto | Real | Variancia |
|---|---|---|---|

## ROI
| Metrica | Valor |
|---|---|

## Scorecard de Fornecedores
| Fornecedor | Servico | Score /5 | Recomendacao |
|---|---|---|---|

## Resultados Survey
### NPS Distribution
### CSAT Breakdown
### Top Feedback Themes
### Verbatim Quotes (selected)

## Gestao de Assets
| Asset | Status | Prazo entrega | Localizacao |
|---|---|---|---|

## Comunicacoes Enviadas
| Tipo | Destinatario | Data | Status |
|---|---|---|---|

## Licoes Aprendidas
| # | Licao | Impacto | Accao para futuro |
|---|---|---|---|

## Proximos Passos
- [ ] Finalizar reconciliacao financeira
- [ ] Completar vendor scorecards
- [ ] Enviar relatorio a stakeholders
- [ ] Arquivar todos os assets
- [ ] Actualizar templates e checklists
- [ ] Decisao: repetir evento? Data proposta?
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Post-Event Report ATLAS.md`

## Red flags — don't do this
- Never delay the attendee survey beyond 48 hours — response rates drop 50%+ after 72 hours and memory fades
- Never skip the team debrief or hold it more than 2 weeks after the event — fresh memories are essential for honest, detailed feedback
- Never publish a stakeholder report without financial reconciliation — approximate numbers undermine credibility
- Never fail to document vendor performance — in 6 months you won't remember who was excellent and who was terrible
- Never ignore negative survey feedback — the harshest comments often contain the most valuable improvement signals
- Never forget RGPD compliance when using photos — attendee consent must be documented, and individuals can request photo removal
- Never send a generic thank-you to speakers and VIPs — personalization shows respect and secures future participation
- Never let the knowledge base update slide — the entire point of post-event analysis is to make the next event better; without updating templates and checklists, the same mistakes repeat

## Interactions
- Follows all other ATLAS skills: `atlas-briefing` (compare objectives vs. results), `atlas-venue` (venue feedback for future), `atlas-timeline` (adherence analysis), `atlas-budget` (financial reconciliation), `atlas-checklist` (operational review)
- Feeds back into `atlas-briefing` template improvements and `atlas-budget` benchmarks
- Save via `dario-obsidian-save` to vault


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-post-event** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-post-event:**

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
