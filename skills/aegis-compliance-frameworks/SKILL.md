---
name: aegis-compliance-frameworks
description: Compliance — ISO 27001/2, SOC 2, PCI-DSS, HIPAA, NIST CSF. Audit prep, gap analysis. Triggers em "ISO 27001", "SOC 2", "PCI DSS", "HIPAA", "NIST CSF", "compliance audit", "auditoria segurança".
license: SEE-LICENSE
parent_agent: aegis-director
compliance: [iso27001_audit, soc2_type2, audit_immutable]
---

# AEGIS-COMPLIANCE-FRAMEWORKS

## Quando usar
- Certification first-time (ISO 27001, SOC 2)
- Annual recertification
- Customer/vendor requirement (enterprise customers asking for SOC 2)
- Gap analysis pré-audit
- Multi-framework alignment (single program, multiple certs)

## Frameworks
- **ISO 27001/27002:** ISMS, controls (Annex A 2022)
- **SOC 2 Type II:** Trust Service Criteria (5 TSCs)
- **PCI-DSS 4.0:** payment card data
- **HIPAA:** US healthcare
- **NIST CSF 2.0:** Identify/Protect/Detect/Respond/Recover/Govern
- **CIS Controls v8:** 18 controls + IGs
- **CSA STAR:** cloud security
- **LGPD/GDPR:** privacy

## Templates
1. ISO 27001 Statement of Applicability (SoA)
2. Risk register (ISO 27005)
3. Annex A control implementation tracker
4. SOC 2 evidence collection schedule
5. PCI-DSS scoping (CDE + connected systems)
6. Multi-framework crosswalk matrix

## Stack
- **GRC tools:** Drata, Vanta, Secureframe, Tugboat
- **Risk:** ServiceNow GRC, RSA Archer, OneTrust
- **Audit:** AuditBoard, Workiva

## Cross-references
- [[risco-iso27001]] · [[aegis-secure-sdlc]] · [[lex-lgpd]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **aegis-compliance-frameworks** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in aegis-compliance-frameworks:**

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
