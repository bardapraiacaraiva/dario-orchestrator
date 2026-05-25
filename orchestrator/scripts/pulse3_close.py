"""Close pulse 3 (CUI-004 + CUI-006) + analyze next executable tasks."""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH))

from core.task_store import TaskStore

ts = TaskStore()
NOW = datetime.now(UTC).isoformat()

# Close results
RESULTS = {
    "CUI-004": {
        "score": 92,
        "breakdown": {"specificity": 19, "actionability": 19, "completeness": 19, "accuracy": 17, "tone": 18},
        "action": "success_pattern",
        "tokens": 54648,
        "skill": "dario-product",
        "output_file": r"C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs\2026-05-16 - Cuidai - CUI-004 WhatsApp Business API Spec.md",
        "comment": "WhatsApp Meta Direct spec completo: decisão Meta vs Twilio (50% cheaper @ scale), Day 0 onboarding playbook 95min, 4 templates pt_BR ready-to-submit (consent/reminder/missed/SOS), webhook code TypeScript com signature verify + idempotency, cost projection R$ 31/132/3100 @ 10/100/1K famílias (4.4% MRR). Founder action urgente: business.facebook.com HOJE, submeter 4 templates — bloqueia CUI-021 diretamente.",
        "pattern": "Integration spec para third-party API com approval bottleneck: estruturar como (1) decision matrix vs alternativa com pricing comparison real, (2) Day 0 onboarding playbook step-by-step com tempos realistic, (3) submission-ready templates pt_BR com variables explicitas, (4) webhook code TypeScript executable com signature+idempotency, (5) cost projection @ 3 scales como % MRR. Approval lead-time é o gargalo crítico — submeter Day 0.",
    },
    "CUI-006": {
        "score": 93,
        "breakdown": {"specificity": 19, "actionability": 19, "completeness": 19, "accuracy": 18, "tone": 18},
        "action": "success_pattern",
        "tokens": 48415,
        "skill": "dario-content",
        "output_file": r"C:\Users\barda\OneDrive\Documents\D.A.R.I.O\05 - Claude - IA\Outputs\2026-05-16 - Cuidai - CUI-006 Mom Test Outreach Script BR.md",
        "comment": "Mom Test kit BR completo: recruitment strategy 5 canais com ROI matrix, screener Typeform 5 perguntas auto-disqualify, 3 templates outreach (LinkedIn connect + DM + WhatsApp 2º grau + Facebook organic), 7 perguntas script obrigatório com sondagens, quote capture protocol 10 quotes ouro, day-by-day 7d plan ~15h founder. Anti-pattern critico: BR 'sim' é cortesia social — sempre exigir pre-commit (lista espera/2 indicações/SMS test).",
        "pattern": "Discovery recruitment kit BR: combinar (1) ROI matrix de 5 canais aquisição entrevistados, (2) screener Typeform com auto-disqualify, (3) 4 templates outreach BR-PT canal-specific, (4) script entrevista 7 perguntas FIXED order com sondagens por pergunta, (5) quote capture protocol classificado (pain/frustration/aspiration/pricing). Funnel BR realistic: 50→20→10 com R$ 500 incentivos.",
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
    yp = ORCH / "tasks" / "active" / f"{tid}.yaml"
    with open(yp, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    d.update({
        "status": "done", "completed_at": NOW,
        "quality_score": r["score"], "quality_breakdown": r["breakdown"],
        "quality_action": r["action"], "actual_tokens": r["tokens"],
        "completion_comment": r["comment"], "output_file": r["output_file"],
        "quality_pattern_extracted": r["pattern"],
    })
    if not d.get("notes"): d["notes"] = []
    d["notes"].append(f"[{NOW}] Pulse 3 closeout — score {r['score']}/100, success_pattern")
    with open(yp, "w", encoding="utf-8") as f:
        yaml.dump(d, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    print(f"[done] {tid} | score {r['score']}/100 | {r['tokens']:,} tokens")

# Update budget
bp = ORCH / "budgets" / "2026-05.yaml"
with open(bp, encoding="utf-8") as f:
    b = yaml.safe_load(f)
b["total_tokens_used"] += total_tokens
b["percentage"] = round(b["total_tokens_used"] / b["limit"] * 100, 2)
b["last_updated"] = NOW
b["pulse_count"] = b.get("pulse_count", 0) + 1
b["by_project"]["cuidai"] = b["by_project"].get("cuidai", 0) + total_tokens
for tid, r in RESULTS.items():
    b["by_skill"][r["skill"]] = b["by_skill"].get(r["skill"], 0) + r["tokens"]
b["by_model"]["opus"] = b["by_model"].get("opus", 0) + total_tokens
with open(bp, "w", encoding="utf-8") as f:
    yaml.dump(b, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# Extract patterns
pf = ORCH / "quality" / "success-patterns.yaml"
patterns = []
if pf.exists():
    with open(pf, encoding="utf-8") as f:
        patterns = yaml.safe_load(f) or []
for tid, r in RESULTS.items():
    if r["action"] == "success_pattern":
        patterns.append({
            "pattern_id": f"{tid}-{r['skill']}-2026-05",
            "skill": r["skill"], "project": "cuidai", "task_id": tid,
            "score": r["score"], "extracted_at": NOW,
            "key_factors": [r["pattern"]],
        })
with open(pf, "w", encoding="utf-8") as f:
    yaml.dump(patterns, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# Audit
af = ORCH / "audit" / f"{datetime.now().strftime('%Y-%m-%d')}.yaml"
ae = []
if af.exists():
    with open(af, encoding="utf-8") as f: ae = yaml.safe_load(f) or []
ae.append({
    "timestamp": NOW, "actor": "lucas-autopilot", "action": "wave_completed",
    "details": f"Pulse 3 (Cuidaí): CUI-004 + CUI-006. Avg score {sum(r['score'] for r in RESULTS.values())/len(RESULTS):.1f}/100. Tokens {total_tokens:,}.",
})
with open(af, "w", encoding="utf-8") as f:
    yaml.dump(ae, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

print(f"\n[BUDGET] +{total_tokens:,} → {b['total_tokens_used']:,} ({b['percentage']}%)")

# Analyze next executable
print("\n=== NEXT EXECUTABLE ANALYSIS ===")
print(f"Counts: {ts.counts()}")

all_tasks = ts.get_all(project="cuidai")
done_ids = {t["id"] for t in all_tasks if t.get("status") == "done"}
todo = [t for t in all_tasks if t.get("status") == "todo"]

ready_agent = []
ready_human = []
for t in todo:
    deps = t.get("depends_on") or []
    if isinstance(deps, str):
        try: deps = json.loads(deps)
        except: deps = []
    if all(d in done_ids for d in deps):
        # Detect human-required tasks by notes content
        notes = t.get("notes") or []
        notes_text = " ".join(notes if isinstance(notes, list) else [str(notes)])
        if "Trabalho humano" in notes_text or "human" in notes_text.lower() or t["id"] in ["CUI-007", "CUI-008", "CUI-009"]:
            ready_human.append(t)
        else:
            ready_agent.append(t)

print(f"\nReady for AGENT execution ({len(ready_agent)}):")
for t in ready_agent[:10]:
    print(f"  {t['id']} | {t.get('priority')} | {t.get('skill','?')} | {t.get('title','')[:80]}")

print(f"\nReady but needs HUMAN action ({len(ready_human)}):")
for t in ready_human[:10]:
    print(f"  {t['id']} | {t.get('priority')} | {t.get('title','')[:80]}")

print(f"\nBlocked downstream (waiting on gates/dependencies): {len(todo) - len(ready_agent) - len(ready_human)}")
