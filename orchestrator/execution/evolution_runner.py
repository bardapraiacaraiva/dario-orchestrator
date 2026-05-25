"""Compatibility shim — evolution_runner.py relocated to runners/evolution.py (Onda 2 #2).

After Phase 4 stage 9 (2026-05-25), this shim lives at
orchestrator/execution/evolution_runner.py. When called as a script,
sys.path[0] is execution/ rather than orchestrator/, so we add the
orchestrator dir so `from runners.evolution` resolves.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from runners.evolution import main

if __name__ == "__main__":
    sys.exit(main())
