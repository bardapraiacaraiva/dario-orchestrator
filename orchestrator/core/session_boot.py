#!/usr/bin/env python3
"""
DARIO Session Boot — Automatic dispatch + state check at session start.
Called by SessionStart hook. Lightweight, fast, no blocking.

Does:
1. Evaluate state machine (detect if system should be in GUARDIAN/REFLECTIVE)
2. Run dispatch on unassigned tasks
3. Output brief status for session context injection

Outputs JSON to stdout (picked up by hook system).
"""
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
PYTHON = sys.executable  # Use same Python that's running this script


def run_engine(script: str, args: list) -> dict:
    """Run an orchestrator engine and return parsed JSON output."""
    script_path = ORCH_DIR / script
    if not script_path.exists():
        return {"error": f"{script} not found"}

    try:
        result = subprocess.run(
            [PYTHON, str(script_path)] + args,
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip():
            return json.loads(result.stdout.strip())
        return {"exit_code": result.returncode, "stderr": result.stderr.strip()[:200]}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except json.JSONDecodeError:
        return {"error": "invalid_json", "raw": result.stdout[:200]}
    except Exception as e:
        return {"error": str(e)[:200]}


def main():
    output = {"boot": "ok", "state": None, "dispatch": None, "autodiag": None, "wal_recovered": 0}

    # 0. WAL crash recovery (before anything else)
    try:
        from reliability.filelock import wal_recover
        recovered = wal_recover()
        output["wal_recovered"] = recovered
    except Exception:
        pass

    # 0.5. Reclaim tasks orphaned by a crashed worker (Fase 4, 2026-06-12).
    # Was wired to a non-existent suspend_resume.py (audit F-01) and silently
    # did nothing — orphaned in_progress tasks waited for a running pulse to be
    # reaped. Now reclaims SLA-breached tasks in-process at boot. SLA-respecting,
    # so concurrent live sessions within the window are never disturbed.
    try:
        from core.sla import recover_orphaned
        rec = recover_orphaned()
        output["resumed_tasks"] = rec.get("reclaimed", 0)
    except Exception:
        output["resumed_tasks"] = 0

    # 1. State machine evaluation
    state_result = run_engine("core/state_machine.py", ["--evaluate", "--json"])
    output["state"] = state_result

    # 2. AutoDiag (silent, with auto-fix)
    diag_result = run_engine("core/autodiag_runner.py", ["--fix", "--json"])
    output["autodiag"] = {
        "passed": diag_result.get("passed", 0),
        "total": diag_result.get("total", 0),
        "warnings": diag_result.get("warnings", 0),
        "criticals": diag_result.get("criticals", 0),
    }

    # 3. Dispatch unassigned tasks (skip if GUARDIAN)
    current_state = state_result.get("state", "ACTIVE")
    if current_state != "GUARDIAN":
        dispatch_result = run_engine("dispatch_engine.py", ["--json"])
        output["dispatch"] = dispatch_result
    else:
        output["dispatch"] = {"skipped": "GUARDIAN state — no dispatch allowed"}

    # 4. Brief summary for context
    state_name = state_result.get("state", "?")
    autonomy = state_result.get("autonomy_level", "?")
    health = state_result.get("system_health", 0)
    dispatched = output["dispatch"].get("dispatched", 0) if isinstance(output["dispatch"], dict) else 0
    diag_ok = diag_result.get("passed", 0) == diag_result.get("total", 0)

    summary = f"State: {state_name} | Autonomy: {autonomy} | Health: {health:.2f}"
    diag_label = "OK" if diag_ok else f"{diag_result.get('warnings',0)}W/{diag_result.get('criticals',0)}C"
    summary += f" | Diag: {diag_label}"
    if dispatched > 0:
        summary += f" | Auto-dispatched: {dispatched} tasks"

    output["summary"] = summary

    # 5. Log boot event to unified audit trail
    run_engine("core/audit_logger.py", [
        "-a", "session-boot", "-A", "session_start",
        "-e", "system", "-i", f"boot-{datetime.now(UTC).strftime('%H%M')}",
        "-d", summary
    ])

    # 6. Cron daily (NEW — Upgrade 12). Runs episode promotion, regression
    # detection, CoT stats, and state snapshot. Only fires if >22h since
    # last run (cooldown handled inside cron_daily). Non-blocking — failures
    # never block session boot.
    try:
        cron_result = run_engine("cron_daily.py", ["--maybe-run", "--json"])
        if cron_result.get("skipped"):
            output["cron_daily"] = {"skipped": True}
        else:
            output["cron_daily"] = {
                "status": cron_result.get("status", "ok"),
                "alerts": len(cron_result.get("alerts", [])),
                "warnings": len(cron_result.get("warnings", [])),
                "duration": cron_result.get("duration_seconds"),
            }
    except Exception:
        output["cron_daily"] = {"error": "unavailable"}

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
