---
name: builder-orpc-api
description: >
  Gera APIs com oRPC — combina DX do tRPC com OpenAPI nativo. TypeScript end-to-end,
  auto-gera spec OpenAPI 3.1, Zod/Valibot validation. O melhor dos dois mundos.
  Use quando: API typesafe, tRPC alternativa, openapi automatico, oRPC, API moderna.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — oRPC API Layer

## Proposito
oRPC (3K stars, v1.0) = tRPC DX + OpenAPI output automatico. Sem escolher entre type-safety e standards.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-orpc-api [app]` | API oRPC completa |
| `/builder-orpc-api crud [recurso]` | CRUD para um recurso |

## Output Template

```typescript
// server/router.ts
import { os } from '@orpc/server'
import { z } from 'zod'

const createProject = os
  .input(z.object({
    name: z.string().min(1),
    budget: z.number().positive().optional(),
  }))
  .handler(async ({ input }) => {
    const project = await db.insert(projects).values(input).returning()
    return project[0]
  })

const listProjects = os
  .input(z.object({
    cursor: z.string().optional(),
    limit: z.number().default(20),
  }))
  .handler(async ({ input }) => {
    return db.select().from(projects).limit(input.limit)
  })

export const router = os.router({
  project: { create: createProject, list: listProjects },
})

// Auto-generated OpenAPI spec at /api/spec
// Auto-generated docs at /api/docs
```

## Why oRPC
- Type-safe client like tRPC — `client.project.create({ name: "X" })`
- Auto-generates OpenAPI 3.1 spec — REST compatibility for free
- Works with Zod, Valibot, ArkType
- Cloudflare Workers, Bun, Deno compatible

## Inspired by
- **unnoq/orpc** (3K stars, v1.0)
