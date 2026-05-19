#!/usr/bin/env python3
"""
DARIO Cron Daily — Background Learning + Drift Detection
=========================================================
Upgrade 12 (operational complement to Sprints 1-4).

Runs once per day the maintenance jobs that the cognitive upgrades
produce data for, but which no daemon currently triggers:

  1. episode_promoter --promote --auto-rule    Cristalize patterns from
                                                last 24h of episodes
  2. golden_eval --regression-check             Compare any cached eval
                                                outputs vs goldens, flag drift
  3. dispatch_cot stats                         Calculate overconfidence rate
  4. synaptic + qvalue state snapshot           Growth/decay tracking

Outputs:
    cron/daily-YYYY-MM-DD.yaml       Full structured report per run
    cron/last_run.yaml               Idempotency guard (gating "ran today?")
    pulse_report alert entries       For session_boot to surface

Idempotency: --maybe-run skips if last run was <22h ago. Use --force to
override. Session_boot calls --maybe-run automatically.

Schedule integration (Windows):
    Option A — session-boot hook (default, no setup):
        Automatically runs --maybe-run on every session start.
    Option B — Task Scheduler (true 24/7 daemon):
        schtasks /create /sc daily /tn "DARIO-Cron-Daily" /tr "python C:\\Users\\barda\\.claude\\orchestrator\\cron_daily.py --json" /st 03:00

CLI:
    python cron_daily.py                Run now (respects gating)
    python cron_daily.py --maybe-run    Run only if >22h since last run
    python cron_daily.py --force        Force run even if recent
    python cron_daily.py --dry-run      Show what would run
    python cron_daily.py --status       Show last-run + recent history
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True
    _yaml.width = 200

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _yaml.load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(data, f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _pyaml.safe_load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _pyaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CRON_DIR = ORCH_DIR / "cron"
LAST_RUN_FILE = CRON_DIR / "last_run.yaml"
PULSE_FILE = ORCH_DIR / "last_pulse.yaml"

# Gating threshold — only run again after this much time
COOLDOWN_HOURS = 22

# Alert thresholds
OVERCONFIDENCE_ALERT_RATE = 0.20    # >20% OVERCONFIDENT verdicts -> alert
QVALUE_AVG_FLOOR = 0.50             # avg Q-value dropping below this -> warn
GOLDEN_DRIFT_ALERT_COUNT = 1        # any drift -> alert


def _ensure_dirs():
    CRON_DIR.mkdir(parents=True, exist_ok=True)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _last_run() -> dict:
    if not LAST_RUN_FILE.exists():
        return {}
    try:
        data = _load_yaml(str(LAST_RUN_FILE))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _hours_since_last_run() -> float:
    last = _last_run()
    ts = last.get("ran_at")
    if not ts:
        return float("inf")
    try:
        last_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (_now() - last_dt).total_seconds() / 3600
    except Exception:
        return float("inf")


def _save_last_run(report: dict):
    payload = {
        "ran_at": report["timestamp"],
        "duration_seconds": report.get("duration_seconds"),
        "alerts": len(report.get("alerts", [])),
        "warnings": len(report.get("warnings", [])),
        "report_file": report.get("report_file"),
    }
    _dump_yaml(payload, str(LAST_RUN_FILE))


def _run_job(name: str, fn):
    """Execute a single job, capture output + error, time it."""
    start = _now()
    try:
        result = fn()
        return {
            "name": name,
            "status": "ok",
            "duration_seconds": (_now() - start).total_seconds(),
            "output": result,
        }
    except Exception as e:
        return {
            "name": name,
            "status": "error",
            "duration_seconds": (_now() - start).total_seconds(),
            "error": str(e)[:300],
        }


def job_promote_episodes() -> dict:
    """Episode → Semantic promotion (last 24h window)."""
    sys.path.insert(0, str(ORCH_DIR))
    from episode_promoter import promote, stats
    pre_stats = stats()
    result = promote(days=1, generate_rules=True, verbose=False)
    post_stats = stats()
    return {
        "promoted_excellence": result.get("promoted_excellence", 0),
        "promoted_patterns": result.get("promoted_patterns", 0),
        "rules_written": result.get("rules_written", 0),
        "memories_before": pre_stats["semantic_memories"],
        "memories_after": post_stats["semantic_memories"],
        "rules_total": post_stats["auto_rules"],
    }


def job_regression_check() -> dict:
    """Golden eval regression detection."""
    sys.path.insert(0, str(ORCH_DIR))
    from golden_eval import regression_check, list_goldens
    r = regression_check()
    goldens = list_goldens()
    return {
        "total_goldens": len(goldens),
        "with_candidate_outputs": r["with_golden"] - len([x for x in r["report"]
                                                          if x.get("status") == "no_candidate"]),
        "drifting": r["drifting"],
        "alerts": r["alerts"],
        "drift_count": len(r["drifting"]),
        "alert_count": len(r["alerts"]),
    }


def job_dispatch_cot_stats() -> dict:
    """CoT trace + postmortem aggregate."""
    sys.path.insert(0, str(ORCH_DIR))
    from dispatch_cot import stats
    s = stats()
    return {
        "total_traces": s["total_traces"],
        "by_level": s["by_confidence_level"],
        "by_winning_signal": s["by_winning_signal"],
        "postmortems": s["postmortems"],
        "overconfidence_rate": s["overconfidence_rate"],
    }


def job_state_snapshot() -> dict:
    """Snapshot of synaptic + Q-value + semantic memory state."""
    sys.path.insert(0, str(ORCH_DIR))
    snapshot = {}
    try:
        from synaptic_update import stats as syn_stats
        snapshot["synaptic"] = syn_stats()
    except Exception as e:
        snapshot["synaptic_error"] = str(e)[:100]
    try:
        from qvalue_memory_wire import stats as q_stats
        snapshot["qvalue"] = q_stats()
    except Exception as e:
        snapshot["qvalue_error"] = str(e)[:100]
    try:
        from episode_promoter import stats as ep_stats
        snapshot["semantic"] = ep_stats()
    except Exception as e:
        snapshot["semantic_error"] = str(e)[:100]
    try:
        from semantic_dispatch import cache_stats as sem_stats
        snapshot["embeddings"] = {"total": sem_stats()["total"]}
    except Exception as e:
        snapshot["embeddings_error"] = str(e)[:100]
    return snapshot


def job_integrity_gate() -> dict:
    """Integrity Gate (Upgrade 14) — eval/skill/golden/chain/synaptic ref check."""
    tools_dir = ORCH_DIR / "tools"
    sys.path.insert(0, str(tools_dir))
    from integrity_gate import run_all
    report = run_all(strict=False)
    failed_checks = [c["name"] for c in report["checks"]
                     if c.get("status") in ("FAIL", "ERROR")]
    warned_checks = [c["name"] for c in report["checks"]
                     if c.get("status") == "WARN"]
    return {
        "verdict": report["verdict"],
        "exit_code": report["exit_code"],
        "total_checks": len(report["checks"]),
        "failed_checks": failed_checks,
        "warned_checks": warned_checks,
    }


def job_prompt_hints_promote() -> dict:
    """Prompt Hints (Upgrade 17) — extract recurring drilldown patterns
    into learned hints injected by context_injector."""
    sys.path.insert(0, str(ORCH_DIR))
    from prompt_hints import promote, list_hints
    pre_count = len(list_hints())
    stats = promote(verbose=False)
    post_count = len(list_hints())
    return {
        "skills_updated": stats["skills_updated"],
        "hints_added": stats["hints_added"],
        "hints_merged": stats["hints_merged"],
        "total_skill_hint_files_before": pre_count,
        "total_skill_hint_files_after": post_count,
    }


def _evaluate_alerts(report: dict) -> tuple:
    """Inspect job outputs and produce alert + warning lists."""
    alerts = []
    warnings = []

    # Regression check alerts
    reg = next((j for j in report["jobs"] if j["name"] == "regression_check"), None)
    if reg and reg["status"] == "ok":
        o = reg["output"]
        if o.get("alert_count", 0) >= GOLDEN_DRIFT_ALERT_COUNT:
            alerts.append({
                "source": "regression_check",
                "severity": "alert",
                "message": f"{o['alert_count']} eval(s) drifted past alert threshold: {o['alerts']}",
            })
        elif o.get("drift_count", 0) > 0:
            warnings.append({
                "source": "regression_check",
                "severity": "warn",
                "message": f"{o['drift_count']} eval(s) drifting (not yet at alert level)",
            })

    # CoT overconfidence rate
    cot = next((j for j in report["jobs"] if j["name"] == "dispatch_cot_stats"), None)
    if cot and cot["status"] == "ok":
        o = cot["output"]
        rate = o.get("overconfidence_rate", 0)
        if rate >= OVERCONFIDENCE_ALERT_RATE:
            alerts.append({
                "source": "dispatch_cot",
                "severity": "alert",
                "message": f"overconfidence rate {rate:.1%} >= {OVERCONFIDENCE_ALERT_RATE:.0%} — recalibrate signal weights",
            })

    # Q-value drift
    snap = next((j for j in report["jobs"] if j["name"] == "state_snapshot"), None)
    if snap and snap["status"] == "ok":
        qv = snap["output"].get("qvalue", {})
        avg_q = qv.get("avg_q_value", 0)
        if avg_q and avg_q < QVALUE_AVG_FLOOR:
            warnings.append({
                "source": "qvalue_memory",
                "severity": "warn",
                "message": f"avg Q-value dropped to {avg_q} (below floor {QVALUE_AVG_FLOOR})",
            })

    # Integrity gate — FAIL = alert, WARN = warning
    ig = next((j for j in report["jobs"] if j["name"] == "integrity_gate"), None)
    if ig and ig["status"] == "ok":
        o = ig["output"]
        if o.get("verdict") == "FAIL":
            alerts.append({
                "source": "integrity_gate",
                "severity": "alert",
                "message": (
                    f"integrity gate FAIL: {len(o.get('failed_checks', []))} broken "
                    f"check(s) — {', '.join(o.get('failed_checks', []))}"
                ),
            })
        elif o.get("verdict") == "WARN":
            warnings.append({
                "source": "integrity_gate",
                "severity": "warn",
                "message": (
                    f"integrity gate WARN: {len(o.get('warned_checks', []))} check(s) "
                    f"degraded — {', '.join(o.get('warned_checks', []))}"
                ),
            })

    # Job errors are always alerts
    for job in report["jobs"]:
        if job["status"] == "error":
            alerts.append({
                "source": job["name"],
                "severity": "alert",
                "message": f"job failed: {job.get('error', 'unknown')}",
            })

    return alerts, warnings


def _push_to_pulse(alerts: list, warnings: list):
    """Add cron alerts/warnings to last_pulse.yaml so session_boot surfaces them."""
    if not PULSE_FILE.exists():
        return
    try:
        pulse = _load_yaml(str(PULSE_FILE)) or {}
        existing_alerts = pulse.get("alerts", []) or []
        # Tag entries so we don't duplicate on repeated runs
        today = _now().strftime("%Y-%m-%d")
        cron_tag = f"cron-daily-{today}"
        # Remove any prior entries from today's cron run
        existing_alerts = [a for a in existing_alerts
                           if not (isinstance(a, dict) and a.get("source", "").startswith("cron-daily-"))]
        for a in alerts + warnings:
            existing_alerts.append({
                "source": cron_tag,
                "severity": a["severity"],
                "subsystem": a["source"],
                "message": a["message"],
                "timestamp": _now().isoformat(),
            })
        pulse["alerts"] = existing_alerts
        _dump_yaml(pulse, str(PULSE_FILE))
    except Exception:
        pass


def run_all(dry_run: bool = False) -> dict:
    """Execute all daily jobs and produce a structured report."""
    _ensure_dirs()
    start = _now()
    report = {
        "timestamp": start.isoformat(),
        "dry_run": dry_run,
        "jobs": [],
    }

    if dry_run:
        report["jobs"] = [
            {"name": "promote_episodes", "status": "skipped (dry-run)"},
            {"name": "regression_check", "status": "skipped (dry-run)"},
            {"name": "dispatch_cot_stats", "status": "skipped (dry-run)"},
            {"name": "state_snapshot", "status": "skipped (dry-run)"},
            {"name": "integrity_gate", "status": "skipped (dry-run)"},
            {"name": "prompt_hints_promote", "status": "skipped (dry-run)"},
        ]
        report["alerts"] = []
        report["warnings"] = []
        report["duration_seconds"] = (_now() - start).total_seconds()
        return report

    # Execute in sequence (not parallel — they share DB/file locks)
    report["jobs"].append(_run_job("promote_episodes", job_promote_episodes))
    report["jobs"].append(_run_job("regression_check", job_regression_check))
    report["jobs"].append(_run_job("dispatch_cot_stats", job_dispatch_cot_stats))
    report["jobs"].append(_run_job("state_snapshot", job_state_snapshot))
    report["jobs"].append(_run_job("integrity_gate", job_integrity_gate))
    report["jobs"].append(_run_job("prompt_hints_promote", job_prompt_hints_promote))

    report["duration_seconds"] = (_now() - start).total_seconds()

    # Evaluate alerts/warnings
    alerts, warnings = _evaluate_alerts(report)
    report["alerts"] = alerts
    report["warnings"] = warnings
    report["status"] = (
        "alert" if alerts else
        "warn" if warnings else
        "ok"
    )

    # Persist report
    date_str = _now().strftime("%Y-%m-%d")
    report_file = CRON_DIR / f"daily-{date_str}.yaml"
    report["report_file"] = str(report_file)
    _dump_yaml(report, str(report_file))

    # Update last_run
    _save_last_run(report)

    # Push alerts to pulse
    _push_to_pulse(alerts, warnings)

    # Push alerts to webhooks (Upgrade 15). Silent fail if webhook_dispatcher
    # unavailable or no webhooks configured — dispatcher itself handles
    # idempotency to prevent duplicate sends for the same event in 24h.
    if alerts or warnings:
        try:
            sys.path.insert(0, str(ORCH_DIR))
            from webhook_dispatcher import send as _wh_send
            for a in alerts + warnings:
                _wh_send({
                    "event": f"cron_daily_{a['source']}",
                    "severity": a["severity"],
                    "subsystem": a["source"],
                    "message": a["message"],
                })
        except Exception:
            pass

    return report


def maybe_run(force: bool = False) -> dict:
    """Run only if cooldown elapsed. Returns either the report or a skip notice."""
    hours = _hours_since_last_run()
    if not force and hours < COOLDOWN_HOURS:
        return {
            "skipped": True,
            "reason": f"last run was {hours:.1f}h ago (cooldown {COOLDOWN_HOURS}h)",
            "hours_since_last": round(hours, 2),
        }
    return run_all(dry_run=False)


def status() -> dict:
    """Summary of recent cron activity."""
    last = _last_run()
    history = []
    if CRON_DIR.exists():
        for f in sorted(CRON_DIR.glob("daily-*.yaml"), reverse=True)[:7]:
            try:
                data = _load_yaml(str(f))
                if isinstance(data, dict):
                    history.append({
                        "date": f.stem.replace("daily-", ""),
                        "status": data.get("status", "ok"),
                        "alerts": len(data.get("alerts", [])),
                        "warnings": len(data.get("warnings", [])),
                        "duration_seconds": data.get("duration_seconds"),
                    })
            except Exception:
                continue
    return {
        "last_run": last,
        "hours_since_last_run": round(_hours_since_last_run(), 2),
        "cooldown_hours": COOLDOWN_HOURS,
        "recent_runs": history,
    }


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from license_guard import enforce_or_exit
        enforce_or_exit("cron_daily")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Cron Daily")
    p.add_argument("--maybe-run", action="store_true",
                   help="Run only if >22h since last run (default for session_boot)")
    p.add_argument("--force", action="store_true",
                   help="Force run regardless of cooldown")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--status", action="store_true")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.status:
        s = status()
        print(json.dumps(s, indent=2, ensure_ascii=False) if args.json
              else _format_status(s))
        return 0

    if args.maybe_run:
        result = maybe_run(force=False)
    elif args.force:
        result = run_all(dry_run=False)
    elif args.dry_run:
        result = run_all(dry_run=True)
    else:
        # Default: maybe_run behaviour to be safe
        result = maybe_run(force=False)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print(_format_report(result))

    # Exit code: 0 = ok, 1 = warn, 2 = alert
    if result.get("skipped"):
        return 0
    status_label = result.get("status", "ok")
    return {"ok": 0, "warn": 1, "alert": 2}.get(status_label, 0)


def _format_status(s: dict) -> str:
    lines = []
    last = s.get("last_run", {})
    if last:
        lines.append(f"Last run: {last.get('ran_at')} ({s['hours_since_last_run']}h ago)")
        lines.append(f"  alerts={last.get('alerts', 0)}  warnings={last.get('warnings', 0)}")
    else:
        lines.append("Never run.")
    lines.append(f"Cooldown: {s['cooldown_hours']}h")
    if s["recent_runs"]:
        lines.append("\nRecent (last 7):")
        for r in s["recent_runs"]:
            lines.append(f"  {r['date']}  {r['status']:5s}  "
                         f"alerts={r['alerts']} warnings={r['warnings']}  "
                         f"({r.get('duration_seconds', 0):.1f}s)")
    return "\n".join(lines)


def _format_report(r: dict) -> str:
    if r.get("skipped"):
        return f"[skipped] {r['reason']}"
    if r.get("dry_run"):
        return "[dry-run] would execute 4 jobs"
    lines = [
        f"Cron daily complete in {r.get('duration_seconds', 0):.1f}s",
        f"  Status: {r.get('status', 'ok')}",
    ]
    for job in r.get("jobs", []):
        if job["status"] == "ok":
            lines.append(f"  [+] {job['name']} ({job.get('duration_seconds', 0):.1f}s)")
            o = job.get("output", {})
            if isinstance(o, dict):
                # short summary line
                if job["name"] == "promote_episodes":
                    lines.append(f"      promoted: {o.get('promoted_excellence', 0)} excellence + "
                                 f"{o.get('promoted_patterns', 0)} patterns")
                elif job["name"] == "regression_check":
                    lines.append(f"      drift={o.get('drift_count', 0)}  alerts={o.get('alert_count', 0)}")
                elif job["name"] == "dispatch_cot_stats":
                    lines.append(f"      traces={o.get('total_traces', 0)}  "
                                 f"overconfidence_rate={o.get('overconfidence_rate', 0)}")
        else:
            lines.append(f"  [!] {job['name']}: {job.get('error')}")
    if r.get("alerts"):
        lines.append("\nALERTS:")
        for a in r["alerts"]:
            lines.append(f"  ! [{a['source']}] {a['message']}")
    if r.get("warnings"):
        lines.append("\nWARNINGS:")
        for w in r["warnings"]:
            lines.append(f"  ~ [{w['source']}] {w['message']}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
