---
name: medik-emr-integration
description: EMR/EHR integration — HL7 FHIR R4, OpenEHR, CDA, RNDS. Tasy, Soul MV, Vidalink. Triggers em "EMR", "EHR", "HL7 FHIR", "OpenEHR", "RNDS", "Tasy", "Soul MV", "prontuário eletrônico".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [lgpd_healthcare_marker, cfm_205_2021_gate, audit_cfm]
jurisdiction: Brasil
---

# MEDIK-EMR-INTEGRATION

## Quando usar
- Greenfield EMR selection (hospital/clínica)
- Integração entre sistemas (Lab → EMR → Faturamento)
- RNDS (Rede Nacional Dados em Saúde) compliance
- Migration entre EMRs
- FHIR-first architecture

## Stack BR
- **Tasy (Philips)** — líder hospitalar
- **Soul MV** — público + privado
- **Vidalink** — Operadoras
- **iClinic** — consultório
- **Doctoralia EMR** — médicos individuais
- **OpenEHR-based:** Better, EHRBase

## Padrões
- **HL7 FHIR R4** — REST API healthcare interop (standard)
- **HL7 v2** — legacy messaging (ainda em uso)
- **OpenEHR** — archetype-based, semantics rich
- **CDA R2** — documentos clínicos estruturados
- **DICOM** — imagens médicas
- **RNDS** — Min. Saúde nacional, FHIR-based

## Templates
1. EMR selection scorecard (clinical + technical + financial)
2. FHIR R4 resource design (Patient, Encounter, Observation, Procedure)
3. Integration architecture (HL7 v2 → FHIR mapping)
4. RNDS publication setup (LACEN, vacinação)
5. EHR migration playbook (Tasy → Cloud-native)

## Cross-references
- [[medik-lgpd-healthcare]] · [[medik-clinical-decision-support]] · [[obsidian-ontology-modeling]]
