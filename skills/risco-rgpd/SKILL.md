---
name: risco-rgpd
description: "RGPD/GDPR compliance — data mapping, DPIA, consent management, breach notification 72h, ROPA, DPO obligations"
version: "1.0"
---

# RISCO-RGPD: RGPD/GDPR Compliance Skill

## When to Activate

**Trigger words (PT):** rgpd, protecao de dados, dados pessoais, consentimento, dpia, violacao de dados, encarregado de protecao de dados, registo de atividades, subcontratante, responsavel pelo tratamento, direito ao esquecimento, portabilidade, base legal
**Trigger words (EN):** gdpr, data protection, personal data, consent, dpia, data breach, dpo, ropa, data mapping, data subject rights, lawful basis, privacy impact, data processing agreement

## Step-by-Step Workflow

### Phase 1: Data Mapping
1. Identify all personal data categories processed (name, email, IP, health, financial, biometric)
2. Map data flows: collection point -> storage -> processing -> sharing -> deletion
3. Identify data controllers, processors, and sub-processors
4. Document lawful basis for each processing activity (Art. 6 RGPD)
5. Classify data sensitivity (standard vs special categories Art. 9)

### Phase 2: ROPA (Record of Processing Activities)
1. Create register per Art. 30 RGPD
2. Document: purpose, categories of data subjects, categories of data, recipients, transfers to third countries, retention periods, security measures
3. Maintain separate registers for controller and processor roles
4. Review and update quarterly

### Phase 3: DPIA (Data Protection Impact Assessment)
1. Determine if DPIA is required (Art. 35 criteria + CNPD mandatory list)
2. Describe processing operations and purposes
3. Assess necessity and proportionality
4. Identify risks to data subjects (likelihood x severity)
5. Define mitigation measures
6. Consult DPO and, if needed, CNPD (Art. 36)

### Phase 4: Consent Management
1. Design consent collection (granular, specific, informed, freely given)
2. Implement consent withdrawal mechanism (as easy as giving consent)
3. Maintain consent records (who, when, what, how)
4. Review consent validity periodically
5. Handle children's consent (Art. 8 — age 13 in PT per Lei 58/2019)

### Phase 5: Breach Notification
1. Detect and classify breach severity
2. Notify CNPD within 72 hours (Art. 33) if risk to rights/freedoms
3. Notify affected data subjects without undue delay if high risk (Art. 34)
4. Document all breaches in internal register (even non-notifiable)
5. Implement corrective measures and lessons learned

### Phase 6: Data Subject Rights
1. Right of access (Art. 15) — respond within 30 days
2. Right to rectification (Art. 16)
3. Right to erasure (Art. 17) — assess exceptions
4. Right to restriction (Art. 18)
5. Right to data portability (Art. 20)
6. Right to object (Art. 21) — including profiling
7. Automated decision-making rights (Art. 22)

## Commands Table

| Command | Description |
|---------|-------------|
| `risco rgpd audit` | Full RGPD compliance gap analysis |
| `risco rgpd ropa` | Generate ROPA template for organization |
| `risco rgpd dpia` | Run DPIA for specific processing activity |
| `risco rgpd breach` | Breach notification checklist and timeline |
| `risco rgpd consent` | Consent mechanism review and design |
| `risco rgpd rights` | Data subject rights response templates |
| `risco rgpd mapping` | Data flow mapping exercise |
| `risco rgpd transfer` | International transfer assessment (SCCs, adequacy) |
| `risco rgpd dpa` | Generate Data Processing Agreement template |

## Output Template

```markdown
# RGPD Compliance Report — [Organization]
**Date:** YYYY-MM-DD | **Assessor:** [Name] | **Scope:** [Description]

## 1. Data Mapping Summary
| Data Category | Lawful Basis | Retention | Recipients | Transfer |
|--------------|-------------|-----------|------------|----------|

## 2. ROPA Status
- Total processing activities: X
- Documented: X | Pending: X
- Last review: YYYY-MM-DD

## 3. DPIA Required
- [ ] High-risk processing identified: [details]
- [ ] DPIA completed: [date]

## 4. Consent Status
- Active consents: X | Withdrawn: X
- Collection mechanism: [compliant/non-compliant]

## 5. Breach Readiness
- Breach procedure: [documented/not documented]
- Last breach drill: [date]
- CNPD contact ready: [yes/no]

## 6. Gaps & Recommendations
| # | Gap | Risk | Priority | Deadline |
|---|-----|------|----------|----------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- No ROPA maintained despite >250 employees or regular processing of sensitive data
- Consent banners pre-ticked or bundled with T&C acceptance
- No breach notification procedure documented
- International transfers without SCCs or adequacy decision
- Retention periods undefined or "indefinite"
- No DPO appointed when mandatory (public authority, large-scale monitoring, special categories)
- Data subject requests ignored or responded after 30-day deadline
- Sub-processors not documented in DPA
- DPIA not conducted for high-risk processing (profiling, large-scale monitoring, biometrics)
- Lei 58/2019 (PT national law) specificities ignored (e.g., employee data, deceased persons)
- Cookie consent not RGPD-compliant (no reject button, implied consent)
- Privacy policy not in Portuguese or not accessible

## Key Legislation

- **Regulation (EU) 2016/679** — General Data Protection Regulation
- **Lei 58/2019** — PT national RGPD implementation
- **Lei 41/2004** — Privacy in electronic communications (cookies, e-marketing)
- **CNPD Guidelines** — Portuguese Data Protection Authority guidance
