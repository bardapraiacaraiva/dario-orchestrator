---
name: builder-drizzle-schema
description: >
  Gera schemas Drizzle ORM (34K stars) — o ORM TypeScript mais rapido. Schema IS TypeScript.
  Migrations auto, type-safe queries, edge-compatible. Substitui Prisma como default.
  Use quando: drizzle, ORM, schema typescript, database drizzle, migrations, tipo seguro.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Drizzle ORM Schema Generator

## Proposito
Gerar schemas Drizzle production-ready. O schema E o TypeScript — zero code generation step.
Drizzle (34K stars) e mais leve que Prisma, SQL-transparent, edge-compatible.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-drizzle-schema [app]` | Schema Drizzle completo |
| `/builder-drizzle-schema from-nl [descricao]` | Natural language → Drizzle schema |
| `/builder-drizzle-schema migrate` | Gerar migration |

## Output Template

```typescript
// db/schema.ts
import { pgTable, uuid, varchar, text, timestamp, decimal, boolean, integer } from 'drizzle-orm/pg-core'
import { relations } from 'drizzle-orm'

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 200 }).notNull(),
  role: varchar('role', { length: 20 }).notNull().default('member'),
  passwordHash: varchar('password_hash', { length: 255 }).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
})

export const usersRelations = relations(users, ({ many }) => ({
  projects: many(projects),
}))

export const projects = pgTable('projects', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: varchar('name', { length: 200 }).notNull(),
  ownerId: uuid('owner_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  status: varchar('status', { length: 20 }).notNull().default('active'),
  budget: decimal('budget', { precision: 12, scale: 2 }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})

// Type inference — zero codegen
export type User = typeof users.$inferSelect
export type NewUser = typeof users.$inferInsert
```

## Drizzle Config
```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit'

export default defineConfig({
  schema: './db/schema.ts',
  out: './db/migrations',
  dialect: 'postgresql',
  dbCredentials: { url: process.env.DATABASE_URL! },
})
```

## Why Drizzle over Prisma
- **7.4KB** vs Prisma's 2MB+ client
- **Zero codegen** — types inferred from schema
- **SQL-transparent** — you see the SQL, not magic
- **Edge-compatible** — works on Vercel Edge, Cloudflare Workers
- **Faster queries** — no query engine overhead

## Inspired by
- **drizzle-team/drizzle-orm** (34K stars)
- **L-Mario564/drizzle-dbml-generator** — auto ERD from schema
