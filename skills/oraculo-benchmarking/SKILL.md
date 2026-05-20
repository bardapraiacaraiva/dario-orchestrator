---
name: oraculo-benchmarking
description: Benchmark design — dataset curation, leaderboard creation, anti-contamination. Triggers em "benchmark design", "leaderboard", "dataset curation", "data contamination", "GLUE", "SuperGLUE", "BIG-Bench design".
license: MIT
parent_agent: oraculo-director
compliance: [research_integrity, audit_immutable]
---

# ORACULO-BENCHMARKING

## Quando usar
- New domain → no benchmark exists
- Existing benchmark saturated (>95% accuracy)
- Custom enterprise eval
- Specialty (BR PT legal, healthcare, etc.)
- Multimodal benchmark

## Anti-contamination
- **Test set leakage:** model trained on test data (common!)
- **Held-out validation:** never used during training
- **Time-based split:** train < cutoff date
- **Canary strings:** detect contamination
- **Private test sets:** API-only, no public release

## Datasets curation
- **Source diversity:** multiple sources
- **Annotator agreement:** inter-rater kappa ≥ 0.7
- **Difficulty distribution:** easy/medium/hard
- **Demographic balance:** avoid bias
- **License clarity:** CC, Apache, MIT
- **Versioning:** semver

## Leaderboard infrastructure
- **Hugging Face Open LLM Leaderboard**
- **PapersWithCode**
- **Chatbot Arena (LMSYS):** human preferences
- **HELM (Stanford)** — controlled
- **Custom:** Streamlit + Postgres

## Templates
1. Benchmark design document
2. Dataset card (Mitchell et al.)
3. Annotation guidelines
4. Leaderboard rules + submission process
5. Anti-contamination audit
6. Benchmark retirement criteria (saturation)

## Cross-references
- [[oraculo-model-evaluation]] · [[oraculo-evaluation-frameworks]] · [[oraculo-replication-studies]]
