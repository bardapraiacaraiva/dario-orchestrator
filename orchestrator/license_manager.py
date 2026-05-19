#!/usr/bin/env python3
"""
DARIO License Manager — Trial enforcement + VIP key activation.
================================================================
Public install (pip/npx) gets 7-day trial with limited features.
VIP key unlocks full access permanently.

Tiers:
    TRIAL   — 7 days, 3 engines, 1 parallel, no API execution, no evolution
    PRO     — unlimited, all engines, 3 parallel, API execution, evolution
    ENTERPRISE — unlimited, all engines, 5 parallel, multi-tenant, federation

Usage:
    python license_manager.py --status          # Show current license
    python license_manager.py --activate KEY    # Activate VIP key
    python license_manager.py --init-trial      # Initialize 7-day trial
    python license_manager.py --check           # Check if license valid (exit 0=ok, 1=expired)
    python license_manager.py --generate-key TIER EMAIL  # Generate VIP key (admin only)
    python license_manager.py --json

Key format: DARIO-XXXX-XXXX-XXXX-TIER
    DARIO-A1B2-C3D4-E5F6-PRO
    DARIO-G7H8-I9J0-K1L2-ENT
"""

import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
LICENSE_FILE = ORCH_DIR / "license.json"

# MASTER_SECRET source priority:
#   1. Env var DARIO_MASTER_SECRET (recommended for production)
#   2. ~/.claude/orchestrator/.master_secret file (admin local)
#   3. Placeholder fallback (signs nothing useful — repo-safe)
#
# Whoever holds the real MASTER_SECRET can mint keys. Keep it private.
# Repo distributions ship the placeholder — keys minted with placeholder
# won't validate on installs that have the real secret, and vice versa.
def _load_master_secret() -> bytes:
    env = os.environ.get("DARIO_MASTER_SECRET")
    if env:
        return env.encode("utf-8")
    secret_file = ORCH_DIR / ".master_secret"
    if secret_file.exists():
        try:
            return secret_file.read_text(encoding="utf-8").strip().encode("utf-8")
        except Exception:
            pass
    return b"DARIO-PLACEHOLDER-NOT-FOR-PRODUCTION-REPLACE-IN-ENV"


MASTER_SECRET = _load_master_secret()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("license")

TIERS = {
    "trial": {
        "name": "Trial (7 dias — acesso completo DARIO + DIVA + LEX-BR)",
        "duration_days": 7,
        "max_parallel": 3,
        "engines_allowed": "all",
        # LEX-BR — trial dá acesso aos 15 skills + 3 MCP servers + 50 peças
        # Após 7 dias: tudo bloqueado até VIP key ou expira definitivamente
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf"],
        "lex_br_pieces_month": 50,
        "features": {
            "api_execution": True,
            "evolution_engine": True,
            "llm_judge": True,
            "predictive_dispatch": True,
            "chain_executor": True,
            "multi_tenancy": True,
            "federation": True,
            "plugins": True,
            "adaptive_rubrics": True,
            "dashboard": True,
            "task_templates": True,
            # LEX-BR features acessíveis durante trial (acesso completo)
            "lex_br_agent": True,
            "oab_205_gate": True,
            "lgpd_marker": True,
            "audit_oab": True,
            "lex_memory_multi_client": True,
            "dms_integration": True,
        },
    },
    "pro": {
        "name": "Professional",
        "duration_days": None,  # Permanent
        "max_parallel": 3,
        "engines_allowed": "all",
        "features": {
            "api_execution": True,
            "evolution_engine": True,
            "llm_judge": True,
            "predictive_dispatch": True,
            "chain_executor": True,
            "multi_tenancy": False,
            "federation": False,
            "plugins": True,
            "adaptive_rubrics": True,
            "dashboard": True,
            "task_templates": True,
        },
    },
    "enterprise": {
        "name": "Enterprise",
        "duration_days": None,
        "max_parallel": 5,
        "engines_allowed": "all",
        "features": {
            "api_execution": True,
            "evolution_engine": True,
            "llm_judge": True,
            "predictive_dispatch": True,
            "chain_executor": True,
            "multi_tenancy": True,
            "federation": True,
            "plugins": True,
            "adaptive_rubrics": True,
            "dashboard": True,
            "task_templates": True,
        },
    },
    # LEX-BR tiers (v11.2.0+ — agente Direito BR)
    "lex_solo": {
        "name": "LEX-BR Solo (Advogado individual)",
        "price_brl_month": 297,
        "duration_days": None,
        "max_parallel": 2,
        "engines_allowed": "lex_br_subset",
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf"],
        "lex_br_pieces_month": 50,
        "features": {
            "api_execution": True, "llm_judge": True, "chain_executor": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "lex_br_agent": True,
            "oab_205_gate": True, "lgpd_marker": True, "audit_oab": True,
            "evolution_engine": False, "predictive_dispatch": False,
            "multi_tenancy": False, "federation": False,
        },
    },
    "lex_office": {
        "name": "LEX-BR Office (Escritório < 10 advogados)",
        "price_brl_month": 997,
        "duration_days": None,
        "max_parallel": 3,
        "engines_allowed": "lex_br_full",
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf", "anpd", "receita_federal"],
        "lex_br_pieces_month": 200,
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "lex_br_agent": True,
            "oab_205_gate": True, "lgpd_marker": True, "audit_oab": True,
            "lex_memory_multi_client": True, "dms_integration": True,
            "multi_tenancy": False, "federation": False,
        },
    },
    "lex_enterprise": {
        "name": "LEX-BR Enterprise (Escritório/Dept. jurídico)",
        "price_brl_month_from": 4000,
        "duration_days": None,
        "max_parallel": 5,
        "engines_allowed": "all",
        "lex_br_skills_count": 15,
        "lex_br_mcp_servers": ["jusbrasil", "cnj_datajud", "stf", "diario_oficial",
                               "anpd", "receita_federal", "advbox", "projuris"],
        "lex_br_pieces_month": "unlimited",
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "multi_tenancy": True, "federation": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "lex_br_agent": True,
            "oab_205_gate": True, "lgpd_marker": True, "audit_oab": True,
            "lex_memory_multi_client": True, "dms_integration": True,
            "dpa_anthropic": True, "sla_4h_support": True,
        },
    },
    # =========================================================================
    # DEMETER tiers (v11.3.0+) — Data Engineering & Analytics
    # =========================================================================
    "demeter_solo": {
        "name": "DEMETER Solo (Data analyst / growth solo)",
        "price_brl_month": 297,
        "duration_days": None,
        "max_parallel": 1,
        "engines_allowed": ["analytics", "etl_basic"],
        "demeter_skills_count": 8,
        "demeter_dashboards_month": 5,
        "demeter_warehouses": ["postgres", "duckdb", "bigquery_sandbox"],
        "features": {
            "api_execution": True, "demeter_agent": True,
            "data_quality_basic": True, "dbt_core": True,
            "ab_testing_basic": True, "single_warehouse": True,
            "metrics_layer_lite": True, "support_email": True,
        },
    },
    "demeter_team": {
        "name": "DEMETER Team (Data team / startup)",
        "price_brl_month": 997,
        "duration_days": None,
        "max_parallel": 3,
        "engines_allowed": "all",
        "demeter_skills_count": 15,
        "demeter_dashboards_month": 25,
        "demeter_warehouses": ["postgres", "duckdb", "bigquery", "snowflake", "redshift"],
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "demeter_agent": True, "data_quality_full": True,
            "dbt_cloud": True, "ml_pipelines": True,
            "ab_testing_full": True, "realtime_streaming": True,
            "metrics_layer_full": True, "data_catalog": True,
            "predictive_models": True, "support_chat": True,
        },
    },
    "demeter_enterprise": {
        "name": "DEMETER Enterprise (Data org / multi-warehouse)",
        "price_brl_month_from": 4000,
        "duration_days": None,
        "max_parallel": 5,
        "engines_allowed": "all",
        "demeter_skills_count": 15,
        "demeter_dashboards_month": "unlimited",
        "demeter_warehouses": "all",
        "features": {
            "api_execution": True, "evolution_engine": True, "llm_judge": True,
            "predictive_dispatch": True, "chain_executor": True,
            "multi_tenancy": True, "federation": True,
            "plugins": True, "adaptive_rubrics": True, "dashboard": True,
            "task_templates": True, "demeter_agent": True,
            "data_quality_full": True, "dbt_cloud": True,
            "ml_pipelines_production": True, "ab_testing_full": True,
            "realtime_streaming": True, "metrics_layer_full": True,
            "data_catalog_enterprise": True, "data_lineage": True,
            "model_explainability": True, "drift_detection": True,
            "dpa_anthropic": True, "sla_4h_support": True,
        },
    },
}


# =============================================================================
# KEY GENERATION + VALIDATION
# =============================================================================

import hmac
import secrets

TIER_SUFFIXES = {
    "starter": "STR", "pro": "PRO", "enterprise": "ENT",
    # LEX-BR tiers (v11.2.0+)
    "lex_solo": "LXS", "lex_office": "LXO", "lex_enterprise": "LXE",
    # DEMETER tiers (v11.3.0+)
    "demeter_solo": "DMS", "demeter_team": "DMT", "demeter_enterprise": "DME",
}
TIER_MAP = {v: k for k, v in TIER_SUFFIXES.items()}


def _hmac_signature(payload: str) -> str:
    """HMAC-SHA256 of payload with MASTER_SECRET. Returns uppercase hex."""
    return hmac.new(MASTER_SECRET, payload.encode("utf-8"),
                    hashlib.sha256).hexdigest().upper()


def generate_key(tier: str, email: str = "") -> str:
    """Generate a license key. Admin only — needs real MASTER_SECRET in env.

    Key format: DARIO-{nonce4}-{sig4}-{sig4}-TIER

    The nonce is random; the signature is HMAC-SHA256(tier:nonce, secret).
    Keys minted with the placeholder secret won't validate on machines that
    set DARIO_MASTER_SECRET — and vice versa. So leave the placeholder in
    public repos and only generate real keys in environments with the env
    var set.

    `email` is stored alongside the key for audit but NOT part of the
    signature payload (so users don't need to remember which email at
    activation time).
    """
    if tier not in TIER_SUFFIXES:
        return None
    suffix = TIER_SUFFIXES[tier]
    nonce = secrets.token_hex(2).upper()  # 4 hex chars
    payload = f"{tier}:{nonce}"
    sig = _hmac_signature(payload)
    return f"DARIO-{nonce}-{sig[0:4]}-{sig[4:8]}-{suffix}"


def validate_key(key: str) -> dict:
    """Validate a license key by recomputing HMAC against MASTER_SECRET.

    Returns {"valid": True, "tier": ...} if signature matches.
    Returns {"valid": False, "reason": ...} otherwise.
    """
    if not key or not key.startswith("DARIO-"):
        return {"valid": False, "reason": "Invalid key format"}

    parts = key.split("-")
    if len(parts) != 5:
        return {"valid": False,
                "reason": "Key must have 5 segments (DARIO-NONCE-SIG-SIG-TIER)"}

    nonce, sig1, sig2, suffix = parts[1], parts[2], parts[3], parts[4].upper()
    if suffix not in TIER_MAP:
        return {"valid": False, "reason": f"Unknown tier suffix: {suffix}"}

    tier = TIER_MAP[suffix]
    payload = f"{tier}:{nonce}"
    expected = _hmac_signature(payload)

    # Constant-time compare to avoid timing leaks
    presented_sig = sig1.upper() + sig2.upper()
    expected_sig = expected[0:8]
    if not hmac.compare_digest(presented_sig, expected_sig):
        return {
            "valid": False,
            "reason": "Signature mismatch (forged key or wrong MASTER_SECRET)",
        }
    return {"valid": True, "tier": tier}


# =============================================================================
# LICENSE FILE
# =============================================================================

def load_license() -> dict:
    """Load current license."""
    if LICENSE_FILE.exists():
        try:
            return json.loads(LICENSE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def save_license(lic: dict):
    """Save license to file."""
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps(lic, indent=2), encoding="utf-8")


TRIAL_FINGERPRINT = ORCH_DIR / ".trial_fingerprint"


def _machine_id() -> str:
    """Return a stable machine identifier for cross-validation.
    Tries Windows MachineGUID, then mac address, then hostname as last resort."""
    try:
        if os.name == "nt":
            import subprocess
            r = subprocess.run(
                ["reg", "query", r"HKLM\SOFTWARE\Microsoft\Cryptography",
                 "/v", "MachineGuid"],
                capture_output=True, text=True, timeout=3,
            )
            for line in (r.stdout or "").splitlines():
                if "MachineGuid" in line:
                    return line.split()[-1]
    except Exception:
        pass
    try:
        import uuid
        return f"mac-{uuid.getnode():012x}"
    except Exception:
        pass
    try:
        import socket
        return f"host-{socket.gethostname()}"
    except Exception:
        return "unknown"


def _write_fingerprint() -> dict:
    """Persistent trial-used marker. Survives license.json deletion.
    Contains: machine_id + first_init_timestamp + signature."""
    now = datetime.now(timezone.utc).isoformat()
    machine = _machine_id()
    sig_payload = f"{MASTER_SECRET}:{machine}:{now}"
    signature = hashlib.sha256(sig_payload.encode()).hexdigest()
    fp = {
        "machine_id": machine,
        "first_init_at": now,
        "signature": signature,
        "note": "Trial activation marker. Do not edit — deletion does NOT grant a new trial.",
    }
    ORCH_DIR.mkdir(parents=True, exist_ok=True)
    TRIAL_FINGERPRINT.write_text(json.dumps(fp, indent=2), encoding="utf-8")
    return fp


def _check_fingerprint() -> dict:
    """Detect if a trial was already initialized on this machine."""
    if not TRIAL_FINGERPRINT.exists():
        return {"used": False}
    try:
        fp = json.loads(TRIAL_FINGERPRINT.read_text(encoding="utf-8"))
        # Verify signature wasn't tampered with
        sig_payload = f"{MASTER_SECRET}:{fp.get('machine_id')}:{fp.get('first_init_at')}"
        expected_sig = hashlib.sha256(sig_payload.encode()).hexdigest()
        if fp.get("signature") != expected_sig:
            return {"used": True, "tampered": True, "first_init_at": fp.get("first_init_at")}
        return {"used": True, "tampered": False, "first_init_at": fp.get("first_init_at"),
                "machine_id": fp.get("machine_id")}
    except Exception:
        # Corrupted fingerprint — treat as used (fail-closed)
        return {"used": True, "corrupted": True}


def init_trial(force: bool = False) -> dict:
    """Initialize a 7-day trial license.

    Refuses to reinitialize if a previous trial was already used on this
    machine (anti-bypass). Use `force=True` only during development with the
    dev.flag enabled.
    """
    # Anti-bypass check (v11.1.1+)
    fp_check = _check_fingerprint()
    if fp_check.get("used") and not force:
        # Allow force only if dev bypass active
        try:
            sys.path.insert(0, str(ORCH_DIR))
            from license_guard import _bypass_active
            if _bypass_active():
                force = True
        except Exception:
            pass

    if fp_check.get("used") and not force:
        return {
            "status": "refused",
            "reason": "trial_already_used",
            "first_init_at": fp_check.get("first_init_at"),
            "tampered": fp_check.get("tampered", False),
            "message": (
                "A trial was already used on this machine. "
                "Trials are one-time per machine. "
                "Activate a VIP key: python license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO"
            ),
        }

    now = datetime.now(timezone.utc)
    lic = {
        "tier": "trial",
        "name": TIERS["trial"]["name"],
        "key": None,
        "email": None,
        "activated_at": now.isoformat(),
        "expires_at": (now + timedelta(days=7)).isoformat(),
        "max_parallel": TIERS["trial"]["max_parallel"],
        "features": TIERS["trial"]["features"],
        "engines_allowed": TIERS["trial"]["engines_allowed"],
        "status": "active",
    }
    save_license(lic)
    # Write persistent marker (only on FIRST activation — don't overwrite if already exists)
    if not TRIAL_FINGERPRINT.exists():
        _write_fingerprint()
    return lic


def activate_key(key: str) -> dict:
    """Activate a VIP license key."""
    validation = validate_key(key)
    if not validation["valid"]:
        return {"success": False, "error": validation["reason"]}

    tier = validation["tier"]
    tier_config = TIERS[tier]
    now = datetime.now(timezone.utc)

    lic = {
        "tier": tier,
        "name": tier_config["name"],
        "key": key,
        "email": None,
        "activated_at": now.isoformat(),
        "expires_at": None,  # Permanent
        "max_parallel": tier_config["max_parallel"],
        "features": tier_config["features"],
        "engines_allowed": tier_config["engines_allowed"],
        "status": "active",
    }
    save_license(lic)
    return {"success": True, "tier": tier, "name": tier_config["name"]}


def check_license() -> dict:
    """Check if current license is valid. Returns status."""
    lic = load_license()

    if not lic:
        return {"valid": False, "reason": "No license found. Run: python license_manager.py --init-trial",
                "tier": "none", "action": "init_trial"}

    tier = lic.get("tier", "trial")
    status = lic.get("status", "unknown")

    # Check expiration for trial
    if tier == "trial" and lic.get("expires_at"):
        try:
            expires = datetime.fromisoformat(lic["expires_at"])
            now = datetime.now(timezone.utc)
            if now > expires:
                lic["status"] = "expired"
                save_license(lic)
                remaining = 0
                return {
                    "valid": False,
                    "tier": "trial",
                    "reason": "Trial expired",
                    "expired_at": lic["expires_at"],
                    "action": "activate_key",
                    "message": "Your 7-day trial has expired. Activate a VIP key: python license_manager.py --activate DARIO-XXXX-XXXX-XXXX-PRO",
                }
            remaining = (expires - now).days
            return {
                "valid": True,
                "tier": "trial",
                "days_remaining": remaining,
                "expires_at": lic["expires_at"],
                "max_parallel": lic.get("max_parallel", 1),
                "features": lic.get("features", {}),
            }
        except Exception:
            pass

    # Pro/Enterprise = permanent
    if tier in ("pro", "enterprise"):
        return {
            "valid": True,
            "tier": tier,
            "name": lic.get("name"),
            "key": lic.get("key", "")[:15] + "...",
            "max_parallel": lic.get("max_parallel", 3),
            "features": lic.get("features", {}),
            "permanent": True,
        }

    return {"valid": False, "tier": tier, "reason": "Unknown license state"}


def is_feature_allowed(feature: str) -> bool:
    """Quick check if a specific feature is allowed."""
    lic = check_license()
    if not lic.get("valid"):
        return False
    features = lic.get("features", {})
    return features.get(feature, False)


def get_max_parallel() -> int:
    """Get allowed max parallel from license."""
    lic = check_license()
    if not lic.get("valid"):
        return 0
    return lic.get("max_parallel", 1)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="DARIO License Manager")
    parser.add_argument("--status", "-s", action="store_true", help="Show license status")
    parser.add_argument("--activate", "-a", help="Activate VIP key")
    parser.add_argument("--init-trial", action="store_true", help="Start 7-day trial")
    parser.add_argument("--check", "-c", action="store_true", help="Check if valid (exit code)")
    parser.add_argument("--generate-key", nargs=2, metavar=("TIER", "EMAIL"), help="Generate key (admin)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.json:
        logging.getLogger().setLevel(logging.ERROR)

    if args.init_trial:
        lic = init_trial()
        if args.json:
            print(json.dumps(lic, indent=2))
        else:
            # v11.1.1+ — handle anti-bypass refusal
            if lic.get("status") == "refused":
                first = (lic.get("first_init_at") or "?")[:10]
                tampered = lic.get("tampered", False)
                print(f"""
╔══════════════════════════════════════════════╗
║  DARIO ORCHESTRATOR — TRIAL REFUSED          ║
║                                              ║
║  Status:    REFUSED (one trial per machine)  ║
║  Used on:   {first}                          ║
║  Tampered:  {'YES — fingerprint modified' if tampered else 'NO':<33s}║
║                                              ║
║  Activate VIP key:                           ║
║  python license_manager.py --activate \\      ║
║    DARIO-XXXX-XXXX-XXXX-PRO                  ║
║                                              ║
║  Or purchase: barda@automationsolutionai.com ║
╚══════════════════════════════════════════════╝
""")
                return 2

            expires = lic["expires_at"][:10]
            print(f"""
╔══════════════════════════════════════════╗
║  DARIO ORCHESTRATOR — 7-DAY TRIAL       ║
║                                          ║
║  Status:   ACTIVE                        ║
║  Expires:  {expires}                    ║
║  Parallel: 1 (max)                       ║
║  Engines:  6 of 26                       ║
║                                          ║
║  To unlock full access:                  ║
║  python license_manager.py --activate    ║
║    DARIO-XXXX-XXXX-XXXX-PRO             ║
╚══════════════════════════════════════════╝
""")
        return 0

    elif args.activate:
        result = activate_key(args.activate)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(f"""
╔══════════════════════════════════════════╗
║  DARIO ORCHESTRATOR — LICENSE ACTIVATED  ║
║                                          ║
║  Tier:     {result['name']:30s}  ║
║  Status:   PERMANENT                     ║
║  Parallel: {TIERS[result['tier']]['max_parallel']}                              ║
║  Engines:  ALL 26                        ║
║  Features: ALL UNLOCKED                  ║
║                                          ║
║  Thank you for supporting DARIO!         ║
╚══════════════════════════════════════════╝
""")
            else:
                print(f"  ERROR: {result['error']}")
        return 0 if result.get("success") else 1

    elif args.check:
        result = check_license()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["valid"]:
                tier = result["tier"]
                if tier == "trial":
                    print(f"  TRIAL — {result.get('days_remaining', '?')} days remaining")
                else:
                    print(f"  {result.get('name', tier).upper()} — permanent license")
            else:
                print(f"  INVALID — {result.get('reason', '?')}")
                if result.get("message"):
                    print(f"  {result['message']}")
        return 0 if result["valid"] else 1

    elif args.generate_key:
        tier, email = args.generate_key
        valid_tiers = ("starter", "pro", "enterprise",
                       "lex_solo", "lex_office", "lex_enterprise",
                       "demeter_solo", "demeter_team", "demeter_enterprise")
        if tier not in valid_tiers:
            print(f"Tier must be one of: {', '.join(valid_tiers)}")
            return 1
        key = generate_key(tier, email)
        if args.json:
            print(json.dumps({"key": key, "tier": tier, "email": email}))
        else:
            print(f"  Generated key for {email} ({tier}):")
            print(f"  {key}")
            print(f"\n  Send to customer. They run:")
            print(f"  python license_manager.py --activate {key}")
        return 0

    elif args.status:
        lic = load_license()
        result = check_license()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if not lic:
                print("  No license. Run: python license_manager.py --init-trial")
            else:
                print(f"  Tier:      {lic.get('tier', '?')}")
                print(f"  Name:      {lic.get('name', '?')}")
                print(f"  Status:    {lic.get('status', '?')}")
                print(f"  Parallel:  {lic.get('max_parallel', '?')}")
                if lic.get("expires_at"):
                    print(f"  Expires:   {lic['expires_at'][:10]}")
                    if result.get("days_remaining") is not None:
                        print(f"  Remaining: {result['days_remaining']} days")
                else:
                    print(f"  Expires:   NEVER (permanent)")
                if lic.get("key"):
                    print(f"  Key:       {lic['key'][:15]}...")
                # Feature summary
                features = lic.get("features", {})
                locked = [k for k, v in features.items() if not v]
                unlocked = [k for k, v in features.items() if v]
                print(f"  Unlocked:  {len(unlocked)} features")
                if locked:
                    print(f"  Locked:    {', '.join(locked[:5])}")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
