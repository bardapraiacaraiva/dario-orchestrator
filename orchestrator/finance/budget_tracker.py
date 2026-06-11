#!/usr/bin/env python3
"""
DARIO Budget Tracker — Automated Token Accounting
Reads completed tasks, calculates token usage, updates monthly budget file.
Called by lucas-heartbeat and lucas-autopilot after each pulse.

Usage:
  python budget_tracker.py                    # Update current month
  python budget_tracker.py --report           # Print budget report
  python budget_tracker.py --check            # Check thresholds only
  python budget_tracker.py --add-tokens 5000 --project mar-brasa --skill dario-brand
"""

import argparse
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
log = logging.getLogger("budget_tracker")

# === PATHS ===
ORCH_DIR = Path.home() / ".claude" / "orchestrator"
# When invoked as a script (python finance/budget_tracker.py), sys.path[0] is
# finance/ and `from core...` fails → the DB-first reader silently fell back to
# YAML. Root on sys.path keeps the data source identical across entry points.
if str(ORCH_DIR) not in sys.path:
    sys.path.insert(0, str(ORCH_DIR))
BUDGET_DIR = ORCH_DIR / "budgets"
TASKS_ACTIVE = ORCH_DIR / "tasks" / "active"
TASKS_DONE = ORCH_DIR / "tasks" / "done"
COMPANY_YAML = ORCH_DIR / "company.yaml"

def get_current_month():
    return datetime.now().strftime("%Y-%m")

def get_budget_path(month=None):
    month = month or get_current_month()
    return BUDGET_DIR / f"{month}.yaml"

def load_company_config():
    """Load company budget limits from company.yaml."""
    if not COMPANY_YAML.exists():
        return {"monthly_limit_tokens": 50_000_000}
    with open(COMPANY_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("company", {}).get("budget", {"monthly_limit_tokens": 50_000_000})

def load_budget(month=None):
    """Load or initialize the monthly budget file."""
    path = get_budget_path(month)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    # Initialize new budget
    company = load_company_config()
    return {
        "month": month or get_current_month(),
        "company": "BARDA Digital Agency",
        "limit": company.get("monthly_limit_tokens", 50_000_000),
        "total_tokens_used": 0,
        "percentage": 0.0,
        "by_project": {},
        "by_skill": {},
        "by_model": {"opus": 0, "sonnet": 0, "haiku": 0},
        "alert_80_sent": False,
        "alert_95_sent": False,
        "last_updated": datetime.now(UTC).isoformat(),
        "pulse_count": 0,
    }

def save_budget(budget, month=None):
    """Write budget to YAML file."""
    BUDGET_DIR.mkdir(parents=True, exist_ok=True)
    path = get_budget_path(month)
    budget["last_updated"] = datetime.now(UTC).isoformat()
    budget["percentage"] = round(
        (budget["total_tokens_used"] / budget["limit"]) * 100, 2
    ) if budget["limit"] > 0 else 0

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Budget Tracking — {budget['month']}\n")
        f.write("# LUCAS Cost Control — Agent Orchestrator\n")
        f.write("# Schema v2 — Token Capture Contract compliant\n\n")
        yaml.dump(budget, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def _task_month(task: dict) -> str | None:
    """Return YYYY-MM the task belongs to, using best-effort field precedence.

    Priority:
      1. completed_at (preferred — when work finished)
      2. checked_out_at (when dispatched — for in-progress tasks)
      3. last_token_capture_at (when tokens were captured — LAST resort because
         backfill sets this to current month and would inflate budget)
    Returns None if no usable timestamp found.
    """
    for field in ("completed_at", "checked_out_at", "last_token_capture_at"):
        ts = task.get(field)
        if isinstance(ts, str) and len(ts) >= 7:
            month = ts[:7]
            if len(month) == 7 and month[4] == "-":
                return month
    return None


def _load_tasks_from_yaml():
    """Load tasks from the YAML task dirs (legacy / DB-unavailable fallback)."""
    tasks = []
    for task_dir in [TASKS_ACTIVE, TASKS_DONE]:
        if not task_dir.exists():
            continue
        for task_file in task_dir.glob("*.yaml"):
            try:
                with open(task_file, encoding="utf-8") as f:
                    t = yaml.safe_load(f)
                if t:
                    tasks.append(t)
            except (OSError, yaml.YAMLError, TypeError) as e:
                print(f"Warning: skipping {task_file.name} — {e}", file=sys.stderr)
                continue
    return tasks


def _load_budget_tasks():
    """DB-FIRST (2026-06-01): SQLite is the source of truth (CONVENTIONS.md).

    Falls back to YAML only when the DB is unavailable — loudly, because the two
    sources can diverge (2026-06: 61 tasks existed only in YAML) and a silent
    fallback makes the same command report different numbers depending on the
    entry point. Tests force the YAML path by monkeypatching this function to
    _load_tasks_from_yaml.
    """
    try:
        from core.task_store import TaskStore
        tasks = TaskStore().get_all()
        if tasks:
            return tasks
    except Exception as e:
        log.warning(f"DB unavailable ({e!r}) — falling back to YAML task scan; totals may diverge from DB-first readers")
    return _load_tasks_from_yaml()


def scan_tasks_for_tokens(month: str | None = None):
    """Scan all active+done tasks and sum actual_tokens.

    Args:
        month: If set (YYYY-MM), only include tasks whose timestamp falls in
            that month. If None, sum everything (legacy behavior).
    """
    totals = {"total": 0, "by_project": {}, "by_skill": {}, "tasks_counted": 0, "tasks_skipped_month": 0}

    for task in _load_budget_tasks():
        if not task:
            continue
        tokens = task.get("actual_tokens") or 0
        if tokens <= 0:
            continue
        if month is not None:
            task_month = _task_month(task)
            if task_month != month:
                totals["tasks_skipped_month"] += 1
                continue
        # `or` (not get-default): a key present with YAML null yields None,
        # which then crashes print_report's format spec downstream
        project = task.get("project") or "unallocated"
        skill = task.get("skill") or "unknown"
        totals["total"] += tokens
        totals["tasks_counted"] += 1
        totals["by_project"][project] = totals["by_project"].get(project, 0) + tokens
        totals["by_skill"][skill] = totals["by_skill"].get(skill, 0) + tokens
    return totals

def add_tokens(budget, tokens, project=None, skill=None, model="opus"):
    """Add tokens to budget from a single execution."""
    budget["total_tokens_used"] += tokens

    if project:
        budget["by_project"][project] = budget["by_project"].get(project, 0) + tokens
    else:
        budget["by_project"]["unallocated"] = budget["by_project"].get("unallocated", 0) + tokens

    if skill:
        budget["by_skill"][skill] = budget["by_skill"].get(skill, 0) + tokens

    if "by_model" not in budget:
        budget["by_model"] = {"opus": 0, "sonnet": 0, "haiku": 0}
    budget["by_model"][model] = budget["by_model"].get(model, 0) + tokens

    budget["pulse_count"] = budget.get("pulse_count", 0) + 1
    return budget

def check_thresholds(budget):
    """Check budget thresholds and return alerts."""
    alerts = []
    pct = budget.get("percentage", 0)

    if pct >= 95 and not budget.get("alert_95_sent"):
        alerts.append({
            "level": "CRITICAL",
            "message": f"Budget CRITICAL: {pct}% used. EXECUTION STOPPED.",
            "action": "stop_all"
        })
        budget["alert_95_sent"] = True
    elif pct >= 80 and not budget.get("alert_80_sent"):
        alerts.append({
            "level": "WARNING",
            "message": f"Budget WARNING: {pct}% used. Limiting to 1 parallel worker.",
            "action": "limit_parallel"
        })
        budget["alert_80_sent"] = True

    return alerts

def estimate_tokens(output_length):
    """Estimate tokens from output character count (fallback when metadata unavailable)."""
    if output_length < 500:
        return 2000
    elif output_length < 3000:
        return 5000
    else:
        return 10000

def print_report(budget):
    """Print a formatted budget report."""
    print(f"\n{'='*50}")
    print(f"  BUDGET REPORT — {budget.get('month', 'N/A')}")
    print(f"{'='*50}")
    print(f"  Total used:  {budget['total_tokens_used']:>12,} tokens")
    print(f"  Limit:       {budget['limit']:>12,} tokens")
    print(f"  Percentage:  {budget.get('percentage', 0):>11.2f}%")
    print(f"  Pulses:      {budget.get('pulse_count', 0):>12}")
    print(f"  Last update: {budget.get('last_updated', 'N/A')}")

    alerts = check_thresholds(budget)
    if alerts:
        print("\n  ALERTS:")
        for a in alerts:
            print(f"    [{a['level']}] {a['message']}")
    else:
        print("\n  Status: OK")

    # str() guards: budget YAMLs in the wild contain null keys (e.g. a task with
    # skill: null) and None has no __format__ for the alignment spec
    if budget.get("by_project"):
        print("\n  BY PROJECT:")
        for proj, tokens in sorted(budget["by_project"].items(), key=lambda x: -x[1]):
            print(f"    {str(proj):<25} {tokens:>10,}")

    if budget.get("by_skill"):
        print("\n  BY SKILL (top 10):")
        sorted_skills = sorted(budget["by_skill"].items(), key=lambda x: -x[1])[:10]
        for skill, tokens in sorted_skills:
            print(f"    {str(skill):<25} {tokens:>10,}")

    if budget.get("by_model"):
        print("\n  BY MODEL:")
        for model, tokens in budget["by_model"].items():
            print(f"    {str(model):<25} {tokens:>10,}")

    print(f"{'='*50}\n")

def build_parser():
    parser = argparse.ArgumentParser(
        description="DARIO Budget Tracker — Automated Token Accounting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                          # Scan tasks + update budget
  %(prog)s --report                                 # Print budget report
  %(prog)s --check                                  # Check thresholds (exit 1 if critical)
  %(prog)s --add-tokens 5000 --project mar-brasa    # Add tokens manually
  %(prog)s --add-tokens 8000 --skill dario-brand --model opus
        """
    )
    parser.add_argument("--report", action="store_true", help="Print formatted budget report")
    parser.add_argument("--check", action="store_true", help="Check thresholds only (exit 1 if critical)")
    parser.add_argument("--add-tokens", type=int, metavar="N", help="Add N tokens to budget")
    parser.add_argument("--project", type=str, help="Project to attribute tokens to")
    parser.add_argument("--skill", type=str, help="Skill to attribute tokens to")
    parser.add_argument("--model", type=str, default="opus", choices=["opus", "sonnet", "haiku"], help="Model used (default: opus)")
    parser.add_argument("--month", type=str, help="Budget month (default: current, format: YYYY-MM)")
    parser.add_argument("--quiet", action="store_true", help="Suppress non-error output")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.quiet:
        logging.getLogger("budget_tracker").setLevel(logging.WARNING)

    if args.report:
        budget = load_budget(args.month)
        print_report(budget)
        return

    if args.check:
        budget = load_budget(args.month)
        alerts = check_thresholds(budget)
        if alerts:
            for a in alerts:
                log.warning(f"[{a['level']}] {a['message']}")
            sys.exit(1 if any(a["action"] == "stop_all" for a in alerts) else 0)
        else:
            log.info(f"OK — {budget.get('percentage', 0):.2f}% used")
        return

    if args.add_tokens is not None:
        budget = load_budget(args.month)
        budget = add_tokens(budget, args.add_tokens, args.project, args.skill, args.model)
        save_budget(budget, args.month)

        alerts = check_thresholds(budget)
        save_budget(budget, args.month)

        log.info(f"Added {args.add_tokens:,} tokens. Total: {budget['total_tokens_used']:,} ({budget['percentage']:.2f}%)")
        for a in alerts:
            log.warning(f"[{a['level']}] {a['message']}")
        return

    # Default: full scan + update (filtered by the budget's month)
    target_month = args.month or get_current_month()
    budget = load_budget(target_month)
    task_totals = scan_tasks_for_tokens(month=target_month)

    if task_totals["total"] > 0:
        # Authoritative: scan result IS the truth for this month. No max() — that
        # was the pre-Faixa-3-#1b bug that let cross-month historical inflate the
        # current month.
        budget["total_tokens_used"] = task_totals["total"]
        budget["by_project"] = dict(task_totals["by_project"])
        budget["by_skill"] = dict(task_totals["by_skill"])

    save_budget(budget, target_month)
    alerts = check_thresholds(budget)
    save_budget(budget, target_month)

    log.info(f"Budget updated [{target_month}]: {budget['total_tokens_used']:,} / "
             f"{budget['limit']:,} ({budget['percentage']:.2f}%) "
             f"· {task_totals['tasks_counted']} tasks counted, "
             f"{task_totals['tasks_skipped_month']} skipped (other months)")
    for a in alerts:
        log.warning(f"[{a['level']}] {a['message']}")

if __name__ == "__main__":
    main()
