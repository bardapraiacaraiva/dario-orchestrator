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

## Delivery-ready self-check (run BEFORE delivering to client)

A brand strategy output is **delivery-ready (90+/100)** only if ALL of these are true. If any is missing, mark as draft and complete before delivery.

### 1. Archetype JUSTIFICATION (not just naming)
- [ ] Archetype name (one of the 12)
- [ ] **3+ sentence rationale** citing: (a) founder's actual values, (b) customer's emotional driver, (c) why NOT the closest alternative archetype
- [ ] Optional secondary archetype with the same rationale depth

❌ NOT delivery-ready: "Archetype: Sage" (no rationale)
✅ Delivery-ready: "Archetype: Sage. Founder's 12 years in BdP supervision means truth-telling is more than positioning — it's identity. Customer (PME CFO) optimises for confidence in numbers, not features. Sage chosen over Caregiver because the client is sold to as a thinking partner, not a protective parent."

### 2. Differentiators MUST be 3-5 CONCRETE items (not generic)
- [ ] Each differentiator names a SPECIFIC mechanism, integration, certification, or contractual term
- [ ] Each differentiator passes the "competitor claim test": no direct competitor offers exactly this
- [ ] At least one differentiator has a number or measurable bound

❌ NOT delivery-ready: "Quality, innovation, customer focus"
✅ Delivery-ready:
  - "Native SAFT-PT validation in real-time, not at month-end close (Moloni does month-end)"
  - "Banco de Portugal SIBS/IBAN integration validated by the BdP API directly (SAGE uses screen-scrape)"
  - "30-day deploy SLA with €5K refund if missed (industry standard is 90 days, no penalty)"

### 3. Onlyness statement passes the unique-mechanism test
- [ ] Each <slot> in the template is unique to this brand vs ALL named competitors
- [ ] The "because <why>" maps to a founder belief or proven track record, not aspiration

### 4. Positioning statement is SPECIFIC, not template-filled
- [ ] <target> names a precise sub-segment (not "everyone in PT")
- [ ] <insight> is something the target would actually agree with if asked
- [ ] <reason to believe> is verifiable (numbers, customers, integrations, certifications)

### 5. Voice guide has "Is / Is Not" populated
- [ ] At least 4 voice attributes
- [ ] At least 5 "is / is not" pairs

### 6. Output uses CLIENT NAME + REAL data throughout
- [ ] Client name appears in every section title
- [ ] No placeholder phrases like "<target>", "<brand>", or unfilled angle brackets
- [ ] All examples reference the client's actual product, market, or stage

## Red flags / anti-patterns (mirror of self-check, for fast spotting)
- Archetype chosen because "it's cool" vs genuinely fitting
- Positioning that says "quality and innovation" (zero differentiation)
- "Unique" claims that competitors also claim
- Customer as Hero is violated (brand plays Hero instead of Guide)
- Voice guide without "is not" examples (leaves ambiguity)
- Brand decision taken without founder values input
- Generic differentiator without a specific mechanism, integration, or measurable bound
- Output contains placeholder angle-brackets (<target>, <brand>) instead of real names

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output de brand strategy deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via inputs do cliente (briefing, sessão, dados reais)
- 🟡 **assumed** — plausível dado o sector/arquétipo, mas precisa confirmação pré-entrega
- 🟢 **projection** — forecast estratégico by design (aspiracional, não verificável agora)

Output checklist upfront mostra ao cliente exatamente o que é trust-as-is vs. o que precisa de validação. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> Archetype: Magician. Competitors: Notion, Linear, Figma. Tagline: "Build what others can't." Target: founders 25-40.

Nenhum label → reader assume tudo verified. Archetype pode estar errado. Competitors podem ser irrelevantes. Tagline pode estar colidindo com concorrente existente.

---

✅ Delivery-ready:

| Item | Label | Status |
|---|---|---|
| Archetype primário: **Magician** | 🟡 assumed | Derivado do sector SaaS + valores do founder — confirmar fit emocional com founder |
| Competitor set: Notion, Linear, Figma | 🟡 assumed | Sugeridos por contexto; cliente deve validar os 3-5 que considera ameaça real |
| Tagline: *"Build what others can't"* | 🟢 projection | Proposta criativa — testar recall com 3-5 pessoas do target antes de fixar |
| Founder story (origem 2019, Lisboa) | 🔵 verified | Confirmado em briefing sessão 14/06 |
| Onlyness statement — slot "category" | 🟡 assumed | "design-ops platform" é hipótese; cliente pode preferir categoria diferente |
| Proof points (3 casos de cliente) | 🔵 verified | Fornecidos pelo cliente via doc partilhado |
| Positioning target: "scale-ups B2B SaaS" | 🟡 assumed | Inferido do portfolio; confirmar se exclui consciente o mercado B2C |
| Kapferer — faceta Reflection | 🟢 projection | "Visto como líder técnico visionário" — aspiracional, não validado com audience real |

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumptions com actuals (archetype, competitors, category slot, target)
- [ ] All 🔵 citations referenciadas com fonte/sessão/doc no deliverable final
- [ ] All 🟢 projections comunicadas explicitamente ao cliente como aspiracionais ("isto é onde queremos chegar, não onde estamos")
- [ ] Onlyness statement revisto com slots todos únicos — nenhum borrowed de competitor
- [ ] Differentiation test (5 checks) passado para cada claim 🔵 ou 🟡 antes de fixar copy

## Fully-worked A-tier example (delivery-ready reference)

This is what a 92+/100 dario-brand output looks like. Use as anchor for self-check.

```markdown
---
project: LUSOconta
date: 2026-05-23
type: brand-strategy
archetype: Sage
---

# Brand Strategy — LUSOconta

## Context & Scope
- Business: SaaS de contabilidade para PMEs portuguesas, integração nativa
  com Banco de Portugal + SAFT-PT real-time.
- Target: CFOs e contabilistas sénior de empresas 50-250 colaboradores em PT.
- Competitors: Moloni, SAGE Negócios, Primavera SOL.
- Ambition: Padrão de mercado para PMEs PT em 36 meses.

## Archetype
**Primary:** Sage

**Rationale:**
O founder passou 12 anos na supervisão prudencial do Banco de Portugal —
truth-telling sobre contabilidade não é positioning, é identidade. O
target (CFO de PME) optimiza decisão por *confiança nos números*, não
por features bonitas. Sage escolhido em vez de Caregiver porque LUSOconta
vende-se como *thinking partner do CFO*, não como pai protector. E em
vez de Magician porque o produto promete clareza, não transformação.

## Onlyness Statement
LUSOconta é a única plataforma de contabilidade que valida SAFT-PT
em tempo real através da API direta do Banco de Portugal para CFOs e
contabilistas de PMEs 50-250 colaboradores em Portugal que tratam
compliance como vantagem competitiva, porque o founder construiu a
ferramenta que ele próprio queria ter tido enquanto supervisor do BdP.

## Differentiators (5 concrete, defensible)
1. **Native SAFT-PT validation in real-time** — não no fecho do mês,
   continuous (Moloni e SAGE só validam no fecho mensal)
2. **Banco de Portugal SIBS/IBAN via API directa** — validation oficial
   (SAGE faz screen-scrape, Moloni manual entry)
3. **30-day deploy SLA com €5K refund** se missed (mercado: 90 dias, zero
   penalty)
4. **Dashboard CFO real-time com 10 KPIs decisórios** (concorrência
   foca em compliance, não em decisão)
5. **Audit-proof guarantee** — se AT aplicar penalty por compliance que
   devíamos detectar, devolvemos 12 meses + multa

## Positioning Statement
Para CFOs e contabilistas de PMEs 50-250 em PT que vêem compliance
como vantagem competitiva e não burocracia, LUSOconta é a plataforma
de contabilidade que valida SAFT-PT em tempo real porque o founder
construiu-a a partir da experiência de 12 anos a supervisor o sistema
no Banco de Portugal. Unlike Moloni e SAGE, fornecemos validação BdP
directa em vez de screen-scraping e oferecemos audit-proof guarantee.

## Voice attributes (4)
1. Confiante mas humilde — afirma sem floreados, admite incertezas
2. Técnico mas claro — usa termos correctos, explica quando necessário
3. Profundo, não rápido — preferimos parágrafos certos a slogans
4. Português europeu rigoroso — sem brasileirismos nem anglicismos

### Is / Is Not
| Is | Is Not |
|---|---|
| "A regra do CIVA artigo 36 é..." | "Tipo, IVA sabe?" |
| "Validámos contra a base do BdP" | "Trust us, está certo" |
| "Recomendamos hesitar antes de..." | "Vai, depois logo se vê" |
| "Cá entre nós, este caso é raro" | "Hahaha cuidado!" |
| "O nosso compromisso é compliance" | "Vamos ser inovadores!" |

## Differentiation Test
- [x] Specific (5 differentiators com mecanismos nomeados)
- [x] True (cada um verificável + entregável)
- [x] Valuable (CFO PME paga premium por estes)
- [x] Defensible (Moloni/SAGE não pode copiar tudo)
- [x] Memorable ("BdP direct" é hook que cola)

## Next Steps
- Visual identity brief — logo conservador + paleta deep-blue/gold/cream
- Copy rollout — homepage, comparison page vs Moloni/SAGE, audit landing
- Brand guidelines doc — voice cheatsheet + caveats em 1 página
```

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
