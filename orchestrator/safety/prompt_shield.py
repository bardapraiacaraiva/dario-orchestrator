"""Prompt injection + secret exfiltration defenses.

Faixa 1 #3 (2026-05-25). Closes audit Risk #3 (HIGH).

This is a **v1 pattern-based** shield. NOT production-grade ML classifier.
For ML-grade defenses (Llama Guard, NeMo Guardrails, Lakera Guard), upgrade
in Faixa 2 once volume justifies the integration cost. Pattern-based catches
~70-80% of common attacks; ML catches ~95%.

What it defends against
───────────────────────
1. **Prompt injection** — user input attempting to override system instructions
   ("ignore previous instructions", "DAN mode", "developer mode", etc.)
2. **Secret exfiltration** — output containing API keys, tokens, paths to
   sensitive files (.env, .audit_privkey, ~/.ssh/, ~/.aws/)
3. **PII leakage** — common patterns for credit cards, IBANs, SSNs
4. **Path traversal hints** — outputs referencing /etc/passwd, ../../, etc.

What it does NOT defend against
───────────────────────────────
- Sophisticated multi-turn jailbreaks (need ML classifier)
- Indirect prompt injection via retrieved documents (need source isolation)
- Native LLM hallucination of plausible-looking secrets (need verification)
- Side-channel attacks via timing/token-count (need different mitigation)

Usage:
    from safety.prompt_shield import inspect_input, inspect_output, shield

    # Pre-execution
    verdict = inspect_input(user_prompt)
    if verdict["block"]:
        raise PromptInjectionDetected(verdict["reason"])

    # Post-execution
    verdict = inspect_output(llm_response)
    sanitized = verdict["sanitized"]  # may have secrets masked

    # Combined context manager
    with shield(skill="dario-brand") as s:
        s.check_input(prompt)
        output = call_llm(prompt)
        clean = s.sanitize_output(output)
"""
from __future__ import annotations

import re
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator

# ─── Patterns: prompt injection (BLOCK on match) ─────────────────────────


# Known jailbreak / instruction-override patterns. Case-insensitive.
INJECTION_PATTERNS = [
    # Direct override attempts
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?)", re.I),
    re.compile(r"disregard\s+(your|the|all)\s+(instructions?|guidelines?|rules?)", re.I),
    re.compile(r"forget\s+(everything|all|what)\s+(you('?ve|\s+have)?|above)", re.I),
    re.compile(r"new\s+(instructions?|prompt|system\s+(prompt|message))\s*:", re.I),

    # Role-play jailbreaks
    re.compile(r"\b(DAN|AIM|STAN|DUDE|MONGO\s+TOM|JAILBREAK)\s+(mode|model)\b", re.I),
    re.compile(r"developer\s+mode\s+(enabled|on|activated)", re.I),
    re.compile(r"god\s+mode\s+(enabled|on|activated)", re.I),
    re.compile(r"pretend\s+(you\s+are|to\s+be)\s+(an?\s+(unrestricted|uncensored|evil))", re.I),

    # System prompt extraction
    re.compile(r"(repeat|reveal|show|print|output)\s+(your\s+)?(system|initial|original)\s+(prompt|instructions?|message)", re.I),
    re.compile(r"what\s+(are\s+)?(your|the)\s+(system\s+)?(instructions?|rules?)\s+\?", re.I),

    # Encoded payload markers (base64, unicode tricks)
    re.compile(r"base64\s*[:=]\s*[A-Za-z0-9+/]{40,}={0,2}", re.I),

    # Tool/code-execution exfil hints
    re.compile(r"\b(execute|run|eval)\s+the\s+following\s+(code|command|script|shell|bash|sh|powershell)\b", re.I),
    re.compile(r"```\s*(bash|sh|powershell|cmd)\s+rm\s+-rf", re.I),
    re.compile(r"\brm\s+-rf\s+[/~]", re.I),  # raw `rm -rf /` or `rm -rf ~`
]

# Lower-confidence patterns (WARN, don't block — could be legit content).
SUSPICIOUS_PATTERNS = [
    re.compile(r"\bprompt\s+injection\b", re.I),       # someone discussing it
    re.compile(r"\bjailbreak\b", re.I),
    re.compile(r"override\s+safety", re.I),
]


# ─── Patterns: secret detection (MASK on match in OUTPUTS) ───────────────


# Common secret formats. Each tuple is (pattern, name, mask_replacement).
SECRET_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    # Anthropic API keys (real format: sk-ant-api01-XXXXX..., sk-ant-admin..., etc.)
    # Hyphen-separated tier id (api01/api02/admin01/test/...) before random portion.
    (re.compile(r"sk-ant-(api\d{2}|admin\d{2}|test)[-_][A-Za-z0-9_-]{40,}", re.I), "anthropic-api-key", "sk-ant-***REDACTED***"),
    # OpenAI
    (re.compile(r"sk-proj-[A-Za-z0-9_-]{40,}"), "openai-project-key", "sk-proj-***REDACTED***"),
    (re.compile(r"sk-[A-Za-z0-9]{48}"), "openai-classic-key", "sk-***REDACTED***"),
    # GitHub
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "github-token", "ghX_***REDACTED***"),
    # AWS
    (re.compile(r"AKIA[0-9A-Z]{16}"), "aws-access-key", "AKIA***REDACTED***"),
    (re.compile(r"aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}", re.I), "aws-secret-key", "aws_secret_access_key=***REDACTED***"),
    # Generic JWT
    (re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"), "jwt", "eyJ***REDACTED***"),
    # DARIO-specific
    (re.compile(r"DARIO-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-(PRO|ENT|ELG|EFL|TRIAL)", re.I), "dario-license-key", "DARIO-****-****-****-***"),
    # SSH private keys
    (re.compile(r"-----BEGIN\s+(RSA|DSA|EC|OPENSSH|ED25519)\s+PRIVATE\s+KEY-----[\s\S]+?-----END\s+\w+\s+PRIVATE\s+KEY-----"), "ssh-private-key", "-----BEGIN PRIVATE KEY----- ***REDACTED*** -----END PRIVATE KEY-----"),
    # Generic high-entropy tokens (length-based heuristic)
    # Less precise — match only if preceded by token/key/secret label
    (re.compile(r"(?:token|secret|api[_-]?key|password)\s*[:=]\s*['\"]?([A-Za-z0-9+/_-]{32,})['\"]?", re.I), "labeled-secret", "<label>=***REDACTED***"),
]

# File path patterns suggesting secret exposure.
SECRET_PATH_PATTERNS = [
    re.compile(r"\.env(\.[a-z]+)?(\s|$|\")", re.I),
    re.compile(r"\.master_secret"),
    re.compile(r"\.audit_privkey"),
    re.compile(r"~?/?\.ssh/(id_rsa|id_ed25519|authorized_keys)"),
    re.compile(r"~?/?\.aws/credentials"),
    re.compile(r"~?/?\.gcloud/credentials"),
    re.compile(r"\.pem\b(\s|$|\")"),
    re.compile(r"\.key\b(\s|$|\")"),
]

# Path traversal indicators
PATH_TRAVERSAL_PATTERNS = [
    re.compile(r"\.\./.*\.\.\/"),
    re.compile(r"/etc/passwd"),
    re.compile(r"/etc/shadow"),
    re.compile(r"\\windows\\system32", re.I),
]


# ─── Public API ──────────────────────────────────────────────────────────


@dataclass
class Verdict:
    block: bool = False
    reason: str = ""
    matches: list[dict[str, str]] = field(default_factory=list)
    sanitized: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "block": self.block,
            "reason": self.reason,
            "matches": self.matches,
            "sanitized": self.sanitized,
        }


def inspect_input(text: str) -> dict[str, Any]:
    """Pre-LLM input check. Returns verdict dict with block + reason.

    Block triggers: any INJECTION_PATTERNS match.
    Warn triggers: any SUSPICIOUS_PATTERNS match (not blocked, just flagged).
    """
    v = Verdict(sanitized=text)
    if not isinstance(text, str) or not text:
        return v.to_dict()

    for pat in INJECTION_PATTERNS:
        m = pat.search(text)
        if m:
            v.block = True
            v.reason = f"prompt injection pattern matched: {m.group(0)[:80]}"
            v.matches.append({"type": "injection", "snippet": m.group(0)[:200]})
            return v.to_dict()

    for pat in SUSPICIOUS_PATTERNS:
        m = pat.search(text)
        if m:
            v.matches.append({"type": "suspicious", "snippet": m.group(0)[:200]})

    return v.to_dict()


def inspect_output(text: str) -> dict[str, Any]:
    """Post-LLM output check. Masks detected secrets in-place.

    Block triggers: SSH private key emission (always critical).
    Mask triggers: any SECRET_PATTERNS match — replaced with redacted token.
    Warn triggers: secret file paths or path traversal mentions.
    """
    v = Verdict(sanitized=text)
    if not isinstance(text, str) or not text:
        return v.to_dict()

    sanitized = text
    for pat, name, replacement in SECRET_PATTERNS:
        if pat.search(sanitized):
            for found in pat.finditer(sanitized):
                v.matches.append({"type": "secret", "kind": name, "snippet": found.group(0)[:40] + "..."})
            sanitized = pat.sub(replacement, sanitized)
            # Block on SSH private key — never proceed
            if name == "ssh-private-key":
                v.block = True
                v.reason = "SSH private key in output — blocked entirely"

    for pat in SECRET_PATH_PATTERNS:
        m = pat.search(sanitized)
        if m:
            v.matches.append({"type": "secret-path", "snippet": m.group(0)[:80]})
            # Don't mask — paths might be discussing security legitimately

    for pat in PATH_TRAVERSAL_PATTERNS:
        m = pat.search(sanitized)
        if m:
            v.matches.append({"type": "path-traversal", "snippet": m.group(0)[:80]})

    v.sanitized = sanitized
    return v.to_dict()


# ─── Context manager for skill execution ──────────────────────────────────


class PromptInjectionDetected(Exception):
    """Raised when inspect_input detects a blocking pattern."""


class SecretLeakageDetected(Exception):
    """Raised when inspect_output detects an unmaskable secret (e.g., SSH key)."""


@contextmanager
def shield(skill: str = "<unknown>") -> "Iterator[_Shield]":
    """Context manager that wraps skill execution with input + output checks.

    Usage:
        with shield(skill="dario-brand") as s:
            s.check_input(user_input)
            result = call_anthropic(user_input)
            safe = s.sanitize_output(result)
    """
    yield _Shield(skill)


class _Shield:
    def __init__(self, skill: str) -> None:
        self.skill = skill
        self.events: list[dict[str, Any]] = []

    def check_input(self, text: str) -> None:
        v = inspect_input(text)
        self.events.append({"phase": "input", **v})
        if v["block"]:
            raise PromptInjectionDetected(f"[{self.skill}] {v['reason']}")

    def sanitize_output(self, text: str) -> str:
        v = inspect_output(text)
        self.events.append({"phase": "output", **v})
        if v["block"]:
            raise SecretLeakageDetected(f"[{self.skill}] {v['reason']}")
        return str(v["sanitized"])


# ─── CLI for ad-hoc testing ──────────────────────────────────────────────


def _cli() -> int:
    import argparse
    import json
    p = argparse.ArgumentParser(description="Prompt injection + secret shield (Faixa 1 #3)")
    p.add_argument("text", help="Text to inspect (use - for stdin)")
    p.add_argument("--output", action="store_true", help="Treat as output (check secrets, not injection)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.text == "-":
        import sys
        args.text = sys.stdin.read()

    verdict = inspect_output(args.text) if args.output else inspect_input(args.text)

    if args.json:
        print(json.dumps(verdict, indent=2))
    else:
        print(f"Block:   {verdict['block']}")
        print(f"Reason:  {verdict['reason']}")
        print(f"Matches: {len(verdict['matches'])}")
        for m in verdict['matches']:
            print(f"  - {m.get('type')}: {m.get('snippet', '')[:100]}")
        if args.output and verdict["sanitized"] != args.text:
            print()
            print("Sanitized output:")
            print(verdict["sanitized"])

    return 1 if verdict["block"] else 0


if __name__ == "__main__":
    import sys
    sys.exit(_cli() or 0)
