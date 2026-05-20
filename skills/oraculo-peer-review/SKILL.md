---
name: oraculo-peer-review
description: Peer review — heuristics, rebuttals, area chair, OpenReview. Triggers em "peer review", "rebuttal", "OpenReview", "area chair", "AC", "meta-review".
license: MIT
parent_agent: oraculo-director
compliance: [research_integrity, audit_immutable]
---

# ORACULO-PEER-REVIEW

## Review categories (NeurIPS-style)
- **1: Strong reject** — fatally flawed
- **3: Reject** — significant issues
- **5: Borderline reject** — minor issues
- **6: Weak accept** — needs improvement
- **7: Accept** — good paper
- **9: Strong accept** — top 15% paper
- **Confidence 1-5** — reviewer expertise

## Quality criteria
- **Soundness:** methodology correct
- **Novelty:** new contribution
- **Significance:** advances field
- **Clarity:** well-written
- **Reproducibility:** code + data

## Reviewer biases (mitigate)
- **Confirmation bias** — favor familiar approaches
- **Halo effect** — famous authors/affiliations
- **Length bias** — confuse longer with better
- **Math heaviness** — confuse complex with rigorous
- **Sample bias** — only read top of pile
- **Reviewer fatigue** — late reviews suffer

## Rebuttal strategies
- **Address each concern** — point by point
- **Cite paper changes** — "in revision, we added..."
- **Acknowledge limitations** — show humility
- **Provide additional experiments** if possible
- **Don't argue subjectively** — facts > emotion
- **Respect reviewer** even if wrong

## Templates
1. Review template (per criterion)
2. Rebuttal template (point-by-point)
3. AC meta-review structure
4. Code review for ML papers
5. Conflict of interest declaration
6. Reviewer ethics guidelines

## Cross-references
- [[oraculo-paper-writing]] · [[oraculo-replication-studies]] · [[oraculo-conference-tracking]]
