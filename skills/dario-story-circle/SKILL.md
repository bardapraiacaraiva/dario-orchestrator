---
name: dario-story-circle
description: Brand story / about page / origin narrative generator using Dan Harmon's Story Circle (8 beats), Campbell's Hero's Journey, and Park Howell's ABT. Produces the brand's core narrative for website, decks, and campaigns. Triggers on "brand story", "origin story", "about page", "story circle", "narrativa", "quem somos", "história da marca".
license: MIT
---

# DARIO Skill — Story Circle

Crafts the brand's core narrative — the story that lives on the About page, opens the pitch deck, anchors the email welcome sequence, and gives the founder something to say in interviews.

## When to activate
- About page writing or redesign
- Brand story for new client
- Founder story for authority building
- Brand video script
- After `dario-brand` (archetype + positioning exist, now need the story)

## Workflow

### 1. RAG consult
```
mcp__dario-rag__search_kb(query: "dan harmon story circle 8 beats", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "joseph campbell heros journey monomyth", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "park howell abt and but therefore", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "matthew dicks five second moment storyworthy", collection: "dario", limit: 5)
```

### 2. Gather story ingredients
- **The founder** — who are they, where did they come from
- **The inciting incident** — what happened that made them start this
- **The struggle** — what was hard, what they almost gave up on
- **The insight** — the "aha moment" that changed everything
- **The mission** — what they now believe and fight for
- **The transformation** — what changed for their customers
- **The proof** — evidence it works (results, testimonials, milestones)

### 3. Apply Dan Harmon's Story Circle (8 beats)

```
    1. YOU (comfort zone)
   /                        \
  8. CHANGE                  2. NEED
  |   (return, transformed)  |   (something is missing)
  |                          |
  7. RETURN                  3. GO
  |   (bring it back)       |   (enter unfamiliar territory)
  |                          |
  6. TAKE                    4. SEARCH
   \  (pay the price)      /   (adapt, struggle)
    5. FIND (the insight)
```

Map the brand story to these 8 beats:
1. **YOU:** Founder in their previous world
2. **NEED:** The gap they noticed, the frustration
3. **GO:** Decision to do something about it (leave comfort)
4. **SEARCH:** Early struggles, failures, learning
5. **FIND:** The breakthrough insight / methodology / product
6. **TAKE:** The cost paid (risk, money, time, reputation)
7. **RETURN:** Bringing the solution to the world (the brand)
8. **CHANGE:** How the founder (and customers) are transformed

### 4. Distill to ABT (And, But, Therefore)
One sentence that captures the whole story:

> **[Founder/Brand] was [doing X] AND [things were Y], BUT [problem/insight], THEREFORE [brand/mission exists].**

### 5. Write 3 versions

#### Version 1: Micro (50 words) — for bios, social media, email signatures
#### Version 2: Medium (200-300 words) — for About page hero, pitch intros
#### Version 3: Full (600-1000 words) — for full About page, brand video script

### 6. StoryBrand integration (if `dario-brand` ran)
Map the brand story to the SB7 framework:
- The CUSTOMER is the Hero (not the founder)
- The BRAND is the Guide (empathetic authority)
- The story proves why the Guide is qualified

So the founder story = the Guide's origin story that builds trust and empathy.

## Output template
```markdown
# Brand Story — <Client>

## Story Ingredients
- Founder: ...
- Inciting incident: ...
- Struggle: ...
- Insight: ...
- Mission: ...
- Transformation: ...
- Proof: ...

## Story Circle (8 beats)
1. YOU: ...
2. NEED: ...
3. GO: ...
4. SEARCH: ...
5. FIND: ...
6. TAKE: ...
7. RETURN: ...
8. CHANGE: ...

## ABT One-liner
> ...

## Version 1 — Micro (50 words)
...

## Version 2 — Medium (200-300 words)
...

## Version 3 — Full (600-1000 words)
...

## Usage guide
- About page: Version 3 + hero image
- Pitch deck slide 4: Version 2
- Email welcome E1: Version 2 adapted
- Social bio: Version 1
- Video script: Version 3 with visual cues
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Brand Story.md`

## Red Flags
- Never make the brand the hero of the story — the customer is always the hero, the brand is the guide; violating this turns the narrative into self-congratulation that repels rather than attracts
- Never skip the epiphany moment (beat 5: FIND) — a story without a breakthrough insight is just a chronological resume with no emotional payoff
- Always produce all 3 output formats (micro/medium/full) — a single version cannot serve bios, About pages, and pitch decks, and the client will ask for the others anyway
- Never write a brand story without first gathering the real inciting incident from the founder — fabricated origin stories ring hollow and crumble under interview questions
- Always connect the story back to the customer's transformation (beat 8: CHANGE) — a founder story that ends with the founder's success instead of the customer's outcome misses the entire point
