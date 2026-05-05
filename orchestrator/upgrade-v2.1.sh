#!/usr/bin/env bash
# ============================================================================
# DARIO Orchestrator — Upgrade to v2.1-ALIVE (Self-Evolving Runtime)
# ============================================================================
# For users who already have the orchestrator installed (v1.x).
# Adds: Evolution Engine, Runtime Service, new governance configs.
#
# Usage:
#   bash upgrade-v2.1.sh                  # Full upgrade (configs + runtime)
#   bash upgrade-v2.1.sh --configs-only   # Only YAML configs (no runtime)
#   bash upgrade-v2.1.sh --runtime-only   # Only Python runtime service
#   bash upgrade-v2.1.sh --check          # Verify upgrade status
#
# Requirements:
#   - Existing orchestrator installation (~/.claude/orchestrator/)
#   - Python 3.11+ (for runtime)
#   - PostgreSQL running locally (for runtime)
#
# Compatible with: Windows (Git Bash), macOS, Linux
# ============================================================================

set -euo pipefail

VERSION="2.1.0"
UPGRADE_NAME="v2.1-ALIVE"

# --- Colors ---
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

# --- Paths ---
ORCH_DIR="${HOME}/.claude/orchestrator"
SKILLS_DIR="${HOME}/.claude/skills"
RUNTIME_DIR=""

# Detect platform for runtime location
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) RUNTIME_DIR="/c/dario-orch" ;;
    *)                     RUNTIME_DIR="${HOME}/dario-orch" ;;
esac

# --- Helpers ---
log() { echo -e "${GREEN}[UPGRADE]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
header() { echo -e "\n${BOLD}${CYAN}═══ $1 ═══${NC}\n"; }

# --- Pre-flight ---
preflight() {
    header "Pre-flight Checks"

    # Check existing installation
    if [ ! -d "$ORCH_DIR" ]; then
        err "Orchestrator not found at $ORCH_DIR. Run install.sh first."
    fi
    log "Existing orchestrator found: $ORCH_DIR"

    # Check company.yaml exists
    if [ ! -f "$ORCH_DIR/company.yaml" ]; then
        err "company.yaml not found. Installation may be corrupted."
    fi
    log "company.yaml present"

    # Check Python
    if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
        warn "Python not found. Runtime service will not be installed."
        warn "Install Python 3.11+ and re-run with --runtime-only"
        SKIP_RUNTIME=true
    else
        PYTHON=$(command -v python3 || command -v python)
        PY_VER=$($PYTHON --version 2>&1 | grep -oP '\d+\.\d+')
        log "Python found: $PY_VER"
        SKIP_RUNTIME=false
    fi

    # Check PostgreSQL
    if ! command -v psql &>/dev/null; then
        if [ "$SKIP_RUNTIME" = false ]; then
            warn "psql not found. Checking if PostgreSQL is reachable..."
            if $PYTHON -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1',5432)); s.close()" 2>/dev/null; then
                log "PostgreSQL reachable on port 5432"
            else
                warn "PostgreSQL not reachable. Runtime needs DB connection."
                SKIP_RUNTIME=true
            fi
        fi
    else
        log "PostgreSQL tools available"
    fi

    echo ""
}

# --- Upgrade Configs ---
upgrade_configs() {
    header "Upgrading Orchestrator Configs"

    # Create new directories
    mkdir -p "$ORCH_DIR/evolution/journal"
    mkdir -p "$ORCH_DIR/evolution/mutations"
    mkdir -p "$ORCH_DIR/evolution/rules"
    mkdir -p "$ORCH_DIR/evolution/checkpoints"
    log "Evolution directories created"

    # Download new config files from GitHub
    REPO_RAW="https://raw.githubusercontent.com/bardapraiacaraiva/dario-orchestrator/master/orchestrator"

    configs=(
        "autodiag.yaml"
        "composite_modes.yaml"
        "evolution_engine.yaml"
        "fallback_matrix.yaml"
        "manifesto.yaml"
        "operational_states.yaml"
        "synaptic_weights.yaml"
    )

    for cfg in "${configs[@]}"; do
        if [ -f "$ORCH_DIR/$cfg" ]; then
            # Backup existing
            cp "$ORCH_DIR/$cfg" "$ORCH_DIR/$cfg.bak-$(date +%Y%m%d)" 2>/dev/null || true
            log "Backed up existing: $cfg"
        fi
        # Download new version
        if curl -sf "$REPO_RAW/$cfg" -o "$ORCH_DIR/$cfg" 2>/dev/null; then
            log "Downloaded: $cfg"
        else
            warn "Could not download $cfg — using local if exists"
        fi
    done

    # Create CHANGELOG if not exists
    if [ ! -f "$ORCH_DIR/evolution/CHANGELOG.md" ]; then
        cat > "$ORCH_DIR/evolution/CHANGELOG.md" << 'CHANGELOG'
# DARIO Evolution Changelog

## Generation 1 — Upgrade Date
### System Upgraded to v2.1-ALIVE
- Evolution Engine installed
- Mutation Engine enabled
- AutoDiag, Fallback Matrix, Manifesto, Composite Modes
- Runtime Service (if Python + PostgreSQL available)
CHANGELOG
        log "CHANGELOG created"
    fi

    # Upgrade dario-evolve skill
    EVOLVE_DIR="$SKILLS_DIR/dario-evolve"
    mkdir -p "$EVOLVE_DIR"
    if curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/dario-orchestrator/master/skills/dario-evolve/SKILL.md" -o "$EVOLVE_DIR/SKILL.md" 2>/dev/null; then
        log "Skill dario-evolve installed"
    else
        warn "Could not download dario-evolve skill"
    fi

    # Update orchestrator skill
    ORCH_SKILL="$SKILLS_DIR/dario-orchestrator/SKILL.md"
    if curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/dario-orchestrator/master/skills/dario-orchestrator/SKILL.md" -o "$ORCH_SKILL" 2>/dev/null; then
        log "dario-orchestrator SKILL.md updated to v2.1"
    fi

    # Update quality scorer
    QUALITY_SKILL="$SKILLS_DIR/lucas-quality/SKILL.md"
    if curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/dario-orchestrator/master/skills/lucas-quality/SKILL.md" -o "$QUALITY_SKILL" 2>/dev/null; then
        log "lucas-quality SKILL.md updated (weighted scoring)"
    fi

    # Update heartbeat
    HB_SKILL="$SKILLS_DIR/lucas-heartbeat/SKILL.md"
    if curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/dario-orchestrator/master/skills/lucas-heartbeat/SKILL.md" -o "$HB_SKILL" 2>/dev/null; then
        log "lucas-heartbeat SKILL.md updated (AutoDiag + Evolution)"
    fi

    echo -e "\n${GREEN}Config upgrade complete.${NC}"
}

# --- Install Runtime ---
install_runtime() {
    if [ "$SKIP_RUNTIME" = true ]; then
        warn "Skipping runtime installation (Python or PostgreSQL not available)"
        return
    fi

    header "Installing Runtime Service"

    mkdir -p "$RUNTIME_DIR"
    cd "$RUNTIME_DIR"

    # Clone runtime files from repo
    if curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/orchestrator-framework/master/run.py" -o run.py &&
       curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/orchestrator-framework/master/pyproject.toml" -o pyproject.toml &&
       curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/orchestrator-framework/master/pytest.ini" -o pytest.ini; then
        log "Core files downloaded"
    else
        err "Could not download runtime files from GitHub"
    fi

    # Download source
    mkdir -p src/routers src/services config migrations tests scripts

    SRC_BASE="https://raw.githubusercontent.com/bardapraiacaraiva/orchestrator-framework/master/runtime-src"
    for f in __init__.py main.py config.py database.py models.py; do
        curl -sf "$SRC_BASE/$f" -o "src/$f" 2>/dev/null || true
    done
    for f in __init__.py health.py tasks.py hooks.py evolution.py budget.py weights.py dashboard.py; do
        curl -sf "$SRC_BASE/routers/$f" -o "src/routers/$f" 2>/dev/null || true
    done
    for f in __init__.py task_sync.py fitness.py state_machine.py autodiag.py mutation_engine.py crystallizer.py weekly_evolution.py; do
        curl -sf "$SRC_BASE/services/$f" -o "src/services/$f" 2>/dev/null || true
    done
    curl -sf "https://raw.githubusercontent.com/bardapraiacaraiva/orchestrator-framework/master/runtime-migrations/001_initial_schema.sql" -o "migrations/001_initial_schema.sql" 2>/dev/null || true
    log "Source files downloaded"

    # Create .env config
    if [ ! -f "config/.env" ]; then
        cat > "config/.env" << ENV
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@127.0.0.1:5432/dario_kb
RAG_ENGINE_URL=http://localhost:8420
ORCH_HOST=0.0.0.0
ORCH_PORT=8421
ORCHESTRATOR_DIR=${ORCH_DIR}
SKILLS_DIR=${SKILLS_DIR}
LOG_LEVEL=INFO
MICRO_PULSE_SECONDS=300
SESSION_PULSE_SECONDS=1800
ENV
        warn "EDIT config/.env — set your DATABASE_URL password!"
    fi

    # Create venv and install deps
    log "Creating Python virtual environment..."
    $PYTHON -m venv .venv

    if [ "$(uname -s)" = "MINGW"* ] || [ "$(uname -s)" = "MSYS"* ]; then
        PIP=".venv/Scripts/pip"
    else
        PIP=".venv/bin/pip"
    fi

    $PIP install -q fastapi uvicorn[standard] "psycopg[binary,pool]" pydantic-settings httpx ruamel.yaml apscheduler
    log "Dependencies installed"

    # Create start script
    cat > "start.sh" << 'START'
#!/usr/bin/env bash
cd "$(dirname "$0")"
if [ -f ".venv/bin/python" ]; then
    .venv/bin/python run.py
elif [ -f ".venv/Scripts/python.exe" ]; then
    .venv/Scripts/python run.py
fi
START
    chmod +x start.sh
    log "Start script created: $RUNTIME_DIR/start.sh"

    echo -e "\n${GREEN}Runtime installed at: $RUNTIME_DIR${NC}"
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Edit $RUNTIME_DIR/config/.env (set DB password)"
    echo "  2. Run: cd $RUNTIME_DIR && bash start.sh"
    echo "  3. Test: curl http://localhost:8421/health"
}

# --- Verify ---
verify() {
    header "Verification"

    local score=0
    local total=0

    check() {
        total=$((total + 1))
        if [ -f "$1" ]; then
            log "OK: $2"
            score=$((score + 1))
        else
            warn "MISSING: $2 ($1)"
        fi
    }

    check "$ORCH_DIR/manifesto.yaml" "Manifesto (governance)"
    check "$ORCH_DIR/evolution_engine.yaml" "Evolution Engine"
    check "$ORCH_DIR/operational_states.yaml" "Operational States"
    check "$ORCH_DIR/autodiag.yaml" "AutoDiag config"
    check "$ORCH_DIR/fallback_matrix.yaml" "Fallback Matrix"
    check "$ORCH_DIR/synaptic_weights.yaml" "Synaptic Weights"
    check "$ORCH_DIR/composite_modes.yaml" "Composite Modes"
    check "$ORCH_DIR/company.yaml" "Company hierarchy"
    check "$SKILLS_DIR/dario-orchestrator/SKILL.md" "Orchestrator skill"
    check "$SKILLS_DIR/dario-evolve/SKILL.md" "Evolution skill"
    check "$SKILLS_DIR/lucas-quality/SKILL.md" "Quality scorer"
    check "$SKILLS_DIR/lucas-heartbeat/SKILL.md" "Heartbeat engine"

    if [ -d "$RUNTIME_DIR" ] && [ -f "$RUNTIME_DIR/run.py" ]; then
        log "OK: Runtime service installed"
        score=$((score + 1))
    else
        warn "Runtime service not installed (optional)"
    fi
    total=$((total + 1))

    echo ""
    echo -e "${BOLD}Score: $score/$total${NC}"
    if [ $score -eq $total ]; then
        echo -e "${GREEN}${BOLD}UPGRADE COMPLETE — v2.1-ALIVE fully operational${NC}"
    elif [ $score -ge $((total - 2)) ]; then
        echo -e "${YELLOW}UPGRADE MOSTLY COMPLETE — minor items missing${NC}"
    else
        echo -e "${RED}UPGRADE INCOMPLETE — run again or check errors${NC}"
    fi
}

# --- Main ---
main() {
    echo -e "${BOLD}${CYAN}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║  DARIO Orchestrator — Upgrade to v2.1-ALIVE        ║"
    echo "║  Self-Evolving Runtime + Evolution Engine           ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    SKIP_RUNTIME=false
    MODE="full"

    # Parse args
    for arg in "$@"; do
        case $arg in
            --configs-only) MODE="configs" ;;
            --runtime-only) MODE="runtime" ;;
            --check)        MODE="check" ;;
            *)              ;;
        esac
    done

    case $MODE in
        check)
            verify
            ;;
        configs)
            preflight
            upgrade_configs
            verify
            ;;
        runtime)
            preflight
            install_runtime
            ;;
        full)
            preflight
            upgrade_configs
            install_runtime
            verify
            ;;
    esac

    echo ""
    log "Done. Version: $UPGRADE_NAME"
}

main "$@"
