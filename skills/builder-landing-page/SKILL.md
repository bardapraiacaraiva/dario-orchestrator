---
name: builder-landing-page
description: >
  Gera landing pages COMPLETAS e FUNCIONAIS em React/Next.js + Tailwind. Output e codigo
  production-ready, nao wireframe. Hero, features, pricing, testimonials, CTA, footer.
  Use quando: landing page, pagina de vendas, homepage, pagina de produto, squeeze page,
  criar site, construir pagina, gerar frontend, pagina de captura.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Landing Page Generator

## Proposito

Gerar uma landing page COMPLETA e FUNCIONAL — nao um mockup, nao um wireframe.
O output e codigo React/Next.js + Tailwind que funciona quando faz `npm run dev`.

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/builder-landing-page [produto]` | Landing page completa |
| `/builder-landing-page saas [produto]` | Template SaaS (hero + features + pricing + FAQ) |
| `/builder-landing-page agency [nome]` | Template agencia (portfolio + servicos + CTA) |
| `/builder-landing-page restaurant [nome]` | Template restaurante (menu + reservas + galeria) |
| `/builder-landing-page event [nome]` | Template evento (lineup + tickets + countdown) |
| `/builder-landing-page minimal [produto]` | Pagina minima (hero + CTA only) |

## Workflow

### Phase 1: CONTEXT
1. Que produto/servico? (nome, descricao, sector)
2. Existe brand positioning? (usar cores, tom, archetype do dario-brand)
3. Existe design system? (usar tokens do builder-design-system)
4. Qual o objectivo? (leads, vendas, waitlist, downloads)
5. Que seccoes? (hero, features, pricing, testimonials, FAQ, CTA, footer)

### Phase 2: STRUCTURE (sections)

Cada pagina tem seccoes. Default sections por tipo:

**SaaS Landing:**
```
1. Navbar (logo + nav + CTA button)
2. Hero (headline + subheadline + CTA + visual)
3. Social Proof (logos + "trusted by X companies")
4. Features (3-4 features com icones + descricao)
5. How it Works (3 steps)
6. Pricing (3 tiers — starter/pro/enterprise)
7. Testimonials (2-3 quotes com foto + nome)
8. FAQ (5-8 perguntas)
9. Final CTA (headline + button)
10. Footer (links + legal + social)
```

**Agency Landing:**
```
1. Navbar
2. Hero (statement + reel/portfolio preview)
3. Services (grid 3-4 services)
4. Portfolio (gallery grid)
5. Process (timeline 4 steps)
6. Testimonials
7. Team (optional)
8. CTA (contact/schedule)
9. Footer
```

### Phase 3: COPY

Para cada seccao, gerar copy:
- **Headline:** Max 8 palavras. Beneficio, nao feature.
- **Subheadline:** 1-2 frases. Expande o headline com prova ou mecanismo.
- **CTA:** Verbo de accao. "Comecar gratis", nao "Submeter".
- **Features:** Titulo (beneficio) + 2 linhas (mecanismo + resultado)

Se existe output de dario-brand ou dario-offer, usar como base.

### Phase 4: GENERATE CODE

Output em **React + Tailwind** (Next.js App Router compatible):

```tsx
// app/page.tsx
import { Hero } from '@/components/sections/hero'
import { Features } from '@/components/sections/features'
import { Pricing } from '@/components/sections/pricing'
import { Testimonials } from '@/components/sections/testimonials'
import { FAQ } from '@/components/sections/faq'
import { CTA } from '@/components/sections/cta'
import { Footer } from '@/components/sections/footer'

export default function LandingPage() {
  return (
    <main>
      <Hero />
      <Features />
      <Pricing />
      <Testimonials />
      <FAQ />
      <CTA />
      <Footer />
    </main>
  )
}
```

Cada componente de seccao e um ficheiro separado, completo, com:
- TypeScript tipado
- Tailwind classes (responsive: sm/md/lg)
- Semantic HTML (section, article, nav, footer)
- Acessibilidade basica (aria-labels, alt text, focus states)
- Dark mode support (dark: classes)
- Animacoes subtis (transition, hover effects)

### Phase 5: HERO SECTION (template core)

```tsx
// components/sections/hero.tsx
export function Hero() {
  return (
    <section className="relative overflow-hidden bg-white dark:bg-neutral-950">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
        <div className="mx-auto max-w-2xl text-center">
          {/* Badge */}
          <div className="mb-6 inline-flex items-center rounded-full border border-primary-200 bg-primary-50 px-4 py-1.5 text-sm text-primary-700 dark:border-primary-800 dark:bg-primary-950 dark:text-primary-300">
            <span className="mr-2">🚀</span>
            Novo: Feature mais recente
          </div>

          {/* Headline */}
          <h1 className="text-4xl font-bold tracking-tight text-neutral-900 dark:text-white sm:text-5xl lg:text-6xl">
            Headline com{' '}
            <span className="text-primary-600 dark:text-primary-400">
              beneficio principal
            </span>
          </h1>

          {/* Subheadline */}
          <p className="mt-6 text-lg leading-relaxed text-neutral-600 dark:text-neutral-400 sm:text-xl">
            Uma ou duas frases que expandem o headline. Explica o mecanismo
            ou oferece prova social. Maximo 25 palavras.
          </p>

          {/* CTAs */}
          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <a href="#pricing" className="rounded-lg bg-primary-600 px-8 py-3 text-base font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 transition-colors">
              Comecar gratis
            </a>
            <a href="#demo" className="flex items-center gap-2 text-base font-semibold text-neutral-700 dark:text-neutral-300 hover:text-primary-600 transition-colors">
              Ver demo <span aria-hidden="true">→</span>
            </a>
          </div>

          {/* Social proof */}
          <p className="mt-8 text-sm text-neutral-500">
            Usado por 500+ empresas em Portugal
          </p>
        </div>
      </div>
    </section>
  )
}
```

### Phase 6: RESPONSIVE CHECK

Antes de entregar, validar mentalmente:
- [ ] Mobile (320px): stack vertical, texto legivel, CTA full-width
- [ ] Tablet (768px): 2 colunas onde faz sentido
- [ ] Desktop (1200px): layout completo, max-width respeitado
- [ ] Hover states em todos os links/botoes
- [ ] Focus states para acessibilidade
- [ ] Dark mode funcional

## Output Deliverable

1. `app/page.tsx` — pagina principal com imports
2. `components/sections/*.tsx` — cada seccao como componente
3. `components/ui/*.tsx` — componentes reutilizaveis (Button, Badge, Card)
4. `tailwind.config.ts` — se nao existir de builder-design-system
5. `LANDING_PAGE.md` — documentacao de seccoes e copy

## Integration

| Depende de | Para que |
|---|---|
| `dario-brand` | Tom de voz, archetype, cores |
| `dario-offer` | Headline, pricing, bonuses |
| `builder-design-system` | Tokens, palette, typography |
| `builder-nextjs-app` | Scaffold do projecto |

## Red Flags
- Landing page sem CTA acima do fold — perde 60% das conversoes
- Texto generico ("solucao inovadora") — zero diferenciacao
- Sem responsive — 60% do trafego PT e mobile
- Sem dark mode — expectativa standard em 2026
- Features sem beneficios (listar funcionalidades em vez de resultados)
- Pricing escondido — frustra o visitante
- Mais de 10 seccoes — fatiga de scroll
