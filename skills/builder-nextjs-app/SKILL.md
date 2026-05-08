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
