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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Schema Zod/Valibot é production-grade
- [ ] Todos os campos têm validação específica (`.min()`, `.max()`, `.email()`, `.positive()`, regex)
- [ ] Campos opcionais explicitamente marcados com `.optional()` ou `.default()`
- [ ] Nenhum `z.any()` ou `z.unknown()` sem comentário justificativo
- ❌ NOT delivery-ready: `name: z.string(), amount: z.number()`
- ✅ Delivery-ready: `name: z.string().min(2).max(100), amount: z.number().positive().max(999999)`

### Gate 2 — Router structure reflete domínio real do cliente
- [ ] Namespaces do router mapeiam entidades reais do projecto (ex: `patient`, `invoice`, `pet`, `loan`)
- [ ] Nenhum `project`/`item`/`resource` genérico no output final
- [ ] Hierarquia do router coerente: max 2 níveis de nesting (`router.entity.action`)
- ❌ NOT delivery-ready: `router = os.router({ project: { create, list } })`
- ✅ Delivery-ready: `router = os.router({ cuidado: { agendar, cancelar, listar }, paciente: { registar, atualizar } })`

### Gate 3 — OpenAPI spec está configurada e acessível
- [ ] Endpoint `/api/spec` documentado com URL real (ex: `https://api.cuidai.pt/api/spec`)
- [ ] Endpoint `/api/docs` (Scalar/Swagger UI) referenciado no output
- [ ] `info.title`, `info.version`, `info.description` preenchidos com dados do cliente
- ❌ NOT delivery-ready: `// Auto-generated OpenAPI spec at /api/spec` (só comentário)
- ✅ Delivery-ready: spec exportada com `title: "Cuidaí API"`, `version: "1.0.0"`, servidor apontado para `https://api.cuidai.pt`

### Gate 4 — Handler tem lógica real (não stub)
- [ ] Cada handler contém pelo menos a query/mutation principal (não `// TODO: implement`)
- [ ] Error handling explícito: `ORPCError` ou try/catch com mensagem tipada
- [ ] Return type coerente com o schema de input (sem `return {}` vazio)
- ❌ NOT delivery-ready: `handler: async ({ input }) => { return {} }`
- ✅ Delivery-ready: `handler: async ({ input }) => { const r = await db.insert(consultas).values({ pacienteId: input.pacienteId, data: input.data }).returning(); if (!r[0]) throw new ORPCError({ code: 'INTERNAL_SERVER_ERROR' }); return r[0] }`

### Gate 5 — Client-side usage está demonstrado
- [ ] Pelo menos 1 exemplo de chamada tipada do cliente (`client.entity.action({...})`)
- [ ] Import path correto para o contexto do projecto (ex: `~/lib/orpc-client`)
- [ ] Demonstra inferência de tipo (ex: `const result: typeof client.entity.list.$output`)
- ❌ NOT delivery-ready: `// use client.project.create() on frontend`
- ✅ Delivery-ready: `const loan = await client.emprestimo.criar({ valor: 5000, prazo: 12 }) // type: { id: string, valorMensal: number, dataVencimento: Date }`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Zero ocorrências de `<client>`, `<recurso>`, `<endpoint>`, `<url>`
- [ ] Nome da app aparece em: `info.title`, comentários de ficheiro, nomes de variáveis onde relevante
- [ ] URLs de servidor são reais ou seguem padrão do cliente (ex: `saquei.pt`, `arrecada.gov.pt`)
- ❌ NOT delivery-ready: `title: "<APP_NAME>"`, `baseURL: "<API_URL>"`
- ✅ Delivery-ready: `title: "SAQUEI Loans API"`, `baseURL: "https://api.saquei.pt"`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output oRPC deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado do projecto/sessão/dados do cliente (ex: nome da app, stack confirmada)
- 🟡 **assumed** — plausível mas precisa de confirm do cliente antes de entregar
- 🟢 **projection** — forecast by design — spec gerada automaticamente, não verificável até runtime

Output checklist upfront mostra o reader exactamente o que é trust-as-is vs o que precisa verificar antes de fazer deploy. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
// router.ts — SaqueiApp API v1.0
baseURL: "https://api.saquei.pt"
limit: 20  
ORPCError code: 'NOT_FOUND'
```
*(zero labels — reader assume tudo verified, mas baseURL pode não existir ainda, limit é arbitrário)*

✅ Delivery-ready:
```
// 🔵 verified: cliente confirmou stack oRPC + Drizzle em sessão anterior
// 🟡 assumed: baseURL "https://api.saquei.pt" — aguarda infra confirm
// 🟡 assumed: limit default 20 — presumido razoável, cliente pode querer 10 ou 50  
// 🟢 projection: OpenAPI spec em /api/spec gerada automaticamente pelo oRPC — válida após primeiro boot
// 🟢 projection: type inference `client.emprestimo.criar.$output` resolve correctamente em runtime
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir `baseURL` assumed com URL real de produção/staging
- [ ] All 🟡 defaults confirmados — `limit`, paginação, timeouts alinhados com requisitos do cliente
- [ ] All 🔵 citations adicionadas — versão oRPC (`v1.0`), schema Zod, DB table names validados contra migration real
- [ ] All 🟢 projections comunicadas ao cliente — deixar claro que spec OpenAPI e tipos só são verificáveis após `npm run dev` / primeiro deploy

## Fully-worked A-tier example (delivery-ready reference)

```markdown
// server/router.ts — SAQUEI Loans API
import { os } from '@orpc/server'
import { ORPCError } from '@orpc/server'
import { z } from 'zod'
import { db } from '~/db'
import { emprestimos, clientes, pagamentos } from '~/db/schema'

// === SCHEMAS ===

const CriarEmprestimoSchema = z.object({
  clienteId: z.string().uuid(),
  valor: z.number().positive().max(50000),
  prazo: z.number().int().min(3).max(60), // meses
  finalidade: z.enum(['pessoal', 'automovel', 'habitacao', 'negocio']),
})

const ListarEmprestimosSchema = z.object({
  clienteId: z.string().uuid().optional(),
  estado: z.enum(['pendente', 'ativo', 'liquidado', 'incumprimento']).optional(),
  cursor: z.string().optional(),
  limit: z.number().int().min(1).max(100).default(20),
})

const RegistarPagamentoSchema = z.object({
  emprestimoId: z.string().uuid(),
  valor: z.number().positive(),
  metodo: z.enum(['mbway', 'transferencia', 'debito_direto']),
  referencia: z.string().max(50).optional(),
})

// === HANDLERS ===

const criarEmprestimo = os
  .input(CriarEmprestimoSchema)
  .handler(async ({ input }) => {
    const cliente = await db.query.clientes.findFirst({
      where: (c, { eq }) => eq(c.id, input.clienteId),
    })
    if (!cliente) throw new ORPCError({ code: 'NOT_FOUND', message: 'Cliente não encontrado' })
    if (cliente.scoreCredito < 500) throw new ORPCError({ code: 'FORBIDDEN', message: 'Score de crédito insuficiente' })

    const taxaJuro = input.finalidade === 'habitacao' ? 0.032 : 0.078
    const valorMensal = (input.valor * taxaJuro / 12) / (1 - Math.pow(1 + taxaJuro / 12, -input.prazo))

    const [emprestimo] = await db.insert(emprestimos).values({
      clienteId: input.clienteId,
      valor: input.valor,
      prazo: input.prazo,
      finalidade: input.finalidade,
      taxaJuro,
      valorMensal: Math.round(valorMensal * 100) / 100,
      estado: 'pendente',
      dataInicio: new Date(),
    }).returning()

    return emprestimo
  })

const listarEmprestimos = os
  .input(ListarEmprestimosSchema)
  .handler(async ({ input }) => {
    return db.select().from(emprestimos)
      .where(input.clienteId ? eq(emprestimos.clienteId, input.clienteId) : undefined)
      .limit(input.limit)
  })

const registarPagamento = os
  .input(RegistarPagamentoSchema)
  .handler(async ({ input }) => {
    const emprestimo = await db.query.emprestimos.findFirst({
      where: (e, { eq }) => eq(e.id, input.emprestimoId),
    })
    if (!emprestimo) throw new ORPCError({ code: 'NOT_FOUND', message: 'Empréstimo não encontrado' })
    if (emprestimo.estado === 'liquidado') throw new ORPCError({ code: 'BAD_REQUEST', message: 'Empréstimo já liquidado' })

    const [pagamento] = await db.insert(pagamentos).values({
      ...input,
      data: new Date(),
    }).returning()

    return pagamento
  })

// === ROUTER ===

export const router = os.router({
  emprestimo: { criar: criarEmprestimo, listar: listarEmprestimos },
  pagamento: { registar: registarPagamento },
})

// === OPENAPI SPEC ===
// title: "SAQUEI Loans API"
// version: "1.0.0"
// server: https://api.saquei.pt
// spec: https://api.saquei.pt/api/spec
// docs: https://api.saquei.pt/api/docs

// === CLIENT USAGE (frontend / app mobile) ===
// import { client } from '~/lib/orpc-client'
//
// const novoEmprestimo = await client.emprestimo.criar({
//   clienteId: 'uuid-do-cliente',
//   valor: 8500,
//   prazo: 24,
//   finalidade: 'automovel',
// })
// // type inferred: { id: string, valorMensal: number, taxaJuro: number, estado: string }
```

---

## Output anti-patterns

- Usar `z.any()` em campos de negócio críticos (valor monetário, datas, IDs) sem validação tipada
- Router com nomes genéricos (`project`, `item`, `resource`) no output final entregue ao cliente
- OpenAPI spec configurada apenas como comentário `// spec at /api/spec` sem código real de export
- Handlers com `return {}` ou `// TODO` — nunca entregar stubs como se fossem implementação
- Esquecer `ORPCError` e usar `throw new Error('string')` genérico — perde type-safety no cliente
- Client-side usage ausente — o cliente não sabe como chamar a API que acabou de receber
- Angle-brackets residuais (`<clienteId>`, `<APP>`, `<URL>`) no output final
- Nesting de router com 3+ níveis (`router.domain.entity.subentity.action`) — quebra DX do oRPC
- Misturar paradigmas REST e oRPC no mesmo ficheiro sem separação clara (confunde o cliente)
- Ignorar runtime target — não mencionar se é Bun/Cloudflare Workers/Node quando o cliente usa Edge
