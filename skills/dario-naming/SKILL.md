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

## Delivery-ready self-check (run BEFORE delivering naming output ao cliente)

Naming workshop é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1. 5+ Nomes scored em rubric 5-dim
- [ ] Mínimo 5 nomes propostos
- [ ] Cada nome scored em: pronunciability + memorability + meaning + availability + strategic fit
- [ ] Score numérico (1-10 ou 0-5) com criteria explícito
- [ ] Top pick + 2 fallbacks identificados

❌ NOT delivery-ready: "Nomes: Acme, Beta, Gamma"
✅ Delivery-ready: "ZELEI (45/50): pronunc 9, memo 8, meaning 9 (BR slang), .com.br+.com livres, fit Caregiver 8"

### 2. Domain + Trademark REAL (whois + INPI/EUIPO cited)
- [ ] .com / .br / .pt / .eu availability per nome (whois data)
- [ ] INPI/EUIPO classes específicas checked
- [ ] Social handles (Instagram, LinkedIn, Twitter)
- [ ] Phonetic confusion check

### 3. Meaning audit cross-language (PT + EN + ES)
- [ ] Native speaker reviewed (or assumption noted)
- [ ] Cultural taboos target market checked

### 4. Strategic fit + 3-sentence rationale por top 3
- [ ] Cada nome ancorado em archetype/strategy
- [ ] Por que score onde está

### 5. Next steps actionable
- [ ] INPI/EUIPO filing recommendation + cost estimate
- [ ] Domain registration urgency
- [ ] Phonetic test plan
- [ ] Fallback budget

### 6. Client name + REAL data, no placeholders

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output de naming deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via tool call real (WHOIS, INPI, EUIPO, Google search)
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — score/previsão por design (não verificável objectivamente)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs. o que precisa de validação antes de registar qualquer nome.  **Honest transparency > shortlist que parece mais limpa do que é.**

❌ **NOT delivery-ready:**
```
| Vórtex | 9 | 8 | 9 | ✅ .com livre | ✅ handles livres | OK | 26/30 |
```
*Sem labels — cliente assume que domínio e INPI foram verificados em real-time. Se não foram, expõe o projecto a conflito de marca ou domínio já tomado.*

✅ **Delivery-ready:**
```
| Vórtex | 🟢 9/10 (score subjectivo) | 🟢 8/10 | 🟡 .com — não verificado ao vivo, assumed available | 🔵 @vortex IG — 404 confirmado via search | 🟡 INPI classe 35 — quick screen, não tool call real | 26/30 |
```
```
Top pick: Vórtex
🔵 Pronunciável em PT e EN — confirmado análise linguística desta sessão
🟡 .com disponível — assumed, requer WHOIS ao vivo antes de registar
🟡 Sem conflito INPI classe 42 — screen visual, não substituí advogado de marcas
🟢 Score de memorabilidade 9/10 — avaliação por design, subjectivo
```

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — WHOIS ao vivo para cada finalista, handles verificados em cada plataforma
- [ ] Todos os itens 🔵 com source citada — ex: "INPI pesquisa em DD/MM/AAAA, classe X, resultado: sem conflito"
- [ ] Todos os itens 🟢 sinalizados ao cliente como scores subjectivos, não rankings absolutos
- [ ] Cliente informado que screen INPI/EUIPO **não substitui** consulta com advogado de marcas antes de registar

## Fully-worked A-tier example: Cuidai BR

```markdown
---
project: Cuidai BR
date: 2026-05-23
type: naming-workshop
top_pick: ZELEI
---

# Naming Workshop — Cuidai BR

## 5 Names Scored (50 max)
| Nome | Pronunc | Memo | Meaning | Domain | Fit | Total |
|---|---|---|---|---|---|---|
| **ZELEI** ⭐ | 9 | 9 | 9 | 10 | 8 | 45 |
| Cuidai | 10 | 8 | 9 | 5 | 9 | 41 |
| Vela | 8 | 7 | 7 | 8 | 7 | 37 |

## Domain + Trademark (2026-05-23)
| Nome | .com.br | .com | INPI BR | EUIPO | IG | LI |
|---|---|---|---|---|---|---|
| ZELEI | ✅ | ✅ | ✅ classes 35+44 | ✅ | @zelei free | free |
| Cuidai | ❌ parked | ⚠️ R$ 8K | ⚠️ partial | ✅ | @cuidai_app | free |

## Meaning Audit
- ZELEI: PT slang "cuidei", EN nothing, ES nothing. Maria PT-BR + Lucas PT-PT + Carla ES validated positive.

## Top pick: ZELEI
Rationale: (1) universal pronunciation PT/EN/ES, (2) meaning ancorado em "cuidei de", (3) availability completa .com.br + .com + INPI clean.

## Next Steps
1. INPI BR filing R$ 1.940/class × 2 = R$ 3.880, 8-12mo
2. Domain registration zelei.com.br + zelei.com hoje (~R$ 90 total)
3. Social handles @zelei block all platforms hoje
4. Phonetic test 5 mães BR cold pronounce, target >80% correct
5. Fallback Cuidai .com.br negotiation budget R$ 15K se INPI ZELEI fail
```

## Output anti-patterns
- Lista de nomes sem scoring rubric
- Domain check placeholder "verificar"
- INPI/EUIPO sem classes específicos
- Meaning audit incompleto (sem ES ou EN)
- Recommendation sem rationale 3-sentences
- Next steps vagos
- Output sem frontmatter
- Placeholder <projecto>/<nome> em vez de real
