#!/usr/bin/env python3
"""
DARIO CFO — Tax Calendar Engine
Reads tax_calendar.yaml, calculates deadline proximity, generates alerts.
Integrates with heartbeat for automatic fiscal monitoring.

Usage:
    python tax_calendar.py                  # Show all obligations with status
    python tax_calendar.py --next           # Next upcoming obligation + checklist
    python tax_calendar.py --alerts         # Only obligations needing attention
    python tax_calendar.py --overdue        # Only overdue obligations
    python tax_calendar.py --month 05       # Obligations for a specific month
    python tax_calendar.py --submit ID      # Mark obligation as submitted
    python tax_calendar.py --json           # JSON output (for heartbeat integration)
    python tax_calendar.py --check          # Silent check, exit code only (0=ok, 1=warning, 2=urgent, 3=overdue)
"""

import argparse
import datetime
import json
import logging
import os
import sys
from pathlib import Path

import yaml

FINANCE_DIR = Path(os.path.expanduser("~/.claude/orchestrator/finance"))
CALENDAR_FILE = FINANCE_DIR / "tax_calendar.yaml"

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tax_calendar")


def load_calendar():
    """Load tax calendar YAML."""
    if not CALENDAR_FILE.exists():
        log.error(f"Tax calendar not found: {CALENDAR_FILE}")
        sys.exit(1)
    with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_calendar(data):
    """Save tax calendar YAML."""
    with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def next_monthly_deadline(deadline_day, today):
    """Calculate the next monthly deadline date."""
    if today.day <= deadline_day:
        try:
            return datetime.date(today.year, today.month, deadline_day)
        except ValueError:
            # Handle months with fewer days
            import calendar
            last_day = calendar.monthrange(today.year, today.month)[1]
            return datetime.date(today.year, today.month, min(deadline_day, last_day))
    else:
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
        try:
            return datetime.date(next_year, next_month, deadline_day)
        except ValueError:
            import calendar
            last_day = calendar.monthrange(next_year, next_month)[1]
            return datetime.date(next_year, next_month, min(deadline_day, last_day))


def get_obligation_deadline(obligation, today):
    """Get the effective deadline for an obligation."""
    if obligation.get("recurrence") == "monthly":
        return next_monthly_deadline(obligation["deadline_day"], today)
    else:
        deadline_str = obligation.get("deadline", "")
        if deadline_str:
            return datetime.date.fromisoformat(deadline_str)
    return None


def classify_urgency(days_until, status):
    """Classify urgency based on days until deadline."""
    if status in ("submitted", "paid"):
        return "DONE", "green"
    if days_until < 0:
        return "OVERDUE", "red"
    if days_until == 0:
        return "TODAY", "red"
    if days_until <= 7:
        return "URGENT", "orange"
    if days_until <= 30:
        return "WARNING", "yellow"
    return "OK", "green"


def analyze_obligations(calendar_data, today=None):
    """Analyze all obligations and return structured results."""
    if today is None:
        today = datetime.date.today()

    results = []
    for obl in calendar_data.get("obligations", []):
        deadline = get_obligation_deadline(obl, today)
        if deadline is None:
            continue

        days_until = (deadline - today).days
        status = obl.get("status", "pending")
        urgency, color = classify_urgency(days_until, status)

        alert_days = obl.get("alert_days_before", 7)
        needs_alert = days_until <= alert_days and status not in ("submitted", "paid")

        results.append({
            "id": obl.get("id", "unknown"),
            "name": obl.get("name", "Unknown"),
            "entity": obl.get("entity", ""),
            "deadline": deadline.isoformat(),
            "days_until": days_until,
            "status": status,
            "urgency": urgency,
            "color": color,
            "needs_alert": needs_alert,
            "recurrence": obl.get("recurrence"),
            "period": obl.get("period", ""),
            "notes": obl.get("notes", ""),
            "penalty": calendar_data.get("penalties", {}).get(
                f"{obl['id'].split('_')[0]}_late_submission", "Coima aplicavel"
            ),
        })

    results.sort(key=lambda x: x["days_until"])
    return results


def format_table(results):
    """Format results as a readable table."""
    lines = []
    lines.append(f"{'ID':<20} {'Obrigacao':<45} {'Deadline':<12} {'Dias':<6} {'Status':<10} {'Urgencia':<10}")
    lines.append("-" * 110)

    for r in results:
        urgency_marker = {
            "OVERDUE": "!!!",
            "TODAY": "!!",
            "URGENT": "!",
            "WARNING": "*",
            "OK": "",
            "DONE": "v",
        }.get(r["urgency"], "")

        days_str = f"{r['days_until']:>3}d" if r["days_until"] >= 0 else f"{abs(r['days_until']):>2}d LATE"

        lines.append(
            f"{r['id']:<20} {r['name'][:44]:<45} {r['deadline']:<12} {days_str:<6} "
            f"{r['status']:<10} {urgency_marker} {r['urgency']}"
        )

    return "\n".join(lines)


def format_next(results):
    """Format the next upcoming obligation with checklist."""
    pending = [r for r in results if r["status"] not in ("submitted", "paid")]
    if not pending:
        return "Todas as obrigacoes estao em dia!"

    nxt = pending[0]
    lines = [
        f"PROXIMA OBRIGACAO: {nxt['name']}",
        f"ID: {nxt['id']}",
        f"Entidade: {nxt['entity']}",
        f"Deadline: {nxt['deadline']} ({nxt['days_until']} dias)",
        f"Urgencia: {nxt['urgency']}",
        f"Penalidade: {nxt['penalty']}",
    ]
    if nxt.get("period"):
        lines.append(f"Periodo: {nxt['period']}")
    if nxt.get("notes"):
        lines.append(f"Notas: {nxt['notes']}")

    return "\n".join(lines)


def submit_obligation(calendar_data, obligation_id):
    """Mark an obligation as submitted."""
    today = datetime.date.today().isoformat()
    for obl in calendar_data.get("obligations", []):
        if obl.get("id") == obligation_id:
            obl["status"] = "submitted"
            obl["submitted_at"] = today
            save_calendar(calendar_data)
            return f"Obrigacao '{obligation_id}' marcada como submetida em {today}"
    return f"Obrigacao '{obligation_id}' nao encontrada"


def get_exit_code(results):
    """Return exit code based on worst urgency."""
    urgencies = [r["urgency"] for r in results if r["status"] not in ("submitted", "paid")]
    if "OVERDUE" in urgencies or "TODAY" in urgencies:
        return 3
    if "URGENT" in urgencies:
        return 2
    if "WARNING" in urgencies:
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="DARIO CFO Tax Calendar Engine")
    parser.add_argument("--next", action="store_true", help="Show next obligation")
    parser.add_argument("--alerts", action="store_true", help="Show only alerts")
    parser.add_argument("--overdue", action="store_true", help="Show only overdue")
    parser.add_argument("--month", type=str, help="Filter by month (MM)")
    parser.add_argument("--submit", type=str, metavar="ID", help="Mark obligation as submitted")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--check", action="store_true", help="Silent check, exit code only")
    parser.add_argument("--quiet", action="store_true", help="Suppress info logging")
    args = parser.parse_args()

    if args.quiet:
        log.setLevel(logging.WARNING)

    calendar_data = load_calendar()

    # Handle submit action
    if args.submit:
        result = submit_obligation(calendar_data, args.submit)
        print(result)
        return

    # Analyze
    today = datetime.date.today()
    results = analyze_obligations(calendar_data, today)

    # Filter
    if args.alerts:
        results = [r for r in results if r["needs_alert"]]
    elif args.overdue:
        results = [r for r in results if r["urgency"] in ("OVERDUE", "TODAY")]
    elif args.month:
        month = int(args.month)
        results = [r for r in results if datetime.date.fromisoformat(r["deadline"]).month == month]

    # Silent check mode
    if args.check:
        sys.exit(get_exit_code(results))

    # Output
    if args.json:
        output = {
            "date": today.isoformat(),
            "total_obligations": len(results),
            "overdue": len([r for r in results if r["urgency"] in ("OVERDUE", "TODAY")]),
            "urgent": len([r for r in results if r["urgency"] == "URGENT"]),
            "warnings": len([r for r in results if r["urgency"] == "WARNING"]),
            "ok": len([r for r in results if r["urgency"] in ("OK", "DONE")]),
            "obligations": results,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.next:
        print(format_next(results))
    else:
        print(f"\n=== CALENDARIO FISCAL PT — {today.isoformat()} ===\n")
        print(format_table(results))

        # Summary
        overdue = len([r for r in results if r["urgency"] in ("OVERDUE", "TODAY")])
        urgent = len([r for r in results if r["urgency"] == "URGENT"])
        warning = len([r for r in results if r["urgency"] == "WARNING"])
        done = len([r for r in results if r["urgency"] == "DONE"])

        print(f"\nResumo: {overdue} overdue | {urgent} urgente | {warning} aviso | {done} concluido")

    sys.exit(get_exit_code(results))


if __name__ == "__main__":
    main()
