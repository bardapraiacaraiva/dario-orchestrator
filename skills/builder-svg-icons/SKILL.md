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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — SVG estrutura válida e renderizável
- [ ] Cada SVG tem `viewBox` definido (`0 0 24 24` ou `0 0 20 20`), sem valores em falta
- [ ] `xmlns="http://www.w3.org/2000/svg"` presente em todos os elementos root
- [ ] Paths fechados correctamente (sem `d=""` vazio ou coordenadas truncadas)
- [ ] SVG abre/fecha sem erros se colado directo no browser
- ❌ NOT delivery-ready: `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0` (path cortado)
- ✅ Delivery-ready: `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />` (path completo, fechado)

### Gate 2 — Tematização via currentColor funcional
- [ ] Nenhum ícone usa cores hardcoded (`#000`, `black`, `rgb(0,0,0)`) — usa `currentColor`
- [ ] `fill="none"` definido em SVGs stroke-based (não mistura fill+stroke sem intenção)
- [ ] `stroke="currentColor"` presente em todos os elementos visuais (path, line, circle, polyline)
- [ ] Testado mentalmente: mudar `color: red` no parent CSS altera o ícone
- ❌ NOT delivery-ready: `stroke="#1a1a1a"` ou `fill="#333333"`
- ✅ Delivery-ready: `stroke="currentColor" fill="none" strokeWidth={2}`

### Gate 3 — Acessibilidade correcta por contexto
- [ ] Ícones decorativos têm `aria-hidden="true"` (não lidos pelo screen reader)
- [ ] Ícones com significado standalone têm `<title>Nome legível</title>` + `role="img"`
- [ ] `strokeLinecap="round"` e `strokeLinejoin="round"` definidos (legibilidade a 16px)
- [ ] Nenhum ícone depende só de cor para transmitir significado
- ❌ NOT delivery-ready: ícone "Alert" sem `<title>` nem `aria-label`, standalone num botão
- ✅ Delivery-ready: `<title>Alerta de pagamento</title> role="img"` em ícone de aviso crítico

### Gate 4 — Consistência de estilo no icon set
- [ ] Todos os ícones do set usam o mesmo `viewBox` (não mistura 24x24 com 16x16)
- [ ] `strokeWidth` uniforme em todo o set (ex: `2` ou `1.5`, não mistura)
- [ ] Corner radius consistente — se um ícone usa `strokeLinejoin="round"`, todos usam
- [ ] Visual weight comparável entre ícones (ícone de "search" não parece mais pesado que "settings")
- ❌ NOT delivery-ready: set com strokeWidth={1} em metade e strokeWidth={2.5} na outra
- ✅ Delivery-ready: todos os 12 ícones do set LUSOconta com `strokeWidth={1.5}`, `viewBox="0 0 24 24"`, `strokeLinejoin="round"`

### Gate 5 — React component pattern correcto (se output é .tsx)
- [ ] Função exportada com nome PascalCase descritivo (`InvoiceIcon`, não `Icon1`)
- [ ] Props tipadas como `React.SVGProps<SVGSVGElement>` com `className` e spread `{...props}`
- [ ] Ficheiro nomeado em kebab-case coincidente com o componente (`invoice-icon.tsx`)
- [ ] Import path relativo funcional no contexto do projecto (`components/icons/`)
- ❌ NOT delivery-ready: `export default () => <svg>...</svg>` sem nome, sem props
- ✅ Delivery-ready: `export function PiggyBankIcon({ className, ...props }: React.SVGProps<SVGSVGElement>)`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Nome do cliente/projecto aparece nos comentários de ficheiro ou `<title>` (ex: `Cuidai`, `ARRECADA.GOV`)
- [ ] Ícones gerados são específicos ao domínio do cliente (não lista genérica copy-paste)
- [ ] Nenhum `<YourBrandName>`, `<insert-color>`, `<TODO>` ou placeholder visível
- [ ] Paths SVG são geometricamente coerentes com o que o ícone representa (invoice parece documento, não círculo)
- ❌ NOT delivery-ready: `// components/icons/<project-name>/invoice.tsx` com `<title>Icon</title>`
- ✅ Delivery-ready: `// components/icons/lusoconta/invoice.tsx` com `<title>Fatura pendente</title>`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
// LUSOconta — Icon Set v1.0
// Domain: contabilidade pessoal PT · 8 ícones · viewBox 24x24 · stroke-based

// components/icons/lusoconta/invoice-icon.tsx
export function InvoiceIcon({ className, ...props }: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={1.5} strokeLinecap="round"
         strokeLinejoin="round" className={className} {...props}>
      <title>Fatura</title>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
  )
}

// components/icons/lusoconta/piggy-bank-icon.tsx
export function PiggyBankIcon({ className, ...props }: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={1.5} strokeLinecap="round"
         strokeLinejoin="round" className={className} {...props}>
      <title>Poupança</title>
      <path d="M19 9c0-3.87-3.13-7-7-7S5 5.13 5 9c-1.1 0-2 .9-2 2v2c0 1.1.9 2 2 2h.1
               C5.56 16.74 6.7 18 8 18.93V21h2v-1.5h4V21h2v-2.07C17.3 18 18.44 16.74
               18.9 15H19c1.1 0 2-.9 2-2v-2c0-1.1-.9-2-2-2z" />
      <circle cx="15" cy="10" r="1" fill="currentColor" stroke="none" />
      <path d="M21 12h1" />
    </svg>
  )
}

// components/icons/lusoconta/chart-bar-icon.tsx
export function ChartBarIcon({ className, ...props }: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={1.5} strokeLinecap="round"
         strokeLinejoin="round" className={className} {...props}>
      <title>Relatório de despesas</title>
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
      <line x1="2" y1="20" x2="22" y2="20" />
    </svg>
  )
}

// components/icons/lusoconta/index.ts — barrel export
export { InvoiceIcon }  from './invoice-icon'
export { PiggyBankIcon } from './piggy-bank-icon'
export { ChartBarIcon }  from './chart-bar-icon'

// Usage — Dashboard LUSOconta
// <InvoiceIcon className="w-5 h-5 text-lusoconta-blue" aria-hidden="true" />
// <ChartBarIcon className="w-6 h-6 text-emerald-600" role="img" />
```

---

## Output anti-patterns

- Gerar ícones com `fill="#000000"` ou cores hex hardcoded — quebra tematização, inútil em dark mode
- Misturar `viewBox="0 0 24 24"` com `viewBox="0 0 16 16"` no mesmo set — alinhamento parte em runtime
- Exportar componente anónimo (`export default () => <svg>`) — impossível de tree-shake e debugar
- Deixar `<title>Icon</title>` genérico — screen readers anunciam "Icon" sem contexto
- Paths SVG que não correspondem visualmente ao conceito (quadrado a representar "câmara") — cliente detecta na primeira review
- Omitir barrel export `index.ts` — força imports verbosos e torna refactor mais difícil
- Gerar 20 ícones sem consistência de stroke weight — set parece colado de 3 bibliotecas diferentes
- Usar `strokeWidth="2px"` com unidade px em vez de número puro — comportamento undefined em SVG scaling
