"""Build the org hierarchy tree from company.yaml + live task load.

Used by the /org endpoint in runtime.py to feed the agent-visualizer
without hardcoded data. Single source of truth: company.yaml.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
COMPANY_YAML = ORCH_DIR / "company.yaml"


def _normalize_id(node_id: str) -> str:
    """Normalize agent IDs to kebab-case (workers already use kebab)."""
    return node_id.replace("_", "-")


def _collect_all(company: dict) -> dict[str, dict]:
    """Flatten all agents + workers across base + extension sections.

    Index by the node's `id` field (e.g. 'dario-ceo') because reports_to/manages
    reference that value. Fall back to the dict key if `id` is absent.
    """
    nodes: dict[str, dict] = {}
    for key, section in company.items():
        if not isinstance(section, dict):
            continue
        if key == "agents" or key == "workers" or key.startswith("agents_") or key.startswith("workers_"):
            for dict_key, node in section.items():
                if not isinstance(node, dict):
                    continue
                resolved_id = _normalize_id(node.get("id") or dict_key)
                nodes[resolved_id] = {**node, "_id": resolved_id, "_section": key}
    return nodes


def _classify_level(node: dict) -> str:
    """Map a node to one of: ceo, vp, dir, worker, service."""
    raw_type = (node.get("type") or "").lower()
    nid = node.get("_id", "")
    if nid == "dario-ceo":
        return "ceo"
    if raw_type == "service":
        return "service"
    if raw_type == "manager" or nid.startswith("dir-") or nid.endswith("-director"):
        return "dir"
    if raw_type == "orchestrator" or nid.startswith("vp-"):
        return "vp"
    if raw_type == "worker" or nid.startswith("worker-"):
        return "worker"
    # Fallback: extension roots like lex-br-director are dirs
    return "dir" if "director" in nid else "worker"


def _resolve_parent(node: dict, all_nodes: dict[str, dict]) -> str | None:
    """Resolve reports_to to a node id that actually exists; normalize underscores."""
    rt = node.get("reports_to")
    if rt is None:
        return None
    rt = _normalize_id(rt)
    return rt if rt in all_nodes else None


def _load_active_assignees() -> dict[str, int]:
    """Map assignee → count of tasks currently in_progress / in_review."""
    db_path = ORCH_DIR / "orchestrator.db"
    if not db_path.exists():
        return {}
    counts: dict[str, int] = {}
    try:
        con = sqlite3.connect(str(db_path))
        cur = con.cursor()
        for row in cur.execute(
            "SELECT assignee, COUNT(*) FROM tasks "
            "WHERE status IN ('in_progress','in_review','todo') "
            "AND assignee IS NOT NULL AND assignee != '' "
            "GROUP BY assignee"
        ):
            assignee, n = row
            counts[_normalize_id(assignee)] = n
        con.close()
    except Exception:
        return counts
    return counts


def _load_lifetime_assignees() -> dict[str, dict[str, int]]:
    """Map assignee → {total, done} task counts ever."""
    db_path = ORCH_DIR / "orchestrator.db"
    if not db_path.exists():
        return {}
    stats: dict[str, dict[str, int]] = {}
    try:
        con = sqlite3.connect(str(db_path))
        cur = con.cursor()
        for row in cur.execute(
            "SELECT assignee, COUNT(*), SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) "
            "FROM tasks WHERE assignee IS NOT NULL AND assignee != '' "
            "GROUP BY assignee"
        ):
            assignee, total, done = row
            stats[_normalize_id(assignee)] = {"total": int(total or 0), "done": int(done or 0)}
        con.close()
    except Exception:
        return stats
    return stats


def build_tree() -> dict[str, Any]:
    """Build the org tree with live task counts. Returns JSON-ready dict."""
    if not COMPANY_YAML.exists():
        return {"error": "company.yaml not found", "nodes": [], "tree": None}

    with open(COMPANY_YAML, encoding="utf-8") as f:
        company = yaml.safe_load(f) or {}

    all_nodes = _collect_all(company)
    active = _load_active_assignees()
    lifetime = _load_lifetime_assignees()

    # First pass: classify + parent
    flat: list[dict] = []
    for nid, node in all_nodes.items():
        level = _classify_level(node)
        parent = _resolve_parent(node, all_nodes)
        # Some workers don't have reports_to set but are listed in a director's manages[].
        # Build worker→manager from manages[] as fallback.
        flat.append({
            "id": nid,
            "name": node.get("name") or nid,
            "title": node.get("title") or "",
            "level": level,
            "parent": parent,
            "active_tasks": active.get(nid, 0),
            "total_tasks": lifetime.get(nid, {}).get("total", 0),
            "done_tasks": lifetime.get(nid, {}).get("done", 0),
        })

    # Backfill worker→director via manages[]
    by_id = {n["id"]: n for n in flat}
    for nid, node in all_nodes.items():
        manages = node.get("manages") or []
        if not isinstance(manages, list):
            continue
        for child_id in manages:
            cid = _normalize_id(child_id)
            if cid in by_id and by_id[cid]["parent"] is None:
                by_id[cid]["parent"] = nid

    # Standalone squad directors with no reports_to → attach to CEO so they appear
    ceo_id = "dario-ceo"
    if ceo_id in by_id:
        for n in flat:
            if n["parent"] is None and n["level"] in ("dir", "vp") and n["id"] != ceo_id:
                n["parent"] = ceo_id

    # Compute aggregate counts: each non-leaf shows total workers under it,
    # plus active count rolled up.
    children_of: dict[str, list[str]] = {}
    for n in flat:
        if n["parent"]:
            children_of.setdefault(n["parent"], []).append(n["id"])

    def _rollup(node_id: str) -> tuple[int, int]:
        """Returns (worker_count_under, active_tasks_under) recursively."""
        kids = children_of.get(node_id, [])
        w_count = 0
        active_sum = by_id[node_id]["active_tasks"] if node_id in by_id else 0
        if not kids:
            return (1 if by_id.get(node_id, {}).get("level") == "worker" else 0, active_sum)
        for k in kids:
            kw, ka = _rollup(k)
            w_count += kw
            active_sum += ka
        return (w_count, active_sum)

    for n in flat:
        wc, ac = _rollup(n["id"])
        n["workers_under"] = wc
        n["active_under"] = ac
        n["status"] = "active" if ac > 0 else "idle"

    # Build tree rooted at CEO; skip services and orphans without a parent
    def _build_subtree(node_id: str) -> dict:
        n = by_id[node_id]
        kids = sorted(
            children_of.get(node_id, []),
            key=lambda k: (-by_id[k]["workers_under"], by_id[k]["name"]),
        )
        return {**n, "children": [_build_subtree(k) for k in kids]}

    tree = _build_subtree(ceo_id) if ceo_id in by_id else None

    # Stats summary
    by_level: dict[str, int] = {}
    for n in flat:
        by_level[n["level"]] = by_level.get(n["level"], 0) + 1

    return {
        "tree": tree,
        "nodes": flat,
        "stats": {
            "total_nodes": len(flat),
            "by_level": by_level,
            "active_tasks": sum(active.values()),
        },
        "source": "company.yaml",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_tree(), indent=2, ensure_ascii=False))
