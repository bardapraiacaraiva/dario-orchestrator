#!/usr/bin/env python3
"""
DARIO Prompt Hints — Drilldown-Derived Skill Calibration
=========================================================
Upgrade 17 (operational complement to U16 eval_drilldown).

When a skill drifts on multiple eval cases, U16 surfaces what's missing
each time. But the next invocation of that skill doesn't know about
those misses — context_injector pulls receives/produces from chains but
not "you usually forget X" lessons.

This module closes that loop:

  1. Aggregates drilldown patterns per skill (missing sections, lost tokens)
  2. When a pattern reaches threshold (>= 3 occurrences across separate evals
     or runs), promotes it to a "hint"
  3. Persists hints to prompt_hints/{skill}.yaml
  4. context_injector.get_skill_hints() reads these and prepends them to
     skill prompts on next invocation

Result: skills self-correct based on observed regressions without manual
prompt engineering.

CLI:
    python prompt_hints.py --analyse                  Scan drilldowns, extract patterns
    python prompt_hints.py --promote                  Apply: write hints to disk
    python prompt_hints.py --list                     Show captured hints
    python prompt_hints.py --get SKILL                Render hints for one skill
    python prompt_hints.py --clear SKILL              Reset hints for a skill
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
HINTS_DIR = ORCH_DIR / "prompt_hints"
EVALS_DIR = ORCH_DIR / "evals"

sys.path.insert(0, str(ORCH_DIR))

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


# Promotion thresholds
MIN_OCCURRENCES_SECTION = 2  # missing section needs >= 2 sightings
MIN_OCCURRENCES_TOKEN = 3    # lost token needs >= 3 sightings (more noisy)
MAX_HINTS_PER_SKILL = 6      # cap hint list to avoid prompt bloat


def _ensure_dirs():
    HINTS_DIR.mkdir(parents=True, exist_ok=True)


def _load_eval_skill_map() -> dict:
    """Map eval_id -> skill from eval_suite.EVAL_CASES."""
    try:
        from eval_suite import EVAL_CASES
        return {c["id"]: c.get("skill") for c in EVAL_CASES}
    except Exception:
        return {}


def _drilldown_runs_dir() -> Path:
    """evals/last_runs/ where regression_check writes candidate outputs."""
    return EVALS_DIR / "last_runs"


def _collect_drilldown_patterns() -> dict:
    """For each (skill, eval_id), run drilldown if a candidate output exists,
    and collect missing-section + lost-token frequencies.

    Returns:
        {skill: {
            "sections": Counter(),
            "tokens": Counter(),
            "evals_observed": set(eval_ids),
            "last_seen": datetime,
        }}
    """
    from eval_drilldown import diff_dimensions
    eval_skill = _load_eval_skill_map()
    runs = _drilldown_runs_dir()
    by_skill = defaultdict(lambda: {
        "sections": Counter(),
        "tokens": Counter(),
        "evals_observed": set(),
        "last_seen": None,
    })

    if not runs.exists():
        return dict(by_skill)

    for cand_file in runs.glob("*.output.txt"):
        eval_id = cand_file.stem.replace(".output", "")
        skill = eval_skill.get(eval_id)
        if not skill:
            continue
        try:
            text = cand_file.read_text(encoding="utf-8")
            score_file = runs / f"{eval_id}.score.json"
            score = 0
            if score_file.exists():
                try:
                    score = int(json.loads(score_file.read_text()).get("score", 0))
                except Exception:
                    pass
            diff = diff_dimensions(eval_id, text, score)
            if diff.get("status") != "ok":
                continue
            verdict = diff.get("compare", {}).get("verdict")
            # Only learn from problematic outputs — MATCH means nothing to fix
            if verdict not in ("DRIFT", "DEGRADED"):
                continue
            entry = by_skill[skill]
            entry["evals_observed"].add(eval_id)
            entry["last_seen"] = datetime.now(timezone.utc)
            for sec in diff["sections"]["missing_in_candidate"]:
                normalized = sec.lower().strip()
                if normalized:
                    entry["sections"][normalized] += 1
            for tok, _freq in diff["tokens"]["top_lost"][:10]:
                entry["tokens"][tok] += 1
        except Exception:
            continue

    # Convert sets to lists for JSON-serializability
    return {
        skill: {
            "sections": dict(data["sections"]),
            "tokens": dict(data["tokens"]),
            "evals_observed": sorted(data["evals_observed"]),
            "last_seen": data["last_seen"].isoformat() if data["last_seen"] else None,
        }
        for skill, data in by_skill.items()
    }


def analyse(verbose: bool = False) -> dict:
    """Run pattern analysis without persisting. Returns dict per skill with
    promotion candidates."""
    raw = _collect_drilldown_patterns()
    candidates = {}
    for skill, data in raw.items():
        section_hints = [
            (sec, freq) for sec, freq in data["sections"].items()
            if freq >= MIN_OCCURRENCES_SECTION
        ]
        token_hints = [
            (tok, freq) for tok, freq in data["tokens"].items()
            if freq >= MIN_OCCURRENCES_TOKEN
        ]
        if not section_hints and not token_hints:
            continue
        section_hints.sort(key=lambda x: -x[1])
        token_hints.sort(key=lambda x: -x[1])
        candidates[skill] = {
            "evals_observed": data["evals_observed"],
            "last_seen": data["last_seen"],
            "section_hints": section_hints[:MAX_HINTS_PER_SKILL],
            "token_hints": token_hints[:MAX_HINTS_PER_SKILL],
        }
        if verbose:
            print(f"  {skill}: {len(section_hints)} section + {len(token_hints)} token candidates")
    return candidates


def _hint_for_section(skill: str, section: str, occurrences: int) -> dict:
    return {
        "type": "missing_section",
        "skill": skill,
        "pattern_key": f"section::{section}",
        "occurrences": occurrences,
        "confidence": min(0.5 + 0.15 * occurrences, 0.95),
        "hint": f'Always include a section titled "{section}" — '
                f'observed missing in {occurrences} regression case(s)',
        "first_seen": datetime.now(timezone.utc).isoformat(),
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }


def _hint_for_token(skill: str, token: str, occurrences: int) -> dict:
    return {
        "type": "lost_token_recurrence",
        "skill": skill,
        "pattern_key": f"token::{token}",
        "occurrences": occurrences,
        "confidence": min(0.4 + 0.10 * occurrences, 0.80),
        "hint": f'Ensure coverage of "{token}" — recurrent high-frequency '
                f'token from golden missing in {occurrences} case(s)',
        "first_seen": datetime.now(timezone.utc).isoformat(),
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }


def _load_existing(skill: str) -> dict:
    path = HINTS_DIR / f"{skill}.yaml"
    if not path.exists():
        return {"skill": skill, "hints": []}
    try:
        data = _load_yaml(str(path))
        if isinstance(data, dict) and isinstance(data.get("hints"), list):
            return data
    except Exception:
        pass
    return {"skill": skill, "hints": []}


def _save(skill: str, data: dict):
    _ensure_dirs()
    data["skill"] = skill
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _dump_yaml(data, str(HINTS_DIR / f"{skill}.yaml"))


def _merge_hint(existing_hints: list, new_hint: dict) -> list:
    """If a hint with the same pattern_key exists, bump occurrences and
    update last_seen; otherwise append."""
    for h in existing_hints:
        if h.get("pattern_key") == new_hint["pattern_key"]:
            h["occurrences"] = new_hint["occurrences"]
            h["confidence"] = new_hint["confidence"]
            h["last_seen"] = new_hint["last_seen"]
            return existing_hints
    existing_hints.append(new_hint)
    return existing_hints


def promote(verbose: bool = False) -> dict:
    """Apply promotions: write hint YAMLs for skills with thresholds met."""
    _ensure_dirs()
    candidates = analyse(verbose=False)
    stats = {"skills_updated": 0, "hints_added": 0, "hints_merged": 0}
    for skill, data in candidates.items():
        existing = _load_existing(skill)
        hints = existing.get("hints", [])
        before_count = len(hints)
        added_or_merged_this_skill = 0
        for sec, occ in data["section_hints"]:
            hint = _hint_for_section(skill, sec, occ)
            keys = {h.get("pattern_key") for h in hints}
            hints = _merge_hint(hints, hint)
            if hint["pattern_key"] in keys:
                stats["hints_merged"] += 1
            else:
                stats["hints_added"] += 1
            added_or_merged_this_skill += 1
        for tok, occ in data["token_hints"]:
            hint = _hint_for_token(skill, tok, occ)
            keys = {h.get("pattern_key") for h in hints}
            hints = _merge_hint(hints, hint)
            if hint["pattern_key"] in keys:
                stats["hints_merged"] += 1
            else:
                stats["hints_added"] += 1
            added_or_merged_this_skill += 1
        # Cap to MAX_HINTS_PER_SKILL (keep highest occurrences)
        hints.sort(key=lambda h: -int(h.get("occurrences", 0)))
        hints = hints[:MAX_HINTS_PER_SKILL]
        if added_or_merged_this_skill:
            stats["skills_updated"] += 1
            existing["hints"] = hints
            existing["evals_observed"] = data["evals_observed"]
            _save(skill, existing)
            if verbose:
                print(f"  + {skill}: {len(hints)} hints written")
    return stats


def list_hints() -> list:
    """All persisted hint files."""
    _ensure_dirs()
    out = []
    for hf in sorted(HINTS_DIR.glob("*.yaml")):
        try:
            data = _load_yaml(str(hf))
            if isinstance(data, dict):
                out.append({
                    "skill": data.get("skill") or hf.stem,
                    "hint_count": len(data.get("hints", [])),
                    "updated_at": data.get("updated_at"),
                    "hints": data.get("hints", []),
                })
        except Exception:
            continue
    return out


def get_hints_for_skill(skill: str) -> str:
    """Render persisted hints for context injection. Returns empty string if none."""
    if not skill:
        return ""
    path = HINTS_DIR / f"{skill}.yaml"
    if not path.exists():
        return ""
    try:
        data = _load_yaml(str(path))
    except Exception:
        return ""
    if not isinstance(data, dict):
        return ""
    hints = data.get("hints") or []
    if not hints:
        return ""
    lines = [f"## Learned hints for {skill} (from past regressions)"]
    for h in hints:
        conf = h.get("confidence", 0.5)
        occ = h.get("occurrences", 1)
        lines.append(f"- [{occ}x · conf {conf:.2f}] {h.get('hint', '')}")
    return "\n".join(lines)


def clear_skill(skill: str) -> bool:
    path = HINTS_DIR / f"{skill}.yaml"
    if path.exists():
        path.unlink()
        return True
    return False


def main():
    p = argparse.ArgumentParser(description="DARIO Prompt Hints")
    p.add_argument("--analyse", action="store_true",
                   help="Dry-run: scan drilldowns, report candidates")
    p.add_argument("--promote", action="store_true",
                   help="Promote candidates to prompt_hints/*.yaml")
    p.add_argument("--list", action="store_true")
    p.add_argument("--get", help="Render hints for a specific skill")
    p.add_argument("--clear", help="Clear hints for a skill")
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.analyse:
        r = analyse(verbose=args.verbose)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.json
              else f"{len(r)} skill(s) with promotion candidates")
        return 0

    if args.promote:
        r = promote(verbose=args.verbose)
        print(json.dumps(r, indent=2) if args.json
              else "\n".join(f"  {k}: {v}" for k, v in r.items()))
        return 0

    if args.list:
        out = list_hints()
        if args.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            for entry in out:
                print(f"\n{entry['skill']}: {entry['hint_count']} hint(s) "
                      f"(updated {entry.get('updated_at', '-')[:19]})")
                for h in entry["hints"]:
                    print(f"  - [{h.get('occurrences')}x] {h.get('hint')}")
        return 0

    if args.get:
        text = get_hints_for_skill(args.get)
        if not text:
            print(f"No hints for {args.get}")
        else:
            print(text)
        return 0

    if args.clear:
        ok = clear_skill(args.clear)
        print(f"{'cleared' if ok else 'no hints to clear'}: {args.clear}")
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
