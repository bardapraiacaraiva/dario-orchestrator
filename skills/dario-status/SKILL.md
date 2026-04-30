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
