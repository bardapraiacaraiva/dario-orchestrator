---
name: dario-cwv-fix
description: Core Web Vitals deep fix for WordPress — diagnose and fix LCP, INP, CLS issues with specific code patches, plugin config, and server-side optimizations. Triggers on "core web vitals", "cwv", "lcp", "inp", "cls", "page speed", "lighthouse score", "performance fix".
license: MIT
---

# DARIO Skill — Core Web Vitals Fix

Goes beyond diagnosis: identifies the specific cause of each CWV failure and provides actionable fixes with code/config snippets.

## When to activate
- Lighthouse mobile score <90
- CrUX data shows LCP >2.5s, INP >200ms, or CLS >0.1
- After `dario-wp-audit` flags performance issues
- Before launch of a redesigned site

## Workflow

### 1. RAG consult
```
mcp__dario-rag__search_kb(query: "core web vitals lcp inp cls wordpress fix", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "litespeed cache nginx performance wordpress", collection: "dario", limit: 5)
```

### 2. Diagnose each metric

#### LCP (<2.5s target)
Common causes + fixes:
- **Hero image not preloaded** → `<link rel="preload" as="image" href="..." fetchpriority="high">`
- **Render-blocking CSS** → critical CSS inline, defer rest
- **TTFB slow** → server cache (LiteSpeed, page cache), CDN, PHP upgrade to 8.2+
- **Web fonts blocking** → `font-display: swap` + preload WOFF2
- **Largest element is below fold** → restructure above-fold content
- **Image format** → WebP/AVIF via Imagify/ShortPixel
- **Image dimensions** → explicit width/height, srcset for responsive

#### INP (<200ms target, replaces FID since March 2024)
Common causes + fixes:
- **Heavy JS on main thread** → defer non-critical scripts, code-split
- **Third-party scripts** (GA4, FB Pixel, chat widgets) → load after interaction / Partytown
- **jQuery dependency chain** → eliminate or defer jQuery
- **Slider/carousel JS** → replace with CSS-only or lightweight (Swiper instead of Slick)
- **Page builder overhead** (Elementor = ~400KB JS) → switch to Bricks/GenerateBlocks, or aggressive defer
- **Event listeners on scroll/resize** → debounce/throttle
- **Long tasks** → break into requestIdleCallback chunks

#### CLS (<0.1 target)
Common causes + fixes:
- **Images without dimensions** → explicit `width` + `height` attributes
- **Web fonts FOUT** → `font-display: optional` or preload + fallback
- **Ads / embeds injected late** → reserved space containers
- **Dynamic content above fold** → skeleton loaders
- **Cookie banner shifting content** → fixed position overlay, not pushing content down
- **Lazy-loaded images above fold** → DON'T lazy-load above fold (fetchpriority="high")

### 3. WordPress-specific fixes

#### LiteSpeed Cache config
```
Page Cache: ON
Object Cache: ON (Redis/Memcached if available)
Browser Cache: ON (max-age 1 year for static assets)
Image Optimization: ON (WebP + LazyLoad except above-fold)
CSS/JS Combine: careful — test for breakage
CSS/JS Minify: ON
Critical CSS: ON (generate per template)
DNS Prefetch: cdn.example.com, fonts.googleapis.com
```

#### Autoptimize (if not using LiteSpeed)
```
Optimize JS: ON, aggregate: OFF (defer instead)
Optimize CSS: ON, aggregate: ON, inline critical: ON
Optimize images: lazy-load (except above fold)
```

#### functions.php snippets
```php
// Preload hero image
add_action('wp_head', function() {
    echo '<link rel="preload" as="image" href="/wp-content/uploads/hero.webp" fetchpriority="high">';
}, 1);

// Defer non-critical JS
add_filter('script_loader_tag', function($tag, $handle) {
    $defer = ['jquery-migrate','comment-reply','wp-embed'];
    if (in_array($handle, $defer)) {
        return str_replace(' src', ' defer src', $tag);
    }
    return $tag;
}, 10, 2);
```

### 4. Verification
- Run Lighthouse mobile BEFORE and AFTER each fix
- Check CrUX 28-day data (real users) vs lab data
- Test on 3G throttled mobile (DevTools Network tab)
- Verify no regressions (CSS broken, JS errors, layout shift)

## Output → save via `dario-obsidian-save`
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - CWV Fix Report.md`

## Red Flags
- Never apply CWV fixes without measuring baseline scores first (Lighthouse + CrUX) — without a before-measurement you cannot prove the fix worked or detect regressions
- Never remove or defer JavaScript without testing the page end-to-end — aggressive JS removal breaks sliders, forms, checkout flows, and analytics tracking
- Always verify every fix on mobile with 3G throttling — desktop Lighthouse green means nothing when 70%+ of real users are on mobile with slow connections
- Never lazy-load images that are above the fold — this worsens LCP instead of improving it, directly contradicting the optimization goal
- Always check for CSS/layout regressions after minification or critical CSS changes — a perfect Lighthouse score on a visually broken page is a net negative
- Never assume lab data (Lighthouse) equals real-user data (CrUX) — always cross-reference both before declaring the fix complete

## Delivery-ready self-check (run BEFORE delivering CWV report ao cliente)

Um CWV Fix Report é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1. Baseline + Target metrics CONCRETOS (3 métricas × 2 valores cada)
- [ ] LCP baseline com fonte (Lighthouse vN, data, dispositivo) + target
- [ ] INP baseline + target
- [ ] CLS baseline + target
- [ ] CrUX 28-day data citada SE disponível (ou explicit "CrUX não disponível, lab-only")
- [ ] Mobile + Desktop scores both reported (não só uma view)

❌ NOT delivery-ready: "Vamos melhorar a performance do site"
✅ Delivery-ready: "LCP mobile 4.8s (Lighthouse v11, iPhone 12, throttled 4G, 2026-05-22) → target <2.0s. CrUX 28d: LCP p75 5.2s para 87% real users (Google PSI)."

### 2. Cada fix tem code/config snippet REAL (não description)
- [ ] LCP fixes têm WordPress hook ou plugin setting concreto
- [ ] INP fixes têm script handle ou plugin specific
- [ ] CLS fixes têm CSS selector + property específico
- [ ] Pelo menos 2 fixes têm copy-paste-able code block

❌ NOT delivery-ready: "Adicionar preload da hero image"
✅ Delivery-ready:
```php
// functions.php — preload hero on home only
add_action('wp_head', function() {
    if (is_front_page()) {
        echo '<link rel="preload" as="image" href="/wp-content/uploads/2026/05/hero.webp" fetchpriority="high">';
    }
}, 1);
```

### 3. Priorização CRÍTICO/IMPORTANTE/OTIMIZAÇÃO com effort em horas
- [ ] Cada fix tem tier
- [ ] Cada fix tem effort estimate (horas)
- [ ] Cada fix tem expected metric delta (ex: "LCP -1.2s")
- [ ] Total effort + total expected impact summed

### 4. Verification protocol DOCUMENTADO
- [ ] How to measure after (Lighthouse command ou tool)
- [ ] Acceptance criteria per fix
- [ ] Regression tests (mobile + 3G throttle + CSS visual check)

### 5. Plugin/server config FULLY specified
- [ ] LiteSpeed/Autoptimize/W3TC settings se aplicável (não "ativar cache")
- [ ] PHP version target
- [ ] CDN config (Cloudflare/BunnyCDN page rules ou similar)
- [ ] Imagify/ShortPixel options se imagens

### 6. Output uses CLIENT NAME + REAL URL throughout
- [ ] Cliente nome em capa + secções
- [ ] URL específico (não <site>)
- [ ] Stack detectado (WordPress version, theme, page builder)
- [ ] Sem placeholder angle-brackets

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/métrica/diagnóstico no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via Lighthouse run, CrUX data, ou client-provided baseline
- 🟡 **assumed** — plausível com base no stack declarado, mas precisa confirm antes de entrega
- 🟢 **projection** — ganho estimado por design (não verificável até re-medição pós-fix)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs o que precisa de verify. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "LCP está em 4.2s causado por hero image sem preload. Após fix esperado LCP <2.5s. CLS a 0.24 por imagens sem dimensões."
> *(reader assume que todos os valores são medidos, que o fix já foi aplicado, e que o ganho é garantido — nada está labelled)*

✅ Delivery-ready:
> - 🔵 **verified** — LCP baseline: 4.2s (Lighthouse mobile, run 2024-01-15, 3G throttled)
> - 🔵 **verified** — CLS: 0.24 causado por 3 imagens sem `width`/`height` (DevTools confirmed)
> - 🟡 **assumed** — hero image servida via `/wp-content/uploads/hero.webp` (path não confirmado — verificar antes de aplicar preload snippet)
> - 🟡 **assumed** — LiteSpeed Cache instalado e activo (declarado pelo cliente; config não auditada directamente)
> - 🟢 **projection** — LCP esperado <2.5s após preload + WebP conversion (estimativa baseada em fixes similares; confirmar com Lighthouse pós-fix)

---

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — paths de imagens, plugins activos e versões de stack validados com acesso real ao site
- [ ] All 🔵 citations added — screenshots de Lighthouse + CrUX 28-day anexados ao relatório antes de entrega
- [ ] All 🟢 projections labeled como tal ao cliente — ganhos de LCP/INP/CLS apresentados como estimativas, não garantias, até re-medição pós-fix confirmada

## Fully-worked A-tier example (delivery-ready reference)

```markdown
---
project: Vivenda Creative Home
date: 2026-05-23
type: cwv-fix-report
url: vivendacreativehome.com
stack: WordPress 6.4 + Astra theme + Elementor + LiteSpeed Cache
---

# CWV Fix Report — Vivenda Creative Home

## Baseline (Lighthouse v11, mobile, iPhone 12, throttled 4G, 2026-05-23)

| Metric | Baseline | Target | Industry P75 |
|---|---|---|---|
| LCP mobile | **4.2s** (largest: hero IMG) | <2.0s | 2.5s |
| INP mobile | **310ms** (Elementor JS) | <200ms | 200ms |
| CLS mobile | **0.18** (web font FOUT) | <0.1 | 0.1 |
| LCP desktop | 2.8s | <1.8s | — |
| Lighthouse mobile score | **42/100** | 90+ | — |
| CrUX 28d data | LCP p75 4.6s (real users) | — | — |

## Priorization

### 🔴 CRÍTICO (effort 6h, expected delta: LCP -2.2s, INP -150ms)

**Fix 1 — Preload hero image + WebP format (LCP)** [effort 1h]
Expected: LCP 4.2s → 2.5s (-1.7s)

```php
// functions.php — Vivenda preload home hero
add_action('wp_head', function() {
    if (is_front_page()) {
        echo '<link rel="preload" as="image" '
           . 'href="/wp-content/uploads/2026/05/hero-vivenda.webp" '
           . 'fetchpriority="high" imagesrcset="...">';
    }
}, 1);
```

Plus Imagify Pro config: WebP delivery ON, lossy quality 75, lazy except above-fold.

**Fix 2 — Defer Elementor + jQuery-migrate (INP)** [effort 2h]
Expected: INP 310ms → 180ms (-130ms)

```php
// functions.php — defer non-critical scripts
add_filter('script_loader_tag', function($tag, $handle) {
    $defer = ['jquery-migrate', 'elementor-frontend', 'wp-embed', 'comment-reply'];
    if (in_array($handle, $defer)) {
        return str_replace(' src', ' defer src', $tag);
    }
    return $tag;
}, 10, 2);
```

Plus LiteSpeed: JS Defer ON, exclude jQuery core (breaks slider).

**Fix 3 — Web font preload + display swap (CLS)** [effort 2h]
Expected: CLS 0.18 → 0.05 (-0.13)

```php
// functions.php — preload primary font
add_action('wp_head', function() {
    echo '<link rel="preload" as="font" type="font/woff2" '
       . 'href="/wp-content/uploads/fonts/inter-var.woff2" crossorigin>';
}, 1);
```

CSS: `font-display: swap` no Astra customizer + `font-family` fallback nativo.

**Fix 4 — PHP 7.4 → 8.2 upgrade (TTFB)** [effort 1h]
Expected: TTFB -300ms, indirect LCP -300ms

Via Hostinger panel: PHP 8.2 + OPcache enabled. Test plugins compat: Elementor 3.21+ OK, WooCommerce 8.5+ OK, Yoast 23.x OK.

### 🟡 IMPORTANTE (effort 8h, expected delta: -200ms total)

**Fix 5 — LiteSpeed Critical CSS per template** [effort 3h]
Generate per: front-page, single-post, page-services. Expected LCP -200ms.

**Fix 6 — Cloudflare CDN free tier setup** [effort 2h]
DNS swap + page rules: cache aggressive for /wp-content/, bypass for /wp-admin/.

**Fix 7 — Defer GA4 + Meta Pixel via Partytown** [effort 3h]
Off main thread. Expected INP -50ms.

### 🟢 OTIMIZAÇÃO (effort 6h)

**Fix 8** — Switch theme builder Elementor → Bricks (long-term)
**Fix 9** — Self-host Google Fonts (avoid third-party connection)
**Fix 10** — Image dimensions audit (CLS prevention systematic)

## Total Plan

- **Total effort:** 20h dev (3 sprints de 1 semana)
- **Expected after CRÍTICO done:** LCP <2.5s, INP <200ms, CLS <0.1, Lighthouse 85+
- **Expected after IMPORTANTE done:** LCP <2.0s, INP <150ms, Lighthouse 92+

## Verification Protocol

### Per-fix acceptance
- Lighthouse mobile (incognito, throttled 4G): metric improves by ≥80% of target delta
- No CSS visual regression (compare screenshots via Percy or manual)
- Forms still submit (contact + booking)
- Slider still works (Elementor hero)

### Post-deploy monitoring
- CrUX 28d window: re-check after 14 days post-deploy
- Slack alert if Lighthouse drops below 80
- Looker Studio dashboard: LCP, INP, CLS, mobile score weekly

## Sequence (recommended deploy order)

1. **Sprint 1 (Sem 1):** Fixes 1-4 (CRÍTICO) — measure after each
2. **Sprint 2 (Sem 2):** Fixes 5-7 (IMPORTANTE) — measure after each
3. **Sprint 3 (Sem 3):** Fixes 8-10 (OTIMIZAÇÃO, optional)

Total timeline: 3 semanas para 90+ mobile Lighthouse.

## Risks

- **Elementor 3.21 + critical CSS:** known issue with above-fold critical CSS shifting. Workaround: exclude `elementor-` selectors from Critical CSS plugin.
- **PHP 8.2 + old plugins:** Yoast <23.0 deprecation warnings. Confirm current Yoast version pre-upgrade.
- **Cloudflare cache + WooCommerce sessions:** bypass /cart, /checkout, /my-account in page rules to avoid stale session bugs.
```

## Output anti-patterns

- "Vamos otimizar o LCP" sem fonte, baseline, target numbers
- Fix descritivo sem code snippet copy-paste-able
- Priorização sem effort em horas + expected delta numérico
- Verification "test on mobile" sem command ou acceptance criteria
- Plugin config "ativar cache" sem options completos
- Missing CrUX cross-reference quando data está disponível
- Output sem frontmatter (impossibilita tracking + filtering)
- Placeholder angle-brackets <site>/<client> em vez de URL/nome real
