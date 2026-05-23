---
name: seo-technical
description: >
  Technical SEO audit across 9 categories: crawlability, indexability, security,
  URL structure, mobile, Core Web Vitals, structured data, JavaScript rendering,
  and IndexNow protocol. Use when user says "technical SEO", "crawl issues",
  "robots.txt", "Core Web Vitals", "site speed", or "security headers".
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Technical SEO Audit

## Categories

### 1. Crawlability
- robots.txt: exists, valid, not blocking important resources
- XML sitemap: exists, referenced in robots.txt, valid format
- Noindex tags: intentional vs accidental
- Crawl depth: important pages within 3 clicks of homepage
- JavaScript rendering: check if critical content requires JS execution
- Crawl budget: for large sites (>10k pages), efficiency matters

#### AI Crawler Management

As of 2025-2026, AI companies actively crawl the web to train models and power AI search. Managing these crawlers via robots.txt is a critical technical SEO consideration.

**Known AI crawlers:**

| Crawler | Company | robots.txt token | Purpose |
|---------|---------|-----------------|---------|
| GPTBot | OpenAI | `GPTBot` | Model training |
| ChatGPT-User | OpenAI | `ChatGPT-User` | Real-time browsing |
| ClaudeBot | Anthropic | `ClaudeBot` | Model training |
| PerplexityBot | Perplexity | `PerplexityBot` | Search index + training |
| Bytespider | ByteDance | `Bytespider` | Model training |
| Google-Extended | Google | `Google-Extended` | Gemini training (NOT search) |
| CCBot | Common Crawl | `CCBot` | Open dataset |

**Key distinctions:**
- Blocking `Google-Extended` prevents Gemini training use but does NOT affect Google Search indexing or AI Overviews (those use `Googlebot`)
- Blocking `GPTBot` prevents OpenAI training but does NOT prevent ChatGPT from citing your content via browsing (`ChatGPT-User`)
- ~3-5% of websites now use AI-specific robots.txt rules

**Example, selective AI crawler blocking:**
```
# Allow search indexing, block AI training crawlers
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

# Allow all other crawlers (including Googlebot for search)
User-agent: *
Allow: /
```

**Recommendation:** Consider your AI visibility strategy before blocking. Being cited by AI systems drives brand awareness and referral traffic. Cross-reference the `seo-geo` skill for full AI visibility optimization.

### 2. Indexability
- Canonical tags: self-referencing, no conflicts with noindex
- Duplicate content: near-duplicates, parameter URLs, www vs non-www
- Thin content: pages below minimum word counts per type
- Pagination: rel=next/prev or load-more pattern
- Hreflang: correct for multi-language/multi-region sites
- Index bloat: unnecessary pages consuming crawl budget

### 3. Security
- HTTPS: enforced, valid SSL certificate, no mixed content
- Security headers:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
- HSTS preload: check preload list inclusion for high-security sites

### 4. URL Structure
- Clean URLs: descriptive, hyphenated, no query parameters for content
- Hierarchy: logical folder structure reflecting site architecture
- Redirects: no chains (max 1 hop), 301 for permanent moves
- URL length: flag >100 characters
- Trailing slashes: consistent usage

### 5. Mobile Optimization
- Responsive design: viewport meta tag, responsive CSS
- Touch targets: minimum 48x48px with 8px spacing
- Font size: minimum 16px base
- No horizontal scroll
- Mobile-first indexing: Google indexes mobile version. **Mobile-first indexing is 100% complete as of July 5, 2024.** Google now crawls and indexes ALL websites exclusively with the mobile Googlebot user-agent.

### 6. Core Web Vitals
- **LCP** (Largest Contentful Paint): target <2.5s
- **INP** (Interaction to Next Paint): target <200ms
  - INP replaced FID on March 12, 2024. FID was fully removed from all Chrome tools (CrUX API, PageSpeed Insights, Lighthouse) on September 9, 2024. Do NOT reference FID anywhere.
- **CLS** (Cumulative Layout Shift): target <0.1
- Evaluation uses 75th percentile of real user data
- Use PageSpeed Insights API or CrUX data if MCP available

### 7. Structured Data
- Detection: JSON-LD (preferred), Microdata, RDFa
- Validation against Google's supported types
- See seo-schema skill for full analysis

### 8. JavaScript Rendering
- Check if content visible in initial HTML vs requires JS
- Identify client-side rendered (CSR) vs server-side rendered (SSR)
- Flag SPA frameworks (React, Vue, Angular) that may cause indexing issues
- Verify dynamic rendering setup if applicable

#### JavaScript SEO: Canonical & Indexing Guidance (December 2025)

Google updated its JavaScript SEO documentation in December 2025 with critical clarifications:

1. **Canonical conflicts:** If a canonical tag in raw HTML differs from one injected by JavaScript, Google may use EITHER one. Ensure canonical tags are identical between server-rendered HTML and JS-rendered output.
2. **noindex with JavaScript:** If raw HTML contains `<meta name="robots" content="noindex">` but JavaScript removes it, Google MAY still honor the noindex from raw HTML. Serve correct robots directives in the initial HTML response.
3. **Non-200 status codes:** Google does NOT render JavaScript on pages returning non-200 HTTP status codes. Any content or meta tags injected via JS on error pages will be invisible to Googlebot.
4. **Structured data in JavaScript:** Product, Article, and other structured data injected via JS may face delayed processing. For time-sensitive structured data (especially e-commerce Product markup), include it in the initial server-rendered HTML.

**Best practice:** Serve critical SEO elements (canonical, meta robots, structured data, title, meta description) in the initial server-rendered HTML rather than relying on JavaScript injection.

### 9. IndexNow Protocol
- Check if site supports IndexNow for Bing, Yandex, Naver
- Supported by search engines other than Google
- Recommend implementation for faster indexing on non-Google engines

## Output

### Technical Score: XX/100

### Category Breakdown
| Category | Status | Score |
|----------|--------|-------|
| Crawlability | pass/warn/fail | XX/100 |
| Indexability | pass/warn/fail | XX/100 |
| Security | pass/warn/fail | XX/100 |
| URL Structure | pass/warn/fail | XX/100 |
| Mobile | pass/warn/fail | XX/100 |
| Core Web Vitals | pass/warn/fail | XX/100 |
| Structured Data | pass/warn/fail | XX/100 |
| JS Rendering | pass/warn/fail | XX/100 |
| IndexNow | pass/warn/fail | XX/100 |

### Critical Issues (fix immediately)
### High Priority (fix within 1 week)
### Medium Priority (fix within 1 month)
### Low Priority (backlog)

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `on_page_instant_pages` for real page analysis (status codes, page timing, broken links, on-page checks), `on_page_lighthouse` for Lighthouse audits (performance, accessibility, SEO scores), and `domain_analytics_technologies_domain_technologies` for technology stack detection.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL, checking DNS resolution, and confirming the site is publicly accessible. |
| robots.txt not found | Note that no robots.txt was detected at the root domain. Recommend creating one with appropriate directives. Continue audit on remaining categories. |
| HTTPS not configured | Flag as a critical issue. Report whether HTTP is served without redirect, mixed content exists, or SSL certificate is missing/expired. |
| Core Web Vitals data unavailable | Note that CrUX data is not available (common for low-traffic sites). Suggest using Lighthouse lab data as a proxy and recommend increasing traffic before re-testing. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Crawlability & robots.txt auditado com dados reais
- [ ] robots.txt fetched e analisado (não assumido)
- [ ] XML sitemap localizado e referenciado no robots.txt verificado
- [ ] AI crawler policy documentada (GPTBot, ClaudeBot, Google-Extended, Bytespider)
- [ ] Noindex tags intencionais vs acidentais distinguidos com URLs concretos
- ❌ NOT delivery-ready: "O robots.txt parece estar a bloquear alguns recursos importantes."
- ✅ Delivery-ready: "robots.txt em cuidai.pt/robots.txt bloqueia `/wp-admin/` (correto) e `/assets/` (PROBLEMA — bloqueia CSS/JS críticos). `GPTBot` sem regra explícita → rasteado para treino sem consentimento."

### Gate 2 — Indexability com evidências de duplicate/thin content
- [ ] Canonical tags verificados: self-referencing, sem conflito com noindex
- [ ] Duplicados identificados (www vs non-www, parâmetros URL, variantes)
- [ ] Thin content flagged com contagem de palavras real por tipo de página
- [ ] Hreflang auditado se site multi-língua/multi-região
- ❌ NOT delivery-ready: "Existem algumas páginas duplicadas que podem afetar o SEO."
- ✅ Delivery-ready: "luso conta.pt resolve www e non-www para HTTPS sem redirect 301 — 2 versões indexáveis. 14 páginas de categoria com <120 palavras (mínimo recomendado: 300). Canonical em `/conta-poupanca/` aponta para `/poupanca/` — conflito detectado."

### Gate 3 — Security headers com status concreto por header
- [ ] HTTPS enforced + SSL válido confirmado (sem mixed content)
- [ ] Cada header listado com status: ✅ presente / ⚠️ misconfigured / ❌ ausente
- [ ] HSTS max-age reportado (recomendado ≥31536000)
- [ ] CSP avaliado: presente mas permissivo (unsafe-inline) conta como ⚠️, não ✅
- ❌ NOT delivery-ready: "Os security headers precisam de ser melhorados."
- ✅ Delivery-ready: "saquei.pt — CSP: ❌ ausente | HSTS: ✅ max-age=31536000 | X-Frame-Options: ✅ DENY | X-Content-Type-Options: ✅ nosniff | Referrer-Policy: ⚠️ no-referrer-when-downgrade (recomendado: strict-origin-when-cross-origin)"

### Gate 4 — Core Web Vitals com valores 75th percentile reais
- [ ] LCP, INP, CLS reportados com valores numéricos reais (não estimados)
- [ ] Fonte indicada: CrUX (dados reais) vs Lighthouse (lab data) — distinção explícita
- [ ] FID **nunca mencionado** (removido em setembro 2024)
- [ ] INP correto como métrica de interatividade desde março 2024
- [ ] Páginas com "Needs Improvement" ou "Poor" identificadas com URLs
- ❌ NOT delivery-ready: "O site tem bom desempenho mas o FID pode ser otimizado para melhor UX."
- ✅ Delivery-ready: "tributario.ai (CrUX, nov 2024, 75th pct): LCP 3.8s ❌ (>2.5s) | INP 310ms ❌ (>200ms) | CLS 0.04 ✅. Páginas críticas: `/simulador/` e `/irs-2024/` com LCP >4s. Lab data (Lighthouse mobile): LCP 4.2s."

### Gate 5 — JavaScript rendering com rendering gap documentado
- [ ] Framework detetado (React/Vue/Angular/Next.js/SSR/CSR/SSG)
- [ ] Rendering gap verificado: conteúdo crítico em HTML inicial vs requer JS
- [ ] Canonical e meta robots servidos no HTML inicial (não injetados via JS)
- [ ] Structured data time-sensitive (e.g. Product) em server-rendered HTML
- ❌ NOT delivery-ready: "O site usa React, o que pode causar problemas de indexação."
- ✅ Delivery-ready: "atrium.pt usa Next.js — SSR confirmado para páginas de produto. PORÉM: canonical tag injetada via `useEffect` (JS) — difere do HTML raw que serve canonical vazio. Google pode usar canonical vazio. Structured data `Product` ausente do HTML inicial em 8 páginas de produto."

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Cliente identificado pelo nome real (ex: Cuidai, LUSOconta, SAQUEI)
- [ ] URLs reais usados, não `https://example.com` ou `[URL]`
- [ ] Valores numéricos reais em todas as métricas (0 campos `[X ms]` ou `[inserir]`)
- [ ] Data da auditoria registada (ex: "auditoria realizada a 14 jan 2025")
- ❌ NOT delivery-ready: "O LCP de `[site do cliente]` é `[X]`s, acima do threshold de 2.5s."
- ✅ Delivery-ready: "Auditoria técnica Vivenda.pt — 14 jan 2025. LCP: 3.1s (desktop) / 4.7s (mobile). robots.txt: sitemap não referenciado. SSL válido. INP: 180ms ✅."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output de auditoria técnica SEO deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via crawl directo, ferramenta (PageSpeed, CrUX, robots.txt fetch) ou sessão anterior
- 🟡 **assumed** — plausível dado o stack/sector, mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — estimativa de impacto ou forecast por design (não verificável sem implementação)

Output checklist upfront mostra ao leitor exactamente o que é trust-as-is vs. o que precisa verify. **Honest transparency > inflated audit delivery.**

---

❌ NOT delivery-ready:
```
- LCP está em 3.8s — recomendo optimizar imagens hero
- robots.txt bloqueia GPTBot e ChatGPT-User
- Implementar SSR vai reduzir crawl delay em 40%
```
*(reader assume que tudo foi medido — mas LCP pode ser lab data, bloqueio AI pode ser inferido, e os 40% são opinião)*

✅ Delivery-ready:
```
- 🔵 verified  — robots.txt bloqueia `GPTBot` e `Google-Extended` (fetched directo via WebFetch, 2025-01-15)
- 🟡 assumed   — LCP estimado em ~3.8s baseado em Lighthouse lab data; CrUX (field data real) não disponível sem acesso Search Console
- 🟡 assumed   — Canonical tags auto-geradas pelo CMS assumidas como self-referencing; não validadas página a página
- 🟢 projection — Migração para SSR deverá reduzir crawl delay em 35-50% (benchmark sector e-commerce; resultado real depende de implementação)
- 🔵 verified  — INP < 200ms (CrUX p75 confirmado via PageSpeed Insights API; FID não referenciado — removido em Set 2024)
```

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir lab data por CrUX/field data real; validar canonicals via crawl completo
- [ ] All 🔵 citations added — URL da fonte + timestamp do fetch (robots.txt, PSI API, CrUX endpoint)
- [ ] All 🟢 projections labeled como tal ao cliente — expectativas claras antes de aprovar roadmap de implementação

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Auditoria SEO Técnica — Cuidai.pt
**Data:** 14 janeiro 2025 | **Auditado por:** DARIO | **Fonte CWV:** CrUX (75th pct, nov 2024)

---

## 1. Crawlability

**robots.txt** (cuidai.pt/robots.txt):
- ✅ Existe e é válido
- ✅ Sitemap referenciado: `Sitemap: https://cuidai.pt/sitemap.xml`
- ⚠️ Bloqueia `/uploads/` — imagens de cuidadores não rasteáveis pelo Googlebot
- ❌ Nenhuma regra para AI crawlers

**Política AI crawlers recomendada:**
```
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: *
Allow: /
```
> Nota: bloquear `Google-Extended` não afeta indexação Google Search (usa `Googlebot`).

**Sitemap:** 847 URLs indexadas. 23 URLs retornam 404 no sitemap — remover.

---

## 2. Indexability

- ❌ **www/non-www:** cuidai.pt e www.cuidai.pt ambos acessíveis sem redirect 301
- ⚠️ **Thin content:** 31 páginas de perfil de cuidador com <90 palavras
- ✅ **Canonical:** self-referencing correto nas páginas principais
- ✅ **Sem hreflang** necessário (site PT apenas)
- ❌ **Parâmetros URL:** `/cuidadores/?cidade=Lisboa&tipo=idosos` indexável sem canonical

**Ação prioritária:** implementar redirect 301 www → non-www.

---

## 3. Security Headers

| Header | Status | Detalhe |
|--------|--------|---------|
| HTTPS | ✅ | SSL válido, expira 2025-09-12 |
| HSTS | ✅ | max-age=31536000; includeSubDomains |
| CSP | ⚠️ | Presente mas inclui `unsafe-inline` |
| X-Frame-Options | ✅ | SAMEORIGIN |
| X-Content-Type-Options | ✅ | nosniff |
| Referrer-Policy | ❌ | Ausente |

**Mixed content:** 3 imagens servidas via HTTP em `/sobre-nos/` — corrigir.

---

## 4. URL Structure

- ✅ URLs descritivas: `/cuidadores/lisboa/idosos/` (lógico, hyphenated)
- ❌ 4 redirects em cadeia detetados: `/cuidador` → `/cuidadores` → `/cuidadores/` (2 hops)
- ⚠️ 7 URLs com >100 caracteres na secção de blog
- ✅ Trailing slash consistente em todo o site

---

## 5. Mobile Optimization

- ✅ Viewport meta tag presente em todas as páginas
- ✅ Design responsivo confirmado (CSS media queries)
- ⚠️ 3 botões CTA no formulário de registo com touch target 38x38px (mínimo: 48x48px)
- ✅ Font-size base: 16px
- ✅ Sem scroll horizontal detetado
- **Nota:** Mobile-first indexing 100% ativo desde 5 julho 2024 — versão mobile é a indexada

---

## 6. Core Web Vitals (CrUX, 75th percentile, novembro 2024)

| Métrica | Valor | Status |
|---------|-------|--------|
| LCP | 2.9s | ⚠️ Needs Improvement (>2.5s) |
| INP | 155ms | ✅ Good (<200ms) |
| CLS | 0.08 | ✅ Good (<0.1) |

**Páginas críticas (LCP >2.5s):** `/`, `/cuidadores/`, `/como-funciona/`
**Causa provável LCP:** imagem hero não otimizada (1.2MB, formato JPEG). Recomendar WebP + lazy load removido do LCP element.

---

## 7. Structured Data

- ✅ JSON-LD detetado em homepage (`Organization`, `WebSite`)
- ❌ Páginas de cuidador sem `Person` ou `Service` markup
- ⚠️ `FAQPage` presente em `/faq/` mas 2 entradas com `acceptedAnswer` vazio
- Ver skill `seo-schema` para análise completa e geração de markup

---

## 8. JavaScript Rendering

- **Framework:** Next.js 14 (SSR + ISR confirmado via headers `x-nextjs-cache`)
- ✅ Conteúdo crítico presente no HTML inicial (sem rendering gap)
- ✅ Canonical servido no HTML raw (não injetado via JS)
- ⚠️ Meta description em `/cuidadores/[id]/` injetada via `useEffect` — não presente no HTML inicial em 12% dos perfis testados
- ✅ Structured data no HTML inicial

---

## Resumo de Prioridades

| Prioridade | Issue | Impacto |
|-----------|-------|---------|
| 🔴 Alta | www/non-www sem redirect 301 | Duplicate content, PageRank dividido |
| 🔴 Alta | LCP 2.9s em homepage | Core Web Vitals ranking signal |
| 🔴 Alta | 23 URLs 404 no sitemap | Crawl budget desperdiçado |
| 🟡 Média | Meta description via JS (12% perfis) | Snippets incorretos no Google |
| 🟡 Média | Touch targets 38px (3 botões) | UX mobile + Mobile-first indexing |
| 🟢 Baixa | Referrer-Policy ausente | Security posture |
```

---

## Output anti-patterns

- Mencionar **FID** (First Input Delay) em qualquer contexto — foi removido em setembro 2024; a métrica correta é INP
- Reportar Core Web Vitals sem indicar fonte (CrUX real user data vs Lighthouse lab data) — são interpretações diferentes
- Listar security headers sem status individual por header (✅/⚠️/❌) — "headers em falta" sem especificar quais é inútil
- Afirmar "bloquear Google-Extended afeta o Google Search" — não afeta; afeta apenas Gemini training
- Entregar auditoria com `[URL do cliente]`, `[inserir valor]` ou outros placeholders angle-bracket não substituídos
- Assumir robots.txt sem o fetcher — descrever conteúdo sem verificar é fabricação de dados
- Marcar CSP como ✅ quando contém `unsafe-inline` ou `unsafe-eval` — é misconfiguration, não conformidade
- Ignorar AI crawler management como fora de escopo — é consideração técnica SEO crítica em 2025
- Reportar LCP/INP/CLS sem indicar percentil (deve ser sempre 75th percentile para avaliação ranking)
- Misturar recomendações de GEO/AI visibility neste output — referenciar `seo-geo` skill sem duplicar conteúdo
