#!/usr/bin/env python3
"""
DARIO Webhook Dispatcher
========================
Upgrade 15 (operational complement to U12 cron daily).

notifications.yaml defines 19 events with 4 channels: pulse_report,
audit_log, obsidian_alert, task_note. None of them push outside the
local machine. This module adds the missing webhook channel — Slack,
Discord, or generic HTTP POST — gated by severity.

Architecture:
  - webhook_config.yaml         Per-webhook URL/format/min_severity (NOT
                                checked into git, holds secrets)
  - webhook_log.yaml            Idempotency ledger — prevents duplicate
                                sends within a 24h window for the same
                                event_key
  - Built-in formatters         slack / discord / generic_json

Used by cron_daily to push alerts when integrity FAIL, regression DRIFT,
overconfidence rate threshold breach, or job execution errors occur.

CLI:
    python webhook_dispatcher.py --init           Generate config skeleton
    python webhook_dispatcher.py --send EVENT --severity alert --message "test"
    python webhook_dispatcher.py --flush-alerts   Push all unsent alerts from last_pulse
    python webhook_dispatcher.py --test           Send test ping to all configured webhooks
    python webhook_dispatcher.py --status         Show configured hooks + recent sends
"""

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _yaml.load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(data, f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return _pyaml.safe_load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _pyaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
WEBHOOK_CONFIG = ORCH_DIR / "webhook_config.yaml"
WEBHOOK_LOG = ORCH_DIR / "webhook_log.yaml"
PULSE_FILE = ORCH_DIR / "last_pulse.yaml"

# Severity ordering (numeric for comparison)
SEVERITY_LEVELS = {"info": 0, "warn": 1, "warning": 1, "alert": 2, "critical": 2}

# Idempotency: same event_key within this window = skip
DEDUP_WINDOW_HOURS = 24

# Timeout per webhook POST
REQUEST_TIMEOUT_SECONDS = 5

# Retry on network failure
MAX_RETRIES = 2


# =============================================================================
# CONFIG
# =============================================================================

DEFAULT_CONFIG = {
    "enabled": False,
    "hooks": [
        {
            "name": "slack-alerts",
            "type": "slack",
            "url": "REPLACE_WITH_SLACK_WEBHOOK_URL",
            "enabled": False,
            "min_severity": "alert",
            "events": "*",
        },
        {
            "name": "discord-alerts",
            "type": "discord",
            "url": "REPLACE_WITH_DISCORD_WEBHOOK_URL",
            "enabled": False,
            "min_severity": "alert",
            "events": "*",
        },
        {
            "name": "generic-monitoring",
            "type": "generic_json",
            "url": "REPLACE_WITH_GENERIC_WEBHOOK_URL",
            "enabled": False,
            "min_severity": "warn",
            "events": "*",
        },
    ],
}


def init_config(force: bool = False) -> dict:
    """Create webhook_config.yaml skeleton if not present."""
    if WEBHOOK_CONFIG.exists() and not force:
        return {"status": "exists", "path": str(WEBHOOK_CONFIG)}
    _dump_yaml(DEFAULT_CONFIG, str(WEBHOOK_CONFIG))
    return {"status": "created", "path": str(WEBHOOK_CONFIG)}


def load_config() -> dict:
    if not WEBHOOK_CONFIG.exists():
        return {"enabled": False, "hooks": []}
    try:
        data = _load_yaml(str(WEBHOOK_CONFIG))
        return data if isinstance(data, dict) else {"enabled": False, "hooks": []}
    except Exception:
        return {"enabled": False, "hooks": []}


# =============================================================================
# IDEMPOTENCY LOG
# =============================================================================

def _event_key(event_name: str, subsystem: str = "", message: str = "") -> str:
    """Deterministic key for dedup. Same (event, subsystem, hash-of-msg)
    within DEDUP_WINDOW_HOURS = skip."""
    msg_hash = hashlib.sha256(message.encode("utf-8")).hexdigest()[:8] if message else ""
    return f"{event_name}::{subsystem}::{msg_hash}"


def _was_sent_recently(event_key: str) -> bool:
    if not WEBHOOK_LOG.exists():
        return False
    try:
        data = _load_yaml(str(WEBHOOK_LOG)) or {}
        sends = data.get("sends", [])
        cutoff = datetime.now(timezone.utc) - timedelta(hours=DEDUP_WINDOW_HOURS)
        for entry in sends:
            if entry.get("event_key") != event_key:
                continue
            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if ts > cutoff:
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def _log_send(event_key: str, hook_name: str, status: str, severity: str,
              message: str = "", http_code: int = 0):
    data = {"sends": []}
    if WEBHOOK_LOG.exists():
        try:
            existing = _load_yaml(str(WEBHOOK_LOG))
            if isinstance(existing, dict) and isinstance(existing.get("sends"), list):
                data = existing
        except Exception:
            pass
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_key": event_key,
        "hook": hook_name,
        "status": status,
        "severity": severity,
        "http_code": http_code,
        "message_preview": (message or "")[:120],
    }
    data["sends"].append(entry)
    # Keep only last 500 entries (prevent unbounded growth)
    data["sends"] = data["sends"][-500:]
    _dump_yaml(data, str(WEBHOOK_LOG))


# =============================================================================
# FORMATTERS — convert event dict to payload per webhook type
# =============================================================================

def _format_slack(event: dict) -> dict:
    sev = event.get("severity", "info").lower()
    emoji = {"info": ":information_source:", "warn": ":warning:",
             "warning": ":warning:", "alert": ":rotating_light:",
             "critical": ":rotating_light:"}.get(sev, ":bell:")
    return {
        "text": f"{emoji} *DARIO {sev.upper()}*: {event.get('event', 'unknown')}",
        "attachments": [{
            "color": {"info": "#3498db", "warn": "#f39c12", "warning": "#f39c12",
                      "alert": "#e74c3c", "critical": "#e74c3c"}.get(sev, "#95a5a6"),
            "fields": [
                {"title": "Subsystem", "value": event.get("subsystem", "-"), "short": True},
                {"title": "Time", "value": event.get("timestamp", "-"), "short": True},
                {"title": "Message", "value": event.get("message", ""), "short": False},
            ],
            "footer": "DARIO Orchestrator",
        }],
    }


def _format_discord(event: dict) -> dict:
    sev = event.get("severity", "info").lower()
    color = {"info": 3447003, "warn": 15844367, "warning": 15844367,
             "alert": 15158332, "critical": 15158332}.get(sev, 9807270)
    return {
        "embeds": [{
            "title": f"DARIO {sev.upper()}: {event.get('event', 'unknown')}",
            "description": event.get("message", ""),
            "color": color,
            "fields": [
                {"name": "Subsystem", "value": event.get("subsystem", "-"), "inline": True},
                {"name": "Time", "value": event.get("timestamp", "-")[:19], "inline": True},
            ],
            "footer": {"text": "DARIO Orchestrator"},
        }],
    }


def _format_generic(event: dict) -> dict:
    """Generic JSON payload — pass-through with normalised keys."""
    return {
        "service": "dario-orchestrator",
        "severity": event.get("severity", "info"),
        "event": event.get("event"),
        "subsystem": event.get("subsystem"),
        "message": event.get("message"),
        "timestamp": event.get("timestamp"),
        "context": event.get("context", {}),
    }


FORMATTERS = {
    "slack": _format_slack,
    "discord": _format_discord,
    "generic_json": _format_generic,
}


# =============================================================================
# HTTP POST
# =============================================================================

def _post(url: str, payload: dict) -> tuple:
    """Returns (success: bool, http_code: int, error: str)."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json",
                 "User-Agent": "DARIO-Orchestrator/1.0"},
        method="POST",
    )
    last_err = ""
    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                return True, resp.status, ""
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.reason}"
            if e.code < 500:
                # Client error — don't retry
                return False, e.code, last_err
        except urllib.error.URLError as e:
            last_err = f"URL error: {e.reason}"
        except Exception as e:
            last_err = str(e)[:100]
    return False, 0, last_err


# =============================================================================
# DISPATCH
# =============================================================================

def _hook_should_fire(hook: dict, event: dict) -> bool:
    if not hook.get("enabled"):
        return False
    if not hook.get("url") or "REPLACE_WITH" in hook.get("url", ""):
        return False
    # Severity gate
    min_sev = SEVERITY_LEVELS.get(hook.get("min_severity", "info").lower(), 0)
    event_sev = SEVERITY_LEVELS.get(event.get("severity", "info").lower(), 0)
    if event_sev < min_sev:
        return False
    # Event filter (specific list or "*")
    events_filter = hook.get("events", "*")
    if events_filter != "*" and isinstance(events_filter, list):
        if event.get("event") not in events_filter:
            return False
    return True


def send(event: dict, dry_run: bool = False) -> dict:
    """Dispatch a single event to all configured webhooks.

    `event` dict expected keys:
        event: str             event name
        severity: str          info | warn | alert | critical
        subsystem: str         which subsystem raised it
        message: str           human-readable text
        timestamp: str         ISO timestamp (optional; defaults now)
        context: dict          extra structured data (optional)
    """
    if "timestamp" not in event:
        event["timestamp"] = datetime.now(timezone.utc).isoformat()

    config = load_config()
    if not config.get("enabled"):
        return {"status": "disabled", "sends": 0}

    event_key = _event_key(
        event.get("event", "unknown"),
        event.get("subsystem", ""),
        event.get("message", ""),
    )

    if _was_sent_recently(event_key):
        return {"status": "deduped", "sends": 0, "event_key": event_key}

    sends = []
    for hook in config.get("hooks", []):
        if not _hook_should_fire(hook, event):
            continue
        formatter = FORMATTERS.get(hook.get("type", "generic_json"), _format_generic)
        payload = formatter(event)
        if dry_run:
            sends.append({
                "hook": hook.get("name"),
                "status": "dry_run",
                "payload_preview": str(payload)[:200],
            })
            continue
        success, code, err = _post(hook["url"], payload)
        status = "ok" if success else "fail"
        _log_send(event_key, hook["name"], status,
                  event.get("severity", "info"),
                  event.get("message", ""), code)
        sends.append({
            "hook": hook.get("name"),
            "status": status,
            "http_code": code,
            "error": err,
        })

    return {
        "status": "sent" if sends else "no_matching_hooks",
        "sends": len(sends),
        "details": sends,
        "event_key": event_key,
    }


def flush_pulse_alerts(dry_run: bool = False) -> dict:
    """Read last_pulse.yaml and dispatch any unsent cron-daily alerts."""
    if not PULSE_FILE.exists():
        return {"status": "no_pulse", "dispatched": 0}
    try:
        pulse = _load_yaml(str(PULSE_FILE)) or {}
    except Exception:
        return {"status": "pulse_unreadable", "dispatched": 0}

    alerts = pulse.get("alerts", []) or []
    dispatched = 0
    results = []
    for entry in alerts:
        if not isinstance(entry, dict):
            continue
        event = {
            "event": entry.get("source", "pulse_alert"),
            "severity": entry.get("severity", "info"),
            "subsystem": entry.get("subsystem", ""),
            "message": entry.get("message", ""),
            "timestamp": entry.get("timestamp"),
        }
        r = send(event, dry_run=dry_run)
        if r["sends"] > 0:
            dispatched += 1
        results.append({"event": event["event"], "result": r["status"], "sends": r["sends"]})

    return {
        "status": "ok",
        "total_alerts_in_pulse": len(alerts),
        "dispatched": dispatched,
        "results": results,
    }


def test_ping() -> dict:
    """Send a test event to all configured webhooks."""
    event = {
        "event": "dario_test_ping",
        "severity": "info",
        "subsystem": "webhook_dispatcher",
        "message": "DARIO test ping — webhook configured correctly.",
    }
    return send(event, dry_run=False)


def status() -> dict:
    config = load_config()
    enabled_hooks = [h for h in config.get("hooks", []) if h.get("enabled")]
    recent_sends = []
    if WEBHOOK_LOG.exists():
        try:
            data = _load_yaml(str(WEBHOOK_LOG)) or {}
            sends = (data.get("sends") or [])[-10:]
            recent_sends = sends[::-1]
        except Exception:
            pass
    return {
        "enabled": bool(config.get("enabled")),
        "config_exists": WEBHOOK_CONFIG.exists(),
        "total_hooks": len(config.get("hooks", [])),
        "enabled_hooks": len(enabled_hooks),
        "enabled_hook_names": [h.get("name") for h in enabled_hooks],
        "recent_sends": recent_sends,
    }


def main():
    p = argparse.ArgumentParser(description="DARIO Webhook Dispatcher")
    p.add_argument("--init", action="store_true",
                   help="Create webhook_config.yaml skeleton")
    p.add_argument("--force", action="store_true",
                   help="Overwrite existing config (use with --init)")
    p.add_argument("--send", help="Event name to send")
    p.add_argument("--severity", default="info",
                   help="Severity: info | warn | alert | critical")
    p.add_argument("--subsystem", default="manual", help="Subsystem name")
    p.add_argument("--message", default="", help="Event message")
    p.add_argument("--flush-alerts", action="store_true",
                   help="Push pulse alerts to webhooks")
    p.add_argument("--test", action="store_true",
                   help="Send test ping to configured webhooks")
    p.add_argument("--status", action="store_true")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be sent without sending")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.init:
        r = init_config(force=args.force)
        print(json.dumps(r, indent=2) if args.json else
              f"[{r['status']}] {r['path']}")
        return 0

    if args.status:
        s = status()
        print(json.dumps(s, indent=2, ensure_ascii=False, default=str) if args.json
              else "\n".join(f"  {k}: {v}" for k, v in s.items()))
        return 0

    if args.test:
        r = test_ping()
        print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        return 0 if r.get("status") in ("sent", "disabled") else 1

    if args.flush_alerts:
        r = flush_pulse_alerts(dry_run=args.dry_run)
        print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        return 0

    if args.send:
        event = {
            "event": args.send,
            "severity": args.severity,
            "subsystem": args.subsystem,
            "message": args.message,
        }
        r = send(event, dry_run=args.dry_run)
        print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
