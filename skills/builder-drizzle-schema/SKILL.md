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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Imports corretos e completos
- [ ] Todos os tipos usados no schema estão importados de `drizzle-orm/pg-core` (ou mysql-core/sqlite-core conforme dialect)
- [ ] `relations` importado de `drizzle-orm` se existirem relações definidas
- [ ] Sem imports fantasma (e.g. `jsonb` importado mas não usado, ou usado mas não importado)
- [ ] Dialect consistente — não mistura `pgTable` com `mysqlTable` no mesmo schema
- ❌ NOT delivery-ready: `import { pgTable, jsonb } from 'drizzle-orm/pg-core'` — `jsonb` não existe nesse path, causa crash em runtime
- ✅ Delivery-ready: `import { pgTable, uuid, varchar, text, timestamp, decimal, boolean, integer, jsonb } from 'drizzle-orm/pg-core'` — todos os tipos presentes e verificados contra a API Drizzle 0.29+

### Gate 2 — Definição de colunas válida e type-safe
- [ ] Primary keys usam `.primaryKey().defaultRandom()` (uuid) ou `.primaryKey().generatedAlwaysAsIdentity()` (serial moderno)
- [ ] Foreign keys referenciam com arrow function: `.references(() => users.id, { onDelete: 'cascade' })` — não string
- [ ] `varchar` inclui `{ length: N }` — nunca `varchar('col')` sem length (Drizzle não infere default)
- [ ] Campos obrigatórios têm `.notNull()`, campos opcionais explicitamente sem ele
- [ ] Enums modelados via `pgEnum` quando domínio fixo (role, status), não `varchar` livre
- ❌ NOT delivery-ready: `status: varchar('status').notNull()` — sem length, type inferred como `string` genérico, migration pode falhar
- ✅ Delivery-ready: `status: statusEnum('status').notNull().default('active')` onde `export const statusEnum = pgEnum('status', ['active', 'paused', 'closed'])`

### Gate 3 — Relations bidirecionais e consistentes
- [ ] Cada `one()` tem o inverso `many()` no outro lado definido em `*Relations`
- [ ] `fields` e `references` em `one()` apontam para colunas que existem no schema
- [ ] Nomes das relations não conflituam com nomes de colunas da mesma tabela
- [ ] Schema sem relações circulares não-resolvidas (self-referencing usa `one(table, { relationName: '...' })`)
- ❌ NOT delivery-ready: `usersRelations` define `many(orders)` mas `ordersRelations` não define `one(users)` — Drizzle queries com `with:` retornam undefined silenciosamente
- ✅ Delivery-ready: `usersRelations` → `many(orders)` + `ordersRelations` → `one(users, { fields: [orders.userId], references: [users.id] })` — par completo, queries com `with: { orders: true }` funcionam

### Gate 4 — drizzle.config.ts correto e funcional
- [ ] `dialect` presente e corresponde ao adapter usado (`postgresql`, `mysql`, `sqlite`)
- [ ] `schema` path relativo correto face à raiz do projeto
- [ ] `out` definido para pasta de migrations (e.g. `./db/migrations`)
- [ ] `dbCredentials` usa variável de ambiente — nunca credenciais hardcoded
- [ ] Config compatível com versão drizzle-kit usada (0.20+ usa `defineConfig`, não export default object)
- ❌ NOT delivery-ready: `driver: 'pg'` — propriedade deprecated desde drizzle-kit 0.21, `drizzle-kit push` falha com warning crítico
- ✅ Delivery-ready: `dialect: 'postgresql'` + `dbCredentials: { url: process.env.DATABASE_URL! }` — sintaxe drizzle-kit 0.21+

### Gate 5 — Type inference exportada e utilizável
- [ ] Cada tabela principal exporta `type X = typeof table.$inferSelect` e `type NewX = typeof table.$inferInsert`
- [ ] Types com campos opcionais reflectem correctamente nullable vs notNull no schema
- [ ] Sem `as any` ou type assertions que quebrem a chain de type-safety
- [ ] Se existir schema Zod para validação, gerado via `drizzle-zod` não manualmente
- ❌ NOT delivery-ready: schema sem exports de types — developer tem de reescrever interfaces manualmente, derrotando o propósito central do Drizzle
- ✅ Delivery-ready: `export type Subscription = typeof subscriptions.$inferSelect` — IDE autocompleta `subscription.planId`, TypeScript recusa `subscription.nonExistentField` em compile time

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholders
- [ ] Nomes de tabelas reflectem o domínio do cliente (e.g. `caregivers`, `tax_cases`, `storage_units`) — não `users`/`items` genéricos
- [ ] Sem `<APP_NAME>`, `<TABLE>`, `<COLUMN_TYPE>` no output final
- [ ] `DATABASE_URL` é a única variável de ambiente — sem `<YOUR_DATABASE_URL>` ou similar
- [ ] Comentários no schema mencionam o projecto real (e.g. `// Cuidai — schema de cuidadores e sessões`)
- ❌ NOT delivery-ready: `// db/schema.ts for <CLIENT_APP>` com `export const items = pgTable('<table_name>', {`
- ✅ Delivery-ready: `// ARRECADA.GOV — schema de processos de recuperação de bens` com `export const recoveryProcesses = pgTable('recovery_processes', {`

---

## Fully-worked A-tier example (delivery-ready reference)

```typescript
// ARRECADA.GOV — schema de processos de recuperação de ativos do Estado
// Drizzle ORM 0.29 · PostgreSQL · drizzle-kit 0.21
import {
  pgTable, pgEnum, uuid, varchar, text,
  timestamp, decimal, boolean, integer
} from 'drizzle-orm/pg-core'
import { relations } from 'drizzle-orm'

// --- Enums ---
export const processStatusEnum = pgEnum('process_status', [
  'rascunho', 'submetido', 'em_analise', 'aprovado', 'arquivado'
])
export const assetTypeEnum = pgEnum('asset_type', [
  'imovel', 'veiculo', 'equipamento', 'outro'
])

// --- Tabelas ---
export const agentes = pgTable('agentes', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  nome: varchar('nome', { length: 200 }).notNull(),
  servico: varchar('servico', { length: 100 }).notNull(), // e.g. "DGPJ", "AT", "ANMP"
  ativo: boolean('ativo').notNull().default(true),
  criadoEm: timestamp('criado_em').defaultNow().notNull(),
})

export const processos = pgTable('processos', {
  id: uuid('id').primaryKey().defaultRandom(),
  referencia: varchar('referencia', { length: 30 }).notNull().unique(), // e.g. "ARR-2024-00341"
  titulo: varchar('titulo', { length: 300 }).notNull(),
  status: processStatusEnum('status').notNull().default('rascunho'),
  valorEstimado: decimal('valor_estimado', { precision: 14, scale: 2 }),
  agenteId: uuid('agente_id').notNull().references(() => agentes.id, { onDelete: 'restrict' }),
  criadoEm: timestamp('criado_em').defaultNow().notNull(),
  atualizadoEm: timestamp('atualizado_em').defaultNow().notNull(),
})

export const ativos = pgTable('ativos', {
  id: uuid('id').primaryKey().defaultRandom(),
  processoId: uuid('processo_id').notNull().references(() => processos.id, { onDelete: 'cascade' }),
  tipo: assetTypeEnum('tipo').notNull(),
  descricao: text('descricao').notNull(),
  matricula: varchar('matricula', { length: 50 }), // null se não aplicável
  valorAvaliado: decimal('valor_avaliado', { precision: 14, scale: 2 }),
  recuperado: boolean('recuperado').notNull().default(false),
  criadoEm: timestamp('criado_em').defaultNow().notNull(),
})

// --- Relations ---
export const agentesRelations = relations(agentes, ({ many }) => ({
  processos: many(processos),
}))

export const processosRelations = relations(processos, ({ one, many }) => ({
  agente: one(agentes, { fields: [processos.agenteId], references: [agentes.id] }),
  ativos: many(ativos),
}))

export const ativosRelations = relations(ativos, ({ one }) => ({
  processo: one(processos, { fields: [ativos.processoId], references: [processos.id] }),
}))

// --- Type inference — zero codegen ---
export type Agente    = typeof agentes.$inferSelect
export type NovoAgente = typeof agentes.$inferInsert
export type Processo  = typeof processos.$inferSelect
export type NovoProcesso = typeof processos.$inferInsert
export type Ativo     = typeof ativos.$inferSelect
export type NovoAtivo = typeof ativos.$inferInsert
```

```typescript
// drizzle.config.ts — ARRECADA.GOV
import { defineConfig } from 'drizzle-kit'

export default defineConfig({
  schema: './db/schema.ts',
  out: './db/migrations',
  dialect: 'postgresql',
  dbCredentials: { url: process.env.DATABASE_URL! },
})
```

---

## Output anti-patterns

- **Imports incompletos** — usar `jsonb` ou `pgEnum` no schema sem importar, output compila aparentemente mas falha em runtime
- **`varchar` sem `{ length: N }`** — Drizzle não tem default, migration gera coluna sem constraint e type fica `string` genérico
- **Relations semi-definidas** — definir `many(orders)` sem o `one(users)` inverso; queries com `with:` retornam `undefined` sem erro visível
- **`driver: 'pg'` no drizzle.config.ts** — API deprecated desde 0.21, substituída por `dialect: 'postgresql'`; quebra `drizzle-kit push` e `generate`
- **Tabelas genéricas** (`users`, `items`, `records`) entregues como output final sem adaptar ao domínio do cliente
- **Angle-brackets no output** — `<CLIENT>`, `<TABLE_NAME>`, `<YOUR_DB_URL>` indicam template não preenchido; nunca delivery-ready
- **Types não exportados** — omitir `$inferSelect`/`$inferInsert` derrota a proposta de valor central do Drizzle; developer reescreve interfaces à mão
- **`onDelete` em cascade em tabelas de auditoria/histórico** — apagar o pai apaga silenciosamente o registo histórico; usar `restrict` ou `set null`
- **Mistura de dialects** — `pgTable` com `dbCredentials: { url }` para SQLite, ou `sqliteTable` com `dialect: 'postgresql'`; schema não roda
- **Schema sem enums para campos de domínio fixo** — `status: varchar('status', { length: 20 })` aceita `'ACTIVO'`, `'activo'`, `'ativo'` sem erro; usar `pgEnum` para garantir integridade
