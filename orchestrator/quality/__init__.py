"""DARIO quality — eval, scoring, rubrics, judges.

Moved here 2026-05-25 from top-level (Recommendation #2: Phase 4 stage 5).
This directory previously held only YAML/JSONL artefacts (skill-metrics,
api_spend_log, polished_production_runs, etc.). Now it also hosts the
Python quality engines.

Public API preserved; callers use `from quality.X import Y`.

Subprocess callers (e.g., `run_engine("score_bundle.py", ...)`) now use
the path `quality/score_bundle.py`.
"""
