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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Workflow YAML é válido e executável
- [ ] Indentação YAML correcta (2 espaços, sem tabs)
- [ ] Todos os `uses:` têm versão pinada (`@v4`, `@v25` — nunca `@latest`)
- [ ] `on:` trigger cobre push para main E pull_request
- [ ] `needs:` chain garante que deploy nunca corre sem lint-and-test passar

❌ NOT delivery-ready: `uses: actions/checkout@latest` ou jobs sem `needs:` definido  
✅ Delivery-ready: `uses: actions/checkout@v4` + `deploy-production: needs: lint-and-test`

---

### Gate 2 — Secrets referenciados são todos declarados
- [ ] Cada `${{ secrets.X }}` no workflow tem entrada correspondente no `.env.example` para CI
- [ ] Nenhum valor sensível hardcoded no YAML (tokens, passwords, IDs)
- [ ] Lista de secrets entregue ao cliente com nome exacto a criar em Settings → Secrets

❌ NOT delivery-ready: `vercel-token: "tok_abc123xyz"` em plaintext no workflow  
✅ Delivery-ready: `vercel-token: ${{ secrets.VERCEL_TOKEN }}` + `.env.example` com `VERCEL_TOKEN=`, `VERCEL_ORG_ID=`, `VERCEL_PROJECT_ID=`

---

### Gate 3 — Jobs cobrem os 3 estágios obrigatórios
- [ ] **lint-and-test**: lint + type-check + test presentes (não só `npm run build`)
- [ ] **deploy-preview**: activado apenas em `pull_request`, gera URL de preview
- [ ] **deploy-production**: activado apenas em push para `main`, usa flag `--prod` ou equivalente
- [ ] Condicionais `if:` correctas em cada job (PR vs push main não se sobrepõem)

❌ NOT delivery-ready: deploy-production corre em todo o push independente de branch  
✅ Delivery-ready: `if: github.ref == 'refs/heads/main' && github.event_name == 'push'`

---

### Gate 4 — Stack do cliente está correctamente configurada
- [ ] `node-version` corresponde ao `.nvmrc` ou `engines` do `package.json` do projecto
- [ ] Package manager correcto: `npm ci` vs `yarn install --frozen-lockfile` vs `pnpm install --frozen-lockfile`
- [ ] Action de deploy corresponde à plataforma real (Vercel action para Vercel, `docker build` para VPS)
- [ ] Cache configurado para o package manager correcto (`cache: npm` / `cache: yarn` / `cache: pnpm`)

❌ NOT delivery-ready: `cache: npm` num projecto que usa pnpm  
✅ Delivery-ready: `uses: pnpm/action-setup@v3` + `cache: pnpm` para projecto Cuidai com pnpm

---

### Gate 5 — Branch protection rules documentadas
- [ ] Documento especifica quais branches proteger (`main`, `production`)
- [ ] Required status checks listadas por nome exacto (e.g., `lint-and-test`)
- [ ] "Require PR before merging" e nº de reviewers especificado
- [ ] "Require branches to be up to date" activado para evitar race conditions

❌ NOT delivery-ready: "configura branch protection" sem especificar os nomes dos status checks  
✅ Delivery-ready: "Em Settings → Branches → main: required checks = `lint-and-test`, 1 reviewer obrigatório, dismiss stale reviews"

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem placeholders entre `<angle-brackets>`
- [ ] Nome do projecto/repo real no `name:` do workflow (não `My App CI/CD`)
- [ ] URL de deploy preview aponta para domínio real do cliente
- [ ] Secrets têm nomes consistentes com o projecto (e.g., `CUIDAI_VERCEL_TOKEN` se multi-projecto)
- [ ] Nenhum `<your-project-id>`, `<TOKEN>`, `<ORG>` no YAML entregue

❌ NOT delivery-ready: `vercel-project-id: <VERCEL_PROJECT_ID>` no ficheiro final  
✅ Delivery-ready: workflow nomeado `Cuidai CI/CD`, secrets documentados como `CUIDAI_VERCEL_TOKEN` no README de setup

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Cuidai — CI/CD Pipeline Setup

## Ficheiros criados

### `.github/workflows/ci.yml`
```yaml
name: Cuidai CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm type-check
      - run: pnpm test --run

  deploy-preview:
    needs: lint-and-test
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        id: vercel-preview
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
      - name: Comment PR with preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview: ${{ steps.vercel-preview.outputs.preview-url }}'
            })

  deploy-production:
    needs: lint-and-test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Secrets a criar (Settings → Secrets → Actions)

| Secret | Onde obter |
|--------|------------|
| `VERCEL_TOKEN` | vercel.com → Account Settings → Tokens |
| `VERCEL_ORG_ID` | `vercel project ls` → campo `orgId` |
| `VERCEL_PROJECT_ID` | `.vercel/project.json` após `vercel link` |

## `.env.example` para CI
```
VERCEL_TOKEN=
VERCEL_ORG_ID=
VERCEL_PROJECT_ID=
```

## Branch Protection — main (configurar em Settings → Branches)
- ✅ Require status checks: `lint-and-test`
- ✅ Require branches to be up to date before merging
- ✅ Require pull request: 1 reviewer
- ✅ Dismiss stale pull request approvals
- ✅ Do not allow bypassing (incluindo admins)

## Stack detectada
- Node 20 · pnpm 8 · Vitest · ESLint · TypeScript
- Deploy: Vercel (cuidai.pt)
```
```

---

## Output anti-patterns

- Usar `@latest` em qualquer action — quebra quando a action tem breaking changes silenciosos
- Hardcodar token ou ID de projecto Vercel no YAML em vez de `${{ secrets.X }}`
- Entregar workflow sem a lista de secrets a criar — cliente fica bloqueado no setup
- `deploy-production` sem `environment: production` — perde audit trail e approval gates do GitHub
- Omitir condicionais `if:` nos jobs — preview dispara em push para main, produção dispara em PRs
- Usar `npm install` em vez de `npm ci` — não garante lockfile, builds não são reproducíveis
- `lint-and-test` só com `npm run build` — passa em produção código que não compilava mas não testava
- Documentar branch protection como "activar protecção" sem listar os nomes exactos dos required status checks
- Gerar workflow genérico com `node-version: 18` quando o projecto usa Node 20 ou tem `.nvmrc`
- Entregar ficheiro com `<VERCEL_PROJECT_ID>` por preencher — placeholder não é um deliverable
