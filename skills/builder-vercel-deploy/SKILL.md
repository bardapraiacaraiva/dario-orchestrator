---
name: builder-vercel-deploy
description: >
  Deploy completo para Vercel: configuracao, env vars, dominio, preview URLs, edge config.
  Gera vercel.json, configura projecto, e faz deploy. Tambem suporta VPS com Docker.
  Use quando: deploy, publicar, colocar online, vercel, hospedar, subir para producao.
tools: Read, Write, Edit, Bash, Glob
version: 1.0
---

# BUILDER — Deploy to Production

## Proposito

Levar uma app do `localhost:3000` para producao acessivel na internet.
Suporta dois caminhos:
1. **Vercel** (recomendado para Next.js) — zero-config, preview URLs, edge
2. **VPS + Docker** (para backends, APIs, stacks custom) — nginx + SSL + systemd

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/builder-vercel-deploy` | Deploy Next.js para Vercel |
| `/builder-vercel-deploy vps` | Deploy para VPS com Docker |
| `/builder-vercel-deploy check` | Verificar se projecto esta pronto para deploy |

## Workflow Vercel

### 1. Pre-Deploy Checklist
```
- [ ] next build passa sem erros
- [ ] .env.example tem todas as vars documentadas
- [ ] Env vars de producao definidas
- [ ] Metadata/OG tags configurados
- [ ] Sitemap.xml gerado
- [ ] Robots.txt correcto
- [ ] Favicon + OG image presentes
- [ ] Error boundaries implementados
- [ ] Analytics configurado
```

### 2. vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["cdg1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
      ]
    }
  ]
}
```

### 3. Deploy Commands

```bash
# Login (first time)
vercel login

# Link project
vercel link

# Set env vars
vercel env add DATABASE_URL production
vercel env add NEXT_PUBLIC_SITE_URL production

# Preview deploy
vercel

# Production deploy
vercel --prod

# Custom domain
vercel domains add yourdomain.com
```

### 4. Post-Deploy Verification
```
- [ ] Site acessivel via URL
- [ ] HTTPS funcional
- [ ] OG tags correctos (usar ogp.me para verificar)
- [ ] Paginas principais carregam sem erros
- [ ] Forms/CTAs funcionais
- [ ] Analytics a receber dados
- [ ] Core Web Vitals aceitaveis
```

## Workflow VPS + Docker

### 1. Dockerfile

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

### 2. docker-compose.yml

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    env_file:
      - .env.production
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 3. Nginx + SSL

```bash
# Nginx reverse proxy
sudo cp nginx.conf /etc/nginx/sites-available/[project]
sudo ln -s /etc/nginx/sites-available/[project] /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# SSL via Certbot
sudo certbot --nginx -d yourdomain.com
```

## Integration

| Depende de | Para que |
|---|---|
| `builder-nextjs-app` | O projecto a deployar |
| `builder-ci-cd` | Pipeline automatico (futuro) |
| `seo-technical` | Validacao pos-deploy |

## Red Flags
- Deploy sem env vars de producao — app crasha
- Sem HTTPS — browsers bloqueiam, SEO penalizado
- Sem health check — nao sabe se app esta UP
- Deploy de sexta a tarde — Murphy's law
- Sem preview URL primeiro — bugs directo em producao
- Esquecer security headers — vulneravel a XSS/clickjacking
