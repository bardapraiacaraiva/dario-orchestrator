---
name: dario-pitch
description: Investor or client pitch deck generator using Klaff STRONG framework + Duarte Sparkline + Campbell Hero's Journey. Outputs slide outline, speaker notes, and hook script. Triggers on "pitch deck", "investor pitch", "apresentação", "keynote", "story deck".
license: MIT
---

# DARIO Skill — Pitch Deck

Builds a narrative-first pitch deck (not a glorified feature list). Uses proven storytelling frameworks so the audience **feels** the pitch, not just understands it.

## When to activate

- Client needs an investor deck (VC, angels, family offices)
- Internal keynote / board presentation
- Client-facing proposal deck (high-ticket services)
- HNW / luxury client presentations (like Atrium Golden Visa to HNW investors)
- Conference talk structure

## Workflow

### 1. Gather inputs
- **Who** is the audience (decision makers, context, time available)
- **What** are they deciding (invest, buy, partner, approve)
- **Why** now (trigger event, timing, urgency)
- **Ask** (the specific action wanted)
- **Stakes** (what happens if they don't act)
- **Proof** (data, testimonials, track record)
- **Analogy** (metaphor that simplifies the idea)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "oren klaff pitch STRONG frame control", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "nancy duarte sparkline resonate presentation", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "joseph campbell heros journey narrative", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "dan harmon story circle", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "park howell abt and but therefore", collection: "dario", limit: 5)
```

### 3. Choose primary framework by context

| Situation | Framework |
|---|---|
| VC pitch, compressed time | **Klaff STRONG** (frame control + pattern interrupt) |
| Keynote, change narrative | **Duarte Sparkline** (what is ↔ what could be) |
| Origin story, purpose-driven | **Campbell Hero's Journey** (condensed) |
| Business narrative, simple | **Park Howell ABT** (And, But, Therefore) |

Most pitches benefit from combining: **Klaff for frames + Duarte for structure + ABT for clarity**.

### 4. Klaff STRONG framework

**S** — **S**et the frame (context control from minute 1)
**T** — **T**ell the story (not pitch, story)
**R** — **R**eveal the intrigue
**O** — **O**ffer the prize (why they should want IN, not you want them in)
**N** — **N**ail the hookpoint (emotional moment of decision)
**G** — **G**et the decision (clear ask)

**Frame control rules:**
- Never be needy
- Make scarcity real
- Position audience as worthy (they qualify for YOU)
- Control time (not them)
- Avoid "analyst frame" (getting quizzed)

### 5. Duarte Sparkline structure

Alternate between **what is** (current state) and **what could be** (better state):

```
Start: what is (status quo reality)
  ↓ contrast ↑
what could be (vision)
  ↓ contrast ↑
what is (new obstacles)
  ↓ contrast ↑
what could be (breakthrough)
  ...
End: New bliss (call to action)
```

Each cycle amplifies the gap between reality and vision. Audience stays engaged because of contrast.

### 6. ABT (And, But, Therefore) — one-sentence narrative

Template:
> **<Context> AND <context> BUT <problem> THEREFORE <solution>.**

Example (Atrium):
> American HNW investors seek diversification AND Portugal Golden Visa is the most efficient EU path, BUT 73% of applications fail because of mis-structured investments, THEREFORE we built an end-to-end compliance-first advisory specifically for Americans.

This is the elevator pitch that anchors the deck.

### 7. Deck structure (12-14 slides standard)

| # | Slide | Purpose | Duarte beat |
|---|---|---|---|
| 1 | **Cover** | Title + credibility hook | What is |
| 2 | **The world today** | Problem + stakes | What is (amplified) |
| 3 | **Trend / Opportunity** | Why now | What could be |
| 4 | **Your founder story** (optional) | Credibility | Personal sparkline |
| 5 | **The unique insight** | What you see that others don't | What could be |
| 6 | **Solution** | Your product/offer | Reality |
| 7 | **How it works** | Mechanism | What is |
| 8 | **Results / Proof** | Metrics, case studies, testimonials | What could be (for them) |
| 9 | **Market size** | TAM/SAM/SOM | What is |
| 10 | **Business model** | How you make money | — |
| 11 | **Competition** | Differentiation matrix | — |
| 12 | **Team** | Why you'll win | — |
| 13 | **Ask + Use of funds** | Specific number + allocation | Call to action |
| 14 | **Vision / Close** | What winning looks like | New bliss |

### 8. Hook script (first 90 seconds)

Open with ONE of these patterns (test 2-3):
- **Shock stat:** "73% of Portugal Golden Visa applications are rejected. Here's why."
- **Contrarian claim:** "Everything you've heard about Golden Visa is 10 years out of date."
- **Story:** "In 2019, Karen watched a $500K investment disappear because of a PFIC rule nobody told her client about."
- **Analogy:** "Think of Portugal Golden Visa like a stock — you're not buying a country, you're buying an option."
- **Question (Socratic):** "How many of you know what Form 8621 is? That's why this matters."

Avoid: "Hi my name is...", "Today I'll talk about...", "Let me show you some slides."

### 9. Speaker notes (per slide)
- **Main point** (1 sentence)
- **Transition** (link from previous)
- **Story / example** (if slide benefits from it)
- **Pause points** (where to let it sink)
- **Audience interaction** (optional Q, show of hands)

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: pitch-deck
audience: <VCs|clients|board>
framework: <STRONG|sparkline|ABT|combined>
---

# Pitch Deck — <Project>

## Strategic Context
- Audience: ...
- Ask: ...
- Stakes: ...

## ABT One-liner
<Context> AND <context> BUT <problem> THEREFORE <solution>.

## Hook (90s script)
<Verbatim opening>

## Slide Outline

### Slide 1 — Cover
**Headline:** ...
**Visual:** ...
**Speaker note:** ...

### Slide 2 — The world today
**Headline:** ...
**Key data:** ...
**Speaker note:** ...

(continua)

## Full Speaker Notes
[By slide number, with transitions and pauses]

## Q&A Preparation
### Likely questions + framed answers
1. ...

## Deliverables
- [ ] Deck in Keynote / Google Slides (this doc as source)
- [ ] 1-pager summary
- [ ] Executive brief (PDF)
- [ ] Dry run rehearsal schedule
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Pitch Deck.md`

## Red flags
- Starting with "About us" or "Company history" (loses audience in 30s)
- 40-slide monster (kills attention)
- Font size <20pt on slides (unreadable in room)
- Charts without a single takeaway highlighted
- No clear ask (audience doesn't know what to do)
- Feature-dumping (no story)
- Treating investor/client as rational-only (emotion drives decisions)

## Interactions
- Depends on `dario-brand` (voice, positioning)
- Pairs with `dario-sales-letter` (can share copy blocks)
- Project: Atrium Golden Visa is the canonical use case — HNW investors need this treatment

## Red Flags
- Never exceed 14 slides (12 is ideal) — every slide beyond that dilutes attention and signals that you cannot prioritize
- Never present a deck without at least one rehearsal with timer — unrehearsed presenters run over time, miss transitions, and lose frame control
- Always open with a hook (shock stat, contrarian claim, story) not credentials — leading with "About Us" loses the audience in the first 30 seconds
- Never feature-dump without a narrative thread — a deck without story structure is a glorified brochure that triggers the analyst frame instead of the buyer frame
- Always end with a specific, unambiguous ask — a deck without a clear call to action wastes the emotional momentum you built throughout the presentation
