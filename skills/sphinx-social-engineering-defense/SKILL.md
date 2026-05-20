---
name: sphinx-social-engineering-defense
description: Anti-social engineering — advanced phishing, vishing, smishing, BEC, deepfakes. Triggers em "social engineering defense", "advanced phishing", "vishing", "smishing", "BEC", "business email compromise", "deepfake detection".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable]
---

# SPHINX-SOCIAL-ENGINEERING-DEFENSE

## Attack vectors
- **Phishing:** email-based
- **Spear phishing:** targeted individual
- **Whaling:** target executives
- **Vishing:** voice (phone)
- **Smishing:** SMS
- **BEC (Business Email Compromise):** CFO fraud, vendor fraud
- **Deepfake voice/video:** AI-generated impersonation
- **Pretexting:** elaborate scenarios

## Defensive layers
- **Technical:** DMARC, DKIM, SPF, sandboxing email
- **AI detection:** behavior anomaly (Abnormal Security, Tessian)
- **Training:** continuous + role-based
- **Process:** out-of-band verification for $$$ transfers
- **Insurance:** cyber + crime policies

## BEC defense
- **Email banner warning:** external sender
- **Wire transfer verification:** phone callback to known number
- **Vendor change verification:** out-of-band
- **CFO/CEO impersonation training**
- **Bait-and-switch detection** (similar domain)

## Templates
1. Anti-phishing program design
2. BEC playbook + financial controls
3. Deepfake awareness training
4. Vendor verification SOP
5. Executive threat protection
6. Incident response (post-compromise wire)

## Cross-references
- [[aegis-security-awareness]] · [[aegis-incident-response]] · [[sphinx-osint-investigations]]
