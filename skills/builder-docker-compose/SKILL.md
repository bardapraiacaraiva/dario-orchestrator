---
name: builder-docker-compose
description: >
  Gera Docker Compose stacks completas: app + DB + cache + proxy. Dockerfile multi-stage,
  health checks, volumes, networking. Production e development configs.
  Use quando: docker, containerizar, docker-compose, deploy com docker, criar container.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Docker Compose Stack

## Proposito
Containerizar qualquer aplicacao com Docker Compose — dev e producao.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-docker-compose [stack]` | Stack completa |
| `/builder-docker-compose nextjs` | Next.js + Postgres |
| `/builder-docker-compose node-api` | Node + Postgres + Redis |
| `/builder-docker-compose python-api` | FastAPI + Postgres |
| `/builder-docker-compose wordpress` | WordPress + MySQL + Redis |

## Templates

### Next.js + PostgreSQL
```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports: ["3000:3000"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    volumes: ["postgres_data:/var/lib/postgresql/data"]
    environment:
      POSTGRES_DB: ${DB_NAME:-app}
      POSTGRES_USER: ${DB_USER:-app}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  postgres_data:
```

### Dockerfile (multi-stage)
```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

## Output
1. `docker-compose.yml` (production)
2. `docker-compose.dev.yml` (development with hot-reload)
3. `Dockerfile` (multi-stage, optimized)
4. `.dockerignore`
5. `.env.example`

## Red Flags
- Container como root — security risk
- Sem health checks — orchestrator nao sabe se esta UP
- Sem volumes para DB — data loss on restart
- Sem .dockerignore — node_modules no build context (lento)
- Sem multi-stage build — imagem 10x maior que necessario
