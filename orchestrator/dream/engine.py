"""Dream Engine — orchestrates the 4 consolidation phases.

Usage:
    python -m dream.engine                  # full cycle, 7-day window
    python -m dream.engine --window 14      # 14-day window
    python -m dream.engine --dry-run        # don't write changes
    python -m dream.engine --agent dario    # scope to agent
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import yaml

from dream.merge import merge
from dream.orient import orient
from dream.prune import prune
from dream.reorganize import reorganize
from memory import cache, retrieval, semantic
from memory.config import get as _cfg
from memory.schemas import DreamReport, utcnow

# Default episode window — configurable (DD finding A13, 2026-06-12)
DEFAULT_WINDOW_DAYS = int(_cfg("dream_window_days"))

REPORTS_DIR = ORCH_DIR / "dream" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# v12.1 — canonical markdown dreams path
DREAMS_DIR = ORCH_DIR / "memory" / "dreams"
DREAMS_DIR.mkdir(parents=True, exist_ok=True)

# Legacy path — kept as mirror during 30-day grace period (drop after 2026-06-22)
LEGACY_DREAMS_DIR = Path.home() / ".claude" / "agent-memory" / "dario-v2-digital-ceo" / "dreams"
LEGACY_MIRROR_UNTIL = "2026-06-22"  # 30d grace period from v12.1 migration


class DreamEngine:
    def __init__(self, window_days: int = DEFAULT_WINDOW_DAYS, agent: str = "dario-ceo", dry_run: bool = False):
        self.window_days = window_days
        self.agent = agent
        self.dry_run = dry_run

    def run(self) -> DreamReport:
        t0 = time.monotonic()
        dream_id = f"DREAM-{datetime.now(UTC).strftime('%Y-%m-%d-%H%M%S')}"
        report = DreamReport(
            dream_id=dream_id,
            agent=self.agent,
            window_days=self.window_days,
        )

        report.memories_before = len(semantic.list_semantic())

        phase1, state = orient(window_days=self.window_days)
        report.phase_1_orient = phase1
        report.episodes_processed = phase1.counts.get("episodes", 0)

        phase2, state = prune(state, dry_run=self.dry_run)
        report.phase_2_prune = phase2

        phase3, state = merge(state, dry_run=self.dry_run)
        report.phase_3_merge = phase3

        phase4, state = reorganize(state, dry_run=self.dry_run)
        report.phase_4_reorganize = phase4

        report.memories_after = len(semantic.list_semantic())
        report.patterns_detected = state.get("patterns_detected", [])
        report.convergent_workflows = state.get("promoted_workflows", [])
        report.promotions = {
            "semantic": phase4.counts.get("promoted_semantic", 0),
            "procedural": phase4.counts.get("promoted_workflows", 0),
        }

        evicted = cache.evict_expired()
        if evicted:
            report.notes.append(f"Evicted {evicted} expired cache entries")

        dropped = retrieval.compact_log(keep_days=90)
        if dropped:
            report.notes.append(f"Compacted retrieval log: dropped {dropped} entries >90d")

        # Legacy workflow cleanup — self-gated by 30d grace period
        try:
            from memory.cleanup_legacy import cleanup as _cleanup_legacy
            cleanup_result = _cleanup_legacy(grace_days=30, dry_run=self.dry_run)
            if cleanup_result["archived"] > 0:
                report.notes.append(
                    f"Archived {cleanup_result['archived']} unused legacy workflow(s): "
                    f"{', '.join(cleanup_result['archived_ids'])}"
                )
        except Exception as e:
            report.warnings.append(f"legacy_cleanup_failed: {type(e).__name__}")

        # P1 (audit 2026-06-01) — close two feedback loops at the daily cycle:
        #  (a) refresh semantic-memory embeddings so newly consolidated/merged
        #      memories become retrievable in task context (memory/semantic_search);
        #  (b) run the golden regression check to surface quality drift.
        # Both guarded + skipped in dry-run; never abort the dream.
        if not self.dry_run:
            try:
                from memory.semantic_search import bootstrap_memory_embeddings
                emb = bootstrap_memory_embeddings()
                if emb.get("ok"):
                    report.notes.append(
                        f"Refreshed memory embeddings: {emb['embedded']} new, "
                        f"{emb['skipped']} unchanged (of {emb['total_memories']})"
                    )
                else:
                    report.warnings.append(f"memory_embeddings_skipped: {emb.get('reason', '?')}")
            except Exception as e:
                report.warnings.append(f"memory_embeddings_failed: {type(e).__name__}")

            try:
                from quality.golden_eval import regression_check
                rc = regression_check()
                report.notes.append(
                    f"Golden regression check: {len(rc.get('alerts', []))} alert(s), "
                    f"{len(rc.get('drifting', []))} drifting of {rc.get('with_golden', 0)} goldens"
                )
                if rc.get("alerts"):
                    report.warnings.append(f"golden_regression_alerts: {rc['alerts']}")
            except Exception as e:
                report.warnings.append(f"golden_regression_failed: {type(e).__name__}")

        report.duration_seconds = round(time.monotonic() - t0, 3)
        report.finished_at = utcnow()

        if not self.dry_run:
            self._save_report(report)
            self._write_dream_markdown(report)

        return report

    def _save_report(self, report: DreamReport) -> None:
        path = REPORTS_DIR / f"{report.dream_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(report.model_dump(mode="json", exclude_none=True), f, sort_keys=False, allow_unicode=True)

    def _build_markdown(self, report: DreamReport) -> tuple[str, str]:
        """Build markdown content for a dream report. Returns (filename, content)."""
        today = report.finished_at[:10] if report.finished_at else datetime.now(UTC).strftime("%Y-%m-%d")
        lines = [
            "---",
            f"name: Dream {today}",
            "description: Real 4-phase consolidation (dream engine v2)",
            "type: dream",
            f"dream_id: {report.dream_id}",
            "---",
            "",
            f"# Dream — {today}",
            "",
            f"**Window:** {report.window_days} days  |  **Episodes processed:** {report.episodes_processed}  |  **Duration:** {report.duration_seconds}s",
            f"**Memories:** {report.memories_before} → {report.memories_after}",
            "",
            "## Phase 1 — Orient",
        ]
        if report.phase_1_orient:
            for a in report.phase_1_orient.actions:
                lines.append(f"- {a}")
        lines.append("")
        lines.append("## Phase 2 — Prune")
        if report.phase_2_prune:
            for a in report.phase_2_prune.actions:
                lines.append(f"- {a}")
        lines.append("")
        lines.append("## Phase 3 — Merge")
        if report.phase_3_merge:
            for a in report.phase_3_merge.actions:
                lines.append(f"- {a}")
        lines.append("")
        lines.append("## Phase 4 — Reorganize")
        if report.phase_4_reorganize:
            for a in report.phase_4_reorganize.actions:
                lines.append(f"- {a}")
        lines.append("")
        if report.patterns_detected:
            lines.append("## Patterns Detected")
            for p in report.patterns_detected:
                lines.append(f"- {p}")
            lines.append("")
        if report.convergent_workflows:
            lines.append("## Convergent Workflows Promoted")
            for wf in report.convergent_workflows:
                lines.append(f"- `{wf}`")
            lines.append("")
        if report.notes:
            lines.append("## Notes")
            for n in report.notes:
                lines.append(f"- {n}")
        return f"dream_{today}.md", "\n".join(lines)

    def _write_dream_markdown(self, report: DreamReport) -> None:
        """Write markdown to canonical v12.1 path + mirror legacy during grace period."""
        filename, content = self._build_markdown(report)

        # v12.1 canonical path
        DREAMS_DIR.mkdir(parents=True, exist_ok=True)
        (DREAMS_DIR / filename).write_text(content, encoding="utf-8")

        # Legacy mirror (drop after 2026-06-22 grace period)
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        if today < LEGACY_MIRROR_UNTIL:
            LEGACY_DREAMS_DIR.mkdir(parents=True, exist_ok=True)
            (LEGACY_DREAMS_DIR / filename).write_text(content, encoding="utf-8")


def run_dream(window_days: int = DEFAULT_WINDOW_DAYS, agent: str = "dario-ceo", dry_run: bool = False) -> DreamReport:
    return DreamEngine(window_days=window_days, agent=agent, dry_run=dry_run).run()


def main():
    parser = argparse.ArgumentParser(description="DARIO Dream Engine — 4-phase memory consolidation")
    parser.add_argument("--window", type=int, default=DEFAULT_WINDOW_DAYS, help="Days of episode history to process")
    parser.add_argument("--agent", default="dario-ceo")
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes, just report")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    report = run_dream(window_days=args.window, agent=args.agent, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(report.model_dump(mode="json", exclude_none=True), indent=2))
        return 0

    print(f"\n[DREAM] {report.dream_id}")
    print(f"  Window: {report.window_days}d  |  Episodes: {report.episodes_processed}  |  Duration: {report.duration_seconds}s")
    print(f"  Memories: {report.memories_before} → {report.memories_after}")
    if report.patterns_detected:
        print(f"\n  Patterns detected ({len(report.patterns_detected)}):")
        for p in report.patterns_detected:
            print(f"    - {p}")
    if report.convergent_workflows:
        print(f"\n  Convergent workflows promoted ({len(report.convergent_workflows)}):")
        for wf in report.convergent_workflows:
            print(f"    - {wf}")
    if report.notes:
        print("\n  Notes:")
        for n in report.notes:
            print(f"    - {n}")
    for phase in [report.phase_1_orient, report.phase_2_prune, report.phase_3_merge, report.phase_4_reorganize]:
        if phase:
            print(f"\n  [{phase.name}] {phase.duration_seconds}s — {phase.counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
