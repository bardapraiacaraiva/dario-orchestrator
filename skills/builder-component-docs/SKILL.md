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
