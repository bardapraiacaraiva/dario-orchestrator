"""Tests for Onda 2 #3 — segmented company config loader."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

from config.company_loader import (
    CONFIG_DIR,
    diff_against_legacy,
    load,
    save_legacy_yaml,
)


class TestLoaderRoundTrip:
    """The whole point: assembled config must equal the legacy monolith."""

    def test_loader_matches_legacy_yaml(self):
        diff = diff_against_legacy()
        assert diff["equal"] is True, (
            f"Segments diverge from legacy. "
            f"only_in_segments={diff['only_in_segments']} "
            f"only_in_legacy={diff['only_in_legacy']} "
            f"value_diffs={list(diff['value_diffs'].keys())}"
        )

    def test_core_sections_present(self):
        cfg = load()
        assert "company" in cfg
        assert "agents" in cfg
        assert "workers" in cfg
        assert "execution_policies" in cfg

    def test_at_least_180_workers(self):
        cfg = load()
        assert len(cfg.get("workers", {})) >= 180

    def test_at_least_37_agents(self):
        cfg = load()
        assert len(cfg.get("agents", {})) >= 37

    def test_squad_files_contribute_keys(self):
        """Each squad/<id>.yaml must add at least one top-level key (agents_X / workers_X / squads_X)."""
        cfg = load()
        # Kept squads (industry squads demeter/aegis/etc archived 2026-06-01 — see VERTICALS_ARCHIVE.md)
        expected_squad_prefixes = ["workers_lex", "workers_nomos", "workers_obsidian"]
        for k in expected_squad_prefixes:
            assert k in cfg, f"missing squad key from segments: {k}"


class TestSegmentFiles:
    """Each segment must be valid YAML on its own."""

    def test_meta_segment_loadable(self):
        data = yaml.safe_load((CONFIG_DIR / "meta.yaml").read_text(encoding="utf-8"))
        assert "company" in data

    def test_agents_segment_loadable(self):
        data = yaml.safe_load((CONFIG_DIR / "agents.yaml").read_text(encoding="utf-8"))
        assert "agents" in data
        assert len(data["agents"]) >= 37

    def test_workers_segment_loadable(self):
        data = yaml.safe_load((CONFIG_DIR / "workers.yaml").read_text(encoding="utf-8"))
        assert "workers" in data
        assert len(data["workers"]) >= 180

    def test_policies_segment_loadable(self):
        data = yaml.safe_load((CONFIG_DIR / "policies.yaml").read_text(encoding="utf-8"))
        assert "execution_policies" in data

    def test_all_squad_files_are_valid_yaml(self):
        squads_dir = CONFIG_DIR / "squads"
        bad = []
        for fp in squads_dir.glob("*.yaml"):
            try:
                yaml.safe_load(fp.read_text(encoding="utf-8"))
            except yaml.YAMLError as e:
                bad.append((fp.name, str(e)[:80]))
        assert not bad, f"invalid squad YAMLs: {bad}"

    def test_at_least_10_squad_files(self):
        # Floor lowered 15->10 after archiving 13 industry squads (26 files)
        # on 2026-06-01 — see orchestrator/VERTICALS_ARCHIVE.md.
        squads_dir = CONFIG_DIR / "squads"
        files = list(squads_dir.glob("*.yaml"))
        assert len(files) >= 10, f"only {len(files)} squad files — expected 10+"


class TestRegeneration:
    """save_legacy_yaml() must produce a file that re-loads equal to the segments."""

    def test_save_and_reload(self, tmp_path, monkeypatch):
        # Re-target LEGACY_YAML to a temp path to avoid clobbering production
        from config import company_loader

        fake_legacy = tmp_path / "company.yaml"
        monkeypatch.setattr(company_loader, "LEGACY_YAML", fake_legacy)

        save_legacy_yaml()  # writes to fake_legacy
        assert fake_legacy.exists()

        reloaded = yaml.safe_load(fake_legacy.read_text(encoding="utf-8"))
        assert reloaded == load()
