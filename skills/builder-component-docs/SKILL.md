---
name: builder-component-docs
description: >
  Auto-gera documentacao de componentes: props, variants, exemplos, stories Storybook.
  De componente React para documentacao completa sem esforco manual.
  Use quando: documentar componentes, storybook, props, API componentes, component docs.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Component Documentation Generator

## Proposito
Auto-gerar docs para CADA componente produzido pelo DARIO. Zero docs manuais.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-component-docs [componente]` | Docs para um componente |
| `/builder-component-docs all [dir]` | Docs para todos os componentes |
| `/builder-component-docs storybook [comp]` | Storybook story |

## Output per component

### 1. MDX Documentation
```mdx
# Button

A versatile button component with multiple variants and sizes.

## Usage
\`\`\`tsx
import { Button } from '@/components/ui/button'

<Button variant="default" size="md">Click me</Button>
\`\`\`

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'default' \| 'destructive' \| 'outline' \| 'ghost' | 'default' | Visual style |
| size | 'sm' \| 'md' \| 'lg' \| 'icon' | 'md' | Size |
| isLoading | boolean | false | Show loading spinner |
| disabled | boolean | false | Disable interaction |

## Examples
[Default] [Destructive] [Outline] [Loading] [With Icon]
```

### 2. Storybook Story
```typescript
// button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './button'

const meta: Meta<typeof Button> = {
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: { control: 'select', options: ['default','destructive','outline','ghost'] },
    size: { control: 'select', options: ['sm','md','lg','icon'] },
  },
}
export default meta

type Story = StoryObj<typeof Button>

export const Default: Story = { args: { children: 'Button' } }
export const Destructive: Story = { args: { children: 'Delete', variant: 'destructive' } }
export const Loading: Story = { args: { children: 'Saving...', isLoading: true } }
```

## Inspired by
- **southleft/story-ui** — AI Storybook story generator
- **Storybook autodocs** — Auto-generated prop tables

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Props table está completa e tipada
- [ ] Cada prop tem Type, Default e Description preenchidos (sem células vazias)
- [ ] Types usam union literals reais (`'default' | 'destructive'`) não genéricos (`string`)
- [ ] Defaults refletem o comportamento real do componente (não "N/A" ou "—")
- ❌ NOT delivery-ready: `| onClick | function | — | Handler |`
- ✅ Delivery-ready: `| onClick | (event: React.MouseEvent) => void | undefined | Callback ao clicar no botão |`

### Gate 2 — Exemplos de código são copy-paste funcionais
- [ ] Import path corresponde à estrutura real do projeto (`@/components/ui/` vs `../components/`)
- [ ] Cada exemplo compila sem erros de tipo (props existem, valores válidos)
- [ ] Pelo menos 3 variants demonstradas com props diferentes
- ❌ NOT delivery-ready: `<Button variant="primary">` (variant não existe no tipo)
- ✅ Delivery-ready: `<PagamentoButton variant="destructive" size="sm" onClick={handleCancelar}>Cancelar Pagamento</PagamentoButton>`

### Gate 3 — Storybook story cobre os casos críticos
- [ ] `meta` tem `tags: ['autodocs']` e `argTypes` para todos os props controláveis
- [ ] Pelo menos uma Story por variant principal (Default, Loading, Disabled)
- [ ] Story names em inglês, sem espaços (convenção Storybook)
- [ ] Ficheiro nomeado `[componente].stories.tsx` no diretório correto
- ❌ NOT delivery-ready: Apenas `export const Default: Story = {}` sem args
- ✅ Delivery-ready: `export const EstadoPendente: Story = { args: { status: 'pendente', valor: 'R$ 1.250,00', dataVencimento: '2025-02-15' } }`

### Gate 4 — Documentação MDX está estruturada e navegável
- [ ] Header H1 com nome do componente, seguido de descrição de 1-2 linhas
- [ ] Secção `## Usage` com import + exemplo mínimo funcional
- [ ] Secção `## Props` com tabela completa
- [ ] Secção `## Examples` com pelo menos os estados: default, loading, disabled, error (quando aplicável)
- ❌ NOT delivery-ready: MDX sem secção de Usage, só com tabela de props isolada
- ✅ Delivery-ready: MDX com Usage mostrando `<TransacaoCard id="TRX-2847" valor={1500} moeda="BRL" status="aprovado" />` e tabela com 6 props tipadas

### Gate 5 — Componente source foi lido antes de documentar
- [ ] Props documentadas batem com as definidas no `interface` / `type` do ficheiro fonte
- [ ] Nenhuma prop inventada que não existe no componente real
- [ ] Valores de default extraídos dos defaultProps ou destructuring real (`size = 'md'`)
- ❌ NOT delivery-ready: Documentar `isLoading` como prop quando o componente usa `loading` (nome errado)
- ✅ Delivery-ready: Props extraídas via Read do `src/components/ui/button.tsx` e verificadas linha a linha

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nome do componente é o real do projeto (ex: `SaqueiCard`, `CuidaiButton`, `ArrrecadaModal`)
- [ ] Import paths refletem a estrutura de pastas real do cliente
- [ ] Exemplos usam valores do domínio do cliente (valores monetários, datas, estados reais)
- [ ] Zero placeholders do tipo `<ComponentName>`, `<YourApp>`, `<description here>`
- ❌ NOT delivery-ready: `import { Button } from '@/components/ui/button'` num projeto SAQUEI que usa `src/ui/`
- ✅ Delivery-ready: `import { SaqueiButton } from 'src/ui/SaqueiButton'` com exemplo `<SaqueiButton variant="outline" onClick={handleSolicitarAdiantamento}>Solicitar R$ 500</SaqueiButton>`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via leitura do ficheiro fonte do componente (Read tool executado)
- 🟡 **assumed** — plausível com base no padrão do projeto, mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — comportamento esperado/documentado por design (não verificável sem runtime)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verificação. **Honest transparency > documentação inflada.**

❌ NOT delivery-ready: Props table com `default: 'md'`, `variant: 'default'` e import path `@/components/ui/button` sem indicar se foram lidos do source — reader assume tudo verified quando pode ser tudo assumed.

✅ Delivery-ready:
- 🔵 `onClick: (event: React.MouseEvent) => void` — extraído do `interface ButtonProps` via Read
- 🟡 Import path `@/components/ui/button` — segue convenção observada no projeto, confirmar estrutura real de pastas
- 🟢 `isLoading` bloqueia interação enquanto spinner está visível — comportamento documentado, não testado em runtime

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumed import paths, variant names e defaultProps por actuals lidos do source
- [ ] All 🔵 citations added — cada prop documentada com referência ao ficheiro e linha de onde foi extraída (`button.tsx:L14`)
- [ ] All 🟢 projections labeled ao cliente — deixar claro que comportamentos de loading/disabled/error são documentação de intenção, não output de teste automatizado

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# StatusBadge

Exibe o estado atual de uma transação SAQUEI com cor e ícone correspondentes.
Usado em listagens de adiantamentos, histórico e painel do trabalhador.

## Usage
```tsx
import { StatusBadge } from 'src/ui/StatusBadge'

<StatusBadge status="aprovado" />
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| status | `'pendente' \| 'aprovado' \| 'recusado' \| 'processando'` | `'pendente'` | Estado da transação |
| size | `'sm' \| 'md'` | `'md'` | Tamanho do badge |
| showIcon | `boolean` | `true` | Exibe ícone à esquerda do label |
| label | `string` | `undefined` | Sobrescreve o label gerado automaticamente |

## Examples

### Aprovado
```tsx
<StatusBadge status="aprovado" />
// → badge verde com ✓ "Aprovado"
```

### Pendente (sem ícone)
```tsx
<StatusBadge status="pendente" showIcon={false} size="sm" />
// → badge amarelo pequeno "Pendente"
```

### Label customizado
```tsx
<StatusBadge status="processando" label="A processar no banco..." />
// → badge azul com spinner "A processar no banco..."
```

### Recusado
```tsx
<StatusBadge status="recusado" size="sm" />
// → badge vermelho com ✕ "Recusado"
```

---

```typescript
// StatusBadge.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { StatusBadge } from './StatusBadge'

const meta: Meta<typeof StatusBadge> = {
  component: StatusBadge,
  title: 'SAQUEI/StatusBadge',
  tags: ['autodocs'],
  argTypes: {
    status: {
      control: 'select',
      options: ['pendente', 'aprovado', 'recusado', 'processando'],
    },
    size: { control: 'radio', options: ['sm', 'md'] },
    showIcon: { control: 'boolean' },
    label: { control: 'text' },
  },
}
export default meta

type Story = StoryObj<typeof StatusBadge>

export const Aprovado: Story = {
  args: { status: 'aprovado' },
}

export const Pendente: Story = {
  args: { status: 'pendente', showIcon: false, size: 'sm' },
}

export const Processando: Story = {
  args: { status: 'processando', label: 'A processar no Banco do Brasil...' },
}

export const Recusado: Story = {
  args: { status: 'recusado', size: 'sm' },
}
```
```

---

## Output anti-patterns

- **Props inventadas**: Documentar props que não existem no source — sempre ler o ficheiro antes de gerar
- **Import paths genéricos**: Usar `@/components/ui/button` sem verificar a estrutura de pastas real do projeto cliente
- **Storybook story vazia**: `export const Default: Story = {}` sem `args` não demonstra nada nem activa os controlos
- **Types vagos**: `type: function` ou `type: object` em vez de `(val: string) => void` ou `{ id: string; nome: string }`
- **Exemplos não-compiláveis**: Passar `variant="primary"` quando o tipo só aceita `'default' | 'outline'`
- **Defaults incorretos**: Copiar "false" para todos os booleanos sem verificar os defaultProps reais
- **Documentar sem ler source**: Gerar docs a partir do nome do componente por inferência, sem Read do ficheiro `.tsx`
- **Labels em inglês num projeto PT**: Story titles e descrições no idioma errado para o contexto do cliente
- **Ausência do estado de erro**: Componentes de formulário/transação documentados sem o estado `error` ou `disabled`
- **MDX sem exemplos visuais**: Tabela de props isolada sem um único bloco de código com caso de uso real
