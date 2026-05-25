#!/usr/bin/env python3
"""Tests for Upgrade 15 webhook dispatcher."""

import shutil
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))


import webhook_dispatcher as wd


def _backup_log():
    if wd.WEBHOOK_LOG.exists():
        backup = wd.WEBHOOK_LOG.with_suffix(".yaml.test-bak")
        shutil.copy(wd.WEBHOOK_LOG, backup)
        return backup
    return None


def _restore_log(backup):
    if backup and backup.exists():
        shutil.copy(backup, wd.WEBHOOK_LOG)
        backup.unlink()
    elif backup is None and wd.WEBHOOK_LOG.exists():
        wd.WEBHOOK_LOG.unlink()


def _backup_config():
    if wd.WEBHOOK_CONFIG.exists():
        backup = wd.WEBHOOK_CONFIG.with_suffix(".yaml.test-bak")
        shutil.copy(wd.WEBHOOK_CONFIG, backup)
        return backup
    return None


def _restore_config(backup):
    if backup and backup.exists():
        shutil.copy(backup, wd.WEBHOOK_CONFIG)
        backup.unlink()


def test_init_creates_config():
    backup = _backup_config()
    try:
        if wd.WEBHOOK_CONFIG.exists():
            wd.WEBHOOK_CONFIG.unlink()
        r = wd.init_config()
        assert r["status"] == "created"
        assert wd.WEBHOOK_CONFIG.exists()
        return True
    finally:
        _restore_config(backup)


def test_init_idempotent_unless_force():
    backup = _backup_config()
    try:
        wd.init_config(force=True)
        r = wd.init_config(force=False)
        assert r["status"] == "exists"
        return True
    finally:
        _restore_config(backup)


def test_disabled_config_returns_disabled():
    """Default config is disabled — send should noop."""
    backup = _backup_config()
    try:
        wd.init_config(force=True)
        r = wd.send({"event": "x", "severity": "alert", "message": "test"})
        assert r["status"] == "disabled"
        assert r["sends"] == 0
        return True
    finally:
        _restore_config(backup)


def test_slack_formatter():
    event = {"event": "drift", "severity": "alert", "subsystem": "reg",
             "message": "msg", "timestamp": "2026-05-19T00:00:00Z"}
    p = wd._format_slack(event)
    assert "text" in p
    assert "attachments" in p
    assert "ALERT" in p["text"]


def test_discord_formatter():
    event = {"event": "drift", "severity": "alert", "subsystem": "reg",
             "message": "msg", "timestamp": "2026-05-19T00:00:00Z"}
    p = wd._format_discord(event)
    assert "embeds" in p
    assert len(p["embeds"]) == 1
    assert p["embeds"][0]["color"] == 15158332  # red


def test_generic_formatter():
    event = {"event": "drift", "severity": "warn", "subsystem": "reg", "message": "m"}
    p = wd._format_generic(event)
    assert p["service"] == "dario-orchestrator"
    assert p["severity"] == "warn"
    assert p["event"] == "drift"


def test_hook_should_fire_severity_gating():
    hook = {"enabled": True, "url": "http://x", "min_severity": "alert", "events": "*"}
    event_alert = {"event": "x", "severity": "alert"}
    event_info = {"event": "x", "severity": "info"}
    assert wd._hook_should_fire(hook, event_alert) is True
    assert wd._hook_should_fire(hook, event_info) is False


def test_hook_should_fire_disabled():
    hook = {"enabled": False, "url": "http://x", "min_severity": "info", "events": "*"}
    assert wd._hook_should_fire(hook, {"event": "x", "severity": "alert"}) is False


def test_hook_should_fire_unset_url():
    hook = {"enabled": True, "url": "REPLACE_WITH_URL", "min_severity": "info", "events": "*"}
    assert wd._hook_should_fire(hook, {"event": "x", "severity": "alert"}) is False


def test_hook_should_fire_event_filter_list():
    hook = {"enabled": True, "url": "http://x", "min_severity": "info",
            "events": ["wanted_event"]}
    assert wd._hook_should_fire(hook, {"event": "wanted_event", "severity": "info"}) is True
    assert wd._hook_should_fire(hook, {"event": "other_event", "severity": "info"}) is False


def test_event_key_deterministic():
    k1 = wd._event_key("e1", "sub", "msg")
    k2 = wd._event_key("e1", "sub", "msg")
    assert k1 == k2
    k3 = wd._event_key("e1", "sub", "different msg")
    assert k1 != k3


def test_dedup_skips_recent():
    """Same event_key within 24h should be deduped."""
    backup = _backup_log()
    try:
        wd.WEBHOOK_LOG.write_text("", encoding="utf-8")
        # Log a fake recent send
        wd._log_send("dedup-test::sub::abc12345", "test-hook", "ok", "alert", "msg", 200)
        assert wd._was_sent_recently("dedup-test::sub::abc12345") is True
        assert wd._was_sent_recently("never-sent-xyz") is False
        return True
    finally:
        _restore_log(backup)


def test_dedup_expires_after_window():
    """Send older than 24h should NOT dedup."""
    backup = _backup_log()
    try:
        old_ts = (datetime.now(UTC) - timedelta(hours=30)).isoformat()
        wd._dump_yaml({
            "sends": [{
                "timestamp": old_ts,
                "event_key": "old-event::sub::aaa11111",
                "hook": "t", "status": "ok", "severity": "alert",
                "http_code": 200, "message_preview": "old",
            }],
        }, str(wd.WEBHOOK_LOG))
        assert wd._was_sent_recently("old-event::sub::aaa11111") is False
        return True
    finally:
        _restore_log(backup)


def test_send_with_dedup_returns_deduped():
    backup_cfg = _backup_config()
    backup_log = _backup_log()
    try:
        # Setup enabled config with a hook to test dedup path
        wd._dump_yaml({
            "enabled": True,
            "hooks": [{
                "name": "test-hook", "type": "generic_json",
                "url": "http://localhost:1/none", "enabled": True,
                "min_severity": "info", "events": "*",
            }],
        }, str(wd.WEBHOOK_CONFIG))

        # First call with a known event_key — we manually pre-populate log
        event = {"event": "dedup-target", "severity": "alert",
                 "subsystem": "test", "message": "dedup test message"}
        key = wd._event_key("dedup-target", "test", "dedup test message")
        wd._log_send(key, "test-hook", "ok", "alert", "msg", 200)

        # Now send — should dedup
        r = wd.send(event, dry_run=True)
        assert r["status"] == "deduped"
        return True
    finally:
        _restore_config(backup_cfg)
        _restore_log(backup_log)


def test_send_dry_run_does_not_post():
    backup_cfg = _backup_config()
    try:
        wd._dump_yaml({
            "enabled": True,
            "hooks": [{
                "name": "test-hook", "type": "slack",
                "url": "http://localhost:1/none", "enabled": True,
                "min_severity": "info", "events": "*",
            }],
        }, str(wd.WEBHOOK_CONFIG))
        event = {"event": "dry-run-only-xyz", "severity": "info",
                 "subsystem": "test", "message": f"dry test {datetime.now().isoformat()}"}
        r = wd.send(event, dry_run=True)
        assert r["status"] in ("sent", "no_matching_hooks")
        if r["status"] == "sent":
            assert all(s["status"] == "dry_run" for s in r["details"])
        return True
    finally:
        _restore_config(backup_cfg)


def test_no_matching_hooks_when_all_fail_filter():
    backup_cfg = _backup_config()
    try:
        wd._dump_yaml({
            "enabled": True,
            "hooks": [{
                "name": "alert-only", "type": "slack",
                "url": "http://localhost:1/none", "enabled": True,
                "min_severity": "alert", "events": "*",
            }],
        }, str(wd.WEBHOOK_CONFIG))
        event = {"event": "low-sev", "severity": "info",
                 "subsystem": "test", "message": "info only"}
        r = wd.send(event, dry_run=True)
        assert r["status"] == "no_matching_hooks"
        assert r["sends"] == 0
        return True
    finally:
        _restore_config(backup_cfg)


def test_status_returns_structure():
    s = wd.status()
    assert "enabled" in s
    assert "config_exists" in s
    assert "total_hooks" in s
    assert "recent_sends" in s


def test_severity_levels_complete():
    """Ensure all expected severities are mapped."""
    for sev in ("info", "warn", "warning", "alert", "critical"):
        assert sev in wd.SEVERITY_LEVELS


def test_formatters_registered():
    for kind in ("slack", "discord", "generic_json"):
        assert kind in wd.FORMATTERS


TESTS = [
    ("init creates config", test_init_creates_config),
    ("init idempotent without force", test_init_idempotent_unless_force),
    ("disabled config returns disabled", test_disabled_config_returns_disabled),
    ("slack formatter shape", test_slack_formatter),
    ("discord formatter shape", test_discord_formatter),
    ("generic formatter shape", test_generic_formatter),
    ("severity gating works", test_hook_should_fire_severity_gating),
    ("disabled hook never fires", test_hook_should_fire_disabled),
    ("unset URL never fires", test_hook_should_fire_unset_url),
    ("event filter list works", test_hook_should_fire_event_filter_list),
    ("event_key deterministic", test_event_key_deterministic),
    ("dedup skips recent sends", test_dedup_skips_recent),
    ("dedup expires after window", test_dedup_expires_after_window),
    ("send dedups duplicate event", test_send_with_dedup_returns_deduped),
    ("dry_run does not POST", test_send_dry_run_does_not_post),
    ("no_matching_hooks when all filter out", test_no_matching_hooks_when_all_fail_filter),
    ("status returns expected schema", test_status_returns_structure),
    ("severity levels complete", test_severity_levels_complete),
    ("formatters registered", test_formatters_registered),
]


def run():
    passed = 0
    failed = 0
    for name, fn in TESTS:
        try:
            ok = fn()
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name}")
            if ok:
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: CRASHED — {e}")
            failed += 1
    print()
    print(f"Results: {passed} passed, {failed} failed (of {len(TESTS)})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
