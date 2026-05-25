"""Budget hard-stop enforcement (Risk #1 thin layer module 1/3).

Before this module, "stop dispatching at 95% budget" was Claude's job
to remember from SKILL.md. Now: any dispatcher call to
`check_budget_or_raise()` actually fails when over threshold.

Reads budgets/YYYY-MM.yaml (legacy mirror) OR queries SQLite budget
table (v2 schema, already in db.py). Whichever has the higher value
wins (defensive — prefers blocking on stale-high over silently-low).

Thresholds (overridable via env):
    DARIO_BUDGET_WARNING_PCT  default 80
    DARIO_BUDGET_HARDSTOP_PCT default 95

Override threshold for tests: pass kwargs to check_budget_or_raise().
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from pathlib import Path

import yaml

from enforcement import BudgetExceededError

log = logging.getLogger("enforcement.budget_gate")

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
BUDGETS_DIR = ORCH_DIR / "budgets"

DEFAULT_WARNING_PCT = float(os.getenv("DARIO_BUDGET_WARNING_PCT", "80"))
DEFAULT_HARDSTOP_PCT = float(os.getenv("DARIO_BUDGET_HARDSTOP_PCT", "95"))


def _load_budget_yaml(month: str) -> dict:
    path = BUDGETS_DIR / f"{month}.yaml"
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _load_budget_sqlite(month: str) -> dict:
    """Best-effort SQLite read. Returns empty dict on any error."""
    try:
        import sys
        sys.path.insert(0, str(ORCH_DIR))
        from core.db import DB
        with DB()._conn() as conn:
            row = conn.execute(
                "SELECT tokens_used, token_limit FROM budget WHERE month = ?",
                (month,),
            ).fetchone()
        if row:
            tokens = row["tokens_used"] or 0
            limit = row["token_limit"] or 50_000_000
            return {"total_tokens_used": tokens, "limit": limit,
                    "percentage": (tokens / limit * 100) if limit else 0}
    except Exception as e:
        log.debug(f"sqlite budget read failed (non-fatal): {e}")
    return {}


def current_budget_state(month: str | None = None) -> dict:
    """Read budget for current month. Returns dict with percentage.

    Defensively picks the source with the higher percentage to avoid
    false-negatives during YAML/SQLite migration.
    """
    month = month or datetime.now(UTC).strftime("%Y-%m")
    yaml_data = _load_budget_yaml(month)
    sqlite_data = _load_budget_sqlite(month)

    def _pct(d: dict) -> float:
        if not d:
            return -1.0
        p = d.get("percentage")
        if p is not None:
            try:
                return float(p)
            except (TypeError, ValueError):
                pass
        tokens = d.get("total_tokens_used") or 0
        limit = d.get("limit") or 1
        return (tokens / limit * 100) if limit else 0.0

    pct_yaml = _pct(yaml_data)
    pct_sqlite = _pct(sqlite_data)
    # Prefer the source reporting the HIGHER usage (defensive — false-positive
    # blocks dispatch but never lets a missed-update silently pass)
    if pct_yaml >= pct_sqlite:
        chosen = yaml_data if yaml_data else {}
        chosen.setdefault("percentage", pct_yaml if pct_yaml >= 0 else 0.0)
        chosen["_source"] = "yaml"
    else:
        chosen = sqlite_data
        chosen["_source"] = "sqlite"
    chosen.setdefault("month", month)
    return chosen


def check_budget_or_raise(
    hardstop_pct: float | None = None,
    warning_pct: float | None = None,
    month: str | None = None,
) -> dict:
    """Raise BudgetExceededError if budget percentage >= hardstop_pct.

    Logs a WARNING when >= warning_pct (but does not raise).
    Returns the budget state dict on success.
    """
    hardstop = hardstop_pct if hardstop_pct is not None else DEFAULT_HARDSTOP_PCT
    warning = warning_pct if warning_pct is not None else DEFAULT_WARNING_PCT

    state = current_budget_state(month=month)
    pct = float(state.get("percentage", 0) or 0)

    if pct >= hardstop:
        raise BudgetExceededError(
            f"Budget hard-stop: {pct:.1f}% (limit {hardstop}%). "
            f"Month {state.get('month')}. Source: {state.get('_source', '?')}. "
            f"Wait for next month or raise the limit in budgets/{state['month']}.yaml."
        )

    if pct >= warning:
        log.warning(
            f"Budget WARNING: {pct:.1f}% (threshold {warning}%). "
            "Reduce parallelism to 1; review per-project spend."
        )

    return state


def is_budget_safe(hardstop_pct: float | None = None, month: str | None = None) -> bool:
    """Non-raising variant — returns bool. Useful for dashboard widgets."""
    try:
        check_budget_or_raise(hardstop_pct=hardstop_pct, month=month)
        return True
    except BudgetExceededError:
        return False
