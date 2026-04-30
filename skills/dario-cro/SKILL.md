---
name: dario-cro
description: CRO & experimentation squad — runs ResearchXL audits, LIFT scoring, emotional targeting, attention ratio analysis, form optimization, trust audits, PXL prioritization, and A/B test planning. Triggers on "cro", "conversion rate", "a/b test", "split test", "landing page audit", "form optimization", "trust audit", "experimentation", "taxa de conversao", "otimizar conversao".
version: 1.0.0
license: MIT
---

# DARIO Skill -- CRO & Experimentation

Full-stack conversion rate optimization: diagnose why pages underperform, audit using six expert lenses, prioritize a test backlog, design statistically valid experiments, and implement winning variants. Built on the combined frameworks of Peep Laja, Chris Goward, Talia Wolf, Oli Gardner, Karl Gilis, and Andre Morys.

## When to activate

- Landing page not converting (below industry benchmark)
- Homepage trying to do everything at once
- "People visit but don't buy/sign up/contact"
- Form abandonment is high
- Client asks for "A/B testing" or "conversion optimization"
- After `dario-funnel` (funnel exists, now optimize each step)
- After `dario-sales-letter` (copy exists, now test variants)
- E-commerce checkout drop-off investigation
- Before paid traffic scale-up (fix the bucket before pouring more water)

## Squad roster

| Agent | Framework | Focus |
|---|---|---|
| **ResearchXL** (Peep Laja) | 6-layer research model | Heuristic, technical, analytics, mouse tracking, qualitative, quantitative |
| **LIFT Model** (Chris Goward) | 6-factor scoring | Value prop, relevance, clarity, anxiety, distraction, urgency |
| **Emotional Targeting** (Talia Wolf) | Emotional conversion | Emotional triggers, color psychology, persuasion hierarchy |
| **Attention Ratio** (Oli Gardner) | 1:1 ratio rule | Single CTA focus, page congruence, information scent |
| **Form Optimization** (Karl Gilis) | Form UX | Field reduction, microcopy, progressive disclosure, error handling |
| **Trust Signals** (Andre Morys) | Conversion trust | Social proof, authority, risk reversal, credibility markers |

## Workflow

### 1. Gather inputs

- **Page URL** (live page or staging)
- **Page purpose** (lead gen, purchase, signup, download, booking)
- **Traffic source** (paid, organic, email, social, direct)
- **Current metrics** (conversion rate, bounce rate, sessions, AOV if e-commerce)
- **Analytics access** (GA4 or equivalent data)
- **Heatmap data** (Hotjar/Clarity if available)
- **Business context** (industry, ticket size, sales cycle)

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "peep laja researchxl conversion optimization heuristic", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "chris goward lift model value proposition clarity", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "talia wolf emotional targeting conversion", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "oli gardner attention ratio unbounce landing page", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "karl gilis form optimization usability", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "andre morys trust signals conversion psychology", collection: "dario", limit: 5)
```

### 3. Diagnose -- ResearchXL 6-layer analysis

Run each layer sequentially:

**Layer 1 -- Heuristic analysis**
Walk the page as a first-time visitor. Score each element:
- Does the headline communicate value in under 5 seconds?
- Is the primary CTA immediately visible above the fold?
- Is the visual hierarchy guiding the eye toward conversion?
- Are trust signals present and credible?
- Is the copy benefit-oriented (not feature-oriented)?

**Layer 2 -- Technical analysis**
- Page load time (target: < 3s)
- Mobile responsiveness and tap targets
- Cross-browser rendering
- Core Web Vitals (LCP, INP, CLS)
- JavaScript errors blocking interactions
- Form submission errors

**Layer 3 -- Analytics deep-dive**
- Traffic segmentation (device, source, geo, new vs returning)
- Funnel visualization (where do users drop off?)
- Exit pages vs bounce pages (different problems)
- Event tracking gaps (what is NOT being measured?)
- Segment comparison (converters vs non-converters behavior)

**Layer 4 -- Mouse tracking / heatmaps**
- Click maps: are users clicking non-clickable elements?
- Scroll maps: what percentage see below-the-fold content?
- Attention maps: is the CTA in a heat zone?
- Rage clicks: frustrated interactions
- Session recordings: 10-20 random non-converting sessions

**Layer 5 -- Qualitative research**
- On-page surveys ("What almost stopped you from completing?")
- Exit-intent survey ("Why are you leaving?")
- Customer interviews (5-10 recent converters)
- Customer support ticket analysis (recurring objections)
- Review mining (competitor reviews for objection patterns)

**Layer 6 -- Quantitative validation**
- A/B test hypotheses ranked by impact x effort
- Sample size calculations before launching tests
- Statistical significance thresholds (95% confidence minimum)
- Test duration planning (minimum 2 full business cycles)

### 4. Audit -- LIFT Model scoring

Score each factor 1-10 and compute overall LIFT score:

| Factor | Question | Score (1-10) | Notes |
|---|---|---|---|
| **Value Proposition** | Is the offer compelling and clearly communicated? | | |
| **Relevance** | Does the page match visitor intent and ad/referral promise? | | |
| **Clarity** | Is the message and next step immediately obvious? | | |
| **Anxiety** | Are there elements creating doubt or hesitation? | | |
| **Distraction** | Are there elements pulling attention away from conversion? | | |
| **Urgency** | Is there a reason to act now vs later? | | |

**LIFT Score** = (Value + Relevance + Clarity - Anxiety - Distraction + Urgency) / 6

- Score 8-10: High conversion potential, fine-tune only
- Score 5-7: Significant issues, structured testing needed
- Score 1-4: Fundamental problems, redesign before testing

### 5. Specialized audits

#### *emotional-audit (Talia Wolf)

Map the emotional conversion path:
1. **Identify dominant buyer emotion** (fear, aspiration, belonging, status, guilt, curiosity)
2. **Audit visual triggers** -- do colors, images, and layout reinforce the emotion?
3. **Audit copy triggers** -- does the language amplify the emotion?
4. **Audit persuasion sequence** -- emotion first, then logic, then action
5. **Emotional gap analysis** -- where does the emotional thread break?

#### *attention-ratio (Oli Gardner)

Calculate the attention ratio:
```
Attention Ratio = Number of links on page : Number of conversion goals
Target: 1:1 (one page, one goal)
```

Audit:
- Count every clickable element (nav links, footer links, social icons, secondary CTAs)
- Identify the single conversion goal
- Flag violations: nav bar on LP, social links, "learn more" links, footer navigation
- Information scent check: does every element point toward the CTA?

#### *form-audit (Karl Gilis)

For every form on the page:
- **Field count** -- target: absolute minimum needed (every field removed = conversion lift)
- **Field labels** -- clear, above the field, not inside (placeholder-as-label is an anti-pattern)
- **Field order** -- easy first (name, email), hard last (phone, budget)
- **Microcopy** -- helper text explaining WHY you need each field
- **Error handling** -- inline validation, specific error messages (not "invalid input")
- **CTA button text** -- specific verb + value ("Get My Free Audit" not "Submit")
- **Progressive disclosure** -- multi-step vs single long form
- **Mobile UX** -- correct keyboard types (email, tel, number), autofill support

#### *trust-audit (Andre Morys)

Inventory and score trust signals:
- **Social proof**: testimonials (with photos/names), review counts, client logos, case studies
- **Authority**: certifications, awards, press mentions, expert endorsements, years in business
- **Risk reversal**: guarantees, free trials, return policies, "no commitment" language
- **Security**: SSL badge, payment security icons, privacy assurances
- **Specificity**: exact numbers beat vague claims ("1,247 clients" vs "thousands of clients")
- **Proximity**: trust signals placed near the CTA, not buried in footer

### 6. Prioritize -- PXL framework

Rank all identified issues using PXL (Peep Laja):

| # | Hypothesis | Page/element | Is it above the fold? (2pt) | Based on user data? (2pt) | Addresses a known problem? (2pt) | Running on high-traffic page? (2pt) | Noticeable in < 5s? (2pt) | Adding/removing? (1pt) | PXL Score | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |

Sort by PXL score descending. Top 3 become the test roadmap.

### 7. Design A/B test plan

For each prioritized hypothesis:

```
Test ID:       CRO-<NNN>
Hypothesis:    If we [change], then [metric] will [improve] because [reason]
Variable:      [specific element being changed]
Control:       [current version description]
Variant:       [new version description]
Primary KPI:   [conversion rate / form completion / AOV / RPV]
Secondary KPI: [bounce rate / time on page / scroll depth]
Sample size:   [calculated — use formula below]
Duration:      [minimum days based on traffic]
Segment:       [all traffic / specific source / device]
Tool:          [Google Optimize successor / VWO / Convert / Optimizely]
```

**Sample size formula:**
```
n = (Z_alpha/2 + Z_beta)^2 * 2 * p * (1-p) / MDE^2

Where:
- Z_alpha/2 = 1.96 (for 95% confidence)
- Z_beta = 0.84 (for 80% power)
- p = baseline conversion rate
- MDE = minimum detectable effect (typically 10-20% relative lift)
```

**Duration rule:**
```
Minimum days = Required sample size / Daily visitors
Never less than 14 days (capture weekly cycles)
Preferably 28 days (capture monthly cycles)
```

### 8. Implement winning changes

After a test reaches significance:
- Document the winner with exact lift percentage and confidence interval
- Implement permanently via code (not just the testing tool)
- Update the page template / component library
- Feed insights back into `dario-sales-letter` and `dario-funnel` for systemic improvement
- Log in test archive for institutional knowledge

## Commands

| Command | Description | Output |
|---|---|---|
| `*cro-research` | Full ResearchXL 6-layer diagnostic | Prioritized issue list with evidence |
| `*lift-audit` | LIFT Model scoring (6 factors) | Score card + recommendations |
| `*emotional-audit` | Talia Wolf emotional targeting analysis | Emotional gap map + fixes |
| `*attention-ratio` | Oli Gardner 1:1 attention ratio check | Ratio score + distraction inventory |
| `*form-audit` | Karl Gilis form optimization review | Field-by-field recommendations |
| `*trust-audit` | Andre Morys trust signal inventory | Trust score + placement map |
| `*pxl-rank` | PXL prioritization of test backlog | Ranked hypothesis table |
| `*test-plan` | Design a statistically valid A/B test | Full test spec document |
| `*teardown` | Oli-style landing page teardown/critique | Page-by-page annotated critique |
| `*ab-sample-size` | Calculate sample size for a test | Sample size + duration estimate |

## CRO audit scoring rubric

Overall CRO Health Score (0-100):

| Dimension | Weight | Score range | Assessment |
|---|---|---|---|
| **Value Proposition Clarity** | 20% | 0-20 | Is the offer immediately understood? |
| **Page Focus & Attention** | 15% | 0-15 | Single goal, no distractions? |
| **Trust & Credibility** | 20% | 0-20 | Social proof, authority, risk reversal? |
| **Form / CTA Optimization** | 15% | 0-15 | Frictionless path to conversion? |
| **Emotional Resonance** | 15% | 0-15 | Does the page connect emotionally? |
| **Technical Performance** | 15% | 0-15 | Fast, functional, mobile-ready? |

**Grading:**
- 85-100: Optimized -- fine-tuning and incremental testing
- 70-84: Good foundation -- targeted tests will yield lifts
- 50-69: Significant issues -- structured optimization program needed
- Below 50: Fundamental problems -- redesign before testing

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: cro-audit
page: <URL>
lift_score: <X/10>
cro_health: <X/100>
---

# CRO Audit -- <Client> -- <Page Name>

## Executive Summary
- Current conversion rate: X%
- Industry benchmark: Y%
- Gap: Z percentage points
- Top 3 issues identified: ...
- Estimated lift potential: X-Y%

## ResearchXL Findings
### Layer 1 -- Heuristic
...
### Layer 2 -- Technical
...
### Layer 3 -- Analytics
...
### Layer 4 -- Mouse tracking
...
### Layer 5 -- Qualitative
...
### Layer 6 -- Quantitative validation plan
...

## LIFT Score Card
| Factor | Score | Key finding |
|---|---|---|
| Value Proposition | /10 | ... |
| Relevance | /10 | ... |
| Clarity | /10 | ... |
| Anxiety | /10 | ... |
| Distraction | /10 | ... |
| Urgency | /10 | ... |

## Specialized Audits
### Emotional Targeting
...
### Attention Ratio
Current: X:1 | Target: 1:1
Distractions: ...

### Form Audit
Fields: X (recommend: Y)
Issues: ...

### Trust Signals
Present: ...
Missing: ...

## PXL Prioritized Test Backlog
| # | Hypothesis | PXL Score | Priority |
|---|---|---|---|
| 1 | ... | ... | HIGH |
| 2 | ... | ... | HIGH |
| 3 | ... | ... | MEDIUM |

## Test Plan -- Top Priority
### Test CRO-001
- Hypothesis: ...
- Variable: ...
- Sample size: ...
- Duration: ...
- Expected lift: ...

## Red Flags Detected
- [ ] ...

## Next Steps
1. ...
2. ...
3. ...
```

## Red flags / anti-patterns

- Homepage trying to be everything (about us + services + blog + testimonials + pricing on one page)
- Hero copy focused on features, not transformation ("We have 20 years of experience" vs "Double your leads in 90 days")
- Multiple competing CTAs on a single landing page (attention ratio > 5:1)
- Forms with 8+ fields when 3-4 would suffice
- Zero social proof anywhere on the page
- Testimonials without names, photos, or specifics ("Great service!" -- Anonymous)
- A/B tests ended before reaching statistical significance
- Testing button colors instead of value propositions (low-impact vanity tests)
- No urgency or scarcity element (no reason to act today vs next month)
- Mobile experience is an afterthought (desktop-designed page squeezed into mobile)
- CTA below the fold with no visual path leading to it
- "Submit" as button text on any form
- Trust signals buried in the footer where nobody scrolls
- Running experiments without a documented hypothesis
- Declaring a winner based on a few days of data (Simpson's paradox risk)

## Metrics to track

| Metric | Definition | Benchmark context |
|---|---|---|
| **Conversion Rate** | Completions / unique visitors | Varies by industry (SaaS trial: 3-8%, e-commerce: 1-4%, lead gen: 5-15%) |
| **Bounce Rate** | Single-page sessions / total sessions | Landing pages: 60-90% is normal; below 40% investigate tracking issues |
| **Form Abandonment** | Started but did not complete form / started | Target: < 30% |
| **Time on Page** | Median time before conversion or exit | Longer is not always better -- depends on page purpose |
| **Scroll Depth** | % of page viewed | 75%+ should see the CTA |
| **Click-Through Rate** | CTA clicks / page views | Depends on placement and copy |
| **Average Order Value** | Revenue / orders | Track lift from upsell/cross-sell tests |
| **Revenue Per Visitor** | Revenue / unique visitors | Ultimate e-commerce CRO metric |

## Integration with other DARIO skills

| Skill | Integration point |
|---|---|
| `dario-funnel` | CRO audits each funnel step; funnel provides the conversion flow to optimize |
| `dario-sales-letter` | Copy variants for A/B tests come from sales-letter frameworks; winning copy feeds back |
| `dario-brand` | Brand voice and positioning constrain what CRO changes are on-brand |
| `dario-offer` | A weak offer cannot be fixed by CRO -- if the value equation is broken, fix the offer first |
| `dario-ads-blueprint` | Ad-to-page congruence (message match) is a critical LIFT factor; ad copy must align with LP |
| `dario-wp-audit` | Technical CRO issues often surface in WP audit (speed, mobile, plugin conflicts) |
| `dario-cwv-fix` | Core Web Vitals directly impact bounce rate and conversion; fix CWV before CRO testing |
| `dario-content` | Content pages that should convert (pillar pages, comparison pages) need CRO lens |

## Save location

`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - CRO Audit.md`

## Critical rules

- Never run A/B tests without calculating required sample size first -- underpowered tests produce false positives that waste development resources and sometimes make conversion worse
- Never skip the ResearchXL diagnostic and jump straight to testing -- testing random ideas without research is guessing with extra steps
- Always check ad-to-page message match (LIFT relevance factor) before blaming the landing page -- if the ad promises X and the page delivers Y, no amount of page optimization will fix the disconnect
- Never optimize a page with broken Core Web Vitals -- a 6-second load time kills conversion before any copy or design change can help; run `dario-cwv-fix` first
- Always separate mobile and desktop analysis -- a page that converts at 5% on desktop and 0.5% on mobile is two different problems, not one
- Never declare a test winner without 95% statistical confidence AND a minimum of 14 days runtime -- weekly and daily traffic patterns can create false patterns that reverse after a full cycle
- Never test cosmetic changes (button color, font size) before structural changes (value proposition, offer, CTA copy) -- optimize the biggest levers first
