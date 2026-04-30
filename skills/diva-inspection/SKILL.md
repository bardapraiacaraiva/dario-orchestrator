---
name: diva-inspection
description: Construction inspection checklist by phase. Covers foundation through final handover with specific check items, tolerances, photos required, and sign-off criteria. Includes punch list / snag list template. Triggers on "inspeccao", "inspection", "fiscalizacao", "controlo qualidade", "vistoria", "recepcao obra", "punch list", "snag list".
license: MIT
---

# DIVA Skill — Construction Inspection Checklist

Phase-by-phase quality control checklist for construction and renovation projects in Portugal. Each phase has specific inspection items, acceptable tolerances (per Portuguese and European norms), required photographic documentation, and sign-off criteria. Includes a comprehensive punch list (lista de remates) template for final inspection before handover.

## When to activate

- Scheduled site visit / inspection at any construction phase
- Client asks "como sei se o trabalho esta bem feito?"
- Preparing for camara municipal vistoria (autorizacao de utilizacao)
- Contractor disputes about quality of work
- Final walkthrough before handover (auto de recepcao)
- Creating a punch list / snag list
- Fiscalizacao (construction supervision) reporting

## Workflow

### 1. Gather inputs

- **Project:** name and reference
- **Phase to inspect:** which construction phase(s) to check
- **Inspection type:** routine / milestone / final / complaint-driven
- **Who inspects:** architect / engineer / fiscalizacao / client / all
- **Previous inspection findings:** any open items from last visit?
- **Applicable specs:** project caderno de encargos, material specifications
- **Weather conditions:** relevant for exterior work inspection

If phase is missing, ask. If "all phases" or "final inspection", generate complete checklist.

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "construction inspection quality control checklist tolerances", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "punch list snag list recepcao obra vistoria Portugal", collection: "dario", limit: 5)
```

### 3. Phase-specific checklists

---

#### Phase 1: Fundacoes (Foundation)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 1.1 | Escavacao conforme projecto | Profundidade +/- 5cm vs projecto | [ ] | Req |
| 1.2 | Solo de fundacao | Capacidade carga conforme estudo geotecnico | [ ] | Req |
| 1.3 | Cofragem | Alinhamento +/- 10mm, estanquidade | [ ] | Req |
| 1.4 | Armadura (ferro) | Diametros e espacamento conforme projecto, recobrimento min 4cm | [ ] | Req |
| 1.5 | Betonagem | Classe de betao conforme projecto (ex: C25/30), vibrado correctamente | [ ] | Req |
| 1.6 | Cura do betao | Min 7 dias cura humida, sem fissuras | [ ] | Req |
| 1.7 | Impermeabilizacao fundacoes | Membrana aplicada sem descontinuidades | [ ] | Req |
| 1.8 | Drenagem perimetral | Tubo drenante instalado, geotextil, brita | [ ] | Req |

**Sign-off:** Engenheiro de estruturas assina antes de aterro.

---

#### Phase 2: Estrutura (Structure)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 2.1 | Pilares - verticalidade | Desvio max 10mm por piso (EN 13670) | [ ] | Req |
| 2.2 | Vigas - nivelamento | Desvio max L/500 (L = vao) | [ ] | Req |
| 2.3 | Lajes - espessura | +/- 5mm vs projecto | [ ] | Req |
| 2.4 | Lajes - nivelamento | Desvio max 10mm em 2m (regua) | [ ] | Req |
| 2.5 | Armaduras pre-betonagem | Conformidade com projecto, recobrimento, amarracoes | [ ] | Req |
| 2.6 | Betonagem | Sem segregacao, vibrado, juntas de betonagem tratadas | [ ] | Req |
| 2.7 | Cura | Sem fissuras > 0.3mm (classe exposicao dependente) | [ ] | Req |
| 2.8 | Negativos e passagens | Aberturas para MEP conforme planta de furacoes | [ ] | Req |
| 2.9 | Ensaios betao | Cubos de ensaio (min 3 por betonagem), resultados 28 dias | [ ] | -- |

**Sign-off:** Engenheiro de estruturas, ensaios de betao aprovados.

---

#### Phase 3: Impermeabilizacao e Isolamento (Waterproofing & Insulation)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 3.1 | Cobertura - impermeabilizacao | Membrana sem bolhas, sobreposicoes min 10cm, remates em platibandas | [ ] | Req |
| 3.2 | WC - impermeabilizacao | Membrana/tela em paredes (min 20cm acima chuveiro/banheira) e pavimento | [ ] | Req |
| 3.3 | Teste estanquidade WC | Inundacao 48h, sem infiltracoes no piso inferior | [ ] | Req |
| 3.4 | Isolamento termico paredes | Espessura conforme REH, sem pontes termicas, continuidade | [ ] | Req |
| 3.5 | Isolamento termico cobertura | Espessura conforme REH, barreira de vapor correcta | [ ] | Req |
| 3.6 | Isolamento acustico | Conforme RRAE, laje flutuante sem contacto paredes (banda resiliente) | [ ] | Req |
| 3.7 | Caixilharia - vedacao | Silicone/EPDM em todo perimetro, sem folgas | [ ] | Req |
| 3.8 | Pontes termicas | Correcao em pilares, vigas, caixas de estore | [ ] | Req |

**Sign-off:** Engenheiro termico / fiscalizacao. Teste WC obrigatorio antes de revestimento.

---

#### Phase 4: MEP Rough-In (Canalizacoes, Electricidade, AVAC)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 4.1 | Agua - tubagem | Diametros conforme projecto, isolamento agua quente, sem cruzamentos com esgoto | [ ] | Req |
| 4.2 | Agua - teste pressao | 10 bar durante 2h, sem queda de pressao | [ ] | Req |
| 4.3 | Esgoto - inclinacao | Min 1-2% (verificar com nivel) | [ ] | Req |
| 4.4 | Esgoto - teste estanquidade | Agua sem fugas em todas as juncoes | [ ] | Req |
| 4.5 | Electricidade - tubagem | Caminhos conforme projecto ITED, separacao potencia/dados | [ ] | Req |
| 4.6 | Electricidade - caixas | Posicao e altura conforme projecto (interruptores 1.1m, tomadas 0.3m) | [ ] | Req |
| 4.7 | Quadro electrico | Espaco suficiente, acessivel, conforme RTIEBT | [ ] | Req |
| 4.8 | AVAC - condutas | Dimensoes conforme projecto, isolamento, suspensoes | [ ] | Req |
| 4.9 | AVAC - unidades exteriores | Posicao conforme projecto, suportes anti-vibrateis | [ ] | Req |
| 4.10 | Gas (se aplicavel) | Tubagem cobre/aco, ventilacao conforme regulamento gas | [ ] | Req |
| 4.11 | Telecomunicacoes ITED | ATI instalado, tubagem dados conforme projecto ITED | [ ] | Req |
| 4.12 | Piso radiante (se aplicavel) | Circuitos conforme projecto, teste pressao, isolamento base | [ ] | Req |

**Sign-off:** Engenheiros MEP respectivos. TODOS os testes de pressao antes de fechar paredes.

---

#### Phase 5: Paredes e Tectos (Drywall / Alvenaria finalizada)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 5.1 | Planeza paredes | Desvio max 3mm em 2m (regua) | [ ] | Req |
| 5.2 | Verticalidade paredes | Desvio max 3mm em 2.5m (fio-de-prumo) | [ ] | Req |
| 5.3 | Esquadria (angulos 90) | Desvio max 2mm em 1m | [ ] | -- |
| 5.4 | Gesso cartonado | Juntas tratadas sem fissuras, parafusos embebidos | [ ] | -- |
| 5.5 | Reforcos para fixacoes | Reforcos em madeira/OSB para sanitarios, TV, armarios | [ ] | Req |
| 5.6 | Tectos falsos | Nivelamento +/- 2mm, estrutura conforme fabricante | [ ] | -- |
| 5.7 | Aberturas portas/janelas | Dimensoes conforme mapa de vaos, esquadria | [ ] | -- |

**Sign-off:** Fiscalizacao / arquitecto. Verificar ANTES de revestimentos.

---

#### Phase 6: Acabamentos (Revestimentos, Pinturas)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 6.1 | Pavimento ceramico | Planeza 2mm/2m, juntas uniformes, sem pecas ocas (teste batimento) | [ ] | Req |
| 6.2 | Pavimento madeira | Planeza 2mm/2m, juntas uniformes, sem rangidos | [ ] | -- |
| 6.3 | Revestimento paredes | Aderencia, alinhamento, sem fissuras, cantos protegidos | [ ] | -- |
| 6.4 | Pintura | Cobertura uniforme, sem escorridos, sem marcas rolo, 2-3 demaos | [ ] | -- |
| 6.5 | Rodape | Alinhamento, juntas de canto a 45, fixacao firme | [ ] | -- |
| 6.6 | Soleiras e peitoris | Inclinacao exterior, pingadeira, vedacao | [ ] | -- |
| 6.7 | Azulejo WC/cozinha | Alinhamento, planeza, juntas uniformes, vedacao silicone em cantos | [ ] | Req |
| 6.8 | Microcimento (se aplicavel) | Sem fissuras, espessura uniforme, impermeabilizado | [ ] | -- |
| 6.9 | Transicoes pavimento | Perfis de transicao correctos, sem desniveis > 2mm | [ ] | -- |

**Sign-off:** Arquitecto / designer de interiores.

---

#### Phase 7: Carpintaria (Portas, Armarios, Cozinha)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 7.1 | Portas - funcionamento | Abertura/fecho suave, sem rocar, fechadura funcional | [ ] | -- |
| 7.2 | Portas - acabamento | Sem riscos, pintura/folheado uniforme, borrachas vedacao | [ ] | -- |
| 7.3 | Portas - folga | 2-3mm lateral, 8-10mm inferior (5mm com tapete) | [ ] | -- |
| 7.4 | Armarios roupeiros | Portas alinhadas, gavetas deslizam suave, interiores conforme desenho | [ ] | Req |
| 7.5 | Cozinha - modulos | Nivelamento, portas alinhadas, gavetas soft-close | [ ] | Req |
| 7.6 | Cozinha - bancada | Planeza, juntas impermeabilizadas, cortes perfeitos (placa, lava-loica) | [ ] | Req |
| 7.7 | Cozinha - electrodomesticos | Encastre correcto, funcionamento, garantias | [ ] | -- |
| 7.8 | WC - movel | Nivelamento, fixacao segura, vedacao agua | [ ] | -- |

**Sign-off:** Arquitecto / designer de interiores + cliente.

---

#### Phase 8: Equipamentos (Sanitarios, Iluminacao, Outros)

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 8.1 | Sanitarios - fixacao | Solidos, sem folga, vedacao silicone | [ ] | -- |
| 8.2 | Torneiras - funcionamento | Quente/frio correctos, caudal adequado, sem fugas | [ ] | -- |
| 8.3 | Base duche/banheira | Nivelamento, escoamento rapido (< 30seg), vedacao | [ ] | -- |
| 8.4 | Iluminacao - funcionamento | Todos os pontos funcionam, intensidade correcta, sem flicker | [ ] | -- |
| 8.5 | Interruptores e tomadas | Funcionamento, nivelamento, acabamento conforme especificacao | [ ] | -- |
| 8.6 | Quadro electrico | Disjuntores identificados, diferencial funcional (teste botao) | [ ] | Req |
| 8.7 | Videoporteiro / intercomunicador | Imagem, som, abertura porta | [ ] | -- |
| 8.8 | Aquecimento / AC | Funcionamento todos os modos, termostato calibrado | [ ] | -- |
| 8.9 | Ventilacao | Extraccao WC/cozinha funcional, caudais adequados | [ ] | -- |
| 8.10 | Estores / blackouts | Subida/descida suave, vedacao luz, motorizado (se aplicavel) | [ ] | -- |

**Sign-off:** Engenheiro electrotecnico (quadro) + arquitecto (restante).

---

#### Phase 9: Inspeccao Final / Vistoria

| # | Item | Criteria / Tolerance | Check | Photos |
|---|---|---|---|---|
| 9.1 | Limpeza geral | Obra limpa, sem residuos, vidros limpos | [ ] | Req |
| 9.2 | Teste geral agua | Todas torneiras, autoclismo, chuveiro, maquina lavar | [ ] | -- |
| 9.3 | Teste geral electricidade | Todos circuitos, todas tomadas (testador), diferenciais | [ ] | -- |
| 9.4 | Teste portas e janelas | Todas abrem/fecham, trancam, vedacao | [ ] | -- |
| 9.5 | Teste aquecimento/AC | Todos os espacos, termostatos | [ ] | -- |
| 9.6 | Verificacao visual completa | Walkthrough sistematico divisao a divisao | [ ] | Req |
| 9.7 | Medicao areas | Conformidade com projecto aprovado | [ ] | -- |
| 9.8 | Documentacao obra | Telas finais, manuais equipamentos, garantias, certificados | [ ] | -- |
| 9.9 | Certificado energetico | SCE emitido por perito ADENE | [ ] | -- |
| 9.10 | Ficha tecnica da habitacao (FTH) | Completa e assinada | [ ] | -- |

**Sign-off:** Arquitecto + dono de obra. Gera lista de remates (punch list).

### 4. Generate punch list (lista de remates)

After final inspection, compile all defects found:

**Severity levels:**
- **A - Critico:** Safety issue or non-compliance with regulations. Must fix before handover.
- **B - Importante:** Functional defect affecting use. Must fix before handover.
- **C - Menor:** Aesthetic defect. Fix within 30 days of handover.
- **D - Observacao:** Minor observation. Fix at next maintenance.

### 5. Handover documentation package

Verify client receives:
- [ ] Telas finais (as-built drawings) - arquitectura + especialidades
- [ ] Manuais de todos os equipamentos
- [ ] Garantias (empreiteiro: 5 anos estrutura, 3 anos equipamentos, 1 ano acabamentos)
- [ ] Certificados de conformidade (materiais, equipamentos)
- [ ] Certificado energetico (SCE)
- [ ] Ficha tecnica da habitacao (FTH)
- [ ] Auto de recepcao provisoria (assinado por ambas partes)
- [ ] Lista de remates pendentes com prazos
- [ ] Chaves (todas as copias)
- [ ] Codigos e passwords (alarme, domotic, WiFi)
- [ ] Contactos de manutencao (canalizador, electricista, AVAC)

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: inspection-report
phase: <phase inspected>
inspector: <name and role>
result: <aprovado / aprovado com reservas / reprovado>
---

# Relatorio de Inspeccao -- <Project Name>

## Dados gerais
- **Obra:** <project name and address>
- **Fase:** <phase>
- **Data inspeccao:** <date>
- **Condicoes meteorologicas:** <weather>
- **Inspector:** <name, role>
- **Presentes:** <list of people on site>

## Resultado global
**<APROVADO / APROVADO COM RESERVAS / REPROVADO>**

## Checklist de inspeccao
[Insert relevant phase checklist with items checked]

## Nao-conformidades encontradas

| # | Divisao | Item | Descricao | Severidade | Foto ref | Prazo correcao |
|---|---|---|---|---|---|---|
| NC-001 | <room> | <item ref> | <description> | A/B/C/D | IMG_001 | <date> |
| NC-002 | ... | ... | ... | ... | ... | ... |

## Registo fotografico
| Ref | Descricao | Localizacao |
|---|---|---|
| IMG_001 | <description> | <room/area> |
| IMG_002 | ... | ... |

## Punch List (se inspeccao final)

| # | Divisao | Descricao defeito | Severidade | Responsavel | Prazo | Status |
|---|---|---|---|---|---|---|
| PL-001 | Sala | Fissura pintura junto a janela | C | Pintor | 30 dias | Pendente |
| PL-002 | WC Suite | Torneira lavatoro pinga | B | Canalizador | Pre-entrega | Pendente |
| ... | ... | ... | ... | ... | ... | ... |

**Total: <N> items | A: <N> | B: <N> | C: <N> | D: <N>**

## Proxima inspeccao
- **Data prevista:** <date>
- **Fase:** <next phase>
- **Items a verificar:** <open items from this inspection>

## Assinaturas
- Inspector: _________________________ Data: ___________
- Empreiteiro: _________________________ Data: ___________
- Dono de obra: _________________________ Data: ___________
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Inspeccao <Phase>.md`

## Red Flags
- Never skip photo documentation at every inspection phase — no photo means no proof, and in Portuguese construction disputes the burden of evidence falls on whoever cannot demonstrate the defect existed before wall closure
- Never approve any phase without the full checklist completed and signed — partial approvals create liability gaps and contractors will claim tacit acceptance for unchecked items
- Always test concealed systems before covering (pressure test plumbing at 10 bar for 2h, test every electrical circuit with socket tester, flood-test WC waterproofing for 48h) — once walls and pavements close, remediation costs 5-10x the original work
- Never sign off structural elements without an engineer's written approval (termo de responsabilidade) — the arquitecto's insurance does not cover structural failures, and DL 67/2003 holds the dono de obra liable for 10 years
- Never accept "vou corrigir depois" for severity A or B items — in the Portuguese market these verbal promises are systematically forgotten, and leverage disappears once final payment is made
- Always insist on a dated photo record with location reference for every non-conformity — Portuguese tribunal proceedings require documentary evidence, and phone photos with metadata are legally admissible

## Interactions

- Pair with `diva-timeline` for scheduling inspections at milestone gates
- Pair with `diva-licensing` for preparing the autorizacao de utilizacao vistoria
- Follow up with `dario-obsidian-save` to archive inspection reports
- Save via `dario-obsidian-save` to vault
