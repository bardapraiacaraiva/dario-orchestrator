---
name: prometheus-stale-fact-finder
description: Cross-check claims factuais em skills (preços, versões, métricas, datas) contra fontes web actuais. Output flag-only em STALE_FACTS.yaml. Triggers em "scan stale facts", "verify facts", "audit factuality", "check claims".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable]
category: "Wave 2 — Decay Detector"
version: "1.0"
autonomy_tier: 1
---

# PROMETHEUS-STALE-FACT-FINDER

**Flag-only.** Verifica claims factuais em skills vs estado actual. Nunca edita.

## Tipos de claims monitorados

| Categoria | Exemplo de claim em skill | Forma de verificar |
|---|---|---|
| **Pricing of LLM models** | "Opus 4.6: $5/M input" | Anthropic pricing page |
| **Tool pricing** | "Mailchimp free até 500 contactos" | Mailchimp pricing page |
| **API versions** | "Stripe API 2023-08-16" | Stripe API changelog |
| **Regulatory deadlines** | "DORA enforcement Jan 2025" | EUR-Lex |
| **Tool capabilities** | "GA4 free tier limits 10M events/mo" | Google docs |
| **Market data** | "BRbid ARR R$ 8-12M" | Crunchbase / public reports |
| **Library versions** | "Next.js 14 stable" | next.js docs |
| **Browser support** | "ES2022 supported in all browsers" | caniuse.com |
| **Numerical claims** | "5570 prefeituras BR" | IBGE |

## Workflow

```
1. Extrair claims das skills usando regex patterns:
   - Currency: R$ X / EUR X / USD X
   - Versions: vN.M.X
   - Percentages: X%
   - Dates: YYYY-MM
   - Specific numerical assertions
2. Para cada claim:
   a. Lookup em fact_sources.yaml (mapping claim_type → URL canonical)
   b. Fetch source
   c. Extract current value
   d. Diff vs claim em skill
3. Compile findings:
   - severity (delta % do valor):
     >50% diff: critical
     20-50%: high
     5-20%: medium
     <5%: ignore (within rounding)
4. Write findings/STALE_FACTS.yaml (append-mode)
```

## Fact sources (canonical)

`~/.claude/orchestrator/prometheus/findings/fact_sources.yaml`:

```yaml
sources:
  anthropic_pricing:
    url: https://www.anthropic.com/pricing
    last_known:
      claude-opus-4-7: {input: 5, output: 25, unit: $_per_M}
      claude-sonnet-4-6: {input: 3, output: 15}
      claude-haiku-4-5: {input: 0.8, output: 4}
    check_freq: weekly

  stripe_api_version:
    url: https://stripe.com/docs/api/versioning
    last_known_stable: '2024-11-20'
    check_freq: monthly

  next_js_version:
    url: https://github.com/vercel/next.js/releases/latest
    last_known: '15.x'
    check_freq: weekly

  ibge_munis_br:
    url: https://www.ibge.gov.br/cidades-e-estados
    last_known: 5570
    check_freq: yearly

  bcb_pix_limits:
    url: https://www.bcb.gov.br/estabilidadefinanceira/pix
    check_freq: monthly

  eu_ai_act:
    url: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
    last_known_status: in_force
    check_freq: monthly
```

## Filter rules (avoid false positives)

1. Skip claims dentro de `examples/` folder (intentional historical data)
2. Skip claims dentro de blockquotes ou tagged `[ASSUMPTION]`
3. Skip claims relativos ("aproximadamente", "cerca de", "~")
4. Skip se claim tiver `<source: URL>` inline — assume source provided
5. Skip claims em prompt_hints (são padrões observados, não factos absolutos)

## Output format

`STALE_FACTS.yaml` (shared com deprecation-detector via append):

```yaml
scan_at: '2026-05-20T19:35:00+00:00'
source_type: stale_fact_finder
findings:
  - file: ".claude/skills/a360-modelo/SKILL.md"
    line: 88
    claim_text: "Charm pricing ($97 vs $100) for consumer"
    claim_type: pricing_psychology_example
    severity: ignore_example
    note: "Example value, not assertion — skip"

  - file: ".claude/skills/a360-modelo/examples/saas-hybrid-debt-recovery-br.md"
    line: 14
    claim_text: "Cap inicial | R$ 80K"
    claim_type: project_specific
    severity: ignore_example
    note: "Anonymized historical example — skip"

  - file: ".claude/skills/atlas-fin-pix-rules-bcb/SKILL.md"
    line: 32
    claim_text: "PIX limit R$ 20K/transaction noturno"
    claim_type: bcb_pix_limit
    fetched_current: "R$ 1K/transaction noturno (BCB Resolução 198 2022)"
    severity: critical
    delta: "20x diferença"
    recommendation: "Fix urgent — limit reduzido pela BCB pós-incidentes 2022"
```

## Performance considerations

- Cache fetched sources for 24h (não bater URL toda chamada)
- Rate limit web fetches: 1/segundo per host
- Total scan should complete <5 min for 549 skills

## Red flags

- NEVER edit a skill claiming to "fix" — só flag
- NEVER auto-update fact_sources.yaml — user maintains
- Web fetches timeout aggressively (5s) — não bloquear scan inteiro

## Cross-references

[[prometheus-director]] · [[prometheus-deprecation-detector]] · [[prometheus-version-drift]]
