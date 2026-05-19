#!/usr/bin/env python3
"""
DARIO Chain Validation Gates
============================
Upgrade 6 (Sprint 2) of the Cognitive Audit roadmap.

skill_chains.yaml declares each step's expected output fields via
`pass_to_next: [field_a, field_b, ...]`. Until now, chain_executor saved
checkpoints and advanced to the next step WITHOUT verifying these fields
actually appeared in the output. Silent cascading failure: step N
"completes" producing nothing useful, step N+1 launches anyway with
empty context, everything degrades downstream.

This module:
  - Loads chain definitions from skill_chains.yaml
  - validate_step_output(chain_name, step_index, artifact) — checks all
    pass_to_next fields are present (and non-empty) in the output
  - Returns explicit verdict + missing-fields list + escalation guidance

Hooked into chain_executor.save_checkpoint() as Step Gate 2 (artifact
schema validation is Gate 1; pass_to_next is Gate 2).

CLI:
    python chain_validator.py --chain brand_to_market --step 0 --artifact '{"posicionamento":"...","archetype":"..."}'
    python chain_validator.py --list-chains
"""

import argparse
import json
import sys
from pathlib import Path

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


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CHAINS_FILE = ORCH_DIR / "skill_chains.yaml"


_CHAIN_CACHE = None


def _load_chains() -> dict:
    global _CHAIN_CACHE
    if _CHAIN_CACHE is not None:
        return _CHAIN_CACHE
    if not CHAINS_FILE.exists():
        _CHAIN_CACHE = {}
        return _CHAIN_CACHE
    data = _load_yaml(str(CHAINS_FILE))
    _CHAIN_CACHE = (data or {}).get("chains", {}) if isinstance(data, dict) else {}
    return _CHAIN_CACHE


def _normalize_artifact(artifact) -> dict:
    """Coerce string/None/dict artifacts into a dict for inspection."""
    if isinstance(artifact, dict):
        return artifact
    if isinstance(artifact, str):
        # If the artifact came as JSON string, try to parse
        s = artifact.strip()
        if s.startswith("{") or s.startswith("["):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass
        return {"_raw_text": artifact}
    if artifact is None:
        return {}
    return {"_value": artifact}


def _field_present(artifact: dict, field: str) -> bool:
    """A field is 'present' if it exists with a non-empty value, OR
    if its content appears as a substring in the raw text fallback.
    """
    if field in artifact:
        val = artifact[field]
        if val is None:
            return False
        if isinstance(val, (list, dict)) and len(val) == 0:
            return False
        if isinstance(val, str) and not val.strip():
            return False
        return True
    # Fallback: if artifact has raw text, check substring presence
    raw = artifact.get("_raw_text", "")
    if raw and field.lower() in raw.lower():
        return True
    return False


def validate_step_output(chain_name: str, step_index: int, artifact) -> dict:
    """Validate a chain step's output against its declared pass_to_next fields.

    Returns:
        {
          "valid": bool,
          "chain": chain_name,
          "step": step_index,
          "skill": "dario-brand",
          "expected_fields": [...],
          "missing": [...],
          "present": [...],
          "verdict": "PASS" | "INCOMPLETE" | "EMPTY" | "TERMINAL",
          "escalation": str | None,
        }
    """
    result = {
        "valid": False,
        "chain": chain_name,
        "step": step_index,
        "skill": None,
        "expected_fields": [],
        "missing": [],
        "present": [],
        "verdict": "UNKNOWN",
        "escalation": None,
    }

    chains = _load_chains()
    chain = chains.get(chain_name)
    if not chain:
        result["verdict"] = "UNKNOWN_CHAIN"
        result["escalation"] = f"chain '{chain_name}' not in skill_chains.yaml"
        return result

    steps = chain.get("steps", [])
    if step_index >= len(steps):
        result["verdict"] = "STEP_OUT_OF_RANGE"
        result["escalation"] = f"step {step_index} >= chain length {len(steps)}"
        return result

    step = steps[step_index]
    result["skill"] = step.get("skill")
    expected = step.get("pass_to_next") or []
    if expected is None:
        expected = []
    result["expected_fields"] = list(expected)

    # Last step typically has pass_to_next=null — nothing to verify
    if not expected:
        result["verdict"] = "TERMINAL"
        result["valid"] = True
        return result

    art = _normalize_artifact(artifact)

    # Total emptiness check
    if not art or (len(art) == 1 and "_raw_text" in art and not art["_raw_text"].strip()):
        result["verdict"] = "EMPTY"
        result["missing"] = list(expected)
        result["escalation"] = (
            f"step '{step.get('skill')}' produced no usable output — "
            f"cannot launch next step without {expected}. Escalate to CEO or retry."
        )
        return result

    for field in expected:
        if _field_present(art, field):
            result["present"].append(field)
        else:
            result["missing"].append(field)

    if not result["missing"]:
        result["verdict"] = "PASS"
        result["valid"] = True
    elif len(result["present"]) == 0:
        result["verdict"] = "EMPTY"
        result["escalation"] = (
            f"none of {expected} found in step output — likely wrong skill "
            f"or task misunderstood. Escalate."
        )
    else:
        # Partial. Mild incomplete is acceptable, severe means escalate.
        ratio = len(result["present"]) / len(expected)
        result["verdict"] = "INCOMPLETE"
        if ratio < 0.5:
            result["escalation"] = (
                f"only {len(result['present'])}/{len(expected)} pass_to_next "
                f"fields present (missing: {result['missing']}). "
                f"Retry skill '{step.get('skill')}' or escalate before launching "
                f"step {step_index + 1}."
            )
        else:
            result["escalation"] = (
                f"partial output — {len(result['missing'])} fields missing "
                f"({result['missing']}). Next step may receive incomplete context."
            )
    return result


def validate_full_chain(chain_name: str, artifacts_by_step: list) -> dict:
    """Validate every step's artifact in order. Useful for post-mortem on
    completed chain runs.

    artifacts_by_step: list aligned to step index
    Returns aggregate report.
    """
    chains = _load_chains()
    chain = chains.get(chain_name)
    if not chain:
        return {"valid": False, "error": f"chain '{chain_name}' not found"}

    steps = chain.get("steps", [])
    per_step = []
    overall_valid = True
    for i, art in enumerate(artifacts_by_step):
        if i >= len(steps):
            break
        v = validate_step_output(chain_name, i, art)
        per_step.append(v)
        if not v["valid"] and v["verdict"] not in ("TERMINAL",):
            overall_valid = False

    return {
        "chain": chain_name,
        "valid": overall_valid,
        "total_steps": len(steps),
        "validated_steps": len(per_step),
        "per_step": per_step,
    }


def list_chains() -> dict:
    """Summary of available chains and their pass_to_next fields per step."""
    chains = _load_chains()
    summary = {}
    for name, chain in chains.items():
        if not isinstance(chain, dict):
            continue
        steps_info = []
        for i, step in enumerate(chain.get("steps", [])):
            steps_info.append({
                "step": i,
                "skill": step.get("skill"),
                "pass_to_next": step.get("pass_to_next") or [],
            })
        summary[name] = {
            "description": chain.get("description", ""),
            "steps": steps_info,
        }
    return summary


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from license_guard import enforce_or_exit
        enforce_or_exit("chain_validator")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Chain Validator")
    p.add_argument("--chain", help="Chain name")
    p.add_argument("--step", type=int, help="Step index (0-based)")
    p.add_argument("--artifact", help="Artifact as JSON string")
    p.add_argument("--list-chains", action="store_true")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.list_chains:
        s = list_chains()
        if args.json:
            print(json.dumps(s, indent=2, ensure_ascii=False))
        else:
            for name, info in s.items():
                print(f"\n{name}: {info['description']}")
                for st in info["steps"]:
                    fields = st["pass_to_next"]
                    print(f"  step {st['step']}: {st['skill']} -> {fields}")
        return 0

    if not args.chain or args.step is None or not args.artifact:
        p.print_help()
        return 1

    try:
        artifact = json.loads(args.artifact)
    except Exception:
        artifact = args.artifact  # treat as raw text

    result = validate_step_output(args.chain, args.step, artifact)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        symbol = {"PASS": "+", "TERMINAL": "+", "INCOMPLETE": "~",
                  "EMPTY": "!", "UNKNOWN_CHAIN": "!",
                  "STEP_OUT_OF_RANGE": "!", "UNKNOWN": "?"}.get(result["verdict"], "?")
        print(f"[{symbol}] {args.chain} step {args.step} ({result['skill']}): {result['verdict']}")
        if result["expected_fields"]:
            print(f"  Expected: {result['expected_fields']}")
            print(f"  Present:  {result['present']}")
            if result["missing"]:
                print(f"  Missing:  {result['missing']}")
        if result["escalation"]:
            print(f"  Escalation: {result['escalation']}")
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
