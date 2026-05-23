---
name: diva-client-onboard
description: "Mega-orchestrator for new architecture/design/construction client onboarding. Runs diva-diagnose + diva-briefing + agent-memory project file + RAG indexing + Obsidian context save + quick wins list. One command = new client fully onboarded. Triggers on \"novo cliente\", \"onboard client\", \"client kickoff\", \"comecar projeto novo\", \"novo projecto DIVA\", \"onboard DIVA\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# DIVA Client Onboard — Mega-Orchestrator

One command onboards a new architecture/design/construction client. Chains: diagnose + briefing + memory + RAG + Obsidian + quick wins.

## When to activate

Invoke `/diva-client-onboard` when:
- New client/project arrives for architecture, interiores, or obra
- User says "novo cliente", "novo projecto", "comecar projecto"
- First contact with any design/construction project
- User wants full setup in one go

Do NOT use when:
- Project already onboarded (use `/diva-projeto` to switch)
- User just wants one specific skill (use that skill directly)

## Workflow — 8 Steps

### Step 1: Gather minimum context
Ask (or infer from input):
- **Quem:** Nome do cliente, contacto
- **O que:** Tipo de projecto (remodelacao, construcao nova, interiores, obra)
- **Onde:** Morada ou zona (Lisboa, Porto, Algarve, etc.)
- **Quanto:** Orcamento indicativo (se disponivel)
- **Quando:** Timeline desejada
- **Porquê agora:** O que motivou o contacto

If critical info missing, ask — don't assume.

### Step 2: Check existing context
```
mcp__dario-rag__search_kb(query: "<client name> <project type>", limit: 5)
mcp__dario-rag__search_kb(query: "<address or zone>", collection: "diva", limit: 3)
```
Check agent memory: `~/.claude/agent-memory/diva-v1-design-architect/`
Check Obsidian: `D.I.V.A vault/05 - Claude - IA/Contextos/`

### Step 3: Run `/diva-diagnose`
Execute diagnostic workflow:
- Avaliar espaco/projecto holisticamente
- Arquitectura + Design + Obras + Regulamentacao + Orcamento
- Classificar: CRITICO / IMPORTANTE / OPTIMIZACAO
- Gerar roadmap 4 milestones

### Step 4: Run `/diva-briefing`
Capture structured briefing:
- Lifestyle, necessidades, desejos
- Orcamento e prioridades
- Preferencias de estilo
- Constrains tecnicos e regulamentares

### Step 5: Create project memory file
Write to `~/.claude/agent-memory/diva-v1-design-architect/project_<slug>.md`:

```markdown
---
name: <Client/Project Name>
description: <one-line project summary>
type: project
---

**Projecto:** <nome>
**Tipo:** <remodelacao/construcao nova/interiores/obra>
**Localizacao:** <morada/zona>
**Area:** <m2>
**Orcamento:** <EUR range>
**Timeline:** <desejada>
**Estilo:** <direccao identificada>
**Estado:** Onboarded <date>

**Why:** <motivacao do cliente>
**How to apply:** <como este contexto deve influenciar recomendacoes>

**Decisoes tomadas:**
- (nenhuma ainda)

**Proximos passos:**
- [ ] <accao 1>
- [ ] <accao 2>
```

Update MEMORY.md index.

### Step 6: Ingest into RAG
```
mcp__dario-rag__ingest_text(
  name: "Projecto <Client> — Contexto Inicial",
  content: <briefing + diagnostico resumido>,
  collection: "diva",
  tags: ["project", "<client-slug>", "<project-type>", "<location>"]
)
```

### Step 7: Save to Obsidian
Save 3 documents:
1. `YYYY-MM-DD - <Client> - Contexto Inicial.md` → `05 - Claude - IA/Contextos/`
2. `YYYY-MM-DD - <Client> - Diagnostico DIVA.md` → `05 - Claude - IA/Outputs/`
3. `YYYY-MM-DD - <Client> - Quick Wins.md` → `05 - Claude - IA/Outputs/`

### Step 8: Generate Quick Wins
List 5-10 accoes imediatas que o cliente pode executar enquanto o projecto avanca:
- Quick wins de design (ex: pintar uma parede, trocar luminarias)
- Quick wins de planeamento (ex: pedir certidao predial, verificar PDM online)
- Quick wins de orcamento (ex: consultar 3 empreiteiros, visitar showroom X)

## Output — Onboarding Complete Summary

```markdown
## Onboarding Completo — <Client>

**Projecto:** <tipo> em <localizacao>
**Area:** <m2> | **Orcamento:** <EUR> | **Timeline:** <meses>

### Diagnostico
- CRITICO: <N items>
- IMPORTANTE: <N items>
- OPTIMIZACAO: <N items>

### Estilo Identificado
- Direccao: <style> (Primary: <designer>, Secondary: <designer>)

### Documentos Criados
- [x] Memory file: project_<slug>.md
- [x] RAG indexed: <chunk ID>
- [x] Obsidian: Contexto + Diagnostico + Quick Wins

### Quick Wins (fazer ja)
1. <accao>
2. <accao>
3. <accao>

### Proximas Skills a Usar
- `/diva-floor-plan` — se tiver planta
- `/diva-materials` — para comecar a definir paleta
- `/diva-budget` — orcamento detalhado
- `/diva-licensing` — verificar necessidade de licenciamento
```

## Red flags
- Never skip RAG check for existing context
- Never skip memory file creation
- Never proceed without minimum context (tipo + localizacao + orcamento indicativo)
- Never forget to save to Obsidian
- Never skip quick wins — high perceived value for client

## Interactions
- Chains: `/diva-diagnose` → `/diva-briefing` → memory → RAG → Obsidian
- After onboard: `/diva-floor-plan`, `/diva-materials`, `/diva-budget`, `/diva-licensing`
- For existing project: `/diva-projeto` instead

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Contexto mínimo capturado (sem assumptions)

- [ ] Nome do cliente real presente (não "Cliente X" ou `<client name>`)
- [ ] Tipo de projecto explícito: remodelação / construção nova / interiores / obra
- [ ] Localização concreta (morada, freguesia ou zona — não "Lisboa" genérico)
- [ ] Orçamento indicativo registado (range EUR ou "TBD com justificação")
- [ ] Timeline desejada capturada ou flagged como "a definir em briefing"

❌ NOT delivery-ready: `Projecto: remodelação em Lisboa. Orçamento: a confirmar.`
✅ Delivery-ready: `Projecto: remodelação de apartamento T3, Rua Actor Vale 12, Arroios. Orçamento: 45–60k EUR. Timeline: ocupação set 2025.`

---

### Gate 2 — Diagnóstico executado com classificação real

- [ ] Pelo menos 1 item CRÍTICO identificado (com descrição concreta, não placeholder)
- [ ] Pelo menos 2 itens IMPORTANTE identificados
- [ ] Roadmap tem 4 milestones com nomes e ordem lógica
- [ ] Diagnóstico reflecte o tipo de projecto (não é genérico copy-paste)

❌ NOT delivery-ready: `CRÍTICO: verificar estrutura. IMPORTANTE: definir estilo.`
✅ Delivery-ready: `CRÍTICO: laje de betão com fissuras diagonais em vão principal — requer inspecção estrutural antes de avançar com obra. IMPORTANTE: instalação eléctrica monofásica incompatível com requisitos AVAC planeados.`

---

### Gate 3 — Memory file criado e indexado correctamente

- [ ] Ficheiro `project_<slug>.md` escrito em `~/.claude/agent-memory/diva-v1-design-architect/`
- [ ] Slug derivado do nome real do cliente/projecto (ex: `project_teatro-verde-cascais.md`)
- [ ] Campos `Why:` e `How to apply:` preenchidos com contexto accionável
- [ ] `MEMORY.md` index actualizado com nova entrada
- [ ] Próximos passos listados com pelo menos 2 acções concretas

❌ NOT delivery-ready: `project_cliente-novo.md` com campos `<nome>`, `<tipo>` por preencher
✅ Delivery-ready: `project_familia-sousa-sintra.md` — `Why: venda de casa planeada em 18 meses, valorização via remodelação. How to apply: priorizar acabamentos com ROI alto, evitar personalização excessiva.`

---

### Gate 4 — RAG ingestão confirmada com tags estruturadas

- [ ] `ingest_text` executado com `collection: "diva"`
- [ ] Tags incluem: `["project", "<client-slug>", "<project-type>", "<location>"]` — sem angle-brackets
- [ ] Conteúdo ingerido inclui briefing resumido + diagnóstico (não só nome do cliente)
- [ ] Chunk ID ou confirmação de ingestão registada no output final

❌ NOT delivery-ready: RAG ingestão omitida ou `tags: ["project", "<client>"]`
✅ Delivery-ready: `tags: ["project", "familia-sousa-sintra", "remodelacao", "sintra-centro"]` — chunk ID `diva-2025-0147` confirmado

---

### Gate 5 — Obsidian: 3 documentos salvos com nomes correctos

- [ ] `2025-MM-DD - <Cliente> - Contexto Inicial.md` → pasta `05 - Claude - IA/Contextos/`
- [ ] `2025-MM-DD - <Cliente> - Diagnostico DIVA.md` → pasta `05 - Claude - IA/Outputs/`
- [ ] `2025-MM-DD - <Cliente> - Quick Wins.md` → pasta `05 - Claude - IA/Outputs/`
- [ ] Datas reais (não `YYYY-MM-DD`), nomes de cliente reais (não `<Client>`)

❌ NOT delivery-ready: `YYYY-MM-DD - <Client> - Contexto Inicial.md` salvo em pasta errada
✅ Delivery-ready: `2025-06-14 - Família Sousa Sintra - Contexto Inicial.md` em `05 - Claude - IA/Contextos/`

---

### Gate 6 — Quick Wins accionáveis + output usa NOME DO CLIENTE e dados reais, sem angle-brackets

- [ ] 5–10 quick wins listados, cada um com verbo de acção e especificidade suficiente para executar hoje
- [ ] Quick wins cobrem pelo menos 2 categorias (design / planeamento / orçamento / regulamentação)
- [ ] Nenhum quick win é genérico ("melhorar iluminação") sem detalhe concreto
- [ ] Output final tem nome real do cliente, localização real, datas reais — zero `<placeholders>`
- [ ] Próximas skills sugeridas são relevantes para o projecto específico (não lista boilerplate)

❌ NOT delivery-ready: `1. Pintar uma parede. 2. Consultar empreiteiros. 3. Ver showroom.`
✅ Delivery-ready: `1. Pedir certidão predial do artigo 1234-A, Sintra — online em predial.inci.pt (15 min). 2. Verificar PDM Sintra para lote — zona ARU com incentivos fiscais aplicáveis. 3. Visitar showroom Porcelanosa Cascais (fecha 18h) para benchmarking de pavimentos — orçamento piso: ~38 EUR/m².`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Onboarding Completo — Família Andrade Costa

**Projecto:** Remodelação integral de moradia V4, Rua das Acácias 27, São João do Estoril
**Área:** 210 m² (r/c + 1º andar) | **Orçamento:** 90–120k EUR | **Timeline:** conclusão fev 2026

---

### Diagnóstico DIVA

**CRÍTICO (2 items)**
- Cobertura com infiltrações activas em 3 pontos — impermeabilização urgente antes de qualquer obra interior
- Quadro eléctrico de 1987, monofásico 25A — substituição obrigatória (AVAC + cozinha nova incompatíveis)

**IMPORTANTE (4 items)**
- Caixilharia alumínio anos 90 sem corte térmico — substituição prioritária para cumprir REH 2024
- WC principal (6 m²) com tubagem em ferro fundido — recomendado rerouting durante obra
- Escada interior sem corrimão conforme — intervenção obrigatória para licenciamento
- Garagem sem ventilação mecânica — requisito PDM Cascais para conversão a espaço habitável

**OPTIMIZAÇÃO (3 items)**
- Hall entrada (18 m²) subaproveitado — potencial para closet embutido + zona mudas
- Cozinha orientada a norte sem janela de serviço — estudo de claraboia ou redireccionamento
- Jardim 85 m² sem drenagem — quick win de baixo custo, alto impacto visual

**Roadmap**
- M1 (ago 2025): Projecto de arquitectura + licenciamento CM Cascais
- M2 (out 2025): Obra estrutural + cobertura + eléctrico
- M3 (dez 2025): Acabamentos + cozinha + WCs
- M4 (fev 2026): Arranjos exteriores + entrega

---

### Estilo Identificado
- Direcção: Contemporary Coastal Portuguese
- Primary ref: João Mendes Ribeiro (materialidade honesta, betão + madeira)
- Secondary ref: Studio Roque Atelier (paleta clara, azulejo contemporâneo)
- Mood: luminoso, atemporal, baixa manutenção — filhos pequenos, cão

---

### Documentos Criados
- [x] Memory file: `project_andrade-costa-estoril.md` → `~/.claude/agent-memory/diva-v1-design-architect/`
- [x] MEMORY.md index actualizado (entrada #14)
- [x] RAG indexado: chunk ID `diva-2025-0203`, tags `["project", "andrade-costa-estoril", "remodelacao", "estoril-cascais"]`
- [x] Obsidian — `2025-06-14 - Andrade Costa Estoril - Contexto Inicial.md` → Contextos/
- [x] Obsidian — `2025-06-14 - Andrade Costa Estoril - Diagnostico DIVA.md` → Outputs/
- [x] Obsidian — `2025-06-14 - Andrade Costa Estoril - Quick Wins.md` → Outputs/

---

### Quick Wins (fazer já — antes de M1)

**Planeamento & Regulamentação**
1. Pedir certidão predial art. 4521-B, Cascais — predial.inci.pt (gratuito, 10 min)
2. Confirmar se imóvel está em ARU Estoril → isenção IMI + apoios reabilitação (CM Cascais, balcão online)
3. Verificar PDM Cascais para índice de construção — parcela 720 m², potencial ampliação a estudar

**Design & Materialidade**
4. Visitar showroom Cerâmica Sant'Ana, Calçada da Boa-Hora, Lisboa — azulejo de autor para entrada (orçamento ref: 85 EUR/m²)
5. Fotografar cobertura por drone antes de obra — documentação para seguro e projecto (drone aluguer ~120 EUR/dia)
6. Pintar quarto principal com Branco Puro NCS S 0500-N (Cin) — teste de luz antes de comprometer em obra

**Orçamento & Parceiros**
7. Consultar 3 empreiteiros de referência zona Cascais: Construtora Oeiras Lda, ReformaCascais, AtlantiCobras — pedir proposta base cobertura
8. Verificar apólice multirriscos habitação — cobertura infiltrações activas pode incluir parcela da obra

---

### Próximas Skills a Usar
- `/diva-floor-plan` — cliente tem planta CAD 2019, carregar e analisar circulações
- `/diva-licensing` — verificar viabilidade de ampliação no PDM antes de M1
- `/diva-materials` — definir paleta completa (Contemporary Coastal confirmado)
- `/diva-budget` — detalhar 90–120k EUR por fase com contingência 15%
```

---

## Output anti-patterns

- Angle-brackets no output final (`<client name>`, `<tipo>`, `YYYY-MM-DD`) — sinal de template não preenchido
- Diagnóstico genérico sem especificidade técnica ("verificar estrutura", "melhorar iluminação") sem contexto do projecto real
- Quick wins inaccionáveis hoje ("pensar no estilo", "consultar alguém") sem verbo concreto, recurso ou estimativa de tempo/custo
- RAG ingestão omitida silenciosamente ou listada como `[x]` sem chunk ID de confirmação
- Memory file com slug `project_cliente-novo.md` ou campos `Why`/`How to apply` em branco
- Obsidian com datas placeholder ou ficheiros salvos na pasta errada (Contextos vs Outputs confundidos)
- Próximas skills sugeridas como lista boilerplate sem ligação ao projecto específico (ex: sugerir `/diva-licensing` a projecto de interiores sem obras estruturais)
- Diagnóstico sem nenhum item CRÍTICO quando projecto tem obra (implausível — indica análise superficial)
- Estilo identificado sem referência a designer ou mood board concreto ("moderno", "minimalista" sem mais)
