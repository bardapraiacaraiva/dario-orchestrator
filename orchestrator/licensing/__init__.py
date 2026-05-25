"""DARIO licensing — auth, license_client, license_guard, license_manager.

Moved here 2026-05-25 from top-level (Recommendation #2: Phase 4 stage 3).
All 4 modules retain their original public API; callers just need to update
the import path from `from license_X import Y` to `from licensing.license_X import Y`.

Note: `license_guard.enforce_or_exit()` is called dynamically from ~17 sites
across the orchestrator (always inside try/except ImportError blocks for
fail-open dev behavior). Each call site updated atomically with this move.
"""
