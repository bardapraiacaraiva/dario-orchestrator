"""Sprint 3 v2 — DSPy compile with JUDGE-based metric (root-cause fix).

ROOT CAUSE (compile_sprint3.py v1):
    generic_text_score() used word-overlap on a SINGLE field. This rewards
    lexical repetition (template-matching), not output quality. Bootstrap
    selected demos that maximized overlap → forced lexical convergence on
    golden vocabulary → ZERO generalization to new verticals.

    Result: dario-brand worked (tight `posicionamento` field), but
    offer/funnel/pitch failed (broad fields, vertical-specific vocab).

FIX (this file):
    Use the JUDGE prompt (Haiku 4.5, 5-dim rubric 0-100) as the DSPy metric.
    The optimizer now bootstraps demos that maximize JUDGED quality, not
    lexical similarity. Demos that generalize well get higher scores
    regardless of vocab overlap.

    Trade-off: ~10x metric cost ($0.05 → $0.50/compile) but real quality lift
    instead of overfitting.

Run:
    python -m optimization.compile_sprint3_v2

Estimated cost: ~$1.50 (3 compiles × 3 demos × judge eval + 3 final evals).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ORCH_DIR))

import dspy
from dspy.teleprompt import BootstrapFewShot

from scripts.anthropic_spend_wrapper import TrackedAnthropic

from optimization.compile_sprint3 import (
    FUNNEL_GOLDENS,
    OFFER_GOLDENS,
    PITCH_GOLDENS,
    FunnelDesignProgram,
    OfferGenerationProgram,
    PitchDeckProgram,
)

try:
    from ruamel.yaml import YAML
    _y = YAML(); _y.preserve_quotes = True; _y.width = 200
    def load_y(p):
        with open(p, encoding='utf-8') as f: return _y.load(f)
    def dump_y(d, p):
        with open(p, 'w', encoding='utf-8') as f: _y.dump(d, f)
except ImportError:
    import yaml
    def load_y(p):
        with open(p, encoding='utf-8') as f: return yaml.safe_load(f)
    def dump_y(d, p):
        with open(p, 'w', encoding='utf-8') as f: yaml.safe_dump(d, f, sort_keys=False)


# Module-level shared client (avoid re-creating per metric call)
_JUDGE_CLIENT = None

JUDGE_PROMPT = """Avalia este output em 5 dimensoes (0-20 cada, total 0-100):

SKILL: {skill}
BRIEFING: {briefing}

OUTPUT:
{output}

RUBRIC:
1. Specificity (0-20) - dados concretos do briefing referenced?
2. Actionability (0-20) - proximos passos sem ambiguidade?
3. Completeness (0-20) - todos os campos preenchidos com substancia?
4. Accuracy (0-20) - factos verificaveis e correctos?
5. Tone (0-20) - formato adequado ao deliverable?

Responde APENAS JSON:
{{"specificity": N, "actionability": N, "completeness": N, "accuracy": N, "tone": N, "total": SUM, "reasoning": "1 frase"}}"""


def _get_judge_client():
    global _JUDGE_CLIENT
    if _JUDGE_CLIENT is None:
        _JUDGE_CLIENT = TrackedAnthropic(caller="dspy/compile_sprint3_v2")
    return _JUDGE_CLIENT


def _render_output(pred) -> str:
    """Concat all relevant pred fields into a single text block for the judge."""
    parts = []
    for attr in ("core_offer", "value_equation", "risk_reversal", "bonuses",
                 "urgency", "stages", "conversion_thresholds", "copy_hooks",
                 "automations", "narrative_arc", "key_slides", "tam_sam_som",
                 "financial_ask"):
        v = getattr(pred, attr, None)
        if v:
            if isinstance(v, list):
                v = "\n".join(str(x) for x in v)
            parts.append(f"{attr}:\n{v}")
    return "\n\n".join(parts)


def make_judge_metric(skill_name: str):
    """Returns a DSPy metric closure that scores via JUDGE (0.0-1.0 normalized).

    DSPy expects metrics in [0,1] for BootstrapFewShot selection. We normalize
    judge score /100 → /1.0.
    """
    def judge_metric(example, pred, trace=None) -> float:
        if pred is None:
            return 0.0
        output_text = _render_output(pred)
        if not output_text:
            return 0.0
        client = _get_judge_client()
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5", max_tokens=400,
                messages=[{"role": "user", "content": JUDGE_PROMPT.format(
                    skill=skill_name,
                    briefing=getattr(example, "briefing", "")[:1000],
                    output=output_text[:3500],
                )}],
            )
            raw = resp.content[0].text.strip()
            m = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
            if not m:
                return 0.5  # neutral on parse failure
            sd = json.loads(m.group(0))
            total = sd.get("total") or sum(sd.get(d, 0) for d in
                ("specificity", "actionability", "completeness", "accuracy", "tone"))
            return min(max(float(total) / 100.0, 0.0), 1.0)
        except Exception as e:
            print(f"  [judge_metric error: {e}]")
            return 0.5
    return judge_metric


SKILLS = [
    ("dario-offer", OfferGenerationProgram, OFFER_GOLDENS),
    ("dario-funnel", FunnelDesignProgram, FUNNEL_GOLDENS),
    ("dario-pitch", PitchDeckProgram, PITCH_GOLDENS),
]


def compile_and_eval(skill_name, ProgramCls, goldens):
    print(f"\n=== Compiling {skill_name} (v2: judge-metric) ===")
    teleprompter = BootstrapFewShot(
        metric=make_judge_metric(skill_name),
        max_bootstrapped_demos=2,
        max_labeled_demos=2,
        max_rounds=1,
    )
    base = ProgramCls()
    compiled = teleprompter.compile(base, trainset=goldens)

    # Save artifact
    compiled_path = ORCH_DIR / "optimization" / "compiled" / f"{skill_name}_v2.json"
    compiled_path.parent.mkdir(parents=True, exist_ok=True)
    compiled.save(str(compiled_path))
    print(f"  saved: {compiled_path.relative_to(ORCH_DIR)}")

    # Live re-eval with judge on the same goldens (sanity check)
    print(f"  re-evaluating with judge on {len(goldens)} briefings...")
    scores = []
    judge = make_judge_metric(skill_name)
    for g in goldens:
        pred = compiled(briefing=g.briefing)
        score_normalized = judge(g, pred)
        score_100 = round(score_normalized * 100)
        scores.append(score_100)
        print(f"    score={score_100}/100")
    avg = sum(scores) / len(scores)
    print(f"  avg compiled (v2): {avg:.1f}/100")
    return scores, avg


def main():
    # Configure DSPy LM
    lm = dspy.LM("anthropic/claude-haiku-4-5", max_tokens=2000, temperature=0.2)
    dspy.configure(lm=lm)

    # Compile + eval each
    results = {}
    for skill_name, ProgramCls, goldens in SKILLS:
        scores, avg = compile_and_eval(skill_name, ProgramCls, goldens)
        results[skill_name] = {"scores": scores, "avg": avg}

    # Update metrics — CRITICAL: do NOT overwrite avg_quality_score.
    # avg_quality_score represents real production quality (delivery-ready outputs
    # scored on actual client work). Judge-on-synthetic-goldens is a DIFFERENT
    # signal — it measures raw model output on training briefings, which is
    # apples-vs-oranges to production. Conflating these (v2-pre-fix) caused the
    # spurious "regression" 90.9 → 84.3 on dario-pitch.
    #
    # This pass writes ONLY synthetic-golden fields. Production fields untouched.
    metrics_path = ORCH_DIR / "quality" / "skill-metrics.yaml"
    metrics = load_y(metrics_path)
    print("\n=== Updating skill-metrics.yaml (synthetic-golden fields only) ===")
    for skill_name, data in results.items():
        if skill_name not in metrics["skills"]:
            print(f"  ! {skill_name} not in metrics; skipping")
            continue
        meta = metrics["skills"][skill_name]
        prev_judge = meta.get("avg_judge_synthetic_goldens")
        new = data["avg"]
        # Synthetic-golden tracking fields (new namespace, do NOT touch avg_quality_score)
        meta["live_scores_compiled_sprint3v2"] = data["scores"]
        meta["avg_judge_synthetic_goldens"] = round(new, 1)
        meta["compile_artifact_v2"] = f"optimization/compiled/{skill_name}_v2.json"
        meta["last_judge_synthetic_at"] = datetime.now(UTC).isoformat()
        # Append history note (production avg_quality unaffected)
        meta.setdefault("score_history", []).append({
            "date": datetime.now(UTC).isoformat()[:10],
            "judge_synthetic_old": prev_judge,
            "judge_synthetic_new": round(new, 1),
            "briefing_quality": "sprint3v2-dspy-judge-metric",
            "note": "synthetic-goldens only; production avg_quality_score untouched",
        })
        prev_str = f"{prev_judge}" if prev_judge is not None else "n/a"
        print(f"  {skill_name}: judge_synthetic {prev_str} -> {new:.1f}")
        prod = meta.get("avg_quality_score")
        if prod is not None:
            print(f"    (production avg_quality_score preserved: {prod})")

    metrics["last_updated"] = datetime.now(UTC).isoformat()

    # Global average remains based on production avg_quality_score (unchanged semantics)
    scored = [(n, float(m.get("avg_quality_score", 0)))
              for n, m in metrics["skills"].items()
              if isinstance(m, dict) and m.get("avg_quality_score") is not None]
    if scored:
        all_avg = sum(s for _, s in scored) / len(scored)
        metrics["global_avg_quality"] = round(all_avg, 1)
        A = sum(1 for _, s in scored if s >= 90)
        B = sum(1 for _, s in scored if 70 <= s < 90)
        print(f"\n=== Global mean (production avg_quality_score): {all_avg:.2f}")
        print(f"  A (>=90): {A}  |  B (70-89): {B}")

    dump_y(metrics, metrics_path)
    print("\nOK skill-metrics.yaml updated (synthetic-golden fields only)")


if __name__ == "__main__":
    main()
