#!/usr/bin/env python3
"""
DARIO Confidence Engine
=======================
Upgrade 4 (Sprint 2) of the Cognitive Audit roadmap.

Previously the orchestrator gated only on absolute score:
    action = "ship" if score >= 60 else "revision"

This left dario-story-circle (range 42-90, σ=24, revision_rate 33%) being
shipped at Tier C as if it were reliable. Confidence was COMPUTED in
llm_judge.py (full dimension breakdown) but SUPPRESSED — never bubbled up.

This module exposes:
    compute_confidence(dimensions, skill_metrics) -> (score, level, reasons)
    gate_decision(score, dimensions, skill, revision_count) -> action

Three confidence levels:
    HIGH   — dimension agreement (σ < 0.15) + skill tier A or B + score consistent with history
    MEDIUM — dimension agreement (σ < 0.25) OR tier B with moderate variance
    LOW    — dimension σ >= 0.25 OR skill tier C/D OR score outside historical range

Gating logic:
    HIGH    + score >= pass_threshold     -> SHIP
    MEDIUM  + score >= pass_threshold + 5 -> SHIP (with caveat)
    MEDIUM  + score < pass_threshold + 5  -> REVIEW
    LOW     + any score                   -> REVIEW or ESCALATE (per tier)
    Critical execution_policy + LOW       -> always ESCALATE

CLI:
    python confidence_engine.py --dims '{"specificity":0.9,...}' --skill dario-brand --score 78
    python confidence_engine.py --task TASK-001
"""

import argparse
import json
import math
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
QUALITY_FILE = ORCH_DIR / "quality" / "skill-metrics.yaml"

# Variance thresholds (computed on dimensions 0.0-1.0 scale)
SIGMA_HIGH = 0.15   # tight agreement
SIGMA_MED = 0.25    # moderate agreement
# Tier impact on confidence
TIER_HIGH_CONF = {"A"}
TIER_MED_CONF = {"B"}
TIER_LOW_CONF = {"C", "D", "unscored"}

# Score outlier sensitivity (z-score against recent scores)
OUTLIER_Z_THRESHOLD = 1.5


def _std_dev(values: list) -> float:
    if not values or len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(var)


def _load_skill_metrics(skill: str) -> dict:
    if not QUALITY_FILE.exists() or not skill:
        return {}
    try:
        data = _load_yaml(str(QUALITY_FILE))
        if not isinstance(data, dict):
            return {}
        skills = data.get("skills", {})
        entry = skills.get(skill, {})
        return entry if isinstance(entry, dict) else {}
    except Exception:
        return {}


def _is_outlier(score: int, history: list) -> tuple:
    """Returns (is_outlier, z_score) using historical mean/std."""
    if not history or len(history) < 3:
        return False, 0.0
    mean = sum(history) / len(history)
    sd = _std_dev(history)
    if sd == 0:
        return False, 0.0
    z = (score - mean) / sd
    return abs(z) > OUTLIER_Z_THRESHOLD, round(z, 2)


def compute_confidence(dimensions: dict, skill: str = None,
                       score: int = 0) -> dict:
    """Compute confidence level and reasons.

    Returns:
        {
          "level": "HIGH" | "MEDIUM" | "LOW",
          "score": 0.0-1.0,
          "sigma": float (dimension std dev),
          "tier": "A"|"B"|"C"|"D"|"unscored",
          "reasons": [...],
          "outlier": bool,
          "z_score": float,
        }
    """
    result = {
        "level": "MEDIUM",
        "score": 0.5,
        "sigma": 0.0,
        "tier": "unscored",
        "reasons": [],
        "outlier": False,
        "z_score": 0.0,
    }

    # 1. Dimension variance
    sigma = 0.0
    if dimensions and isinstance(dimensions, dict):
        dim_values = [float(v) for v in dimensions.values() if isinstance(v, (int, float))]
        if dim_values:
            sigma = _std_dev(dim_values)
            result["sigma"] = round(sigma, 3)
            if sigma >= SIGMA_MED:
                result["reasons"].append(f"high dimension variance (σ={sigma:.3f})")
            elif sigma < SIGMA_HIGH:
                result["reasons"].append(f"tight dimension agreement (σ={sigma:.3f})")

    # 2. Skill tier
    metrics = _load_skill_metrics(skill) if skill else {}
    tier = metrics.get("tier", "unscored")
    result["tier"] = tier
    if tier in TIER_LOW_CONF:
        result["reasons"].append(f"skill tier {tier}")
    elif tier in TIER_HIGH_CONF:
        result["reasons"].append(f"skill tier {tier}")

    # 3. Historical outlier check
    history = metrics.get("live_scores") or metrics.get("scores") or []
    is_outlier, z = _is_outlier(score, history)
    result["outlier"] = is_outlier
    result["z_score"] = z
    if is_outlier:
        direction = "above" if z > 0 else "below"
        result["reasons"].append(f"score {z:+.1f}σ {direction} historical mean")

    # 4. Combine into level + numeric confidence
    # Start at 0.7 (default medium-ish), adjust up/down
    conf = 0.7
    if sigma > 0:
        if sigma < SIGMA_HIGH:
            conf += 0.15
        elif sigma >= SIGMA_MED:
            conf -= 0.20
    if tier in TIER_HIGH_CONF:
        conf += 0.15
    elif tier in TIER_LOW_CONF:
        conf -= 0.15
    if is_outlier:
        conf -= 0.15
    # Round first to avoid floating-point cliff edges (0.7 - 0.15 = 0.5499...)
    conf = round(max(0.0, min(1.0, conf)), 3)
    result["score"] = conf

    if conf >= 0.80:
        result["level"] = "HIGH"
    elif conf >= 0.55:
        result["level"] = "MEDIUM"
    else:
        result["level"] = "LOW"

    return result


def gate_decision(score: int, dimensions: dict, skill: str = None,
                  revision_count: int = 0, pass_threshold: int = 60,
                  execution_policy: str = "default") -> dict:
    """Decide ship/review/escalate using score + confidence.

    Replaces quality_scorer.determine_action() logic with confidence awareness.

    Returns:
        {
          "action": "ship" | "review" | "revision" | "escalate" | "success_pattern",
          "confidence": <confidence dict>,
          "rationale": str,
          "score": int,
        }
    """
    conf = compute_confidence(dimensions, skill, score)
    level = conf["level"]
    rationale_parts = [
        f"score={score}",
        f"threshold={pass_threshold}",
        f"confidence={level}",
        f"σ={conf['sigma']}",
        f"tier={conf['tier']}",
    ]

    # Critical task with LOW confidence — always escalate (Manifesto: critical needs approval)
    if execution_policy == "critical" and level == "LOW":
        return {
            "action": "escalate",
            "confidence": conf,
            "score": score,
            "rationale": " | ".join(rationale_parts + ["critical+LOW=escalate"]),
        }

    # Revision exhausted -> escalate regardless of confidence
    if score < pass_threshold and revision_count >= 3:
        return {
            "action": "escalate",
            "confidence": conf,
            "score": score,
            "rationale": " | ".join(rationale_parts + [f"revision_max ({revision_count})"]),
        }

    # Below threshold
    if score < pass_threshold:
        return {
            "action": "revision",
            "confidence": conf,
            "score": score,
            "rationale": " | ".join(rationale_parts + ["score<threshold"]),
        }

    # Excellence regardless of confidence (extract pattern)
    if score >= 90 and level != "LOW":
        return {
            "action": "success_pattern",
            "confidence": conf,
            "score": score,
            "rationale": " | ".join(rationale_parts + ["excellence"]),
        }

    # The new layer: confidence gating between ship/review
    if level == "HIGH":
        return {
            "action": "ship",
            "confidence": conf,
            "score": score,
            "rationale": " | ".join(rationale_parts + ["HIGH conf -> ship"]),
        }

    if level == "MEDIUM":
        # Medium confidence ships only if comfortably above threshold
        if score >= pass_threshold + 5:
            return {
                "action": "ship",
                "confidence": conf,
                "score": score,
                "rationale": " | ".join(rationale_parts + ["MED conf + score buffer -> ship"]),
            }
        return {
            "action": "review",
            "confidence": conf,
            "score": score,
            "rationale": " | ".join(rationale_parts + ["MED conf near threshold -> review"]),
        }

    # LOW confidence
    if conf["tier"] in TIER_HIGH_CONF or conf["tier"] in TIER_MED_CONF:
        # Mature skill that hit a low-confidence moment — human review
        return {
            "action": "review",
            "confidence": conf,
            "score": score,
            "rationale": " | ".join(rationale_parts + ["LOW conf + mature skill -> review"]),
        }
    # Low confidence + immature/low tier -> escalate
    return {
        "action": "escalate",
        "confidence": conf,
        "score": score,
        "rationale": " | ".join(rationale_parts + ["LOW conf + low tier -> escalate"]),
    }


def main():
    p = argparse.ArgumentParser(description="DARIO Confidence Engine")
    p.add_argument("--dims", type=str, help="JSON dimensions dict")
    p.add_argument("--score", type=int, default=0)
    p.add_argument("--skill", type=str, default=None)
    p.add_argument("--threshold", type=int, default=60)
    p.add_argument("--revisions", type=int, default=0)
    p.add_argument("--policy", type=str, default="default")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    dimensions = {}
    if args.dims:
        try:
            dimensions = json.loads(args.dims)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON for --dims: {e}", file=sys.stderr)
            return 1

    result = gate_decision(
        score=args.score,
        dimensions=dimensions,
        skill=args.skill,
        revision_count=args.revisions,
        pass_threshold=args.threshold,
        execution_policy=args.policy,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        c = result["confidence"]
        print(f"Decision: {result['action'].upper()}")
        print(f"  Score:      {result['score']} (threshold {args.threshold})")
        print(f"  Confidence: {c['level']} ({c['score']})")
        print(f"  Tier:       {c['tier']}")
        print(f"  Sigma:      {c['sigma']}")
        if c["outlier"]:
            print(f"  Outlier:    z={c['z_score']}")
        if c["reasons"]:
            print(f"  Reasons:    {'; '.join(c['reasons'])}")
        print(f"  Rationale:  {result['rationale']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
