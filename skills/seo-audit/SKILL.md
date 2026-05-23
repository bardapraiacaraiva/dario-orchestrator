---
name: seo-audit
description: >
  Full website SEO audit with parallel subagent delegation. Crawls up to 500
  pages, detects business type, delegates to 7 specialists, generates health
  score. Use when user says "audit", "full SEO check", "analyze my site",
  or "website health check".
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Full Website SEO Audit

## Process

1. **Fetch homepage**: use `scripts/fetch_page.py` to retrieve HTML
2. **Detect business type**: analyze homepage signals per seo orchestrator
3. **Crawl site**: follow internal links up to 500 pages, respect robots.txt
4. **Delegate to subagents** (if available, otherwise run inline sequentially):
   - `seo-technical` -- robots.txt, sitemaps, canonicals, Core Web Vitals, security headers
   - `seo-content` -- E-E-A-T, readability, thin content, AI citation readiness
   - `seo-schema` -- detection, validation, generation recommendations
   - `seo-sitemap` -- structure analysis, quality gates, missing pages
   - `seo-performance` -- LCP, INP, CLS measurements
   - `seo-visual` -- screenshots, mobile testing, above-fold analysis
   - `seo-geo` -- AI crawler access, llms.txt, citability, brand mention signals
   - `seo-local` -- GBP signals, NAP consistency, reviews, local schema, industry-specific local factors (spawn when Local Service industry detected: brick-and-mortar, SAB, or hybrid business type)
5. **Score** -- aggregate into SEO Health Score (0-100)
6. **Report** -- generate prioritized action plan

## Crawl Configuration

```
Max pages: 500
Respect robots.txt: Yes
Follow redirects: Yes (max 3 hops)
Timeout per page: 30 seconds
Concurrent requests: 5
Delay between requests: 1 second
```

## Output Files

- `FULL-AUDIT-REPORT.md`: Comprehensive findings
- `ACTION-PLAN.md`: Prioritized recommendations (Critical > High > Medium > Low)
- `screenshots/`: Desktop + mobile captures (if Playwright available)

## Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

## Report Structure

### Executive Summary
- Overall SEO Health Score (0-100)
- Business type detected
- Top 5 critical issues
- Top 5 quick wins

### Technical SEO
- Crawlability issues
- Indexability problems
- Security concerns
- Core Web Vitals status

### Content Quality
- E-E-A-T assessment
- Thin content pages
- Duplicate content issues
- Readability scores

### On-Page SEO
- Title tag issues
- Meta description problems
- Heading structure
- Internal linking gaps

### Schema & Structured Data
- Current implementation
- Validation errors
- Missing opportunities

### Performance
- LCP, INP, CLS scores
- Resource optimization needs
- Third-party script impact

### Images
- Missing alt text
- Oversized images
- Format recommendations

### AI Search Readiness
- Citability score
- Structural improvements
- Authority signals

## Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, spawn the `seo-dataforseo` agent alongside existing subagents to enrich the audit with live data: real SERP positions, backlink profiles with spam scores, on-page analysis (Lighthouse), business listings, and AI visibility checks (ChatGPT scraper, LLM mentions).

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| robots.txt blocks crawling | Report which paths are blocked. Analyze only accessible pages and note the limitation in the report. |
| Rate limiting (429 responses) | Back off and reduce concurrent requests. Report partial results with a note on which sections could not be completed. |
| Timeout on large sites (500+ pages) | Cap the crawl at the timeout limit. Report findings for pages crawled and estimate total site scope. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

### 1. GATE — Findings têm source data rastreável e números reais
- [ ] Cada issue cita a URL ou página específica onde foi encontrada (não "várias páginas")
- [ ] Contagens são exactas: "47 páginas sem meta description" não "muitas páginas"
- [ ] Core Web Vitals têm valores medidos: LCP 4.2s, CLS 0.31, INP 380ms (não "slow")
- [ ] Score final (0-100) tem breakdown por categoria com pesos aplicados visivelmente

❌ NOT delivery-ready: "O site tem problemas de performance e falta de meta descriptions em várias páginas."
✅ Delivery-ready: "LCP: 4.2s (threshold: 2.5s) — falha em 34/47 páginas crawled. 23 páginas sem meta description (home, /servicos, /contacto incluídas). SEO Health Score: 61/100."

---

### 2. GATE — Priorização é accionável com impacto estimado
- [ ] Cada issue tem severity label explícito: Critical / High / Medium / Low
- [ ] Issues Critical têm prazo "fix immediately" com justificação (ex: bloqueia indexação)
- [ ] Cada recomendação tem effort estimate (ex: "2h dev", "30min no CMS") 
- [ ] Top 5 quick wins identificadas separadamente com ROI esperado

❌ NOT delivery-ready: "Recomendamos melhorar os títulos e corrigir os erros técnicos o mais rápido possível."
✅ Delivery-ready: "[CRITICAL] robots.txt bloqueia /produtos/ — Google não indexa 80% do catálogo. Fix: 5 min no servidor. Impacto: desbloqueio imediato de indexação. [HIGH] 14 páginas com título duplicado 'Homepage | Marca' — fix dentro de 1 semana, esforço 1h CMS."

---

### 3. GATE — Todos os 7 subagents (ou inline equivalents) têm output reportado
- [ ] `seo-technical`: robots.txt, sitemap, canonicals, security headers — todos cobertos
- [ ] `seo-content`: E-E-A-T assessment, thin content count, readability score presente
- [ ] `seo-schema`: schemas detectados listados + erros de validação concretos
- [ ] `seo-performance`: LCP, INP, CLS com valores numéricos e pass/fail
- [ ] `seo-geo` / `seo-visual` / `seo-sitemap`: cada um com pelo menos 1 finding ou "pass"
- [ ] Se negócio local detectado: `seo-local` incluído com GBP signals + NAP check

❌ NOT delivery-ready: Report só cobre Technical e Content, Performance secção vazia ou "N/A".
✅ Delivery-ready: Todas as 7 secções têm dados — mesmo que seja "Schema: nenhum schema detectado (oportunidade crítica para FAQ e LocalBusiness)."

---

### 4. GATE — SEO Health Score é calculado com pesos visíveis
- [ ] Score breakdown mostra cada categoria com peso e pontuação parcial
- [ ] Score total é soma verificável (não número mágico)
- [ ] Comparação de contexto incluída (ex: "61/100 — abaixo da média do sector ~72")
- [ ] Executive Summary mostra score + top 5 issues + top 5 quick wins em ≤ 1 página

❌ NOT delivery-ready: "SEO Health Score: 58/100" sem breakdown nem como foi calculado.
✅ Delivery-ready: "Technical 22% → 14/22 | Content 23% → 16/23 | On-Page 20% → 12/20 | Schema 10% → 2/10 | Performance 10% → 6/10 | AI Readiness 10% → 7/10 | Images 5% → 3/5 = **60/100**"

---

### 5. GATE — Roadmap tem fases temporais concretas
- [ ] ACTION-PLAN.md separado existe (ou secção equivalente claramente demarcada)
- [ ] Issues agrupados em: Semana 1 (Critical) / Mês 1 (High) / Trimestre (Medium) / Backlog (Low)
- [ ] Cada acção tem owner sugerido: developer, content editor, SEO manager, client
- [ ] Pelo menos 1 "quick win" executável pelo cliente sem developer (ex: meta description no CMS)

❌ NOT delivery-ready: Lista de 30 recomendações sem ordem nem responsável nem prazo.
✅ Delivery-ready: "SEMANA 1 — Dev: corrigir robots.txt (5min) + redirecionar 301 para 12 URLs quebradas (2h). Cliente: atualizar meta description da homepage no WordPress (15min)."

---

### 6. GATE — Output usa NOME DO CLIENTE + dados reais em todo o documento — zero placeholders com angle-brackets
- [ ] Nome do site/marca aparece no título do report e em pelo menos 3x no corpo
- [ ] URLs citadas são reais do domínio auditado (não exemplo.com ou `<url>`)
- [ ] Nenhum campo contém `[INSERT]`, `<client>`, `[URL]`, `[METRIC]` ou equivalente
- [ ] Screenshots ou referências visuais mencionam páginas reais do site

❌ NOT delivery-ready: "O site `<client_domain>` tem `<number>` páginas com problemas de `<issue_type>`."
✅ Delivery-ready: "O site cuidai.pt tem 34 páginas com LCP acima de 2.5s, sendo /cuidadores e /como-funciona as páginas com pior desempenho (LCP 5.1s e 4.8s respectivamente)."

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SEO Audit Report — Cuidai.pt
**Data do audit:** 2025-01-15 | **Páginas crawled:** 127/500 | **Tempo de análise:** 4m 32s

---

## Executive Summary

**SEO Health Score: 63/100**

| Categoria | Peso | Score | Parcial |
|-----------|------|-------|---------|
| Technical SEO | 22% | 12/22 | Sitemap ausente, canonicals com erros |
| Content Quality | 23% | 17/23 | Bom E-E-A-T, 8 páginas thin content |
| On-Page SEO | 20% | 14/20 | 23 meta descriptions em falta |
| Schema / Structured Data | 10% | 2/10 | Nenhum schema implementado |
| Performance (CWV) | 10% | 5/10 | LCP falha em 78% das páginas |
| AI Search Readiness | 10% | 8/10 | llms.txt presente, boa citabilidade |
| Images | 5% | 5/5 | Alt text 100%, formatos WebP |
| **TOTAL** | **100%** | **63/100** | Abaixo da média plataformas de cuidados (~71) |

### Top 5 Issues Críticos
1. **[CRITICAL]** Sitemap XML ausente — Google não descobre 40+ páginas de cuidadores
2. **[CRITICAL]** robots.txt bloqueia /cuidadores/* — perfis de cuidadores não indexáveis
3. **[HIGH]** LCP médio 4.1s (threshold 2.5s) — falha em 99/127 páginas
4. **[HIGH]** 0 schemas implementados — sem rich results para serviços de cuidados
5. **[HIGH]** 23 páginas sem meta description incluindo homepage e /como-funciona

### Top 5 Quick Wins (esta semana)
1. Corrigir robots.txt: remover `Disallow: /cuidadores/` — 5 min, impacto imediato
2. Gerar e submeter sitemap.xml via Yoast/plugin — 30 min
3. Adicionar meta description à homepage no CMS — 15 min
4. Implementar LocalBusiness schema na homepage — 2h dev
5. Comprimir imagens hero (/static/hero-cuidadora.jpg, 2.3MB → target <200KB) — 1h dev

---

## Technical SEO

### Crawlability
- **robots.txt** (`cuidai.pt/robots.txt`): linha `Disallow: /cuidadores/` bloqueia 67 perfis de cuidadores
  → **[CRITICAL]** Fix: remover linha. Impacto: 67 páginas passam a ser indexáveis
- **Sitemap**: AUSENTE em cuidai.pt/sitemap.xml e cuidai.pt/sitemap_index.xml
  → **[CRITICAL]** Google Search Console mostra 0 sitemaps submetidos
- **Canonicals**: 12 páginas com self-referencing canonical correcto. 
  Problema: /cuidadores?page=2 e /cuidadores?page=3 sem canonical → duplicate content risk

### Indexability
- **Páginas indexáveis**: 89/127 crawled (70%)
- **Noindex tags**: 4 páginas com noindex desnecessário (/termos, /privacidade, /cookies, /sitemap-html)
  → Remover noindex de /termos — é útil para long-tail queries de confiança
- **Redirect chains**: 3 chains detectadas
  - /home → / → (correcto, 1 hop OK)
  - /cuidadores-lisboa → /cuidadores/lisboa → /cuidadores/lisboa/ (3 hops — crítico)

### Security Headers
- ✅ HTTPS activo com certificado válido (expira 2025-08-12)
- ✅ HSTS header presente
- ❌ Content-Security-Policy ausente
- ❌ X-Frame-Options ausente

---

## Content Quality

### E-E-A-T Assessment: 7/10
- **Experience**: Testemunhos de famílias presentes em 4 páginas — positivo
- **Expertise**: Bio de cuidadores com certificações — positivo. Falta: quem fundou a Cuidai.pt e credenciais
- **Authoritativeness**: 0 backlinks de domínios .pt de saúde ou cuidados detectados
- **Trust**: Política de privacidade, termos de serviço presentes. Falta: selos de certificação visíveis

### Thin Content (< 300 palavras)
8 páginas identificadas:
- /cuidadores/porto — 87 palavras (apenas listagem, sem contexto local)
- /cuidadores/braga — 124 palavras
- /blog/cuidados-idosos — 210 palavras, sem imagens, sem links internos
- + 5 páginas de cuidadores individuais com bio < 100 palavras

**Recomendação**: Expandir páginas de cidades com conteúdo local (media de serviços, preços na zona, guia de recursos locais). Esforço: 3-4h por página.

---

## Schema & Structured Data

**Status: NENHUM schema detectado** em 127 páginas crawled.

### Oportunidades Imediatas (impacto alto):
| Schema | Página | Benefício |
|--------|--------|-----------|
| `LocalBusiness` + `HomeAndConstructionBusiness` | Homepage | Rich result com horário, morada, rating |
| `Service` | /como-funciona | Destaque em SERP para queries "cuidadores em casa" |
| `Person` | /cuidadores/[id] | Rich result com foto e especialização do cuidador |
| `FAQPage` | /perguntas-frequentes | FAQ expandido na SERP (CTR +20-30% estimado) |
| `Review` / `AggregateRating` | Homepage | Star rating visível na SERP |

**Prioridade**: LocalBusiness + FAQPage esta semana. Esforço dev: 4h total.

---

## Performance (Core Web Vitals)

| Métrica | Score Cuidai.pt | Threshold | Status |
|---------|----------------|-----------|--------|
| LCP (Largest Contentful Paint) | 4.1s | < 2.5s | ❌ FAIL |
| INP (Interaction to Next Paint) | 210ms | < 200ms | ⚠️ NEEDS IMPROVEMENT |
| CLS (Cumulative Layout Shift) | 0.04 | < 0.1 | ✅ PASS |

**LCP offenders** (top 3):
- /cuidadores — hero image `/static/cuidadora-hero.jpg` 2.3MB não comprimida
- /como-funciona — render-blocking script `analytics-v2.js` atrasa LCP em ~1.2s
- Homepage — Google Fonts carregadas synchronously (300ms de bloqueio)

**Fix rápido**: Lazy load + WebP conversion para hero images → LCP estimado 2.8s (-32%)

---

## AI Search Readiness

- ✅ `llms.txt` presente em cuidai.pt/llms.txt (detectado)
- ✅ Conteúdo estruturado com headers H2/H3 claros em 89% das páginas
- ✅ Respostas directas a perguntas comuns em /perguntas-frequentes
- ❌ Nenhuma menção de marca detectada em fontes públicas (Reddit, forums PT)
- ❌ Citability score: 6/10 — falta conteúdo estatístico original e estudos próprios

**Recomendação AI**: Publicar 1 relatório/dados originais sobre "custo médio de cuidadores em Portugal 2025" — asset altamente citável por LLMs e jornalistas.

---

## ACTION-PLAN.md — Cuidai.pt

### SEMANA 1 — Issues Críticos
| Acção | Owner | Esforço | Impacto |
|-------|-------|---------|---------|
| Remover `Disallow: /cuidadores/` do robots.txt | Dev | 5 min | 67 páginas indexáveis |
| Gerar e submeter sitemap.xml | Dev/SEO | 30 min | Descoberta de 40+ URLs |
| Adicionar meta description à homepage | Cliente (CMS) | 15 min | CTR +5-10% estimado |
| Implementar LocalBusiness + FAQPage schema | Dev | 4h | Rich results activados |

### MÊS 1 — Issues High
| Acção | Owner | Esforço | Impacto |
|-------|-------|---------|---------|
| Optimizar LCP: comprimir images + WebP | Dev | 1 dia | LCP 4.1s → ~2.8s |
| Corrigir redirect chain /cuidadores-lisboa | Dev | 1h | Eliminar perda de PageRank |
| Escrever meta descriptions para 23 páginas | SEO/Cliente | 3h | SERP CTR improvement |
| Expandir thin content em 3 páginas de cidades | Content | 2 dias | Rankings long-tail |

### TRIMESTRE — Issues Medium
- Programa de link building: parceiros de saúde .pt
- Publicar relatório original "Cuidados em Portugal 2025"
- Implementar schema `Person` nos 67 perfis de cuidadores
- Resolver Content-Security-Policy e X-Frame-Options

### BACKLOG — Issues Low
- HTML sitemap em /sitemap-html (remover noindex)
- Remover render-blocking Google Fonts (self-host)
- INP: optimizar analytics-v2.js (defer/async)
```

---

## Output anti-patterns

- **Score sem breakdown**: escrever "SEO Score: 67/100" sem mostrar os pesos por categoria e como chegou ao número — o cliente não consegue validar nem priorizar
- **Issues vagos sem URL**: reportar "várias páginas têm problemas de canonical" sem listar quais — inutilizável para o developer que vai fazer o fix
- **Métricas de performance sem threshold**: "LCP é lento" em vez de "LCP 4.1s vs threshold 2.5s — FAIL" — o cliente não sabe se é grave ou ligeiro
- **Subagents silenciados**: omitir secções inteiras (ex: Schema, AI Readiness) porque não havia dados, em vez de reportar "nenhum schema detectado — oportunidade crítica"
- **Recomendações sem owner nem esforço**: listar 30 acções sem dizer quem faz, quanto tempo leva e em que ordem — gera paralisia, não acção
- **Placeholders no report final**: entregar documento com `[CLIENT_URL]`, `<número de páginas>`, ou `[inserir metric aqui]` — quebra confiança imediatamente
- **Quick wins misturadas com projetos longos**: colocar "implementar estratégia de conteúdo" ao lado de "corrigir robots.txt em 5 minutos" sem distinguir esforço — o cliente não sabe por onde começar
- **Thin content sem contagem exacta**: "algumas páginas têm pouco conteúdo" em vez de "8 páginas com menos de 300 palavras, listadas abaixo" — impede priorização
- **robots.txt não verificado**: reportar crawlability sem confirmar explicitamente o que o robots.txt bloqueia — erro de omissão que pode esconder o issue mais crítico do audit
- **ACTION-PLAN ausente ou fundido no report**: entregar apenas o FULL-AUDIT-REPORT.md sem um ACTION-PLAN.md separado e orientado a tarefas — o cliente recebe análise mas não sabe o que fazer amanhã de manhã
