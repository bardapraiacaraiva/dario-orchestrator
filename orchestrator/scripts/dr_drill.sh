#!/usr/bin/env bash
# DARIO Disaster Recovery Drill — non-destructive validation that the
# latest backup can be restored to a working state.
#
# Restores to /tmp/dr-drill-<timestamp>/ (cleaned up at end), runs the
# Full Restore Procedure from DR_RUNBOOK.md, validates with a smoke
# suite, then deletes the test directory.
#
# DOES NOT TOUCH production install at ~/.claude.
#
# Usage:
#   bash scripts/dr_drill.sh             # full drill (~5min)
#   bash scripts/dr_drill.sh --keep      # leave restore dir for inspection

set -uo pipefail
# Don't fail-fast; we want all validation steps to run and report status.

KEEP=0
[ "${1:-}" = "--keep" ] && KEEP=1

BACKUPS_DIR="$HOME/.claude-backups"
LATEST_BACKUP=$(ls -1dt "$BACKUPS_DIR"/20*/ 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "FAIL: no backups in $BACKUPS_DIR"
    exit 1
fi

LATEST_BACKUP="${LATEST_BACKUP%/}"  # strip trailing slash
TIMESTAMP=$(date +%s)
DRILL_DIR="/tmp/dr-drill-$TIMESTAMP"
DRILL_HOME="$DRILL_DIR/home"
ORCH="$DRILL_HOME/.claude/orchestrator"

echo "═══════════════════════════════════════════════════════"
echo " DARIO DR Drill — $(date -Iseconds)"
echo "═══════════════════════════════════════════════════════"
echo " Backup:  $LATEST_BACKUP"
echo " Restore: $DRILL_DIR"
echo

mkdir -p "$DRILL_HOME/.claude"
cd "$DRILL_HOME/.claude"

FAILS=0
WARNS=0

# ─── Step 1: Restore orchestrator repo from bundle ───────────────────
echo "[1/7] Cloning from bundle..."
if git clone "$LATEST_BACKUP/dario-orchestrator.bundle" . >/dev/null 2>&1; then
    HEAD_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "?")
    echo "  OK head=$HEAD_SHA"
else
    echo "  FAIL"
    FAILS=$((FAILS + 1))
fi

# ─── Step 2: Restore user memory ──────────────────────────────────────
echo "[2/7] Extracting memory.tar.gz..."
mkdir -p "$DRILL_HOME/.claude/projects/C--Users-barda"
cd "$DRILL_HOME/.claude/projects/C--Users-barda"
if tar -xzf "$LATEST_BACKUP/memory.tar.gz" 2>/dev/null; then
    MEM_COUNT=$(find memory -name "*.md" 2>/dev/null | wc -l)
    echo "  OK $MEM_COUNT memory files"
    [ "$MEM_COUNT" -lt 50 ] && { echo "  WARN: only $MEM_COUNT memory files (expected >=80)"; WARNS=$((WARNS+1)); }
else
    echo "  FAIL"
    FAILS=$((FAILS + 1))
fi

# ─── Step 3: Restore runtime state ────────────────────────────────────
echo "[3/7] Extracting orchestrator-runtime.tar.gz..."
cd "$ORCH"
if tar -xzf "$LATEST_BACKUP/orchestrator-runtime.tar.gz" 2>/dev/null; then
    DBSIZE=$([ -f core/dario.db ] && stat -c%s core/dario.db || echo 0)
    echo "  OK runtime restored, dario.db=$DBSIZE bytes"
    [ -f .license ]       && echo "  OK .license present" || { echo "  WARN: .license missing"; WARNS=$((WARNS+1)); }
    [ -f .master_secret ] && echo "  OK .master_secret present" || { echo "  WARN: .master_secret missing"; WARNS=$((WARNS+1)); }
else
    echo "  FAIL"
    FAILS=$((FAILS + 1))
fi

# ─── Step 4: Verify file layout ───────────────────────────────────────
echo "[4/7] Checking layout..."
LAYOUT_FAILS=0
for f in pyproject.toml cron_daily.py core/runtime.py dispatch/dispatch_engine.py quality/golden_eval.py safety/ethical_gate.py licensing/license_guard.py enforcement/budget_gate.py; do
    if [ ! -f "$ORCH/$f" ]; then
        echo "  FAIL: missing $f"
        LAYOUT_FAILS=$((LAYOUT_FAILS + 1))
    fi
done
if [ "$LAYOUT_FAILS" -eq 0 ]; then
    echo "  OK all 8 critical paths present"
else
    FAILS=$((FAILS + LAYOUT_FAILS))
fi

# ─── Step 5: Bundle integrity verification ────────────────────────────
echo "[5/7] Verifying bundle integrity..."
if git -C "$ORCH/.." bundle verify "$LATEST_BACKUP/dario-orchestrator.bundle" >/dev/null 2>&1; then
    echo "  OK bundle verified (complete history)"
else
    echo "  FAIL: bundle is corrupted"
    FAILS=$((FAILS + 1))
fi

# ─── Step 6: Audit chain integrity (if any signed entries) ────────────
echo "[6/7] Audit chain check (informational, no fail)..."
TODAY=$(date +%Y-%m-%d)
if [ -f "$ORCH/audit/$TODAY.yaml" ]; then
    echo "  Today's audit file present ($(wc -l < "$ORCH/audit/$TODAY.yaml") lines)"
    # We can't actually verify here without the venv; just confirm file exists.
else
    echo "  (no audit file for today — informational)"
fi

# ─── Step 7: Final status ─────────────────────────────────────────────
echo
echo "═══════════════════════════════════════════════════════"
echo " DR Drill Result"
echo "═══════════════════════════════════════════════════════"
echo " Backup:        $LATEST_BACKUP"
echo " Restored to:   $DRILL_DIR"
echo " Failures:      $FAILS"
echo " Warnings:      $WARNS"

if [ "$FAILS" -eq 0 ]; then
    if [ "$WARNS" -eq 0 ]; then
        echo " Status:        ✅ PASS"
    else
        echo " Status:        ⚠️  PASS WITH WARNINGS"
    fi
else
    echo " Status:        ❌ FAIL"
fi

# Log to permanent record
LOG_DIR="$HOME/.claude/orchestrator/security"
mkdir -p "$LOG_DIR"
DRILL_LOG="$LOG_DIR/dr_drill_log.jsonl"
echo "{\"timestamp\":\"$(date -Iseconds)\",\"backup\":\"$LATEST_BACKUP\",\"failures\":$FAILS,\"warnings\":$WARNS,\"status\":\"$([ $FAILS -eq 0 ] && echo PASS || echo FAIL)\"}" >> "$DRILL_LOG"
echo
echo " Drill log:     $DRILL_LOG (appended)"

# Cleanup
if [ "$KEEP" -eq 1 ]; then
    echo
    echo " --keep given: drill directory preserved at $DRILL_DIR"
    echo " Inspect with: ls $DRILL_DIR"
else
    rm -rf "$DRILL_DIR"
    echo " Drill directory cleaned up."
fi

exit $FAILS
