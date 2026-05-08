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
