---
name: prometheus-version-drift
description: Detecta skills que referenciam versões específicas de frameworks/libs/standards desatualizadas. Output flag-only em STALE_FACTS.yaml. Triggers em "scan versions", "version drift", "audit versions", "framework versions outdated".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable]
category: "Wave 2 — Decay Detector"
version: "1.0"
autonomy_tier: 1
---

# PROMETHEUS-VERSION-DRIFT

**Flag-only.** Detecta version drift em skills. Não edita.

## O que detecta

| Type | Pattern | Example |
|---|---|---|
| Framework versions | `Next\.js \d+(\.\d+)*` | "Next.js 14" → flag if current is 15+ |
| Library versions | `vN.M.X` | "react v18.2.0" → flag if outdated |
| Standard versions | `WCAG \d+\.\d+` | "WCAG 2.1" → flag if 2.2 is current |
| Regulation versions | `LGPD Art\. \d+` | "LGPD Art. 11" no contexto outdated |
| Frameworks específicos | `Tailwind v\d` | "Tailwind v3" → flag if v4+ stable |
| LLM model versions | `(claude|gpt|gemini)[\s-]?\d+\.\d+` | "Claude 4.6" → flag if 4.7 current |
| Library APIs | `MCP SDK v\d` | "MCP SDK v1" → flag se v2 stable |
| Compliance frameworks | `NIST CSF \d\.\d` | "NIST CSF 1.1" → flag if 2.0 current |

## Reference: known current versions

Maintained em `~/.claude/orchestrator/prometheus/findings/version_baselines.yaml`:

```yaml
last_updated: '2026-05-20'
frameworks:
  next.js: {current: '15.x', released: 2024-10}
  react: {current: '19.x', released: 2024-12}
  tailwind: {current: '4.x', released: 2024-09}
  shadcn-ui: {current: 'latest', cycle: rolling}
  vue: {current: '3.5.x', released: 2024-09}
  svelte: {current: '5.x', released: 2024-10}

llm_models:
  anthropic: {current: 'claude-opus-4-7', released: 2026-04-16}
  openai: {current: 'gpt-5.x', released: 2026-04}
  google: {current: 'gemini-3.x', released: 2026-04}

mcp:
  typescript_sdk: {current: '2.0.0-alpha.2', stable_expected: 2026-Q3}
  python_sdk: {current: '1.27.1'}
  servers_repo: {last_release: '2026.1.26'}

standards:
  wcag: {current: '2.2', released: 2023-10}
  oauth: {current: '2.1 in progress', stable: '2.0'}
  http: {current: 'HTTP/3', most_used: 'HTTP/2'}

regulations:
  rgpd: {in_force: 2018-05, last_amendment: 2023-EDPB-guidelines}
  ai_act: {in_force: 2024-08, full_compliance: 2026-08}
  dora: {in_force: 2025-01-17}
  lgpd: {in_force: 2020-08, last_amendment: 2025-CD-ANPD}
  pix_bcb: {last_circular: 'check monthly'}
```

## Workflow

```
1. Load version_baselines.yaml
2. Para cada skill em ~/.claude/skills/*/SKILL.md + templates/*/*.md:
   a. Aplicar regex patterns para extrair version mentions
   b. Para cada mention:
      - Normalize (e.g., "Next.js 14" → framework=next.js, version=14)
      - Compare semver vs current baseline
      - Compute drift gap (major/minor/patch versions behind)
3. Tag severity:
   - Major version behind: 🔥 critical
   - Minor: ⚠️ high
   - Patch: 💤 low (ignore unless security)
4. Skip if version is referenced AS HISTORY (e.g. "Since Next.js 13 introduced...")
5. Write findings to STALE_FACTS.yaml (append mode)
```

## Severity ladder

| Drift | Tag | User action |
|---|---|---|
| 0 versions (current) | ✅ ignore | none |
| 1 minor / patch behind | 💤 info | optional update on next refactor |
| 1 major behind | ⚠️ high | plan update next sprint |
| 2+ major behind | 🔥 critical | breaking risk, update agora |
| Deprecated framework | 🔥 critical | migrate to alternative |

## False positive guards

- Skip versions mentioned em CHANGELOG context: "Migration from Next.js 13 to 14..."
- Skip historical references: "Heroku free tier (deprecated 2022)..."
- Skip in `examples/` folder
- Skip if version já tem inline tag `[CURRENT AS OF YYYY-MM]`

## Output format (append to STALE_FACTS.yaml)

```yaml
findings:
  - file: ".claude/skills/builder-nextjs-app/SKILL.md"
    line: 12
    type: version_drift
    framework: next.js
    claimed_version: "14"
    current_version: "15.x"
    drift: "1 major behind"
    severity: high
    context_30chars: "Use Next.js 14 com App Router..."
    recommendation: "Update to Next.js 15 (released 2024-10). App Router stable since 13.4 — no breaking changes for basic usage."

  - file: ".claude/skills/builder-react-components/SKILL.md"
    line: 8
    type: version_drift
    framework: react
    claimed_version: "18.2"
    current_version: "19.x"
    drift: "1 major behind"
    severity: high
    recommendation: "React 19 stable since 2024-12. Server Components nativos. Update."
```

## Maintenance

`version_baselines.yaml` updated:
- Manualmente quando há major releases conhecidos
- prometheus-paper-tracker pode flag novos releases via Anthropic blog / GitHub
- Próxima iteração: auto-fetch latest stable de npm registry / github releases

## Red flags

- NEVER edit skill files — apenas flag
- NEVER assume "patch" updates são seguros sem CHANGELOG read
- Coordenação com `prometheus-deprecation-detector` (algumas versions são deprecated, não apenas old)

## Cross-references

[[prometheus-director]] · [[prometheus-deprecation-detector]] · [[prometheus-stale-fact-finder]]
