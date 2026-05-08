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
