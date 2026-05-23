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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — VPS e ambiente especificados
- [ ] Provider do VPS indicado (Hetzner, DigitalOcean, OVH, Contabo, etc.)
- [ ] Specs do servidor documentadas (CPU, RAM, disco mínimo)
- [ ] SO e versão confirmados (Ubuntu 22.04/24.04, Debian 12)
- [ ] Porta 8000 (Coolify dashboard) e 443/80 abertas no firewall

❌ NOT delivery-ready: `"Instalar num VPS qualquer com specs adequadas"`
✅ Delivery-ready: `"Hetzner CX22 — 2 vCPU, 4GB RAM, 40GB SSD, Ubuntu 22.04 — firewall rules: 22, 80, 443, 8000 abertas"`

---

### Gate 2 — Coolify install e versão validados
- [ ] Comando de install com versão ou flag de versão estável
- [ ] URL do dashboard gerado após install (ex: `http://IP:8000`)
- [ ] Admin email e password inicial documentados (ou geração automática confirmada)
- [ ] SSH key adicionada ao Coolify para acesso ao servidor

❌ NOT delivery-ready: `"Correr o script de install e configurar"`
✅ Delivery-ready: `"Coolify v4.x instalado em 194.233.81.42:8000 — admin: deploy@cuidai.pt — SSH key /root/.ssh/id_ed25519 adicionada ao server resource"`

---

### Gate 3 — Projecto conectado e build pack definido
- [ ] Repositório GitHub/GitLab ligado (org + repo name explícitos)
- [ ] Build pack selecionado: Nixpacks / Dockerfile / Docker Compose / Static
- [ ] Branch de deploy configurada (main/production/deploy)
- [ ] Webhook de auto-deploy ativado e URL do webhook documentado

❌ NOT delivery-ready: `"Conectar o repositório e escolher o build pack certo"`
✅ Delivery-ready: `"github.com/saquei-pt/app-backend — branch: main — Nixpacks (Node 20 auto-detetado) — webhook: https://coolify.saquei.pt/api/v1/webhooks/abc123 adicionado ao GitHub"`

---

### Gate 4 — Docker Compose / Dockerfile entregue e funcional
- [ ] `docker-compose.yml` ou `Dockerfile` presentes com nomes de serviços reais do cliente
- [ ] Healthcheck definido no serviço principal (`/api/health` ou equivalente)
- [ ] Volumes nomeados (não anónimos) para dados persistentes
- [ ] Network interna entre serviços definida se multi-container

❌ NOT delivery-ready: `"services: app: build: . db: image: postgres"` (sem healthcheck, sem volumes nomeados)
✅ Delivery-ready: `"services: cuidai-api (healthcheck: /api/health, interval 30s), cuidai-db (postgres:16, volume: cuidai_pg_data), network: cuidai-internal"`

---

### Gate 5 — Domínio, SSL e variáveis de ambiente
- [ ] Domínio custom configurado no Coolify (FQDN explícito)
- [ ] Let's Encrypt SSL ativado e certificado emitido confirmado
- [ ] Todas as ENV vars listadas (sem valores secretos expostos no output — usar `***`)
- [ ] Redirect HTTP → HTTPS ativo

❌ NOT delivery-ready: `"Configurar domínio e SSL no painel — adicionar as variáveis necessárias"`
✅ Delivery-ready: `"app.tributario.ai → SSL Let's Encrypt emitido — ENV: DATABASE_URL=*** OPENAI_KEY=*** JWT_SECRET=*** NODE_ENV=production — HTTP→HTTPS redirect: ativo"`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Zero placeholders tipo `<your-domain>`, `<repo>`, `<password>`, `<vps-ip>`
- [ ] Nome do projecto/cliente aparece nos nomes de serviços, volumes e domínios
- [ ] Checklist pós-deploy preenchida com próximos passos concretos (não genéricos)
- [ ] Backups e monitoring configurados ou explicitamente agendados com data

❌ NOT delivery-ready: `"Domain: <client-domain> — DB volume: <app>_pg_data — backup: configure as needed"`
✅ Delivery-ready: `"Domain: app.arrecada.gov.pt — DB volume: arrecada_pg_data — Coolify backup S3 ativo diariamente às 03h00 para bucket arrecada-backups-prod"`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / dados do cliente / infra existente
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — estimativa por design (não verificável até deploy real)

Output checklist upfront mostra ao reader exatamente o que é trust-as-is vs o que precisa verify antes de ir a produção. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready: `"Coolify instalado em 194.233.81.42, domínio app.cliente.pt com SSL ativo, custo ~€15/mês, deploy em ~3 min"` — reader assume tudo verificado, mas IP pode ser placeholder, SSL pode não ter propagado, custo é estimativa.

✅ Delivery-ready:
- 🔵 **verified** — `github.com/cliente-pt/app-backend`, branch `main`, Nixpacks Node 20 auto-detetado (confirmado em sessão anterior)
- 🟡 **assumed** — Hetzner CX22 a €4.15/mês (plano atual do cliente não confirmado); porta 8000 aberta no firewall (não testado)
- 🟢 **projection** — SSL Let's Encrypt emitido em ~2 min após DNS propagar; custo VPS fixo vs Vercel break-even estimado em ~3 apps simultâneas

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — specs do VPS, firewall rules e provider validados com cliente antes de correr install script
- [ ] All 🔵 citations added — repo URL, branch, webhook URL e admin email documentados com fonte (sessão / painel Coolify)
- [ ] All 🟢 projections labeled as such ao cliente — deixar claro que tempo de SSL e estimativas de custo são forecasts, não garantias

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Deploy Coolify — SAQUEI Backend API

## Servidor
- **Provider:** Hetzner CX32 — 4 vCPU, 8GB RAM, 80GB SSD
- **IP:** 65.108.44.21 | **SO:** Ubuntu 22.04 LTS
- **Coolify:** v4.0.0-beta.338 instalado em https://coolify.saquei.pt:8000
- **Admin:** infra@saquei.pt (password gerada no install, alterada no 1º login)

## Install
```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
# Dashboard disponível: http://65.108.44.21:8000
```

## Projecto Ligado
- **Repo:** github.com/saquei-pt/saquei-api (branch: main)
- **Build pack:** Dockerfile (Node 20 + Fastify)
- **Webhook:** https://coolify.saquei.pt/api/v1/webhooks/sq-prod-7f3a2b
  → Adicionado em GitHub → Settings → Webhooks ✅

## docker-compose.yml
```yaml
services:
  saquei-api:
    build: .
    ports: ["3000:3000"]
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks: [saquei-internal]

  saquei-db:
    image: postgres:16-alpine
    volumes: ["saquei_pg_data:/var/lib/postgresql/data"]
    environment:
      - POSTGRES_DB=saquei_prod
      - POSTGRES_USER=saquei_app
    networks: [saquei-internal]

  saquei-redis:
    image: redis:7-alpine
    volumes: ["saquei_redis_data:/data"]
    networks: [saquei-internal]

volumes:
  saquei_pg_data:
  saquei_redis_data:

networks:
  saquei-internal:
```

## Variáveis de Ambiente (Coolify → Environment)
| Key | Value |
|-----|-------|
| DATABASE_URL | *** (postgres://saquei_app:***@saquei-db:5432/saquei_prod) |
| REDIS_URL | *** (redis://saquei-redis:6379) |
| JWT_SECRET | *** |
| STRIPE_KEY | *** |
| NODE_ENV | production |

## Domínio & SSL
- **FQDN:** api.saquei.pt → 65.108.44.21
- **SSL:** Let's Encrypt — certificado emitido 2025-07-14 ✅
- **HTTP→HTTPS redirect:** ativo ✅

## Post-Deploy Checklist
- [x] `GET https://api.saquei.pt/api/health` → `{"status":"ok","db":"connected"}`
- [x] SSL válido (expira 2025-10-12, auto-renovação ativa)
- [x] Backup S3 configurado — diário às 03h00 → bucket `saquei-coolify-backups`
- [x] Webhook testado — push para main dispara deploy em ~90s
- [ ] Monitoring: UptimeRobot configurar para api.saquei.pt/api/health (pendente)
```

---

## Output anti-patterns

- Deixar `<your-domain>`, `<vps-ip>` ou `<repo-name>` no output final — o cliente recebe placeholders inutilizáveis
- `docker-compose.yml` sem healthcheck — Coolify não sabe quando o container está realmente pronto
- Volumes anónimos (`- /var/lib/postgresql/data`) em vez de nomeados — dados perdidos no redeploy
- Listar variáveis de ambiente sem indicar quais são obrigatórias vs opcionais — bloqueia o primeiro deploy
- Omitir o webhook URL após setup — cliente não sabe como activar o auto-deploy
- Dockerfile genérico copiado do SKILL.md sem adaptar ao stack real do cliente (Node vs Python vs PHP)
- Confirmar SSL como "configurado" sem verificar que o certificado foi efectivamente emitido (Let's Encrypt tem rate limits)
- Post-deploy checklist com itens vagos tipo "verificar que está a funcionar" sem URL e resposta esperada
- Não documentar a porta do dashboard Coolify (8000) — cliente fica sem saber como aceder ao painel
