---
name: nexus-security
description: "SecOps — SIEM, vulnerability scanning, incident response playbooks, patching, threat detection"
version: "1.0"
---

# NEXUS-SECURITY: Security Operations Skill

## When to Activate

**Trigger words (PT):** seguranca operacional, siem, vulnerabilidades, incidentes de seguranca, patching, ameacas, deteção, resposta a incidentes, pentest, hardening, zero trust
**Trigger words (EN):** secops, siem, vulnerability scanning, incident response, patching, threat detection, security operations, penetration testing, hardening, zero trust, soc, security playbook

## Step-by-Step Workflow

### Phase 1: Security Baseline
1. Asset inventory: all servers, endpoints, network devices, cloud resources, SaaS
2. Vulnerability scanning: schedule and scope (Nessus, Qualys, Tenable, OpenVAS)
3. Configuration baseline: CIS Benchmarks for OS, databases, cloud services
4. Network segmentation review: internal zones, DMZ, trust boundaries
5. Endpoint protection: EDR deployed on all endpoints, AV signatures current
6. Patch management baseline: current patch levels across all systems

### Phase 2: Threat Detection (SIEM)
1. Log sources: OS events, application logs, firewall, WAF, DNS, auth, cloud trail
2. SIEM deployment: Splunk, Sentinel, Elastic SIEM, QRadar, Wazuh
3. Detection rules:
   - Brute force attempts (>5 failed logins in 5 min)
   - Privilege escalation
   - Lateral movement (unusual internal traffic)
   - Data exfiltration (large outbound transfers)
   - Malware indicators (known IoCs)
4. MITRE ATT&CK mapping for detection coverage
5. Threat intelligence feed integration
6. SOC procedures: triage, investigation, escalation

### Phase 3: Vulnerability Management
1. Scan cadence: weekly for internet-facing, monthly for internal, on-change for critical
2. Severity classification: CVSS-based (Critical >9.0, High 7.0-8.9, Medium 4.0-6.9, Low <4.0)
3. Remediation SLAs: Critical <7d, High <30d, Medium <90d, Low <180d
4. Patch management workflow: test -> stage -> prod (with rollback plan)
5. Exception process for cannot-patch situations (compensating controls)
6. Vulnerability trending and mean-time-to-remediate (MTTR) tracking

### Phase 4: Incident Response
1. Incident classification: P1-P4 per severity and impact
2. Response playbooks per incident type:
   - Ransomware: isolate, preserve, report, restore from backup
   - Data breach: contain, assess scope, notify (CNPD 72h), remediate
   - DDoS: activate mitigation, CDN/WAF rules, ISP coordination
   - Insider threat: preserve evidence, HR involvement, access revocation
   - Phishing: block sender, reset credentials, scan for compromise
3. Evidence preservation: forensic images, log exports, chain of custody
4. Communication: internal (CISO, legal, PR) and external (regulators, customers)

### Phase 5: Hardening
1. OS hardening: CIS Benchmark Level 1 minimum
2. Network: WAF, IDS/IPS, DDoS protection, DNS filtering
3. Application: OWASP Top 10 mitigations, CSP headers, rate limiting
4. Cloud: Security Hub, Azure Security Center, GCP Security Command Center
5. Email: SPF, DKIM, DMARC, anti-phishing training
6. Zero Trust: verify explicitly, least privilege, assume breach

### Phase 6: Metrics & Reporting
1. Security KPIs: MTTR, patch compliance, vuln aging, incidents by type
2. Monthly security report to CISO/management
3. Quarterly vulnerability trend analysis
4. Annual penetration test and red team exercise
5. Security awareness training metrics (phishing simulation results)
6. Compliance alignment: ISO 27001, NIS2, SOC2 technical controls

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus security audit` | Security posture assessment |
| `nexus security vuln` | Vulnerability management dashboard |
| `nexus security incident` | Incident response playbook generator |
| `nexus security siem` | SIEM rule and log source review |
| `nexus security patch` | Patch compliance report |
| `nexus security harden` | Hardening checklist by asset type |
| `nexus security threat` | Threat model for application/system |
| `nexus security pentest` | Pentest scope and findings template |

## Output Template

```markdown
# Security Operations Report — [Organization]
**Date:** YYYY-MM-DD | **Period:** [Month/Quarter] | **CISO:** [Name]

## 1. Security Posture Score: X/100

## 2. Vulnerability Summary
| Severity | Open | New | Remediated | Overdue SLA | MTTR |
|----------|------|-----|-----------|-------------|------|
| Critical | | | | | |
| High | | | | | |
| Medium | | | | | |
| Low | | | | | |

## 3. Patch Compliance
| Asset Type | Total | Patched | Compliance % | Oldest Missing |
|-----------|-------|---------|-------------|---------------|

## 4. Incidents (Period)
| # | Date | Type | Severity | MTTA | MTTR | Status |
|---|------|------|----------|------|------|--------|

## 5. SIEM Detection Coverage
| MITRE Tactic | Rules Active | Coverage % |
|-------------|-------------|-----------|

## 6. Recommendations
| # | Finding | Risk | Action | Priority |
|---|---------|------|--------|----------|

## 7. Next Pentest: YYYY-MM-DD | Next Review: YYYY-MM-DD
```

## Red Flags

- No vulnerability scanning in place
- Critical vulnerabilities open >30 days
- No SIEM or centralized log management
- Incident response procedure undocumented
- No regular penetration testing (<1/year)
- Patch management ad-hoc (no SLAs or tracking)
- Endpoints without EDR/antivirus
- No security awareness training
- Internet-facing systems without WAF
- Default credentials in production systems
- No network segmentation between environments
- SIEM rules not updated for emerging threats
