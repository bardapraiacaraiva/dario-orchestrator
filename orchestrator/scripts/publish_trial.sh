#!/bin/bash
# scripts/publish_trial.sh — Fix 3 trial repo trimmer
# ==============================================================================
# Produces a "trial-safe" snapshot of master and force-pushes it to origin.
# The full repo (`full` remote, private VIP) keeps everything intact.
#
# Trim policy:
#   - Crown-jewel intelligence modules → REPLACED by import-time stubs
#   - Crown-jewel subdirs (upgrades/, dream/, intelligence/) → REPLACED by
#     a single __init__.py shim that raises ImportError with purchase link
#   - Everything else (skills, configs, license_manager, runtime, basic
#     plumbing) → unchanged
#
# Usage:
#   bash scripts/publish_trial.sh                # dry-run by default
#   bash scripts/publish_trial.sh --execute      # actually force-push
#   bash scripts/publish_trial.sh --execute --no-tag   # skip tag
#
# After execution, the public trial repo on GitHub has fewer files —
# specifically, the modules an attacker would need to clone the
# intelligence layer of DARIO.
# ==============================================================================

set -euo pipefail
cd "$(dirname "$0")/../.."   # → ~/.claude

EXECUTE=0
NO_TAG=0
for arg in "$@"; do
    case "$arg" in
        --execute) EXECUTE=1 ;;
        --no-tag) NO_TAG=1 ;;
        --help|-h)
            sed -n '1,30p' "$0"
            exit 0 ;;
    esac
done

echo "═══ Fix 3: Publish trimmed trial repo to origin ═══"
echo "  Working dir: $(pwd)"
echo "  Execute:     $([ $EXECUTE -eq 1 ] && echo YES || echo 'DRY-RUN (use --execute)')"
echo ""

# ─── Crown-jewel files (top-level .py) to STUB OUT ───────────────────────────
STUB_FILES=(
    "orchestrator/dispatch_engine.py"
    "orchestrator/dispatch_cot.py"
    "orchestrator/golden_eval.py"
    "orchestrator/qvalue_memory_wire.py"
    "orchestrator/episode_promoter.py"
    "orchestrator/semantic_dispatch.py"
    "orchestrator/confidence_engine.py"
    "orchestrator/executor.py"
    "orchestrator/chain_graph.py"
    "orchestrator/dynamic_branch.py"
    "orchestrator/synaptic_update.py"
    "orchestrator/prompt_hints.py"
    "orchestrator/ethical_gate.py"
)

# ─── Crown-jewel subdirs to REPLACE with stub __init__.py ────────────────────
STUB_DIRS=(
    "orchestrator/upgrades"
    "orchestrator/dream"
)

# ─── Stub content for any crown-jewel file ────────────────────────────────────
read -r -d '' STUB_CONTENT_FILE <<'EOF' || true
"""Crown-jewel module — TRIAL VERSION (stub).

This file is a stub in the public trial repository. The actual
implementation is part of the proprietary VIP build of the DARIO
Orchestrator and is delivered to paying customers via the private
`dario-orchestrator-full` repository.

Trial users running the showcase can see the orchestrator's behaviour
through the dispatch wrapper, but cannot directly import or read the
intelligence implementation.

To unlock the full module:
    1. Purchase a license key (any tier from Professional upwards)
       at barda@automationsolutionai.com
    2. Re-install with the VIP repo:
         DARIO_GH_TOKEN=ghp_xxx npx \\
             github:bardapraiacaraiva/dario-orchestrator-installer \\
             --key DARIO-XXXX-XXXX-XXXX-PRO

See LICENSE for terms. Reverse-engineering this stub or attempting to
re-create the intelligence by reading the orchestration wrapper is a
breach of the Evaluation License (Section 3.b — derivative works).
"""

import sys

_MODULE_NAME = __name__.rsplit(".", 1)[-1]
raise ImportError(
    f"{_MODULE_NAME!r} is a VIP-only module. "
    "Buy a Professional or Enterprise license to unlock it. "
    "Contact: barda@automationsolutionai.com"
)
EOF

read -r -d '' STUB_CONTENT_DIR <<'EOF' || true
"""Crown-jewel package — TRIAL VERSION (stub).

This entire package is replaced by a stub in the public trial repository.
The actual implementation lives in the private `dario-orchestrator-full`
repo and is delivered to paying customers via the VIP installer flow.

Buy a license to unlock: barda@automationsolutionai.com
See LICENSE for terms.
"""
raise ImportError(
    "This package is VIP-only in the trial build. "
    "Buy a license: barda@automationsolutionai.com"
)
EOF

# ─── Create temporary worktree to do the trim ────────────────────────────────
TRIM_DIR=$(mktemp -d)
echo "Creating detached worktree at: $TRIM_DIR"
# Use --detach so we don't clash with the master branch already checked out
# in the main working directory.
git worktree add --detach "$TRIM_DIR" master >/dev/null

cleanup() {
    cd ~ 2>/dev/null || cd /tmp
    git worktree remove "$TRIM_DIR" --force >/dev/null 2>&1 || true
}
trap cleanup EXIT

cd "$TRIM_DIR"
echo ""
echo "=== Stubbing crown-jewel files ==="
for f in "${STUB_FILES[@]}"; do
    if [ -f "$f" ]; then
        # Preserve a small shim that raises on import
        echo "$STUB_CONTENT_FILE" > "$f"
        echo "  stubbed: $f"
    fi
done

echo ""
echo "=== Stubbing crown-jewel subdirs ==="
for d in "${STUB_DIRS[@]}"; do
    if [ -d "$d" ]; then
        # Wipe contents, leave only an __init__.py stub
        rm -rf "$d"
        mkdir -p "$d"
        echo "$STUB_CONTENT_DIR" > "$d/__init__.py"
        echo "  stubbed: $d/ (replaced with __init__.py shim)"
    fi
done

# ─── Stage + commit ──────────────────────────────────────────────────────────
echo ""
echo "=== Staging trim ==="
git add -A
N_CHANGED=$(git diff --cached --name-only | wc -l)
echo "  $N_CHANGED files changed"

if [ "$N_CHANGED" -eq 0 ]; then
    echo "Nothing to trim — exiting."
    exit 0
fi

if [ $EXECUTE -eq 0 ]; then
    echo ""
    echo "DRY-RUN — would commit + force-push the above changes to origin/master."
    echo "Re-run with --execute to actually publish."
    git diff --cached --stat
    exit 0
fi

git commit -m "trial: crown-jewel modules replaced with import-time stubs (Fix 3)"
echo ""
echo "=== Force-pushing trimmed snapshot to origin/master ==="
git push origin HEAD:master --force

if [ $NO_TAG -eq 0 ]; then
    TAG="trial-v$(date +%Y%m%d)-$(git rev-parse --short HEAD)"
    git tag -a "$TAG" -m "Trial snapshot — Fix 3 trim of crown-jewels"
    git push origin "$TAG"
    echo "  Tagged as: $TAG"
fi

echo ""
echo "✅ Fix 3 published. Origin (public trial) now serves the trimmed snapshot."
echo "✅ Full (private VIP) remains unchanged — push to it from master as usual."
