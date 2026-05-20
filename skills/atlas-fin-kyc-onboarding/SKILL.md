---
name: atlas-fin-kyc-onboarding
description: KYC onboarding — document validation, liveness check, biometrics, PEP screening, BR + EU. Triggers em "KYC onboarding", "liveness check", "biometric KYC", "Jumio", "Onfido", "Sumsub", "Unico", "PEP screening".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [audit_immutable, sanctions_realtime]
---

# ATLAS-FIN-KYC-ONBOARDING

## Workflow KYC
```
1. Customer initiates signup
2. Document capture (CNH/RG/Passport)
3. Document validation (OCR + authenticity)
4. Liveness check (selfie + face match)
5. Biometric vs doc face
6. PEP + sanctions screening
7. Address validation (proof of address)
8. Risk scoring
9. Onboarding decision (auto/review/reject)
```

## Stack
- **Jumio** — global líder
- **Onfido (now Entrust)** — UK líder
- **Sumsub** — emerging markets focus
- **Unico (BR)** — líder BR (PIX endorsed)
- **Veriff** — emerging markets
- **iDenfy** — mid-market
- **Persona** — developer-friendly

## BR document types
- CNH (Carteira Nacional Habilitação)
- RG (Registro Geral) com CPF
- Passaporte
- CRNM (Carteira Registro Nacional Migratório)

## Liveness check types
- **Passive:** selfie analysis (mais UX-friendly)
- **Active:** turn head, smile, blink (mais seguro)
- **3D depth:** TrueDepth iOS, structured light Android

## Templates
1. KYC flow architecture
2. Document validation rules per country
3. Liveness check UX best practices
4. Risk scoring matrix (auto-approve threshold)
5. Manual review queue + SLA
6. KYC refresh policy (annual high-risk)

## Cross-references
- [[atlas-fin-aml-monitoring]] · [[atlas-fin-sanctions-screening]] · [[nomos-kyc-aml-pt]]
