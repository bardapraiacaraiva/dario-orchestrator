---
name: dario-email-seq
description: Email sequence generator — welcome, soap opera (Chaperon), indoctrination, launch, post-purchase, re-engagement. Uses copy squad frameworks (Chaperon, Settle, Makepeace, Koe). Triggers on "email sequence", "email campaign", "welcome series", "nurture sequence", "launch sequence".
license: MIT
---

# DARIO Skill — Email Sequence

Designs and writes email sequences matched to the business goal: convert new subs, nurture, launch, re-engage, upsell. Based on Chaperon's Soap Opera, Settle's daily sending, Makepeace's emotion, and Koe's creator patterns.

## When to activate

- Client has opt-in list (even small — 50 subs is enough)
- After lead magnet creation
- Pre-launch of a new product/service
- Cart abandonment flow setup
- Re-engage dormant segment
- Post-purchase onboarding / ascension

## Sequence types

| Type | Length | Goal |
|---|---|---|
| **Welcome / Indoctrination** | 5-7 emails | New sub → first purchase + brand trust |
| **Soap Opera Sequence (SOS)** | 5 emails | Bond + first sale within 5 days |
| **Nurture** | 12+ emails | Long-term relationship, education, soft pitches |
| **Launch** | 7-14 emails | Pre-launch → open cart → close cart urgency |
| **Cart Abandonment** | 3-5 emails | Recover abandoned checkouts |
| **Post-Purchase** | 4-8 emails | Onboard + upsell + review request |
| **Re-engagement** | 3 emails | "Are you still interested?" + final purge |
| **Weekly / Daily Broadcast** | ongoing | Ongoing engagement (Settle / Koe style) |

## Workflow

### 1. Gather inputs
- **List source** (what opt-in? lead magnet?)
- **Offer / product**
- **Avatar**
- **Awareness level** (Schwartz)
- **Brand voice** (tone from `dario-brand` if exists)
- **Sequence type + goal**
- **Length preference**
- **Delivery tool** (ActiveCampaign, ConvertKit, Mailchimp, custom)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "andre chaperon soap opera sequence storytelling", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "ben settle daily email copywriting", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "clayton makepeace dominant emotion email", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "dan koe creator one person business email", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "jeff walker product launch formula", collection: "dario", limit: 5)
```

### 3. Soap Opera Sequence (SOS) template — Chaperon style

**Day 1 — Set the stage**
- Subject line: curiosity + open loop
- Open: personal story beginning
- Close: open loop that forces next email

**Day 2 — High drama**
- Subject line: continuation
- Open: pickup from day 1
- Middle: raise the stakes / conflict
- Close: cliffhanger

**Day 3 — Epiphany**
- Subject line: revelation
- Middle: the breakthrough moment
- Close: soft hint of solution

**Day 4 — Hidden benefits**
- Subject line: benefit-driven
- Middle: reveal what's possible
- Close: transition to offer

**Day 5 — Urgency + pitch**
- Subject line: "last chance" or direct offer
- Middle: the offer
- Close: strong CTA + P.S. with urgency

### 4. Indoctrination sequence — Brunson style

6-email series that transforms a cold sub into a believer:
1. **Who I am** (origin story, why you started)
2. **Why I'm different** (unique mechanism / contrarian view)
3. **What I believe** (beliefs that differentiate)
4. **How it works** (proof + case studies)
5. **Offer introduction** (soft)
6. **Ask** (direct CTA)

### 5. Launch sequence — Jeff Walker PLF

**Pre-launch (1-2 weeks)**
- Email 1: "Something big is coming" + date tease
- Email 2: Content video 1 — the opportunity
- Email 3: Content video 2 — transformation case study
- Email 4: Content video 3 — the experience (how it works)

**Cart open (5-7 days)**
- Email 5: "Doors are open" + offer detail
- Email 6: FAQ + objection handling
- Email 7: Case study / transformation story
- Email 8: Scarcity reminder + bonuses
- Email 9: "24 hours left"
- Email 10: "Final hours" + last CTA

**Post-launch**
- Email 11: Thank you + onboarding (for buyers)
- Email 12: "Cart closed" (for non-buyers — seed next launch)

### 6. Cart abandonment — 3 email minimum

- **Email 1 (1 hour after abandon):** "Forgot something?" soft reminder + item image
- **Email 2 (24 hours):** Address common objection + social proof
- **Email 3 (48-72 hours):** Urgency ("cart expires in X hours") + incentive (free shipping, bonus)

### 7. Writing principles (copy squad distilled)

**Subject lines**
- Open curiosity gap
- Specific > vague ("You were right about X" > "Update")
- Lowercase often outperforms Title Case
- <50 chars preferred
- Emoji: A/B test, often bad for B2B

**Opens (first sentence)**
- Never "Hi [First Name]"
- Start with a story, a question, or a pattern interrupt
- Reference the subject line to validate the click

**Body**
- Short paragraphs (1-3 lines)
- Conversational voice
- One idea per email
- Prove > claim
- Specific > general

**CTAs**
- One primary CTA per email
- Action verb + outcome
- Also text link in P.S.

**P.S.**
- ALWAYS include
- Restate core benefit OR reveal new hook
- Often the most-read part of the email

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: email-sequence
sequence_type: <sos|indoc|launch|cart|post-purchase|reengage>
length: N emails
---

# Email Sequence — <Client / Offer>

## Strategic Context
- Avatar: ...
- Sequence type: ...
- Goal: ...
- Awareness level: ...
- Voice: ...

## Architecture
| Day | Email | Subject | Main beat | CTA |
|---|---|---|---|---|
| 0 | E1 | ... | Open story | Soft |
| 1 | E2 | ... | ... | ... |
| ... |

---

## EMAIL 1

**Send:** Day 0, immediately after opt-in
**Subject:** ...
**Preview text:** ...

<body>

**P.S.** <ps>

---

## EMAIL 2

**Send:** Day 1
**Subject:** ...

<body>

---

(continua para cada email)

## Automation Rules
- Send time: ...
- Timezone: ...
- Skip rules: ...
- Tag on open/click: ...
- Exit conditions (e.g. if buys, exit sequence and enter "customer onboarding")
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Email Sequence.md`

## Red flags
- "Buy now buy now buy now" (dies in spam)
- Corporate voice ("We at [Company]...") vs conversational
- No personalization beyond first name
- Same CTA in every email (gets ignored)
- 10-paragraph emails (loses mobile readers)
- No P.S.
- Hard sell before relationship (SOS needs 4 emails before pitch)
- Ignoring deliverability (sender reputation, authentication SPF/DKIM/DMARC)

## Interactions
- Depends on `dario-offer` (what's being sold)
- Depends on `dario-brand` (voice)
- Pair with `dario-sales-letter` for the main LP
