---
name: seo-page
description: >
  Deep single-page SEO analysis covering on-page elements, content quality,
  technical meta tags, schema, images, and performance. Use when user says
  "analyze this page", "check page SEO", or provides a single URL for review.
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Single Page Analysis

## What to Analyze

### On-Page SEO
- Title tag: 50-60 characters, includes primary keyword, unique
- Meta description: 150-160 characters, compelling, includes keyword
- H1: exactly one, matches page intent, includes keyword
- H2-H6: logical hierarchy (no skipped levels), descriptive
- URL: short, descriptive, hyphenated, no parameters
- Internal links: sufficient, relevant anchor text, no orphan pages
- External links: to authoritative sources, reasonable count

### Content Quality
- Word count vs page type minimums (see quality-gates.md)
- Readability: Flesch Reading Ease score, grade level
- Keyword density: natural (1-3%), semantic variations present
- E-E-A-T signals: author bio, credentials, first-hand experience markers
- Content freshness: publication date, last updated date

### Technical Elements
- Canonical tag: present, self-referencing or correct
- Meta robots: index/follow unless intentionally blocked
- Open Graph: og:title, og:description, og:image, og:url
- Twitter Card: twitter:card, twitter:title, twitter:description
- Hreflang: if multi-language, correct implementation

### Schema Markup
- Detect all types (JSON-LD preferred)
- Validate required properties
- Identify missing opportunities
- NEVER recommend HowTo (deprecated) or FAQ (restricted to gov/health)

### Images
- Alt text: present, descriptive, includes keywords where natural
- File size: flag >200KB (warning), >500KB (critical)
- Format: recommend WebP/AVIF over JPEG/PNG
- Dimensions: width/height set for CLS prevention
- Lazy loading: loading="lazy" on below-fold images

### Core Web Vitals (reference only, not measurable from HTML alone)
- Flag potential LCP issues (huge hero images, render-blocking resources)
- Flag potential INP issues (heavy JS, no async/defer)
- Flag potential CLS issues (missing image dimensions, injected content)

## Output

### Page Score Card
```
Overall Score: XX/100

On-Page SEO:     XX/100  ████████░░
Content Quality: XX/100  ██████████
Technical:       XX/100  ███████░░░
Schema:          XX/100  █████░░░░░
Images:          XX/100  ████████░░
```

### Issues Found
Organized by priority: Critical -> High -> Medium -> Low

### Recommendations
Specific, actionable improvements with expected impact

### Schema Suggestions
Ready-to-use JSON-LD code for detected opportunities

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `serp_organic_live_advanced` for real SERP positions and `backlinks_summary` for backlink data and spam scores.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess page content. Suggest the user verify the URL and try again. |
| Page requires authentication (401/403) | Report that the page is behind authentication. Suggest the user provide the rendered HTML directly or a publicly accessible URL. |
| JavaScript-rendered content (empty body in HTML) | Note that key content may be rendered client-side. Analyze the available HTML and flag that results may be incomplete. Suggest using a browser-rendered snapshot if available. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Page Score Card é real e justificado
- [ ] Score Overall entre 0-100 com breakdown visível nas 5 dimensões
- [ ] Cada sub-score tem pelo menos 1 finding que o justifica (não inventado)
- [ ] Barras de progresso em bloco `code` com caracteres ██░ proporcionais ao score
- [ ] Score não é "75/100 genérico" — varia por página real analisada
- ❌ NOT delivery-ready: `Overall Score: 72/100` sem nenhum dado da página a suportar
- ✅ Delivery-ready: `On-Page SEO: 58/100` porque title tag tem 73 chars e H1 ausente na homepage `/`

### Gate 2 — Issues têm localização exata na página
- [ ] Critical/High issues citam o elemento HTML exato (`<title>`, `<h1>`, `og:image`, etc.)
- [ ] Cada issue inclui o valor atual encontrado (não "meta description em falta" — citar o que existe ou confirmar ausência)
- [ ] Issues de imagem incluem nome do ficheiro e tamanho em KB quando disponível
- [ ] Prioridades (Critical/High/Medium/Low) respeitam critérios do skill — Critical reservado para bloqueios de indexação
- ❌ NOT delivery-ready: `A meta description está em falta ou é muito curta.`
- ✅ Delivery-ready: `Meta description atual: "Cuidai — plataforma de cuidadores" (42 chars). Mínimo: 150 chars. Impacto: CTR orgânico reduzido.`

### Gate 3 — Recomendações são accionáveis com texto pronto a usar
- [ ] Title tag recomendada escrita por extenso com contagem de caracteres entre parêntesis
- [ ] Meta description recomendada escrita por extenso
- [ ] Alt text sugerido para imagens sem alt inclui keyword natural quando aplicável
- [ ] Cada recomendação tem Expected Impact (ex: `+CTR estimado`, `resolve CLS`, `elegível para rich result`)
- ❌ NOT delivery-ready: `Optimiza o title tag para incluir a keyword principal.`
- ✅ Delivery-ready: `Title sugerido: "Cuidadores ao Domicílio em Lisboa | Cuidai" (48 chars) — inclui keyword primária + brand`

### Gate 4 — Schema é válido e nunca inclui tipos proibidos
- [ ] JSON-LD gerado é sintacticamente válido (chaves fechadas, vírgulas correctas)
- [ ] NUNCA inclui `HowTo` nem `FAQPage` (excepto gov/saúde confirmado)
- [ ] `@context` e `@type` presentes em todos os blocos
- [ ] Schema sugerido é coerente com o tipo de página (Product numa página de produto, LocalBusiness na homepage, etc.)
- ❌ NOT delivery-ready: Schema `FAQPage` sugerido para blog post de SaaS
- ✅ Delivery-ready: Schema `Service` com `provider`, `areaServed`, `name` preenchidos com dados reais da página

### Gate 5 — Flags técnicas de Core Web Vitals são específicas
- [ ] LCP flag só disparado se há evidência real (imagem hero >200KB, `<link rel="preload">` ausente)
- [ ] CLS flag só disparado se imagens sem `width`/`height` ou conteúdo injectado detectado
- [ ] INP flag só disparado se scripts sem `async`/`defer` identificados no `<head>`
- [ ] Flags marcadas como "referência — não mensurável só por HTML" (não confundir com dados reais de CrUX)
- ❌ NOT delivery-ready: `Provável problema de LCP.` sem identificar o elemento suspeito
- ✅ Delivery-ready: `LCP potencial: hero image \`banner-home.jpg\` sem \`loading="eager"\` + sem preload hint. Dimensões não definidas → CLS risk.`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Zero ocorrências de `[URL]`, `[keyword]`, `[client name]`, `[inserir aqui]`
- [ ] URL analisada aparece explicitamente no output
- [ ] Nome do projecto/domínio identificado no cabeçalho do relatório
- [ ] Todos os exemplos de título, meta, alt text usam conteúdo real da página ou proposta concreta
- ❌ NOT delivery-ready: `Title sugerido: "[Keyword Principal] | [Nome da Empresa]"`
- ✅ Delivery-ready: `Title sugerido: "Software de Gestão Tributária para PMEs | Tributario.AI" (52 chars)`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via fetch/read da página real nesta sessão
- 🟡 **assumed** — plausível com base em padrões do sector, mas precisa confirmação do cliente antes de entrega
- 🟢 **projection** — estimativa de impacto por design (não verificável sem dados externos)

Output checklist upfront mostra ao reader exatamente o que é trust-as-is vs o que precisa verify antes de publicar ou apresentar.  **Honest transparency > inflated delivery.**

❌ NOT delivery-ready: `Overall Score: 68/100 — meta description em falta, imagens sem alt text, schema ausente.` — reader não sabe se os scores foram calculados da página real ou estimados; dados de tráfego e impacto surgem sem origem.

✅ Delivery-ready:
- 🔵 **verified** — `<title>` tem 81 caracteres (extraído do HTML via fetch); H1 ausente confirmado no DOM
- 🟡 **assumed** — página assume público PT; hreflang não implementado — cliente deve confirmar se existe versão EN planeada
- 🟢 **projection** — corrigir meta description de 38→155 chars estima +8-12% CTR orgânico (benchmark sector e-commerce; não garantido)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (ex: intenção de internacionalização, autor/bio para E-E-A-T, canonical intencional ou erro)
- [ ] All 🔵 citations referem elemento HTML exato + valor encontrado (ex: `og:image` URL real, tamanho ficheiro em KB)
- [ ] All 🟢 projections de impacto (score lifts, CTR, ranking) labeled como estimativa ao cliente — clear expectations

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SEO Analysis — cuidai.pt/cuidadores-lisboa

**Analisado em:** 2025-06-10  
**URL:** https://cuidai.pt/cuidadores-lisboa  
**Tipo de página:** Landing page de serviço (cidade)

---

## Page Score Card

Overall Score: 61/100

On-Page SEO:     54/100  █████░░░░░
Content Quality: 70/100  ███████░░░
Technical:       65/100  ██████░░░░
Schema:          20/100  ██░░░░░░░░
Images:          75/100  ███████░░░
```

---

## Issues Found

### 🔴 Critical
**C1 — Canonical ausente**  
Nenhuma tag `<link rel="canonical">` encontrada. Risco de conteúdo duplicado se a página
for acessível via `?utm_source=` ou `www.` variante.  
→ Adicionar: `<link rel="canonical" href="https://cuidai.pt/cuidadores-lisboa" />`

### 🟠 High
**H1 — Title tag com 78 caracteres (acima do limite)**  
Actual: `"Encontra os Melhores Cuidadores ao Domicílio em Lisboa e Região de Lisboa, Portugal"`  
Limite: 50-60 chars para evitar truncagem no SERP.

**H2 — Meta description ausente**  
Nenhuma `<meta name="description">` encontrada. Google vai gerar snippet automático
(normalmente sub-óptimo para CTR).

**H3 — Schema inexistente**  
Página sem nenhum JSON-LD. Oportunidade perdida para `LocalBusiness` + `Service`.

### 🟡 Medium
**M1 — og:image não definido**  
Open Graph incompleto: `og:title` e `og:url` presentes, `og:image` ausente.
Partilhas sociais vão usar imagem genérica ou nenhuma.

**M2 — 3 imagens sem atributo width/height**  
`cuidadora-ana.jpg`, `cuidadora-rute.jpg`, `equipa-cuidai.png` sem dimensões.
CLS risk em mobile.

### 🟢 Low
**L1 — Keyword density abaixo do esperado**  
"cuidadores Lisboa" aparece 4× em ~680 palavras (0.6%). Recomendado 1-2%.

---

## Recommendations

| Prioridade | Acção | Impact esperado |
|---|---|---|
| Critical | Adicionar canonical self-referencing | Elimina risco duplicado |
| High | Novo title: `"Cuidadores ao Domicílio em Lisboa \| Cuidai"` (45 chars) | +CTR SERP estimado |
| High | Meta description (ver abaixo) | +CTR, controlo do snippet |
| High | Implementar Schema (ver JSON-LD abaixo) | Elegível rich result |
| Medium | Adicionar `og:image` 1200×630px | Melhora partilha social |
| Medium | Definir `width`/`height` nas 3 imagens | Resolve CLS mobile |

**Meta description sugerida** (155 chars):  
`"Encontra cuidadores ao domicílio certificados em Lisboa. Matching personalizado, perfis verificados e suporte 24h. Começa hoje — é grátis."`

---

## Schema Suggestion — LocalBusiness + Service

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Cuidai",
  "url": "https://cuidai.pt",
  "description": "Plataforma de matching entre famílias e cuidadores ao domicílio em Portugal",
  "areaServed": {
    "@type": "City",
    "name": "Lisboa"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Serviços de Cuidadores",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Cuidador ao Domicílio em Lisboa"
        }
      }
    ]
  }
}
```

---

## Core Web Vitals — Flags (referência, não dados CrUX reais)

- ⚠️ **CLS potencial:** `cuidadora-ana.jpg`, `cuidadora-rute.jpg`, `equipa-cuidai.png`
  sem dimensões declaradas — browser faz reflow ao carregar
- ✅ **LCP OK aparente:** hero image tem `loading="eager"` e tamanho 187KB (abaixo de 200KB)
- ✅ **INP OK aparente:** scripts principais têm `defer` no `<head>`
```

---

## Output anti-patterns

- Scores redondos sem evidência: `72/100` igual em todas as páginas analisadas, independentemente dos findings
- Issues vagos sem citar o elemento HTML actual: "a meta description podia ser melhor"
- Recomendar schema `FAQPage` ou `HowTo` em páginas que não são gov/saúde
- Title/meta description sugeridos com placeholders: `"[Keyword] | [Empresa]"` em vez de texto real
- Confundir flags de CWV (inferidas do HTML) com métricas reais de CrUX/PSI — não afirmar scores LCP/CLS concretos
- Canonical "sugerida" sem fornecer a tag HTML pronta a copiar
- JSON-LD com erros de sintaxe: vírgula a mais, propriedades sem aspas, `@context` ausente
- Análise de imagens sem citar nome do ficheiro — "há imagens sem alt text" sem especificar quais
- Omitir a secção de prioridades (Critical/High/Medium/Low) e listar tudo no mesmo nível
- Relatório sem a URL real no cabeçalho — impossível o cliente saber qual página foi analisada
