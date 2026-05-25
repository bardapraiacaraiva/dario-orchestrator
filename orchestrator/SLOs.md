# DARIO Orchestrator — Service Level Objectives

Honest, measurable, alertable. Defined 2026-05-25 as part of Risk recommendation #6.

Inspired by Google SRE Workbook (Ch. 2-4). Three SLOs cover the dimensions that
matter most for a consulting accelerator: dispatch responsiveness, budget data
freshness, pulse cadence.

## SLO definitions

### 1. Dispatch latency — Tier C skill responds <5s for status query

**Statement:** 95% of `dispatch_engine.py --status` calls complete in ≤5 seconds.

**Why:** When the operator runs `--status` during planning, they expect instant
feedback. Slowness here means dispatch is degraded across the board.

**Measurement:** Time `subprocess.run([python, "dispatch_engine.py", "--status"])`
on each pulse. Record to `quality/slo_dispatch_latency.jsonl`.

**Error budget:** 5% of measurements may exceed 5s (≈ 36 minutes downtime/month
if measured every minute, but only 36 single-measurement violations).

**Alert:** if 3+ consecutive measurements exceed 5s, emit a `WARN` to dashboard.

### 2. Budget freshness — current month's budget file is ≤6h stale

**Statement:** `budgets/YYYY-MM.yaml` for the current month must be updated
within the last 6 hours during any active session.

**Why:** Stale budget means the enforcement layer's `BudgetExceededError`
won't fire when it should. The 95% hard-stop becomes a 95% suggestion.

**Measurement:** Read `last_updated` from current month's budget file. Compare
to now. Alert if >6h.

**Error budget:** Budget can be stale during quiet periods (no work happening).
Only alert during sessions with >0 dispatched tasks in the last hour.

**Alert:** dashboard widget red banner + console warning on session_boot if stale.

### 3. Pulse cadence — `cron_daily` runs at least every 26 hours

**Statement:** `cron_daily.py` records a successful run (status=ok or warn)
within the last 26 hours.

**Why:** cron_daily exercises 6 of the 13 restored cognitive modules + does
regression_check + integrity_gate. If it stops running, the orchestrator goes
deaf to drift.

**Measurement:** Parse `last_run.yaml` for `last_completed_at`. Compare to now.

**Error budget:** 26h instead of 24h gives 2h slack for power outages, holidays,
DST transitions.

**Alert:** dashboard widget shows ⚠️ if >26h, 🔴 if >48h.

## What's NOT in scope (intentional)

- **Task completion latency** — workers run in Agent tool, latency dominated
  by Claude model speed (Anthropic SLA, not ours)
- **Dashboard render time** — generated artifact, refreshed lazily
- **Test suite duration** — already gated by pre-push hook (<60s)
- **API spend velocity** — covered by budget enforcement layer (not an SLO)

## How alerts surface

| Severity | Surface | Audience |
|---|---|---|
| INFO | Dashboard widget (green/yellow/red badge) | Operator at glance |
| WARN | Console output on session boot (`SessionStart` hook) | Operator on next session |
| CRITICAL | Both above + entry in `quality/slo_violations.jsonl` | Operator + audit trail |

## Implementation

`scripts/slo_check.py` runs all 3 checks on demand or via cron. Writes to:
- `quality/slo_status.yaml` (current state)
- `quality/slo_violations.jsonl` (append-only history)
- Dashboard widget reads `slo_status.yaml`

```bash
# Manual check
python scripts/slo_check.py

# JSON output for dashboard
python scripts/slo_check.py --json
```

## Review cadence

- Quarterly: review error budgets, adjust thresholds based on real usage
- After any production incident: ask "would an SLO have caught this?"
- Annually: revisit whether the 3 SLOs are still the right 3

## Status

Defined: 2026-05-25
First measurement: TBD (after `slo_check.py` lands)
Last review: 2026-05-25 (this file)
