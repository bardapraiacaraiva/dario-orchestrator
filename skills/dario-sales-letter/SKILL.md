---
name: dario-sales-letter
description: Long-form sales letter generator using Halbert / Schwartz / Kennedy / Brunson frameworks. Takes a Grand Slam Offer and produces full sales copy with headline sweep, body, CTA. Triggers on "sales letter", "carta de vendas", "long-form copy", "VSL script", "landing page copy".
license: MIT
---

# DARIO Skill — Sales Letter

Writes high-conversion long-form sales copy for a product or service. Pairs naturally after `dario-offer`. Works for written sales pages, VSL scripts, and email long-form.

## When to activate

- User has a Grand Slam Offer ready and wants copy
- Rewrite of underperforming sales page
- Launch copy for new service
- VSL script needed
- Long-form email (Solo broadcast, newsletter deep-dive)

## Workflow

### 1. Gather inputs
- **The offer** (output of `dario-offer` ideally)
- **Target avatar** (as specific as possible)
- **Awareness level** (Schwartz):
  - 1. Unaware (don't know they have a problem)
  - 2. Problem-aware (know problem, not solution)
  - 3. Solution-aware (know solutions exist)
  - 4. Product-aware (know your product)
  - 5. Most-aware (just need offer/push)
- **Market sophistication** (Schwartz):
  - Stage 1: first to make the claim
  - Stage 2: bigger claim than competitors
  - Stage 3: mechanism ("here's HOW we do it")
  - Stage 4: bigger mechanism
  - Stage 5: identification / experience (most mature)
- **Dominant emotion** (fear, greed, guilt, shame, pride, hope)
- **Proof elements** (testimonials, results, screenshots, credentials)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "eugene schwartz awareness levels sophistication", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "gary halbert sales letter structure", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "dan kennedy 3ms market message media", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "russell brunson epiphany bridge vsl", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "hopkins claude scientific advertising", collection: "dario", limit: 5)
```

### 3. Choose framework based on awareness level

| Awareness | Framework | Pattern |
|---|---|---|
| 1 (unaware) | Halbert problem-entry | Lead with a story of someone similar to avatar hitting the problem |
| 2 (problem-aware) | PAS + amplification | Problem → Agitate → Solve |
| 3 (solution-aware) | Unique Mechanism | "Others try X, we do Y because..." |
| 4 (product-aware) | Proof-stacking | Case studies, side-by-sides, direct comparison |
| 5 (most-aware) | Offer-first + urgency | Get straight to the deal + scarcity |

### 4. Headline sweep (20 minimum)
Generate at least 20 headline variations covering:
- News / Curiosity
- Benefit-driven (specific outcome + timeframe)
- Question-based
- Shock / bold claim
- Testimonial-style
- "How to" / "Why"
- Negative framing ("stop doing X")
- Numbers / list-style
Pick top 3 for A/B consideration.

### 5. Body structure (Halbert 22-step condensed)
1. **Headline** — grab attention
2. **Subheadline** — extend the promise
3. **Lead** — hook the reader (story / stat / question)
4. **Problem amplification** — make them feel the cost of inaction
5. **Transition: story of discovery** — "I was in the same place until..."
6. **Introduce the mechanism** — why this is different
7. **Social proof** — testimonials, case studies
8. **Specific benefits** — bullet list (fascination bullets)
9. **The offer** — what you get
10. **Bonus stack** — total value
11. **Price reveal** — anchor high, reveal "real" price
12. **Guarantee** — reverse risk
13. **Urgency / scarcity** — why now
14. **CTA** — specific, action-oriented
15. **P.S.** — restate key promise + CTA

### 6. Fascination bullets (Lampropoulos / Makepeace style)
Each bullet:
- Promises a specific outcome
- Creates curiosity (open loop)
- Is specific (number, time, place)
- Example: "The 'weird Tuesday trick' that saved me €4,200 in legal fees — page 47"

Generate 15-25 of these. Keep best 10-15 for the page.

### 7. CTA
- Specific verb + outcome ("Apply Now — See If You Qualify")
- Not generic ("Submit", "Click Here")
- Accompanied by risk-reversal ("100% money back if...")
- First CTA after ~40% of the read, again at 70%, final at end

### 8. Proof elements placement
- Above fold: 1 social proof element (logo bar, testimonial snippet, result number)
- Middle: deep case study (1-2)
- Near CTA: risk-reversal + guarantee
- Before price: "others who tried this" montage

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: sales-letter
awareness_level: <1-5>
sophistication_stage: <1-5>
framework: <halbert|pas|unique-mechanism|proof-stack|offer-first>
---

# Sales Letter — <Product / Service>

## Strategic Context
- Avatar: ...
- Awareness: ...
- Sophistication: ...
- Dominant emotion: ...
- Dream outcome: ...

## Headline Options (Top 3)
1. ...
2. ...
3. ...

## Subheadline
...

---

## FULL COPY

[HEADLINE]

[SUBHEADLINE]

<opening hook — 150-300 words>

<problem amplification — 300-500 words>

<transition + discovery story — 300-500 words>

<introduce unique mechanism — 200-400 words>

<social proof block 1>

<specific benefits — fascination bullets>
- ...
- ...
- (15+ bullets)

<deep case study>

[CTA 1 — mid-page]

<more proof / objection handling>

<offer reveal>

<bonus stack>

<price anchor + reveal>

<guarantee>

<urgency / scarcity>

[CTA 2 — final]

<P.S. — restate main promise + CTA>

---

## Versions to A/B test
1. Headline variant A vs B
2. Guarantee wording
3. Price anchor style
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Sales Letter.md`

## Red flags
- Vague benefits ("better results") instead of specific ("add 3.2kg muscle in 90 days")
- Hopium (promising things you can't deliver)
- Walls of text without subheadings / bullets / breaks
- Starting with "we" or "our" (always start with reader)
- Feature list instead of benefit list
- Single CTA at the bottom only
- No P.S.
- Using "exclusive", "secret", "revolutionary" (instant credibility killer)

## Red Flags
- Never write sales copy without first identifying the audience's awareness level (Schwartz 1-5) — copy pitched at the wrong awareness stage either bores or confuses the reader
- Never skip the headline sweep (minimum 20 variations) — the headline accounts for 80% of whether the page gets read, and the first draft is almost never the best
- Always include specific proof elements (testimonials with names, exact numbers, case studies) — vague claims like "amazing results" trigger skepticism and kill conversions
- Never start the copy with "we" or "our company" — the reader only cares about themselves, and self-centered openings signal that you do not understand their world
- Always place at least 3 CTAs throughout the letter (40%, 70%, end) — a single CTA at the bottom means everyone who drops off mid-page never sees the action step
- Never promise outcomes you cannot substantiate — hopium copy generates refunds, chargebacks, and reputation damage that far exceed any short-term revenue
