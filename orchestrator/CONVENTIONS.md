# DARIO Orchestrator — Conventions

Quick reference for naming, project classification, and folder hygiene.

---

## Project classification

Every project that incurs spend MUST be classified in `config/project_types.yaml`
as either **client** (paid work) or **dev** (DARIO internal work). Unmapped
projects appear as `unknown` in the budget breakdown dashboard widget — they
are visible (not silently misclassified) so they can be cleaned up.

```bash
# Inspect current month breakdown
python -m scripts.budget_breakdown_by_type

# Inspect another month
python -m scripts.budget_breakdown_by_type --month 2026-04

# All months at once
python -m scripts.budget_breakdown_by_type --all

# JSON for programmatic use
python -m scripts.budget_breakdown_by_type --json
```

When adding a new client, add the slug to `clients:` in
`config/project_types.yaml`. When adding a new dev workstream (e.g., a new
refactor wave, a new internal squad), add to `dev:`.

---

## Task ID convention (when tasks/active is used)

Tasks should follow the pattern `<PROJECT_SLUG_UPPER>-<NNN>`:

- **Client tasks:** `CUIDAI-001`, `ATRIUM-042`, `SAQUEI-099`
- **Dev tasks:** `DARIO-001`, `PADRAO_A-007`, `REFACTOR-003`

The project slug must match an entry in `config/project_types.yaml`. The
budget breakdown maps tokens spent by project slug to dev vs client buckets.

---

## File / folder hygiene

| Path | Owner | What lives here |
|---|---|---|
| `tasks/active/` | runtime | In-flight tasks (atomic checkout, one yaml per task) |
| `tasks/done/` | runtime | Completed tasks |
| `tasks/backlog_blocked/` | runtime | Blocked / on-hold |
| `tasks/templates/` | versioned | Reusable task templates |
| `audit/YYYY-MM-DD.yaml` | runtime | Append-only mutation log |
| `budgets/YYYY-MM.yaml` | runtime | Monthly token spend |
| `quality/polished_production_runs.yaml` | runtime | Padrão A telemetry |
| `quality/skill-metrics.yaml` | runtime | Per-skill scoring |
| `quality/pending-review.yaml` | runtime | Human review queue |
| `config/company/*.yaml` | versioned | Worker/squad definitions |
| `config/project_types.yaml` | versioned | dev/client classification |
| `config/padrao_a_briefing_validators.yaml` | versioned | Tier 2 validator rules |
| `scripts/*.py` | versioned | Operational scripts |
| `scripts/hooks/pre-push` | versioned | Test gate before push |
| `tests/test_*.py` | versioned | Test suite |

Runtime state is gitignored. Versioned files live in git.

---

## Path discipline — NO hardcoded user slugs

Every path in production code MUST use `Path.home()` or an env var override.
NEVER hardcode user-specific slugs like `C--Users-barda`, `/Users/barda/`,
or `barda` in path strings.

```python
# ❌ Don't — breaks for any other user / multi-tenant install
MEMORY_DIR = Path("/c/Users/barda/.claude/projects/C--Users-barda/memory")

# ✅ Do — works on any machine
MEMORY_DIR = Path.home() / ".claude" / "projects" / "<resolved>" / "memory"
# Or with env var override (RFC §5 PW-1 pattern):
override = os.environ.get("DARIO_MEMORY_DIR")
```

Enforced by `tests/test_no_hardcoded_user_paths.py` — pre-push hook
catches violations.

Why: RFC_MULTI_TENANT.md Path B (per-tenant install) assumes each
client's `~/.claude/` is parameterized via `Path.home()`. One hardcoded
user slug breaks isolation for the next client install.

---

## Direct Anthropic API calls — MUST use TrackedAnthropic

Any Python script that imports `anthropic` and calls `messages.create(...)`
bills the API directly (not the Max subscription). These calls were
invisible until 2026-05-24 when `TrackedAnthropic` was added to wrap
them with spend logging.

**Rule:** every new script using anthropic SDK MUST use the wrapper.

```python
# ❌ Don't (silent spend)
from anthropic import Anthropic
client = Anthropic()

# ✅ Do (spend logged to dashboard)
from scripts.anthropic_spend_wrapper import TrackedAnthropic
client = TrackedAnthropic(caller="my-script/short-name")
```

Verify spend live:
```bash
python -m scripts.aggregate_api_spend         # CLI breakdown
# Dashboard shows: "API Spend Direct" card with 24h/month/all-time
```

Existing scripts (compile_sprint3_v2, compile_sprint4) still use raw
Anthropic — retrofit when next touched. New scripts: no excuse.

---

## Quality logs — SQLite is source of truth (post-2026-05-24)

Padrão A telemetry (`polished_runs`) and direct API spend (`api_spend`)
live in SQLite via `db.py` (schema v3). YAML/JSONL files are kept as
backward-compat mirrors during the migration period (legacy aggregators
still read them).

```python
# Write (new code):
from db import DB
DB().record_polished_run(
    skill="dario-pitch-polished", client="cuidai",
    v1_score=80, v2_score=88, final="v2",
    gate_decision="revised",
)
DB().record_api_spend(
    caller="dspy/compile_sprint4",
    model="claude-opus-4-7",
    input_tokens=1000, output_tokens=500,
    cost_usd=0.0175,
)

# Read:
runs = DB().get_polished_runs(skill="dario-pitch-polished", month="2026-05")
spend = DB().get_api_spend(caller="dspy/compile_sprint4", since_iso="2026-05-01")
```

**Concurrency:** SQLite uses WAL mode + 5s busy timeout. 50 concurrent
inserts validated by `tests/test_db_v3_polished_and_spend.py::test_concurrent_inserts_via_threads`.
The race condition that affected YAML append-rewrite is **structurally
impossible** here.

**Tenant isolation:** all v3 tables have `tenant_id` (default `'default'`).
Pre-work for RFC_MULTI_TENANT Path B per-tenant install.

Migration tool: `python -m scripts.migrate_quality_to_sqlite --apply` —
idempotent backfill from YAML/JSONL to SQLite.

---

## When in doubt

1. Read `~/.claude/skills/dario-onboarding/SKILL.md` first (5-min tour with
   real health checks).
2. Read the relevant skill's SKILL.md before invoking it.
3. Use `/dario-orchestrator` for any task touching 2+ skills.
4. Check the dashboard (`generate_dashboard.py`) for live state.
