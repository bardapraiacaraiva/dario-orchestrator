#!/usr/bin/env python3
"""
DARIO score_real_output — Score a real production output with the delivery-ready rubric.
========================================================================================

Scores a single real output (file or stdin) for a given skill using the
LLM-judge with the "delivery-ready" rubric (5 dims × 20 = 100), and
records the score in quality/skill-metrics.yaml under the skill's
`production_scores_delivery_ready` field.

This is the canonical way to push the `delivery_ready_rate` metric:
every time a skill output is delivered to a client, run it through this
script to capture the real quality measurement.

Usage:
    # From file
    python score_real_output.py --skill dario-brand --output ./out.md \
        --context "client briefing or context"

    # From stdin
    cat output.md | python score_real_output.py --skill dario-funnel \
        --context "..."

    # With explicit deliverable verdict (skip LLM judge)
    python score_real_output.py --skill dario-offer --output ./out.md \
        --context "..." --human-verdict yes --human-score 92

    # JSON output (for piping into automation)
    python score_real_output.py --skill X --output Y --json

Exit codes:
    0 = scored, deliverable=yes  (90+, no review needed)
    1 = error
    2 = scored, deliverable=needs-review  (70-89, senior review required)
    3 = scored, deliverable=no  (<70, rework needed)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
METRICS_PATH = ORCH / "quality" / "skill-metrics.yaml"

try:
    from ruamel.yaml import YAML
    _y = YAML()
    _y.preserve_quotes = True
    _y.width = 200

    def load_y(p):
        with open(p, encoding="utf-8") as f:
            return _y.load(f)

    def dump_y(d, p):
        with open(p, "w", encoding="utf-8") as f:
            _y.dump(d, f)
except ImportError:
    import yaml

    def load_y(p):
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def dump_y(d, p):
        with open(p, "w", encoding="utf-8") as f:
            yaml.safe_dump(d, f, sort_keys=False)


JUDGE_PROMPT = """Avalia este output usando rubric "delivery-ready" (consultor sénior).

SKILL: {skill}
CONTEXT: {context}

OUTPUT:
{output}

Pergunta CHAVE: "Entregaria isto ao cliente HOJE, com 0-1 ajustes menores?"

5 dimensoes (0-20 cada):

1. Specificity — usa dados concretos do contexto (nomes, valores, prazos)?
   18-20: cada afirmacao ancorada. 15-17: maioria. 12-14: estrutura ok.

2. Actionability — proximo passo claro?
   18-20: cliente sabe ja. 15-17: claro com 1 follow-up. 12-14: requer detalhe.

3. Completeness — TODOS os requisitos cobertos?
   18-20: 100%. 15-17: 80-95%. 12-14: 60-80%.

4. Accuracy — factos correctos?
   18-20: tudo verificavel. 15-17: 1-2 imprecisoes menores. 12-14: alguns erros.

5. Tone — formato adequado?
   18-20: tom profissional perfeito. 15-17: requer 1-2 ajustes. 12-14: requer polishing.

REGRA: Se entregarias AO CLIENTE com 0-1 ajustes menores, total >= 90.

Responde APENAS JSON:
{{"specificity": N, "actionability": N, "completeness": N, "accuracy": N, "tone": N, "total": SUM, "deliverable": "yes/needs-review/no", "reasoning": "1 frase justificando"}}"""


def llm_judge(skill: str, context: str, output: str, model: str = "claude-haiku-4-5") -> dict:
    """Run the LLM-judge delivery-ready rubric. Returns dict with score + verdict."""
    try:
        from anthropic import Anthropic
    except ImportError:
        raise RuntimeError("pip install anthropic — required for LLM-judge mode")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY not set in env")

    client = Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(
                skill=skill,
                context=context[:1500],
                output=output[:4000],
            ),
        }],
    )
    raw = resp.content[0].text.strip()
    m = re.search(r"\{[^{}]+\}", raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"Judge response did not contain JSON: {raw[:200]}")
    return json.loads(m.group(0))


def record_score(skill: str, score: int, deliverable: str, dims: dict,
                 context: str, output_preview: str) -> dict:
    """Append the score to the skill's metrics and recompute global delivery_ready_rate."""
    if not METRICS_PATH.exists():
        raise RuntimeError(f"Metrics not found at {METRICS_PATH}")

    metrics = load_y(METRICS_PATH)
    skills = metrics.setdefault("skills", {})

    meta = skills.setdefault(skill, {
        "avg_quality_score": None,
        "tier": "?",
        "total_executions": 0,
    })

    # Append to production scores (delivery-ready stream)
    prod_scores = meta.setdefault("production_scores_delivery_ready", [])
    prod_scores.append(score)
    meta["production_n_real_outputs"] = len(prod_scores)
    meta["production_avg_delivery_ready"] = round(sum(prod_scores) / len(prod_scores), 1)

    # Tally deliverable verdict
    if deliverable == "yes":
        meta["deliverable_yes_count"] = int(meta.get("deliverable_yes_count", 0)) + 1
    elif deliverable == "no":
        meta["deliverable_no_count"] = int(meta.get("deliverable_no_count", 0)) + 1
    else:
        meta["deliverable_needs_review_count"] = int(meta.get("deliverable_needs_review_count", 0)) + 1

    # Audit trail
    meta.setdefault("production_audit", []).append({
        "scored_at": datetime.now(UTC).isoformat(),
        "score": score,
        "deliverable": deliverable,
        "dims": dims,
        "context_preview": context[:120],
        "output_preview": output_preview[:120],
    })

    meta["last_scored_at"] = datetime.now(UTC).isoformat()

    # Update combined avg (80% production + 20% synthetic if both)
    syn = meta.get("avg_quality_score")
    prod = meta["production_avg_delivery_ready"]
    if syn is not None:
        combined = 0.8 * prod + 0.2 * float(syn)
    else:
        combined = prod
    meta["avg_quality_score"] = round(combined, 1)
    meta["tier"] = "A" if combined >= 90 else "B" if combined >= 70 else "C"

    # Recompute global metrics
    all_scored = [
        (n, float(m.get("avg_quality_score", 0)))
        for n, m in skills.items()
        if isinstance(m, dict) and m.get("avg_quality_score") is not None
    ]
    if all_scored:
        metrics["global_avg_quality"] = round(
            sum(s for _, s in all_scored) / len(all_scored), 1
        )

    # Delivery-ready rate (NEW first-class metric)
    delivery_yes = sum(int(m.get("deliverable_yes_count", 0)) for n, m in skills.items() if isinstance(m, dict))
    delivery_total = sum(int(m.get("production_n_real_outputs", 0)) for n, m in skills.items() if isinstance(m, dict))
    delivery_rate = (100.0 * delivery_yes / delivery_total) if delivery_total else 0.0
    metrics["delivery_ready_rate_pct"] = round(delivery_rate, 1)
    metrics["delivery_ready_yes_count"] = delivery_yes
    metrics["delivery_ready_total"] = delivery_total

    metrics["last_updated"] = datetime.now(UTC).isoformat()
    dump_y(metrics, METRICS_PATH)

    return {
        "skill": skill,
        "score": score,
        "deliverable": deliverable,
        "combined_avg": combined,
        "global_avg_quality": metrics.get("global_avg_quality"),
        "delivery_ready_rate_pct": metrics["delivery_ready_rate_pct"],
        "delivery_ready_total": delivery_total,
        "delivery_ready_yes": delivery_yes,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Score a real output with the delivery-ready rubric.")
    p.add_argument("--skill", required=True, help="Skill name (e.g. dario-brand)")
    p.add_argument("--output", help="Path to output file. If omitted, reads from stdin.")
    p.add_argument("--context", default="", help="Briefing / context for the output.")
    p.add_argument("--model", default="claude-haiku-4-5", help="Judge model (default: claude-haiku-4-5)")
    p.add_argument("--human-verdict", choices=["yes", "needs-review", "no"],
                   help="Skip LLM-judge and use this verdict (also requires --human-score)")
    p.add_argument("--human-score", type=int, help="Score 0-100, only used with --human-verdict")
    p.add_argument("--no-queue", action="store_true",
                   help="Skip auto-routing to human review queue when score < 90")
    p.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = p.parse_args()

    # Read output
    if args.output:
        output_text = Path(args.output).read_text(encoding="utf-8")
    else:
        output_text = sys.stdin.read()

    if not output_text.strip():
        print("error: output is empty", file=sys.stderr)
        return 1

    # Score
    if args.human_verdict:
        if args.human_score is None:
            print("error: --human-verdict requires --human-score", file=sys.stderr)
            return 1
        sd = {
            "specificity": None, "actionability": None, "completeness": None,
            "accuracy": None, "tone": None,
            "total": args.human_score,
            "deliverable": args.human_verdict,
            "reasoning": "(human-provided verdict)",
        }
    else:
        try:
            sd = llm_judge(args.skill, args.context, output_text, args.model)
        except Exception as e:
            print(f"error: judge failed: {e}", file=sys.stderr)
            return 1

    score = int(sd.get("total") or sum(sd.get(d, 0) or 0 for d in
                ("specificity", "actionability", "completeness", "accuracy", "tone")))
    verdict = sd.get("deliverable", "needs-review")
    dims = {k: sd.get(k) for k in
            ("specificity", "actionability", "completeness", "accuracy", "tone")}

    # Record
    result = record_score(args.skill, score, verdict, dims, args.context, output_text)

    # Auto-route to human review queue if score < 90 (and not human-verdict)
    queue_id = None
    if score < 90 and not args.human_verdict and not args.no_queue:
        try:
            import subprocess
            queue_script = ORCH / "human_review_queue.py"
            if queue_script.exists():
                # Write output to a temp file for the queue tool
                import tempfile
                with tempfile.NamedTemporaryFile(mode="w", suffix=".md",
                                                  delete=False, encoding="utf-8") as tmp:
                    tmp.write(output_text)
                    tmp_path = tmp.name
                queue_proc = subprocess.run(
                    [sys.executable, str(queue_script), "--add",
                     "--skill", args.skill,
                     "--output", tmp_path,
                     "--context", args.context,
                     "--ai-score", str(score),
                     "--ai-verdict", verdict,
                     "--ai-reasoning", sd.get("reasoning", "")[:200]],
                    capture_output=True, text=True, timeout=15,
                )
                # Parse id from output
                m = re.search(r"id=(\w+)", queue_proc.stdout)
                if m:
                    queue_id = m.group(1)
                Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            pass  # fail-soft: queue is bonus, not blocking

    # Report
    if args.json:
        print(json.dumps({**result, "dims": dims, "reasoning": sd.get("reasoning", ""),
                          "queue_id": queue_id}, indent=2))
    else:
        emoji = "OK" if verdict == "yes" else "REVIEW" if verdict == "needs-review" else "REWORK"
        print(f"[{emoji}] {args.skill}: {score}/100 — {verdict}")
        print(f"  Skill avg (combined): {result['combined_avg']:.1f}")
        print(f"  Global avg quality:   {result['global_avg_quality']:.1f}")
        print(f"  Delivery-ready rate:  {result['delivery_ready_rate_pct']:.1f}% ({result['delivery_ready_yes']}/{result['delivery_ready_total']})")
        if sd.get("reasoning"):
            print(f"  Reasoning: {sd['reasoning']}")
        if queue_id:
            print(f"  Queued for review: id={queue_id}")
            print(f"  After editing: python human_review_queue.py --resolved {queue_id} --polished-score N")

    # Exit codes mapped to verdict
    return 0 if verdict == "yes" else 2 if verdict == "needs-review" else 3


if __name__ == "__main__":
    sys.exit(main())
