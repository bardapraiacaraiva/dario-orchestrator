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
