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
