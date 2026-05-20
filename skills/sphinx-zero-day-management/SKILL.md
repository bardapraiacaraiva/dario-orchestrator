---
name: sphinx-zero-day-management
description: 0day disclosure, exploit dev for defense, bounty programs, CVE coordination. Triggers em "zero day", "0day", "CVE", "responsible disclosure", "exploit development", "bug bounty", "ZDI", "HackerOne".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [responsible_disclosure, classified_handling, audit_immutable]
---

# SPHINX-ZERO-DAY-MANAGEMENT

## Disclosure models
- **Full disclosure:** public immediately (controversial)
- **Coordinated (CVD):** vendor → patch → public (standard)
- **Responsible:** give vendor 90 days
- **No disclosure:** government / IC reservation

## Bug bounty programs
- **HackerOne** — largest platform
- **Bugcrowd** — alternative
- **Intigriti** — EU-focused
- **YesWeHack** — France
- **Vendor self-managed:** Google, Microsoft, Apple

## Marketplaces (controversial)
- **ZDI (Zerodium):** acquires 0days for offensive
- **Crowdfense** — similar
- **Government exclusive** — US, Israel, etc.

## Exploit development
- **Memory corruption:** buffer overflow, UAF, type confusion
- **Web:** SQLi, XSS, deserialization, SSRF
- **Logic flaws:** authn/authz bypass
- **Crypto:** padding oracle, timing attacks
- **Hardware:** Spectre/Meltdown variants

## Templates
1. CVD process (timeline, escalation)
2. Bug bounty program design
3. CVE submission template
4. Patch verification framework
5. Exploit weaponization (for defense)
6. Internal 0day handling policy

## Cross-references
- [[sphinx-reverse-engineering]] · [[aegis-vulnerability-management]] · [[aegis-pentest-methodology]]
