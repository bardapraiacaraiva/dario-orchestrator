"""Compatibility shim — api_executor.py relocated to providers/anthropic.py (Onda 2 #2).

Renaming makes intent obvious: this file is the Anthropic SDK wrapper used
to invoke Claude directly. Future provider wrappers (OpenAI, Gemini)
should follow the same pattern: providers/<vendor>.py.
"""

import sys

from providers.anthropic import main

if __name__ == "__main__":
    sys.exit(main())
