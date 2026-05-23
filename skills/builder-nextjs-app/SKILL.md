---
name: builder-nextjs-app
description: >
  Scaffold completo de aplicacao Next.js App Router com TypeScript, Tailwind, shadcn/ui.
  Gera estrutura de directórios, configurações, layouts, páginas, componentes base.
  Use quando: criar app, scaffold next, nova aplicacao, iniciar projecto, montar estrutura,
  criar SaaS, criar dashboard, criar website.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Next.js App Scaffold

## Proposito

Gerar a ESTRUTURA COMPLETA de uma app Next.js — nao boilerplate generico,
mas uma app configurada para o projecto especifico com:
- App Router (app/ directory)
- TypeScript strict mode
- Tailwind CSS com design tokens do projeto
- shadcn/ui components
- Layout system (root + nested)
- Error boundaries + loading states
- Metadata + SEO base

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/builder-nextjs-app [nome]` | Scaffold completo |
| `/builder-nextjs-app landing [nome]` | Optimizado para landing page |
| `/builder-nextjs-app saas [nome]` | SaaS com auth + dashboard + billing |
| `/builder-nextjs-app blog [nome]` | Blog com MDX + content layer |

## Output: Estrutura de Ficheiros

```
[project-name]/
├── app/
│   ├── layout.tsx          ← Root layout (fonts, metadata, providers)
│   ├── page.tsx            ← Homepage
│   ├── loading.tsx         ← Global loading state
│   ├── error.tsx           ← Global error boundary
│   ├── not-found.tsx       ← 404 page
│   ├── globals.css         ← Tailwind + CSS variables
│   ├── (marketing)/        ← Marketing pages group
│   │   ├── page.tsx        ← Landing page
│   │   ├── pricing/page.tsx
│   │   └── about/page.tsx
│   ├── (app)/              ← App pages (authenticated)
│   │   ├── layout.tsx      ← Dashboard layout (sidebar)
│   │   ├── dashboard/page.tsx
│   │   └── settings/page.tsx
│   └── api/                ← API routes
│       └── health/route.ts
├── components/
│   ├── ui/                 ← shadcn/ui base components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── badge.tsx
│   ├── sections/           ← Page sections
│   │   ├── hero.tsx
│   │   ├── features.tsx
│   │   ├── pricing.tsx
│   │   └── footer.tsx
│   └── layout/             ← Layout components
│       ├── navbar.tsx
│       ├── sidebar.tsx
│       └── mobile-nav.tsx
├── lib/
│   ├── utils.ts            ← cn() helper + utilities
│   └── constants.ts        ← Site config, navigation, etc.
├── public/
│   ├── favicon.ico
│   └── og-image.png
├── tailwind.config.ts      ← From builder-design-system
├── next.config.ts
├── tsconfig.json
├── package.json
└── .env.example
```

## Root Layout Template

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })

export const metadata: Metadata = {
  title: { default: 'Project Name', template: '%s | Project Name' },
  description: 'Project description for SEO',
  openGraph: { title: 'Project Name', description: '...', type: 'website' },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt" className={inter.variable} suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
```

## Package.json Base

```json
{
  "name": "project-name",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/typography": "^0.5.0"
  }
}
```

## Integration

| Depende de | Para que |
|---|---|
| `builder-design-system` | tailwind.config.ts + globals.css com tokens |
| `builder-landing-page` | Seccoes da homepage |
| `dario-brand` | Metadata, copy, tom de voz |
| `seo-technical` | Validacao SEO pos-scaffold |

## Red Flags
- Gerar sem TypeScript strict — bugs em producao
- Esquecer metadata/OG — SEO zero desde o inicio
- Sem loading.tsx — UX degradada
- Sem error.tsx — crashes visiveis ao user
- Pages router em vez de App Router — arquitectura legacy
- Sem .env.example — devs nao sabem que vars configurar

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Estrutura de directórios completa e coerente

- [ ] Todos os ficheiros core presentes: `app/layout.tsx`, `app/page.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`
- [ ] Route groups usados correctamente (`(marketing)/`, `(app)/`) com layouts nested onde necessário
- [ ] Nenhum ficheiro com nome genérico como `page.tsx` sem estar dentro da pasta de rota correcta
- [ ] `components/` dividido em `ui/`, `sections/`, `layout/` — sem mistura de responsabilidades

❌ NOT delivery-ready: Estrutura plana com `components/Hero.tsx`, `components/Navbar.tsx` sem subdirectórios  
✅ Delivery-ready: `components/sections/hero.tsx`, `components/layout/navbar.tsx`, `components/ui/button.tsx` — cada um na sua camada

---

### Gate 2 — TypeScript strict + tipagem sem lacunas

- [ ] `tsconfig.json` inclui `"strict": true` e `"noUncheckedIndexedAccess": true`
- [ ] Props de todos os componentes têm interface ou type explícito (sem `any` implícito)
- [ ] `Metadata` importado de `'next'` e preenchido com dados reais do projecto
- [ ] `children: React.ReactNode` tipado em layouts e providers

❌ NOT delivery-ready: `export default function Hero(props: any)` ou props sem tipo  
✅ Delivery-ready: `interface HeroProps { title: string; cta: string; badge?: string }` em `components/sections/hero.tsx`

---

### Gate 3 — Metadata + SEO base configurados com dados do projecto

- [ ] `title.default` e `title.template` preenchidos com nome real do projecto (não `"Project Name"`)
- [ ] `description` com copy real — não placeholder genérico
- [ ] `openGraph` com `title`, `description`, `url`, `type` preenchidos
- [ ] `lang` do `<html>` correcto para o mercado (`"pt"` para PT/BR, não `"en"`)

❌ NOT delivery-ready: `title: 'Project Name'`, `description: 'Project description for SEO'`  
✅ Delivery-ready: `title: { default: 'SAQUEI', template: '%s | SAQUEI' }`, `description: 'Antecipa o teu salário em minutos. Sem burocracia.'`

---

### Gate 4 — package.json com versões reais e dependências do projecto

- [ ] `"name"` no package.json é o slug do projecto real (não `"project-name"`)
- [ ] Versões de `next`, `react`, `typescript` pinadas com `^` às major actuais (Next 15, React 19, TS 5.5+)
- [ ] Dependências adicionais do projecto incluídas (ex: `@supabase/ssr` se SaaS, `next-mdx-remote` se blog)
- [ ] `"dev"` script usa `--turbopack` e scripts de lint/build presentes

❌ NOT delivery-ready: `"next": "latest"` ou dependências de projecto SaaS sem `auth` library  
✅ Delivery-ready: `"next": "^15.0.0"`, `"@supabase/ssr": "^0.5.0"`, `"@supabase/supabase-js": "^2.45.0"` para LUSOconta SaaS

---

### Gate 5 — .env.example reflecte todas as vars necessárias

- [ ] Todas as vars de ambiente usadas no código têm entrada em `.env.example`
- [ ] Vars com prefixo `NEXT_PUBLIC_` separadas das server-only
- [ ] Comentários em cada var explicando de onde obter o valor
- [ ] Nenhuma secret real no `.env.example` — apenas `your_value_here` ou descrição

❌ NOT delivery-ready: `.env.example` vazio ou ausente; `SUPABASE_URL=https://real-project.supabase.co` com URL real  
✅ Delivery-ready:
```
# Supabase — obter em app.supabase.com > Project Settings > API
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_keep_secret
```

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder

- [ ] Zero ocorrências de `[project-name]`, `[nome]`, `<ProjectName>`, `<description>` no output final
- [ ] Nome do projecto real aplicado em: `package.json name`, `metadata.title`, `html lang`, `og:title`, nomes de pastas
- [ ] Copy de SEO (`description`, OG) reflecte proposta de valor real do cliente — não boilerplate
- [ ] Comandos de exemplo usam nome real: `/builder-nextjs-app saas lusoconta` não `/builder-nextjs-app saas [nome]`

❌ NOT delivery-ready: `title: 'Project Name'`, `name: "project-name"` no package.json  
✅ Delivery-ready: `title: 'Cuidai'`, `name: "cuidai-app"`, `description: 'Plataforma de gestão de cuidadores ao domicílio'`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Scaffold — Cuidai App (Next.js 15, App Router, SaaS)

## Estrutura gerada

cuidai-app/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── loading.tsx
│   ├── error.tsx
│   ├── not-found.tsx
│   ├── globals.css
│   ├── (marketing)/
│   │   ├── page.tsx          ← Landing homepage
│   │   ├── pricing/page.tsx
│   │   └── sobre/page.tsx
│   ├── (app)/
│   │   ├── layout.tsx        ← Dashboard com sidebar
│   │   ├── dashboard/page.tsx
│   │   ├── cuidadores/page.tsx
│   │   └── relatorios/page.tsx
│   └── api/
│       ├── health/route.ts
│       └── cuidadores/route.ts
├── components/
│   ├── ui/button.tsx
│   ├── ui/card.tsx
│   ├── ui/badge.tsx
│   ├── sections/hero.tsx
│   ├── sections/features.tsx
│   └── layout/sidebar.tsx
├── lib/
│   ├── utils.ts
│   └── constants.ts
└── .env.example

## app/layout.tsx

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })

export const metadata: Metadata = {
  title: { default: 'Cuidai', template: '%s | Cuidai' },
  description: 'Gestão simplificada de cuidadores ao domicílio. Escalas, relatórios e pagamentos numa só plataforma.',
  openGraph: {
    title: 'Cuidai — Plataforma de Gestão de Cuidadores',
    description: 'Gestão simplificada de cuidadores ao domicílio.',
    url: 'https://cuidai.pt',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt" className={inter.variable} suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  )
}

## package.json

{
  "name": "cuidai-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@supabase/ssr": "^0.5.0",
    "@supabase/supabase-js": "^2.45.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "tailwindcss": "^4.0.0"
  }
}

## .env.example

# Supabase — obter em app.supabase.com > Cuidai project > Settings > API
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_never_expose_client

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Output anti-patterns

- Gerar estrutura genérica sem substituir `[project-name]` pelo nome real do cliente — scaffold inútil sem contexto
- Usar `Pages Router` (`pages/index.tsx`) em vez de `App Router` (`app/page.tsx`) — arquitectura deprecated
- `metadata` com `title: 'Project Name'` e `description: 'Project description'` — SEO zerado desde o deploy
- Omitir `loading.tsx` e `error.tsx` — UX degradada em produção sem feedback de estado
- `package.json` com `"next": "latest"` — builds não-determinísticos que quebram sem aviso
- `.env.example` vazio ou ausente — devs em onboarding não sabem que variáveis configurar
- Misturar componentes em `components/` sem subdirectórios `ui/`, `sections/`, `layout/` — codebase desorganizada desde o dia 1
- TypeScript sem `"strict": true` no `tsconfig.json` — bugs de tipo silenciosos que só aparecem em produção
- Scaffoldar variant `saas` sem incluir dependências de auth (`@supabase/ssr` ou equivalente) — funcionalidade core em falta
- Copy de OG/metadata copiado do boilerplate sem adaptar ao produto — zero impacto em partilhas sociais
