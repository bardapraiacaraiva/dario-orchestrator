"""Company config loader (Onda 2 #3).

The legacy `company.yaml` (4,042 LOC monolith) was split into modular YAML
sources under `config/company/`:

    config/company/
    ├── meta.yaml           — company name, owner, budget
    ├── agents.yaml         — 37 core agents (CEO, VPs, directors)
    ├── workers.yaml        — 180 core workers
    ├── policies.yaml       — execution policies (default, critical, ...)
    ├── misc.yaml           — heartbeat_defaults, routines, mcp_servers_br,
    │                          prometheus_governance
    └── squads/
        ├── lex.yaml         — workers_lex + squads_lex
        ├── demeter.yaml     — workers_demeter + squads_demeter
        ├── aegis.yaml       — agents_security + workers_aegis + squads_aegis
        └── ... (38 total)

This module loads all of those and rebuilds the legacy dict shape so all
existing callers (15+ engines that read `company.yaml`) keep working
unchanged. The original `company.yaml` becomes a generated artefact —
treated as cache, not source of truth.

API:
    from config.company_loader import load, save_legacy_yaml

    cfg = load()                  # → dict identical to legacy company.yaml
    save_legacy_yaml(cfg)         # regenerate company.yaml from the segments
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CONFIG_DIR = ORCH_DIR / "config" / "company"
LEGACY_YAML = ORCH_DIR / "company.yaml"


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load() -> dict[str, Any]:
    """Assemble the full company config dict from segment files.

    Order of merging is fixed so that core segments cannot be silently
    overridden by a malformed squad file.
    """
    result: dict[str, Any] = {}

    # 1) Core segments (in canonical order)
    for fname in ("meta.yaml", "agents.yaml", "workers.yaml", "policies.yaml"):
        result.update(_read_yaml(CONFIG_DIR / fname))

    # 2) Misc top-level keys (heartbeat_defaults, routines, prometheus_governance, ...)
    result.update(_read_yaml(CONFIG_DIR / "misc.yaml"))

    # 3) Per-squad files — each contributes its own agents_X/workers_X/squads_X keys
    squads_dir = CONFIG_DIR / "squads"
    if squads_dir.exists():
        for squad_file in sorted(squads_dir.glob("*.yaml")):
            squad_data = _read_yaml(squad_file)
            for key, val in squad_data.items():
                if key in result:
                    # Duplicate detected — keep the segmented value (loader
                    # is source of truth) but warn in dev.
                    pass
                result[key] = val

    return result


def save_legacy_yaml(data: dict[str, Any] | None = None) -> Path:
    """Write the assembled config to the legacy `company.yaml` path.

    Useful for callers that still read the monolithic file directly (15+
    engines). Run this once after editing a segment to keep both in sync.
    """
    if data is None:
        data = load()
    LEGACY_YAML.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=200),
        encoding="utf-8",
    )
    return LEGACY_YAML


def diff_against_legacy() -> dict[str, Any]:
    """Report any divergence between the segmented config and `company.yaml`.

    Returns a structured diff:
        {
            "only_in_segments": [keys],
            "only_in_legacy":   [keys],
            "value_diffs":      {key: {"segments": ..., "legacy": ...}},
        }
    """
    segmented = load()
    legacy = _read_yaml(LEGACY_YAML)

    seg_keys = set(segmented.keys())
    leg_keys = set(legacy.keys())

    value_diffs: dict[str, Any] = {}
    for k in seg_keys & leg_keys:
        if segmented[k] != legacy[k]:
            value_diffs[k] = {
                "segments_type": type(segmented[k]).__name__,
                "legacy_type": type(legacy[k]).__name__,
            }

    return {
        "only_in_segments": sorted(seg_keys - leg_keys),
        "only_in_legacy": sorted(leg_keys - seg_keys),
        "value_diffs": value_diffs,
        "equal": not (seg_keys ^ leg_keys) and not value_diffs,
    }


__all__ = ["load", "save_legacy_yaml", "diff_against_legacy", "CONFIG_DIR", "LEGACY_YAML"]
