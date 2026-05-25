"""DARIO core — runtime, state machine, task management, db, lifecycle.

These modules form the orchestrator runtime spine. Most are imported
heavily by the rest of the codebase via subprocess (`run_engine(...)`)
rather than direct python imports.
"""
