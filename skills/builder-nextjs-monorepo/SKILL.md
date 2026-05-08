---
name: builder-nextjs-monorepo
description: >
  Scaffold monorepo production-grade com Turborepo: app + packages (ui, db, email, auth).
  Baseado em next-forge (9K stars, Vercel official). Auth (Clerk), DB (Drizzle), Payments
  (Stripe), Email (Resend), Analytics, Feature Flags, i18n, dark mode pre-configurados.
  Use quando: monorepo, turborepo, next-forge, SaaS completo, app com billing, startup kit.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Next.js Production Monorepo (next-forge)

## Proposito
Scaffold um MONOREPO production-grade que em 1 comando tem tudo que um SaaS precisa.
Baseado no next-forge (Vercel official, 9K stars).

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-nextjs-monorepo [nome]` | Monorepo completo |
| `/builder-nextjs-monorepo minimal [nome]` | Apenas app + db + ui |
| `/builder-nextjs-monorepo init` | Gerar comando npx next-forge |

## Estrutura
```
[project]/
├── apps/
│   ├── web/              ← Next.js main app
│   └── docs/             ← Documentation site
├── packages/
│   ├── ui/               ← Shared components (shadcn)
│   ├── db/               ← Drizzle schema + migrations
│   ├── auth/             ← Clerk config + middleware
│   ├── email/            ← React Email templates
│   ├── analytics/        ← PostHog/Vercel Analytics
│   └── config/           ← Shared ESLint, TS, Tailwind configs
├── turbo.json
├── package.json
└── .env.example
```

## Pre-wired
- **Auth:** Clerk (or lean JWT from saas-starter)
- **Database:** Drizzle ORM + PostgreSQL (Neon recommended)
- **Payments:** Stripe subscriptions + webhooks
- **Email:** Resend + React Email templates
- **Analytics:** PostHog or Vercel Analytics
- **Feature Flags:** Vercel Edge Config or PostHog
- **Observability:** OpenTelemetry spans
- **Dark mode:** next-themes
- **i18n:** next-intl ready

## Init Command
```bash
npx next-forge init [project-name]
```

## Integration
| Alimenta | Com que |
|---|---|
| `builder-database-schema` | packages/db/ (Drizzle schema) |
| `builder-react-components` | packages/ui/ (shadcn components) |
| `builder-auth-system` | packages/auth/ (Clerk or JWT) |
| `builder-api-design` | apps/web/app/api/ (oRPC or REST) |
| `builder-vercel-deploy` | Vercel monorepo deploy config |
| `builder-coolify-deploy` | Docker multi-stage for self-hosted |

## Inspired by
- **vercel/next-forge** (9K stars) — Official Vercel monorepo template
- **t3-oss/create-t3-app** (28K stars) — Typesafe Next.js scaffold
- **nextjs/saas-starter** (12K stars) — Official Stripe + Auth pattern
