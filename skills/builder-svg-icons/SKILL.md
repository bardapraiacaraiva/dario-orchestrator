---
name: builder-svg-icons
description: >
  Gera icones e ilustracoes SVG a partir de descricoes textuais ou keywords de marca.
  SVGs optimizados, acessiveis, tematizaveis via CSS. Icon sets customizados por projecto.
  Use quando: icones, SVG, ilustracoes, icon set, vector graphics, logo icon.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — SVG Icon & Illustration Generator

## Proposito
Gerar SVGs production-ready — icones, ilustracoes, logos simplificados.
Tematizaveis via CSS (currentColor), optimizados (SVGO), acessiveis (title + role).

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-svg-icons [tema]` | Icon set de 10-20 icones para um tema |
| `/builder-svg-icons logo [marca]` | Logo icon simplificado |
| `/builder-svg-icons illustration [cena]` | Ilustracao SVG |

## Workflow

### 1. Define Icon Needs (from project context)
```
SaaS de contabilidade → icons: invoice, calculator, chart, calendar, user, settings,
                                check, alert, download, upload, filter, search
```

### 2. Generate SVGs
Cada icone:
- Viewbox: 24x24 (standard) ou 20x20 (compact)
- Stroke-based (nao fill) — permite tematizacao
- `currentColor` como cor — herda do parent CSS
- Acessivel: `<title>` + `role="img"` + `aria-hidden="true"` para decorativos

### 3. Output: React Components (Lucide pattern)
```tsx
// components/icons/invoice.tsx
export function InvoiceIcon({ className, ...props }: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"
         className={className} {...props}>
      <title>Invoice</title>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
  )
}
```

## Approach
1. **Use Lucide as base** (200K+ downloads/week) — extend with custom icons
2. **Match brand style** — if builder-brand-identity ran, match stroke weight/roundness
3. **Consistent sizing** — all icons same viewBox, stroke width, corner radius

## Inspired by
- **OmniSVG** (NeurIPS 2025) — AI SVG generation model
- **lucide-icons/lucide** (12K stars) — Standard React icon library
