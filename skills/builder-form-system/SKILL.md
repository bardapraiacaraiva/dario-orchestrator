---
name: builder-form-system
description: >
  Gera forms completos React: validation com Zod, multi-step, file upload, error handling,
  loading states, success feedback. react-hook-form + Zod + shadcn/ui.
  Use quando: formulario, form, validacao, multi-step form, contacto, registo, checkout.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Form System

## Proposito
Forms sao onde o dinheiro entra. Form mal feito = conversao perdida. Gerar forms PERFEITOS.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-form-system contact` | Form de contacto |
| `/builder-form-system register` | Form de registo |
| `/builder-form-system checkout` | Form de checkout/pagamento |
| `/builder-form-system multi-step [steps]` | Form multi-step |
| `/builder-form-system [campos]` | Form custom com campos listados |

## Stack
- **react-hook-form** — performance (uncontrolled by default)
- **Zod** — schema validation (TypeScript-first)
- **shadcn/ui** — styled inputs, labels, error messages
- **Server Actions** — Next.js form submission (no API route needed)

## Template

```tsx
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(2, 'Nome muito curto'),
  email: z.string().email('Email invalido'),
  message: z.string().min(10, 'Mensagem muito curta').max(1000),
})

type FormData = z.infer<typeof schema>

export function ContactForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  async function onSubmit(data: FormData) {
    const res = await fetch('/api/contact', {
      method: 'POST',
      body: JSON.stringify(data),
    })
    if (!res.ok) throw new Error('Failed')
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name" className="text-sm font-medium">Nome</label>
        <input {...register('name')} className="w-full rounded-md border px-3 py-2" />
        {errors.name && <p className="text-sm text-red-500 mt-1">{errors.name.message}</p>}
      </div>
      {/* email, message similar */}
      <button type="submit" disabled={isSubmitting}
        className="w-full rounded-md bg-primary px-4 py-2 text-white disabled:opacity-50">
        {isSubmitting ? 'A enviar...' : 'Enviar'}
      </button>
    </form>
  )
}
```

## Output
1. Form component (React + TypeScript)
2. Zod schema (validation rules)
3. API route / Server Action (handler)
4. Success/error feedback UI

## Red Flags
- Form sem validation client-side — UX ma
- Form sem validation server-side — security risk
- Sem loading state no submit — user clica 10x
- Sem success feedback — user nao sabe se funcionou
- Labels sem htmlFor — inacessivel
