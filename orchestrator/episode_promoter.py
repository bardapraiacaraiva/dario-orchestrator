#!/usr/bin/env python3
"""
DARIO Episode → Semantic Memory Promotion
=========================================
Upgrade 8 (Sprint 3) of the Cognitive Audit roadmap.

memory/semantic.py defines promote_from_episode() — a working function
that takes successful episodes and crystallizes them as semantic memories
(SEM-*.yaml). It was never called. The semantic layer was dormant.

The dream cycle's Reorganize phase has been writing one timestamped
observation per cycle, but never extracting transferable knowledge.

This module fixes that. It:
  1. Scans episodes (filesystem + DB tasks done in last N days)
  2. Identifies promotion candidates:
     - Score >= 90 (excellence — capture what worked)
     - 3+ episodes of same skill+project with avg score >= 85 (proven pattern)
     - Episodes flagged with `promote: true` in tags
  3. Clusters by skill+project to avoid duplicate semantic entries
  4. Promotes via memory.semantic.promote_from_episode()
  5. Optionally generates a brief rule snippet:
     "skill X on project Y produces high-quality output when … " — saved to
     evolution/rules/auto-rule-{slug}.yaml

CLI:
    python episode_promoter.py --scan              Show candidates (dry-run)
    python episode_promoter.py --promote           Apply promotions
    python episode_promoter.py --auto-rule         Generate rules from clusters
    python episode_promoter.py --stats             Promotion + rule counts
    python episode_promoter.py --days 14           Limit lookback window
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True

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
EPISODES_DIR = ORCH_DIR / "memory" / "episodes"
SEMANTIC_DIR = ORCH_DIR / "memory" / "semantic"
RULES_DIR = ORCH_DIR / "evolution" / "rules"

# Promotion thresholds
EXCELLENCE_SCORE = 90       # single-episode excellence → promote
PATTERN_MIN_EPISODES = 3    # how many to form a "proven pattern"
PATTERN_MIN_AVG_SCORE = 85
DEFAULT_LOOKBACK_DAYS = 30


def _load_episodes(days: int = DEFAULT_LOOKBACK_DAYS) -> list:
    """Walk episodes/ filesystem and return list of dicts (Pydantic-free for portability)."""
    if not EPISODES_DIR.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    for day_dir in sorted(EPISODES_DIR.iterdir()):
        if not day_dir.is_dir():
            continue
        # Parse day from dir name "YYYY-MM-DD"
        try:
            d = datetime.fromisoformat(day_dir.name).replace(tzinfo=timezone.utc)
            if d < cutoff:
                continue
        except Exception:
            pass
        for ep_file in day_dir.glob("EP-*.yaml"):
            try:
                data = _load_yaml(str(ep_file))
                if not isinstance(data, dict):
                    continue
                data["_file"] = str(ep_file)
                out.append(data)
            except Exception:
                continue
    return out


def _classify(episodes: list) -> dict:
    """Group episodes into clusters and identify promotion candidates.

    Returns dict:
        {
          "excellence": [episode...],                   # single-shot >= 90
          "clusters": {(skill, project): [episode...]}, # patterns
          "tagged": [episode...],                       # explicit promote tag
        }
    """
    excellence = []
    tagged = []
    clusters = defaultdict(list)

    for ep in episodes:
        score = ep.get("score")
        outcome = ep.get("outcome")
        skill = ep.get("skill") or ""
        project = ep.get("project") or ""

        if outcome != "success" or not skill:
            continue

        if isinstance(score, int) and score >= EXCELLENCE_SCORE:
            excellence.append(ep)

        if "promote" in (ep.get("tags") or []):
            tagged.append(ep)

        # Always add to cluster (whether or not excellent) for pattern detection
        clusters[(skill, project)].append(ep)

    return {
        "excellence": excellence,
        "clusters": dict(clusters),
        "tagged": tagged,
    }


def _candidate_patterns(clusters: dict) -> list:
    """Return clusters that meet pattern-promotion threshold."""
    patterns = []
    for (skill, project), eps in clusters.items():
        if len(eps) < PATTERN_MIN_EPISODES:
            continue
        scores = [e.get("score") for e in eps if isinstance(e.get("score"), int)]
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        if avg >= PATTERN_MIN_AVG_SCORE:
            patterns.append({
                "skill": skill,
                "project": project,
                "episodes": eps,
                "count": len(eps),
                "avg_score": round(avg, 1),
                "min_score": min(scores),
                "max_score": max(scores),
            })
    return patterns


def _existing_semantic_names() -> set:
    """Collect already-promoted memory names so we don't duplicate."""
    if not SEMANTIC_DIR.exists():
        return set()
    names = set()
    for f in SEMANTIC_DIR.glob("SEM-*.yaml"):
        try:
            data = _load_yaml(str(f))
            if isinstance(data, dict) and data.get("name"):
                names.add(data["name"])
        except Exception:
            continue
    return names


def _build_excellence_content(ep: dict) -> tuple:
    """For a single excellent episode, build (name, content) for promotion."""
    skill = ep.get("skill", "unknown-skill")
    project = ep.get("project", "global")
    summary = ep.get("output_summary", "")[:800]
    tags = ", ".join(ep.get("tags") or [])
    name = f"{skill}__{project}__excellence"
    content = (
        f"High-quality output ({ep.get('score')}/100) from skill `{skill}` "
        f"on project `{project}`.\n\n"
        f"Episode: {ep.get('episode_id')}\n"
        f"Tags: {tags}\n\n"
        f"What worked:\n{summary}"
    )
    return name, content


def _build_pattern_content(pattern: dict) -> tuple:
    """For a proven pattern cluster, build (name, content) for promotion."""
    skill = pattern["skill"]
    project = pattern["project"] or "cross-project"
    name = f"{skill}__{project}__pattern"
    examples = []
    for ep in pattern["episodes"][:5]:
        score = ep.get("score", "?")
        summary = (ep.get("output_summary") or "")[:200]
        examples.append(f"- {ep.get('episode_id')} (score {score}): {summary}")
    examples_text = "\n".join(examples)
    content = (
        f"Proven pattern: `{skill}` on project `{project}` "
        f"({pattern['count']} episodes, avg score {pattern['avg_score']}, "
        f"range {pattern['min_score']}-{pattern['max_score']}).\n\n"
        f"Recent episodes:\n{examples_text}\n\n"
        f"Recommendation: when dispatching tasks matching this skill+project, "
        f"this combination has reliably produced high-quality outputs. "
        f"Use as positive prior in dispatch decisions."
    )
    return name, content


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "rule"


def _write_rule(slug: str, rule: dict) -> Path:
    """Write a YAML rule file under evolution/rules/."""
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    path = RULES_DIR / f"auto-rule-{slug}.yaml"
    rule["generated_at"] = datetime.now(timezone.utc).isoformat()
    rule["source"] = "episode_promoter"
    _dump_yaml(rule, str(path))
    return path


def scan(days: int = DEFAULT_LOOKBACK_DAYS) -> dict:
    """Dry-run scan — return what WOULD be promoted."""
    episodes = _load_episodes(days)
    classified = _classify(episodes)
    patterns = _candidate_patterns(classified["clusters"])
    existing = _existing_semantic_names()

    excellence_names = [_build_excellence_content(ep)[0]
                        for ep in classified["excellence"]]
    pattern_names = [_build_pattern_content(p)[0] for p in patterns]

    new_excellence = [n for n in excellence_names if n not in existing]
    new_patterns = [n for n in pattern_names if n not in existing]

    return {
        "total_episodes_scanned": len(episodes),
        "excellence_candidates": len(classified["excellence"]),
        "pattern_candidates": len(patterns),
        "already_promoted": len(existing),
        "would_promote_excellence": new_excellence,
        "would_promote_patterns": new_patterns,
        "lookback_days": days,
    }


def promote(days: int = DEFAULT_LOOKBACK_DAYS, generate_rules: bool = False,
            verbose: bool = False) -> dict:
    """Apply promotions. Returns stats."""
    # Lazy import — only when we actually persist
    sys.path.insert(0, str(ORCH_DIR))
    try:
        from memory.semantic import promote_from_episode
    except Exception as e:
        return {"error": f"memory.semantic unavailable: {e}"}

    episodes = _load_episodes(days)
    classified = _classify(episodes)
    patterns = _candidate_patterns(classified["clusters"])
    existing = _existing_semantic_names()

    promoted_excellence = []
    promoted_patterns = []
    rules_written = []

    # Excellence promotions (one per excellent episode)
    seen_excellence = set()  # avoid duplicate per skill+project from many high-scorers
    for ep in classified["excellence"]:
        name, content = _build_excellence_content(ep)
        if name in existing or name in seen_excellence:
            continue
        seen_excellence.add(name)
        try:
            mem = promote_from_episode(
                name=name,
                content=content,
                source_episode_ids=[ep.get("episode_id")],
                type_="excellence",
                confidence=0.85,
            )
            promoted_excellence.append({"name": name, "memory_id": mem.memory_id})
            if verbose:
                print(f"  +excellence {name}")
        except Exception as e:
            if verbose:
                print(f"  ! fail {name}: {e}")

    # Pattern promotions (clustered)
    for pattern in patterns:
        name, content = _build_pattern_content(pattern)
        if name in existing:
            continue
        try:
            ep_ids = [e.get("episode_id") for e in pattern["episodes"]
                      if e.get("episode_id")]
            mem = promote_from_episode(
                name=name,
                content=content,
                source_episode_ids=ep_ids,
                type_="pattern",
                confidence=min(0.95, 0.6 + (pattern["avg_score"] - 70) / 100),
            )
            promoted_patterns.append({
                "name": name,
                "memory_id": mem.memory_id,
                "count": pattern["count"],
                "avg_score": pattern["avg_score"],
            })
            if verbose:
                print(f"  +pattern {name} ({pattern['count']} eps, avg {pattern['avg_score']})")

            # Auto-rule generation
            if generate_rules:
                rule = {
                    "rule_id": f"auto-rule-{_slug(name)}",
                    "type": "dispatch_prior",
                    "skill": pattern["skill"],
                    "project": pattern["project"] or "*",
                    "rationale": (
                        f"{pattern['count']} consecutive successful executions of "
                        f"`{pattern['skill']}` on `{pattern['project']}` "
                        f"(avg {pattern['avg_score']}/100). Suggest as positive prior."
                    ),
                    "boost": round(min(0.20, (pattern["avg_score"] - 80) / 100), 3),
                    "source_episodes": ep_ids,
                    "from_memory": mem.memory_id,
                }
                path = _write_rule(_slug(name), rule)
                rules_written.append(str(path))
                if verbose:
                    print(f"    rule: {path}")
        except Exception as e:
            if verbose:
                print(f"  ! pattern fail {name}: {e}")

    return {
        "promoted_excellence": len(promoted_excellence),
        "promoted_patterns": len(promoted_patterns),
        "rules_written": len(rules_written),
        "rule_files": rules_written,
        "excellence_names": [p["name"] for p in promoted_excellence],
        "pattern_names": [p["name"] for p in promoted_patterns],
    }


def stats() -> dict:
    """Summary of semantic + rules state."""
    semantic_count = 0
    by_type = defaultdict(int)
    if SEMANTIC_DIR.exists():
        for f in SEMANTIC_DIR.glob("SEM-*.yaml"):
            try:
                data = _load_yaml(str(f))
                if isinstance(data, dict):
                    semantic_count += 1
                    by_type[data.get("type", "unknown")] += 1
            except Exception:
                continue

    rules_count = 0
    if RULES_DIR.exists():
        rules_count = sum(1 for _ in RULES_DIR.glob("auto-rule-*.yaml"))

    return {
        "semantic_memories": semantic_count,
        "by_type": dict(by_type),
        "auto_rules": rules_count,
    }


def main():
    p = argparse.ArgumentParser(description="DARIO Episode → Semantic Promotion")
    p.add_argument("--scan", action="store_true", help="Dry-run (show candidates)")
    p.add_argument("--promote", action="store_true", help="Apply promotions")
    p.add_argument("--auto-rule", action="store_true", help="Generate rules with promotions")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--days", type=int, default=DEFAULT_LOOKBACK_DAYS)
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.stats:
        s = stats()
        print(json.dumps(s, indent=2) if args.json
              else "\n".join(f"  {k}: {v}" for k, v in s.items()))
        return 0

    if args.scan:
        r = scan(days=args.days)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.json
              else "\n".join([
                  f"Scanned {r['total_episodes_scanned']} episodes (last {r['lookback_days']}d)",
                  f"  Excellence candidates: {r['excellence_candidates']}",
                  f"  Pattern candidates:    {r['pattern_candidates']}",
                  f"  Already promoted:      {r['already_promoted']}",
                  f"  Would promote (new excellence): {len(r['would_promote_excellence'])}",
                  f"  Would promote (new patterns):   {len(r['would_promote_patterns'])}",
              ]))
        return 0

    if args.promote:
        r = promote(days=args.days, generate_rules=args.auto_rule, verbose=args.verbose)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.json
              else "\n".join([
                  f"Promoted excellence: {r.get('promoted_excellence', 0)}",
                  f"Promoted patterns:   {r.get('promoted_patterns', 0)}",
                  f"Rules written:       {r.get('rules_written', 0)}",
              ]))
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
