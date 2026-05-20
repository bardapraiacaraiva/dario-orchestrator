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
