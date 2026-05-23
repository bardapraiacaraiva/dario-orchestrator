---
name: builder-auth-system
description: >
  Gera sistema de autenticacao completo: JWT, sessions, OAuth, RBAC, middleware,
  password hashing, refresh tokens, rate limiting. Production-ready security.
  Use quando: autenticacao, login, register, JWT, OAuth, roles, permissoes, auth.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Authentication System

## Proposito
Gerar auth PRODUCTION-READY — nao tutoriais basicos. JWT + refresh tokens + RBAC + rate limiting.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-auth-system jwt` | JWT + refresh tokens |
| `/builder-auth-system session` | Session-based auth |
| `/builder-auth-system oauth [provider]` | OAuth2 (Google, GitHub, etc) |
| `/builder-auth-system clerk` | Clerk integration (managed auth) |

## Output por tipo

### JWT Flow
```
POST /auth/register    → hash password, create user, return tokens
POST /auth/login       → verify password, return access + refresh tokens
POST /auth/refresh     → verify refresh, rotate both tokens
POST /auth/logout      → blacklist refresh token
GET  /auth/me          → return current user (from token)
```

### Security Requirements
- Password: bcrypt/argon2 (NUNCA MD5/SHA)
- Access token: 15 min expiry, JWT RS256
- Refresh token: 7 day expiry, stored in DB, rotated on use
- Rate limit: 5 login attempts per 15 min per IP
- CORS: whitelist origins only
- CSRF: SameSite cookies or double-submit token

### RBAC (Role-Based Access Control)
```typescript
const roles = {
  admin:  ['read', 'write', 'delete', 'manage_users', 'manage_billing'],
  member: ['read', 'write'],
  viewer: ['read'],
} as const

// Middleware
function requireRole(...roles: Role[]) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) return res.status(403).json({error: 'Forbidden'})
    next()
  }
}

// Usage
router.delete('/projects/:id', requireRole('admin'), deleteProject)
```

## Output
1. Auth routes (register, login, refresh, logout, me)
2. JWT utility (sign, verify, decode)
3. Password utility (hash, compare)
4. Auth middleware (requireAuth, requireRole)
5. Rate limiter middleware
6. CORS config

## Red Flags
- Passwords em plaintext ou MD5/SHA — NUNCA, usar bcrypt/argon2
- JWT sem expiry — token eterno = sessao eterna
- Refresh token sem rotacao — replay attacks
- Sem rate limiting no login — brute force vulnerability
- Secrets em codigo — SEMPRE usar env vars
- CORS com * em producao — qualquer site pode chamar a API

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Password hashing é seguro e verificável
- [ ] Usa bcrypt (cost ≥ 12) ou argon2id — nunca MD5, SHA-1, SHA-256 bare
- [ ] Hash gerado é visível no output (ex: `$2b$12$...` ou `$argon2id$...`)
- [ ] Função `compare` usa timing-safe comparison (não `===` direto)
- [ ] Salt é gerado automaticamente pela lib (nunca hardcoded)
- ❌ NOT delivery-ready: `const hash = sha256(password)` ou `bcrypt.hash(password, 8)`
- ✅ Delivery-ready: `const hash = await bcrypt.hash(password, 12)` com import `bcryptjs@^2.4.3` em `package.json`

### Gate 2 — JWT configurado para produção (não tutorial)
- [ ] Access token expiry: ≤ 15 min (`expiresIn: '15m'`)
- [ ] Algoritmo: RS256 (assimétrico) ou HS256 com secret ≥ 32 chars em env var
- [ ] Refresh token: expiry 7 dias, stored na DB com campo `revoked_at`
- [ ] Refresh rotation: ao usar refresh, o antigo é invalidado e novo é emitido
- [ ] Payload do JWT contém apenas `sub`, `role`, `iat`, `exp` — não inclui password hash ou dados sensíveis
- ❌ NOT delivery-ready: `jwt.sign({ user }, 'secret')` sem expiry, secret hardcoded
- ✅ Delivery-ready: `jwt.sign({ sub: user.id, role: user.role }, process.env.JWT_SECRET, { expiresIn: '15m', algorithm: 'HS256' })`

### Gate 3 — Rate limiting e proteção brute-force implementados
- [ ] Rate limiter no endpoint `/auth/login`: máx 5 tentativas / 15 min / IP
- [ ] Rate limiter no `/auth/register`: máx 3 requests / hora / IP
- [ ] Resposta 429 inclui header `Retry-After` com segundos restantes
- [ ] Implementação usa `express-rate-limit` + `rate-limit-redis` (ou `memory` em dev com aviso)
- ❌ NOT delivery-ready: sem rate limiter, ou `windowMs: 60000, max: 100` (muito permissivo)
- ✅ Delivery-ready: `rateLimit({ windowMs: 15 * 60 * 1000, max: 5, message: { error: 'Too many attempts. Try again in 15 minutes.' } })`

### Gate 4 — RBAC implementado com roles reais do cliente
- [ ] Roles definidas correspondem ao domínio do cliente (ex: Cuidai: `caregiver/family/admin`; Tributario.AI: `accountant/client/admin`)
- [ ] Middleware `requireRole` rejeita com 403 (não 401) quando role insuficiente
- [ ] Permissões são granulares e listadas explicitamente (não só `true/false`)
- [ ] Pelo menos um exemplo de rota protegida por role está incluído no output
- ❌ NOT delivery-ready: `roles: ['admin', 'user']` genérico sem ligação ao domínio do cliente
- ✅ Delivery-ready: `const roles = { admin: ['read','write','delete','manage_users','manage_billing'], accountant: ['read','write','export'], client: ['read'] }` (Tributario.AI)

### Gate 5 — CORS e variáveis de ambiente production-safe
- [ ] CORS whitelist contém apenas origins reais do cliente (nunca `*` em prod)
- [ ] Todos os secrets referenciados via `process.env.NOME_VAR` com nome explícito
- [ ] Ficheiro `.env.example` gerado com todas as vars necessárias (valores placeholder, não secrets reais)
- [ ] `credentials: true` nas CORS options se usar cookies
- ❌ NOT delivery-ready: `cors({ origin: '*' })` ou `JWT_SECRET=mysecret` hardcoded no código
- ✅ Delivery-ready: `cors({ origin: ['https://app.cuidai.pt', 'https://admin.cuidai.pt'], credentials: true })` + `.env.example` com `JWT_SECRET=`, `REFRESH_SECRET=`, `DATABASE_URL=`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Sem `<your-app>`, `<client>`, `<domain>`, `<secret>` no output final
- [ ] Nome da app/projeto aparece em comments, prefixos de env var, e origem CORS
- [ ] Stack tecnológica corresponde ao projeto real do cliente (Node/Express, Next.js, FastAPI, etc.)
- [ ] Endpoints seguem convenção de nomenclatura já existente no projeto (se aplicável)
- ❌ NOT delivery-ready: `origin: 'https://<your-domain>.com'` ou `APP_NAME=<your-app>`
- ✅ Delivery-ready: `origin: 'https://app.tributario.ai'`, `TRIBUTARIO_JWT_SECRET=`, comentários com `// Tributario.AI — Auth System v1`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output de auth deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado do codebase/sessão do cliente (ex: algoritmo JWT já em uso, versão da lib)
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — decisão de design/security default (não verificável até deploy)

Output checklist upfront mostra o reader exactamente o que é trust-as-is vs o que precisa ser validado. **Honest transparency > auth system que parece completo mas tem assumptions enterradas.**

❌ NOT delivery-ready:
```
bcrypt cost factor: 12
JWT secret: process.env.JWT_SECRET
Roles: admin / member / viewer
Refresh token expiry: 7 dias
Rate limit: 5 tentativas / 15 min
```
*(reader assume que tudo é real — mas as roles são genéricas, o secret pode não existir no .env do cliente, e o cost factor foi escolhido arbitrariamente)*

✅ Delivery-ready:
```
🟡 bcrypt cost factor: 12 — assumed (validar se infra do cliente aguenta; reduzir p/ 10 em edge functions)
🔵 JWT secret: process.env.JWT_SECRET — verified (confirmado no .env.example do repo do cliente)
🟡 Roles: admin / member / viewer — assumed (cliente usa estes nomes? confirmar antes de hardcodar middleware)
🟢 Refresh token expiry: 7 dias — projection by design (OWASP default; ajustável por política do cliente)
🟡 Rate limit store: memory (dev) — assumed (produção precisa Redis; confirmar se cliente tem instância)
```

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — roles reais substituídas nos enums, env vars existem no ambiente target, rate limit store validada
- [ ] Todos os itens 🔵 têm fonte citada — versão da lib (`bcryptjs@^2.4.3`), algoritmo JWT (`HS256`/`RS256`), nome real das env vars
- [ ] Todos os itens 🟢 comunicados explicitamente ao cliente como defaults de design — não assumir que o cliente sabe que refresh expiry e cost factor são configuráveis

## Fully-worked A-tier example (delivery-ready reference)

```markdown
// Tributario.AI — Authentication System
// Stack: Node.js + Express + Prisma + PostgreSQL
// Generated: 2024-01

// === .env.example ===
DATABASE_URL=postgresql://user:pass@localhost:5432/tributario
JWT_SECRET=                        # min 32 chars, openssl rand -hex 32
REFRESH_SECRET=                    # diferente do JWT_SECRET
JWT_EXPIRES_IN=15m
REFRESH_EXPIRES_IN=7d
ALLOWED_ORIGINS=https://app.tributario.ai,https://admin.tributario.ai

// === src/config/cors.ts ===
import cors from 'cors'

export const corsConfig = cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') ?? [],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
})

// === src/lib/password.ts ===
import bcrypt from 'bcryptjs' // ^2.4.3

const BCRYPT_ROUNDS = 12

export async function hashPassword(plain: string): Promise<string> {
  return bcrypt.hash(plain, BCRYPT_ROUNDS)
}

export async function verifyPassword(plain: string, hash: string): Promise<boolean> {
  return bcrypt.compare(plain, hash) // timing-safe internamente
}

// === src/lib/jwt.ts ===
import jwt from 'jsonwebtoken'

type TokenPayload = { sub: string; role: TributarioRole }

export function signAccessToken(payload: TokenPayload): string {
  return jwt.sign(payload, process.env.JWT_SECRET!, {
    expiresIn: process.env.JWT_EXPIRES_IN ?? '15m',
    algorithm: 'HS256',
  })
}

export function signRefreshToken(payload: { sub: string }): string {
  return jwt.sign(payload, process.env.REFRESH_SECRET!, {
    expiresIn: process.env.REFRESH_EXPIRES_IN ?? '7d',
    algorithm: 'HS256',
  })
}

export function verifyAccessToken(token: string): TokenPayload {
  return jwt.verify(token, process.env.JWT_SECRET!) as TokenPayload
}

// === src/lib/rbac.ts ===
export type TributarioRole = 'admin' | 'accountant' | 'client'

const PERMISSIONS = {
  admin:      ['read', 'write', 'delete', 'manage_users', 'manage_billing', 'export'],
  accountant: ['read', 'write', 'export'],
  client:     ['read'],
} as const

export function requireRole(...roles: TributarioRole[]) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden: insufficient role' })
    }
    next()
  }
}

// === src/middleware/rateLimiter.ts ===
import rateLimit from 'express-rate-limit'

export const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 min
  max: 5,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many login attempts. Try again in 15 minutes.' },
  keyGenerator: (req) => req.ip ?? 'unknown',
})

export const registerLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hora
  max: 3,
  message: { error: 'Too many registrations from this IP.' },
})

// === src/routes/auth.ts ===
router.post('/auth/register', registerLimiter, async (req, res) => {
  const { email, password, role = 'client' } = req.body
  const hash = await hashPassword(password)
  const user = await prisma.user.create({ data: { email, passwordHash: hash, role } })
  const accessToken  = signAccessToken({ sub: user.id, role: user.role })
  const refreshToken = signRefreshToken({ sub: user.id })
  await prisma.refreshToken.create({ data: { token: refreshToken, userId: user.id } })
  res.status(201).json({ accessToken, refreshToken })
})

router.post('/auth/login', loginLimiter, async (req, res) => {
  const { email, password } = req.body
  const user = await prisma.user.findUnique({ where: { email } })
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    return res.status(401).json({ error: 'Invalid credentials' })
  }
  const accessToken  = signAccessToken({ sub: user.id, role: user.role })
  const refreshToken = signRefreshToken({ sub: user.id })
  await prisma.refreshToken.create({ data: { token: refreshToken, userId: user.id } })
  res.json({ accessToken, refreshToken })
})

router.post('/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body
  const stored = await prisma.refreshToken.findUnique({ where: { token: refreshToken } })
  if (!stored || stored.revokedAt) return res.status(401).json({ error: 'Invalid refresh token' })
  const payload = jwt.verify(refreshToken, process.env.REFRESH_SECRET!) as { sub: string }
  const user = await prisma.user.findUnique({ where: { id: payload.sub } })
  // Rotate: revogar antigo, emitir novo par
  await prisma.refreshToken.update({ where: { token: refreshToken }, data: { revokedAt: new Date() } })
  const newAccess  = signAccessToken({ sub: user!.id, role: user!.role })
  const newRefresh = signRefreshToken({ sub: user!.id })
  await prisma.refreshToken.create({ data: { token: newRefresh, userId: user!.id } })
  res.json({ accessToken: newAccess, refreshToken: newRefresh })
})

// Rota protegida — exemplo Tributario.AI
router.delete('/declarations/:id', requireAuth, requireRole('admin', 'accountant'), deleteDeclaration)
```

---

## Output anti-patterns

- `jwt.sign({ user }, 'secret')` — secret hardcoded, sem expiry, payload com objeto inteiro do user (expõe dados)
- `bcrypt.hash(password, 8)` — cost factor 8 é insuficiente em 2024; mínimo 12
- `cors({ origin: '*' })` em produção — qualquer domínio pode chamar a API com credenciais
- Refresh token sem campo `revoked_at` na DB — impossível invalidar tokens comprometidos
- Rate limiter em memória sem aviso — não sobrevive a restart ou multi-instance (usar Redis em prod)
- Roles genéricas `['admin', 'user']` sem ligação ao domínio real do cliente — não reflete permissões reais do negócio
- `.env` com secrets reais committed — deve existir apenas `.env.example` no output
- `return res.status(401)` quando role é insuficiente — deve ser 403 Forbidden, não 401 Unauthorized
- `if (user.password === password)` — comparação plaintext, sem hash, crítico
- Refresh token com `expiresIn: '30d'` ou sem expiry — janela de ataque desnecessariamente longa
