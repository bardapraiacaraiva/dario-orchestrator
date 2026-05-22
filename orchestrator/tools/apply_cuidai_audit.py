#!/usr/bin/env python3
"""
Apply Cuidaí Taskboard Audit (2026-05-19)
==========================================
One-shot script to apply transitions from `2026-05-19 - Cuidai - Taskboard
Audit vs Prod.md`:

  Bucket 1 (5 tasks) → status: done, waste_reason: existed_in_prod
  Bucket 3 (7 tasks) → blocked_reason populated/refined

Bucket 2 + Bucket 4 are NOT touched here — they need founder confirmation
or repo audit.

Idempotent: tasks already in target state are skipped.

CLI:
    python tools/apply_cuidai_audit.py --dry-run
    python tools/apply_cuidai_audit.py --apply
"""

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
ACTIVE_DIR = ORCH_DIR / "tasks" / "active"
DONE_DIR = ORCH_DIR / "tasks" / "done"

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True
    _yaml.width = 200

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _yaml.load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(data, f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _pyaml.safe_load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _pyaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# Bucket 1 — VERIFIED_DONE_IN_PROD
BUCKET_1 = {
    "CUI-019": "Auth + Family + Elder models + base API verified via /elder/add 3-step form, audit trail confirmed.",
    "CUI-034": "Lighthouse 100 A11y badge visible on production homepage.",
    "CUI-043": "WhatsApp consent step verified at /elder/add step 2. LGPD Art. 11 + immutable audit trail in place.",
    "CUI-044": "Medication reminder engine verified: 15-min pre-notify + 1-touch confirm + 30-min escalation match spec exactly.",
    "CUI-047": "SOS WhatsApp button + push <30s confirmed in production.",
}

# Bucket 3 — REQUIRES_FOUNDER  (refine blocked_reason)
BUCKET_3 = {
    "CUI-008": "Aguarda founder conduzir 10 entrevistas Mom Test IRL — não automatizável.",
    "CUI-022": "Aguarda founder contratar escritório LGPD (R$ 5-10K). 4 candidatos: Chenut · Opice Blum · Astrea · Demarest.",
    "CUI-036": "Aguarda founder completar Stripe BR onboarding (requer CNPJ + dados bancários).",
    "CUI-037": "Aguarda 5 design partners reais usarem app e darem feedback (depende de M3 = 10 design partners onboarded).",
    "CUI-038": "Meta-gate: aguarda outras 20 tasks completarem.",
    "CUI-039": "Aguarda CUI-038 verde + decisão timing founder para launch coordenado.",
    "CUI-040": "Aguarda founder aprovar R$ 500 budget Meta Ads + setup tracking.",
}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def apply_bucket_1(dry_run: bool) -> dict:
    """Move tasks to done/ with waste_reason."""
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for task_id, evidence in BUCKET_1.items():
        active = ACTIVE_DIR / f"{task_id}.yaml"
        if not active.exists():
            results.append({"task": task_id, "status": "missing", "skipped": True})
            continue
        try:
            data = _load_yaml(str(active))
            if not isinstance(data, dict):
                results.append({"task": task_id, "status": "unparseable", "skipped": True})
                continue
            if data.get("status") == "done":
                results.append({"task": task_id, "status": "already_done", "skipped": True})
                continue
            if dry_run:
                results.append({
                    "task": task_id,
                    "status": "would_apply",
                    "from": data.get("status"),
                    "to": "done",
                    "evidence": evidence,
                })
                continue
            # Apply
            data["status"] = "done"
            data["completed_at"] = _now()
            data["waste_reason"] = "existed_in_prod"
            data["audit_2026_05_19_evidence"] = evidence
            if not isinstance(data.get("notes"), list):
                data["notes"] = []
            data["notes"].append({
                "timestamp": _now(),
                "actor": "audit-bucket-1",
                "text": evidence,
            })
            # Move to done/
            dest = DONE_DIR / f"{task_id}.yaml"
            _dump_yaml(data, str(dest))
            active.unlink()
            results.append({
                "task": task_id,
                "status": "moved_to_done",
                "evidence": evidence[:60] + "...",
            })
        except Exception as e:
            results.append({"task": task_id, "status": "error", "error": str(e)[:100]})
    return {"bucket": 1, "actions": results}


def apply_bucket_3(dry_run: bool) -> dict:
    """Refine blocked_reason on tasks staying blocked."""
    results = []
    for task_id, reason in BUCKET_3.items():
        active = ACTIVE_DIR / f"{task_id}.yaml"
        if not active.exists():
            results.append({"task": task_id, "status": "missing", "skipped": True})
            continue
        try:
            data = _load_yaml(str(active))
            if not isinstance(data, dict):
                results.append({"task": task_id, "status": "unparseable", "skipped": True})
                continue
            existing = data.get("blocked_reason") or ""
            if existing == reason:
                results.append({"task": task_id, "status": "already_set"})
                continue
            if dry_run:
                results.append({
                    "task": task_id,
                    "status": "would_apply",
                    "old_reason": existing,
                    "new_reason": reason,
                })
                continue
            data["blocked_reason"] = reason
            data["audit_2026_05_19"] = "REQUIRES_FOUNDER bucket"
            if not isinstance(data.get("notes"), list):
                data["notes"] = []
            data["notes"].append({
                "timestamp": _now(),
                "actor": "audit-bucket-3",
                "text": f"Refined blocked_reason: {reason}",
            })
            _dump_yaml(data, str(active))
            results.append({"task": task_id, "status": "reason_refined"})
        except Exception as e:
            results.append({"task": task_id, "status": "error", "error": str(e)[:100]})
    return {"bucket": 3, "actions": results}


def main():
    p = argparse.ArgumentParser(description="Apply Cuidaí 2026-05-19 audit")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would change without writing")
    p.add_argument("--apply", action="store_true",
                   help="Apply transitions")
    args = p.parse_args()

    if not (args.dry_run or args.apply):
        p.print_help()
        return 1

    dry = args.dry_run
    print(f"Mode: {'DRY RUN' if dry else 'APPLY'}")
    print()

    r1 = apply_bucket_1(dry_run=dry)
    print("=== Bucket 1 (VERIFIED_DONE_IN_PROD) ===")
    for a in r1["actions"]:
        print(f"  {a['task']:<10} | {a['status']}")
        if a.get("evidence"):
            print(f"             evidence: {a['evidence']}")
    print()

    r3 = apply_bucket_3(dry_run=dry)
    print("=== Bucket 3 (REQUIRES_FOUNDER — blocked_reason refined) ===")
    for a in r3["actions"]:
        print(f"  {a['task']:<10} | {a['status']}")
        if a.get("new_reason"):
            print(f"             new: {a['new_reason'][:80]}")
    print()

    moved = sum(1 for a in r1["actions"] if a["status"] == "moved_to_done")
    would = sum(1 for a in r1["actions"] if a["status"] == "would_apply")
    refined = sum(1 for a in r3["actions"] if a["status"] == "reason_refined")
    refined_dry = sum(1 for a in r3["actions"] if a["status"] == "would_apply")

    if dry:
        print(f"Would: move {would} to done, refine {refined_dry} blocked_reasons.")
    else:
        print(f"Moved {moved} tasks to done. Refined {refined} blocked_reasons.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
