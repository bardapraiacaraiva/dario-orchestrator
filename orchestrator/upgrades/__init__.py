"""DARIO Orchestrator — upgrade packs (Onda 2 #1, Fase 1).

Each module here was previously a top-level `X_upgrades.py` that organically
accumulated over sprints. They are now collected in this package without
internal splitting (yet). Each pack exposes one `init_X_upgrades(app)` entry
point that registers its FastAPI routes/middleware.

Phase 1 (this commit): structural relocation only — same code, new path.
Phase 2 (future): split each pack into thematic modules under
`upgrades/<pack>/<feature>.py` so individual features can be imported
without dragging in the whole pack.

Module      → init function
─────────────────────────────────────────────────
upgrades.core            init_core_upgrades(app, db)
upgrades.execution       init_execution_upgrades(app)
upgrades.intelligence    init_intelligence_upgrades(app)
upgrades.quality         init_quality_upgrades(app)
upgrades.state           init_state_upgrades(app)
upgrades.observability   init_observability_upgrades(app)
upgrades.security        init_security_upgrades(app)
upgrades.financial       init_financial_upgrades(app)
"""

from upgrades.core import init_core_upgrades
from upgrades.execution import init_execution_upgrades
from upgrades.financial import init_financial_upgrades
from upgrades.intelligence import init_intelligence_upgrades
from upgrades.observability import init_observability_upgrades
from upgrades.quality import init_quality_upgrades
from upgrades.security import init_security_upgrades
from upgrades.state import init_state_upgrades

__all__ = [
    "init_core_upgrades",
    "init_execution_upgrades",
    "init_financial_upgrades",
    "init_intelligence_upgrades",
    "init_observability_upgrades",
    "init_quality_upgrades",
    "init_security_upgrades",
    "init_state_upgrades",
]
