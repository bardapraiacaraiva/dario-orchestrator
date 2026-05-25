"""Knowledge Graph subsystem (extracted from `upgrades/intelligence.py` — Onda 5 #1).

`GraphEntity` + `GraphRelation` dataclasses + `KnowledgeGraph` class.
LightRAG-inspired hybrid retrieval: keyword match + graph centrality.

Parent `upgrades/intelligence.py` re-imports these so existing callers keep working.
"""

from __future__ import annotations

import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
DB_PATH = ORCH_DIR / "orchestrator.db"


@dataclass
class GraphEntity:
    """An entity in the knowledge graph."""

    entity_id: str
    name: str
    entity_type: str  # project, skill, pattern, client, concept
    properties: dict = field(default_factory=dict)


@dataclass
class GraphRelation:
    """A relationship between entities."""

    source_id: str
    target_id: str
    relation_type: str  # uses, depends_on, similar_to, produced_by, effective_for
    weight: float = 1.0
    evidence: str = ""


class KnowledgeGraph:
    """Entity-relationship graph for relational retrieval.

    Inspired by LightRAG — combines graph traversal with keyword matching.
    Enables: "project X used pattern Y which was effective in Z"
    """

    def __init__(self):
        self._entities: dict[str, GraphEntity] = {}
        self._relations: list[GraphRelation] = []
        self._adjacency: dict[str, list[tuple[str, str, float]]] = defaultdict(list)

    def add_entity(
        self,
        entity_id: str,
        name: str,
        entity_type: str,
        properties: dict | None = None,
    ) -> GraphEntity:
        """Add or update an entity."""
        entity = GraphEntity(entity_id, name, entity_type, properties or {})
        self._entities[entity_id] = entity
        return entity

    def add_relation(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        weight: float = 1.0,
        evidence: str = "",
    ) -> GraphRelation:
        """Add a relationship between entities."""
        rel = GraphRelation(source_id, target_id, relation_type, weight, evidence)
        self._relations.append(rel)
        self._adjacency[source_id].append((target_id, relation_type, weight))
        self._adjacency[target_id].append((source_id, f"inv_{relation_type}", weight))
        return rel

    def query_neighbors(
        self,
        entity_id: str,
        relation_type: str | None = None,
        depth: int = 1,
    ) -> list[dict]:
        """Find connected entities up to N hops."""
        visited: set[str] = set()
        results = []
        queue: list[tuple[str, int]] = [(entity_id, 0)]

        while queue:
            current, current_depth = queue.pop(0)
            if current in visited or current_depth > depth:
                continue
            visited.add(current)

            for target, rel_type, weight in self._adjacency.get(current, []):
                if relation_type and rel_type != relation_type:
                    continue
                if target not in visited:
                    entity = self._entities.get(target)
                    if entity:
                        results.append(
                            {
                                "entity_id": entity.entity_id,
                                "name": entity.name,
                                "type": entity.entity_type,
                                "relation": rel_type,
                                "weight": weight,
                                "depth": current_depth + 1,
                            }
                        )
                    if current_depth + 1 < depth:
                        queue.append((target, current_depth + 1))

        results.sort(key=lambda x: (-float(x["weight"]), int(x["depth"])))  # type: ignore[arg-type,call-overload]
        return results

    def find_path(self, source_id: str, target_id: str) -> list[str]:
        """Find shortest path between two entities (BFS)."""
        visited = {source_id}
        queue: list[tuple[str, list[str]]] = [(source_id, [source_id])]
        while queue:
            current, path = queue.pop(0)
            for neighbor, _, _ in self._adjacency.get(current, []):
                if neighbor == target_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def hybrid_search(self, query: str, limit: int = 10) -> list[dict]:
        """Hybrid search: keyword match on entities + graph traversal for context.

        Returns entities ranked by keyword relevance + graph centrality.
        """
        query_words = set(query.lower().split())
        scored = []

        for eid, entity in self._entities.items():
            name_words = set(entity.name.lower().split())
            type_words = {entity.entity_type.lower()}
            prop_words = set()
            for v in entity.properties.values():
                if isinstance(v, str):
                    prop_words.update(v.lower().split())

            all_words = name_words | type_words | prop_words
            keyword_score = len(query_words & all_words) / max(len(query_words), 1)

            degree = len(self._adjacency.get(eid, []))
            centrality = min(degree / 10, 1.0)

            total = keyword_score * 0.6 + centrality * 0.4

            if total > 0.05:
                scored.append(
                    {
                        "entity_id": eid,
                        "name": entity.name,
                        "type": entity.entity_type,
                        "score": round(total, 3),
                        "connections": degree,
                    }
                )

        scored.sort(key=lambda x: -float(x["score"]))  # type: ignore[arg-type]
        return scored[:limit]

    def auto_build_from_tasks(self):
        """Auto-build graph from orchestrator task history."""
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            tasks = [dict(r) for r in conn.execute("SELECT * FROM tasks").fetchall()]
            conn.close()
        except Exception:
            return

        for task in tasks:
            project = task.get("project", "unknown")
            if project:
                self.add_entity(f"proj_{project}", project, "project")
            skill = task.get("skill", "")
            if skill:
                self.add_entity(f"skill_{skill}", skill, "skill")
            assignee = task.get("assignee", "")
            if assignee:
                self.add_entity(f"worker_{assignee}", assignee, "worker")
            if project and skill:
                self.add_relation(
                    f"proj_{project}", f"skill_{skill}", "uses",
                    weight=1.0, evidence=task.get("id", ""),
                )
            if skill and assignee:
                self.add_relation(f"skill_{skill}", f"worker_{assignee}", "executed_by")

    def stats(self) -> dict:
        type_counts: dict[str, int] = defaultdict(int)
        for e in self._entities.values():
            type_counts[e.entity_type] += 1
        return {
            "entities": len(self._entities),
            "relations": len(self._relations),
            "entity_types": dict(type_counts),
        }


__all__ = ["GraphEntity", "GraphRelation", "KnowledgeGraph"]
