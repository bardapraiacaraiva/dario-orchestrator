---
name: seo-sitemap
description: >
  Analyze existing XML sitemaps or generate new ones with industry templates.
  Validates format, URLs, and structure. Use when user says "sitemap",
  "generate sitemap", "sitemap issues", or "XML sitemap".
user-invokable: true
argument-hint: "[url or generate]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# Sitemap Analysis & Generation

## Mode 1: Analyze Existing Sitemap

### Validation Checks
- Valid XML format
- URL count <50,000 per file (protocol limit)
- All URLs return HTTP 200
- `<lastmod>` dates are accurate (not all identical)
- No deprecated tags: `<priority>` and `<changefreq>` are ignored by Google
- Sitemap referenced in robots.txt
- Compare crawled pages vs sitemap; flag missing pages

### Quality Signals
- Sitemap index file if >50k URLs
- Split by content type (pages, posts, images, videos)
- No non-canonical URLs in sitemap
- No noindexed URLs in sitemap
- No redirected URLs in sitemap
- HTTPS URLs only (no HTTP)

### Common Issues
| Issue | Severity | Fix |
|-------|----------|-----|
| >50k URLs in single file | Critical | Split with sitemap index |
| Non-200 URLs | High | Remove or fix broken URLs |
| Noindexed URLs included | High | Remove from sitemap |
| Redirected URLs included | Medium | Update to final URLs |
| All identical lastmod | Low | Use actual modification dates |
| Priority/changefreq used | Info | Can remove (ignored by Google) |

## Mode 2: Generate New Sitemap

### Process
1. Ask for business type (or auto-detect from existing site)
2. Load industry template from `../seo-plan/assets/` directory
3. Interactive structure planning with user
4. Apply quality gates:
   - ⚠️ WARNING at 30+ location pages (require 60%+ unique content)
   - 🛑 HARD STOP at 50+ location pages (require justification)
5. Generate valid XML output
6. Split at 50k URLs with sitemap index
7. Generate STRUCTURE.md documentation

### Safe Programmatic Pages (OK at scale)
✅ Integration pages (with real setup docs)
✅ Template/tool pages (with downloadable content)
✅ Glossary pages (200+ word definitions)
✅ Product pages (unique specs, reviews)
✅ User profile pages (user-generated content)

### Penalty Risk (avoid at scale)
❌ Location pages with only city name swapped
❌ "Best [tool] for [industry]" without industry-specific value
❌ "[Competitor] alternative" without real comparison data
❌ AI-generated pages without human review and unique value

## Sitemap Format

### Standard Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2026-02-07</lastmod>
  </url>
</urlset>
```

### Sitemap Index (for >50k URLs)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-posts.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
</sitemapindex>
```

## Error Handling

- **URL unreachable**: Report the HTTP status code and suggest checking if the site is live
- **No sitemap found**: Check common locations (/sitemap.xml, /sitemap_index.xml, robots.txt reference) before reporting "not found"
- **Invalid XML format**: Report specific parsing errors with line numbers
- **Rate limiting detected**: Back off and report partial results with a note about retry timing

## Output

### For Analysis
- `VALIDATION-REPORT.md`: analysis results
- Issues list with severity
- Recommendations

### For Generation
- `sitemap.xml` (or split files with index)
- `STRUCTURE.md`: site architecture documentation
- URL count and organization summary

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1. XML validity + protocol compliance
- [ ] Sitemap abre sem erros de parsing (namespace correto: `http://www.sitemaps.org/schemas/sitemap/0.9`)
- [ ] Nenhum ficheiro único excede 50.000 URLs — se excede, sitemap index gerado
- [ ] Todas as URLs usam HTTPS (zero URLs com `http://`)
- [ ] `<priority>` e `<changefreq>` removidos ou flagged como ignorados pelo Google (não apresentados como "otimizações")
- [ ] `<lastmod>` com datas reais e distintas — não todas iguais (ex: `2024-01-01` em 847 URLs = inválido)

❌ NOT delivery-ready: "O sitemap tem priority=0.8 nas páginas principais para ajudar o ranking"
✅ Delivery-ready: "Removidos `<priority>` e `<changefreq>` de 234 URLs — ignorados pelo Google desde 2023; mantido apenas `<lastmod>` com datas reais por ficheiro"

### 2. URL health: 200s only, sem redirects nem noindex
- [ ] Zero URLs não-200 incluídas (404, 301, 302 identificados e removidos/corrigidos)
- [ ] Zero URLs com `noindex` no sitemap — verificado via header `X-Robots-Tag` e meta tag
- [ ] Zero URLs redirecionadas — substituídas pela URL final canónica
- [ ] Sitemap referenciado em `robots.txt` (linha `Sitemap: https://...`)

❌ NOT delivery-ready: "Encontrei algumas URLs com redirect mas deixei para o cliente verificar"
✅ Delivery-ready: "17 URLs com redirect 301 substituídas por destino final; 3 URLs noindex removidas; robots.txt confirma `Sitemap: https://cuidai.pt/sitemap.xml`"

### 3. Cobertura: missing pages identificadas
- [ ] Comparação crawl vs sitemap realizada — páginas indexáveis ausentes listadas
- [ ] Categorias de conteúdo cobertas: páginas core, blog/posts, landing pages, páginas de produto/serviço
- [ ] Páginas com tráfego orgânico (se GSC disponível) confirmadas no sitemap
- [ ] Se site multilingue: hreflang implementado e cada URL tem par na língua alternativa

❌ NOT delivery-ready: "O sitemap tem 45 URLs" (sem verificar se existem mais páginas indexáveis no site)
✅ Delivery-ready: "Sitemap actual: 45 URLs. Crawl identificou 23 páginas ausentes — adicionadas 19 (blog posts publicados); 4 excluídas por serem duplicados com canonical"

### 4. Estrutura e organização do sitemap
- [ ] Se >500 URLs: split por tipo de conteúdo (`sitemap-pages.xml`, `sitemap-posts.xml`, `sitemap-products.xml`)
- [ ] Sitemap index presente e válido se múltiplos ficheiros
- [ ] Nenhuma URL duplicada dentro do mesmo sitemap
- [ ] Páginas programáticas (location pages, glossário) avaliadas: ≥200 palavras únicas por página ou flagged

❌ NOT delivery-ready: Um único `sitemap.xml` com 1.200 URLs misturando blog, produtos e landing pages
✅ Delivery-ready: "3 ficheiros: `sitemap-pages.xml` (12 URLs), `sitemap-services.xml` (34 URLs), `sitemap-blog.xml` (198 URLs) — index em `sitemap_index.xml`"

### 5. Documentação entregue (VALIDATION-REPORT + STRUCTURE.md)
- [ ] `VALIDATION-REPORT.md` com: contagem de URLs, issues por severidade, fixes aplicados, issues em aberto
- [ ] `STRUCTURE.md` com arquitectura do site e lógica de organização do sitemap
- [ ] Issues classificadas por severidade (Critical / High / Medium / Low / Info)
- [ ] Recomendações accionáveis com proprietário claro (dev / SEO / conteúdo)

❌ NOT delivery-ready: "Aqui está o sitemap.xml" (sem relatório, sem documentação)
✅ Delivery-ready: VALIDATION-REPORT com 5 Critical resolvidos, 2 High em aberto com ticket sugerido; STRUCTURE.md com mapa das 3 secções do site

### 6. Output usa NOME DO CLIENTE + dados reais — zero angle-brackets ou placeholders
- [ ] Zero instâncias de `<client-name>`, `example.com`, `YOUR_DOMAIN`, `[inserir aqui]`
- [ ] Todas as URLs no sitemap gerado são do domínio real do cliente
- [ ] Datas `<lastmod>` são datas reais (não `YYYY-MM-DD` ou `2026-02-07` genérico)
- [ ] Contagens de URLs, HTTP status codes e nomes de ficheiros são os reais do projecto

❌ NOT delivery-ready: `<loc>https://example.com/servicos</loc>` no sitemap entregue
✅ Delivery-ready: `<loc>https://cuidai.pt/servicos/higiene-canina</loc>` com `<lastmod>2025-03-14</lastmod>`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/URL/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via WebFetch/HTTP check/parse real do ficheiro
- 🟡 **assumed** — plausível com base na estrutura detectada, mas precisa de confirmação do cliente antes da entrega
- 🟢 **projection** — estimativa por design (ex: contagens após geração, datas sugeridas)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
- "847 URLs válidas no sitemap" — sem indicar se foram fetchadas (🔵) ou contadas pelo parser sem verificar HTTP status (🟡)
- "`<lastmod>` actualizado" — sem indicar se as datas vieram do servidor (🔵) ou foram assumidas como data de hoje (🟡)
- "Sitemap referenciado no robots.txt" — sem ter feito WebFetch ao `/robots.txt` real

✅ Delivery-ready:
- 🔵 **verified** — 312 URLs retornam HTTP 200 (confirmado via Bash/curl batch)
- 🟡 **assumed** — 28 URLs de `/blog/*` assumidas como indexáveis; cliente deve confirmar ausência de `noindex` em templates de categoria
- 🟢 **projection** — sitemap index com 3 ficheiros gerado para ~74.000 URLs estimadas após crawl completo; split real depende do volume final

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — substituir assumptions com actuals (ex: status HTTP real, meta robots verificados)
- [ ] Todos os itens 🔵 com fonte citada — URL do ficheiro analisado, timestamp do fetch, comando HTTP usado
- [ ] Todos os itens 🟢 labeled explicitamente ao cliente como projecção — nunca apresentados como factos verificados

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Sitemap Audit — Cuidai.pt

**Data:** 2025-06-10
**Domínio:** https://cuidai.pt
**Sitemap actual:** https://cuidai.pt/sitemap.xml
**URLs no sitemap:** 38
**URLs encontradas no crawl:** 61

---

## VALIDATION-REPORT.md

### Resumo Executivo
O sitemap actual da Cuidai.pt cobre apenas 62% das páginas indexáveis do site.
Foram identificadas 23 páginas ausentes, 4 URLs com redirect e 2 URLs noindex
incluídas indevidamente. Após correcção, sitemap passa de 38 para 54 URLs válidas.

### Issues por Severidade

#### 🔴 Critical (resolver antes de publicar)
| # | Issue | URLs afectadas | Fix |
|---|-------|---------------|-----|
| 1 | 2 URLs noindex incluídas no sitemap | /obrigado, /404-custom | Removidas |
| 2 | Sitemap não referenciado em robots.txt | — | Adicionado `Sitemap:` line |

#### 🟠 High
| # | Issue | URLs afectadas | Fix |
|---|-------|---------------|-----|
| 3 | 4 URLs com redirect 301 | /servicos-old, /higiene, /passeios-caes, /contacto-antigo | Substituídas por URLs finais |
| 4 | 23 páginas indexáveis ausentes do sitemap | Ver lista abaixo | Adicionadas 19; 4 excluídas |

#### 🟡 Medium
| # | Issue | URLs afectadas | Fix |
|---|-------|---------------|-----|
| 5 | `<lastmod>` idêntico em 38 URLs (2024-01-01) | Todas | Actualizado com datas reais |

#### 🔵 Info
| # | Issue | URLs afectadas | Nota |
|---|-------|---------------|------|
| 6 | `<priority>` e `<changefreq>` presentes | 38 URLs | Removidos — ignorados pelo Google |

### Páginas ausentes identificadas (crawl vs sitemap)

**Adicionadas ao sitemap (19):**
- /blog/como-cortar-unhas-cao (publicado 2025-04-02)
- /blog/racao-premium-portugal (publicado 2025-03-18)
- /servicos/higiene-canina (destino final do redirect /higiene)
- /servicos/passeios-individuais
- /servicos/creche-diurna
- /sobre-nos/equipa
- /sobre-nos/instalacoes
- /faq
- ... (+ 11 blog posts de 2024-2025)

**Excluídas intencionalmente (4):**
- /obrigado — página de thank-you, noindex correcto
- /carrinho — conteúdo dinâmico, não indexável
- /minha-conta — área privada
- /404-custom — página de erro

### robots.txt — fix aplicado
```
# Adicionado em 2025-06-10
Sitemap: https://cuidai.pt/sitemap.xml
```

---

## Sitemap gerado (sitemap.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

  <!-- Páginas core -->
  <url>
    <loc>https://cuidai.pt/</loc>
    <lastmod>2025-05-30</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/sobre-nos</loc>
    <lastmod>2025-04-15</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/sobre-nos/equipa</loc>
    <lastmod>2025-04-15</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/sobre-nos/instalacoes</loc>
    <lastmod>2025-02-20</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/faq</loc>
    <lastmod>2025-05-01</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/contacto</loc>
    <lastmod>2025-01-10</lastmod>
  </url>

  <!-- Serviços -->
  <url>
    <loc>https://cuidai.pt/servicos</loc>
    <lastmod>2025-05-30</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/servicos/higiene-canina</loc>
    <lastmod>2025-03-05</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/servicos/passeios-individuais</loc>
    <lastmod>2025-03-05</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/servicos/creche-diurna</loc>
    <lastmod>2025-04-22</lastmod>
  </url>

  <!-- Blog (amostra) -->
  <url>
    <loc>https://cuidai.pt/blog/como-cortar-unhas-cao</loc>
    <lastmod>2025-04-02</lastmod>
  </url>
  <url>
    <loc>https://cuidai.pt/blog/racao-premium-portugal</loc>
    <lastmod>2025-03-18</lastmod>
  </url>

  <!-- ... restantes 42 URLs ... -->

</urlset>
```

**Total final: 54 URLs válidas** (era 38; +16 líquidas após remover 4 inválidas e adicionar 20)

---

## STRUCTURE.md — Arquitectura Cuidai.pt

### Organização do sitemap
Ficheiro único (`sitemap.xml`) — 54 URLs, abaixo do limite de 50.000.
Não requer sitemap index neste momento.

### Secções do site
| Secção | URLs | % do sitemap |
|--------|------|-------------|
| Blog / Conteúdo | 34 | 63% |
| Serviços | 10 | 18% |
| Páginas core | 8 | 15% |
| Sobre / Equipa | 2 | 4% |

### Recomendações futuras
- **Quando blog atingir 200+ posts:** split em `sitemap-pages.xml` + `sitemap-blog.xml`
- **Se lançarem loja:** adicionar `sitemap-products.xml`
- **Revisão trimestral:** verificar novas páginas e `<lastmod>` desactualizados
```

---

## Output anti-patterns

- **Deixar `<priority>` e `<changefreq>` sem comentar** — são ignorados pelo Google desde 2023; incluí-los como "boas práticas" induz o cliente em erro
- **Reportar "sitemap com X URLs" sem fazer crawl comparison** — a ausência de páginas é frequentemente o problema maior que o formato
- **Usar `example.com` ou `YOUR_DOMAIN` no sitemap gerado** — o output de produção tem de ter o domínio real do cliente em todas as `<loc>`
- **`<lastmod>` idêntico em todas as URLs** — sinaliza ao Google que as datas são fictícias; usar datas reais ou omitir o campo
- **Não verificar se a URL final de um redirect foi adicionada** — substituir `/old-url` por `/new-url` sem confirmar que a nova URL existe e retorna 200
- **Incluir URLs noindex no sitemap** — contradição directa: diz ao Google "indexa esta" e "não indexas esta" simultaneamente
- **Entregar só o `sitemap.xml` sem VALIDATION-REPORT** — o cliente não sabe o que foi corrigido, o que ficou em aberto, nem porquê
- **Apresentar páginas programáticas sem avaliação de conteúdo único** — 50 location pages com só o nome da cidade trocado é risco de penalização, não uma feature
- **Não verificar `robots.txt`** — um sitemap válido não referenciado em robots.txt tem menor probabilidade de ser descoberto pelos crawlers
- **Reportar HTTP status sem confirmar o URL final** — um 301 que redireciona para outro 301 (redirect chain) precisa de ser resolvido até ao destino final, não só flagged como "redirect"
