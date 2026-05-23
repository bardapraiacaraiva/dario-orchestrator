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
