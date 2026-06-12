"""Behavior tests for the CoT confidence gate in find_best_worker (Onda 3).

Advisory→enforced: a low-confidence semantic verdict across the skill surface
is how unrelated industry skills hijacked tasks (the medik misroute). Below
LOW_CONF_THRESHOLD the auto path must QUEUE, not guess — unless the task
carries an explicit skill (most-specific-wins).
"""

import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import dispatch.dispatch_engine as de


class _StubHierarchy:
    def get_worker_for_skill(self, skill):
        return "worker-stub"  # engine contract: worker ID string

    def get_siblings(self, worker_id):
        return []

    def get_director(self, worker_id):
        return None


def _low_conf_reason(task, persist=True):
    return {"decision": {"winner": "medik-totally-wrong", "confidence": 0.21,
                         "level": "LOW", "agreement": "1/4"}}


def _high_conf_reason(task, persist=True):
    return {"decision": {"winner": "dario-wp-audit", "confidence": 0.88,
                         "level": "HIGH", "agreement": "4/4"}}


def test_low_confidence_queues_instead_of_guessing(monkeypatch):
    import dispatch.dispatch_cot as cot
    monkeypatch.setattr(cot, "reason", _low_conf_reason)

    task = {"id": "GATE-001", "title": "coisa ambígua sem rota óbvia", "description": ""}
    worker, reasons = de.find_best_worker(task, _StubHierarchy(), workload={})

    assert worker is None, f"low-confidence task must queue, got {worker}"
    assert any("COT_LOW_CONFIDENCE" in r for r in reasons), reasons


def test_explicit_skill_bypasses_gate(monkeypatch):
    import dispatch.dispatch_cot as cot
    monkeypatch.setattr(cot, "reason", _low_conf_reason)

    task = {"id": "GATE-002", "title": "coisa ambígua", "description": "",
            "skill": "dario-wp-audit"}
    worker, reasons = de.find_best_worker(task, _StubHierarchy(), workload={})

    # Most-specific-wins: the user named the route; low CoT confidence is advisory here
    assert not any("COT_LOW_CONFIDENCE" in r for r in reasons), reasons
    assert worker == "worker-stub"


def test_high_confidence_proceeds(monkeypatch):
    import dispatch.dispatch_cot as cot
    monkeypatch.setattr(cot, "reason", _high_conf_reason)

    task = {"id": "GATE-003", "title": "auditoria wordpress do site", "description": "",
            "skill": "dario-wp-audit"}
    worker, reasons = de.find_best_worker(task, _StubHierarchy(), workload={})

    assert worker == "worker-stub"
    assert any("COT: winner=" in r for r in reasons), reasons
