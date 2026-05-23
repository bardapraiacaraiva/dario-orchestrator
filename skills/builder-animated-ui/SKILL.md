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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Componentes instaláveis e funcionais
- [ ] Cada componente tem o comando `npx shadcn` exato e correto (não inventado)
- [ ] Import path corresponde ao ficheiro gerado pelo CLI (`@/components/magicui/...`)
- [ ] Dependências peer (framer-motion, clsx, tailwind-merge) mencionadas se necessário
- ❌ NOT delivery-ready: `import { Meteors } from "magic-ui"` — package name errado, não instala
- ✅ Delivery-ready: `npx shadcn@latest add "https://magicui.design/r/meteors"` → `import { Meteors } from "@/components/magicui/meteors"`

### Gate 2 — Máximo 3 animações por página respeitado
- [ ] Output lista explicitamente quais 3 animações foram escolhidas e porquê
- [ ] Justificação de cada animação: "guia atenção para X" não "fica bonito"
- [ ] Animações restantes da lista são explicitamente descartadas com razão
- ❌ NOT delivery-ready: Hero com Particles + MorphingText + Meteors + SparklesText + AnimatedBeam numa página só
- ✅ Delivery-ready: "Escolhido: AnimatedGradientText (headline), NumberTicker (social proof), ShimmerButton (CTA) — RestroGrid descartado: conflitaria com Meteors no z-index"

### Gate 3 — `prefers-reduced-motion` implementado
- [ ] Cada componente personalizado tem guard `useReducedMotion()` ou CSS `@media (prefers-reduced-motion: reduce)`
- [ ] Componentes Magic UI nativos: confirmar que a versão instalada já inclui o guard
- [ ] Animações críticas (ex: loading states) têm fallback estático funcional
- ❌ NOT delivery-ready: `animate={{ x: [0, 10, 0] }}` sem qualquer reduced-motion check
- ✅ Delivery-ready: `const shouldReduceMotion = useReducedMotion(); <motion.div animate={shouldReduceMotion ? {} : { x: [0,10,0] }}>`

### Gate 4 — Mobile safety verificada
- [ ] Animações com `Particles` ou `GlowEffect` desactivadas em viewport < 768px
- [ ] `BentoGrid` tem layout fallback (grid-cols-1) sem hover effects em touch devices
- [ ] Performance: componentes com `will-change` não aplicado a mais de 3 elementos simultâneos
- ❌ NOT delivery-ready: `<Particles quantity={150} />` sem `className="hidden md:block"`
- ✅ Delivery-ready: `<Particles quantity={80} className="hidden md:block" />` + static background em mobile

### Gate 5 — Props e customização com dados reais do cliente
- [ ] Cores do gradiente correspondem à palette do cliente (não os defaults roxo/azul Magic UI)
- [ ] `NumberTicker` mostra números reais do cliente (não "500+", "1000+", "99%")
- [ ] `MorphingText` usa palavras do domínio do cliente (não "Hello", "World", "Motion")
- ❌ NOT delivery-ready: `<AnimatedGradientText>Welcome to our platform</AnimatedGradientText>`
- ✅ Delivery-ready: `<AnimatedGradientText className="from-[#0EA5E9] to-[#6366F1]">Recupera o teu dinheiro em 48h</AnimatedGradientText>` (SAQUEI, cores brand)

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder
- [ ] Zero ocorrências de `<ClientName>`, `<color>`, `<your-text>`, `<NUMBER>` no output final
- [ ] Ficheiros têm nomes reais: `hero-cuidai.tsx` não `hero-component.tsx`
- [ ] Tailwind config snippet usa as cores hex reais do cliente se custom theme necessário
- ❌ NOT delivery-ready: `text="<insira slogan aqui>"` ou `from-<primary-color> to-<secondary-color>`
- ✅ Delivery-ready: `text="Cuidar começa aqui."` com `from-[#22C55E] to-[#15803D]` (Cuidai green palette)

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/componente/claim no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via Magic UI docs, repo, ou dados reais do cliente (codebase, brand guide)
- 🟡 **assumed** — plausível dado o contexto mas precisa de confirmação do cliente antes de entregar
- 🟢 **projection** — estimativa de impacto visual/performance por design (não verificável antes de produção)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs o que precisa de verify.  
**Honest transparency > inflated delivery.**

❌ **NOT delivery-ready:**
```
"Adicionámos AnimatedGradientText com as cores da vossa brand, NumberTicker a contar até 500,
e ShimmerButton no CTA — performance garantida em mobile."
```
*(zero labels — reader assume tudo verified, mas cores podem estar erradas, número pode ser fictício, performance não foi testada)*

✅ **Delivery-ready:**
```
- 🔵 AnimatedGradientText — install command verificado: `npx shadcn@latest add "https://magicui.design/r/animated-gradient-text"`
- 🟡 Gradient colours (#7C3AED → #3B82F6) — assumed da palette do site actual; confirmar com brand guide antes de ship
- 🟡 NumberTicker value "500+ clientes" — assumed do briefing verbal; confirmar número real com cliente
- 🔵 `prefers-reduced-motion` guard — presente na versão Magic UI 0.x via useReducedMotion() hook
- 🟢 +15-25% engagement no CTA estimado com ShimmerButton vs botão estático — projection baseada em padrões de animação, não em dados do cliente
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — cores do gradiente substituídas pelos hex reais da brand, números validados pelo cliente
- [ ] All 🔵 citations added — versão exacta do Magic UI e Framer Motion usada documentada no PR/README
- [ ] All 🟢 projections labeled as such ao cliente — "estimativa de impacto visual, não garantia mensurável"

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# SAQUEI — Hero Section Animada

## Componentes selecionados (3/3 budget)
1. **AnimatedGradientText** — headline principal (guia leitura imediata)
2. **NumberTicker** — social proof (ancora credibilidade)
3. **ShimmerButton** — CTA único (maximiza click-through)

*Descartados: Meteors (distrai do formulário), Particles (pesado em mobile), MorphingText (reduz clareza da proposta de valor)*

## Install
```bash
npx shadcn@latest add "https://magicui.design/r/animated-gradient-text"
npx shadcn@latest add "https://magicui.design/r/number-ticker"
npx shadcn@latest add "https://magicui.design/r/shimmer-button"
```

## `/components/saquei/hero-animated.tsx`

```tsx
"use client";

import { useReducedMotion } from "framer-motion";
import { AnimatedGradientText } from "@/components/magicui/animated-gradient-text";
import { NumberTicker } from "@/components/magicui/number-ticker";
import { ShimmerButton } from "@/components/magicui/shimmer-button";
import { cn } from "@/lib/utils";

export function SaqueiHeroAnimated() {
  const shouldReduce = useReducedMotion();

  return (
    <section className="relative flex min-h-[600px] flex-col items-center justify-center gap-8 px-4 py-24">
      {/* Badge */}
      <div className="flex items-center gap-2 rounded-full border border-[#F59E0B]/30 bg-[#F59E0B]/10 px-4 py-1.5">
        <span className="text-xs font-medium text-[#F59E0B]">
          Processo 100% digital
        </span>
      </div>

      {/* Headline com gradiente SAQUEI brand */}
      <AnimatedGradientText
        className={cn(
          "text-center text-5xl font-bold leading-tight md:text-7xl",
          "from-[#F59E0B] via-[#EF4444] to-[#F59E0B]",
          shouldReduce && "animate-none"
        )}
      >
        Recupera o que é teu.
      </AnimatedGradientText>

      <p className="max-w-xl text-center text-lg text-muted-foreground">
        Reclamações de consumo resolvidas sem advogados, sem filas,
        sem stress. Só resultados.
      </p>

      {/* Social proof com números reais */}
      <div className="flex gap-12">
        <div className="flex flex-col items-center">
          <div className="flex items-baseline gap-1">
            <NumberTicker
              value={2340}
              className="text-4xl font-bold text-[#F59E0B]"
            />
            <span className="text-2xl font-bold text-[#F59E0B]">+</span>
          </div>
          <span className="text-sm text-muted-foreground">casos resolvidos</span>
        </div>
        <div className="flex flex-col items-center">
          <div className="flex items-baseline gap-1">
            <NumberTicker
              value={94}
              className="text-4xl font-bold text-[#F59E0B]"
            />
            <span className="text-2xl font-bold text-[#F59E0B]">%</span>
          </div>
          <span className="text-sm text-muted-foreground">taxa de sucesso</span>
        </div>
        <div className="flex flex-col items-center">
          <div className="flex items-baseline gap-1">
            <NumberTicker
              value={48}
              className="text-4xl font-bold text-[#F59E0B]"
            />
            <span className="text-2xl font-bold text-[#F59E0B]">h</span>
          </div>
          <span className="text-sm text-muted-foreground">resposta média</span>
        </div>
      </div>

      {/* CTA */}
      <ShimmerButton
        shimmerColor="#F59E0B"
        background="#EF4444"
        className="px-10 py-4 text-lg font-semibold"
        onClick={() => window.location.href = "/reclamar"}
      >
        Iniciar reclamação grátis
      </ShimmerButton>

      <p className="text-xs text-muted-foreground">
        Sem cartão de crédito · Resultado em 48h · Cancelamento gratuito
      </p>
    </section>
  );
}
```

## Mobile behaviour
- `NumberTicker` ativo em todos os viewports (CPU leve)
- `AnimatedGradientText` reduz para `text-5xl` em mobile (já via responsive)
- `ShimmerButton` full-width em `< 640px`: adicionar `className="w-full sm:w-auto"`

## Performance checklist
- [x] `will-change: transform` apenas no ShimmerButton shimmer layer
- [x] `prefers-reduced-motion` via `useReducedMotion()` — desactiva gradient animation
- [x] Sem Particles: hero mantém < 50ms interaction latency em low-end Android
```

---

## Output anti-patterns

- Instalar componente via `import from "magic-ui"` ou `"@magic-ui/react"` — package não existe; sempre usar CLI `npx shadcn@latest add "https://magicui.design/r/[component]"`
- Usar mais de 3 animações distintas na mesma página sem justificação explícita de hierarquia visual
- Omitir `prefers-reduced-motion` guard em qualquer animação custom com Framer Motion
- Deixar cores dos componentes como defaults Magic UI (roxo `#8B5CF6` / azul `#3B82F6`) quando o cliente tem brand palette definida
- Gerar `NumberTicker` com valores inventados (`value={500}`, `value={99}`) sem confirmar dados reais do produto
- Aplicar `Particles` ou `GlowEffect` sem `className="hidden md:block"` — destrói performance em mobile mid-range
- Usar `MorphingText` em headlines com proposta de valor — o morfing atrasa leitura e reduz conversão
- Esquecer `"use client"` directive em ficheiros com hooks Framer Motion — quebra em Next.js App Router
- Entregar componente isolado sem mostrar onde encaixa na página (`page.tsx` ou layout pai)
- Placeholder copy nos exemplos: `"Your Amazing Product"`, `"Click here"`, `<slogan>` — sempre substituir por copy real do cliente
