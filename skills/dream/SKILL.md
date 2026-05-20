---
name: dream
description: Run the DARIO 4-phase memory consolidation cycle (orient -> prune -> merge -> reorganize). Inspired by Anthropic's "Memory and Dreaming for Self-Learning Agents" talk. Use to manually trigger consolidation, inspect memory health, list episodes, or inspect learned procedural workflows.
---

# /dream — DARIO Memory Consolidation

Triggers the Dream engine: a 4-phase consolidation pipeline that reviews
recent episodes (task executions), prunes stale memories, merges duplicates,
detects statistical patterns, and promotes recurring skill sequences into
procedural workflows.

## When to invoke

- After a busy work session, to consolidate what was learned
- To inspect memory health (`/dream health`)
- To see learned procedural workflows (`/dream workflows`)
- Before a long session, to load fresh procedural hints
- Anytime you want to see *what patterns DARIO has detected* across projects

## Commands

| Command | Action |
|---|---|
| `/dream` | Full cycle, 7-day window, writes changes |
| `/dream --window 14` | Use 14-day episode window |
| `/dream --dry-run` | Show what would change, don't write |
| `/dream health` | Print memory health summary (no consolidation) |
| `/dream episodes` | List recent episodes |
| `/dream workflows` | List procedural workflows (learned + legacy) |

## What happens

1. **ORIENT** — Load all episodes in window + existing memories + retrieval stats
2. **PRUNE** — Archive stale (>90d, 0 retrievals) and never-retrieved memories
3. **MERGE** — Find duplicate semantic memories (Jaccard >0.55) and consolidate
4. **REORGANIZE** — Detect statistical patterns (regressions, failed tools, correction clusters), find convergent skill sequences (>=3 sessions, avg_score>=70), promote them to procedural workflows

## Output

- Structured report saved to `~/.claude/orchestrator/dream/reports/DREAM-*.yaml`
- Markdown mirror at `~/.claude/agent-memory/dario-v2-digital-ceo/dreams/dream_YYYY-MM-DD.md`
- New procedural workflows in `~/.claude/orchestrator/memory/procedural/PROC-*.yaml`
- Archived memories moved to `~/.claude/orchestrator/memory/semantic/.archive/`

## Implementation

When invoked, execute (PowerShell on Windows):

```powershell
python "$env:USERPROFILE\.claude\orchestrator\dream_cli.py" $args
```

Or via Bash:

```bash
python ~/.claude/orchestrator/dream_cli.py "$@"
```

Default subcommand is `run` (full cycle). Pass `health`, `episodes`, or `workflows` to inspect without consolidating.

## Cron

Daily 03:00 consolidation runs via Windows Task Scheduler. Install with:
```powershell
powershell -File "$env:USERPROFILE\.claude\orchestrator\scripts\dream_install_cron.ps1"
```

Logs at `~/.claude/orchestrator/dream/cron.log`.
