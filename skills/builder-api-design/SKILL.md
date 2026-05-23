---
name: builder-api-design
description: >
  Gera APIs REST/GraphQL production-ready: endpoints, schemas, validation, error handling,
  auth middleware, rate limiting, OpenAPI spec. Output e codigo funcional Node/Python.
  Use quando: criar API, REST endpoints, backend routes, GraphQL schema, API design.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — API Design & Implementation

## Proposito
Gerar APIs COMPLETAS e FUNCIONAIS — endpoints, validation, error handling, middleware, docs.
Suporta dois stacks: **Node.js (Express/Fastify)** e **Python (FastAPI)**.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-api-design [recurso]` | CRUD API para um recurso |
| `/builder-api-design full [app]` | API completa para uma app |
| `/builder-api-design graphql [app]` | GraphQL schema + resolvers |

## Workflow

### 1. Define Resources
Mapear entidades, relacoes, e operacoes:
```
User: id, email, name, role, created_at
Project: id, name, client_id, status, budget
Task: id, title, project_id, assignee_id, status, due_date
```

### 2. Generate Endpoints (REST)
Para cada recurso, gerar CRUD + custom:
```
GET    /api/v1/projects          — List (filtros, paginacao, sort)
GET    /api/v1/projects/:id      — Get by ID
POST   /api/v1/projects          — Create (validation)
PATCH  /api/v1/projects/:id      — Update (partial)
DELETE /api/v1/projects/:id      — Soft delete
GET    /api/v1/projects/:id/tasks — Nested resource
```

### 3. Request Validation (Zod/Pydantic)
```typescript
// Node.js + Zod
const createProjectSchema = z.object({
  name: z.string().min(1).max(200),
  client_id: z.string().uuid(),
  budget: z.number().positive().optional(),
  status: z.enum(['draft', 'active', 'completed', 'archived']).default('draft'),
})
```

```python
# Python + Pydantic
class CreateProject(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    client_id: UUID
    budget: Optional[float] = Field(gt=0, default=None)
    status: Literal['draft', 'active', 'completed', 'archived'] = 'draft'
```

### 4. Error Handling
```typescript
// Standardized error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [{"field": "email", "message": "Invalid email format"}],
    "request_id": "req_abc123"
  }
}
```

### 5. Pagination
```typescript
// Cursor-based (recommended) or offset-based
GET /api/v1/projects?cursor=abc&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "has_more": true,
    "next_cursor": "def",
    "total": 150
  }
}
```

### 6. OpenAPI Spec (auto-generated)
Gerar spec OpenAPI 3.1 com todos os endpoints, schemas, exemplos.

## Output
1. Route files (endpoints per resource)
2. Validation schemas (Zod or Pydantic)
3. Error handler middleware
4. Pagination utility
5. OpenAPI spec (openapi.yaml)
6. README with setup instructions

## Red Flags
- API sem versionamento (/api/v1/) — breaking changes sem controlo
- Sem validation no input — injection risk
- Sem paginacao em list endpoints — performance killer
- Sem error handling padronizado — debugging nightmare
- Sem rate limiting — DoS vulnerability

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Recursos & endpoints cobrem o domínio real do cliente
- [ ] Entidades mapeadas correspondem ao negócio (não genéricas "User/Product/Order" sem contexto)
- [ ] CRUD completo gerado para cada recurso principal + relações nested identificadas
- [ ] Endpoints custom (além de CRUD) cobertos onde o domínio exige (ex: `/projects/:id/assign`, `/invoices/:id/send`)
- [ ] Versionamento `/api/v1/` presente em TODOS os endpoints sem excepção
- ❌ NOT delivery-ready: `GET /projects` sem versão, sem filtros, sem nested routes para tasks
- ✅ Delivery-ready: `GET /api/v1/cuidai/caregivers?status=available&region=lisboa&cursor=abc&limit=20` com nested `GET /api/v1/cuidai/caregivers/:id/bookings`

---

### Gate 2 — Validation schemas completos (Zod ou Pydantic) com regras de negócio
- [ ] Schema gerado para cada `POST` e `PATCH` — sem campos sem tipo ou sem constraint
- [ ] Enums reflectem estados reais do domínio (não `['a','b','c']` placeholder)
- [ ] Campos opcionais vs obrigatórios correctos segundo lógica de negócio
- [ ] UUID, email, date formats validados explicitamente
- ❌ NOT delivery-ready: `budget: z.number()` sem `.positive()`, `status: z.string()` sem enum
- ✅ Delivery-ready: `status: z.enum(['pending_match','active','on_hold','completed','cancelled']).default('pending_match')` para Cuidai bookings

---

### Gate 3 — Error handling padronizado e response contract consistente
- [ ] Estrutura `{ error: { code, message, details, request_id } }` aplicada a TODOS os handlers
- [ ] Códigos HTTP correctos: 400 validation, 401 auth, 403 forbidden, 404 not found, 409 conflict, 429 rate limit, 500 server
- [ ] Error codes semânticos específicos (não apenas `"GENERIC_ERROR"`) — ex: `PROJECT_NOT_FOUND`, `DUPLICATE_EMAIL`
- [ ] Middleware global de error catching incluído (não try/catch inline em cada route)
- ❌ NOT delivery-ready: `res.status(400).json({ message: "Error" })` inline, sem request_id, sem code
- ✅ Delivery-ready: `{ "error": { "code": "CAREGIVER_UNAVAILABLE", "message": "Cuidador não disponível para o período solicitado", "request_id": "req_7f3a9c" } }`

---

### Gate 4 — Paginação implementada em TODOS os list endpoints
- [ ] `GET /resource` nunca retorna array não paginado — sempre wrapped com `{ data, pagination }`
- [ ] Cursor-based **ou** offset-based escolhido consistentemente (não misturado)
- [ ] `has_more`, `next_cursor`/`total`, `limit` presentes no response
- [ ] Parâmetros de query documentados: `?cursor=`, `?limit=`, `?sort=`, `?filter=`
- ❌ NOT delivery-ready: `res.json(await db.findAll())` sem paginação, sem total
- ✅ Delivery-ready: `{ "data": [...], "pagination": { "has_more": true, "next_cursor": "eyJpZCI6MTIzfQ", "total": 847, "limit": 20 } }`

---

### Gate 5 — Auth middleware + rate limiting cobertos
- [ ] Middleware de autenticação (JWT/Bearer) aplicado nas rotas protegidas — explicitado quais são públicas
- [ ] Rate limiting configurado com valores concretos (não `rateLimit({})` sem params)
- [ ] Diferenciação de limites por tipo de endpoint (ex: auth endpoints mais restritivos)
- [ ] `req.user` tipado e disponível nos handlers após middleware
- ❌ NOT delivery-ready: rotas sem auth listadas sem justificação, `rateLimit({ windowMs: 15*60*1000 })` sem `max`
- ✅ Delivery-ready: `rateLimit({ windowMs: 15 * 60 * 1000, max: 100 })` globalmente, `rateLimit({ max: 5 })` em `/api/v1/auth/login` para SAQUEI

---

### Gate 6 — OpenAPI spec + README gerados e populados com dados reais do cliente
- [ ] `openapi.yaml` inclui todos os endpoints com `summary`, `parameters`, `requestBody`, `responses`
- [ ] Exemplos nos schemas usam dados reais do domínio (não `"string"`, `"123"`, `"example"`)
- [ ] README contém: setup, env vars necessárias, como correr localmente, como testar
- [ ] Output usa **NOME DO CLIENTE + dados reais** — zero angle-brackets `<placeholder>` no output final
- ❌ NOT delivery-ready: `example: "string"`, `description: "The id"`, README com `<YOUR_DB_URL>`
- ✅ Delivery-ready: `example: "Lisboa Norte — Cuidado Sénior"`, `DATABASE_URL=postgresql://localhost:5432/cuidai_prod` no `.env.example`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# API Design — Cuidai Plataforma de Cuidadores

## Stack: Node.js + Express + Zod + Prisma

---

## Recursos Mapeados
- Caregiver: id, name, email, region, specializations[], hourly_rate, status
- Booking: id, caregiver_id, family_id, start_date, end_date, status, total_amount
- Review: id, booking_id, rating, comment, created_at

---

## Endpoints Gerados

### Caregivers
GET    /api/v1/caregivers              — Lista com filtros
GET    /api/v1/caregivers/:id          — Perfil completo
POST   /api/v1/caregivers              — Registo (admin only)
PATCH  /api/v1/caregivers/:id          — Update parcial
DELETE /api/v1/caregivers/:id          — Soft delete (status: 'inactive')
GET    /api/v1/caregivers/:id/bookings — Histórico de reservas

### Bookings
GET    /api/v1/bookings                — Lista (filtro por família ou cuidador)
GET    /api/v1/bookings/:id            — Detalhe
POST   /api/v1/bookings                — Criar reserva
PATCH  /api/v1/bookings/:id/status     — Transição de estado
DELETE /api/v1/bookings/:id            — Cancelar (soft)

---

## Validation Schema (Zod)

```typescript
// POST /api/v1/bookings
const createBookingSchema = z.object({
  caregiver_id: z.string().uuid(),
  family_id: z.string().uuid(),
  start_date: z.string().datetime(),
  end_date: z.string().datetime(),
  notes: z.string().max(500).optional(),
  service_type: z.enum(['hourly', 'daily', 'overnight']),
}).refine(d => new Date(d.end_date) > new Date(d.start_date), {
  message: 'end_date deve ser posterior a start_date',
  path: ['end_date'],
})

// PATCH /api/v1/bookings/:id/status
const updateBookingStatusSchema = z.object({
  status: z.enum([
    'pending_confirmation',
    'confirmed',
    'active',
    'completed',
    'cancelled_by_family',
    'cancelled_by_caregiver',
  ]),
  cancellation_reason: z.string().max(300).optional(),
})
```

---

## Error Handler (global middleware)

```typescript
app.use((err: AppError, req: Request, res: Response, _next: NextFunction) => {
  const requestId = req.headers['x-request-id'] || `req_${Date.now()}`

  if (err instanceof ZodError) {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Dados de entrada inválidos',
        details: err.errors.map(e => ({ field: e.path.join('.'), message: e.message })),
        request_id: requestId,
      },
    })
  }

  if (err.code === 'CAREGIVER_UNAVAILABLE') {
    return res.status(409).json({
      error: {
        code: 'CAREGIVER_UNAVAILABLE',
        message: 'Cuidador não disponível para o período 2025-08-01 a 2025-08-07',
        request_id: requestId,
      },
    })
  }

  return res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Erro interno', request_id: requestId },
  })
})
```

---

## Paginação (cursor-based)

```typescript
// GET /api/v1/caregivers?region=lisboa&status=available&limit=20&cursor=abc
{
  "data": [
    { "id": "c8a3f1...", "name": "Maria João Silva", "region": "Lisboa Norte",
      "hourly_rate": 14.50, "rating": 4.8, "status": "available" }
  ],
  "pagination": {
    "has_more": true,
    "next_cursor": "eyJpZCI6ImM5YjRmMiJ9",
    "total": 312,
    "limit": 20
  }
}
```

---

## Rate Limiting

```typescript
// Global
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }))

// Auth endpoints
router.post('/auth/login', rateLimit({ windowMs: 15 * 60 * 1000, max: 5 }), loginHandler)
router.post('/auth/reset-password', rateLimit({ windowMs: 60 * 60 * 1000, max: 3 }), resetHandler)
```

---

## OpenAPI excerpt (openapi.yaml)

```yaml
paths:
  /api/v1/bookings:
    post:
      summary: Criar reserva de cuidador
      tags: [Bookings]
      requestBody:
        required: true
        content:
          application/json:
            example:
              caregiver_id: "c8a3f1b2-1234-4abc-8def-9f0a1b2c3d4e"
              family_id: "f1e2d3c4-5678-4bcd-9ef0-1a2b3c4d5e6f"
              start_date: "2025-08-01T09:00:00Z"
              end_date: "2025-08-07T18:00:00Z"
              service_type: "daily"
      responses:
        '201':
          description: Reserva criada com sucesso
        '409':
          description: Cuidador indisponível no período
```
```

---

## Output anti-patterns

- Endpoints sem `/api/v1/` — qualquer route sem versionamento é breaking change à espera de acontecer
- List endpoints que retornam array directo sem wrapper `{ data, pagination }` — cliente parte quando dataset cresce
- Schemas Zod/Pydantic com `z.string()` sem constraints — aceita `""`, `"   "`, strings de 50k chars
- Error responses inconsistentes entre routes — alguns com `{ message }`, outros com `{ error }`, outros com `{ detail }`
- Auth middleware aplicado globalmente sem explicitar quais rotas são públicas — ambiguidade que vira bug de segurança
- Rate limiting sem valores concretos (`rateLimit({})`) — configuração vazia não protege nada
- OpenAPI spec com `example: "string"` em todos os campos — inútil para onboarding de developers
- README com `<YOUR_DATABASE_URL>`, `<API_KEY>` sem mostrar formato real esperado
- Misturar cursor-based e offset-based pagination no mesmo projecto sem justificação
- Soft delete implementado em algumas rotas e hard delete noutras sem convenção documentada
