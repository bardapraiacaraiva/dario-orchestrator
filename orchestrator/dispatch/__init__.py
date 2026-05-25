"""DARIO dispatch — engine, CoT trace, model router, semantic routing.

Moved here 2026-05-25 from top-level (Recommendation #2: Phase 4 stage 4).
Public API preserved; callers updated to use `from dispatch.X import Y`.

Note: webhook_dispatcher.py is NOT in this package — it routes events to
external webhooks, not dispatcher work.
"""
