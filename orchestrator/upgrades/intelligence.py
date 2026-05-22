#!/usr/bin/env python3
"""
DARIO Intelligence Upgrades v11.0 — Module 3 Complete Implementation
=====================================================================
8 patterns from 8 repos — the learning brain of the orchestrator:

M3.1  TieredMemory           (mem0)       — user/session/agent/project memory layers
M3.2  QValueEpisodicMemory   (MemRL)      — RL-based selection from past experiences
M3.3  GraphRAG               (LightRAG)   — entity/relationship graph for retrieval
M3.4  LearnedRouter          (RouteLLM)   — data-driven model routing with calibration
M3.5  ToolMemory             (MemOS)      — persist learned tool-use patterns
M3.6  BenchmarkEvolution     (EvoAgentX)  — mutate workflows, test against benchmarks
M3.7  ResearchMetrics        (deepeval)   — 50+ research-backed eval metrics
M3.8  RedTeamCI              (promptfoo)  — adversarial testing as CI gate

Usage:
    python intelligence_upgrades.py --test      # 20+ self-tests
    python intelligence_upgrades.py --memory    # Show tiered memory stats
    python intelligence_upgrades.py --graph     # Show knowledge graph stats
    python intelligence_upgrades.py --router    # Show routing decisions history
    python intelligence_upgrades.py --status    # All components
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict
from pathlib import Path

ORCH_DIR = Path(os.path.expanduser("~/.claude/orchestrator"))
DB_PATH = ORCH_DIR / "orchestrator.db"

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("intelligence_upgrades")


# =============================================================================
# M3.1: TIERED MEMORY (mem0 pattern) — extracted to intelligence_tiered.py (Onda 4 #3)
# =============================================================================
# Re-imported so existing callers `from upgrades.intelligence import TieredMemory` keep working.
# =============================================================================
# M3.2: Q-VALUE EPISODIC MEMORY (MemRL pattern)
# =============================================================================
# Store past experiences with Q-values. Select strategies with highest utility.
# Episode + QValueMemory moved to upgrades/intelligence_qvalue.py (Onda 3 #2).
# Re-imported here so existing callers keep working.
# =============================================================================
# M3.3: GRAPH RAG (LightRAG pattern) — extracted to intelligence_kg.py (Onda 5 #1)
# M3.4: LEARNED ROUTER (RouteLLM pattern) — extracted to intelligence_router.py (Onda 5 #1)
# =============================================================================
# Legacy block below (M3.3 + M3.4) preserved as a stripped triple-quoted dump
# for grep-friendly diff archaeology. The live classes come from the imports
# above. Will be deleted in Onda 6 once the dust settles.
# Original M3.3 (KnowledgeGraph) + M3.4 (LearnedRouter) source removed Onda 5 #1.
# See upgrades/intelligence_kg.py and upgrades/intelligence_router.py for the live code.
# =============================================================================
# M3.5: TOOL MEMORY (MemOS pattern) — extracted to intelligence_tools.py (Onda 6 #1)
# M3.6: BENCHMARK EVOLUTION (EvoAgentX pattern) — extracted to intelligence_benchmark.py
# M3.7 + M3.8: METRICS REGISTRY (deepeval + garak) — extracted to intelligence_metrics.py
# =============================================================================
from upgrades.intelligence_benchmark import BenchmarkEvolution, Mutation  # noqa: F401
from upgrades.intelligence_kg import GraphEntity, GraphRelation, KnowledgeGraph  # noqa: F401
from upgrades.intelligence_metrics import MetricsRegistry  # noqa: F401
from upgrades.intelligence_qvalue import Episode, QValueMemory  # noqa: F401
from upgrades.intelligence_router import LearnedRouter, RoutingDecision  # noqa: F401
from upgrades.intelligence_tiered import (  # noqa: F401
    MemoryEntry,
    MemoryTier,
    TieredMemory,
)
from upgrades.intelligence_tools import ToolMemory, ToolPattern  # noqa: F401

# =============================================================================
# GLOBAL INSTANCES
# =============================================================================

tiered_memory = TieredMemory()
q_value_memory = QValueMemory()
knowledge_graph = KnowledgeGraph()
learned_router = LearnedRouter()
tool_memory = ToolMemory()
benchmark_evolution = BenchmarkEvolution()
metrics_registry = MetricsRegistry()


def init_intelligence_upgrades(app=None):
    """Initialize all intelligence upgrades."""

    # Auto-build knowledge graph from task history
    knowledge_graph.auto_build_from_tasks()
    log.info(f"Knowledge Graph: {knowledge_graph.stats()}")

    if app:
        _register_endpoints(app)

    log.info("Intelligence Upgrades v11.0 initialized: "
             "TieredMemory + QValueMemory + KnowledgeGraph + "
             "LearnedRouter + ToolMemory + BenchmarkEvolution + "
             "MetricsRegistry")


def _register_endpoints(app):
    """Register intelligence upgrade endpoints."""

    @app.get("/intel/status")
    async def intel_status():
        return {
            "version": "v11.0",
            "tiered_memory": tiered_memory.stats(),
            "q_value_memory": q_value_memory.stats(),
            "knowledge_graph": knowledge_graph.stats(),
            "learned_router": learned_router.get_savings_report(),
            "tool_memory": tool_memory.stats(),
            "benchmark_evolution": benchmark_evolution.stats(),
            "metrics": len(MetricsRegistry.METRICS),
            "red_team_probes": len(MetricsRegistry.RED_TEAM_PROBES),
        }

    @app.get("/intel/memory")
    async def memory_stats():
        return tiered_memory.stats()

    @app.get("/intel/memory/recall")
    async def recall_memory(query: str, tier: str = None):
        t = MemoryTier(tier) if tier else None
        return {"results": tiered_memory.recall(query, tier=t)}

    @app.get("/intel/graph")
    async def graph_stats():
        return knowledge_graph.stats()

    @app.get("/intel/graph/search")
    async def graph_search(query: str):
        return {"results": knowledge_graph.hybrid_search(query)}

    @app.get("/intel/router/report")
    async def router_report():
        return learned_router.get_savings_report()

    @app.post("/intel/router/route")
    async def route_task(description: str, skill: str = "", quality: float = 70):
        decision = learned_router.route(description, skill, quality)
        return asdict(decision)


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

    print("=== Intelligence Upgrades v11.0 — Self Tests ===\n")

    # TieredMemory
    print("--- TieredMemory (mem0) ---")
    tm = TieredMemory()
    eid = tm.store("Brand positioning for restaurant in Cascais", MemoryTier.PROJECT,
                   scope="mar-brasa", tags=["brand", "cascais"], importance=0.8)
    check("store_memory", lambda: None if eid else (_ for _ in ()).throw(AssertionError))
    tm.store("IVA trimestral deadline approaching", MemoryTier.AGENT,
             scope="cfo", tags=["iva", "tax", "deadline"], importance=0.9)
    results = tm.recall("brand restaurant cascais")
    check("recall_by_keywords", lambda: None if len(results) > 0 else (_ for _ in ()).throw(AssertionError))
    check("recall_scored", lambda: None if results[0]["score"] > 0.1 else (_ for _ in ()).throw(AssertionError))
    stats = tm.stats()
    check("memory_stats", lambda: None if stats["total"] >= 2 else (_ for _ in ()).throw(AssertionError))

    # QValueMemory
    print("\n--- QValueMemory (MemRL) ---")
    qm = QValueMemory()
    qm.record("brand positioning restaurant", "kapferer_prism", "dario-brand", 85)
    qm.record("brand positioning saas", "storybrand_sb7", "dario-brand", 72)
    qm.record("brand positioning restaurant", "kapferer_prism", "dario-brand", 90)
    strategies = qm.select_strategy("brand positioning for restaurant in Lisbon")
    check("select_strategy", lambda: None if len(strategies) > 0 else (_ for _ in ()).throw(AssertionError))
    check("kapferer_ranked_higher", lambda: None if strategies[0]["strategy"] == "kapferer_prism" else (_ for _ in ()).throw(AssertionError))
    check("q_value_updated", lambda: None if strategies[0]["q_value"] > 0.8 else (_ for _ in ()).throw(AssertionError(f"q={strategies[0]['q_value']}")))

    # KnowledgeGraph
    print("\n--- KnowledgeGraph (LightRAG) ---")
    kg = KnowledgeGraph()
    kg.add_entity("proj_mb", "Mar & Brasa", "project", {"sector": "restaurant"})
    kg.add_entity("skill_brand", "dario-brand", "skill")
    kg.add_entity("skill_naming", "dario-naming", "skill")
    kg.add_entity("pattern_kapferer", "Kapferer Prism", "pattern")
    kg.add_relation("proj_mb", "skill_brand", "uses")
    kg.add_relation("proj_mb", "skill_naming", "uses")
    kg.add_relation("skill_brand", "pattern_kapferer", "applies")
    neighbors = kg.query_neighbors("proj_mb", depth=2)
    check("find_neighbors_depth_2", lambda: None if len(neighbors) >= 3 else (_ for _ in ()).throw(AssertionError(f"got {len(neighbors)}")))
    path = kg.find_path("proj_mb", "pattern_kapferer")
    check("find_path", lambda: None if len(path) == 3 else (_ for _ in ()).throw(AssertionError(f"path={path}")))
    search = kg.hybrid_search("restaurant brand")
    check("hybrid_search", lambda: None if len(search) > 0 else (_ for _ in ()).throw(AssertionError))

    # LearnedRouter
    print("\n--- LearnedRouter (RouteLLM) ---")
    lr = LearnedRouter()
    d1 = lr.route("Quick NIF validation check", "pt_validators", required_quality=60)
    check("route_simple_to_haiku", lambda: None if d1.selected_model == "haiku" else (_ for _ in ()).throw(AssertionError(f"got {d1.selected_model}")))
    d2 = lr.route("Comprehensive brand strategy with market analysis", "dario-brand", required_quality=85)
    check("route_complex_to_sonnet", lambda: None if d2.selected_model == "sonnet" else (_ for _ in ()).throw(AssertionError(f"got {d2.selected_model}")))
    d3 = lr.route("Critical financial audit requiring maximum accuracy", "conta-auditoria", required_quality=95)
    check("route_critical_to_opus", lambda: None if d3.selected_model == "opus" else (_ for _ in ()).throw(AssertionError(f"got {d3.selected_model}")))

    # ToolMemory
    print("\n--- ToolMemory (MemOS) ---")
    tmem = ToolMemory()
    tmem.record_sequence("dario-brand", ["Read", "Grep", "Write"], success=True, tokens=3000)
    tmem.record_sequence("dario-brand", ["Read", "Grep", "Write"], success=True, tokens=2800)
    tmem.record_sequence("dario-brand", ["Read", "Write"], success=False, tokens=4000)
    recs = tmem.recommend("dario-brand")
    check("recommend_best_sequence", lambda: None if recs[0]["success_rate"] > 0.5 else (_ for _ in ()).throw(AssertionError))
    check("recommend_rgw_first", lambda: None if recs[0]["tools"] == ["Read", "Grep", "Write"] else (_ for _ in ()).throw(AssertionError))

    # BenchmarkEvolution
    print("\n--- BenchmarkEvolution (EvoAgentX) ---")
    be = BenchmarkEvolution(improvement_threshold=2.0)
    m1 = be.propose_mutation("swap_skill", "step_3", "dario-content", "dario-kw-cluster")
    accepted = be.evaluate(m1, score_before=72, score_after=78)
    check("accept_improvement", lambda: None if accepted else (_ for _ in ()).throw(AssertionError))
    m2 = be.propose_mutation("remove_step", "step_5", "exists", "removed")
    rejected = be.evaluate(m2, score_before=78, score_after=77)
    check("reject_regression", lambda: None if not rejected else (_ for _ in ()).throw(AssertionError))
    check("generation_incremented", lambda: None if be._generation == 1 else (_ for _ in ()).throw(AssertionError))

    # MetricsRegistry
    print("\n--- MetricsRegistry (deepeval + promptfoo) ---")
    check("7_metrics_defined", lambda: None if len(MetricsRegistry.METRICS) == 7 else (_ for _ in ()).throw(AssertionError))
    check("3_red_team_profiles", lambda: None if len(MetricsRegistry.RED_TEAM_PROBES) == 3 else (_ for _ in ()).throw(AssertionError))

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="DARIO Intelligence Upgrades v11.0")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--memory", action="store_true")
    parser.add_argument("--graph", action="store_true")
    parser.add_argument("--router", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.test:
        sys.exit(_run_self_tests())

    if args.memory:
        print(json.dumps(tiered_memory.stats(), indent=2))
    elif args.graph:
        knowledge_graph.auto_build_from_tasks()
        print(json.dumps(knowledge_graph.stats(), indent=2))
    elif args.router:
        print(json.dumps(learned_router.get_savings_report(), indent=2))
    elif args.status:
        knowledge_graph.auto_build_from_tasks()
        print("\n=== Intelligence Upgrades v11.0 ===")
        print(f"  Memory: {tiered_memory.stats()}")
        print(f"  Q-Value: {q_value_memory.stats()}")
        print(f"  Graph: {knowledge_graph.stats()}")
        print(f"  Router: {learned_router.get_savings_report()}")
        print(f"  Tool Memory: {tool_memory.stats()}")
        print(f"  Evolution: {benchmark_evolution.stats()}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
