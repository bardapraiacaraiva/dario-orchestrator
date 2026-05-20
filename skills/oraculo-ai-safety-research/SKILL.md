---
name: oraculo-ai-safety-research
description: AI safety methodologies — interpretability, mech interp, scalable oversight. Triggers em "AI safety", "interpretability", "mechanistic interpretability", "mech interp", "circuit analysis", "Anthropic interp", "responsible AI".
license: MIT
parent_agent: oraculo-director
compliance: [audit_immutable, ai_governance, responsible_disclosure]
---

# ORACULO-AI-SAFETY-RESEARCH

## Sub-fields
- **Mechanistic Interpretability:** understand neural circuits
- **Behavioral Interpretability:** input-output patterns
- **Scalable Oversight:** humans supervise superhuman AI
- **Robustness:** adversarial, distribution shift
- **Honesty:** model says what it believes
- **Corrigibility:** model accepts correction
- **Capability evaluations:** dangerous capabilities (METR, Apollo)
- **Power-seeking:** resource acquisition behaviors

## Mechanistic interpretability key concepts
- **Circuits:** specific computations within neural network
- **Features:** what concepts neurons encode (sparse autoencoders)
- **Polysemanticity:** neurons encoding multiple concepts
- **Superposition:** more features than neurons (compressed)
- **Activation patching:** intervention experiments
- **Attribution patching:** scalable activation patching
- **Logit lens:** track predictions through layers

## Stack
- **TransformerLens** — interp library
- **nnsight (NDIF)** — distributed interp
- **Anthropic interpretability** — leading research lab
- **Apollo Research** — model evals
- **METR (ARC Evals)** — frontier capability evals
- **Redwood Research** — safety research

## Key papers/projects 2024-2026
- "Mapping the Mind of a Large Language Model" (Anthropic 2024, paper estudou Claude 3 Sonnet — referência histórica)
- "Sleeper Agents" (Anthropic — deceptive AI)
- "Sparse Autoencoders" — feature discovery
- "Constitutional AI" — alignment without RLHF
- "Frontier Models" eval frameworks (METR)

## Templates
1. Interp experiment design
2. Circuit identification protocol
3. Sparse autoencoder training
4. Adversarial robustness test
5. Capability eval framework
6. Safety case template

## Cross-references
- [[oraculo-alignment-research]] · [[sphinx-ai-security]] · [[lex-ai-governance]] · [[nomos-eu-ai-act-pt]]
