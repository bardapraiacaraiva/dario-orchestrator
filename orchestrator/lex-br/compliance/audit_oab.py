#!/usr/bin/env python3
"""
Audit Trail OAB-Compatible
============================
Log imutável (append-only) de todas as operações LEX-BR para conformidade
com fiscalização OAB. Cada entrada inclui:
  - timestamp UTC
  - skill invocada
  - cliente (hash anonimizado)
  - output_type
  - revisão humana (boolean + OAB do reviewer)
  - flags compliance (cite_check, ZDR, privilege, OAB 205)
  - hash do output (integrity)

Storage: ~/.claude/orchestrator/lex-br/memory/compliance_log/YYYY-MM-DD.yaml
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

LEX_DIR = Path.home() / ".claude" / "orchestrator" / "lex-br"
AUDIT_DIR = LEX_DIR / "memory" / "compliance_log"

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True

    def _dump_yaml(data, path):
        with open(path, "a", encoding="utf-8") as f:
            _yaml.dump(data, f)
except ImportError:
    import yaml as _pyaml

    def _dump_yaml(data, path):
        with open(path, "a", encoding="utf-8") as f:
            _pyaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                        sort_keys=False)


def _hash_client(client_id: str) -> str:
    """Hash anonimizado do cliente para audit."""
    if not client_id:
        return "anonymous"
    return "client-" + hashlib.sha256(client_id.encode()).hexdigest()[:12]


def _hash_output(output: str) -> str:
    """Hash do output para integrity check."""
    if not output:
        return ""
    return hashlib.sha256(output.encode()).hexdigest()[:16]


def log(skill: str, task_id: str, output: str = "",
        client_id: str = None, output_type: str = "draft_interno",
        revisao_humana: bool = False, advogado_oab: str = None,
        flags: dict = None, tokens_used: int = 0) -> dict:
    """Append entry to today's audit log.

    Returns the persisted entry dict.
    """
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_file = AUDIT_DIR / f"{today}.yaml"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": skill,
        "task_id": task_id,
        "client_hash": _hash_client(client_id) if client_id else None,
        "output_type": output_type,
        "output_hash": _hash_output(output) if output else "",
        "output_length_chars": len(output) if output else 0,
        "revisao_humana": revisao_humana,
        "advogado_oab": advogado_oab,
        "flags": flags or {},
        "tokens_used": tokens_used,
    }

    _dump_yaml([entry], str(log_file))
    return entry


def count_today() -> int:
    """Quantos eventos hoje."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_file = AUDIT_DIR / f"{today}.yaml"
    if not log_file.exists():
        return 0
    try:
        from ruamel.yaml import YAML
        _y = YAML()
        with open(log_file, "r", encoding="utf-8") as f:
            data = _y.load(f) or []
        return len(data) if isinstance(data, list) else 0
    except Exception:
        try:
            import yaml as _pyaml
            with open(log_file, "r", encoding="utf-8") as f:
                data = _pyaml.safe_load(f) or []
            return len(data) if isinstance(data, list) else 0
        except Exception:
            return 0


def summary(days: int = 7) -> dict:
    """Resumo dos últimos N dias para dashboard."""
    if not AUDIT_DIR.exists():
        return {"total_events": 0, "days": []}

    from datetime import timedelta
    out = []
    total = 0
    for i in range(days):
        d = (datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = AUDIT_DIR / f"{d}.yaml"
        if log_file.exists():
            try:
                import yaml as _pyaml
                data = _pyaml.safe_load(log_file.read_text(encoding="utf-8")) or []
                out.append({"date": d, "events": len(data)})
                total += len(data)
            except Exception:
                out.append({"date": d, "events": 0})

    return {"total_events": total, "days": out}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        print(json.dumps(summary(), indent=2, ensure_ascii=False))
    else:
        # Sample log
        entry = log(
            skill="lex-trabalhista",
            task_id="LEX-TEST-001",
            output="Sample output content for testing",
            client_id="cliente-teste",
            output_type="draft_interno",
            revisao_humana=False,
            flags={"cite_check": "passed", "zdr": True, "oab_205": "pass"},
        )
        print(json.dumps(entry, indent=2, ensure_ascii=False, default=str))
