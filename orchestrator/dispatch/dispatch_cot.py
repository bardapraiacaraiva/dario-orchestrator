#!/usr/bin/env python3
"""
DARIO Dispatch Chain-of-Thought
===============================
Upgrade 9 (Sprint 4) of the Cognitive Audit roadmap.

Today's dispatch pattern-matches and acts. Even with Sprints 1-3 wired,
the orchestrator picks the first signal that hits and never inspects
WHY. There's no record of "this skill was picked because semantic
returned 0.71, keyword backed it up, Q-memory had 3 prior wins."

This module makes dispatch DELIBERATIVE rather than REACTIVE:

  1. Gather all 4 signals (explicit / semantic / keyword / Q-value)
     including their numeric scores and alternatives.
  2. Synthesise a structured reasoning trace.
  3. Choose the winner with explicit rationale.
  4. Persist the trace to dispatch_cot/{task_id}.yaml so failures can
     be post-mortemed: "which signal was wrong, why did we trust it?"

Zero LLM calls — runs deterministically against signal data already
produced by the prior upgrades. Cheap, transparent, auditable.

CLI:
    python dispatch_cot.py --reason "criar marca completa para restaurante"
    python dispatch_cot.py --task TASK-001   # CoT for a specific task
    python dispatch_cot.py --postmortem TASK-001 --actual-score 45
    python dispatch_cot.py --stats           # how often each signal wins
"""

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True

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
            _pyaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
COT_DIR = ORCH_DIR / "dispatch_cot"
DB_PATH = ORCH_DIR / "orchestrator.db"
RULES_DIR = ORCH_DIR / "evolution" / "rules"

# Signal weights — used when multiple signals agree, to score the winner
SIGNAL_WEIGHTS = {
    "explicit": 1.0,    # task already declared skill — strongest
    "semantic": 0.70,   # embedding-based, generally reliable
    "qvalue": 0.65,     # past experience, depends on sample size
    "keyword": 0.50,    # legacy fallback, brittle but specific
    "auto_rule": 0.20,  # additive boost from generated rules
}

# Disagreement penalty — when signals point to DIFFERENT skills
DISAGREEMENT_PENALTY = 0.15

# Minimum confidence to be considered "high-confidence" dispatch
HIGH_CONF_THRESHOLD = 0.75
LOW_CONF_THRESHOLD = 0.45


def _ensure_dir():
    COT_DIR.mkdir(parents=True, exist_ok=True)


def _gather_signals(task: dict) -> dict:
    """Run all 4 dispatch signals and capture raw outputs."""
    sys.path.insert(0, str(ORCH_DIR))

    signals = {
        "explicit": None,
        "semantic": None,
        "keyword": None,
        "qvalue": None,
        "auto_rules": [],
    }

    # Signal 1: explicit
    if task.get("skill"):
        signals["explicit"] = {
            "skill": task["skill"],
            "score": 1.0,
            "note": "task.skill set explicitly",
        }

    # Signal 2: semantic
    try:
        from dispatch.semantic_dispatch import semantic_match
        text = f"{task.get('title', '')} {task.get('description', '')}".strip()
        if text:
            top_matches = semantic_match(text, top_k=3)
            if top_matches:
                signals["semantic"] = {
                    "skill": top_matches[0][0],
                    "score": round(top_matches[0][1], 3),
                    "alternatives": [
                        {"skill": s, "score": round(sc, 3)}
                        for s, sc in top_matches[1:3]
                    ],
                }
    except Exception as e:
        signals["semantic_error"] = str(e)

    # Signal 3: keyword
    try:
        from dispatch.dispatch_engine import KEYWORD_SKILL_MAP
        text = f"{task.get('title', '')} {task.get('description', '')}".lower()
        scored = {}
        for kw, skill in KEYWORD_SKILL_MAP.items():
            if kw in text:
                scored[skill] = scored.get(skill, 0) + len(kw)
        if scored:
            best = max(scored, key=scored.get)
            total = sum(scored.values())
            signals["keyword"] = {
                "skill": best,
                "score": round(scored[best] / total, 3) if total else 0.0,
                "raw_strength": scored[best],
                "alternatives": [
                    {"skill": s, "score": round(v / total, 3)}
                    for s, v in sorted(scored.items(), key=lambda x: -x[1])[1:3]
                ],
            }
    except Exception as e:
        signals["keyword_error"] = str(e)

    # Signal 4: Q-value memory
    try:
        from cognitive.qvalue_memory_wire import suggest_skill
        text = f"{task.get('title', '')} {task.get('description', '')}".strip()
        if text:
            suggestions = suggest_skill(text, project=task.get("project"), top_k=3)
            if suggestions:
                top = suggestions[0]
                signals["qvalue"] = {
                    "skill": top["skill"],
                    "score": round(top["q_value"], 3),
                    "visits": top.get("visits", 0),
                    "avg_score": top.get("avg_score", 0),
                    "alternatives": [
                        {"skill": s["skill"], "score": round(s["q_value"], 3)}
                        for s in suggestions[1:3]
                    ],
                }
    except Exception as e:
        signals["qvalue_error"] = str(e)

    # Auto-rules (Upgrade 8) — additive boosts
    try:
        if RULES_DIR.exists():
            for rf in RULES_DIR.glob("auto-rule-*.yaml"):
                rule = _load_yaml(str(rf))
                if not isinstance(rule, dict):
                    continue
                if rule.get("type") != "dispatch_prior":
                    continue
                rule_project = rule.get("project", "*")
                task_project = task.get("project", "")
                if rule_project not in ("*", "", task_project):
                    continue
                signals["auto_rules"].append({
                    "skill": rule.get("skill"),
                    "boost": float(rule.get("boost", 0)),
                    "rule_id": rule.get("rule_id"),
                })
    except Exception:
        pass

    return signals


def _synthesise(signals: dict) -> dict:
    """Combine signals into a final decision with rationale."""
    # Tally votes per skill
    votes = {}  # skill -> {sources: [...], score: float, conflicts: []}

    for source, weight in SIGNAL_WEIGHTS.items():
        if source == "auto_rule":
            continue  # handled separately
        sig = signals.get(source)
        if not sig or not isinstance(sig, dict):
            continue
        skill = sig.get("skill")
        if not skill:
            continue
        raw = float(sig.get("score", 0.5))
        contribution = weight * raw
        if skill not in votes:
            votes[skill] = {"sources": [], "score": 0.0, "details": {}}
        votes[skill]["sources"].append(source)
        votes[skill]["score"] += contribution
        votes[skill]["details"][source] = round(raw, 3)

    # Apply auto-rule boosts
    for rule in signals.get("auto_rules", []):
        skill = rule.get("skill")
        boost = rule.get("boost", 0)
        if not skill or skill not in votes:
            continue  # don't introduce skills not already in vote
        votes[skill]["score"] += boost
        votes[skill]["details"]["auto_rule_boost"] = boost

    if not votes:
        return {
            "winner": None,
            "confidence": 0.0,
            "level": "NONE",
            "rationale": "no signal returned a skill; dispatch will queue or escalate",
            "votes": {},
            "agreement": "no_signal",
        }

    # Sort by combined score
    sorted_votes = sorted(votes.items(), key=lambda x: -x[1]["score"])
    winner_skill, winner_data = sorted_votes[0]
    confidence = winner_data["score"]

    # Agreement analysis
    skills_chosen = set(votes.keys())
    if len(skills_chosen) == 1:
        agreement = "unanimous"
    elif winner_skill in {s.get("skill") for s in [signals.get(k) for k in ("semantic", "qvalue", "keyword")] if isinstance(s, dict)}:
        # Check how many signals point to winner
        pointing_to_winner = sum(
            1 for k in ("explicit", "semantic", "keyword", "qvalue")
            if isinstance(signals.get(k), dict) and signals[k].get("skill") == winner_skill
        )
        total_active = sum(
            1 for k in ("explicit", "semantic", "keyword", "qvalue")
            if isinstance(signals.get(k), dict)
        )
        agreement = f"{pointing_to_winner}/{total_active}_signals"
        # Apply disagreement penalty
        if total_active > 1 and pointing_to_winner < total_active:
            confidence -= DISAGREEMENT_PENALTY * (total_active - pointing_to_winner)
    else:
        agreement = "split"
        confidence -= DISAGREEMENT_PENALTY

    confidence = round(max(0.0, min(1.0, confidence)), 3)
    if confidence >= HIGH_CONF_THRESHOLD:
        level = "HIGH"
    elif confidence >= LOW_CONF_THRESHOLD:
        level = "MEDIUM"
    else:
        level = "LOW"

    # Build human-readable rationale
    src_summary = ", ".join(winner_data["sources"])
    detail_parts = [f"{k}={v}" for k, v in winner_data["details"].items()]
    rationale = (
        f"Picked '{winner_skill}' (confidence {confidence}, {level}). "
        f"Backed by: {src_summary}. Signals: {', '.join(detail_parts)}. "
        f"Agreement: {agreement}."
    )

    # Surface alternatives (skills that got non-zero votes but didn't win)
    alternatives = [
        {"skill": s, "score": round(d["score"], 3), "sources": d["sources"]}
        for s, d in sorted_votes[1:4]
    ]

    return {
        "winner": winner_skill,
        "confidence": confidence,
        "level": level,
        "rationale": rationale,
        "votes": {s: {"score": round(d["score"], 3),
                      "sources": d["sources"],
                      "details": d["details"]} for s, d in votes.items()},
        "alternatives": alternatives,
        "agreement": agreement,
    }


def reason(task: dict, persist: bool = True) -> dict:
    """Run the full deliberative reasoning step.

    Returns the CoT trace; optionally persists it under dispatch_cot/.
    """
    _ensure_dir()
    signals = _gather_signals(task)
    decision = _synthesise(signals)
    trace = {
        "timestamp": datetime.now(UTC).isoformat(),
        "task_id": task.get("id") or task.get("task_id"),
        "task_title": task.get("title", "")[:200],
        "task_project": task.get("project"),
        "signals": signals,
        "decision": decision,
    }
    if persist and trace["task_id"]:
        path = COT_DIR / f"{trace['task_id']}.yaml"
        _dump_yaml(trace, str(path))
    return trace


def postmortem(task_id: str, actual_score: int, actual_outcome: str = "unknown") -> dict:
    """After a task completes, evaluate the original CoT trace against reality.

    Identifies which signal was right/wrong, updates a learning summary, and
    flags the trace as 'mortem_complete'.
    """
    _ensure_dir()
    path = COT_DIR / f"{task_id}.yaml"
    if not path.exists():
        return {"status": "no_trace", "task_id": task_id}

    trace = _load_yaml(str(path))
    if not isinstance(trace, dict):
        return {"status": "invalid_trace", "task_id": task_id}

    signals = trace.get("signals", {})
    decision = trace.get("decision", {})
    winner = decision.get("winner")

    # Was the actual outcome consistent with high confidence?
    confidence = decision.get("confidence", 0)
    level = decision.get("level", "UNKNOWN")
    bad_outcome = actual_score < 60 or actual_outcome in ("failure", "revision")

    verdict = "UNKNOWN"
    if not bad_outcome:
        verdict = "VINDICATED"
    elif level == "HIGH" and bad_outcome:
        verdict = "OVERCONFIDENT"  # we were sure, we were wrong
    elif level == "LOW" and bad_outcome:
        verdict = "CONFIRMED_DOUBT"  # we already weren't sure
    elif level == "MEDIUM" and bad_outcome:
        verdict = "MARGINAL_MISS"

    # Which signal can we 'blame' or 'credit'?
    signal_blame = []
    for src in ("explicit", "semantic", "keyword", "qvalue"):
        s = signals.get(src)
        if isinstance(s, dict) and s.get("skill") == winner:
            signal_blame.append(src)

    learning = {
        "task_id": task_id,
        "verdict": verdict,
        "confidence_called": level,
        "confidence_score": confidence,
        "actual_score": actual_score,
        "actual_outcome": actual_outcome,
        "signals_that_chose_winner": signal_blame,
        "rationale_was": decision.get("rationale"),
    }

    trace["postmortem"] = learning
    trace["postmortem_at"] = datetime.now(UTC).isoformat()
    _dump_yaml(trace, str(path))
    return {"status": "complete", **learning}


def stats() -> dict:
    """Aggregate stats across persisted CoT traces."""
    _ensure_dir()
    total = 0
    by_level = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "NONE": 0}
    by_winner_source = {"explicit": 0, "semantic": 0, "keyword": 0, "qvalue": 0, "no_winner": 0}
    postmortems = {"VINDICATED": 0, "OVERCONFIDENT": 0, "CONFIRMED_DOUBT": 0,
                   "MARGINAL_MISS": 0, "UNKNOWN": 0}

    for tf in COT_DIR.glob("*.yaml"):
        try:
            trace = _load_yaml(str(tf))
            if not isinstance(trace, dict):
                continue
            total += 1
            level = trace.get("decision", {}).get("level", "NONE")
            by_level[level] = by_level.get(level, 0) + 1

            winner = trace.get("decision", {}).get("winner")
            if not winner:
                by_winner_source["no_winner"] += 1
            else:
                signals = trace.get("signals", {})
                # Find the first source that matches winner
                for src in ("explicit", "semantic", "qvalue", "keyword"):
                    s = signals.get(src)
                    if isinstance(s, dict) and s.get("skill") == winner:
                        by_winner_source[src] += 1
                        break

            pm = trace.get("postmortem")
            if isinstance(pm, dict):
                v = pm.get("verdict", "UNKNOWN")
                postmortems[v] = postmortems.get(v, 0) + 1
        except Exception:
            continue

    return {
        "total_traces": total,
        "by_confidence_level": by_level,
        "by_winning_signal": by_winner_source,
        "postmortems": postmortems,
        "overconfidence_rate": round(
            postmortems["OVERCONFIDENT"] / max(sum(postmortems.values()), 1), 3
        ),
    }


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("dispatch_cot")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Dispatch Chain-of-Thought")
    p.add_argument("--reason", help="Task title/text to reason about (ad-hoc)")
    p.add_argument("--description", default="", help="Optional description for --reason")
    p.add_argument("--project", help="Project context for --reason")
    p.add_argument("--task", help="Task ID (loads from YAML)")
    p.add_argument("--postmortem", help="Run post-mortem on a task")
    p.add_argument("--actual-score", type=int, help="Actual score for postmortem")
    p.add_argument("--actual-outcome", default="unknown",
                   help="Actual outcome for postmortem: success | failure | revision")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.stats:
        s = stats()
        print(json.dumps(s, indent=2) if args.json
              else "\n".join(f"  {k}: {v}" for k, v in s.items()))
        return 0

    if args.postmortem:
        if args.actual_score is None:
            print("--postmortem requires --actual-score", file=sys.stderr)
            return 1
        r = postmortem(args.postmortem, args.actual_score, args.actual_outcome)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.json
              else "\n".join(f"  {k}: {v}" for k, v in r.items()))
        return 0

    if args.reason:
        task = {"title": args.reason, "description": args.description, "project": args.project}
        trace = reason(task, persist=False)
        if args.json:
            print(json.dumps(trace, indent=2, ensure_ascii=False))
        else:
            d = trace["decision"]
            print(f"Winner:     {d['winner']}")
            print(f"Confidence: {d['confidence']} ({d['level']})")
            print(f"Agreement:  {d['agreement']}")
            print(f"Rationale:  {d['rationale']}")
            if d.get("alternatives"):
                print("Alternatives:")
                for a in d["alternatives"]:
                    print(f"  {a['skill']:30s} score={a['score']}  via {a['sources']}")
        return 0

    if args.task:
        task_file = ORCH_DIR / "tasks" / "active" / f"{args.task}.yaml"
        if not task_file.exists():
            print(f"Task {args.task} not found", file=sys.stderr)
            return 1
        task = _load_yaml(str(task_file))
        trace = reason(task, persist=True)
        if args.json:
            print(json.dumps(trace, indent=2, ensure_ascii=False))
        else:
            print(f"CoT trace persisted to {COT_DIR / (args.task + '.yaml')}")
            print(f"Winner: {trace['decision']['winner']} "
                  f"({trace['decision']['level']} conf {trace['decision']['confidence']})")
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
