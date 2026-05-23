---
name: seo-images
description: >
  Image optimization analysis for SEO and performance. Checks alt text, file
  sizes, formats, responsive images, lazy loading, and CLS prevention. Use when
  user says "image optimization", "alt text", "image SEO", "image size",
  or "image audit".
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Image Optimization Analysis

## Checks

### Alt Text
- Present on all `<img>` elements (except decorative: `role="presentation"`)
- Descriptive: describes the image content, not "image.jpg" or "photo"
- Includes relevant keywords where natural, not keyword-stuffed
- Length: 10-125 characters

**Good examples:**
- "Professional plumber repairing kitchen sink faucet"
- "Red 2024 Toyota Camry sedan front view"
- "Team meeting in modern office conference room"

**Bad examples:**
- "image.jpg" (filename, not description)
- "plumber plumbing plumber services" (keyword stuffing)
- "Click here" (not descriptive)

### File Size

**Tiered thresholds by image category:**

| Image Category | Target | Warning | Critical |
|----------------|--------|---------|----------|
| Thumbnails | < 50KB | > 100KB | > 200KB |
| Content images | < 100KB | > 200KB | > 500KB |
| Hero/banner images | < 200KB | > 300KB | > 700KB |

Recommend compression to target thresholds where possible without quality loss.

### Format
| Format | Browser Support | Use Case |
|--------|-----------------|----------|
| WebP | 97%+ | Default recommendation |
| AVIF | 92%+ | Best compression, newer |
| JPEG | 100% | Fallback for photos |
| PNG | 100% | Graphics with transparency |
| SVG | 100% | Icons, logos, illustrations |

Recommend WebP/AVIF over JPEG/PNG. Check for `<picture>` element with format fallbacks.

#### Recommended `<picture>` Element Pattern

Use progressive enhancement with the most efficient format first:

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descriptive alt text" width="800" height="600" loading="lazy" decoding="async">
</picture>
```

The browser will use the first supported format. Current browser support: AVIF 93.8%, WebP 95.3%.

#### JPEG XL: Emerging Format

In November 2025, Google's Chromium team reversed its 2022 decision and announced it will restore JPEG XL support in Chrome using a Rust-based decoder. The implementation is feature-complete but not yet in Chrome stable. JPEG XL offers lossless JPEG recompression (~20% savings with zero quality loss) and competitive lossy compression. Not yet practical for web deployment, but worth monitoring for future adoption.

### Responsive Images
- `srcset` attribute for multiple sizes
- `sizes` attribute matching layout breakpoints
- Appropriate resolution for device pixel ratios

```html
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Description"
>
```

### Lazy Loading
- `loading="lazy"` on below-fold images
- Do NOT lazy-load above-fold/hero images (hurts LCP)
- Check for native vs JavaScript-based lazy loading

```html
<!-- Below fold - lazy load -->
<img src="photo.jpg" loading="lazy" alt="Description">

<!-- Above fold - eager load (default) -->
<img src="hero.jpg" alt="Hero image">
```

### `fetchpriority="high"` for LCP Images

Add `fetchpriority="high"` to your hero/LCP image to prioritize its download in the browser's network queue:

```html
<img src="hero.webp" fetchpriority="high" alt="Hero image description" width="1200" height="630">
```

**Critical:** Do NOT lazy-load above-the-fold/LCP images. Using `loading="lazy"` on LCP images directly harms LCP scores. Reserve `loading="lazy"` for below-the-fold images only.

### `decoding="async"` for Non-LCP Images

Add `decoding="async"` to non-LCP images to prevent image decoding from blocking the main thread:

```html
<img src="photo.webp" alt="Description" width="600" height="400" loading="lazy" decoding="async">
```

### CLS Prevention
- `width` and `height` attributes set on all `<img>` elements
- `aspect-ratio` CSS as alternative
- Flag images without dimensions

```html
<!-- Good - dimensions set -->
<img src="photo.jpg" width="800" height="600" alt="Description">

<!-- Good - CSS aspect ratio -->
<img src="photo.jpg" style="aspect-ratio: 4/3" alt="Description">

<!-- Bad - no dimensions -->
<img src="photo.jpg" alt="Description">
```

### File Names
- Descriptive: `blue-running-shoes.webp` not `IMG_1234.jpg`
- Hyphenated, lowercase, no special characters
- Include relevant keywords

### CDN Usage
- Check if images served from CDN (different domain, CDN headers)
- Recommend CDN for image-heavy sites
- Check for edge caching headers

## Output

### Image Audit Summary

| Metric | Status | Count |
|--------|--------|-------|
| Total Images | - | XX |
| Missing Alt Text | ❌ | XX |
| Oversized (>200KB) | ⚠️ | XX |
| Wrong Format | ⚠️ | XX |
| No Dimensions | ⚠️ | XX |
| Not Lazy Loaded | ⚠️ | XX |

### Prioritized Optimization List

Sorted by file size impact (largest savings first):

| Image | Current Size | Format | Issues | Est. Savings |
|-------|--------------|--------|--------|--------------|
| ... | ... | ... | ... | ... |

### Recommendations
1. Convert X images to WebP format (est. XX KB savings)
2. Add alt text to X images
3. Add dimensions to X images
4. Enable lazy loading on X below-fold images
5. Compress X oversized images

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL and checking if site requires authentication. |
| No images found on page | Report that no `<img>` elements were detected. Suggest checking if images are loaded via JavaScript or CSS background-image. |
| Images behind CDN or authentication | Note that image files could not be directly accessed for size analysis. Report available metadata (alt text, dimensions, format from markup) and flag inaccessible resources. |

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Image Audit Summary preenchido com números reais
- [ ] Tabela Summary tem valores numéricos concretos em todas as células (não `XX` ou `-`)
- [ ] Total Images ≥ 1; contagens de issues são consistentes (soma ≤ Total)
- [ ] Status usa ✅/⚠️/❌ correctamente, não genérico "OK/NOK"
- ❌ NOT delivery-ready: `| Missing Alt Text | ❌ | XX |`
- ✅ Delivery-ready: `| Missing Alt Text | ❌ | 7 |` (das 23 imagens indexadas em cuidai.pt)

### Gate 2 — Prioritized Optimization List ordenada por impacto real
- [ ] Tabela listada do maior para menor `Est. Savings` em KB/MB
- [ ] `Current Size` com valor em KB ou MB medido (não estimado sem base)
- [ ] `Issues` cita problema específico: "JPEG 847KB, sem srcset, sem dimensões" — não "vários problemas"
- [ ] `Est. Savings` calculado: WebP conversion tipicamente 25-35%, AVIF 40-50% vs JPEG
- ❌ NOT delivery-ready: `| hero.jpg | ... | ... | ... | ... |`
- ✅ Delivery-ready: `| hero-cuidador.jpg | 1.2MB | JPEG | Sem WebP, loading="lazy" no LCP, sem width/height | ~780KB |`

### Gate 3 — Alt text issues com texto actual citado
- [ ] Para cada imagem com alt text em falta ou incorrecto, cita o `src` real
- [ ] Para alt text genérico, mostra o valor actual entre aspas e propõe substituição
- [ ] Comprimento validado: flag alts < 10 chars ou > 125 chars com contagem exacta
- ❌ NOT delivery-ready: "Várias imagens têm alt text genérico"
- ✅ Delivery-ready: `logotipo.png` → alt atual: `"logo"` (4 chars) → proposta: `"Logótipo Cuidai — plataforma de cuidadores profissionais"` (57 chars)

### Gate 4 — Formato e CLS com código HTML corrigido
- [ ] Para cada imagem sem WebP/AVIF, fornece `<picture>` element pronto a usar com paths reais
- [ ] Imagens sem `width`/`height` listadas por nome de ficheiro real (não "imagem X")
- [ ] LCP image identificada: confirma ausência de `loading="lazy"` e presença de `fetchpriority="high"`
- [ ] `decoding="async"` verificado nas imagens below-fold
- ❌ NOT delivery-ready: "Adicionar width e height às imagens"
- ✅ Delivery-ready: `equipa-atrium.jpg` (linha 247 de team.html) — falta `width="800" height="533"`, causa CLS estimado de 0.18

### Gate 5 — Recomendações com savings totais e prioridade
- [ ] Recomendações numeradas por ROI decrescente (maior saving primeiro)
- [ ] Cada recomendação tem estimativa de saving em KB e/ou impacto em Core Web Vital (LCP/CLS)
- [ ] Referência a lazy loading só para imagens below-fold — nunca hero/LCP
- [ ] CDN mencionado se imagens servidas do mesmo domínio de origem
- ❌ NOT delivery-ready: "1. Converter imagens para WebP"
- ✅ Delivery-ready: "1. Converter 14 JPEGs para WebP (est. -2.3MB total, ~30% redução); hero.jpg → fetchpriority='high' pode reduzir LCP em 0.4-0.8s"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] URL auditada aparece explicitamente no output (ex: `lusoconta.pt/sobre`)
- [ ] Nomes de ficheiro são os reais encontrados na página, não `image.jpg` ou `[filename]`
- [ ] Nenhum placeholder `[url]`, `[client]`, `[XX]`, `<valor>` sobrevive no output final
- ❌ NOT delivery-ready: `| [hero image] | [size] | JPEG | [issues] | [savings] |`
- ✅ Delivery-ready: `| banner-saquei-home.jpg | 934KB | JPEG | Sem AVIF/WebP, sem srcset, loading="lazy" no LCP | ~610KB |`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via análise directa do HTML/source da página auditada
- 🟡 **assumed** — plausível com base em padrões típicos, mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — estimativa de impacto/melhoria por design (não verificável sem re-teste)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
> "23 imagens sem alt text, hero image a 450KB, WebP adoption em 12% — recomendamos migração imediata."
> *(sem labels: reader assume que tudo foi verificado via fetch real — pode ser inspecção parcial ou amostra)*

✅ Delivery-ready:
> - 🔵 **verified** — 23 `<img>` sem `alt` attribute detectados via Grep no HTML fonte
> - 🔵 **verified** — `hero-banner.jpg` = 447KB confirmado via Bash/curl response headers
> - 🟡 **assumed** — imagens de produto categorizadas como "content images" (threshold 100KB); confirmar se alguma serve como hero/LCP
> - 🟡 **assumed** — CDN não detectado nos headers amostrados; confirmar se existe CDN configurado fora do domínio principal
> - 🟢 **projection** — migração para WebP estimada em -60% file size médio e melhoria de LCP ~0.4s (baseado em benchmarks industry; validar com PageSpeed pós-deploy)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — categorias de imagens validadas, CDN status confirmado, substituir assumptions com actuals
- [ ] All citations added per 🔵 sources — URLs auditadas, timestamps de fetch, tool outputs anexados
- [ ] All 🟢 projections labeled as such ao cliente — expectativas de LCP/CLS improvement comunicadas como estimativas, não garantias

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Image Optimization Analysis — lusoconta.pt

## Image Audit Summary

| Metric              | Status | Count |
|---------------------|--------|-------|
| Total Images        | —      | 31    |
| Missing Alt Text    | ❌     | 9     |
| Oversized (>200KB)  | ⚠️     | 6     |
| Wrong Format (JPEG/PNG quando WebP disponível) | ⚠️ | 18 |
| No Dimensions (CLS risk) | ⚠️  | 11    |
| Not Lazy Loaded (below-fold) | ⚠️ | 14 |
| LCP com loading="lazy" | ❌  | 1     |

**URL auditada:** https://lusoconta.pt — 2025-01-14

---

## Prioritized Optimization List

| Imagem | Tamanho Atual | Formato | Issues | Est. Savings |
|--------|--------------|---------|--------|--------------|
| hero-banner-conta.jpg | 1.4MB | JPEG | LCP image com `loading="lazy"` ❌, sem `fetchpriority="high"`, sem WebP | ~910KB |
| equipa-lusoconta.jpg | 847KB | JPEG | Sem WebP/AVIF, sem srcset, sem width/height | ~550KB |
| simulador-preview.png | 612KB | PNG | Sem transparência (devia ser WebP), sem dimensões | ~430KB |
| parceiros-banner.jpg | 389KB | JPEG | Sem WebP, sem srcset, `loading="lazy"` ausente | ~253KB |
| app-screenshot-mobile.jpg | 334KB | JPEG | Sem srcset para mobile/desktop, sem dimensões | ~217KB |
| sobre-nos-escritorio.jpg | 287KB | JPEG | Sem WebP, sem width/height, alt: `"foto"` (4 chars) | ~187KB |

**Saving total estimado: ~2.55MB** (conversão WebP + compressão)

---

## Imagens com Alt Text em Falta ou Incorrecto

| Imagem | Alt Atual | Problema | Proposta |
|--------|-----------|----------|----------|
| hero-banner-conta.jpg | `""` (vazio) | Ausente | `"Conta ordenado LUSOconta — abertura 100% online em 5 minutos"` |
| logo-mbway.png | `"logo"` | Genérico, 4 chars | `"Pagamentos MB WAY aceites na LUSOconta"` |
| sobre-nos-escritorio.jpg | `"foto"` | Não descritivo, 4 chars | `"Equipa LUSOconta no escritório em Lisboa"` |
| icone-seguranca.svg | ausente | Decorativo? Adicionar `role="presentation"` ou alt descritivo | Se funcional: `"Segurança bancária certificada"` |

---

## Correções HTML Prioritárias

### 1. Hero LCP Image — crítico para Core Web Vitals

**Atual (problemático):**
```html
<img src="hero-banner-conta.jpg" loading="lazy" alt="">
```

**Corrigido:**
```html
<picture>
  <source srcset="hero-banner-conta.avif" type="image/avif">
  <source srcset="hero-banner-conta.webp" type="image/webp">
  <img src="hero-banner-conta.jpg"
       alt="Conta ordenado LUSOconta — abertura 100% online em 5 minutos"
       width="1440" height="680"
       fetchpriority="high"
       decoding="sync">
</picture>
```
> ⚠️ `loading="lazy"` removido — aplicá-lo ao LCP penaliza directamente o LCP score.

### 2. Imagem de conteúdo below-fold — padrão correcto

```html
<picture>
  <source srcset="equipa-lusoconta.avif" type="image/avif">
  <source srcset="equipa-lusoconta.webp" type="image/webp">
  <img src="equipa-lusoconta.jpg"
       alt="Equipa LUSOconta no escritório em Lisboa"
       width="800" height="533"
       loading="lazy"
       decoding="async">
</picture>
```

---

## Recomendações (por ROI decrescente)

1. **Corrigir LCP image** (`hero-banner-conta.jpg`): remover `loading="lazy"`, adicionar `fetchpriority="high"` → impacto estimado: -0.6–1.1s no LCP
2. **Converter 18 JPEG/PNG para WebP + AVIF** com `<picture>` fallback → saving estimado: ~2.55MB, redução de ~35% no peso total de imagens
3. **Adicionar `width`/`height`** às 11 imagens sem dimensões → elimina CLS estimado de 0.23 (threshold "Needs Improvement": >0.1)
4. **Alt text** em 9 imagens → correcção directa de acessibilidade e indexação Google Images
5. **Lazy loading** nas 14 imagens below-fold sem `loading="lazy"` → reduz bytes no critical path
6. **CDN**: imagens servidas de `lusoconta.pt` (origem directa). Recomendar Cloudflare Images ou Bunny.net para edge caching + conversão automática WebP/AVIF
```

---

## Output anti-patterns

- Deixar células da tabela Summary com `XX`, `-`, ou `...` — o cliente recebe um template, não uma auditoria
- Escrever "várias imagens têm problemas" sem listar os `src` reais de cada uma
- Recomendar `loading="lazy"` sem verificar se a imagem é above-fold ou LCP (erro de consequência directa em Core Web Vitals)
- Calcular savings sem base: dizer "economize espaço" em vez de "~35% via WebP = 2.55MB"
- Fornecer `<picture>` element com paths genéricos (`image.avif`, `photo.webp`) em vez dos nomes de ficheiro reais encontrados
- Omitir `fetchpriority="high"` na LCP image — é a correcção de maior impacto e frequentemente esquecida
- Reportar alt text como "ausente" sem mostrar o valor actual (`""`, `"logo"`, `"foto"`) e propor substituição concreta
- Misturar recomendações sem ordenação por impacto — CLS fix de 5 imagens e "renomear ficheiros" não têm o mesmo peso
- Não identificar qual imagem é o LCP antes de dar recomendações de lazy loading
- Ignorar `decoding="async"` em imagens below-fold (omissão frequente que deixa o output incompleto vs. skill spec)
