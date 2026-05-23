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

## Delivery-ready self-check (run BEFORE delivering content ao cliente)

Output dario-content é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1. Editorial Calendar com VOLUMES, intent e CTA per piece
- [ ] Cada artigo tem keyword PRIMARY com search volume + difficulty cited
- [ ] Funnel stage explícito por peça (TOFU/MOFU/BOFU)
- [ ] CTA per piece (não "share" genérico — define qual lead magnet ou conversion)
- [ ] Word count target por piece
- [ ] Deadline em data calendar (não "Q3" genérico)
- [ ] Author atribuído (cliente provides, internal writer, freelancer named)

❌ NOT delivery-ready: "Artigo sobre SEO local, semana 1"
✅ Delivery-ready: "Artigo pillar 'Guia Golden Visa Portugal 2026' (kw: 'portugal golden visa', 6.6K/mo, diff 42) | TOFU | 2400 words | deadline 2026-06-15 | author Maria | CTA: download checklist 30-passos via email opt-in"

### 2. Social Posts com hooks + CTA específicos (não genéricos)
- [ ] Cada post tem hook A/B (não "Did you know?")
- [ ] Platform específica (não "all socials")
- [ ] CTA precisa por platform (Instagram CTA ≠ LinkedIn CTA)
- [ ] Engagement target ou success metric

❌ NOT delivery-ready: "Posts sobre dog care"
✅ Delivery-ready: "LinkedIn carrossel 10 slides: 'Por que 73% dos cães de Lisboa têm ansiedade de separação' | Hook A: stat shock | Hook B: pergunta direta | CTA: 'Avaliação grátis no DM' | Target: 50 saves + 5 DMs"

### 3. Newsletter com angle + segment + open rate target
- [ ] Subject A/B testing variants documented
- [ ] Segment definido (não "all subscribers")
- [ ] Open rate target + industry benchmark fonte
- [ ] Body angle + CTA primary

### 4. SEO checklist FULLY populated per artigo
- [ ] Primary keyword em title + H1 + first 100 words + 1 H2 + meta
- [ ] Internal links 3+ named (não "link to related content")
- [ ] External links 1+ authoritative + URL
- [ ] FAQPage schema-ready (3-5 questions)
- [ ] Readability target stated

### 5. Reuse Matrix cross-channel
- [ ] Cada pillar → 3+ derivative formats explícito
- [ ] Tabela origem → destino mapeada
- [ ] Adaptation rules per channel (LinkedIn ≠ Twitter ≠ Email)

### 6. Output uses CLIENT NAME + REAL data throughout
- [ ] Client name em cada section title
- [ ] Keywords reais (não <keyword> placeholders)
- [ ] Authors named (não <writer>)
- [ ] Deadlines em calendar dates (não <date>)

## Fully-worked A-tier example (delivery-ready reference)

Editorial calendar 92+/100 para SAQUEI BR:

```markdown
---
project: SAQUEI BR
date: 2026-05-23
type: editorial-calendar
period: Q3 2026 (Jul-Set)
target_kpi: organic traffic 8.5K → 25K sessões/mês
---

# Content Calendar Q3 2026 — SAQUEI BR

## Content Goals
- **Primary:** organic traffic from R$ esquecido + restituição BR keywords
- **KPIs:** sessões +250%, scroll depth >65%, opt-in rate >12%, R$ 29 conversion rate >3%
- **Baseline (2026-05-22):** 8.5K sessões/mês, 41% scroll, 8% opt-in, 1.8% conv

## 12 Pillar Articles (Jul-Set)

| W | Type | Title | Primary KW (vol/diff) | Word Count | Stage | Author | CTA | Deadline |
|---|---|---|---|---|---|---|---|---|
| 1 | Pillar | "Como descobrir R$ esquecidos: guia 2026" | "dinheiro esquecido CPF" (49K/mo, 38) | 3500 | TOFU | Lucas | "Verificar grátis em 30s" | 2026-07-05 |
| 1 | Blog | "Receita federal: 7 restituições que você esqueceu" | "restituição receita federal" (74K/mo, 42) | 2200 | MOFU | Maria | "Relatório R$ 29 — começar agora" | 2026-07-08 |
| 2 | Blog | "PIS/PASEP esquecido: como sacar em 2026" | "pis pasep esquecido" (33K/mo, 35) | 1800 | MOFU | João | "Verificar saldos via SAQUEI" | 2026-07-15 |
| 2 | Blog | "INSS: benefícios não reclamados em 2026" | "inss benefício esquecido" (18K/mo, 39) | 1900 | BOFU | Maria | "Auditoria patrimonial R$ 29" | 2026-07-22 |
| 3 | Pillar | "FGTS inativo: como sacar R$ X em 2026" | "fgts inativo sacar" (61K/mo, 41) | 3200 | MOFU | Lucas | "Auditoria FGTS+restituições R$ 29" | 2026-07-29 |
| ... (7 more com mesmo level de detalhe) |

## 24 Social Posts

### Twitter (12 posts, 1/week × 12 weeks)
| W | Hook A | Hook B | CTA | Target |
|---|---|---|---|---|
| 1 | "🚨 75% dos brasileiros têm dinheiro esquecido em 4+ fontes oficiais" (stat shock) | "Você sabia que a média brasileira tem R$ 4.200 esquecidos no CPF?" (pergunta) | "Link no perfil para auditoria grátis" | 200 likes, 30 RTs |
| 2 | "Receita federal: 7 restituições que TODA família esquece" | "Sua mãe tem dinheiro esquecido. Sua avó também." | "Auditoria 30s — link na bio" | 250+30 |
| ... 10 more |

### LinkedIn (12 posts B2B angle — para contadores parceiros)
| W | Format | Angle | Target |
|---|---|---|---|
| 1 | Carousel 10 slides | "Contadores: como 5 verificações automatizadas economizam 8h/cliente" | 100 saves, 10 DMs |
| ... 11 more |

## 6 Newsletter Editions

| Edição | Subject A | Subject B | Segment | Open target | CTA |
|---|---|---|---|---|---|
| #28 | "O R$ esquecido que sua mãe tem (provavelmente)" | "5 minutos pode valer R$ 4.200 hoje" | all 12K subs | 38% (vs 32% benchmark BR fintech) | Auditoria R$ 29 |
| #29 | "Reforma Tributária BR 2026: 3 R$ que você ainda pode recuperar" | "AT muda restituição em Janeiro — antes ou depois?" | high-engagement 4K | 42% | Pre-2026 auditoria |
| ... 4 more |

## Reuse Matrix

Cada Pillar → 4 derivative formats:

| Origem | LinkedIn | Twitter Thread | Newsletter Section | Vídeo TikTok/Reel |
|---|---|---|---|---|
| Pillar W1 (Como descobrir R$ esquecidos) | Carousel 8 slides | Thread 12 tweets | Edição #28 main story | 90s "antes vs depois" |
| Pillar W3 (FGTS inativo) | Long-form post | Thread 8 tweets | Edição #30 main story | 60s "sacar em 3 cliques" |
| ... |

## SEO Checklist (per artigo)

Aplicar a cada um dos 12 pillars antes de publish:
- [x] Primary kw em: title, H1, first 100 words, 1+ H2, meta desc, 2+ alt texts
- [x] Internal links: 3+ para SAQUEI tool pages (verificar-cpf, restituições, fgts)
- [x] External link: 1+ para fonte oficial (receita.fazenda.gov.br, gov.br/inss)
- [x] FAQPage schema: 4 perguntas com markup
- [x] Readability: Flesch BR > 60 (target sub-graduação)
- [x] Featured snippet target: H2 = pergunta + parágrafo resposta <40 words

## Distribution Plan

- **Blog posts**: WordPress agendado weekly Mondays 09:00 BRT
- **Social**: Buffer scheduled, Twitter Tue+Thu 12:00, LinkedIn Wed 18:00
- **Newsletter**: Mailchimp, bi-weekly Fridays 10:00 BRT
- **TikTok/Reel**: org content team, 2/week Mon+Thu 19:00 BRT

## Owner + Workflow

- Lucas (head of content): 6 pillars
- Maria (SEO writer): 4 blogs
- João (junior writer): 2 blogs + research
- Brief approval: Lucas + Filipe (founder) por sexta da semana antes
- QA gate: lucas-quality skill score >=80 antes de publish
```

## Output anti-patterns

- "Artigo sobre SEO" sem keyword + volume + difficulty
- "Posts sociais" sem hook A/B + platform + CTA específico
- "Newsletter mensal" sem segment + open rate target
- Deadline "Q3" sem date concreta
- Author "freelancer" sem nome
- SEO checklist sem numbers (densidade kw, links count)
- Reuse matrix mencionada mas tabela vazia
- Output sem frontmatter (impede tracking)
- Placeholder <Client>/<keyword> em vez de real data
