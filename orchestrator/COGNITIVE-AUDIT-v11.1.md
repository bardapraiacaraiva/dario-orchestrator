# DARIO v11.1.0 — Cognitive Audit (2026-05-19)

**Release notes para upgrade.** Quem já tinha v11.0 e correu:
```
npx github:bardapraiacaraiva/dario-orchestrator-installer --upgrade
```
recebe 18 novos módulos que transformam o orchestrator de **reactivo a deliberativo**.

## TL;DR

- **18 módulos novos** (Sprints 1-4 cognitive + U11-U18 operational)
- **216 testes verde** em 18 test files
- **Zero LLM calls extra** em runtime — apenas eval-time (postmortem). Cache embeddings local (Ollama nomic-embed-text).
- **Backwards compatible** — todos os hooks são opt-in com fallback silencioso.

## Antes vs Depois

| Camada | v11.0 | v11.1 |
|---|---|---|
| Dispatch | Keyword matching (370+ regex) | Embeddings semantic (cosine) + Q-value + CoT trace |
| Quality gate | `score >= 60 ? ship : revision` | 5-way: ship/review/revision/escalate/success_pattern com confidence |
| Ethical gate | YAML decorativo | Wired Check 0 do guardrails (3 perguntas) |
| Synaptic weights | Read-only em dispatch | Write-back em runtime após cada task |
| Chains | Static DAG | Runtime branching (CONTINUE/REVISION/PARALLELIZE/EARLY_STOP/ESCALATE) |
| Pattern crystallization | 0 (CHANGELOG dizia "0 every cycle") | Auto-promotion + auto-rules em `evolution/rules/` |
| Eval suite | Keyword presence check | Golden compare 4-axis (lexical/semantic/length/score) |
| Drift detection | Inexistente | Daily cron + Slack/Discord webhooks |
| Diagnostics | "score baixo, rever" | Drilldown: tokens perdidos, sections em falta, recovery hints concretos |
| Dashboard | Tasks/budget only | + Cognitive health (8 cards: drift, CoT, semantic, integrity, etc) |
| Self-maintenance | Manual | Cron daily 6 jobs auto-run |

## Os 18 Módulos

### Sprint 1 — Foundation (3 módulos)
- **U1 `semantic_dispatch.py`** — Embeddings via Ollama nomic-embed-text + SQLite cache. 292 skills cached.
- **U2 `ethical_gate.py`** — Triade clarity/freedom/coherence wired em guardrails.
- **U3 `synaptic_update.py`** — Hook em executor.complete_task para write-back de pares co-activated.

### Sprint 2 — Quality with Consequences (3 módulos)
- **U4 `confidence_engine.py`** — Dimension σ + skill tier + outlier z-score → HIGH/MED/LOW.
- **U5 `qvalue_memory_wire.py`** — M3.2 (que era shelf-ware) instantiated + SQLite persistence + dispatch Signal 4.
- **U6 `chain_validator.py`** — Gate 2 em save_checkpoint: pass_to_next fields verificados.

### Sprint 3 — Real Learning (2 módulos)
- **U7 `golden_eval.py`** — capture/compare/regression-check com lexical jaccard + semantic cosine + length + score delta.
- **U8 `episode_promoter.py`** — score >= 90 → SEM-*.yaml + 3+ eps avg >= 85 → auto-rule.

### Sprint 4 — Deliberative (2 módulos)
- **U9 `dispatch_cot.py`** — 4 signals (explicit/semantic/keyword/qvalue) + agreement + rationale + alternatives. Postmortem auto.
- **U10 `dynamic_branch.py`** — 5-way runtime decision baseada em score + confidence + foundational status + step independence.

### Operational (8 módulos)
- **U11** `tools/seed_goldens.py` — 12 goldens reais (avg 2096 chars).
- **U12** `cron_daily.py` — 6 jobs idempotentes (gating 22h cooldown).
- **U13** `cognitive_dashboard.py` — HTML estático 8 cards.
- **U14** `tools/integrity_gate.py` — 7 checks cross-layer (eval/skill/embeddings/golden/chain/synaptic).
- **U15** `webhook_dispatcher.py` — Slack/Discord/generic com 24h dedup.
- **U16** `eval_drilldown.py` — Token/section/paragraph diff + recovery hints concretos.
- **U17** `prompt_hints.py` — Drilldown patterns → hints injectados em context_injector.
- **U18** `weekly_summary.py` — Markdown semanal Obsidian-ready.

### Utility
- `obsidian_safe_write.py` — Wrapper que limpa shadows quando Obsidian vault tem `newFileLocation: folder`.

## Files Modificados (existing → enhanced)

| File | Changes |
|---|---|
| `dispatch_engine.py` | infer_skill: explicit → semantic → keyword → qvalue + CoT trace |
| `executor.py` | Post-completion hooks: synaptic + qvalue + cot postmortem + episode_promoter if score>=90 |
| `session_boot.py` | Calls cron_daily --maybe-run after autodiag/dispatch |
| `chain_executor.py` | save_checkpoint Gates 2 (pass_to_next) + 3 (dynamic_branch) |
| `quality_scorer.py` | determine_action substitute por gate_decision (5-way) |
| `guardrails.py` | Check 0 = ethical_gate.evaluate() before other checks |
| `context_injector.py` | get_skill_hints merges chain hints + learned prompt_hints |
| `notifications.yaml` | + canal `webhook` (config em webhook_config.yaml) |

## Setup VIP — Configurações Recomendadas

Após upgrade, considera:

1. **Webhooks (opcional):**
   ```bash
   python ~/.claude/orchestrator/webhook_dispatcher.py --init
   # Edita ~/.claude/orchestrator/webhook_config.yaml com URLs Slack/Discord
   # Põe enabled: true
   python ~/.claude/orchestrator/webhook_dispatcher.py --test
   ```

2. **Goldens (recomendado para evals):**
   ```bash
   python ~/.claude/orchestrator/tools/seed_goldens.py
   # Captura 12 goldens reference automaticamente
   ```

3. **Bootstrap embeddings:**
   ```bash
   # Pré-requisito: Ollama com nomic-embed-text
   ollama pull nomic-embed-text
   python ~/.claude/orchestrator/semantic_dispatch.py --bootstrap
   # Cacheia 292 skill embeddings (~3 min primeira vez)
   ```

4. **Cron daily setup (automático):**
   - Session_boot já chama `cron_daily --maybe-run` automaticamente
   - Ou Windows Task Scheduler:
     ```
     schtasks /create /sc daily /tn "DARIO-Cron-Daily" /tr "python C:\Users\<user>\.claude\orchestrator\cron_daily.py --json" /st 03:00
     ```

5. **Dashboard cognitivo:**
   ```bash
   python ~/.claude/orchestrator/cognitive_dashboard.py --open
   ```

## Quality Numbers

```
Embeddings cached:   292 skills × 768-dim
Goldens:             12 (avg 2096 chars)
Semantic memories:   Cresce auto (excellence + patterns)
Auto-rules:          Geradas auto quando padrão 3+ eps com avg ≥85
Test files:          18
Total tests:        216 (0 failures)
Modulos Python:      18 novos
```

## Como Verificar Upgrade Funcionou

```bash
# 1. Version check
npx github:bardapraiacaraiva/dario-orchestrator-installer --check

# 2. Smoke test cognitive modules
python ~/.claude/orchestrator/semantic_dispatch.py --stats
python ~/.claude/orchestrator/synaptic_update.py --stats
python ~/.claude/orchestrator/cron_daily.py --status

# 3. Visual confirm
python ~/.claude/orchestrator/cognitive_dashboard.py --open
```

## Rollback

Se algo correr mal após upgrade:
```bash
# Files modificados foram backed-up automaticamente com .bak-YYYY-MM-DD suffix
ls ~/.claude/orchestrator/*.bak-*
# Restore o que precisares
mv dispatch_engine.py.bak-2026-05-19 dispatch_engine.py
```

## Próximas direcções (não no v11.1)

- **U19**: Quando hints atingem confidence ≥0.9 + occurrences ≥5, propor edit ao SKILL.md
- **U20**: Cross-chain pattern detection — refactor sugestões automáticas
- **SaaS trial mode**: hospedado em vez de instalação local (decisão arquitectural em aberto)

## Source

Cognitive audit completo executado 2026-05-18 → 2026-05-19. Doc principal:
- Vault Obsidian: `05 - Claude - IA/Decisoes/2026-05-18 - Cognitive Audit - DARIO Orchestrator.md`
- Repo full: `dario-orchestrator-full` (VIP)
- Repo público: `dario-orchestrator` (trial 7d acesso completo)
