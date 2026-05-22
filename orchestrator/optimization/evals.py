"""Eval dataset loader for DSPy optimisation (Onda 4 #5 pilot).

Re-uses the goldens already captured by `golden_eval.py` to build a small
training set. Each golden becomes one `dspy.Example` with:

    inputs:  briefing (the original eval prompt)
    outputs: posicionamento, archetype, tom_de_voz, diferenciadores
             (parsed from the golden's saved output)

For the pilot, we expect ~3-5 examples for `dario-brand`. DSPy's
BootstrapFewShot can compile useful programs from datasets that small;
MIPRO needs ~20+ to shine.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import dspy

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
# golden_eval.py uses "golden" (singular). Mirror that.
GOLDEN_DIR = ORCH_DIR / "evals" / "golden"


def _parse_brand_output(text: str) -> dict[str, Any]:
    """Best-effort parse of a markdown brand output into the four fields.

    Goldens are saved as freeform markdown. We grep for the obvious section
    headers in PT/EN. Anything we can't parse becomes empty — the example
    is still useful for the briefing → output mapping, even with partial
    target labels.
    """
    out: dict[str, Any] = {
        "posicionamento": "",
        "archetype": "",
        "tom_de_voz": "",
        "diferenciadores": [],
    }
    # Positioning
    m = re.search(
        r"(?im)^#{1,3}\s*(posicionamento|positioning)\b[^\n]*\n+([^\n#]+(?:\n[^\n#]+)*)",
        text,
    )
    if m:
        out["posicionamento"] = m.group(2).strip()
    # Archetype
    m = re.search(r"(?im)archetype[:\s]+(\w+)", text)
    if m:
        out["archetype"] = m.group(1).strip()
    # Tone
    m = re.search(
        r"(?im)^#{1,3}\s*(tom[\s_]de[\s_]voz|tone of voice)\b[^\n]*\n+([^\n#]+)",
        text,
    )
    if m:
        out["tom_de_voz"] = m.group(2).strip()
    # Differentiators (bulleted list)
    diffs: list[str] = []
    in_section = False
    for line in text.splitlines():
        if re.match(r"(?i)^#{1,3}\s*(diferencia|differentiat)", line):
            in_section = True
            continue
        if in_section:
            if line.startswith("#"):
                break
            stripped = line.lstrip("*- ").strip()
            if stripped:
                diffs.append(stripped)
            if len(diffs) >= 5:
                break
    out["diferenciadores"] = diffs[:5]
    return out


def load_brand_examples() -> list[dspy.Example]:
    """Discover goldens for `dario-brand` and return DSPy examples."""
    examples: list[dspy.Example] = []
    if not GOLDEN_DIR.exists():
        return examples

    for golden_file in GOLDEN_DIR.glob("*.golden.txt"):
        # Companion metadata file is `.json` next to `.golden.txt`.
        # NOTE: `with_suffix(".json")` on `name.golden.txt` produces `name.golden.json`.
        meta_file = golden_file.with_suffix(".json")
        meta: dict[str, Any] = {}
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
            except Exception:
                meta = {}

        # Identify dario-brand goldens via three signals: explicit `skill`
        # field, eval_id prefix `brand-`, or notes/briefing presence.
        eval_id = meta.get("eval_id", "") or golden_file.stem.replace(".golden", "")
        is_brand = (
            meta.get("skill", "").startswith("dario-brand")
            or eval_id.startswith("brand-")
            or eval_id.startswith("dario-brand-")
        )
        if not is_brand:
            continue

        # Briefing may live in `input`, `briefing`, or `notes` (legacy fallback).
        briefing = (
            meta.get("input", "")
            or meta.get("briefing", "")
            or meta.get("notes", "")
        )
        if not briefing:
            continue

        output_text = golden_file.read_text(encoding="utf-8")
        parsed = _parse_brand_output(output_text)

        ex = dspy.Example(
            briefing=briefing,
            posicionamento=parsed["posicionamento"],
            archetype=parsed["archetype"],
            tom_de_voz=parsed["tom_de_voz"],
            diferenciadores=parsed["diferenciadores"],
        ).with_inputs("briefing")
        examples.append(ex)

    return examples


def brand_score(example: dspy.Example, pred: Any, trace: Any = None) -> float:
    """Composite score: 0.4 keyword overlap + 0.3 length + 0.3 archetype match.

    Used as DSPy metric during BootstrapFewShot. Returns a float in [0, 1].
    """
    if pred is None:
        return 0.0

    score = 0.0
    # Keyword overlap on positioning
    gold_words = set((example.posicionamento or "").lower().split())
    pred_words = set((getattr(pred, "posicionamento", "") or "").lower().split())
    if gold_words:
        overlap = len(gold_words & pred_words) / len(gold_words)
        score += 0.4 * overlap

    # Length plausibility (50-400 chars target)
    plen = len(getattr(pred, "posicionamento", "") or "")
    if 50 <= plen <= 400:
        score += 0.3
    elif 25 <= plen <= 800:
        score += 0.15

    # Archetype exact match (case-insensitive)
    gold_arch = (example.archetype or "").lower().strip()
    pred_arch = (getattr(pred, "archetype", "") or "").lower().strip()
    if gold_arch and pred_arch and gold_arch == pred_arch:
        score += 0.3
    elif gold_arch and pred_arch and gold_arch in pred_arch:
        score += 0.15

    return min(score, 1.0)


__all__ = ["load_brand_examples", "brand_score"]
