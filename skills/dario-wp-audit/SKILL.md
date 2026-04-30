---
name: dario-wp-audit
description: Holistic WordPress + WooCommerce audit covering performance, security, SEO, content, plugin bloat, theme health, checkout flow, accessibility and PT legal compliance. Triggers on "wordpress audit", "woocommerce audit", "wp audit", "auditoria wordpress".
license: MIT
---

# DARIO Skill — WordPress + Woo Audit

The agency's most repetitive deliverable. Runs a 9-category audit that covers every angle that matters on a production WordPress/Woo site.

## When to activate

- User asks for a WordPress or WooCommerce audit
- New client onboarding with WP/Woo stack
- Before any major WP migration or redesign
- After suspicious traffic drop, ranking loss, or performance regression

## Workflow

### 1. Gather site info
- URL (production), staging URL if exists
- WP version, theme, page builder
- Hosting (shared, VPS, managed)
- Plugin list (or access to `wp-admin/plugins.php`)
- Current KPI baseline (traffic, conversions, CWV)

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "wordpress audit checklist performance security", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "woocommerce checkout friction audit", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "core web vitals inp wordpress", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "rgpd cookies consent mode v2 wordpress", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "wcag eaa wordpress accessibility", collection: "dario", limit: 5)
```

### 3. Run the 9 audit categories

#### 1. Performance / Core Web Vitals
- PageSpeed Insights mobile + desktop (p75 CrUX data)
- LCP, INP, CLS per top template
- Total JS, CSS, image weight
- Image format (WebP/AVIF adoption)
- Critical rendering path
- Cache plugin (LiteSpeed, WP Rocket, W3TC) config
- CDN usage
- Render-blocking resources

#### 2. Security
- WP core, themes, plugins updated
- SSL/TLS config (SSL Labs grade)
- `wp-login.php` brute-force protection
- 2FA enabled on admins
- File integrity monitoring (Wordfence/Sucuri)
- Readable `/wp-config.php`?
- Debug mode disabled in prod
- `xmlrpc.php` disabled
- Admin usernames (avoid `admin`)
- Backup strategy (frequency, off-site, tested)

#### 3. SEO — Technical
- `robots.txt` correct
- XML sitemap (submitted to GSC)
- Canonicals correct
- Schema markup (Organization, BreadcrumbList, Article, Product, LocalBusiness)
- Crawl errors (GSC)
- Index coverage
- Duplicate content (cannibalization)
- hreflang if multi-lingual
- HTTPS redirect, trailing slash consistency
- URL structure

#### 4. SEO — Content / E-E-A-T
- Title + meta description per page
- H1/H2 hierarchy
- Content depth vs competitors
- Author pages + credentials
- Fresh content cadence
- Internal linking
- E-E-A-T signals (author bio, reviewer, sources, update dates)
- AI Overviews citability

#### 5. Conversion (CRO)
- Hero clarity + CTA prominence
- Single 1:1 attention ratio per LP
- Trust signals (testimonials, logos, certifications)
- Friction in forms / checkout
- Mobile UX
- Cart abandonment (Woo) — payment methods, guest checkout, shipping costs upfront

#### 6. Plugins / Theme health
- Plugin count (more than 30 is a smell)
- Abandoned plugins (>6 months no update)
- Duplicate-function plugins (two caches, two SEO plugins)
- Theme child setup
- Custom code in theme vs mu-plugins
- Premium licenses valid

#### 7. Accessibility (EAA 2025 — obrigatório)
- WCAG 2.2 AA checklist (axe + WAVE scan)
- Keyboard-only navigation
- Contrast ratios
- Alt text coverage
- Form labels + aria-describedby errors
- No accessibility overlay (UserWay/AccessiBe = red flag)
- Declaração de acessibilidade pública
- Mobile target size ≥24×24 CSS px

#### 8. Legal / Compliance PT
- Política de Privacidade presente + atualizada
- Política de Cookies + banner CNPD-compliant
- Livro de Reclamações eletrónico
- Identificação jurídica no rodapé (NIF, CRC, morada)
- Termos e Condições
- Botão "encomendar com obrigação de pagar" (Woo)
- Consent Mode v2 em GA4
- FB Pixel / scripts NÃO disparam antes de consent

#### 9. WooCommerce (se aplicável)
- Checkout flow (steps, fields, mandatory vs optional)
- Payment methods (MBWay, Multibanco PT, credit card, PayPal)
- Shipping methods + costs upfront
- Tax config (IVA PT)
- Product schema + images
- Cart/checkout mobile UX
- Order emails (design + deliverability)
- Stock management
- Refund flow
- GDPR "right to delete account + orders"

### 4. Score each category
Use 0-10 with justification. Aggregate weighted score.

| Category | Weight | Score | Notes |
|---|---|---|---|
| Performance | 15% | X/10 | |
| Security | 15% | X/10 | |
| Technical SEO | 12% | X/10 | |
| Content / E-E-A-T | 10% | X/10 | |
| CRO | 12% | X/10 | |
| Plugins / Theme | 8% | X/10 | |
| Accessibility | 10% | X/10 | |
| Legal Compliance | 10% | X/10 | |
| WooCommerce | 8% | X/10 | |
| **Total** | **100%** | **X/10** | |

### 5. Tier issues
- **TIER 0 — Blocker:** site should not launch / is in legal risk / serious security hole
- **TIER 1 — Critical (1-2 semanas):** measurable impact on revenue/SEO/compliance
- **TIER 2 — Important (1 mês):** should be fixed but not blocking
- **TIER 3 — Nice-to-have:** long-term polish

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: audit
stack: wordpress<+woocommerce>
score_global: X.X/10
---

# Auditoria WordPress — <Client Name>

## Resumo Executivo
Score global **X.X/10**. TIER 0 blockers: **N**. Quick wins: **M**.

Principais findings:
- ...

## Scores por Dimensão
<table>

## TIER 0 — Bloqueadores
1. ... (file:line if aplicável)

## TIER 1 — Críticos (1-2 semanas)
1. ...

## TIER 2 — Importantes (1 mês)
1. ...

## TIER 3 — Otimizações
1. ...

## Dados em Falta (a pedir ao cliente)
- ...

## Roadmap de Remediação
M1: TIER 0 → ...
M2: TIER 1 → ...
M3: TIER 2 → ...
M4: TIER 3 + monitoring → ...

## KPIs Baseline vs Target
| KPI | Baseline | Target 30d | Target 90d |
|---|---|---|---|
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Auditoria WordPress.md`

## Skill interactions
- Consulta `spec/pt-legal-compliance` automaticamente
- Consulta `spec/accessibility-eu-accessibility-act` automaticamente
- Consulta `spec/server-side-analytics-consent-mode-v2` automaticamente
- Pode encadear com `dario-obsidian-save` para save automático
- Pode ser chamado por `dario-client-onboard` como subtask

## Red flags / anti-patterns a reportar
- Accessibility overlay (UserWay/AccessiBe) instalado
- Cookie banner sem botão "Rejeitar" visível igualmente ao "Aceitar"
- GA4 a disparar antes de consent
- Plugin count >40
- Duplicate plugins (e.g. 2 caches, 2 SEO, 2 backup)
- Tema premium não atualizado há >6 meses
- Plugin builders a conviver (Elementor + Divi + Gutenberg custom)
- Sem staging environment
- Admin com username `admin`

## Red Flags
- Never skip the security category (category 2) even if the client only asked about performance — an insecure site with fast LCP is still a liability waiting to be exploited
- Never ignore PT legal compliance checks (Livro de Reclamacoes, NIF no footer, Consent Mode v2) — non-compliance carries real fines and the agency shares the risk
- Always run the audit on mobile separately from desktop — a site that scores 90 desktop and 45 mobile is failing for the majority of real users
- Never deliver an audit without tier-classified findings (TIER 0-3) — an untiered list of 40 issues gives the client no sense of priority and leads to inaction
- Always check plugin count and duplicate-function plugins — bloated plugin stacks are the single most common cause of poor CWV scores on WordPress sites
