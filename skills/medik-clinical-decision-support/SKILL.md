---
name: medik-clinical-decision-support
description: Clinical Decision Support — drug-drug interactions, alergias, dose adjust, evidence-based prompts. Triggers em "CDSS", "decision support", "drug interaction", "alerta clínico", "prescrição segura".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [cfm_205_2021_gate, privilege_clinical, model_explainability]
jurisdiction: Brasil
---

# MEDIK-CLINICAL-DECISION-SUPPORT

## Quando usar
- CDSS embarcado em EMR
- Rule engine de prescrição (Allergies, DDI)
- Alertas evidence-based (sepsis, AKI, deterioration)
- Antimicrobial stewardship
- Risk stratification ML models

## Stack
- **Drools / OpenRules** — rule engine open-source
- **Cliniface / Bahmni** — open-source healthcare
- **Epic Sepsis Model** (reference, controvertido)
- **DDI databases:** Lexicomp, Micromedex
- **LLM-augmented CDSS** — careful sobre hallucinations

## Princípios
- **Alert fatigue:** menos é mais (especificidade > sensibilidade)
- **Explainable:** mostrar why-alert
- **Override-friendly:** doutor sempre decide, alerta NÃO bloqueia
- **Audit trail:** log overrides com motivo
- **Evidence-graded:** Cochrane/GRADE level

## Templates
1. Drug-Drug Interaction rule library
2. Allergy cross-reactivity matrix
3. Dose adjust algorithms (renal/hepatic)
4. Sepsis early warning score (qSOFA + SIRS)
5. CDSS deployment + iteration playbook

## Compliance
- ✓ ANVISA SaMD (Software as Medical Device) Classe II
- ✓ LGPD Art. 20 — direito à revisão decisão automatizada
- ✓ Model card + explainability

## Cross-references
- [[medik-clinical-protocols]] · [[demeter-predictive]] · [[lex-ai-governance]]
