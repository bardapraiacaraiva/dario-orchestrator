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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Fase de obra identificada e checklist correspondente gerada

- [ ] A fase inspeccionada está explicitamente nomeada (Fundações / Estrutura / Impermeabilização / MEP / Final)
- [ ] A checklist gerada é a da fase correcta — não uma checklist genérica
- [ ] Se "final inspection", todas as fases relevantes estão incluídas com punch list
- [ ] Itens inaplicáveis à fase estão omitidos ou marcados N/A com justificação

❌ NOT delivery-ready: "Verifique a qualidade da obra conforme as normas aplicáveis."
✅ Delivery-ready: "Fase 2 — Estrutura | Item 2.1 Pilares: desvio medido 7mm/piso (máx. EN 13670: 10mm) ✅ | Item 2.4 Lajes: desvio 14mm em 2m ❌ REPROVADO"

---

### Gate 2 — Tolerâncias e normas citadas com valores concretos

- [ ] Cada item crítico inclui o valor de tolerância numérico (ex: ±5mm, L/500, min 4cm)
- [ ] A norma ou regulamento fonte está identificado (EN 13670, REH, RRAE, RTIEBT, RGEU)
- [ ] Desvios encontrados são comparados directamente à tolerância ("medido: X | limite: Y")
- [ ] Ensaios obrigatórios (betão 28 dias, pressão 10 bar/2h, inundação 48h) têm resultado registado

❌ NOT delivery-ready: "Verificar se a armadura está correcta conforme o projecto."
✅ Delivery-ready: "Item 1.4 Armadura: recobrimento medido 3.2cm — REPROVADO (mínimo 4cm per projecto). Foto REF-ARM-003."

---

### Gate 3 — Sign-off e responsáveis identificados por fase

- [ ] Cada fase tem o responsável de aprovação nomeado (engenheiro estruturas, fiscalização, etc.)
- [ ] Data da inspecção está registada no output
- [ ] Itens em aberto da vistoria anterior (se fornecidos) estão referenciados como "carry-over"
- [ ] Pré-condição bloqueante indicada quando aplicável (ex: "Teste WC obrigatório ANTES de revestimento")

❌ NOT delivery-ready: "Assinar quando estiver tudo conforme."
✅ Delivery-ready: "Sign-off: Eng. Rui Faria (estruturas) — Data prevista: 2025-03-14 | BLOQUEANTE: ensaios betão C25/30 (cubos 28 dias) pendentes → betonagem laje P2 não autorizada"

---

### Gate 4 — Documentação fotográfica especificada por item

- [ ] Cada item marcado "Req" tem referência fotográfica (código ou placeholder estruturado)
- [ ] Fotos de itens reprovados estão explicitamente indicadas como obrigatórias
- [ ] Se inspecção já realizada, o número real de fotos tiradas está registado
- [ ] Ângulos/detalhes críticos sugeridos onde a foto genérica é insuficiente (ex: "foto regua sobre laje, 2m visível")

❌ NOT delivery-ready: "Tirar fotos da obra."
✅ Delivery-ready: "Item 3.3 Teste estanquidade WC Suite Master: foto ANTES enchimento (REF-WC-001), DURANTE 48h (REF-WC-002), resultado piso inferior sem mancha (REF-WC-003) ✅"

---

### Gate 5 — Punch list com estados RAG e prazo de resolução

- [ ] Cada não-conformidade tem estado: 🔴 Crítico (bloqueia fase) / 🟡 Maior (resolver antes handover) / 🟢 Menor (remate)
- [ ] Data-limite de resolução atribuída a cada item em aberto
- [ ] Responsável pela correcção identificado (empreiteiro geral / subcontratado / fornecedor)
- [ ] Critério de re-inspecção definido ("reinspeção em 5 dias úteis, Eng. X valida no local")

❌ NOT delivery-ready: "Lista de remates: reparar pintura, verificar tomada, ajustar porta."
✅ Delivery-ready: "PL-007 🟡 Porta WC serviço: folga superior 6mm (máx. 3mm, NP EN 1121) | Resp: Carpintaria Sousa | Prazo: 2025-04-02 | Re-inspecção: Arq. Marta Dias in loco"

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets

- [ ] Nome do projecto real substituiu `<nome do projecto>` ou similar
- [ ] Referências a morada/lote/fracção estão preenchidas
- [ ] Datas concretas (inspecção, sign-off, prazo punch list) substituíram placeholders
- [ ] Engenheiros/fiscalização nomeados com nome real ou "A definir" explícito — nunca `<engenheiro>`

❌ NOT delivery-ready: "Projecto: `<inserir projecto>` | Inspector: `<nome>` | Data: `<data>`"
✅ Delivery-ready: "Projecto: Cuidai HQ — Remodelação Piso 2, Rua Actor Isidoro 8, Lisboa | Inspector: Arq. Sofia Monteiro | Inspecção: 2025-03-11"

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmed from prior session/memory/cliente data
- 🟡 **assumed** — plausible but needs cliente confirm pre-delivery
- 🟢 **projection** — forecast by design (not verifiable)

Output checklist upfront mostra reader exactly o que é trust-as-is vs precisa verify. **Honest transparency > inflated delivery.**

❌ NOT delivery-ready:
> "Recobrimento mínimo: 4cm. Betão classe C25/30. Teste de estanquidade: 48h. Membrana com sobreposições de 10cm."
> *(Reader assume que todos os valores são do projecto real do cliente — podem ser defaults normativos, não os especificados no caderno de encargos)*

✅ Delivery-ready:
> - 🔵 **verified** — Recobrimento mínimo 4cm (EN 1992-1-1, confirmado em sessão anterior com eng. estruturas)
> - 🟡 **assumed** — Classe de betão C25/30 (típico para fundações residenciais PT; confirmar caderno de encargos antes da betonagem)
> - 🟢 **projection** — Ensaios de betão aos 28 dias aprovados (resultado esperado se execução conforme; verificar quando disponíveis)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir defaults normativos pelos valores reais do caderno de encargos / projecto de execução do cliente
- [ ] All 🔵 citations added — referenciar norma (EN, LNEC, REH, RRAE) ou documento de projecto fonte para cada tolerância indicada
- [ ] All 🟢 projections labeled as such ao cliente — deixar claro que resultados de ensaios, testes de estanquidade e conformidade final são projecções até execução e medição real em obra

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# Relatório de Inspecção — Atrium Reabilitação Edifício Pombalino
**Projecto:** ATR-2025-04 | Rua do Ouro 112, Lisboa | Fracção: Pisos 1-3
**Tipo:** Milestone — Fase MEP Rough-In (Fase 4)
**Inspector:** Eng. Paulo Guerreiro (fiscalização) + Arq. Inês Tavares
**Data inspecção:** 2025-03-11 | **Hora:** 09h30
**Inspecção anterior:** 2025-02-18 | Items carry-over: 2 (ver §Carry-Over)

---

## Fase 4 — MEP Rough-In: Canalizações, Electricidade, AVAC

| # | Item | Critério / Tolerância | Medido / Observado | Estado | Fotos |
|---|---|---|---|---|---|
| 4.1 | Água — tubagem | Ø conforme projecto, isolamento AQ, sem cruzamentos esgoto | Ø22mm AQ ✅ Isolamento 9mm ✅ Sem cruzamentos ✅ | ✅ | ATR-MEP-001/002 |
| 4.2 | Água — teste pressão | 10 bar durante 2h, queda <0.1 bar | 10 bar → 9.94 bar (2h) ✅ | ✅ | ATR-MEP-003 |
| 4.3 | Esgoto — inclinação | Mín. 1% (verificado com nível digital) | WC Piso 1: 1.8% ✅ Cozinha: 0.7% ❌ | ❌ | ATR-MEP-004/005 |
| 4.4 | Esgoto — estanquidade | Sem fugas em junções após carga 2h | 1 fuga detected junção PVC Piso 2 WC | ❌ | ATR-MEP-006 |
| 4.5 | Elect. — tubagem ITED | Caminhos conf. projecto, sep. potência/dados mín 30cm | Separação 28cm troço corredor Piso 2 | 🟡 | ATR-MEP-007 |
| 4.6 | Elect. — caixas | Interruptores 1.10m, tomadas 0.30m (±10mm) | Interruptores: 1.08–1.12m ✅ Tomadas: OK ✅ | ✅ | ATR-MEP-008 |
| 4.7 | Quadro eléctrico | Acessível, espaço suficiente, conf. RTIEBT Art.º 412 | Localização OK, espaço 20% livre ✅ | ✅ | ATR-MEP-009 |
| 4.8 | AVAC — condutas | Dimensões conf. projecto, isolamento, suspensões máx. 1.5m | Suspensões: 1.8m troço Piso 3 ❌ | ❌ | ATR-MEP-010 |
| 4.9 | AVAC — unidades ext. | Suportes anti-vibráticos, posição conf. projecto | Instalação pendente (programada 2025-03-18) | ⏳ | — |

---

## Punch List — Items em Aberto

| ID | Descrição | Severidade | Responsável | Prazo | Re-inspecção |
|---|---|---|---|---|---|
| PL-ATR-009 | Esgoto cozinha Piso 1: inclinação 0.7% (mín. 1%) — rectificar percurso | 🔴 Crítico | Canalizações Ferreira Lda | 2025-03-17 | Eng. Guerreiro in loco |
| PL-ATR-010 | Fuga junção PVC Piso 2 WC — substituir luva, repetir teste 10 bar/2h | 🔴 Crítico | Canalizações Ferreira Lda | 2025-03-17 | Teste documentado foto |
| PL-ATR-011 | Separação potência/dados 28cm (mín. 30cm) — troço corredor Piso 2 | 🟡 Maior | Electro-Tejo SA | 2025-03-21 | Medição no local |
| PL-ATR-012 | Suspensões AVAC Piso 3: vão 1.8m (máx. 1.5m) — adicionar fixação | 🟡 Maior | ClimaTec Norte | 2025-03-21 | Eng. Guerreiro in loco |

---

## Carry-Over da Inspecção Anterior (2025-02-18)

| ID | Item | Estado actual |
|---|---|---|
| PL-ATR-007 | Recobrimento armadura laje Piso 2: 3.6cm (mín. 4cm) | ✅ RESOLVIDO — foto ATR-EST-044 |
| PL-ATR-008 | Ensaios betão C25/30 Piso 2 pendentes | ✅ RESOLVIDO — resultados 28 dias: 27.4 MPa (OK) |

---

## Sign-Off

**FASE 4 — STATUS: 🔴 NÃO APROVADA**
Condição de progressão: PL-ATR-009 e PL-ATR-010 resolvidos e validados.
Próxima inspecção agendada: **2025-03-18, 10h00**
Assinatura fiscalização: Eng. Paulo Guerreiro ________________
```

---

## Output anti-patterns

- Checklist gerada sem fase identificada — itens de fundações misturados com MEP numa lista indiferenciada
- Tolerâncias escritas em prosa vaga ("verificar se está nivelado") sem valor numérico nem norma fonte
- Punch list sem severidade RAG — cliente não sabe o que bloqueia progressão da obra
- Sign-off "a assinar quando concluído" sem responsável nomeado nem data concreta
- Fotos listadas como "tirar fotos" sem código de referência por item — impossível rastrear em obra
- Teste de estanquidade WC ou pressão de água marcado ✅ sem registar valores medidos (pressão inicial, pressão final, duração)
- Carry-over de inspecção anterior ignorado — itens em aberto desaparecem do relatório seguinte sem resolução documentada
- Output entregue com `<nome do projecto>`, `<engenheiro>`, `<data>` por preencher — placeholders visíveis ao cliente
