"""
closeout_wave.py — Score, complete, log a wave of just-executed tasks.
Reads results dict inline, updates DB + YAML, updates budget, audit log.
"""
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH))

from db import DB
from task_store import TaskStore

NOW = datetime.now(UTC).isoformat()

# Inline results from Wave 0 — populated by autopilot after Agent execution
RESULTS = {
    "CUI-001": {
        "score": 90,
        "breakdown": {"specificity": 18, "actionability": 19, "completeness": 18, "accuracy": 17, "tone": 18},
        "action": "success_pattern",
        "tokens": 45375,
        "skill": "dario-naming",
        "output_file": str(Path("C:/Users/barda/OneDrive/Documents/D.A.R.I.O/05 - Claude - IA/Outputs/2026-05-16 - Cuidai - CUI-001 Brand Availability Verification Kit.md")),
        "completion_comment": "Verification kit completo com URLs reais (registro.br + busca.inpi.gov.br + 7 social platforms) + decision matrix semáforo + 3 fallback brand candidates + 48h Day 0 action plan. MEDIUM brand collision risk (Cuidai = imperativo do verbo cuidar, alta probabilidade @cuidai IG já taken). Founder action urgente: registro.br query + comprar cuidai.com.br se livre.",
        "pattern_summary": "Brand availability kit BR: combinar registro.br + INPI busca + social handles tabela + Google collision queries num único playbook 48h, sempre com 3 fallback brands rankeados. Inclui custo R$ por classe INPI (R$ 530 + R$ 355/classe) e flag mixed mark (palavra+logo) para evitar rejeição INPI por descritivo.",
    },
    "CUI-002": {
        "score": 93,
        "breakdown": {"specificity": 19, "actionability": 19, "completeness": 19, "accuracy": 18, "tone": 18},
        "action": "success_pattern",
        "tokens": 49142,
        "skill": "dario-legal",
        "output_file": str(Path("C:/Users/barda/OneDrive/Documents/D.A.R.I.O/05 - Claude - IA/Outputs/2026-05-16 - Cuidai - CUI-002 Legal Scope Brief LGPD Saude.md")),
        "completion_comment": "Scope LGPD-saúde completo: 7 deliverables (RIPD + bases legais + ToU + privacy + WhatsApp consent + ANPD notif + transfer internacional) + 3 outreach emails personalizados (Opice/Astrea/Chenut) + comparative table + recomendação Astrea com Plan B Chenut. Decisão pendente founder: enviar 3 emails simultaneamente + budget hard cap R$ 8K vs R$ 10K antes do briefing inicial.",
        "pattern_summary": "Scope jurídico LGPD-saúde para SaaS BR pre-revenue: estruturar como (1) scope técnico 7 deliverables com bases legais Art. 11 explícitas, (2) 3 outreach emails tiered (luxury/mid/budget), (3) comparative matrix com fee+timeline+strength+risco, (4) recomendação ranked com plan B trigger. Sweet spot R$ 5-10K mid tier para velocity 90 dias.",
    },
    "CUI-003": {
        "score": 94,
        "breakdown": {"specificity": 19, "actionability": 20, "completeness": 19, "accuracy": 18, "tone": 18},
        "action": "success_pattern",
        "tokens": 48877,
        "skill": "dario-product",
        "output_file": str(Path("C:/Users/barda/OneDrive/Documents/D.A.R.I.O/05 - Claude - IA/Outputs/2026-05-16 - Cuidai - CUI-003 Architecture Baseline SAQUEI Fork Plan.md")),
        "completion_comment": "Architecture baseline com 78% reuse alcançado (acima do 75% target), 25 módulos SAQUEI mapeados, fork strategy recomendada, custo R$ 180/mês @ 10 famílias, break-even 21 famílias pagas. W1 day-by-day plan 32h founder time. Ação mais urgente: submeter 4 templates Meta WhatsApp HOJE — bloqueia CUI-021 consent flow LGPD.",
        "pattern_summary": "Fork plan SaaS BR a partir de codebase mãe: estruturar como (1) reuse map exhaustivo 20+ módulos com %, (2) decision matrix fork/greenfield/copypaste, (3) DB isolation 3 opções, (4) env vars delta exact, (5) cost projection @ 3 scales, (6) W1 day-by-day 6h/dia realista, (7) 5 ADRs Decision/Rationale/Tradeoff/Revisit-when. Velocity founder 50+ features/3 semanas valida 32h W1 plan.",
    },
}

ts = TaskStore()
db = DB()

# 1. Mark each task as done with score
total_tokens = 0
for tid, r in RESULTS.items():
    ok = ts.update(tid, {
        "status": "done",
        "completed_at": NOW,
        "quality_score": r["score"],
        "actual_tokens": r["tokens"],
        "completion_comment": r["completion_comment"],
    })
    total_tokens += r["tokens"]
    print(f"[DB]   {tid} → done | score={r['score']} | tokens={r['tokens']} (ok={ok})")

    # Update YAML
    yaml_path = ORCH / "tasks" / "active" / f"{tid}.yaml"
    if yaml_path.exists():
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        data["status"] = "done"
        data["completed_at"] = NOW
        data["quality_score"] = r["score"]
        data["quality_breakdown"] = r["breakdown"]
        data["quality_action"] = r["action"]
        data["actual_tokens"] = r["tokens"]
        data["completion_comment"] = r["completion_comment"]
        data["output_file"] = r["output_file"]
        if r["action"] == "success_pattern":
            data["quality_pattern_extracted"] = r["pattern_summary"]
        if data.get("notes") is None:
            data["notes"] = []
        data["notes"].append(f"[{NOW}] Wave 0 closeout — score {r['score']}/100, action={r['action']}")
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
        print(f"[YAML] {tid} updated")

# 2. Update budget
budget_path = ORCH / "budgets" / "2026-05.yaml"
with open(budget_path, encoding="utf-8") as f:
    budget = yaml.safe_load(f)

budget["total_tokens_used"] += total_tokens
budget["percentage"] = round(budget["total_tokens_used"] / budget["limit"] * 100, 2)
budget["last_updated"] = NOW
budget["pulse_count"] = budget.get("pulse_count", 0) + 1

# By project
budget["by_project"]["cuidai"] = budget["by_project"].get("cuidai", 0) + total_tokens

# By skill
for tid, r in RESULTS.items():
    s = r["skill"]
    budget["by_skill"][s] = budget["by_skill"].get(s, 0) + r["tokens"]

# By model (assume opus for these tasks based on default)
budget["by_model"]["opus"] = budget["by_model"].get("opus", 0) + total_tokens

# Alert thresholds
if budget["percentage"] >= 80 and not budget.get("alert_80_sent"):
    budget["alert_80_sent"] = True
    print("[WARN] Budget reached 80% threshold")
if budget["percentage"] >= 95 and not budget.get("alert_95_sent"):
    budget["alert_95_sent"] = True
    print("[CRITICAL] Budget reached 95% threshold")

with open(budget_path, "w", encoding="utf-8") as f:
    yaml.dump(budget, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
print(f"\n[BUDGET] +{total_tokens:,} tokens this wave → total {budget['total_tokens_used']:,} ({budget['percentage']}%)")

# 3. Update quality/skill-metrics + extract success patterns
patterns_file = ORCH / "quality" / "success-patterns.yaml"
patterns_file.parent.mkdir(parents=True, exist_ok=True)
patterns = []
if patterns_file.exists():
    with open(patterns_file, encoding="utf-8") as f:
        patterns = yaml.safe_load(f) or []

for tid, r in RESULTS.items():
    if r["action"] == "success_pattern":
        patterns.append({
            "pattern_id": f"{tid}-{r['skill']}-2026-05",
            "skill": r["skill"],
            "project": "cuidai",
            "task_id": tid,
            "score": r["score"],
            "extracted_at": NOW,
            "key_factors": [r["pattern_summary"]],
        })
        print(f"[PATTERN] {tid} extracted (score {r['score']})")

with open(patterns_file, "w", encoding="utf-8") as f:
    yaml.dump(patterns, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# 4. Audit log
audit_file = ORCH / "audit" / f"{datetime.now().strftime('%Y-%m-%d')}.yaml"
audit_entries = []
if audit_file.exists():
    with open(audit_file, encoding="utf-8") as f:
        audit_entries = yaml.safe_load(f) or []

audit_entries.append({
    "timestamp": NOW,
    "actor": "lucas-autopilot",
    "action": "wave_completed",
    "details": f"Wave 0 (Cuidaí): completed {', '.join(RESULTS.keys())}. Avg score: {sum(r['score'] for r in RESULTS.values())/len(RESULTS):.1f}/100. Tokens: {total_tokens:,}. Patterns extracted: {sum(1 for r in RESULTS.values() if r['action']=='success_pattern')}.",
})

with open(audit_file, "w", encoding="utf-8") as f:
    yaml.dump(audit_entries, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# 5. Final state report
print(f"\n[AUDIT] logged to {audit_file.name}")
print("\n=== WAVE 0 SUMMARY ===")
print("Tasks completed: 3 (CUI-001, CUI-002, CUI-003)")
print(f"Avg quality: {sum(r['score'] for r in RESULTS.values())/3:.1f}/100")
print(f"Tokens consumed: {total_tokens:,}")
print("Patterns extracted: 3 (all success_pattern tier)")
print(f"\nTaskboard counts: {ts.counts()}")
print(f"Budget: {budget['percentage']}% ({budget['total_tokens_used']:,} / {budget['limit']:,})")

# 6. Identify next executable tasks
all_tasks = ts.get_all()
todo_tasks = [t for t in all_tasks if t.get("status") == "todo" and t.get("project") == "cuidai"]
done_ids = {t["id"] for t in all_tasks if t.get("status") == "done"}

ready = []
for t in todo_tasks:
    deps = t.get("depends_on") or []
    if isinstance(deps, str):
        import json
        try: deps = json.loads(deps)
        except: deps = []
    if all(d in done_ids for d in deps):
        ready.append(t)

ready.sort(key=lambda t: (
    {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(t.get("priority", "medium"), 2),
    t["id"]
))

print(f"\n=== NEXT PULSE READY ({len(ready)} tasks) ===")
for t in ready[:5]:
    print(f"  {t['id']} | {t.get('priority')} | {t.get('assignee')} | {t.get('title','')[:70]}")
