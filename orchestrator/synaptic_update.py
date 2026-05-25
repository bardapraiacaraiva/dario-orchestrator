#!/usr/bin/env python3
"""
DARIO Synaptic Weights Write-Back
=================================
Upgrade 3 (Sprint 1) of the Cognitive Audit roadmap.

The orchestrator already READ synaptic_weights.yaml at dispatch time (via
dispatch_engine.get_weight_boost). It NEVER wrote back. Evolution happened
only in offline batch cycles. This module closes the loop:

  task done -> find companion skills in same project in time window ->
  update affinity weight in-place (increment if both scored high, decrement
  if either scored low). Atomic via filelock.

Reinforcement parameters come from synaptic_weights.yaml:reinforcement
(success_threshold=85, failure_threshold=50, increment=0.05).

CLI:
    python synaptic_update.py --simulate skill-a skill-b 88 90   Dry-run
    python synaptic_update.py --recompute                        Recompute all from done tasks
    python synaptic_update.py --task TASK-001 --score 88         Process a single completion
    python synaptic_update.py --stats                            Show current weights summary
"""

import argparse
import json
import sqlite3
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True
    _yaml.width = 200

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _yaml.load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(data, f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _pyaml.safe_load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _pyaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=True)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
WEIGHTS_FILE = ORCH_DIR / "synaptic_weights.yaml"
DB_PATH = ORCH_DIR / "orchestrator.db"

# Defaults if reinforcement block is missing from weights file
DEFAULT_REINFORCEMENT = {
    "success_threshold": 85,
    "failure_threshold": 50,
    "success_increment": 0.05,
    "failure_decrement": 0.05,
    "max_weight": 1.0,
    "min_weight": 0.1,
}

# Companion window — two skills completed within this many hours
# on the same project count as co-activated.
COMPANION_WINDOW_HOURS = 24


def _pair_key(a: str, b: str) -> str:
    """Canonical pair key, alphabetical so 'a + b' == 'b + a'."""
    x, y = sorted([a, b])
    return f"{x} + {y}"


def _load_weights() -> dict:
    if not WEIGHTS_FILE.exists():
        return {"affinity_graph": {}, "reinforcement": dict(DEFAULT_REINFORCEMENT)}
    data = _load_yaml(str(WEIGHTS_FILE))
    if not isinstance(data, dict):
        return {"affinity_graph": {}, "reinforcement": dict(DEFAULT_REINFORCEMENT)}
    data.setdefault("affinity_graph", {})
    data.setdefault("reinforcement", dict(DEFAULT_REINFORCEMENT))
    return data


def _save_weights(data: dict) -> None:
    # Atomic write via filelock if available, plain write as fallback
    try:
        sys.path.insert(0, str(ORCH_DIR))
        from filelock import YAMLLock
        with YAMLLock(str(WEIGHTS_FILE), timeout=5) as lock:
            lock.write(data)
            return
    except Exception:
        pass
    _dump_yaml(data, str(WEIGHTS_FILE))


def update_pair(skill_a: str, skill_b: str, score_a: int, score_b: int,
                note: str = "", simulate: bool = False) -> dict:
    """Update affinity weight for a skill pair given their combined scores.

    Returns delta dict:
        {"pair": "a + b", "old_weight": 0.55, "new_weight": 0.60,
         "old_co_act": 4, "new_co_act": 5, "combined_avg": 89.0,
         "rule_applied": "success_increment" | "failure_decrement" | "no_change"}
    """
    if skill_a == skill_b:
        return {"pair": None, "rule_applied": "self_pair_ignored"}

    pair = _pair_key(skill_a, skill_b)
    data = _load_weights()
    rein = data.get("reinforcement", DEFAULT_REINFORCEMENT)

    success_threshold = rein.get("success_threshold", 85)
    failure_threshold = rein.get("failure_threshold", 50)
    inc = rein.get("success_increment", 0.05)
    dec = rein.get("failure_decrement", 0.05)
    max_w = rein.get("max_weight", 1.0)
    min_w = rein.get("min_weight", 0.1)

    affinity = data["affinity_graph"]
    if pair not in affinity:
        affinity[pair] = {
            "weight": 0.5,
            "co_activations": 0,
            "avg_combined_score": 0.0,
            "notes": note or "auto-discovered via execution",
        }

    entry = affinity[pair]
    old_weight = float(entry.get("weight", 0.5))
    old_co = int(entry.get("co_activations", 0))
    old_avg = float(entry.get("avg_combined_score", 0.0))

    new_co = old_co + 1
    combined = (score_a + score_b) / 2.0
    new_avg = ((old_avg * old_co) + combined) / new_co if new_co else combined

    rule = "no_change"
    new_weight = old_weight
    if combined >= success_threshold:
        new_weight = min(old_weight + inc, max_w)
        rule = "success_increment"
    elif combined < failure_threshold:
        new_weight = max(old_weight - dec, min_w)
        rule = "failure_decrement"

    delta = {
        "pair": pair,
        "old_weight": round(old_weight, 3),
        "new_weight": round(new_weight, 3),
        "old_co_act": old_co,
        "new_co_act": new_co,
        "combined_avg": round(combined, 1),
        "rule_applied": rule,
    }

    if simulate:
        return delta

    entry["weight"] = round(new_weight, 3)
    entry["co_activations"] = new_co
    entry["avg_combined_score"] = round(new_avg, 2)
    if note and not entry.get("notes"):
        entry["notes"] = note
    _save_weights(data)
    return delta


def _recent_companions_db(project: str, skill: str, window_hours: int) -> list:
    """Query DB for recent done tasks in same project (excluding current skill)."""
    if not DB_PATH.exists():
        return []
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cutoff = (datetime.now(UTC) - timedelta(hours=window_hours)).isoformat()
        rows = conn.execute(
            """SELECT skill, score, completed_at
               FROM tasks
               WHERE project = ? AND status = 'done' AND skill != ?
                 AND completed_at >= ?
               ORDER BY completed_at DESC
               LIMIT 20""",
            (project, skill, cutoff),
        ).fetchall()
        conn.close()
        return [{"skill": r[0], "score": r[1] or 0, "completed_at": r[2]} for r in rows if r[0]]
    except Exception:
        return []


def _recent_companions_yaml(project: str, skill: str, window_hours: int) -> list:
    """Fallback: scan tasks/done/ YAML files."""
    done_dir = ORCH_DIR / "tasks" / "done"
    if not done_dir.exists():
        return []
    cutoff = datetime.now(UTC) - timedelta(hours=window_hours)
    companions = []
    for tf in done_dir.glob("*.yaml"):
        try:
            data = _load_yaml(str(tf))
            if not data or data.get("project") != project:
                continue
            other_skill = data.get("skill")
            if not other_skill or other_skill == skill:
                continue
            completed = data.get("completed_at")
            if completed:
                try:
                    ts = datetime.fromisoformat(completed.replace("Z", "+00:00"))
                    if ts < cutoff:
                        continue
                except Exception:
                    pass
            companions.append({
                "skill": other_skill,
                "score": int(data.get("quality_score", 0) or 0),
                "completed_at": completed or "",
            })
        except Exception:
            continue
    return companions


def process_completion(task_id: str, skill: str, project: str, score: int,
                       window_hours: int = COMPANION_WINDOW_HOURS,
                       simulate: bool = False) -> list:
    """Main hook — called by executor after each task completes.

    Looks for companion tasks (same project, recent window) and updates the
    affinity weight for each (companion_skill, current_skill) pair.

    Returns list of delta dicts (one per companion processed).
    """
    if not skill or not project or score <= 0:
        return []

    companions = _recent_companions_db(project, skill, window_hours)
    if not companions:
        companions = _recent_companions_yaml(project, skill, window_hours)

    deltas = []
    seen_skills = set()
    for c in companions:
        cs = c["skill"]
        if cs in seen_skills:
            continue  # only first (most recent) instance per skill
        seen_skills.add(cs)
        if c["score"] <= 0:
            continue
        delta = update_pair(cs, skill, c["score"], score,
                            note=f"co-active in {project}",
                            simulate=simulate)
        deltas.append(delta)
    return deltas


def stats() -> dict:
    """Summary of current affinity graph state."""
    data = _load_weights()
    graph = data.get("affinity_graph", {})
    weights = [float(p.get("weight", 0.5)) for p in graph.values() if isinstance(p, dict)]
    activations = [int(p.get("co_activations", 0)) for p in graph.values() if isinstance(p, dict)]
    return {
        "total_pairs": len(graph),
        "active_pairs": sum(1 for a in activations if a > 0),
        "dormant_pairs": sum(1 for a in activations if a == 0),
        "avg_weight": round(sum(weights) / len(weights), 3) if weights else 0.0,
        "max_weight": round(max(weights), 3) if weights else 0.0,
        "min_weight": round(min(weights), 3) if weights else 0.0,
        "total_co_activations": sum(activations),
    }


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("synaptic_update")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Synaptic Weights Write-Back")
    p.add_argument("--simulate", nargs=4, metavar=("SKILL_A", "SKILL_B", "SCORE_A", "SCORE_B"),
                   help="Dry-run a pair update (no write)")
    p.add_argument("--update", nargs=4, metavar=("SKILL_A", "SKILL_B", "SCORE_A", "SCORE_B"),
                   help="Update a pair (writes)")
    p.add_argument("--task", help="Process a completed task (used by executor hook)")
    p.add_argument("--skill", help="Skill of the task")
    p.add_argument("--project", help="Project of the task")
    p.add_argument("--score", type=int, default=0, help="Score of the task")
    p.add_argument("--stats", action="store_true", help="Show graph stats")
    p.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = p.parse_args()

    if args.stats:
        s = stats()
        print(json.dumps(s, indent=2) if args.json else
              "\n".join(f"  {k}: {v}" for k, v in s.items()))
        return 0

    if args.simulate:
        a, b, sa, sb = args.simulate
        delta = update_pair(a, b, int(sa), int(sb), simulate=True)
        print(json.dumps(delta, indent=2))
        return 0

    if args.update:
        a, b, sa, sb = args.update
        delta = update_pair(a, b, int(sa), int(sb), simulate=False)
        print(json.dumps(delta, indent=2))
        return 0

    if args.task and args.skill and args.project:
        deltas = process_completion(args.task, args.skill, args.project, args.score)
        if args.json:
            print(json.dumps(deltas, indent=2))
        else:
            print(f"Processed {args.task}: {len(deltas)} pair updates")
            for d in deltas:
                print(f"  {d['pair']}: {d['old_weight']} -> {d['new_weight']} "
                      f"(co_act {d['old_co_act']}->{d['new_co_act']}, rule={d['rule_applied']})")
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
