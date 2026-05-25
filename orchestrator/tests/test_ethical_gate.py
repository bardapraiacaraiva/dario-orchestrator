#!/usr/bin/env python3
"""End-to-end tests for Upgrade 2 ethical pre-gate."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import pytest

from safety.ethical_gate import evaluate

pytestmark = pytest.mark.slow

SCENARIOS = [
    # (label, task_dict, expected_verdict, must_have_reason_substring or None)

    ("clean well-formed task",
     {
         "id": "TEST-001",
         "title": "Criar auditoria SEO completa do site",
         "description": "Analisar a estrutura do site, identificar problemas tecnicos, propor 10 melhorias priorizadas",
         "project": "atrium",
         "skill": "seo-audit",
         "execution_policy": "client_facing",
     },
     "PASS", None),

    ("vague help request",
     {
         "id": "TEST-002",
         "title": "ajuda",
         "description": "preciso de ajuda com isto",
     },
     "FAIL", "vague"),

    ("destructive without confirmation",
     {
         "id": "TEST-003",
         "title": "delete all old client data",
         "description": "remove every record older than 2 years from the database",
         "project": "atrium",
         "skill": "dario-legal",
     },
     "WARN", "destructive"),

    ("destructive with confirmation",
     {
         "id": "TEST-004",
         "title": "delete all old client data",
         "description": "Remove every record older than 2 years. User approved this on call.",
         "project": "atrium",
         "skill": "dario-legal",
         "confirmation_received": True,
     },
     "PASS", None),

    ("missing project field",
     {
         "id": "TEST-005",
         "title": "Generate marketing content for blog",
         "description": "Three SEO-optimized articles about Portugal real estate trends",
         "skill": "dario-content",
     },
     "WARN", "project"),

    ("DIVA skill on SaaS project — incoherent",
     {
         "id": "TEST-006",
         "title": "Render 3D do dashboard",
         "description": "Criar render fotorrealista do dashboard com 8 KPIs principais",
         "project": "lucas saas audit",
         "skill": "diva-render",
     },
     "WARN", "DIVA"),

    ("critical task without success criteria",
     {
         "id": "TEST-007",
         "title": "Lancar marketing campaign next week",
         "description": "Coordenar com todos os canais e fazer lancamento perfeito",
         "project": "atrium",
         "skill": "dario-content",
         "execution_policy": "critical",
     },
     "WARN", "success_criteria"),

    ("empty task",
     {"id": "TEST-008", "title": "", "description": ""},
     "FAIL", None),
]


def run():
    passed = 0
    failed = 0
    for label, task, expected_verdict, must_have in SCENARIOS:
        result = evaluate(task)
        verdict_ok = result["verdict"] == expected_verdict
        reason_ok = True
        if must_have:
            all_reasons = " ".join(
                result["clarity"]["reasons"]
                + result["freedom"]["reasons"]
                + result["coherence"]["reasons"]
            ).lower()
            reason_ok = must_have.lower() in all_reasons

        ok = verdict_ok and reason_ok
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {label}")
        print(f"         verdict: {result['verdict']} (expected {expected_verdict})  "
              f"c={result['clarity']['score']} f={result['freedom']['score']} co={result['coherence']['score']}")
        if not ok:
            print(f"         clarity reasons:   {result['clarity']['reasons']}")
            print(f"         freedom reasons:   {result['freedom']['reasons']}")
            print(f"         coherence reasons: {result['coherence']['reasons']}")
            if must_have:
                print(f"         expected reason substring: '{must_have}'")
        if ok:
            passed += 1
        else:
            failed += 1
    print()
    print(f"Results: {passed} passed, {failed} failed (of {len(SCENARIOS)})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
