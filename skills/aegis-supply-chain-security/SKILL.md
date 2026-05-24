---
name: aegis-supply-chain-security
description: Software supply chain security — SLSA, SBOM, Sigstore, dependency confusion, typosquatting. Triggers em "supply chain security", "SLSA", "SBOM", "Sigstore", "cosign", "in-toto", "dependency confusion", "SolarWinds", "Log4Shell".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable]
---

# AEGIS-SUPPLY-CHAIN-SECURITY

## Quando usar
- SBOM (Software Bill of Materials) program
- SLSA level achievement (1 → 4)
- Signed releases (Sigstore/cosign)
- Detect dependency confusion / typosquatting
- Build provenance attestation
- Post-SolarWinds maturity review

## Frameworks
- **SLSA v1.0 (Google/OpenSSF):** 4 levels of supply chain integrity
- **NIST SSDF (SP 800-218):** Secure Software Dev Framework
- **CIS Software Supply Chain Security Guide**
- **EU Cyber Resilience Act (CRA)** — coming 2027
- **US Executive Order 14028** — federal SBOM requirement

## SLSA levels
- **L1:** Documentation of build process
- **L2:** Tampering-resistant builds (signed provenance)
- **L3:** Source + build platform meet stronger criteria
- **L4:** Two-party review + hermetic builds

## Stack
- **SBOM:** Syft, CycloneDX, SPDX
- **Signing:** Sigstore (cosign, fulcio, rekor)
- **Verification:** in-toto, SLSA verifier
- **Dependency scan:** Snyk, Dependabot, Renovate
- **Container scan:** Trivy, Grype
- **Provenance:** GitHub Actions OIDC + cosign

## Templates
1. SBOM generation pipeline (Syft → CycloneDX format → store + sign)
2. SLSA L3 deployment workflow (signed provenance + verify before deploy)
3. Dependency confusion prevention (private registry namespace claim)
4. Cosign keyless signing (OIDC-based, no key management)
5. SBOM ingestion + vuln correlation (continuous)
6. Vendor SBOM request template

## Threats típicas
- **Dependency confusion** (Birsan attack)
- **Typosquatting** (similar package names)
- **Maintainer takeover** (account compromise)
- **Compromised build system** (SolarWinds)
- **Backdoored dependencies** (xz utils, event-stream)

## Cross-references
- [[aegis-secure-sdlc]] · [[aegis-third-party-risk]] · [[builder-ci-cd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-supply-chain-security** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-supply-chain-security:**

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
