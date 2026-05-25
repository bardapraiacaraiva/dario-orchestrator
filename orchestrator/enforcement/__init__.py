"""Thin enforcement layer — Python invariants for orchestrator dispatch.

Closes audit Risk #1 (orchestrator = markdown). Before this package,
critical invariants ("max 3 parallel workers", "stop if budget >= 95%",
"validate task before dispatch") were enforced only by Claude reading
SKILL.md markdown and choosing to honor them. No code path actually
blocked violations.

This package adds Python-enforced rails on the three most-impactful
invariants. Wrappers call these guards before any dispatch decision;
violations raise exceptions that the orchestrator MUST handle.

Modules:
    budget_gate         — hard stop when monthly budget >= threshold
    dispatch_validator  — schema-validate task against company.yaml rules
    parallelism_guard   — process-level lock on max concurrent dispatches

Design principles:
    1. Real exceptions, not warnings. The whole point is to make
       violations LOUD and unmissable.
    2. Cross-process safe. parallelism_guard uses filelock so two
       Python processes can't both believe they're under the limit.
    3. No silent fallback. Failed guard = blocked dispatch.
    4. Testable. Every guard has behavior tests, not config checks.

Usage pattern:
    from enforcement.budget_gate import check_budget_or_raise
    from enforcement.dispatch_validator import validate_task_or_raise
    from enforcement.parallelism_guard import slot

    check_budget_or_raise()                  # raises if >= 95%
    validate_task_or_raise(task_dict)        # raises if schema invalid
    with slot():                              # blocks if max parallel hit
        dispatch_to_worker(task)
"""

from __future__ import annotations


class EnforcementError(Exception):
    """Base for all enforcement violations."""


class BudgetExceededError(EnforcementError):
    """Monthly budget at/above hard-stop threshold."""


class ParallelismExceededError(EnforcementError):
    """Max concurrent dispatches already claimed."""


class TaskValidationError(EnforcementError):
    """Task dict failed pre-dispatch validation."""


__all__ = [
    "EnforcementError",
    "BudgetExceededError",
    "ParallelismExceededError",
    "TaskValidationError",
]
