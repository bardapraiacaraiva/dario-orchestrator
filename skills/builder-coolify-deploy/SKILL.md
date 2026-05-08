---
name: builder-coolify-deploy
description: >
  Deploy para Coolify — PaaS self-hosted open-source (52K stars). Alternativa a Vercel
  para projectos que precisam de infra propria. Git push deploy, auto SSL, Docker native,
  280+ templates. Para clientes que querem controlar o servidor.
  Use quando: coolify, self-hosted, deploy vps, alternativa vercel, infra propria, PaaS.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Coolify Self-Hosted Deploy

## Proposito
Deploy para clientes que querem/precisam de controlar a infra. Coolify e o "Vercel self-hosted"
com 52K stars — git push deploy, auto SSL, 280+ templates, Docker native.

## Quando usar Coolify vs Vercel
| Criterio | Vercel | Coolify |
|---|---|---|
| Next.js simple | Melhor | Bom |
| Custom backend | Nao | Melhor |
| Preco a escala | Caro (>$20/mo) | VPS fixo (~EUR 15/mo) |
| Data residency | US/EU Vercel | Onde quiseres |
| Docker compose | Nao | Nativo |
| Multiple apps | 1 por projecto | Ilimitadas |
| Government/compliance | Depende | Full control |

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-coolify-deploy [app]` | Deploy para Coolify |
| `/builder-coolify-deploy setup [vps]` | Instalar Coolify num VPS |
| `/builder-coolify-deploy template [tipo]` | One-click template (Supabase, Pocketbase, etc) |

## Workflow

### 1. Install Coolify on VPS
```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

### 2. Configure Project
- Connect GitHub repo
- Set build pack: Nixpacks (auto-detect) or Dockerfile
- Set environment variables
- Configure domain + auto-SSL

### 3. Docker Compose Stack (if needed)
```yaml
# coolify-compose.yml
services:
  app:
    build: .
    ports: ["3000:3000"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
  db:
    image: postgres:16
    volumes: ["pg_data:/var/lib/postgresql/data"]
```

### 4. Post-Deploy
- Verify SSL
- Configure backups (Coolify built-in)
- Set up monitoring
- Configure webhooks for auto-deploy on push

## Output
1. Coolify project config
2. docker-compose.yml (if multi-service)
3. Dockerfile (if custom)
4. Environment variables list
5. Post-deploy checklist

## Inspired by
- **coollabsio/coolify** (52K stars) — Self-hosted PaaS
- **Dokploy/dokploy** (26K stars) — Alternative self-hosted PaaS
