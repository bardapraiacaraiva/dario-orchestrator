#!/usr/bin/env python3
"""
DARIO Golden Eval — Ground-Truth Regression Detection
=====================================================
Upgrade 7 (Sprint 3) of the Cognitive Audit roadmap.

eval_suite.py runs 14 eval cases against `expected_keywords` + `min_length` +
`not_error`. That is VALIDATION (does the output look plausible?) not
VERIFICATION (does it match a known-good output?). No human-verified
golden output. Drift is silent.

This module adds the verification layer:
  1. capture_golden(eval_id, output, human_score, human_dimensions)
     — record a human-reviewed reference for an eval case
  2. compare_against_golden(eval_id, candidate_output, candidate_score)
     — lexical jaccard + length ratio + semantic cosine + score delta
  3. regression_check([eval_ids])
     — run all golden comparisons, alert if drift > 10pts vs baseline
  4. calibration_log
     — append-only ledger of when goldens were captured/refreshed

Storage layout:
    ~/.claude/orchestrator/evals/golden/
        {eval_id}.golden.txt     The actual reference output text
        {eval_id}.golden.json    Metadata: human_score, dimensions, captured_at, notes
    ~/.claude/orchestrator/evals/calibration_log.yaml
        Append-only audit trail of capture/recapture events

Semantic similarity uses the same nomic-embed-text already cached for
semantic_dispatch — zero new dependencies.

CLI:
    python golden_eval.py --capture EVAL-ID --output-file path.txt --human-score 92
    python golden_eval.py --compare EVAL-ID --candidate path.txt --score 78
    python golden_eval.py --regression-check          Run all goldens, report drift
    python golden_eval.py --list                      Which evals have goldens?
    python golden_eval.py --status                    Calibration log summary
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _yaml.load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(data, f)
except ImportError:
    import yaml as _pyaml

    def _load_yaml(path):
        with open(path, encoding="utf-8") as f:
            return _pyaml.safe_load(f)

    def _dump_yaml(data, path):
        with open(path, "w", encoding="utf-8") as f:
            _pyaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


ORCH_DIR = Path.home() / ".claude" / "orchestrator"
EVAL_DIR = ORCH_DIR / "evals"
GOLDEN_DIR = EVAL_DIR / "golden"
CALIBRATION_LOG = EVAL_DIR / "calibration_log.yaml"

# Drift thresholds
DRIFT_WARN_PTS = 5     # score deviation that warrants a soft warn
DRIFT_ALERT_PTS = 10   # hard alert — eval regressing
LEXICAL_MIN = 0.30     # jaccard below this = very different from golden
SEMANTIC_MIN = 0.50    # cosine below this = topical mismatch
LENGTH_RATIO_MIN = 0.5
LENGTH_RATIO_MAX = 2.5

# Same stop words as Q-value memory — focus on content words
_STOP = {
    "a", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos",
    "em", "na", "no", "nas", "nos", "para", "por", "com", "sem", "que",
    "se", "e", "ou", "mas", "como", "the", "an", "of", "to", "for",
    "and", "or", "but", "in", "on", "at", "by", "with", "from", "is",
    "are", "was", "were", "be", "this", "that", "these", "those",
}


def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def _tokens(text: str) -> set:
    """Content-word tokens (lowercase, stop-words removed)."""
    raw = re.findall(r"\w{3,}", (text or "").lower())
    return {w for w in raw if w not in _STOP}


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = a & b
    union = a | b
    return len(inter) / len(union) if union else 0.0


def _length_ratio(candidate: str, golden: str) -> float:
    lc, lg = len(candidate or ""), len(golden or "")
    if lg == 0:
        return 1.0 if lc == 0 else float("inf")
    return lc / lg


def _semantic_similarity(text_a: str, text_b: str) -> float:
    """Cosine similarity via Ollama nomic-embed-text. Returns 0.0 on failure."""
    try:
        sys.path.insert(0, str(ORCH_DIR))
        from dispatch.semantic_dispatch import _cosine, _embed
        va = _embed(text_a[:4000])
        vb = _embed(text_b[:4000])
        if not va or not vb:
            return 0.0
        return _cosine(va, vb)
    except Exception:
        return 0.0


def capture_golden(eval_id: str, output_text: str, human_score: int,
                   human_dimensions: dict = None, notes: str = "",
                   force: bool = False) -> dict:
    """Record a human-reviewed golden output for an eval case.

    Idempotent unless force=True. If an existing golden exists with same
    content hash, returns 'unchanged' verdict and skips write.
    """
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    if not eval_id or not output_text:
        return {"status": "error", "reason": "missing eval_id or output_text"}

    text_file = GOLDEN_DIR / f"{eval_id}.golden.txt"
    meta_file = GOLDEN_DIR / f"{eval_id}.golden.json"

    new_hash = _hash(output_text)
    existing_meta = {}
    if meta_file.exists():
        try:
            existing_meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception:
            existing_meta = {}

    if existing_meta.get("content_hash") == new_hash and not force:
        return {"status": "unchanged", "eval_id": eval_id,
                "captured_at": existing_meta.get("captured_at")}

    text_file.write_text(output_text, encoding="utf-8")
    meta = {
        "eval_id": eval_id,
        "content_hash": new_hash,
        "human_score": int(human_score),
        "human_dimensions": human_dimensions or {},
        "captured_at": datetime.now(UTC).isoformat(),
        "char_count": len(output_text),
        "token_count": len(_tokens(output_text)),
        "notes": notes,
        "version": (existing_meta.get("version", 0) or 0) + 1,
    }
    meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    _log_calibration("capture", eval_id, meta, notes)
    return {"status": "captured", "eval_id": eval_id, "version": meta["version"],
            "human_score": meta["human_score"]}


def compare_against_golden(eval_id: str, candidate_output: str,
                            candidate_score: int = 0) -> dict:
    """Compare a candidate output to the stored golden. Returns full report."""
    text_file = GOLDEN_DIR / f"{eval_id}.golden.txt"
    meta_file = GOLDEN_DIR / f"{eval_id}.golden.json"

    if not text_file.exists() or not meta_file.exists():
        return {
            "status": "no_golden",
            "eval_id": eval_id,
            "message": "no golden captured yet — use capture_golden() first",
        }

    golden_text = text_file.read_text(encoding="utf-8")
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    human_score = int(meta.get("human_score", 0))

    # 1. Lexical overlap (jaccard of content words)
    cand_tokens = _tokens(candidate_output)
    gold_tokens = _tokens(golden_text)
    lex = _jaccard(cand_tokens, gold_tokens)

    # 2. Length ratio (candidate / golden)
    length_ratio = _length_ratio(candidate_output, golden_text)

    # 3. Semantic similarity (cosine of embeddings)
    sem = _semantic_similarity(candidate_output, golden_text)

    # 4. Score delta vs human baseline
    score_delta = candidate_score - human_score
    drift_severity = "ok"
    if abs(score_delta) >= DRIFT_ALERT_PTS:
        drift_severity = "alert"
    elif abs(score_delta) >= DRIFT_WARN_PTS:
        drift_severity = "warn"

    # 5. Combined verdict
    flags = []
    if lex < LEXICAL_MIN:
        flags.append(f"low_lexical_overlap ({lex:.2f} < {LEXICAL_MIN})")
    if sem < SEMANTIC_MIN:
        flags.append(f"low_semantic_similarity ({sem:.2f} < {SEMANTIC_MIN})")
    if length_ratio < LENGTH_RATIO_MIN:
        flags.append(f"output_too_short (ratio {length_ratio:.2f})")
    elif length_ratio > LENGTH_RATIO_MAX:
        flags.append(f"output_too_long (ratio {length_ratio:.2f})")
    if abs(score_delta) >= DRIFT_ALERT_PTS:
        flags.append(f"score_drift {score_delta:+d}pts vs human baseline")

    if not flags:
        verdict = "MATCH"
    elif drift_severity == "alert" or lex < LEXICAL_MIN or sem < SEMANTIC_MIN:
        verdict = "DRIFT"
    else:
        verdict = "DEGRADED"

    return {
        "status": "compared",
        "eval_id": eval_id,
        "verdict": verdict,
        "drift_severity": drift_severity,
        "human_score": human_score,
        "candidate_score": candidate_score,
        "score_delta": score_delta,
        "lexical_jaccard": round(lex, 3),
        "semantic_cosine": round(sem, 3),
        "length_ratio": round(length_ratio, 3),
        "candidate_tokens": len(cand_tokens),
        "golden_tokens": len(gold_tokens),
        "flags": flags,
        "golden_version": meta.get("version", 1),
        "golden_captured_at": meta.get("captured_at"),
    }


def _log_calibration(action: str, eval_id: str, meta: dict, notes: str = ""):
    """Append-only log of capture/recapture events."""
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    log_data = {"calibrations": []}
    if CALIBRATION_LOG.exists():
        try:
            existing = _load_yaml(str(CALIBRATION_LOG))
            if isinstance(existing, dict) and "calibrations" in existing:
                log_data = existing
        except Exception:
            pass
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "action": action,
        "eval_id": eval_id,
        "version": meta.get("version", 1),
        "human_score": meta.get("human_score"),
        "content_hash": meta.get("content_hash"),
        "notes": notes,
    }
    log_data["calibrations"].append(entry)
    _dump_yaml(log_data, str(CALIBRATION_LOG))


def list_goldens() -> list:
    """All eval cases with a golden captured."""
    if not GOLDEN_DIR.exists():
        return []
    out = []
    for meta_file in sorted(GOLDEN_DIR.glob("*.golden.json")):
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            out.append({
                "eval_id": meta.get("eval_id"),
                "human_score": meta.get("human_score"),
                "version": meta.get("version", 1),
                "captured_at": meta.get("captured_at"),
                "char_count": meta.get("char_count"),
            })
        except Exception:
            continue
    return out


def regression_check(eval_ids: list = None) -> dict:
    """Run all golden comparisons against last-known candidate outputs.
    For now, compares against any cached candidate outputs in evals/runs/
    or generates a stub report if none exist.

    Returns:
        {
          "total_evals": N,
          "with_golden": M,
          "drifting": [eval_id...],
          "alerts": [eval_id...],
          "report": [per-eval comparison],
        }
    """
    goldens = list_goldens()
    if eval_ids:
        goldens = [g for g in goldens if g["eval_id"] in eval_ids]

    report = []
    drifting = []
    alerts = []

    # Look for cached candidate outputs in evals/last_runs/
    runs_dir = EVAL_DIR / "last_runs"
    for g in goldens:
        eid = g["eval_id"]
        candidate_file = runs_dir / f"{eid}.output.txt" if runs_dir.exists() else None
        if not candidate_file or not candidate_file.exists():
            report.append({
                "eval_id": eid,
                "status": "no_candidate",
                "message": "no recent run output to compare",
            })
            continue
        candidate_text = candidate_file.read_text(encoding="utf-8")
        score_file = runs_dir / f"{eid}.score.json"
        candidate_score = 0
        if score_file.exists():
            try:
                candidate_score = int(json.loads(score_file.read_text())
                                      .get("score", 0))
            except Exception:
                pass
        comp = compare_against_golden(eid, candidate_text, candidate_score)
        report.append(comp)
        if comp.get("verdict") == "DRIFT":
            drifting.append(eid)
        if comp.get("drift_severity") == "alert":
            alerts.append(eid)

    return {
        "total_evals": len(goldens),
        "with_golden": len(goldens),
        "drifting": drifting,
        "alerts": alerts,
        "report": report,
    }


def calibration_status() -> dict:
    """Summary of calibration log."""
    if not CALIBRATION_LOG.exists():
        return {"total_entries": 0, "captures": 0}
    try:
        data = _load_yaml(str(CALIBRATION_LOG))
        entries = (data or {}).get("calibrations", []) if isinstance(data, dict) else []
    except Exception:
        return {"total_entries": 0, "error": "log unreadable"}

    captures = [e for e in entries if e.get("action") == "capture"]
    return {
        "total_entries": len(entries),
        "captures": len(captures),
        "last_capture": captures[-1] if captures else None,
        "distinct_evals": len({e.get("eval_id") for e in captures}),
    }


def main():
    # license_guard wired (v11.1+ hardening)
    try:
        from licensing.license_guard import enforce_or_exit
        enforce_or_exit("golden_eval")
    except SystemExit:
        raise
    except Exception:
        pass  # license_guard unavailable — fail-open during dev/testing

    p = argparse.ArgumentParser(description="DARIO Golden Eval")
    p.add_argument("--capture", help="Eval ID to capture golden for")
    p.add_argument("--output-file", help="File with output text to capture/compare")
    p.add_argument("--human-score", type=int, help="Human-verified score for capture")
    p.add_argument("--dimensions", help="JSON human dimensions for capture")
    p.add_argument("--notes", default="", help="Capture notes")
    p.add_argument("--force", action="store_true", help="Re-capture even if unchanged")
    p.add_argument("--compare", help="Eval ID to compare candidate against golden")
    p.add_argument("--candidate", help="Candidate output text file for --compare")
    p.add_argument("--score", type=int, default=0, help="Candidate's auto-score")
    p.add_argument("--regression-check", action="store_true")
    p.add_argument("--list", action="store_true", help="List goldens captured")
    p.add_argument("--status", action="store_true", help="Calibration log summary")
    p.add_argument("--json", "-j", action="store_true")
    args = p.parse_args()

    if args.list:
        out = list_goldens()
        if args.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            for g in out:
                print(f"  {g['eval_id']:30s} v{g['version']}  human={g['human_score']}  "
                      f"chars={g['char_count']}  @ {g['captured_at']}")
            print(f"\n{len(out)} goldens captured")
        return 0

    if args.status:
        s = calibration_status()
        print(json.dumps(s, indent=2, ensure_ascii=False) if args.json
              else "\n".join(f"  {k}: {v}" for k, v in s.items()))
        return 0

    if args.capture:
        if not args.output_file or args.human_score is None:
            print("--capture requires --output-file and --human-score", file=sys.stderr)
            return 1
        text = Path(args.output_file).read_text(encoding="utf-8")
        dims = json.loads(args.dimensions) if args.dimensions else None
        r = capture_golden(args.capture, text, args.human_score,
                           human_dimensions=dims, notes=args.notes, force=args.force)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.json
              else f"[{r['status']}] {r.get('eval_id', args.capture)}: {r}")
        return 0

    if args.compare:
        if not args.candidate:
            print("--compare requires --candidate", file=sys.stderr)
            return 1
        text = Path(args.candidate).read_text(encoding="utf-8")
        r = compare_against_golden(args.compare, text, args.score)
        if args.json:
            print(json.dumps(r, indent=2, ensure_ascii=False))
        else:
            print(f"Verdict: {r.get('verdict', r.get('status'))}")
            for k in ("lexical_jaccard", "semantic_cosine", "length_ratio",
                      "score_delta", "drift_severity"):
                if k in r:
                    print(f"  {k}: {r[k]}")
            for f in r.get("flags", []):
                print(f"  ! {f}")
        return 0 if r.get("verdict") in ("MATCH", "DEGRADED") else 2

    if args.regression_check:
        r = regression_check()
        if args.json:
            print(json.dumps(r, indent=2, ensure_ascii=False))
        else:
            print(f"Total evals with golden: {r['with_golden']}")
            print(f"Drifting: {r['drifting'] or 'none'}")
            print(f"Alerts:   {r['alerts'] or 'none'}")
        return 0 if not r.get("alerts") else 2

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
