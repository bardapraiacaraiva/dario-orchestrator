---
name: seo-programmatic
description: >
  Programmatic SEO planning and analysis for pages generated at scale from data
  sources. Covers template engines, URL patterns, internal linking automation,
  thin content safeguards, and index bloat prevention. Use when user says
  "programmatic SEO", "pages at scale", "dynamic pages", "template pages",
  "generated pages", or "data-driven SEO".
user-invokable: true
argument-hint: "[url or plan]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# Programmatic SEO Analysis & Planning

Build and audit SEO pages generated at scale from structured data sources.
Enforces quality gates to prevent thin content penalties and index bloat.

## Data Source Assessment

Evaluate the data powering programmatic pages:
- **CSV/JSON files**: Row count, column uniqueness, missing values
- **API endpoints**: Response structure, data freshness, rate limits
- **Database queries**: Record count, field completeness, update frequency
- Data quality checks:
  - Each record must have enough unique attributes to generate distinct content
  - Flag duplicate or near-duplicate records (>80% field overlap)
  - Verify data freshness; stale data produces stale pages

## Template Engine Planning

Design templates that produce unique, valuable pages:
- **Variable injection points**: Title, H1, body sections, meta description, schema
- **Content blocks**: Static (shared across pages) vs dynamic (unique per page)
- **Conditional logic**: Show/hide sections based on data availability
- **Supplementary content**: Related items, contextual tips, user-generated content
- Template review checklist:
  - Each page must read as a standalone, valuable resource
  - No "mad-libs" patterns (just swapping city/product names in identical text)
  - Dynamic sections must add genuine information, not just keyword variations

## URL Pattern Strategy

### Common Patterns
- `/tools/[tool-name]`: Tool/product directory pages
- `/[city]/[service]`: Location + service pages
- `/integrations/[platform]`: Integration landing pages
- `/glossary/[term]`: Definition/reference pages
- `/templates/[template-name]`: Downloadable template pages

### URL Rules
- Lowercase, hyphenated slugs derived from data
- Logical hierarchy reflecting site architecture
- No duplicate slugs; enforce uniqueness at generation time
- Keep URLs under 100 characters
- No query parameters for primary content URLs
- Consistent trailing slash usage (match existing site pattern)

## Internal Linking Automation

- **Hub/spoke model**: Category hub pages linking to individual programmatic pages
- **Related items**: Auto-link to 3-5 related pages based on data attributes
- **Breadcrumbs**: Generate BreadcrumbList schema from URL hierarchy
- **Cross-linking**: Link between programmatic pages sharing attributes (same category, same city, same feature)
- **Anchor text**: Use descriptive, varied anchor text. Avoid exact-match keyword repetition
- Link density: 3-5 internal links per 1000 words (match seo-content guidelines)

## Thin Content Safeguards

### Quality Gates

| Metric | Threshold | Action |
|--------|-----------|--------|
| Pages without content review | 100+ | ⚠️ WARNING: require content audit before publishing |
| Pages without justification | 500+ | 🛑 HARD STOP: require explicit user approval and thin content audit |
| Unique content per page | <40% | ❌ Flag as thin content (likely penalty risk) |
| Word count per page | <300 | ⚠️ Flag for review (may lack sufficient value) |

### Scaled Content Abuse: Enforcement Context (2025-2026)

Google's Scaled Content Abuse policy (introduced March 2024) saw major enforcement escalation in 2025:

- **June 2025:** Wave of manual actions targeting websites with AI-generated content at scale
- **August 2025:** SpamBrain spam update enhanced pattern detection for AI-generated link schemes and content farms
- **Result:** Google reported 45% reduction in low-quality, unoriginal content in search results post-March 2024 enforcement

**Enhanced quality gates for programmatic pages:**
- **Content differentiation:** ≥30-40% of content must be genuinely unique between any two programmatic pages (not just city/keyword string replacement)
- **Human review:** Minimum 5-10% sample review of generated pages before publishing
- **Progressive rollout:** Publish in batches of 50-100 pages. Monitor indexing and rankings for 2-4 weeks before expanding. Never publish 500+ programmatic pages simultaneously without explicit quality review.
- **Standalone value test:** Each page should pass: "Would this page be worth publishing even if no other similar pages existed?"
- **Site reputation abuse:** If publishing programmatic content under a high-authority domain (not your own), this may trigger site reputation abuse penalties. Google began enforcing this aggressively in November 2024.

> **Recommendation:** The WARNING gate at `<40% unique content` remains appropriate. Consider a HARD STOP at `<30%` unique content to prevent scaled content abuse risk.

### Safe Programmatic Pages (OK at scale)
✅ Integration pages (with real setup docs, API details, screenshots)
✅ Template/tool pages (with downloadable content, usage instructions)
✅ Glossary pages (200+ word definitions with examples, related terms)
✅ Product pages (unique specs, reviews, comparison data)
✅ Data-driven pages (unique statistics, charts, analysis per record)

### Penalty Risk (avoid at scale)
❌ Location pages with only city name swapped in identical text
❌ "Best [tool] for [industry]" without industry-specific value
❌ "[Competitor] alternative" without real comparison data
❌ AI-generated pages without human review and unique value-add
❌ Pages where >60% of content is shared template boilerplate

### Uniqueness Calculation
Unique content % = (words unique to this page) / (total words on page) × 100

Measure against all other pages in the programmatic set. Shared headers, footers, and navigation are excluded from the calculation. Template boilerplate text IS included.

## Canonical Strategy

- Every programmatic page must have a self-referencing canonical tag
- Parameter variations (sort, filter, pagination) canonical to the base URL
- Paginated series: canonical to page 1 or use rel=next/prev
- If programmatic pages overlap with manual pages, the manual page is canonical
- No canonical to a different domain unless intentional cross-domain setup

## Sitemap Integration

- Auto-generate sitemap entries for all programmatic pages
- Split at 50,000 URLs per sitemap file (protocol limit)
- Use sitemap index if multiple sitemap files needed
- `<lastmod>` reflects actual data update timestamp (not generation time)
- Exclude noindexed programmatic pages from sitemap
- Register sitemap in robots.txt
- Update sitemap dynamically as new records are added to data source

## Index Bloat Prevention

- **Noindex low-value pages**: Pages that don't meet quality gates
- **Pagination**: Noindex paginated results beyond page 1 (or use rel=next/prev)
- **Faceted navigation**: Noindex filtered views, canonical to base category
- **Crawl budget**: For sites with >10k programmatic pages, monitor crawl stats in Search Console
- **Thin page consolidation**: Merge records with insufficient data into aggregated pages
- **Regular audits**: Monthly review of indexed page count vs intended count

## Output

### Programmatic SEO Score: XX/100

### Assessment Summary
| Category | Status | Score |
|----------|--------|-------|
| Data Quality | ✅/⚠️/❌ | XX/100 |
| Template Uniqueness | ✅/⚠️/❌ | XX/100 |
| URL Structure | ✅/⚠️/❌ | XX/100 |
| Internal Linking | ✅/⚠️/❌ | XX/100 |
| Thin Content Risk | ✅/⚠️/❌ | XX/100 |
| Index Management | ✅/⚠️/❌ | XX/100 |

### Critical Issues (fix immediately)
### High Priority (fix within 1 week)
### Medium Priority (fix within 1 month)
### Low Priority (backlog)

### Recommendations
- Data source improvements
- Template modifications
- URL pattern adjustments
- Quality gate compliance actions

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL accessibility and checking for authentication requirements. |
| No programmatic pages detected | Inform user that no template-generated or data-driven page patterns were found. Suggest checking if pages use client-side rendering or if the URL points to the correct section. |
| Thin content threshold exceeded | Trigger quality gate warning. Report the unique content percentage and flag pages below 40% uniqueness. Require user acknowledgment before proceeding. |
| Quality gate violation | Halt analysis at the HARD STOP threshold (500+ pages without justification or <30% unique content). Present findings and require explicit user approval to continue. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Data source assessment é concreto e quantificado
- [ ] Row/record count indicado com número real (não "muitos registos")
- [ ] Campos únicos por registo identificados e percentagem de completude calculada
- [ ] Registos duplicados ou near-duplicate (>80% field overlap) flagged com contagem
- [ ] Freshness do data source especificada (data última actualização ou frequência de sync)
- ❌ NOT delivery-ready: "O CSV tem bastantes linhas e os dados parecem razoavelmente completos."
- ✅ Delivery-ready: "CSV de 1.247 concelhos PT; 94% dos registos têm os 8 campos obrigatórios; 23 registos near-duplicate flagged; última actualização INE: Março 2025."

---

### Gate 2 — Template engine plan distingue static vs dynamic com ratio explícito
- [ ] Variáveis de injeção listadas por secção (title, H1, meta, body, schema)
- [ ] Ratio static/dynamic estimado por template (target: ≤60% static)
- [ ] Conditional logic documentada para campos ausentes (fallback definido)
- [ ] "Mad-libs test" aplicado: cada página passa o standalone value test?
- ❌ NOT delivery-ready: "O template vai injetar o nome da cidade e do serviço nos sítios certos."
- ✅ Delivery-ready: "Template: 38% static (header, CTA, footer), 62% dynamic. H1 = `[serviço] em [concelho]`; body bloco 2 = dados INE de desemprego local; bloco 3 = 3 casos de uso específicos da região. Fallback: se população <5.000, ocultar bloco de estatísticas e substituir por testimonial regional."

---

### Gate 3 — URL pattern strategy é completa e sem ambiguidade
- [ ] Padrão URL definido com exemplo real preenchido (não `[placeholder]`)
- [ ] Unicidade de slugs garantida (mecanismo descrito: hash, slug-collision check, etc.)
- [ ] Comprimento máximo verificado (<100 chars) com exemplo do slug mais longo
- [ ] Trailing slash consistente com padrão existente do site documentado
- ❌ NOT delivery-ready: "URLs seguirão o padrão `/[cidade]/[serviço]` com slugs limpos."
- ✅ Delivery-ready: "Padrão: `/contabilidade/[distrito]/[concelho]/` — ex: `/contabilidade/lisboa/cascais/`. Slug mais longo testado: `/contabilidade/viana-do-castelo/ponte-de-lima/` = 47 chars ✅. Trailing slash: ON (match com site LUSOconta existente). Collision check via script Python pré-geração."

---

### Gate 4 — Internal linking automation especifica regras de relacionamento
- [ ] Hub pages identificadas (quantas, qual URL, quantas spoke pages cada)
- [ ] Critério de "related items" explícito (ex: mesmo distrito, mesmo sector, mesma feature)
- [ ] Anchor text rules definidas com 3+ exemplos variados (sem exact-match repetido)
- [ ] BreadcrumbList schema gerado automaticamente confirmado com exemplo JSON-LD
- ❌ NOT delivery-ready: "Cada página terá links internos para páginas relacionadas e um breadcrumb."
- ✅ Delivery-ready: "18 hub pages (1 por distrito); cada hub linka para média de 18 concelhos. Related: mesmo distrito + mesmo serviço (max 5 links). Anchors variados: 'contabilistas em Cascais' / 'serviços fiscais em Cascais' / 'apoio contabilístico no concelho de Cascais'. Schema BreadcrumbList: `Home > Contabilidade > Lisboa > Cascais`."

---

### Gate 5 — Thin content safeguards aplicados com números reais e plano de rollout
- [ ] Uniqueness % calculado para amostra de 3+ páginas (não estimado)
- [ ] Volume total de páginas classificado contra os thresholds (WARNING/HARD STOP)
- [ ] Plano de rollout em batches definido: tamanho batch, janela de monitorização
- [ ] % de páginas para human review especificada (mínimo 5-10% da amostra)
- [ ] Site reputation abuse risk avaliado (domínio próprio vs high-authority host?)
- ❌ NOT delivery-ready: "O conteúdo vai ser suficientemente único e publicaremos em fases."
- ✅ Delivery-ready: "324 páginas totais → abaixo do WARNING (500+). Uniqueness medida em 10 amostras: média 61%, mínimo 44% ✅ (acima do hard stop de 30%). Rollout: batch 1 = 50 páginas semana 1, monitorização 3 semanas, depois batches de 100. Human review: 33 páginas (10%). Domínio próprio lusocontabilidade.pt — sem risco site reputation abuse."

---

### Gate 6 — Output usa CLIENT NAME + dados reais, sem angle-brackets por preencher
- [ ] Nome do cliente ou projecto aparece no output (não "Cliente X" nem `[client]`)
- [ ] URLs de exemplo usam domínio real ou domínio plausível confirmado
- [ ] Números no plano (páginas, batches, campos, percentagens) são específicos e verificáveis
- [ ] Nenhum `[placeholder]`, `<inserir>`, `[TBD]` ou equivalente no output final
- ❌ NOT delivery-ready: "Para o projecto `[CLIENT]`, planear `[N]` páginas com URL `/[categoria]/[item]`."
- ✅ Delivery-ready: "Para a LUSOconta, planear 324 páginas com URL `/contabilidade/[distrito]/[concelho]/`, publicação em 7 batches de ~46 páginas, janeiro–março 2026."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Programmatic SEO Plan — LUSOconta (lusocontabilidade.pt)

## Data Source Assessment

**Fonte:** CSV INE — Concelhos de Portugal com dados económicos
- **Total registos:** 308 concelhos (Portugal continental + ilhas)
- **Campos disponíveis:** 11 (nome, distrito, população, nº empresas, sector dominante,
  taxa desemprego, PIB/capita, código postal, lat/long, município, NUTS II)
- **Completude:** 97% (9 concelhos sem dado PIB/capita — usar média distrital como fallback)
- **Near-duplicates flagged:** 4 pares (ex: Lisboa/Grande Lisboa NUTS — removidos da geração)
- **Freshness:** INE actualização anual; última: Outubro 2024. Próxima: Outubro 2025.
  Risco: dados 2024 usados em páginas de 2026 — adicionar disclaimer "dados referentes a 2024"

**Resultado:** ✅ Data source apta para geração. 304 páginas viáveis após limpeza.

---

## Template Engine Plan

**URL pattern:** `/contabilidade/[distrito-slug]/[concelho-slug]/`
**Exemplo real:** `/contabilidade/lisboa/mafra/`
**Slug mais longo:** `/contabilidade/viana-do-castelo/ponte-de-lima/` = 47 chars ✅

**Ratio static/dynamic por template:**
| Secção | Tipo | Notas |
|--------|------|-------|
| Header/nav/footer | Static | 18% do total |
| H1 + meta title | Dynamic | `Contabilistas em [Concelho] — LUSOconta` |
| Intro paragraph | Semi-dynamic | 40% dynamic: população, nº empresas, sector dominante |
| Bloco estatísticas | Dynamic | Taxa desemprego, PIB/capita — dados INE directos |
| Bloco serviços | Static | Lista serviços LUSOconta — igual em todas as páginas |
| Bloco casos de uso | Dynamic | 2-3 exemplos específicos do sector dominante do concelho |
| FAQ (3 perguntas) | Semi-dynamic | P1+P2 dinâmicas; P3 static |
| CTA + formulário | Static | 12% do total |

**Uniqueness estimada:** 58% dynamic/semi-dynamic ✅ (acima do threshold 40%)

**Mad-libs test (amostra Mafra):**
"Em Mafra, concelho com 83.000 habitantes e 4.200 empresas registadas, o sector
dominante é a construção civil (23% do tecido empresarial). A taxa de desemprego
de 6,2% está 1.1pp abaixo da média nacional..."
→ PASSA: informação específica e verificável, não apenas nome da cidade substituído.

**Conditional logic:**
- Se `população < 5.000`: ocultar bloco estatísticas completo → mostrar bloco regional
- Se `sector_dominante == NULL`: usar "diversificado" e bloco genérico de serviços
- Se `pib_capita == NULL`: substituir por média distrital + nota "estimativa distrital"

---

## Internal Linking Architecture

**Hub pages (18 total — 1 por distrito):**
- `/contabilidade/lisboa/` → linka 52 concelhos
- `/contabilidade/porto/` → linka 18 concelhos
- [... 16 distritos restantes]

**Related items logic (max 5 por página):**
1. Outros concelhos do mesmo distrito
2. Concelhos com mesmo sector dominante (cross-district)
3. Páginas de serviços LUSOconta relacionadas com sector dominante

**Anchor text pool (exemplo para Mafra):**
- "contabilistas em Mafra"
- "serviços de contabilidade no concelho de Mafra"
- "apoio fiscal para empresas em Mafra"
- "gestão contabilística em Mafra, Lisboa"

**BreadcrumbList schema (Mafra):**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://lusocontabilidade.pt/"},
    {"@type": "ListItem", "position": 2, "name": "Contabilidade por Região", "item": "https://lusocontabilidade.pt/contabilidade/"},
    {"@type": "ListItem", "position": 3, "name": "Lisboa", "item": "https://lusocontabilidade.pt/contabilidade/lisboa/"},
    {"@type": "ListItem", "position": 4, "name": "Mafra", "item": "https://lusocontabilidade.pt/contabilidade/lisboa/mafra/"}
  ]
}
```

---

## Thin Content & Rollout Plan

**Volume total:** 304 páginas → abaixo do HARD STOP (500+) ✅

**Uniqueness medida (10 páginas amostra):**
| Página | Unique % |
|--------|----------|
| /contabilidade/lisboa/cascais/ | 63% |
| /contabilidade/porto/matosinhos/ | 59% |
| /contabilidade/braga/guimaraes/ | 61% |
| /contabilidade/algarve/faro/ | 57% |
| /contabilidade/beja/serpa/ | 44% ⚠️ |
| Média | 58% ✅ |

→ Serpa (população 15.000, dados limitados): adicionar bloco "empresas agrícolas no Alentejo"
para elevar unique % acima de 50% antes de publicar.

**Rollout plan:**
- **Semana 1:** Batch 1 — 50 páginas (distritos Lisboa e Porto, alta procura)
- **Semanas 2-4:** Monitorização GSC — impressões, CTR, indexação
- **Semana 5:** Batch 2 — 75 páginas (Braga, Aveiro, Setúbal)
- **Semanas 6-8:** Monitorização + ajuste de template se necessário
- **Semanas 9-16:** Batches 3-6 de ~45 páginas cada (restantes distritos)

**Human review:** 31 páginas (10%) — reviewer interno LUSOconta, checklist de 5 pontos.

**Site reputation risk:** Domínio próprio lusocontabilidade.pt, DR 34 — sem risco de
site reputation abuse. Conteúdo principal do site, não secção parasita.
```

---

## Output anti-patterns

- Usar `[cidade]`, `[serviço]`, `[cliente]` no output final sem substituir por dados reais
- Declarar uniqueness % "estimada" sem medir pelo menos 3-5 páginas de amostra reais
- Omitir o rollout plan quando volume total ultrapassa 100 páginas
- Descrever o template como "vai injectar variáveis" sem especificar quais campos e em que secções
- Não calcular o ratio static/dynamic e assumir que o template passa no thin content test
- Ignorar o fallback logic para campos com dados em falta no data source
- Recomendar publicação simultânea de >100 páginas sem referência aos thresholds de WARNING/HARD STOP
- Não distinguir entre conteúdo "semi-dynamic" (template com dados) e genuinamente único — ambos contam diferente no uniqueness %
- Omitir avaliação de site reputation abuse risk quando cliente menciona publicar em domínio de terceiro
