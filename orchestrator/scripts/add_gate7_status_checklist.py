"""Add Gate 7 (Status Checklist per data point) to all 145 refactored SKILL.md.

Validated em FASE 1 (2026-05-23): adicionar checklist 🔵verified/🟡assumed/🟢projection
lifts Accuracy +4-5 pts → polish loop 88→93 e 81→92 consistently.

This script inserts a Gate 7 section between existing Gate 6 and the
Fully-worked A-tier example.

Run:
    python scripts/add_gate7_status_checklist.py            # full batch
    python scripts/add_gate7_status_checklist.py --dry-run  # show actions only
    python scripts/add_gate7_status_checklist.py --limit 5  # test on 5 first
"""

from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"
GATE7_MARKER = "Status checklist per data point"


GATE7_GENERATION_PROMPT = """Gera o Gate 7 (Status Checklist per data point) para o SKILL.md abaixo. Pattern validado em FASE 1 production (lifts Accuracy +4-5 pts, polish loop 88→93).

TEMPLATE OBRIGATÓRIO:

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmed from prior session/memory/cliente data
- 🟡 **assumed** — plausible but needs cliente confirm pre-delivery
- 🟢 **projection** — forecast by design (not verifiable)

Output checklist upfront mostra reader exactly o que é trust-as-is vs precisa verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready: [exemplo skill-specific: dados sem labels, reader assumes tudo verified]
✅ Delivery-ready: [exemplo skill-specific com 2-3 items labeled per status]

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (substituir assumptions com actuals)
- [ ] All citations added per 🔵 sources
- [ ] All 🟢 projections labeled as such ao cliente (clear expectations)

---

SKILL.md content (use para infer o domain + tailor examples):
{skill_md}

---

Gera APENAS o Gate 7 section (começa com "### 7." e termina com a ship checklist). NÃO incluas outros gates ou A-tier example. ❌/✅ examples MUST be domain-specific ao skill (não generic).

Target: 25-40 linhas markdown. PT-PT/BR misto OK."""


def has_existing_refactor(content: str) -> bool:
    """Skill has the original refactor (gates 1-6 + A-tier example)."""
    return "Delivery-ready self-check" in content


def has_gate7(content: str) -> bool:
    """Skill already has Gate 7 added."""
    return GATE7_MARKER in content


def find_insertion_point(content: str) -> tuple[int, str] | None:
    """Find where to insert Gate 7.

    Strategy: insert before "Fully-worked A-tier example" section if it exists,
    or before "Output anti-patterns" if not, or at end of self-check section.
    """
    # Priority 1: before A-tier example
    m = re.search(r"\n##+\s*Fully-worked A-tier", content)
    if m:
        return m.start(), "before A-tier example"
    # Priority 2: before Output anti-patterns
    m = re.search(r"\n##+\s*Output anti-patterns", content)
    if m:
        return m.start(), "before anti-patterns"
    # Priority 3: end of file
    return len(content.rstrip()), "end of file"


def generate_gate7(skill_md: str) -> str:
    from scripts.anthropic_spend_wrapper import TrackedAnthropic
    client = TrackedAnthropic(caller="scripts/add_gate7_status_checklist")
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": GATE7_GENERATION_PROMPT.format(skill_md=skill_md[:5000]),
        }],
    )
    return resp.content[0].text.strip()


def collect_targets() -> list[Path]:
    """All refactored skills that don't have Gate 7 yet."""
    targets = []
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        if not has_existing_refactor(content):
            continue  # not refactored yet
        if has_gate7(content):
            continue  # already has Gate 7
        targets.append(skill_md)
    return sorted(targets)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int, help="Cap skills to process")
    p.add_argument("--start", type=int, default=0)
    args = p.parse_args()

    targets = collect_targets()
    if args.start:
        targets = targets[args.start:]
    if args.limit:
        targets = targets[: args.limit]

    print(f"=== Add Gate 7 (Status Checklist) to {len(targets)} skills ===\n")

    if args.dry_run:
        for t in targets[:10]:
            print(f"  [dry-run] {t.parent.name}")
        if len(targets) > 10:
            print(f"  ... +{len(targets)-10} more")
        return

    start = time.time()
    success = 0
    failed = 0
    for i, skill_path in enumerate(targets, 1):
        name = skill_path.parent.name
        elapsed = time.time() - start
        if i > 1:
            avg = elapsed / (i - 1)
            eta = avg * (len(targets) - i + 1)
            print(f"[{i:3}/{len(targets)}] {name:35s} (avg {avg:.1f}s, ETA {eta/60:.1f}min)")
        else:
            print(f"[{i:3}/{len(targets)}] {name:35s}")

        try:
            content = skill_path.read_text(encoding="utf-8")
            gate7 = generate_gate7(content)
            ip, where = find_insertion_point(content)
            new_content = content[:ip] + "\n" + gate7 + "\n" + content[ip:]
            skill_path.write_text(new_content, encoding="utf-8")
            print(f"              ✓ inserted {len(gate7):,} chars ({where})")
            success += 1
        except Exception as e:
            print(f"              ✗ ERROR: {str(e)[:120]}")
            failed += 1

    print("\n=== Done ===")
    print(f"  Success: {success}")
    print(f"  Failed:  {failed}")
    print(f"  Time:    {(time.time()-start)/60:.1f} min")


if __name__ == "__main__":
    main()
