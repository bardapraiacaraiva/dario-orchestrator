"""Tests for memory decay, retrieval tracking and realistic pattern thresholds.

DD finding A13 (2026-06-12):
1. Decay — confidence decays with age; retrieval slows/freezes the decay.
2. Retrieval tracking — pending retrievals staged at context time are consumed
   by the completion hooks, incrementing retrieval_count + last_retrieved.
3. Thresholds — convergence fires with 2 sessions / avg score >= 60; quality
   trends fire with 3 runs of the same skill.
"""

from __future__ import annotations

import sys
import types
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

# Pin to mid-day UTC — day-window logic must not flake near midnight.
NOW = datetime(2026, 6, 12, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def isolated_memory(tmp_path, monkeypatch):
    """Redirect all memory + dream paths to a temp directory."""
    fake_orch = tmp_path / "orchestrator"
    (fake_orch / "memory" / "episodes").mkdir(parents=True)
    (fake_orch / "memory" / "semantic").mkdir(parents=True)
    (fake_orch / "memory" / "procedural").mkdir(parents=True)
    (fake_orch / "memory" / "cache").mkdir(parents=True)
    (fake_orch / "memory" / "retrieval").mkdir(parents=True)

    import dream.prune as prune_mod
    import memory.cache as cache_mod
    import memory.episodic as ep_mod
    import memory.procedural as proc_mod
    import memory.retrieval as ret_mod
    import memory.semantic as sem_mod

    monkeypatch.setattr(ep_mod, "EPISODES_DIR", fake_orch / "memory" / "episodes")
    monkeypatch.setattr(ep_mod, "EP_COUNTER_FILE", fake_orch / "memory" / "episodes" / ".counter")
    monkeypatch.setattr(sem_mod, "SEMANTIC_DIR", fake_orch / "memory" / "semantic")
    monkeypatch.setattr(prune_mod, "SEMANTIC_DIR", fake_orch / "memory" / "semantic")
    monkeypatch.setattr(proc_mod, "PROCEDURAL_DIR", fake_orch / "memory" / "procedural")
    monkeypatch.setattr(cache_mod, "CACHE_DIR", fake_orch / "memory" / "cache")
    monkeypatch.setattr(ret_mod, "RETRIEVAL_DIR", fake_orch / "memory" / "retrieval")
    monkeypatch.setattr(ret_mod, "LOG_FILE", fake_orch / "memory" / "retrieval" / "retrieval_log.jsonl")
    monkeypatch.setattr(ret_mod, "PENDING_DIR", fake_orch / "memory" / "retrieval" / "pending")

    yield fake_orch


def _write_semantic_yaml(sem_dir: Path, memory_id: str, *, confidence: float,
                         created_days_ago: float, retrieval_count: int = 0,
                         last_retrieved_days_ago: float | None = None,
                         links: list | None = None, ref: datetime | None = None) -> None:
    """Write a SEM-*.yaml directly so timestamps are NOT refreshed by write_semantic()."""
    ref = ref or datetime.now(UTC)
    created = (ref - timedelta(days=created_days_ago)).isoformat()
    data = {
        "memory_id": memory_id,
        "name": memory_id.replace("SEM-", ""),
        "description": "test memory",
        "type": "pattern",
        "content": "test content",
        "created_at": created,
        "updated_at": created,
        "retrieval_count": retrieval_count,
        "confidence": confidence,
        "links": links or [],
        "promoted_from_episodes": [],
    }
    if last_retrieved_days_ago is not None:
        data["last_retrieved"] = (ref - timedelta(days=last_retrieved_days_ago)).isoformat()
    with open(sem_dir / f"{memory_id}.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def _make_episode(skill, score, project="testproj", days_ago=0, minutes=0, outcome="success"):
    from memory.schemas import Episode, Outcome
    ts = (NOW - timedelta(days=days_ago) + timedelta(minutes=minutes)).isoformat()
    return Episode(
        episode_id=f"EP-TEST-{skill}-{days_ago}-{minutes}",
        task_id=f"T-{skill}-{days_ago}-{minutes}",
        timestamp=ts,
        skill=skill,
        outcome=Outcome(outcome),
        score=score,
        project=project,
    )


class TestConfidenceDecay:
    def _mem(self, confidence=0.8, created_days_ago=0.0, retrieval_count=0,
             last_retrieved_days_ago=None):
        created = (NOW - timedelta(days=created_days_ago)).isoformat()
        last = (NOW - timedelta(days=last_retrieved_days_ago)).isoformat() \
            if last_retrieved_days_ago is not None else None
        return types.SimpleNamespace(
            confidence=confidence, created_at=created, updated_at=created,
            last_retrieved=last, retrieval_count=retrieval_count,
        )

    def test_fresh_memory_keeps_confidence(self):
        from memory.decay import effective_confidence
        mem = self._mem(confidence=0.8, created_days_ago=0)
        assert effective_confidence(mem, now=NOW) == pytest.approx(0.8, abs=0.001)

    def test_decay_reduces_confidence_over_time(self):
        from memory.decay import effective_confidence
        mem = self._mem(confidence=0.8, created_days_ago=120)
        eff = effective_confidence(mem, now=NOW)
        # 120d age, 60d half-life -> 0.8 * 0.25 = 0.2
        assert eff == pytest.approx(0.2, abs=0.01)
        assert eff < 0.8

    def test_high_retrieval_count_slows_decay(self):
        from memory.decay import effective_confidence
        unused = self._mem(confidence=0.8, created_days_ago=120, retrieval_count=0)
        used = self._mem(confidence=0.8, created_days_ago=120, retrieval_count=10,
                         last_retrieved_days_ago=120)
        eff_unused = effective_confidence(unused, now=NOW)
        eff_used = effective_confidence(used, now=NOW)
        assert eff_used > eff_unused
        assert eff_used > 0.5  # half-life 360d -> barely decayed

    def test_recent_retrieval_freezes_decay_clock(self):
        from memory.decay import effective_confidence
        mem = self._mem(confidence=0.8, created_days_ago=120, retrieval_count=1,
                        last_retrieved_days_ago=1)
        # Age counts from last retrieval (1d), not creation (120d)
        assert effective_confidence(mem, now=NOW) > 0.78

    def test_legacy_memory_without_timestamps_keeps_static_confidence(self):
        from memory.decay import effective_confidence
        legacy = types.SimpleNamespace(confidence=0.7, created_at=None,
                                       updated_at="not-a-date", last_retrieved=None,
                                       retrieval_count=0)
        assert effective_confidence(legacy, now=NOW) == 0.7


class TestPruneUsesDecayedConfidence:
    def test_old_high_confidence_unused_memory_is_pruned(self, isolated_memory):
        """Static confidence 0.9 used to protect forever; decayed it falls below 0.85."""
        from dream.prune import prune
        sem_dir = isolated_memory / "memory" / "semantic"
        _write_semantic_yaml(sem_dir, "SEM-old_conf", confidence=0.9, created_days_ago=40)

        report, state = prune({}, dry_run=False)
        assert "SEM-old_conf" in state["pruned_ids"]
        assert not (sem_dir / "SEM-old_conf.yaml").exists()
        assert (sem_dir / ".archive" / "SEM-old_conf.yaml").exists()

    def test_fresh_memory_is_kept(self, isolated_memory):
        from dream.prune import prune
        sem_dir = isolated_memory / "memory" / "semantic"
        _write_semantic_yaml(sem_dir, "SEM-fresh", confidence=0.9, created_days_ago=2)

        report, state = prune({}, dry_run=False)
        assert "SEM-fresh" not in state["pruned_ids"]
        assert (sem_dir / "SEM-fresh.yaml").exists()

    def test_decay_floor_archives_long_abandoned_retrieved_memory(self, isolated_memory):
        """Retrieved long ago then abandoned -> effective conf < floor -> archived."""
        from dream.prune import prune
        sem_dir = isolated_memory / "memory" / "semantic"
        _write_semantic_yaml(sem_dir, "SEM-abandoned", confidence=0.4,
                             created_days_ago=300, retrieval_count=2,
                             last_retrieved_days_ago=300)

        report, state = prune({}, dry_run=False)
        assert "SEM-abandoned" in state["pruned_ids"]
        assert report.counts["decayed_below_floor"] >= 1

    def test_frequently_retrieved_memory_self_protects(self, isolated_memory):
        from dream.prune import prune
        sem_dir = isolated_memory / "memory" / "semantic"
        _write_semantic_yaml(sem_dir, "SEM-useful", confidence=0.7,
                             created_days_ago=200, retrieval_count=10,
                             last_retrieved_days_ago=10)

        report, state = prune({}, dry_run=False)
        assert "SEM-useful" not in state["pruned_ids"]
        assert (sem_dir / "SEM-useful.yaml").exists()


class TestRetrievalTracking:
    def test_record_and_pop_pending_roundtrip(self, isolated_memory):
        from memory import retrieval
        retrieval.record_pending("T-001", [{"memory_id": "SEM-a"}])
        retrieval.record_pending("T-001", [{"memory_id": "SEM-a"}, {"memory_id": "SEM-b"}])
        pending = retrieval.pop_pending("T-001")
        assert [m["memory_id"] for m in pending] == ["SEM-a", "SEM-b"]  # deduped
        assert retrieval.pop_pending("T-001") == []  # consumed

    def test_pop_pending_missing_task_returns_empty(self, isolated_memory):
        from memory import retrieval
        assert retrieval.pop_pending("T-nope") == []
        assert retrieval.pop_pending("") == []

    def test_on_task_complete_increments_retrieval_count(self, isolated_memory):
        from memory import hooks, semantic
        from memory.schemas import SemanticMemory
        semantic.write_semantic(SemanticMemory(memory_id="SEM-hit", name="hit", confidence=0.7))
        assert semantic.read_semantic("SEM-hit").retrieval_count == 0

        hooks.on_task_complete(
            task_id="T-100", skill="dario-brand", outcome="success", score=88,
            project="testproj",
            retrieved_memories=[{"memory_id": "SEM-hit", "layer": "semantic"}],
        )
        mem = semantic.read_semantic("SEM-hit")
        assert mem.retrieval_count == 1
        assert mem.last_retrieved is not None
        # Retrieval log got the entry too
        from memory import retrieval
        assert retrieval.frequency_by_memory(7).get("SEM-hit") == 1

    def test_completion_hooks_consume_pending_retrievals(self, isolated_memory, monkeypatch):
        """run_learning_writebacks auto-loads pending memories and marks them used."""
        from memory import retrieval, semantic
        from memory.schemas import SemanticMemory

        # Stub the cognitive write-backs that would touch real state
        def _stub(name, **attrs):
            mod = types.ModuleType(name)
            for k, v in attrs.items():
                setattr(mod, k, v)
            monkeypatch.setitem(sys.modules, name, mod)

        class _Registry:
            def emit(self, *a, **k):
                pass

        _stub("cognitive.synaptic_update", process_completion=lambda **k: [])
        _stub("cognitive.qvalue_memory_wire", record_outcome=lambda **k: None)
        _stub("dispatch.dispatch_cot", postmortem=lambda *a, **k: None)
        _stub("reliability.reactive_subscriptions", on_task_completed=lambda *a, **k: [])
        _stub("core.lifecycle_hooks", get_registry=lambda: _Registry())

        semantic.write_semantic(SemanticMemory(memory_id="SEM-ctx", name="ctx", confidence=0.7))
        retrieval.record_pending("T-CH-1", [{"memory_id": "SEM-ctx", "layer": "semantic"}])

        from execution.completion_hooks import run_learning_writebacks
        info = run_learning_writebacks(
            task={}, task_id="T-CH-1", skill="dario-brand", project="testproj",
            score=75, tokens=100, status="done", output="output text",
        )
        assert info.get("episode_recorded") is True
        assert info.get("retrieved_memories_tracked") == 1
        assert semantic.read_semantic("SEM-ctx").retrieval_count == 1
        assert retrieval.pop_pending("T-CH-1") == []  # consumed


class TestRealisticPatternThresholds:
    def test_quality_trend_fires_with_three_runs(self):
        from dream.pattern_detector import detect_patterns
        eps = [_make_episode("some-skill", s, minutes=i) for i, s in enumerate([95, 80, 70])]
        patterns = detect_patterns(eps)
        assert any("regression" in p.lower() for p in patterns), patterns

    def test_convergence_fires_with_two_sessions_avg_above_60(self, isolated_memory):
        """2 sessions of the same sequence, avg score 65 — must promote now."""
        from dream.convergence import promote_convergent
        from dream.pattern_detector import detect_convergence
        from memory import procedural

        episodes = []
        for day in (1, 2):  # two distinct day-sessions, same project
            episodes.append(_make_episode("skill-a", 63, days_ago=day, minutes=0))
            episodes.append(_make_episode("skill-b", 67, days_ago=day, minutes=10))

        candidates = detect_convergence(episodes)
        assert any(c["sequence"] == ["skill-a", "skill-b"] for c in candidates), candidates

        promoted = promote_convergent(episodes, candidates, dry_run=False)
        assert promoted, "2 sessions with avg 65 must promote under the new thresholds"
        wfs = procedural.list_workflows()
        assert any(w.skills_sequence == ["skill-a", "skill-b"] for w in wfs)

    def test_convergence_still_rejects_below_min_score(self, isolated_memory):
        from dream.convergence import promote_convergent

        episodes = []
        for day in (1, 2):
            episodes.append(_make_episode("skill-a", 50, days_ago=day, minutes=0))
            episodes.append(_make_episode("skill-b", 55, days_ago=day, minutes=10))

        candidates = [{"sequence": ["skill-a", "skill-b"], "session_count": 2,
                       "projects": ["testproj"]}]
        assert promote_convergent(episodes, candidates, dry_run=False) == []

    def test_thresholds_come_from_single_config_source(self):
        from dream import convergence
        from dream.pattern_detector import CONVERGENCE_MIN_SESSIONS, FAILURE_MIN, TREND_MIN_RUNS
        from memory.config import get as cfg
        assert convergence.MIN_SESSIONS == int(cfg("convergence_min_sessions"))
        assert convergence.MIN_SCORE == float(cfg("convergence_min_score"))
        assert TREND_MIN_RUNS == int(cfg("pattern_trend_min_runs"))
        assert FAILURE_MIN == int(cfg("pattern_failure_min"))
        assert CONVERGENCE_MIN_SESSIONS == int(cfg("convergence_min_sessions"))


class TestOrphanEmbeddingPrune:
    """prune_orphan_embeddings removes vectors for archived/merged memories.

    Regression for the retrieval_count starvation found 2026-06-13: Dream archived
    memories but left their embeddings behind (54 rows for 14 live memories), and
    high-similarity orphans stole top_k slots so search_memories returned [] even
    when a live memory was relevant — so retrieval_count never moved and the prune
    saw useful memories as never-retrieved.
    """

    def _make_table(self, tmp_path):
        import sqlite3

        from memory import semantic_search as ss
        db = tmp_path / "orch.db"
        conn = sqlite3.connect(str(db))
        ss._ensure_schema(conn)
        for mid in ("SEM-live-1", "SEM-live-2", "SEM-dead-1", "SEM-dead-2", "SEM-dead-3"):
            conn.execute(
                "INSERT INTO memory_embeddings (memory_id, content_hash, vec, updated_at) "
                "VALUES (?, 'h', ?, datetime('now'))",
                (mid, b"\x00\x00\x00\x00"),
            )
        conn.commit()
        return conn

    def test_removes_only_orphans(self, tmp_path):
        from memory import semantic_search as ss
        conn = self._make_table(tmp_path)
        removed = ss.prune_orphan_embeddings(conn, {"SEM-live-1", "SEM-live-2"})
        assert removed == 3
        remaining = {r[0] for r in conn.execute("SELECT memory_id FROM memory_embeddings").fetchall()}
        assert remaining == {"SEM-live-1", "SEM-live-2"}
        conn.close()

    def test_noop_when_all_live(self, tmp_path):
        from memory import semantic_search as ss
        conn = self._make_table(tmp_path)
        live = {"SEM-live-1", "SEM-live-2", "SEM-dead-1", "SEM-dead-2", "SEM-dead-3"}
        assert ss.prune_orphan_embeddings(conn, live) == 0
        assert conn.execute("SELECT COUNT(*) FROM memory_embeddings").fetchone()[0] == 5
        conn.close()

    def test_empty_live_set_is_refused(self, tmp_path):
        """An empty live set means a wrong/isolated context (e.g. a test that
        redirects SEMANTIC_DIR but not DB_PATH), not total archival. Deleting on
        it would wipe every real embedding — the safety guard must refuse."""
        from memory import semantic_search as ss
        conn = self._make_table(tmp_path)
        assert ss.prune_orphan_embeddings(conn, set()) == 0
        assert conn.execute("SELECT COUNT(*) FROM memory_embeddings").fetchone()[0] == 5
        conn.close()
