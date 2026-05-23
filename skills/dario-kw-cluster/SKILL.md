---
name: dario-kw-cluster
description: Semantic keyword clustering — groups keywords by intent and topic into content clusters for site architecture and content planning. Pairs with seo-dataforseo for live volume data. Triggers on "keyword cluster", "topic cluster", "keyword map", "content cluster", "keyword grouping", "pillar page".
license: MIT
---

# DARIO Skill — Keyword Clustering

Takes a list of keywords (or a seed topic) and groups them into semantic clusters for content architecture. Each cluster becomes a pillar page + supporting articles + internal linking map.

## When to activate
- Content strategy from scratch
- Site architecture planning
- After keyword research (from seo-dataforseo or manual)
- Blog editorial calendar design
- URL structure redesign

## Workflow

### 1. Gather keywords
Sources:
- User-provided list
- `/seo-dataforseo` keyword suggestions for seed terms
- GSC queries export
- Competitor keyword analysis
- "People also ask" / related searches

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "semantic keyword clustering content architecture pillar", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "search intent informational transactional navigational", collection: "dario", limit: 5)
```

### 3. Classify intent per keyword
- **Informational** → "how to", "what is", "guide", "tutorial"
- **Navigational** → brand names, specific pages
- **Commercial investigation** → "best", "vs", "review", "top 10"
- **Transactional** → "buy", "price", "coupon", "hire", "contratar"

### 4. Cluster by semantic topic
Group keywords that target the same search intent + topic. Rules:
- Same SERP overlap (>3 shared URLs in top 10) = same cluster
- One cluster = one page (avoid cannibalization)
- Name each cluster by its primary keyword (highest volume)

### 5. Build cluster map

```
Pillar: "design de interiores lisboa" (800/mo)
├── Supporting: "design interiores moderno apartamento" (210/mo)
├── Supporting: "quanto custa design interiores" (170/mo)
├── Supporting: "designer interiores preços portugal" (140/mo)
├── Supporting: "remodelação apartamento lisboa" (390/mo)
└── Supporting: "home staging lisboa" (90/mo)
```

### 6. Content brief per cluster
For each cluster page:
- **Primary KW** + volume + difficulty
- **Secondary KWs** (2-5)
- **Intent** match
- **URL** proposed
- **H1** suggested
- **Content type** (guide, comparison, service page, blog)
- **Word count** target (based on SERP average)
- **Internal links** to/from pillar and siblings

## Output template
```markdown
# Keyword Cluster Map — <Client / Topic>

## Cluster 1: <Primary KW> (vol/mo)
| Keyword | Volume | Difficulty | Intent | Target URL |
|---|---|---|---|---|
| ... | | | | |

**Content brief:** ...
**Internal linking:** pillar ↔ support articles

## Cluster 2: ...
```

## Cannibalization Check

Before finalizing clusters, check for keyword cannibalization:
1. Search each primary keyword on the client's site: `site:domain.com "keyword"`
2. If 2+ pages rank for the same keyword → merge into one or 301 redirect the weaker
3. If zero pages rank → new content opportunity
4. Document in the cluster map: "Existing URL" column with current ranking page if any

## Integration

- Pairs with `seo-dataforseo` for live volume/difficulty data
- Feeds into `seo-plan` for site architecture
- Content briefs feed into `dario-content` for production
- Pillar page structure feeds into `seo-sitemap`

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Keyword Cluster Map.md`

## Red Flags

- Never create a cluster with only 1 keyword — that's a page, not a cluster
- Never assign two clusters to the same URL — one URL, one cluster
- Never skip intent classification — informational and transactional keywords need different pages
- Always validate SERP overlap before merging keywords into a cluster
- Always check existing content first to avoid creating duplicates
- Minimum 3 supporting articles per pillar page for internal linking effectiveness

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Cobertura mínima de clusters
- [ ] Cada cluster tem **mínimo 1 pillar + 3 supporting keywords** (nunca 1 kw isolada)
- [ ] Número de clusters cobre todos os tópicos core do negócio do cliente (sem lacunas óbvias)
- [ ] Nenhum cluster tem >15 keywords sem sub-divisão temática justificada
- ❌ NOT delivery-ready: "Cluster: dog care (3 keywords)"
- ✅ Delivery-ready: "Pillar: 'creche para cães lisboa' (480/mo) + 5 supporting: 'hotel cães lisboa' (320/mo), 'babysitting cães' (140/mo)..."

### Gate 2 — Intent classification completa
- [ ] **Cada keyword** tem intent atribuído (Informational / Commercial / Transactional / Navigational)
- [ ] Keywords transacionais e informacionais com o mesmo tema estão em **clusters separados** (ex: "como treinar cão" ≠ "contratar treino cão lisboa")
- [ ] Nenhuma linha com célula Intent vazia na tabela
- ❌ NOT delivery-ready: "design interiores | 800 | 35 | — | /design"
- ✅ Delivery-ready: "design de interiores lisboa | 800 | 38 | Transactional | /servicos/design-interiores-lisboa"

### Gate 3 — Cannibalization check documentado
- [ ] Coluna "Existing URL" presente e preenchida (ou explicitamente "—" = nova página)
- [ ] Qualquer página existente do cliente com solapamento identificada e acção recomendada (merge / 301 / expand)
- [ ] Confirmação explícita `site:domain.com` foi executado para os primary KWs dos pillar pages
- ❌ NOT delivery-ready: Tabela sem coluna Existing URL, sem menção a conteúdo já publicado
- ✅ Delivery-ready: "Existing URL: /blog/quanto-custa-design-interiores — MERGE com Cluster 3 (301 recomendado)"

### Gate 4 — Volumes e dificuldade reais (não estimados a olho)
- [ ] Volumes têm fonte indicada: DataForSEO, GSC, Ahrefs, ou "estimativa manual" com aviso
- [ ] Difficulty score presente (0-100) para cada primary KW dos pillars
- [ ] Nenhum volume com formato vago como "médio" ou "alto" — números reais ou range (ex: 200-400/mo)
- ❌ NOT delivery-ready: "remodelação apartamento | alto volume | difícil | ..."
- ✅ Delivery-ready: "remodelação apartamento lisboa | 390/mo (DataForSEO) | KD 42 | Commercial | /remodelacao-apartamentos-lisboa"

### Gate 5 — Content brief accionável por cluster
- [ ] Cada cluster tem: Primary KW + Secondary KWs (2-5) + URL proposta + H1 sugerido + Content type + Word count target
- [ ] URL proposta segue slug limpo, lowercase, hifens, sem acentos
- [ ] Word count baseado em SERP benchmark (não inventado) — ou justificado ("top 3 avg: 1.800 palavras")
- ❌ NOT delivery-ready: "Brief: escrever sobre design de interiores moderno, SEO, fotos"
- ✅ Delivery-ready: "URL: /blog/design-interiores-moderno-apartamento | H1: Design de Interiores Moderno para Apartamentos: Guia 2025 | Type: Informational guide | Target: 1.600 words (SERP avg top-5)"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders com angle-brackets
- [ ] Zero instâncias de `<Client>`, `<Topic>`, `<URL>`, `<keyword>` no output final
- [ ] Nome do cliente aparece no título do documento e no save path
- [ ] Datas, domínios, URLs são reais e verificáveis (não "seusite.com" ou "exemplo.pt")
- ❌ NOT delivery-ready: `# Keyword Cluster Map — <Client / Topic>`
- ✅ Delivery-ready: `# Keyword Cluster Map — Lisbon Dog Care | Maio 2025`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados reais do cliente
- 🟡 **assumed** — plausível mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — forecast por design (não verificável até publicação/indexação)

Output checklist upfront mostra ao reader exatamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
Cluster 1: "design de interiores lisboa" (800/mo, KD 42)
Supporting: "remodelação apartamento lisboa" (390/mo)
→ Sem labels — reader não sabe se volumes são live data de hoje,
  exportados há 6 meses, ou estimativas manuais. Tudo parece "verified".
```

✅ Delivery-ready:
```
Cluster 1: "design de interiores lisboa"
- Volume: 800/mo 🔵 verified — extraído DataForSEO 2025-01-14
- KD: 42 🔵 verified — DataForSEO mesma pull
- Supporting "remodelação apartamento lisboa": 390/mo 🟡 assumed — volume de memória, confirmar com pull fresca
- URL proposta /design-interiores-lisboa: 🟡 assumed — sem acesso ao site; confirmar não existe já
- Tráfego esperado pós-publicação: +420 visitas/mês 🟢 projection — estimativa CTR 8% × volume
- Dificuldade de ranquear em 90 dias: média 🟢 projection — baseado em KD + DA do domínio estimado
```

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — volumes re-pulled com data fresca, URLs existentes verificadas no site real
- [ ] Todas as fontes 🔵 citadas com data da extração (DataForSEO / GSC / export manual)
- [ ] Todos os 🟢 projections comunicados ao cliente como forecast, não como garantia de resultado

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Keyword Cluster Map — Lisbon Dog Care | Maio 2025
**Domínio:** lisbondogcare.pt | **Fonte volumes:** DataForSEO PT-PT | **Data:** 2025-05-14

---

## Cluster 1 (Pillar): creche para cães lisboa (480/mo)

| Keyword | Volume | KD | Intent | Target URL | Existing URL |
|---|---|---|---|---|---|
| creche para cães lisboa | 480 | 28 | Transactional | /creche-caes-lisboa | — (nova) |
| creche cães preços lisboa | 210 | 24 | Transactional | /creche-caes-lisboa | — |
| jardim infantil cães lisboa | 140 | 18 | Transactional | /creche-caes-lisboa | — |
| creche canina alfama | 90 | 15 | Navigational | /creche-caes-lisboa | — |
| deixar cão durante dia lisboa | 170 | 22 | Transactional | /creche-caes-lisboa | — |

**Content brief:**
- **Primary KW:** creche para cães lisboa (480/mo, KD 28)
- **Secondary KWs:** creche cães preços, jardim infantil cães, deixar cão durante dia lisboa
- **Intent:** Transactional (service page)
- **URL:** /creche-caes-lisboa
- **H1:** Creche para Cães em Lisboa — Cuidados Diários com Amor e Segurança
- **Content type:** Service page
- **Word count target:** 900 palavras (SERP top-5 avg)
- **Internal links:** → /hotel-caes-lisboa (sibling), → /sobre-nos (navigational), ← /index (homepage)

---

## Cluster 2 (Pillar): hotel cães lisboa (320/mo)

| Keyword | Volume | KD | Intent | Target URL | Existing URL |
|---|---|---|---|---|---|
| hotel cães lisboa | 320 | 31 | Transactional | /hotel-caes-lisboa | /servicos (MERGE recomendado) |
| hotel canino lisboa preços | 190 | 27 | Transactional | /hotel-caes-lisboa | — |
| hospedar cão férias lisboa | 150 | 22 | Transactional | /hotel-caes-lisboa | — |
| pensão cães lisboa | 110 | 19 | Transactional | /hotel-caes-lisboa | — |

**Content brief:**
- **Primary KW:** hotel cães lisboa (320/mo, KD 31)
- **Secondary KWs:** hotel canino preços, hospedar cão férias, pensão cães
- **Intent:** Transactional (service page)
- **URL:** /hotel-caes-lisboa
- **H1:** Hotel para Cães em Lisboa — Hospedagem Segura Durante as Suas Férias
- **Content type:** Service page
- **Word count target:** 850 palavras (SERP top-5 avg)
- **⚠️ Cannibalization:** /servicos ranka para "hotel cães" (posição 14) — consolidar conteúdo aqui + 301 de /servicos para /hotel-caes-lisboa
- **Internal links:** → /creche-caes-lisboa (sibling), → /treino-caes-lisboa (cross-cluster), ← /index

---

## Cluster 3 (Blog Pillar): como escolher creche para cão (260/mo)

| Keyword | Volume | KD | Intent | Target URL | Existing URL |
|---|---|---|---|---|---|
| como escolher creche para cão | 260 | 21 | Informational | /blog/como-escolher-creche-caes | — |
| o que perguntar creche cães | 90 | 14 | Informational | /blog/como-escolher-creche-caes | — |
| creche cães segura checklist | 70 | 16 | Informational | /blog/como-escolher-creche-caes | — |
| sinais mau comportamento creche canina | 50 | 12 | Informational | /blog/como-escolher-creche-caes | — |

**Content brief:**
- **Primary KW:** como escolher creche para cão (260/mo, KD 21)
- **Secondary KWs:** o que perguntar creche cães, checklist creche segura
- **Intent:** Informational (blog guide)
- **URL:** /blog/como-escolher-creche-caes
- **H1:** Como Escolher a Melhor Creche para o Seu Cão: 7 Critérios Essenciais
- **Content type:** Informational guide + checklist
- **Word count target:** 1.400 palavras (SERP top-3 avg)
- **Internal links:** → /creche-caes-lisboa (CTA transactional), → /hotel-caes-lisboa, ← /blog (index)

---

**Save:** `05 - Claude - IA/Outputs/2025-05-14 - Lisbon Dog Care - Keyword Cluster Map.md`
```

---

## Output anti-patterns

- Criar cluster com 1 única keyword — isso é uma página, não um cluster; nunca entrega sem mínimo 4 kws agrupadas
- Omitir coluna "Existing URL" — cannibalization não detectada = trabalho duplicado para o cliente
- Usar "volume alto/médio/baixo" em vez de números — sem dados verificáveis o cliente não consegue priorizar
- Misturar intent informacional e transactional no mesmo cluster — cria cannibalization estrutural desde o início
- Propor URLs com acentos, maiúsculas ou espaços — `/Design-Interiores-Lisboa` quebra em produção
- Deixar H1 idêntico ao Primary KW — demonstra zero value-add; o H1 deve expandir e contextualizar
- Cluster map sem internal linking map — a arquitectura fica desconectada e perde equity de PageRank
- Entregar sem cannibalization check documentado para os pillar pages — erro crítico que o cliente vai descobrir em auditoria
- Gerar clusters genéricos sem adaptar ao sector do cliente — "como fazer X" para um cliente B2B SaaS é desperdício de crawl budget
- Usar o template com angle-brackets por preencher (`<Client>`, `<URL>`) — entrega não-profissional que invalida credibilidade do trabalho
