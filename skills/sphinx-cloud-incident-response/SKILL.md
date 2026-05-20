---
name: sphinx-cloud-incident-response
description: Cloud IR — AWS/Azure/GCP, account compromise, container forensics. Triggers em "cloud incident response", "AWS incident", "Azure compromise", "GCP forensics", "container forensics", "K8s forensics", "cloud forensics".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, responsible_disclosure]
---

# SPHINX-CLOUD-INCIDENT-RESPONSE

## Differences vs on-prem IR
- **Ephemeral resources:** containers killed = evidence lost
- **API-based access:** different forensics approach
- **Shared responsibility:** customer vs CSP
- **Audit logs primary:** CloudTrail, Azure Activity, GCP Audit
- **Storage forensics:** S3, Azure Blob, GCS
- **Identity-based:** IAM compromise common

## Per-CSP playbooks

### AWS
- **Disable IAM access keys:** immediate
- **GuardDuty findings:** review
- **CloudTrail:** export + analyze
- **S3 versioning + MFA delete**
- **Containment:** isolate VPC, suspend instance
- **Forensic snapshot:** EBS snapshot before terminate

### Azure
- **Disable principal:** Entra ID
- **Defender for Cloud:** alerts
- **Activity log:** export
- **Sentinel:** incidents
- **Containment:** NSG, snapshot VM

### GCP
- **Disable service account:** keys
- **Cloud Audit Logs**
- **Security Command Center**
- **Forensic disk:** Compute Engine snapshot

## Templates
1. Multi-cloud IR playbook
2. AWS account compromise SOP
3. Container forensics (Falco + Tracee)
4. Kubernetes incident workflow
5. Cloud-native log preservation
6. CSP escalation contacts

## Cross-references
- [[aegis-cloud-security]] · [[aegis-incident-response]] · [[aegis-digital-forensics]]
