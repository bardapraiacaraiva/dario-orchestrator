---
name: builder-component-registry
description: >
  Registry privado de componentes DARIO — shadcn registry pattern. Componentes pre-configurados
  instaláveis via npx shadcn add @dario/component. Reutilizaveis across projectos.
  Use quando: registry componentes, componentes partilhados, shadcn registry, @dario components.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — DARIO Component Registry (@dario/)

## Proposito
Registry privado de componentes DARIO — cada componente e pre-configurado, testado,
e instalavel com um unico comando em qualquer projecto.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-component-registry init` | Setup registry no projecto |
| `/builder-component-registry add [comp]` | Adicionar componente ao registry |
| `/builder-component-registry publish` | Publicar registry |

## Como funciona

### Install from DARIO registry
```bash
npx shadcn@latest add "https://registry.dario.pt/r/data-table"
npx shadcn@latest add "https://registry.dario.pt/r/auth-form"
npx shadcn@latest add "https://registry.dario.pt/r/pricing-card"
```

### Registry structure
```json
// registry.json
{
  "$schema": "https://ui.shadcn.com/schema/registry.json",
  "name": "@dario",
  "homepage": "https://dario.pt",
  "items": [
    {
      "name": "data-table",
      "type": "registry:ui",
      "files": [{ "path": "components/ui/data-table.tsx" }],
      "dependencies": ["@tanstack/react-table"]
    },
    {
      "name": "auth-form",
      "type": "registry:ui",
      "files": [{ "path": "components/auth/auth-form.tsx" }],
      "dependencies": ["react-hook-form", "zod"]
    }
  ]
}
```

### DARIO Pre-built Components
| Component | Description |
|---|---|
| `@dario/data-table` | Sortable, filterable, paginated table |
| `@dario/auth-form` | Login + register + forgot password |
| `@dario/pricing-card` | 3-tier pricing with toggle monthly/yearly |
| `@dario/hero-section` | Hero with badge + headline + CTA + social proof |
| `@dario/contact-form` | Contact form with Zod validation |
| `@dario/dashboard-layout` | Sidebar + header + content layout |
| `@dario/stats-card` | KPI card with trend indicator |
| `@dario/file-upload` | Drag & drop file upload with preview |

## Inspired by
- **shadcn-ui/registry-template** (78K ecosystem) — Custom registries
- **shadcn MCP server** — AI-powered component installation
