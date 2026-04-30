---
name: risco-aml
description: "AML/KYC compliance — customer due diligence, PEP screening, suspicious transaction reporting, PT Law 83/2017"
version: "1.0"
---

# RISCO-AML: Anti-Money Laundering & KYC Skill

## When to Activate

**Trigger words (PT):** branqueamento de capitais, financiamento do terrorismo, kyc, due diligence, pep, pessoa politicamente exposta, lei 83/2017, comunicacao de operacoes suspeitas, dmbii, uif, beneficiario efetivo
**Trigger words (EN):** aml, anti-money laundering, kyc, know your customer, due diligence, pep screening, suspicious transaction, beneficial owner, cft, terrorist financing, fatf, compliance officer

## Step-by-Step Workflow

### Phase 1: Risk Assessment (Entity-Level)
1. Identify obliged entity category under Lei 83/2017 (Art. 3)
2. Conduct national risk assessment alignment
3. Map products/services by ML/TF risk (high/medium/low)
4. Assess geographic risk (FATF grey/black list, high-risk jurisdictions)
5. Document risk appetite and tolerance

### Phase 2: Customer Due Diligence (CDD)
1. **Simplified DD** (Art. 23): low-risk customers, verify identity
2. **Standard DD** (Art. 24-27): identify + verify customer and beneficial owner
3. **Enhanced DD** (Art. 35-37): high-risk situations, PEPs, high-risk countries
4. Collect: full name, DOB, nationality, tax ID (NIF), address, profession
5. Verify via official documents (CC, passport, certidao comercial)
6. Identify beneficial owners (>25% ownership or control)

### Phase 3: PEP Screening
1. Screen against PEP lists (national and international)
2. Check family members and close associates of PEPs
3. Apply enhanced measures: senior management approval, source of wealth/funds
4. Ongoing monitoring for PEP status changes
5. Maintain PEP records for 7 years after relationship ends

### Phase 4: Ongoing Monitoring
1. Transaction monitoring against customer profile
2. Periodic review based on risk rating (high: annual, medium: biennial, low: triennial)
3. Update CDD information upon trigger events
4. Screen against sanctions lists (EU, UN, OFAC)
5. Monitor for unusual patterns or red flag indicators

### Phase 5: Suspicious Transaction Reporting
1. Detect suspicious activity using red flag indicators
2. Internal escalation to compliance officer (OCRI)
3. File report with UIF (Unidade de Informacao Financeira) via DMBII platform
4. Do NOT tip off the customer (Art. 54 Lei 83/2017)
5. Maintain report records and follow-up

### Phase 6: Record Keeping
1. CDD documents: retain 7 years after end of relationship
2. Transaction records: retain 7 years after execution
3. STR records: retain 7 years after filing
4. Training records: retain indefinitely
5. Ensure records available to ASAE, BdP, CMVM, or sector supervisor

## Commands Table

| Command | Description |
|---------|-------------|
| `risco aml audit` | Full AML/CFT compliance assessment |
| `risco aml cdd` | Customer Due Diligence checklist |
| `risco aml pep` | PEP screening procedure and checklist |
| `risco aml risk` | ML/TF risk assessment for entity |
| `risco aml str` | Suspicious Transaction Report template |
| `risco aml training` | AML training plan and materials |
| `risco aml sanctions` | Sanctions screening procedure |
| `risco aml bo` | Beneficial owner identification guide |

## Output Template

```markdown
# AML/KYC Compliance Report — [Entity]
**Date:** YYYY-MM-DD | **OCRI:** [Name] | **Supervisor:** [BdP/CMVM/ASAE/IF]

## 1. Entity Risk Profile
- Entity type: [obliged entity category]
- Risk rating: [HIGH/MEDIUM/LOW]
- Products: [list with risk ratings]
- Jurisdictions: [list with risk ratings]

## 2. CDD Status
| Customer Segment | Total | CDD Complete | Pending | Overdue |
|-----------------|-------|-------------|---------|---------|

## 3. PEP Exposure
- PEP customers identified: X
- Enhanced DD applied: X/X
- Senior management approval: [yes/no per case]

## 4. Monitoring
- Transactions monitored (period): X
- Alerts generated: X | Investigated: X | Cleared: X
- STRs filed: X

## 5. Gaps & Recommendations
| # | Gap | Risk Level | Action Required | Deadline |
|---|-----|-----------|----------------|----------|

## 6. Next Review: YYYY-MM-DD
```

## Red Flags

- No formal AML/CFT risk assessment conducted
- CDD incomplete or outdated for high-risk customers
- No beneficial owner identification for corporate customers
- PEP screening not conducted or not documented
- No compliance officer (OCRI) appointed
- Suspicious transactions not reported to UIF
- Tipping off customer about STR
- Records destroyed before 7-year retention period
- No staff training on AML/CFT obligations
- Sanctions screening not performed or not automated
- Cash transactions above EUR 3,000 not properly documented
- Wire transfers missing originator/beneficiary information
- Shell company customers with no clear economic purpose
- Customers from FATF high-risk/grey-list jurisdictions without enhanced DD

## Key Legislation

- **Lei 83/2017** — PT AML/CFT framework (transposing 4AMLD/5AMLD)
- **Lei 89/2017** — Central Register of Beneficial Owners (RCBE)
- **Directive (EU) 2015/849** — 4th Anti-Money Laundering Directive
- **Directive (EU) 2018/843** — 5th Anti-Money Laundering Directive
- **FATF Recommendations** — International standards
- **Aviso BdP 2/2018** — Bank of Portugal AML instructions
