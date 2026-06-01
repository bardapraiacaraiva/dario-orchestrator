# DARIO Memory + Dream Subsystem

Inspired by Anthropic's *"Memory and Dreaming for Self-Learning Agents"* (Mahesh Murag, Code w/ Claude 2026).

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          MEMORY LAYERS                                │
├──────────────────────────────────────────────────────────────────────┤
│  EPISODIC   memory/episodes/YYYY-MM-DD/EP-*.yaml                     │
│             One record per task execution: outcome, corrections,     │
│             retrieved memories, failed tool calls, duration, score.  │
│                                                                       │
│  SEMANTIC   memory/semantic/SEM-*.yaml                                │
│             Consolidated facts, patterns, observations.              │
│             Promoted from episodes by the Dream engine.              │
│             Mirror of user MEMORY.md is also indexed.                │
│                                                                       │
│  PROCEDURAL memory/procedural/PROC-*.yaml                             │
│             Learned skill sequences (workflows).                     │
│             Two sources: legacy skill_chains.yaml import, and        │
│             auto-promoted via convergence detection.                 │
│                                                                       │
│  CACHE      memory/cache/CACHE-*.yaml                                 │
│             Deterministic skill output cache (TTL=7d default).       │
│             Keyed by SHA256(skill + input).                          │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                          DREAM ENGINE                                 │
├──────────────────────────────────────────────────────────────────────┤
│  Phase 1  ORIENT      Load episodes + memories + retrieval stats     │
│  Phase 2  PRUNE       Archive stale + never-retrieved memories       │
│  Phase 3  MERGE       Consolidate duplicates (Jaccard >0.55)         │
│  Phase 4  REORGANIZE  Detect patterns + promote convergent workflows │
└──────────────────────────────────────────────────────────────────────┘
```

## Integration

Existing modules call thin facade `memory/hooks.py`:

```python
from memory import hooks

# After each task:
hooks.on_task_complete(
    task_id="CUI-008", skill="dario-product", outcome="success",
    score=87, project="cuidai", duration_seconds=245,
    tokens_used=12450, model="opus",
    retrieved_memories=[
        {"memory_id": "SEM-cuidai_strategy", "layer": "semantic", "relevance": "high"},
    ],
)

# Before context assembly:
pack = hooks.assemble_context_pack(project="cuidai")
# pack["procedural_hints"] → list of relevant learned workflows

# Optional cache:
cached = hooks.try_cache("dario-brand", input_text)
```

## CLI

```bash
python ~/.claude/orchestrator/dream_cli.py              # full dream cycle
python ~/.claude/orchestrator/dream_cli.py --dry-run    # don't write
python ~/.claude/orchestrator/dream_cli.py --window 14
python ~/.claude/orchestrator/dream_cli.py health
python ~/.claude/orchestrator/dream_cli.py episodes
python ~/.claude/orchestrator/dream_cli.py workflows
```

Slash command: `/dream` (see `~/.claude/commands/dream.md`).

## Cron

Daily 03:00 consolidation:
```powershell
powershell -File ~/.claude/orchestrator/scripts/dream_install_cron.ps1
```

Logs: `~/.claude/orchestrator/dream/cron.log`.

## Schemas

All Pydantic models in `memory/schemas.py`:
- `Episode` — task execution record
- `SemanticMemory` — consolidated fact / pattern / observation
- `ProceduralWorkflow` — learned skill sequence
- `CacheEntry` — TTL-bound skill output cache
- `DreamReport` — full report from one Dream cycle
- `PhaseReport` — per-phase summary inside a DreamReport

## Pattern Detection

`dream/pattern_detector.py` surfaces:
- Quality regression / improvement per skill (≥10pt delta across ≥4 runs)
- Skills failing ≥3 times in window
- Tool calls failing ≥3 times
- Skills accumulating ≥2 user corrections
- Convergent skill n-grams (≥3 sessions, ≥2 skills, no repeats)

## Promotion Thresholds

- **Procedural promotion** (convergent → workflow): ≥3 sessions, avg_score≥70
- **Semantic promotion** (episode insight → memory): score≥90 (existing `quality_scorer.py`)
- **Pruning**: never retrieved + ≥14d old + confidence<0.85 + no links
- **Stale pruning**: ≥90d without update + 0 retrievals + no links
- **Merge threshold**: Jaccard similarity ≥0.55 on normalized tokens
