"""Tests for memory_contradiction_detector (Risk #9 partial fix)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from scripts.memory_contradiction_detector import (
    IGNORE_LABELS,
    SKIP_LINE_RE,
    detect_contradictions,
    normalize_label,
    parse_value,
    scan_file,
)


class TestLabelNormalization:

    def test_lowercase(self):
        assert normalize_label("DeliveryRate") == "deliveryrate"

    def test_strip_whitespace(self):
        assert normalize_label("  delivery rate  ") == "delivery_rate"

    def test_internal_spaces_to_underscore(self):
        assert normalize_label("delivery rate per skill") == "delivery_rate_per_skill"


class TestParseValue:

    def test_plain_int(self):
        assert parse_value("80", "") == 80.0

    def test_with_comma(self):
        assert parse_value("1,500", "") == 1500.0

    def test_with_percent_unit(self):
        assert parse_value("85", "%") == 85.0

    def test_with_k_unit(self):
        assert parse_value("2", "K") == 2000.0
        assert parse_value("2", "k") == 2000.0

    def test_with_m_unit(self):
        assert parse_value("5", "M") == 5_000_000.0

    def test_unparseable_returns_none(self):
        assert parse_value("abc", "") is None
        assert parse_value("", "") is None


class TestSkipPatterns:

    @pytest.mark.parametrize("text", [
        "originSessionId: 0a3e122c-3078-4b4e-abb2-66396fe81f16",
        "Hash: sha256:abc123",
        "Commit HEAD a1c3717 deployed",
        "---",
    ])
    def test_skip_line_matches(self, text):
        assert SKIP_LINE_RE.search(text)

    @pytest.mark.parametrize("text", [
        "Score: 80/100",
        "Delivery rate: 50%",
        "Total clients: 5",
    ])
    def test_skip_line_does_not_match_normal(self, text):
        assert not SKIP_LINE_RE.search(text)


class TestScanFile:

    def test_extracts_labeled_numbers(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "# Test\n"
            "delivery_rate: 50%\n"
            "users: 1,500\n"
            "score = 87\n",
            encoding="utf-8",
        )
        findings = scan_file(f)
        labels = [f["label"] for f in findings]
        assert "delivery_rate" in labels
        assert "users" in labels

    def test_skips_frontmatter(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "---\n"
            "originSessionId: 0a3e122c-3078\n"
            "delivery_rate: 99\n"  # in frontmatter, should be ignored
            "---\n"
            "# Body\n"
            "delivery_rate: 50\n",  # in body, should be captured
            encoding="utf-8",
        )
        findings = scan_file(f)
        delivery_values = [f["value"] for f in findings if f["label"] == "delivery_rate"]
        assert 50.0 in delivery_values, f"Body value not captured: {delivery_values}"
        assert 99.0 not in delivery_values, "Frontmatter value should be skipped"

    def test_skips_uuid_lines(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "Session: 0a3e122c-3078-4b4e-abb2-66396fe81f16, count: 80\n",
            encoding="utf-8",
        )
        findings = scan_file(f)
        # The whole line should be skipped because of UUID
        assert all(f["label"] != "count" for f in findings)

    def test_ignores_blacklisted_labels(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "total: 1000\n"      # 'total' is in IGNORE_LABELS
            "antes: 50\n"        # ditto
            "real_metric: 80\n", # this one should pass
            encoding="utf-8",
        )
        findings = scan_file(f)
        labels = [f["label"] for f in findings]
        assert "total" not in labels
        assert "antes" not in labels
        assert "real_metric" in labels


class TestDetectContradictions:

    def _findings(self, *triples):
        """Helper: build findings list from (file, label, value) triples."""
        return [
            {"file": f, "line": i, "label": label, "value": v,
             "unit": "", "raw_line": f"{label}: {v}"}
            for i, (f, label, v) in enumerate(triples, 1)
        ]

    def test_no_contradiction_with_same_value(self):
        findings = self._findings(
            ("a.md", "users", 100),
            ("b.md", "users", 100),
        )
        assert detect_contradictions(findings, 0.25) == []

    def test_contradiction_above_threshold(self):
        findings = self._findings(
            ("a.md", "users", 100),
            ("b.md", "users", 200),  # 50% divergence
        )
        result = detect_contradictions(findings, 0.25)
        assert len(result) == 1
        assert result[0]["label"] == "users"
        assert result[0]["divergence"] == 0.5

    def test_no_contradiction_below_threshold(self):
        findings = self._findings(
            ("a.md", "users", 100),
            ("b.md", "users", 110),  # 9% divergence
        )
        assert detect_contradictions(findings, 0.25) == []

    def test_single_occurrence_not_flagged(self):
        findings = self._findings(("a.md", "users", 100))
        assert detect_contradictions(findings, 0.25) == []

    def test_same_file_not_flagged(self):
        """Multiple values in same file are likely intentional time-series."""
        findings = self._findings(
            ("a.md", "users", 100),
            ("a.md", "users", 200),
        )
        assert detect_contradictions(findings, 0.25) == []

    def test_results_sorted_by_divergence(self):
        findings = self._findings(
            ("a.md", "metric_a", 100), ("b.md", "metric_a", 150),  # 33%
            ("c.md", "metric_b", 100), ("d.md", "metric_b", 500),  # 80%
        )
        result = detect_contradictions(findings, 0.25)
        assert result[0]["divergence"] > result[1]["divergence"]


class TestLiveScan:
    """Smoke test against the actual memory dir — no assertions about
    specific contradictions (those drift over time), just that the
    detector runs cleanly."""

    def test_runs_without_crashing(self):
        from scripts.memory_contradiction_detector import MEMORY_DIR_CANDIDATES
        valid_dirs = [d for d in MEMORY_DIR_CANDIDATES if d.exists()]
        if not valid_dirs:
            pytest.skip("No memory dir found")

        all_findings = []
        files_seen = 0
        for d in valid_dirs:
            for f in d.glob("*.md"):
                if f.name == "MEMORY.md":
                    continue
                all_findings.extend(scan_file(f))
                files_seen += 1

        assert files_seen > 0
        # Just check the detector returns a list, doesn't crash
        result = detect_contradictions(all_findings, threshold=0.5)
        assert isinstance(result, list)
