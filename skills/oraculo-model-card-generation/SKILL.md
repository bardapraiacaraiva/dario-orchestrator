---
name: oraculo-model-card-generation
description: Model cards (Mitchell et al.), datasheets for datasets. Triggers em "model card", "datasheet for datasets", "model documentation", "responsible AI documentation", "AI Act conformity".
license: MIT
parent_agent: oraculo-director
compliance: [audit_immutable, ai_governance]
---

# ORACULO-MODEL-CARD-GENERATION

## Marco
- **Model Cards (Mitchell et al., 2019)** — Google standard
- **Datasheets for Datasets (Gebru et al., 2018)** — dataset documentation
- **EU AI Act Annex IV** — high-risk model technical documentation
- **NIST AI RMF** — model risk management
- **Hugging Face model card spec** — implementation

## Model card sections
1. **Model details:** developer, date, type, license
2. **Intended use:** primary + downstream + out-of-scope
3. **Factors:** subgroups, environments
4. **Metrics:** performance + caveats
5. **Evaluation data:** datasets used
6. **Training data:** datasets + biases
7. **Quantitative analyses:** results per subgroup
8. **Ethical considerations:** risks, mitigations
9. **Caveats:** known limitations
10. **References + contact**

## Datasheets for Datasets sections
- Motivation (why created)
- Composition (what's in it)
- Collection process
- Preprocessing
- Uses (intended + unintended)
- Distribution (license, IP)
- Maintenance

## Stack
- **Hugging Face Model Cards** — standard implementation
- **Google Model Card Toolkit** — automated generation
- **Card creation forms** — guided wizards
- **DAGsHub model registry** — versioned cards

## Templates
1. Model card template (Mitchell format)
2. Datasheet template (Gebru format)
3. EU AI Act Annex IV doc
4. Model card automation (CI)
5. Bias evaluation section
6. Carbon footprint disclosure

## Cross-references
- [[oraculo-ai-safety-research]] · [[nomos-eu-ai-act-pt]] · [[lex-ai-governance]]
