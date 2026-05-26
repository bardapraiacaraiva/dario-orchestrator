# UPGRADE v12.1 — Design Intelligence Stack (2026-05-26)

## Summary

Added 3-layer design pipeline to DARIO orchestrator. Three new workers under
`dir_design_visual` squad. Two new skill chains. Zero changes to existing skills
(strictly additive).

## What shipped

### New workers in `company.yaml`

| Worker ID | Skill | Layer | Source |
|---|---|---|---|
| `worker-ui-ux-pro-max` | `ui-ux-pro-max:ui-ux-pro-max` | Reference DB | nextlevelbuilder marketplace, MIT |
| `worker-emil-design-eng` | `emil-design-eng` | Decision framework | emilkowalski git clone, 1703⭐ |
| `worker-dario-design-shotgun` | `dario-design-shotgun` | Exploration | Adapted from gstack /design-shotgun |

All three report to `dir-design-visual`. The `manages` list and `capabilities`
of `dir-design-visual` were extended (additive, no removals).

### New skill chains in `skill_chains.yaml`

1. **`design_reference_chain`** — Catalog → variants → tokens → landing page
   - Trigger: "landing page novo cliente", "novo design system", "criar website", "rebrand visual"
   - Steps: `ui-ux-pro-max` → `dario-design-shotgun` → `builder-design-system` → `builder-landing-page`
   - Estimated tokens: 28 000 · Output target: `client_facing`

2. **`design_decision_chain`** — Animation craft taste → implementation → a11y
   - Trigger: "adicionar animacao", "polish micro-interactions", "transicoes premium"
   - Steps: `emil-design-eng` → (`builder-animated-ui` OR `framer-motion-animator`) → `builder-accessibility-check`
   - Estimated tokens: 18 000 · Output target: `client_facing`

## Layering rationale (3-tier model)

```
┌─ DECISION LAYER ───────────────────────────────────┐
│  emil-design-eng                                    │
│  • Should this animate? (frequency-based)           │
│  • Easing rules (ease-out enter, never ease-in)     │
│  • Durations (button 100-160ms, modal 200-500ms)    │
│  • Component polish principles                      │
└────────────────────┬───────────────────────────────┘
                     ↓ informs
┌─ REFERENCE LAYER ──────────────────────────────────┐
│  ui-ux-pro-max                                      │
│  • 67 UI styles catalog (glassmorphism, bento, ...) │
│  • 161 industry-specific color palettes             │
│  • 57 curated Google Fonts pairings                 │
│  • 25 chart type recommendations                    │
│  • 99 UX guidelines + 161 reasoning rules           │
│  • 15 stacks (React, Vue, Flutter, SwiftUI, RN ...) │
└────────────────────┬───────────────────────────────┘
                     ↓ feeds
┌─ EXPLORATION LAYER ────────────────────────────────┐
│  dario-design-shotgun                               │
│  • Generate N=3-8 variants in parallel              │
│  • Comparison board side-by-side (HTML)             │
│  • Persistent taste profile (5%/week decay)         │
│  • Krug Three Laws of Usability                     │
└────────────────────┬───────────────────────────────┘
                     ↓ chosen variant feeds
┌─ GENERATOR LAYER (existing) ───────────────────────┐
│  builder-design-system, builder-landing-page,       │
│  builder-react-components, builder-animated-ui,     │
│  framer-motion-animator, aidesigner-frontend,       │
│  builder-brand-identity                             │
└────────────────────┬───────────────────────────────┘
                     ↓ gated by
┌─ QUALITY GATE (existing) ──────────────────────────┐
│  builder-accessibility-check (axe-core WCAG 2.1 AA) │
└────────────────────────────────────────────────────┘
```

## Routing rules (orchestrator dispatch)

When dispatch detects a UI/design task, evaluate in this order:

1. **User says "explore variants" / "show options"** → invoke `dario-design-shotgun` directly
2. **User says "animation" / "should this animate" / "motion"** → trigger `design_decision_chain`
3. **User says "landing page" / "novo design" / "rebrand visual"** → trigger `design_reference_chain`
4. **User picks specific style** ("brutalist landing", "claymorphism dashboard") → consult `ui-ux-pro-max` for that style's CSS keywords, then route to `builder-landing-page`
5. **Routine implementation** (no design exploration needed) → existing builders direct, no chain

The `dario-orchestrator` dispatch logic does NOT need code changes. Skill chain
triggers are keyword-based and read from `skill_chains.yaml` at runtime.

## Cost & quality expectations

- **`design_reference_chain` cost:** ~28K tokens (~$0.42 Sonnet or $2.10 Opus per run)
- **`design_decision_chain` cost:** ~18K tokens (~$0.27 Sonnet or $1.35 Opus per run)
- **Padrao A interaction:** Both chains end with `client_facing` output target. If a polished
  wrapper exists for the final step (`builder-landing-page-polished` future), it will be
  selected by execution_policy routing (per `dario-orchestrator` SKILL.md step 3).

## Files modified

- `~/.claude/orchestrator/company.yaml`:
  - Lines 505-528: extended `dir_design_visual.manages` and `capabilities`
  - After line 2282 (`worker-builder-wireframe`): added 3 new worker entries (~50 lines)
- `~/.claude/orchestrator/skill_chains.yaml`:
  - Inserted before `brand_to_market` chain: 2 new chains (~75 lines)
- `~/.claude/skills/dario-design-shotgun/SKILL.md`: created (2026-05-26)
- `~/.claude/skills/emil-design-eng/SKILL.md`: installed via git clone (28KB, 679 lines)
- `~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/`: marketplace + plugin installed
- `~/.claude/orchestrator/research/gstack_patterns_2026_05_26.md`: pattern mining notes
- `~/.claude/orchestrator/research/canary_policy_spec.md`: deferred spec
- `~/.claude/orchestrator/UPGRADE-v12.1-design-stack.md`: this file

## Open follow-ups (not blockers)

1. **Canary deployment policy** — `~/.claude/orchestrator/research/canary_policy_spec.md`
   waits for user decision on 4 open questions (flag vs separate skill, duration,
   auto-rollback, baseline location). ~2.75h estimated implementation when greenlit.

2. **Padrao A polished wrappers** for builders — `builder-landing-page-polished`,
   `builder-react-components-polished` candidates. Would unlock `execution_policy:
   client_facing` automatic upgrade for these generators in the chains above.

3. **Run a real test** of `design_reference_chain` end-to-end with a live client briefing
   to validate token estimate and quality gates.

4. **Update `MEMORY.md`** index with plugin evaluation session entry (done in this session).

## Rollback

If chains misbehave:
```bash
git -C ~/.claude/orchestrator diff company.yaml skill_chains.yaml
git -C ~/.claude/orchestrator checkout HEAD -- company.yaml skill_chains.yaml
```

Removing the 2 new skills (if needed):
```bash
rm -rf ~/.claude/skills/dario-design-shotgun
rm -rf ~/.claude/skills/emil-design-eng
# ui-ux-pro-max uninstall via plugin manager:
/plugin uninstall ui-ux-pro-max@ui-ux-pro-max-skill
```

## Validation

Verify Skill tool sees all three (next session start):
- `ui-ux-pro-max:ui-ux-pro-max` ✅ confirmed visible
- `emil-design-eng` ✅ confirmed visible (after session resume)
- `dario-design-shotgun` ✅ confirmed visible
