---
name: builder-visual-to-code
description: >
  Converte screenshots, wireframes, mockups e imagens de design em codigo React/Tailwind
  funcional. Usa visao multimodal para interpretar layout, cores, tipografia, espacamento.
  Inspirado em screenshot-to-code (71K stars). O elo entre wireframe e codigo production.
  Use quando: imagem para codigo, screenshot to code, mockup to react, design to code,
  converter imagem em pagina, replicar design.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Visual to Code (screenshot-to-code pattern)

## Proposito
Aceitar qualquer INPUT VISUAL (screenshot, wireframe, mockup, foto de whiteboard) e produzir
codigo React + Tailwind FUNCIONAL. O elo que faltava entre design e implementacao.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-visual-to-code [imagem]` | Converter imagem em React + Tailwind |
| `/builder-visual-to-code refine` | Iterar sobre output anterior |
| `/builder-visual-to-code section [imagem]` | Converter apenas uma seccao |

## Workflow

### 1. Analyze Visual Input
Quando recebe uma imagem, analisar:
- **Layout:** Grid? Flexbox? Columns? Stack? Sidebar + content?
- **Hierarchy:** O que e H1? O que e body? Onde esta o CTA?
- **Colors:** Extrair palette dominante (primary, bg, text, accent)
- **Typography:** Tamanho relativo dos textos, peso, font family
- **Spacing:** Padding, margin, gaps entre elementos
- **Components:** Identificar buttons, cards, inputs, badges, navbars
- **Responsive hints:** Se mostra mobile vs desktop layout

### 2. Map to React Components
Cada elemento visual mapeado para componente shadcn/ui ou custom:
```
[Navbar com logo + links + CTA]  → <Navbar />
[Hero com headline + CTA]        → <Hero />
[Grid 3 colunas com icones]      → <Features />
[Card com preco e botao]         → <PricingCard />
[Footer com links e social]      → <Footer />
```

### 3. Generate Production Code
Output: React + TypeScript + Tailwind CSS completo
- Semantic HTML (section, article, nav, main, footer)
- Responsive (mobile-first com sm:/md:/lg: breakpoints)
- Accessible (alt text, aria-labels, focus states)
- Dark mode support (dark: classes)
- Cores extraidas como CSS variables (nao hardcoded hex)

### 4. Fidelity Levels
| Level | O que replica | O que adapta |
|---|---|---|
| **Pixel-perfect** | Layout, cores, fonts exactas | Nada — replica 1:1 |
| **Structural** (default) | Layout e hierarquia | Cores e fonts mapeadas para design system |
| **Conceptual** | Estrutura geral | Tudo adaptado ao design system do projecto |

## Integration
| Depende de | Para que |
|---|---|
| `builder-design-system` | Mapear cores extraidas para tokens do projecto |
| `builder-react-components` | Reutilizar componentes existentes |
| `builder-landing-page` | Estrutura de seccoes como referencia |

## Inspired by
- **abi/screenshot-to-code** (71K stars) — Pipeline imagem → vision LLM → HTML/React
- **wandb/openui** (20K stars) — Text → live UI iteration
- **nexu-io/open-design** (30K stars) — Design systems as prompting context

## Red Flags
- Gerar sem semantic HTML — inacessivel
- Cores hardcoded em vez de CSS variables — impossivel tematizar
- Ignorar responsive — 60% mobile em PT
- Copiar texto da imagem como Lorem Ipsum — usar copy real ou placeholder claro
