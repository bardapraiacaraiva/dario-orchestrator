#!/usr/bin/env python3
"""
DARIO Orchestrator — Upgrade Runner v12.0 → v12.1

Run after `git pull full master`. Idempotent — safe to re-run.

What it does:
  1. Creates ~/.claude/orchestrator/prometheus/ directory structure
  2. Initializes state YAML files (last_run, releases, mcp, papers, regulatory)
  3. Creates scheduled task "PROMETHEUS Weekly" (Sunday 22h00 BRT)
  4. Creates scheduled task "PROMETHEUS Wave 3 Reminder" (one-shot 2026-06-17 09h00)
  5. Verifies cron_daily continues active (Memory & Dreaming)
  6. Validates integrity post-upgrade
  7. Optionally re-ingests skills into RAG (if engine running)

Usage:
  python scripts/upgrade_v12_1.py            # full run
  python scripts/upgrade_v12_1.py --check    # dry-run, only validation
  python scripts/upgrade_v12_1.py --skip-cron # don't create scheduled tasks
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
PROM_DIR = ORCH_DIR / "prometheus"
RAG_DIR = Path("C:/dario-rag")  # adapta se diferente


# ── Helpers ──────────────────────────────────────────────────────────────

def log(level: str, msg: str) -> None:
    emoji = {"ok": "✅", "warn": "⚠️", "fail": "❌", "info": "ℹ️", "skip": "⏭️"}.get(level, " ")
    print(f"  {emoji} {msg}", flush=True)


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def check_python_version():
    if sys.version_info < (3, 9):
        log("fail", f"Python {sys.version_info.major}.{sys.version_info.minor} detected. Need ≥ 3.9.")
        sys.exit(1)
    log("ok", f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def run_powershell(cmd: str) -> tuple[int, str]:
    """Run a PowerShell command, return (exit_code, output)."""
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, timeout=30
        )
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)


# ── Step 1: Directory structure ──────────────────────────────────────────

def step_directories(dry_run: bool) -> None:
    section("Step 1: Directory structure")
    dirs = [
        PROM_DIR,
        PROM_DIR / "state",
        PROM_DIR / "digests",
        PROM_DIR / "findings",
        PROM_DIR / "experiments",  # for Wave 3 future
        ORCH_DIR / "bundles",
    ]
    for d in dirs:
        if d.exists():
            log("ok", f"exists: {d.relative_to(Path.home())}")
        else:
            if dry_run:
                log("info", f"would create: {d.relative_to(Path.home())}")
            else:
                d.mkdir(parents=True, exist_ok=True)
                log("ok", f"created: {d.relative_to(Path.home())}")


# ── Step 2: State YAML init ──────────────────────────────────────────────

def step_state_files(dry_run: bool) -> None:
    section("Step 2: Initialize state YAML files")
    state_init = {
        "last_run.yaml": {
            "prometheus_wave": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_weekly_scan": None,
            "total_digests_produced": 0,
            "total_findings_flagged_high": 0,
            "total_findings_actioned_by_user": 0,
            "weeks_run": [],
        },
        "last_seen_releases.yaml": {"last_scan": None, "repos": {}},
        "known_mcp_servers.yaml": {"last_scan": None, "sources_scanned": [], "servers": {}, "new_this_week": []},
        "seen_papers.yaml": {"last_scan": None, "sources_scanned": [], "papers_seen": [], "total_seen": 0},
        "regulatory_state.yaml": {"last_scan": None, "sources_scanned": [], "findings_this_week": [], "critical_pending": []},
    }
    try:
        import yaml
    except ImportError:
        log("fail", "PyYAML not installed. Run: pip install pyyaml")
        return

    for filename, content in state_init.items():
        path = PROM_DIR / "state" / filename
        if path.exists():
            log("ok", f"exists (preserved): {filename}")
        else:
            if dry_run:
                log("info", f"would create: {filename}")
            else:
                path.write_text(yaml.dump(content, sort_keys=False), encoding="utf-8")
                log("ok", f"created: {filename}")


# ── Step 3: Scheduled tasks ──────────────────────────────────────────────

def step_scheduled_tasks(dry_run: bool, skip_cron: bool) -> None:
    section("Step 3: Scheduled tasks (Windows Task Scheduler)")
    if skip_cron:
        log("skip", "skipped (--skip-cron flag)")
        return

    if os.name != "nt":
        log("warn", f"Not Windows ({os.name}). Skipping schtasks. Configure cron manually.")
        return

    cron_script = RAG_DIR / "scripts" / "prometheus_cron.py"
    reminder_script = RAG_DIR / "scripts" / "prometheus_wave3_reminder.py"
    python_exe = RAG_DIR / "engine" / ".venv" / "Scripts" / "python.exe"

    if not python_exe.exists():
        log("warn", f"Python venv não encontrado em {python_exe}. Skipping schtasks. Configura manualmente.")
        return

    tasks = [
        {
            "name": "PROMETHEUS Weekly",
            "schedule": ["weekly", "/d", "SUN", "/st", "22:00"],
            "script": cron_script,
            "exists_check": "PROMETHEUS Weekly",
        },
        {
            "name": "PROMETHEUS Wave 3 Reminder",
            "schedule": ["once", "/sd", "17/06/2026", "/st", "09:00"],
            "script": reminder_script,
            "exists_check": "PROMETHEUS Wave 3 Reminder",
        },
    ]

    for task in tasks:
        # Check if exists
        code, _ = run_powershell(f"schtasks /query /tn '{task['exists_check']}' 2>&1")
        if code == 0:
            log("ok", f"already scheduled: {task['name']}")
            continue

        if not task["script"].exists():
            log("warn", f"script missing: {task['script']} — skipping {task['name']}")
            continue

        if dry_run:
            log("info", f"would schedule: {task['name']}")
            continue

        sched_str = " ".join(task["schedule"])
        cmd = (
            f"schtasks /create /tn '{task['name']}' /sc {sched_str} "
            f"/tr '\"{python_exe}\" \"{task['script']}\"' /f"
        )
        code, output = run_powershell(cmd)
        if code == 0:
            log("ok", f"scheduled: {task['name']}")
        else:
            log("fail", f"failed to schedule {task['name']}: {output[:200]}")


# ── Step 4: Cron daily (Memory & Dreaming) ──────────────────────────────

def step_dream_cron(dry_run: bool) -> None:
    section("Step 4: Memory & Dreaming cron (cron_daily)")
    if os.name != "nt":
        log("skip", "non-Windows")
        return
    code, _ = run_powershell("schtasks /query /tn 'DARIO Dream Daily' 2>&1")
    if code == 0:
        log("ok", "DARIO Dream Daily already scheduled")
    else:
        log("warn", "DARIO Dream Daily not scheduled. Run: powershell scripts/dream_install_cron.ps1")


# ── Step 5: RAG re-ingest (optional) ────────────────────────────────────

def step_rag_reingest(dry_run: bool) -> None:
    section("Step 5: RAG re-ingest novas skills (optional)")
    bulk_script = RAG_DIR / "scripts" / "bulk_ingest_skills.py"
    python_exe = RAG_DIR / "engine" / ".venv" / "Scripts" / "python.exe"
    if not bulk_script.exists() or not python_exe.exists():
        log("warn", "RAG bulk_ingest_skills.py ou venv não encontrado — skip. Re-ingest manualmente.")
        return

    # Check if RAG engine is reachable
    try:
        import urllib.request
        with urllib.request.urlopen("http://localhost:8420/health", timeout=3) as r:
            data = json.loads(r.read())
        log("ok", f"RAG engine alive: {data.get('sources')} sources / {data.get('chunks')} chunks")
    except Exception:
        log("warn", "RAG engine não responde em localhost:8420. Skip re-ingest. Start RAG e re-corre upgrade.")
        return

    if dry_run:
        log("info", "would re-ingest skills via bulk_ingest_skills.py")
        return

    log("info", "Re-ingesting skills (~30-60s, hash-skip para skills inalteradas)...")
    try:
        r = subprocess.run(
            [str(python_exe), str(bulk_script)],
            capture_output=True, text=True, timeout=180
        )
        if r.returncode == 0:
            last_line = r.stdout.strip().split("\n")[-1]
            log("ok", f"re-ingest done: {last_line[:120]}")
        else:
            log("warn", f"bulk_ingest exit code {r.returncode}: {r.stderr[:200]}")
    except Exception as e:
        log("fail", f"bulk_ingest failed: {e}")


# ── Step 6: Integrity check ─────────────────────────────────────────────

def step_integrity_check() -> None:
    section("Step 6: Integrity check pos-upgrade")
    critical_files = [
        ORCH_DIR / "company.yaml",
        ORCH_DIR / "skill_chains.yaml",
        ORCH_DIR / "license_manager.py",
        ORCH_DIR / "MANUAL.md",
        Path.home() / ".claude" / "skills" / "a360-director" / "SKILL.md",
        Path.home() / ".claude" / "skills" / "prometheus-director" / "SKILL.md",
        PROM_DIR / "findings" / "deprecations_kb.yaml",
        PROM_DIR / "findings" / "version_baselines.yaml",
    ]
    ok = 0
    for f in critical_files:
        if f.exists():
            log("ok", f"present: {f.relative_to(Path.home())}")
            ok += 1
        else:
            log("fail", f"MISSING: {f.relative_to(Path.home())}")
    if ok == len(critical_files):
        log("ok", f"all {ok}/{len(critical_files)} critical files present")
    else:
        log("warn", f"{ok}/{len(critical_files)} critical files — review missing files")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DARIO v12.0 → v12.1 upgrade runner")
    parser.add_argument("--check", action="store_true", help="dry-run, no changes")
    parser.add_argument("--skip-cron", action="store_true", help="don't create scheduled tasks")
    args = parser.parse_args()

    dry_run = args.check
    print(f"=== DARIO Orchestrator Upgrade v12.0 → v12.1 {'(DRY-RUN)' if dry_run else ''} ===")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Orch dir: {ORCH_DIR}")
    print(f"RAG dir:  {RAG_DIR}")
    print()

    check_python_version()
    step_directories(dry_run)
    step_state_files(dry_run)
    step_scheduled_tasks(dry_run, args.skip_cron)
    step_dream_cron(dry_run)
    step_rag_reingest(dry_run)
    step_integrity_check()

    print()
    if dry_run:
        print("=== DRY-RUN complete. Run without --check to apply changes. ===")
    else:
        print("=== Upgrade v12.1 complete. ===")
        print()
        print("Next steps:")
        print("  1. Verify cron: schtasks /query /tn 'PROMETHEUS Weekly'")
        print("  2. Próxima auto-execução: Domingo 22h00 BRT")
        print("  3. Read UPGRADE-v12.0-to-v12.1.md para detalhes")
        print("  4. Em 2026-06-17 → 'PROMETHEUS Wave 3 Reminder' cria marker para review")


if __name__ == "__main__":
    main()
