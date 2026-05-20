---
name: helios-aneel-compliance
description: ANEEL compliance — REN, deveres consumidores, geração distribuída, regulação. Triggers em "ANEEL", "REN", "geração distribuída", "ANEEL compliance", "Resolução Normativa", "PRODIST".
license: SEE-LICENSE
parent_agent: helios-director
compliance: [aneel_compliance_gate, audit_immutable]
jurisdiction: Brasil
---

# HELIOS-ANEEL-COMPLIANCE

## Marco
- **Lei 9.427/1996** — ANEEL criação
- **REN 1000/2021** — geração distribuída
- **REN 414/2010** — condições gerais fornecimento
- **PRODIST** — Procedimentos Distribuição (módulos 1-11)
- **PROREDE** — Procedimentos Rede

## Quando usar
- Greenfield projeto GD (≤ 5 MW)
- Cadastro ANEEL como agente
- Resposta a notificação ANEEL
- Tarifa social, baixa renda compliance
- Modicidade tarifária
- Bandeira tarifária (verde/amarela/vermelha)

## Tipos consumidor (regulado)
- Grupo A: alta tensão (industrial)
- Grupo B: baixa tensão (residencial, comercial pequeno)
- Subgrupos por demanda + classe

## REN 1000 GD compliance
- **Microgeração:** ≤ 75 kW
- **Minigeração:** 75 kW - 5 MW
- **SCEE (Sistema Compensação):** créditos energia injetada
- **Transição Lei 14.300:** subsídios decrescentes 2023-2028

## Templates
1. Cadastro ANEEL agente
2. Projeto GD parecer técnico distribuidora
3. SCEE compensação tracker
4. PRODIST compliance checklist
5. Bandeira tarifária impact analysis
6. Subsídio cruzado análise

## Cross-references
- [[helios-mercado-livre-br]] · [[helios-grid-integration]] · [[helios-utility-rate-design]]
