"""Behavior tests for enforcement.token_capture (Faixa 3 #1).

Closes the honor-system gap where Agent tool tokens were guessed by close_*.py
scripts. These tests exercise REAL code paths against synthetic transcript
JSONL fixtures and a temp orchestrator dir.

Test budget: ~25 tests covering parse, aggregate, attribute, write, dedup,
and resilience (missing files, malformed JSON, no sidechain, etc).
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


@pytest.fixture
def isolated_capture(tmp_path, monkeypatch):
    """Redirect ORCH_DIR, RUNS_DIR, STATE_FILE, DEBUG_LOG to tmp_path."""
    fake_orch = tmp_path / "orchestrator"
    fake_orch.mkdir()
    (fake_orch / "tasks" / "active").mkdir(parents=True)
    (fake_orch / "tasks" / "done").mkdir(parents=True)
    (fake_orch / "state").mkdir()

    import enforcement.token_capture as tc
    monkeypatch.setattr(tc, "ORCH_DIR", fake_orch)
    monkeypatch.setattr(tc, "RUNS_DIR", fake_orch / "subagent_runs")
    monkeypatch.setattr(tc, "STATE_FILE", fake_orch / "state" / "last_subagent_capture.json")
    monkeypatch.setattr(tc, "DEBUG_LOG", fake_orch / "state" / "debug.jsonl")
    return fake_orch


def _make_sidechain_msg(uuid: str, ts: str, model: str = "claude-opus-4-7",
                        input_tokens: int = 1, output_tokens: int = 100,
                        cache_creation: int = 2000, cache_read: int = 50000,
                        text: str = "executing task") -> dict:
    return {
        "uuid": uuid,
        "isSidechain": True,
        "timestamp": ts,
        "sessionId": "test-session-001",
        "message": {
            "model": model,
            "role": "assistant",
            "content": [{"type": "text", "text": text}],
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": cache_creation,
                "cache_read_input_tokens": cache_read,
            },
        },
    }


def _write_transcript(path: Path, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


# ────────────────────────────────────────────────────────────────────────
# parse_transcript_sidechains
# ────────────────────────────────────────────────────────────────────────

class TestParseTranscript:

    def test_empty_file_returns_empty(self, isolated_capture):
        from enforcement.token_capture import parse_transcript_sidechains
        tp = isolated_capture / "transcript.jsonl"
        _write_transcript(tp, [])
        assert parse_transcript_sidechains(tp, None, set()) == []

    def test_missing_file_returns_empty(self, isolated_capture):
        from enforcement.token_capture import parse_transcript_sidechains
        result = parse_transcript_sidechains(isolated_capture / "nope.jsonl", None, set())
        assert result == []

    def test_skips_non_sidechain_messages(self, isolated_capture):
        from enforcement.token_capture import parse_transcript_sidechains
        tp = isolated_capture / "transcript.jsonl"
        main_msg = _make_sidechain_msg("main-1", "2026-05-26T10:00:00Z")
        main_msg["isSidechain"] = False
        sidechain_msg = _make_sidechain_msg("sc-1", "2026-05-26T10:01:00Z")
        _write_transcript(tp, [main_msg, sidechain_msg])
        result = parse_transcript_sidechains(tp, None, set())
        assert len(result) == 1
        assert result[0]["uuid"] == "sc-1"

    def test_skips_messages_without_usage(self, isolated_capture):
        from enforcement.token_capture import parse_transcript_sidechains
        tp = isolated_capture / "transcript.jsonl"
        no_usage = _make_sidechain_msg("nu-1", "2026-05-26T10:00:00Z")
        del no_usage["message"]["usage"]
        with_usage = _make_sidechain_msg("wu-1", "2026-05-26T10:01:00Z")
        _write_transcript(tp, [no_usage, with_usage])
        result = parse_transcript_sidechains(tp, None, set())
        assert len(result) == 1
        assert result[0]["uuid"] == "wu-1"

    def test_filters_by_since_ts(self, isolated_capture):
        from enforcement.token_capture import parse_transcript_sidechains
        tp = isolated_capture / "transcript.jsonl"
        old = _make_sidechain_msg("old", "2026-05-26T10:00:00Z")
        new = _make_sidechain_msg("new", "2026-05-26T11:00:00Z")
        _write_transcript(tp, [old, new])
        result = parse_transcript_sidechains(tp, "2026-05-26T10:30:00Z", set())
        assert [m["uuid"] for m in result] == ["new"]

    def test_filters_by_seen_uuids(self, isolated_capture):
        from enforcement.token_capture import parse_transcript_sidechains
        tp = isolated_capture / "transcript.jsonl"
        m1 = _make_sidechain_msg("seen", "2026-05-26T10:00:00Z")
        m2 = _make_sidechain_msg("fresh", "2026-05-26T10:01:00Z")
        _write_transcript(tp, [m1, m2])
        result = parse_transcript_sidechains(tp, None, {"seen"})
        assert [m["uuid"] for m in result] == ["fresh"]

    def test_tolerates_malformed_json_lines(self, isolated_capture):
        from enforcement.token_capture import parse_transcript_sidechains
        tp = isolated_capture / "transcript.jsonl"
        tp.parent.mkdir(parents=True, exist_ok=True)
        good = _make_sidechain_msg("good", "2026-05-26T10:00:00Z")
        with open(tp, "w", encoding="utf-8") as f:
            f.write("not json at all\n")
            f.write(json.dumps(good) + "\n")
            f.write("{\"truncated\":\n")
        result = parse_transcript_sidechains(tp, None, set())
        assert len(result) == 1
        assert result[0]["uuid"] == "good"


# ────────────────────────────────────────────────────────────────────────
# aggregate_usage
# ────────────────────────────────────────────────────────────────────────

class TestAggregateUsage:

    def test_sums_all_token_kinds(self, isolated_capture):
        from enforcement.token_capture import aggregate_usage
        msgs = [
            {"uuid": "a", "model": "claude-opus-4-7",
             "usage": {"input_tokens": 10, "output_tokens": 100,
                       "cache_creation_input_tokens": 1000,
                       "cache_read_input_tokens": 10000}},
            {"uuid": "b", "model": "claude-opus-4-7",
             "usage": {"input_tokens": 20, "output_tokens": 200,
                       "cache_creation_input_tokens": 2000,
                       "cache_read_input_tokens": 20000}},
        ]
        totals = aggregate_usage(msgs)
        assert totals["input_tokens"] == 30
        assert totals["output_tokens"] == 300
        assert totals["cache_creation_input_tokens"] == 3000
        assert totals["cache_read_input_tokens"] == 30000
        assert totals["total_tokens"] == 33330
        assert totals["message_count"] == 2

    def test_groups_by_model(self, isolated_capture):
        from enforcement.token_capture import aggregate_usage
        msgs = [
            {"uuid": "a", "model": "claude-opus-4-7",
             "usage": {"input_tokens": 10, "output_tokens": 100,
                       "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}},
            {"uuid": "b", "model": "claude-haiku-4-5",
             "usage": {"input_tokens": 50, "output_tokens": 500,
                       "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}},
        ]
        totals = aggregate_usage(msgs)
        assert "claude-opus-4-7" in totals["by_model"]
        assert "claude-haiku-4-5" in totals["by_model"]
        assert totals["by_model"]["claude-opus-4-7"]["input"] == 10
        assert totals["by_model"]["claude-haiku-4-5"]["output"] == 500

    def test_cost_calculation_opus(self, isolated_capture):
        from enforcement.token_capture import aggregate_usage
        msgs = [
            {"uuid": "a", "model": "claude-opus-4-7",
             "usage": {"input_tokens": 1_000_000, "output_tokens": 1_000_000,
                       "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}},
        ]
        totals = aggregate_usage(msgs)
        # Opus 4.7: $5/M in + $25/M out = $30 total
        assert totals["cost_usd"] == 30.0

    def test_cost_calculation_with_cache(self, isolated_capture):
        from enforcement.token_capture import aggregate_usage
        msgs = [
            {"uuid": "a", "model": "claude-opus-4-7",
             "usage": {"input_tokens": 0, "output_tokens": 0,
                       "cache_creation_input_tokens": 1_000_000,
                       "cache_read_input_tokens": 1_000_000}},
        ]
        totals = aggregate_usage(msgs)
        # $6.25 cache_write + $0.50 cache_read = $6.75
        assert totals["cost_usd"] == 6.75

    def test_unknown_model_uses_default_pricing(self, isolated_capture):
        from enforcement.token_capture import aggregate_usage
        msgs = [
            {"uuid": "a", "model": "claude-future-model-99",
             "usage": {"input_tokens": 1_000_000, "output_tokens": 0,
                       "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}},
        ]
        totals = aggregate_usage(msgs)
        # Default = $5.00 input
        assert totals["cost_usd"] == 5.0

    def test_empty_list_returns_zero(self, isolated_capture):
        from enforcement.token_capture import aggregate_usage
        totals = aggregate_usage([])
        assert totals["total_tokens"] == 0
        assert totals["cost_usd"] == 0.0
        assert totals["message_count"] == 0


# ────────────────────────────────────────────────────────────────────────
# find_task_id
# ────────────────────────────────────────────────────────────────────────

class TestFindTaskId:

    def test_explicit_marker_wins(self, isolated_capture):
        from enforcement.token_capture import find_task_id
        msgs = [
            {"content_preview": "some preamble [TASK_ID:CUI-005] more text"},
            {"content_preview": "different ABC-001 nearby"},
        ]
        assert find_task_id(msgs) == "CUI-005"

    def test_falls_back_to_bare_pattern(self, isolated_capture):
        from enforcement.token_capture import find_task_id
        msgs = [{"content_preview": "Executing task CRE-007 for project credito"}]
        assert find_task_id(msgs) == "CRE-007"

    def test_no_match_returns_none(self, isolated_capture):
        from enforcement.token_capture import find_task_id
        msgs = [{"content_preview": "no identifiers here"}]
        assert find_task_id(msgs) is None

    def test_empty_messages_returns_none(self, isolated_capture):
        from enforcement.token_capture import find_task_id
        assert find_task_id([]) is None

    def test_blocklist_filters_cve_iso_etc(self, isolated_capture):
        """CVE-2021, ISO-9001, RFC-3986 etc should NOT match as task IDs."""
        from enforcement.token_capture import find_task_id
        msgs = [
            {"content_preview": "Patching CVE-2021 vulnerability in lib"},
            {"content_preview": "Reviewing ISO-9001 compliance"},
            {"content_preview": "RFC-3986 URI parsing question"},
        ]
        assert find_task_id(msgs) is None

    def test_blocklist_does_not_block_real_task_id(self, isolated_capture):
        """Real task IDs like CUI-005, ATR-042 must still match even when CVE is nearby."""
        from enforcement.token_capture import find_task_id
        msgs = [{"content_preview": "patching CVE-2021 in context of CUI-005"}]
        assert find_task_id(msgs) == "CUI-005"


# ────────────────────────────────────────────────────────────────────────
# update_task_yaml
# ────────────────────────────────────────────────────────────────────────

class TestUpdateTaskYaml:

    def _write_task(self, orch: Path, subdir: str, task_id: str, body: dict) -> Path:
        path = orch / "tasks" / subdir / f"{task_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(body, f)
        return path

    def test_writes_actual_tokens_to_active_task(self, isolated_capture):
        from enforcement.token_capture import update_task_yaml
        path = self._write_task(isolated_capture, "active", "TEST-001",
                                {"id": "TEST-001", "status": "in_progress"})
        totals = {
            "input_tokens": 100, "output_tokens": 200,
            "cache_creation_input_tokens": 1000, "cache_read_input_tokens": 10000,
            "total_tokens": 11300, "cost_usd": 0.05,
        }
        ok = update_task_yaml("TEST-001", totals)
        assert ok is True
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["actual_tokens"] == 11300
        assert data["actual_tokens_breakdown"]["input"] == 100
        assert data["actual_tokens_breakdown"]["cache_read"] == 10000
        assert data["actual_cost_usd"] == 0.05
        assert data["token_capture_source"] == "subagent_stop_hook"

    def test_writes_to_done_task_too(self, isolated_capture):
        from enforcement.token_capture import update_task_yaml
        self._write_task(isolated_capture, "done", "DONE-001", {"id": "DONE-001"})
        totals = {"input_tokens": 5, "output_tokens": 10,
                  "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
                  "total_tokens": 15, "cost_usd": 0.0001}
        assert update_task_yaml("DONE-001", totals) is True

    def test_adds_to_existing_actual_tokens(self, isolated_capture):
        """Re-running the hook on the same task accumulates, not overwrites."""
        from enforcement.token_capture import update_task_yaml
        path = self._write_task(isolated_capture, "active", "TEST-002",
                                {"id": "TEST-002", "actual_tokens": 5000})
        totals = {"input_tokens": 10, "output_tokens": 20,
                  "cache_creation_input_tokens": 100, "cache_read_input_tokens": 500,
                  "total_tokens": 630, "cost_usd": 0.001}
        update_task_yaml("TEST-002", totals)
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["actual_tokens"] == 5630

    def test_missing_task_returns_false(self, isolated_capture):
        from enforcement.token_capture import update_task_yaml
        ok = update_task_yaml("NONEXISTENT-999", {"total_tokens": 100, "input_tokens": 0,
                                                   "output_tokens": 0,
                                                   "cache_creation_input_tokens": 0,
                                                   "cache_read_input_tokens": 0,
                                                   "cost_usd": 0})
        assert ok is False


# ────────────────────────────────────────────────────────────────────────
# capture (end-to-end pipeline)
# ────────────────────────────────────────────────────────────────────────

class TestCaptureEndToEnd:

    def test_no_transcript_path_returns_noop(self, isolated_capture):
        from enforcement.token_capture import capture
        result = capture({})
        assert result["status"] == "no_transcript_path"

    def test_missing_transcript_returns_noop(self, isolated_capture):
        from enforcement.token_capture import capture
        result = capture({"transcript_path": str(isolated_capture / "nope.jsonl")})
        assert result["status"] == "transcript_missing"

    def test_no_sidechain_returns_noop(self, isolated_capture):
        from enforcement.token_capture import capture
        tp = isolated_capture / "transcript.jsonl"
        main_only = _make_sidechain_msg("main", "2026-05-26T10:00:00Z")
        main_only["isSidechain"] = False
        _write_transcript(tp, [main_only])
        result = capture({"transcript_path": str(tp), "session_id": "sess1"})
        assert result["status"] == "no_new_sidechain_messages"

    def test_full_capture_writes_run_record(self, isolated_capture):
        from enforcement.token_capture import capture
        tp = isolated_capture / "transcript.jsonl"
        msg = _make_sidechain_msg("agent-1", "2026-05-26T10:00:00Z",
                                  text="Executing task CUI-007")
        _write_transcript(tp, [msg])
        result = capture({"transcript_path": str(tp), "session_id": "abc12345"})
        assert result["status"] == "captured"
        assert result["messages_captured"] == 1
        assert result["task_id"] == "CUI-007"
        assert result["total_tokens"] > 0
        assert result["run_path"] is not None
        # Run record exists
        run_path = Path(result["run_path"])
        assert run_path.exists()
        record = json.loads(run_path.read_text(encoding="utf-8"))
        assert record["task_id"] == "CUI-007"
        assert record["totals"]["total_tokens"] == result["total_tokens"]

    def test_capture_updates_state_for_dedup(self, isolated_capture):
        from enforcement.token_capture import capture, load_state
        tp = isolated_capture / "transcript.jsonl"
        msg = _make_sidechain_msg("agent-1", "2026-05-26T10:00:00Z")
        _write_transcript(tp, [msg])
        capture({"transcript_path": str(tp), "session_id": "s1"})
        state = load_state()
        assert "agent-1" in state["captured_uuids"]
        assert state["last_capture_ts"] == "2026-05-26T10:00:00Z"

    def test_capture_is_idempotent(self, isolated_capture):
        """Running capture twice on same transcript captures only once."""
        from enforcement.token_capture import capture
        tp = isolated_capture / "transcript.jsonl"
        msg = _make_sidechain_msg("agent-1", "2026-05-26T10:00:00Z")
        _write_transcript(tp, [msg])
        r1 = capture({"transcript_path": str(tp), "session_id": "s1"})
        r2 = capture({"transcript_path": str(tp), "session_id": "s1"})
        assert r1["status"] == "captured"
        assert r2["status"] == "no_new_sidechain_messages"

    def test_capture_picks_up_new_sidechain_on_second_run(self, isolated_capture):
        """Adding a new sidechain message after first capture is captured second."""
        from enforcement.token_capture import capture
        tp = isolated_capture / "transcript.jsonl"
        msg1 = _make_sidechain_msg("agent-1", "2026-05-26T10:00:00Z")
        _write_transcript(tp, [msg1])
        capture({"transcript_path": str(tp), "session_id": "s1"})
        msg2 = _make_sidechain_msg("agent-2", "2026-05-26T10:01:00Z")
        _write_transcript(tp, [msg1, msg2])
        r = capture({"transcript_path": str(tp), "session_id": "s1"})
        assert r["status"] == "captured"
        assert r["messages_captured"] == 1

    def test_capture_writes_to_task_yaml_when_task_id_found(self, isolated_capture):
        from enforcement.token_capture import capture
        task_path = isolated_capture / "tasks" / "active" / "PROJ-042.yaml"
        with open(task_path, "w", encoding="utf-8") as f:
            yaml.dump({"id": "PROJ-042", "status": "in_progress"}, f)
        tp = isolated_capture / "transcript.jsonl"
        msg = _make_sidechain_msg("agent-x", "2026-05-26T10:00:00Z",
                                  text="[TASK_ID:PROJ-042] do the thing")
        _write_transcript(tp, [msg])
        result = capture({"transcript_path": str(tp), "session_id": "s1"})
        assert result["task_id"] == "PROJ-042"
        data = yaml.safe_load(task_path.read_text(encoding="utf-8"))
        assert data["actual_tokens"] > 0
        assert data["token_capture_source"] == "subagent_stop_hook"


# ────────────────────────────────────────────────────────────────────────
# main / hook entrypoint
# ────────────────────────────────────────────────────────────────────────

class TestMainEntrypoint:

    def test_main_handles_malformed_stdin(self, isolated_capture, monkeypatch, capsys):
        from enforcement import token_capture as tc
        import io
        monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
        rc = tc.main()
        assert rc == 0  # Never fails even with bad input

    def test_main_handles_valid_empty_payload(self, isolated_capture, monkeypatch):
        from enforcement import token_capture as tc
        import io
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({})))
        rc = tc.main()
        assert rc == 0

    def test_main_does_not_raise_on_internal_error(self, isolated_capture, monkeypatch):
        """Even if internals throw, main returns 0 to not block Claude Code."""
        from enforcement import token_capture as tc
        import io
        def boom(_payload):
            raise RuntimeError("internal explosion")
        monkeypatch.setattr(tc, "capture", boom)
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"x": 1})))
        rc = tc.main()
        assert rc == 0
