---
name: dario-status
description: DARIO system health dashboard — shows RAG stats, query log, knowledge decay, memory state, eval baseline, scheduled tasks, and overall system health in one view. Triggers on "status dario", "dario health", "estado do sistema", "system check", "health check dario".
license: MIT
---

# DARIO Skill — System Status

One-command full health check of the DARIO system.

## When to activate
- Start of session ("como está o sistema?")
- After changes to engine/RAG/scripts
- Periodic health review
- Debugging issues

## Workflow

### 1. RAG Engine Health
```
mcp__dario-rag__kb_health()
mcp__dario-rag__kb_stats()
```
Report: sources, chunks, collections, model, uptime.

### 2. Query Log Analytics
```bash
python C:\dario-rag\scripts\check_query_log.py
```
Report: total queries, last query, avg top_score, gap queries.

### 3. Knowledge Decay Check
```bash
python C:\dario-rag\scripts\check_knowledge_decay.py
```
Report: fresh/warning/stale by category.

### 4. Agent Memory State
Read `~/.claude/agent-memory/dario-v2-digital-ceo/MEMORY.md`.
Count: total files, projects, user, feedback, reference.
Check for stale projects (>30 days without update).

### 5. Eval Baseline
Check latest eval run in `C:\dario-rag\evals\runs\`.
Report: pass rate, avg score, last run date.

### 6. Scheduled Tasks
```powershell
Get-ScheduledTask -TaskName 'Dario*' | Select TaskName, State
```
Report: all 4 tasks status (Engine, Watcher, Watchdog, Backup).

### 7. Skills Count
Count directories in `~/.claude/skills/dario-*`.

### 8. Ollama Models
```bash
curl -s http://localhost:11434/api/tags
```
Report: embedding model + chat model availability.

### 9. AutoDiag (Silent Audit) — ASIMO Pattern
Run checks from `~/.claude/orchestrator/autodiag.yaml`:
- Coherence check (assignees valid)
- Orphan detection (broken parent refs)
- Dependency integrity (broken depends_on)
- Budget drift (sum mismatch)
- Stale reviews (>2x SLA)
- Quality regression (avg score drop >15)

Report: only issues found. If all pass → "AutoDiag: OK".
Log code: `DARIO_AUTODIAG_OK_{timestamp}` or `DARIO_AUTODIAG_WARN_{check}_{id}`

### 10. Fallback Matrix Health
Read `~/.claude/orchestrator/fallback_matrix.yaml`.
Check: all primary skills in matrix exist in `~/.claude/skills/`.
Report: missing skills, orphan entries.

### 11. Reactivation Status
Check last log entry for `DARIO_REACTIVATION_OK` or `DARIO_REACTIVATION_DEGRADED`.
Report: last successful reactivation timestamp, any degraded steps.

## Output format

```
## DARIO System Status — YYYY-MM-DD HH:MM

| Component | Status | Details |
|---|---|---|
| RAG Engine | UP/DOWN | X sources, Y chunks |
| Query Log | X rows | last: HH:MM, avg score: 0.XX |
| Knowledge Decay | X stale | Y warning, Z fresh |
| Agent Memory | X files | Y projects, Z user/feedback |
| Eval Baseline | XX.X% | last run: YYYY-MM-DD |
| Scheduled Tasks | X/4 running | ... |
| Skills | X dario + Y seo | total Z |
| Ollama | X models | embed: Y, chat: Z |
| AutoDiag | OK/WARN/FAIL | last: HH:MM, issues: N |
| Fallback Matrix | X skills mapped | Y missing |
| Reactivation | OK/DEGRADED | last: YYYY-MM-DD HH:MM |
| Auto-Dream | last: YYYY-MM-DD | X dreams total |
| Overall | HEALTHY/DEGRADED/DOWN | ... |
```

## Health Check Protocol

Comprehensive health checks for all shared services. Run each check in order; collect results into the Health Report Template below.

### 1. RAG Engine

```bash
rtk curl -s http://localhost:8420/health
```

- If the endpoint responds with HTTP 200: status = **UP**.
- If connection refused / timeout: status = **DOWN** — skip kb_health/kb_stats calls.
- When UP, call MCP tools:
  ```
  mcp__dario-rag__kb_health()   → uptime, model, status
  mcp__dario-rag__kb_stats()    → source_count, chunk_count, collection_count, last_ingest_date
  ```
- Report: `UP | 88 sources, 1215 chunks, last ingest: 2026-04-25` or `DOWN | connection refused`.

### 2. Obsidian Vaults

Check both vault root paths exist and are accessible:

```bash
# DARIO vault
ls "C:\Users\barda\OneDrive\Documents\D.A.R.I.O" > /dev/null 2>&1 && echo "DARIO: OK" || echo "DARIO: MISSING"

# DIVA vault
ls "C:\Users\barda\OneDrive\Documents\D.I.V.A" > /dev/null 2>&1 && echo "DIVA: OK" || echo "DIVA: MISSING"
```

For each vault that exists:
- Count files in `05 - Claude - IA/Outputs/`:
  ```bash
  rtk find "C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs" -type f | wc -l
  ```
- Get last modified date of most recent file in Outputs.
- Report: `DARIO: OK (23 outputs, last: 2026-04-26) | DIVA: OK (8 outputs, last: 2026-04-20)` or `DARIO: MISSING`.

### 3. Agent Memory

Check existence and freshness of all memory files:

| File | Path |
|------|------|
| DARIO agent | `~/.claude/agent-memory/dario-v2-digital-ceo/MEMORY.md` |
| DIVA agent | `~/.claude/agent-memory/diva-v1-design-architect/MEMORY.md` |
| Project memory | `~/.claude/projects/C--Users-barda/memory/MEMORY.md` |

For each file:
```bash
test -f "$HOME/.claude/agent-memory/dario-v2-digital-ceo/MEMORY.md" && \
  stat --format="%Y %s" "$HOME/.claude/agent-memory/dario-v2-digital-ceo/MEMORY.md" || \
  echo "MISSING"
```

- Report: file count (X/3 present), last modified date per file, total size.
- Flag any file older than 7 days as **STALE**.
- Flag any missing file as **MISSING** (red flag).

### 4. Orchestrator

Check all required directories and files:

| Directory / File | Path |
|------------------|------|
| Active tasks | `~/.claude/orchestrator/tasks/active/` |
| Done tasks | `~/.claude/orchestrator/tasks/done/` |
| Audit logs | `~/.claude/orchestrator/audit/` |
| Budgets | `~/.claude/orchestrator/budgets/` |
| Quality | `~/.claude/orchestrator/quality/` |
| Company config | `~/.claude/orchestrator/company.yaml` |

Checks:
```bash
# Directory existence
for dir in tasks/active tasks/done audit budgets quality; do
  test -d "$HOME/.claude/orchestrator/$dir" && echo "$dir: OK" || echo "$dir: MISSING"
done

# company.yaml exists and is non-empty
test -s "$HOME/.claude/orchestrator/company.yaml" && echo "company.yaml: OK" || echo "company.yaml: EMPTY/MISSING"

# Count active and done tasks
rtk ls "$HOME/.claude/orchestrator/tasks/active/" 2>/dev/null | wc -l
rtk ls "$HOME/.claude/orchestrator/tasks/done/" 2>/dev/null | wc -l
```

Budget check — read current month:
```bash
cat "$HOME/.claude/orchestrator/budgets/$(date +%Y-%m).yaml"
```
- Extract `percentage` field. Report current spend percentage.
- Flag **>80%** as WARNING, **>95%** as CRITICAL.

### 5. Skills

Count and categorize all installed skills:

```bash
ls -d "$HOME/.claude/skills/"*/ 2>/dev/null | while read d; do basename "$d"; done | sort
```

Group by division prefix:
- `dario-*` → DARIO division
- `diva-*` → DIVA division
- `lucas-*` → LUCAS division
- `seo-*` → SEO division
- Everything else → Other

Report: `Skills: 42 total (24 dario, 12 diva, 3 lucas, 8 seo, 1 other)`

---

## Health Report Template

Generate this markdown dashboard as the final output:

```markdown
## DARIO System Health — YYYY-MM-DD HH:MM

### Services
| Service | Status | Details |
|---------|--------|---------|
| RAG Engine | [UP]/[DOWN] | X sources, Y chunks, last ingest: DATE |
| Obsidian DARIO | [OK]/[MISSING] | X outputs, last: DATE |
| Obsidian DIVA | [OK]/[MISSING] | X outputs, last: DATE |
| Ollama | [UP]/[DOWN] | embed: MODEL, chat: MODEL |

### Agent Memory
| Memory File | Status | Last Modified | Size |
|-------------|--------|---------------|------|
| DARIO agent | [OK]/[MISSING]/[STALE] | DATE | X KB |
| DIVA agent | [OK]/[MISSING]/[STALE] | DATE | X KB |
| Project memory | [OK]/[MISSING]/[STALE] | DATE | X KB |

### Orchestrator
| Component | Status | Details |
|-----------|--------|---------|
| tasks/active | [OK]/[MISSING] | X tasks |
| tasks/done | [OK]/[MISSING] | X tasks |
| audit | [OK]/[MISSING] | — |
| budgets | [OK]/[MISSING] | Current month: X% |
| quality | [OK]/[MISSING] | — |
| company.yaml | [OK]/[EMPTY]/[MISSING] | — |

### Skills Inventory
| Division | Count | Examples |
|----------|-------|----------|
| DARIO | X | status, diagnose, offer... |
| DIVA | X | briefing, budget, timeline... |
| LUCAS | X | autopilot, heartbeat, quality... |
| SEO | X | audit, technical, schema... |
| Other | X | — |
| **Total** | **X** | — |

### Knowledge Health
| Metric | Value |
|--------|-------|
| Query Log | X queries, last: DATE, avg score: 0.XX |
| Knowledge Decay | X fresh, Y warning, Z stale |
| Eval Baseline | XX.X% pass, last run: DATE |
| Scheduled Tasks | X/4 running |

### Overall Verdict
- **Status**: HEALTHY / DEGRADED / DOWN
- **Red Flags**: (list any, or "None")
- **Recommendations**: (list any, or "All clear")
```

Status icon rules:
- `[UP]` / `[OK]` — service healthy and responding
- `[DOWN]` / `[MISSING]` — service unreachable or path does not exist
- `[STALE]` — file exists but not updated in >7 days
- `[EMPTY]` — file exists but has zero bytes
- `[WARNING]` — budget >80%
- `[CRITICAL]` — budget >95%

---

## Auto-Fix

Actions the skill can perform automatically without user confirmation:

### Can Auto-Fix
| Issue | Fix Action |
|-------|------------|
| Missing orchestrator dirs | `mkdir -p ~/.claude/orchestrator/{tasks/active,tasks/done,audit,budgets,quality}` |
| Missing budget file for current month | Create `~/.claude/orchestrator/budgets/YYYY-MM.yaml` with `percentage: 0` and `spent: 0` |
| Missing quality dir | `mkdir -p ~/.claude/orchestrator/quality` |
| Missing agent-memory dirs | `mkdir -p ~/.claude/agent-memory/{dario-v2-digital-ceo,diva-v1-design-architect}` |
| Empty company.yaml | Create with minimal template (company name, divisions list) |
| RAG engine not running | Start with `cd /c/dario-rag/engine && /c/dario-rag/engine/.venv/Scripts/python.exe main.py &` |

### Requires Manual Intervention
| Issue | Why | Suggested Action |
|-------|-----|------------------|
| Obsidian vault missing | OneDrive sync or vault relocation — cannot be auto-created | Check OneDrive sync status, verify vault path in settings |
| RAG engine crashes repeatedly | Underlying dependency or data issue | Check logs at `/c/dario-rag/engine/logs/`, inspect Python traceback |
| Agent memory file MISSING (not dir) | Content cannot be auto-generated — represents accumulated knowledge | Re-run agent onboarding or restore from backup |
| Budget >95% | Business decision required — cannot auto-extend | Review with user, adjust budget cap, or wait for next month |
| Ollama models missing | Requires model download (~4GB+) | `ollama pull nomic-embed-text && ollama pull llama3.1` |
| Scheduled tasks not running | Windows Task Scheduler permissions | Open Task Scheduler, check task status, re-enable manually |
| Eval baseline missing/outdated | Requires running eval suite which consumes tokens | `cd /c/dario-rag && python evals/run_evals.py` — run during off-peak |

Auto-fix runs silently during the health check. If any auto-fix is applied, it is reported in the dashboard under **Auto-Fixed** with the action taken.

---

## Red Flags

Conditions that should trigger an immediate alert to the user. If any red flag is detected, the Overall Verdict must be **DEGRADED** or **DOWN**.

### Critical (Overall = DOWN)
| Red Flag | Condition | Impact |
|----------|-----------|--------|
| RAG engine down | `curl localhost:8420` fails | No knowledge retrieval — all RAG-dependent skills broken |
| All agent memory missing | 0/3 memory files present | Complete context loss — agents start from scratch |
| Budget >= 95% | Budget file shows `percentage >= 95` | All orchestrator execution blocked per LUCAS policy |
| company.yaml missing | File does not exist or is empty | Orchestrator cannot identify company structure or divisions |

### Warning (Overall = DEGRADED)
| Red Flag | Condition | Impact |
|----------|-----------|--------|
| Budget >= 80% | Budget file shows `percentage >= 80` | Orchestrator limited to 1 task per pulse (not 3 parallel) |
| Any agent memory stale | Memory file >7 days old | Agent operating on outdated context |
| Any agent memory missing | 1-2 of 3 memory files absent | Partial context loss for that agent |
| Obsidian vault missing | Either DARIO or DIVA vault path not found | Cannot save/retrieve knowledge from that vault |
| Knowledge decay high | >30% of sources rated "stale" | RAG answers may be outdated |
| Eval baseline failing | Pass rate <70% | RAG quality below acceptable threshold |
| Scheduled tasks down | <3 of 4 tasks running | Automation gaps — backups, watchdog, or watcher offline |
| Zero active tasks | `tasks/active/` is empty | Orchestrator has nothing queued — may indicate stalled pipeline |
| Ollama down | `curl localhost:11434` fails | Local embedding/chat unavailable — RAG may fall back or fail |

### Escalation
When red flags are detected:
1. Print the red flag prominently at the top of the health report.
2. If auto-fixable, apply the fix and re-check.
3. If not auto-fixable, include the **Suggested Action** from the tables above.
4. For CRITICAL flags, prefix the report with: `ALERT: System requires immediate attention.`

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — RAG Engine reportado com dados reais
- [ ] Status UP/DOWN explícito (não "a verificar...")
- [ ] Source count + chunk count numéricos presentes
- [ ] Last ingest date em formato YYYY-MM-DD
- [ ] Se DOWN: motivo indicado (connection refused / timeout)

❌ NOT delivery-ready: `RAG Engine | UP | sources disponíveis, chunks carregados`
✅ Delivery-ready: `RAG Engine | UP | 88 sources, 1 215 chunks, last ingest: 2026-04-25`

---

### Gate 2 — Query Log com métricas numéricas
- [ ] Total de queries (número inteiro)
- [ ] Timestamp da última query (HH:MM ou YYYY-MM-DD HH:MM)
- [ ] avg top_score com 2 casas decimais
- [ ] Gap queries count (mesmo que 0)

❌ NOT delivery-ready: `Query Log | OK | queries recentes encontradas`
✅ Delivery-ready: `Query Log | 347 rows | last: 09:42, avg score: 0.81, gap queries: 3`

---

### Gate 3 — Knowledge Decay categorizado por frescura
- [ ] Contagem numérica para cada categoria: fresh / warning / stale
- [ ] Itens stale listados por categoria (não apenas total)
- [ ] Se stale > 0: categoria afectada identificada

❌ NOT delivery-ready: `Knowledge Decay | alguns itens desactualizados`
✅ Delivery-ready: `Knowledge Decay | 2 stale | fresh: 41, warning: 7, stale: 2 (fiscal-PT, concorrentes)`

---

### Gate 4 — AutoDiag com log code e timestamp
- [ ] Resultado explícito: OK / WARN / FAIL (não "sem problemas detectados")
- [ ] Log code presente: `DARIO_AUTODIAG_OK_20260426T0912` ou `DARIO_AUTODIAG_WARN_budget_drift_T007`
- [ ] Se WARN/FAIL: check específica identificada (não genérico)
- [ ] Timestamp da última execução em HH:MM

❌ NOT delivery-ready: `AutoDiag | OK | nenhum problema`
✅ Delivery-ready: `AutoDiag | WARN | DARIO_AUTODIAG_WARN_stale_review_T012, last: 09:44`

---

### Gate 5 — Scheduled Tasks com contagem X/4
- [ ] Contagem no formato X/4 running
- [ ] Nome de cada task visível (Engine / Watcher / Watchdog / Backup)
- [ ] Estado individual de cada task (Running / Ready / Disabled)
- [ ] Tasks não-Running assinaladas

❌ NOT delivery-ready: `Scheduled Tasks | a maioria activa`
✅ Delivery-ready: `Scheduled Tasks | 3/4 running | Engine: Running, Watcher: Running, Watchdog: Disabled, Backup: Running`

---

### Gate 6 — Output usa dados reais, zero placeholders angle-bracket
- [ ] Nenhum `<client>`, `<date>`, `<score>`, `<model>` no output final
- [ ] Ollama models com nomes reais (ex: `nomic-embed-text`, `llama3.2`)
- [ ] Reactivation timestamp real (não `YYYY-MM-DD HH:MM`)
- [ ] Overall health = HEALTHY / DEGRADED / DOWN com justificação

❌ NOT delivery-ready: `Ollama | <X> models | embed: <model>, chat: <model>`
✅ Delivery-ready: `Ollama | 2 models | embed: nomic-embed-text, chat: llama3.2:3b`

---

### 7. Status Checklist per Data Point (Gate 7 — validated FASE 1)

Cada número/métrica/estado no output do DARIO Status deve ter label EXPLÍCITO:

- 🔵 **verified** — lido directamente de ficheiro, endpoint ou log em tempo real
- 🟡 **assumed** — valor padrão/esperado mas não confirmado nesta execução
- 🟢 **projection** — tendência calculada, não estado actual verificável

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs precisa confirm antes de agir.

**Honest transparency > inflated health report.**

---

❌ NOT delivery-ready:
```
| RAG Engine | UP | 88 sources, 1215 chunks |
| Eval Baseline | 94.2% | last run: 2026-04-20 |
| Scheduled Tasks | 4/4 running |
```
*(reader assume tudo verified — mas RAG pode estar cached, eval pode ser stale, tasks podem ter mudado de estado)*

✅ Delivery-ready:
```
| RAG Engine      | 🔵 verified   | UP — lido de /health endpoint @ 10:32 |
| Eval Baseline   | 🟡 assumed    | 94.2% — last run >7 days, precisa re-run confirm |
| Scheduled Tasks | 🔵 verified   | 3/4 running — DarioBackup: Disabled (confirmed Get-ScheduledTask) |
| Knowledge Decay | 🟡 assumed    | 2 stale — script não correu nesta sessão, valor de cache |
| AutoDiag        | 🟢 projection | WARN estimado — baseado em padrão histórico, audit não executado |
```

---

**Ship checklist post-execução completa:**
- [ ] Todos os 🟡 items confirmados — scripts correram com sucesso nesta sessão (não cached)
- [ ] Todos os 🔵 sources têm timestamp da leitura (ex: `@ HH:MM`) para rastreabilidade
- [ ] Todos os 🟢 projections/estimativas identificados como tal ao utilizador antes de qualquer acção correctiva
- [ ] `DARIO_AUTODIAG_OK_{timestamp}` ou `DARIO_AUTODIAG_WARN_{check}_{id}` emitido e registado
- [ ] Reactivation status verificado contra log real (não assumido OK por ausência de erros)

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## DARIO System Status — 2026-04-26 09:47

| Component         | Status        | Details                                                      |
|-------------------|---------------|--------------------------------------------------------------|
| RAG Engine        | UP            | 88 sources, 1 215 chunks, 3 collections, last ingest: 2026-04-25 |
| Query Log         | 347 rows      | last: 09:42, avg score: 0.81, gap queries: 3                 |
| Knowledge Decay   | 2 stale       | fresh: 41, warning: 7, stale: 2 (fiscal-PT, concorrentes)   |
| Agent Memory      | 3/3 files     | DARIO: 2026-04-26, DIVA: 2026-04-24, Project: 2026-04-26    |
| Eval Baseline     | 87.4%         | last run: 2026-04-22, 23/26 pass                             |
| Scheduled Tasks   | 3/4 running   | Engine ✅ Watcher ✅ Watchdog ❌ Backup ✅                   |
| Skills            | 17 dario + 4 seo | total 21                                                  |
| Ollama            | 2 models      | embed: nomic-embed-text, chat: llama3.2:3b                   |
| AutoDiag          | WARN          | DARIO_AUTODIAG_WARN_stale_review_T012, last: 09:44, issues: 1|
| Fallback Matrix   | 14 skills mapped | missing: 0                                               |
| Reactivation      | OK            | last: 2026-04-26 07:31, 0 degraded steps                     |
| Obsidian Vaults   | DARIO ✅ DIVA ✅ | DARIO: 23 outputs (last: 2026-04-26), DIVA: 8 outputs (last: 2026-04-20) |
| Overall           | DEGRADED      | Watchdog task inactivo + 2 stale knowledge items             |

### ⚠️ Issues encontrados (2)

**1. Scheduled Task — Watchdog inactivo**
- Task: `Dario-Watchdog`
- Estado actual: `Disabled`
- Acção: `Task Scheduler → Enable → Run`

**2. Knowledge Decay — 2 itens stale**
- Categorias: `fiscal-PT` (last update: 2026-02-14), `concorrentes` (last update: 2026-01-30)
- Acção: re-ingest sources ou marcar como arquivado

### AutoDiag log
`DARIO_AUTODIAG_WARN_stale_review_T012_20260426T0944`
Stale review detectado em task T012 (revisão pendente há 9 dias, SLA = 4 dias).
```

---

## Output anti-patterns

- Status reportado como "OK" sem nenhum número de suporte (sources, chunks, score)
- Usar "alguns", "vários", "recente" em vez de contagens e timestamps concretos
- AutoDiag concluído sem log code — invalida rastreabilidade
- Overall = HEALTHY quando existe qualquer task Disabled ou item stale
- Scheduled Tasks reportadas como "X/4" sem nomear qual está em falta
- Knowledge Decay apresentado apenas como total stale sem identificar categorias afectadas
- Ollama section com modelo listado como "embedding model available" sem nome real
- Issues section omitida quando Overall = DEGRADED (acções correctivas são obrigatórias)
- Reactivation reportado como "OK" sem timestamp verificável da última execução
- Placeholders `<model>`, `<date>`, `<score>` sobrevivem no output final entregue
