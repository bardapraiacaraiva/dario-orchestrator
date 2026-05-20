---
name: atlas-fin-sanctions-screening
description: Sanctions screening — OFAC, EU, UN, BR (COAF), real-time + batch. Triggers em "sanctions screening", "OFAC", "EU sanctions", "UN sanctions", "BR COAF", "watchlist screening", "Refinitiv World-Check".
license: SEE-LICENSE
parent_agent: atlas-fin-director
compliance: [sanctions_realtime, audit_immutable]
---

# ATLAS-FIN-SANCTIONS-SCREENING

## Listas sanções principais
- **OFAC SDN (US)** — Specially Designated Nationals
- **EU Consolidated List**
- **UN Security Council Sanctions**
- **UK HMT Sanctions List**
- **BR COAF / Bacen** — listas internas
- **PT BdP** — sanctions PT-specific
- **HMT (UK)** — Treasury sanctions list

## Stack
- **Refinitiv World-Check** — líder
- **Dow Jones Risk & Compliance** — premium
- **LexisNexis Bridger** — enterprise
- **ComplyAdvantage** — modern API-first
- **Sanctions.io** — developer-friendly
- **Acuris (now Moody's)** — Risk integrated

## Screening modes
- **Real-time:** transaction-time check (mandatory)
- **Daily batch:** customer base re-screen (lists update)
- **Onboarding:** KYC moment
- **Periodic refresh:** annual high-risk customers

## Match handling
- **True positive:** confirmed match → block + escalate
- **False positive:** similar name, different person → whitelist
- **Partial match:** require manual review
- **Fuzzy match:** transliteration (Mohammed = Muhammad)

## Templates
1. Sanctions screening architecture (real-time API)
2. List update automation (Refinitiv feed)
3. False positive review workflow
4. PEP screening (separate from sanctions)
5. Annual screening audit report
6. Sanctions program governance

## Cross-references
- [[atlas-fin-aml-monitoring]] · [[atlas-fin-kyc-onboarding]] · [[aegis-third-party-risk]]
