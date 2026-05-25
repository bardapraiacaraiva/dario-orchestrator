"""Close pulse 2 (CUI-005) + dispatch pulse 3 (CUI-004 + CUI-006)."""
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH))

from core.task_store import TaskStore

ts = TaskStore()
NOW = datetime.now(UTC).isoformat()

# Close CUI-005
score = 92
tokens = 53581
breakdown = {"specificity": 19, "actionability": 19, "completeness": 18, "accuracy": 18, "tone": 18}
comment = (
    "Benchmark 9 produtos + 6 UX refs. Top whitespace: multi-caregiver n:n + WhatsApp-first idoso "
    "+ LGPD-saúde Art. 11 auditável — combinação não existe em nenhum competitor BR ou internacional. "
    "Anti-feature crítica: CareZone journal pattern (caregiver quer dashboards, não input manual). "
    "Top 5 features a roubar com twist BR identificadas + pricing R$ 29.90 validado entre Famileo e Sami."
)
pattern = (
    "Benchmark report para SaaS pre-MVP: estruturar como (1) 9-12 produtos com Que faz/Strengths-3/"
    "Weaknesses-3/Feature-a-roubar-com-twist por linha, (2) 6 UX craft refs com aplicação concreta, "
    "(3) Strategic synthesis com whitespace map + features confirmadas tabela + pricing comparison, "
    "(4) Top 5 features priorizadas + anti-features explícitas, (5) Threats & defensive moats."
)
output_file = r"C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs\2026-05-16 - Cuidai - CUI-005 Benchmark Report 9 Products.md"

ts.update("CUI-005", {
    "status": "done",
    "completed_at": NOW,
    "quality_score": score,
    "actual_tokens": tokens,
    "completion_comment": comment,
})

yaml_path = ORCH / "tasks" / "active" / "CUI-005.yaml"
with open(yaml_path, encoding="utf-8") as f:
    d = yaml.safe_load(f)
d.update({
    "status": "done",
    "completed_at": NOW,
    "quality_score": score,
    "quality_breakdown": breakdown,
    "quality_action": "success_pattern",
    "actual_tokens": tokens,
    "completion_comment": comment,
    "quality_pattern_extracted": pattern,
    "output_file": output_file,
})
if not d.get("notes"):
    d["notes"] = []
d["notes"].append(f"[{NOW}] Pulse 2 closeout — score {score}/100, success_pattern")
with open(yaml_path, "w", encoding="utf-8") as f:
    yaml.dump(d, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

# Update budget
budget_path = ORCH / "budgets" / "2026-05.yaml"
with open(budget_path, encoding="utf-8") as f:
    b = yaml.safe_load(f)
b["total_tokens_used"] += tokens
b["percentage"] = round(b["total_tokens_used"] / b["limit"] * 100, 2)
b["last_updated"] = NOW
b["pulse_count"] = b.get("pulse_count", 0) + 1
b["by_project"]["cuidai"] = b["by_project"].get("cuidai", 0) + tokens
b["by_skill"]["a360-nicho"] = b["by_skill"].get("a360-nicho", 0) + tokens
b["by_model"]["opus"] = b["by_model"].get("opus", 0) + tokens
with open(budget_path, "w", encoding="utf-8") as f:
    yaml.dump(b, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# Pulse 3 checkout: CUI-004 + CUI-006 in parallel (different workers)
for tid in ["CUI-004", "CUI-006"]:
    ts.update(tid, {"status": "in_progress", "checked_out_at": NOW})
    yp = ORCH / "tasks" / "active" / f"{tid}.yaml"
    with open(yp, encoding="utf-8") as f:
        yd = yaml.safe_load(f)
    yd["status"] = "in_progress"
    yd["checked_out_at"] = NOW
    if not yd.get("notes"):
        yd["notes"] = []
    yd["notes"].append(f"[{NOW}] Pulse 3 checkout — lucas-autopilot autonomous")
    with open(yp, "w", encoding="utf-8") as f:
        yaml.dump(yd, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

print(f"[Pulse 2 closed] CUI-005 done | score 92/100 | {tokens:,} tokens")
print(f"[Budget] {b['percentage']}% ({b['total_tokens_used']:,} / {b['limit']:,})")
print("[Pulse 3 dispatched] CUI-004 + CUI-006 in parallel")
print(f"Counts: {ts.counts()}")
