#!/usr/bin/env python3
"""
DARIO Ethical Pre-Gate ("Filtro Triplice")
==========================================
Upgrade 2 (Sprint 1) of the Cognitive Audit roadmap.

Wires the three-question gate from operational_states.yaml:94-104 into the
runtime. Previously the gate existed only in YAML — never called in code.
Now invoked by guardrails.py BEFORE any other validation (Check 0).

Three questions:
    1. Clarity   — Is the task clearly defined with unambiguous success criteria?
    2. Freedom   — Does executing this respect user autonomy and informed consent?
    3. Coherence — Is this aligned with project objectives and manifesto values?

All three answer yes → PASS.
Two yes → WARN (executable but flag reasoning).
Less than two → FAIL (reformulate before dispatch).

Hooks into blocklist (operational_states.yaml:106-115) for hard-stops.

CLI:
    python ethical_gate.py --task MNB-002          Evaluate single task
    python ethical_gate.py --task MNB-002 --json   Machine-readable verdict
"""

import json
import re
import sys
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _yaml.load(f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _pyaml.safe_load(f)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
STATES_FILE = ORCH_DIR / "operational_states.yaml"
COMPANY_FILE = ORCH_DIR / "company.yaml"
MEMORY_INDEX = Path.home() / ".claude" / "projects" / "C--Users-barda" / "memory" / "MEMORY.md"

# Action verbs (PT + EN) that indicate clear intent.
ACTION_VERBS = {
    "criar", "fazer", "gerar", "produzir", "construir", "desenhar",
    "auditar", "analisar", "avaliar", "rever", "diagnosticar",
    "optimizar", "otimizar", "melhorar", "corrigir", "fix", "fixar",
    "implementar", "desenvolver", "escrever", "redigir", "publicar",
    "lancar", "lançar", "deployar", "configurar", "integrar",
    "create", "build", "generate", "produce", "design",
    "audit", "analyze", "evaluate", "review", "diagnose",
    "optimize", "improve", "implement", "develop",
    "write", "publish", "launch", "deploy", "configure", "integrate",
    "calcular", "calculate", "validar", "validate", "testar", "test",
    "documentar", "document", "planear", "plan", "definir", "define",
    "decompor", "decompose", "orquestrar", "orchestrate",
}

# Vague placeholders that signal unclear intent.
VAGUE_TOKENS = {
    "isto", "aquilo", "isso", "ajuda", "help", "stuff", "thing",
    "qualquer coisa", "algo", "something", "anything", "whatever",
    "tbd", "tba", "todo", "fix me", "fix this",
}

# Destructive verbs that need explicit confirmation.
DESTRUCTIVE_VERBS = {
    "delete", "drop", "remove", "wipe", "purge", "truncate",
    "apagar", "eliminar", "remover", "destruir", "limpar",
    "rm -rf", "force push", "force-push", "reset --hard",
}

# Blocklist from operational_states.yaml (cached at import — refresh on long-running).
_BLOCKLIST_CACHE = None


def _load_blocklist() -> list:
    global _BLOCKLIST_CACHE
    if _BLOCKLIST_CACHE is not None:
        return _BLOCKLIST_CACHE
    try:
        data = _load_yaml(str(STATES_FILE))
        _BLOCKLIST_CACHE = data.get("blocklist", []) if data else []
    except Exception:
        _BLOCKLIST_CACHE = []
    return _BLOCKLIST_CACHE


def _load_known_projects() -> set:
    """Read MEMORY.md to extract names of known projects. Empty set if unavailable."""
    if not MEMORY_INDEX.exists():
        return set()
    try:
        content = MEMORY_INDEX.read_text(encoding="utf-8", errors="ignore")
        # Match list entries like "- [Project Name](file.md) — ..."
        matches = re.findall(r"-\s+\[([^\]]+)\]", content)
        projects = set()
        for m in matches:
            normalized = m.lower().strip()
            projects.add(normalized)
            # Also add first word as informal key (e.g. "Atrium Golden Visa" -> "atrium")
            first = normalized.split()[0] if normalized.split() else ""
            if first and len(first) > 2:
                projects.add(first)
        return projects
    except Exception:
        return set()


def evaluate_clarity(task: dict) -> tuple:
    """Question 1: Is the task clearly defined?
    Returns (passed: bool, score: float 0-1, reasons: list[str])."""
    reasons = []
    score = 1.0

    title = (task.get("title") or "").strip()
    description = (task.get("description") or "").strip()
    combined = f"{title} {description}".lower()

    if not title:
        reasons.append("missing title")
        score -= 0.60
    elif len(title) < 5:
        reasons.append(f"title too short ({len(title)} chars)")
        score -= 0.35

    if not description:
        reasons.append("missing description")
        score -= 0.40
    elif len(description) < 20:
        reasons.append(f"description too short ({len(description)} chars)")
        score -= 0.20

    # Vague tokens are a strong negative signal
    for vague in VAGUE_TOKENS:
        if vague in combined:
            reasons.append(f"vague token: '{vague}'")
            score -= 0.25
            break

    # Action verb bonus
    has_action = any(verb in combined for verb in ACTION_VERBS)
    if has_action:
        score = min(score + 0.10, 1.0)
    else:
        reasons.append("no clear action verb found")
        score -= 0.15

    # Success criteria signal
    if task.get("success_criteria") or "success criteria" in description.lower() or "criterio" in description.lower():
        score = min(score + 0.05, 1.0)

    score = max(0.0, score)
    return (score >= 0.65, round(score, 3), reasons)


def evaluate_freedom(task: dict) -> tuple:
    """Question 2: Does this respect user autonomy?
    Returns (passed, score, reasons)."""
    reasons = []
    score = 1.0

    title = (task.get("title") or "").lower()
    description = (task.get("description") or "").lower()
    combined = f"{title} {description}"

    # Destructive verb without explicit confirmation
    for verb in DESTRUCTIVE_VERBS:
        if verb in combined:
            confirmed = bool(
                task.get("confirmation_received")
                or task.get("user_approved")
                or "confirmed" in combined
                or "approved" in combined
            )
            if not confirmed:
                reasons.append(f"destructive verb '{verb}' without confirmation")
                score -= 0.55
                break

    # Force flag without approval
    if task.get("force") and not task.get("confirmation_received"):
        reasons.append("force=true without confirmation_received")
        score -= 0.40

    # Blocklist match (operational_states.yaml)
    blocklist = _load_blocklist()
    for rule in blocklist:
        rule_lower = rule.lower() if isinstance(rule, str) else ""
        if not rule_lower:
            continue
        # Crude heuristic — look for distinctive phrase chunks from the rule in the task text
        key_phrases = []
        if "delete user data" in rule_lower:
            key_phrases = ["delete user data", "apagar dados"]
        elif "manipulative" in rule_lower:
            key_phrases = ["fake urgency", "fear-based", "urgencia falsa"]
        elif "bypass" in rule_lower and "explicit" in rule_lower:
            key_phrases = ["bypass user", "ignore user", "override user"]
        elif "security vulnerabilities" in rule_lower:
            key_phrases = ["bypass security", "ignore vulnerability"]
        for phrase in key_phrases:
            if phrase in combined:
                reasons.append(f"blocklist match: {rule}")
                score -= 0.50
                break

    score = max(0.0, score)
    return (score >= 0.65, round(score, 3), reasons)


def evaluate_coherence(task: dict) -> tuple:
    """Question 3: Aligned with project objectives?
    Returns (passed, score, reasons)."""
    reasons = []
    score = 1.0

    project = (task.get("project") or "").strip().lower()

    if not project:
        reasons.append("no project field")
        score -= 0.40
    else:
        known = _load_known_projects()
        if known:
            # Project recognized if any known key is contained in or contains the project name
            match = any(
                project == k or project in k or k in project
                for k in known
            )
            if not match:
                reasons.append(f"project '{project}' not in memory index")
                score -= 0.20

    # Skill <-> project domain coherence (basic checks)
    skill = (task.get("skill") or "").lower()
    if project and skill:
        # DIVA skills are arquitectura/design — flag if project is clearly software SaaS
        if skill.startswith("diva-") and any(t in project for t in ["saas", "api", "backend"]):
            reasons.append(f"DIVA architecture skill '{skill}' on software project '{project}'")
            score -= 0.35
        # Conta-* (Portuguese accounting) on non-PT/non-finance project
        if skill.startswith("conta-") and project and not any(
            t in project for t in ["lucas", "lusoconta", "finance", "conta", "fiscal", "saquei"]
        ):
            reasons.append(f"PT-accounting skill '{skill}' on non-finance project '{project}'")
            score -= 0.25

    # Empty success criteria + critical policy is incoherent
    if task.get("execution_policy") == "critical" and not (
        task.get("success_criteria") or task.get("acceptance_criteria")
    ):
        reasons.append("critical task without success_criteria")
        score -= 0.35

    score = max(0.0, score)
    return (score >= 0.70, round(score, 3), reasons)


def evaluate(task: dict) -> dict:
    """Run the full three-question gate.

    Returns dict:
        {
          "verdict": "PASS" | "WARN" | "FAIL",
          "clarity":   {"passed": bool, "score": float, "reasons": [...]},
          "freedom":   {"passed": bool, "score": float, "reasons": [...]},
          "coherence": {"passed": bool, "score": float, "reasons": [...]},
          "summary": "...",
          "reformulation_hint": "..." | None,
        }
    """
    c_pass, c_score, c_reasons = evaluate_clarity(task)
    f_pass, f_score, f_reasons = evaluate_freedom(task)
    co_pass, co_score, co_reasons = evaluate_coherence(task)

    passes = sum([c_pass, f_pass, co_pass])
    # Catastrophic fail: any single dimension below 0.30 forces FAIL
    # regardless of how the other two scored (e.g. empty task — clarity=0.1).
    catastrophic = min(c_score, f_score, co_score) < 0.30
    if catastrophic:
        verdict = "FAIL"
    elif passes == 3:
        verdict = "PASS"
    elif passes == 2:
        verdict = "WARN"
    else:
        verdict = "FAIL"

    reformulation = None
    if verdict == "FAIL":
        hints = []
        if not c_pass:
            hints.append("clarify task: add specific deliverable, success criteria, and action verb")
        if not f_pass:
            hints.append("add explicit user confirmation for destructive/forced actions")
        if not co_pass:
            hints.append("set project field and align skill choice with project domain")
        reformulation = "; ".join(hints)

    return {
        "verdict": verdict,
        "passes": passes,
        "clarity":   {"passed": c_pass,  "score": c_score,  "reasons": c_reasons},
        "freedom":   {"passed": f_pass,  "score": f_score,  "reasons": f_reasons},
        "coherence": {"passed": co_pass, "score": co_score, "reasons": co_reasons},
        "summary": f"clarity={c_score} freedom={f_score} coherence={co_score} → {verdict}",
        "reformulation_hint": reformulation,
    }


def _load_task(task_id: str) -> dict:
    # Try DB first, fall back to YAML
    try:
        sys.path.insert(0, str(ORCH_DIR))
        from core.db import DB
        db = DB()
        t = db.get_task(task_id)
        if t:
            return t
    except Exception:
        pass
    task_file = ORCH_DIR / "tasks" / "active" / f"{task_id}.yaml"
    if task_file.exists():
        return _load_yaml(str(task_file))
    return None


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("ethical_gate")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    import argparse
    p = argparse.ArgumentParser(description="DARIO Ethical Pre-Gate")
    p.add_argument("--task", "-t", help="Task ID to evaluate")
    p.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = p.parse_args()

    if not args.task:
        p.print_help()
        return 1

    task = _load_task(args.task)
    if not task:
        print(f"Task {args.task} not found", file=sys.stderr)
        return 1

    result = evaluate(task)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        symbol = {"PASS": "+", "WARN": "~", "FAIL": "!"}[result["verdict"]]
        print(f"[{symbol}] Ethical gate: {result['verdict']} ({result['passes']}/3)")
        for q in ("clarity", "freedom", "coherence"):
            r = result[q]
            mark = "+" if r["passed"] else "!"
            print(f"  [{mark}] {q}: {r['score']}")
            for reason in r["reasons"]:
                print(f"        - {reason}")
        if result["reformulation_hint"]:
            print(f"\n  REFORMULATE: {result['reformulation_hint']}")
    return 0 if result["verdict"] != "FAIL" else 2


if __name__ == "__main__":
    sys.exit(main())
