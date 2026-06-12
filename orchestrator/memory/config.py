"""Single source of memory/dream tunables (DD finding A13, 2026-06-12).

Defaults below are calibrated for the current volume (~150 real episodes,
few runs per skill). Override any key via config/memory_dream.yaml.
"""

from __future__ import annotations

from pathlib import Path

import yaml

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
CONFIG_FILE = ORCH_DIR / "config" / "memory_dream.yaml"

DEFAULTS: dict[str, float | int] = {
    # ── Confidence decay (semantic memories) ──
    "decay_half_life_days": 60.0,      # confidence halves every N days without retrieval
    "decay_retrieval_bonus": 0.5,      # each retrieval extends half-life by this fraction
    "decay_retrieval_bonus_cap": 10,   # retrievals counted toward the bonus (cap)
    "decay_prune_floor": 0.15,         # below this effective confidence → prune candidate
    # ── Pattern detection / convergence ──
    "convergence_min_sessions": 2,     # was 3 — never fired at current volume
    "convergence_min_score": 60.0,     # was 70 — killed legitimate convergences
    "pattern_trend_min_runs": 3,       # was 4 — runs of same skill for trend detection
    "pattern_failure_min": 2,          # was 3 — repeated failures worth surfacing
    # ── Dream cycle ──
    "dream_window_days": 14,           # was 7 — wider window ≈ 15-20 episodes today
}


def _load() -> dict:
    cfg = dict(DEFAULTS)
    try:
        if CONFIG_FILE.exists():
            data = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
            for key in DEFAULTS:
                if key in data and data[key] is not None:
                    cfg[key] = data[key]
    except Exception:
        pass  # malformed config file → fall back to defaults
    return cfg


_CFG = _load()


def get(key: str):
    """Return a tunable by key (falls back to DEFAULTS for unknown state)."""
    return _CFG.get(key, DEFAULTS[key])
