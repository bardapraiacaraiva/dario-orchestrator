---
name: sphinx-mobile-forensics
description: Mobile forensics — iOS/Android extraction, Cellebrite, Magnet AXIOM, Oxygen Forensic. Triggers em "mobile forensics", "iOS forensics", "Android forensics", "Cellebrite UFED", "Magnet AXIOM", "Oxygen Forensic", "GrayKey".
license: SEE-LICENSE
parent_agent: sphinx-director
compliance: [audit_immutable, classified_handling, responsible_disclosure]
---

# SPHINX-MOBILE-FORENSICS

## Extraction levels
- **Manual:** photo of screen
- **Logical:** file system via vendor protocol (iTunes-like)
- **File system:** root/jailbreak access
- **Physical:** bit-by-bit copy (chip-off, JTAG)
- **Cloud:** iCloud/Google Drive backups

## Stack
- **Cellebrite UFED** — líder LE/government
- **Magnet AXIOM** — competitive
- **Oxygen Forensic Detective** — cost-effective
- **GrayKey (Grayshift):** iOS specific unlock
- **MOBILedit Forensic** — affordable

## iOS challenges
- Secure Enclave + Touch ID/Face ID
- iOS 17/18 lockdown mode
- iCloud encrypted backups
- Recovery vs forensic data

## Android challenges
- Manufacturer variations (Samsung, Xiaomi)
- TrustZone (ARM)
- KeyMaster (hardware-backed crypto)
- File-based encryption (FBE)
- Verified boot

## Templates
1. Forensic acquisition SOP
2. Chain of custody mobile
3. iOS extraction workflow
4. Android extraction workflow
5. Report court-admissible
6. Anti-forensics detection

## Cross-references
- [[aegis-digital-forensics]] · [[sphinx-malware-analysis]] · [[lex-criminal]]
