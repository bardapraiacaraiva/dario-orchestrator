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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Ficheiros completos e não truncados
- [ ] Os 5 ficheiros obrigatórios estão presentes: `docker-compose.yml`, `docker-compose.dev.yml`, `Dockerfile`, `.dockerignore`, `.env.example`
- [ ] Nenhum ficheiro termina com `...` ou `# adicionar mais serviços`
- [ ] `docker-compose.dev.yml` tem hot-reload configurado (volume mount do source code + comando de dev)
- [ ] `.env.example` lista **todas** as variáveis referenciadas nos compose files

❌ NOT delivery-ready: `# TODO: adicionar healthcheck` ou ficheiro com apenas o serviço `app` sem `db`
✅ Delivery-ready: `docker-compose.yml` com `app`, `db: postgres:16-alpine`, `redis: redis:7-alpine`, volumes, healthchecks e `restart: unless-stopped` em todos os serviços

---

### Gate 2 — Segurança: sem root, sem secrets expostos
- [ ] Dockerfile cria utilizador não-root e termina com `USER <nome>` (ex: `USER nextjs`, `USER appuser`)
- [ ] Nenhuma password hardcoded — todas as credenciais via `${VAR}` com fallback seguro ou sem fallback
- [ ] `.dockerignore` inclui: `.env`, `node_modules`, `.git`, `*.log`, `.next` (se Next.js)
- [ ] Variáveis sensíveis no `.env.example` têm valor placeholder `CHANGE_ME` e não valor real

❌ NOT delivery-ready: `POSTGRES_PASSWORD: mysecretpassword` hardcoded no compose ou `USER root` no Dockerfile
✅ Delivery-ready: `POSTGRES_PASSWORD: ${DB_PASSWORD}` no compose + `.env.example` com `DB_PASSWORD=CHANGE_ME`

---

### Gate 3 — Health checks e dependências correctas
- [ ] Todos os serviços com estado (DB, cache) têm `healthcheck` com `test`, `interval`, `timeout`, `retries`
- [ ] Serviços que dependem de DB usam `depends_on: db: { condition: service_healthy }` e não apenas `depends_on: db`
- [ ] Healthcheck do `app` aponta para endpoint real (ex: `/api/health`, `/healthz`) e não para `/`
- [ ] `restart: unless-stopped` presente em todos os serviços de produção

❌ NOT delivery-ready: `depends_on: [db]` sem condition, ou healthcheck com `test: ["CMD", "echo", "ok"]`
✅ Delivery-ready: `test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-cuidai}"]` com `interval: 10s`, `retries: 5`

---

### Gate 4 — Multi-stage Dockerfile optimizado
- [ ] Dockerfile tem mínimo 2 stages (deps/builder/runner ou equivalente)
- [ ] Stage final usa imagem `*-alpine` ou `*-slim` — não imagem base full
- [ ] `node_modules` de dev NÃO estão na imagem de produção (`npm ci --only=production` ou `--omit=dev`)
- [ ] `COPY` do código fonte acontece depois das dependências para aproveitar layer cache

❌ NOT delivery-ready: `FROM node:22` (sem alpine) com `COPY . .` antes de `npm install` — invalida cache sempre
✅ Delivery-ready: 3 stages (deps → builder → runner), imagem final `node:22-alpine`, `COPY --from=builder --chown=nextjs:nodejs`

---

### Gate 5 — Volumes e persistência de dados
- [ ] Bases de dados têm named volume (não bind mount) para dados: `postgres_data:/var/lib/postgresql/data`
- [ ] Named volumes declarados na secção `volumes:` no final do compose
- [ ] `docker-compose.dev.yml` usa bind mounts para o código fonte (hot-reload), não para dados
- [ ] Nenhum dado de DB mapeado para path relativo como `./data` em produção

❌ NOT delivery-ready: sem secção `volumes:` no compose, ou DB sem volume algum (data loss on restart)
✅ Delivery-ready: `volumes: postgres_data:` declarado + `- postgres_data:/var/lib/postgresql/data` no serviço `db`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nomes de base de dados, utilizadores e imagens reflectem o projecto real (ex: `cuidai_db`, `POSTGRES_DB: saquei`, `image: atrium-api`)
- [ ] Portas são as reais do projecto — não `3000` genérico se o cliente usa `8080`
- [ ] Nenhum placeholder do tipo `<your-app>`, `<DB_NAME>`, `[PROJECT]` presente no output final
- [ ] Se stack inclui proxy (Nginx/Traefik), domínio é o real do cliente e não `example.com`

❌ NOT delivery-ready: `POSTGRES_DB: myapp` ou `image: my-api:latest` ou `- <HOST_PORT>:3000`
✅ Delivery-ready: `POSTGRES_DB: cuidai_prod`, `image: cuidai-backend:1.0`, `ports: ["8080:8080"]`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado do projecto do cliente (package.json, código existente, infra actual)
- 🟡 **assumed** — plausível para o stack gerado, mas precisa confirmação antes de entregar
- 🟢 **projection** — decisão de design/defaults razoáveis (não verificável sem deploy real)

Output checklist upfront mostra ao cliente exactamente o que é trust-as-is vs. o que precisa de verify antes de fazer `docker compose up --build` em produção. **Honest transparency > stack que parte no primeiro deploy.**

❌ NOT delivery-ready: `postgres:16-alpine`, porta `5432`, `POSTGRES_USER=app`, `NODE_ENV=production` — todos sem labels, cliente assume que foram extraídos do projecto real quando são defaults assumidos.

✅ Delivery-ready:
- 🔵 **verified** — `node:22-alpine` (confirmado via `package.json` → `"engines": { "node": "22" }` no repo do cliente)
- 🟡 **assumed** — `POSTGRES_DB=app` (nome da base de dados não especificado — confirmar antes de deploy; substituir em `.env.example`)
- 🟡 **assumed** — healthcheck endpoint `/api/health` (rota assumida como existente — confirmar que está implementada na app)
- 🟡 **assumed** — porta `3000` exposta (confirmar que a app não usa `PORT` env var diferente)
- 🟢 **projection** — `restart: unless-stopped` em todos os serviços (best-practice por design; comportamento real depende do orquestrador/hosting)
- 🟢 **projection** — imagem final ~150 MB com multi-stage build (estimativa típica para Next.js standalone; valor real após primeiro `docker build`)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — `DB_NAME`, `DB_USER`, endpoint de healthcheck e porta da app actualizados com valores reais antes de `docker compose up`
- [ ] All 🔵 citations added — versão Node, versão Postgres e variáveis de ambiente extraídas do repo/infra do cliente documentadas no PR/handoff
- [ ] All 🟢 projections labeled as such ao cliente — deixar claro que `restart` policy e tamanho de imagem são defaults/estimativas, validar após primeiro build em staging

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Docker Compose Stack — Cuidai Platform

## docker-compose.yml (production)

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
    image: cuidai-api:1.0
    ports: ["8080:8080"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    volumes: ["cuidai_postgres:/var/lib/postgresql/data"]
    environment:
      POSTGRES_DB: ${DB_NAME:-cuidai_prod}
      POSTGRES_USER: ${DB_USER:-cuidai}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-cuidai}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes: ["cuidai_redis:/data"]
    healthcheck:
      test: ["CMD", "redis-cli", "--no-auth-warning", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped

volumes:
  cuidai_postgres:
  cuidai_redis:

## docker-compose.dev.yml (development)

services:
  app:
    build:
      context: .
      target: deps
    command: npm run dev
    volumes:
      - .:/app
      - /app/node_modules
    ports: ["8080:8080"]
    environment:
      NODE_ENV: development
    env_file: .env.local
    depends_on:
      db: { condition: service_healthy }

  db:
    image: postgres:16-alpine
    volumes: ["cuidai_postgres_dev:/var/lib/postgresql/data"]
    environment:
      POSTGRES_DB: cuidai_dev
      POSTGRES_USER: cuidai
      POSTGRES_PASSWORD: devpassword123
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cuidai"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  cuidai_postgres_dev:

## Dockerfile

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
ENV PORT=8080
RUN addgroup -g 1001 -S cuidai && adduser -S cuidai -u 1001 -G cuidai
COPY --from=builder --chown=cuidai:cuidai /app/dist ./dist
COPY --from=deps --chown=cuidai:cuidai /app/node_modules ./node_modules
COPY --from=builder --chown=cuidai:cuidai /app/package.json ./
USER cuidai
EXPOSE 8080
CMD ["node", "dist/server.js"]

## .dockerignore

node_modules
.next
.git
*.log
.env
.env.local
coverage
dist
.DS_Store

## .env.example

# Cuidai Platform — Environment Variables
# Copiar para .env e preencher TODOS os valores CHANGE_ME

DB_NAME=cuidai_prod
DB_USER=cuidai
DB_PASSWORD=CHANGE_ME

REDIS_PASSWORD=CHANGE_ME

NODE_ENV=production
PORT=8080
```

---

## Output anti-patterns

- Entregar `docker-compose.yml` sem `docker-compose.dev.yml` — cliente fica sem ambiente de desenvolvimento funcional
- `depends_on: [db]` sem `condition: service_healthy` — app arranca antes do Postgres estar pronto e crasha
- Dockerfile sem stage final `AS runner` — imagem de produção inclui devDependencies e código fonte raw (imagem 3-5x maior)
- Password de DB hardcoded no compose (`POSTGRES_PASSWORD: admin123`) em vez de variável de ambiente
- `.env.example` com valores reais (`DB_PASSWORD=cuidai2024!`) — segredo exposto no repositório
- Healthcheck do app a apontar para `/` que pode retornar 200 mesmo com DB desconectada
- Volumes de base de dados como bind mounts (`./postgres-data:/var/lib/postgresql/data`) — permissões erradas em Linux, perda de dados em CI
- Dockerfile com `COPY . .` antes de `COPY package*.json` — invalida layer cache em cada mudança de código, builds 3-4x mais lentos
- Stack gerada com nomes genéricos `myapp`, `mydb`, `my-network` sem qualquer referência ao projecto do cliente
