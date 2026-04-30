---
name: dario-naming
description: Brand naming workshop — generates name candidates using linguistic analysis, archetype alignment, domain availability check, trademark screening, and shortlist scoring. Triggers on "naming", "nome da marca", "brand name", "nome do produto", "nome do projeto".
license: MIT
---

# DARIO Skill — Brand Naming

Structured naming process that produces 20-30 candidates, filters by criteria, and delivers a scored shortlist of 5-7 names.

## When to activate
- New brand or product launch
- Rename / rebrand
- Sub-brand creation
- Naming for a service, app, or SaaS product

## Workflow

### 1. Gather inputs
- **What it is** (product/service/brand category)
- **Target audience** (who uses it)
- **Brand archetype** (from `dario-brand` if exists)
- **Tone** (premium, playful, tech, traditional, disruptive)
- **Language** (PT, EN, both, other)
- **Naming constraints** (max chars, must include X, must NOT include Y)
- **Domain requirements** (.com, .pt, .io, flexible)
- **Competitor names** (to avoid similarity)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "naming strategy brand archetype", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "yohn heyward wheeler naming domain", collection: "dario", limit: 5)
```

### 3. Generate candidates (7 categories, ~4 each)
- **Descriptive:** says what it does (e.g. "PayPal", "YouTube")
- **Suggestive/Evocative:** implies a quality (e.g. "Uber", "Slack")
- **Abstract/Invented:** neologism (e.g. "Kodak", "Xerox")
- **Compound:** two words merged (e.g. "Facebook", "WordPress")
- **Acronym/Abbreviation:** (e.g. "IBM", "IKEA")
- **Founder/Place:** eponymous (e.g. "Tesla", "Lisbon")
- **Metaphorical:** borrowed meaning (e.g. "Amazon", "Apple")

### 4. Filter checklist (per candidate)
- [ ] Pronounceable in target language(s)
- [ ] Spellable on first hearing (phone test)
- [ ] No negative connotation in PT/EN/ES
- [ ] .com or .pt domain available (or purchasable <€500)
- [ ] No trademark conflict (INPI.pt + EUIPO quick check)
- [ ] Social handles available (@name on IG, X, LinkedIn)
- [ ] Google search doesn't return dominant competitor
- [ ] ≤12 characters (ideally ≤8 for memorability)
- [ ] Works as hashtag (no double-meaning when concatenated)

### 5. Score shortlist (top 5-7)
| Name | Memorability | Relevance | Distinctiveness | Domain | Handles | Trademark | Total |
|---|---|---|---|---|---|---|---|
| ... | /10 | /10 | /10 | Y/N | Y/N | OK/Risk | /30 |

### 6. Present recommendation
- **Top pick** with rationale
- **Runner-up** (safe alternative)
- **Bold pick** (higher risk, higher reward)

## Domain Check Method

1. **WHOIS lookup** — check `.com` and `.pt` via `whois` or web tool
2. **PT domains (.pt)** — DNS.pt is the registry. `.pt` WHOIS is often blocked; try `https://www.dns.pt/en/domain-search`
3. **Expired domains** — check if available via aftermarket (GoDaddy Auctions, Sedo)
4. **Social handles** — check @name on Instagram, Twitter/X, LinkedIn, Facebook, TikTok
5. **Google search** — first page results. If a strong brand owns page 1, avoid the name

## INPI Trademark Quick Screen

1. Go to `https://servicosonline.inpi.pt/pesquisas/main/marcas.jsp`
2. Search exact name in Nice classes relevant to client's industry
3. Check EUIPO `https://euipo.europa.eu/eSearch/` for EU-wide conflicts
4. If conflict found: note the class and owner. Same class = high risk. Different class = medium risk.
5. **This is a screen, not legal advice** — always recommend client confirm with a trademark lawyer before registering

## Linguistic Analysis Checklist

For each finalist name:
- **Portuguese pronunciation** — natural? No awkward sounds?
- **English pronunciation** — works for international clients?
- **Spanish cross-check** — no negative meaning (important for Iberian market)
- **French cross-check** — no negative meaning (former colonies, Africa market)
- **Abbreviation test** — what happens when shortened? (e.g., "ASS" problem)
- **Rhyme/rhythm** — does it flow? Count syllables (2-3 ideal)
- **Alliteration** — bonus if natural (e.g., Coca-Cola, PayPal)

## Output Template

```markdown
# Brand Naming Workshop — <Client>

## Brief
- Category: ...
- Archetype: ...
- Tone: ...
- Constraints: ...

## 28 Candidates (7 categories x 4 each)
| # | Name | Category | Notes |
|---|------|----------|-------|
| 1 | ... | Descriptive | ... |
| ... | | | |

## Filter Results
Passed filter: X of 28
Failed: [list with reason]

## Scored Shortlist (Top 7)
| Name | Memorability | Relevance | Distinct | Domain | Handles | INPI | Total /30 |
|---|---|---|---|---|---|---|---|
| ... | | | | | | | |

## Recommendation
**Top pick:** ... — [rationale]
**Runner-up:** ... — [rationale]
**Bold pick:** ... — [rationale]

## Next Steps
1. Client picks finalist
2. Trademark lawyer confirms INPI/EUIPO
3. Register domain + social handles
4. Update brand guidelines with new name
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Brand Naming Workshop.md`

## Red Flags

- Never present a name without checking domain availability first
- Never skip INPI/EUIPO search — trademark conflicts are expensive to fix
- Never recommend a name that's hard to spell on the phone
- Always provide at least 5 scored alternatives (client may reject top pick)
- Always check meaning in PT, EN, and ES at minimum for Iberian market
