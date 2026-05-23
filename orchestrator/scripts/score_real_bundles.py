"""Score 4 real multi-skill bundles already in Obsidian.

These are deliverables that were assembled across multiple skills for a
single client engagement. Scoring at bundle-level is the structural test
of whether the bundle metric unlocks delivery-ready >90% genuinely.

Bundles tested:
  1. LUCAS strategic (5 components — pipeline + benchmark + pricing + proposal)
  2. Atrium audit (2 components — SEO + URLs map)
  3. ARRECADA.GOV (3 components — analysis + pitch + roadmap)
  4. Cuidai Wave 0 (5 components — brand + design + bootstrap + handoff + burden)

Run:
    python scripts/score_real_bundles.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
OBS = Path.home() / "OneDrive" / "Documents" / "D.A.R.I.O" / "05 - Claude - IA" / "Outputs"


BUNDLES = [
    {
        "name": "lucas-strategy-q2",
        "context": ("LUCAS / LUSOconta — SaaS contabilidade PT, target contabilistas + PMEs 50-250. "
                    "Competidores Moloni/SAGE. Bundle: benchmark + plano estratégico + pricing + proposta comercial."),
        "components": [
            ("dario-pipeline", "2026-04-02 - Benchmark Competitivo - LUCAS vs Mercado PT e EU com Faturacao.md"),
            ("dario-pipeline", "2026-04-02 - LUCAS + LUSACONTA - Plano Estrategico para Lider Europeu.md"),
            ("dario-financial-model", "2026-04-02 - LUCAS + LUSACONTA - Pricing Real e Estrategia de Expansao.md"),
            ("dario-proposal", "2026-04-02 - LUCAS + LUSACONTA - Proposta Comercial com Custos Reais.md"),
        ],
    },
    {
        "name": "atrium-site-audit-q1",
        "context": ("Atrium Golden Visa — target HNW US investors em PT golden visa €500K. "
                    "Bundle: audit SEO + mapa URLs estrutural."),
        "components": [
            ("seo-audit", "2026-03-30 - Atrium - CTA Fix + SEO Audit Homepage.md"),
            ("seo-sitemap", "2026-03-30 - Atrium - Mapa Completo URLs.md"),
        ],
    },
    {
        "name": "arrecada-gov-pitch-bundle",
        "context": ("ARRECADA.GOV — SaaS B2G recuperação dívida ativa municipal com IA. "
                    "Success fee 12%. Bundle: análise POC + pitch parceiros + roadmap aprovado."),
        "components": [
            ("dario-diagnose", "2026-05-21 - ARRECADA.GOV - Analise POC Sorocaba + Roadmap Evolucao.md"),
            ("dario-pitch", "2026-05-21 - ARRECADA.GOV - Pitch Parceiros 9 Slides.md"),
            ("dario-produto", "2026-05-21 - ARRECADA.GOV - Roadmap Aprovado (5 Features + 4 GAPs).md"),
        ],
    },
    {
        "name": "cuidai-wave0-foundation",
        "context": ("Cuidaí BR — plataforma caregiver multigeracional. MVP fork SAQUEI. Capital R$ 100K split. "
                    "Bundle Wave 0: brand identity + design tokens + bootstrap kit + handoff founder + burden index."),
        "components": [
            ("dario-brand", "2026-05-18 - Cuidai - CUI-014 Brand Identity Workshop.md"),
            ("diva-materials", "2026-05-18 - Cuidai - CUI-015 Design Tokens Tailwind.md"),
            ("dario-client-onboard", "2026-05-18 - Cuidai - CUI-018 Bootstrap Kit Day 0.md"),
            ("dario-proposal", "2026-05-18 - Cuidai - HANDOFF BRIEF Founder.md"),
            ("dario-produto", "2026-05-19 - Cuidai - CUI-046 Burden Index Algorithm.md"),
        ],
    },
]


def score_one_bundle(b):
    args = [
        sys.executable, str(ORCH / "score_bundle.py"),
        "--bundle-name", b["name"],
        "--context", b["context"],
        "--json",
    ]
    for skill, fname in b["components"]:
        path = OBS / fname
        if not path.exists():
            return {"error": f"missing file: {fname}"}
        args.extend(["--skill", skill, "--output", str(path)])

    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=180, cwd=str(ORCH))
        # Parse JSON from stdout
        m = re.search(r"\{[\s\S]+\}", out.stdout)
        if m:
            return json.loads(m.group(0))
        return {"error": f"no JSON in output", "stdout": out.stdout[:300], "stderr": out.stderr[:300]}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}


def main():
    print(f"=== Scoring {len(BUNDLES)} real multi-skill bundles ===\n")
    results = []
    for i, b in enumerate(BUNDLES, 1):
        print(f"[{i}/{len(BUNDLES)}] {b['name']}  ({len(b['components'])} components)")
        r = score_one_bundle(b)
        if "error" in r:
            print(f"  → ERROR: {r['error']}")
        else:
            print(f"  → {r.get('score')}/100 [{r.get('verdict')}]  weakest={r.get('weakest_component')}")
            print(f"    bundle_delivery_rate={r.get('bundle_delivery_rate_pct')}%  ({r.get('bundles_yes')}/{r.get('bundles_total')})")
        results.append({**b, **r})

    # Summary
    ok = [r for r in results if "score" in r]
    yes = [r for r in ok if r.get("verdict") == "yes"]
    review = [r for r in ok if r.get("verdict") == "needs-review"]
    no = [r for r in ok if r.get("verdict") == "no"]
    print(f"\n=== Summary ===")
    print(f"  Scored: {len(ok)}/{len(results)}")
    print(f"  Yes:    {len(yes)}")
    print(f"  Review: {len(review)}")
    print(f"  No:     {len(no)}")
    if ok:
        avg = sum(r["score"] for r in ok) / len(ok)
        print(f"  Avg:    {avg:.1f}/100")
        print(f"\n  Bundle-level vs single-skill comparison:")
        print(f"    Single-skill avg:  83.5 (mean across 55 outputs)")
        print(f"    Single-skill yes:  14.5% (8/55)")
        print(f"    BUNDLE avg:        {avg:.1f}")
        print(f"    BUNDLE yes:        {100*len(yes)/len(ok):.1f}% ({len(yes)}/{len(ok)})")


if __name__ == "__main__":
    main()
