#!/usr/bin/env python3
"""Real ROI from the revenue registry + measured AI cost.

Closes the cfo-token-roi gap (2026-06-12): the orchestrator could cost every
task but had no revenue data, so ROI was incomputable. This reads
finance/revenue.yaml (founder-maintained values) and the measured API cost from
subagent_runs/, and reports an HONEST ROI — including the "still incomputable"
state while project values remain null. It never invents a revenue number.

CLI:
    python finance/revenue_roi.py            # human report
    python finance/revenue_roi.py --json     # machine-readable
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
REVENUE_FILE = ORCH_DIR / "finance" / "revenue.yaml"
RUNS_DIR = ORCH_DIR / "subagent_runs"
USD_EUR = 0.92


def load_revenue() -> dict:
    try:
        import yaml
        data = yaml.safe_load(REVENUE_FILE.read_text(encoding="utf-8")) or {}
        return data.get("projects", {}) or {}
    except Exception:
        return {}


def attributed_revenue_eur(projects: dict) -> dict:
    """Sum valor_eur × weight over projects with a recorded value.

    Returns the total plus coverage stats so the caller can be honest about how
    much of the portfolio is actually measured.
    """
    total = 0.0
    valued = 0
    unmeasured = []
    for slug, p in projects.items():
        if not isinstance(p, dict):
            continue
        val = p.get("valor_eur")
        if val is None:
            unmeasured.append(slug)
            continue
        weight = float(p.get("weight", 1.0))
        total += float(val) * weight
        valued += 1
    return {
        "revenue_eur": round(total, 2),
        "projects_valued": valued,
        "projects_unmeasured": len(unmeasured),
        "unmeasured": unmeasured,
        "coverage_pct": round(valued / max(len(projects), 1) * 100, 1),
    }


def measured_cost_usd() -> dict:
    """Sum the real per-run cost from captured transcripts (subagent_runs)."""
    total = 0.0
    runs = 0
    out_tokens = 0
    cache_read = 0
    for f in glob.glob(str(RUNS_DIR / "**" / "*.json"), recursive=True):
        try:
            t = (json.load(open(f, encoding="utf-8")) or {}).get("totals", {}) or {}
            total += float(t.get("cost_usd", 0) or 0)
            out_tokens += int(t.get("output_tokens", 0) or 0)
            cache_read += int(t.get("cache_read_input_tokens", 0) or 0)
            runs += 1
        except Exception:
            continue
    return {
        "cost_usd": round(total, 2),
        "cost_eur": round(total * USD_EUR, 2),
        "runs": runs,
        "output_tokens": out_tokens,
        "cache_read_tokens": cache_read,
    }


def compute_roi() -> dict:
    projects = load_revenue()
    rev = attributed_revenue_eur(projects)
    cost = measured_cost_usd()
    # ROI is only computable once at least one REVENUE-GENERATING project has a
    # value (revenue_eur > 0). An internal/€0 project being "valued" must not
    # make ROI read as a misleading 0.0x — that's still "no revenue measured".
    roi = None
    if rev["revenue_eur"] > 0 and cost["cost_eur"] > 0:
        roi = round(rev["revenue_eur"] / cost["cost_eur"], 2)
    return {
        "revenue": rev,
        "cost": cost,
        "roi": roi,  # None = incomputable until a paying project is valued
        "computable": roi is not None,
    }


def _report() -> str:
    r = compute_roi()
    rev, cost = r["revenue"], r["cost"]
    total_proj = rev["projects_valued"] + rev["projects_unmeasured"]
    lines = ["=== DARIO Real ROI (revenue registry × measured cost) ===", ""]
    lines.append(f"Custo medido (transcripts): ${cost['cost_usd']:.2f} "
                 f"(~EUR {cost['cost_eur']:.2f}) sobre {cost['runs']} runs")
    lines.append(f"Receita realizada: EUR {rev['revenue_eur']:.2f} "
                 f"({rev['projects_valued']}/{total_proj} projetos valorizados, "
                 f"{rev['coverage_pct']}% cobertura)")
    if r["computable"]:
        lines.append(f"\n>>> ROI = {r['roi']}x")
    elif rev["projects_unmeasured"] > 0:
        lines.append("\n>>> ROI = INCOMPUTÁVEL — projetos sem valor_eur registado:")
        lines.append("    " + ", ".join(rev["unmeasured"][:10]))
        lines.append(f"    Preenche valor_eur em {REVENUE_FILE}.")
    else:
        # All projects valued, but realized revenue is €0 — this is the diagnosis.
        lines.append("\n>>> ROI ≈ 0x — receita realizada CONFIRMADA em €0.")
        lines.append("    Os projetos são ventures pré-receita (founder-confirmed); o")
        lines.append("    orchestrator foi usado para I&D próprio, não entrega faturável.")
        lines.append("    O ROI 0x é o diagnóstico, não uma falha de medição.")
    return "\n".join(lines)


def main() -> int:
    if "--json" in sys.argv:
        print(json.dumps(compute_roi(), indent=2, ensure_ascii=False))
    else:
        print(_report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
