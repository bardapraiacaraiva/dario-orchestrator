#!/usr/bin/env python3
"""
DARIO assemble_bundle — Meta-skill that produces coherent multi-skill deliverables.
====================================================================================

The Coherence dimension discovered in score_bundle.py testing showed that
ad-hoc concatenations of independently-generated outputs score 70-77 (not
delivery-ready). The fix is to generate the bundle DESIGNED as a unit:

  1. Take ONE client briefing
  2. Generate a SHARED VOICE SPEC first (carries through all components)
  3. Generate each component with explicit cross-references to siblings
  4. Add a ONE-PAGER INDEX at the top tying everything together
  5. Single output file delimited by component

Then auto-score with score_bundle.py to validate Coherence >= 18/20.

Usage:
    python assemble_bundle.py \
        --client "Atrium Premium RE" \
        --briefing "Boutique brokerage NYC+Lisboa+Porto..." \
        --components dario-brand,diva-moodboard,dario-content \
        --out ./atrium-rebrand-bundle.md

    python assemble_bundle.py \
        --client "Cuidai BR" \
        --briefing-file ./cuidai-context.md \
        --components dario-brand,dario-pipeline,dario-pitch \
        --out ./cuidai-bundle.md \
        --auto-score

Required env: ANTHROPIC_API_KEY

Cost: ~$0.10-0.15 per bundle (Sonnet 4.6 generation + Haiku judge).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from datetime import UTC, datetime
from pathlib import Path

ORCH = Path.home() / ".claude" / "orchestrator"
SKILLS = Path.home() / ".claude" / "skills"


VOICE_SPEC_PROMPT = """Estabelece o VOICE SPEC partilhado para o bundle multi-skill abaixo.

CLIENT: {client}
BRIEFING: {briefing}

O Voice Spec é o anchor que TODOS os {n_components} componentes vão herdar
(brand, content, pitch, design, etc.). Sem voice partilhada, os componentes
parecem 3 documentos separados — a métrica Coherence cai.

Produz o Voice Spec em formato estruturado:

1. **Brand archetype** (Jung/Pearson) + 2-sentence rationale ancorada no founder/target
2. **Tom de voz** (4 atributos concretos)
3. **Léxico CORE** (5-8 termos/expressões que SEMPRE usamos)
4. **Léxico FORBIDDEN** (5-8 termos/clichés que NUNCA usamos)
5. **Frase-bandeira** (1 frase que destila TUDO — vai aparecer literal em pelo menos 2 componentes)
6. **Cross-reference convention** (como cada componente refere os outros — ex: "ver Section 2 da brand strategy")

Output como markdown bem estruturado, ~400-600 palavras."""


COMPONENT_PROMPT = """Gera o componente <{skill}> do bundle multi-skill para {client}.

CLIENT: {client}
BRIEFING: {briefing}

VOICE SPEC PARTILHADO (todos os componentes do bundle herdam isto):
{voice_spec}

OUTROS COMPONENTES DO BUNDLE: {other_skills}

INSTRUÇÕES CRÍTICAS:
1. Aplica o Voice Spec — usa o léxico CORE, evita o FORBIDDEN, integra a frase-bandeira.
2. Cross-reference INLINE os outros componentes — DENTRO DO CORPO do output, NÃO só no final. Exemplo dentro de uma secção:
   "Esta hipótese de aquisição alinha com o archetype Caregiver definido em dario-brand (Section 2) e materializa-se na Slide 4 do dario-pitch."
3. Inclui pelo menos 3 cross-references inline (uma por skill irmã).
4. Usa client name em CADA secção/título.
5. Sem placeholder angle-brackets <>.
6. PROIBIDO truncar — termina cada secção. Se ficares perto do limite de tokens, corta o NÚMERO de bullet points por secção, NÃO mid-sentence.
7. Cada secção termina sempre com 1-2 frases concretas + número/data/cliente.

Produz o output COMPLETO do skill {skill} aplicado ao briefing. Formato markdown estruturado. Tamanho alvo: 800-1500 palavras COMPLETAS.

Estrutura obrigatória:

### COMPONENT: {skill}

#### Context anchored to {client}
[1 parágrafo amarrando este componente ao briefing do cliente]

[secções específicas do skill {skill} — incluir cross-references inline]

### Cross-references neste componente
- ↔ [skill irmã 1]: [frase concreta da ligação]
- ↔ [skill irmã 2]: [frase concreta da ligação]
- ↔ [skill irmã 3 se >=4 components]: [frase concreta]"""


INDEX_PROMPT = """Gera o ONE-PAGER INDEX do bundle multi-skill para {client}.

O Index é a primeira página que o cliente vê. Tem 3 jobs:
1. Tie together os {n_components} componentes numa narrativa única
2. Mostrar a "story" do deliverable (não a lista de docs)
3. Direcionar o cliente sobre como ler / usar o bundle

CLIENT: {client}
BRIEFING: {briefing}
VOICE SPEC (extrair o essencial): {voice_spec_summary}
COMPONENTES INCLUÍDOS: {skill_list}

Cabeça o output com:
### BUNDLE INDEX — {client}
### Generated: {date}

Estrutura:

# {client} — Strategy Bundle

## TL;DR (3-line story do bundle)
[3 frases que destilam o valor]

## What's Inside
| Component | Skill | Purpose |
|---|---|---|
[uma linha por componente]

## How to Read
[1 parágrafo guiding o cliente: onde começar, em que ordem, quando voltar]

## Voice Spec (1-sentence)
[a frase-bandeira do Voice Spec]

## Next Steps After Reading
[3 bullets concretos do que cliente faz a seguir]

Tamanho: 250-400 palavras max. Concise + actionable."""


def call_anthropic(prompt: str, model: str = "claude-sonnet-4-6",
                   max_tokens: int = 2500) -> str:
    try:
        from anthropic import Anthropic
    except ImportError:
        raise RuntimeError("pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    client = Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def read_briefing(args) -> str:
    if args.briefing_file:
        return Path(args.briefing_file).read_text(encoding="utf-8")
    if args.briefing:
        return args.briefing
    raise SystemExit("error: --briefing or --briefing-file required")


def assemble(client: str, briefing: str, components: list[str], out_path: Path,
             model: str = "claude-sonnet-4-6"):
    print(f"=== Assembling bundle for {client} ===")
    print(f"  Components ({len(components)}): {', '.join(components)}")

    # Step 1: Generate shared voice spec
    print("\n[1/3] Generating shared Voice Spec...")
    voice_spec = call_anthropic(
        VOICE_SPEC_PROMPT.format(
            client=client, briefing=briefing[:2000],
            n_components=len(components),
        ),
        model=model, max_tokens=1500,
    )
    print(f"      Voice Spec generated ({len(voice_spec)} chars)")

    # Step 2: Generate each component with voice spec embedded
    print(f"\n[2/3] Generating {len(components)} components with cross-references...")
    component_outputs = {}
    for i, skill in enumerate(components, 1):
        other_skills = [s for s in components if s != skill]
        print(f"      ({i}/{len(components)}) {skill}")
        out = call_anthropic(
            COMPONENT_PROMPT.format(
                skill=skill, client=client, briefing=briefing[:2000],
                voice_spec=voice_spec[:3000],
                other_skills=", ".join(other_skills),
            ),
            model=model, max_tokens=4500,
        )
        component_outputs[skill] = out
        print(f"         {len(out)} chars")

    # Step 3: Generate one-pager INDEX
    print(f"\n[3/3] Generating Bundle Index (one-pager)...")
    voice_summary = "\n".join(
        line for line in voice_spec.split("\n")
        if "frase-bandeira" in line.lower() or "Frase" in line
    )[:500] or voice_spec[:500]

    index = call_anthropic(
        INDEX_PROMPT.format(
            client=client, briefing=briefing[:2000],
            voice_spec_summary=voice_summary,
            skill_list=", ".join(components),
            n_components=len(components),
            date=datetime.now(UTC).isoformat()[:10],
        ),
        model=model, max_tokens=1200,
    )
    print(f"      Index generated ({len(index)} chars)")

    # Assemble final output
    print(f"\nAssembling final bundle file...")
    parts = [
        f"<!-- DARIO Bundle — assembled {datetime.now(UTC).isoformat()} -->",
        index,
        "",
        "---",
        "",
        "## SHARED VOICE SPEC",
        "",
        voice_spec,
        "",
        "---",
        "",
    ]
    for skill in components:
        parts.append(component_outputs[skill])
        parts.append("")
        parts.append("---")
        parts.append("")

    bundle_text = "\n".join(parts)
    out_path.write_text(bundle_text, encoding="utf-8")

    print(f"\n✓ Bundle assembled: {out_path}")
    print(f"  Total size: {len(bundle_text)} chars ({len(bundle_text)//4} ~tokens)")
    print(f"  Components: {len(components)} + index + voice spec")

    return bundle_text


def main() -> int:
    p = argparse.ArgumentParser(description="Assemble a coherent multi-skill bundle.")
    p.add_argument("--client", required=True, help="Client name")
    p.add_argument("--briefing", help="Inline briefing text")
    p.add_argument("--briefing-file", help="Path to briefing file (.md)")
    p.add_argument("--components", required=True,
                   help="Comma-separated skill names (e.g. dario-brand,dario-content,dario-pitch)")
    p.add_argument("--out", required=True, help="Output file path (.md)")
    p.add_argument("--model", default="claude-sonnet-4-6", help="Generation model")
    p.add_argument("--auto-score", action="store_true",
                   help="Run score_bundle.py on the result automatically")
    args = p.parse_args()

    briefing = read_briefing(args)
    components = [s.strip() for s in args.components.split(",") if s.strip()]
    if len(components) < 2:
        print("error: need at least 2 components for a bundle", file=sys.stderr)
        return 1

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        assemble(args.client, briefing, components, out_path, args.model)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.auto_score:
        print("\n=== Auto-scoring assembled bundle ===")
        import re as re_mod
        import subprocess
        import tempfile

        # The assembled bundle is ONE file containing N components. score_bundle.py
        # expects one file per component. Split the file by component delimiters
        # into N temp files, then pass them to score_bundle.py.
        bundle_text = out_path.read_text(encoding="utf-8")
        bundle_name = f"{args.client.lower().replace(' ', '-')}-assembled"

        # Split on '### COMPONENT: <skill>' markers
        split_temp_dir = Path(tempfile.mkdtemp(prefix="dario-bundle-"))
        component_files = []
        for skill in components:
            # Find this component's section
            marker = f"### COMPONENT: {skill}"
            start = bundle_text.find(marker)
            if start == -1:
                print(f"  warn: no '{marker}' marker — using whole bundle for {skill}")
                continue
            # Find next component marker (or end of file)
            next_marker = re_mod.search(r"### COMPONENT: ", bundle_text[start + len(marker):])
            end = (start + len(marker) + next_marker.start()) if next_marker else len(bundle_text)
            section = bundle_text[start:end]
            tmp = split_temp_dir / f"{skill}.md"
            tmp.write_text(section, encoding="utf-8")
            component_files.append((skill, str(tmp)))

        if not component_files:
            print("  error: no components extracted from bundle file", file=sys.stderr)
            return 1

        print(f"  Split bundle into {len(component_files)} temp component files")
        score_cmd = [
            sys.executable, str(ORCH / "score_bundle.py"),
            "--bundle-name", bundle_name,
            "--context", briefing[:800],
        ]
        for skill, path in component_files:
            score_cmd.extend(["--skill", skill, "--output", path])
        score_cmd.append("--json")
        result = subprocess.run(score_cmd, capture_output=True, text=True, cwd=str(ORCH))
        print(result.stdout)
        if result.returncode != 0 and result.returncode != 2:  # 2 = needs-review (ok)
            print(f"score stderr: {result.stderr[:400]}", file=sys.stderr)

        # Cleanup temp files
        import shutil
        try:
            shutil.rmtree(split_temp_dir)
        except Exception:
            pass

        return result.returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
