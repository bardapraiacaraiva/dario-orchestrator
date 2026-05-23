---
name: builder-sst-deploy
description: >
  Deploy para AWS com SST v3 (22K stars) — Infrastructure-as-Code em TypeScript.
  Next.js + Postgres + S3 + Lambda. sst.config.ts define tudo. Para apps que precisam de AWS.
  Use quando: AWS deploy, lambda, serverless, SST, infrastructure as code, edge deploy AWS.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — SST v3 AWS Deploy

## Proposito
Deploy para AWS usando SST v3 — IaC em TypeScript puro. Para projectos que precisam de
AWS (compliance, scale, servicos especificos) em vez de Vercel.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-sst-deploy [app]` | Config SST completa |
| `/builder-sst-deploy nextjs` | Next.js on Lambda@Edge |

## Output

```typescript
// sst.config.ts
export default $config({
  app(input) {
    return {
      name: "my-app",
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws",
      providers: { aws: { region: "eu-west-1" } },
    }
  },
  async run() {
    // Database
    const db = new sst.aws.Postgres("Database", { scaling: { min: "0.5 ACU", max: "4 ACU" } })

    // Storage
    const bucket = new sst.aws.Bucket("Uploads")

    // Next.js
    new sst.aws.Nextjs("Web", {
      link: [db, bucket],
      environment: { DATABASE_URL: db.url },
    })
  },
})
```

## When to use SST vs Vercel vs Coolify
| Criterio | Vercel | SST (AWS) | Coolify (VPS) |
|---|---|---|---|
| Simple Next.js | Best | Good | Good |
| Custom AWS services | No | Best | No |
| Lambda/Edge | No | Best | No |
| Cost at scale | Expensive | Cheapest | Fixed cost |
| Government/PT | Maybe | Best (eu-west-1) | Good |

## Inspired by
- **sst/sst** (22K stars) — TypeScript IaC for AWS

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — sst.config.ts completo e funcional
- [ ] `app()` define `name`, `removal` condicional por stage, `home: "aws"` e `providers` com região explícita
- [ ] `run()` instancia pelo menos um recurso linkado ao Next.js
- [ ] `link: [...]` presente no `Nextjs` component — sem ele as env vars não chegam ao runtime
- ❌ NOT delivery-ready: `providers: { aws: {} }` sem região, removal hardcoded `"remove"` em production
- ✅ Delivery-ready: `providers: { aws: { region: "eu-west-1" } }`, `removal: input?.stage === "production" ? "retain" : "remove"`

### Gate 2 — Recursos AWS correctamente dimensionados
- [ ] Postgres Aurora Serverless v2 com `scaling.min` e `scaling.max` explícitos (não defaults)
- [ ] Bucket com nome lógico que reflecte o propósito (ex: `"CuidaiUploads"`, não `"Bucket"`)
- [ ] Lambda memory/timeout configurado se há processamento pesado (default 128 MB mata muitos casos)
- ❌ NOT delivery-ready: `new sst.aws.Postgres("Database")` sem scaling — billing surprise em produção
- ✅ Delivery-ready: `new sst.aws.Postgres("LUSOcontaDB", { scaling: { min: "0.5 ACU", max: "8 ACU" } })`

### Gate 3 — Secrets e variáveis de ambiente
- [ ] Secrets sensíveis via `new sst.Secret(...)`, nunca hardcoded no config
- [ ] `DATABASE_URL` linkado via `db.url` (não string manual)
- [ ] `.env.example` ou equivalente documentado no output para o dev saber o que configurar
- ❌ NOT delivery-ready: `environment: { DATABASE_URL: "postgres://user:pass@host/db" }` literal
- ✅ Delivery-ready: `const stripeKey = new sst.Secret("StripeKey")` + `link: [db, bucket, stripeKey]`

### Gate 4 — Multi-stage (dev / staging / production)
- [ ] Config diferencia comportamento por `input.stage` (pelo menos `removal`)
- [ ] Comando de deploy por stage documentado: `npx sst deploy --stage production`
- [ ] Custo estimado ou aviso de recursos que persistem em production (`retain`) vs dev (`remove`)
- ❌ NOT delivery-ready: config sem qualquer referência a stages — cliente faz deploy e apaga DB em dev por engano
- ✅ Delivery-ready: nota explícita "stage=production retém RDS e S3; stages dev/staging destroem tudo no `sst remove`"

### Gate 5 — Justificação SST vs alternativas
- [ ] Tabela de decisão SST/Vercel/Coolify preenchida com critérios do projecto actual (não genérica)
- [ ] Razão concreta documentada: compliance PT/Gov → `eu-west-1`, AWS Rekognition, SES, etc.
- [ ] Custo estimado mensal indicado (mesmo que aproximado: "~€12/mês em idle com Aurora Serverless 0.5 ACU")
- ❌ NOT delivery-ready: "use SST porque é melhor para AWS" sem contexto do cliente
- ✅ Delivery-ready: "Tributario.AI requer dados em território EU + SES para envio de emails fiscais → SST eu-west-1"

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] `name:` no `sst.config.ts` é o app name real, não `"my-app"` ou `"<app-name>"`
- [ ] Recursos têm nomes que reflectem o produto (ex: `"SaqueiUploads"`, `"CuidaiDB"`)
- [ ] Região AWS é a correcta para o cliente (PT/Gov → `eu-west-1`; Brasil → `sa-east-1`)
- [ ] Não existe nenhum `<placeholder>`, `TODO`, `YOUR_REGION` no output final
- ❌ NOT delivery-ready: `name: "my-app"`, `new sst.aws.Bucket("Uploads")`, região omissa
- ✅ Delivery-ready: `name: "saquei"`, `new sst.aws.Bucket("SaqueiDocumentos")`, `region: "eu-west-1"`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output SST deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / dados reais do cliente / repo inspeccionado
- 🟡 **assumed** — plausível para o projecto mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — estimativa por design (custo, scaling, performance — não verificável a priori)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verify antes de `sst deploy --stage production`.  **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
name: "tributario-ai"          # verificado? assumido? ninguém sabe
region: "eu-west-1"            # porquê esta região? compliance? preferência?
scaling: { min: "0.5 ACU", max: "8 ACU" }   # baseado em quê?
custo estimado: ~€35/mês       # número sem fonte
```

✅ Delivery-ready:
```
🔵 name: "tributario-ai"           — confirmado do package.json do repo cliente
🟡 region: "eu-west-1"             — assumed: compliance PT/Gov; confirmar se há restrição contratual
🟡 scaling max: "8 ACU"            — assumed: estimativa para pico fiscal; confirmar load esperado
🟢 custo estimado: ~€35/mês idle   — projecção Aurora Serverless 0.5 ACU + Lambda; validar pós-deploy real
🔵 removal: "retain" em production — verificado: Gate 4 passa, stage check presente no config
```

**Ship checklist post-cliente-sync:**
- [ ] Todos os 🟡 items confirmados — substituir `region`, `scaling.max`, secrets names com actuals do cliente
- [ ] Todos os 🔵 items com fonte citada — package.json, repo URL, conversa de sessão (não "eu lembro")
- [ ] Todos os 🟢 projections comunicados explicitamente ao cliente como estimativas — nunca apresentar custo AWS como garantido antes de load real

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SST v3 Deploy — SAQUEI (Marketplace Imobiliário)

## Stack
- Next.js 14 App Router
- Aurora Serverless v2 (Postgres) — eu-west-1
- S3 para documentos de transacção
- Lambda@Edge para SSR

## sst.config.ts

```typescript
/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "saquei",
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws",
      providers: {
        aws: { region: "eu-west-1" }, // RGPD — dados em território EU
      },
    }
  },
  async run() {
    // Secrets (configurar via: npx sst secret set StripeKey sk_live_xxx --stage production)
    const stripeKey = new sst.Secret("StripeKey")
    const authSecret = new sst.Secret("AuthSecret")

    // Aurora Serverless v2 — escala a zero em staging, max 8 ACU em produção
    const db = new sst.aws.Postgres("SaqueiDB", {
      scaling: {
        min: input?.stage === "production" ? "2 ACU" : "0.5 ACU",
        max: input?.stage === "production" ? "8 ACU" : "2 ACU",
      },
    })

    // S3 para documentos imobiliários (escrituras, certidões)
    const documentos = new sst.aws.Bucket("SaqueiDocumentos", {
      versioning: true, // audit trail de documentos legais
    })

    // Next.js em Lambda@Edge
    new sst.aws.Nextjs("SaqueiWeb", {
      link: [db, documentos, stripeKey, authSecret],
      environment: {
        DATABASE_URL: db.url,
        NEXT_PUBLIC_APP_URL:
          input?.stage === "production"
            ? "https://saquei.pt"
            : `https://${input?.stage}.saquei.pt`,
      },
      server: {
        memory: "512 MB",   // geração de PDF de contratos
        timeout: "30 seconds",
      },
    })
  },
})
```

## Deploy

```bash
# Instalar dependências SST
npx sst install

# Deploy staging
npx sst deploy --stage staging

# Configurar secrets (fazer UMA vez por stage)
npx sst secret set StripeKey sk_live_xxx --stage production
npx sst secret set AuthSecret $(openssl rand -base64 32) --stage production

# Deploy produção
npx sst deploy --stage production

# Ver recursos criados
npx sst console --stage production
```

## Custos estimados (eu-west-1)

| Recurso | Idle/mês | Load médio/mês |
|---|---|---|
| Aurora 0.5–8 ACU | ~€12 | ~€45 |
| Lambda@Edge (SSR) | ~€0 | ~€8 |
| S3 (100 GB docs) | ~€2 | ~€2 |
| **Total** | **~€14** | **~€55** |

> Vercel Pro equivalente: €20/mês fixo + €0.40/GB bandwidth — SST ganha a partir de ~50K visitas/mês

## Porquê SST e não Vercel para SAQUEI
- Documentos legais (escrituras) não podem sair de EU → `eu-west-1` garantido
- SES para emails transaccionais de oferta/contraproposta (Vercel não tem integração nativa)
- Lambda timeout 30s para geração de PDFs (Vercel limite: 10s no Pro)
```

---

## Output anti-patterns

- `name: "my-app"` no sst.config.ts entregue ao cliente — indica que o config é genérico, não pensado
- Região AWS omissa ou `us-east-1` para cliente português/governamental sem justificação
- Secrets hardcoded no `environment: {}` em vez de `sst.Secret` — falha de segurança crítica
- `scaling` omisso no Postgres — Aurora sem min/max pode gerar bills de centenas de euros
- Config sem diferenciação de stage — cliente apaga base de dados de produção com `sst remove`
- Tabela SST vs Vercel vs Coolify copiada verbatim sem adaptar ao projecto real do cliente
- `link: []` ausente — resources criados mas inacessíveis ao runtime da app (erro silencioso em produção)
- Timeout Lambda no default (3s) quando o projecto tem operações longas (PDF, email batch, scraping)
- Output sem comandos de deploy concretos — cliente não sabe como fazer o primeiro `sst deploy`
- `new sst.aws.Bucket("Uploads")` sem nome de cliente — indica placeholder, não produção-ready
