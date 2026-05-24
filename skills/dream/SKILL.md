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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **dream** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in dream:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
