"""Anthropic SDK spend wrapper — closes the visibility gap for direct API calls.

Problem this solves:
    Claude Code interactive sessions run on the Max subscription (no
    per-token cost). But ANY Python script that does
    `anthropic.Anthropic().messages.create(...)` hits the API directly
    and gets billed. These calls were invisible to the dashboard —
    spent ~$15 in one session on DSPy training without realizing it
    until checking later.

What this wrapper does:
    Wraps `anthropic.Anthropic` so every `messages.create()` call is
    persisted to a shared yaml log with token counts + USD estimate +
    caller + timestamp. The aggregator + dashboard widget read this log
    to surface "direct script spend" alongside the orchestrator-tracked
    budget.

Usage (replace `Anthropic()` with `TrackedAnthropic()`):

    # Before:
    from anthropic import Anthropic
    client = Anthropic()
    resp = client.messages.create(...)

    # After:
    from scripts.anthropic_spend_wrapper import TrackedAnthropic
    client = TrackedAnthropic(caller="dspy/compile_sprint4")
    resp = client.messages.create(...)

The wrapper is fully API-compatible — every other call passes through
to the real client unchanged.

Pricing source: Anthropic public pricing as of 2026-05.
Update PRICING dict when prices change.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None  # type: ignore

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
SPEND_LOG = ORCH_DIR / "quality" / "api_spend_log.yaml"

# USD per million tokens — update when Anthropic changes pricing.
# Source: anthropic.com/pricing (verified 2026-05).
PRICING = {
    "claude-opus-4-7":           {"input": 5.00, "output": 25.00},
    "claude-opus-4-6":           {"input": 5.00, "output": 25.00},
    "claude-opus-4-5":           {"input": 5.00, "output": 25.00},
    "claude-opus-4":             {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6":         {"input": 3.00, "output": 15.00},
    "claude-sonnet-4-5":         {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5":          {"input": 0.80, "output": 4.00},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "claude-3-opus-20240229":    {"input": 15.00, "output": 75.00},
    "claude-3-sonnet-20240229":  {"input": 3.00, "output": 15.00},
    "claude-3-haiku-20240307":   {"input": 0.25, "output": 1.25},
}

DEFAULT_PRICING = {"input": 3.00, "output": 15.00}  # Sonnet-like fallback


def estimate_cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate USD cost for an API call. Uses fallback price if model unknown."""
    pricing = PRICING.get(model, DEFAULT_PRICING)
    cost = (input_tokens / 1_000_000) * pricing["input"] + \
           (output_tokens / 1_000_000) * pricing["output"]
    return round(cost, 6)


SPEND_JSONL = ORCH_DIR / "quality" / "api_spend_log.jsonl"


def _append_entry(entry: dict) -> None:
    """Append one spend entry — concurrent-safe via JSONL append + file lock.

    Migrated from full-file YAML rewrite (O(n) + race condition) to JSONL
    append (O(1) + atomic). Legacy YAML still updated for backward compat
    until aggregator is switched.
    """
    import json
    import os
    SPEND_JSONL.parent.mkdir(parents=True, exist_ok=True)

    # Primary write: JSONL append-only, single open(..., "a") is atomic
    # on POSIX for writes <PIPE_BUF (~4KB); JSON entries fit comfortably.
    with open(SPEND_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        try:
            os.fsync(f.fileno())  # durability on crash
        except (AttributeError, OSError):
            pass

    # Legacy YAML write — guarded by a simple lock file to prevent race.
    # TODO: deprecate YAML once aggregator reads JSONL natively.
    lock_path = SPEND_LOG.with_suffix(".yaml.lock")
    acquired = False
    try:
        # Best-effort lock (atomic O_CREAT|O_EXCL); silently skip YAML write
        # if another writer holds it. Entries are still safe in JSONL.
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            acquired = True
        except FileExistsError:
            return  # JSONL already captured it; skip the redundant YAML write

        existing: dict = {}
        if SPEND_LOG.exists():
            with open(SPEND_LOG, encoding="utf-8") as f:
                existing = yaml.safe_load(f) or {}
        existing.setdefault("schema_version", 1)
        existing.setdefault("description",
            "Direct Anthropic API spend log (scripts only, NOT orchestrator subscription work). "
            "Append-only — every TrackedAnthropic.messages.create() writes one row. "
            "Primary source of truth is api_spend_log.jsonl; this YAML is a legacy mirror."
        )
        existing.setdefault("entries", [])
        existing["entries"].append(entry)
        with open(SPEND_LOG, "w", encoding="utf-8") as f:
            yaml.safe_dump(existing, f, sort_keys=False, allow_unicode=True)
    finally:
        if acquired:
            try:
                lock_path.unlink()
            except OSError:
                pass


class _TrackedMessages:
    """Proxy that wraps client.messages and logs each create() call."""

    def __init__(self, real_messages, caller: str):
        self._real = real_messages
        self._caller = caller

    def create(self, *args, **kwargs):
        resp = self._real.create(*args, **kwargs)

        try:
            model = kwargs.get("model") or "unknown"
            usage = getattr(resp, "usage", None)
            input_tokens = getattr(usage, "input_tokens", 0) if usage else 0
            output_tokens = getattr(usage, "output_tokens", 0) if usage else 0
            cost = estimate_cost_usd(model, input_tokens, output_tokens)
            entry = {
                "ts": datetime.now(UTC).isoformat(timespec="seconds"),
                "caller": self._caller,
                "model": model,
                "input_tokens": int(input_tokens),
                "output_tokens": int(output_tokens),
                "total_tokens": int(input_tokens) + int(output_tokens),
                "cost_usd": cost,
            }
            _append_entry(entry)
        except Exception as e:
            # Never let logging break the actual API response
            print(f"[anthropic_spend_wrapper] log write failed: {e}",
                  file=sys.stderr)

        return resp

    def __getattr__(self, name):
        # Pass through anything we didn't explicitly wrap
        return getattr(self._real, name)


class TrackedAnthropic:
    """Drop-in replacement for anthropic.Anthropic with spend logging.

    All non-messages attributes pass through unchanged. The messages
    proxy intercepts create() to log tokens + cost estimate.

    Args:
        caller: identifier for the calling script/module (e.g.
                "dspy/compile_sprint4" or "scoring/judge"). Required
                for traceability — appears in every log entry.
        **kwargs: forwarded to anthropic.Anthropic()
    """

    def __init__(self, caller: str, **kwargs: Any):
        if Anthropic is None:
            raise ImportError(
                "anthropic package not installed. "
                "Run: pip install anthropic"
            )
        if not caller or not isinstance(caller, str):
            raise ValueError("caller must be a non-empty string")
        self._caller = caller
        self._real = Anthropic(**kwargs)
        self.messages = _TrackedMessages(self._real.messages, caller)

    def __getattr__(self, name):
        return getattr(self._real, name)
