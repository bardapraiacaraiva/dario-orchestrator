# DARIO ORCHESTRATOR v12.1 — MANUAL (Offline Reference)

> Quick offline reference. Para manual completo (4 partes detalhadas) ver Obsidian:
> `~/OneDrive/Documents/D.A.R.I.O/05 - Claude - IA/Outputs/2026-05-20 - DARIO v12.0 MANUAL*.md`

---

## SISTEMA EM 1 LINHA

**DARIO Orchestrator v12.1** = AI Enterprise OS com 32 squads / 536+ skills / 54 license tiers / 18 cognitive modules / 66+ engines / 5 jurisdições (PT+BR+EU+US+Global). v12.1 adiciona Meta-Evolution Layer (PROMETHEUS Squad) + A360 Premium upgrade + NASA Mission Control dashboard.

---

## INSTALAÇÃO

```bash
npx github:bardapraiacaraiva/dario-orchestrator-installer
python ~/.claude/orchestrator/license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO
```

---

## INVOKE 3 MÉTODOS

1. **Slash:** `/dario-brand`, `/dario-diagnose`, `/dream`, `/lucas-autopilot`
2. **Natural:** "Cria petição civil danos morais" → auto-activates `lex-civil`
3. **Explícito:** "Usa skill orion-prd-writing para esta feature"

---

## TOP SLASH COMMANDS

```
/dario-orchestrator     /dario-diagnose         /dario-status
/dario-brand            /dario-pitch            /dario-offer
/dario-funnel           /dario-cfo              /dario-dashboard
/seo-audit              /dario-wp-audit         /dario-rag-ingest
/dream                  /lucas-heartbeat        /lucas-autopilot
/diva-briefing          /diva-floor-plan        /diva-render
```

---

## 32 SQUADS (Use case → Squad)

| Use case | Squad |
|---|---|
| Brand/marketing core | dario-* + a360-* |
| Marketing avançado (MMM/MTA/CDP) | euterpe-* |
| WordPress + dev | dario-wp-audit + builder-* |
| SEO | seo-* (15) |
| Legal BR | LEX-BR (15) |
| Saúde BR | MEDIK (15) |
| Educação BR | CAMPUS (15) |
| Compliance PT | NOMOS (15) |
| ESG/CSRD | GAIA (15) |
| Cybersec | AEGIS (18) ou SPHINX (15) |
| Data engineering | DEMETER (15) |
| Product management | ORION (15) |
| Sales excellence | MERCURIUS (15) |
| Fintech | ATLAS-FIN (15) |
| Energy/Utilities | HELIOS (15) |
| Real Estate | KIRION (15) |
| Executive/Board | ZENITH (15) |
| AI research | ORACULO (15) |
| Knowledge graph/RAG | OBSIDIAN-CORP (15) |
| Arquitectura PT | DIVA (28) |
| Eventos PT | atlas-* (24) |
| Contabilidade PT | conta-* (17) |
| Admin office PT | adriana-* (16) |
| HR PT | pessoa-* (12) |
| Risk PT | risco-* (13) |
| DevOps | nexus-* (14) |
| Supply chain | suply-* (8) |
| Customer success | client-* (10) |
| CFO virtual | cfo-* (3) |
| Heartbeat/autopilot | lucas-* (5) |

---

## COGNITIVE LAYER 18 MÓDULOS

**Sprints 1-4:** semantic_dispatch, ethical_gate, synaptic_update, confidence_engine, qvalue_memory_wire, chain_validator, golden_eval, episode_promoter, dispatch_cot, dynamic_branch

**Sprints U11-U18:** seed_goldens, cron_daily, cognitive_dashboard, integrity_gate, webhook_dispatcher, eval_drilldown, prompt_hints, weekly_summary

---

## COMPLIANCE GATES TOP 10

1. `oab_205_gate` (LEX-BR) — revisão humana obrigatória
2. `cfm_205_gate` (MEDIK) — idem para saúde BR
3. `lgpd_marker` / `rgpd_marker` — auto-rodapé
4. `zdr_healthcare` — bloqueia CPF/prontuário
5. `cmvm_disclosure_gate` (NOMOS PT) — disclosures CMVM
6. `ai_act_risk_classification` (NOMOS EU) — Reg. 2024/1689
7. `dora_testing_schedule` (NOMOS+AEGIS) — TLPT
8. `csrd_disclosure_gate` (GAIA) — Wave 1-4
9. `iso27001_audit` (AEGIS+SPHINX)
10. `audit_immutable` (TODOS enterprise)

Total: 30+ gates implementados.

---

## EMERGENCY COMMANDS

```bash
# License status
python ~/.claude/orchestrator/license_manager.py --status

# Cognitive dashboard
python ~/.claude/orchestrator/cognitive_dashboard.py --generate

# Trigger dream
echo "/dream" | claude-code

# Cron daily manual
python ~/.claude/orchestrator/cron_daily.py --force

# Semantic dispatch debug
python ~/.claude/orchestrator/semantic_dispatch.py --debug --query "test"

# Token ROI
python ~/.claude/orchestrator/cfo-token-roi.py --month current

# Re-install everything
npx github:bardapraiacaraiva/dario-orchestrator-installer --upgrade
```

---

## PATHS

```
~/.claude/orchestrator/        # Engines + configs (66+ .py + YAMLs)
~/.claude/skills/              # All 536+ skills
~/.claude/orchestrator/dario.db  # SQLite (cognitive + audit)
~/OneDrive/Documents/D.A.R.I.O/  # Obsidian vault
```

---

## BUDGET

```yaml
# ~/.claude/orchestrator/budgets/YYYY-MM.yaml
limit: 50000000  # 50M tokens default
percentage: 0    # auto-updated
alert_80_sent: false
alert_95_sent: false
```

**Behaviour:**
- 80% → safe mode (1 worker parallel vs 3)
- 95% → HARD STOP (manual override required)

---

## MANUAL COMPLETO (Obsidian)

4 partes (~30K palavras):
1. **Parte 1 (Foundation):** Intro, Install, Concepts
2. **Parte 2 (Usage + Squads):** Slash commands, triggers, 32 squads detalhados
3. **Parte 3 (Cognitive/Licensing/Configs):** 18 modules, 54 tiers, YAMLs, compliance
4. **Parte 4 (Advanced/Commercial):** Memory, automation, dashboards, troubleshoot, commercial, roadmap

Location: `~/OneDrive/Documents/D.A.R.I.O/05 - Claude - IA/Outputs/2026-05-20 - DARIO v12.0 MANUAL*.md`

---

## SUPPORT

**Comunidade:**
- GitHub: github.com/bardapraiacaraiva/dario-orchestrator
- Issues: github.com/bardapraiacaraiva/dario-orchestrator/issues

**Documentação extensa:** Obsidian vault `D.A.R.I.O / 05 - Claude - IA / Outputs/`

**Backup local:** `~/Desktop/dario-v12.0-7squads-20260520-083804.zip`

---

**v12.0 LIVE · 2026-05-20**
**32 squads · 536+ skills · 54 tiers · 78/78 tests verde**
