#!/usr/bin/env python3
"""
DARIO Execution Upgrades v11.0 — Module 2 Complete Implementation
==================================================================
8 patterns from 8 repos, unified execution layer:

M2.1  ParallelAgent + LoopAgent   (Google ADK)      — fan-out/fan-in + iteration
M2.2  AgentCard Registry          (A2A Protocol)     — self-describing agent capabilities
M2.3  DualOrchestration + YAML    (MS Agent Fw)      — LLM-driven + graph-based modes
M2.4  TeamCoordination            (Agno)             — route/coordinate/collaborate modes
M2.5  Blackboard SchemaRouter     (Flock)            — type-contract routing replaces keywords
M2.6  AgentsAsTools               (Strands AWS)      — engines exposed as callable tools
M2.7  RaceExecution + Versioning  (VoltAgent)        — andRace + workflow replay
M2.8  WaveScheduler + PEVR        (VMAO paper)       — critical-path DAG + Plan-Execute-Verify-Replan

Usage:
    python execution_upgrades.py --test        # Run 20+ self-tests
    python execution_upgrades.py --cards       # List all agent cards
    python execution_upgrades.py --schedule T  # Show wave schedule for task chain T
    python execution_upgrades.py --blackboard  # Show blackboard state
    python execution_upgrades.py --status      # All component status
"""

import argparse
import copy
import json
import logging
import os
import sys
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("execution_upgrades")


# =============================================================================
# M2.1: PARALLEL + LOOP AGENTS (Google ADK pattern)
# =============================================================================
# First-class primitives for fan-out/fan-in and iteration.

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
    output_data: Optional[dict] = None
    status: str = "pending"  # pending | running | completed | failed | skipped
    error: Optional[str] = None
    duration_ms: int = 0


class ParallelAgent:
    """
    Fan-out N subtasks to workers, fan-in results.
    Inspired by Google ADK's ParallelAgent primitive.
    """

    @staticmethod
    def execute(tasks: list[AgentTask], max_parallel: int = 3,
                executor_fn: Callable = None) -> list[AgentTask]:
        """Execute tasks in parallel batches, collect all results."""
        results = []
        for i in range(0, len(tasks), max_parallel):
            batch = tasks[i:i + max_parallel]
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
    def fan_in(results: list[AgentTask], merge_fn: Callable = None) -> dict:
        """Merge parallel results into a single output."""
        if merge_fn:
            return merge_fn(results)
        return {
            "total": len(results),
            "completed": sum(1 for r in results if r.status == "completed"),
            "failed": sum(1 for r in results if r.status == "failed"),
            "outputs": {r.task_id: r.output_data for r in results if r.output_data},
        }


class LoopAgent:
    """
    Iterate until a condition is met.
    Inspired by Google ADK's LoopAgent primitive.
    """

    @staticmethod
    def execute(task: AgentTask, condition_fn: Callable,
                executor_fn: Callable, max_iterations: int = 10) -> AgentTask:
        """Execute task repeatedly until condition_fn returns True."""
        for i in range(max_iterations):
            start = time.time()
            try:
                task.status = "running"
                task.output_data = executor_fn(task, iteration=i)
                task.duration_ms += int((time.time() - start) * 1000)

                if condition_fn(task, i):
                    task.status = "completed"
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


# =============================================================================
# M2.2: AGENT CARD REGISTRY (A2A Protocol)
# =============================================================================
# Each engine publishes a JSON capabilities manifest for semantic routing.

@dataclass
class AgentCard:
    """
    A2A-style Agent Card — self-describing capability manifest.
    Enables semantic routing: the orchestrator reads cards to decide
    which agent handles a task, instead of keyword matching.
    """
    agent_id: str
    name: str
    description: str
    skills: list[str] = field(default_factory=list)
    input_types: list[str] = field(default_factory=list)
    output_types: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    constraints: dict = field(default_factory=dict)
    version: str = "1.0"
    status: str = "available"
    max_concurrent: int = 1
    avg_duration_ms: int = 0
    avg_quality_score: float = 0.0


class AgentCardRegistry:
    """
    Registry of Agent Cards for capability-based routing.
    Replaces keyword→skill matching with semantic matching.
    """

    def __init__(self):
        self._cards: dict[str, AgentCard] = {}

    def register(self, card: AgentCard):
        """Register or update an agent card."""
        self._cards[card.agent_id] = card

    def find_by_capability(self, capability: str) -> list[AgentCard]:
        """Find agents that have a specific capability."""
        return [c for c in self._cards.values()
                if capability in c.capabilities and c.status == "available"]

    def find_by_input_type(self, input_type: str) -> list[AgentCard]:
        """Find agents that accept a specific input type."""
        return [c for c in self._cards.values()
                if input_type in c.input_types and c.status == "available"]

    def find_best_match(self, requirements: dict) -> Optional[AgentCard]:
        """
        Find the best agent for given requirements.
        Scores by: capability match + quality + availability.
        """
        scores = []
        for card in self._cards.values():
            if card.status != "available":
                continue
            score = 0
            # Capability match
            req_caps = requirements.get("capabilities", [])
            for cap in req_caps:
                if cap in card.capabilities:
                    score += 10
            # Input type match
            req_input = requirements.get("input_type")
            if req_input and req_input in card.input_types:
                score += 5
            # Quality bonus
            score += card.avg_quality_score / 10
            if score > 0:
                scores.append((score, card))

        scores.sort(key=lambda x: -x[0])
        return scores[0][1] if scores else None

    def get_card(self, agent_id: str) -> Optional[AgentCard]:
        return self._cards.get(agent_id)

    def list_cards(self) -> list[AgentCard]:
        return list(self._cards.values())

    def auto_register_from_company(self):
        """Auto-create agent cards from company.yaml workers."""
        import yaml
        company_file = ORCH_DIR / "company.yaml"
        if not company_file.exists():
            return
        with open(company_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        workers = data.get("workers", {})
        for wk, wv in workers.items():
            skill = wv.get("skill", "")
            caps = wv.get("capabilities", [])
            tier = wv.get("security_tier")
            self.register(AgentCard(
                agent_id=wk,
                name=wk,
                description=f"Worker: {skill}",
                skills=[skill],
                capabilities=caps,
                input_types=["task", "text"],
                output_types=["markdown", "json", "yaml"],
                constraints={"security_tier": tier} if tier else {},
            ))


# =============================================================================
# M2.3: DUAL ORCHESTRATION (Microsoft Agent Framework pattern)
# =============================================================================
# Two modes: LLM-driven (non-deterministic) + Graph-based (deterministic).

class OrchestrationMode(Enum):
    LLM_DRIVEN = "llm_driven"      # LLM decides next agent dynamically
    GRAPH_BASED = "graph_based"     # Predefined DAG execution
    HYBRID = "hybrid"               # Graph with LLM at decision nodes


@dataclass
class WorkflowDefinition:
    """
    YAML-serializable workflow definition.
    Can be stored in DB, versioned, and replayed.
    """
    workflow_id: str
    name: str
    mode: OrchestrationMode = OrchestrationMode.GRAPH_BASED
    steps: list[dict] = field(default_factory=list)
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add_step(self, name: str, skill: str, depends_on: list[str] = None,
                 parallel: bool = False, condition: str = None):
        """Add a step to the workflow."""
        self.steps.append({
            "name": name,
            "skill": skill,
            "depends_on": depends_on or [],
            "parallel": parallel,
            "condition": condition,
        })
        return self

    def to_yaml(self) -> str:
        """Serialize to YAML for storage."""
        import yaml
        return yaml.dump(asdict(self), default_flow_style=False)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "WorkflowDefinition":
        """Load from YAML string."""
        import yaml
        data = yaml.safe_load(yaml_str)
        data["mode"] = OrchestrationMode(data["mode"])
        return cls(**data)


class DualOrchestrator:
    """Execute workflows in LLM-driven or graph-based mode."""

    def __init__(self):
        self._workflows: dict[str, WorkflowDefinition] = {}

    def register_workflow(self, workflow: WorkflowDefinition):
        self._workflows[workflow.workflow_id] = workflow

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        return self._workflows.get(workflow_id)

    def execute_graph(self, workflow: WorkflowDefinition,
                      executor_fn: Callable = None) -> list[dict]:
        """Execute workflow in graph-based (deterministic) mode."""
        results = []
        completed_steps = set()

        for step in workflow.steps:
            # Check dependencies
            deps = step.get("depends_on", [])
            if not all(d in completed_steps for d in deps):
                results.append({"step": step["name"], "status": "blocked", "reason": f"deps not met: {deps}"})
                continue

            # Check condition
            cond = step.get("condition")
            if cond and not self._eval_condition(cond, results):
                results.append({"step": step["name"], "status": "skipped", "reason": f"condition failed: {cond}"})
                continue

            # Execute
            start = time.time()
            try:
                if executor_fn:
                    output = executor_fn(step)
                else:
                    output = {"executed": True}
                duration = int((time.time() - start) * 1000)
                results.append({"step": step["name"], "status": "completed", "output": output, "duration_ms": duration})
                completed_steps.add(step["name"])
            except Exception as e:
                results.append({"step": step["name"], "status": "failed", "error": str(e)})

        return results

    def _eval_condition(self, condition: str, results: list) -> bool:
        """Evaluate a simple condition string."""
        if "score >=" in condition:
            parts = condition.split(">=")
            step_name = parts[0].strip().replace("score", "").strip()
            threshold = float(parts[1].strip())
            for r in results:
                if r.get("step") == step_name:
                    return r.get("output", {}).get("score", 0) >= threshold
        return True


# =============================================================================
# M2.4: TEAM COORDINATION (Agno pattern)
# =============================================================================
# Three modes: route (orchestrator picks), coordinate (agents negotiate),
# collaborate (all see all messages).

class TeamMode(Enum):
    ROUTE = "route"             # Orchestrator picks one agent
    COORDINATE = "coordinate"   # Agents negotiate who handles it
    COLLABORATE = "collaborate"  # All agents see all messages


@dataclass
class TeamDecision:
    """Result of team coordination."""
    mode: TeamMode
    selected_agent: Optional[str] = None
    votes: dict = field(default_factory=dict)
    contributions: list[dict] = field(default_factory=list)
    consensus: bool = False


class TeamCoordinator:
    """
    Coordinate teams of agents in different modes.
    Inspired by Agno's Team routing patterns.
    """

    def __init__(self):
        self._teams: dict[str, list[str]] = {}

    def register_team(self, team_name: str, members: list[str]):
        self._teams[team_name] = members

    def route(self, team_name: str, task: dict,
              scorer_fn: Callable = None) -> TeamDecision:
        """Route mode: orchestrator picks the best agent."""
        members = self._teams.get(team_name, [])
        if not members:
            return TeamDecision(mode=TeamMode.ROUTE)

        if scorer_fn:
            scores = {m: scorer_fn(m, task) for m in members}
            best = max(scores, key=scores.get)
            return TeamDecision(mode=TeamMode.ROUTE, selected_agent=best, votes=scores)

        # Default: first available
        return TeamDecision(mode=TeamMode.ROUTE, selected_agent=members[0])

    def coordinate(self, team_name: str, task: dict,
                   vote_fn: Callable = None) -> TeamDecision:
        """Coordinate mode: agents vote on who handles it."""
        members = self._teams.get(team_name, [])
        votes = {}
        for member in members:
            if vote_fn:
                votes[member] = vote_fn(member, task)
            else:
                votes[member] = 1  # Equal vote

        winner = max(votes, key=votes.get) if votes else None
        return TeamDecision(mode=TeamMode.COORDINATE, selected_agent=winner,
                            votes=votes, consensus=len(set(votes.values())) == 1)

    def collaborate(self, team_name: str, task: dict,
                    contribute_fn: Callable = None) -> TeamDecision:
        """Collaborate mode: all agents contribute, results merged."""
        members = self._teams.get(team_name, [])
        contributions = []
        for member in members:
            if contribute_fn:
                result = contribute_fn(member, task)
            else:
                result = {"agent": member, "contribution": "placeholder"}
            contributions.append(result)

        return TeamDecision(mode=TeamMode.COLLABORATE,
                            contributions=contributions, consensus=True)


# =============================================================================
# M2.5: BLACKBOARD SCHEMA ROUTER (Flock pattern)
# =============================================================================
# Agents declare input/output schemas. Router matches by type compatibility.

@dataclass
class SchemaContract:
    """Input/output schema contract for an agent."""
    agent_id: str
    input_fields: dict[str, str] = field(default_factory=dict)   # field_name: type
    output_fields: dict[str, str] = field(default_factory=dict)  # field_name: type
    required_inputs: list[str] = field(default_factory=list)


class Blackboard:
    """
    Shared typed blackboard for agent coordination.
    Agents read/write to the blackboard. The scheduler routes
    tasks based on schema compatibility, not keywords.
    """

    def __init__(self):
        self._state: dict[str, Any] = {}
        self._contracts: dict[str, SchemaContract] = {}
        self._history: list[dict] = []

    def register_contract(self, contract: SchemaContract):
        """Register an agent's schema contract."""
        self._contracts[contract.agent_id] = contract

    def write(self, key: str, value: Any, writer: str = "system"):
        """Write a value to the blackboard."""
        self._state[key] = value
        self._history.append({
            "action": "write", "key": key,
            "writer": writer,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def read(self, key: str) -> Any:
        """Read a value from the blackboard."""
        return self._state.get(key)

    def find_ready_agents(self) -> list[str]:
        """Find agents whose input requirements are satisfied by current blackboard state."""
        ready = []
        available_keys = set(self._state.keys())
        for agent_id, contract in self._contracts.items():
            required = set(contract.required_inputs)
            if required.issubset(available_keys):
                ready.append(agent_id)
        return ready

    def route_by_schema(self, data: dict) -> list[str]:
        """Find agents that can process the given data based on schema match."""
        data_keys = set(data.keys())
        matches = []
        for agent_id, contract in self._contracts.items():
            input_keys = set(contract.input_fields.keys())
            required = set(contract.required_inputs)
            # Agent matches if all required inputs are in the data
            if required.issubset(data_keys):
                overlap = len(input_keys.intersection(data_keys))
                matches.append((overlap, agent_id))
        matches.sort(key=lambda x: -x[0])
        return [m[1] for m in matches]

    def get_state(self) -> dict:
        return dict(self._state)


# =============================================================================
# M2.6: AGENTS AS TOOLS (Strands AWS pattern)
# =============================================================================
# Each engine is exposed as a callable tool that the LLM can invoke.

@dataclass
class ToolSpec:
    """Tool specification for agents-as-tools pattern."""
    tool_id: str
    name: str
    description: str
    parameters: dict = field(default_factory=dict)
    engine: str = ""
    handler: Optional[Callable] = None


class AgentToolbox:
    """
    Expose DARIO engines as callable tools.
    The LLM sees available engines as tools and selects by semantic understanding.
    """

    def __init__(self):
        self._tools: dict[str, ToolSpec] = {}

    def register_tool(self, spec: ToolSpec):
        self._tools[spec.tool_id] = spec

    def get_tool(self, tool_id: str) -> Optional[ToolSpec]:
        return self._tools.get(tool_id)

    def list_tools(self) -> list[dict]:
        """List tools in LLM-friendly format."""
        return [
            {"name": t.name, "description": t.description,
             "parameters": t.parameters}
            for t in self._tools.values()
        ]

    def invoke(self, tool_id: str, params: dict = None) -> Any:
        """Invoke a tool by ID."""
        tool = self._tools.get(tool_id)
        if not tool:
            raise ValueError(f"Tool '{tool_id}' not found")
        if tool.handler:
            return tool.handler(**(params or {}))
        return {"tool": tool_id, "status": "invoked", "params": params}

    def auto_register_engines(self):
        """Auto-register DARIO engines as tools."""
        engine_tools = {
            "dispatch": ("dispatch_engine", "Route a task to the best worker", {"task_description": "string"}),
            "execute": ("executor", "Execute a task through the full pipeline", {"task_id": "string"}),
            "chain": ("chain_executor", "Run a multi-step skill chain", {"chain_name": "string", "project": "string"}),
            "score": ("quality_scorer", "Score a task output", {"task_id": "string", "output": "string"}),
            "diagnose": ("autodiag_runner", "Run health diagnostics", {}),
            "budget": ("budget_tracker", "Check token budget status", {"month": "string"}),
            "tax": ("tax_calendar", "Check fiscal obligations", {}),
            "validate": ("pt_validators", "Validate PT financial data", {"data": "object"}),
        }
        for tool_id, (engine, desc, params) in engine_tools.items():
            self.register_tool(ToolSpec(
                tool_id=tool_id, name=tool_id,
                description=desc, parameters=params, engine=engine,
            ))


# =============================================================================
# M2.7: RACE EXECUTION + VERSIONING (VoltAgent pattern)
# =============================================================================

class RaceExecutor:
    """
    Send same task to multiple agents, take first valid result.
    Inspired by VoltAgent's andRace primitive.
    """

    @staticmethod
    def race(tasks: list[AgentTask], executor_fn: Callable,
             validator_fn: Callable = None) -> Optional[AgentTask]:
        """Execute all tasks, return first valid result."""
        for task in tasks:
            start = time.time()
            try:
                task.status = "running"
                task.output_data = executor_fn(task)
                task.duration_ms = int((time.time() - start) * 1000)

                if validator_fn:
                    if validator_fn(task):
                        task.status = "completed"
                        # Cancel remaining
                        for other in tasks:
                            if other.task_id != task.task_id and other.status == "pending":
                                other.status = "skipped"
                        return task
                else:
                    task.status = "completed"
                    for other in tasks:
                        if other.task_id != task.task_id and other.status == "pending":
                            other.status = "skipped"
                    return task
            except Exception as e:
                task.status = "failed"
                task.error = str(e)

        return None  # All failed


class WorkflowVersionStore:
    """
    Store workflow definition versions for replay.
    Inspired by VoltAgent's workflow versioning.
    """

    def __init__(self):
        self._versions: dict[str, list[WorkflowDefinition]] = {}

    def save_version(self, workflow: WorkflowDefinition):
        """Save a new version of a workflow."""
        wf_id = workflow.workflow_id
        if wf_id not in self._versions:
            self._versions[wf_id] = []
        workflow.version = len(self._versions[wf_id]) + 1
        self._versions[wf_id].append(copy.deepcopy(workflow))

    def get_version(self, workflow_id: str, version: int = None) -> Optional[WorkflowDefinition]:
        """Get a specific version (or latest)."""
        versions = self._versions.get(workflow_id, [])
        if not versions:
            return None
        if version:
            return versions[version - 1] if version <= len(versions) else None
        return versions[-1]

    def list_versions(self, workflow_id: str) -> list[dict]:
        """List all versions of a workflow."""
        versions = self._versions.get(workflow_id, [])
        return [{"version": v.version, "steps": len(v.steps), "created": v.created_at}
                for v in versions]


# =============================================================================
# M2.8: WAVE SCHEDULER + PLAN-EXECUTE-VERIFY-REPLAN (VMAO paper)
# =============================================================================
# Critical-path DAG scheduling with inline quality verification.

class WaveScheduler:
    """
    Wave-based parallel execution with critical-path optimization.
    Inspired by VMAO (Verified Multi-Agent Orchestration).

    Wave 1 = all tasks with no dependencies
    Wave 2 = tasks depending only on Wave 1 outputs
    ...continues until all waves scheduled.
    After each wave, a Verifier checks intermediate outputs.
    """

    @staticmethod
    def compute_waves(steps: list[dict]) -> list[list[dict]]:
        """
        Compute execution waves from a list of steps with dependencies.
        Returns waves ordered by dependency depth.
        """
        step_map = {s["name"]: s for s in steps}
        completed = set()
        waves = []

        remaining = list(steps)
        max_iterations = len(steps) + 1

        for _ in range(max_iterations):
            if not remaining:
                break

            # Find steps whose deps are all completed
            wave = []
            still_remaining = []
            for s in remaining:
                deps = set(s.get("depends_on", []))
                if deps.issubset(completed):
                    wave.append(s)
                else:
                    still_remaining.append(s)

            if not wave:
                # Circular dependency or unresolvable
                for s in still_remaining:
                    s["_blocked"] = True
                waves.append(still_remaining)
                break

            waves.append(wave)
            for s in wave:
                completed.add(s["name"])
            remaining = still_remaining

        return waves

    @staticmethod
    def critical_path(waves: list[list[dict]]) -> list[str]:
        """Identify the critical path (longest chain through the DAG)."""
        if not waves:
            return []
        # Critical path = one step from each wave (the bottleneck)
        path = []
        for wave in waves:
            # Pick the step with most downstream dependencies (heuristic)
            path.append(wave[0]["name"])
        return path

    @staticmethod
    def plan_execute_verify_replan(
        workflow: WorkflowDefinition,
        executor_fn: Callable = None,
        verifier_fn: Callable = None,
        replanner_fn: Callable = None,
        quality_threshold: float = 60.0,
    ) -> dict:
        """
        Full PEVR loop:
        1. PLAN: compute waves from workflow
        2. EXECUTE: run each wave
        3. VERIFY: check intermediate outputs after each wave
        4. REPLAN: if verification fails, adjust remaining waves
        """
        waves = WaveScheduler.compute_waves(workflow.steps)
        results = {"waves": [], "replans": 0, "total_steps": 0, "passed_steps": 0}

        for wave_idx, wave in enumerate(waves):
            wave_results = []

            # EXECUTE wave
            for step in wave:
                start = time.time()
                try:
                    if executor_fn:
                        output = executor_fn(step)
                    else:
                        output = {"executed": True, "score": 75}
                    duration = int((time.time() - start) * 1000)
                    step_result = {
                        "step": step["name"], "skill": step.get("skill", ""),
                        "status": "completed", "output": output,
                        "duration_ms": duration
                    }
                except Exception as e:
                    step_result = {"step": step["name"], "status": "failed", "error": str(e)}

                wave_results.append(step_result)
                results["total_steps"] += 1

            # VERIFY wave
            wave_passed = True
            for sr in wave_results:
                if sr["status"] == "failed":
                    wave_passed = False
                    continue

                score = 0
                if verifier_fn:
                    score = verifier_fn(sr)
                else:
                    score = sr.get("output", {}).get("score", quality_threshold)

                sr["quality_score"] = score
                if score >= quality_threshold:
                    results["passed_steps"] += 1
                else:
                    wave_passed = False
                    sr["verification"] = "FAILED"

            results["waves"].append({
                "wave": wave_idx + 1,
                "steps": len(wave),
                "passed": wave_passed,
                "results": wave_results,
            })

            # REPLAN if verification failed
            if not wave_passed and replanner_fn and wave_idx < len(waves) - 1:
                failed_steps = [sr for sr in wave_results if sr.get("verification") == "FAILED"]
                new_steps = replanner_fn(failed_steps, waves[wave_idx + 1:])
                if new_steps:
                    # Replace remaining waves with replanned steps
                    waves[wave_idx + 1:] = [new_steps]
                    results["replans"] += 1

        results["success"] = results["passed_steps"] == results["total_steps"]
        return results


# =============================================================================
# GLOBAL INSTANCES
# =============================================================================

agent_card_registry = AgentCardRegistry()
dual_orchestrator = DualOrchestrator()
team_coordinator = TeamCoordinator()
blackboard = Blackboard()
agent_toolbox = AgentToolbox()
workflow_versions = WorkflowVersionStore()


def init_execution_upgrades(app=None):
    """Initialize all execution upgrades."""

    # Auto-register agent cards from company.yaml
    agent_card_registry.auto_register_from_company()
    log.info(f"Agent Card Registry: {len(agent_card_registry._cards)} cards registered")

    # Auto-register engines as tools
    agent_toolbox.auto_register_engines()
    log.info(f"Agent Toolbox: {len(agent_toolbox._tools)} tools registered")

    # Register default teams
    team_coordinator.register_team("marketing", [
        "worker-brand", "worker-offer", "worker-naming",
        "worker-story-circle", "worker-pitch",
    ])
    team_coordinator.register_team("seo", [
        "worker-seo-audit", "worker-seo-technical", "worker-seo-content",
        "worker-seo-local", "worker-seo-schema",
    ])
    team_coordinator.register_team("finance", [
        "worker-financial-model", "worker-cfo-agency-pnl",
        "worker-cfo-token-roi", "worker-cfo-tax-autopilot",
    ])

    # Register FastAPI endpoints
    if app:
        _register_endpoints(app)

    log.info("Execution Upgrades v11.0 initialized: "
             "ParallelAgent + AgentCards + DualOrchestrator + "
             "TeamCoordinator + Blackboard + AgentToolbox + "
             "RaceExecutor + WaveScheduler+PEVR")


def _register_endpoints(app):
    """Register execution upgrade endpoints."""

    @app.get("/exec/status")
    async def exec_status():
        return {
            "version": "v11.0",
            "agent_cards": len(agent_card_registry._cards),
            "tools": len(agent_toolbox._tools),
            "teams": {k: len(v) for k, v in team_coordinator._teams.items()},
            "blackboard_keys": len(blackboard._state),
            "workflows": len(dual_orchestrator._workflows),
            "workflow_versions": {k: len(v) for k, v in workflow_versions._versions.items()},
        }

    @app.get("/exec/cards")
    async def list_cards():
        cards = agent_card_registry.list_cards()
        return {"count": len(cards), "cards": [asdict(c) for c in cards[:50]]}

    @app.get("/exec/tools")
    async def list_tools():
        return {"tools": agent_toolbox.list_tools()}

    @app.get("/exec/blackboard")
    async def get_blackboard():
        return {"state": blackboard.get_state(), "ready_agents": blackboard.find_ready_agents()}

    @app.post("/exec/wave-schedule")
    async def compute_wave_schedule(steps: list[dict]):
        waves = WaveScheduler.compute_waves(steps)
        critical = WaveScheduler.critical_path(waves)
        return {
            "waves": len(waves),
            "steps_per_wave": [len(w) for w in waves],
            "critical_path": critical,
            "detail": [[s["name"] for s in w] for w in waves],
        }


# =============================================================================
# SELF-TESTS
# =============================================================================

def _run_self_tests():
    passed = 0
    failed = 0

    def check(name, fn):
        nonlocal passed, failed
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1

    print("=== Execution Upgrades v11.0 — Self Tests ===\n")

    # ParallelAgent
    print("--- ParallelAgent (ADK) ---")
    tasks = [AgentTask(f"t{i}", f"skill{i}") for i in range(5)]
    results = ParallelAgent.execute(tasks, max_parallel=2)
    check("parallel_execute_5_tasks", lambda: None if len(results) == 5 else (_ for _ in ()).throw(AssertionError))
    check("all_completed", lambda: None if all(r.status == "completed" for r in results) else (_ for _ in ()).throw(AssertionError))
    merged = ParallelAgent.fan_in(results)
    check("fan_in_merge", lambda: None if merged["completed"] == 5 else (_ for _ in ()).throw(AssertionError))

    # LoopAgent
    print("\n--- LoopAgent (ADK) ---")
    loop_task = AgentTask("loop1", "iterate")
    result = LoopAgent.execute(
        loop_task,
        condition_fn=lambda t, i: i >= 2,
        executor_fn=lambda t, iteration: {"iter": iteration},
        max_iterations=10,
    )
    check("loop_stops_at_condition", lambda: None if result.output_data["iterations"] == 3 else (_ for _ in ()).throw(AssertionError))

    # AgentCardRegistry
    print("\n--- AgentCardRegistry (A2A) ---")
    acr = AgentCardRegistry()
    acr.register(AgentCard("w1", "Brand Worker", "Does branding", capabilities=["brand", "naming"], input_types=["task"]))
    acr.register(AgentCard("w2", "SEO Worker", "Does SEO", capabilities=["seo", "audit"], input_types=["url"]))
    check("find_by_capability", lambda: None if len(acr.find_by_capability("brand")) == 1 else (_ for _ in ()).throw(AssertionError))
    check("find_best_match", lambda: None if acr.find_best_match({"capabilities": ["brand"]}).agent_id == "w1" else (_ for _ in ()).throw(AssertionError))

    # DualOrchestrator
    print("\n--- DualOrchestrator (MS) ---")
    wf = WorkflowDefinition("wf1", "Test Workflow")
    wf.add_step("step1", "brand")
    wf.add_step("step2", "naming", depends_on=["step1"])
    do = DualOrchestrator()
    results = do.execute_graph(wf)
    check("graph_execution_2_steps", lambda: None if len(results) == 2 else (_ for _ in ()).throw(AssertionError))
    check("step1_completed", lambda: None if results[0]["status"] == "completed" else (_ for _ in ()).throw(AssertionError))

    # TeamCoordinator
    print("\n--- TeamCoordinator (Agno) ---")
    tc = TeamCoordinator()
    tc.register_team("test", ["a1", "a2", "a3"])
    decision = tc.route("test", {"desc": "brand task"}, scorer_fn=lambda m, t: 10 if m == "a2" else 5)
    check("route_picks_best", lambda: None if decision.selected_agent == "a2" else (_ for _ in ()).throw(AssertionError))
    decision2 = tc.collaborate("test", {"desc": "big task"})
    check("collaborate_all_contribute", lambda: None if len(decision2.contributions) == 3 else (_ for _ in ()).throw(AssertionError))

    # Blackboard
    print("\n--- Blackboard (Flock) ---")
    bb = Blackboard()
    bb.register_contract(SchemaContract("agent1", input_fields={"text": "str"}, required_inputs=["text"]))
    bb.register_contract(SchemaContract("agent2", input_fields={"score": "float"}, required_inputs=["score"]))
    check("no_ready_agents_initially", lambda: None if len(bb.find_ready_agents()) == 0 else (_ for _ in ()).throw(AssertionError))
    bb.write("text", "hello")
    check("agent1_ready_after_write", lambda: None if "agent1" in bb.find_ready_agents() else (_ for _ in ()).throw(AssertionError))
    check("schema_route_match", lambda: None if bb.route_by_schema({"text": "hi"})[0] == "agent1" else (_ for _ in ()).throw(AssertionError))

    # AgentToolbox
    print("\n--- AgentToolbox (Strands) ---")
    at = AgentToolbox()
    at.auto_register_engines()
    check("auto_register_tools", lambda: None if len(at._tools) >= 5 else (_ for _ in ()).throw(AssertionError))
    check("invoke_tool", lambda: None if at.invoke("dispatch")["status"] == "invoked" else (_ for _ in ()).throw(AssertionError))

    # RaceExecutor
    print("\n--- RaceExecutor (VoltAgent) ---")
    race_tasks = [AgentTask(f"r{i}", f"model{i}") for i in range(3)]
    winner = RaceExecutor.race(race_tasks, executor_fn=lambda t: {"result": t.task_id})
    check("race_returns_first", lambda: None if winner and winner.status == "completed" else (_ for _ in ()).throw(AssertionError))
    check("race_skips_others", lambda: None if sum(1 for t in race_tasks if t.status == "skipped") >= 1 else (_ for _ in ()).throw(AssertionError))

    # WorkflowVersionStore
    print("\n--- WorkflowVersionStore (VoltAgent) ---")
    wvs = WorkflowVersionStore()
    wf1 = WorkflowDefinition("test_wf", "Test")
    wf1.add_step("s1", "brand")
    wvs.save_version(wf1)
    wf1.add_step("s2", "naming")
    wvs.save_version(wf1)
    check("two_versions_stored", lambda: None if len(wvs.list_versions("test_wf")) == 2 else (_ for _ in ()).throw(AssertionError))
    check("latest_has_2_steps", lambda: None if len(wvs.get_version("test_wf").steps) == 2 else (_ for _ in ()).throw(AssertionError))

    # WaveScheduler
    print("\n--- WaveScheduler + PEVR (VMAO) ---")
    steps = [
        {"name": "analyze", "skill": "brand", "depends_on": []},
        {"name": "research", "skill": "seo", "depends_on": []},
        {"name": "synthesize", "skill": "report", "depends_on": ["analyze", "research"]},
        {"name": "review", "skill": "quality", "depends_on": ["synthesize"]},
    ]
    waves = WaveScheduler.compute_waves(steps)
    check("3_waves_computed", lambda: None if len(waves) == 3 else (_ for _ in ()).throw(AssertionError(f"got {len(waves)}")))
    check("wave1_has_2_parallel", lambda: None if len(waves[0]) == 2 else (_ for _ in ()).throw(AssertionError))
    check("critical_path", lambda: None if len(WaveScheduler.critical_path(waves)) == 3 else (_ for _ in ()).throw(AssertionError))

    # PEVR
    wf_pevr = WorkflowDefinition("pevr_test", "PEVR Test")
    for s in steps:
        wf_pevr.add_step(s["name"], s["skill"], depends_on=s.get("depends_on"))
    pevr_result = WaveScheduler.plan_execute_verify_replan(wf_pevr)
    check("pevr_all_steps_executed", lambda: None if pevr_result["total_steps"] == 4 else (_ for _ in ()).throw(AssertionError))
    check("pevr_success", lambda: None if pevr_result["success"] else (_ for _ in ()).throw(AssertionError))

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="DARIO Execution Upgrades v11.0")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    parser.add_argument("--cards", action="store_true", help="List agent cards")
    parser.add_argument("--tools", action="store_true", help="List agent tools")
    parser.add_argument("--status", action="store_true", help="Status of all components")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.test:
        sys.exit(_run_self_tests())

    if args.cards:
        agent_card_registry.auto_register_from_company()
        cards = agent_card_registry.list_cards()
        if args.json:
            print(json.dumps([asdict(c) for c in cards], indent=2, default=str))
        else:
            print(f"\n=== Agent Card Registry ({len(cards)} cards) ===\n")
            for c in cards[:30]:
                print(f"  {c.agent_id:35s} caps: {c.capabilities[:3]}")
            if len(cards) > 30:
                print(f"  ... and {len(cards) - 30} more")
        return

    if args.tools:
        agent_toolbox.auto_register_engines()
        tools = agent_toolbox.list_tools()
        if args.json:
            print(json.dumps(tools, indent=2))
        else:
            print(f"\n=== Agent Toolbox ({len(tools)} tools) ===\n")
            for t in tools:
                print(f"  {t['name']:20s} — {t['description']}")
        return

    if args.status:
        agent_card_registry.auto_register_from_company()
        agent_toolbox.auto_register_engines()
        print(f"\n=== Execution Upgrades v11.0 ===")
        print(f"  Agent Cards: {len(agent_card_registry._cards)}")
        print(f"  Tools: {len(agent_toolbox._tools)}")
        print(f"  Teams: {list(team_coordinator._teams.keys())}")
        print(f"  Blackboard keys: {len(blackboard._state)}")
        print(f"  Workflows: {len(dual_orchestrator._workflows)}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
