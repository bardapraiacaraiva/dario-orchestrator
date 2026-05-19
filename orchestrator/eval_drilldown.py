#!/usr/bin/env python3
"""
DARIO Eval Drilldown
====================
Upgrade 16 (operational complement to U7 golden_eval).

When `golden_eval.compare_against_golden` returns DRIFT or DEGRADED, the
caller learns the lexical/semantic/length/score numbers but NOT what
exactly changed. This module answers that question:

  - Which content tokens were present in golden but missing in candidate?
  - Which were added in candidate that aren't in golden?
  - Which markdown sections (# / ##) disappeared or were renamed?
  - Which paragraphs from golden are not echoed anywhere in candidate?
  - What concrete additions would recover MATCH verdict?

Pure inspection — no LLM, no embeddings beyond the cosine already computed
by golden_eval. Runs in milliseconds.

CLI:
    python eval_drilldown.py --eval EVAL-ID --candidate FILE
    python eval_drilldown.py --eval EVAL-ID --candidate FILE --json
    python eval_drilldown.py --all-drifting        Drilldown across drifting evals
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import golden_eval


# Stop words (shared with golden_eval / qvalue_memory)
_STOP = set(golden_eval._STOP) if hasattr(golden_eval, "_STOP") else set()


def _tokens(text: str) -> list:
    """Ordered tokens for diff (preserves duplicates for frequency analysis)."""
    raw = re.findall(r"\w{3,}", (text or "").lower())
    return [w for w in raw if w not in _STOP]


def _sections(text: str) -> list:
    """Extract markdown headers ## Section Name."""
    return re.findall(r"^#{1,3}\s+(.+?)\s*$", text or "", flags=re.MULTILINE)


def _paragraphs(text: str) -> list:
    """Non-empty paragraphs (separated by blank lines)."""
    return [p.strip() for p in re.split(r"\n\s*\n", (text or "")) if p.strip()]


def _paragraph_signature(p: str, k: int = 10) -> str:
    """First-N content-words of a paragraph — used to match paragraphs across versions."""
    toks = _tokens(p)[:k]
    return " ".join(toks)


def diff_dimensions(eval_id: str, candidate_text: str,
                    candidate_score: int = 0) -> dict:
    """Produce a structured comparison between candidate and golden.

    Returns:
        {
          "eval_id": ...,
          "compare": <golden_eval.compare_against_golden full result>,
          "tokens": {
              "lost": [...]      tokens in golden not in candidate,
              "gained": [...]    tokens in candidate not in golden,
              "shared": int,
              "lost_count": int,
              "gained_count": int,
              "top_lost": [(token, golden_freq), ...]   most-frequent lost tokens
          },
          "sections": {
              "golden": [...],
              "candidate": [...],
              "missing_in_candidate": [...],
              "added_in_candidate": [...],
          },
          "paragraphs": {
              "golden_count": int,
              "candidate_count": int,
              "missing_paragraphs": [signatures...]    paragraphs not echoed at all
          },
          "recovery_hints": [str, ...],
        }
    """
    text_file = golden_eval.GOLDEN_DIR / f"{eval_id}.golden.txt"
    meta_file = golden_eval.GOLDEN_DIR / f"{eval_id}.golden.json"
    if not text_file.exists() or not meta_file.exists():
        return {"status": "no_golden", "eval_id": eval_id}

    golden_text = text_file.read_text(encoding="utf-8")

    # 1. Use existing compare for top-line numbers
    compare = golden_eval.compare_against_golden(eval_id, candidate_text, candidate_score)

    # 2. Token diff
    g_tokens = _tokens(golden_text)
    c_tokens = _tokens(candidate_text)
    g_counter = Counter(g_tokens)
    c_counter = Counter(c_tokens)
    g_set = set(g_tokens)
    c_set = set(c_tokens)
    lost = sorted(g_set - c_set)
    gained = sorted(c_set - g_set)
    shared = len(g_set & c_set)
    top_lost = sorted(
        [(t, g_counter[t]) for t in lost],
        key=lambda x: -x[1]
    )[:15]

    # 3. Section diff
    g_sections = _sections(golden_text)
    c_sections = _sections(candidate_text)
    g_section_set = {s.lower().strip() for s in g_sections}
    c_section_set = {s.lower().strip() for s in c_sections}
    missing_sections = [s for s in g_sections if s.lower().strip() not in c_section_set]
    added_sections = [s for s in c_sections if s.lower().strip() not in g_section_set]

    # 4. Paragraph echo detection
    g_paragraphs = _paragraphs(golden_text)
    c_paragraphs = _paragraphs(candidate_text)
    c_sigs = [_paragraph_signature(p) for p in c_paragraphs]
    missing_paragraphs = []
    for p in g_paragraphs:
        sig = _paragraph_signature(p)
        if not sig:
            continue
        # Loose match: signature appears as substring in any candidate paragraph
        if not any(sig in cs or cs in sig for cs in c_sigs):
            missing_paragraphs.append(sig[:80])

    # 5. Recovery hints
    hints = []
    if compare.get("verdict") == "MATCH":
        hints.append("output already matches golden — no recovery needed")
    else:
        if compare.get("score_delta", 0) < -10:
            hints.append(
                f"score is {abs(compare['score_delta'])}pts below human "
                f"baseline ({compare.get('human_score')}) — quality regression"
            )
        if top_lost:
            top_3 = ", ".join(f"'{t}'" for t, _ in top_lost[:3])
            hints.append(f"add coverage for high-frequency lost tokens: {top_3}")
        if missing_sections:
            sec = "; ".join(f'"{s}"' for s in missing_sections[:3])
            hints.append(f"restore sections: {sec}")
        if missing_paragraphs:
            hints.append(
                f"{len(missing_paragraphs)} paragraph(s) from golden have no echo "
                f"in candidate (first: '{missing_paragraphs[0]}...')"
            )
        lr = compare.get("length_ratio", 1.0)
        if lr < 0.5:
            hints.append(f"output is {(1 - lr) * 100:.0f}% shorter than golden — expand content")
        elif lr > 2.5:
            hints.append(f"output is {(lr - 1) * 100:.0f}% longer than golden — verbose, trim")
        if not hints:
            hints.append("no specific recovery hint — review compare details for nuance")

    return {
        "status": "ok",
        "eval_id": eval_id,
        "compare": compare,
        "tokens": {
            "lost_count": len(lost),
            "gained_count": len(gained),
            "shared": shared,
            "lost": lost[:30],
            "gained": gained[:30],
            "top_lost": top_lost,
        },
        "sections": {
            "golden": g_sections,
            "candidate": c_sections,
            "missing_in_candidate": missing_sections,
            "added_in_candidate": added_sections,
        },
        "paragraphs": {
            "golden_count": len(g_paragraphs),
            "candidate_count": len(c_paragraphs),
            "missing_count": len(missing_paragraphs),
            "missing_paragraphs": missing_paragraphs[:10],
        },
        "recovery_hints": hints,
    }


def format_human(diff: dict) -> str:
    """Pretty-print drilldown report."""
    if diff.get("status") == "no_golden":
        return f"[!] no golden captured for {diff['eval_id']}"

    cmp_ = diff["compare"]
    eval_id = diff["eval_id"]
    out = [
        f"=== Eval Drilldown — {eval_id} ===",
        f"  Verdict:     {cmp_.get('verdict', '?')}",
        f"  Drift:       {cmp_.get('drift_severity', 'ok')}",
        f"  Score:       {cmp_.get('candidate_score', 0)} (human baseline {cmp_.get('human_score', '?')}, "
        f"delta {cmp_.get('score_delta', 0):+d})",
        f"  Lexical:     {cmp_.get('lexical_jaccard', 0)}  (1.0 = identical)",
        f"  Semantic:    {cmp_.get('semantic_cosine', 0)}",
        f"  Length:      ratio {cmp_.get('length_ratio', 0)}",
        "",
        "--- TOKEN DIFF ---",
        f"  Shared:      {diff['tokens']['shared']}",
        f"  Lost:        {diff['tokens']['lost_count']}  (in golden, not in candidate)",
        f"  Gained:      {diff['tokens']['gained_count']}  (in candidate, not in golden)",
    ]
    if diff["tokens"]["top_lost"]:
        out.append("  Top lost (by golden freq):")
        for tok, freq in diff["tokens"]["top_lost"][:8]:
            out.append(f"    - {tok} ({freq}x)")

    out.extend(["", "--- SECTIONS ---"])
    out.append(f"  Golden:    {len(diff['sections']['golden'])} headers")
    out.append(f"  Candidate: {len(diff['sections']['candidate'])} headers")
    if diff["sections"]["missing_in_candidate"]:
        out.append("  Missing:")
        for s in diff["sections"]["missing_in_candidate"][:6]:
            out.append(f"    - {s}")
    if diff["sections"]["added_in_candidate"]:
        out.append("  Added:")
        for s in diff["sections"]["added_in_candidate"][:6]:
            out.append(f"    - {s}")

    out.extend(["", "--- PARAGRAPHS ---"])
    out.append(f"  Golden:    {diff['paragraphs']['golden_count']}")
    out.append(f"  Candidate: {diff['paragraphs']['candidate_count']}")
    out.append(f"  Missing (no echo): {diff['paragraphs']['missing_count']}")
    if diff["paragraphs"]["missing_paragraphs"]:
        for p in diff["paragraphs"]["missing_paragraphs"][:3]:
            out.append(f"    - {p}...")

    out.extend(["", "--- RECOVERY HINTS ---"])
    for h in diff["recovery_hints"]:
        out.append(f"  > {h}")

    return "\n".join(out)


def drilldown_drifting(eval_ids: list = None) -> dict:
    """Run drilldown on all evals that are currently drifting against their goldens.

    Uses cached runs in evals/last_runs/ if present, otherwise reports
    no_candidate. Returns aggregate report.
    """
    runs_dir = golden_eval.EVAL_DIR / "last_runs"
    if not runs_dir.exists():
        return {"status": "no_runs_dir", "evals": []}

    goldens = golden_eval.list_goldens()
    if eval_ids:
        goldens = [g for g in goldens if g["eval_id"] in eval_ids]

    reports = []
    for g in goldens:
        eid = g["eval_id"]
        candidate_file = runs_dir / f"{eid}.output.txt"
        if not candidate_file.exists():
            continue
        candidate_text = candidate_file.read_text(encoding="utf-8")
        score_file = runs_dir / f"{eid}.score.json"
        score = 0
        if score_file.exists():
            try:
                score = int(json.loads(score_file.read_text()).get("score", 0))
            except Exception:
                pass
        diff = diff_dimensions(eid, candidate_text, score)
        verdict = diff.get("compare", {}).get("verdict", "?")
        if verdict in ("DRIFT", "DEGRADED"):
            reports.append(diff)

    return {
        "status": "ok",
        "total_drifting": len(reports),
        "evals": reports,
    }


def main():
    p = argparse.ArgumentParser(description="DARIO Eval Drilldown")
    p.add_argument("--eval", help="Eval ID to drilldown")
    p.add_argument("--candidate", help="Candidate output file to compare")
    p.add_argument("--score", type=int, default=0, help="Candidate's auto-score")
    p.add_argument("--all-drifting", action="store_true",
                   help="Drilldown across all drifting evals (uses evals/last_runs/)")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.all_drifting:
        r = drilldown_drifting()
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.json
              else f"{r['total_drifting']} drifting eval(s)")
        return 0 if r.get("total_drifting", 0) == 0 else 2

    if args.eval and args.candidate:
        text = Path(args.candidate).read_text(encoding="utf-8")
        diff = diff_dimensions(args.eval, text, args.score)
        if args.json:
            print(json.dumps(diff, indent=2, ensure_ascii=False))
        else:
            print(format_human(diff))
        verdict = diff.get("compare", {}).get("verdict")
        return 0 if verdict == "MATCH" else (1 if verdict == "DEGRADED" else 2)

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
