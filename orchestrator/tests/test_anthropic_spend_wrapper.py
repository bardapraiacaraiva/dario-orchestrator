"""Tests for TrackedAnthropic wrapper + spend aggregator (gap #6)."""

from __future__ import annotations

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


@pytest.fixture
def isolated_spend_log(tmp_path, monkeypatch):
    """Redirect BOTH SPEND_LOG (yaml legacy) and SPEND_JSONL (new primary)
    to tmp_path, AND point SQLite DB at a fresh tmp file so the aggregator's
    DB-first read doesn't pick up the production database."""
    fake_yaml = tmp_path / "api_spend_log.yaml"
    fake_jsonl = tmp_path / "api_spend_log.jsonl"
    fake_db = tmp_path / "test_orchestrator.db"
    monkeypatch.setattr("scripts.anthropic_spend_wrapper.SPEND_LOG", fake_yaml)
    monkeypatch.setattr("scripts.anthropic_spend_wrapper.SPEND_JSONL", fake_jsonl)
    monkeypatch.setattr("scripts.aggregate_api_spend.SPEND_LOG", fake_yaml)
    monkeypatch.setattr("scripts.aggregate_api_spend.SPEND_JSONL", fake_jsonl)
    # Force a fresh DB for these tests — production DB has unrelated rows
    from core import db as _db_module
    monkeypatch.setattr(_db_module, "DB_PATH", fake_db)
    return fake_yaml


@pytest.fixture
def mock_anthropic(monkeypatch):
    """Replace anthropic.Anthropic with a mock that returns predictable usage."""
    import scripts.anthropic_spend_wrapper as wrap

    fake_resp = MagicMock()
    fake_resp.usage.input_tokens = 200
    fake_resp.usage.output_tokens = 100
    fake_client = MagicMock()
    fake_client.messages.create.return_value = fake_resp
    fake_anthropic = MagicMock(return_value=fake_client)
    monkeypatch.setattr(wrap, "Anthropic", fake_anthropic)
    return fake_anthropic


# ─────────────────────────────────────────────────────────────────────
# Pricing + cost estimate
# ─────────────────────────────────────────────────────────────────────

class TestPricing:

    def test_opus_4_7_priced(self):
        from scripts.anthropic_spend_wrapper import PRICING
        assert "claude-opus-4-7" in PRICING
        assert PRICING["claude-opus-4-7"]["input"] == 5.00
        assert PRICING["claude-opus-4-7"]["output"] == 25.00

    def test_haiku_4_5_priced(self):
        from scripts.anthropic_spend_wrapper import PRICING
        assert "claude-haiku-4-5" in PRICING

    def test_cost_estimate_opus(self):
        from scripts.anthropic_spend_wrapper import estimate_cost_usd
        # 1M input + 1M output for opus-4-7 = $5 + $25 = $30
        assert estimate_cost_usd("claude-opus-4-7", 1_000_000, 1_000_000) == 30.00

    def test_cost_estimate_unknown_model_uses_fallback(self):
        from scripts.anthropic_spend_wrapper import estimate_cost_usd
        # Should not raise — uses fallback pricing
        cost = estimate_cost_usd("unknown-model-xyz", 1000, 500)
        assert cost > 0


# ─────────────────────────────────────────────────────────────────────
# Wrapper instantiation + call passthrough
# ─────────────────────────────────────────────────────────────────────

class TestWrapper:

    def test_requires_caller_name(self, isolated_spend_log, mock_anthropic):
        from scripts.anthropic_spend_wrapper import TrackedAnthropic
        with pytest.raises(ValueError, match="caller"):
            TrackedAnthropic(caller="")
        with pytest.raises(ValueError, match="caller"):
            TrackedAnthropic(caller=None)

    def test_create_logs_entry(self, isolated_spend_log, mock_anthropic):
        from scripts.anthropic_spend_wrapper import TrackedAnthropic
        client = TrackedAnthropic(caller="test/wrapper-suite")
        resp = client.messages.create(
            model="claude-opus-4-7", max_tokens=200,
            messages=[{"role": "user", "content": "hi"}],
        )
        # Mock returned 200 input / 100 output
        assert resp.usage.input_tokens == 200

        import yaml
        data = yaml.safe_load(isolated_spend_log.read_text(encoding="utf-8"))
        assert len(data["entries"]) == 1
        entry = data["entries"][0]
        assert entry["caller"] == "test/wrapper-suite"
        assert entry["model"] == "claude-opus-4-7"
        assert entry["input_tokens"] == 200
        assert entry["output_tokens"] == 100
        assert entry["total_tokens"] == 300
        # Cost: 200/1M * 5 + 100/1M * 25 = 0.001 + 0.0025 = 0.0035
        assert entry["cost_usd"] == pytest.approx(0.0035, abs=1e-6)

    def test_multiple_calls_accumulate(self, isolated_spend_log, mock_anthropic):
        from scripts.anthropic_spend_wrapper import TrackedAnthropic
        client = TrackedAnthropic(caller="test/multi")
        for _ in range(3):
            client.messages.create(model="claude-haiku-4-5", max_tokens=100,
                                   messages=[{"role": "user", "content": "x"}])
        import yaml
        data = yaml.safe_load(isolated_spend_log.read_text(encoding="utf-8"))
        assert len(data["entries"]) == 3

    def test_logging_failure_does_not_break_call(self, isolated_spend_log,
                                                  mock_anthropic, monkeypatch):
        from scripts.anthropic_spend_wrapper import TrackedAnthropic
        # Force _append_entry to raise
        def _broken(_):
            raise OSError("disk full")
        monkeypatch.setattr("scripts.anthropic_spend_wrapper._append_entry", _broken)
        client = TrackedAnthropic(caller="test/broken-log")
        # Call should still succeed
        resp = client.messages.create(model="claude-opus-4-7", max_tokens=200,
                                      messages=[{"role": "user", "content": "x"}])
        assert resp.usage.input_tokens == 200

    def test_passthrough_for_non_messages_attrs(self, isolated_spend_log,
                                                 mock_anthropic):
        from scripts.anthropic_spend_wrapper import TrackedAnthropic
        client = TrackedAnthropic(caller="test/passthrough")
        # The mock has whatever attrs MagicMock auto-creates — access should not fail
        _ = client.completions  # arbitrary attribute, mock will return MagicMock


# ─────────────────────────────────────────────────────────────────────
# Aggregator
# ─────────────────────────────────────────────────────────────────────

class TestAggregator:

    def _seed(self, log_path, entries):
        import yaml
        data = {"schema_version": 1, "entries": entries}
        log_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def test_empty_returns_zero(self, isolated_spend_log):
        from scripts.aggregate_api_spend import aggregate, load_entries
        agg = aggregate(load_entries())
        assert agg["n_calls"] == 0
        assert agg["total_usd"] == 0.0
        assert agg["by_caller"] == {}

    def test_single_entry_aggregates(self, isolated_spend_log):
        now = datetime.now(UTC).isoformat(timespec="seconds")
        self._seed(isolated_spend_log, [
            {"ts": now, "caller": "x", "model": "claude-opus-4-7",
             "input_tokens": 1000, "output_tokens": 500, "total_tokens": 1500,
             "cost_usd": 0.0175},
        ])
        from scripts.aggregate_api_spend import aggregate, load_entries
        agg = aggregate(load_entries())
        assert agg["n_calls"] == 1
        assert agg["total_usd"] == 0.0175
        assert agg["by_caller"]["x"]["calls"] == 1

    def test_window_filters_old_entries(self, isolated_spend_log):
        now = datetime.now(UTC)
        old_ts = (now - timedelta(hours=48)).isoformat(timespec="seconds")
        new_ts = now.isoformat(timespec="seconds")
        self._seed(isolated_spend_log, [
            {"ts": old_ts, "caller": "old", "model": "claude-opus-4-7",
             "input_tokens": 100, "output_tokens": 0, "total_tokens": 100,
             "cost_usd": 0.0005},
            {"ts": new_ts, "caller": "new", "model": "claude-opus-4-7",
             "input_tokens": 200, "output_tokens": 0, "total_tokens": 200,
             "cost_usd": 0.0010},
        ])
        from scripts.aggregate_api_spend import aggregate, load_entries
        all_entries = load_entries()
        assert aggregate(all_entries, window_hours=24)["n_calls"] == 1
        assert aggregate(all_entries)["n_calls"] == 2

    def test_month_filter(self, isolated_spend_log):
        self._seed(isolated_spend_log, [
            {"ts": "2026-05-01T10:00:00+00:00", "caller": "a", "model": "x",
             "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost_usd": 0.01},
            {"ts": "2026-04-30T23:59:59+00:00", "caller": "b", "model": "x",
             "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost_usd": 0.02},
        ])
        from scripts.aggregate_api_spend import aggregate, load_entries
        all_entries = load_entries()
        may = aggregate(all_entries, month="2026-05")
        april = aggregate(all_entries, month="2026-04")
        assert may["n_calls"] == 1 and may["total_usd"] == 0.01
        assert april["n_calls"] == 1 and april["total_usd"] == 0.02

    def test_per_caller_breakdown(self, isolated_spend_log):
        now = datetime.now(UTC).isoformat(timespec="seconds")
        self._seed(isolated_spend_log, [
            {"ts": now, "caller": "dspy/compile", "model": "haiku",
             "input_tokens": 100, "output_tokens": 50, "total_tokens": 150,
             "cost_usd": 0.0001},
            {"ts": now, "caller": "dspy/compile", "model": "haiku",
             "input_tokens": 100, "output_tokens": 50, "total_tokens": 150,
             "cost_usd": 0.0001},
            {"ts": now, "caller": "judge/eval", "model": "haiku",
             "input_tokens": 200, "output_tokens": 100, "total_tokens": 300,
             "cost_usd": 0.0003},
        ])
        from scripts.aggregate_api_spend import aggregate, load_entries
        agg = aggregate(load_entries())
        assert agg["by_caller"]["dspy/compile"]["calls"] == 2
        assert agg["by_caller"]["dspy/compile"]["tokens"] == 300
        assert agg["by_caller"]["judge/eval"]["calls"] == 1
        assert agg["by_caller"]["judge/eval"]["tokens"] == 300

    def test_per_model_breakdown(self, isolated_spend_log):
        now = datetime.now(UTC).isoformat(timespec="seconds")
        self._seed(isolated_spend_log, [
            {"ts": now, "caller": "x", "model": "claude-opus-4-7",
             "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost_usd": 0.05},
            {"ts": now, "caller": "x", "model": "claude-haiku-4-5",
             "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost_usd": 0.01},
        ])
        from scripts.aggregate_api_spend import aggregate, load_entries
        agg = aggregate(load_entries())
        assert agg["by_model"]["claude-opus-4-7"]["cost_usd"] == 0.05
        assert agg["by_model"]["claude-haiku-4-5"]["cost_usd"] == 0.01
