---
name: dario-brand
description: Brand positioning workshop — generates brand statement, archetype, messaging hierarchy, and differentiation using Kapferer Prism + Neumeier Zag + StoryBrand SB7 + Aaker. Triggers on "brand", "branding", "posicionamento", "brand strategy", "marca", "archetype", "positioning statement".
license: MIT
---

# DARIO Skill — Brand Strategy

Workshop-in-a-skill: takes a client and produces a complete brand positioning artifact — archetype, positioning statement, messaging hierarchy, differentiation, and voice guide.

## When to activate

- New brand / rebrand project
- Rename / reposition
- "Tudo parece genérico, como nos destacamos?"
- Before writing any brand copy (website, decks, campaigns)
- Before logo/visual identity work (brand first, then visual)

## Workflow

### 1. Gather inputs
- **Business description** (what, who for, how)
- **Current positioning** (if any)
- **3-5 competitors** (real ones)
- **Brand history / origin story**
- **Founder values** (what they believe)
- **Target audience** (not "everyone")
- **Main business model** (B2B, B2C, DTC, SaaS, agency, marketplace)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "kapferer brand identity prism luxury", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "neumeier zag brand onlyness", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "donald miller storybrand sb7 hero guide", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "aaker brand equity positioning", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "byron sharp mental availability distinctiveness", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "yohn heyward archetype naming", collection: "dario", limit: 5)
```

### 3. Archetype selection (Jung / Pearson adaptation)

Pick ONE primary + 1 optional secondary:
- **Innocent** (purity, simplicity) — Dove, Coca-Cola
- **Explorer** (freedom, discovery) — Jeep, Patagonia
- **Sage** (wisdom, truth) — Harvard, Google
- **Hero** (courage, mastery) — Nike, Gillette
- **Outlaw** (revolution, disruption) — Harley, Virgin
- **Magician** (transformation, vision) — Apple, Disney
- **Regular Guy** (belonging, down-to-earth) — IKEA, Budweiser
- **Lover** (intimacy, beauty) — Chanel, Godiva
- **Jester** (joy, fun) — M&Ms, Old Spice
- **Caregiver** (service, compassion) — Johnson's, UNICEF
- **Creator** (innovation, imagination) — LEGO, Adobe
- **Ruler** (control, prosperity) — Rolex, Mercedes

### 4. Apply Neumeier's Zag (Onlyness statement)

Template:
> **<Brand>** is the only **<category>** that **<unique benefit>** for **<target>** who **<problem>** in/at **<when/where>** because **<why>**.

Example (Patagonia-ish):
> Patagonia is the only outdoor apparel company that gives 1% of revenue to environmental groups for outdoor enthusiasts who want to leave the planet better than they found it, because profit without purpose is outdated.

Each slot must be unique — not borrowed from competitors.

### 5. Apply StoryBrand SB7 (Donald Miller)

Map the client's brand as the **GUIDE** (never the Hero). The customer is the Hero.

1. **Character (customer)** — who wants what
2. **Problem (external + internal + philosophical)** — what's in the way
3. **Guide (brand)** — empathetic + authoritative
4. **Plan** — simple steps to success
5. **Call to action** — direct (buy/apply) + transitional (lead magnet)
6. **Success** — what winning looks like
7. **Failure** — what losing looks like (stakes)

### 6. Kapferer Brand Identity Prism

6 facets, interconnected:
- **Physique** (physical attributes, visual)
- **Personality** (character traits)
- **Culture** (values, beliefs)
- **Relationship** (how brand relates to customer)
- **Reflection** (how customer wants to be seen)
- **Self-image** (how customer sees themselves when using the brand)

Fill each facet with 3-5 concrete words or phrases.

### 7. Positioning statement (Aaker/Ries approach)

Short and clear:
> For **<target>** who **<insight/need>**, **<brand>** is the **<category>** that **<key benefit>** because **<reason to believe>**. Unlike **<alternative>**, we **<differentiator>**.

### 8. Messaging hierarchy

- **Tagline** (5-9 words, benefit+twist)
- **Brand promise** (1 sentence, what they'll experience)
- **Elevator pitch** (30s)
- **Value props** (3-5 bullets)
- **Proof points** (evidence for each)
- **Voice attributes** (4 adjectives + "is / is not" table)

### 9. Differentiation test

For each positioning, ask:
- ✅ Is it **specific** (not generic)?
- ✅ Is it **true**? (can deliver)
- ✅ Is it **valuable** to the target?
- ✅ Is it **defensible**? (not easily copied)
- ✅ Is it **memorable**?

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: brand-strategy
archetype: <primary>
---

# Brand Strategy — <Client Name>

## Context & Scope
- Business: ...
- Target: ...
- Competitors: ...
- Ambition: ...

## Archetype
**Primary:** <Archetype>
**Secondary:** <Archetype or none>
**Rationale:** ...

## Onlyness Statement (Neumeier Zag)
<Brand> is the only <category> that <benefit> for <target> who <problem> at <when/where> because <why>.

## Kapferer Brand Prism
| Facet | Content |
|---|---|
| Physique | ... |
| Personality | ... |
| Culture | ... |
| Relationship | ... |
| Reflection | ... |
| Self-image | ... |

## StoryBrand SB7
1. Character (Hero): ...
2. Problem: ...
3. Guide: ...
4. Plan: ...
5. Call to action: ...
6. Success: ...
7. Failure (stakes): ...

## Positioning Statement
For <target> who <insight>, <brand> is the <category> that <key benefit> because <reason to believe>. Unlike <alternative>, we <differentiator>.

## Messaging Hierarchy
### Tagline
<5-9 words>

### Brand Promise
<1 sentence>

### Elevator Pitch (30s)
...

### Value Props (3-5)
1. ...
2. ...

### Proof Points
- [Value prop 1] → <evidence>
- ...

## Voice & Tone
### Voice attributes (4)
- ...

### Is / Is Not
| Is | Is Not |
|---|---|
| ... | ... |

## Differentiation Test
- [x] Specific
- [x] True
- [x] Valuable
- [x] Defensible
- [x] Memorable

## Next Steps
- Visual identity brief (logo, palette, typography, imagery)
- Copy rollout (website, decks, emails)
- Brand guidelines doc
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Brand Strategy.md`

## Red flags / anti-patterns
- Archetype chosen because "it's cool" vs genuinely fitting
- Positioning that says "quality and innovation" (zero differentiation)
- "Unique" claims that competitors also claim
- Customer as Hero is violated (brand plays Hero instead of Guide)
- Voice guide without "is not" examples (leaves ambiguity)
- Brand decision taken without founder values input

## Interactions
- Pairs with `dario-sales-letter` (provides voice + positioning)
- Pairs with `dario-pitch` (provides core narrative)
- Pairs with `dario-offer` (grounds the offer in brand truth)

## Red Flags
- Never skip competitive analysis before defining positioning — without knowing what competitors claim, your "unique" positioning may be identical to three others in the market
- Never select an archetype because it sounds aspirational without evidence it fits — an archetype that contradicts the founder's actual values will collapse under real-world use
- Always validate the brand strategy with the client/founder before any downstream work (copy, design, campaigns) — rebuilding a sales letter or pitch deck because the positioning changed is expensive and avoidable
- Never accept "quality and innovation" as a differentiator — if every competitor can (and does) say the same thing, it differentiates nothing
- Always complete the "Is Not" column in the voice guide — without explicit boundaries, every writer interprets the brand voice differently and consistency breaks down
