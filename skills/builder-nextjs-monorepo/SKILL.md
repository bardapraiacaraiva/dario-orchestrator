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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Estrutura de pastas gerada é completa e correcta
- [ ] `apps/` contém pelo menos `web/` (e `docs/` se não for modo `minimal`)
- [ ] `packages/` tem os 6 subdirectórios esperados: `ui`, `db`, `auth`, `email`, `analytics`, `config`
- [ ] `turbo.json`, `package.json` raiz e `.env.example` estão presentes na raiz
- [ ] Modo `minimal` omite correctamente `docs/`, `email/`, `analytics/`
- ❌ NOT delivery-ready: pasta genérica `src/` sem separação `apps/`/`packages/`
- ✅ Delivery-ready: `tributario-ai/apps/web/`, `tributario-ai/packages/db/`, `tributario-ai/turbo.json` gerados com conteúdo real

### Gate 2 — Stack pré-configurada corresponde ao pedido do cliente
- [ ] Auth especificada (Clerk ou JWT lean) está no `packages/auth/` com middleware real, não placeholder
- [ ] `packages/db/` tem schema Drizzle com pelo menos uma tabela relevante ao projecto (ex: `users`, `subscriptions`)
- [ ] Stripe presente com webhook handler em `apps/web/app/api/webhooks/stripe/route.ts` se billing foi pedido
- [ ] Resend + React Email template mínimo em `packages/email/` se email foi pedido
- ❌ NOT delivery-ready: `// TODO: add Stripe webhook` sem implementação
- ✅ Delivery-ready: `stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET)` com handler real para `checkout.session.completed`

### Gate 3 — `turbo.json` e `package.json` raiz são funcionais
- [ ] `turbo.json` define pipeline `build`, `dev`, `lint` com dependências correctas (`dependsOn: ["^build"]`)
- [ ] `package.json` raiz tem `workspaces` apontando para `apps/*` e `packages/*`
- [ ] Scripts `dev`, `build`, `lint` no raiz executam via Turborepo (`turbo run dev`)
- [ ] Versões de dependências são fixas (não `*` ou `latest`)
- ❌ NOT delivery-ready: `turbo.json` com pipeline vazia `{}` ou sem `outputs`
- ✅ Delivery-ready: `"build": { "dependsOn": ["^build"], "outputs": [".next/**", "dist/**"] }` com cache configurado

### Gate 4 — `.env.example` cobre todas as integrações declaradas
- [ ] Cada serviço pre-wired tem as suas variáveis documentadas: `CLERK_*`, `DATABASE_URL`, `STRIPE_*`, `RESEND_API_KEY`, `NEXT_PUBLIC_POSTHOG_KEY`
- [ ] Variáveis `NEXT_PUBLIC_` separadas das server-only — sem expor secrets ao browser
- [ ] Comentários no `.env.example` indicam onde obter cada chave (ex: `# https://dashboard.clerk.com`)
- [ ] `DATABASE_URL` usa formato Neon se PostgreSQL foi especificado
- ❌ NOT delivery-ready: `.env.example` com 3 variáveis para um stack de 6 serviços
- ✅ Delivery-ready: 20+ variáveis organizadas por secção (`# Auth — Clerk`, `# Database — Neon`, `# Payments — Stripe`) com URLs de referência

### Gate 5 — `init` command e instruções de bootstrap são executáveis
- [ ] Comando `npx next-forge init [project-name]` está explícito com o nome real do projecto substituído
- [ ] Passos pós-init estão ordenados: instalar deps → configurar `.env` → `turbo run dev`
- [ ] Integração com outros builders (`builder-database-schema`, `builder-auth-system`) é referenciada com o caminho exacto onde o output se encaixa
- [ ] Versão do Node.js mínima e do pnpm/npm especificada
- ❌ NOT delivery-ready: "run the init command and configure your env vars"
- ✅ Delivery-ready: `npx next-forge init cuidai && cd cuidai && pnpm install && cp .env.example .env.local` seguido de checklist de 5 passos com links

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Nome do projecto aparece no path raiz, no `package.json` `name` field e nos scripts
- [ ] Nenhum `<project-name>`, `<your-api-key>`, `<database-url>` presente no output final
- [ ] Schema Drizzle tem nomes de tabelas relevantes ao domínio do cliente (não `users_table_example`)
- [ ] URLs de exemplo usam domínio real ou fictício coerente (ex: `cuidai.pt`, não `example.com`)
- ❌ NOT delivery-ready: `DATABASE_URL=<your-neon-connection-string>`
- ✅ Delivery-ready: `DATABASE_URL=postgresql://cuidai:[email protected]/cuidai-prod`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via next-forge repo / stack oficial / versão fixada no lock file
- 🟡 **assumed** — plausível para o projecto mas precisa de confirm do cliente antes de delivery
- 🟢 **projection** — estimativa de comportamento em runtime/deploy (não verificável no scaffold)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready: scaffold entregue com `"next-forge (9K stars, Clerk, Drizzle, Stripe pré-configurados"` sem distinguir o que foi realmente gerado no projecto vs o que é feature do template base vs o que depende de env vars do cliente — reader assume tudo como production-ready.

✅ Delivery-ready:
- 🔵 **verified** — `turbo.json` com `"build": { "dependsOn": ["^build"], "outputs": [".next/**"] }` gerado e validado localmente
- 🟡 **assumed** — `DATABASE_URL` aponta para Neon (plausível para stack recomendada, mas cliente pode usar Supabase ou self-hosted Postgres)
- 🟢 **projection** — cold start < 200 ms no Vercel Edge com Clerk middleware activo (estimativa baseada em benchmarks next-forge, não medido neste projecto)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir `DATABASE_URL` provider, `CLERK_*` keys e `STRIPE_WEBHOOK_SECRET` com actuals do cliente
- [ ] All 🔵 citations added — versões de `next`, `drizzle-orm`, `@clerk/nextjs`, `stripe` fixadas no `package.json` raiz com hash do commit next-forge base
- [ ] All 🟢 projections labeled ao cliente — performance estimates e cache hit rates de Turborepo comunicados como projecções, não garantias

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Monorepo: Cuidai — Next.js Production Setup

## Bootstrap

```bash
npx next-forge init cuidai
cd cuidai
pnpm install
cp .env.example .env.local
pnpm turbo run dev
```

Node ≥ 20.x | pnpm ≥ 9.x

---

## Estrutura gerada

```
cuidai/
├── apps/
│   ├── web/                          ← Next.js 14 (App Router)
│   │   └── app/
│   │       ├── api/
│   │       │   └── webhooks/
│   │       │       └── stripe/
│   │       │           └── route.ts  ← Stripe billing events
│   │       ├── (auth)/
│   │       │   ├── sign-in/page.tsx
│   │       │   └── sign-up/page.tsx
│   │       └── dashboard/page.tsx
│   └── docs/                         ← Fumadocs (cuidai.pt/docs)
├── packages/
│   ├── ui/          ← shadcn/ui components (Button, Card, Badge)
│   ├── db/          ← Drizzle ORM (Neon PostgreSQL)
│   ├── auth/        ← Clerk middleware + helpers
│   ├── email/       ← Resend + React Email templates
│   ├── analytics/   ← PostHog (cuidai eventos: cuidador_matched)
│   └── config/      ← ESLint, TypeScript, Tailwind configs
├── turbo.json
├── package.json
└── .env.example
```

---

## `turbo.json`

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": { "outputs": [] },
    "type-check": { "outputs": [] }
  }
}
```

---

## `packages/db/schema.ts` (Drizzle)

```typescript
import { pgTable, text, timestamp, boolean, integer } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: text("id").primaryKey(), // Clerk user ID
  email: text("email").notNull().unique(),
  planId: text("plan_id").default("free"),
  stripeCustomerId: text("stripe_customer_id"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const cuidadores = pgTable("cuidadores", {
  id: text("id").primaryKey(),
  userId: text("user_id").references(() => users.id),
  zona: text("zona").notNull(), // ex: "Lisboa - Alvalade"
  disponivel: boolean("disponivel").default(true),
  ratingMedia: integer("rating_media").default(0),
  updatedAt: timestamp("updated_at").defaultNow(),
});
```

---

## `packages/auth/middleware.ts`

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isPublicRoute = createRouteMatcher(["/", "/sign-in(.*)", "/sign-up(.*)", "/api/webhooks/stripe"]);

export default clerkMiddleware((auth, request) => {
  if (!isPublicRoute(request)) auth().protect();
});

export const config = { matcher: ["/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)", "/(api|trpc)(.*)"] };
```

---

## `.env.example`

```bash
# Auth — Clerk (https://dashboard.clerk.com → cuidai app)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
CLERK_SECRET_KEY=sk_live_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up

# Database — Neon PostgreSQL (https://console.neon.tech → cuidai-prod)
DATABASE_URL=postgresql://cuidai:[email protected]/cuidai-prod?sslmode=require

# Payments — Stripe (https://dashboard.stripe.com → cuidai)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...

# Email — Resend (https://resend.com/api-keys → cuidai.pt domain)
RESEND_API_KEY=re_...
EMAIL_FROM=noreply@cuidai.pt

# Analytics — PostHog (https://eu.posthog.com → cuidai project)
NEXT_PUBLIC_POSTHOG_KEY=phc_...
NEXT_PUBLIC_POSTHOG_HOST=https://eu.i.posthog.com
```

---

## Próximos builders a invocar

| Builder | Path de destino | Comando |
|---|---|---|
| `builder-database-schema` | `packages/db/schema.ts` | Expand cuidadores + pedidos tables |
| `builder-auth-system` | `packages/auth/` | Role-based (cuidador vs família) |
| `builder-vercel-deploy` | `vercel.json` + monorepo config | Deploy cuidai.pt + docs.cuidai.pt |
```

---

## Output anti-patterns

- Gerar `<project-name>` literalmente no output em vez do nome real do cliente
- `turbo.json` com pipeline vazia ou sem `dependsOn: ["^build"]` (quebra cache cascading)
- `.env.example` incompleto — listar Stripe mas omitir `STRIPE_WEBHOOK_SECRET`
- Schema Drizzle com tabelas genéricas `items`, `things` sem relação ao domínio do cliente
- Misturar `apps/` e `packages/` na raiz (non-monorepo flat structure)
- Modo `minimal` que ainda inclui `analytics/` e `email/` (ignora o flag)
- `package.json` raiz sem `"workspaces": ["apps/*", "packages/*"]` (pnpm/yarn não detecta monorepo)
- Webhook Stripe sem verificação de assinatura (`stripe.webhooks.constructEvent`) — falha de segurança
- Variáveis `CLERK_SECRET_KEY` prefixadas com `NEXT_PUBLIC_` — expõe secret ao browser
- Omitir passos de bootstrap ordenados — cliente não sabe por onde começar após scaffold
