#!/usr/bin/env python3
"""Skill Usage Audit — honest inventory of which skills are actually used.

Scans:
  - memory/episodes/*/EP-*.yaml      (real dispatch history)
  - quality/skill-metrics.yaml        (scoring history)
  - quality/polished_production_runs.yaml (Padrão A polished invocations)
  - quality/api_spend_log.jsonl       (anthropic API spend)
  - audit/*.yaml                      (mutation log)

Outputs:
  - quality/skill_usage_audit.yaml    structured per-skill usage
  - stdout: tiered inventory (A/B/C/Experimental/Unused) + summary

Tier rules:
  A — invoked >= 10 times, scored >= 70 avg, last invocation <= 30d ago
  B — invoked >= 5 times, scored >= 60 avg
  C — invoked >= 1 time
  Experimental — has SKILL.md but never invoked, age >= 30d
  Unused — has SKILL.md but never invoked
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

HOME = Path.home()
ORCH = HOME / ".claude" / "orchestrator"
SKILLS = HOME / ".claude" / "skills"
EPISODES = ORCH / "memory" / "episodes"
QUALITY = ORCH / "quality"
AUDIT = ORCH / "audit"

NOW = datetime.now(UTC)
THIRTY_D_AGO = NOW - timedelta(days=30)


def load_skill_inventory() -> dict[str, dict]:
    """Walk skills/*/SKILL.md and capture name + first-seen-on-disk mtime."""
    inv = {}
    for d in sorted(SKILLS.iterdir()):
        if not d.is_dir():
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            continue
        # First line of SKILL.md often has the description
        head = ""
        try:
            head = skill_md.read_text(encoding="utf-8", errors="ignore").splitlines()[0][:120]
        except Exception:
            pass
        inv[d.name] = {
            "name": d.name,
            "skill_md_size": skill_md.stat().st_size,
            "skill_md_mtime": datetime.fromtimestamp(skill_md.stat().st_mtime, UTC).isoformat(),
            "first_line": head,
            "invocations": 0,
            "scores": [],
            "last_invoked": None,
            "polished_invocations": 0,
            "api_spend_usd": 0.0,
        }
    return inv


def scan_episodes(inv: dict[str, dict]) -> None:
    """Count episodes per skill."""
    if not EPISODES.exists():
        return
    for ep_file in EPISODES.rglob("*.yaml"):
        try:
            ep = yaml.safe_load(ep_file.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        skill = ep.get("skill")
        if not skill or skill not in inv:
            continue
        inv[skill]["invocations"] += 1
        ts = ep.get("timestamp")
        if ts:
            inv[skill]["last_invoked"] = max(
                inv[skill]["last_invoked"] or ts, ts
            )


def scan_skill_metrics(inv: dict[str, dict]) -> None:
    """Pull scoring history from quality/skill-metrics.yaml."""
    metrics_file = QUALITY / "skill-metrics.yaml"
    if not metrics_file.exists():
        return
    try:
        data = yaml.safe_load(metrics_file.read_text(encoding="utf-8")) or {}
    except Exception:
        return

    # skill-metrics.yaml has multiple top-level dicts — bundles, skills, ...
    for top_key in ("skills", "bundles"):
        nested = data.get(top_key, {}) or {}
        for skill_name, payload in nested.items():
            if skill_name not in inv:
                continue
            # Polished wrappers have "polished" sibling — capture scores
            scores = payload.get("scores", []) or []
            for s in scores:
                if isinstance(s, dict) and "score" in s:
                    inv[skill_name]["scores"].append(s["score"])


def scan_polished_runs(inv: dict[str, dict]) -> None:
    """Count Padrão A polished invocations."""
    runs_file = QUALITY / "polished_production_runs.yaml"
    if not runs_file.exists():
        return
    try:
        data = yaml.safe_load(runs_file.read_text(encoding="utf-8")) or {}
    except Exception:
        return
    runs = data.get("runs", []) if isinstance(data, dict) else []
    for run in runs:
        skill = run.get("skill", "")
        # Map "dario-pitch-polished" → "dario-pitch" so both surfaces credit
        if skill in inv:
            inv[skill]["polished_invocations"] += 1
        # Also credit the base skill
        base = skill.replace("-polished", "")
        if base in inv and base != skill:
            inv[base]["polished_invocations"] += 1


def scan_api_spend(inv: dict[str, dict]) -> None:
    """Sum API spend tagged with skill caller."""
    spend_file = QUALITY / "api_spend_log.jsonl"
    if not spend_file.exists():
        return
    for line in spend_file.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except Exception:
            continue
        caller = entry.get("caller", "")
        # Caller is often "dspy/compile_sprint4" or "skill-name/short"
        for skill_name in inv:
            if caller.startswith(skill_name) or skill_name in caller:
                inv[skill_name]["api_spend_usd"] += float(entry.get("cost_usd", 0) or 0)


def classify_tier(s: dict) -> str:
    """Apply tier rules."""
    invs = s["invocations"] + s["polished_invocations"]
    scores = s["scores"]
    avg = sum(scores) / len(scores) if scores else 0
    last = s["last_invoked"]

    if invs >= 10 and avg >= 70 and last and last >= THIRTY_D_AGO.isoformat():
        return "A"
    if invs >= 5 and avg >= 60:
        return "B"
    if invs >= 1:
        return "C"
    # Never invoked — distinguish experimental (old, never used) vs new
    if s["skill_md_mtime"] < THIRTY_D_AGO.isoformat():
        return "Experimental"
    return "Unused"


def main():
    print("Loading skill inventory...", flush=True)
    inv = load_skill_inventory()
    print(f"  {len(inv)} skills with SKILL.md")

    print("Scanning episode history...", flush=True)
    scan_episodes(inv)

    print("Scanning skill-metrics...", flush=True)
    scan_skill_metrics(inv)

    print("Scanning polished production runs...", flush=True)
    scan_polished_runs(inv)

    print("Scanning API spend log...", flush=True)
    scan_api_spend(inv)

    # Classify
    tiers = defaultdict(list)
    for skill_name, s in inv.items():
        s["tier"] = classify_tier(s)
        tiers[s["tier"]].append(skill_name)

    # Save structured output
    output_file = QUALITY / "skill_usage_audit.yaml"
    out = {
        "generated_at": NOW.isoformat(),
        "total_skills": len(inv),
        "tier_counts": {t: len(ss) for t, ss in sorted(tiers.items())},
        "tier_a": sorted(tiers["A"]),
        "tier_b": sorted(tiers["B"]),
        "tier_c": sorted(tiers["C"]),
        "experimental": sorted(tiers["Experimental"]),
        "unused": sorted(tiers["Unused"]),
        "per_skill": {k: {
            "tier": v["tier"],
            "invocations": v["invocations"],
            "polished_invocations": v["polished_invocations"],
            "avg_score": round(sum(v["scores"]) / len(v["scores"]), 1) if v["scores"] else None,
            "last_invoked": v["last_invoked"],
            "api_spend_usd": round(v["api_spend_usd"], 4),
        } for k, v in sorted(inv.items())},
    }
    output_file.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # Print summary
    print("\n" + "═" * 60)
    print("SKILL USAGE AUDIT — Tier Distribution")
    print("═" * 60)
    print(f"{'Tier':<14} {'Count':>6} {'% of total':>12}  Examples")
    total = len(inv)
    for tier in ["A", "B", "C", "Experimental", "Unused"]:
        n = len(tiers[tier])
        pct = (n / total * 100) if total else 0
        examples = ", ".join(tiers[tier][:3])
        if len(tiers[tier]) > 3:
            examples += f", +{len(tiers[tier]) - 3} more"
        print(f"{tier:<14} {n:>6} {pct:>11.1f}%  {examples}")

    print(f"\nTotal skills: {total}")
    print(f"Output: {output_file}")
    print(f"\nKILL CANDIDATES: Unused ({len(tiers['Unused'])}) + Experimental ({len(tiers['Experimental'])}) = {len(tiers['Unused']) + len(tiers['Experimental'])} ({(len(tiers['Unused']) + len(tiers['Experimental'])) / total * 100:.0f}% of inventory)")


if __name__ == "__main__":
    main()
