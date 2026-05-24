---
name: dario-onboarding
description: "5-minute tour of the DARIO Orchestrator. Runs real health checks (RAG, license, polished wrappers, budget) + maps the system + shows first dispatch. Use when starting on a new machine, returning after a long break, or onboarding someone else. Triggers: 'onboarding', 'tour', 'estou perdido', 'primeira vez', 'como começo', 'dario tour', '/dario-onboarding', 'where am I'."
argument-hint: "[optional: 'short' for executive summary | 'health' for diagnostic only | 'first-task' to jump straight to dispatching]"
allowed-tools: Read, Bash, Glob, Grep
license: MIT
---

# DARIO Onboarding — 5-min Tour

You (the user OR a future me on a clean machine) have ~584 skills, 32 squads, 8 polished wrappers, a RAG engine, a memory subsystem, an orchestrator, and a licence file. That's a lot. This skill gives you the **mental map + a working first invocation in 5 minutes**.

## Argument modes

| Arg | Behavior |
|---|---|
| (none) | Full tour: health → architecture → first dispatch → map → resources |
| `short` | Executive summary only (~30 lines, no health checks) |
| `health` | Run diagnostics only (RAG + license + wrappers + budget + tests) |
| `first-task` | Skip the tour, walk straight into dispatching first task |

---

## Step 1 — HEALTH CHECK (run real diagnostics)

Execute these in order. Each should produce output, not just "OK".

### 1.1 RAG engine
```bash
curl -s http://localhost:8420/health 2>&1 | head -3
```
Expected: JSON with `status: ok` and source counts. If empty → RAG engine down. Start with:
```bash
cd /c/dario-rag/engine && .venv/Scripts/python.exe main.py &
```

### 1.2 License
```bash
cat ~/.claude/orchestrator/.license 2>&1 | head -3
```
Expected: license key starting with `DARIO-`. If "No such file" → trial mode, runs but features limited.

### 1.3 Polished wrappers (Padrão A)
```bash
ls ~/.claude/skills/ | grep polished
```
Expected: 8 entries (brand/offer/funnel/sales-letter/financial-model/product/wp-audit/pitch). If <8 → integration test will catch it:
```bash
cd ~/.claude/orchestrator && .venv/Scripts/python.exe -m pytest tests/test_padrao_a_dispatch_routing.py -q 2>&1 | tail -3
```

### 1.4 Budget (this month)
```bash
month=$(date +%Y-%m) && grep -E "percentage|total_tokens" ~/.claude/orchestrator/budgets/$month.yaml 2>&1 | head -3
```
Expected: `percentage: X.XX` with X < 80. If >80 → throttle paralelism. If >95 → STOP.

### 1.5 Test suite
```bash
bash ~/.claude/orchestrator/scripts/hooks/pre-push 2>&1 | tail -2
```
Expected: `[pre-push] PASS — N tests passed (Ns)`. If FAIL → don't push code today, debug first.

**Output health summary to user** with 🟢/🟡/🔴 per check.

---

## Step 2 — MENTAL MODEL (60 seconds)

```
┌─ DARIO ────────────────────────────────────────────────────────┐
│                                                                  │
│  User request                                                    │
│      ↓                                                           │
│  /dario-orchestrator (this is the "CEO" skill)                   │
│      ↓ decompose into tasks                                      │
│      ↓ dispatch each task to a worker (company.yaml)             │
│      ↓                                                           │
│  Workers run SKILLS (584 in ~/.claude/skills/)                   │
│      ↓                                                           │
│  For client_facing tasks → routed to POLISHED WRAPPER            │
│      (Padrão A: generate → critique → revise → final)            │
│      ↓                                                           │
│  Output delivered + TELEMETRY recorded                           │
│      ↓                                                           │
│  Saved to Obsidian (D.A.R.I.O vault) for client                  │
│                                                                   │
│  Underlying:                                                      │
│    RAG (localhost:8420) for retrieval                            │
│    Memory (~/.claude/projects/.../memory/) persists across       │
│    Audit log (orchestrator/audit/) append-only                   │
│    Pre-push hook gates the suite (orchestrator/scripts/hooks/)   │
└──────────────────────────────────────────────────────────────────┘
```

**3 things to remember:**
1. **Don't dispatch single tasks directly** — invoke `/dario-orchestrator` and let it decompose
2. **Client work → polished wrapper auto** (configured in `company.yaml` `skill_client_facing`)
3. **Telemetry is mandatory** — Step 6 in every polished wrapper logs to `polished_production_runs.yaml`

---

## Step 3 — FIRST DISPATCH (do this NOW)

Pick the smallest real task you have and run:

```
/dario-orchestrator

Mission: <one-line description>
Client: <existing client slug OR "internal" if dev work>
Constraints: <budget cap | deadline | dependencies>
```

The orchestrator will:
1. Phase 0: validate (circular deps, budget, stale tasks)
2. Phase 1: understand + RAG consult
3. Phase 2: decompose into atomic tasks
4. Phase 3: dispatch (routing client_facing → polished wrappers)
5. Phase 4-7: execute, review, synthesize, audit

**If you don't have a real task ready:** use the `dispatch-rehearsal` block at the end of this skill.

---

## Step 4 — WHERE THINGS LIVE (the map)

```
~/.claude/
├── skills/                       ← 584 skills (10 polished wrappers + 576 base)
│   ├── dario-orchestrator/       ← The CEO skill
│   ├── dario-*-polished/         ← 8 Padrão A wrappers (auto-routed for client_facing)
│   ├── dario-onboarding/         ← THIS skill
│   └── ... (DIVA, LUCAS, SEO, A360, AEGIS, ATLAS, etc.)
│
├── orchestrator/
│   ├── company.yaml              ← Worker→skill mapping (where polished routing lives)
│   ├── config/company/workers.yaml ← Segmented version (kept in sync)
│   ├── tasks/active/             ← In-flight tasks (atomic checkout)
│   ├── tasks/done/               ← Completed tasks archive
│   ├── audit/YYYY-MM-DD.yaml    ← Append-only mutation log
│   ├── budgets/YYYY-MM.yaml     ← Monthly token spend tracker
│   ├── quality/
│   │   ├── skill-metrics.yaml   ← Per-skill mean scores (production)
│   │   ├── polished_production_runs.yaml  ← Padrão A telemetry log
│   │   └── pending-review.yaml  ← Human review queue
│   ├── scripts/
│   │   ├── record_polished_run.py     ← Wrapper Step 6 telemetry
│   │   ├── aggregate_polished_metrics.py
│   │   └── hooks/pre-push       ← Test gate before any push
│   ├── tests/                    ← 300+ tests (run via pre-push)
│   ├── dashboard.html            ← Live state (generate_dashboard.py)
│   ├── MANUAL.md                 ← 30K-word manual (4 parts)
│   └── PADRAO_A_AB_TEST_RESULTS.md  ← Why polished wrappers exist
│
└── projects/C--Users-barda/memory/
    ├── MEMORY.md                 ← Index (always loaded, <200 lines)
    ├── project_*.md              ← Client/project state
    ├── reference_*.md            ← External pointers
    └── feedback_*.md             ← Learned patterns / preferences
```

**RAG engine:** `localhost:8420` (separate process at `/c/dario-rag/engine/`)
**Obsidian vault:** `OneDrive/Documents/D.A.R.I.O/05 - Claude - IA/Outputs/` (client deliverables go here)

---

## Step 5 — DAILY HEARTBEAT

After onboarding, your everyday commands:

| Command | When |
|---|---|
| `/dario-status` | Start of session — system health snapshot |
| `/dario-orchestrator` | Any new mission > 1 task |
| `/dario-X-polished` (any of 8) | Direct client-facing skill invocation |
| `/dario-dashboard` | Visual state in browser |
| `/dream` | End of week — memory consolidation |
| `/lucas-autopilot` | Autonomous run on existing taskboard |

---

## Step 6 — KEY RESOURCES (read in this order if you have time)

1. **`~/.claude/orchestrator/PADRAO_A_AB_TEST_RESULTS.md`** (10 min) — Why polished wrappers exist + cross-skill validation evidence
2. **`~/.claude/orchestrator/MANUAL.md`** (deep dive, 30K words) — Full system reference, 4 parts
3. **`~/.claude/projects/C--Users-barda/memory/MEMORY.md`** (always-loaded, <2 min) — Current state of all projects + lessons
4. **Skill files** — Each `SKILL.md` has its own usage doc. List with `ls ~/.claude/skills/`
5. **Dashboard** — `python ~/.claude/orchestrator/generate_dashboard.py` (auto-opens browser)

---

## DISPATCH REHEARSAL (if you don't have a real task)

Don't have a real task to try the orchestrator on? Use this synthetic one:

```
/dario-orchestrator

Mission: Audit one of my own projects (Vivenda Creative Home / Lisbon Dog Care / pick any from MEMORY)
   and produce a 1-page health report + top 3 next actions.
Client: <pick one>
Constraints: zero API spend (use Max subscription), 1 deliverable max, ship in <15min
```

This exercises: orchestrator → dispatch → likely routes to `dario-wp-audit-polished` (Tier 1) → polish loop → telemetry. Full end-to-end with zero risk.

---

## Red flags (things that should make you pause)

- ❌ RAG engine down for >24h — `mcp__dario-rag__search_kb` returns empty, all dispatches will be context-poor
- ❌ Budget >80% mid-month — throttle to 1 worker max
- ❌ Pre-push hook failing — don't push, debug first (the failure is real)
- ❌ Polished wrapper count <8 — install drift, re-clone or check `git status`
- ❌ MEMORY.md >180 lines — approaching 200-line truncation, prune historical entries (see `feedback_product_pivot_decisions` for kill criteria)

---

## What this skill is NOT

- Not a replacement for `MANUAL.md` (which is deep dive, this is orientation)
- Not a status dashboard (use `/dario-status` or `/dario-dashboard`)
- Not a task runner (use `/dario-orchestrator`)
- Not memory-modifying (read-only diagnostics + read-only docs)

---

<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

When this skill reports health to the user, each check must carry an EXPLICIT label.

- 🔵 **verified** — health check passed (command returned expected output)
- 🟡 **assumed** — partial signal (e.g., file exists but didn't validate content)
- 🟢 **projection** — derived estimate (e.g., "budget on track for month")

❌ NOT delivery-ready:
```
RAG OK. License OK. Budget OK. Tests OK.
```

✅ Delivery-ready:
```
- RAG: 1225 sources active 🔵 verified (localhost:8420/health returned JSON)
- License: DARIO-A7B7-...-PRO present 🔵 verified (~/.claude/orchestrator/.license)
- Wrappers: 8/8 polished present 🔵 verified (ls + integration test 16/16 pass)
- Budget: 4.8% used 🔵 verified (budgets/2026-05.yaml percentage field)
- Tests: 306 passed 🔵 verified (pre-push hook smoke ran in 22s)
- Month-end projection: ~12% 🟢 projection (linear from current usage)

Status mix: 5 🔵 · 0 🟡 · 1 🟢 — System healthy, dispatch can proceed.
```
<!-- gate7:end -->
