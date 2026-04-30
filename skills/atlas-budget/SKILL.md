---
name: atlas-budget
description: Event budget and financial management. Budget categories with benchmarks, cost estimation (per-person, fixed/variable), revenue streams (tickets, sponsorship, exhibitors), P&L with breakeven, payment schedules, IVA rates PT, variance tracking RAG status, contingency management, and ROI calculation. Triggers on "budget evento", "orcamento evento", "custo evento", "quanto custa evento", "event budget", "event costs", "financeiro evento", "sponsorship pricing".
license: MIT
---

# ATLAS Skill — Event Budget & Financial Management

Produces comprehensive event budgets with category benchmarks, revenue projections, P&L analysis, payment schedules, and ROI calculations. Calibrated for the Portuguese market with correct IVA rates, local pricing benchmarks, and vendor payment norms. The budget is a living document — tracked against actuals with RAG (Red/Amber/Green) variance monitoring throughout the planning cycle.

## When to activate

Invoke `/atlas-budget` (or trigger automatically) when:
- User asks "quanto vai custar o evento" or needs a cost estimate
- User needs to build a business case for event approval
- User needs to set ticket prices or sponsorship tiers
- User wants to track budget vs. actual spending
- After `atlas-briefing` defines scope and `atlas-venue` confirms venue costs
- User needs to calculate event ROI

Do NOT use when:
- User needs only a venue comparison (use `atlas-venue`)
- User needs day-of logistics (use `atlas-checklist`)
- Event has no financial dimension (informal internal meeting)

## Workflow

### 1. Gather budget inputs
From `atlas-briefing` and `atlas-venue` or directly:
- **Event type:** corporate, social, public, hybrid
- **Scale:** number of attendees (minimum, target, maximum)
- **Duration:** hours, full day, multi-day
- **Venue:** confirmed cost or estimated range
- **Format:** seated dinner, cocktail, conference, festival
- **Production level:** basic (screen + mic), standard (stage + lighting), premium (full production)
- **Catering level:** coffee breaks only, buffet, seated service, premium gastronomy
- **Revenue model:** free event, ticketed, sponsored, mixed

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "event budget categories cost breakdown benchmarks", limit: 5)
mcp__dario-rag__search_kb(query: "event sponsorship pricing tiers ROI calculation", limit: 5)
```

### 3. Budget category benchmarks
Standard allocation ranges by event type:

#### Corporate Conference/Seminar
| Category | % of Total | Notes |
|---|---|---|
| Venue hire | 20-30% | Room hire, setup, teardown |
| Catering | 25-35% | Coffee breaks, lunch, dinner, beverages |
| AV/Production | 15-25% | Sound, lighting, video, stage, streaming |
| Speakers/Entertainment | 5-15% | Fees, travel, accommodation |
| Marketing/Communications | 3-8% | Website, email, social, print |
| Staffing | 5-10% | Event team, hostesses, security |
| Decor/Branding | 3-7% | Signage, florals, branded elements |
| Photography/Video | 3-5% | Event coverage, aftermovie |
| Transportation | 2-5% | Shuttles, transfers, parking |
| Insurance | 1-2% | Event liability, cancellation |
| Contingency | 10-15% | MANDATORY — never budget without it |

#### Gala Dinner / Awards
| Category | % of Total | Notes |
|---|---|---|
| Venue hire | 15-25% | Often included in F&B minimum |
| Catering (F&B) | 35-45% | Seated dinner, open bar, premium |
| Entertainment | 10-20% | Band, DJ, performers |
| AV/Production | 10-15% | Stage, lighting, screens, awards |
| Decor/Florals | 8-12% | Centrepieces, styling, theming |
| Photography/Video | 3-5% | |
| Staffing | 3-5% | |
| Print/Stationery | 2-3% | Invitations, menus, programs |
| Contingency | 10-15% | |

#### Wedding (Portuguese market 2026)
| Category | % of Total | Notes |
|---|---|---|
| Venue + Catering | 40-50% | Often bundled in quintas |
| Photography/Video | 8-12% | Premium PT photographers: 2,000-5,000 EUR |
| Music/Entertainment | 8-12% | DJ + band typical |
| Florals/Decor | 5-10% | Arch, centrepieces, church |
| Bride attire + beauty | 5-8% | Dress, makeup, hair |
| Stationery | 1-3% | Invitations, menus, signage |
| Transport | 2-3% | Classic car, shuttle |
| Officiant | 1% | Civil: 200-400 EUR, religious: variable |
| Contingency | 10% | |

### 4. Cost estimation methods
#### Per-person cost benchmarks (Portugal 2026)
| Item | Economy | Standard | Premium | Luxury |
|---|---|---|---|---|
| Coffee break (AM or PM) | 5-8 EUR | 8-12 EUR | 12-18 EUR | 18-25 EUR |
| Buffet lunch | 20-30 EUR | 30-45 EUR | 45-65 EUR | 65-100 EUR |
| Seated dinner (3 courses) | 35-50 EUR | 50-75 EUR | 75-120 EUR | 120-200+ EUR |
| Cocktail reception (2h) | 25-35 EUR | 35-50 EUR | 50-75 EUR | 75-120 EUR |
| Open bar (3h) | 15-25 EUR | 25-40 EUR | 40-60 EUR | 60-100 EUR |
| Welcome bag / gift | 10-20 EUR | 20-40 EUR | 40-80 EUR | 80-150+ EUR |
| Badge + materials | 3-5 EUR | 5-10 EUR | 10-15 EUR | 15-25 EUR |

#### Fixed costs (not per-person)
| Item | Range (PT 2026) | Notes |
|---|---|---|
| Event photographer (8h) | 800-2,500 EUR | Delivery: 2-4 weeks |
| Videographer (8h + edit) | 1,500-5,000 EUR | Aftermovie: +1,000-3,000 EUR |
| DJ (5h) | 500-2,000 EUR | Premium/known: 2,000-5,000+ |
| Live band (3h) | 1,500-5,000 EUR | Top bands: 5,000-15,000 EUR |
| Sound system rental | 500-3,000 EUR | Dependent on venue/size |
| Lighting package | 500-5,000 EUR | Basic to full production |
| LED wall (per m2/day) | 150-300 EUR/m2 | 4K: premium pricing |
| Stage (per m2) | 30-60 EUR/m2 | Including structure, carpet |
| Streaming setup | 1,000-5,000 EUR | Camera, encoder, platform |
| MC / Presenter | 500-3,000 EUR | Celebrity: 5,000-15,000+ |
| Hostesses (per person/day) | 120-200 EUR | Bilingual: +25% |
| Security (per person/8h) | 100-180 EUR | Licensed security mandatory for 500+ |
| Event manager (day-of) | 500-1,500 EUR | Full-service agency: 15-25% of total |

### 5. Revenue streams
#### Ticket pricing strategy
- **Cost-plus:** total cost / target attendance + margin (20-40%)
- **Value-based:** price based on perceived value and competitor benchmarks
- **Tiered:** early bird (-20%), standard, VIP (+50-100%), group (-10-15%)
- **Portuguese market norms:** corporate conferences 100-500 EUR, workshops 50-200 EUR, galas 80-200 EUR

#### Sponsorship tiers (standard structure)
| Tier | Price range (PT) | Deliverables |
|---|---|---|
| Title/Presenting | 10,000-50,000+ EUR | Logo everywhere, speaking slot, exhibition space, exclusivity |
| Gold | 5,000-15,000 EUR | Logo main stage, exhibition space, attendee access, 1 social post |
| Silver | 2,000-7,000 EUR | Logo materials, roll-up, attendee access |
| Bronze | 1,000-3,000 EUR | Logo website + program, attendee passes |
| In-kind | Value equivalent | Services/products in exchange for visibility |

#### Other revenue
- Exhibition stands: 500-5,000 EUR per 3x3m (depends on event prestige)
- Workshop fees: separate paid sessions within event
- Merchandise: event-branded items
- Bar revenue: if operating own bar vs. venue bar
- Post-event content: recordings, on-demand access

### 6. P&L template with breakeven
| Line | Amount EUR |
|---|---|
| **REVENUE** | |
| Ticket sales (X tickets x Y EUR) | ... |
| Sponsorship (breakdown by tier) | ... |
| Exhibition fees | ... |
| Other revenue | ... |
| **Total Revenue** | **...** |
| | |
| **EXPENSES** | |
| Venue | ... |
| Catering | ... |
| AV/Production | ... |
| Speakers/Entertainment | ... |
| Marketing | ... |
| Staffing | ... |
| Decor | ... |
| Photography/Video | ... |
| Transport | ... |
| Insurance | ... |
| Contingency (10-15%) | ... |
| **Total Expenses** | **...** |
| | |
| **NET RESULT** | **...** |
| **Breakeven (attendees)** | **X pax** |
| **Breakeven (sponsorship)** | **X EUR** |

### 7. IVA (VAT) rates — Portugal 2026
| Item | IVA Rate | Legal basis |
|---|---|---|
| Venue hire | 23% | Taxa normal |
| Catering services (with service) | 13% | Lista II, verba 3.1 CIVA |
| Food products (take-away) | 13% or 6% | Depends on type |
| Beverages (alcoholic) | 23% | Taxa normal |
| AV equipment rental | 23% | Taxa normal |
| Photography/Video services | 23% | Taxa normal |
| Entertainment/performance | 6% | Lista I, verba 2.14 CIVA (espetaculos) |
| Speaker fees (PT resident) | 23% | Prestacao de servicos |
| Speaker fees (EU, B2B) | 0% (reverse charge) | Art. 6 CIVA |
| Accommodation | 6% | Lista I, verba 2.17 CIVA |
| Transportation | 6% | Lista I, verba 2.16 CIVA (passageiros) |
| Event insurance | Isento | Art. 9 CIVA |
| Ticket sales (event admission) | 6% | If classified as spectacle/entertainment |

**Important:** mixed-rate invoicing is common in events. Always request itemized invoices from vendors to correctly apply rates.

### 8. Payment schedule (standard PT market)
| Phase | % of Total | Timing | Notes |
|---|---|---|---|
| Venue deposit | 25-50% venue cost | On booking (6-12mo before) | Non-refundable after X days |
| Vendor deposits | 30-50% per vendor | On contract signing (3-6mo) | Secures date and resources |
| Progress payments | 25-30% per vendor | 1-2 months before event | Materials, production starts |
| Pre-event balance | 70-100% catering | 7-14 days before (final numbers) | Based on confirmed headcount |
| Final settlements | Remaining balance | 7-30 days after event | After reconciliation |
| Retention (production) | 5-10% | 30 days after event | Quality guarantee |

### 9. Variance tracking (RAG status)
Monitor budget vs. actual throughout planning:

| Status | Variance | Action |
|---|---|---|
| **GREEN** | Within 5% of budget | On track, no action needed |
| **AMBER** | 5-15% over budget | Investigate cause, identify savings elsewhere |
| **RED** | >15% over budget | Escalate to event owner, reforecast, cut scope if needed |

Track weekly from 3 months before event, daily in final week.

### 10. ROI calculation
| Metric | Formula | Target |
|---|---|---|
| Cost per attendee | Total cost / attendees | Benchmark against industry |
| Cost per lead | Total cost / qualified leads | Compare with digital marketing CPL |
| Revenue per attendee | Total revenue / attendees | > cost per attendee = profitable |
| Sponsorship ROI | Sponsor value delivered / sponsor fee | >3x for retention |
| Net margin | (Revenue - Cost) / Revenue x 100 | 15-25% for commercial events |
| Brand value | Media coverage equivalent value | PR agency benchmark |

## Output template

```markdown
---
project: <event name>
date: <YYYY-MM-DD>
type: atlas-budget
event_type: <corporate|social|public|hybrid>
attendees: <target number>
total_budget: <EUR>
---

# Event Budget — <Event Name>

## Resumo Financeiro
| Parametro | Valor |
|---|---|
| Evento | ... |
| Data | ... |
| Assistencia prevista | ... pax |
| Budget total | ... EUR |
| Receita prevista | ... EUR |
| Resultado liquido | ... EUR |
| Custo/participante | ... EUR |
| Breakeven | ... pax ou ... EUR sponsorship |

## Receitas
| Fonte | Quantidade | Preco unit. | Total EUR | Status |
|---|---|---|---|---|
| Bilhetes early bird | X | Y | Z | Confirmado/Estimado |
| Bilhetes standard | X | Y | Z | ... |
| Bilhetes VIP | X | Y | Z | ... |
| Patrocinio Title | 1 | Y | Z | ... |
| Patrocinio Gold | X | Y | Z | ... |
| Patrocinio Silver | X | Y | Z | ... |
| Stands exposicao | X | Y | Z | ... |
| Outros | - | - | Z | ... |
| **Total Receitas** | | | **Z** | |

## Despesas
| Categoria | % | Orcamento EUR | Real EUR | Variancia | RAG |
|---|---|---|---|---|---|
| Venue | X% | ... | ... | ... | G/A/R |
| Catering | X% | ... | ... | ... | G/A/R |
| AV/Producao | X% | ... | ... | ... | G/A/R |
| Speakers/Entretenimento | X% | ... | ... | ... | G/A/R |
| Marketing | X% | ... | ... | ... | G/A/R |
| Staffing | X% | ... | ... | ... | G/A/R |
| Decor/Branding | X% | ... | ... | ... | G/A/R |
| Fotografia/Video | X% | ... | ... | ... | G/A/R |
| Transporte | X% | ... | ... | ... | G/A/R |
| Seguro | X% | ... | ... | ... | G/A/R |
| Contingencia | 10-15% | ... | ... | ... | G/A/R |
| **Total Despesas** | **100%** | **...** | **...** | | |

## Analise IVA
| Categoria | Base EUR | Taxa IVA | IVA EUR |
|---|---|---|---|
| Venue | ... | 23% | ... |
| Catering | ... | 13% | ... |
| Entretenimento | ... | 6% | ... |
| Alojamento | ... | 6% | ... |
| Outros servicos | ... | 23% | ... |
| **Total IVA** | | | **...** |

## Calendario de Pagamentos
| Data | Fornecedor | Valor EUR | Tipo | Status |
|---|---|---|---|---|
| ... | Venue (deposito) | ... | Transferencia | Pago/Pendente |
| ... | AV (deposito) | ... | ... | ... |
| ... | Catering (sinal) | ... | ... | ... |

## Analise de Sensibilidade
| Cenario | Assistencia | Receita | Custo | Resultado |
|---|---|---|---|---|
| Optimista | +20% | ... | ... | ... |
| Base | Target | ... | ... | ... |
| Pessimista | -30% | ... | ... | ... |
| Breakeven | X pax | ... | ... | 0 |

## ROI
| Metrica | Valor |
|---|---|
| Custo por participante | ... EUR |
| Custo por lead | ... EUR |
| Receita por participante | ... EUR |
| Margem liquida | ...% |

## Riscos Orcamentais
| Risco | Impacto | Mitigacao |
|---|---|---|
| Assistencia abaixo do target | -X EUR receita | Early bird agressivo, marketing reforco |
| Aumento custos catering | +X% | Fixar precos no contrato |
| Cancelamento de patrocinador | -X EUR | Clausula contratual, reserva extra |

## Proximos Passos
- [ ] Aprovar budget com stakeholder
- [ ] Solicitar orcamentos formais a vendors (minimo 3 por categoria)
- [ ] Confirmar modelo de receitas e iniciar vendas
- [ ] Activar tracking semanal de variancia
- [ ] Seguir com `atlas-timeline` para alinhar pagamentos com milestones
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Event> - Budget ATLAS.md`

## Red flags — don't do this
- Never present a budget without a contingency line of 10-15% minimum — events always have surprises and the contingency is not optional
- Never allocate >40% of total budget to a single vendor — concentration risk means one vendor issue can sink the entire event
- Never pay 100% upfront to any vendor — standard is 30-50% deposit, balance on delivery/completion, with 5-10% retention
- Never accept verbal quotes — all pricing must be in writing with scope, inclusions, exclusions, and validity period
- Never ignore scope creep — every "small addition" without budget adjustment erodes the contingency and leads to overrun
- Never forget IVA in cost calculations — the difference between net and gross on a 50,000 EUR event can be 6,500-11,500 EUR depending on rate mix
- Never set ticket prices without a breakeven analysis — pricing below cost requires guaranteed sponsorship to cover the gap
- Never skip the sensitivity analysis — knowing the minimum viable attendance for breakeven is critical for Go/No-Go decisions
- Never mix budget currencies without hedging — international speaker fees in USD/GBP need a rate buffer of 5-10%

## Interactions
- Follows `atlas-briefing` (objectives, scale) and `atlas-venue` (confirmed venue cost)
- Aligns with `atlas-timeline` for payment milestone scheduling
- Feeds into `atlas-post-event` for financial reconciliation and ROI report
- Sponsorship tiers feed into marketing and sales materials
- Save via `dario-obsidian-save` to vault
