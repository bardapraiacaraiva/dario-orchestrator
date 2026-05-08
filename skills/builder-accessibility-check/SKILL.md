---
name: builder-accessibility-check
description: >
  Verifica acessibilidade WCAG 2.1 AA em todo o codigo UI gerado pelo DARIO. Detecta
  violacoes, sugere fixes, gera relatorio. Deve correr em CADA output de builder-*.
  Inspirado em axe-core (6K stars, 13M+ projectos). Quality gate obrigatorio.
  Use quando: acessibilidade, a11y, WCAG, aria, contraste, screen reader, teclado.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Accessibility Check (axe-core pattern)

## Proposito
QUALITY GATE obrigatorio: todo o codigo UI gerado por builder-* passa por este check
ANTES de ser entregue. Detecta violacoes WCAG 2.1 AA e sugere correcoes.

## Comandos
| Comando | Descricao |
|---------|-----------|
| `/builder-accessibility-check [ficheiro]` | Check um componente |
| `/builder-accessibility-check full [dir]` | Check todos os componentes |
| `/builder-accessibility-check fix [ficheiro]` | Auto-fix violacoes simples |

## Checks (baseados em axe-core rules)

### Critical (MUST fix)
- [ ] Imagens sem `alt` text
- [ ] Links sem texto acessivel
- [ ] Form inputs sem `label` associado (htmlFor)
- [ ] Botoes sem texto ou aria-label
- [ ] Contrast ratio < 4.5:1 (texto normal) ou < 3:1 (texto grande)
- [ ] Heading hierarchy quebrada (h1 → h3, salta h2)
- [ ] `tabIndex` > 0 (altera focus order)

### Serious (SHOULD fix)
- [ ] Sem `lang` no html root
- [ ] Color como unico indicador (ex: erro so com vermelho)
- [ ] Touch targets < 44x44px em mobile
- [ ] Auto-playing media sem controlos
- [ ] Scroll hijacking sem alternativa

### Moderate (NICE to fix)
- [ ] Links que abrem em nova tab sem aviso
- [ ] Falta de `aria-live` em conteudo dinamico
- [ ] Skip-to-content link ausente
- [ ] Focus visible nao customizado (outline generica)

## Output
```markdown
## Accessibility Report — [component/page]

### Score: 85/100 (AA Compliant with warnings)

### Critical Issues (0)
None — all critical checks pass.

### Serious Issues (2)
1. **Color-only indicator** in error state (line 45)
   - Current: `className="text-red-500"`
   - Fix: Add icon + text alongside color: `<AlertCircle className="inline mr-1" /> Error message`

2. **Touch target too small** — CTA button on mobile (line 78)
   - Current: `className="px-3 py-1"` (32x28px)
   - Fix: `className="px-4 py-2.5 min-h-[44px]"` (44px minimum)

### Passed (15/17)
✓ Alt text on images
✓ Labels on all inputs
✓ Heading hierarchy
✓ Contrast ratios
...
```

## Integration
- Corre AUTOMATICAMENTE apos: builder-landing-page, builder-react-components, builder-form-system
- Score < 70 → bloqueia entrega (quality gate)
- Score 70-85 → entrega com warnings
- Score > 85 → entrega clean

## Inspired by
- **dequelabs/axe-core** (6K stars, 13M+ projectos) — WCAG testing engine
- **@axe-core/playwright** — CI integration for automated testing
