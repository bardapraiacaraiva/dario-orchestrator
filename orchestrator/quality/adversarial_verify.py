"""Adversarial output verification for client-facing work (Next-Gen N4, 2026-06-12).

The Padrão A wrappers critique INSIDE the generating context — that is what
caps quality at the ~85 structural ceiling (caminho B, 2026-05-23). This
module is the independent skeptic: it never saw the generation, it only
tries to find reasons the deliverable should NOT ship.

Two layers:
  1. DETERMINISTIC (always on, zero cost): placeholder leakage, broken
     arithmetic in totals, internal contradictions on repeated money
     amounts, empty sections, missing/invalid confidence block (G5).
  2. LLM JUDGE (best-effort, Haiku): refutation-prompted second opinion —
     runs only when the Anthropic SDK + key are available (autonomous
     path); silently skipped otherwise. The deterministic layer is the
     tested contract; the judge is an enhancement.

Honesty note: this does NOT break the 90+ ceiling — human review remains
the gate for delivery. What it does is reduce the ERROR RATE reaching the
human: a deliverable with a [CONFIRMAR] leak or a broken total now arrives
in in_review with the issues pre-identified instead of arriving as "done".

Confidence block (G5): client_facing/financial outputs must end with a
machine-readable block the prompt builder now requests:

    ```json
    {"confidence": {"mode": "HIGH_CONFIDENCE", "score": 82,
                    "verified_facts": [...], "assumed_facts": [...],
                    "needs_client_confirmation": [...]}}
    ```
"""

import json
import logging
import re
import secrets
from datetime import UTC, datetime
from pathlib import Path

log = logging.getLogger("adversarial_verify")

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
QUEUE_DIR = ORCH_DIR / "human_review_queue"  # same dir as cognitive/human_review_queue.py

VERIFIED_POLICIES = {"client_facing", "financial"}

# Placeholder patterns that must never reach a client deliverable as-is.
_CRITICAL_PLACEHOLDERS = [
    (re.compile(r"\[CONFIRMAR[^\]]*\]", re.I), "[CONFIRMAR] tag left in deliverable"),
    (re.compile(r"<(client|cliente|project|projeto|date|data|name|nome|empresa)>", re.I),
     "angle-bracket placeholder left in deliverable"),
    (re.compile(r"\{\{[^}]+\}\}"), "template variable {{...}} left in deliverable"),
    (re.compile(r"\b(TODO|TBD|FIXME)\b"), "TODO/TBD/FIXME left in deliverable"),
    (re.compile(r"lorem ipsum", re.I), "lorem ipsum filler text"),
    (re.compile(r"\bYYYY-MM-DD\b"), "literal YYYY-MM-DD date placeholder"),
]

# Sanctioned-but-flag-worthy: invented examples are allowed in drafts, but a
# client_facing FINAL carrying them needs a human pass before sending.
_MEDIUM_PLACEHOLDERS = [
    (re.compile(r"\[EXEMPLO\]", re.I), "[EXEMPLO] invented data — confirm before client sees it"),
]

_MONEY = r"(?:€|R\$|\$)\s*([\d][\d\s.,]*)"


def _to_number(raw: str) -> float | None:
    """Parse a PT/BR/US formatted money string to float (best-effort)."""
    s = raw.strip().replace(" ", "").replace(" ", "")
    if not s:
        return None
    # 1.234,56 (PT/BR) vs 1,234.56 (US) vs 1234.56
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        # comma as decimal if exactly 2 digits follow, else thousands
        s = s.replace(",", ".") if re.search(r",\d{2}$", s) else s.replace(",", "")
    elif s.count(".") > 1 or re.search(r"\.\d{3}$", s):
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def check_placeholders(output: str) -> list[dict]:
    issues = []
    for pat, reason in _CRITICAL_PLACEHOLDERS:
        m = pat.search(output)
        if m:
            issues.append({"type": "placeholder", "severity": "critical",
                           "quote": m.group(0)[:60], "reason": reason})
    for pat, reason in _MEDIUM_PLACEHOLDERS:
        m = pat.search(output)
        if m:
            issues.append({"type": "placeholder", "severity": "medium",
                           "quote": m.group(0)[:60], "reason": reason})
    return issues


def check_table_totals(output: str, tolerance: float = 0.01) -> list[dict]:
    """Markdown tables where a Total row mismatches the sum of its column."""
    issues = []
    for table in re.split(r"\n\s*\n", output):
        rows = [r for r in table.splitlines() if r.strip().startswith("|")]
        if len(rows) < 3:
            continue
        body = [r for r in rows if not re.match(r"^\s*\|[\s:|-]+\|?\s*$", r)]
        parsed = [[c.strip() for c in r.strip().strip("|").split("|")] for r in body]
        total_rows = [p for p in parsed if p and re.search(r"\btotal\b", p[0], re.I)]
        if not total_rows:
            continue
        data_rows = [p for p in parsed[1:] if p not in total_rows]
        for col in range(1, max(len(p) for p in parsed)):
            vals = []
            for p in data_rows:
                if col < len(p):
                    m = re.search(_MONEY, p[col])
                    n = _to_number(m.group(1)) if m else None
                    if n is not None:
                        vals.append(n)
            if len(vals) < 2:
                continue
            for trow in total_rows:
                if col < len(trow):
                    m = re.search(_MONEY, trow[col])
                    declared = _to_number(m.group(1)) if m else None
                    if declared is None:
                        continue
                    real = sum(vals)
                    if abs(real - declared) > max(tolerance, 0.005 * max(real, declared)):
                        issues.append({
                            "type": "math", "severity": "critical",
                            "quote": trow[col][:60],
                            "reason": (f"table total declares {declared:,.2f} but the "
                                       f"column sums to {real:,.2f}")})
    return issues


def check_contradictions(output: str) -> list[dict]:
    """The same labelled total stated twice with different amounts."""
    issues = []
    found: dict[str, set[float]] = {}
    for m in re.finditer(r"(?im)^.*?\b(total[^:€$R\n]{0,40}):?\s*" + _MONEY, output):
        label = re.sub(r"\s+", " ", m.group(1).strip().lower())
        n = _to_number(m.group(2))
        if n is not None:
            found.setdefault(label, set()).add(round(n, 2))
    for label, values in found.items():
        if len(values) > 1:
            issues.append({"type": "contradiction", "severity": "critical",
                           "quote": label[:60],
                           "reason": f"'{label}' stated with conflicting values: "
                                     f"{sorted(values)}"})
    return issues


def check_empty_sections(output: str) -> list[dict]:
    issues = []
    for m in re.finditer(r"(?m)^(#{2,4}\s+.+)\n+(?=#{2,4}\s|\Z)", output):
        issues.append({"type": "structure", "severity": "medium",
                       "quote": m.group(1)[:60].strip(),
                       "reason": "section header with no content"})
    return issues


# ─── Confidence block (G5) ─────────────────────────────────────────────────

_CONF_FENCE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)


def parse_confidence_block(output: str) -> dict | None:
    """Extract the machine-readable confidence block, newest-last wins."""
    for raw in reversed(_CONF_FENCE.findall(output or "")):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        conf = data.get("confidence") if isinstance(data, dict) else None
        if isinstance(conf, dict):
            return conf
    return None


def check_confidence_block(output: str) -> tuple[dict | None, list[dict]]:
    conf = parse_confidence_block(output)
    if conf is None:
        return None, [{"type": "confidence", "severity": "medium",
                       "quote": "(missing)",
                       "reason": "no machine-readable confidence block at end of output"}]
    issues = []
    score = conf.get("score")
    if not isinstance(score, (int, float)) or not (0 <= score <= 100):
        issues.append({"type": "confidence", "severity": "medium",
                       "quote": str(score)[:40],
                       "reason": "confidence.score missing or outside 0-100"})
    if conf.get("mode") not in ("HIGH_CONFIDENCE", "UNCERTAINTY", "EXPLORATION"):
        issues.append({"type": "confidence", "severity": "medium",
                       "quote": str(conf.get("mode"))[:40],
                       "reason": "confidence.mode must be HIGH_CONFIDENCE|UNCERTAINTY|EXPLORATION"})
    return conf, issues


# ─── LLM judge (best-effort enhancement) ───────────────────────────────────

def llm_judge(task: dict, output: str) -> list[dict]:
    """Refutation-prompted Haiku pass. Empty list when SDK/key unavailable."""
    try:
        from scripts.anthropic_spend_wrapper import TrackedAnthropic
        client = TrackedAnthropic(caller="quality/adversarial_verify")
        prompt = (
            "You are an adversarial reviewer. Your ONLY job is to find reasons this "
            "deliverable should NOT be sent to the client. Look for: fabricated facts "
            "(laws, statistics, names), unsupported claims, numbers that do not add up, "
            "promises the vendor cannot keep. Respond ONLY with JSON: "
            '{"issues": [{"severity": "critical|medium", "quote": "...", "reason": "..."}]} '
            "— an empty issues list if you genuinely find nothing.\n\n"
            f"TASK: {task.get('title', '')}\n\nDELIVERABLE:\n{output[:12000]}"
        )
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=1024,
            messages=[{"role": "user", "content": prompt}])
        text = resp.content[0].text
        m = re.search(r"\{.*\}", text, re.S)
        data = json.loads(m.group(0)) if m else {}
        out = []
        for i in data.get("issues", [])[:10]:
            if isinstance(i, dict) and i.get("reason"):
                out.append({"type": "llm_judge",
                            "severity": "critical" if i.get("severity") == "critical" else "medium",
                            "quote": str(i.get("quote", ""))[:80],
                            "reason": str(i["reason"])[:200]})
        return out
    except Exception:
        return []  # judge unavailable — the deterministic layer stands alone


# ─── Public API ────────────────────────────────────────────────────────────

def verify_output(task: dict, output: str, use_llm_judge: bool = True) -> dict:
    """Independent verification verdict for a deliverable.

    Returns {"verdict": "pass"|"flag", "critical": bool, "issues": [...],
             "confidence": dict|None} — critical issues mean the output must
    NOT complete as done; route it to in_review with the issues attached.
    """
    policy = (task or {}).get("execution_policy", "default")
    issues = []
    issues += check_placeholders(output)
    issues += check_table_totals(output)
    issues += check_contradictions(output)
    issues += check_empty_sections(output)
    confidence, conf_issues = check_confidence_block(output)
    if policy in VERIFIED_POLICIES:
        issues += conf_issues
    if use_llm_judge:
        issues += llm_judge(task, output)

    critical = any(i["severity"] == "critical" for i in issues)
    return {
        "verdict": "flag" if issues else "pass",
        "critical": critical,
        "issues": issues,
        "confidence": confidence,
    }


def enqueue_for_review(task: dict, output: str, verdict: dict) -> str | None:
    """Drop a flagged deliverable into the human review queue (same file
    conventions as cognitive/human_review_queue.py cmd_add)."""
    try:
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        item_id = secrets.token_hex(3)
        ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
        base = f"{task.get('skill', 'unknown')}__{ts}__{item_id}"
        (QUEUE_DIR / f"{base}.md").write_text(output, encoding="utf-8")
        reasons = "; ".join(i["reason"] for i in verdict["issues"][:5])
        meta = {
            "id": item_id,
            "skill": task.get("skill", ""),
            "context": f"task {task.get('id', '')} — adversarial verify (N4)",
            "ai_score": None,
            "ai_verdict": "verifier-flagged",
            "ai_reasoning": reasons[:500],
            "added_at": datetime.now(UTC).isoformat(),
            "state": "pending",
            "polished_at": None,
            "polished_score": None,
            "time_to_resolution_minutes": None,
        }
        import yaml
        (QUEUE_DIR / f"{base}.meta.yaml").write_text(
            yaml.safe_dump(meta, allow_unicode=True), encoding="utf-8")
        return item_id
    except Exception as e:
        log.warning(f"enqueue_for_review failed: {e}")
        return None
