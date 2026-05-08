---
name: builder-ci-cd
description: >
  Gera pipelines CI/CD com GitHub Actions: build, test, lint, deploy preview, deploy production.
  Branch protection, environment secrets, rollback. Zero-downtime deploys.
  Use quando: CI/CD, github actions, pipeline, deploy automatico, continuous integration.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — CI/CD Pipeline

## Proposito
Gerar GitHub Actions workflows completos — build, test, deploy preview, deploy production.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-ci-cd [stack]` | Pipeline completo |
| `/builder-ci-cd vercel` | CI + Vercel deploy |
| `/builder-ci-cd docker` | CI + Docker build + VPS deploy |
| `/builder-ci-cd test-only` | Apenas lint + test (sem deploy) |

## Standard Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test

  deploy-preview:
    needs: lint-and-test
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

  deploy-production:
    needs: lint-and-test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Output
1. `.github/workflows/ci.yml`
2. `.github/workflows/deploy.yml` (if separate)
3. Branch protection rules (documentation)
4. Secrets list (.env.example for CI)

## Red Flags
- Deploy sem testes — bugs directo em producao
- Secrets em plaintext no workflow — usar GitHub Secrets SEMPRE
- Sem preview deploys em PRs — nao ha review visual
- Deploy em push para main sem protection — qualquer merge vai para prod
