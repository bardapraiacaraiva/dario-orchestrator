#!/usr/bin/env python3
"""
Reconcile skill-metrics.yaml: rebuild aggregate fields from the trustworthy
real `scores[]` array, undoing the corruption left by the ARCHIVED DSPy
sprint3 compile (compile_sprint3.py overwrote avg_quality_score with synthetic
compiled values and inflated total_executions).

Canonical method mirrors quality_scorer.py:update_skill_metrics:
    avg_quality_score = mean(scores[-20:])   # recent performance
    avg_quality_alltime = mean(scores)
    revision_rate = count(s < 60) / len(scores)
    total_executions = len(scores)           # real scored runs only

Preserves pre_compile_baseline_sprint3 / live_scores_compiled_sprint3 /
score_history as archived audit trail (no hard delete).

Usage:
    python reconcile_skill_metrics.py            # dry-run (default, no writes)
    python reconcile_skill_metrics.py --apply    # write, after timestamped backup
"""
import datetime
import shutil
import sys
from pathlib import Path

import yaml

SHIP_THRESHOLD = 60
RECENT = 20
PATH = Path(__file__).with_name("skill-metrics.yaml")


def num_scores(meta):
    out = []
    for s in (meta.get("scores") or []):
        v = s.get("score") if isinstance(s, dict) else s
        if isinstance(v, (int, float)):
            out.append(v)
    return out


def main():
    apply = "--apply" in sys.argv
    data = yaml.safe_load(PATH.read_text(encoding="utf-8"))
    skills = data.get("skills", {})
    changed = []
    for name, meta in skills.items():
        if not isinstance(meta, dict):
            continue
        scores = num_scores(meta)
        if not scores:
            continue
        new_avg = round(sum(scores[-RECENT:]) / len(scores[-RECENT:]), 1)
        new_alltime = round(sum(scores) / len(scores), 1)
        new_rev = round(sum(1 for s in scores if s < SHIP_THRESHOLD) / len(scores), 2)
        new_n = len(scores)
        new_tier = "A" if new_avg >= 85 else "B" if new_avg >= 75 else "C"

        old_avg = meta.get("avg_quality_score")
        old_n = meta.get("total_executions")
        if (old_avg != new_avg) or (old_n != new_n):
            changed.append((name, old_avg, new_avg, old_n, new_n))

        # Archive the sprint3 residue under a clearly-labelled key (don't delete).
        if "_archived_sprint3" not in meta:
            arch = {}
            for k in ("live_scores_compiled_sprint3", "pre_compile_baseline_sprint3",
                      "compile_artifact"):
                if k in meta:
                    arch[k] = meta[k]
            if arch:
                meta["_archived_sprint3"] = arch

        meta["avg_quality_score"] = new_avg
        meta["avg_quality_alltime"] = new_alltime
        meta["revision_rate"] = new_rev
        meta["total_executions"] = new_n
        meta["best_score"] = max(scores)
        meta["worst_score"] = min(scores)
        meta["tier"] = new_tier
        meta["reconciled_at"] = datetime.datetime.now(datetime.UTC).isoformat()

    # Recompute global avg from corrected per-skill avgs (real scored skills only).
    scored = [m["avg_quality_score"] for m in skills.values()
              if isinstance(m, dict) and m.get("avg_quality_score")]
    if scored:
        data["global_avg_quality"] = round(sum(scored) / len(scored), 1)

    print(f"{'SKILL':<28}{'old_avg':>9}{'new_avg':>9}{'old_n':>7}{'new_n':>7}")
    for name, oa, na, on, nn in sorted(changed, key=lambda x: x[0]):
        print(f"{name:<28}{str(oa):>9}{na:>9}{str(on):>7}{nn:>7}")
    print(f"\n{len(changed)} skills reconciled. "
          f"global_avg_quality -> {data.get('global_avg_quality')}")

    if apply:
        bak = PATH.with_suffix(
            f".yaml.bak-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(PATH, bak)
        PATH.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
                        encoding="utf-8")
        print(f"\nAPPLIED. Backup: {bak.name}")
    else:
        print("\nDRY-RUN (no writes). Re-run with --apply to commit.")


if __name__ == "__main__":
    main()
