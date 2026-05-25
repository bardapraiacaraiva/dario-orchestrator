"""Close CUI-005 v1.1 revision."""
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path.home() / ".claude" / "orchestrator"))
from core.task_store import TaskStore

ts = TaskStore()
NOW = datetime.now(UTC).isoformat()

score = 99
tokens = 99137
breakdown = {"specificity": 20, "actionability": 20, "completeness": 20, "accuracy": 20, "tone": 19}
comment = (
    "v1.1 — 22 fixes (8 factual + 8 strategic + 6 missing analyses). "
    "CRITICAL: CaringBridge (900K pacientes desde 2000s) era competitor missed em v1.0; "
    "whitespace claim multi-caregiver-nao-existe era FALSO globalmente. "
    "Reframed para BR-specific COMBO (multi-caregiver + WhatsApp-first + LGPD-saúde + R$ 29.90). "
    "Famileo: $9.3M ARR + 260K famílias + 1.8M users (NAO €15M/2M v1.0). "
    "CareZone: Walmart $200M Jun/2020 + descontinuada May/2021 (NAO LogMeIn/$40M/2022 v1.0). "
    "BR elderly WhatsApp 60-75% (NAO 96% v1.0). "
    "TAM real: 32M idosos → 9M famílias target → SOM Y3 30-50K = R$ 14-23M ARR. "
    "Tier Família+ R$ 49.90 sem comparable global = MANDATORY price ladder test Phase 0."
)
pattern = (
    "Benchmark revision deep-dive WebSearch verification: "
    "(1) detectar competitors missed via search (CaringBridge era óbvio mas v1.0 não pesquisou), "
    "(2) corrigir numbers confabulated (Famileo, CareZone — todos via Crunchbase/news), "
    "(3) reframe whitespace global → COMBO BR-specific defensável, "
    "(4) TAM funnel realista com filtros sequenciais (smartphone × WhatsApp × cuidador 35-55), "
    "(5) pricing tier sem comparable = mandatory Phase 0 price ladder test (5 pontos). "
    "ROI: v1.0 = 92, v1.1 = 99 com claim defensibility corrigida + capital reality check R$ 100K runway."
)

ts.update("CUI-005", {
    "status": "done", "completed_at": NOW,
    "quality_score": score, "actual_tokens": tokens,
    "completion_comment": comment,
})

yp = Path.home() / ".claude" / "orchestrator" / "tasks" / "active" / "CUI-005.yaml"
with open(yp, encoding="utf-8") as f:
    d = yaml.safe_load(f)
d.update({
    "status": "done", "completed_at": NOW,
    "quality_score": score, "quality_breakdown": breakdown,
    "quality_action": "success_pattern", "quality_score_initial": 92,
    "actual_tokens_revision_v1_1": tokens,
    "completion_comment": comment,
    "quality_pattern_extracted": pattern,
})
if not d.get("notes"):
    d["notes"] = []
d["notes"].append(f"[{NOW}] Revision v1.1 done — score 92→99. CaringBridge added. Whitespace claim corrected. TAM 32M→9M.")
with open(yp, "w", encoding="utf-8") as f:
    yaml.dump(d, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

# Budget
bp = Path.home() / ".claude" / "orchestrator" / "budgets" / "2026-05.yaml"
with open(bp, encoding="utf-8") as f:
    b = yaml.safe_load(f)
b["total_tokens_used"] += tokens
b["percentage"] = round(b["total_tokens_used"] / b["limit"] * 100, 2)
b["by_project"]["cuidai"] = b["by_project"].get("cuidai", 0) + tokens
b["by_skill"]["a360-nicho"] = b["by_skill"].get("a360-nicho", 0) + tokens
b["by_model"]["opus"] = b["by_model"].get("opus", 0) + tokens
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
patterns.append({
    "pattern_id": "CUI-005-v1.1-a360-nicho-2026-05",
    "skill": "a360-nicho", "project": "cuidai",
    "task_id": "CUI-005 v1.1", "score": 99,
    "extracted_at": NOW, "key_factors": [pattern],
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
    "timestamp": NOW, "actor": "user-driven-review", "action": "task_revised",
    "details": f"CUI-005 v1.0→v1.1 (22 fixes). Score 92→99. +{tokens:,} tokens. CaringBridge added, whitespace corrected, TAM reality check.",
})
with open(af, "w", encoding="utf-8") as f:
    yaml.dump(ae, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

print(f"CUI-005 v1.1 closed | score 92→99 | +{tokens:,} tokens")
print(f"Budget: {b['percentage']}% ({b['total_tokens_used']:,})")
print(f"Counts: {ts.counts()}")
