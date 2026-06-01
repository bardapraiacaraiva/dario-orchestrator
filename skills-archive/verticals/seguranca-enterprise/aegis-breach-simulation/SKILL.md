---
name: aegis-breach-simulation
description: Breach & Attack Simulation (BAS) — AttackIQ, SafeBreach, Picus, MITRE Caldera, Atomic Red Team. Triggers em "BAS", "breach simulation", "AttackIQ", "SafeBreach", "Picus", "Caldera", "Atomic Red Team", "purple team", "continuous validation".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, audit_immutable, responsible_disclosure]
---

# AEGIS-BREACH-SIMULATION

## Filosofia
**Continuous validation > point-in-time pentest.** BAS runs ATT&CK techniques diariamente, validates detection coverage.

## Quando usar
- Validate detection coverage (qual % ATT&CK detectamos?)
- Purple team continuous engagement
- Post-breach validation (gap closed?)
- Annual control attestation (compliance evidence)
- M&A integration (security maturity)

## BAS vs Pentest vs Red Team
| | BAS | Pentest | Red Team |
|---|---|---|---|
| Frequência | Continuous | Annual | Quarterly |
| Scope | Detection coverage | Vulnerabilities | Objective-based |
| Automation | High | Low | Low-Medium |
| Cost | $$ subscription | $$ engagement | $$$ engagement |

## Stack
- **AttackIQ Platform** — enterprise líder BAS
- **SafeBreach** — enterprise BAS
- **Picus Security** — BAS + Security Validation
- **Mandiant Security Validation** (ex-Verodin)
- **MITRE Caldera** — open-source BAS framework
- **Atomic Red Team (Red Canary)** — open-source ATT&CK tests
- **Cymulate** — BAS platform

## Templates
1. BAS program design (purple team operating model)
2. ATT&CK coverage matrix (technique × detection × response)
3. Atomic Red Team test execution playbook
4. Caldera adversary emulation campaign
5. Quarterly BAS report (coverage trend + gaps + fixes)
6. Purple team tabletop scenarios

## Métricas
- **ATT&CK coverage:** % techniques detected
- **MTTD trend:** Mean Time to Detect (improving?)
- **Defense efficacy:** % simulated attacks detected
- **False positive rate:** detections that fired but shouldn't

## Compliance
- ✓ ISO 27001 A.12.6.1 — Vuln management
- ✓ SOC 2 CC7.1 — System operations monitoring
- ✓ PCI-DSS 11.4 — Network IDS/IPS testing
- ✓ NIST CSF DE.CM — Continuous monitoring

## Cross-references
- [[aegis-pentest-methodology]] · [[aegis-soc-operations]] · [[aegis-threat-modeling]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-breach-simulation** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-breach-simulation:**

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
