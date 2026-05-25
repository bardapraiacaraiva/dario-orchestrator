"""Compatibility shim — autodiag_runner.py relocated to runners/autodiag.py (Onda 2 #2).

Subprocess callers (`python autodiag_runner.py ...`) keep working.
Importers should switch to `from runners.autodiag import ...` directly.
This shim will be removed once all callers in tree have been migrated.
"""

import sys

from runners.autodiag import main

if __name__ == "__main__":
    sys.exit(main())
