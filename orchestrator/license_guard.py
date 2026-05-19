#!/usr/bin/env python3
"""
DARIO License Guard — Centralised enforcement helpers
======================================================
v11.1+ hardening (2026-05-19).

Before this module, license enforcement existed in license_manager.py but
was only called by 4/37 endpoints of runtime.py. All CLI scripts and the
18 cognitive modules bypassed it entirely — trial users could continue
using the system indefinitely outside the runtime server.

This module exposes three reusable mechanisms:

  1. `enforce_or_exit(component)` — CLI guard. Call at the top of a
     standalone script's main(). Prints message and sys.exit(2) on expired.

  2. `@require_license(component)` decorator — Function guard. Wrap any
     function that should refuse to run on expired trial.

  3. `fastapi_middleware(app)` — FastAPI middleware. Guards ALL endpoints
     except a whitelist (/health, /license/*, /docs, /openapi.json,
     /redoc). Returns 402 Payment Required on expired.

Bypass for development:
  Set `DARIO_LICENSE_BYPASS=1` AND ensure `~/.claude/orchestrator/dev.flag`
  exists. This double-gate prevents casual bypass — accidental env var
  alone won't work, and creating the dev.flag is a deliberate act.

CLI:
    python license_guard.py --check         Status check (same as license_manager --check but quiet)
    python license_guard.py --test-bypass   Show whether bypass is active
"""

import argparse
import functools
import json
import os
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
DEV_FLAG = ORCH_DIR / "dev.flag"

# Endpoints that should NEVER be license-gated in the FastAPI middleware
WHITELIST_PATHS = {
    "/health", "/healthz", "/ready", "/status",
    "/license", "/license/", "/license/status", "/license/activate",
    "/docs", "/openapi.json", "/redoc",
    "/", "/favicon.ico",
}


def _bypass_active() -> bool:
    """Bypass requires BOTH env var AND dev.flag file. Single-gate would be
    too easy to flip accidentally."""
    env = os.environ.get("DARIO_LICENSE_BYPASS") == "1"
    flag = DEV_FLAG.exists()
    return env and flag


def _check() -> dict:
    """Wrapper around license_manager.check_license — never crash on import."""
    try:
        sys.path.insert(0, str(ORCH_DIR))
        from license_manager import check_license
        return check_license()
    except Exception as e:
        # If license_manager can't load, fail-CLOSED (safer default)
        return {"valid": False, "reason": f"license_manager unavailable: {e}",
                "tier": "unknown", "action": "investigate"}


def is_valid() -> bool:
    """Lightweight boolean check. Honours bypass."""
    if _bypass_active():
        return True
    return _check().get("valid", False)


def enforce_or_exit(component: str = "orchestrator", quiet: bool = False) -> None:
    """Call at start of CLI scripts. Exits with code 2 on invalid license.

    Usage:
        from license_guard import enforce_or_exit
        enforce_or_exit("executor")
        # ... rest of script ...
    """
    if _bypass_active():
        return  # dev mode

    lic = _check()
    if lic.get("valid"):
        return

    if not quiet:
        tier = lic.get("tier", "unknown")
        reason = lic.get("reason", "Invalid")
        msg = lic.get("message", "")
        action = lic.get("action", "")

        sys.stderr.write(
            f"\n┌─────────────────────────────────────────────────────────────┐\n"
            f"│ DARIO LICENSE — {component:<40s}    │\n"
            f"├─────────────────────────────────────────────────────────────┤\n"
            f"│ Status:  BLOCKED (tier: {tier:<10s})                         │\n"
            f"│ Reason:  {reason:<50s} │\n"
        )
        if msg:
            sys.stderr.write(f"│                                                             │\n")
            sys.stderr.write(f"│ {msg[:59]:<59s} │\n")
        sys.stderr.write(
            f"├─────────────────────────────────────────────────────────────┤\n"
            f"│ To activate VIP:                                            │\n"
            f"│   python ~/.claude/orchestrator/license_manager.py \\        │\n"
            f"│     --activate DARIO-XXXX-XXXX-XXXX-PRO                     │\n"
            f"│                                                             │\n"
            f"│ To start a fresh 7-day trial:                               │\n"
            f"│   python ~/.claude/orchestrator/license_manager.py \\        │\n"
            f"│     --init-trial                                            │\n"
            f"└─────────────────────────────────────────────────────────────┘\n\n"
        )
    sys.exit(2)


def require_license(component: str = "function"):
    """Decorator for functions. Skips execution if license invalid.

    Usage:
        from license_guard import require_license

        @require_license("executor.run_task")
        def run_task(...):
            ...
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if not is_valid():
                lic = _check()
                raise RuntimeError(
                    f"License invalid — {component} refused. "
                    f"Reason: {lic.get('reason', 'unknown')}. "
                    f"Run: python ~/.claude/orchestrator/license_manager.py --activate <KEY>"
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def fastapi_middleware(app):
    """Add a FastAPI middleware that guards all non-whitelisted endpoints.

    Usage in runtime.py:
        from license_guard import fastapi_middleware
        fastapi_middleware(app)
    """
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @app.middleware("http")
    async def _license_middleware(request: Request, call_next):
        # Whitelist: health, license endpoints, docs
        path = request.url.path
        # Match exact whitelist
        if path in WHITELIST_PATHS:
            return await call_next(request)
        # Match prefix /license/*
        if path.startswith("/license/"):
            return await call_next(request)
        # Match docs/openapi/redoc anything
        if path.startswith(("/docs", "/openapi", "/redoc")):
            return await call_next(request)

        # Bypass for dev
        if _bypass_active():
            return await call_next(request)

        # Enforce
        lic = _check()
        if not lic.get("valid"):
            return JSONResponse(
                status_code=402,  # Payment Required — semantically correct
                content={
                    "error": "License expired or invalid",
                    "tier": lic.get("tier", "unknown"),
                    "reason": lic.get("reason", "Invalid"),
                    "action": lic.get("action", "activate_key"),
                    "message": lic.get("message", ""),
                    "blocked_path": path,
                    "activation": "python license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO",
                },
            )

        # Attach tier to request state for downstream use
        request.state.license = lic
        return await call_next(request)

    return app


def main():
    p = argparse.ArgumentParser(description="DARIO License Guard")
    p.add_argument("--check", action="store_true", help="Quiet status check (exit code)")
    p.add_argument("--test-bypass", action="store_true", help="Report bypass status")
    p.add_argument("--enforce", help="Test enforce_or_exit for given component")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.test_bypass:
        active = _bypass_active()
        info = {
            "bypass_active": active,
            "env_set": os.environ.get("DARIO_LICENSE_BYPASS") == "1",
            "dev_flag_present": DEV_FLAG.exists(),
            "dev_flag_path": str(DEV_FLAG),
            "instructions": "Both env var AND dev.flag required. Set: DARIO_LICENSE_BYPASS=1 + touch dev.flag",
        }
        print(json.dumps(info, indent=2) if args.json else
              "\n".join(f"  {k}: {v}" for k, v in info.items()))
        return 0

    if args.check:
        lic = _check()
        if args.json:
            print(json.dumps(lic, indent=2))
        else:
            valid = lic.get("valid", False)
            tier = lic.get("tier", "?")
            print(f"  {tier.upper()}: {'VALID' if valid else 'INVALID'}")
            if not valid:
                print(f"  Reason: {lic.get('reason', '?')}")
        return 0 if lic.get("valid") else 2

    if args.enforce:
        enforce_or_exit(args.enforce)
        # If we reach here, license valid
        print(f"License OK for {args.enforce}")
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
