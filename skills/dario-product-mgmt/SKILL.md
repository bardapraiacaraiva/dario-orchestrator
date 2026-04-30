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
