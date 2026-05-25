#!/usr/bin/env python3
"""End-to-end test for Upgrade 1 semantic dispatch integration."""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from dispatch.dispatch_engine import SEMANTIC_DISPATCH_ENABLED, infer_skill_from_task

SCENARIOS = [
    # (label, task_dict, expected_skill_or_acceptable_set, expected_path)
    ("explicit skill wins",
     {"skill": "dario-brand", "title": "anything", "description": "..."},
     {"dario-brand"}, "explicit"),

    ("WordPress slow checkout — semantic should beat keyword",
     {"title": "Site WordPress muito lento no checkout WooCommerce",
      "description": "O site demora 8 segundos para carregar o checkout, perdendo clientes"},
     {"dario-woo-audit", "dario-wp-audit", "dario-cwv-fix"}, "semantic_or_keyword"),

    ("SEO audit — clear case",
     {"title": "Auditoria SEO completa",
      "description": "Preciso de uma auditoria SEO completa do site para identificar todos os problemas"},
     {"seo-audit"}, "semantic_or_keyword"),

    ("Pitch deck — clear",
     {"title": "Criar pitch deck para investidores",
      "description": "Apresentação para round seed, 12 slides estilo Sequoia"},
     {"dario-pitch", "a360-pitch"}, "semantic_or_keyword"),

    ("Empty task fields",
     {"title": "", "description": ""},
     {None}, "no_match"),

    ("Pure ambiguity — should not crash",
     {"title": "ajuda", "description": "preciso de ajuda com isto"},
     None, "any"),  # any result acceptable, just must not crash
]


def run():
    print(f"SEMANTIC_DISPATCH_ENABLED = {SEMANTIC_DISPATCH_ENABLED}")
    passed = 0
    failed = 0
    for label, task, expected, path in SCENARIOS:
        try:
            result = infer_skill_from_task(task)
            if expected is None:
                ok = True  # any result accepted
            elif None in expected and result is None:
                ok = True
            elif result in expected:
                ok = True
            else:
                ok = False
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {label}")
            print(f"         got: {result!r}  expected: {expected}")
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [FAIL] {label} — CRASHED: {e}")
            failed += 1
    print()
    print(f"Results: {passed} passed, {failed} failed (of {len(SCENARIOS)})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
