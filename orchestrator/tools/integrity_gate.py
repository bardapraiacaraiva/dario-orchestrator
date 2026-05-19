#!/usr/bin/env python3
"""
DARIO Integrity Gate — Skill / Memory / Reference Consistency Check
====================================================================
Upgrade 14 (operational).

There's no `git commit` in the orchestrator runtime, but skills, eval
cases, goldens, embeddings, chain definitions, and memories cross-
reference each other. When a SKILL.md is removed/renamed/edited, broken
references can sit silently for weeks. This module surfaces them in
seconds.

7 integrity checks (all run on every invocation):
  1. eval_skills_exist        Each eval_suite.EVAL_CASES skill exists on disk
  2. skill_frontmatter_valid  Each referenced SKILL.md has name+description
  3. embeddings_coverage      Cache has an entry for every skill in corpus
  4. embeddings_freshness     Hashed description matches current SKILL.md
  5. golden_skills_alive      Each captured golden's skill still exists
  6. chain_skills_resolve     skill_chains.yaml steps reference valid skills
  7. synaptic_pairs_valid     synaptic_weights.yaml pairs reference valid skills

Exit codes (CI-friendly):
  0 = PASS  (all checks green)
  1 = WARN  (non-blocking issues — broken refs in non-critical layers)
  2 = FAIL  (eval/skill mismatch — would silently degrade output quality)

CLI:
    python tools/integrity_gate.py            Run all checks (human-readable)
    python tools/integrity_gate.py --json     Machine-readable
    python tools/integrity_gate.py --strict   Treat warnings as failures
    python tools/integrity_gate.py --fix      Auto-fix what's safely fixable
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SKILLS_DIR = Path.home() / ".claude" / "skills"
sys.path.insert(0, str(ORCH_DIR))

try:
    from ruamel.yaml import YAML
    _yaml = YAML()

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _yaml.load(f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _pyaml.safe_load(f)


def _skill_path(name: str) -> Path:
    return SKILLS_DIR / name / "SKILL.md"


def _has_skill(name: str) -> bool:
    return _skill_path(name).exists()


def _skill_frontmatter(name: str) -> dict:
    """Return frontmatter dict for a skill, or empty dict if invalid."""
    path = _skill_path(name)
    if not path.exists():
        return {}
    try:
        from semantic_dispatch import _parse_frontmatter
        content = path.read_text(encoding="utf-8", errors="ignore")
        return _parse_frontmatter(content) or {}
    except Exception:
        return {}


def check_eval_skills_exist() -> dict:
    """Check 1: Each eval_suite skill exists on disk."""
    try:
        from eval_suite import EVAL_CASES
    except Exception as e:
        return {"status": "ERROR", "message": f"eval_suite unavailable: {e}"}

    missing = []
    for case in EVAL_CASES:
        skill = case.get("skill")
        if not skill:
            continue
        if not _has_skill(skill):
            missing.append({"eval_id": case["id"], "skill": skill})

    return {
        "status": "PASS" if not missing else "FAIL",
        "severity": "fail",
        "total": len(EVAL_CASES),
        "missing": missing,
        "summary": (
            f"all {len(EVAL_CASES)} eval skills exist"
            if not missing else
            f"{len(missing)} eval(s) reference missing skill files"
        ),
    }


def check_skill_frontmatter_valid() -> dict:
    """Check 2: Each referenced SKILL.md has name + description in frontmatter."""
    try:
        from eval_suite import EVAL_CASES
    except Exception as e:
        return {"status": "ERROR", "message": f"eval_suite unavailable: {e}"}

    invalid = []
    for case in EVAL_CASES:
        skill = case.get("skill")
        if not skill or not _has_skill(skill):
            continue  # missing skills caught by Check 1
        fm = _skill_frontmatter(skill)
        if not fm.get("name") or not fm.get("description"):
            invalid.append({
                "skill": skill,
                "has_name": bool(fm.get("name")),
                "has_description": bool(fm.get("description")),
            })

    return {
        "status": "PASS" if not invalid else "FAIL",
        "severity": "fail",
        "invalid": invalid,
        "summary": (
            "all skill frontmatters valid"
            if not invalid else
            f"{len(invalid)} skill(s) with incomplete frontmatter"
        ),
    }


def check_embeddings_coverage() -> dict:
    """Check 3: Embeddings cache has entries for skills used by evals + chains."""
    try:
        from semantic_dispatch import extract_skill_corpus
        import sqlite3
        corpus = extract_skill_corpus()
        conn = sqlite3.connect(str(ORCH_DIR / "orchestrator.db"))
        rows = conn.execute("SELECT skill_name FROM skill_embeddings").fetchall()
        conn.close()
        cached = {r[0] for r in rows}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)[:200]}

    missing = sorted(set(corpus.keys()) - cached)
    orphan = sorted(cached - set(corpus.keys()))

    severity = "warn"
    if len(missing) > 10:
        severity = "fail"

    return {
        "status": "PASS" if not missing and not orphan else (
            "FAIL" if severity == "fail" else "WARN"
        ),
        "severity": severity,
        "corpus_size": len(corpus),
        "cached": len(cached),
        "missing": missing[:20],
        "missing_count": len(missing),
        "orphan_in_cache": orphan[:20],
        "orphan_count": len(orphan),
        "summary": (
            f"all {len(corpus)} skills have embeddings"
            if not missing and not orphan else
            f"{len(missing)} skill(s) without embeddings, "
            f"{len(orphan)} orphan cache entry(ies)"
        ),
    }


def check_embeddings_freshness() -> dict:
    """Check 4: Cached description hash matches current SKILL.md content."""
    try:
        from semantic_dispatch import (
            extract_skill_corpus, _hash, _load_keyword_index, _augment_description
        )
        import sqlite3
        corpus = extract_skill_corpus()
        keyword_index = _load_keyword_index()
        conn = sqlite3.connect(str(ORCH_DIR / "orchestrator.db"))
        rows = conn.execute(
            "SELECT skill_name, description_hash FROM skill_embeddings"
        ).fetchall()
        conn.close()
        cached_hashes = {r[0]: r[1] for r in rows}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)[:200]}

    stale = []
    for name, desc in corpus.items():
        augmented = _augment_description(name, desc, keyword_index)
        expected_hash = _hash(augmented)
        if cached_hashes.get(name) != expected_hash:
            if name in cached_hashes:
                stale.append(name)
            # if not in cached_hashes that's covered by Check 3

    return {
        "status": "PASS" if not stale else "WARN",
        "severity": "warn",
        "stale_count": len(stale),
        "stale_skills": stale[:20],
        "summary": (
            "all embeddings fresh"
            if not stale else
            f"{len(stale)} skill(s) with stale embeddings — run "
            f"`semantic_dispatch --bootstrap` to refresh"
        ),
    }


def check_golden_skills_alive() -> dict:
    """Check 5: Each captured golden's eval references a still-existing skill."""
    try:
        from golden_eval import list_goldens
        from eval_suite import EVAL_CASES
    except Exception as e:
        return {"status": "ERROR", "message": str(e)[:200]}

    case_lookup = {c["id"]: c.get("skill") for c in EVAL_CASES}
    orphaned = []
    for g in list_goldens():
        eid = g["eval_id"]
        skill = case_lookup.get(eid)
        if not skill:
            orphaned.append({"eval_id": eid, "reason": "no matching eval_case"})
        elif not _has_skill(skill):
            orphaned.append({"eval_id": eid, "skill": skill, "reason": "skill removed"})

    return {
        "status": "PASS" if not orphaned else "FAIL",
        "severity": "fail",
        "orphaned": orphaned,
        "summary": (
            "all goldens reference live skills"
            if not orphaned else
            f"{len(orphaned)} golden(s) orphaned — eval or skill removed"
        ),
    }


def check_chain_skills_resolve() -> dict:
    """Check 6: skill_chains.yaml steps reference valid skills."""
    chains_file = ORCH_DIR / "skill_chains.yaml"
    if not chains_file.exists():
        return {"status": "PASS", "severity": "warn", "summary": "no skill_chains.yaml"}

    try:
        data = _load_yaml(str(chains_file))
        chains = (data or {}).get("chains", {}) if isinstance(data, dict) else {}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)[:200]}

    broken = []
    total_steps = 0
    for chain_name, chain in chains.items():
        if not isinstance(chain, dict):
            continue
        for i, step in enumerate(chain.get("steps", [])):
            total_steps += 1
            skill = step.get("skill")
            if skill and not _has_skill(skill):
                broken.append({"chain": chain_name, "step": i, "skill": skill})

    return {
        "status": "PASS" if not broken else "FAIL",
        "severity": "fail",
        "total_steps": total_steps,
        "broken": broken,
        "summary": (
            f"all {total_steps} chain steps resolve"
            if not broken else
            f"{len(broken)} chain step(s) reference missing skills"
        ),
    }


def check_synaptic_pairs_valid() -> dict:
    """Check 7: synaptic_weights.yaml pairs reference valid skills."""
    weights_file = ORCH_DIR / "synaptic_weights.yaml"
    if not weights_file.exists():
        return {"status": "PASS", "severity": "warn", "summary": "no synaptic_weights.yaml"}

    try:
        data = _load_yaml(str(weights_file))
        graph = (data or {}).get("affinity_graph", {}) if isinstance(data, dict) else {}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)[:200]}

    broken = []
    for pair_key in graph.keys():
        if not isinstance(pair_key, str):
            continue
        # Pair format: "skill-a + skill-b"
        skills = [s.strip() for s in pair_key.split(" + ")]
        for skill in skills:
            if not _has_skill(skill):
                broken.append({"pair": pair_key, "missing_skill": skill})

    return {
        "status": "PASS" if not broken else "WARN",
        "severity": "warn",
        "total_pairs": len(graph),
        "broken": broken,
        "summary": (
            f"all {len(graph)} synaptic pairs valid"
            if not broken else
            f"{len(broken)} synaptic pair(s) reference missing skills"
        ),
    }


CHECKS = [
    ("eval_skills_exist", check_eval_skills_exist),
    ("skill_frontmatter_valid", check_skill_frontmatter_valid),
    ("embeddings_coverage", check_embeddings_coverage),
    ("embeddings_freshness", check_embeddings_freshness),
    ("golden_skills_alive", check_golden_skills_alive),
    ("chain_skills_resolve", check_chain_skills_resolve),
    ("synaptic_pairs_valid", check_synaptic_pairs_valid),
]


def run_all(strict: bool = False) -> dict:
    """Execute all integrity checks. Aggregate verdict."""
    report = {"checks": []}
    any_fail = False
    any_warn = False

    for name, fn in CHECKS:
        try:
            r = fn()
            r["name"] = name
            report["checks"].append(r)
            if r["status"] == "FAIL" or (strict and r["status"] == "WARN"):
                any_fail = True
            elif r["status"] == "WARN":
                any_warn = True
            elif r["status"] == "ERROR":
                # Treat ERROR as fail in strict mode; warn otherwise
                if strict:
                    any_fail = True
                else:
                    any_warn = True
        except Exception as e:
            report["checks"].append({
                "name": name, "status": "ERROR", "message": str(e)[:200],
            })
            if strict:
                any_fail = True
            else:
                any_warn = True

    if any_fail:
        report["verdict"] = "FAIL"
        report["exit_code"] = 2
    elif any_warn:
        report["verdict"] = "WARN"
        report["exit_code"] = 1
    else:
        report["verdict"] = "PASS"
        report["exit_code"] = 0

    return report


def auto_fix() -> dict:
    """Apply safe automatic fixes:
       - Re-bootstrap embeddings if stale or missing entries
    """
    fixes = {"applied": [], "skipped": []}

    try:
        from semantic_dispatch import bootstrap_embeddings
        # Only triggered if a check would have caught the issue
        report_pre = run_all()
        needs_bootstrap = any(
            c.get("name") in ("embeddings_coverage", "embeddings_freshness")
            and c.get("status") in ("WARN", "FAIL")
            for c in report_pre["checks"]
        )
        if needs_bootstrap:
            s = bootstrap_embeddings(verbose=False)
            fixes["applied"].append({
                "fix": "embeddings_rebootstrap",
                "generated": s.get("generated", 0),
                "pruned": s.get("pruned", 0),
            })
        else:
            fixes["skipped"].append("embeddings_rebootstrap (no need)")
    except Exception as e:
        fixes["skipped"].append(f"embeddings: {e}")

    return fixes


def _format(report: dict) -> str:
    lines = [f"=== DARIO Integrity Gate — {report['verdict']} (exit {report['exit_code']}) ==="]
    for c in report["checks"]:
        status = c["status"]
        symbol = {"PASS": "+", "WARN": "~", "FAIL": "!", "ERROR": "?"}.get(status, "?")
        lines.append(f"  [{symbol}] {c['name']:30s} {status:5s}  {c.get('summary', '')}")
        if status in ("FAIL", "WARN") and c.get("missing"):
            for m in c["missing"][:5]:
                lines.append(f"        - {m}")
        if status in ("FAIL", "WARN") and c.get("broken"):
            for b in c["broken"][:5]:
                lines.append(f"        - {b}")
        if status in ("FAIL", "WARN") and c.get("orphaned"):
            for o in c["orphaned"][:5]:
                lines.append(f"        - {o}")
        if status in ("FAIL", "WARN") and c.get("stale_skills"):
            for s in c["stale_skills"][:5]:
                lines.append(f"        - stale: {s}")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="DARIO Integrity Gate")
    p.add_argument("--strict", action="store_true",
                   help="Treat warnings as failures")
    p.add_argument("--fix", action="store_true",
                   help="Apply safe auto-fixes (re-bootstrap embeddings if stale)")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.fix:
        fixes = auto_fix()
        print(json.dumps(fixes, indent=2) if args.json else
              f"Applied: {fixes['applied']}\nSkipped: {fixes['skipped']}")

    report = run_all(strict=args.strict)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(_format(report))

    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
