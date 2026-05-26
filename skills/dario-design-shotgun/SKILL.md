---
name: dario-design-shotgun
description: >
  Gera N variantes de design visual (3-5) antes de qualquer single-shot. Comparison board
  side-by-side, persistent taste profile com decay, conflict-aware. Inspirado em
  garrytan/gstack /design-shotgun mas adaptado ao stack DARIO (aidesigner-frontend +
  builder-design-system + emilkowalski/skill).
  Use quando: explorar designs, mostrar opcoes, design variants, visual brainstorm,
  "nao gosto desta versao", "tens outras alternativas?".
tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
version: 1.0.0
license: MIT
---

# DARIO Skill — Design Shotgun (multi-variant visual exploration)

Visual brainstorming, not a review process. Gera N opcoes em paralelo, mostra lado a lado,
itera ate o utilizador aprovar uma direccao. Substitui o anti-pattern "AI gera 1 design e
utilizador pede iteracao N vezes" por "AI gera N variantes em 1 turn e utilizador escolhe".

## When to activate

- Utilizador descreve uma feature/screen UI sem ter visto opcoes ainda
- Utilizador diz "nao gosto desta versao", "tens outras opcoes?", "explora variantes"
- Antes de `builder-landing-page`, `builder-react-components`, ou `aidesigner-frontend`
  comprometerem a um design unico
- Pedido explicito: "design shotgun", "visual brainstorm", "mostra-me opcoes"

Do NOT activate when:
- Utilizador ja aprovou uma direccao visual (segue direto para o builder)
- Pedido tecnico sem componente visual (API, schema, deploy)
- Iteracao incremental num design ja aprovado (usar `aidesigner-frontend` refine em vez)

## Workflow (4 phases)

### Phase 0: Session detection

Verificar sessoes anteriores deste projeto:

```bash
PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
DESIGN_DIR=~/.claude/dario-design/$PROJECT_SLUG
mkdir -p "$DESIGN_DIR"
ls "$DESIGN_DIR"/approved-*.json 2>/dev/null | head -3
```

Se houver sessoes anteriores: mostrar resumo (data, screen, escolha), oferecer
`Revisitar | Nova exploracao | Continuar de onde parou`.

### Phase 1: Context gathering (max 2 rounds)

Required context (5 dimensoes):
1. **Who** — persona, audience, expertise level
2. **Job to be done** — o que o utilizador final tenta fazer neste screen
3. **What exists** — codigo/componentes/patterns ja no projeto
4. **User flow** — como chegam aqui, para onde vao a seguir
5. **Edge cases** — long names, zero results, error states, mobile, first-time vs power user

Auto-gather primeiro (zero perguntas):
- `cat DESIGN.md 2>/dev/null | head -80` (design system existente)
- `ls src/ app/ pages/ components/ 2>/dev/null | head -30` (codebase)
- Consultar taste profile (se existe)

**AskUserQuestion** apenas o que ficou missing, pre-filling o que ja sabes.
Maximum 2 rounds de gathering, depois proceed com assumptions marcadas.

### Phase 2: Taste memory consult

Ler `~/.claude/dario-design/$PROJECT_SLUG/taste-profile.json` (schema v1):

```json
{
  "version": 1,
  "dimensions": {
    "fonts": {
      "approved": [{ "value": "Geist Sans", "confidence": 0.85, "approved_count": 4, "last_seen": "2026-05-20" }],
      "rejected": [{ "value": "Roboto", "confidence": 0.7, "rejected_count": 2 }]
    },
    "colors": { "approved": [...], "rejected": [...] },
    "layouts": { "approved": [...], "rejected": [...] },
    "aesthetics": { "approved": [...], "rejected": [...] }
  },
  "sessions": [{ "date": "2026-05-20", "screen": "landing hero", "chosen_variant": "v3" }]
}
```

**Decay rule:** confidence decresce 5% por semana sem reaproval (computed at read time).
Font aprovada ha 6 meses com 10 approvals < font aprovada na semana passada com 2 approvals.

**Conflict handling:** se request actual contradiz signal persistente strong:
> "O teu taste profile prefere minimalismo (confidence 0.92). Pediste 'playful' desta vez.
> Sigo o pedido. Treat como one-off ou update profile?"

### Phase 3: Variant generation (parallel)

**Default N=3, up to 8 para screens importantes (hero, checkout, dashboard).**

Gerar variantes em paralelo via Agent tool:

```python
# 3 Agent calls em paralelo (mesma message)
Agent({ description: "Variant A: minimal Swiss", prompt: "..." })
Agent({ description: "Variant B: editorial brutalist", prompt: "..." })
Agent({ description: "Variant C: warm playful", prompt: "..." })
```

Cada variant deve diferir em **eixo principal** (nao 3 variacoes da mesma estetica):
- Variant A: estetica X, font family Y, paleta Z
- Variant B: estetica W, font family V, paleta U
- Variant C: estetica T, font family S, paleta R

**Tools disponiveis para geracao:**
- `aidesigner-frontend` (MCP) → cada variant em HTML/React standalone
- `builder-design-system` → tokens diferentes por variant
- `builder-landing-page` → page completa por variant
- Se `ui-ux-pro-max-skill` instalado: consultar 67 UI styles + 161 paletas para diversificar
- Se `emil-design-eng` instalado: cada variant respeita animation framework

### Phase 4: Comparison board + collection

Output: **HTML side-by-side** salvo em `~/.claude/dario-design/$PROJECT_SLUG/board-{ts}.html`:

```html
<!DOCTYPE html>
<html>
<head><title>Design Shotgun — {feature} — {timestamp}</title></head>
<body style="display:grid;grid-template-columns:repeat({N},1fr);gap:24px;padding:24px">
  <div><h2>Variant A — {label}</h2><iframe srcdoc="..."></iframe><button>Choose A</button></div>
  <div><h2>Variant B — {label}</h2><iframe srcdoc="..."></iframe><button>Choose B</button></div>
  <div><h2>Variant C — {label}</h2><iframe srcdoc="..."></iframe><button>Choose C</button></div>
</body>
</html>
```

Abrir no browser: `start "" "file://...board.html"` (Windows) ou `open` (Mac).

**AskUserQuestion** estruturado para escolha:
- Options: A / B / C / Mix (combinar elementos) / None (regenerar)
- Se Mix: pedir "elementos de A: ___, elementos de B: ___"
- Se None: pedir feedback "o que falta?" e regenerar 3 novas variantes

### Phase 5: Persistence (after user picks)

```bash
mkdir -p ~/.claude/dario-design/$PROJECT_SLUG
echo '{ "session_id": "...", "chosen": "B", "feedback": "...", "ts": "..." }' \
  > ~/.claude/dario-design/$PROJECT_SLUG/approved-$(date +%s).json
```

Update taste profile:
- Chosen variant elements → approved bucket (confidence +0.05, approved_count++)
- Rejected variants elements → rejected bucket (confidence -0.03, rejected_count++)

Update Obsidian (D.A.R.I.O. vault):
- `05 - Claude - IA/Outputs/YYYY-MM-DD - Design Shotgun - {feature}.md` com board HTML embedded

## UX Principles (apply during variant generation)

### Three Laws of Usability (Krug)

1. **Don't make me think** — every screen self-evident. Falha = user stops to think
   "what does this mean?".
2. **Clicks don't matter, thinking does** — 3 mindless unambiguous clicks > 1 click
   that requires thought.
3. **Omit, then omit again** — remove half the words. Happy talk dies. Instructions die.

### How users actually behave

- Users **scan, don't read** — design billboards 60mph, not brochures
- Users **satisfice** — pick first reasonable option, not best. Make right choice most visible
- Users **muddle through** — once they find something that works (badly), they stick to it
- Users **don't read instructions** — guidance must be brief, timely, unavoidable

### Goodwill Reservoir

**Deplete faster:** hiding info users want (pricing, contact), punishing wrong format,
asking unnecessary info, splash screens, sloppy appearance.

**Replenish:** make obvious what users want, save steps, easy error recovery, apologize when in doubt.

### Mobile = same rules, higher stakes

44px minimum touch targets. No hover-to-discover (no cursor on touch). Affordances VISIBLE.
Prioritize ruthlessly: things needed in hurry close at hand.

## Quality gate

Before declaring done:
- [ ] N >= 3 variants (default), diverged on principal axis (estetica/font/paleta)
- [ ] Comparison board renders side-by-side, no overlap
- [ ] User picked (or explicitly requested regen)
- [ ] Taste profile updated (or new file created)
- [ ] Session log saved to `~/.claude/dario-design/$PROJECT_SLUG/`
- [ ] Obsidian note created in 05 - Outputs

## Anti-patterns

- **Generate 1 design and ask "what do you think?"** — single-shot defeats the entire skill
- **Generate 3 variations of the same estetica** — variants must differ on principal axis
- **Skip taste profile read** — ignores cross-session learning
- **No quality gate on individual variants** — bad variants pollute the choice
- **Fail to persist choice** — next session starts from zero again

## Integration with DARIO stack

| Use case | Skill chain |
|---|---|
| Landing page novo cliente | `dario-design-shotgun` → escolha → `builder-landing-page` com variant escolhida |
| Dashboard SaaS | `dario-design-shotgun` → escolha → `builder-react-components` + `builder-design-system` |
| Brand visual identity | `dario-brand` → `dario-design-shotgun` (3 visual interpretations) → escolha → `builder-brand-identity` |
| Componente novo | `dario-design-shotgun` (3 variants) → escolha → `builder-react-components` |

## Credit

Pattern inspirado em `garrytan/gstack /design-shotgun` (102K stars, MIT). UX Principles
section sintetiza Krug "Don't Make Me Think". Adaptado ao stack DARIO: nao usa o
binario gstack-design (GPT Image API), usa o stack instalado (aidesigner MCP +
builder-* + opcionalmente ui-ux-pro-max + emil-design-eng).

Reject decision rationale documented in `~/.claude/orchestrator/research/gstack_patterns_2026_05_26.md`.
