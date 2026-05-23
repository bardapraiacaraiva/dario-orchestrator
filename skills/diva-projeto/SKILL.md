---
name: diva-projeto
description: Project context switcher for architecture/design/construction projects — loads all memory, RAG context, and audit history for a specific DIVA project. Displays project summary, last decisions, pending items, budget status, timeline status. Triggers on "projeto", "projecto", "switch project", "mudar projeto", "contexto do", "carrega projeto", "projeto DIVA".
license: MIT
---

# DIVA Skill — Project Context Switcher (Architecture/Design/Construction)

Loads the complete context for a specific architecture, design, or construction project in one command. Searches agent-memory, DIVA RAG collection, and Obsidian vault to assemble a comprehensive project briefing. Specialized for building projects with budget tracking, timeline phases, regulatory status, and technical decisions.

## When to activate

- User says "projeto DIVA Vila Cascais" or "projecto Moradia Sintra"
- User switches between architecture projects mid-session
- Start of session when user wants to resume work on a building project
- Before any DIVA skill execution for a specific project
- User asks "onde estamos com o projeto X?"
- User says "contexto do projeto" or "carrega projeto"

Do NOT use for:
- Non-architecture projects (websites, SaaS, marketing) — use `dario-projeto` instead
- Creating a new project from scratch (use project brief workflow instead)
- Generic architecture questions without a specific project

## Workflow

### 1. Identify the project

Match user input against known projects. Search in this order:

**a) Agent-memory files:**
Search `~/.claude/agent-memory/` and `~/.claude/plugins/` for project files:
```
Glob(pattern: "**/project_*.md", path: "C:/Users/barda/.claude")
Glob(pattern: "**/MEMORY.md", path: "C:/Users/barda/.claude")
```

Look for DIVA/architecture project entries containing:
- Building type (moradia, apartamento, edificio, loja, escritorio)
- Location references (Portuguese cities, addresses)
- Architecture terms (projeto, obra, remodelacao, construcao)

**b) RAG search:**
```
mcp__dario-rag__search_kb(query: "<project name>", collection: "diva", limit: 10)
```

**c) Obsidian vault:**
```
Glob(pattern: "**/*<project>*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/05 - Claude - IA")
Glob(pattern: "**/*<project>*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/01 - Projetos")
```

If no exact match found, list available DIVA projects and ask user to clarify.

### 2. Load project memory

Read the matching project file(s) and extract:
- **Project name and type** (new build, renovation, interiors, mixed)
- **Client name and contacts**
- **Location** (address, municipality, parish)
- **Building type** (moradia, apartamento, edificio comercial, etc.)
- **Area** (gross, net, plot)
- **Current phase** (programa, estudo previo, projeto base, projeto execucao, obra, conclusao)
- **Stack/team** (architect, engineers, contractor, subcontractors)
- **Budget** (approved, spent, remaining, contingency)
- **Timeline** (milestones, current phase dates, delays)
- **Regulatory status** (licenciamento, PIP, comunicacao previa, alvara)
- **Pending items and blockers**

### 3. Load technical decisions history

Search for decision records:
```
Glob(pattern: "**/*<project>*Decisao*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/05 - Claude - IA/Decisoes")
```

And in RAG:
```
mcp__dario-rag__search_kb(query: "<project name> decision", collection: "diva", limit: 5)
```

Extract key decisions:
- Material selections (finishes, structure, insulation)
- System choices (HVAC, domotica, security)
- Design decisions (layout changes, program adjustments)
- Budget decisions (value engineering, scope changes)

### 4. Load recent outputs

Search Obsidian for DIVA outputs related to this project:
```
Glob(pattern: "**/*<project>*", path: "C:/Users/barda/OneDrive/Documents/VCHOME segundo cerebro/05 - Claude - IA/Outputs")
```

List the 5 most recent with dates and types.

### 5. Check regulatory status

If project has licensing/regulatory context, summarize:
- **RJUE phase:** PIP submitted? Comunicacao previa? Alvara de construcao?
- **SCE status:** Energy certification submitted? Class achieved?
- **Especialidades:** Structural project approved? MEP projects approved?
- **Municipal PDM/PP constraints:** Max height, COS, afastamentos

### 6. Present comprehensive context

Output format:

```
## Projeto DIVA: <Project Name>

**Tipo:** <Moradia / Apartamento / Comercial / Misto>
**Localizacao:** <address>, <municipality>
**Area:** <X> m2 brutos / <Y> m2 uteis / Lote <Z> m2
**Fase actual:** <phase>
**Working dir:** <path if applicable>

### Equipa
- **Arquitecto:** <name>
- **Engenheiro estruturas:** <name>
- **Empreiteiro:** <name>
- **Instalador AVAC:** <name>
- **Instalador domotica:** <name>

### Orcamento
| Rubrica | Aprovado | Gasto | Restante |
|---|---|---|---|
| Construcao | EUR X | EUR Y | EUR Z |
| Especialidades | EUR X | EUR Y | EUR Z |
| Acabamentos | EUR X | EUR Y | EUR Z |
| Equipamento | EUR X | EUR Y | EUR Z |
| Contingencia | EUR X | EUR Y | EUR Z |
| **Total** | **EUR X** | **EUR Y** | **EUR Z** |

### Timeline
| Fase | Previsto | Real | Estado |
|---|---|---|---|
| Programa | MM/YYYY | MM/YYYY | Concluido |
| Estudo previo | MM/YYYY | MM/YYYY | Concluido |
| Projeto base | MM/YYYY | MM/YYYY | Em curso |
| Licenciamento | MM/YYYY | — | Pendente |
| Projeto execucao | MM/YYYY | — | Pendente |
| Obra | MM/YYYY | — | Pendente |
| Conclusao | MM/YYYY | — | Pendente |

### Licenciamento / Regulamentar
- RJUE: <status>
- SCE: <status>
- Especialidades: <status>
- PDM: <constraints>

### Decisoes activas
1. <date> — <decision summary>
2. <date> — <decision summary>
3. ...

### Pendente / Bloqueios
- [ ] <pending item>
- [ ] <pending item>
- ...

### Ultimos outputs (Obsidian)
1. YYYY-MM-DD — <title> (<type>)
2. YYYY-MM-DD — <title> (<type>)
3. ...

### RAG DIVA — contexto disponivel
- N sources, M chunks relevantes
- Temas indexados: <list>

Pronto para trabalhar no projeto. O que precisas?
```

### 7. Set active project context

After presenting, all subsequent DIVA interactions in this session should:
- Auto-include project name in RAG queries (collection: "diva")
- Reference project memory for decisions and constraints
- Save outputs with project name prefix via `diva-obsidian-save`
- Apply project-specific budget and regulatory constraints
- Use project's location for climate zone (energy), municipality (regulations), etc.

## Project phase reference (Portuguese architecture workflow)

| Phase | Description | Key deliverables |
|---|---|---|
| Programa | Requirements gathering | Program of requirements, brief |
| Estudo Previo | Concept design | Concept drawings, area calculations, initial budget |
| Anteprojeto | Developed design | Developed drawings, material palette, preliminary specs |
| Projeto Base | Planning application | Full drawings for licensing, memoria descritiva |
| Licenciamento | Municipal approval | Submitted to CM, awaiting approval |
| Projeto Execucao | Construction docs | Detail drawings, caderno de encargos, BOQ |
| Concurso/Adjudicacao | Tender/contractor selection | Tender docs, contractor evaluation, contract |
| Obra | Construction | Site management, progress tracking, changes |
| Recepcao | Handover | Snag list, telas finais, licenca de utilizacao |

## Quick usage examples

```
User: "projeto DIVA moradia sintra"
DIVA: loads Moradia Sintra context — phase: projeto execucao, budget 85% allocated, 
      pending: HVAC subcontractor selection, domotica spec approval

User: "projecto apartamento alfama"
DIVA: loads Apt Alfama context — phase: obra, 60% complete, budget on track,
      pending: kitchen finishes selection, energy cert scheduling

User: "projetos DIVA"
DIVA: lists all known architecture projects with phase and status summary

User: "contexto do Vila Cascais"
DIVA: loads Vila Cascais — new build, phase: licenciamento submitted 2 months ago,
      waiting CM approval, all especialidades approved
```

## Interactions

- Pairs with all DIVA skills — sets project context before execution
- Uses `diva-rag-ingest` collection for RAG searches
- References files saved by `diva-obsidian-save`
- Can cross-reference with `dario-projeto` if project has both building and digital components
- Updates agent-memory project file if significant new information is loaded

## Red flags — don't do this

- Don't load project context without checking if memory/RAG entries exist — if empty, ask user to provide context
- Don't assume project details — if memory is stale (>60 days without update), flag it and ask for current status
- Don't mix DIVA and DARIO project contexts — keep architecture and digital separate
- Don't display budget numbers without confirming they're current — budgets change frequently in construction
- Don't assume regulatory status — always caveat with "ultimo estado registado em <date>"
- If project has no RAG entries, suggest ingesting key documents: caderno de encargos, memoria descritiva, orcamento
- Don't forget to check for related projects at the same location (e.g., interiors project + landscape project for same property)

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas checks passam.

---

### Gate 1 — Projeto identificado e sem ambiguidade

- [ ] Nome do projeto corresponde a uma entrada real em agent-memory, RAG DIVA, ou Obsidian vault (não inferido)
- [ ] Tipo de projecto está categorizado (moradia / apartamento / comercial / misto)
- [ ] Localização inclui morada OU município OU freguesia — não "local desconhecido"
- [ ] Se houver mais de um projecto com nome similar, foi pedida clarificação ao utilizador antes de carregar contexto

❌ NOT delivery-ready: `Projeto: Vila Cascais — localização: a definir`
✅ Delivery-ready: `Projeto: Moradia Vila Cascais — Rua das Acácias 12, Cascais, Município de Cascais`

---

### Gate 2 — Dados de orçamento com valores reais e datas

- [ ] Tabela de orçamento tem pelo menos 3 rubricas preenchidas com valores EUR reais
- [ ] Colunas Aprovado / Gasto / Restante têm números concretos (mesmo que Gasto = EUR 0 com data de início)
- [ ] Contingência está explícita como rubrica separada
- [ ] Nenhuma célula contém apenas "EUR X" ou "a definir" sem nota explicativa

❌ NOT delivery-ready: `Construção | EUR X | EUR Y | EUR Z`
✅ Delivery-ready: `Construção | EUR 285 000 | EUR 47 200 | EUR 237 800`

---

### Gate 3 — Timeline com estados actualizados e desvios assinalados

- [ ] Todas as fases têm data Previsto preenchida
- [ ] Fases concluídas têm data Real preenchida
- [ ] Fases com atraso têm Estado marcado como "Atrasado (N semanas)" não apenas "Pendente"
- [ ] Fase actual está inequivocamente identificada (não duas fases marcadas "Em curso")

❌ NOT delivery-ready: `Licenciamento | 03/2025 | — | Pendente`
✅ Delivery-ready: `Licenciamento | 03/2025 | — | Atrasado (6 semanas) — aguarda parecer DGPC`

---

### Gate 4 — Estatuto regulamentar / licenciamento completo

- [ ] RJUE status indica fase concreta: PIP / Comunicação Prévia submetida / Alvará emitido / nenhum ainda iniciado
- [ ] SCE tem estado claro: não iniciado / em curso / classe obtida (letra)
- [ ] Especialidades indicam quais estão aprovadas e quais pendentes individualmente
- [ ] PDM/PP menciona pelo menos COS, cércea máxima, ou afastamentos mínimos se informação existir

❌ NOT delivery-ready: `RJUE: em processo. SCE: pendente.`
✅ Delivery-ready: `RJUE: Comunicação Prévia submetida 2024-11-14, referência CM-CAS-2024-4421. SCE: não iniciado. Especialidades: estrutural aprovado 2025-01-08; AVAC pendente. PDM Cascais: COS máx 0,35; cércea máx 7,5 m; afastamento lateral mín 3 m.`

---

### Gate 5 — Decisões activas e pendentes accionáveis

- [ ] Cada decisão activa tem data e sumário com 1 linha de contexto — não apenas palavra-chave
- [ ] Lista de pendentes usa checkbox `[ ]` com responsável ou prazo quando conhecido
- [ ] Bloqueios críticos estão separados de pendentes de rotina (ou assinalados com 🔴)
- [ ] Nenhum item de pendentes está vazio ou genérico como "ver com equipa"

❌ NOT delivery-ready: `[ ] Acabamentos — ver com cliente`
✅ Delivery-ready: `[ ] Seleccionar revestimento piso cozinha — cliente enviou 3 amostras Margres, decisão esperada até 2025-03-28 (bloqueante para encomenda)`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem placeholders angle-brackets

- [ ] Zero ocorrências de `<project name>`, `<address>`, `<name>`, `<X>`, `<Y>`, `<Z>` no output final
- [ ] Nome do cliente/projecto aparece no título H2 e pelo menos uma vez no corpo
- [ ] Equipa tem nomes reais ou "a confirmar" explícito — não `<architect>` ou `<empreiteiro>`
- [ ] Últimos outputs Obsidian têm títulos reais com datas YYYY-MM-DD, não `<title> (<type>)`

❌ NOT delivery-ready: `Arquitecto: <name> | Empreiteiro: <name>`
✅ Delivery-ready: `Arquitecto: Arq. Rui Menezes | Empreiteiro: Construções Barata Lda (a confirmar — proposta recebida 2025-02-10)`

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via agent-memory, RAG, ou Obsidian vault (fonte localizável)
- 🟡 **assumed** — plausível com base no histórico do projeto, mas precisa confirmação do cliente antes de entregar
- 🟢 **projection** — previsão por design (custos estimados, datas de fase futura, métricas regulatórias pendentes)

Output checklist upfront mostra ao leitor exatamente o que é trust-as-is vs. o que precisa de verify antes de avançar com decisões de obra ou licenciamento.

❌ NOT delivery-ready:
> "Orçamento restante: EUR 42.000 | Fase actual: Projeto de Execução | Alvará previsto: Março 2025"
> *(reader assume tudo verified — mas restante pode estar desatualizado, fase pode ter avançado, alvará é estimativa não confirmada)*

✅ Delivery-ready:
> - 🔵 **verified** — Orçamento aprovado EUR 180.000 (lido de `project_vila_cascais.md`, sessão 2024-11-03)
> - 🟡 **assumed** — Orçamento gasto EUR 138.000 (último registo em Obsidian; confirmar com empreiteiro se houve auto de medição recente)
> - 🟢 **projection** — Alvará de construção previsto Q1 2025 (estimativa baseada em prazo médio municipal; sujeito a resposta da CM)

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed — substituir assumptions com actuals (ex: auto de medição actualizado, fase real da obra)
- [ ] All 🔵 citations added — indicar ficheiro-fonte e data de última actualização para cada dado de orçamento e equipa
- [ ] All 🟢 projections labeled as such ao cliente — datas de licenciamento, estimativas de custo de especialidades, e prazos de conclusão apresentados como previsão, não como compromisso

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Projeto DIVA: Moradia Unifamiliar Birre

**Tipo:** Moradia nova construção
**Localização:** Rua do Moinho 34, Birre, Cascais
**Área:** 320 m² brutos / 278 m² úteis / Lote 890 m²
**Fase actual:** Projecto Base — em curso
**Working dir:** `VCHOME segundo cerebro/01 - Projetos/DIVA/Moradia-Birre/`

---

### Equipa
- **Arquitecto:** Arq. Rui Menezes (Atelier Menezes & Associados)
- **Engenheiro estruturas:** Eng. Paulo Saraiva (EST.Lda)
- **Engenheiro MEP:** Eng. Catarina Lopes (TecnoMEP)
- **Empreiteiro:** Construções Barata Lda (proposta aceite 2025-02-10)
- **Instalador AVAC:** ClimaSul (a contratar — concurso aberto)
- **Instalador domótica:** KNX Home Cascais

---

### Orçamento
| Rubrica          | Aprovado     | Gasto       | Restante     |
|------------------|--------------|-------------|--------------|
| Construção       | EUR 285 000  | EUR 47 200  | EUR 237 800  |
| Especialidades   | EUR 38 000   | EUR 12 400  | EUR 25 600   |
| Acabamentos      | EUR 64 000   | EUR 0       | EUR 64 000   |
| Equipamento      | EUR 22 000   | EUR 0       | EUR 22 000   |
| Arquitectura     | EUR 31 500   | EUR 15 750  | EUR 15 750   |
| Contingência     | EUR 24 000   | EUR 0       | EUR 24 000   |
| **Total**        | **EUR 464 500** | **EUR 75 350** | **EUR 389 150** |

> ⚠️ Acabamentos: orçamento Margres recebido (EUR 18 400) — aguarda aprovação cliente.

---

### Timeline
| Fase               | Previsto    | Real        | Estado                        |
|--------------------|-------------|-------------|-------------------------------|
| Programa           | 06/2024     | 06/2024     | Concluído                     |
| Estudo Prévio      | 09/2024     | 10/2024     | Concluído (4 sem. atraso)     |
| Projecto Base      | 01/2025     | —           | Em curso (entrega 2025-04-15) |
| Licenciamento      | 04/2025     | —           | Pendente                      |
| Projecto Execução  | 09/2025     | —           | Pendente                      |
| Obra               | 11/2025     | —           | Pendente                      |
| Conclusão          | 06/2027     | —           | Pendente                      |

---

### Licenciamento / Regulamentar
- **RJUE:** Comunicação Prévia em preparação — submissão prevista 2025-04-22 na CM Cascais
- **SCE:** Não iniciado — perito SCE Eng. Filipa Antunes contactada, proposta pendente
- **Especialidades:** Projecto estrutural aprovado 2025-01-08; MEP em curso (entrega EST. 2025-03-31); AVAC aguarda definição equipamentos
- **PDM Cascais:** COS máx 0,35 (projecto em 0,31 ✅); cércea máx 7,5 m (projecto 7,2 m ✅); afastamento lateral mín 3 m (cumprido ✅); afastamento frontal mín 5 m (cumprido ✅)

---

### Decisões activas
1. **2025-02-10** — Empreiteiro seleccionado: Construções Barata Lda (proposta EUR 268 000, prazo 18 meses)
2. **2025-01-22** — Sistema domótica: KNX (descartado Z-Wave por incompatibilidade com painel solar SMA)
3. **2024-12-05** — Laje fungiforme aligeirada aprovada para cave (redução de peso vs. maciça, poupança EUR 8 200)
4. **2024-11-18** — Orientação principal da moradia rodada 12° Sul para optimizar ganhos solares passivos
5. **2024-10-30** — Área de piscina removida do programa (cliente: restrições orçamentais — adicionada como fase 2 opcional)

---

### Pendente / Bloqueios
- 🔴 [ ] Aprovação cliente orçamento Margres (EUR 18 400) — bloqueante para peça de acabamentos do Proj. Base — prazo: 2025-03-28
- 🔴 [ ] Definir equipamentos AVAC (VRF vs. Split DC) — bloqueante para projecto MEP de ClimaSul — decidir até 2025-04-05
- [ ] Receber proposta perito SCE Eng. Filipa Antunes — enviado pedido 2025-03-10, aguarda resposta
- [ ] Confirmar ponto de ligação EPAL — requerimento enviado 2025-02-28, referência EPAL-2025-03847
- [ ] Reunião cliente revisão Projecto Base — agendar semana de 2025-04-07

---

### Últimos outputs (Obsidian)
1. 2025-03-12 — `Moradia-Birre_Comparativo-AVAC_VRF-vs-Split.md` (análise técnica)
2. 2025-02-25 — `Moradia-Birre_Acta-Reuniao-Cliente-Rev2.md` (acta)
3. 2025-02-10 — `Moradia-Birre_Avaliacao-Proposta-Barata.md` (análise de proposta)
4. 2025-01-22 — `Moradia-Birre_Decisao-Domotica-KNX.md` (registo de decisão)
5. 2025-01-08 — `Moradia-Birre_Aprovacao-Estrutural-EST.md` (output regulamentar)

---

### RAG DIVA — contexto disponível
- 23 sources indexadas, 147 chunks relevantes
- Temas indexados: regulamento PDM Cascais, RJUE comunicação prévia, sistema KNX Birre, especificações Margres, caderno de encargos Barata Lda, peças desenhadas EP Rev.2
```

---

## Output anti-patterns

- Entregar output com `<project name>`, `<X>`, `<address>` ou qualquer placeholder angle-bracket visível ao cliente
- Tabela de orçamento com todas as colunas "EUR X / EUR Y / EUR Z" — pior do que omitir a tabela
- Estado de timeline igual para múltiplas fases simultâneas ("Em curso" em 3 linhas ao mesmo tempo)
- Licenciamento resumido a uma linha genérica ("em processo") sem número de referência ou data de submissão
- Decisões activas sem data — impossível auditar cronologia do projecto
- Pendentes sem responsável nem prazo em itens marcados como bloqueantes (🔴 sem contexto)
- Carregar contexto de projecto errado por match parcial de nome sem pedir confirmação ao utilizador
- Equipa com campos em branco silenciosos — preferir "a confirmar" explícito a célula vazia
- RAG summary sem número de sources — "contexto disponível" sem quantificação não é auditável
- Omitir secção de Licenciamento/Regulamentar porque "ainda não há nada" — deve aparecer com estado "não iniciado" e próximo passo
