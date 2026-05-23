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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

### Gate 1 — vercel.json está correcto e completo
- [ ] Ficheiro tem `$schema`, `framework`, `regions` definidos
- [ ] Security headers presentes: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`
- [ ] Region escolhida é adequada ao mercado do cliente (PT/EU → `cdg1`, não `iad1`)
- [ ] JSON é válido (sem vírgulas a mais, sem aspas erradas)
- ❌ NOT delivery-ready: `"regions": ["us-east-1"]` para cliente português, sem headers de segurança
- ✅ Delivery-ready: `"regions": ["cdg1"]` com todos os 4 headers para Cuidai — app PT com dados de saúde, DENY em X-Frame-Options obrigatório

### Gate 2 — Env vars de produção documentadas e configuradas
- [ ] `.env.example` lista todas as vars sem valores reais
- [ ] Cada `vercel env add` tem o nome correcto da var e o scope (`production` vs `preview`)
- [ ] `NEXT_PUBLIC_SITE_URL` aponta para o domínio final, não `localhost`
- [ ] Vars sensíveis (DB, API keys) não estão no `vercel.json` nem no repositório
- ❌ NOT delivery-ready: `DATABASE_URL=postgresql://localhost:5432/dev` em produção; `NEXT_PUBLIC_SITE_URL` vazio
- ✅ Delivery-ready: `vercel env add DATABASE_URL production` → valor é `postgresql://neon.tech/cuidai-prod`; `NEXT_PUBLIC_SITE_URL=https://cuidai.pt`

### Gate 3 — Pre-deploy checklist concluída sem excepções
- [ ] `next build` executado localmente sem erros ou warnings críticos
- [ ] `sitemap.xml` e `robots.txt` existem e são acessíveis em `/sitemap.xml` e `/robots.txt`
- [ ] OG image presente em `/public/og-image.png` (mínimo 1200×630px)
- [ ] Favicon existe em múltiplos tamanhos (16, 32, 180px)
- [ ] Error boundaries implementados nas rotas críticas
- ❌ NOT delivery-ready: checklist copiada sem executar; `next build` não foi corrido; OG image é placeholder genérico
- ✅ Delivery-ready: `next build` output sem erros para SAQUEI; `https://saquei.pt/sitemap.xml` retorna 200; ogp.me confirma OG tags corretas

### Gate 4 — Estratégia de deploy respeitada (preview antes de produção)
- [ ] Preview deploy (`vercel`) executado e URL partilhada com cliente para validação
- [ ] Deploy de produção (`vercel --prod`) só feito após aprovação da preview
- [ ] Deploy NÃO foi feito em sexta à tarde ou véspera de feriado
- [ ] Domínio custom adicionado (`vercel domains add`) e propagação DNS verificada
- ❌ NOT delivery-ready: `vercel --prod` directo sem preview; domínio adicionado mas DNS não verificado; deploy às 17h30 de sexta
- ✅ Delivery-ready: preview `tributario-ai-git-main-xyz.vercel.app` aprovada por cliente às 14h quarta; `vercel --prod` às 15h; `tributario.ai` a resolver correctamente

### Gate 5 — Post-deploy verification completa
- [ ] Site acessível via HTTPS (sem warnings de certificado)
- [ ] Core Web Vitals medidos via PageSpeed Insights: LCP < 2.5s, CLS < 0.1
- [ ] Forms e CTAs testados em produção (submissão real, não só visual)
- [ ] Analytics (GA4/Plausible) a receber eventos — verificado no dashboard em tempo real
- [ ] Health check endpoint `/api/health` retorna 200 (se VPS) ou Vercel Functions a responder
- ❌ NOT delivery-ready: "parece estar a funcionar"; analytics não verificado; formulário de contacto não testado em prod
- ✅ Delivery-ready: LCP 1.8s no PageSpeed para Atrium; form de lead testado → email recebido em `geral@atrium.pt`; Plausible mostra 3 pageviews de teste

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Nenhum `[project]`, `yourdomain.com`, `your-api-key` no output final entregue
- [ ] Nome do projecto Vercel reflecte o cliente real (ex: `cuidai-app`, não `my-app`)
- [ ] URLs são os domínios reais confirmados com o cliente
- [ ] Vars de ambiente têm nomes reais do projecto, não genéricos
- ❌ NOT delivery-ready: `vercel domains add yourdomain.com`; `DATABASE_URL=[your-database-url]`
- ✅ Delivery-ready: `vercel domains add lusoconta.pt`; `DATABASE_URL` → Supabase URL de produção LUSOconta confirmada

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Deploy — Lisbon Dog Care

## vercel.json

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

## Env vars de produção

```bash
vercel env add NEXT_PUBLIC_SITE_URL production
# valor: https://lisbondogcare.pt

vercel env add DATABASE_URL production
# valor: postgresql://[supabase-host]/lisbondogcare-prod (fornecida pelo cliente 2025-01-14)

vercel env add RESEND_API_KEY production
# valor: re_xxxx (Resend account lisbondogcare@gmail.com)

vercel env add NEXT_PUBLIC_GOOGLE_MAPS_KEY production
# valor: AIza... (Google Cloud Console projecto "lisbon-dog-care-prod")
```

## Sequência de deploy

```bash
# 1. Build local — confirmar sem erros
npm run build
# ✅ Output: "Route (app) — /booking 4.2 kB, /services 2.8 kB" — sem erros

# 2. Link ao projecto Vercel
vercel link
# Seleccionar: lisbondogcare (org: dario-studio)

# 3. Preview deploy
vercel
# URL gerada: lisbondogcare-git-main-dario-studio.vercel.app

# 4. Validação da preview (partilhada com Sofia Marques, GM Lisbon Dog Care)
# Aprovação recebida via email 2025-01-15 14:23

# 5. Produção
vercel --prod
# ✅ Deployed: https://lisbondogcare.pt (2025-01-15 15:10)

# 6. Domínio custom
vercel domains add lisbondogcare.pt
# DNS: A record → 76.76.21.21 (Vercel IP)
# Propagação confirmada: dnschecker.org — 15 min após configuração
```

## Post-deploy checklist — resultados

- [x] https://lisbondogcare.pt — acessível, HTTPS verde
- [x] PageSpeed Mobile: LCP 2.1s, CLS 0.04, FID 12ms ✅
- [x] ogp.me — OG title "Lisbon Dog Care | Passeios e Creche para Cães em Lisboa", imagem 1200×630 ✅
- [x] Form de reserva testado → email recebido em reservas@lisbondogcare.pt (15:24)
- [x] Google Analytics 4 — evento `page_view` visível em tempo real (15:15)
- [x] /sitemap.xml retorna 200 com 8 URLs indexáveis
- [x] /robots.txt correcto — Googlebot allowed, /admin disallowed
```

---

## Output anti-patterns

- Entregar `vercel.json` com `regions: ["iad1"]` para cliente PT/EU — latência desnecessária de ~80ms
- Copiar checklist pre-deploy sem executar `next build` localmente — bugs chegam a produção
- Fazer `vercel --prod` sem preview aprovada — cliente vê bugs directo no domínio público
- Deixar `yourdomain.com` ou `[project]` no output final — demonstra output genérico não personalizado
- Omitir verificação de analytics pós-deploy — cliente perde dados de lançamento (dia de maior tráfego)
- Documentar env vars sem esclarecer origem/quem fornece — bloqueia deploy por falta de credenciais
- Deploy em sexta à tarde sem plano de rollback — qualquer bug fica sem suporte até segunda
- Esquecer security headers — app vulnerável a clickjacking, especialmente grave em e-commerce e saúde
- Reportar "está online" sem Core Web Vitals medidos — SEO e UX comprometidos sem o cliente saber
- Misturar env vars de preview e produção — `NEXT_PUBLIC_SITE_URL` aponta para preview URL em prod
