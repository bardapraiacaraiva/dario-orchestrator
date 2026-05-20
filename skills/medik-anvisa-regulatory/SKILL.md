---
name: medik-anvisa-regulatory
description: ANVISA — RDC, registro de dispositivos médicos, biotech, cosméticos, alimentos funcionais. Triggers em "ANVISA", "RDC", "registro dispositivo médico", "biotech regulatório", "vigilância sanitária".
license: SEE-LICENSE
parent_agent: medik-director
compliance: [anvisa_regulatory, audit_trail]
jurisdiction: Brasil
---

# MEDIK-ANVISA-REGULATORY

## Quando usar
- Registro de dispositivo médico Classe I/II/III/IV
- Fabricante/importador setup (CBPF)
- Pós-comercialização (farmacovigilância)
- Notificações de eventos adversos
- Inspeções ANVISA

## Marco regulatório
- **Lei 6.360/1976** — Vigilância sanitária
- **RDC 16/2013** — Boas Práticas de Fabricação dispositivos
- **RDC 185/2001** — Notificação evento adverso
- **RDC 27/2011** — Cosméticos
- **RDC 751/2022** — Software como dispositivo médico (SaMD)
- **IN 81/2020** — Inteligência artificial em saúde

## Classes risco dispositivos médicos
- Classe I (baixo): notificação simples
- Classe II (médio): cadastro
- Classe III (alto): registro + estudos clínicos
- Classe IV (máximo): registro + ensaios + dossiê

## Templates
1. Dossiê de registro Classe II/III
2. Risk Management File (ISO 14971)
3. Pós-mercado vigilância plan
4. SaMD documentation (FDA + ANVISA alignment)
5. Inspection readiness checklist

## Cross-references
- [[medik-clinical-protocols]] · [[lex-regulatorio]] · [[risco-iso27001]]
