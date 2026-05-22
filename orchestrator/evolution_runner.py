"""Compatibility shim — evolution_runner.py relocated to runners/evolution.py (Onda 2 #2)."""

import sys

from runners.evolution import main

if __name__ == "__main__":
    sys.exit(main())
