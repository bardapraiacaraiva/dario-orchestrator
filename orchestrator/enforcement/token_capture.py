"""Token capture from SubagentStop hook events.

Closes the honor-system gap where Agent tool token usage was never measured —
only guessed by close_*.py scripts with hardcoded values.

Flow:
  1. SubagentStop hook fires with JSON payload on stdin
  2. Read transcript JSONL, find sidechain messages newer than last capture
  3. Sum usage tokens (input + output + cache_creation + cache_read)
  4. Best-effort attribute to a task_id (parsed from sidechain prompt)
  5. Append run record to subagent_runs/YYYY-MM/<session>-<ts>.json
  6. Update state file to advance last_capture_ts

Idempotent: re-running on the same transcript with the same state file
will not double-count (uses timestamp-based dedup).
Non-raising: hook must never block Claude Code; errors logged to stderr only.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
RUNS_DIR = ORCH_DIR / "subagent_runs"
STATE_FILE = ORCH_DIR / "state" / "last_subagent_capture.json"
DEBUG_LOG = ORCH_DIR / "state" / "token_capture_debug.jsonl"

# Pricing per million tokens (Anthropic public pricing, verified 2026-05).
# Mirrored from scripts/anthropic_spend_wrapper.py to avoid import cycle.
PRICING_PER_M = {
    "claude-opus-4-7":   {"input": 5.00, "output": 25.00, "cache_write": 6.25, "cache_read": 0.50},
    "claude-opus-4-6":   {"input": 5.00, "output": 25.00, "cache_write": 6.25, "cache_read": 0.50},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00, "cache_write": 3.75, "cache_read": 0.30},
    "claude-haiku-4-5":  {"input": 0.80, "output": 4.00,  "cache_write": 1.00, "cache_read": 0.08},
}
DEFAULT_PRICING = {"input": 5.00, "output": 25.00, "cache_write": 6.25, "cache_read": 0.50}

TASK_ID_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,9}-\d{3,4})\b")
# Prefixes that match the pattern but are NOT task IDs.
TASK_ID_BLOCKLIST = frozenset({
    # Standards / regulations
    "CVE", "ISO", "RFC", "SOC", "NIST", "OWASP", "GDPR", "LGPD",
    "PCI", "HIPAA", "ARI", "IRC", "IRS", "TUSS", "PT", "EU", "DL",
    # Crypto / network
    "AES", "RSA", "SHA", "MD5", "TLS", "SSL", "HTTP", "HTTPS", "TCP", "UDP",
    "IPV4", "IPV6", "DNS", "API", "SDK", "JWT", "OAUTH",
    # HTTP status / common 3-letter
    "NON", "GET", "PUT",
    # Currency / dates / quarters
    "USD", "EUR", "BRL", "GBP", "JPY",
    "Q1", "Q2", "Q3", "Q4", "H1", "H2",
    # Pricing/SaaS noise
    "MRR", "ARR", "ARPU", "LTV", "CAC", "ROI", "TAM", "SAM", "SOM",
    # Common legal/financial
    "NDA", "MOU", "SLA", "KPI", "OKR",
})


def _stderr(msg: str) -> None:
    """Hook output goes to stderr so it never contaminates stdout."""
    print(f"[token_capture] {msg}", file=sys.stderr)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def load_state() -> dict:
    """Read state file or return defaults. Never raises."""
    if not STATE_FILE.exists():
        return {"last_capture_ts": None, "captured_uuids": []}
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        _stderr(f"state load failed ({e}); using defaults")
        return {"last_capture_ts": None, "captured_uuids": []}


def save_state(state: dict) -> None:
    """Persist state file. Truncates captured_uuids to last 200k to bound size."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["captured_uuids"] = state.get("captured_uuids", [])[-200_000:]
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def _resolve_transcript_files(transcript_path: Path) -> list[Path]:
    """Given a path from the hook payload, return all files to scan.

    Claude Code stores subagent transcripts in two places depending on context:
      - <session-uuid>.jsonl                          (main session transcript)
      - <session-uuid>/subagents/agent-<id>.jsonl     (per-subagent transcripts)

    The SubagentStop hook's transcript_path may point to either. To be robust
    we accept both layouts:
      - If main file: also scan sibling <session>/subagents/*.jsonl
      - If per-agent file: just scan it directly
      - If a directory: scan all .jsonl inside (recursive 1 level)
    """
    if not transcript_path.exists():
        return []

    files: list[Path] = []
    if transcript_path.is_file():
        files.append(transcript_path)
        # Sibling subagents/ directory (main transcript case)
        stem = transcript_path.stem
        parent = transcript_path.parent
        sibling_dir = parent / stem / "subagents"
        if sibling_dir.is_dir():
            files.extend(sorted(sibling_dir.glob("agent-*.jsonl")))
    elif transcript_path.is_dir():
        files.extend(sorted(transcript_path.glob("*.jsonl")))
        sub = transcript_path / "subagents"
        if sub.is_dir():
            files.extend(sorted(sub.glob("agent-*.jsonl")))
    return files


def parse_transcript_sidechains(transcript_path: Path, since_ts: str | None,
                                 seen_uuids: set[str]) -> list[dict]:
    """Return all sidechain assistant messages with usage data not yet captured.

    Filters:
      - isSidechain == true
      - message.usage present
      - uuid not in seen_uuids
      - timestamp > since_ts (if provided)

    Scans both the main transcript and any sibling subagents/agent-*.jsonl files.
    """
    files = _resolve_transcript_files(transcript_path)
    if not files:
        return []

    messages: list[dict] = []
    for fp in files:
        try:
            with open(fp, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if not obj.get("isSidechain"):
                        continue
                    msg = obj.get("message")
                    if not isinstance(msg, dict):
                        continue
                    usage = msg.get("usage")
                    if not isinstance(usage, dict):
                        continue
                    uuid = obj.get("uuid")
                    if uuid and uuid in seen_uuids:
                        continue
                    ts = obj.get("timestamp")
                    if since_ts and ts and ts <= since_ts:
                        continue
                    messages.append({
                        "uuid": uuid,
                        "timestamp": ts,
                        "model": msg.get("model", "unknown"),
                        "usage": usage,
                        "session_id": obj.get("sessionId"),
                        "agent_id": obj.get("agentId"),
                        "source_file": str(fp),
                        "content_preview": _extract_text_preview(msg.get("content")),
                    })
        except OSError:
            continue
    # Deterministic order by timestamp for downstream consumers
    messages.sort(key=lambda m: m.get("timestamp") or "")
    return messages


def _extract_text_preview(content) -> str:
    """Extract a short text preview from message content (for task_id parsing)."""
    if not isinstance(content, list):
        return ""
    parts = []
    for block in content:
        if isinstance(block, dict):
            if block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                inp = block.get("input")
                if isinstance(inp, dict):
                    parts.append(json.dumps(inp)[:500])
    return " ".join(parts)[:2000]


def aggregate_usage(messages: list[dict]) -> dict:
    """Sum usage across a list of sidechain messages.

    Returns dict with totals + per-model breakdown.
    """
    totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "total_tokens": 0,
        "by_model": {},
        "cost_usd": 0.0,
        "message_count": len(messages),
    }
    for m in messages:
        u = m["usage"]
        model = m["model"]
        i = int(u.get("input_tokens") or 0)
        o = int(u.get("output_tokens") or 0)
        cc = int(u.get("cache_creation_input_tokens") or 0)
        cr = int(u.get("cache_read_input_tokens") or 0)

        totals["input_tokens"] += i
        totals["output_tokens"] += o
        totals["cache_creation_input_tokens"] += cc
        totals["cache_read_input_tokens"] += cr

        model_totals = totals["by_model"].setdefault(model, {
            "input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "cost_usd": 0.0,
        })
        model_totals["input"] += i
        model_totals["output"] += o
        model_totals["cache_write"] += cc
        model_totals["cache_read"] += cr

        pricing = PRICING_PER_M.get(model, DEFAULT_PRICING)
        cost = (
            (i / 1_000_000) * pricing["input"]
            + (o / 1_000_000) * pricing["output"]
            + (cc / 1_000_000) * pricing["cache_write"]
            + (cr / 1_000_000) * pricing["cache_read"]
        )
        model_totals["cost_usd"] = round(model_totals["cost_usd"] + cost, 6)
        totals["cost_usd"] = round(totals["cost_usd"] + cost, 6)

    # cache_read EXCLUDED from the budget figure: at $0.50/M vs $5.00/M input it
    # is ~10% of the cost but dominates raw volume (one review run read 13.1M
    # cached tokens → 30% of the monthly budget if counted 1:1). Cost stays
    # exact in cost_usd; raw volume stays visible in the breakdown.
    totals["total_tokens"] = (
        totals["input_tokens"]
        + totals["output_tokens"]
        + totals["cache_creation_input_tokens"]
    )
    return totals


def find_task_id(messages: list[dict]) -> str | None:
    """Best-effort extract TASK-ID like CUI-005 from sidechain content.

    Returns first match found. Orchestrator dispatch prompts should embed
    [TASK_ID:XXX-NNN] explicitly; pattern also matches bare CUI-005 style.
    """
    for m in messages:
        text = m.get("content_preview", "")
        explicit = re.search(r"\[TASK_ID:([A-Z][A-Z0-9]{1,9}-\d{3,4})\]", text)
        if explicit:
            return explicit.group(1)
    for m in messages:
        text = m.get("content_preview", "")
        for match in TASK_ID_RE.finditer(text):
            candidate = match.group(1)
            prefix = candidate.split("-", 1)[0]
            if prefix in TASK_ID_BLOCKLIST:
                continue
            return candidate
    return None


def write_run_record(payload: dict, messages: list[dict], totals: dict,
                     task_id: str | None) -> Path | None:
    """Append a run record to subagent_runs/YYYY-MM/SESSION-TS.json.

    Returns path written, or None if no messages.
    """
    if not messages:
        return None

    session_id = payload.get("session_id") or "unknown"
    ts = _now_iso()
    month_dir = RUNS_DIR / ts[:7]
    month_dir.mkdir(parents=True, exist_ok=True)
    safe_ts = ts.replace(":", "-").replace("+00:00", "Z")
    out_path = month_dir / f"{session_id[:8]}-{safe_ts}.json"

    record = {
        "captured_at": ts,
        "session_id": session_id,
        "transcript_path": payload.get("transcript_path"),
        "task_id": task_id,
        "message_count": len(messages),
        "first_message_ts": messages[0].get("timestamp"),
        "last_message_ts": messages[-1].get("timestamp"),
        "totals": totals,
        "uuids": [m.get("uuid") for m in messages if m.get("uuid")],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return out_path


def update_task_yaml(task_id: str, totals: dict) -> bool:
    """Set actual_tokens on a task YAML if found in active/ or done/.

    Uses additive update — if task already has actual_tokens, we add to it.
    Returns True if file updated.
    """
    try:
        import yaml
    except ImportError:
        _stderr("PyYAML not available; skipping task YAML update")
        return False

    for subdir in ("active", "done"):
        candidate = ORCH_DIR / "tasks" / subdir / f"{task_id}.yaml"
        if not candidate.exists():
            continue
        try:
            with open(candidate, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            previous = int(data.get("actual_tokens") or 0)
            data["actual_tokens"] = previous + totals["total_tokens"]
            data["actual_tokens_breakdown"] = {
                "input": data.get("actual_tokens_breakdown", {}).get("input", 0) + totals["input_tokens"],
                "output": data.get("actual_tokens_breakdown", {}).get("output", 0) + totals["output_tokens"],
                "cache_write": data.get("actual_tokens_breakdown", {}).get("cache_write", 0) + totals["cache_creation_input_tokens"],
                "cache_read": data.get("actual_tokens_breakdown", {}).get("cache_read", 0) + totals["cache_read_input_tokens"],
            }
            data["actual_cost_usd"] = round(
                float(data.get("actual_cost_usd") or 0) + totals["cost_usd"], 6
            )
            data["token_capture_source"] = "subagent_stop_hook"
            data["last_token_capture_at"] = _now_iso()
            with open(candidate, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
            return True
        except (OSError, Exception) as e:  # noqa: BLE001
            _stderr(f"failed to update {candidate}: {e}")
            return False
    return False


def capture(payload: dict) -> dict:
    """Main capture pipeline. Returns result summary (never raises).

    Result dict keys: status, messages_captured, total_tokens, task_id, run_path
    """
    result = {
        "status": "noop",
        "messages_captured": 0,
        "total_tokens": 0,
        "task_id": None,
        "run_path": None,
    }

    transcript_path = payload.get("transcript_path")
    if not transcript_path:
        result["status"] = "no_transcript_path"
        return result

    tp = Path(transcript_path)
    if not tp.exists():
        result["status"] = "transcript_missing"
        return result

    state = load_state()
    seen = set(state.get("captured_uuids", []))
    # Dedup via UUID set only; timestamp filter would wrongly skip older sessions
    # processed AFTER newer ones (e.g. during backfill).
    messages = parse_transcript_sidechains(tp, None, seen)
    if not messages:
        result["status"] = "no_new_sidechain_messages"
        return result

    totals = aggregate_usage(messages)
    task_id = find_task_id(messages)
    run_path = write_run_record(payload, messages, totals, task_id)

    if task_id:
        update_task_yaml(task_id, totals)

    new_seen = seen | {m["uuid"] for m in messages if m.get("uuid")}
    prior_ts = state.get("last_capture_ts")
    latest_ts = max((m["timestamp"] for m in messages if m.get("timestamp")), default=prior_ts)
    save_state({"last_capture_ts": latest_ts, "captured_uuids": list(new_seen)})

    result.update({
        "status": "captured",
        "messages_captured": len(messages),
        "total_tokens": totals["total_tokens"],
        "cost_usd": totals["cost_usd"],
        "task_id": task_id,
        "run_path": str(run_path) if run_path else None,
    })
    return result


def _debug_log(payload: dict, result: dict) -> None:
    """Append debug entry — useful while validating in production."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": _now_iso(),
                "payload_keys": list(payload.keys()),
                "session_id": payload.get("session_id"),
                "result": result,
            }) + "\n")
    except OSError:
        pass


def main() -> int:
    """Hook entrypoint. Never raises — returns 0 always to not block Claude Code."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError) as e:
        _stderr(f"stdin parse failed: {e}")
        return 0

    try:
        result = capture(payload)
        _debug_log(payload, result)
        if result["status"] == "captured":
            _stderr(
                f"captured {result['messages_captured']} msgs, "
                f"{result['total_tokens']} tokens, "
                f"${result['cost_usd']:.4f}, "
                f"task={result['task_id'] or 'unattributed'}"
            )
    except Exception as e:  # noqa: BLE001
        _stderr(f"capture failed: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
