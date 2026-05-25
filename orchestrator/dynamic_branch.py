#!/usr/bin/env python3
"""
DARIO Dynamic Chain Branching
=============================
Upgrade 10 (Sprint 4) of the Cognitive Audit roadmap.

workflow_graph.py defines `.branch()` but evaluates conditions at build
time — once the chain compiles, the DAG is fixed. Chains today are static
recipes: dario-brand → dario-naming → dario-offer → ... regardless of
how each step actually performed.

This module adds RUNTIME branching. After every step the chain executor
calls `decide_next_action()`, which inspects:
  - current step's score
  - dimension variance from quality scoring
  - confidence engine verdict
  - chain quality_gate threshold
  - dependency graph between remaining steps
  - skill independence (can next N steps run in parallel?)

…and returns one of five branch decisions:

  CONTINUE_SERIAL  — score is OK, proceed to next step as planned
  REVISION_LOOP    — score below threshold, retry current step once
  PARALLELIZE_NEXT — score excellent + next steps independent, fan-out
  EARLY_STOP       — revision exhausted or catastrophic failure
  ESCALATE         — needs human review (low confidence or critical fail)

Idempotent and stateless — same inputs, same decision. Pure function
over chain state. No LLM calls.

CLI:
    python dynamic_branch.py --simulate <chain> <step> <score>
    python dynamic_branch.py --explain brand_to_market 0 88
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _yaml.load(f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _pyaml.safe_load(f)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CHAINS_FILE = ORCH_DIR / "skill_chains.yaml"

# Decision thresholds
SCORE_REVISION_BELOW = 70    # below this -> revision loop
SCORE_EXCELLENCE_AT = 85     # at/above -> can consider parallelization
SCORE_CATASTROPHIC = 40      # below this twice -> early stop
MAX_REVISION_ATTEMPTS = 1    # how many times to retry a step

# Action names
CONTINUE_SERIAL = "CONTINUE_SERIAL"
REVISION_LOOP = "REVISION_LOOP"
PARALLELIZE_NEXT = "PARALLELIZE_NEXT"
EARLY_STOP = "EARLY_STOP"
ESCALATE = "ESCALATE"

# Skills that almost always block downstream (their output is foundational)
# Sequential discipline > speed for these — never parallelize after them
FOUNDATIONAL_SKILLS = {
    "dario-brand", "dario-diagnose", "diva-briefing", "diva-diagnose",
    "a360-nicho", "a360-validacao", "dario-product",
}


_CHAIN_CACHE = None


def _load_chain(chain_name: str) -> dict:
    global _CHAIN_CACHE
    if _CHAIN_CACHE is None:
        if not CHAINS_FILE.exists():
            _CHAIN_CACHE = {}
        else:
            data = _load_yaml(str(CHAINS_FILE))
            _CHAIN_CACHE = (data or {}).get("chains", {}) if isinstance(data, dict) else {}
    return _CHAIN_CACHE.get(chain_name, {})


def _steps_independent(step_a: dict, step_b: dict) -> bool:
    """Two steps are independent if step_b doesn't consume any of step_a's
    pass_to_next fields.
    """
    a_produces = set(step_a.get("pass_to_next") or [])
    b_receives_str = (step_b.get("receives") or "").lower()
    if not a_produces or not b_receives_str:
        return False  # can't prove independence, assume dependent
    # If any field a produces is mentioned in b's receives, they're coupled
    for f in a_produces:
        if f.lower() in b_receives_str:
            return False
    return True


def _parse_quality_gate(chain: dict) -> int:
    """Extract score threshold from chain's quality_gate text."""
    gate = chain.get("quality_gate", "") or ""
    # Look for >= NN pattern
    import re
    m = re.search(r">=?\s*(\d{2,3})", gate)
    if m:
        return int(m.group(1))
    return SCORE_REVISION_BELOW


def decide_next_action(
    chain_name: str,
    step_index: int,
    score: int,
    revision_count: int = 0,
    dimension_variance: float = None,
    confidence_level: str = None,
    artifact: dict = None,
) -> dict:
    """Pure function — decide what to do after step_index completed with `score`.

    Returns:
        {
          "action": CONTINUE_SERIAL | REVISION_LOOP | PARALLELIZE_NEXT | EARLY_STOP | ESCALATE,
          "next_steps": [int...],
          "rationale": str,
          "metadata": {...},
        }
    """
    chain = _load_chain(chain_name)
    if not chain:
        return {
            "action": ESCALATE,
            "next_steps": [],
            "rationale": f"chain '{chain_name}' not found in skill_chains.yaml",
            "metadata": {"error": "unknown_chain"},
        }

    steps = chain.get("steps", [])
    total_steps = len(steps)
    threshold = _parse_quality_gate(chain)

    if step_index < 0 or step_index >= total_steps:
        return {
            "action": EARLY_STOP,
            "next_steps": [],
            "rationale": f"step_index {step_index} out of range (0..{total_steps - 1})",
            "metadata": {"error": "out_of_range"},
        }

    current_step = steps[step_index]
    current_skill = current_step.get("skill", "")
    is_last = (step_index == total_steps - 1)

    # 1. Catastrophic failure — bail
    if score < SCORE_CATASTROPHIC:
        if revision_count > 0:
            return {
                "action": EARLY_STOP,
                "next_steps": [],
                "rationale": (
                    f"catastrophic score ({score} < {SCORE_CATASTROPHIC}) "
                    f"after {revision_count} revision(s) — stop the chain"
                ),
                "metadata": {"score": score, "revision_count": revision_count},
            }
        return {
            "action": ESCALATE,
            "next_steps": [],
            "rationale": (
                f"catastrophic score ({score}) on first attempt — "
                f"escalate to human review before retrying"
            ),
            "metadata": {"score": score, "skill": current_skill},
        }

    # 2. Below revision threshold — try one more time (if attempts left)
    if score < threshold:
        if revision_count < MAX_REVISION_ATTEMPTS:
            return {
                "action": REVISION_LOOP,
                "next_steps": [step_index],  # retry same step
                "rationale": (
                    f"score {score} < gate {threshold}; "
                    f"retry attempt {revision_count + 1}/{MAX_REVISION_ATTEMPTS}"
                ),
                "metadata": {
                    "score": score,
                    "threshold": threshold,
                    "revision_count": revision_count + 1,
                    "skill": current_skill,
                },
            }
        # Revision exhausted — escalate (Manifesto: never exceed max revisions silently)
        return {
            "action": ESCALATE,
            "next_steps": [],
            "rationale": (
                f"score {score} < gate {threshold} after {revision_count} "
                f"revision(s) — escalate to CEO/human"
            ),
            "metadata": {
                "score": score,
                "threshold": threshold,
                "skill": current_skill,
            },
        }

    # 3. LOW confidence even with good score — review before proceeding
    if confidence_level == "LOW":
        return {
            "action": ESCALATE,
            "next_steps": [],
            "rationale": (
                f"score {score} acceptable but LOW confidence "
                f"(sigma={dimension_variance}); escalate before propagating "
                f"uncertain output to next step"
            ),
            "metadata": {
                "score": score,
                "confidence": confidence_level,
                "sigma": dimension_variance,
            },
        }

    # 4. Last step — chain done
    if is_last:
        return {
            "action": CONTINUE_SERIAL,
            "next_steps": [],
            "rationale": f"final step completed with score {score}",
            "metadata": {"score": score, "terminal": True},
        }

    next_index = step_index + 1

    # 5. Excellence + foundational skill — never parallelize (its output blocks
    # everything that follows by definition)
    if current_skill in FOUNDATIONAL_SKILLS:
        return {
            "action": CONTINUE_SERIAL,
            "next_steps": [next_index],
            "rationale": (
                f"score {score} >= {threshold}; '{current_skill}' is "
                f"foundational — proceed serial to preserve dependency"
            ),
            "metadata": {"score": score, "foundational": True},
        }

    # 6. Excellence + next steps independent of each other — parallelize
    if score >= SCORE_EXCELLENCE_AT and next_index + 1 < total_steps:
        next_step = steps[next_index]
        after_next = steps[next_index + 1]
        if _steps_independent(next_step, after_next):
            parallel_set = [next_index, next_index + 1]
            return {
                "action": PARALLELIZE_NEXT,
                "next_steps": parallel_set,
                "rationale": (
                    f"score {score} >= {SCORE_EXCELLENCE_AT} (excellence) and "
                    f"steps {next_index}+{next_index + 1} are independent — "
                    f"fan-out for speed"
                ),
                "metadata": {
                    "score": score,
                    "parallel_skills": [steps[i].get("skill") for i in parallel_set],
                },
            }

    # 7. Default — proceed serial
    return {
        "action": CONTINUE_SERIAL,
        "next_steps": [next_index],
        "rationale": f"score {score} >= {threshold}; proceed to step {next_index}",
        "metadata": {"score": score, "next_skill": steps[next_index].get("skill")},
    }


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("dynamic_branch")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Dynamic Chain Branching")
    p.add_argument("--simulate", nargs=3, metavar=("CHAIN", "STEP", "SCORE"),
                   help="Simulate a branch decision")
    p.add_argument("--explain", nargs=3, metavar=("CHAIN", "STEP", "SCORE"),
                   help="Same as simulate but verbose")
    p.add_argument("--revision-count", type=int, default=0)
    p.add_argument("--confidence", default=None,
                   help="Confidence level: HIGH | MEDIUM | LOW")
    p.add_argument("--sigma", type=float, default=None)
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    inputs = args.simulate or args.explain
    if not inputs:
        p.print_help()
        return 1

    chain, step, score = inputs
    r = decide_next_action(
        chain_name=chain,
        step_index=int(step),
        score=int(score),
        revision_count=args.revision_count,
        dimension_variance=args.sigma,
        confidence_level=args.confidence,
    )

    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print(f"Action:     {r['action']}")
        print(f"Next steps: {r['next_steps']}")
        print(f"Rationale:  {r['rationale']}")
        if r.get("metadata"):
            print("Metadata:")
            for k, v in r["metadata"].items():
                print(f"  {k}: {v}")
    return 0 if r["action"] not in (ESCALATE, EARLY_STOP) else 2


if __name__ == "__main__":
    sys.exit(main())
