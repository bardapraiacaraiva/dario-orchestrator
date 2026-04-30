---
name: dario-movement
description: Movement building squad -- analyzes cultural phenomena, builds brand movements, creates tribal identity, writes manifestos, designs community flywheels, and measures movement impact. Uses Ostrom commons governance, network theory, ritual studies, and DAO-inspired coordination. Triggers on "movement", "movimento", "community", "comunidade", "manifesto", "tribe", "tribo", "flywheel", "community building", "brand movement", "cultural movement", "tribal marketing".
version: 1.0.0
license: MIT
---

# DARIO Skill -- Movement Building

Transforms brands from vendors into movements. Analyzes cultural phenomena, architects tribal identity, writes manifestos, designs community flywheels, and measures movement health. Seven specialist agents collaborate to build something people join, not just buy from.

## When to activate

- Brand wants to become a movement (not just a business)
- Community building strategy needed
- Manifesto or declaration of beliefs required
- Cultural phenomenon analysis (why is X blowing up?)
- Tribal identity architecture (us vs them, shared language, rituals)
- Community engagement is stagnant ("people sign up but don't participate")
- Brand needs a cause larger than its product
- After `dario-brand` (brand identity exists, now build the tribe around it)
- Before `dario-content` (movement narrative informs all content)
- DAO or decentralized community governance design

## Squad roster

| Agent | Role | Focus |
|---|---|---|
| **Movement Chief** | Orchestrator | Routes tasks, resolves conflicts, ensures coherence across all movement elements |
| **Movement Architect** | Systems designer | Community flywheel, governance structures, platform architecture, growth loops |
| **Fenomenologo** | Cultural analyst | Analyzes why phenomena emerge, spread, and either sustain or collapse |
| **Identitario** | Identity architect | Tribal symbols, language, rituals, us/them boundaries, belonging mechanics |
| **Estrategista de Ciclo** | Lifecycle strategist | Movement phases (spark to institution), timing, scaling without diluting |
| **Manifestador** | Manifesto writer | Declarations, belief statements, founding documents, narrative anchors |
| **Analista de Impacto** | Impact measurer | Community health metrics, network analysis, sentiment tracking, cohort behavior |

## Workflow

### 1. Gather inputs

- **Brand/project** (name, what it does, who it serves)
- **Current community** (size, platforms, engagement level, existing assets)
- **Founder beliefs** (what they stand for, what they stand against)
- **Cultural context** (industry trends, frustrations, unmet desires in the market)
- **Competitive landscape** (other communities or movements in the space)
- **Resources** (team capacity for community management, budget, platforms available)
- **Desired outcome** (awareness, retention, advocacy, governance, all of the above)

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "movement building community flywheel tribal identity", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "manifesto anatomy brand beliefs declaration", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ostrom commons governance community rules", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "network theory viral spread cultural phenomenon", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ritual studies belonging identity tribal formation", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "DAO decentralized governance token community", collection: "dario", limit: 5)
```

### 3. Diagnose -- Phenomenon analysis (Fenomenologo)

Before building, understand the cultural forces at play:

#### Cultural landscape scan

1. **What tension exists?** -- Every movement is born from a tension between how things are and how they should be
2. **Who feels this tension most?** -- The early adopters, the frustrated, the underserved
3. **What language do they already use?** -- The organic vocabulary of the frustrated (forums, Reddit, Twitter, reviews)
4. **What failed attempts exist?** -- Previous movements or communities that tried and died (learn from their collapse)
5. **What adjacent movements succeeded?** -- Patterns to borrow from neighboring cultural territories

#### Phenomenon viability assessment

| Factor | Score (1-10) | Evidence |
|---|---|---|
| **Tension intensity** | | How painful is the status quo? |
| **Population density** | | How many people feel this tension? |
| **Articulation gap** | | Can they name their frustration, or is it vague? |
| **Existing gathering** | | Are they already clustering somewhere (online/offline)? |
| **Enemy clarity** | | Is there a clear "old way" or adversary to rally against? |
| **Transformation promise** | | Can joining the movement change their identity? |

**Viability score** = sum / 60. Above 0.7 = strong foundation. Below 0.4 = premature.

### 4. Build -- Community flywheel (Movement Architect)

The core engine of any sustainable movement:

```
    ┌──────────┐
    │ ATTRACT  │  Draw people in with the manifesto + founding story
    │          │  Channels: content, events, word of mouth, PR
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │  ENGAGE  │  Give them something meaningful to DO (not just consume)
    │          │  Actions: challenges, contributions, discussions, projects
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │ EMPOWER  │  Elevate members to leaders / ambassadors / creators
    │          │  Roles: mentors, moderators, local chapter leads, speakers
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │CELEBRATE │  Recognize and amplify member achievements publicly
    │          │  Rituals: spotlights, awards, milestones, annual gathering
    └────┬─────┘
         │
         └──── feeds back to ATTRACT (members bring others)
```

#### Flywheel design checklist

For each phase, define:

| Phase | Mechanism | Metric | Owner |
|---|---|---|---|
| **Attract** | How do outsiders discover the movement? | New member rate, referral source | |
| **Engage** | What is the first meaningful action for a new member? | Activation rate (% who take action in first 7 days) | |
| **Empower** | How do engaged members level up? | % members in leadership/creator roles | |
| **Celebrate** | How are achievements recognized? | Recognition frequency, member sentiment | |

#### Governance framework (Ostrom-inspired)

Elinor Ostrom's 8 principles for governing the commons, adapted for brand communities:

1. **Clear boundaries** -- Who is a member? What defines "in" vs "out"?
2. **Proportional equivalence** -- Benefits match contributions (more you give, more you get)
3. **Collective choice** -- Members have voice in rules that affect them
4. **Monitoring** -- Community behavior is observable (not anonymous chaos)
5. **Graduated sanctions** -- Violations have proportional consequences (warning before ban)
6. **Conflict resolution** -- Low-cost, accessible dispute resolution mechanism
7. **Local autonomy** -- Sub-groups can self-organize within shared principles
8. **Nested governance** -- Multiple layers (local chapters, regional, global) for scale

### 5. Create identity (Identitario)

#### Identity architecture

Every movement needs these identity elements:

**1. Sacred narrative** -- The origin story that explains WHY this movement exists
- What was the breaking point?
- Who was the first person to say "enough"?
- What did they do differently?

**2. Enemy / old way** -- What the movement stands AGAINST
- Not a person (avoid personal attacks)
- A system, mindset, or practice
- Must be real and recognized by the audience
- Example: Basecamp vs "hustle culture"; Patagonia vs "disposable consumption"

**3. Promised land** -- The vision of how things SHOULD be
- Specific enough to feel real
- Ambitious enough to inspire
- Achievable enough to believe
- Example: "A world where every small business has enterprise-level marketing"

**4. Tribal language** -- Words and phrases only insiders use
- Neologisms (new terms coined by the movement)
- Redefined terms (common words given new meaning)
- Insider acronyms and shorthand
- Example: CrossFit's "WOD", "AMRAP", "box" (not gym)

**5. Visual markers** -- How members visually identify each other
- Logo / symbol (not just the brand logo -- a movement symbol)
- Colors associated with the cause
- Merchandise, stickers, badges
- Digital equivalents (profile frames, avatars, badges)

**6. Rituals** -- Repeated practices that reinforce belonging
- Daily: check-in, gratitude post, accountability share
- Weekly: community call, challenge, roundup
- Monthly: spotlight, awards, retrospective
- Annual: summit, anniversary, founding day celebration

**7. Rites of passage** -- Milestones that mark progression
- Entry ritual (welcome sequence, first contribution, introduction post)
- Level-up moments (first 100 days, first leadership role, first mentee)
- Graduation / mastery (recognized expert, alumni status, speaker invite)

### 6. Write manifesto (Manifestador)

#### 7-component manifesto anatomy

Every manifesto follows this structure:

```
1. DECLARATION    -- The bold opening statement (what we believe)
2. INDICTMENT     -- What is broken in the world (the problem)
3. VISION         -- What we are building instead (the promised land)
4. PRINCIPLES     -- The non-negotiable values (3-7 core beliefs)
5. INVITATION     -- The call to join (not sell -- invite)
6. COMMITMENT     -- What members pledge (the social contract)
7. SIGNATURE      -- The founding moment (date, founder, first signatories)
```

#### Manifesto writing rules

- Write in first person plural ("We believe..." not "The company believes...")
- Use short, punchy sentences (manifesto is spoken aloud, not read silently)
- Include specific enemies and specific visions (no generic "make the world better")
- Maximum 500 words for the core manifesto (1 page, large font, frameable)
- Every sentence must pass the "would someone tattoo this?" test for conviction
- End with an invitation, not a sales pitch

#### Manifesto template

```markdown
# [Movement Name] Manifesto

## We believe...
[2-3 sentences: the core belief that started everything]

## The world told us...
[2-3 sentences: the status quo, the old way, the lie we were sold]

## But we know...
[2-3 sentences: the truth that the movement has discovered]

## We stand for:
1. [Principle 1] -- [one-line explanation]
2. [Principle 2] -- [one-line explanation]
3. [Principle 3] -- [one-line explanation]
4. [Principle 4] -- [one-line explanation]
5. [Principle 5] -- [one-line explanation]

## We are building...
[2-3 sentences: the vision of the promised land]

## If you believe what we believe...
[2-3 sentences: the invitation to join -- what to do next]

## Our pledge:
[1-2 sentences: what the movement commits to every member]

---
Founded [date] by [founder/founding group]
[Movement name or symbol]
```

### 7. Movement lifecycle (Estrategista de Ciclo)

Every movement passes through phases. Misdiagnosing the current phase leads to wrong tactics.

| Phase | Duration | Focus | Danger |
|---|---|---|---|
| **1. Spark** | 0-6 months | Founder story, manifesto, first 50 true believers | Trying to scale before product-market-fit equivalent |
| **2. Kindling** | 6-18 months | First rituals, identity markers, 50-500 members | Founder burnout, inconsistent engagement |
| **3. Flame** | 18-36 months | Community leaders emerge, flywheel turns on its own | Losing control of narrative, toxic members |
| **4. Fire** | 3-5 years | Movement has its own momentum, media picks up | Dilution ("everyone claims to be part of it") |
| **5. Institution** | 5+ years | Formal structures, governance, legacy planning | Bureaucracy kills the original energy |

#### Phase-appropriate tactics

**Spark:** Do things that do not scale. Personal invitations. Handwritten notes. 1-on-1 conversations. The founder IS the movement.

**Kindling:** Create the first repeatable ritual. Find 3-5 community leaders (not employees -- genuine believers). Document the tribal language as it emerges organically.

**Flame:** Systematize the flywheel. Publish the governance charter. Create the leadership pipeline. Start saying no to people who want to join but do not share the values.

**Fire:** Protect the core identity while allowing local adaptation. Write the "brand movement guidelines." Launch the annual gathering. Consider organizational structure.

**Institution:** Separate the movement from the founder (must survive beyond them). Create succession planning. Archive the history. Endow the principles.

### 8. Measure impact (Analista de Impacto)

#### Movement health metrics

| Category | Metric | Healthy range | Warning |
|---|---|---|---|
| **Growth** | New members / month | Steady 5-15% MoM | Spikes without retention = vanity |
| **Activation** | % new members who act in first 7 days | > 40% | Below 20% = broken onboarding |
| **Engagement** | Monthly active members / total members | > 30% | Below 10% = ghost town |
| **Depth** | Avg. contributions per active member | > 3/month | 1 or less = passive consumption |
| **Leadership** | % members in leadership/mentor roles | 3-8% | Below 1% = founder dependency |
| **Retention** | 90-day cohort retention | > 50% | Below 25% = leaky bucket |
| **Advocacy** | NPS or referral rate | NPS > 50 | NPS < 20 = dissatisfaction |
| **Sentiment** | Positive sentiment in discussions | > 70% | Below 50% = cultural problem |
| **Network density** | Connections per member (not just to center) | > 3 | 1 = hub-spoke (fragile) |

#### Network topology analysis

- **Hub-spoke** (fragile): All connections through the founder/brand. If the hub fails, the network collapses. Common in Phase 1-2.
- **Multi-hub** (resilient): Several community leaders each with their own cluster. Information and energy flow through multiple paths. Target for Phase 3+.
- **Mesh** (antifragile): Members connect to each other independently. The movement has its own life. The ultimate goal for Phase 4-5.

## Commands

| Command | Description | Output |
|---|---|---|
| `/movement:analyze-phenomenon` | Cultural phenomenon analysis | Viability assessment + tension map + spreading mechanics |
| `/movement:build-movement` | Full movement architecture | Flywheel + governance + identity + lifecycle roadmap |
| `/movement:create-identity` | Tribal identity design | 7-element identity architecture document |
| `/movement:diagnose` | Movement health diagnostic | Current phase + health metrics + recommendations |
| `/movement:measure-impact` | Impact measurement framework | Metrics dashboard + network analysis + cohort tracking |
| `/movement:review` | Review existing movement/community | Audit scorecard + gap analysis + improvement plan |
| `/movement:write-manifesto` | Write a movement manifesto | 7-component manifesto document |

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: movement-blueprint
phase: <spark|kindling|flame|fire|institution>
---

# Movement Blueprint -- <Movement Name>

## Executive Summary
- Movement thesis: [one sentence -- what we believe and why it matters]
- Current phase: [spark/kindling/flame/fire/institution]
- Community size: [current] -> [12-month target]
- Key metric: [the ONE number that matters most right now]

## Cultural Landscape
### The tension
[What is broken? Who feels it? How intensely?]

### Viability assessment
| Factor | Score | Evidence |
|---|---|---|
| Tension intensity | /10 | ... |
| Population density | /10 | ... |
| Articulation gap | /10 | ... |
| Existing gathering | /10 | ... |
| Enemy clarity | /10 | ... |
| Transformation promise | /10 | ... |
| **Total** | **/60** | |

## Manifesto
[Full 7-component manifesto]

## Identity Architecture
### Sacred narrative
...
### Enemy / old way
...
### Promised land
...
### Tribal language
| Term | Meaning | Usage context |
|---|---|---|
| ... | ... | ... |

### Visual markers
...
### Rituals
| Cadence | Ritual | Description |
|---|---|---|
| Daily | ... | ... |
| Weekly | ... | ... |
| Monthly | ... | ... |
| Annual | ... | ... |

### Rites of passage
| Milestone | Ritual | Recognition |
|---|---|---|
| Entry | ... | ... |
| Level-up | ... | ... |
| Mastery | ... | ... |

## Community Flywheel
### Attract
...
### Engage
...
### Empower
...
### Celebrate
...

## Governance Charter
### Ostrom principles applied
| Principle | Implementation |
|---|---|
| Clear boundaries | ... |
| Proportional equivalence | ... |
| Collective choice | ... |
| Monitoring | ... |
| Graduated sanctions | ... |
| Conflict resolution | ... |
| Local autonomy | ... |
| Nested governance | ... |

## Lifecycle Roadmap
### Current phase: [phase name]
- Status: ...
- Key actions for next 90 days: ...

### Phase transitions
| From | To | Trigger conditions | Timeline |
|---|---|---|---|
| ... | ... | ... | ... |

## Health Metrics Dashboard
| Metric | Current | Target (90d) | Status |
|---|---|---|---|
| New members/month | ... | ... | ... |
| Activation rate | ... | ... | ... |
| MAM ratio | ... | ... | ... |
| Leadership ratio | ... | ... | ... |
| 90-day retention | ... | ... | ... |
| NPS | ... | ... | ... |

## Network Topology
Current: [hub-spoke / multi-hub / mesh]
Target: [multi-hub / mesh]
Actions to evolve: ...

## Next Steps
1. ...
2. ...
3. ...
```

## Scoring rubric -- Movement audit

Overall Movement Health Score (0-100):

| Dimension | Weight | Score range | Assessment |
|---|---|---|---|
| **Narrative clarity** | 20% | 0-20 | Is the manifesto compelling, specific, and shareable? |
| **Identity strength** | 20% | 0-20 | Do members self-identify? Is there tribal language, ritual, and visual markers? |
| **Flywheel health** | 25% | 0-25 | Does the Attract-Engage-Empower-Celebrate loop actually turn? |
| **Governance quality** | 15% | 0-15 | Are rules clear, fair, and enforceable? Do members have voice? |
| **Impact & metrics** | 20% | 0-20 | Are key metrics tracked, healthy, and trending in the right direction? |

**Grading:**
- 85-100: Thriving movement, self-sustaining, ready to scale or institutionalize
- 70-84: Strong foundation, specific growth levers to pull
- 50-69: Movement exists but flywheel is not spinning on its own
- Below 50: Community, not a movement -- needs narrative, identity, and flywheel redesign

## Red flags / anti-patterns

- Movement built around the product instead of around a belief (product movements die when the product becomes obsolete)
- Manifesto that reads like marketing copy ("We are the leading provider of...") instead of a declaration of belief
- No clear enemy or "old way" to rally against (movements need contrast to define themselves)
- Founder as the sole energy source (if the founder stops posting, everything stops)
- Engagement = consumption only (likes, views) with no meaningful member action
- No governance structure (anarchy works for 50 people, chaos for 500)
- Growth prioritized over culture (adding members faster than you can acculturate them)
- Rituals imposed from the top instead of emerging organically and being formalized
- Tribal language that excludes instead of inviting (jargon wall for newcomers)
- Measuring vanity metrics (total members, social followers) instead of depth metrics (activation, retention, NPS)
- No rites of passage (everyone is at the same level forever -- no progression, no aspiration)
- Community platform chosen for the brand's convenience instead of where members naturally gather
- Celebrating the brand/founder instead of celebrating members
- No plan for what happens when the movement succeeds (post-victory identity crisis)

## Integration with other DARIO skills

| Skill | Integration point |
|---|---|
| `dario-brand` | Brand archetype and positioning provide the foundation -- movement extends brand into cause. Always run brand first. |
| `dario-content` | Movement narrative drives all content strategy. Manifesto becomes the editorial north star. |
| `dario-story-circle` | The brand origin story (Story Circle) becomes the movement's sacred narrative. |
| `dario-social` | Social media becomes the primary channel for movement engagement, ritual execution, and celebration. |
| `dario-email-seq` | Onboarding/welcome sequence becomes the entry ritual for new movement members. |
| `dario-funnel` | The funnel's lead magnet can be the manifesto; the community IS the retention mechanism. |
| `dario-offer` | The Grand Slam Offer is for customers; the movement invitation is for believers. Different framing, same people. |
| `dario-pitch` | Investor/partner pitch can leverage movement metrics (engagement, NPS, advocacy) as proof of market pull. |
| `dario-cro` | Community pages, membership signups, and event registrations all benefit from CRO optimization. |

## Save location

`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Movement Blueprint.md`

## Critical rules

- Never build a movement around a product feature -- features change, beliefs endure. The movement must be about a worldview that the product happens to serve, not the other way around
- Never write a manifesto in corporate voice -- if it sounds like it was approved by a legal department, it will inspire nobody. Manifestos are raw, convicted, and human
- Never skip the phenomenon analysis before building -- launching a movement where no cultural tension exists is like lighting a match underwater
- Never prioritize growth over culture -- 100 true believers who recruit others will always outperform 10,000 passive subscribers who joined for a freebie
- Never let the flywheel depend entirely on the founder -- if the movement dies when one person goes on vacation, it is a personal brand, not a movement
- Always define the enemy as a system or practice, never a specific person or competitor -- personal attacks create legal risk and moral weakness
- Always create governance before you need it -- writing community rules during a crisis is reactive and perceived as authoritarian
- Always track network topology, not just member count -- a hub-spoke network of 10,000 is more fragile than a mesh network of 1,000
