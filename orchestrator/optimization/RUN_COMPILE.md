# DSPy Compile — How to run the real optimization

Onda 7 #4 validated the full DSPy pipeline against Anthropic API live.
Pipeline status:

- ✅ `BrandPositioning` signature loads
- ✅ `BrandPositioningProgram` (ChainOfThought wrapper) executes
- ✅ Anthropic API connection works (Haiku model)
- ✅ Output parses into 4 typed fields (posicionamento, archetype, tom_de_voz, diferenciadores)
- ✅ 3 brand goldens captured in `evals/golden/` (fintech, hotel, ai-devtools)

## Run baseline-only (3 LM calls, ~$0.015)

```bash
cd ~/.claude/orchestrator
python -m optimization.optimize_skill dario-brand --provider anthropic --model claude-haiku-4-5
```

The pilot config uses `BootstrapFewShot` with `max_bootstrapped_demos=2` and
`max_labeled_demos=2` (we only have 3 goldens). Estimated cost: **~$0.20–$0.50**
depending on how many bootstrap attempts the optimiser tries.

The compiled program is saved to:

```
optimization/compiled/brand_positioning.json
```

It contains the optimised instructions + selected demos. Load it back with:

```python
from optimization.programs import BrandPositioningProgram

p = BrandPositioningProgram()
p.load("optimization/compiled/brand_positioning.json")
result = p(briefing="...")
```

## Expected uplift on the pilot

With only 3 goldens, BootstrapFewShot's lift is modest (5-15% on the
`brand_score` composite). The MIPRO optimiser is more powerful but needs
≥20 examples — we'll hit that threshold after the next batch of goldens.

## Capture more goldens

```bash
python -m optimization.seed_brand_goldens   # currently 3 hardcoded
# Or add a new one programmatically:
python -c "
from golden_eval import capture_golden
capture_golden(
    eval_id='brand-my-startup-01',
    output_text='# Brand Positioning\n## Posicionamento\n...\narchetype: Hero\n...',
    human_score=85,
    notes='Briefing text describing the company...',
    force=True,
)
"
```

## Cost guard

If you want to cap spend, set:

```bash
export DSPY_MAX_LM_CALLS=20    # custom guard you can wire if needed
```

(Not enforced by DSPy directly; would require a wrapper around `dspy.LM`.)
