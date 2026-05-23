---
name: dario-layout-visual
description: Layout & visual design squad -- typography, grid systems, hierarchy/composition, color theory, and modern web layout. Produces design specs for landing pages, dashboards, editorial layouts, and SaaS apps using Bringhurst, Muller-Brockmann, Gestalt, Itten/Albers, and modern CSS. Triggers on "layout", "visual design", "typography", "grid system", "color palette", "design spec", "hierarchy", "composition", "design system", "tipografia", "grelha", "cores", "layout spec".
version: 1.0.0
license: MIT
---

# DARIO Skill -- Layout & Visual Design

Produces complete visual design specifications: typography systems, grid frameworks, color palettes, hierarchy maps, and responsive layout blueprints. Five specialist masters collaborate through a Chief Router to deliver production-ready design specs for any digital product.

## When to activate

- New website or app needs a design system before development
- Landing page layout spec required
- Dashboard or SaaS interface design
- Editorial / blog / magazine layout
- Typography audit or type pairing selection
- Color palette creation or audit (accessibility, brand alignment)
- Visual hierarchy analysis ("users are not reading the page")
- Before `dario-cro` (design problems are often the root of conversion problems)
- After `dario-brand` (brand defines the constraints; layout executes them)

## Squad roster

| Agent | Domain | Key frameworks |
|---|---|---|
| **Chief Router** (Tier 0) | Triage & orchestration | Routes to the right specialist; resolves cross-domain conflicts |
| **Typography Master** | Type systems | Bringhurst's Elements, Lupton's Thinking with Type, Spiekermann's Stop Stealing Sheep |
| **Grid Systems Master** | Spatial layout | Muller-Brockmann Swiss Grid, 8pt spatial system, responsive breakpoints |
| **Hierarchy/Composition Master** | Visual structure | Gestalt principles, F-pattern/Z-pattern, CRAP (Contrast, Repetition, Alignment, Proximity) |
| **Color Theory Master** | Color systems | Itten's Art of Color, Albers' Interaction of Color, OKLCH, WCAG 2.2 |
| **Modern Web Layout Master** | CSS implementation | CSS Grid, Flexbox, container queries, fluid typography, clamp() |

## Workflow

### 1. Gather inputs

- **Project type** (landing page, dashboard, editorial, SaaS app, e-commerce, portfolio)
- **Brand guidelines** (output of `dario-brand` if available -- archetype, voice, colors)
- **Content inventory** (what needs to go on the page: text blocks, images, forms, data tables)
- **Target devices** (desktop-first, mobile-first, responsive, specific breakpoints)
- **Accessibility requirements** (WCAG AA minimum, AAA for government/healthcare)
- **Competitive references** (3-5 sites the client admires or wants to differentiate from)
- **Existing design system** (if redesign: current fonts, colors, components)

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "bringhurst typography elements vertical rhythm", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "muller brockmann grid systems swiss design", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "gestalt principles visual hierarchy CRAP design", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "itten albers color theory OKLCH WCAG contrast", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "css grid flexbox container queries fluid type", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "lupton thinking with type modular scale", collection: "dario", limit: 5)
```

### 3. Typography system (Typography Master)

#### Type selection

1. **Primary typeface** -- headlines, hero text, navigation
2. **Secondary typeface** -- body copy, descriptions, UI text
3. **Monospace** (if needed) -- code, data tables, technical content
4. **Display** (if needed) -- decorative accents, pull quotes

#### Type pairing rules

- **Contrast, not conflict** -- pair a serif with a sans-serif, or a geometric with a humanist
- **Shared skeleton** -- similar x-height, stroke weight proportions
- **Hierarchy clarity** -- the two faces must look obviously different at a glance
- **Performance** -- limit to 2-3 families, 4-6 weights total (font loading budget)

#### Modular scale (Bringhurst)

Select a ratio and generate the type scale:

| Ratio | Name | Use case |
|---|---|---|
| 1.067 | Minor second | Dense UI, dashboards |
| 1.125 | Major second | Body-heavy editorial |
| 1.200 | Minor third | General purpose (recommended default) |
| 1.250 | Major third | Marketing, landing pages |
| 1.333 | Perfect fourth | Bold headlines, hero sections |
| 1.414 | Augmented fourth | High-impact display |
| 1.618 | Golden ratio | Classical, editorial, luxury |

Generated scale (example at 1.250 with 16px base):

```
Step -2:  10px  (0.625rem)  -- caption, fine print
Step -1:  13px  (0.8125rem) -- small text, metadata
Step  0:  16px  (1rem)      -- body text (base)
Step  1:  20px  (1.25rem)   -- large body, intro
Step  2:  25px  (1.5625rem) -- h4 / subheading
Step  3:  31px  (1.9375rem) -- h3
Step  4:  39px  (2.4375rem) -- h2
Step  5:  49px  (3.0625rem) -- h1
Step  6:  61px  (3.8125rem) -- display / hero
```

#### Vertical rhythm (Bringhurst / Lupton)

- **Baseline grid**: set to body line-height (typically 24px for 16px body at 1.5)
- All spacing, padding, and margins snap to multiples of the baseline unit
- Headings: line-height tighter (1.1-1.3); body: 1.4-1.6; small text: 1.3-1.5
- Paragraph spacing: 1 baseline unit between paragraphs
- Measure (line length): 45-75 characters per line (Bringhurst ideal: 66)

#### Fluid typography (Modern Web Layout Master)

```css
/* Fluid type using clamp() */
--font-size-body: clamp(1rem, 0.5rem + 1vw, 1.125rem);
--font-size-h1:   clamp(2rem, 1rem + 3vw, 3.5rem);
--font-size-h2:   clamp(1.5rem, 0.75rem + 2vw, 2.5rem);

/* Fluid spacing */
--space-s: clamp(0.75rem, 0.5rem + 0.5vw, 1rem);
--space-m: clamp(1.5rem, 1rem + 1vw, 2rem);
--space-l: clamp(2rem, 1.5rem + 1.5vw, 3rem);
--space-xl: clamp(3rem, 2rem + 2.5vw, 5rem);
```

### 4. Grid system (Grid Systems Master)

#### 8pt spatial system (Muller-Brockmann adapted)

All spatial values are multiples of 8px:

```
4px  -- half-unit (icon padding, fine adjustments only)
8px  -- base unit
16px -- standard gap
24px -- component padding
32px -- section gap (small)
48px -- section gap (medium)
64px -- section gap (large)
96px -- major section break
128px -- hero/feature spacing
```

#### Responsive grid

| Breakpoint | Width | Columns | Gutter | Margin |
|---|---|---|---|---|
| Mobile (xs) | < 640px | 4 | 16px | 16px |
| Tablet (sm) | 640-1023px | 8 | 24px | 24px |
| Desktop (md) | 1024-1279px | 12 | 24px | 32px |
| Wide (lg) | 1280-1535px | 12 | 32px | 48px |
| Ultra-wide (xl) | >= 1536px | 12 | 32px | auto (max-width container) |

#### CSS Grid implementation

```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-gutter);
  max-width: var(--grid-max-width, 1280px);
  margin-inline: auto;
  padding-inline: var(--grid-margin);
}

/* Container queries for component-level responsiveness */
.card-grid {
  container-type: inline-size;
}

@container (min-width: 600px) {
  .card-grid__inner {
    grid-template-columns: repeat(2, 1fr);
  }
}

@container (min-width: 900px) {
  .card-grid__inner {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 5. Visual hierarchy & composition (Hierarchy/Composition Master)

#### Gestalt principles audit

For each page section, verify:

| Principle | Check | Pass/Fail |
|---|---|---|
| **Proximity** | Related items grouped; unrelated items separated | |
| **Similarity** | Same-function elements share visual treatment | |
| **Closure** | Incomplete shapes/patterns are perceivable as whole | |
| **Continuity** | Eye follows smooth lines and curves | |
| **Figure-ground** | Clear distinction between foreground content and background | |
| **Common region** | Grouped elements enclosed in shared boundary | |

#### Reading patterns

**F-pattern** (text-heavy content):
- Horizontal scan across top (headline)
- Drop down, shorter horizontal scan (subheading)
- Vertical scan down left side (scanning mode)
- Best for: blog posts, news, search results, documentation

**Z-pattern** (minimal content):
- Top-left (logo) to top-right (CTA/nav)
- Diagonal to bottom-left (supporting info)
- Bottom-left to bottom-right (final CTA)
- Best for: landing pages, hero sections, ads, simple homepages

#### CRAP principles (Robin Williams)

| Principle | Application | Common violation |
|---|---|---|
| **Contrast** | If things are different, make them VERY different | Gray on slightly-lighter-gray text |
| **Repetition** | Reuse visual elements consistently | Every section uses a different heading style |
| **Alignment** | Every element should connect visually to something else | Random left/center/right mix on same page |
| **Proximity** | Group related items; separate unrelated items | Label far from its input field |

#### Hierarchy scoring

For each page, identify and rank the visual hierarchy levels:

```
Level 1 (Primary):    What the user MUST see first (headline, hero CTA)
Level 2 (Secondary):  What they see next (subheadline, key benefits)
Level 3 (Tertiary):   Supporting content (details, features, proof)
Level 4 (Quaternary): Navigation, footer, fine print
Level 5 (Background): Decorative elements, subtle patterns
```

Each level must be distinguishable through at minimum 2 of these 4 differentiators:
- **Size** (larger = more important)
- **Weight** (bolder = more important)
- **Color** (higher contrast / brand color = more important)
- **Space** (more whitespace around = more important)

### 6. Color system (Color Theory Master)

#### Color palette generation

**60-30-10 rule:**
- 60% -- Dominant (backgrounds, large surfaces)
- 30% -- Secondary (cards, sections, navigation)
- 10% -- Accent (CTAs, highlights, interactive elements)

#### OKLCH color space (modern best practice)

```css
:root {
  /* Primary palette in OKLCH */
  --color-primary-50:  oklch(0.97 0.01 <hue>);
  --color-primary-100: oklch(0.93 0.03 <hue>);
  --color-primary-200: oklch(0.87 0.06 <hue>);
  --color-primary-300: oklch(0.78 0.10 <hue>);
  --color-primary-400: oklch(0.68 0.15 <hue>);
  --color-primary-500: oklch(0.58 0.18 <hue>);  /* base */
  --color-primary-600: oklch(0.50 0.16 <hue>);
  --color-primary-700: oklch(0.42 0.14 <hue>);
  --color-primary-800: oklch(0.35 0.11 <hue>);
  --color-primary-900: oklch(0.27 0.08 <hue>);

  /* Semantic colors */
  --color-success: oklch(0.65 0.18 145);
  --color-warning: oklch(0.78 0.15 80);
  --color-error:   oklch(0.55 0.20 25);
  --color-info:    oklch(0.60 0.15 240);

  /* Neutral scale */
  --color-neutral-50:  oklch(0.98 0.003 <hue>);
  --color-neutral-900: oklch(0.15 0.005 <hue>);
}
```

#### WCAG contrast requirements

| Element | WCAG AA | WCAG AAA |
|---|---|---|
| Normal text (< 18px) | 4.5:1 minimum | 7:1 minimum |
| Large text (>= 18px bold / 24px regular) | 3:1 minimum | 4.5:1 minimum |
| UI components / graphical objects | 3:1 minimum | 3:1 minimum |
| Focus indicators | 3:1 minimum | 3:1 minimum |

#### Color archetype alignment

Map colors to the brand archetype (from `dario-brand`):

| Archetype | Primary palette direction | Avoid |
|---|---|---|
| Innocent | Soft pastels, white, sky blue | Dark, aggressive colors |
| Explorer | Earth tones, forest green, khaki | Corporate blues, pinks |
| Sage | Deep blue, gold, white | Neon, playful colors |
| Hero | Bold red, navy, gold, black | Pastels, muted tones |
| Outlaw | Black, red, dark purple, chrome | Soft, institutional colors |
| Magician | Deep purple, gold, midnight blue | Bland, corporate neutrals |
| Regular Guy | Warm neutrals, denim blue, brown | Luxury gold, flashy colors |
| Lover | Rich burgundy, deep pink, gold, cream | Cold, clinical colors |
| Jester | Bright yellow, orange, electric blue | Muted, serious palettes |
| Caregiver | Warm blue, soft green, peach | Aggressive red, black |
| Creator | Vibrant accent on neutral base | Boring monochrome |
| Ruler | Gold, navy, black, deep burgundy | Cheap-feeling brights |

### 7. Composition tasks

#### Task: full-system

Complete design system spec: typography + grid + color + component patterns. Output includes CSS custom properties, spacing tokens, and component guidelines.

#### Task: landing-page-spec

Z-pattern hero layout, single-column scroll, strategic CTA placement, social proof blocks, FAQ accordion. Optimized for conversion (pairs with `dario-cro`).

#### Task: dashboard-spec

Dense information layout: sidebar nav, data cards, charts area, action bars. 8pt grid strict. Color-coded status indicators. Responsive collapse patterns.

#### Task: editorial-spec

Reading-optimized layout: narrow content column (max 680px), generous margins, pull quotes, image treatments (full-bleed, inset, gallery). Vertical rhythm strict.

#### Task: saas-app-spec

Application shell: top bar + sidebar + main content area. Component inventory: forms, tables, modals, toasts, empty states. Dark mode support via OKLCH lightness inversion.

## Commands

| Command | Description | Output |
|---|---|---|
| `*layout:full-system` | Complete design system specification | Typography + grid + color + components doc |
| `*layout:landing-page` | Landing page layout spec | Wireframe description + CSS grid + hierarchy map |
| `*layout:dashboard` | Dashboard layout spec | Grid layout + component inventory + responsive behavior |
| `*layout:editorial` | Editorial / blog layout spec | Reading column + type scale + image treatment |
| `*layout:saas-app` | SaaS application layout spec | App shell + component system + dark mode |
| `*type:audit` | Typography audit of existing site | Issues + recommendations + new scale |
| `*type:pair` | Type pairing recommendation | 3 pairing options with rationale |
| `*type:scale` | Generate modular type scale | Full scale with CSS custom properties |
| `*grid:spec` | Grid system specification | Breakpoints + columns + gutters + CSS |
| `*color:palette` | Generate color palette | OKLCH values + contrast checks + CSS vars |
| `*color:audit` | Audit existing palette for WCAG | Contrast matrix + failing pairs + fixes |
| `*hierarchy:audit` | Visual hierarchy analysis | Level map + Gestalt check + reading pattern |
| `*composition:crap` | CRAP principles audit | Score per principle + violations + fixes |

## Output template

```markdown
---
project: <client>
date: <YYYY-MM-DD>
type: layout-visual-spec
task: <full-system|landing-page|dashboard|editorial|saas-app>
---

# Layout & Visual Design Spec -- <Client> -- <Project>

## Design Decisions Summary
- Type system: <primary + secondary face>
- Scale ratio: <ratio name> at <base>px
- Grid: <columns> col, <gutter>px gutter, <max-width>px max
- Color: <primary hue> + <secondary> + <accent>
- Reading pattern: <F|Z>-pattern
- Accessibility: WCAG <AA|AAA>

## Typography System
### Selected typefaces
| Role | Family | Weight range | Fallback stack |
|---|---|---|---|
| Primary | ... | 400-700 | ... |
| Secondary | ... | 400-600 | ... |

### Type scale
| Step | Size | Line-height | Use |
|---|---|---|---|
| -2 | ... | ... | ... |
| ... | ... | ... | ... |

### Fluid type CSS
```css
/* paste clamp() declarations */
```

## Grid System
### Breakpoints
| Name | Range | Columns | Gutter | Margin |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

### CSS Grid implementation
```css
/* paste grid CSS */
```

## Color System
### Palette
| Token | OKLCH | Hex (fallback) | Use |
|---|---|---|---|
| primary-500 | ... | ... | ... |
| ... | ... | ... | ... |

### Contrast matrix
| Combo | Ratio | WCAG AA | WCAG AAA |
|---|---|---|---|
| ... | ... | ... | ... |

## Visual Hierarchy Map
| Level | Element | Differentiators |
|---|---|---|
| 1 | ... | size, weight, color |
| ... | ... | ... |

## Gestalt Audit
| Principle | Status | Notes |
|---|---|---|
| Proximity | ... | ... |
| ... | ... | ... |

## Composition Layout
### Section map
<section-by-section wireframe description>

### Responsive behavior
<how layout adapts across breakpoints>

## Component Patterns
<key UI components with spacing + type + color tokens>

## Dark Mode (if applicable)
<OKLCH lightness inversion strategy>

## Next Steps
1. ...
2. ...
```

## Scoring rubric -- Layout & Visual Design audit

Overall Visual Design Score (0-100):

| Dimension | Weight | Score range | Assessment |
|---|---|---|---|
| **Typography quality** | 25% | 0-25 | Scale consistency, pairing, readability, measure |
| **Grid consistency** | 20% | 0-20 | 8pt adherence, responsive behavior, alignment |
| **Color system** | 20% | 0-20 | WCAG compliance, brand alignment, 60-30-10 balance |
| **Visual hierarchy** | 20% | 0-20 | Clear levels, Gestalt compliance, reading pattern |
| **Technical implementation** | 15% | 0-15 | Modern CSS, fluid type, container queries, performance |

**Grading:**
- 85-100: Production-ready design system
- 70-84: Solid foundation, minor refinements needed
- 50-69: Significant inconsistencies, systematic rework required
- Below 50: No coherent system in place, full design system build needed

## Red flags / anti-patterns

- More than 3 typeface families loaded (performance and coherence killer)
- Font sizes chosen arbitrarily instead of from a modular scale
- Line length exceeding 80 characters on desktop (unreadable)
- Body text below 16px on any device
- No consistent spacing system (random pixel values throughout)
- Colors defined as hex without a systematic palette (ad-hoc color picking)
- Text failing WCAG AA contrast requirements (especially light gray on white)
- Centering everything on the page regardless of content type
- No visual distinction between heading levels (h2 looks like h3 looks like h4)
- Grid breaking at tablet widths (designed for desktop and mobile, forgot the middle)
- Using 15+ colors with no discernible system
- Decorative elements competing with primary content for attention
- Icon styles mixed within the same interface (outline + filled + illustrative)
- Dark mode implemented by inverting colors instead of adjusting lightness systematically
- Ignoring the brand archetype when selecting colors (luxury brand in neon green)

## Integration with other DARIO skills

| Skill | Integration point |
|---|---|
| `dario-brand` | Brand archetype, voice, and values constrain all visual decisions. Always run brand first. |
| `dario-cro` | CRO audits often reveal visual hierarchy failures. Layout fixes should be CRO-informed. |
| `dario-sales-letter` | Sales pages need specific layout patterns (headline hierarchy, proof blocks, CTA placement). |
| `dario-funnel` | Each funnel step has a different layout need (LP, thank-you page, upsell, checkout). |
| `dario-content` | Editorial content layout (blog, pillar pages) uses the editorial-spec task. |
| `dario-wp-audit` | Theme assessment includes typography, color, and layout evaluation. |
| `dario-ios-hig` | iOS apps follow Apple HIG but share type scale and color palette with the web design system. |

## Save location

`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Layout Visual Spec.md`

## Critical rules

- Never select typefaces based on aesthetics alone without checking x-height compatibility, weight range availability, and web performance (WOFF2 file size) -- a beautiful font that loads in 800ms defeats its own purpose
- Never skip the WCAG contrast check -- visual design that excludes users with low vision is not professional design, it is decoration
- Always start with the content, then design the layout -- designing empty containers and then cramming content in produces layouts that fight the content instead of serving it
- Never use pixel values directly in CSS without mapping them to design tokens -- hardcoded pixels make systematic changes impossible and guarantee inconsistency
- Always test the grid at every breakpoint, including tablet landscape and small desktop -- the 1024px zone is where most grid systems break
- Never apply the 60-30-10 color rule by counting CSS declarations -- it refers to visual surface area as perceived by the user
- Always define a dark mode strategy at system design time, not as an afterthought -- retrofitting dark mode onto an existing color system requires rebuilding the entire palette

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Typography system completo

- [ ] Tipo primário + secundário nomeados com fornecedor (Google Fonts, Adobe Fonts, etc.)
- [ ] Modular scale com ratio explícito e mínimo 6 steps calculados em px + rem
- [ ] Baseline grid definida (valor em px) e line-heights por nível documentados
- [ ] Measure (caracteres/linha) especificada para body copy
- ❌ NOT delivery-ready: "Use uma fonte serif para títulos e uma sans-serif para corpo"
- ✅ Delivery-ready: "Fraunces (Google Fonts, weights 400/700) para headings + Inter (weights 400/500/600) para body; escala 1.250 com base 16px; baseline 24px; measure 62ch para body"

---

### Gate 2 — Grid system especificado para todos os breakpoints

- [ ] Número de colunas definido por breakpoint (mobile / tablet / desktop)
- [ ] Gutter width e margin/padding externos especificados em px ou rem por breakpoint
- [ ] Max-width do container declarado
- [ ] Spatial system (8pt ou outro) documentado com lista de tokens de espaçamento
- ❌ NOT delivery-ready: "Grid responsivo com colunas para mobile e desktop"
- ✅ Delivery-ready: "4 col / 16px gutter @ <640px — 8 col / 24px gutter @ 640-1024px — 12 col / 32px gutter @ >1024px; max-width 1280px; spatial tokens: 8/16/24/32/48/64/96px"

---

### Gate 3 — Color system com tokens e validação WCAG

- [ ] Paleta nomeada com valores HEX + OKLCH para todos os tokens
- [ ] Pares de contraste críticos testados (texto/fundo, CTA/fundo) com ratio declarado
- [ ] Status WCAG AA/AAA confirmado para cada par
- [ ] Dark mode ou modo alternativo indicado (mesmo que "fora de scope")
- ❌ NOT delivery-ready: "Azul primário com bom contraste no fundo branco"
- ✅ Delivery-ready: "`--color-brand-primary: #1A4FD6` (oklch(45% 0.22 264)); sobre `#FFFFFF`: ratio 7.3:1 → WCAG AAA ✓; CTA hover `#1340B0` sobre branco: 9.1:1 ✓"

---

### Gate 4 — Hierarchy map e composição documentados

- [ ] Hierarquia visual mapeada para cada template/página (H1→H2→body→caption)
- [ ] Padrão de leitura identificado (F-pattern / Z-pattern / leitura centrada) e justificado
- [ ] Pelo menos 2 princípios Gestalt aplicados com exemplo concreto na página
- [ ] CRAP checklist (Contrast / Repetition / Alignment / Proximity) passada explicitamente
- ❌ NOT delivery-ready: "Hierarquia clara com bom contraste entre secções"
- ✅ Delivery-ready: "Hero → Z-pattern; CTA alinhado ao ponto de saída do olho (bottom-right); Proximidade: form fields agrupados com gap 8px vs 32px entre grupos; Repetição: mesmo border-radius 6px em todos os cards"

---

### Gate 5 — CSS tokens e implementação prontos para handoff

- [ ] Todas as variáveis CSS declaradas com `--nome-token: valor`
- [ ] `clamp()` fluid typography com min/preferred/max para H1, H2, body mínimo
- [ ] Layout principal especificado em CSS Grid ou Flexbox com código ou pseudocódigo
- [ ] Container queries indicados onde relevante (componentes reutilizáveis)
- ❌ NOT delivery-ready: "Tipografia fluida que escala entre mobile e desktop"
- ✅ Delivery-ready: `` `--font-size-h1: clamp(2rem, 1rem + 3vw, 3.5rem)` `` com breakpoints min 320px / max 1280px documentados; grid: `grid-template-columns: repeat(12, 1fr)` com named areas para hero, aside, main

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets

- [ ] Nenhum placeholder do tipo `[CLIENT_NAME]`, `<cor_da_marca>`, `[inserir fonte aqui]`
- [ ] Nomes de fontes, cores, e breakpoints são os reais do projeto, não exemplos genéricos
- [ ] Referências competitivas mencionadas são as do briefing do cliente, não exemplos de template
- [ ] Todas as medidas (px, rem, vw) são valores numéricos concretos, não "X" ou "Y"
- ❌ NOT delivery-ready: "Usar `[PRIMARY_COLOR]` com contraste adequado sobre fundo claro"
- ✅ Delivery-ready: "Cuidai usa `#2D6A4F` (verde floresta) sobre `#F8FAF9`; ratio 5.8:1 → WCAG AA ✓ para texto ≥18px"

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Design Spec — Cuidai Landing Page v1.0
*Gerado por dario-layout-visual | 2025-01-15*

---

## Typography System

**Primary:** Fraunces (Google Fonts) — Display / Hero / H1-H2
Weights carregados: 400 (Regular), 600 (SemiBold), 700 (Bold)

**Secondary:** Plus Jakarta Sans (Google Fonts) — H3-H6, Body, UI
Weights carregados: 400 (Regular), 500 (Medium), 600 (SemiBold)

**Ratio:** 1.250 (Major Third) | **Base:** 16px | **Baseline grid:** 24px

| Token              | px  | rem    | Uso                        |
|--------------------|-----|--------|----------------------------|
| `--text-caption`   | 10  | 0.625  | Fine print, disclaimers    |
| `--text-small`     | 13  | 0.8125 | Metadata, timestamps       |
| `--text-body`      | 16  | 1      | Corpo principal            |
| `--text-lead`      | 20  | 1.25   | Intro paragraphs           |
| `--text-h4`        | 25  | 1.5625 | Card headings              |
| `--text-h3`        | 31  | 1.9375 | Secção headings            |
| `--text-h2`        | 39  | 2.4375 | Page sections              |
| `--text-h1`        | 49  | 3.0625 | Hero headline              |
| `--text-display`   | 61  | 3.8125 | Acima do fold (desktop)    |

**Fluid typography (clamp):**
```css
--font-size-body:    clamp(1rem, 0.875rem + 0.25vw, 1.125rem);
--font-size-h2:      clamp(1.5625rem, 1rem + 2vw, 2.4375rem);
--font-size-h1:      clamp(2.4375rem, 1.5rem + 3vw, 3.8125rem);
```

**Measure:** 62ch máximo em body copy; 44ch em colunas laterais
**Line-heights:** Display 1.1 · H1-H2 1.2 · H3-H4 1.3 · Body 1.55 · Caption 1.4

---

## Grid System

| Breakpoint     | Colunas | Gutter | Margin | Max-width  |
|----------------|---------|--------|--------|------------|
| Mobile <640px  | 4       | 16px   | 20px   | 100%       |
| Tablet 640-1024px | 8    | 24px   | 32px   | 100%       |
| Desktop >1024px | 12     | 32px   | 48px   | 1280px     |

**Spatial tokens (8pt system):**
```css
--space-2:   4px;   /* micro — icon padding interno */
--space-4:   8px;   /* xs — gap entre form fields */
--space-8:  16px;   /* s  — padding de card */
--space-12: 24px;   /* m  — gap entre cards */
--space-16: 32px;   /* l  — secção padding vertical */
--space-24: 48px;   /* xl — entre secções major */
--space-32: 64px;   /* 2xl — hero padding */
--space-48: 96px;   /* 3xl — between page sections */
```

---

## Color System

```css
/* Brand */
--color-brand-primary:   #2D6A4F;  /* oklch(42% 0.12 158) */
--color-brand-light:     #74C69D;  /* oklch(73% 0.10 158) */
--color-brand-dark:      #1B4332;  /* oklch(28% 0.09 158) */

/* Neutrals */
--color-surface:         #F8FAF9;
--color-surface-raised:  #FFFFFF;
--color-border:          #D8E5E0;
--color-text-primary:    #1A2E25;
--color-text-secondary:  #4A6358;
--color-text-muted:      #7A9A8A;

/* Feedback */
--color-success:         #40916C;
--color-warning:         #E9C46A;
--color-error:           #C1121F;
```

**Contraste WCAG 2.2 (pares críticos):**
| Par                                     | Ratio | Status  |
|-----------------------------------------|-------|---------|
| `--text-primary` (#1A2E25) / `--surface` (#F8FAF9) | 14.2:1 | AAA ✓ |
| `--brand-primary` (#2D6A4F) / `#FFFFFF` | 5.8:1  | AA ✓ (texto ≥18px) |
| CTA texto branco / `--brand-primary`    | 5.8:1  | AA ✓   |
| `--text-muted` / `--surface`            | 3.9:1  | AA ✓ (texto ≥18px) |

---

## Visual Hierarchy — Landing Page

**Padrão de leitura:** Z-pattern (landing de conversão; conteúdo escasso acima do fold)

**Gestalt aplicado:**
- **Proximidade:** Testemunhos agrupados em cards com gap interno 16px vs gap entre cards 32px
- **Similaridade:** Todos os CTAs com `border-radius: 8px`, `font-weight: 600`, cor `--brand-primary`
- **Continuidade:** Linha-guia vertical alinhada ao canto esquerdo das colunas de texto cria fluxo entre secções

**CRAP checklist — Hero section:**
- ✅ Contrast: H1 (61px Fraunces 700 #1A2E25) vs body (16px Jakarta 400 #4A6358) — diferença óbvia
- ✅ Repetition: espaçamento 48px consistente entre todas as secções major
- ✅ Alignment: todos os elementos alinhados a grid column 1 (left-edge) ou centrados em 12 cols
- ✅ Proximity: CTA button a ≤16px do headline benefício imediato

---

## CSS Layout (Hero section)

```css
.hero {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: auto;
  gap: var(--space-8);
  padding-block: var(--space-32);
  max-width: 1280px;
  margin-inline: auto;
}

.hero__copy    { grid-column: 1 / 7; }
.hero__visual  { grid-column: 7 / 13; }

@media (max-width: 1024px) {
  .hero__copy,
  .hero__visual { grid-column: 1 / -1; }
}
```
```

---

## Output anti-patterns

- Fontes mencionadas sem peso, fornecedor ou fallback stack ("usar uma sans-serif moderna")
- Paleta com nomes de cor subjetivos sem valores HEX/OKLCH ("verde natural da marca")
- Modular scale listada só em px sem tokens CSS `--` prontos para implementação
- Contraste afirmado como "bom" sem ratio numérico e status WCAG explícito
- Grid descrito em prosa ("layout de 3 colunas") sem colunas/gutter/margin por breakpoint
- Spacing arbitrário fora do spatial system documentado (ex: margin-top: 37px)
- Hierarquia descrita sem padrão de leitura identificado (F/Z/centrado) ou Gestalt nomeado
- `clamp()` com valores placeholder sem min/max de viewport declarados
- Spec gerada para "um cliente de wellness" em vez do cliente real do briefing
- Design tokens misturados com valores hardcoded no mesmo spec (inconsistência de handoff)
