---
name: builder-animated-ui
description: >
  Componentes animados para landing pages e marketing: gradient text, bento grids, particles,
  morphing text, meteors, sparkles. Baseado em Magic UI (19K stars) + Framer Motion.
  Eleva landing pages de estatico para premium visual.
  Use quando: animacoes, landing page animada, motion, transicoes, efeitos visuais, premium UI.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Animated UI Components (Magic UI pattern)

## Proposito
Elevar landing pages de "estatico funcional" para "premium visual" com animacoes subtis.
Baseado em Magic UI (19K stars) — 150+ componentes animados para shadcn + Framer Motion.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-animated-ui hero` | Hero section com animacoes |
| `/builder-animated-ui bento` | Bento grid animada |
| `/builder-animated-ui [componente]` | Componente animado especifico |
| `/builder-animated-ui upgrade [pagina]` | Adicionar animacoes a pagina existente |

## Componentes Disponiveis

### Text Effects
- **AnimatedGradientText** — Headline com gradiente animado
- **SparklesText** — Texto com particulas sparkle
- **MorphingText** — Texto que morphs entre palavras
- **TypingAnimation** — Efeito typewriter
- **NumberTicker** — Contagem animada (ex: "500+ clientes")

### Layout
- **BentoGrid** — Grid estilo Apple com hover animations
- **Marquee** — Scroll horizontal infinito (logos, testimonials)
- **Dock** — macOS-style dock navigation
- **AnimatedList** — Items que aparecem em sequencia

### Visual Effects
- **Meteors** — Background particles
- **Particles** — Interactive particle field
- **RetroGrid** — Grid background animada
- **DotPattern** — Background dot pattern com mask
- **AnimatedBeam** — Beam que conecta elementos (diagrams)

### Interactive
- **MagicCard** — Card com efeito spotlight on hover
- **ShimmerButton** — CTA com efeito shimmer
- **GlowEffect** — Glow seguindo o cursor

## Regras de Uso
1. **Menos e mais** — max 3 animacoes por pagina
2. **Propositado** — cada animacao guia atencao (nao distrai)
3. **Performante** — `will-change: transform`, GPU-accelerated
4. **Respeitoso** — `prefers-reduced-motion` always respected
5. **Mobile-safe** — animacoes complexas desactivadas em mobile

## Install Pattern
```bash
npx shadcn@latest add "https://magicui.design/r/animated-gradient-text"
```

## Inspired by
- **magicuidesign/magicui** (19K stars) — 150+ animated shadcn components
- **framer/motion** (26K stars) — React animation library
