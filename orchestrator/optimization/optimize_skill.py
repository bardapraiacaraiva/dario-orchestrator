"""DSPy optimization runner (Onda 4 #5 pilot).

Compiles a DSPy Program against a metric using BootstrapFewShot. Saves
the compiled program (instructions + selected demos) to disk so callers
can load it later without re-running the optimisation.

Usage:
    python -m optimization.optimize_skill dario-brand
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import dspy

from optimization.evals import brand_score, load_brand_examples
from optimization.programs import BrandPositioningProgram

COMPILED_DIR = ORCH_DIR / "optimization" / "compiled"


def configure_lm(provider: str = "anthropic", model: str = "claude-haiku-4-5"):
    """Configure DSPy's default language model.

    Defaults to Haiku for cost efficiency during compilation (BootstrapFewShot
    can issue ~50 LM calls).
    """
    if provider == "anthropic":
        lm = dspy.LM(f"anthropic/{model}", max_tokens=2000, temperature=0.2)
    else:
        lm = dspy.LM(model)
    dspy.configure(lm=lm)


def compile_brand(min_examples: int = 2) -> dict[str, Any]:
    """Compile BrandPositioningProgram against existing goldens.

    Returns a small report with the example count, baseline vs compiled
    metric, and the path to the saved compiled program.
    """
    examples = load_brand_examples()
    if len(examples) < min_examples:
        return {
            "compiled": False,
            "reason": f"only {len(examples)} brand goldens — need at least {min_examples}",
            "examples_found": len(examples),
        }

    student = BrandPositioningProgram()

    # Baseline score on the dataset before optimisation
    baseline_scores: list[float] = []
    for ex in examples:
        try:
            pred = student(briefing=ex.briefing)
            baseline_scores.append(brand_score(ex, pred))
        except Exception:
            baseline_scores.append(0.0)
    baseline_avg = sum(baseline_scores) / max(len(baseline_scores), 1)

    # Compile with BootstrapFewShot
    optimizer = dspy.BootstrapFewShot(
        metric=brand_score,
        max_bootstrapped_demos=min(4, len(examples) - 1),
        max_labeled_demos=min(4, len(examples)),
    )
    compiled = optimizer.compile(student=student, trainset=examples)

    # Score after compilation
    compiled_scores: list[float] = []
    for ex in examples:
        try:
            pred = compiled(briefing=ex.briefing)
            compiled_scores.append(brand_score(ex, pred))
        except Exception:
            compiled_scores.append(0.0)
    compiled_avg = sum(compiled_scores) / max(len(compiled_scores), 1)

    # Persist the compiled program
    COMPILED_DIR.mkdir(parents=True, exist_ok=True)
    save_path = COMPILED_DIR / "brand_positioning.json"
    try:
        compiled.save(str(save_path))
    except Exception as e:
        return {
            "compiled": False,
            "reason": f"save failed: {e}",
            "examples": len(examples),
            "baseline_avg": round(baseline_avg, 3),
            "compiled_avg": round(compiled_avg, 3),
        }

    return {
        "compiled": True,
        "skill": "dario-brand",
        "examples": len(examples),
        "baseline_avg": round(baseline_avg, 3),
        "compiled_avg": round(compiled_avg, 3),
        "uplift": round(compiled_avg - baseline_avg, 3),
        "saved_to": str(save_path),
    }


def main():
    parser = argparse.ArgumentParser(
        description="DSPy optimization runner for DARIO skills"
    )
    parser.add_argument(
        "skill",
        default="dario-brand",
        nargs="?",
        help="Skill to compile (only `dario-brand` supported in the pilot)",
    )
    parser.add_argument(
        "--provider", default="anthropic", choices=["anthropic", "openai", "ollama"]
    )
    parser.add_argument("--model", default="claude-haiku-4-5")
    parser.add_argument("--dry-run", action="store_true",
                        help="Skip the LM and just report dataset stats.")
    args = parser.parse_args()

    if args.skill != "dario-brand":
        print(f"[ERR] Pilot only supports dario-brand. Got: {args.skill}")
        return 1

    if args.dry_run:
        examples = load_brand_examples()
        print(json.dumps({"examples_found": len(examples)}, indent=2))
        return 0

    configure_lm(args.provider, args.model)
    report = compile_brand()
    print(json.dumps(report, indent=2))
    return 0 if report.get("compiled") else 1


if __name__ == "__main__":
    sys.exit(main())
