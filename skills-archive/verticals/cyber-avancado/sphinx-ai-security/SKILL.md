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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-ai-security** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-ai-security:**

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
