---
name: builder-design-system
description: >
  Gera design systems completos e executaveis: design tokens, color palette, typography scale,
  spacing system, Tailwind CSS config, component specs. Output e CODIGO, nao template.
  Use quando: design system, tokens, palette, typography, tailwind config, brand visual system,
  cores, fontes, espacamento, criar identidade visual de sistema.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Design System Generator

## Proposito

Gerar um design system EXECUTAVEL — nao um documento, mas codigo real que funciona:
- `tailwind.config.ts` com tokens customizados
- `globals.css` com CSS variables
- Palette completa (primary, secondary, neutral, semantic)
- Typography scale (fluid, responsive)
- Spacing system (4pt ou 8pt grid)
- Component specs (buttons, inputs, cards, badges)

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/builder-design-system [marca]` | Design system completo para uma marca |
| `/builder-design-system minimal` | Sistema minimo (palette + typo + spacing) |
| `/builder-design-system from-brand [brand-doc]` | Extrair tokens de um brand positioning existente |

## Workflow

### Phase 1: INPUTS
Recolher ou inferir:
1. **Brand archetype** (se existe dario-brand output, usar)
2. **Industry** (tech, restaurant, luxury, health, etc.)
3. **Mood** (professional, playful, bold, minimal, warm)
4. **Target audience** (B2B enterprise, consumer young, premium, etc.)

### Phase 2: COLOR PALETTE

Gerar palette completa com rationale:

```typescript
// Design Tokens — Colors
const colors = {
  // Primary — the brand's main color (CTA, links, active states)
  primary: {
    50:  '#eff6ff',  // backgrounds
    100: '#dbeafe',  // hover backgrounds
    200: '#bfdbfe',  // borders
    300: '#93c5fd',  // icons inactive
    400: '#60a5fa',  // icons active
    500: '#3b82f6',  // DEFAULT — buttons, links
    600: '#2563eb',  // hover buttons
    700: '#1d4ed8',  // active/pressed
    800: '#1e40af',  // headings
    900: '#1e3a8a',  // text on light
    950: '#172554',  // darkest
  },
  // Neutral — text, backgrounds, borders
  neutral: {
    50:  '#fafafa',  // page background
    100: '#f5f5f5',  // card background
    200: '#e5e5e5',  // borders
    300: '#d4d4d4',  // disabled
    400: '#a3a3a3',  // placeholder text
    500: '#737373',  // secondary text
    600: '#525252',  // body text
    700: '#404040',  // headings
    800: '#262626',  // strong headings
    900: '#171717',  // maximum contrast
    950: '#0a0a0a',  // inverse backgrounds
  },
  // Semantic
  success: { light: '#ecfdf5', DEFAULT: '#10b981', dark: '#065f46' },
  warning: { light: '#fffbeb', DEFAULT: '#f59e0b', dark: '#92400e' },
  error:   { light: '#fef2f2', DEFAULT: '#ef4444', dark: '#991b1b' },
  info:    { light: '#eff6ff', DEFAULT: '#3b82f6', dark: '#1e40af' },
}
```

WCAG AA contrast check obrigatorio: text-on-bg >= 4.5:1, large text >= 3:1.

### Phase 3: TYPOGRAPHY

```typescript
const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
    heading: ['Cal Sans', 'Inter', 'sans-serif'],
    mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
  },
  fontSize: {
    // Fluid scale using clamp()
    'xs':   'clamp(0.75rem, 0.7rem + 0.25vw, 0.8rem)',     // 12-13px
    'sm':   'clamp(0.8rem, 0.75rem + 0.3vw, 0.875rem)',     // 13-14px
    'base': 'clamp(0.9rem, 0.85rem + 0.3vw, 1rem)',         // 14-16px
    'lg':   'clamp(1.05rem, 0.95rem + 0.5vw, 1.125rem)',    // 17-18px
    'xl':   'clamp(1.2rem, 1rem + 0.8vw, 1.25rem)',         // 19-20px
    '2xl':  'clamp(1.4rem, 1.1rem + 1.2vw, 1.5rem)',        // 22-24px
    '3xl':  'clamp(1.7rem, 1.3rem + 1.5vw, 1.875rem)',      // 27-30px
    '4xl':  'clamp(2rem, 1.5rem + 2vw, 2.25rem)',           // 32-36px
    '5xl':  'clamp(2.5rem, 1.8rem + 3vw, 3rem)',            // 40-48px
    '6xl':  'clamp(3rem, 2rem + 4vw, 3.75rem)',             // 48-60px
  },
  lineHeight: {
    tight: '1.2',    // headings
    snug: '1.35',    // subheadings
    normal: '1.5',   // body
    relaxed: '1.65', // long text
  },
}
```

### Phase 4: SPACING & LAYOUT

```typescript
const spacing = {
  // 4pt grid system
  px: '1px',
  0.5: '2px',
  1: '4px',
  1.5: '6px',
  2: '8px',
  3: '12px',
  4: '16px',
  5: '20px',
  6: '24px',
  8: '32px',
  10: '40px',
  12: '48px',
  16: '64px',
  20: '80px',
  24: '96px',
  32: '128px',
}

const layout = {
  container: { center: true, padding: '1rem' },
  maxWidth: {
    content: '680px',   // blog, long text
    page: '1200px',     // page width
    wide: '1400px',     // dashboard
  },
  borderRadius: {
    sm: '4px',
    DEFAULT: '8px',
    md: '12px',
    lg: '16px',
    xl: '24px',
    full: '9999px',
  },
}
```

### Phase 5: OUTPUT — tailwind.config.ts

Gerar ficheiro completo e funcional:

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{ts,tsx,mdx}', './app/**/*.{ts,tsx,mdx}'],
  theme: {
    extend: {
      colors: { /* Phase 2 output */ },
      fontFamily: { /* Phase 3 output */ },
      fontSize: { /* Phase 3 output */ },
      spacing: { /* Phase 4 output */ },
      borderRadius: { /* Phase 4 output */ },
      maxWidth: { /* Phase 4 output */ },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}

export default config
```

### Phase 6: OUTPUT — globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 9%;
    --primary: 221 83% 53%;
    --primary-foreground: 210 40% 98%;
    /* ... all tokens as CSS vars */
  }
  .dark {
    --background: 0 0% 4%;
    --foreground: 0 0% 95%;
    /* ... dark mode overrides */
  }
}
```

### Phase 7: COMPONENT SPECS

Para cada componente core, gerar spec:
- **Button:** sizes (sm/md/lg), variants (primary/secondary/ghost/destructive), states, icons
- **Input:** sizes, states (default/focus/error/disabled), label, helper text
- **Card:** padding, border, shadow, header/body/footer
- **Badge:** colors (semantic), sizes, dot variant
- **Avatar:** sizes, fallback, group overlap

## Output

O deliverable MINIMO e:
1. `tailwind.config.ts` (funcional, copy-paste ready)
2. `globals.css` (CSS variables + base styles)
3. `DESIGN_TOKENS.md` (documentacao human-readable)
4. Component specs (pelo menos Button + Input + Card)

## Red Flags
- Gerar tokens sem verificar WCAG contrast — NUNCA
- Palette sem neutral scale — inutilizavel
- Typography sem fluid/responsive — quebra em mobile
- Spacing sem sistema (valores random) — inconsistencia visual
- Tailwind config que nao compila — testar SEMPRE

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Color Palette é completa e WCAG-válida
- [ ] Primary scale tem 11 steps (50→950) com hex values reais, não placeholders
- [ ] Neutral, semantic (success/warning/error/info) incluídos com light/DEFAULT/dark
- [ ] Contrast ratio primary-500 sobre branco verificado: ≥ 4.5:1 para body text
- [ ] Rationale de cada cor reflecte o brand/industry do cliente (ex: saúde → verde, fintech → azul)

❌ NOT delivery-ready: `primary: '#YOURCOLOR'` ou `// insert brand color here`
✅ Delivery-ready: `primary: { 500: '#1a6b4a', 600: '#15593d' }` — verde saúde Cuidai, contrast 5.8:1 vs white

---

### Gate 2 — Typography Scale usa fluid clamp() e fontes específicas da marca
- [ ] Todos os 10 tamanhos (xs→6xl) usam `clamp()` com min/max em px explícito no comentário
- [ ] `fontFamily.sans` e `fontFamily.heading` têm fontes REAIS (não "YourFont"), justificadas pelo posicionamento
- [ ] `lineHeight` valores definidos para tight/snug/normal/relaxed
- [ ] Fonte heading ≠ fonte body (excepção: marca deliberadamente minimalista — documentado)

❌ NOT delivery-ready: `fontFamily: { sans: ['YOUR_FONT', 'sans-serif'] }`
✅ Delivery-ready: `fontFamily: { heading: ['Sora', 'Inter', 'sans-serif'] }` — Sora para Tributario.AI: legibilidade técnica + modernidade

---

### Gate 3 — `tailwind.config.ts` é executável sem edição
- [ ] `content` paths cobrem `./src/**/*.{ts,tsx,mdx}` e `./app/**/*.{ts,tsx,mdx}`
- [ ] Todos os tokens de Phase 2–4 estão populados dentro do `extend` (sem `/* Phase X output */` no ficheiro final)
- [ ] Plugins `@tailwindcss/typography` e `@tailwindcss/forms` incluídos
- [ ] Export default `config` correcto e tipagem `Config` importada

❌ NOT delivery-ready: `colors: { /* Phase 2 output */ }` no ficheiro entregue
✅ Delivery-ready: cores completamente expandidas, `npx tailwindcss build` executa sem erro

---

### Gate 4 — `globals.css` tem CSS variables completas + dark mode
- [ ] Todas as cores primary/neutral/semantic mapeadas como CSS vars HSL em `:root`
- [ ] `.dark {}` block presente com overrides de background, foreground, e primary
- [ ] `@tailwind base/components/utilities` nas primeiras 3 linhas
- [ ] Nenhuma var fica como `/* TODO */` ou com valor fictício `0 0% 0%` sem intenção

❌ NOT delivery-ready: `.dark { /* dark mode overrides */ }`
✅ Delivery-ready: `.dark { --background: 222 47% 7%; --foreground: 210 40% 97%; --primary: 221 83% 65%; }`

---

### Gate 5 — Component Specs cobrem os 4 componentes core com estados
- [ ] **Button** tem 4 variants (primary/secondary/ghost/destructive) × 3 sizes com classes Tailwind concretas
- [ ] **Input** tem estados default/focus/error/disabled com ring/border colours específicos
- [ ] **Card** e **Badge** incluídos com pelo menos variant + padding + radius
- [ ] Estados hover/focus/disabled usam tokens do sistema (não cores hardcoded como `bg-blue-500`)

❌ NOT delivery-ready: `Button primary: "use primary color for background"`
✅ Delivery-ready: `Button primary md: "bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded text-sm font-medium"`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero angle-brackets
- [ ] Nome da marca aparece no comentário do ficheiro (`// Design System — Cuidai v1.0`)
- [ ] Nenhum `<brand-name>`, `<primary-color>`, `<font-choice>` visível no output final
- [ ] Rationale de cor/tipografia menciona explicitamente o posicionamento do cliente
- [ ] Spacing grid (4pt vs 8pt) escolhido com justificação baseada no tipo de produto (app vs site editorial)

❌ NOT delivery-ready: `// Design tokens for <CLIENT_NAME>`
✅ Delivery-ready: `// Design tokens — SAQUEI • Fintech BNPL PT • Sistema v1.0 • Janeiro 2025`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
// tailwind.config.ts — Design System SAQUEI • Fintech BNPL • v1.0

import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/**/*.{ts,tsx,mdx}',
    './app/**/*.{ts,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Primary — Índigo SAQUEI: confiança fintech + modernidade BNPL
        primary: {
          50:  '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1', // DEFAULT — CTAs, links — contrast 4.6:1 vs white
          600: '#4f46e5', // hover buttons — contrast 6.1:1 vs white
          700: '#4338ca', // active/pressed
          800: '#3730a3', // headings escuros
          900: '#312e81', // texto sobre fundos claros
          950: '#1e1b4b', // darkest
        },
        // Accent — Esmeralda: confirmações, sucesso de pagamento
        accent: {
          400: '#34d399',
          500: '#10b981',
          600: '#059669',
        },
        // Neutral — base do produto
        neutral: {
          50:  '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
          950: '#0a0a0a',
        },
        // Semantic
        success: { light: '#ecfdf5', DEFAULT: '#10b981', dark: '#065f46' },
        warning: { light: '#fffbeb', DEFAULT: '#f59e0b', dark: '#92400e' },
        error:   { light: '#fef2f2', DEFAULT: '#ef4444', dark: '#991b1b' },
        info:    { light: '#eef2ff', DEFAULT: '#6366f1', dark: '#3730a3' },
      },
      fontFamily: {
        // Sora: moderna, geométrica, legível em tabelas de crédito
        heading: ['Sora', 'Inter', 'system-ui', 'sans-serif'],
        // Inter: máxima legibilidade para montantes, datas, condições BNPL
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      fontSize: {
        // Fluid scale — 4pt grid — mobile-first fintech app
        'xs':   ['clamp(0.75rem, 0.7rem + 0.25vw, 0.8rem)',   { lineHeight: '1.5' }],  // 12–13px
        'sm':   ['clamp(0.8rem, 0.75rem + 0.3vw, 0.875rem)',  { lineHeight: '1.5' }],  // 13–14px
        'base': ['clamp(0.875rem, 0.85rem + 0.3vw, 1rem)',    { lineHeight: '1.5' }],  // 14–16px
        'lg':   ['clamp(1.05rem, 0.95rem + 0.5vw, 1.125rem)', { lineHeight: '1.35' }], // 17–18px
        'xl':   ['clamp(1.2rem, 1rem + 0.8vw, 1.25rem)',      { lineHeight: '1.35' }], // 19–20px
        '2xl':  ['clamp(1.4rem, 1.1rem + 1.2vw, 1.5rem)',     { lineHeight: '1.2' }],  // 22–24px
        '3xl':  ['clamp(1.7rem, 1.3rem + 1.5vw, 1.875rem)',   { lineHeight: '1.2' }],  // 27–30px
        '4xl':  ['clamp(2rem, 1.5rem + 2vw, 2.25rem)',        { lineHeight: '1.2' }],  // 32–36px
        '5xl':  ['clamp(2.5rem, 1.8rem + 3vw, 3rem)',         { lineHeight: '1.1' }],  // 40–48px
        '6xl':  ['clamp(3rem, 2rem + 4vw, 3.75rem)',          { lineHeight: '1.1' }],  // 48–60px
      },
      spacing: {
        // 4pt grid — app móvel SAQUEI: density alta, touch targets >= 44px
        px: '1px', 0.5: '2px', 1: '4px', 1.5: '6px',
        2: '8px',  3: '12px',  4: '16px', 5: '20px',
        6: '24px', 8: '32px',  10: '40px', 11: '44px',
        12: '48px', 16: '64px', 20: '80px', 24: '96px',
      },
      borderRadius: {
        sm: '4px', DEFAULT: '8px', md: '12px',
        lg: '16px', xl: '24px', full: '9999px',
      },
      maxWidth: {
        content: '680px', page: '1200px', wide: '1400px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}

export default config

// ─── Component Specs — SAQUEI ────────────────────────────────────────────────
//
// BUTTON
//   primary-lg:  bg-primary-500 hover:bg-primary-600 active:bg-primary-700
//                text-white font-semibold text-base px-6 py-3 rounded-lg
//                min-h-[44px] focus:ring-2 focus:ring-primary-300
//   primary-md:  bg-primary-500 hover:bg-primary-600 px-4 py-2 rounded text-sm
//   ghost-md:    border border-primary-500 text-primary-600
//                hover:bg-primary-50 px-4 py-2 rounded text-sm
//   destructive: bg-error hover:bg-error/90 text-white px-4 py-2 rounded text-sm
//
// INPUT
//   default:  border border-neutral-200 rounded px-3 py-2 text-sm text-neutral-800
//             placeholder:text-neutral-400 bg-white
//   focus:    ring-2 ring-primary-200 border-primary-500 outline-none
//   error:    border-error ring-2 ring-error/20 + mensagem text-error text-xs mt-1
//   disabled: bg-neutral-100 text-neutral-400 cursor-not-allowed
//
// CARD (ex: resumo de prestação BNPL)
//   bg-white rounded-xl shadow-sm border border-neutral-100 p-6
//   hover: shadow-md transition-shadow duration-200
//
// BADGE (estado do pagamento)
//   pago:      bg-success/10 text-success-dark text-xs font-medium px-2 py-0.5 rounded-full
//   pendente:  bg-warning/10 text-warning-dark text-xs font-medium px-2 py-0.5 rounded-full
//   em-atraso: bg-error/10   text-error-dark   text-xs font-medium px-2 py-0.5 rounded-full
```

---

## Output anti-patterns

- Entregar `tailwind.config.ts` com `/* Phase 2 output */` ainda no lugar dos tokens — o ficheiro não compila e não é executável
- Escolher fontes genéricas ("use a clean sans-serif") sem nomear família concreta e sem link Google Fonts / npm package
- Omitir dark mode no `globals.css` alegando "o cliente decide depois" — o sistema fica incompleto por omissão
- Definir component specs em prosa ("usar cor primária no botão") em vez de classes Tailwind concretas e copiáveis
- Usar `bg-blue-500` ou `text-gray-700` hardcoded nos componentes em vez dos tokens do sistema recém-criado
- Gerar uma palette sem verificar contraste — entregar primary-400 como cor de texto sem confirmar ratio WCAG AA
- Produzir spacing scale sem declarar se é 4pt ou 8pt grid, nem justificar face ao tipo de produto
- Incluir `<brand-name>` ou `<primary-hex>` no output final — zero angle-brackets tolerados em entrega
