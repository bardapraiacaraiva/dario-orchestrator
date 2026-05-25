#!/usr/bin/env python3
"""
DARIO Semantic Dispatch — Embeddings-based Skill Routing
========================================================
Upgrade 1 (Sprint 1) of the Cognitive Audit roadmap.

Replaces the keyword-matching dispatch (dispatch_engine.KEYWORD_SKILL_MAP)
with cosine similarity between task text and skill descriptions, using
nomic-embed-text via Ollama. Cached in orchestrator.db.

Keyword matching remains as automatic fallback when semantic score is
below SEMANTIC_THRESHOLD or Ollama is unreachable.

CLI:
    python semantic_dispatch.py --bootstrap          Generate/refresh embeddings
    python semantic_dispatch.py --test <query>       Top-5 matches for a query
    python semantic_dispatch.py --stats              Cache status
"""

import array
import hashlib
import json
import sqlite3
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SKILLS_DIR = Path.home() / ".claude" / "skills"
DB_PATH = ORCH_DIR / "orchestrator.db"

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"

# Threshold raised after empirical testing: nomic-embed-text gives noisy
# matches in 0.45-0.55 range across PT/EN mixed queries. 0.60 yields
# precision-favoured behaviour; below threshold falls through to keyword.
SEMANTIC_THRESHOLD = 0.60
TOP_K = 3


def _load_keyword_index() -> dict:
    """Build skill -> [keyword,...] index from dispatch_engine.KEYWORD_SKILL_MAP.
    These PT/EN keywords are concatenated to descriptions before embedding,
    giving the model a stronger signal for routing intent vs surface nouns.
    """
    try:
        sys_path_added = False
        if str(ORCH_DIR) not in sys.path:
            sys.path.insert(0, str(ORCH_DIR))
            sys_path_added = True
        from dispatch.dispatch_engine import KEYWORD_SKILL_MAP
        if sys_path_added:
            sys.path.remove(str(ORCH_DIR))
    except Exception:
        return {}
    skill_kws = {}
    for kw, skill in KEYWORD_SKILL_MAP.items():
        skill_kws.setdefault(skill, []).append(kw)
    return skill_kws


def _augment_description(name: str, desc: str, keyword_index: dict) -> str:
    """Append known dispatch keywords to a skill description for embedding.
    Keeps original description first (semantic anchor), keywords as bag-of-words.
    """
    kws = keyword_index.get(name, [])
    if not kws:
        return desc
    return f"{desc} | Triggers: {', '.join(kws)}"


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skill_embeddings (
            skill_name TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            description_hash TEXT NOT NULL,
            vector BLOB NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()


def _embed(text: str, timeout: int = 30) -> list:
    payload = json.dumps({"model": OLLAMA_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    return data.get("embedding", [])


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _cosine(a: list, b: list) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = 0.0
    mag_a = 0.0
    mag_b = 0.0
    for x, y in zip(a, b):
        dot += x * y
        mag_a += x * x
        mag_b += y * y
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0
    return dot / ((mag_a ** 0.5) * (mag_b ** 0.5))


def _vec_to_blob(vec: list) -> bytes:
    return array.array("f", vec).tobytes()


def _blob_to_vec(blob: bytes) -> list:
    a = array.array("f")
    a.frombytes(blob)
    return list(a)


def _parse_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end < 0:
        return {}
    raw = content[3:end].strip()
    if yaml:
        try:
            data = yaml.safe_load(raw)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    out = {}
    current_key = None
    buf = []
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            if current_key:
                out[current_key] = " ".join(buf).strip()
                buf = []
            k, _, v = line.partition(":")
            current_key = k.strip()
            buf.append(v.strip())
        else:
            buf.append(line.strip())
    if current_key:
        out[current_key] = " ".join(buf).strip()
    return out


def extract_skill_corpus() -> dict:
    """Walk skills directory and extract name -> description from SKILL.md frontmatter."""
    corpus = {}
    if not SKILLS_DIR.exists():
        return corpus
    for entry in SKILLS_DIR.iterdir():
        try:
            skill_md = entry / "SKILL.md"
            if not skill_md.exists():
                continue
            content = skill_md.read_text(encoding="utf-8", errors="ignore")
            meta = _parse_frontmatter(content)
            name = meta.get("name")
            desc = meta.get("description")
            if name and desc and isinstance(name, str) and isinstance(desc, str):
                corpus[name] = desc.strip()
        except Exception:
            continue
    return corpus


def bootstrap_embeddings(verbose: bool = False) -> dict:
    """Ensure all skills have current embeddings. Returns stats dict."""
    corpus = extract_skill_corpus()
    keyword_index = _load_keyword_index()
    conn = sqlite3.connect(str(DB_PATH))
    _ensure_schema(conn)

    existing = {row[0]: row[1] for row in conn.execute(
        "SELECT skill_name, description_hash FROM skill_embeddings"
    )}

    stats = {"corpus_size": len(corpus), "generated": 0, "skipped": 0, "failed": 0}

    for name, desc in corpus.items():
        augmented = _augment_description(name, desc, keyword_index)
        h = _hash(augmented)
        if existing.get(name) == h:
            stats["skipped"] += 1
            continue
        try:
            vec = _embed(augmented)
            if not vec:
                stats["failed"] += 1
                if verbose:
                    print(f"  FAIL (empty vector): {name}")
                continue
            conn.execute(
                """INSERT OR REPLACE INTO skill_embeddings
                   (skill_name, description, description_hash, vector, created_at)
                   VALUES (?, ?, ?, ?, datetime('now'))""",
                (name, augmented, h, _vec_to_blob(vec)),
            )
            stats["generated"] += 1
            if verbose:
                print(f"  embed: {name}")
        except Exception as e:
            stats["failed"] += 1
            if verbose:
                print(f"  FAIL: {name}: {e}")

    # Prune orphans (skill removed from filesystem)
    conn.execute(
        "DELETE FROM skill_embeddings WHERE skill_name NOT IN ({})".format(
            ",".join("?" * len(corpus)) if corpus else "''"
        ),
        list(corpus.keys()),
    )
    pruned = conn.total_changes - stats["generated"]
    stats["pruned"] = max(0, pruned)

    conn.commit()
    conn.close()
    return stats


def _keyword_rerank_boost(text_lower: str, keyword_index: dict) -> dict:
    """Compute per-skill boosts from exact keyword presence in query.
    Each matched keyword adds 0.05 (multi-word keywords add 0.08 to favour specificity).
    Capped at +0.20 per skill. Hybrid signal: semantic gets the gist, keywords confirm intent.
    """
    boosts = {}
    for skill, kws in keyword_index.items():
        for kw in kws:
            if kw in text_lower:
                inc = 0.08 if " " in kw else 0.05
                boosts[skill] = min(boosts.get(skill, 0.0) + inc, 0.20)
    return boosts


def semantic_match(task_text: str, top_k: int = TOP_K) -> list:
    """Top-K skills by hybrid score: cosine similarity + keyword boost.
    Returns [(skill, final_score), ...]. Empty list on Ollama/DB failure.
    """
    if not task_text or not task_text.strip():
        return []
    try:
        task_vec = _embed(task_text)
        if not task_vec:
            return []
    except Exception:
        return []

    keyword_index = _load_keyword_index()
    keyword_boosts = _keyword_rerank_boost(task_text.lower(), keyword_index)

    try:
        conn = sqlite3.connect(str(DB_PATH))
        _ensure_schema(conn)
        results = []
        for skill, blob in conn.execute(
            "SELECT skill_name, vector FROM skill_embeddings"
        ):
            base = _cosine(task_vec, _blob_to_vec(blob))
            final = base + keyword_boosts.get(skill, 0.0)
            results.append((skill, final))
        conn.close()
    except Exception:
        return []

    results.sort(key=lambda x: -x[1])
    return results[:top_k]


def infer_skill_semantic(task: dict, threshold: float = SEMANTIC_THRESHOLD):
    """
    Semantic-first skill inference.
    Returns (skill_or_None, debug_matches).
    None means: fall back to keyword matching upstream.
    """
    if task.get("skill"):
        return task["skill"], [("explicit", 1.0)]

    text = f"{task.get('title', '')} {task.get('description', '')}".strip()
    if not text:
        return None, []

    matches = semantic_match(text, top_k=5)
    if not matches:
        return None, []

    best_skill, best_score = matches[0]
    if best_score < threshold:
        return None, matches
    return best_skill, matches


def cache_stats() -> dict:
    conn = sqlite3.connect(str(DB_PATH))
    _ensure_schema(conn)
    total = conn.execute("SELECT COUNT(*) FROM skill_embeddings").fetchone()[0]
    oldest = conn.execute(
        "SELECT skill_name, created_at FROM skill_embeddings ORDER BY created_at ASC LIMIT 1"
    ).fetchone()
    newest = conn.execute(
        "SELECT skill_name, created_at FROM skill_embeddings ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return {"total": total, "oldest": oldest, "newest": newest}


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("semantic_dispatch")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    if "--bootstrap" in sys.argv:
        verbose = "--verbose" in sys.argv or "-v" in sys.argv
        print("Bootstrapping skill embeddings via Ollama (nomic-embed-text)...")
        stats = bootstrap_embeddings(verbose=verbose)
        print(f"Corpus size:  {stats['corpus_size']}")
        print(f"Generated:    {stats['generated']}")
        print(f"Skipped (up to date): {stats['skipped']}")
        print(f"Pruned (orphans):     {stats['pruned']}")
        print(f"Failed:       {stats['failed']}")
        return 0
    if "--stats" in sys.argv:
        s = cache_stats()
        print(f"Cached embeddings: {s['total']}")
        if s["oldest"]:
            print(f"Oldest: {s['oldest'][0]} @ {s['oldest'][1]}")
        if s["newest"]:
            print(f"Newest: {s['newest'][0]} @ {s['newest'][1]}")
        return 0
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        query = " ".join(sys.argv[idx + 1:]).strip()
        if not query:
            query = "create a brand positioning workshop for a restaurant"
        print(f"Query: {query}")
        print("Top-5 semantic matches:")
        for skill, score in semantic_match(query, top_k=5):
            print(f"  {score:.3f}  {skill}")
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
