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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-clinical-decision-support** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-clinical-decision-support:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
