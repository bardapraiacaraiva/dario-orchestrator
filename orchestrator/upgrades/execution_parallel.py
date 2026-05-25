"""Parallel + Loop agents (extracted from `upgrades/execution.py` — Onda 6 #2).

Google ADK-inspired execution primitives:
    - `ExecutionMode` — sequential | parallel | loop | race
    - `AgentTask` — typed work unit
    - `ParallelAgent` — fan-out / fan-in over batched workers
    - `LoopAgent` — iterate-until-condition pattern

Parent `upgrades/execution.py` re-imports these for backward-compat.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum


class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    LOOP = "loop"
    RACE = "race"


@dataclass
class AgentTask:
    """A unit of work for execution primitives."""

    task_id: str
    skill: str
    input_data: dict = field(default_factory=dict)
    output_data: dict | None = None
    status: str = "pending"  # pending | running | completed | failed | skipped
    error: str | None = None
    duration_ms: int = 0


class ParallelAgent:
    """Fan-out N subtasks to workers, fan-in results.

    Inspired by Google ADK's ParallelAgent primitive.
    """

    @staticmethod
    def execute(
        tasks: list[AgentTask],
        max_parallel: int = 3,
        executor_fn: Callable | None = None,
    ) -> list[AgentTask]:
        """Execute tasks in parallel batches, collect all results."""
        results = []
        for i in range(0, len(tasks), max_parallel):
            batch = tasks[i : i + max_parallel]
            batch_results = []
            for task in batch:
                start = time.time()
                try:
                    task.status = "running"
                    if executor_fn:
                        task.output_data = executor_fn(task)
                    else:
                        task.output_data = {"executed": True, "skill": task.skill}
                    task.status = "completed"
                except Exception as e:
                    task.status = "failed"
                    task.error = str(e)
                task.duration_ms = int((time.time() - start) * 1000)
                batch_results.append(task)
            results.extend(batch_results)
        return results

    @staticmethod
    def fan_in(
        results: list[AgentTask],
        merge_fn: Callable | None = None,
    ) -> dict:
        """Merge parallel results into a single output."""
        if merge_fn:
            merged: dict = merge_fn(results)
            return merged
        return {
            "total": len(results),
            "completed": sum(1 for r in results if r.status == "completed"),
            "failed": sum(1 for r in results if r.status == "failed"),
            "outputs": {
                r.task_id: r.output_data for r in results if r.output_data
            },
        }


class LoopAgent:
    """Iterate until a condition is met.

    Inspired by Google ADK's LoopAgent primitive.
    """

    @staticmethod
    def execute(
        task: AgentTask,
        condition_fn: Callable,
        executor_fn: Callable,
        max_iterations: int = 10,
    ) -> AgentTask:
        """Execute task repeatedly until condition_fn returns True."""
        for i in range(max_iterations):
            start = time.time()
            try:
                task.status = "running"
                task.output_data = executor_fn(task, iteration=i)
                task.duration_ms += int((time.time() - start) * 1000)

                if condition_fn(task, i):
                    task.status = "completed"
                    if task.output_data is not None:
                        task.output_data["iterations"] = i + 1
                    return task
            except Exception as e:
                task.status = "failed"
                task.error = f"Iteration {i}: {e}"
                return task

        task.status = "completed"
        task.output_data = task.output_data or {}
        task.output_data["iterations"] = max_iterations
        task.output_data["max_reached"] = True
        return task


__all__ = ["ExecutionMode", "AgentTask", "ParallelAgent", "LoopAgent"]
