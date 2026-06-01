---
name: sphinx-quantum-crypto-prep
description: Post-quantum crypto migration, NIST PQC, crypto inventory, hybrid schemes. Triggers em "post quantum crypto", "PQC", "NIST PQC", "quantum threat", "harvest now decrypt later", "CRYSTALS Kyber", "CRYSTALS Dilithium", "quantum-safe".
license: SEE-LICENSE
parent_agent: sphinx-director
---

# SPHINX-QUANTUM-CRYPTO-PREP

## Threat
**Harvest now, decrypt later:** adversaries collecting encrypted data NOW, decrypt when CRQC (Cryptographically-Relevant Quantum Computer) available (2030-2035 estimated).

## NIST PQC (2024 standards)
- **FIPS 203 (ML-KEM):** Key Encapsulation (CRYSTALS-Kyber)
- **FIPS 204 (ML-DSA):** Digital Signatures (CRYSTALS-Dilithium)
- **FIPS 205 (SLH-DSA):** Hash-based Signatures (SPHINCS+)
- **FIPS 206 (FN-DSA):** FALCON-based (forthcoming)

## Migration approach
- **Crypto inventory:** identify ALL crypto usage
- **Risk-based prioritize:** long-shelf-life data first
- **Hybrid mode:** classical + post-quantum together (transition)
- **Cryptographic agility:** ability to swap algorithms
- **Hardware constraints:** PQC larger keys/signatures

## Timeline NIST
- **2024:** standards published
- **2025-2030:** migration begin (high-value systems)
- **2030:** end-of-life classical (recommended)
- **2035:** legacy crypto deprecated

## Templates
1. Crypto inventory methodology
2. Risk assessment (data sensitivity × longevity)
3. Migration roadmap 2025-2030
4. Hybrid implementation patterns
5. Vendor PQC readiness questionnaire
6. Crypto-agility architecture

## Cross-references
- [[sphinx-post-quantum-cryptography]] · [[aegis-secrets-management]] · [[gaia-transition-planning]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-quantum-crypto-prep** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-quantum-crypto-prep:**

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
