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

## When in doubt

1. Read `~/.claude/skills/dario-onboarding/SKILL.md` first (5-min tour with
   real health checks).
2. Read the relevant skill's SKILL.md before invoking it.
3. Use `/dario-orchestrator` for any task touching 2+ skills.
4. Check the dashboard (`generate_dashboard.py`) for live state.
