"""DSPy-based prompt optimization (Onda 4 #5).

Skills in DARIO are currently written-by-hand markdown prompts. DSPy lets
us treat the prompt as a compiled artefact of an optimisation run against
a metric — i.e., the prompt is learned from data instead of authored.

This package is the seed of that capability:

    optimization/signatures.py   — DSPy Signature classes per skill
    optimization/programs.py     — DSPy Modules that wrap Signatures
    optimization/optimize_skill.py — CLI to compile a skill via BootstrapFewShot
    optimization/evals.py        — Dataset loader for golden_eval data

Status: pilot for `dario-brand`. Other skills follow once the pilot proves ROI.
"""
