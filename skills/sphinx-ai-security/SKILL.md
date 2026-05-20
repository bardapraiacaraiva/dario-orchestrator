---
name: sphinx-ai-security
description: AI/ML security — prompt injection, model theft, data poisoning, adversarial ML, jailbreak defense. Triggers em "AI security", "ML security", "prompt injection", "jailbreak LLM", "model theft", "data poisoning", "adversarial ML", "MITRE ATLAS".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, ai_governance]
---

# SPHINX-AI-SECURITY

## Threat taxonomy (MITRE ATLAS)
- **Reconnaissance:** model fingerprinting
- **Resource Development:** adversarial example crafting
- **Initial Access:** prompt injection, supply chain
- **Execution:** jailbreak, RCE via LLM
- **Persistence:** backdoor model
- **Defense Evasion:** evasion attacks
- **Discovery:** model extraction
- **Collection:** training data extraction
- **Impact:** denial of service, integrity

## Attack categories
- **Prompt injection:** direct + indirect (cross-document)
- **Jailbreak:** bypass guardrails (DAN, role-play)
- **Data poisoning:** training set tampering
- **Model theft:** API → recreate model
- **Adversarial examples:** perturbations → misclassify
- **Backdoor:** trigger-activated behavior
- **Membership inference:** is X in training set?
- **Training data extraction:** verbatim memorization

## Defensive frameworks
- **MITRE ATLAS:** Adversarial Threat Landscape AI Systems
- **OWASP Top 10 for LLMs**
- **NIST AI RMF (Risk Management Framework)**
- **EU AI Act** — security obligations high-risk

## Stack
- **Lakera Guard** — prompt injection defense
- **Robust Intelligence (now Cisco)** — AI security platform
- **HiddenLayer** — model security
- **Protect AI** — MLSecOps
- **Garak (NVIDIA)** — LLM red-teaming
- **PromptFoo** — adversarial testing

## Templates
1. AI security threat model (per use case)
2. Red team LLM playbook
3. Prompt injection defense (input/output filters)
4. Model card security section
5. Incident response AI-specific
6. Vendor AI security questionnaire

## Cross-references
- [[lex-ai-governance]] · [[nomos-eu-ai-act-pt]] · [[sphinx-red-team-ops]]
