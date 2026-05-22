"""Runners package — cron-style cycles that are NOT the request-path executor.

Naming clarification (Onda 2 #2): "executor" was overloaded for both
- the per-task lifecycle (`executor.py` — kept at root, request path)
- and standalone cycles (autodiag, evolution — moved here)

Modules:
    runners.autodiag    System health-check runner (was autodiag_runner.py)
    runners.evolution   Learning + mutation cycle runner (was evolution_runner.py)
"""
