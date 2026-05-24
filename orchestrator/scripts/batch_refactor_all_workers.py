"""Batch-refactor ALL unrefactored worker skills (dario-*, diva-*, seo-*, builder-*, lucas-*, a360-*).

Estimate: 129 skills × ~$0.05 each = ~$6.50 total cost. ~15-20 min wall time.

Run:
    python scripts/batch_refactor_all_workers.py            # full batch
    python scripts/batch_refactor_all_workers.py --dry-run  # list only
    python scripts/batch_refactor_all_workers.py --prefix dario  # filter
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"
PRODUCTION_PREFIXES = ["dario-", "diva-", "seo-", "builder-", "lucas-", "a360-"]


REFACTOR_PROMPT = """Tu és um especialista em quality refinement de DARIO skills. Vou-te dar um SKILL.md. Gera um REFACTOR FOOTER seguindo este template (proven across 16 skills, ceiling 88-93 single-skill outputs).

TEMPLATE OBRIGATÓRIO (5 components, ordem fixa):

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1-6. [SEIS GATES — específicos do skill domain]
Cada gate:
- [ ] 3-5 checkpoints concretos com criteria
- ❌ NOT delivery-ready: [exemplo genérico ruim]
- ✅ Delivery-ready: [exemplo COM DADOS CONCRETOS números/datas/nomes]

Gate FINAL (sempre): "Output uses CLIENT NAME + REAL data, no placeholder angle-brackets"

## Fully-worked A-tier example (delivery-ready reference)

```markdown
[exemplo 60-100 linhas, client real conhecido (Cuidai/Atrium/LUSOconta/SAQUEI/Lisbon Dog Care/Tributario.AI/Atelier AI/Vivenda/Pupli/ARRECADA.GOV), template populated com dados verificáveis]
```

## Output anti-patterns

- 6-10 items list

---

SKILL.md content:
{skill_md}

---

Gera APENAS o refactor footer (começa com "## Delivery-ready self-check", termina com lista de anti-patterns). NÃO incluas o SKILL.md original. Específico ao domínio detectado do skill.

PT-PT/BR misto OK. Target 80-150 linhas markdown."""


def generate_refactor(skill_name: str, skill_md: str) -> str:
    from scripts.anthropic_spend_wrapper import TrackedAnthropic
    client = TrackedAnthropic(caller="scripts/batch_refactor_all_workers")
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=5500,
        messages=[{
            "role": "user",
            "content": REFACTOR_PROMPT.format(skill_md=skill_md[:6000]),
        }],
    )
    return resp.content[0].text.strip()


def collect_targets(prefix_filter: str | None = None) -> list[tuple[str, Path]]:
    targets = []
    for prefix in PRODUCTION_PREFIXES:
        if prefix_filter and prefix.rstrip("-") != prefix_filter:
            continue
        for skill_dir in SKILLS_DIR.glob(f"{prefix}*"):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            existing = skill_md.read_text(encoding="utf-8")
            if "Delivery-ready self-check" in existing:
                continue  # already refactored
            targets.append((skill_dir.name, skill_md))
    return sorted(targets)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--prefix", help="Filter to one prefix (e.g. dario, diva, seo)")
    p.add_argument("--limit", type=int, help="Cap on number of skills")
    p.add_argument("--start", type=int, default=0, help="Start from index N")
    args = p.parse_args()

    targets = collect_targets(args.prefix)
    if args.start:
        targets = targets[args.start:]
    if args.limit:
        targets = targets[: args.limit]

    print(f"=== Batch refactor {len(targets)} skills ===")
    if args.dry_run:
        for name, _ in targets:
            print(f"  [dry-run] {name}")
        return

    start_time = time.time()
    refactored = 0
    failed = 0
    for i, (name, path) in enumerate(targets, 1):
        elapsed = time.time() - start_time
        if i > 1:
            avg = elapsed / (i - 1)
            eta = avg * (len(targets) - i + 1)
            print(f"[{i:3}/{len(targets)}] {name:35s} (avg {avg:.1f}s/skill, ETA {eta/60:.1f}min)")
        else:
            print(f"[{i:3}/{len(targets)}] {name:35s}")

        try:
            existing = path.read_text(encoding="utf-8")
            refactor = generate_refactor(name, existing)
            new_content = existing.rstrip() + "\n\n" + refactor + "\n"
            path.write_text(new_content, encoding="utf-8")
            print(f"              ✓ +{len(refactor):,} chars")
            refactored += 1
        except Exception as e:
            print(f"              ✗ ERROR: {str(e)[:120]}")
            failed += 1

    print(f"\n=== Done ===")
    print(f"  Refactored: {refactored}")
    print(f"  Failed: {failed}")
    print(f"  Time: {(time.time()-start_time)/60:.1f} min")


if __name__ == "__main__":
    main()
