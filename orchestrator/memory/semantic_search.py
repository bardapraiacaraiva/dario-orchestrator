"""
Semantic search over consolidated semantic memories (P1 — audit 2026-06-01).

WHY THIS EXISTS
---------------
The Dream engine consolidates episodes into SemanticMemory items (SEM-*.yaml),
but until now those memories were ORPHANED from the execution path: nothing
retrieved them by relevance and injected them into task context. Knowledge was
consolidated and then never used at inference time (a broken feedback loop).

This module closes that loop. It embeds each semantic memory with the same
infra the dispatcher already uses (nomic-embed-text via Ollama, cosine over
vectors cached in orchestrator.db) and exposes `search_memories()` so the
context injector can pull the top-k most relevant consolidated memories for a
given task.

GRACEFUL DEGRADATION
--------------------
If Ollama is unavailable (or embeddings fail for any reason), every public
function returns empty / no-op. The caller falls back to its existing behaviour;
execution is never blocked.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
if str(ORCH_DIR) not in sys.path:
    sys.path.insert(0, str(ORCH_DIR))

DB_PATH = ORCH_DIR / "orchestrator.db"

# Reuse the dispatcher's embedding primitives (single source of truth).
try:
    from dispatch.semantic_dispatch import _blob_to_vec, _cosine, _embed, _hash, _vec_to_blob
    _EMBED_OK = True
except Exception:
    _EMBED_OK = False

try:
    from memory.semantic import increment_retrieval, list_semantic, read_semantic
except Exception:  # pragma: no cover - memory package must exist in real installs
    list_semantic = lambda: []  # type: ignore
    read_semantic = lambda _id: None  # type: ignore
    increment_retrieval = lambda _id: None  # type: ignore

DEFAULT_TOP_K = 3
DEFAULT_THRESHOLD = 0.55  # same bar Dream uses for merge similarity


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS memory_embeddings (
            memory_id    TEXT PRIMARY KEY,
            content_hash TEXT NOT NULL,
            vec          BLOB NOT NULL,
            updated_at   TEXT
        )
        """
    )
    conn.commit()


def _memory_text(mem) -> str:
    """The text we embed for a memory: name + description + content."""
    return f"{getattr(mem, 'name', '')}\n{getattr(mem, 'description', '')}\n{getattr(mem, 'content', '')}".strip()


def bootstrap_memory_embeddings(verbose: bool = False) -> dict:
    """Embed any new/changed semantic memories. Idempotent (content-hash gated)."""
    if not _EMBED_OK:
        return {"ok": False, "reason": "embedding infra unavailable", "embedded": 0}
    memories = list_semantic()
    embedded = skipped = failed = 0
    conn = sqlite3.connect(str(DB_PATH))
    try:
        _ensure_schema(conn)
        existing = dict(conn.execute("SELECT memory_id, content_hash FROM memory_embeddings").fetchall())
        for mem in memories:
            text = _memory_text(mem)
            if not text:
                continue
            h = _hash(text)
            if existing.get(mem.memory_id) == h:
                skipped += 1
                continue
            try:
                vec = _embed(text)
                if not vec:
                    failed += 1
                    continue
                conn.execute(
                    "INSERT OR REPLACE INTO memory_embeddings (memory_id, content_hash, vec, updated_at) "
                    "VALUES (?, ?, ?, datetime('now'))",
                    (mem.memory_id, h, _vec_to_blob(vec)),
                )
                embedded += 1
            except Exception as e:
                failed += 1
                if verbose:
                    print(f"[semantic_search] embed failed for {mem.memory_id}: {e}")
        conn.commit()
    finally:
        conn.close()
    return {"ok": True, "embedded": embedded, "skipped": skipped, "failed": failed,
            "total_memories": len(memories)}


def search_memories(query: str, top_k: int = DEFAULT_TOP_K,
                    threshold: float = DEFAULT_THRESHOLD,
                    bump_retrieval: bool = True) -> list[dict]:
    """
    Return the top-k consolidated semantic memories most similar to `query`.

    Each result: {"memory_id", "name", "score", "confidence", "content"}.
    Returns [] gracefully if embeddings are unavailable or nothing clears the
    threshold. When `bump_retrieval` is True, increments retrieval_count on the
    returned memories (feeds the existing dream prune/never-retrieved analytics).
    """
    if not _EMBED_OK or not query or not query.strip():
        return []
    try:
        qvec = _embed(query.strip())
    except Exception:
        return []
    if not qvec:
        return []

    conn = sqlite3.connect(str(DB_PATH))
    try:
        _ensure_schema(conn)
        rows = conn.execute("SELECT memory_id, vec FROM memory_embeddings").fetchall()
    finally:
        conn.close()

    scored = []
    for memory_id, blob in rows:
        try:
            score = _cosine(qvec, _blob_to_vec(blob))
        except Exception:
            continue
        if score >= threshold:
            scored.append((memory_id, score))

    scored.sort(key=lambda x: (-x[1], x[0]))
    results = []
    for memory_id, score in scored[:top_k]:
        mem = read_semantic(memory_id)
        if not mem:
            continue
        if bump_retrieval:
            try:
                increment_retrieval(memory_id)
            except Exception:
                pass
        try:
            from memory.decay import effective_confidence
            conf = round(effective_confidence(mem), 3)  # decayed, not static (DD finding A13)
        except Exception:
            conf = getattr(mem, "confidence", 0.7)
        results.append({
            "memory_id": memory_id,
            "name": getattr(mem, "name", memory_id),
            "score": round(score, 4),
            "confidence": conf,
            "content": getattr(mem, "content", "") or getattr(mem, "description", ""),
        })
    return results


def main():
    import argparse
    import json
    p = argparse.ArgumentParser(description="Semantic search over consolidated memories")
    p.add_argument("--bootstrap", action="store_true", help="Embed new/changed memories")
    p.add_argument("--search", metavar="TEXT", help="Search memories by text")
    p.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.bootstrap:
        res = bootstrap_memory_embeddings(verbose=not args.json)
        print(json.dumps(res) if args.json else res)
    elif args.search:
        res = search_memories(args.search, top_k=args.top_k, bump_retrieval=False)
        print(json.dumps(res, ensure_ascii=False) if args.json
              else "\n".join(f"{r['score']:.3f}  {r['memory_id']}  {r['name']}" for r in res) or "(no matches)")
    else:
        p.print_help()


if __name__ == "__main__":
    main()
