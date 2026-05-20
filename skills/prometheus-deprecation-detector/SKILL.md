---
name: prometheus-deprecation-detector
description: Scan skills + templates + configs do sistema DARIO em busca de referências a ferramentas/APIs/regras conhecidamente deprecated. Output flag-only em STALE_FACTS.yaml. Triggers em "scan deprecations", "detect stale", "find outdated", "audit deprecated".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable]
category: "Wave 2 — Decay Detector"
version: "1.0"
autonomy_tier: 1
---

# PROMETHEUS-DEPRECATION-DETECTOR

**Flag-only.** Detecta. Não edita. User aprova antes do fix.

## Knowledge base de deprecations conhecidas

Maintained em `~/.claude/orchestrator/prometheus/findings/deprecations_kb.yaml`. Updateable. Wave 2 baseline:

### Tools/Services deprecated
| Term | Deprecated since | Replacement | Source |
|---|---|---|---|
| Google Optimize | 2023-09 | GA4 + Optimize alternatives (VWO, Optimizely) | Google official sunset |
| Google Universal Analytics (UA) | 2023-07-01 | GA4 | Google official sunset |
| Heroku free tier | 2022-11-28 | Render, Railway, Fly.io | Salesforce sunset |
| LogMeIn (CareZone product) | 2021-05 | various caregivers apps | Walmart discontinued |
| Adobe Flash | 2020-12-31 | HTML5 | Adobe |
| Internet Explorer 11 | 2022-06-15 | Edge | Microsoft sunset |
| Jest @types/jest cli vs jest CLI | check version | use jest-cli >= 30 | Migration guide |
| ESLint legacy config (.eslintrc) | 2024 (deprecated, removed v10) | flat config (eslint.config.js) | ESLint docs |
| Vercel Edge Functions config | 2024 (consolidated) | App Router runtime config | Vercel docs |

### APIs deprecated
| API | Status | Action |
|---|---|---|
| Twitter API v1.1 | Removed 2023-06 | X API v2 |
| Facebook Graph API < v17 | Deprecated | Update to v18+ |
| Stripe API < 2023-08-16 | Outdated | Update to latest stable |

### Regulations / Standards superseded
| Old | New | Effective |
|---|---|---|
| RGPD Art. 6 sole-discretion (consent) | EDPB consent guidelines 2023 | 2023+ |
| AI Act draft Art. 5 | AI Act final Reg 2024/1689 | 2024-08 |
| LGPD Art. 11 antiga interpretação | ANPD Reg CD/ANPD 2026 | 2026 quando publicado |

## Workflow

```
1. Carregar deprecations_kb.yaml
2. Para cada skill em ~/.claude/skills/*/SKILL.md + templates/*/*.md:
   a. Ler conteúdo
   b. Grep case-insensitive por cada term do KB
   c. Se match: extrair contexto (linha + 2 surrounding lines)
   d. Tag severity (high/medium/low) baseado em deprecation_kb
3. Compilar findings:
   - skill_path : list[finding]
4. Escrever ~/.claude/orchestrator/prometheus/findings/STALE_FACTS.yaml
5. Output summary table no terminal
6. NO file edits.
```

## Real command (Python via bash)

```bash
python ~/.claude/orchestrator/prometheus/run_deprecation_scan.py
```

Ou manualmente:

```python
import yaml, re
from pathlib import Path

kb = yaml.safe_load(open(r'C:/Users/barda/.claude/orchestrator/prometheus/findings/deprecations_kb.yaml'))
skills_root = Path.home() / '.claude' / 'skills'

findings = []
for skill_md in skills_root.rglob('*.md'):
    content = skill_md.read_text(encoding='utf-8', errors='ignore')
    for term_entry in kb['terms']:
        term = term_entry['term']
        if re.search(re.escape(term), content, re.IGNORECASE):
            line_num = next(
                (i for i, l in enumerate(content.split('\n'), 1) if term.lower() in l.lower()),
                None
            )
            findings.append({
                'file': str(skill_md.relative_to(Path.home())),
                'term': term,
                'line': line_num,
                'replacement': term_entry.get('replacement'),
                'severity': term_entry.get('severity', 'medium'),
            })

# Write
out = Path.home() / '.claude' / 'orchestrator' / 'prometheus' / 'findings' / 'STALE_FACTS.yaml'
out.write_text(yaml.dump({'scan_at': '...', 'findings': findings}, sort_keys=False))
```

## Filter rules

For a finding to be flagged:
1. Term match (case-insensitive)
2. NOT inside a code block tagged as ``` "DEPRECATED" comment (false positive guard)
3. NOT in `prometheus-deprecation-detector` itself (would be self-referencing the KB)
4. NOT in `examples/` folder (intentional historical reference)

## Severity rubric

| Severity | Criteria | User action expected |
|---|---|---|
| 🔥 critical | Replacement mandatory (regulatory, removed API) | Fix imediato |
| ⚠️ high | Tool dead but functional alternatives exist | Plan migration <30d |
| 💤 medium | Better alternatives but still works | Note, no urgency |
| ℹ️ info | Historical reference (acceptable) | Skip flagging |

## Output format

`~/.claude/orchestrator/prometheus/findings/STALE_FACTS.yaml`:

```yaml
scan_at: '2026-05-20T19:30:00+00:00'
total_skills_scanned: 549
total_findings: N
by_severity: {critical: X, high: Y, medium: Z}
findings:
  - file: ".claude/skills/a360-validacao/templates/smoke-test-17-day.md"
    term: "Google Optimize"
    line: 224
    context: "⚠️ Google Optimize foi descontinuado em 2023..."
    replacement: "VWO, PostHog, GrowthBook"
    severity: medium
    note: "Already self-flagged in template — informational"
```

## Red flags

- Não modificar skills directamente — APENAS escrever em `findings/`
- Não criar issues em GitHub automaticamente — só flag
- Quando KB tem term ambíguo (e.g. "GA" pode ser Google Analytics OR Google Ads), exigir context match

## Maintenance

`deprecations_kb.yaml` é updated quando:
- prometheus-paper-tracker detecta papers anunciando deprecations
- prometheus-regulatory-watch detecta novas regulamentações
- User manualmente adiciona após findings de outras squads

## Cross-references

[[prometheus-director]] · [[prometheus-stale-fact-finder]] · [[prometheus-version-drift]]
