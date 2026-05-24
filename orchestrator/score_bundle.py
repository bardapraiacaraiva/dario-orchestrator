#!/usr/bin/env python3
"""
DARIO score_bundle — Score a multi-skill deliverable bundle with one rubric pass.
=================================================================================

Single-skill outputs hit a structural ceiling at ~88-89 because the
delivery-ready judge consistently asks for follow-on deliverables that
belong to OTHER skills (e.g., dario-brand output marked "needs-review"
because it lacks visual roadmap + message matrix — which are
diva-moodboard / dario-content territory).

This script scores a BUNDLE as a single deliverable. The bundle
combines multiple skill outputs (brand + visual + content + pitch, for
example) into one client-facing package. The judge evaluates the bundle
as a whole — which is how the client actually receives value.

Usage:
    # YAML-defined bundle
    python score_bundle.py --bundle bundle.yaml --context "..."

    # Inline file list
    python score_bundle.py \
        --skill dario-brand --output ./brand.md \
        --skill diva-moodboard --output ./moodboard.md \
        --skill dario-content --output ./content.md \
        --context "Atrium rebrand bundle Q3 2026" \
        --bundle-name "atrium-rebrand-q3"

    # JSON output
    python score_bundle.py ... --json

The bundle gets recorded into quality/skill-metrics.yaml under
`bundles:` section + the top-level `bundle_delivery_rate_pct` metric.

Bundle YAML format:
    bundle_name: atrium-rebrand-q3
    context: "Atrium Golden Visa rebrand — HNW Americans investing PT"
    components:
      - skill: dario-brand
        output: ./atrium-brand.md
      - skill: diva-moodboard
        output: ./atrium-moodboard.md
      - skill: dario-content
        output: ./atrium-content-plan.md

Exit codes:
    0 = bundle scored, deliverable=yes
    1 = error
    2 = bundle scored, deliverable=needs-review
    3 = bundle scored, deliverable=no
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


BUNDLE_JUDGE_PROMPT = """Avalia este BUNDLE multi-skill usando rubric "delivery-ready" sénior.

CONTEXT (cliente, projecto, target): {context}

BUNDLE NAME: {bundle_name}
COMPONENTS ({n_components} skills): {skill_list}

BUNDLE CONTENT (cada componente delimitado):
{bundle_text}

Pergunta CHAVE: "Entregaria este BUNDLE ao cliente hoje, com 0-1 ajustes menores?"

Um bundle multi-skill é mais do que a soma das partes. Avalia se:
- Os componentes formam um deliverable COESO (não 3 docs soltos)
- Há continuidade entre brand → visual → message → activation
- Cliente entende o conjunto sem precisar de explicação adicional
- Cada componente referencia os outros onde apropriado

5 dimensoes (0-20 cada):

1. Specificity — bundle usa dados concretos do contexto consistentemente?
   18-20: cada componente ancorado no mesmo cliente/dados
   15-17: maioria ancorado, 1 componente genérico
   12-14: ancoragem irregular entre componentes

2. Coherence — os componentes formam um conjunto coeso?
   18-20: brand→visual→content→activation flui sem gaps
   15-17: 1 gap menor entre componentes
   12-14: componentes parecem 3 docs separados

3. Completeness — bundle entrega o que o cliente precisa para activar?
   18-20: cliente pode lançar imediatamente
   15-17: cliente precisa de 1 follow-up para activar
   12-14: cliente precisa de 2-3 deliverables adicionais

4. Accuracy — factos/recomendações verificáveis e correctos across components?
   18-20: tudo verificável + sem contradições entre componentes
   15-17: 1-2 imprecisões menores
   12-14: 1 contradição entre componentes

5. Tone — voice consistente across components + format adequado?
   18-20: voice é o mesmo em todos os 3+ componentes
   15-17: 1 componente desviado
   12-14: voice irregular

REGRA: Se entregarias O BUNDLE INTEIRO ao cliente com 0-1 ajustes, total >= 90.

Responde APENAS JSON:
{{"specificity": N, "coherence": N, "completeness": N, "accuracy": N, "tone": N, "total": SUM, "deliverable": "yes/needs-review/no", "reasoning": "1 frase justificando", "weakest_component": "nome-skill ou nenhum"}}"""


def load_bundle_from_yaml(path: Path) -> dict:
    return load_y(path)


def build_bundle_text(components: list[dict]) -> tuple[str, list[str]]:
    """Concatenate component outputs with clear delimiters. Returns
    (bundle_text, list_of_skill_names)."""
    parts = []
    skills = []
    for c in components:
        skill = c["skill"]
        skills.append(skill)
        path = Path(c["output"])
        if not path.exists():
            parts.append(f"### {skill}\n[FILE NOT FOUND: {path}]\n")
            continue
        content = path.read_text(encoding="utf-8")
        # Truncate per-component to keep total under ~12K chars
        max_per = 4500 // max(len(components), 1)
        parts.append(f"### COMPONENT: {skill}\n{content[:max_per]}\n")
    return "\n---\n".join(parts), skills


def judge_bundle(bundle_name: str, context: str, components: list[dict],
                 model: str = "claude-haiku-4-5") -> dict:
    try:
        from scripts.anthropic_spend_wrapper import TrackedAnthropic
    except ImportError:
        raise RuntimeError("pip install anthropic — required for LLM-judge")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    bundle_text, skills = build_bundle_text(components)
    client = TrackedAnthropic(caller="score_bundle")
    resp = client.messages.create(
        model=model,
        max_tokens=900,
        messages=[{
            "role": "user",
            "content": BUNDLE_JUDGE_PROMPT.format(
                context=context[:1500],
                bundle_name=bundle_name,
                n_components=len(components),
                skill_list=", ".join(skills),
                bundle_text=bundle_text[:12000],
            ),
        }],
    )
    raw = resp.content[0].text.strip()
    m = re.search(r"\{[^{}]+\}", raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"Judge response did not contain JSON: {raw[:200]}")
    return json.loads(m.group(0))


def record_bundle(bundle_name: str, score: int, verdict: str, dims: dict,
                  components: list[dict], context: str, weakest: str) -> dict:
    """Record bundle into metrics under `bundles:` section."""
    if not METRICS_PATH.exists():
        raise RuntimeError(f"Metrics not found at {METRICS_PATH}")

    metrics = load_y(METRICS_PATH)
    bundles = metrics.setdefault("bundles", {})

    entry = bundles.setdefault(bundle_name, {
        "name": bundle_name,
        "scores": [],
        "components": [c["skill"] for c in components],
        "first_scored_at": datetime.now(UTC).isoformat(),
    })
    entry["scores"].append({
        "scored_at": datetime.now(UTC).isoformat(),
        "score": score,
        "verdict": verdict,
        "dims": dims,
        "context_preview": context[:120],
        "weakest_component": weakest,
    })
    entry["last_scored_at"] = datetime.now(UTC).isoformat()
    entry["latest_score"] = score
    entry["latest_verdict"] = verdict

    # Recompute global bundle metrics
    all_bundles = []
    for name, b in bundles.items():
        if isinstance(b, dict) and b.get("scores"):
            latest = b["scores"][-1]
            all_bundles.append({
                "name": name,
                "score": latest["score"],
                "verdict": latest["verdict"],
            })

    total = len(all_bundles)
    yes = sum(1 for b in all_bundles if b["verdict"] == "yes")
    review = sum(1 for b in all_bundles if b["verdict"] == "needs-review")
    no_b = sum(1 for b in all_bundles if b["verdict"] == "no")
    avg = round(sum(b["score"] for b in all_bundles) / total, 1) if total else 0

    metrics["bundle_delivery_rate_pct"] = round(100.0 * yes / total, 1) if total else 0
    metrics["bundle_avg_score"] = avg
    metrics["bundles_total"] = total
    metrics["bundles_yes"] = yes
    metrics["bundles_needs_review"] = review
    metrics["bundles_no"] = no_b
    metrics["last_updated"] = datetime.now(UTC).isoformat()

    dump_y(metrics, METRICS_PATH)

    return {
        "bundle_name": bundle_name,
        "score": score,
        "verdict": verdict,
        "weakest_component": weakest,
        "bundle_delivery_rate_pct": metrics["bundle_delivery_rate_pct"],
        "bundle_avg_score": avg,
        "bundles_total": total,
        "bundles_yes": yes,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Score a multi-skill bundle.")
    p.add_argument("--bundle", help="Path to bundle.yaml")
    p.add_argument("--bundle-name", help="Name (used when not from YAML)")
    p.add_argument("--context", default="", help="Client/project context")
    p.add_argument("--skill", action="append", default=[],
                   help="Skill name (use multiple times paired with --output)")
    p.add_argument("--output", action="append", default=[],
                   help="Output file path (paired with --skill)")
    p.add_argument("--model", default="claude-haiku-4-5", help="Judge model")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.bundle:
        bundle = load_bundle_from_yaml(Path(args.bundle))
        bundle_name = bundle.get("bundle_name") or Path(args.bundle).stem
        context = bundle.get("context", "")
        components = bundle.get("components", [])
    else:
        if not args.skill or len(args.skill) != len(args.output):
            print("error: --skill and --output must be paired (same count)", file=sys.stderr)
            return 1
        bundle_name = args.bundle_name or f"adhoc-{datetime.now(UTC).strftime('%Y%m%d-%H%M')}"
        context = args.context
        components = [{"skill": s, "output": o} for s, o in zip(args.skill, args.output)]

    if not components:
        print("error: no components in bundle", file=sys.stderr)
        return 1

    print(f"Bundle: {bundle_name}")
    print(f"  components: {len(components)}")
    for c in components:
        print(f"    - {c['skill']:25s}  {c['output']}")

    try:
        sd = judge_bundle(bundle_name, context, components, args.model)
    except Exception as e:
        print(f"error: judge failed: {e}", file=sys.stderr)
        return 1

    dims = ("specificity", "coherence", "completeness", "accuracy", "tone")
    score = int(sd.get("total") or sum(sd.get(d, 0) or 0 for d in dims))
    verdict = sd.get("deliverable", "needs-review")
    weakest = sd.get("weakest_component", "?")
    dim_scores = {k: sd.get(k) for k in dims}

    result = record_bundle(bundle_name, score, verdict, dim_scores, components,
                           context, weakest)

    if args.json:
        print(json.dumps({**result, "dims": dim_scores,
                          "reasoning": sd.get("reasoning", "")}, indent=2))
    else:
        emoji = "OK" if verdict == "yes" else "REVIEW" if verdict == "needs-review" else "REWORK"
        print(f"\n[{emoji}] {bundle_name}: {score}/100 — {verdict}")
        print(f"  Dims: {' '.join(f'{k[:4]}={v}' for k, v in dim_scores.items())}")
        if weakest and weakest != "nenhum":
            print(f"  Weakest component: {weakest}")
        print(f"\n  Bundle delivery rate: {result['bundle_delivery_rate_pct']:.1f}%  ({result['bundles_yes']}/{result['bundles_total']})")
        print(f"  Bundle avg score:     {result['bundle_avg_score']}")
        if sd.get("reasoning"):
            print(f"  Reasoning: {sd['reasoning']}")

    return 0 if verdict == "yes" else 2 if verdict == "needs-review" else 3


if __name__ == "__main__":
    sys.exit(main())
