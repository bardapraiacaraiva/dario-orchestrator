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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — registry.json é válido e instalável
- [ ] `$schema` aponta para `https://ui.shadcn.com/schema/registry.json`
- [ ] Cada item tem `name`, `type`, `files[]` e `dependencies[]` preenchidos
- [ ] URL de install é `https://registry.dario.pt/r/[nome-componente]` (sem trailing slash)
- [ ] JSON é válido (sem vírgulas a mais, sem campos em falta)
- ❌ NOT delivery-ready: `"dependencies": []` em componente que usa `@tanstack/react-table`
- ✅ Delivery-ready: `"dependencies": ["@tanstack/react-table", "@tanstack/react-query"]` confirmados via `package.json` do projecto

### Gate 2 — Componente exporta interface correcta
- [ ] Ficheiro `.tsx` tem export default + export named types
- [ ] Props são tipadas com TypeScript (sem `any`)
- [ ] Componente aceita `className?: string` para customização
- [ ] Sem imports hardcoded de paths de outros projectos
- ❌ NOT delivery-ready: `import { Button } from '../../cuidai/components/ui/button'`
- ✅ Delivery-ready: `import { Button } from '@/components/ui/button'` — path relativo ao projecto consumidor

### Gate 3 — Instalação end-to-end funciona
- [ ] `npx shadcn@latest add "https://registry.dario.pt/r/[comp]"` corre sem erro
- [ ] Ficheiros gerados aparecem no path correcto (`components/ui/` ou `components/[domínio]/`)
- [ ] Dependencies são auto-instaladas pelo shadcn CLI
- [ ] Componente renderiza sem erros após install
- ❌ NOT delivery-ready: comando documentado mas não testado — registry URL devolve 404
- ✅ Delivery-ready: `npx shadcn@latest add "https://registry.dario.pt/r/stats-card"` testado, gera `components/ui/stats-card.tsx` com peer deps instalados

### Gate 4 — Componente é data-agnostic e reutilizável
- [ ] Zero strings hardcoded de cliente específico (nomes, cores de marca, copy)
- [ ] Dados injectados via props (não dentro do componente)
- [ ] Variantes configuráveis via `variant` prop ou `cn()` class merging
- [ ] Funciona em Next.js 14+ App Router (sem `"use client"` desnecessário no topo)
- ❌ NOT delivery-ready: `<h1>Bem-vindo ao Cuidai</h1>` hardcoded dentro do `@dario/hero-section`
- ✅ Delivery-ready: `<h1>{headline}</h1>` com `headline: string` como prop obrigatória

### Gate 5 — registry.json está publicado e acessível
- [ ] `registry.json` está no root de `https://registry.dario.pt/`
- [ ] Cada item está acessível em `https://registry.dario.pt/r/[name].json`
- [ ] CORS headers permitem fetch do shadcn CLI
- [ ] Versão do componente está documentada no item (`"version": "1.0.0"`)
- ❌ NOT delivery-ready: registry existe localmente mas não está deployed — cliente não consegue instalar
- ✅ Delivery-ready: `curl https://registry.dario.pt/r/data-table.json` retorna JSON válido com status 200

### Gate 6 — Output usa CLIENT NAME + dados reais, sem angle-brackets
- [ ] Nenhum placeholder do tipo `<component-name>`, `<registry-url>`, `<client>` no output final
- [ ] Nome do projecto cliente (ex: Cuidai, SAQUEI, Tributario.AI) aparece no contexto correcto
- [ ] URLs de install são reais e testáveis, não `https://example.com/r/component`
- [ ] Nomes de componentes seguem convenção `@dario/[nome-kebab-case]` consistentemente
- ❌ NOT delivery-ready: `npx shadcn@latest add "https://<your-registry>/r/<component>"`
- ✅ Delivery-ready: `npx shadcn@latest add "https://registry.dario.pt/r/stats-card"` para projecto Tributario.AI

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## @dario/stats-card — instalação no Tributario.AI

### Install
```bash
npx shadcn@latest add "https://registry.dario.pt/r/stats-card"
```

### registry.json entry
```json
{
  "name": "stats-card",
  "type": "registry:ui",
  "version": "1.2.0",
  "files": [
    { "path": "components/ui/stats-card.tsx" }
  ],
  "dependencies": ["lucide-react"],
  "devDependencies": [],
  "registryDependencies": ["card", "badge"]
}
```

### Componente gerado: `components/ui/stats-card.tsx`
```tsx
"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { TrendingUp, TrendingDown } from "lucide-react"
import { cn } from "@/lib/utils"

interface StatsCardProps {
  title: string
  value: string | number
  trend?: number          // ex: +12.4 ou -3.1
  trendLabel?: string     // ex: "vs mês anterior"
  className?: string
}

export function StatsCard({
  title,
  value,
  trend,
  trendLabel = "vs período anterior",
  className,
}: StatsCardProps) {
  const isPositive = trend !== undefined && trend >= 0

  return (
    <Card className={cn("", className)}>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {trend !== undefined && (
          <div className="flex items-center gap-1 mt-1">
            {isPositive
              ? <TrendingUp className="h-4 w-4 text-green-500" />
              : <TrendingDown className="h-4 w-4 text-red-500" />}
            <Badge variant={isPositive ? "default" : "destructive"}>
              {isPositive ? "+" : ""}{trend}%
            </Badge>
            <span className="text-xs text-muted-foreground">{trendLabel}</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

### Uso no Tributario.AI dashboard
```tsx
// app/dashboard/page.tsx
import { StatsCard } from "@/components/ui/stats-card"

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-3 gap-4">
      <StatsCard
        title="Declarações submetidas"
        value="1.284"
        trend={+12.4}
        trendLabel="vs Março 2024"
      />
      <StatsCard
        title="Clientes ativos"
        value="347"
        trend={-2.1}
        trendLabel="vs semana anterior"
      />
      <StatsCard
        title="Receita mensal"
        value="€ 48.200"
        trend={+8.7}
        trendLabel="vs Abril 2024"
      />
    </div>
  )
}
```
```

---

## Output anti-patterns

- Gerar `registry.json` com `dependencies: []` quando o componente importa libraries externas (ex: `react-hook-form`, `@tanstack/react-table`)
- URL de install com placeholders: `https://<registry-domain>/r/<component-name>` em vez de `https://registry.dario.pt/r/stats-card`
- Componente com copy hardcoded de cliente (`"Bem-vindo ao SAQUEI"`) em vez de props (`headline: string`)
- Ficheiro `.tsx` sem tipagem TypeScript — props como `any` ou sem interface declarada
- Registry item sem `registryDependencies` quando usa componentes shadcn base (`card`, `badge`, `button`)
- `"use client"` no topo de componentes puramente presentacionais sem hooks de estado
- Path de import relativo ao projecto de origem: `../../dario-core/components/button` em vez de `@/components/ui/button`
- Documentar comando `npx shadcn add` sem confirmar que o endpoint está deployed e devolve 200
- Misturar `type: "registry:ui"` com `type: "registry:component"` sem critério consistente
- Publicar registry sem CORS headers — shadcn CLI falha silenciosamente sem mensagem de erro útil
