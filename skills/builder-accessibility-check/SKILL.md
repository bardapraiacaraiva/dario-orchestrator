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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Violações Critical identificadas com localização exacta
- [ ] Cada violação Critical lista ficheiro + linha exacta (ex: `LoginForm.tsx:34`)
- [ ] Fix sugerido inclui código antes/depois, não só descrição
- [ ] Ratio de contraste calculado com valores reais (ex: `3.2:1 → precisa 4.5:1`)
- [ ] Imagens sem alt listadas com src parcial identificável

❌ NOT delivery-ready: `"Alguns botões não têm aria-label"`
✅ Delivery-ready: `Button sem aria-label — CuidaiApp/src/components/Header.tsx:87 | Fix: adicionar aria-label="Abrir menu de navegação"`

---

### Gate 2 — Score calculado com metodologia transparente
- [ ] Score numérico presente (ex: `72/100`) com breakdown visível
- [ ] Fórmula ou peso por severidade explicado (Critical=−15, Serious=−7, Moderate=−3)
- [ ] Status de entrega declarado: BLOQUEADO / COM WARNINGS / CLEAN
- [ ] Número de checks total passado vs total (ex: `18/21 checks passed`)

❌ NOT delivery-ready: `"Score: alto. Componente está razoavelmente acessível"`
✅ Delivery-ready: `Score: 78/100 — 14/17 passed | −7 (1× Serious) −15 (n/a) | Status: ⚠️ ENTREGA COM WARNINGS`

---

### Gate 3 — Serious issues com fix copy-paste ready
- [ ] Cada Serious issue tem className/atributo actual e substituto
- [ ] Touch targets indicam dimensão actual em px (ex: `32×28px`)
- [ ] Fix proposto não introduz novas violações (ex: aria-label não duplica texto visível)
- [ ] Color-only indicators têm alternativa com ícone + texto especificada

❌ NOT delivery-ready: `"Botão muito pequeno no mobile — aumentar tamanho"`
✅ Delivery-ready: `Touch target insuficiente — CTA "Aderir Agora" (36×30px) | Fix: className="px-4 py-2.5 min-h-[44px] min-w-[44px]"`

---

### Gate 4 — Heading hierarchy e estrutura semântica verificadas
- [ ] Mapa de headings documentado sequencialmente (h1→h2→h3, sem saltos)
- [ ] `lang` no html root confirmado ou flagged
- [ ] `tabIndex > 0` ausente ou justificado com contexto
- [ ] Skip-to-content link presença/ausência declarada explicitamente

❌ NOT delivery-ready: `"Hierarquia de headings parece OK"`
✅ Delivery-ready: `Hierarquia: h1("Dashboard") → h2("Resumo") → h3("Transacções") ✓ | lang="pt" presente ✓ | Skip-link ausente — Moderate #3`

---

### Gate 5 — Passed checks listados (prova de cobertura total)
- [ ] Secção "Passed" lista cada check individualmente, não agrupada
- [ ] Mínimo 10 checks nomeados explicitamente como ✓ passados
- [ ] Labels/htmlFor coverage indicada (ex: `4/4 inputs com label associado`)
- [ ] ARIA roles utilizados listados e validados (ou "nenhum role custom usado")

❌ NOT delivery-ready: `"✓ Acessibilidade geral OK | ✓ Formulários"`
✅ Delivery-ready: `✓ alt text (3/3 imagens) ✓ labels (5/5 inputs) ✓ contraste body 7.2:1 ✓ contraste CTA 5.1:1 ✓ heading hierarchy ✓ lang="pt"...`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] Nome do componente/página é real, não `[component]` ou `<PageName>`
- [ ] Ficheiros referenciados existem no projecto do cliente (path verificável)
- [ ] Cliente identificado no header do relatório (ex: `Accessibility Report — SAQUEI / TransferModal.tsx`)
- [ ] Zero placeholders `<client>`, `[ficheiro]`, `YOUR_COMPONENT` no output final

❌ NOT delivery-ready: `"Accessibility Report — [component/page] — Score: XX/100"`
✅ Delivery-ready: `"Accessibility Report — LUSOconta / OnboardingForm.tsx — Score: 81/100 (AA com warnings)"`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/score/violação/referência no accessibility report deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via análise estática do código (ficheiro + linha inspecionada)
- 🟡 **assumed** — plausível com base em padrões comuns, mas requer confirmação do cliente antes da entrega
- 🟢 **projection** — estimativa por design (ex: score projectado após aplicar fixes sugeridos)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. o que precisa de verify. **Honest transparency > inflated accessibility score.**

❌ NOT delivery-ready: `Score: 85/100 — contrast ratio OK, touch targets OK` — sem labels; reader assume que tudo foi verificado no código real, mas alguns valores podem ser estimados ou baseados em defaults do Tailwind.

✅ Delivery-ready:
- 🔵 **verified** — `Button sem aria-label — Header.tsx:87` (ficheiro inspeccionado, linha confirmada)
- 🟡 **assumed** — `Contrast ratio estimado em 4.8:1` (baseado em classe `text-gray-600 / bg-white`; validar com ferramenta se tema customizado override as cores)
- 🟢 **projection** — `Score projectado: 92/100 após aplicar os 2 fixes sugeridos` (não verificado; requer re-run do check)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmados — contrast ratios validados com valores reais do tema (não só classes CSS)
- [ ] All 🔵 citations presentes — cada violação lista ficheiro + linha exacta como fonte
- [ ] All 🟢 projections comunicadas ao cliente como estimativas — re-run obrigatório após fixes para score final

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Accessibility Report — SAQUEI / RequestLoanForm.tsx

### Score: 76/100 — ⚠️ ENTREGA COM WARNINGS
**Breakdown:** 14/17 checks passed | −7 (1× Serious) −7 (1× Serious) −0 Critical | Moderate: 1× aviso
**Status:** Score 70–85 → entrega permitida com warnings obrigatoriamente comunicados

---

### Critical Issues (0) ✅
Nenhuma violação crítica detectada. Todos os checks críticos passam.

---

### Serious Issues (2)

**S-1 — Color-only indicator no estado de erro** `RequestLoanForm.tsx:52`
- Situação: campo "Montante" mostra erro apenas com `className="border-red-500 text-red-500"`
- Problema: utilizadores daltónicos ou em screen reader não percepcionam o erro
- Fix:
  ```tsx
  // Antes
  <p className="text-red-500 text-sm">Montante inválido</p>

  // Depois
  <p className="text-red-500 text-sm flex items-center gap-1">
    <AlertCircle className="h-4 w-4" aria-hidden="true" />
    Montante inválido
  </p>
  ```

**S-2 — Touch target abaixo do mínimo** `RequestLoanForm.tsx:89`
- Situação: botão "Simular Crédito" renderiza `28×36px` em viewport 375px
- Problema: WCAG 2.5.5 exige mínimo 44×44px em dispositivos touch
- Fix:
  ```tsx
  // Antes
  <button className="px-3 py-1 bg-saquei-green text-white rounded">

  // Depois
  <button className="px-5 py-2.5 min-h-[44px] min-w-[44px] bg-saquei-green text-white rounded">
  ```

---

### Moderate Issues (1)

**M-1 — Skip-to-content link ausente** `layout/AppShell.tsx` (global)
- Impacto: utilizadores de teclado percorrem toda a navegação antes de chegar ao form
- Fix sugerido:
  ```tsx
  // Adicionar como primeiro elemento do <body>
  <a href="#main-content"
     className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 
                focus:z-50 focus:bg-white focus:px-4 focus:py-2 focus:rounded">
    Saltar para conteúdo principal
  </a>
  ```
- Prioridade: implementar antes de go-live

---

### Passed (14/17) ✅

✓ **Alt text** — 3/3 imagens com alt descritivo (`logo SAQUEI`, `ícone segurança`, `ícone rápido`)
✓ **Labels** — 5/5 inputs com `htmlFor` associado correctamente (nome, NIF, montante, prazo, IBAN)
✓ **Botões** — 4/4 com texto visível ou `aria-label` explícito
✓ **Contraste — texto body** — `#1A1A1A` sobre `#FFFFFF` = 18.1:1 ✓ (mínimo 4.5:1)
✓ **Contraste — CTA primário** — `#FFFFFF` sobre `#00A651` = 5.2:1 ✓ (mínimo 4.5:1)
✓ **Contraste — placeholder** — `#6B7280` sobre `#FFFFFF` = 4.6:1 ✓
✓ **Heading hierarchy** — h1("Pedido de Crédito") → h2("Dados Pessoais") → h2("Simulação") ✓
✓ **lang no root** — `<html lang="pt">` confirmado em `index.html`
✓ **tabIndex** — nenhum `tabIndex > 0` detectado no componente
✓ **Links acessíveis** — 2/2 links com texto descritivo (sem "clique aqui")
✓ **Sem auto-play** — nenhum media auto-play presente
✓ **ARIA roles** — nenhum role custom; roles nativos HTML usados correctamente
✓ **Formulário** — `<form>` com `aria-labelledby` apontando para h1 ✓
✓ **Erros** — `aria-describedby` liga inputs às mensagens de erro ✓

---

### Próximos passos recomendados
1. **Antes de entregar:** corrigir S-1 e S-2 (15 min estimado)
2. **Antes de go-live:** implementar skip-link global em AppShell.tsx
3. **Sprint seguinte:** adicionar `aria-live="polite"` na área de resultado da simulação
```

---

## Output anti-patterns

- Listar violações sem localização (ficheiro:linha) — inutilizável para o dev corrigir
- Score sem breakdown — "85/100" sem explicar o que penalizou não é auditável
- Fix descrito em prosa em vez de código antes/depois — gera retrabalho e ambiguidade
- Secção "Passed" vazia ou colapsada em "✓ Tudo OK" — remove prova de cobertura
- Usar valores de contraste aproximados ("parece bom") em vez de ratio calculado
- Reportar Moderate como Critical — degrada confiança nos thresholds de bloqueio
- Placeholder `[component]` no header do relatório entregue ao cliente
- Sugerir fix que viola outro check (ex: `aria-label` duplicando texto visível → redundância)
- Omitir status de entrega (BLOQUEADO/WARNINGS/CLEAN) — cliente não sabe o que fazer
- Misturar checks de diferentes componentes no mesmo relatório sem separação clara
