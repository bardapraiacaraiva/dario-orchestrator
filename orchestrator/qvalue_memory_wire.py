#!/usr/bin/env python3
"""
DARIO Q-Value Memory Wire-In
============================
Upgrade 5 (Sprint 2) of the Cognitive Audit roadmap.

intelligence_upgrades.py defines QValueMemory (M3.2) — a working class
with TD-learning, two-phase retrieval, and Q-value selection. Until now
NOTHING in the runtime called it. It was shelf-ware.

This module:
  1. Wraps QValueMemory with SQLite persistence (table q_episodes)
  2. Provides bootstrap_from_history() — populates from DB tasks + episode files
  3. Provides suggest_skill(task_text, project) — used by dispatch as a 3rd signal
  4. Provides record_outcome() — hook called by executor after each task completes

Wiring points:
  - dispatch_engine.infer_skill_from_task → falls through to Q-value if
    explicit + semantic + keyword all return None or low confidence
  - executor.py post-completion → call record_outcome() to grow the memory

CLI:
    python qvalue_memory_wire.py --bootstrap   Populate from history (idempotent)
    python qvalue_memory_wire.py --suggest "create a brand for restaurant"
    python qvalue_memory_wire.py --stats       Show memory state
    python qvalue_memory_wire.py --top 10      Top strategies by Q-value
"""

import argparse
import json
import sqlite3
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
DB_PATH = ORCH_DIR / "orchestrator.db"
EPISODES_DIR = ORCH_DIR / "memory" / "episodes"


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS q_episodes (
            episode_id   TEXT PRIMARY KEY,
            context      TEXT NOT NULL,
            strategy     TEXT NOT NULL,
            skill        TEXT NOT NULL,
            project      TEXT,
            outcome_score REAL NOT NULL,
            tokens_used  INTEGER DEFAULT 0,
            q_value      REAL NOT NULL,
            visits       INTEGER DEFAULT 1,
            created_at   TEXT NOT NULL,
            updated_at   TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_q_skill_proj ON q_episodes(skill, project)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_q_qvalue ON q_episodes(q_value DESC)
    """)
    conn.commit()


def _load_qvm():
    """Construct a QValueMemory instance loaded with persisted episodes."""
    sys.path.insert(0, str(ORCH_DIR))
    from upgrades.intelligence import Episode, QValueMemory

    qvm = QValueMemory(learning_rate=0.1, discount=0.95)
    if not DB_PATH.exists():
        return qvm
    conn = sqlite3.connect(str(DB_PATH))
    _ensure_schema(conn)
    rows = conn.execute(
        "SELECT episode_id, context, strategy, skill, outcome_score, tokens_used, q_value, visits, created_at FROM q_episodes"
    ).fetchall()
    conn.close()
    for r in rows:
        ep = Episode(
            episode_id=r[0],
            context=r[1] or "",
            strategy=r[2] or "",
            skill=r[3] or "",
            outcome_score=float(r[4] or 0),
            tokens_used=int(r[5] or 0),
            q_value=float(r[6] or 0),
            visits=int(r[7] or 1),
            created_at=r[8] or datetime.now(UTC).isoformat(),
        )
        qvm._episodes.append(ep)
    return qvm


def _persist_episode(ep) -> None:
    conn = sqlite3.connect(str(DB_PATH))
    _ensure_schema(conn)
    conn.execute("""
        INSERT OR REPLACE INTO q_episodes
        (episode_id, context, strategy, skill, project, outcome_score, tokens_used, q_value, visits, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ep.episode_id, ep.context, ep.strategy, ep.skill,
        getattr(ep, "project", None),
        float(ep.outcome_score), int(ep.tokens_used),
        float(ep.q_value), int(ep.visits),
        ep.created_at, datetime.now(UTC).isoformat(),
    ))
    conn.commit()
    conn.close()


def record_outcome(context: str, skill: str, score: float,
                   tokens_used: int = 0, project: str = None,
                   strategy: str = None) -> dict:
    """Record a task outcome as a Q-learning episode.
    Called by executor.py post-completion hook.
    """
    if not context or not skill or score <= 0:
        return {"recorded": False, "reason": "missing context/skill/score"}

    if not strategy:
        strategy = f"{skill}@{project or 'global'}"

    qvm = _load_qvm()
    ep = qvm.record(context=context, strategy=strategy, skill=skill,
                    outcome_score=float(score), tokens_used=int(tokens_used))
    # Attach project for retrieval filtering
    ep.project = project
    _persist_episode(ep)
    return {
        "recorded": True,
        "episode_id": ep.episode_id,
        "q_value": round(ep.q_value, 3),
        "visits": ep.visits,
        "avg_score": round(ep.outcome_score, 1),
    }


# PT/EN stop words — filtered before keyword overlap matching so that
# generic verbs like "criar/uma/para/the/of" don't fake relevance.
STOP_WORDS = {
    # PT
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "da", "do",
    "das", "dos", "em", "na", "no", "nas", "nos", "para", "por", "com",
    "sem", "que", "se", "e", "ou", "mas", "como", "quando", "onde", "ser",
    "criar", "fazer", "ter", "ir", "vir", "preciso", "quero", "queria",
    "meu", "minha", "seu", "sua", "este", "esse", "aquele", "esta", "essa",
    "ao", "à", "aos", "às", "pelo", "pela", "pelos", "pelas",
    # EN
    "the", "an", "of", "to", "for", "and", "or", "but", "in", "on",
    "at", "by", "with", "from", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "does", "did", "will",
    "would", "could", "should", "may", "might", "can", "this", "that",
    "these", "those", "i", "you", "we", "they", "it", "create", "make",
    "want", "need", "my", "your", "our", "their",
}


def _meaningful_words(text: str) -> set:
    """Lowercase tokens minus stop words and very short ones."""
    raw = text.lower().split()
    return {w.strip(".,;:!?()[]\"'") for w in raw
            if len(w) > 2 and w.lower() not in STOP_WORDS}


def suggest_skill(task_text: str, project: str = None, top_k: int = 3) -> list:
    """Suggest skills based on Q-value of similar past episodes.
    Returns ordered list: [{skill, q_value, avg_score, visits, relevance}, ...]

    Custom retrieval (replaces qvm.select_strategy) — filters stop words so
    that generic verbs don't trigger spurious matches, and requires at least
    2 meaningful overlap tokens for relevance.
    """
    if not task_text or not task_text.strip():
        return []
    qvm = _load_qvm()
    if not qvm._episodes:
        return []

    query_words = _meaningful_words(task_text)
    if not query_words:
        return []

    candidates = []
    for ep in qvm._episodes:
        ep_words = _meaningful_words(ep.context)
        overlap = query_words & ep_words
        if len(overlap) < 2:
            continue
        relevance = len(overlap) / max(len(query_words), 1)
        # Combined ranking: q_value as primary, relevance as secondary
        candidates.append((ep.q_value, relevance, ep))

    if not candidates:
        return []

    # If project given, boost in-project episodes
    if project:
        candidates = [
            (q + (0.05 if (project in getattr(ep, "strategy", "")) else 0),
             rel, ep)
            for q, rel, ep in candidates
        ]

    candidates.sort(key=lambda x: (-x[0], -x[1]))
    return [
        {
            "strategy": ep.strategy,
            "skill": ep.skill,
            "q_value": round(ep.q_value, 3),
            "avg_score": round(ep.outcome_score, 1),
            "visits": ep.visits,
            "relevance": round(rel, 3),
        }
        for _q, rel, ep in candidates[:top_k]
    ]


def bootstrap_from_history(verbose: bool = False) -> dict:
    """Populate Q-memory from existing task history.
    Idempotent: existing episodes (by episode_id) are skipped.

    Sources:
      1. tasks table in DB (status=done, has skill+score)
      2. memory/episodes/ YAML files
    """
    stats = {"db_tasks": 0, "yaml_episodes": 0, "skipped": 0, "errors": 0}

    if not DB_PATH.exists():
        return stats

    conn = sqlite3.connect(str(DB_PATH))
    _ensure_schema(conn)
    existing_ids = {row[0] for row in conn.execute("SELECT episode_id FROM q_episodes")}

    # Source 1: tasks table
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(tasks)").fetchall()]
        title_col = "title" if "title" in cols else None
        desc_col = "description" if "description" in cols else None
        if title_col and "skill" in cols and "score" in cols:
            rows = conn.execute(f"""
                SELECT id, {title_col}, {'description' if desc_col else "''"}, skill,
                       project, score, tokens, completed_at
                FROM tasks
                WHERE status = 'done' AND skill IS NOT NULL AND score > 0
                LIMIT 500
            """).fetchall()
            for r in rows:
                task_id, title, desc, skill, project, score, tokens, completed = r
                ep_id = f"task-{task_id}"
                if ep_id in existing_ids:
                    stats["skipped"] += 1
                    continue
                context = f"{title or ''} {desc or ''}".strip()[:500]
                if not context or not skill:
                    continue
                strategy = f"{skill}@{project or 'global'}"
                conn.execute("""
                    INSERT OR IGNORE INTO q_episodes
                    (episode_id, context, strategy, skill, project, outcome_score, tokens_used, q_value, visits, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ep_id, context, strategy, skill, project,
                    float(score), int(tokens or 0), float(score) / 100.0, 1,
                    completed or datetime.now(UTC).isoformat(),
                ))
                stats["db_tasks"] += 1
                if verbose:
                    print(f"  +task {task_id} ({skill}, score={score})")
    except Exception as e:
        stats["errors"] += 1
        if verbose:
            print(f"  DB scan error: {e}")
    conn.commit()

    # Source 2: episode YAML files
    if EPISODES_DIR.exists():
        for day_dir in EPISODES_DIR.iterdir():
            if not day_dir.is_dir():
                continue
            for ep_file in day_dir.glob("*.yaml"):
                try:
                    with open(ep_file, encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if not isinstance(data, dict):
                        continue
                    ep_id = f"file-{ep_file.stem}"
                    if ep_id in existing_ids:
                        stats["skipped"] += 1
                        continue
                    score = data.get("score") or data.get("outcome_score") or 0
                    skill = data.get("skill")
                    if not skill or float(score) <= 0:
                        continue
                    context = (data.get("task_title") or data.get("output_summary") or
                               data.get("context") or "")[:500]
                    project = data.get("project")
                    strategy = f"{skill}@{project or 'global'}"
                    conn.execute("""
                        INSERT OR IGNORE INTO q_episodes
                        (episode_id, context, strategy, skill, project, outcome_score, tokens_used, q_value, visits, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        ep_id, context, strategy, skill, project,
                        float(score), int(data.get("tokens_used", 0) or 0),
                        float(score) / 100.0, 1,
                        data.get("timestamp") or datetime.now(UTC).isoformat(),
                    ))
                    stats["yaml_episodes"] += 1
                except Exception:
                    stats["errors"] += 1
    conn.commit()
    conn.close()
    return stats


def stats() -> dict:
    """Return summary of Q-memory state."""
    if not DB_PATH.exists():
        return {"total_episodes": 0}
    conn = sqlite3.connect(str(DB_PATH))
    _ensure_schema(conn)
    total = conn.execute("SELECT COUNT(*) FROM q_episodes").fetchone()[0]
    if not total:
        conn.close()
        return {"total_episodes": 0}
    avg_q = conn.execute("SELECT AVG(q_value) FROM q_episodes").fetchone()[0] or 0.0
    top_skill = conn.execute(
        "SELECT skill, AVG(q_value) as avg_q FROM q_episodes GROUP BY skill ORDER BY avg_q DESC LIMIT 1"
    ).fetchone()
    distinct_skills = conn.execute(
        "SELECT COUNT(DISTINCT skill) FROM q_episodes"
    ).fetchone()[0]
    conn.close()
    return {
        "total_episodes": total,
        "distinct_skills": distinct_skills,
        "avg_q_value": round(float(avg_q), 3),
        "top_skill": top_skill[0] if top_skill else None,
        "top_skill_q": round(float(top_skill[1]), 3) if top_skill else None,
    }


def top_strategies(n: int = 10) -> list:
    if not DB_PATH.exists():
        return []
    conn = sqlite3.connect(str(DB_PATH))
    _ensure_schema(conn)
    rows = conn.execute("""
        SELECT skill, strategy, q_value, visits, outcome_score
        FROM q_episodes
        ORDER BY q_value DESC
        LIMIT ?
    """, (n,)).fetchall()
    conn.close()
    return [
        {"skill": r[0], "strategy": r[1], "q_value": round(r[2], 3),
         "visits": r[3], "avg_score": round(r[4], 1)}
        for r in rows
    ]


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("qvalue_memory_wire")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Q-Value Memory Wire-In")
    p.add_argument("--bootstrap", action="store_true", help="Populate from history")
    p.add_argument("--suggest", type=str, help="Suggest skills for given task text")
    p.add_argument("--project", type=str, help="Project filter for suggest")
    p.add_argument("--top", type=int, default=0, help="Top N strategies by Q-value")
    p.add_argument("--stats", action="store_true", help="Memory state")
    p.add_argument("--record", nargs=4, metavar=("CONTEXT", "SKILL", "SCORE", "PROJECT"),
                   help="Record an outcome (for testing)")
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.bootstrap:
        s = bootstrap_from_history(verbose=args.verbose)
        print(json.dumps(s, indent=2) if args.json else
              "\n".join(f"  {k}: {v}" for k, v in s.items()))
        return 0

    if args.suggest:
        out = suggest_skill(args.suggest, project=args.project, top_k=5)
        if args.json:
            print(json.dumps(out, indent=2))
        else:
            print(f"Suggestions for: {args.suggest}")
            for s in out:
                print(f"  q={s['q_value']:.3f}  {s['skill']:30s} avg={s['avg_score']:.1f} visits={s['visits']}")
        return 0

    if args.top:
        out = top_strategies(args.top)
        if args.json:
            print(json.dumps(out, indent=2))
        else:
            for s in out:
                print(f"  q={s['q_value']:.3f}  {s['skill']:30s} avg={s['avg_score']:.1f} visits={s['visits']}")
        return 0

    if args.stats:
        s = stats()
        print(json.dumps(s, indent=2) if args.json else
              "\n".join(f"  {k}: {v}" for k, v in s.items()))
        return 0

    if args.record:
        ctx, sk, sc, proj = args.record
        r = record_outcome(context=ctx, skill=sk, score=float(sc), project=proj)
        print(json.dumps(r, indent=2))
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
