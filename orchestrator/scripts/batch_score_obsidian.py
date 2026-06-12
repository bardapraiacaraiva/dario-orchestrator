"""Batch-score 20 real Obsidian outputs to grow the production dataset.

Each output is mapped to its likely skill based on filename pattern.
Uses LLM-judge with delivery-ready rubric. Updates skill-metrics.yaml.

Run:
    python scripts/batch_score_obsidian.py            # full batch
    python scripts/batch_score_obsidian.py --dry-run  # show what would score
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
OBS = Path.home() / "OneDrive" / "Documents" / "D.A.R.I.O" / "05 - Claude - IA" / "Outputs"

# Curated list — real outputs with clear skill mapping
# Format: (filename, skill, context)
BATCH = [
    # === Batch 1 (already scored 2026-05-23) ===
    ("2026-03-30 - Atrium - CTA Fix + SEO Audit Homepage.md", "seo-audit",
     "Audit SEO + CTA fix Atrium Golden Visa homepage. Target HNW US investors."),
    ("2026-03-30 - Atrium - Mapa Completo URLs.md", "seo-sitemap",
     "Mapa de URLs Atrium Golden Visa site herbalifeportugal.com"),
    ("2026-04-03 - Vivenda Creative Home - SEO Completo SERP Top 10.md", "seo-audit",
     "SEO completo Vivenda Creative Home, target SERP top 10"),
    ("2026-03-31 - Vivenda Creative Home - Auditoria e Correcoes WordPress.md", "dario-wp-audit",
     "Auditoria + correções WordPress Vivenda Creative Home (design interiores Lisboa)"),
    ("2026-04-01 - Vivenda Creative Home - Auditoria Mobile Performance e SEO.md", "dario-cwv-fix",
     "CWV + mobile performance Vivenda Creative Home"),
    ("2026-04-04 - Auditoria - Lisbon Dog Care by Marcela.md", "dario-diagnose",
     "Diagnose holístico Lisbon Dog Care WordPress, target dog parents PT/expat"),
    ("2026-04-04 - Lisbon Dog Care - Auditoria Lighthouse e Correcoes Performance.md", "dario-cwv-fix",
     "Lighthouse + performance fixes Lisbon Dog Care"),
    ("2026-04-01 - LUSOconta - Auditoria Tecnica e Parecer Completo DARIO.md", "dario-diagnose",
     "Auditoria técnica completa LUSOconta SaaS contabilidade PT"),
    ("2026-04-02 - Benchmark Competitivo - LUCAS vs Mercado PT e EU com Faturacao.md", "dario-pipeline",
     "Benchmark competitivo LUCAS vs Moloni/SAGE/etc com dados faturação"),
    ("2026-04-02 - LUCAS + LUSACONTA - Plano Estrategico para Lider Europeu.md", "dario-pipeline",
     "Plano estratégico LUCAS para liderança europeia em SaaS contabilidade"),
    ("2026-04-02 - LUCAS + LUSACONTA - Pricing Real e Estrategia de Expansao.md", "dario-financial-model",
     "Pricing real + estratégia expansão LUCAS"),
    ("2026-04-02 - LUCAS + LUSACONTA - Proposta Comercial com Custos Reais.md", "dario-proposal",
     "Proposta comercial LUCAS com custos reais para investidor/comprador"),
    ("2026-04-02 - LUCAS v2 - Benchmark Tecnico Profissional.md", "dario-diagnose",
     "Benchmark técnico profissional LUCAS v2"),
    ("2026-04-02 - LUSOconta - Compendio Completo de Capacidades.md", "dario-content",
     "Compendio completo capacidades LUSOconta para apresentação cliente"),

    # === Batch 2 (2026-05-23 continue) — Cuidai + ARRECADA + others ===
    # Cuidai (caregiver platform BR — Wave 0 production work, real deliverables)
    ("2026-05-18 - Cuidai - CUI-014 Brand Identity Workshop.md", "dario-brand",
     "Brand identity workshop Cuidaí BR (caregiver multigeracional). Capital R$ 100K split. Wave 0 complete 2026-05-17."),
    ("2026-05-18 - Cuidai - CUI-015 Design Tokens Tailwind.md", "diva-materials",
     "Design tokens Tailwind Cuidaí — paleta + tipografias + spacing scale para MVP fork SAQUEI"),
    ("2026-05-18 - Cuidai - CUI-018 Bootstrap Kit Day 0.md", "dario-client-onboard",
     "Bootstrap kit Day 0 Cuidaí — checklist completo registro.br + INPI + Meta + 2 emails legal"),
    ("2026-05-18 - Cuidai - HANDOFF BRIEF Founder.md", "dario-proposal",
     "Handoff brief founder Cuidaí — Wave 0 complete deliverable summary, 9 patterns + 12 decisions resolved"),
    ("2026-05-19 - Cuidai - CUI-046 Burden Index Algorithm.md", "dario-produto",
     "Burden Index algorithm Cuidaí — pontuação carga cuidador multigeracional, formula + thresholds"),
    ("2026-05-19 - Cuidai - Design Partners Kit M3.md", "dario-pipeline",
     "Design Partners kit Cuidaí M3 — outreach 5 prospects + ICP + handoff template"),

    # ARRECADA.GOV (SaaS recuperação dívida ativa municipal)
    ("2026-05-21 - ARRECADA.GOV - Analise POC Sorocaba + Roadmap Evolucao.md", "dario-diagnose",
     "Análise POC Sorocaba ARRECADA.GOV + roadmap evolução. SaaS B2G recuperação dívida ativa municipal com IA."),
    ("2026-05-21 - ARRECADA.GOV - Pitch Parceiros 9 Slides.md", "dario-pitch",
     "Pitch parceiros ARRECADA.GOV 9 slides. Success fee 12%. MVP LIVE VPS:3333. Investigador + Chatbot + Dashboard."),
    ("2026-05-21 - ARRECADA.GOV - Roadmap Aprovado (5 Features + 4 GAPs).md", "dario-produto",
     "Roadmap aprovado ARRECADA.GOV — 5 features + 4 GAPs identificados, priorizado"),

    # adgeniuspro (external audit work)
    ("2026-05-20 - Auditoria Web - adgeniuspro Genius Search Big4 Audit.md", "dario-diagnose",
     "Big4-grade audit adgeniuspro (Genius Search) — site audit completo multi-dimensão"),
    ("2026-05-21 - adgeniuspro - Plano Executivo Sprint 1 (founder brief).md", "dario-pipeline",
     "Plano executivo adgeniuspro Sprint 1 founder brief — ações priorizadas pós-audit"),

    # DARIO docs (commercial deliverables)
    ("2026-05-20 - DARIO v12.0 - Catalogo Comercial 9 Squads Roadmap.md", "dario-content",
     "Catálogo comercial DARIO v12.0 — 9 squads + roadmap para venda VIP"),
    ("2026-05-20 - DARIO v11.4 - Strategic Benchmark + Valuation + Roadmap.md", "dario-financial-model",
     "Strategic benchmark + valuation DARIO v11.4 + roadmap. Valor estimado + comp set."),

    # SAQUEI (SaaS B2C BR)
    ("2026-05-19 - SAQUEI - Gate 1 Readiness Report.md", "a360-validacao",
     "Gate 1 readiness report SAQUEI BR. LIVE saquei.vercel.app. 50+ features. CEO check pendente."),
]


def score_one(path: Path, skill: str, context: str, dry: bool = False):
    if not path.exists():
        return {"skipped": True, "reason": "file_not_found", "path": str(path)}
    if dry:
        return {"skipped": True, "dry_run": True, "skill": skill, "path": path.name}

    script = ORCH / "score_real_output.py"
    cmd = [
        sys.executable, str(script),
        "--skill", skill,
        "--output", str(path),
        "--context", context,
        "--json",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(ORCH))
        # exit 0=yes, 2=needs-review, 3=no, 1=error
        if out.returncode == 1:
            return {"error": True, "stderr": out.stderr.strip()[:200]}
        # Parse last JSON object in stdout
        m = re.search(r"\{[\s\S]+\}", out.stdout)
        if m:
            data = json.loads(m.group(0))
            return {"ok": True, **data}
        return {"error": True, "stderr": "no JSON in output", "stdout": out.stdout[:200]}
    except subprocess.TimeoutExpired:
        return {"error": True, "stderr": "timeout"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int, default=20, help="Max outputs to score")
    args = p.parse_args()

    print(f"=== Batch-scoring {min(len(BATCH), args.limit)} Obsidian outputs ===\n")

    results = []
    for i, (fname, skill, context) in enumerate(BATCH[: args.limit], 1):
        path = OBS / fname
        print(f"[{i:2}/{args.limit}] {skill:25s} {fname[:60]}")
        r = score_one(path, skill, context, args.dry_run)
        results.append({"file": fname, "skill": skill, **r})
        if r.get("ok"):
            verdict = r.get("deliverable", "?")
            score = r.get("score", "?")
            print(f"          → {score}/100 [{verdict}]  global avg={r.get('global_avg_quality')}  rate={r.get('delivery_ready_rate_pct')}%")
        elif r.get("error"):
            print(f"          → ERROR: {r.get('stderr', '?')[:120]}")
        elif r.get("skipped"):
            print(f"          → SKIPPED: {r.get('reason', 'dry-run')}")

    # Summary
    ok = [r for r in results if r.get("ok")]
    yes = [r for r in ok if r.get("deliverable") == "yes"]
    review = [r for r in ok if r.get("deliverable") == "needs-review"]
    no = [r for r in ok if r.get("deliverable") == "no"]
    print("\n=== Summary ===")
    print(f"  Scored: {len(ok)}/{len(results)}")
    print(f"  Yes:    {len(yes)}")
    print(f"  Review: {len(review)}")
    print(f"  No:     {len(no)}")
    if ok:
        last = ok[-1]
        print("\n  Final state:")
        print(f"    Global avg quality:  {last.get('global_avg_quality')}")
        print(f"    Delivery-ready rate: {last.get('delivery_ready_rate_pct')}%  ({last.get('delivery_ready_yes')}/{last.get('delivery_ready_total')})")


if __name__ == "__main__":
    main()
