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
