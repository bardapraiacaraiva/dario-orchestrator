#!/usr/bin/env python3
"""
DARIO AutoDiag Runner — Executes system health checks.
=======================================================
Implements the 7 checks defined in autodiag.yaml as real executable code.
Silent by default — only reports problems.

Usage:
    python autodiag_runner.py              # Run all checks, silent if OK
    python autodiag_runner.py --verbose    # Show all check results
    python autodiag_runner.py --fix        # Apply auto-fixes for fixable issues
    python autodiag_runner.py --json       # Machine-readable output
    python autodiag_runner.py --check X    # Run single check by ID

Exit codes:
    0 = all checks pass
    1 = error (missing files)
    2 = warnings found (non-critical)
    3 = critical issues found
"""

import argparse
import logging
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

try:
    from ruamel.yaml import YAML
    yaml_engine = YAML()
    yaml_engine.preserve_quotes = True
    yaml_engine.width = 200

    def load_yaml(path):
        with open(path, encoding='utf-8') as f:
            return yaml_engine.load(f)

    def dump_yaml(data, path):
        with open(path, 'w', encoding='utf-8') as f:
            yaml_engine.dump(data, f)
except ImportError:
    import yaml
    def load_yaml(path):
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)
    def dump_yaml(data, path):
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
TASKS_DIR = ORCH_DIR / "tasks" / "active"
DONE_DIR = ORCH_DIR / "tasks" / "done"
COMPANY_FILE = ORCH_DIR / "company.yaml"
QUALITY_FILE = ORCH_DIR / "quality" / "skill-metrics.yaml"
BUDGET_DIR = ORCH_DIR / "budgets"
AUDIT_DIR = ORCH_DIR / "audit"
def _resolve_memory_dir() -> Path:
    """Resolve the auto-memory dir without hard-coding a user slug.

    Claude Code creates dirs like ~/.claude/projects/C--Users-<user>/memory/.
    We pick the first existing one (there's usually only one per user).
    Falls back to barda's path for legacy compat if no match found.
    Override via DARIO_MEMORY_DIR env var for multi-tenant installs (RFC §5 PW-1).
    """
    import os
    override = os.environ.get("DARIO_MEMORY_DIR")
    if override:
        return Path(override)

    projects_dir = Path.home() / ".claude" / "projects"
    if projects_dir.exists():
        for child in projects_dir.iterdir():
            if child.is_dir() and (child / "memory").is_dir():
                return child / "memory"

    # Last-resort fallback (legacy barda path) — preserves existing behavior
    # when the new logic finds nothing.
    return Path.home() / ".claude" / "projects" / "C--Users-barda" / "memory"


MEMORY_DIR = _resolve_memory_dir()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("autodiag")


# =============================================================================
# HELPERS
# =============================================================================

def load_all_tasks() -> list:
    """Load tasks — DB first, YAML fallback (fixed: was YAML-only)."""
    try:
        sys.path.insert(0, str(ORCH_DIR))
        from core.db import DB
        db = DB()
        tasks = db.get_tasks()
        if tasks:
            return tasks
    except Exception:
        pass
    # YAML fallback
    tasks = []
    if not TASKS_DIR.exists():
        return tasks
    for f in TASKS_DIR.glob("*.yaml"):
        try:
            data = load_yaml(str(f))
            if data:
                data["_file"] = str(f)
                tasks.append(data)
        except Exception:
            pass
    return tasks


def persist_task_changes(t: dict) -> bool:
    """Persist task changes to whichever source the task came from.

    YAML-loaded tasks have '_file' key — write back to that file.
    DB-loaded tasks lack '_file' — update via db.update_task (column whitelist).

    Returns True on success. Logs warning on failure but does not raise.
    """
    if "_file" in t and t.get("_file"):
        try:
            dump_yaml({k: v for k, v in t.items() if k != "_file"}, t["_file"])
            return True
        except Exception as e:
            log.warning(f"YAML persist failed for {t.get('id')}: {e}")
            return False

    # DB-loaded task — update via DB API (respects column whitelist + transitions)
    try:
        sys.path.insert(0, str(ORCH_DIR))
        from core.db import DB
        db_inst = DB()
        # Serialize depends_on if it's a list (DB stores TEXT JSON)
        fields = dict(t)
        deps = fields.get("depends_on")
        if isinstance(deps, list):
            import json as _json
            fields["depends_on"] = _json.dumps(deps)
        # Remove non-column metadata
        for k in ("id", "_file"):
            fields.pop(k, None)
        return db_inst.update_task(t["id"], fields)
    except Exception as e:
        log.warning(f"DB persist failed for {t.get('id')}: {e}")
        return False


def load_done_task_ids_with_status() -> dict:
    """Return mapping of task_id -> status for tasks in done/ folder.

    Used by dependency_integrity and false_cascade_correction checks to
    distinguish 'dep moved to done/ folder after completion' (valid)
    from 'dep never existed' (invalid).
    """
    result = {}
    if not DONE_DIR.exists():
        return result
    for f in DONE_DIR.glob("*.yaml"):
        try:
            data = load_yaml(str(f))
            if data and data.get("id"):
                result[data["id"]] = data.get("status", "done")
        except Exception:
            pass
    return result


def load_company_workers() -> set:
    if not COMPANY_FILE.exists():
        return set()
    data = load_yaml(str(COMPANY_FILE))
    workers = set()
    for wid in (data.get("workers") or {}).keys():
        workers.add(wid)
    for agent in (data.get("agents") or {}).values():
        if isinstance(agent, dict) and "id" in agent:
            workers.add(agent["id"])
    return workers


# =============================================================================
# CHECKS
# =============================================================================

def check_coherence(tasks: list, workers: set, fix: bool) -> dict:
    """Verify all assignees exist in company.yaml.

    Skip done/cancelled tasks — their assignee history is immaterial once
    the work is complete. Re-blocking a done task would corrupt outcomes.
    """
    TERMINAL_STATUSES = {"done", "cancelled"}
    issues = []
    for t in tasks:
        if t.get("status") in TERMINAL_STATUSES:
            continue
        assignee = t.get("assignee")
        if assignee and assignee != "null" and assignee not in workers:
            issue = {
                "task": t.get("id"),
                "assignee": assignee,
                "problem": "assignee not in company.yaml",
                "current_status": t.get("status"),
            }
            if fix:
                t["status"] = "blocked"
                t["blocked_reason"] = f"assignee '{assignee}' not found in hierarchy"
                persist_task_changes(t)
                issue["fixed"] = True
            issues.append(issue)

    return {"id": "coherence_check", "severity": "warning", "passed": len(issues) == 0, "issues": issues}


def check_orphans(tasks: list, fix: bool) -> dict:
    """Find tasks with parent IDs that don't exist."""
    task_ids = {t.get("id") for t in tasks}
    issues = []
    for t in tasks:
        parent = t.get("parent")
        if parent and parent not in task_ids:
            issue = {"task": t.get("id"), "parent": parent, "problem": "parent task missing"}
            if fix:
                del_keys = [k for k in t if k == "parent"]
                for k in del_keys:
                    t[k] = None
                t.setdefault("notes", [])
                if isinstance(t.get("notes"), list):
                    t["notes"].append("orphaned — parent removed by autodiag")
                persist_task_changes(t)
                issue["fixed"] = True
            issues.append(issue)

    return {"id": "orphan_detection", "severity": "info", "passed": len(issues) == 0, "issues": issues}


def check_dependencies(tasks: list, done_ids: dict, fix: bool) -> dict:
    """Verify all depends_on references exist in active/ OR done/.

    A dep moved to done/ is still a valid reference (historical lineage).
    Only deps that exist in NEITHER folder are truly broken.
    """
    active_ids = {t.get("id") for t in tasks}
    all_ids = active_ids | set(done_ids.keys())
    issues = []
    for t in tasks:
        deps = t.get("depends_on", [])
        if not isinstance(deps, list):
            continue
        broken = [d for d in deps if d not in all_ids]
        if broken:
            issue = {"task": t.get("id"), "broken_deps": broken}
            if fix:
                t["depends_on"] = [d for d in deps if d in all_ids]
                persist_task_changes(t)
                issue["fixed"] = True
            issues.append(issue)

    return {"id": "dependency_integrity", "severity": "warning", "passed": len(issues) == 0, "issues": issues}


def check_false_cascade(tasks: list, done_ids: dict, fix: bool) -> dict:
    """Detect tasks blocked by cascade reason whose deps are actually done.

    Background: a previous one-off audit bulk-marked tasks status:blocked with
    blocked_reason 'awaiting_upstream' under the assumption their deps were
    still pending. When the deps later moved to done/, the cascade-block never
    got reconciled. This check finds and (optionally) unblocks them.

    A task is considered false-cascade if:
      - status == 'blocked'
      - blocked_reason indicates cascade (awaiting_upstream / cascade / awaiting_founder_day_0)
      - ALL items in depends_on have status:done in done/ folder

    Partial cascades (some deps done, some not) are reported but NOT auto-fixed —
    they need human review to decide if the remaining gates are real.
    """
    CASCADE_MARKERS = ("awaiting_upstream", "awaiting_founder_day_0", "cascade")
    issues = []
    for t in tasks:
        if t.get("status") != "blocked":
            continue
        reason = (t.get("blocked_reason") or "")
        reason_lower = reason.lower() if isinstance(reason, str) else ""
        is_cascade = any(marker in reason_lower for marker in CASCADE_MARKERS)
        if not is_cascade:
            continue
        deps = t.get("depends_on") or []
        if not isinstance(deps, list) or not deps:
            continue

        unfinished = [d for d in deps if done_ids.get(d) != "done"]
        all_done = len(unfinished) == 0

        if all_done:
            issue = {
                "task": t.get("id"),
                "deps": deps,
                "old_reason": reason,
                "action": "unblock (all deps done)",
            }
            if fix:
                t["status"] = "todo"
                t["blocked_reason"] = None
                t.setdefault("notes", [])
                if isinstance(t.get("notes"), list):
                    ts = datetime.now(UTC).isoformat()
                    t["notes"].append(
                        f"[{ts}] AutoDiag false_cascade_correction: deps {deps} "
                        f"confirmed status:done in done/. status: blocked->todo, "
                        f"blocked_reason cleared."
                    )
                t["updated_at"] = datetime.now(UTC).isoformat()
                persist_task_changes(t)
                issue["fixed"] = True
            issues.append(issue)
        elif len(unfinished) < len(deps):
            # Partial: some deps done, some not — flag for human review
            issues.append({
                "task": t.get("id"),
                "partial_cascade": True,
                "done_deps": [d for d in deps if done_ids.get(d) == "done"],
                "unfinished_deps": unfinished,
                "action": "review_manually_or_refine_blocked_reason",
            })

    return {"id": "false_cascade_correction", "severity": "warning", "passed": len(issues) == 0, "issues": issues}


def check_budget_drift(tasks: list, fix: bool) -> dict:
    """Compare sum of task tokens vs budget total."""
    now = datetime.now(UTC)
    budget_file = BUDGET_DIR / f"{now.strftime('%Y-%m')}.yaml"
    if not budget_file.exists():
        return {"id": "budget_drift", "severity": "warning", "passed": True, "issues": [], "note": "no budget file"}

    budget = load_yaml(str(budget_file))
    recorded_total = int(budget.get("total_tokens_used") or 0)

    # Sum actual tokens from tasks
    task_sum = 0
    for t in tasks:
        tokens = t.get("actual_tokens")
        if tokens and str(tokens).isdigit():
            task_sum += int(tokens)

    drift = abs(recorded_total - task_sum)
    issues = []
    if drift > 1000:  # >1K token drift
        issue = {"recorded": recorded_total, "calculated": task_sum, "drift": drift}
        # NEVER downgrade the budget — many tasks may lack actual_tokens
        # (e.g. assigned manually, dispatched outside orchestrator).
        # The recorded total reflects real Anthropic API spend; auto-fixing
        # downward would lose unattributed history.
        if fix and task_sum > recorded_total:
            issue["direction"] = "upgrade"
            budget["total_tokens_used"] = task_sum
            budget["percentage"] = round(task_sum / int(budget.get("limit", 50000000)) * 100, 2)
            budget["last_updated"] = now.isoformat()
            dump_yaml(budget, str(budget_file))
            issue["fixed"] = True
        elif task_sum < recorded_total:
            issue["direction"] = "no_fix (would_downgrade)"
            issue["note"] = "task_sum < recorded — likely tasks without actual_tokens attribution; recorded preserved"
        issues.append(issue)

    return {"id": "budget_drift", "severity": "warning", "passed": len(issues) == 0, "issues": issues}


def check_stale_review(tasks: list, fix: bool) -> dict:
    """Find tasks in_review too long."""
    issues = []
    now = datetime.now(UTC)
    for t in tasks:
        if t.get("status") != "in_review":
            continue
        scored_at = t.get("scored_at") or t.get("updated_at") or t.get("assigned_at")
        if not scored_at:
            continue
        try:
            ts = datetime.fromisoformat(str(scored_at).replace("Z", "+00:00"))
            age_hours = (now - ts).total_seconds() / 3600
            sla = {"critical": 1, "client_facing": 4, "financial": 2}.get(
                t.get("execution_policy", "default"), 8
            )
            if age_hours > sla * 2:
                issue = {"task": t.get("id"), "age_hours": round(age_hours, 1), "sla": sla}
                # Auto-approve if score meets threshold
                if fix:
                    score = t.get("quality_score", 0)
                    if score and int(score) >= 75:
                        t["status"] = "done"
                        persist_task_changes(t)
                        issue["fixed"] = True
                        issue["action"] = "auto-approved (score >= 75)"
                issues.append(issue)
        except (ValueError, TypeError):
            pass

    return {"id": "stale_review", "severity": "critical", "passed": len(issues) == 0, "issues": issues}


def check_quality_regression(tasks: list, fix: bool) -> dict:
    """Check if recent scores show regression."""
    if not QUALITY_FILE.exists():
        return {"id": "quality_regression", "severity": "critical", "passed": True, "issues": [], "note": "no metrics"}

    metrics = load_yaml(str(QUALITY_FILE))
    all_scores = []
    for sd in (metrics.get("skills") or {}).values():
        if isinstance(sd, dict):
            scores = sd.get("live_scores") or sd.get("scores") or []
            if isinstance(scores, list):
                all_scores.extend(scores)

    issues = []
    if len(all_scores) >= 5:
        last_5_avg = sum(all_scores[-5:]) / 5
        baseline = metrics.get("global_avg_quality", 85)
        drop = baseline - last_5_avg
        if drop > 15:
            issues.append({
                "last_5_avg": round(last_5_avg, 1),
                "baseline": baseline,
                "drop": round(drop, 1),
                "action": "quality regression detected — review needed",
            })

    return {"id": "quality_regression", "severity": "critical", "passed": len(issues) == 0, "issues": issues}


def check_skill_regression(tasks: list, fix: bool) -> dict:
    """Per-skill regression detection.

    Trigger: any skill whose last 5 live_scores show mean drop >= 10 pts
    vs that skill's avg_quality_score baseline. Routes to pending-review.yaml.

    Unlike check_quality_regression (global mean), this catches skill-level
    degradation that gets masked by stable global averages.
    """
    if not QUALITY_FILE.exists():
        return {"id": "skill_regression", "severity": "critical", "passed": True, "issues": [], "note": "no metrics"}

    metrics = load_yaml(str(QUALITY_FILE))
    skills = (metrics or {}).get("skills") or {}

    issues = []
    flagged_for_review = []

    for skill_name, sd in skills.items():
        if not isinstance(sd, dict):
            continue
        # Collect live_scores from any field that exposes them
        live = sd.get("live_scores") or sd.get("live_scores_compiled_sprint3v2") or \
               sd.get("live_scores_compiled_sprint3") or sd.get("live_scores_compiled") or []
        if not isinstance(live, list) or len(live) < 5:
            continue
        last_5 = [float(s) for s in live[-5:] if isinstance(s, (int, float))]
        if len(last_5) < 5:
            continue
        baseline = float(sd.get("avg_quality_score", 0) or 0)
        if baseline <= 0:
            continue
        last_5_avg = sum(last_5) / 5
        drop = baseline - last_5_avg
        if drop >= 10.0:
            issues.append({
                "skill": skill_name,
                "baseline": round(baseline, 1),
                "last_5_avg": round(last_5_avg, 1),
                "drop": round(drop, 1),
                "tier": sd.get("tier", "unknown"),
                "action": f"per-skill regression: {skill_name} dropped {round(drop,1)}pts over last 5 runs",
            })
            flagged_for_review.append({
                "skill": skill_name,
                "reason": "skill_regression",
                "drop_pts": round(drop, 1),
                "detected_at": datetime.now(UTC).isoformat(),
            })

    # Auto-route to pending-review.yaml (non-destructive: append-only)
    if fix and flagged_for_review:
        review_path = ORCH_DIR / "quality" / "pending-review.yaml"
        try:
            existing = load_yaml(str(review_path)) if review_path.exists() else {}
            if not isinstance(existing, dict):
                existing = {}
            queue = existing.get("regression_queue") or []
            existing_skills = {item.get("skill") for item in queue if isinstance(item, dict)}
            for entry in flagged_for_review:
                if entry["skill"] not in existing_skills:
                    queue.append(entry)
            existing["regression_queue"] = queue
            existing["last_skill_regression_scan"] = datetime.now(UTC).isoformat()
            dump_yaml(existing, str(review_path))
        except Exception as e:
            log.warning(f"skill_regression: failed to write pending-review.yaml: {e}")

    return {
        "id": "skill_regression",
        "severity": "critical",
        "passed": len(issues) == 0,
        "issues": issues,
    }


def check_memory_staleness(fix: bool) -> dict:
    """Check if project memories are stale (>30 days)."""
    issues = []
    if not MEMORY_DIR.exists():
        return {"id": "memory_staleness", "severity": "info", "passed": True, "issues": []}

    now = datetime.now(UTC)
    threshold = timedelta(days=30)

    for f in MEMORY_DIR.glob("*.md"):
        if f.name == "MEMORY.md":
            continue
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=UTC)
            age = now - mtime
            if age > threshold:
                issues.append({
                    "file": f.name,
                    "age_days": age.days,
                    "last_modified": mtime.strftime("%Y-%m-%d"),
                })
        except Exception:
            pass

    return {"id": "memory_staleness", "severity": "info", "passed": len(issues) == 0, "issues": issues}


# =============================================================================
# MAIN
# =============================================================================

def check_metrics_invariant(tasks: list, fix: bool) -> dict:
    """Invariant: avg_quality_score must equal mean(scores[-20:]) and
    total_executions must equal len(scores). Drift means a non-canonical writer
    (e.g. the archived DSPy compile) corrupted the aggregate — this was the root
    cause of the DB<->YAML divergence fixed 2026-06-01. quality_scorer.py is the
    SINGLE legitimate writer of these fields. With fix=True, recompute from the
    trustworthy scores[] array (mirrors quality/reconcile_skill_metrics.py)."""
    if not QUALITY_FILE.exists():
        return {"id": "metrics_invariant", "severity": "critical", "passed": True, "issues": [], "note": "no metrics"}

    metrics = load_yaml(str(QUALITY_FILE))
    issues, dirty = [], False
    for name, sd in (metrics.get("skills") or {}).items():
        if not isinstance(sd, dict):
            continue
        scores = [s.get("score") if isinstance(s, dict) else s for s in (sd.get("scores") or [])]
        scores = [x for x in scores if isinstance(x, (int, float))]
        if not scores:
            continue
        expect_avg = round(sum(scores[-20:]) / len(scores[-20:]), 1)
        expect_n = len(scores)
        cur_avg = sd.get("avg_quality_score")
        cur_n = sd.get("total_executions")
        if (cur_avg is None or abs(cur_avg - expect_avg) > 1.0) or (cur_n != expect_n):
            issues.append({"skill": name, "stored_avg": cur_avg, "expected_avg": expect_avg,
                           "stored_n": cur_n, "expected_n": expect_n})
            if fix:
                sd["avg_quality_score"] = expect_avg
                sd["avg_quality_alltime"] = round(sum(scores) / len(scores), 1)
                sd["total_executions"] = expect_n
                sd["revision_rate"] = round(sum(1 for s in scores if s < 60) / len(scores), 2)
                sd["best_score"], sd["worst_score"] = max(scores), min(scores)
                sd["tier"] = "A" if expect_avg >= 85 else "B" if expect_avg >= 75 else "C"
                dirty = True
    if fix and dirty:
        scored = [m["avg_quality_score"] for m in metrics["skills"].values()
                  if isinstance(m, dict) and m.get("avg_quality_score")]
        if scored:
            metrics["global_avg_quality"] = round(sum(scored) / len(scored), 1)
        try:
            dump_yaml(metrics, str(QUALITY_FILE))
        except Exception as e:
            log.warning(f"metrics_invariant: failed to write skill-metrics.yaml: {e}")
    return {"id": "metrics_invariant", "severity": "critical", "passed": len(issues) == 0, "issues": issues}


def run_all_checks(fix: bool = False, single: str = None) -> list:
    tasks = load_all_tasks()
    workers = load_company_workers()
    done_ids = load_done_task_ids_with_status()

    all_checks = {
        "coherence_check": lambda: check_coherence(tasks, workers, fix),
        "orphan_detection": lambda: check_orphans(tasks, fix),
        "dependency_integrity": lambda: check_dependencies(tasks, done_ids, fix),
        "false_cascade_correction": lambda: check_false_cascade(tasks, done_ids, fix),
        "budget_drift": lambda: check_budget_drift(tasks, fix),
        "stale_review": lambda: check_stale_review(tasks, fix),
        "quality_regression": lambda: check_quality_regression(tasks, fix),
        "skill_regression": lambda: check_skill_regression(tasks, fix),
        "metrics_invariant": lambda: check_metrics_invariant(tasks, fix),
        "memory_staleness": lambda: check_memory_staleness(fix),
    }

    if single:
        if single not in all_checks:
            return [{"id": single, "error": f"Unknown check. Available: {list(all_checks.keys())}"}]
        return [all_checks[single]()]

    return [fn() for fn in all_checks.values()]


def log_results(results: list):
    """Append to audit log."""
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    log_file = AUDIT_DIR / "autodiag.log"
    ts = datetime.now(UTC).isoformat()

    warnings = sum(1 for r in results if not r.get("passed") and r.get("severity") == "warning")
    criticals = sum(1 for r in results if not r.get("passed") and r.get("severity") == "critical")

    if warnings == 0 and criticals == 0:
        code = f"DARIO_AUTODIAG_OK_{ts}"
    elif criticals > 0:
        code = f"DARIO_AUTODIAG_FAIL_{criticals}critical_{warnings}warn_{ts}"
    else:
        code = f"DARIO_AUTODIAG_WARN_{warnings}issues_{ts}"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {code}\n")
        for r in results:
            if not r.get("passed"):
                f.write(f"  {r['id']}: {len(r.get('issues', []))} issues ({r.get('severity')})\n")


def main():
    parser = argparse.ArgumentParser(description="DARIO AutoDiag — System health checks")
    parser.add_argument("--fix", "-f", action="store_true", help="Apply auto-fixes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all results")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--check", "-c", help="Run single check by ID")

    args = parser.parse_args()
    if args.json:
        logging.getLogger().setLevel(logging.ERROR)

    results = run_all_checks(fix=args.fix, single=args.check)
    log_results(results)

    passed = sum(1 for r in results if r.get("passed"))
    warnings = [r for r in results if not r.get("passed") and r.get("severity") == "warning"]
    criticals = [r for r in results if not r.get("passed") and r.get("severity") == "critical"]
    infos = [r for r in results if not r.get("passed") and r.get("severity") == "info"]

    if args.json:
        import json
        print(json.dumps({
            "passed": passed,
            "total": len(results),
            "warnings": len(warnings),
            "criticals": len(criticals),
            "infos": len(infos),
            "results": results,
        }, indent=2))
    else:
        if not args.verbose and not warnings and not criticals and not infos:
            print(f"DARIO_AUTODIAG_OK — {passed}/{len(results)} checks passed")
        else:
            print(f"=== AUTODIAG: {passed}/{len(results)} passed ===\n")
            for r in results:
                status = "PASS" if r.get("passed") else r.get("severity", "?").upper()
                mark = "+" if r.get("passed") else "!"
                print(f"  [{mark}] {r['id']}: {status}")
                if not r.get("passed") or args.verbose:
                    for issue in r.get("issues", []):
                        fixed = " [FIXED]" if issue.get("fixed") else ""
                        print(f"      - {issue}{fixed}")
            if warnings or criticals:
                print(f"\n  Summary: {len(criticals)} critical, {len(warnings)} warning, {len(infos)} info")

    if criticals:
        return 3
    elif warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
