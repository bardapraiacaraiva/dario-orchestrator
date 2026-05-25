"""Close CUI-006 v1.1 + CUI-009 template."""
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path.home() / ".claude" / "orchestrator"))
from core.task_store import TaskStore

ts = TaskStore()
NOW = datetime.now(UTC).isoformat()

RESULTS = {
    "CUI-006": {
        "score": 96,
        "tokens": 54244,
        "breakdown": {"specificity": 19, "actionability": 20, "completeness": 19, "accuracy": 19, "tone": 19},
        "skill": "dario-content",
        "output_file": r"C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs\2026-05-16 - Cuidai - CUI-006 Mom Test Outreach Script BR.md",
        "comment": "v1.1 patch — 6 patches integrando founder decisions session 2026-05-17. Price ladder 5 pontos substitui Q7 single-price. Pre-commit protocol expandido 1→4 opcoes hierarchy (Waitlist/Indicacoes/SMS Test/Pre-pay). Interview duration 60→75min. Section 8 nova: Gate Criteria CUI-009 referencia cross-doc com GO/PIVOT/KILL explicit thresholds.",
        "pattern": "Mom Test script patch para integrar founder decisions: substituir single-price Q7 por 5-point ladder + pre-commit hierarchy quantificada por pontos + cross-reference gate criteria. Transforma entrevista de hypothesis test em pricing research tool.",
        "initial_score": 93,
    },
    "CUI-009": {
        "score": 97,
        "tokens": 42370,
        "breakdown": {"specificity": 20, "actionability": 20, "completeness": 20, "accuracy": 19, "tone": 19},
        "skill": "dario-product",
        "output_file": r"C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs\2026-05-17 - Cuidai - CUI-009 Gate Criteria Template.md",
        "comment": "Template criado para Phase 0 Gate Decision. 5 criteria quantitativos (Pain >=7/10 + WTP pre-commit >=5/10 + Quotes ouro >=3 + Zero red flags LGPD + Whitespace >=4/10). Pre-committed PRE-data collection (bias resistance). GO/PIVOT/KILL outcomes explicit. Audit trail LGPD-ready. Status: template-ready-for-cui-008-output.",
        "pattern": "Gate decision template para Phase 0 discovery: criteria locked-in PRE-data com thresholds quantitativos, fill-in-the-blanks tabelas para data capture, 3 outcomes pre-defined (GO/PIVOT/KILL) cada um com next-action explicit, audit trail LGPD compliant.",
        "initial_score": None,  # New file, no v1.0
    },
}

total_tokens = 0
for tid, r in RESULTS.items():
    ts.update(tid, {
        "status": "done", "completed_at": NOW,
        "quality_score": r["score"], "actual_tokens": r["tokens"],
        "completion_comment": r["comment"],
    })
    total_tokens += r["tokens"]
    yp = Path.home() / ".claude" / "orchestrator" / "tasks" / "active" / f"{tid}.yaml"
    with open(yp, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    d.update({
        "status": "done", "completed_at": NOW,
        "quality_score": r["score"], "quality_breakdown": r["breakdown"],
        "quality_action": "success_pattern",
        "actual_tokens_revision": r["tokens"],
        "completion_comment": r["comment"],
        "quality_pattern_extracted": r["pattern"],
        "output_file": r["output_file"],
    })
    if r["initial_score"]:
        d["quality_score_initial"] = r["initial_score"]
    if not d.get("notes"):
        d["notes"] = []
    delta = r["score"] - (r["initial_score"] or 0)
    d["notes"].append(f"[{NOW}] Patch done — score {r['initial_score']}→{r['score']} (Δ+{delta}). Integrates session decisions.")
    with open(yp, "w", encoding="utf-8") as f:
        yaml.dump(d, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    print(f"[done] {tid} | score {r['score']}/100 | {r['tokens']:,} tokens")

# Budget
bp = Path.home() / ".claude" / "orchestrator" / "budgets" / "2026-05.yaml"
with open(bp, encoding="utf-8") as f:
    b = yaml.safe_load(f)
b["total_tokens_used"] += total_tokens
b["percentage"] = round(b["total_tokens_used"] / b["limit"] * 100, 2)
b["by_project"]["cuidai"] = b["by_project"].get("cuidai", 0) + total_tokens
for tid, r in RESULTS.items():
    b["by_skill"][r["skill"]] = b["by_skill"].get(r["skill"], 0) + r["tokens"]
b["by_model"]["opus"] = b["by_model"].get("opus", 0) + total_tokens
b["last_updated"] = NOW
b["pulse_count"] = b.get("pulse_count", 0) + 1
with open(bp, "w", encoding="utf-8") as f:
    yaml.dump(b, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# Patterns
pf = Path.home() / ".claude" / "orchestrator" / "quality" / "success-patterns.yaml"
patterns = []
if pf.exists():
    with open(pf, encoding="utf-8") as f:
        patterns = yaml.safe_load(f) or []
for tid, r in RESULTS.items():
    patterns.append({
        "pattern_id": f"{tid}-patch-decisions-2026-05",
        "skill": r["skill"], "project": "cuidai", "task_id": f"{tid} patch",
        "score": r["score"], "extracted_at": NOW,
        "key_factors": [r["pattern"]],
    })
with open(pf, "w", encoding="utf-8") as f:
    yaml.dump(patterns, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# Audit
af = Path.home() / ".claude" / "orchestrator" / "audit" / f"{datetime.now().strftime('%Y-%m-%d')}.yaml"
ae = []
if af.exists():
    with open(af, encoding="utf-8") as f:
        ae = yaml.safe_load(f) or []
ae.append({
    "timestamp": NOW, "actor": "user-driven-review", "action": "decisions_integrated",
    "details": f"CUI-006 patch v1.1 + CUI-009 template created. Integrates 12 founder decisions from session 2026-05-17. +{total_tokens:,} tokens.",
})
with open(af, "w", encoding="utf-8") as f:
    yaml.dump(ae, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

print(f"\n[BUDGET] +{total_tokens:,} → {b['total_tokens_used']:,} ({b['percentage']}%)")
print(f"[Counts] {ts.counts()}")
