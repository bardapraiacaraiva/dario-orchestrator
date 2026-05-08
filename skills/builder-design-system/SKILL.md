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
