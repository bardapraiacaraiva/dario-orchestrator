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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Schema Zod é específico ao contexto do cliente
- [ ] Schema tem campos reais do negócio (não `name/email/message` genéricos copiados do template)
- [ ] Mensagens de erro estão em PT-PT/BR e fazem sentido para o utilizador final
- [ ] Regras de validação reflectem a realidade (ex: NIF tem 9 dígitos, telefone PT começa por `9[1236]`)
- [ ] `.superRefine()` ou `.refine()` usados quando há validação cross-field (ex: senha === confirmação)

❌ NOT delivery-ready: `email: z.string().email('Email invalido')` com mensagem genérica para plataforma fiscal  
✅ Delivery-ready: `nif: z.string().regex(/^\d{9}$/, 'NIF deve ter exactamente 9 dígitos').refine(validateNIF, 'NIF inválido')` para Tributario.AI

---

### Gate 2 — Loading & error states são bulletproof
- [ ] Botão de submit tem `disabled={isSubmitting}` E `aria-disabled`
- [ ] Loading state mostra feedback visual (spinner ou texto "A enviar...")
- [ ] Erro de rede/servidor capturado e mostrado ao utilizador (não swallowed silenciosamente)
- [ ] Múltiplos submits impossíveis (não cria 3 registos por double-click)

❌ NOT delivery-ready: `async function onSubmit(data) { await fetch(...) }` sem try/catch nem feedback de erro  
✅ Delivery-ready: `try { await submitLead(data) } catch (e) { setError('root', { message: 'Erro de ligação. Tenta novamente.' }) }` com toast visível

---

### Gate 3 — Acessibilidade não é afterthought
- [ ] Todos os `<input>` têm `<label>` com `htmlFor` matching o `id` do campo
- [ ] Erros de validação têm `role="alert"` ou estão ligados via `aria-describedby`
- [ ] Form pode ser completado apenas com teclado (Tab order lógico)
- [ ] Placeholder não substitui label (label sempre visível)

❌ NOT delivery-ready: `<input placeholder="Nome completo" />` sem label associada  
✅ Delivery-ready: `<label htmlFor="fullName">Nome completo</label><input id="fullName" aria-describedby="fullName-error" /><p id="fullName-error" role="alert">{errors.fullName?.message}</p>`

---

### Gate 4 — Server-side validation existe e é independente do client
- [ ] API route / Server Action valida com o mesmo schema Zod (ou equivalente)
- [ ] Nunca confia apenas na validação client-side para dados sensíveis
- [ ] Rate limiting ou protecção básica contra spam implementada (especialmente forms de contacto)
- [ ] Resposta do servidor devolve erros estruturados que o form consegue mapear para campos

❌ NOT delivery-ready: Server Action que faz `db.insert(data)` directamente sem re-validar  
✅ Delivery-ready: `const parsed = leadSchema.safeParse(formData); if (!parsed.success) return { errors: parsed.error.flatten().fieldErrors }` em `app/actions/submitLead.ts` da Cuidai

---

### Gate 5 — Multi-step (quando aplicável) gere estado correctamente
- [ ] Dados de steps anteriores preservados ao navegar para trás
- [ ] Validação ocorre step-a-step (não só no submit final)
- [ ] Progress indicator mostra step actual / total (ex: "Passo 2 de 4")
- [ ] URL ou estado reflecte o step (back button não perde tudo)

❌ NOT delivery-ready: Step 3 re-valida campos do Step 1 que o utilizador já preencheu, forçando reescrita  
✅ Delivery-ready: `useForm` com `mode: 'onBlur'` por step + `trigger(['campo1','campo2'])` antes de avançar, estado persistido em `sessionStorage` para SAQUEI checkout

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets de placeholder
- [ ] Nome do componente reflecte o cliente/contexto (`CuidaiContactForm`, não `ContactForm`)
- [ ] Endpoint, Server Action ou API route tem path real (ex: `/api/cuidai/leads`, não `/api/contact`)
- [ ] Campos do schema correspondem ao modelo de dados real do projecto
- [ ] Nenhum `<YOUR_CLIENT>`, `<FORM_TYPE>`, `<API_ENDPOINT>` sobreviveu no output final

❌ NOT delivery-ready: `export function ContactForm()` entregue a qualquer cliente sem adaptar  
✅ Delivery-ready: `export function PupliAdoptionRequestForm()` com schema `adoptionSchema` e action `submitAdoptionRequest` em `/app/actions/adoption.ts`

---

## Fully-worked A-tier example (delivery-ready reference)

```tsx
// app/components/forms/CuidaiCaregiverRegisterForm.tsx
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useState } from 'react'
import { registerCaregiver } from '@/app/actions/registerCaregiver'

const caregiverSchema = z.object({
  fullName: z.string().min(3, 'Nome deve ter pelo menos 3 caracteres'),
  email: z.string().email('Endereço de email inválido'),
  phone: z.string().regex(/^9[1236]\d{7}$/, 'Telefone português inválido (ex: 912345678)'),
  nif: z.string().regex(/^\d{9}$/, 'NIF deve ter 9 dígitos'),
  experience: z.enum(['menos_1_ano', '1_3_anos', 'mais_3_anos'], {
    errorMap: () => ({ message: 'Selecciona a tua experiência' }),
  }),
  certifications: z.string().optional(),
  acceptsTerms: z.literal(true, {
    errorMap: () => ({ message: 'Tens de aceitar os termos para continuar' }),
  }),
})

type CaregiverFormData = z.infer<typeof caregiverSchema>

export function CuidaiCaregiverRegisterForm() {
  const [submitStatus, setSubmitStatus] = useState<'idle'|'success'|'error'>('idle')

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<CaregiverFormData>({
    resolver: zodResolver(caregiverSchema),
    mode: 'onBlur',
  })

  async function onSubmit(data: CaregiverFormData) {
    try {
      const result = await registerCaregiver(data)
      if (result.errors) {
        Object.entries(result.errors).forEach(([field, messages]) =>
          setError(field as keyof CaregiverFormData, { message: messages[0] })
        )
        return
      }
      setSubmitStatus('success')
    } catch {
      setError('root', { message: 'Erro de ligação. Por favor tenta novamente.' })
      setSubmitStatus('error')
    }
  }

  if (submitStatus === 'success') {
    return (
      <div role="status" className="rounded-lg bg-green-50 p-6 text-center">
        <h2 className="text-lg font-semibold text-green-800">Registo enviado!</h2>
        <p className="mt-2 text-sm text-green-700">
          A equipa Cuidai irá analisar o teu perfil em 48h e contactar-te pelo email indicado.
        </p>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" noValidate>
      {errors.root && (
        <div role="alert" className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">
          {errors.root.message}
        </div>
      )}

      <div className="space-y-1">
        <label htmlFor="fullName" className="text-sm font-medium text-gray-700">
          Nome completo
        </label>
        <input
          id="fullName"
          {...register('fullName')}
          aria-describedby={errors.fullName ? 'fullName-error' : undefined}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-cuidai-500 focus:outline-none"
          placeholder="Maria Silva"
        />
        {errors.fullName && (
          <p id="fullName-error" role="alert" className="text-xs text-red-600">
            {errors.fullName.message}
          </p>
        )}
      </div>

      {/* ... campos email, phone, nif seguem o mesmo padrão ... */}

      <div className="space-y-1">
        <label htmlFor="experience" className="text-sm font-medium text-gray-700">
          Anos de experiência em cuidados
        </label>
        <select
          id="experience"
          {...register('experience')}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="">Selecciona...</option>
          <option value="menos_1_ano">Menos de 1 ano</option>
          <option value="1_3_anos">1 a 3 anos</option>
          <option value="mais_3_anos">Mais de 3 anos</option>
        </select>
        {errors.experience && (
          <p role="alert" className="text-xs text-red-600">{errors.experience.message}</p>
        )}
      </div>

      <div className="flex items-start gap-2">
        <input
          id="acceptsTerms"
          type="checkbox"
          {...register('acceptsTerms')}
          className="mt-0.5 h-4 w-4 rounded border-gray-300"
        />
        <label htmlFor="acceptsTerms" className="text-sm text-gray-600">
          Aceito os <a href="/termos-cuidadores" className="underline">termos para cuidadores</a> da Cuidai
        </label>
      </div>
      {errors.acceptsTerms && (
        <p role="alert" className="text-xs text-red-600">{errors.acceptsTerms.message}</p>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        aria-disabled={isSubmitting}
        className="w-full rounded-md bg-cuidai-600 px-4 py-2.5 text-sm font-medium text-white
                   hover:bg-cuidai-700 disabled:cursor-not-allowed disabled:opacity-50
                   focus:outline-none focus:ring-2 focus:ring-cuidai-500 focus:ring-offset-2"
      >
        {isSubmitting ? (
          <span className="flex items-center justify-center gap-2">
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            A registar...
          </span>
        ) : (
          'Registar como Cuidador'
        )}
      </button>
    </form>
  )
}
```

---

## Output anti-patterns

- **Schema genérico colado do template** — `name/email/message` entregues sem adaptar ao modelo de dados do cliente
- **Validação só no client** — Server Action não re-valida; qualquer `curl` bypassa todas as regras
- **`onSubmit` sem try/catch** — erro de rede silencioso; utilizador fica preso sem feedback
- **Labels em falta ou quebradas** — `placeholder` usado como substituto de label; leitores de ecrã cegos
- **Botão não desabilitado durante submit** — double-click cria dois registos/pagamentos/leads duplicados
- **Mensagens de erro em inglês** — `'String must contain at least 2 character(s)'` visível ao utilizador final
- **Success state não existe** — utilizador não sabe se o form foi submetido; volta a submeter
- **Multi-step perde dados ao navegar** — step 1 re-vazio quando utilizador volta do step 2
- **Angle-brackets sobrevivem no output** — `<CLIENT_NAME>`, `<API_ENDPOINT>` literalmente presentes no código entregue
- **Form sem `noValidate`** — browser validation nativa conflitua com Zod e mostra popups inconsistentes
