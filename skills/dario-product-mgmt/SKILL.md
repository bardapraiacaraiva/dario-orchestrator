---
name: dario-product-mgmt
description: Product management squad — roadmap prioritization, continuous discovery, OKRs, MVP scoping, hypothesis validation, stage-gate decisions. Based on Marty Cagan (Inspired/Empowered), Teresa Torres (Continuous Discovery Habits), Lenny Rachitsky, Shreyas Doshi, Melissa Perri (Escaping Build Trap), Adam Biddle (DHM Model). Triggers on "product management", "roadmap", "discovery", "prioritization", "MVP", "feature", "backlog", "OKR", "hypothesis", "user interview", "opportunity", "continue pivot kill", "PRD", "product strategy", "empowered team", "DHM".
version: 1.0.0
license: MIT
---

# DARIO Skill — Product Management

The discipline of deciding what to build, for whom, and in what order — before writing a single line of code. Combines Cagan's empowered product teams, Torres's continuous discovery, Perri's build trap escape, Doshi's ruthless prioritization, and Rachitsky's operator playbooks into a single decision-making framework.

## Squad Agents

| Agent | Mindset | Core Contribution |
|-------|---------|-------------------|
| **Cagan (Inspired/Empowered)** | "Fall in love with the problem, not the solution" | Empowered teams vs feature teams. Product discovery before delivery. Missionaries, not mercenaries. |
| **Torres (Continuous Discovery)** | "Good product decisions come from good product habits" | Opportunity Solution Trees, weekly customer touchpoints, assumption testing, experiment design. |
| **Perri (Escaping Build Trap)** | "Building more features doesn't mean building the right features" | Strategic intent, outcome-driven roadmaps, product kata, build trap diagnosis. |
| **Doshi (Ruthless Prioritization)** | "What you say no to defines your product more than what you say yes to" | Pre-mortems, LNO framework (Leverage/Neutral/Overhead), effort estimation honesty, high-agency PM behaviors. |
| **Rachitsky (Operator)** | "The best PMs ship, learn, and iterate faster than everyone else" | Tactical playbooks, benchmark data, hiring, stakeholder management, growth-product interface. |
| **Biddle (DHM Model)** | "Great products delight users in hard-to-copy, margin-enhancing ways" | DHM scoring (Delight, Hard-to-copy, Margin-enhancing), value proposition stress-testing, competitive moat assessment, PMF measurement. |

## When to activate

- "What should we build next?" — prioritization and roadmap
- "How do we know users want this?" — discovery and validation
- "We're shipping a lot but nothing moves the needle" — build trap diagnosis
- "Should we continue, pivot, or kill this feature/product?" — stage-gate decisions
- "How do we scope an MVP?" — minimum viable product design
- "We need a PRD" — product requirements document
- New product or major feature initiative
- Quarterly/annual planning cycle
- Product-market fit assessment or re-assessment
- User interview design and synthesis
- Backlog grooming and sprint planning
- Stakeholder alignment on product direction
- Relevant for: LUSOconta SaaS, Atelier AI, and any future product

## Workflow

### 1. Gather context

- **Product:** What exists today? What stage? (idea / prototype / MVP / PMF / growth / mature)
- **Users:** Who uses it? How many? What do they do with it?
- **Metrics:** Current NSM, activation rate, retention, revenue
- **Team:** Who's building? PM, engineers, designers — or solo founder doing everything?
- **Constraints:** Budget, timeline, technical debt, regulatory
- **Strategy:** Company-level strategy that product must serve
- **Backlog state:** How many items? When was it last groomed? How are things prioritized today?

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "marty cagan empowered product teams discovery delivery", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "teresa torres continuous discovery opportunity solution tree", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "melissa perri build trap outcome roadmap product kata", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "shreyas doshi prioritization DHM leverage neutral overhead", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "lenny rachitsky product management metrics benchmarks", collection: "dario", limit: 5)
```

### 3. Apply frameworks

#### Cagan: Product Discovery vs Delivery

**The Four Risks (validate before building):**

| Risk | Question | Discovery Technique |
|------|----------|-------------------|
| **Value** | Will users choose to use/buy this? | User interviews, prototype testing, demand tests |
| **Usability** | Can users figure out how to use it? | Prototype testing, usability tests |
| **Feasibility** | Can we build this with time/skills/tech available? | Technical spike, architecture review |
| **Business Viability** | Does this work for our business (legal, financial, strategic)? | Stakeholder alignment, financial model |

**Empowered vs Feature Teams:**

| Feature Team (bad) | Empowered Team (good) |
|--------------------|----------------------|
| Given solutions to implement | Given problems to solve |
| Measured by output (features shipped) | Measured by outcomes (metrics moved) |
| Roadmap = list of features with dates | Roadmap = list of problems/outcomes with timeframes |
| PM = project manager | PM = product leader |
| Stakeholders dictate what to build | Stakeholders provide context and constraints |

#### Torres: Continuous Discovery Habits

**Opportunity Solution Tree (OST):**

```
Desired Outcome (metric to move)
    |
    +-- Opportunity 1 (user need/pain)
    |       +-- Solution A
    |       |       +-- Assumption Test 1
    |       |       +-- Assumption Test 2
    |       +-- Solution B
    |               +-- Assumption Test 3
    |
    +-- Opportunity 2 (user need/pain)
            +-- Solution C
            +-- Solution D
```

**Rules:**
- Start with a clear desired outcome (not a feature request)
- Discover opportunities through weekly customer interviews (minimum 1/week)
- Generate multiple solutions per opportunity (never just one)
- Test assumptions before building (fastest/cheapest way to learn)
- Compare solutions against each other, not in isolation

**Assumption testing:**
1. List all assumptions that must be true for the solution to work
2. Rank by risk: which assumption, if wrong, kills the idea?
3. Test the riskiest assumption first, with the smallest possible experiment
4. Types: survey, prototype test, Wizard of Oz, concierge, data analysis, competitor analysis

#### Perri: Escaping the Build Trap

**Build Trap diagnosis checklist:**
- [ ] We ship features without measuring their impact
- [ ] Our roadmap is a list of features, not outcomes
- [ ] Success = "we shipped on time" not "users benefited"
- [ ] We don't talk to users regularly
- [ ] Product decisions are made by the highest-paid person in the room (HiPPO)
- [ ] We have a feature factory — high output, low outcome

If 3+ items checked → you're in the build trap.

**Product Kata (Perri's improvement cycle):**
1. **Understand the direction** — what strategic outcome are we driving?
2. **Analyze the current state** — where are we now? What do metrics say?
3. **Set the next target condition** — what's the next measurable milestone?
4. **Choose the first step** — smallest experiment to test if we're on track
5. **Review** — what did we learn? Adjust and repeat.

**Outcome-based roadmaps:**
- Theme: "Reduce time-to-value for new users" (not "Build onboarding wizard")
- Timeframe: Now / Next / Later (not specific dates)
- Each theme has: desired outcome, success metric, current baseline, target

#### Biddle: DHM Model

**DHM (Delight, Hard-to-copy, Margin-enhancing):**

Score every feature/initiative on three dimensions:

| Dimension | Question | Score 1-5 |
|-----------|----------|-----------|
| **Delight** | Does this create genuine user delight? Not just satisfaction — delight? | |
| **Hard-to-copy** | Can competitors replicate this within 6 months? If yes, low score. | |
| **Margin-enhancing** | Does this improve unit economics, reduce costs, increase willingness to pay? | |

**DHM Score = D + H + M** (max 15). Prioritize features scoring 10+.

Features that score high on Delight but low on Hard-to-copy are temporary advantages.
Features that score high on Hard-to-copy and Margin-enhancing are moats.

#### Doshi: LNO Framework & Pre-mortems

**LNO Framework (for PM's own time):**

| Category | Description | Time allocation |
|----------|-------------|----------------|
| **Leverage** | Tasks where 1 hour of effort creates 10x value | 80% of time |
| **Neutral** | Tasks that need to be done competently | 15% of time |
| **Overhead** | Tasks that just need to be completed | 5% of time |

Apply to: meetings, documents, analyses, stakeholder conversations. Ruthlessly de-prioritize Overhead tasks.

#### Stage-Gate Decision Framework

At each milestone, make an explicit decision: **Continue / Pivot / Kill**

| Gate | Question | Evidence Required | Decision Criteria |
|------|----------|-------------------|-------------------|
| **G0: Problem** | Is this a real problem worth solving? | 10+ user interviews confirming the pain | At least 8/10 say it's a top-3 problem |
| **G1: Solution** | Does our solution address the problem? | Prototype tested with 5+ users | 4/5 can complete key task without help |
| **G2: MVP** | Do users actually use/pay for this? | Live MVP with real users for 2+ weeks | Activation > 25%, retention D7 > 20% |
| **G3: PMF** | Can we grow this sustainably? | 3+ months of data, Ellis test done | 40%+ "very disappointed," or sustainable organic growth |
| **G4: Scale** | Is the unit economics viable at 10x? | Financial model, operational plan | LTV:CAC > 3:1, CAC payback < 12 months |

**Kill criteria (any of these = kill or pivot):**
- 3 consecutive experiments fail to move the target metric
- Users say they want it but don't use it when built (revealed preference)
- Unit economics don't work even with optimistic assumptions
- Market timing is wrong (too early/too late) based on adoption signals

### 4. MVP scoping

**Minimum Viable Product = the smallest thing you can build that lets you test your riskiest assumption with real users.**

**MVP is NOT:**
- A crappy version of the full product
- Phase 1 of a 5-phase plan
- A prototype (prototypes test usability, MVPs test value)
- A feature list with checkboxes

**MVP scoping exercise:**
1. List all features in the "full vision"
2. For each: is this required for users to get core value? Yes/No
3. For each "Yes": can we fake it, do it manually, or use an existing tool? (Wizard of Oz)
4. What's left is the MVP. If it's still > 4 weeks of work, cut more.

**MVP types:**
| Type | Description | Best For | Example |
|------|-------------|----------|---------|
| **Wizard of Oz** | Looks automated, human behind the scenes | Service businesses, early SaaS | Zappos (manual shoe fulfillment) |
| **Concierge** | Full manual service for a few users | High-touch, complex products | Food delivery (founder delivers) |
| **Landing Page** | Describe the product, measure signups | Demand validation | Buffer (pricing page before product) |
| **Single Feature** | Build one feature extremely well | Platform/tool products | Slack (just messaging, nothing else) |
| **Piecemeal** | Combine existing tools to deliver value | Budget constraints | Groupon (WordPress + PayPal + PDF) |

### 5. Backlog grooming

**Weekly grooming cadence:**
1. Review items added since last grooming (5 min)
2. For each new item: does it connect to a current outcome/OKR? If no, park it. (5 min)
3. Score top items by RICE or ICE (10 min)
4. Verify top 5 items have clear acceptance criteria (5 min)
5. Remove/archive anything older than 90 days that hasn't been prioritized (5 min)

**RICE scoring:**

| Factor | Definition | Scale |
|--------|-----------|-------|
| **Reach** | How many users affected per quarter? | Number of users |
| **Impact** | How much will it move the target metric? | 0.25 (minimal) to 3 (massive) |
| **Confidence** | How sure are we about reach and impact? | 0.5 (low) to 1.0 (high) |
| **Effort** | Person-weeks to ship | Number (lower = better) |

**RICE Score = (Reach x Impact x Confidence) / Effort**

## Commands

| Command | Description |
|---------|-------------|
| `/roadmap` | Design an outcome-based roadmap — themes, timeframes (Now/Next/Later), success metrics |
| `/discovery` | Run a discovery cycle — define outcome, map opportunities, generate solutions, design assumption tests |
| `/ost` | Build an Opportunity Solution Tree for a specific outcome |
| `/okr-cascade` | Create OKR cascade from company mission to team-level key results with alignment map |
| `/prioritize` | Prioritize a backlog using RICE, ICE, or DHM — input list, output ranked list with scores |
| `/mvp-scope` | Scope an MVP — from full vision to minimum viable product with build timeline |
| `/hypothesis-test` | Structure a product hypothesis and experiment design — "We believe [change] will cause [effect] for [users]. We'll know when [metric] moves by [amount] within [timeframe]." |
| `/backlog-groom` | Guided backlog grooming session — review, score, prune, prioritize |
| `/stage-gate` | Run a stage-gate decision — gather evidence, evaluate against criteria, recommend continue/pivot/kill |
| `/user-interview-prep` | Design a user interview guide — questions, structure, do's and don'ts, synthesis template |
| `/nsm-define` | Define North Star Metric, input metrics tree, and guardrail metrics for a product |
| `/prd` | Generate a Product Requirements Document — problem, users, requirements, success metrics, constraints |
| `/build-trap` | Diagnose if a team/company is in the build trap — checklist, evidence, escape plan |
| `/dhm` | Score features/initiatives on Biddle's DHM (Delight, Hard-to-copy, Margin-enhancing) |
| `/pre-mortem` | Run a Doshi-style pre-mortem — "imagine this failed, why?" — surface risks before committing |
| `/sprint-plan` | Plan a sprint — select from prioritized backlog, define sprint goal, estimate, assign |

## Output template

```markdown
---
project: <product name>
date: <YYYY-MM-DD>
type: product-management
framework: <cagan|torres|perri|doshi|combined>
---

# Product Management — <Topic>

## Context
- Product: ...
- Stage: Idea / Prototype / MVP / PMF / Growth / Mature
- Team: ...
- Current metrics: ...
- Strategic context: ...

## Discovery

### Desired Outcome
<The metric we want to move and by how much>

### Opportunity Solution Tree
```
Outcome: <metric>
    |
    +-- Opportunity: <user need>
    |       +-- Solution: <approach>
    |       +-- Solution: <approach>
    +-- Opportunity: <user need>
            +-- Solution: <approach>
```

### User Research Summary
- Interviews conducted: ...
- Key insights:
  1. ...
  2. ...
  3. ...
- Patterns: ...

### Riskiest Assumptions
| Assumption | Risk Level | Test Design | Result |
|-----------|-----------|-------------|--------|
| ... | Critical | ... | ... |
| ... | High | ... | ... |

## Prioritization

### DHM Analysis
| Feature | Delight | Hard-to-copy | Margin | Total | Decision |
|---------|---------|-------------|--------|-------|----------|
| ... | ... | ... | ... | ... | Build / Defer / Kill |

### RICE Ranked Backlog
| # | Feature | Reach | Impact | Confidence | Effort | RICE | Status |
|---|---------|-------|--------|-----------|--------|------|--------|
| 1 | ... | ... | ... | ... | ... | ... | ... |

## Roadmap

### Now (This Sprint/Month)
| Theme | Outcome | Metric | Target |
|-------|---------|--------|--------|
| ... | ... | ... | ... |

### Next (Next 1-3 Months)
| Theme | Outcome | Metric | Target |
|-------|---------|--------|--------|
| ... | ... | ... | ... |

### Later (3-6 Months)
| Theme | Outcome | Metric | Target |
|-------|---------|--------|--------|
| ... | ... | ... | ... |

## MVP Specification (if applicable)
### Core value proposition
<One sentence>

### Must-have features (launch blockers)
1. ...

### Nice-to-have (post-launch)
1. ...

### Explicitly excluded (not this MVP)
1. ...

### Build estimate
<X person-weeks>

## Stage-Gate Decision
- **Gate:** G0 / G1 / G2 / G3 / G4
- **Evidence reviewed:** ...
- **Decision:** Continue / Pivot / Kill
- **Rationale:** ...
- **Conditions for next gate:** ...

## Product Hypothesis
> We believe **<change>** will cause **<effect>** for **<users>**.
> We'll know this is true when **<metric>** moves by **<amount>** within **<timeframe>**.

## Pre-mortem (Top Risks)
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ... | ... | ... | ... |

## Next Steps
- [ ] ...
```

## Save location

- Product strategy → `05 - Claude - IA/Outputs/YYYY-MM-DD - Product - <Topic>.md`
- PRDs → `05 - Claude - IA/Outputs/YYYY-MM-DD - PRD - <Feature Name>.md`
- Roadmaps → `05 - Claude - IA/Outputs/YYYY-MM-DD - Roadmap - <Product>.md`
- Discovery reports → `05 - Claude - IA/Outputs/YYYY-MM-DD - Discovery - <Topic>.md`
- MVP specs → `05 - Claude - IA/Outputs/YYYY-MM-DD - MVP Spec - <Product>.md`

## Integration points

| Skill | Relationship |
|-------|-------------|
| `dario-c-level` | CEO/CTO provide strategic context; product management translates strategy into roadmap |
| `dario-data` | Data squad provides metrics, AARRR analysis, NSM definition — shared with product decisions |
| `dario-product` | `dario-product` handles PRDs, user stories, sprint planning at execution level; this skill handles strategy and discovery |
| `dario-offer` | Offer design informs pricing and packaging decisions in product |
| `dario-pipeline` | Sales pipeline feedback reveals product gaps and feature requests |
| `dario-brand` | Brand positioning constrains product messaging and positioning |
| `dario-saas-metrics` | SaaS metrics inform stage-gate decisions and scaling readiness |
| `dario-financial-model` | Financial model validates unit economics for product decisions |
| `dario-ai-engineering` | AI engineering implements AI features that product defines |
| `dario-diagnose` | Diagnostic identifies product opportunities in new client engagements |
| `dario-sop` | SOPs generated for product processes (grooming, discovery cadence, sprint rituals) |
| `dario-obsidian-save` | All outputs saved to vault |

## Red flags / anti-patterns

- **Building without discovery** — shipping features without talking to users is the definition of the build trap. At minimum: 1 user interview per week, every week, no exceptions. If you don't have time for discovery, you don't have time to build the wrong thing twice.
- **Roadmap as promise** — a roadmap is a strategic communication tool, not a contract. Putting specific features with specific dates on a roadmap and then being surprised when they change is organizational dysfunction. Use Now/Next/Later with outcomes, not Gantt charts with feature names.
- **HiPPO-driven decisions** — the Highest Paid Person's Opinion is not evidence. If the CEO says "build X," the PM's job is to ask "what problem does X solve?" and validate that problem with users before committing engineering time.
- **Feature parity as strategy** — "competitor X has feature Y, so we need it too" is not product strategy. It's a race to mediocrity. Ask instead: "What can we do that competitors cannot?" (Doshi's Hard-to-copy dimension).
- **MVP that isn't minimum** — if the MVP takes more than 4-6 weeks to build, it's not minimum. Cut scope until it hurts. The goal is to learn, not to launch a polished product. You can always add more after you validate.
- **Prioritization theater** — scoring features with RICE/ICE and then ignoring the scores to build what the loudest stakeholder wants. If you're going to override the framework, at least document why. Repeated overrides mean the framework is wrong or the organization is.
- **No kill criteria** — every initiative needs explicit conditions under which it will be killed. Without kill criteria, zombie projects consume resources indefinitely. "We've invested too much to stop" is the sunk cost fallacy, not a strategy.
- **Vanity features** — features that look impressive in demos but don't move the NSM. Before building, ask: "Which metric does this move?" If the answer is unclear, the feature probably shouldn't be built.
- **Confusing output with outcome** — "We shipped 47 features this quarter" is output. "We increased activation from 15% to 32%" is outcome. Empowered product teams are measured on outcomes. Feature factories are measured on output.
- **Discovery without synthesis** — conducting 20 user interviews and then not synthesizing patterns into opportunities is research theater. Every interview must be synthesized within 48 hours and connected to the Opportunity Solution Tree.

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Contexto do produto mapeado (stage + métricas reais)

- [ ] Stage do produto identificado: ideia / protótipo / MVP / PMF / crescimento / maduro
- [ ] NSM (North Star Metric) ou proxy definido com valor actual, não hipotético
- [ ] Utilizadores identificados com segmento concreto (não "utilizadores genéricos")
- [ ] Pelo menos uma métrica de negócio citada (activation rate, churn, ARR, DAU…)

❌ NOT delivery-ready: "O produto está numa fase inicial e tem alguns utilizadores."
✅ Delivery-ready: "LUSOconta — MVP lançado Q1 2025, 340 contas criadas, activation rate 38 %, NSM = transações completadas por conta/mês (actual: 2.1)."

---

### Gate 2 — Os 4 Risks de Cagan abordados antes de recomendar build

- [ ] Risco de Value: evidência de que utilizadores querem isto (interview quotes, demand test, waitlist)
- [ ] Risco de Usability: testado com protótipo ou usability session (não assumido)
- [ ] Risco de Feasibility: validado com tech lead ou spike (não "parece simples")
- [ ] Risco de Business Viability: alinhamento com estratégia, legal, margens confirmado

❌ NOT delivery-ready: "Vamos construir a feature de exportação PDF porque o cliente pediu."
✅ Delivery-ready: "Exportação PDF — Value: 6/8 entrevistados mencionaram espontaneamente; Usability: protótipo testado com 3 utilizadores, 0 bloqueios; Feasibility: spike 4h — biblioteca pdfmake suporta caso; Viability: sem implicações RGPD adicionais."

---

### Gate 3 — Opportunity Solution Tree (OST) com outcome raiz real

- [ ] Outcome raiz é uma métrica movível, não uma feature ou iniciativa
- [ ] Mínimo 2 oportunidades mapeadas com framing em necessidade do utilizador
- [ ] Cada oportunidade tem ≥ 2 soluções alternativas (não solução única pré-decidida)
- [ ] Pelo menos 1 assumption test identificado por solução top-candidate

❌ NOT delivery-ready: "Queremos melhorar a app. Oportunidade: adicionar notificações. Solução: push notifications."
✅ Delivery-ready: "Outcome raiz: aumentar retention D30 de 22 % → 35 % (Atelier AI, Q2 2025). Oportunidade A: utilizadores esquecem de voltar à plataforma (n=5 entrevistas). Sol. A1: digest semanal por email — assumption test: envio manual a 50 users semana que vem. Sol. A2: in-app reminder no login — assumption test: interceptar 20 % dos logins com modal."

---

### Gate 4 — Roadmap orientado a outcomes, não lista de features com datas

- [ ] Itens do roadmap formulados como problema/outcome a resolver, não como feature descrita
- [ ] Priorização usa critério explícito (DHM score, ICE, RICE, LNO — não feeling ou HiPPO)
- [ ] "Continue / Pivot / Kill" aplicado a itens com evidência associada
- [ ] Horizonte temporal honesto: Now / Next / Later (não waterfall com datas precisas para tudo)

❌ NOT delivery-ready: "Q2: Dashboard v2, Q3: Integrações, Q4: Mobile app, Q1 26: AI features."
✅ Delivery-ready: "Now (Q2 2025): Reduzir time-to-first-value < 5 min — DHM score 8/10 (Delight: onboarding friction é o bloqueio #1; Hard-to-copy: 6/10; Margin: elimina suporte manual = €1.2k/mês). Next (Q3): Aumentar expansão de conta — hipótese a validar. Later: Integrações contabilísticas — dependente de PMF confirmado."

---

### Gate 5 — Build Trap diagnosticada (se aplicável) ou descartada com evidência

- [ ] Avaliado se equipa está a ser medida por output (features) ou por outcome (métricas)
- [ ] Identificado se PM está a funcionar como project manager vs product leader
- [ ] Backlog tem critério de saída (o que justifica remover ou matar um item)
- [ ] Product Kata aplicado: estado actual → estado desejado → obstáculo → próximo passo experimental

❌ NOT delivery-ready: "Temos 87 itens no backlog e vamos priorizar por votação da equipa."
✅ Delivery-ready: "SAQUEI — diagnóstico Build Trap: equipa reporta 12 features shipped em Q1, mas DAU manteve-se flat (1 240 → 1 255). Recomendação: congelar backlog, correr 3 discovery sprints. Obstáculo identificado: stakeholders pedem estimativas de entrega antes de validação. Próximo passo: instaurar weekly interview habit + OST partilhado com stakeholders."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder

- [ ] Nome do cliente/produto aparece no output (não "\<company\>", "\<product\>", "\<metric\>")
- [ ] Datas, números e nomes de agentes são verificáveis ou explicitamente marcados como hipótese
- [ ] Nenhum bloco de exemplo contém `[INSERT X]`, `TBD`, ou `X%` sem valor atribuído
- [ ] Se dados reais não existem, output marca explicitamente "hipótese a validar" com método de teste

❌ NOT delivery-ready: "A \<empresa\> deve aumentar a sua \<métrica\> de \<valor atual\> para \<valor alvo\>."
✅ Delivery-ready: "Cuidai deve aumentar retenção de cuidadores activos de 61 % (Março 2025) para 75 % até Junho 2025 — hipótese a validar via cohort analysis após onboarding redesign."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados reais do cliente / fontes citadas
- 🟡 **assumed** — plausível com base no contexto, mas precisa de confirmação do cliente antes da entrega
- 🟢 **projection** — forecast ou estimativa por design (não verificável até execução)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verificação. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "A activation rate actual é 34%, o MVP deve estar pronto em 6 semanas, e o segmento principal são PMEs com 10–50 colaboradores."
*(reader assume tudo verified — nenhum label, nenhuma fonte, expectativas infladas)*

✅ Delivery-ready:
> - 🔵 **verified** — Framework DHM (Biddle) aplicado conforme documentado em `dario-rag` (Delight / Hard-to-copy / Margin-enhancing)
> - 🟡 **assumed** — Activation rate estimada em ~30–35% com base no estágio MVP declarado; cliente deve confirmar métrica real antes de definir OKR de activation
> - 🟡 **assumed** — Segmento-alvo "PMEs SaaS B2B, 10–50 seats" inferido do contexto LUSOconta — confirmar ICP antes de priorizar roadmap Q3
> - 🟢 **projection** — Se hipótese de value risk validada em 3 user interviews, estima-se redução de churn em 8–12 pp no ciclo seguinte (Torres: assumption testing → experiment design)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumptions com actuals (activation rate real, ICP validado, métricas NSM actuais)
- [ ] All 🔵 citations added — RAG source confirmada para cada framework citado (Cagan, Torres, Perri, Doshi, Rachitsky, Biddle)
- [ ] All 🟢 projections labeled as such ao cliente — expectativas de forecast explicitamente comunicadas como estimativas, não garantias

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Product Review — LUSOconta | Q2 2025 Planning

**Produto:** LUSOconta (SaaS contabilidade para freelancers PT)
**Stage:** MVP → PMF (lançado Outubro 2024)
**Data da review:** 15 Maio 2025
**PM responsável:** Dario (via Atelier AI squad)

---

## North Star Metric
**Transações categorizadas correctamente por conta/mês**
Actual: 4.2 | Target Q2: 7.0 | Benchmark sector (Lenny 2024): 6–9 para SaaS fintech SMB

---

## Estado das métricas-chave (Abril 2025)
| Métrica | Valor actual | Benchmark | Gap |
|---|---|---|---|
| Activation rate (D7) | 38 % | 45 % (P50 fintech) | −7 pp |
| Retention D30 | 29 % | 35 % (P50 SaaS) | −6 pp |
| Time-to-first-value | 11 min | < 5 min (best-in-class) | +6 min |
| NPS | 34 | 40 (bom SaaS) | −6 |

---

## Diagnóstico: Build Trap Assessment
- Últimos 90 dias: 9 features shipped, NSM moveu +0.3 (flat)
- Equipa medida por "features entregues a tempo" → **feature team mode activo**
- Backlog tem 94 itens, sem critério de saída, último grooming: 6 semanas atrás
- **Veredito: Build Trap confirmado. Acção imediata necessária.**

---

## Opportunity Solution Tree — Q2 2025

**Outcome raiz:** Aumentar time-to-first-value de 11 min → < 5 min
(proxy de activation rate D7 de 38 % → 45 %)

```
Outcome: Time-to-first-value < 5 min
    |
    +-- Oportunidade A: Utilizadores bloqueiam na ligação bancária (n=7/10 entrevistas)
    |       +-- Sol. A1: Open Banking pré-configurado para CGD/BPI/Novo Banco
    |       |       Assumption: utilizadores têm conta nestes 3 bancos → validar via sign-up survey
    |       +-- Sol. A2: Import manual CSV com template guiado
    |               Assumption: utilizadores têm CSV disponível → testar com 20 users semana 1
    |
    +-- Oportunidade B: Categorização inicial confusa — utilizadores não sabem o que fazer (n=4/10)
            +-- Sol. B1: Checklist de onboarding com 3 passos obrigatórios
            +-- Sol. B2: Modo "guiado" com tooltips contextuais
                    Assumption test: protótipo Figma → 5 usability sessions esta semana
```

---

## Validação dos 4 Risks — Sol. A1 (Open Banking pré-configurado)

| Risk | Status | Evidência |
|---|---|---|
| Value | ✅ Validado | 7/10 entrevistas mencionaram ligação bancária como bloqueio principal |
| Usability | 🟡 Em teste | Protótipo v2 em usability test com 3 utilizadores (resultados: 22 Mai) |
| Feasibility | ✅ Validado | Spike 6h com Nuno (CTO): Salt Edge API suporta CGD/BPI/NB, 3 semanas dev |
| Viability | ✅ Validado | RGPD: consentimento explícito já no fluxo; custo Salt Edge: €0.08/conexão |

---

## Roadmap Q2–Q3 2025 (outcome-driven)

### Now (Mai–Jun 2025)
**Problema:** Time-to-first-value demasiado alto bloqueia activation
- Iniciativa: Open Banking onboarding (Sol. A1)
- DHM Score: Delight 9/10 · Hard-to-copy 7/10 · Margin 8/10 → **Total: 8.0**
- Stage-gate: se activation D7 ≥ 43 % até 30 Jun → continuar para expansão bancária

### Next (Jul–Set 2025)
**Problema:** Retenção D30 abaixo de benchmark — utilizadores não constroem hábito
- Hipótese a validar: digest semanal de "saúde fiscal" aumenta logins recorrentes
- Método: A/B test email vs controlo, n=200 por grupo, 6 semanas
- Critério de pivot: se D30 não move +3 pp → explorar Oportunidade B (onboarding guiado)

### Later (Q4 2025+)
- Integrações contabilísticas (TOC/ROC export): **dependente de PMF confirmado** (NPS ≥ 45)
- Mobile app: **kill temporário** — 94 % acessos são desktop (dados Mixpanel Abril 2025)

---

## Continue / Pivot / Kill — Backlog Review (Top 5)

| Item | Decisão | Justificação |
|---|---|---|
| Relatórios PDF personalizados | ✅ Continue | 6/8 entrevistas, DHM 7.5 |
| Dark mode | ❌ Kill | 0 menções em 10 entrevistas, DHM 2.0 |
| Multi-empresa por conta | 🔄 Pivot | Necessidade real mas scope errado — reduzir para "sub-perfis" |
| Notificações push mobile | ⏸ Later | Mobile < 6 % tráfego; reavaliar Q4 |
| Integração Sage | 🔄 Pivot | Pedido por 2 enterprise leads — criar waitlist, não build agora |

---

**Próximos passos imediatos (esta semana):**
1. Dario agenda 3 usability sessions protótipo Open Banking (até 19 Mai)
2. Nuno confirma estimativa final Salt Edge integration (até 16 Mai)
3. Backlog freeze — 94 itens em revisão com novo critério DHM mínimo 5.0
```

---

## Output anti-patterns

- **Roadmap como lista de features com datas** — "Q3: Dashboard v2, Q4: Integrações" sem outcome associado nem critério de sucesso
- **4 Risks ignorados** — recomendar build sem validar value, usability, feasibility e viability, mesmo que brevemente
- **OST com solução única** — árvore com uma oportunidade e uma solução é decisão disfarçada de discovery
- **Stage-gate sem critério de saída** — "vamos ver como corre" não é uma decisão de Continue/Pivot/Kill
- **Métricas sem benchmark** — "retention de 29 %" sem contexto de sector/stage não permite decisão
- **Build Trap não diagnosticada** — output foca em como priorizar features sem perguntar se a equipa está a ser medida por outcomes
- **NSM inventada** — North Star Metric definida sem dados actuais nem método de medição identificado
- **Backlog grooming sem critério de kill** — listar itens e ordenar por importância sem definir o que sai do backlog
- **DHM score sem componentes** — dar um número final sem detalhar Delight / Hard-to-copy / Margin separadamente
- **Placeholders no output** — "\<inserir métrica\>", "\<empresa\>", "X %" entregues ao cliente sem substituição por dados reais ou hipóteses explicitamente marcadas
