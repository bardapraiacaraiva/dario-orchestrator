---
name: dario-pipeline
description: Sales pipeline builder and auditor — ICP definition, outbound cadence, pipeline math, proposal framework, target accounts. Uses Sales Squad (Blount, Ross, Enns, Weinberg). Triggers on "pipeline", "vendas", "sales", "prospecção", "outbound", "clientes novos", "como arranjar clientes".
license: MIT
---

# DARIO Skill — Sales Pipeline

## Workflow
1. RAG: `search_kb("sales pipeline prospecting outbound icp", collection: "dario")`
2. Define ICP (Ideal Customer Profile)
3. Build target account list (20-30 contas)
4. Design outbound cadence (8-12 touches, 3-4 weeks)
5. Pipeline math: emails → responses → meetings → proposals → deals
6. Proposal framework (Blair Enns 3 options)
7. Weekly pipeline review cadence

## Output includes
- ICP document
- Target account list template
- Email/LinkedIn outreach templates (3 variants)
- Pipeline math with conversion rates
- Proposal structure (3 tiers)
- Weekly review checklist

---

## ICP Template

Fill this for every new prospecting campaign before writing a single email.

| Field | Definition |
|-------|-----------|
| **Industry** | Primary vertical (e.g., Real Estate, Health & Wellness, Legal, SaaS, E-commerce, Hospitality) |
| **Company Size** | Employee count range (e.g., 5-50 for SMB, 50-200 for mid-market) |
| **Revenue Range** | Annual revenue bracket (e.g., 500K-2M EUR for PT SMB sweet spot) |
| **Decision Maker Title** | CEO, CMO, Marketing Director, Founder, General Manager |
| **Pain Points** | 1. Website outdated, losing leads to competitors with modern presence |
| | 2. No organic traffic — paying for every click, zero compounding |
| | 3. No system to convert visitors into leads (no funnel, no automation) |
| | 4. Previous agency delivered templates, not strategy |
| | 5. Growing but brand image doesn't reflect quality of service |
| **Trigger Events** | Rebranding, new product/service launch, competitor redesign, funding round, expansion to new market, hiring a marketing role for the first time, negative Google reviews spike |
| **Disqualifiers** | Annual marketing budget under 3K EUR, expects results in under 30 days, no willingness to provide content/access, decision maker unreachable after 3 attempts, "just need a logo" |

---

## Outbound Cadence

3-week, 10-touch multi-channel cadence. Each touch builds on the previous — never repeat the same angle twice.

| Day | Channel | Action | Notes |
|-----|---------|--------|-------|
| **Day 1** | Email | **Email 1 — Curiosity Hook** | Subject: "Reparei numa coisa no vosso site..." — short, personalized observation about their website or digital presence |
| **Day 3** | LinkedIn | **Connect Request** | Personalized note referencing their industry or a recent post. No pitch. |
| **Day 5** | Email | **Email 2 — Value Add** | Share a specific insight: "3 coisas que os vossos concorrentes estao a fazer que vos estao a custar leads" — attach a 1-page mini-audit or screenshot |
| **Day 8** | Phone | **Call 1** | Reference emails sent. Ask one calibrated question: "Como estao a gerar novos clientes neste momento?" — listen, don't pitch |
| **Day 10** | LinkedIn | **Engage Content** | Comment meaningfully on their post or share their content with a tag. Build visibility. |
| **Day 12** | Email | **Email 3 — Social Proof** | Case study: "Como ajudamos [similar company] a aumentar leads em X% em 90 dias" — include one specific metric |
| **Day 15** | Phone | **Call 2** | Voicemail OK. Reference the case study email. Offer a free 15-min diagnostic call. |
| **Day 17** | LinkedIn | **Direct Message** | Short DM: "Vi que abriu o meu email sobre [topic] — faz sentido trocarmos 15 minutos esta semana?" |
| **Day 19** | Email | **Email 4 — Breakup** | "Parece que o timing nao e o melhor — vou parar de incomodar. Se no futuro fizer sentido, fico disponivel." Creates urgency through withdrawal. |
| **Day 21** | LinkedIn | **Final Value Drop** | Share a relevant article or resource without asking for anything. Leave the door open. |

**Rules:** Never send more than 1 touch per day. Personalize every email (no mass templates). If they reply at any point, exit cadence and enter conversation mode.

---

## Pipeline Math

Realistic conversion funnel for a Portuguese digital agency doing cold outbound to SMBs.

| Stage | Volume | Rate | Notes |
|-------|--------|------|-------|
| **Emails Sent** | 500 | — | Monthly volume for 1 SDR/founder doing outbound |
| **Opened** | 175 | 35% | Good subject lines, warm-ish list, deliverability above 95% |
| **Replied** | 25 | 5% of sent | Mix of positive, neutral, and "not interested" |
| **Positive Replies** | 12 | 2.4% of sent | Willing to talk, asked questions, showed interest |
| **Meetings Booked** | 10 | 40% of replies | Some ghost, some reschedule — 40% of all replies convert to meeting |
| **Proposals Sent** | 6 | 60% of meetings | Not every meeting is qualified — 60% get a proposal |
| **Deals Closed** | 2 | 30% of proposals | Industry average for agency services |
| **Average Deal Value** | 3,000 EUR | — | Website + SEO starter package (PT SMB) |
| **Monthly Revenue from Outbound** | 6,000 EUR | — | 2 deals x 3,000 EUR |
| **Revenue per Email Sent** | 12 EUR | — | 6,000 / 500 — track this as your North Star efficiency metric |

**Levers to improve:**
- Better targeting (ICP refinement) → higher reply rate
- Stronger case studies → higher meeting-to-proposal rate
- 3-option proposals (Blair Enns) → higher proposal-to-close rate and larger deal size
- Referral program from closed clients → compounds pipeline without extra outbound effort

---

## Email Templates

### Template 1 — Curiosity-Based

**Subject:** Reparei numa coisa no site da [EMPRESA]
**Body:**
Ola [NOME],

Estava a pesquisar [INDUSTRIA] em [CIDADE] e o vosso site apareceu-me. Reparei em [OBSERVACAO ESPECIFICA — ex: "que a pagina de servicos nao tem CTAs claros" ou "que o site demora 6s a carregar no mobile"].

Nao sei se e algo que ja tem no radar, mas tipicamente isso custa entre 20-40% dos visitantes que chegam ao site.

Se fizer sentido, posso partilhar 2-3 sugestoes rapidas — sem compromisso.

[ASSINATURA]

---

### Template 2 — Pain-Based

**Subject:** [EMPRESA] esta a perder clientes para [CONCORRENTE]?
**Body:**
Ola [NOME],

Trabalhamos com empresas de [INDUSTRIA] que tinham o mesmo problema: investiam em trafego pago mas o site nao convertia. Resultado — dinheiro a sair, leads a ir para a concorrencia.

O padrao que vemos: site desatualizado + zero SEO + nenhum funil = dependencia total de ads e boca-a-boca.

Se isto soa familiar, temos um diagnostico rapido (15 min) onde mostramos exactamente onde estao a perder e o que corrigir primeiro.

Vale a pena trocar uma ideia?

[ASSINATURA]

---

### Template 3 — Social Proof-Based

**Subject:** Como a [CLIENTE SIMILAR] passou de 0 a 40 leads/mes
**Body:**
Ola [NOME],

A [CLIENTE SIMILAR] — tambem em [INDUSTRIA] — veio ter connosco com um site de 2018 e zero presenca organica. Em 90 dias:
- Site novo com funil integrado
- De 0 a 1.200 visitas organicas/mes
- 40 leads qualificados/mes via formulario

Nao e magia — e processo: auditoria → estrategia → execucao → otimizacao.

Se a [EMPRESA] esta numa fase parecida, faz sentido trocar 15 minutos esta semana?

[ASSINATURA]

---

## Weekly Pipeline Review

Run this every Monday morning. 30 minutes max.

- [ ] **New leads this week:** How many new contacts entered the pipeline? Is volume on track for monthly target?
- [ ] **Cadence compliance:** Did every active lead get their scheduled touch? Check for missed follow-ups.
- [ ] **Reply analysis:** Review all replies from last week. Categorize: positive / neutral / negative / objection. Extract patterns.
- [ ] **Meetings scheduled:** How many meetings booked for this week? Prep accusation audits for each (use dario-negotiation).
- [ ] **Proposals outstanding:** Which proposals are pending response? Follow up on anything older than 5 business days.
- [ ] **Deals closed/lost:** Update pipeline math with actual numbers. Compare to benchmarks.
- [ ] **ICP validation:** Are the leads responding the type we expected? Adjust ICP if pattern shows a different sweet spot.
- [ ] **Content gaps:** Did any prospect ask a question we don't have content for? Create that asset this week.
- [ ] **Revenue forecast:** Based on current pipeline, project this month's close rate and revenue.
- [ ] **Top 3 actions:** Define the 3 highest-leverage pipeline actions for this week.

---

## Save Location

- Pipeline plans → `05 - Claude - IA/Outputs/YYYY-MM-DD - Pipeline - [Cliente ou Campanha].md`
- ICP documents → `05 - Claude - IA/Outputs/YYYY-MM-DD - ICP - [Segmento].md`
- Email templates → `05 - Claude - IA/Outputs/YYYY-MM-DD - Outbound Templates - [Campanha].md`

---

## Red Flags

Stop and reassess the pipeline strategy if any of these appear:

- Open rate below 20% for 2+ weeks → deliverability issue or bad subject lines
- Zero replies after 100 emails → ICP is wrong or messaging doesn't resonate
- Meetings booked but no proposals sent → qualification criteria too loose
- Proposals sent but zero closes → pricing mismatch, weak value framing, or wrong decision maker
- Same objection appearing 3+ times → systemic messaging gap, address in templates
- Prospect ghosting after proposal → follow-up cadence missing or proposal too complex
- Outbound feels "spammy" → over-automation, not enough personalization per touch

## Delivery-ready self-check (run BEFORE delivering pipeline strategy ao cliente)

Pipeline output é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1. ICP completo com NÚMEROS específicos (não ranges genéricos)
- [ ] Industry + sub-vertical específico
- [ ] Company size com employee count CONCRETO (não "small business")
- [ ] Revenue range com bracket exato (não "small budget")
- [ ] Decision maker title named (não "decision makers")
- [ ] Pain points 5+ com cliente quote ou case anchor
- [ ] Trigger events 3+ events específicos detectáveis
- [ ] Disqualifiers 3+ items com hard line

❌ NOT delivery-ready: "Target small businesses with marketing needs"
✅ Delivery-ready: "ICP: SaaS PT B2B 50-250 empregados, receita anual €2-15M, decision maker é Head of Marketing ou CEO directo. Pain: outbound team de 2 SDRs sem escala, CAC €4.5K acima do benchmark €2.8K, response rate <2%. Triggers: founding new sales role, deteccao competidor PT a crescer, ARR plateau >12 meses."

### 2. Cadence com touches EXACTOS + scripts + channels
- [ ] 8-12 touches mapeados em calendar days específicos
- [ ] Channel definido por touch (email/LinkedIn/phone/video)
- [ ] Script ou angle por touch (não "follow-up email")
- [ ] Personalização variables marcados ({first_name}, {pain_anchor}, {recent_event})

### 3. Pipeline math com CONVERSION RATES citadas (fonte ou industry benchmark)
- [ ] N contas → emails sent (volume target)
- [ ] Open rate target + benchmark fonte
- [ ] Reply rate target + benchmark
- [ ] Meeting book rate
- [ ] Proposal-to-deal rate
- [ ] Bottom-line: X dollars in N months

❌ NOT delivery-ready: "Aproximadamente 1-2 deals por mês"
✅ Delivery-ready: "30 target accounts × 80% emailed (24) × 25% open (6) × 15% reply (1) × 60% meeting (0.6) × 40% proposal (0.24) × 35% close = 0.084 deals/account. 30 accounts = ~2.5 deals em 90d. AVG deal €8K = €20K/quarter pipeline value (fontes: HubSpot 2026 B2B benchmarks + agência stats próprias)."

### 4. Target Account List TEMPLATE com 5+ critérios + scoring
- [ ] Selection criteria explícito (ICP fit, signal strength, accessibility)
- [ ] Lead scoring formula (não "high/medium/low" subjective)
- [ ] Source channels (Apollo, ZoomInfo, manual research, etc.)
- [ ] Cadence assignment rules (A-tier accounts = full cadence, B = lighter)

### 5. CRM + tracking setup EXPLICIT
- [ ] HubSpot/Pipedrive/Outreach options + recommendation
- [ ] Stages definition (não "qualified leads")
- [ ] Activity targets per SDR/week
- [ ] Reporting dashboard fields

### 6. Output uses CLIENT NAME + REAL data throughout
- [ ] Client name em cada section title
- [ ] Industry/vertical-specific (não generic B2B)
- [ ] Templates referencem actual case studies + names
- [ ] Sem placeholder angle-brackets

## Fully-worked A-tier example (delivery-ready reference)

Pipeline 92+/100 para SaaS PT B2B:

```markdown
---
project: Tributario.AI (sales pipeline launch)
date: 2026-05-23
type: sales-pipeline
target_revenue_quarter: €60K pipeline value
---

# Sales Pipeline — Tributario.AI

## ICP

| Field | Definition |
|---|---|
| Industry | Empresas brasileiras com faturação >R$ 100M/ano sujeitas Reforma Tributária CBS+IBS |
| Sub-vertical | Indústria + varejo + serviços com complexidade fiscal alta (multi-estado) |
| Employee count | 200-2000 colaboradores |
| Revenue | R$ 100M - R$ 1B ARR |
| Decision Maker | CFO + Tax Director (parallel) |
| Pain points | 1. Reforma 2026 obriga rebuilder modelos fiscais com prazo Set 2026 |
| | 2. Big4 consultor cobra R$ 250-500K, planning ciclo 12 meses |
| | 3. Excel-based fiscal forecast: 1 senior controller 50% do tempo |
| | 4. Audit BR receita federal: 6 cases/ano (industry avg) |
| | 5. Sem simulador "what-if" para changes regulatórios |
| Triggers | Reforma aprovação Lei Complementar (Jul 2026), nova hire CFO/Tax (LinkedIn signal), audit BR receita (news scraping), pos-IPO TG transition |
| Disqualifiers | Faturação <R$ 50M, decision maker inacessível 3 attempts, Big4 contracted (12mo lock), "só ferramenta sem advisory" |

## Pipeline Math (90-day projection)

Target accounts: **30 contas** Tier-1 (full cadence)

| Stage | Conversion | Volume | Source benchmark |
|---|---|---|---|
| Accounts emailed | 90% (after research) | 27 | n/a |
| Emails opened | 32% (CFO B2B SaaS PT/BR 2026) | 8.6 | HubSpot 2026 + RD Station |
| Replied | 18% of opens | 1.5 | Outreach.io 2026 |
| Meeting booked | 65% of replies | 1.0 | (account-specific, low N variance) |
| Proposal sent | 80% of meetings | 0.8 | (qualification rate) |
| Closed-won | 35% of proposals | 0.28 | (B2B SaaS BR enterprise) |
| **Deals expected** | | **~0.28/account** | |
| **Total 30 accounts** | | **~8.4 deals/90d** | |
| AVG deal value | R$ 12K/mo × 24mo = R$ 288K | | |
| **Pipeline value 90d** | | **R$ 2.4M ARR** | |

## Outbound Cadence (10 touches over 21 days)

[full table aqui]

## Target Account List (30 contas Tier-1)

Selection score per account:
- ICP fit (1-5): industry + size + revenue + trigger event
- Accessibility (1-5): contact found via Apollo/LinkedIn + email validated
- Signal strength (1-5): recent funding / news / hires / org changes
- **Total score >12/15 → Tier-1 cadence**, 8-12 = Tier-2 (light), <8 = drop

Source mix:
- Apollo.io: 15 (filtros revenue + employees + role)
- LinkedIn Sales Navigator: 10 (industry + hires last 90d)
- Manual research: 5 (referrals, conference attendance)

[full account list aqui com nome empresa + CFO + nota signal]

## CRM Setup (HubSpot Pro)

- Pipeline name: "Tributario.AI BR Enterprise Q3 2026"
- Stages: New Lead → Researched → Engaged → Meeting Booked → Proposal Sent → Negotiation → Closed-Won / Closed-Lost
- Properties custom: ICP_score, Trigger_event, Reform_compliance_priority (1-5), Big4_competitor (Y/N)
- Activity targets/SDR/week: 100 emails + 50 LinkedIn + 25 calls
- Reporting: weekly review template (replies, meetings, proposals, blockers)

## Weekly Pipeline Review

Every Friday 16h00:
1. Stage transitions (last 7d)
2. Stuck accounts >14d → escalation criteria
3. Objections seen → messaging gap analysis
4. Net new accounts to add Tier-1 (target +5/week)
5. SDR ratio: actual vs target activity

## Next 14 Days

- Day 1-3: Apollo extract + LinkedIn enrichment (30 accounts)
- Day 4-7: Email templates A/B (2 variants × 3 cohorts)
- Day 8-10: HubSpot setup + pipeline configuration
- Day 11-14: Cadence launch + first 10 accounts triggered

Owner: João (SDR Lead). Slack channel #pipeline-tributario.
```

## Output anti-patterns

- ICP "small businesses" sem employee count + revenue range exato
- Pipeline math "aproximadamente N deals" sem conversion rates + source benchmark
- Cadence "follow-up email" sem script ou angle específico
- Target account list "20-30 accounts" sem scoring criteria
- CRM stages "qualified leads" sem definition
- Output sem frontmatter (tracking impossível)
- Placeholder <Client>/<Industry> em vez de nome real
