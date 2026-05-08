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
