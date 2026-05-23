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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Código funciona ao `npm run dev` sem erros

- [ ] Todos os imports de componentes resolvem para ficheiros que existem (`@/components/sections/hero`, etc.)
- [ ] Nenhum placeholder `TODO`, `...`, `{/* add content */}` no JSX final
- [ ] Props tipadas com TypeScript — sem `any` explícito
- [ ] `tailwind.config` inclui `darkMode: 'class'` se dark mode foi usado

❌ NOT delivery-ready: `export function Pricing() { return <div>Pricing goes here</div> }`
✅ Delivery-ready: Componente `Pricing` completo com 3 tiers (Starter €0/Pro €29/Enterprise €99), badges, feature lists, e botões CTA funcionais com `href="#contact"`

---

### Gate 2 — Todas as secções do template estão presentes e populadas

- [ ] `app/page.tsx` importa e renderiza TODAS as secções acordadas com o cliente (hero, features, pricing, etc.)
- [ ] Cada secção tem headline, corpo e CTA — não está vazia nem tem um único parágrafo genérico
- [ ] Secção FAQ tem mínimo 5 perguntas reais do domínio do produto
- [ ] Footer tem links reais: Política de Privacidade, Termos, redes sociais (mesmo que `href="#"` marcado como `// TODO: update`)

❌ NOT delivery-ready: Hero com headline "O Seu Produto Aqui" e subheadline "Descrição do produto."
✅ Delivery-ready: Hero com headline "Gere relatórios fiscais em 3 minutos" + subheadline "Tributario.AI analisa os teus documentos automaticamente e entrega ao TOC em PDF pronto a submeter."

---

### Gate 3 — Copy é específico ao cliente, não genérico

- [ ] Headline do Hero: máximo 8 palavras, nomeia benefício concreto (não "A Melhor Solução Para Si")
- [ ] Features: cada feature tem título (benefício) + 2 linhas com mecanismo + resultado mensurável
- [ ] Números de social proof são reais ou plausíveis para o estágio do negócio (não "10.000+ clientes" para uma startup em pré-launch)
- [ ] CTAs usam verbos de acção específicos ao funil: "Reservar mesa", "Pedir demo", "Entrar na waitlist" — não "Submeter" ou "Clique aqui"

❌ NOT delivery-ready: Features com títulos "Feature 1", "Feature 2", "Feature 3" e descrições de 1 linha genérica
✅ Delivery-ready: Feature "Recupera IVA automaticamente — O motor de OCR lê os recibos e calcula o IVA dedutível em segundos. Poupes em média €340/mês."

---

### Gate 4 — Responsive e acessibilidade básica validados mentalmente

- [ ] Layout não quebra a 320px (mobile): flex-col em vez de flex-row, padding reduzido com `px-4`
- [ ] Imagens e ícones têm `alt` text descritivo (não `alt=""` em conteúdo significativo)
- [ ] Botões e links têm `focus-visible` styles presentes
- [ ] Contraste de cor: texto sobre fundo primário é legível (não cinza claro sobre branco)
- [ ] `sm:`, `md:`, `lg:` breakpoints usados consistentemente em todo o ficheiro

❌ NOT delivery-ready: Grid de features com `grid-cols-4` sem breakpoint — colapsa em mobile
✅ Delivery-ready: `className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4"`

---

### Gate 5 — Estrutura de ficheiros entregue completa

- [ ] `app/page.tsx` + cada componente de secção num ficheiro separado em `components/sections/`
- [ ] Se existe design system do cliente, tokens de cor usados (`primary-600`, não `blue-600` hardcoded)
- [ ] Dark mode: classes `dark:` presentes em backgrounds, textos e borders — não só no wrapper
- [ ] Animações e hovers presentes mas subtis: `transition-colors`, `hover:scale-105` — não `animate-spin` em elementos de conteúdo

❌ NOT delivery-ready: Todo o código num único bloco em `page.tsx` com 400 linhas
✅ Delivery-ready: `components/sections/hero.tsx`, `features.tsx`, `pricing.tsx`, `testimonials.tsx`, `faq.tsx`, `cta.tsx`, `footer.tsx` — cada um auto-contido

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets

- [ ] Zero ocorrências de `[PRODUTO]`, `<client-name>`, `YOUR_BRAND`, `Insert headline here` no código entregue
- [ ] Nome do produto/empresa aparece no `<title>`, navbar logo, e footer copyright
- [ ] Cores primárias são as do cliente (hex ou token), não o default `blue-600` do Tailwind
- [ ] Testimonials têm nomes reais (ou personas nomeadas acordadas), cargo e empresa — não "João S., CEO"

❌ NOT delivery-ready: `<title>Landing Page | [Nome da Empresa]</title>` e copyright `© 2024 [EMPRESA]`
✅ Delivery-ready: `<title>Cuidai — Gestão de cuidadores em casa, simples</title>` e `© 2025 Cuidai, Lda.`

---

## Fully-worked A-tier example (delivery-ready reference)

```tsx
// components/sections/hero.tsx — Cuidai (plataforma de gestão de cuidadores domiciliários)

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-white dark:bg-neutral-950">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
        <div className="mx-auto max-w-2xl text-center">

          {/* Badge */}
          <div className="mb-6 inline-flex items-center rounded-full border border-teal-200 bg-teal-50 px-4 py-1.5 text-sm text-teal-700 dark:border-teal-800 dark:bg-teal-950 dark:text-teal-300">
            <span className="mr-2">🏠</span>
            Novo: Relatórios de turno em PDF automáticos
          </div>

          {/* Headline */}
          <h1 className="text-4xl font-bold tracking-tight text-neutral-900 dark:text-white sm:text-5xl lg:text-6xl">
            Gere cuidadores{' '}
            <span className="text-teal-600 dark:text-teal-400">
              sem folhas de Excel
            </span>
          </h1>

          {/* Subheadline */}
          <p className="mt-6 text-lg leading-relaxed text-neutral-600 dark:text-neutral-400 sm:text-xl">
            A Cuidai organiza turnos, regista ocorrências e comunica com famílias —
            tudo numa app usada por 120+ IPSS e agências em Portugal.
          </p>

          {/* CTAs */}
          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <a
              href="#pricing"
              className="rounded-lg bg-teal-600 px-8 py-3 text-base font-semibold text-white shadow-sm hover:bg-teal-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-600 transition-colors"
            >
              Experimentar 30 dias grátis
            </a>
            <a
              href="#demo"
              className="flex items-center gap-2 text-base font-semibold text-neutral-700 dark:text-neutral-300 hover:text-teal-600 transition-colors"
            >
              Ver demo de 3 min <span aria-hidden="true">→</span>
            </a>
          </div>

          {/* Social proof */}
          <p className="mt-8 text-sm text-neutral-500 dark:text-neutral-400">
            Usado por 120+ organizações · 4.8★ na App Store · Sem cartão de crédito
          </p>

          {/* Logos */}
          <div className="mt-10 flex flex-wrap items-center justify-center gap-6 opacity-50 grayscale">
            <img src="/logos/ipss-lisboa.svg" alt="IPSS Lisboa" className="h-8" />
            <img src="/logos/santa-casa.svg" alt="Santa Casa" className="h-8" />
            <img src="/logos/misericordia-porto.svg" alt="Misericórdia Porto" className="h-8" />
          </div>
        </div>
      </div>
    </section>
  )
}
```

```tsx
// components/sections/pricing.tsx — Cuidai

const tiers = [
  {
    name: 'Essencial',
    price: '€0',
    period: 'para sempre',
    description: 'Para equipas até 5 cuidadores.',
    features: ['5 cuidadores', 'Agenda semanal', 'App mobile iOS/Android', 'Suporte por email'],
    cta: 'Começar grátis',
    href: '/signup',
    highlight: false,
  },
  {
    name: 'Profissional',
    price: '€49',
    period: '/mês',
    description: 'Para agências e IPSS em crescimento.',
    features: ['Cuidadores ilimitados', 'Relatórios PDF automáticos', 'Comunicação com famílias', 'Integração com SISS.GOV', 'Suporte prioritário'],
    cta: 'Começar 30 dias grátis',
    href: '/signup?plan=pro',
    highlight: true,
  },
  {
    name: 'Enterprise',
    price: 'Sob consulta',
    period: '',
    description: 'Para redes de cuidados com múltiplas unidades.',
    features: ['Multi-unidade', 'SSO / Active Directory', 'SLA 99.9%', 'Onboarding dedicado', 'API access'],
    cta: 'Falar com vendas',
    href: '/contact',
    highlight: false,
  },
]

export function Pricing() {
  return (
    <section id="pricing" className="bg-neutral-50 dark:bg-neutral-900 py-20 lg:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold text-neutral-900 dark:text-white sm:text-4xl">
            Preços transparentes, sem surpresas
          </h2>
          <p className="mt-4 text-lg text-neutral-600 dark:text-neutral-400">
            Cancela quando quiseres. Migração assistida incluída em todos os planos.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {tiers.map((tier) => (
            <div
              key={tier.name}
              className={`rounded-2xl p-8 ${
                tier.highlight
                  ? 'bg-teal-600 text-white ring-2 ring-teal-600'
                  : 'bg-white dark:bg-neutral-800 ring-1 ring-neutral-200 dark:ring-neutral-700'
              }`}
            >
              <h3 className={`text-lg font-semibold ${tier.highlight ? 'text-white' : 'text-neutral-900 dark:text-white'}`}>
                {tier.name}
              </h3>
              <p className="mt-4 flex items-baseline gap-1">
                <span className="text-4xl font-bold">{tier.price}</span>
                <span className={`text-sm ${tier.highlight ? 'text-teal-100' : 'text-neutral-500'}`}>{tier.period}</span>
              </p>
              <p className={`mt-2 text-sm ${tier.highlight ? 'text-teal-100' : 'text-neutral-600 dark:text-neutral-400'}`}>
                {tier.description}
              </p>
              <ul className="mt-8 space-y-3">
                {tier.features.map((f) => (
                  <li key={f} className="flex items-center gap-3 text-sm">
                    <span aria-hidden="true">✓</span> {f}
                  </li>
                ))}
              </ul>
              <a
                href={tier.href}
                className={`mt-8 block rounded-lg px-6 py-3 text-center text-sm font-semibold transition-colors ${
                  tier.highlight
                    ? 'bg-white text-teal-600 hover:bg-teal-50'
                    : 'bg-teal-600 text-white hover:bg-teal-500'
                }`}
              >
                {tier.cta}
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

## Output anti-patterns

- Entregar `page.tsx` com todo o código inline em 500+ linhas em vez de componentes separados por ficheiro
- Usar `blue-600` hardcoded quando o cliente tem brand colors definidas (deve usar `primary-600` ou o token específico)
- Headlines com mais de 8 palavras que descrevem features ("Plataforma completa de gestão com relatórios e integração") em vez de benefícios ("Gere cuidadores sem folhas de Excel")
- Social proof inventada desproporcionada ao estágio do cliente ("Usado por 50.000+ empresas" para produto em pré-launch)
- CTAs passivos: "Saiba mais", "Clique aqui", "Submeter formulário" em vez de verbos de acção orientados ao resultado
- Grid de features `grid-cols-3` sem breakpoints `sm:` e `lg:` — colapsa em mobile e fica ilegível
- Ficheiros entregues com `<angle-bracket-placeholders>` tipo `[NOME_EMPRESA]` ou `YOUR_PRIMARY_COLOR`
- FAQ com perguntas genéricas ("O que é o vosso produto?") que não reflectem as objecções reais do segmento do cliente
- Testimonials com "J.S., Gestor" sem empresa, foto placeholder, ou citações de 3 palavras sem substância
- Dark mode aplicado só no wrapper `<main>` mas não nas secções internas — cria backgrounds mistos luz/escuro
