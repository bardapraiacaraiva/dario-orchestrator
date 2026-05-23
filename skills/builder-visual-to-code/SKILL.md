---
name: builder-visual-to-code
description: >
  Converte screenshots, wireframes, mockups e imagens de design em codigo React/Tailwind
  funcional. Usa visao multimodal para interpretar layout, cores, tipografia, espacamento.
  Inspirado em screenshot-to-code (71K stars). O elo entre wireframe e codigo production.
  Use quando: imagem para codigo, screenshot to code, mockup to react, design to code,
  converter imagem em pagina, replicar design.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Visual to Code (screenshot-to-code pattern)

## Proposito
Aceitar qualquer INPUT VISUAL (screenshot, wireframe, mockup, foto de whiteboard) e produzir
codigo React + Tailwind FUNCIONAL. O elo que faltava entre design e implementacao.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-visual-to-code [imagem]` | Converter imagem em React + Tailwind |
| `/builder-visual-to-code refine` | Iterar sobre output anterior |
| `/builder-visual-to-code section [imagem]` | Converter apenas uma seccao |

## Workflow

### 1. Analyze Visual Input
Quando recebe uma imagem, analisar:
- **Layout:** Grid? Flexbox? Columns? Stack? Sidebar + content?
- **Hierarchy:** O que e H1? O que e body? Onde esta o CTA?
- **Colors:** Extrair palette dominante (primary, bg, text, accent)
- **Typography:** Tamanho relativo dos textos, peso, font family
- **Spacing:** Padding, margin, gaps entre elementos
- **Components:** Identificar buttons, cards, inputs, badges, navbars
- **Responsive hints:** Se mostra mobile vs desktop layout

### 2. Map to React Components
Cada elemento visual mapeado para componente shadcn/ui ou custom:
```
[Navbar com logo + links + CTA]  → <Navbar />
[Hero com headline + CTA]        → <Hero />
[Grid 3 colunas com icones]      → <Features />
[Card com preco e botao]         → <PricingCard />
[Footer com links e social]      → <Footer />
```

### 3. Generate Production Code
Output: React + TypeScript + Tailwind CSS completo
- Semantic HTML (section, article, nav, main, footer)
- Responsive (mobile-first com sm:/md:/lg: breakpoints)
- Accessible (alt text, aria-labels, focus states)
- Dark mode support (dark: classes)
- Cores extraidas como CSS variables (nao hardcoded hex)

### 4. Fidelity Levels
| Level | O que replica | O que adapta |
|---|---|---|
| **Pixel-perfect** | Layout, cores, fonts exactas | Nada — replica 1:1 |
| **Structural** (default) | Layout e hierarquia | Cores e fonts mapeadas para design system |
| **Conceptual** | Estrutura geral | Tudo adaptado ao design system do projecto |

## Integration
| Depende de | Para que |
|---|---|
| `builder-design-system` | Mapear cores extraidas para tokens do projecto |
| `builder-react-components` | Reutilizar componentes existentes |
| `builder-landing-page` | Estrutura de seccoes como referencia |

## Inspired by
- **abi/screenshot-to-code** (71K stars) — Pipeline imagem → vision LLM → HTML/React
- **wandb/openui** (20K stars) — Text → live UI iteration
- **nexu-io/open-design** (30K stars) — Design systems as prompting context

## Red Flags
- Gerar sem semantic HTML — inacessivel
- Cores hardcoded em vez de CSS variables — impossivel tematizar
- Ignorar responsive — 60% mobile em PT
- Copiar texto da imagem como Lorem Ipsum — usar copy real ou placeholder claro

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Visual analysis documentada antes do código
- [ ] Layout identificado explicitamente (ex: "Sidebar 280px + content flex-1", "Grid 3-col com gap-8")
- [ ] Palette extraída com valores concretos (ex: primary `#1E40AF`, bg `#F8FAFC`, text `#0F172A`)
- [ ] Componentes identificados por nome antes de gerar código (Navbar, Hero, PricingCard…)
- [ ] Hierarquia tipográfica mapeada (H1 ≈ 48px bold, H2 ≈ 32px semibold, body ≈ 16px)
- ❌ NOT delivery-ready: "cores azuladas, texto grande no topo, alguns cards"
- ✅ Delivery-ready: "Hero: bg `#0F172A`, headline `text-5xl font-bold text-white`, subheadline `text-lg text-slate-400`, CTA button `bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg`"

### Gate 2 — Código React estruturalmente correto
- [ ] Cada secção é um componente nomeado (`<HeroSection />`, `<PricingCard />`, não tudo num `<div>` monolítico)
- [ ] Semantic HTML usado: `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>` — não apenas `<div>`
- [ ] TypeScript: props com interfaces declaradas, sem `any`
- [ ] Imports corretos (shadcn/ui, lucide-react, tailwind classes — sem imports fantasma)
- ❌ NOT delivery-ready: `export default function Page() { return <div><div><div>...` sem semântica
- ✅ Delivery-ready: `export function PricingSection() { return <section aria-labelledby="pricing-heading"><h2 id="pricing-heading"...`

### Gate 3 — Tailwind fiel ao visual, sem hardcode
- [ ] Cores definidas como CSS variables em `tailwind.config` ou `globals.css`, não hex inline
- [ ] Spacing reproduz o visual: gaps, padding, margin identificados na análise (não valores arbitrários)
- [ ] Classes responsive presentes: pelo menos `sm:` e `lg:` breakpoints onde o layout muda
- [ ] Dark mode com `dark:` classes se o design original mostrar ou o projecto usar
- ❌ NOT delivery-ready: `style={{ backgroundColor: '#1E40AF', padding: '24px' }}` inline styles
- ✅ Delivery-ready: `className="bg-brand-primary py-6 lg:py-12 dark:bg-brand-primary-dark"`

### Gate 4 — Fidelity level declarado e respeitado
- [ ] Fidelity level explicitamente escolhido e comunicado ao cliente (Pixel-perfect / Structural / Conceptual)
- [ ] Se Structural (default): cores mapeadas para tokens do design system existente do projecto
- [ ] Se Pixel-perfect: cada medida retirada da imagem justificada (ex: "hero height ≈ 600px → `min-h-[600px]`")
- [ ] Copy do visual replicado fielmente — sem Lorem Ipsum silencioso; se ilegível, placeholder `[COPY: headline aqui]` visível
- ❌ NOT delivery-ready: mistura Lorem Ipsum com copy real sem avisar
- ✅ Delivery-ready: texto da imagem transcrito; onde ilegível: `{/* TODO: copy — ilegível na imagem */}` e `[Headline principal]` no JSX

### Gate 5 — Acessibilidade mínima não negociável
- [ ] Imagens com `alt` descritivo (não `alt=""` em imagens de conteúdo)
- [ ] Botões com texto acessível ou `aria-label` (não apenas ícone sem label)
- [ ] Inputs com `<label>` associado ou `aria-label`
- [ ] Focus states visíveis (Tailwind `focus:ring-2 focus:ring-brand-primary`)
- ❌ NOT delivery-ready: `<button><img src="icon.svg" /></button>` sem aria-label
- ✅ Delivery-ready: `<button aria-label="Abrir menu de navegação"><Menu className="h-5 w-5" /></button>`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Nome do projecto/cliente no código (ex: `CuidaiApp`, `SaqueiDashboard`, `LusocontaLanding`)
- [ ] Copy real ou placeholders explícitos com contexto (não `<YOUR_HEADLINE>` ou `<LOGO_URL>`)
- [ ] Cores nomeadas com o cliente em mente: `cuidai-green`, `saquei-orange` — não `primary-color`
- [ ] Nenhum `TODO: replace with real data` sem especificar o quê
- ❌ NOT delivery-ready: `<h1>Your Amazing Headline Here</h1>`, `color: '<BRAND_COLOR>'`
- ✅ Delivery-ready: `<h1>Cuide de quem ama, onde estiver.</h1>` com `bg-cuidai-500` definido em config

---

## Fully-worked A-tier example (delivery-ready reference)

```tsx
// Visual analysis (feita antes de gerar código):
// Layout: Hero full-width + Features 3-col + CTA strip — desktop first
// Palette: bg #0A0F1E (navy), primary #22C55E (green), text #F1F5F9, muted #94A3B8
// Typography: H1 ~56px bold, H2 ~36px semibold, body 16px regular
// Fidelity: Structural — cores mapeadas para tokens Cuidai existentes

// tailwind.config.ts (excerpt)
// colors: { cuidai: { 500: '#22C55E', 900: '#0A0F1E' }, slate: { ... } }

// app/landing/page.tsx
import { HeroSection } from '@/components/landing/HeroSection'
import { FeaturesSection } from '@/components/landing/FeaturesSection'
import { CtaStrip } from '@/components/landing/CtaStrip'

export default function LandingPage() {
  return (
    <main className="bg-cuidai-900 text-slate-100">
      <HeroSection />
      <FeaturesSection />
      <CtaStrip />
    </main>
  )
}

// components/landing/HeroSection.tsx
import { Button } from '@/components/ui/button'
import { ArrowRight, Shield } from 'lucide-react'

export function HeroSection() {
  return (
    <section
      className="relative min-h-[640px] flex items-center px-6 lg:px-24 py-20"
      aria-labelledby="hero-heading"
    >
      <div className="max-w-2xl">
        <span className="inline-flex items-center gap-2 text-sm text-cuidai-500
                         font-medium mb-6 bg-cuidai-500/10 px-3 py-1 rounded-full">
          <Shield className="h-4 w-4" aria-hidden="true" />
          Certificado pela ACSS
        </span>

        <h1
          id="hero-heading"
          className="text-5xl lg:text-6xl font-bold text-white leading-tight mb-6"
        >
          Cuide de quem ama,{' '}
          <span className="text-cuidai-500">onde estiver.</span>
        </h1>

        <p className="text-lg text-slate-400 mb-10 max-w-xl">
          Gerencie cuidadores, histórico médico e alertas da sua família
          numa plataforma construída para cuidadores portugueses.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <Button
            size="lg"
            className="bg-cuidai-500 hover:bg-cuidai-600 text-white
                       focus:ring-2 focus:ring-cuidai-500 focus:ring-offset-2
                       focus:ring-offset-cuidai-900"
          >
            Começar grátis
            <ArrowRight className="ml-2 h-5 w-5" aria-hidden="true" />
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="border-slate-600 text-slate-300 hover:bg-slate-800"
          >
            Ver demonstração
          </Button>
        </div>
      </div>
    </section>
  )
}

// components/landing/FeaturesSection.tsx
interface Feature {
  icon: React.ElementType
  title: string
  description: string
}

const features: Feature[] = [
  {
    icon: Shield,
    title: 'Gestão de cuidadores',
    description: 'Perfis verificados, horários e relatórios em tempo real.',
  },
  {
    icon: Shield,
    title: 'Histórico médico centralizado',
    description: 'Medicação, consultas e alertas acessíveis a toda a família.',
  },
  {
    icon: Shield,
    title: 'Alertas inteligentes',
    description: 'Notificações proativas antes de qualquer urgência.',
  },
]

export function FeaturesSection() {
  return (
    <section
      className="px-6 lg:px-24 py-20 border-t border-slate-800"
      aria-labelledby="features-heading"
    >
      <h2
        id="features-heading"
        className="text-3xl lg:text-4xl font-semibold text-white text-center mb-14"
      >
        Tudo o que um cuidador precisa
      </h2>

      <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 list-none">
        {features.map((feature) => (
          <li
            key={feature.title}
            className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700
                       hover:border-cuidai-500/50 transition-colors duration-200"
          >
            <feature.icon
              className="h-8 w-8 text-cuidai-500 mb-4"
              aria-hidden="true"
            />
            <h3 className="text-lg font-semibold text-white mb-2">
              {feature.title}
            </h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              {feature.description}
            </p>
          </li>
        ))}
      </ul>
    </section>
  )
}
```

---

## Output anti-patterns

- **Visual analysis pulada** — código gerado directamente da imagem sem documentar palette, layout e componentes identificados; resulta em Tailwind arbitrário desligado do design real
- **Monobloco JSX** — toda a página num único componente de 300 linhas sem separação por secção; impossível reutilizar ou iterar
- **Cores hardcoded** — `bg-[#1E40AF]` ou `style={{ color: '#22C55E' }}` espalhados; bloqueia tematização e viola o design system do cliente
- **Lorem Ipsum silencioso** — texto placeholder inserido sem aviso onde a imagem tinha copy legível; entrega código que parece incompleto ao cliente
- **Zero responsive** — layout desktop replicado sem breakpoints; falha em 60%+ do tráfego mobile português
- **Semantic HTML ignorado** — `<div onClick>` em vez de `<button>`, ausência de `<nav>`/`<main>`/`<footer>`; inacessível e penalizado em SEO
- **Fidelity level não declarado** — cliente não sabe se recebe pixel-perfect ou adaptação conceptual; expectativas desalinhadas
- **Imports fantasma** — `import { Tooltip } from '@/components/ui/tooltip'` sem o componente existir no projecto; código que não compila na primeira run
- **Props sem interface TypeScript** — `function Card({ title, desc, price })` sem tipos; falha silenciosa em runtime e sem autocomplete
- **Angle-brackets no output final** — `<CLIENT_NAME>`, `<LOGO_URL>`, `<PRIMARY_COLOR>` entregues ao cliente sem substituição
