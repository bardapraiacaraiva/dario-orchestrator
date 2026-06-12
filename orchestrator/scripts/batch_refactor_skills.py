"""Batch-refactor remaining skills with AI-generated domain-specific blocks.

For each skill SKILL.md, generates a tailored refactor footer (6-gate
self-check + A-tier example + anti-patterns) using Sonnet 4.6 based on
the existing SKILL.md content, then appends it.

Run:
    python scripts/batch_refactor_skills.py            # full batch
    python scripts/batch_refactor_skills.py --dry-run  # show without writing
"""

from __future__ import annotations

import argparse
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"

# 9 remaining production-validated skills with their domain hints
TARGETS = [
    ("seo-audit", "SEO technical audit", "audit findings concretos com source data + impact estimates + priorização + roadmap"),
    ("dario-produto", "Product roadmap + RICE prioritization", "features priorizadas RICE com effort + impact + dependencies + acceptance criteria"),
    ("dario-wp-audit", "WordPress technical audit", "plugins audit + theme review + security + performance + WooCommerce specific findings com effort/impact"),
    ("seo-sitemap", "Sitemap.xml audit + generation", "URLs map completo + priorities + changefreq + hreflang + canonicals + missing pages identification"),
    ("a360-validacao", "Lean validation framework", "Mom Test scripts + 15 maes/clientes recruitment + decision matrix go/no-go thresholds quantitative"),
    ("dario-client-onboard", "Client onboarding kit", "kickoff checklist + week-1 deliverables + communication plan + tools setup + handoff documents"),
    ("dario-offer", "Grand Slam Offer Hormozi", "value equation completa + risk reversal + bonus stack com anchor values + urgency genuino"),
    ("dario-pitch", "Pitch deck investor", "12 slides com narrative arc + TAM/SAM/SOM concretos + financial ask + use of funds milestones"),
    ("diva-materials", "Interior design materials specs", "paleta cores hex + texturas + tipografias + finishes com cost estimates + suppliers PT"),
]

REFACTOR_GENERATION_PROMPT = """Tu és um especialista em quality refinement de DARIO skills. Vou-te dar um SKILL.md e um domain hint. Gera um REFACTOR FOOTER que segue exatamente este template (proven across 8 skills, ceiling 88-89 cleanly).

TEMPLATE OBRIGATÓRIO (5 components, ordem fixa):

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### 1. [PRIMEIRO GATE — específico do skill]
- [ ] checkpoints concretos (3-5 items)

❌ NOT delivery-ready: [exemplo genérico ruim]
✅ Delivery-ready: [exemplo com dados concretos numericamente]

### 2-6. [OUTROS 5 GATES — todos específicos do skill]
- [ ] checkpoints (3-5 items each)

(gate final SEMPRE: "Output uses CLIENT NAME + REAL data throughout — no placeholder angle-brackets")

## Fully-worked A-tier example (delivery-ready reference)

```markdown
[exemplo COMPLETO, ~80-120 linhas, com client real conhecido (Cuidai/Atrium/LUSOconta/SAQUEI/Lisbon Dog Care/Tributario.AI/Atelier AI), todos os campos do template populated com dados verificáveis, exemplo de ENTREGA cliente-ready]
```

## Output anti-patterns

- 8-10 items list de specific mistakes a evitar

---

SKILL: {skill}
DOMAIN: {domain_short}
TASK FOCUS: {domain_hint}

SKILL.md actual content:
{skill_md}

---

Gera APENAS o refactor footer (começa com "## Delivery-ready self-check", termina com a lista de anti-patterns). NÃO incluas o SKILL.md original. Cira específico ao domínio.

Linguagem: PT-PT/BR misto OK (como os skills existentes).
Tamanho target: 80-150 linhas de markdown."""


def generate_refactor(skill: str, domain: str, hint: str, skill_md: str) -> str:
    from scripts.anthropic_spend_wrapper import TrackedAnthropic
    client = TrackedAnthropic(caller="scripts/batch_refactor_skills")
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=5500,
        messages=[{
            "role": "user",
            "content": REFACTOR_GENERATION_PROMPT.format(
                skill=skill,
                domain_short=domain,
                domain_hint=hint,
                skill_md=skill_md[:6000],
            ),
        }],
    )
    return resp.content[0].text.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    print(f"=== Batch refactor {len(TARGETS)} skills ===\n")

    results = []
    for i, (skill, domain, hint) in enumerate(TARGETS, 1):
        skill_path = SKILLS_DIR / skill / "SKILL.md"
        if not skill_path.exists():
            print(f"[{i}/{len(TARGETS)}] {skill:25s} SKIPPED (no SKILL.md found)")
            continue

        existing = skill_path.read_text(encoding="utf-8")
        if "Delivery-ready self-check" in existing:
            print(f"[{i}/{len(TARGETS)}] {skill:25s} ALREADY REFACTORED — skipping")
            continue

        print(f"[{i}/{len(TARGETS)}] {skill:25s} domain={domain}")
        print(f"               Generating refactor block ({len(existing)} chars existing)...")

        try:
            refactor = generate_refactor(skill, domain, hint, existing)
        except Exception as e:
            print(f"               ERROR: {e}")
            continue

        if args.dry_run:
            print(f"               [dry-run] would append {len(refactor)} chars")
            print(f"               Preview: {refactor[:120]}...")
            continue

        # Append to SKILL.md
        new_content = existing.rstrip() + "\n\n" + refactor + "\n"
        skill_path.write_text(new_content, encoding="utf-8")
        print(f"               ✓ Appended {len(refactor)} chars")
        results.append((skill, len(refactor)))

    if not args.dry_run:
        print("\n=== Done ===")
        print(f"  Refactored: {len(results)}/{len(TARGETS)}")
        total_chars = sum(r[1] for r in results)
        print(f"  Total chars added: {total_chars:,}")


if __name__ == "__main__":
    main()
