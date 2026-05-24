"""Tests for budget_breakdown_by_type — dev vs client visibility (gap #4)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from scripts.budget_breakdown_by_type import (
    aggregate_month,
    classify,
    load_types_config,
)


class TestTypesConfig:
    """Live config sanity."""

    def test_config_loads(self):
        cfg = load_types_config()
        assert "clients" in cfg
        assert "dev" in cfg

    def test_known_clients_classified(self):
        cfg = load_types_config()
        for client in ("cuidai", "credito", "arrecada-gov", "atrium",
                       "lucas", "vivenda", "pupli", "atelier-ai",
                       "tributario-ai"):
            assert classify(client, cfg) == "client", (
                f"{client} should be classified as client"
            )

    def test_known_dev_slugs_classified(self):
        cfg = load_types_config()
        for dev in ("audit", "test", "dario", "padrao-a", "ruflo-audit"):
            assert classify(dev, cfg) == "dev", (
                f"{dev} should be classified as dev"
            )

    def test_unmapped_defaults_to_unknown(self):
        cfg = load_types_config()
        assert classify("totally-new-project-xyz-123", cfg) == "unknown"

    def test_blank_classified_as_unknown(self):
        cfg = load_types_config()
        assert classify("", cfg) == "unknown"
        assert classify("   ", cfg) == "unknown"


class TestAggregation:
    """Aggregation math + structure."""

    def _cfg(self):
        return {
            "clients": {"cuidai": {}, "atrium": {}},
            "dev": {"audit": {}, "refactor": {}},
            "default_for_unmapped": "unknown",
        }

    def test_empty_yaml_returns_zero_total(self):
        agg = aggregate_month({}, self._cfg())
        assert agg["total_tokens"] == 0
        assert agg["by_type"] == {}
        assert agg["breakdown"] == []

    def test_all_client_spend(self):
        data = {"month": "2026-05", "by_project": {"cuidai": 1000, "atrium": 500}}
        agg = aggregate_month(data, self._cfg())
        assert agg["total_tokens"] == 1500
        assert agg["by_type"]["client"] == 1500
        assert "dev" not in agg["by_type"]
        assert agg["percentages_by_type"]["client"] == 100.0

    def test_mixed_types(self):
        data = {"month": "2026-05", "by_project": {
            "cuidai": 800, "audit": 100, "unknown-thing": 100,
        }}
        agg = aggregate_month(data, self._cfg())
        assert agg["total_tokens"] == 1000
        assert agg["by_type"]["client"] == 800
        assert agg["by_type"]["dev"] == 100
        assert agg["by_type"]["unknown"] == 100
        assert agg["percentages_by_type"]["client"] == 80.0
        assert agg["percentages_by_type"]["dev"] == 10.0
        assert agg["percentages_by_type"]["unknown"] == 10.0

    def test_breakdown_sorted_descending(self):
        data = {"month": "2026-05", "by_project": {
            "cuidai": 100, "atrium": 500, "audit": 50,
        }}
        agg = aggregate_month(data, self._cfg())
        tokens_seq = [r["tokens"] for r in agg["breakdown"]]
        assert tokens_seq == sorted(tokens_seq, reverse=True)
        assert agg["breakdown"][0]["project"] == "atrium"

    def test_non_numeric_tokens_ignored(self):
        data = {"month": "2026-05", "by_project": {
            "cuidai": 1000, "bad-row": "not a number", "atrium": 500,
        }}
        agg = aggregate_month(data, self._cfg())
        assert agg["total_tokens"] == 1500  # bad-row excluded silently

    def test_blank_project_treated_as_unknown(self):
        data = {"month": "2026-05", "by_project": {"": 200, "cuidai": 800}}
        agg = aggregate_month(data, self._cfg())
        assert agg["by_type"]["unknown"] == 200
        assert agg["by_type"]["client"] == 800


class TestLiveBudgetBreakdown:
    """Run against actual current-month budget if it exists."""

    def test_live_breakdown_runs(self):
        """Smoke test that real classification doesn't crash."""
        from datetime import UTC, datetime

        from scripts.budget_breakdown_by_type import load_budget_file
        month = datetime.now(UTC).strftime("%Y-%m")
        path = ORCH_DIR / "budgets" / f"{month}.yaml"
        if not path.exists():
            pytest.skip(f"No budget for {month}")
        cfg = load_types_config()
        data = load_budget_file(path)
        agg = aggregate_month(data, cfg)
        assert agg["total_tokens"] >= 0
        assert isinstance(agg["by_type"], dict)
