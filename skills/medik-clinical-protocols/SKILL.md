---
name: medik-clinical-protocols
description: Protocolos clínicos — PCDT (Min. Saúde), guidelines internacionais, evidence-based medicine. Triggers em "protocolo clínico", "PCDT", "guideline", "evidence-based", "MBE", "diretrizes clínicas".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [cfm_205_2021_gate, privilege_clinical]
jurisdiction: Brasil
---

# MEDIK-CLINICAL-PROTOCOLS

## Quando usar
- Implementar PCDT no serviço (SUS-compatível)
- Criar protocolos internos clínica/hospital
- Auditoria de adesão a guidelines
- Adaptação de guideline internacional → contexto BR
- CDSS (Clinical Decision Support System) setup

## Fontes
- **PCDT Min. Saúde** — Protocolos Clínicos e Diretrizes Terapêuticas
- **CONITEC** — Comissão Nac. Incorporação Tecnologias SUS
- **UpToDate / DynaMed / BMJ Best Practice** — referência internacional
- **Sociedades médicas BR:** SBC, SBI, AMB, FBG, etc.
- **CMS Guidelines** (US), NICE (UK) — adaptação cuidadosa

## Templates
1. Protocolo institucional template (objetivo + escopo + população + intervenção + outcomes)
2. CDSS rule engine (drug-allergy, drug-drug, dose adjust)
3. Audit de adesão (% pacientes conforme protocolo)
4. Adaptação guideline internacional (cultural + epidemiológica + econômica)
5. Avaliação de tecnologia (ATS/HTA-style)

## Cross-references
- [[medik-clinical-decision-support]] · [[medik-emr-integration]] · [[medik-anvisa-regulatory]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **medik-clinical-protocols** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in medik-clinical-protocols:**

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
