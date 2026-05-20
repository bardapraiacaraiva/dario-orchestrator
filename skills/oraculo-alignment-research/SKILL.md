---
name: oraculo-alignment-research
description: AI alignment — Constitutional AI, RLHF, debate, scalable oversight. Triggers em "AI alignment", "Constitutional AI", "RLHF", "DPO", "scalable oversight", "debate", "weak to strong generalization".
license: MIT
parent_agent: oraculo-director
compliance: [audit_immutable, ai_governance, responsible_disclosure]
---

# ORACULO-ALIGNMENT-RESEARCH

## Techniques
- **RLHF (Reinforcement Learning Human Feedback):** OpenAI ChatGPT method
- **DPO (Direct Preference Optimization):** simpler alternative
- **Constitutional AI (Anthropic):** self-critique with principles
- **RLAIF:** Reinforcement Learning AI Feedback
- **Process supervision:** reward chains of reasoning
- **Debate:** two AIs argue, human judges
- **Iterated Amplification:** human + AI assistance
- **Weak-to-Strong:** train strong model on weak supervision

## Open problems
- **Specification gaming:** AI finds loopholes
- **Goal misgeneralization:** training objective ≠ deployment
- **Sycophancy:** AI tells humans what they want
- **Deception:** AI hides capabilities
- **Mesa-optimization:** learned objectives vs base objective
- **Scalable oversight:** humans can't supervise superhuman AI

## Stack research
- **Anthropic Interpretability** — mech interp leader
- **OpenAI Superalignment** — disbanded 2024 but pubs continue
- **DeepMind Scalable Alignment**
- **Redwood Research** — focused on safety
- **MIRI** — agent foundations
- **ARC Evals (METR)** — evaluations

## Templates
1. RLHF pipeline (PPO + reward model)
2. Constitutional AI workflow
3. Red-teaming alignment evaluations
4. Specification gaming detection
5. Deception monitoring framework
6. Alignment research project structure

## Cross-references
- [[oraculo-ai-safety-research]] · [[oraculo-evaluation-frameworks]] · [[sphinx-ai-security]]
