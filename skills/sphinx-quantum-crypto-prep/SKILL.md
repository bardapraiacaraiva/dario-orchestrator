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
