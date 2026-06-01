---
name: sphinx-post-quantum-cryptography
description: PQC implementation — Kyber/Dilithium/SPHINCS+/Falcon, hybrid schemes. Triggers em "post quantum cryptography", "PQC", "Kyber", "Dilithium", "SPHINCS", "Falcon", "lattice-based crypto", "hash-based signatures".
license: SEE-LICENSE
parent_agent: sphinx-director
---

# SPHINX-POST-QUANTUM-CRYPTOGRAPHY

## Algorithm families
- **Lattice-based:** Kyber (KEM), Dilithium (sig), Falcon (sig)
- **Hash-based:** SPHINCS+ (sig only)
- **Code-based:** Classic McEliece (KEM, very large keys)
- **Isogeny-based:** SIKE (broken 2022)
- **Multivariate:** Rainbow (broken 2022)

## NIST FIPS standards (2024)
- **FIPS 203 (ML-KEM):** Kyber → standardized
- **FIPS 204 (ML-DSA):** Dilithium → standardized
- **FIPS 205 (SLH-DSA):** SPHINCS+ → standardized
- **FIPS 206 (FN-DSA):** Falcon → in draft (2025)

## Hybrid schemes
- **TLS:** X25519+Kyber (Cloudflare, Apple, etc.)
- **SSH:** OpenSSH supports
- **PKI:** transition certificates
- **VPN:** WireGuard PQ extensions

## Practical sizes
| Algorithm | Public key | Signature/Ciphertext |
|---|---|---|
| Ed25519 (classical) | 32 bytes | 64 bytes |
| Dilithium 3 | 1952 bytes | 3293 bytes |
| Falcon 512 | 897 bytes | 666 bytes |
| Kyber 768 | 1184 bytes | 1088 bytes |
| SPHINCS+ small | 32 bytes | 7856 bytes |

## Stack
- **liboqs (Open Quantum Safe)** — reference implementation
- **wolfSSL** — PQ-enabled
- **BoringSSL (Google)** — PQ experiments
- **AWS KMS Hybrid PQ** — available
- **Cloudflare PQ** — public deployment

## Templates
1. PQC algorithm selection per use case
2. Hybrid migration plan (X25519+Kyber example)
3. PKI re-issuance roadmap
4. Performance benchmark methodology
5. PQC integration testing
6. Vendor PQ readiness assessment

## Cross-references
- [[sphinx-quantum-crypto-prep]] · [[aegis-secrets-management]] · [[aegis-zero-trust-architecture]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **sphinx-post-quantum-cryptography** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in sphinx-post-quantum-cryptography:**

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
