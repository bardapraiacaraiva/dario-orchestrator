---
name: builder-react-components
description: >
  Gera componentes React/TypeScript production-ready com shadcn/ui, Tailwind, CVA variants,
  compound components, acessibilidade. Storybook-ready.
  Use quando: componentes react, UI components, shadcn, botoes, forms, tabelas, modais.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — React Component Library

## Proposito
Gerar componentes React PRODUCTION-READY — TypeScript strict, variantes, acessibilidade, composicao.
Padrao: **shadcn/ui** + **CVA** (Class Variance Authority) + **Radix UI** primitives.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-react-components [componente]` | Componente individual |
| `/builder-react-components kit` | Kit completo (button, input, card, badge, dialog, table) |
| `/builder-react-components form [campos]` | Form completo com validation |
| `/builder-react-components dashboard` | Dashboard components (stats, charts, sidebar) |

## Component Pattern (CVA + forwardRef)

```tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof buttonVariants> {
  isLoading?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, ...props }, ref) => (
    <button className={cn(buttonVariants({ variant, size, className }))} ref={ref} disabled={isLoading} {...props}>
      {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {children}
    </button>
  )
)
Button.displayName = 'Button'
export { Button, buttonVariants }
```

## Core Kit (minimum 6 components)
1. **Button** — variants, sizes, loading, icon, asChild
2. **Input** — label, helper, error, sizes, disabled, prefix/suffix
3. **Card** — header, content, footer, hover, clickable
4. **Badge** — semantic colors, sizes, dot variant, removable
5. **Dialog** — modal with overlay, close, responsive, focus trap
6. **DataTable** — sortable, filterable, paginated, selectable

## Output per component
- `components/ui/[name].tsx` — component file
- TypeScript types exported
- CVA variants for customization
- forwardRef for composition
- aria-* attributes for a11y
- Responsive (mobile-first)

## Red Flags
- Componentes sem forwardRef — nao composable
- Sem TypeScript types — bugs em integracao
- Inline styles em vez de Tailwind — inconsistencia
- Sem focus states — inacessivel por teclado
- Sem loading/disabled states — UX incompleta

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — TypeScript strict & forwardRef
- [ ] Todos os componentes exportam interface própria (`ButtonProps`, `InputProps`, etc.)
- [ ] `forwardRef` aplicado com generic correcto: `forwardRef<HTMLButtonElement, ButtonProps>`
- [ ] `displayName` definido em cada componente (`Button.displayName = 'Button'`)
- [ ] Sem `any` implícito; props `extends` do elemento HTML nativo correcto
- ❌ NOT delivery-ready: `const Button = ({ onClick, ...props }) => <button {...props} />`
- ✅ Delivery-ready: `const Button = forwardRef<HTMLButtonElement, ButtonProps>(({ variant, size, isLoading, className, ...props }, ref) => ...); Button.displayName = 'Button'`

### Gate 2 — CVA variants completos
- [ ] `cva()` com base classes + `variants` object + `defaultVariants`
- [ ] Pelo menos 2 axes de variação (ex: `variant` + `size`)
- [ ] `cn()` de `@/lib/utils` usado no `className` merge (nunca template literals crus)
- [ ] `compoundVariants` usado quando há combinações especiais (ex: `sm` + `destructive`)
- ❌ NOT delivery-ready: `className={variant === 'primary' ? 'bg-blue-500' : 'bg-gray-200'}`
- ✅ Delivery-ready: `const badgeVariants = cva('...base', { variants: { variant: { default: 'bg-primary', success: 'bg-emerald-500 text-white', destructive: 'bg-destructive' }, size: { sm: 'text-xs px-2', md: 'text-sm px-3' } }, defaultVariants: { variant: 'default', size: 'md' } })`

### Gate 3 — Acessibilidade (a11y)
- [ ] Todos os elementos interactivos têm `focus-visible:ring-2 focus-visible:ring-ring` (nunca `outline-none` isolado)
- [ ] `aria-disabled`, `aria-label`, `aria-describedby` presentes onde aplicável
- [ ] Dialog/Modal tem `role="dialog"`, `aria-modal="true"`, focus trap implementado
- [ ] Loading state comunica estado: `aria-busy={isLoading}` no botão
- ❌ NOT delivery-ready: `<button className="... focus:outline-none">` sem ring substituto
- ✅ Delivery-ready: `<button ... aria-busy={isLoading} aria-disabled={disabled} className={cn(buttonVariants({ variant, size }), 'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2')}>`

### Gate 4 — States UX completos
- [ ] `disabled` state: `disabled:pointer-events-none disabled:opacity-50`
- [ ] `isLoading` state: spinner (`Loader2 animate-spin`) + `disabled={isLoading}` + texto preservado
- [ ] `error` state em Input: ring vermelho + helper text + `aria-invalid`
- [ ] Hover + active states definidos (não apenas hover)
- ❌ NOT delivery-ready: Input sem `errorMessage` prop; form submits sem loading state no botão
- ✅ Delivery-ready: `<Input label="Email" error="Email inválido" aria-invalid={!!error} aria-describedby="email-error" />` + `<div id="email-error" className="text-destructive text-sm mt-1">{error}</div>`

### Gate 5 — Estrutura de ficheiros & exports
- [ ] Path correcto: `components/ui/[name].tsx` (lowercase, kebab-case)
- [ ] Export nomeado do componente + export do `variants` object (ex: `export { Button, buttonVariants }`)
- [ ] Imports de `@/lib/utils`, `class-variance-authority`, `lucide-react` correctos
- [ ] Storybook-ready: componente funciona com props isoladas sem context obrigatório
- ❌ NOT delivery-ready: `export default Button` sem export do `buttonVariants`; import `../../lib/utils` (path relativo)
- ✅ Delivery-ready: `export { DataTable, type DataTableProps, type ColumnDef }` em `components/ui/data-table.tsx` com import `@/lib/utils`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets `<placeholder>`
- [ ] Nomes de campos reflectem domínio do cliente (ex: `pacienteId`, `valorSinistro`, `nifContribuinte`)
- [ ] Cores/tokens Tailwind alinhados com design system mencionado (não `blue-500` genérico)
- [ ] Exemplos de uso mostram props com dados do projecto real (não `label="Label aqui"`)
- [ ] Sem nenhum `<YourComponent>`, `<INSERT_NAME>`, `TODO:` no output final
- ❌ NOT delivery-ready: `<Button variant="primary">Click here</Button>` em contexto do Cuidai
- ✅ Delivery-ready: `<Button variant="default" isLoading={submittingConsulta} onClick={agendarConsulta}>Agendar Consulta</Button>` — Cuidai, fluxo de marcações

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado de sessão anterior / memória / dados do cliente (ex: design system existente, versão do pacote)
- 🟡 **assumed** — plausível mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — decisão de design por padrão da stack (não verificável sem contexto do projeto)

Output checklist upfront mostra ao reader exatamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
```
Button usa `h-10 px-4 py-2` como size default, tema de cores `bg-primary/90` no hover,
e o projeto tem shadcn/ui ^1.0 instalado.
```
*(Reader assume que tudo foi confirmado — versão, tokens, sizing — quando podem ser assumptions.)*

✅ Delivery-ready:
```
- 🔵 verified   — forwardRef + displayName aplicados (padrão CVA/shadcn validado)
- 🟡 assumed    — `bg-primary` mapeia para a cor de brand do cliente (confirmar CSS vars em globals.css)
- 🟡 assumed    — shadcn/ui ≥ 2.0 instalado (compoundVariants usa API v2); confirmar package.json
- 🟢 projection — size `icon: h-10 w-10` incluído por default; remover se não há uso de icon-only buttons
- 🟢 projection — focus ring usa `focus-visible:ring-ring` — assume token `--ring` definido no tema
```

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — CSS vars (`--primary`, `--ring`, `--radius`) existem no tema do cliente
- [ ] Versão do `class-variance-authority` e `shadcn/ui` verificadas contra `package.json` real do projeto
- [ ] Todos os 🟢 projections comunicados ao cliente como decisões de design (não factos fixos)
- [ ] Se `cn()` de `@/lib/utils` não existir no projeto, alternativa documentada antes de entregar

## Fully-worked A-tier example (delivery-ready reference)

```tsx
// components/ui/badge.tsx
// Cliente: Cuidai — plataforma de saúde domiciliária
// Contexto: badge de estado de consulta no dashboard do cuidador

import { cva, type VariantProps } from 'class-variance-authority'
import { X } from 'lucide-react'
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        agendada:   'border-transparent bg-blue-100 text-blue-800',
        confirmada: 'border-transparent bg-emerald-100 text-emerald-800',
        em_curso:   'border-transparent bg-amber-100 text-amber-800',
        concluida:  'border-transparent bg-gray-100 text-gray-700',
        cancelada:  'border-transparent bg-destructive/10 text-destructive',
        outline:    'border-border text-foreground bg-transparent',
      },
      size: {
        sm: 'text-[10px] px-2 py-px',
        md: 'text-xs px-2.5 py-0.5',
        lg: 'text-sm px-3 py-1',
      },
      dot: {
        true:  'pl-2',
        false: '',
      },
    },
    defaultVariants: { variant: 'agendada', size: 'md', dot: false },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  onRemove?: () => void
  removable?: boolean
}

const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant, size, dot, removable, onRemove, children, ...props }, ref) => (
    <span
      ref={ref}
      className={cn(badgeVariants({ variant, size, dot, className }))}
      {...props}
    >
      {dot && (
        <span
          className="h-1.5 w-1.5 rounded-full bg-current"
          aria-hidden="true"
        />
      )}
      {children}
      {removable && (
        <button
          type="button"
          onClick={onRemove}
          className="ml-0.5 rounded-full p-0.5 hover:bg-black/10 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
          aria-label={`Remover filtro ${children}`}
        >
          <X className="h-3 w-3" aria-hidden="true" />
        </button>
      )}
    </span>
  )
)
Badge.displayName = 'Badge'

export { Badge, badgeVariants }

// --- Exemplo de uso no dashboard Cuidai ---
// app/dashboard/consultas/page.tsx

import { Badge } from '@/components/ui/badge'

const estadoConsulta: Record<string, VariantProps<typeof badgeVariants>['variant']> = {
  AGENDADA:   'agendada',
  CONFIRMADA: 'confirmada',
  EM_CURSO:   'em_curso',
  CONCLUIDA:  'concluida',
  CANCELADA:  'cancelada',
}

export function EstadoConsultaBadge({ estado }: { estado: keyof typeof estadoConsulta }) {
  return (
    <Badge variant={estadoConsulta[estado]} dot size="md">
      {estado.replace('_', ' ')}
    </Badge>
  )
}

// Uso real na tabela de consultas:
// <EstadoConsultaBadge estado="EM_CURSO" />   → amber badge com dot
// <EstadoConsultaBadge estado="CANCELADA" />  → destructive badge com dot
```

---

## Output anti-patterns

- Usar `export default` sem exportar também o `variants` object — quebra composição externa
- `className` com template literals (`\`bg-${variant}\``) em vez de CVA — Tailwind purge elimina classes dinâmicas em produção
- `forwardRef` omitido em componentes de form — `react-hook-form` `register` e `Controller` ficam quebrados
- `outline-none` sem `focus-visible:ring-*` substituto — falha WCAG 2.1 AA (critério 2.4.7)
- Props de domínio genéricas (`label="Label"`, `placeholder="Enter text"`) em vez de alinhadas ao projecto do cliente
- Dialog sem `aria-modal="true"` e sem focus trap — leitores de ecrã percorrem conteúdo por baixo do modal
- Inline styles (`style={{ color: '#2563eb' }}`) misturados com Tailwind — quebra design tokens e dark mode
- Componente sem `displayName` — React DevTools e stack traces mostram `Anonymous`
- DataTable sem tipo genérico `<TData>` — perde type-safety nas colunas e row actions
