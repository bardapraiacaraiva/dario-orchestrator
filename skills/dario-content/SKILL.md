---
name: dario-content
description: "Content production at scale — editorial calendar, blog post writer, content briefs, repurposing (1 piece → 10 formats), copy QA review, content cluster execution, pillar page creation. Triggers on: 'content', 'conteudo', 'blog post', 'artigo', 'editorial calendar', 'calendario editorial', 'repurposing', 'content brief', 'escrever artigo', 'pillar page', 'content production'."
license: MIT
---

# DARIO Content — Production at Scale

## When to activate

- Client needs blog posts, articles, or pillar pages
- Monthly editorial calendar creation
- Content brief for human writers
- Repurposing existing content (1 → 10 formats)
- Copy QA review before publishing
- Content cluster execution (from seo-plan keyword map)

## Modules

### 1. Editorial Calendar (Monthly/Quarterly)

Input: brand voice (from dario-brand), keyword map (from seo-plan), content pillars (from dario-social)
Output:

```markdown
## Editorial Calendar — [Client] — [Month]

### Content Goals
- Primary: [traffic / leads / authority / engagement]
- KPIs: [sessions, time on page, conversions, backlinks]

### Calendar
| Week | Type | Title | Target Keyword | Funnel Stage | Platform | Author | Status |
|---|---|---|---|---|---|---|---|
| 1 | Pillar | "Guia Completo: [topic]" | [kw, vol] | TOFU | Blog | [name] | Draft |
| 1 | Social | 3 posts from pillar | [derived] | TOFU | IG+LI | [name] | Planned |
| 2 | Blog | "[How-to article]" | [kw, vol] | MOFU | Blog | [name] | Brief done |
| 2 | Email | Newsletter with blog summary | — | MOFU | Email | [name] | Planned |
| 3 | Blog | "[Case study]" | [kw, vol] | BOFU | Blog | [name] | Planned |
| 3 | Video | Reel from case study | [derived] | BOFU | IG+TT | [name] | Planned |
| 4 | Blog | "[Industry trend]" | [kw, vol] | TOFU | Blog | [name] | Planned |
| 4 | Social | Monthly roundup | — | — | All | [name] | Planned |
```

### 2. Blog Post Writer

Input: topic, target keyword, word count, tone (from brand), audience
Output: Complete blog post with:

**Structure:**
```
Title (H1) — includes primary keyword, <60 chars
Meta description — 150-160 chars, keyword + CTA
Introduction — hook + promise + what you'll learn (150 words)
[H2 sections] — 3-7 sections, each with:
  - H2 heading (keyword variant or question)
  - 150-300 words
  - At least 1 internal link
  - Data/examples where relevant
FAQ section — 3-5 questions (FAQPage schema ready)
Conclusion — summary + CTA (100 words)
```

**SEO checklist (auto-verify):**
- [ ] Primary keyword in: title, H1, first 100 words, 1 H2, meta description, alt text
- [ ] Keyword density: 1-2% (not stuffed)
- [ ] Internal links: minimum 3
- [ ] External links: minimum 1 (authoritative source)
- [ ] Images: minimum 2 with descriptive alt text
- [ ] Word count: meets target (+/- 10%)
- [ ] Readability: Flesch-Kincaid grade 8-10 (PT equivalent)
- [ ] No AI detection signals (varied sentence length, specific examples, original insights)

### 3. Content Brief (for human writers)

When the blog post needs a human writer:

```markdown
## Content Brief — [Title]

**Target keyword:** [keyword] ([volume]/month, [difficulty])
**Secondary keywords:** [3-5 related terms]
**Word count:** [target]
**Deadline:** [date]
**Author:** [name]

### Audience
- Who: [persona description]
- Pain point: [what they're searching for and why]
- Knowledge level: [beginner / intermediate / expert]

### Outline
1. [H2: Section title] — [what to cover, 2-3 sentences]
2. [H2: Section title] — [what to cover]
3. [H2: Section title] — [what to cover]

### Mandatory elements
- Include [specific data point / stat / example]
- Link to: [internal pages]
- Mention: [product / service / CTA]
- Tone: [from dario-brand]

### Reference material
- [competitor article 1 URL] — what they do well / what's missing
- [competitor article 2 URL]
- [internal resource]

### SEO requirements
- Primary keyword in: title, H1, first 100 words, 1 H2
- Alt text for all images
- Meta description: include keyword + benefit

### Do NOT
- [specific things to avoid for this client]
```

### 4. Content Repurposing (1 → 10)

Take 1 piece of content and create 10 derivative pieces:

```
INPUT: 1 blog post (1500 words)

OUTPUT:
1. Twitter/X thread (8-12 tweets) — key insights
2. LinkedIn post (long-form) — professional angle
3. Instagram carousel (10 slides) — visual summary
4. Instagram Reel script (30s) — 1 key takeaway
5. TikTok script (60s) — hook + value + CTA
6. Email newsletter excerpt (300 words) — teaser + link
7. Pinterest pin (title + description) — evergreen format
8. YouTube Shorts script (60s) — visual version of reel
9. Quote graphics (3 images) — shareable key quotes
10. FAQ expansion (3 new questions) — from blog content
```

### 5. Copy QA Review

Quality check before publishing:

```markdown
## Copy QA — [Title]

### Factual accuracy
- [ ] All claims supported by sources
- [ ] Statistics are current (not outdated)
- [ ] Brand names correctly spelled
- [ ] No hallucinated information

### SEO compliance
- [ ] Primary keyword placed correctly
- [ ] Meta title < 60 chars
- [ ] Meta description 150-160 chars
- [ ] All images have alt text
- [ ] Internal links present and working

### Brand voice
- [ ] Matches approved tone (from dario-brand)
- [ ] No banned words used
- [ ] Consistent style throughout

### Readability
- [ ] Sentences average < 20 words
- [ ] Paragraphs max 3-4 lines
- [ ] Technical terms explained
- [ ] Active voice preferred

### Legal
- [ ] No copyright infringement
- [ ] Image licenses verified
- [ ] RGPD-compliant (no personal data without consent)

### Score: [X/20] — [PASS >= 16 | REVISE 12-15 | REJECT < 12]
```

### 6. Pillar Page Creator

Long-form authoritative content (3000-5000 words):

- Comprehensive topic coverage
- Table of contents with anchor links
- Links to all cluster blog posts
- FAQ section (10+ questions)
- Schema: Article + FAQPage + BreadcrumbList
- Downloadable asset (checklist, template, guide)
- Internal linking hub (every cluster post links back)

## Integration Points

- **seo-plan** → Keyword map feeds editorial calendar topics
- **seo-content** → E-E-A-T analysis validates content quality
- **dario-brand** → Tone of voice applied to all copy
- **dario-social** → Blog posts feed social media calendar
- **dario-email-seq** → Content feeds email nurture sequences
- **dario-kw-cluster** → Topic clusters define content architecture
- **lucas-quality** → Content scored after creation

## Red Flags

- Never publish without QA review (minimum self-check)
- Never keyword stuff (1-2% density max)
- Never use AI-generated content without human review layer
- Always include original insights (not just regurgitated info)
- Always check competitor content before writing (don't duplicate)
