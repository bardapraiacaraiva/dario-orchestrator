---
name: diva-licensing
description: Portuguese building permits checklist based on RJUE/RGEU. Covers procedure types, required documents, entities, timelines, costs, and RERU exemptions for rehabilitation. Triggers on "licenciamento", "licensing", "camara", "alvara", "comunicacao previa", "RJUE", "RGEU", "obras isentas".
license: MIT
---

# DIVA Skill — Portuguese Building Permits (RJUE/RGEU)

Comprehensive checklist and workflow for obtaining building permits in Portugal. Covers the full RJUE (Regime Juridico da Urbanizacao e Edificacao) framework, required documentation per project type, entity coordination, timelines, costs, and special regimes (RERU for rehabilitation, heritage zones, PDM constraints).

## When to activate

- Client asks "preciso de licenca para esta obra?"
- Starting a new construction or renovation project
- Determining whether a project is exempt (art.6 RJUE) or needs comunicacao previa vs licenciamento
- Preparing documentation package for camara municipal
- Client received a notification from camara about illegal works
- Heritage zone project requiring DGPC consultation
- Rehabilitation project potentially eligible for RERU exemptions

## Workflow

### 1. Gather inputs

- **Project type:** new build / extension / renovation / interior alteration / change of use / demolition
- **Building type:** residential / commercial / mixed / industrial
- **Location:** municipality + freguesia
- **Heritage zone (ZP)?** yes/no + which monument
- **PDM classification:** urbano consolidado / urbano nao consolidado / rural / industrial
- **Building age:** pre-1951 / 1951-1990 / post-1990
- **Structural changes?** yes/no
- **Facade changes?** yes/no
- **Change of use?** yes/no
- **Total area of intervention:** m2
- **Number of fractions/units:** N

If location or project type is missing, stop and ask.

### 2. RAG consult

```
mcp__dario-rag__search_kb(query: "RJUE licenciamento comunicacao previa obras isentas Portugal", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "RERU reabilitacao urbana isencoes", collection: "dario", limit: 5)
mcp__dario-rag__search_kb(query: "documentos projecto arquitectura especialidades camara", collection: "dario", limit: 5)
```

### 3. Determine procedure type

Apply RJUE decision tree:

**Obras isentas (art.6 RJUE) -- no permit needed:**
- Interior works without structural or facade changes
- Painting exterior (same color, no heritage zone)
- Equipment maintenance/replacement (like-for-like)
- Temporary structures < 30 days
- Agricultural structures < 50m2 in rural areas
- Demolition of structures < 2 floors (non-heritage, non-listed)

**Comunicacao previa (art.34-36 RJUE) -- notification, 20-day tacit approval:**
- Interior renovations with structural changes (no facade change)
- Change of use (within same PDM category)
- Works in loteamento areas with alvara that already defines parameters
- Small extensions within PDM limits
- Installation of solar panels
- Pool construction (some municipalities)

**Licenciamento (art.4 RJUE) -- full permit required:**
- New construction
- Extensions/alterations with facade changes
- Change of use with building works
- Works in heritage zones (ZP)
- Works in areas without loteamento or PU
- Demolition of buildings > 2 floors or in protected areas

**Autorizacao de utilizacao (art.62-65 RJUE) -- use permit:**
- Required after any licenciamento before occupation
- Change of use (even without works)
- First occupation of new building

### 4. Required documents checklist

#### Base documents (all procedures)
- [ ] Requerimento (official form from camara portal)
- [ ] Certidao de registo predial (< 6 months)
- [ ] Caderneta predial (Financas)
- [ ] Legitimidade do requerente (proof of ownership or authorization)
- [ ] Levantamento topografico (for new builds / extensions)
- [ ] Fotografias do estado actual (dated)

#### Projecto de arquitectura
- [ ] Memorias descritiva e justificativa
- [ ] Plantas (implantacao, pisos, cobertura) escala 1:100 ou 1:50
- [ ] Alcados (all facades) escala 1:100 ou 1:50
- [ ] Cortes (minimum 2) escala 1:100 ou 1:50
- [ ] Mapa de areas (areas brutas, uteis, implantacao, construcao)
- [ ] Mapa de acabamentos
- [ ] Estimativa orcamental
- [ ] Declaracao do autor (arquitecto inscrito na OA)
- [ ] Termo de responsabilidade do arquitecto
- [ ] Seguro de responsabilidade civil do arquitecto

#### Projectos de especialidades (after architecture approval)
- [ ] **Estruturas (estabilidade)** -- engenheiro civil, termo de responsabilidade
- [ ] **Redes de abastecimento de agua** -- engenheiro civil/mecanico
- [ ] **Redes de drenagem de aguas residuais** -- engenheiro civil/mecanico
- [ ] **Redes de drenagem de aguas pluviais** -- engenheiro civil/mecanico
- [ ] **Instalacoes electricas (ITED)** -- engenheiro electrotecnico
- [ ] **Telecomunicacoes (ITED)** -- engenheiro electrotecnico, ANACOM
- [ ] **Instalacoes de gas** -- engenheiro mecanico (if applicable)
- [ ] **Comportamento termico (REH/RECS)** -- perito qualificado ADENE
- [ ] **Acustica (RRAE)** -- engenheiro acustico
- [ ] **Seguranca contra incendios (SCIE)** -- conforme RJSCIE, parecer bombeiros/ANPC
- [ ] **AVAC** -- engenheiro mecanico (if central system)
- [ ] **Acessibilidades** -- conforme DL 163/2006

#### Heritage zone additional
- [ ] Parecer DGPC (Direccao-Geral do Patrimonio Cultural)
- [ ] Parecer IGESPAR (if national monument)
- [ ] Relatorio arqueologico (if required by DGPC)
- [ ] Documentacao fotografica detalhada do existente

### 5. Entity coordination

| Entidade | Quando | Prazo resposta | Notas |
|---|---|---|---|
| Camara Municipal | Sempre | 30 dias (arq) + 45 dias (esp) | Consultar portal online |
| Bombeiros / ANPC | SCIE categoria >= 2a | 30 dias | Parecer vinculativo |
| DGPC | Zona de protecao monumento | 30-60 dias | Pode bloquear projecto |
| CCDR | Fora perimetro urbano | 30 dias | Parecer sobre REN/RAN |
| APA / ARH | Junto a linhas de agua | 30-45 dias | Dominio hidrico |
| ANACOM | Telecomunicacoes ITED | 20 dias | Via projecto ITED |
| ADENE | Certificado energetico | Imediato (perito) | Obrigatorio pre-venda/arrendamento |
| ARS (Saude) | Restauracao/alimentar | 30 dias | Condicoes sanitarias |
| IGAMAOT | Gestao residuos demolicao | N/A | Plano de residuos obrigatorio |

### 6. Timelines and tacit approval

| Procedimento | Prazo decisao | Aprovacao tacita | Validade |
|---|---|---|---|
| Comunicacao previa | 20 dias uteis | Sim (deferimento tacito) | 1 ano para iniciar |
| Licenciamento - arquitectura | 30 dias uteis | Sim (art.111 RJUE) | -- |
| Licenciamento - especialidades | 45 dias uteis | Sim | -- |
| Alvara de construcao | 30 dias apos aprovacao | N/A | 1 ano (prorrogavel) |
| Autorizacao de utilizacao | 10 dias uteis (vistoria) | Sim (30 dias uteis) | Permanente |
| Parecer externo (bombeiros, etc) | 30 dias uteis | Parecer favoravel tacito | -- |

### 7. Costs estimate

| Taxa | Base de calculo | Estimativa |
|---|---|---|
| Taxa de apreciacao do projecto | Por m2 de area bruta | 3-8 EUR/m2 |
| Taxa de licenca de construcao | Por m2 de area bruta | 5-15 EUR/m2 |
| Taxa de ocupacao de via publica | Por m2 x tempo | 1-5 EUR/m2/mes |
| Taxa de autorizacao de utilizacao | Por fracao | 50-200 EUR/fracao |
| Compensacoes urbanisticas | Se aplicavel (PDM) | Variavel |
| Taxa de ligacao a rede (agua/saneamento) | Por fracao | 500-2000 EUR |

**Nota:** Taxas variam significativamente entre municipios. Consultar tabela de taxas do municipio especifico.

### 8. RERU exemptions (rehabilitation)

If building is in ARU (Area de Reabilitacao Urbana) or was built before entry of specific regulations:
- **Exemption from RGEU** minimum areas/dimensions (for buildings pre-1951)
- **Exemption from RRAE** acoustic requirements (pre-existing conditions)
- **Simplified REH** thermal requirements
- **Exemption from accessibility** requirements (pre-existing conditions, if improvement demonstrated)
- **Reduced taxas** (many municipalities offer 50-80% reduction in ARU)
- **Tax benefits:** IMI exemption 3-5 years, IVA 6% (instead of 23%), IMT exemption

## Output template

```markdown
---
project: <project name>
date: <YYYY-MM-DD>
type: licensing-checklist
procedure: <isento / comunicacao-previa / licenciamento>
municipality: <name>
---

# Licenciamento -- <Project Name>

## Classificacao do procedimento
- **Tipo de obra:** <description>
- **Procedimento aplicavel:** <isento / comunicacao previa / licenciamento>
- **Fundamento legal:** Art. <N> do RJUE (DL 555/99)
- **Regime especial:** <RERU / zona proteccao / nenhum>

## Documentos necessarios
### Fase 1: Projecto de arquitectura
- [ ] <list per project type>

### Fase 2: Projectos de especialidades
- [ ] <list per project type>

## Entidades a consultar
| Entidade | Motivo | Prazo | Status |
|---|---|---|---|
| ... | ... | ... | Pendente |

## Cronograma do licenciamento
| Etapa | Duracao estimada | Inicio | Fim |
|---|---|---|---|
| Preparacao documentos | <N> semanas | | |
| Submissao arquitectura | 1 dia | | |
| Apreciacao arquitectura | <N> dias uteis | | |
| Submissao especialidades | 1 dia | | |
| Apreciacao especialidades | <N> dias uteis | | |
| Emissao alvara | <N> dias uteis | | |
| **Total estimado** | **<N> semanas** | | |

## Custos estimados
| Taxa | Valor estimado |
|---|---|
| ... | ... |
| **Total** | **EUR X** |

## RERU / beneficios fiscais (se aplicavel)
- <list applicable exemptions>

## Riscos
| Risco | Impacto | Mitigacao |
|---|---|---|
| ... | ... | ... |

## Proximos passos
- [ ] Confirmar classificacao PDM no portal do municipio
- [ ] Solicitar certidao predial actualizada
- [ ] Contratar equipa de projectistas com termos de responsabilidade
- [ ] Submeter projecto de arquitectura
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Project> - Licenciamento Checklist.md`

## Red Flags
- Never skip the PDM (Plano Director Municipal) check for the property's location — the PDM defines buildable area, height limits, land use, and setbacks, and ignoring it leads to project rejection or forced demolition
- Never assume RERU exemption without written verification from the camara municipal — RERU only applies within confirmed ARU boundaries, and relying on outdated maps or verbal assurances has voided exemptions mid-project
- Always check camara-specific requirements beyond the standard RJUE list — each municipio has its own tabela de taxas, additional documentation requirements, and interpretation of isencao criteria that can delay or block submission
- Never start any obra without the alvara de construcao or comunicacao previa aceite in hand — works without permit carry fines of 500 to 200,000 EUR under RJUE, plus mandatory demolition at the owner's expense
- Never submit specialty projects before architecture approval (apreciacao liminar) — if architecture is rejected or requires alterations, all specialty fees are wasted and the process restarts from zero
- Always verify heritage zone (Zona de Proteccao) status on the PDM plant before any facade or exterior work — DGPC consultation adds 2-4 months and can impose material/colour restrictions that reshape the entire project

## Interactions

- Pair with `diva-timeline` for overall project schedule including licensing phase
- Pair with `diva-inspection` for final vistoria preparation
- Follow up with `dario-proposal` for licensing cost inclusion in client proposal
- Save via `dario-obsidian-save` to vault

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Procedure type correctly determined (isentas / comunicação prévia / licenciamento)

- [ ] Decision tree aplicado com base nos inputs reais (project type + facade changes + heritage zone + loteamento)
- [ ] Artigo RJUE correto citado (art.6, art.34-36, ou art.4)
- [ ] Se "comunicação prévia", prazo de 20 dias mencionado explicitamente
- [ ] Autorizações de utilização identificadas quando aplicável (art.62-65)

❌ NOT delivery-ready: "Provavelmente precisa de licenciamento, confirme com a câmara."
✅ Delivery-ready: "Projeto de extensão com alteração de fachada em Cascais → **Licenciamento (art.4 RJUE)**. Sem zona de proteção — não requer parecer DGPC. Prazo expectável câmara: 30 dias (arquitetura) + 45 dias (especialidades)."

---

### Gate 2 — Checklist de documentos completa e calibrada ao projeto

- [ ] Documentos base listados (certidão registo predial < 6 meses, caderneta predial, legitimidade)
- [ ] Projeto de arquitetura com todos os elementos (plantas, alçados, cortes, mapa de áreas, termo responsabilidade OA)
- [ ] Especialidades filtradas ao projeto real (ex: AVAC só se sistema central; gás só se aplicável)
- [ ] Heritage zone → documentação DGPC/IGESPAR adicionada se ZP confirmada

❌ NOT delivery-ready: "Documentos necessários: projeto de arquitetura, especialidades, requerimento."
✅ Delivery-ready: "Para reabilitação interior (sem fachada) em edifício pré-1951, Lisboa: Requerimento CM Lisboa + Certidão Registo Predial (< 6 meses) + Caderneta Predial Finanças + Projeto Arquitetura (plantas 1:50, alçados, cortes, mapa áreas) + Termo Responsabilidade Arquiteto OA + REH (comportamento térmico ADENE). Estruturas **não obrigatórias** se sem alterações estruturais."

---

### Gate 3 — Entidades externas e pareceres corretamente mapeados

- [ ] Tabela de entidades gerada com prazo de resposta por entidade
- [ ] ANPC/Bombeiros referenciado se SCIE categoria ≥ 2ª
- [ ] CCDR/APA/ARH identificados se fora perímetro urbano ou junto a linha de água
- [ ] DGPC com prazo 30-60 dias se zona de proteção ativa
- [ ] ANACOM para telecomunicações (ITED) se obra nova ou reabilitação com alteração de redes

❌ NOT delivery-ready: "Pode ser necessário consultar entidades externas dependendo do local."
✅ Delivery-ready: "Projeto em ZP do Convento de Cristo, Tomar → Parecer DGPC obrigatório (prazo: 30-60 dias, vinculativo). SCIE categoria 2ª → Parecer Bombeiros Tomar (30 dias). ITED → ANACOM. Total pipeline externo estimado: 60-90 dias antes de aprovação final."

---

### Gate 4 — Timelines e custos com dados concretos do município

- [ ] Timeline total estimada (procedimento + entidades + prazo câmara) em dias/semanas
- [ ] Taxas municipais referenciadas por nome (ex: "TMU Lisboa tabela 2024") ou estimativa range €
- [ ] RERU mencionado e aplicabilidade avaliada (reabilitação urbana, ARU, edifício pré-1990)
- [ ] Eventuais suspensões de prazo (art.24 RJUE) identificadas se parecer externo bloqueante

❌ NOT delivery-ready: "O processo pode demorar vários meses e há taxas a pagar."
✅ Delivery-ready: "Comunicação prévia Porto, renovação interior 120m²: prazo câmara 20 dias úteis (tacit approval). Taxas estimadas CM Porto: €800–1.400 (tabela municipal 2024, base m² + coeficiente uso). RERU aplicável se edifício em ARU Baixa do Porto → isenção IMT + desconto taxas. Timeline total estimada: 6–10 semanas (incluindo preparação dossier)."

---

### Gate 5 — RERU / regimes especiais avaliados explicitamente

- [ ] RERU applicability declarada (sim/não + justificação: edifício em ARU? pré-1990? reabilitação ≥ 25% valor?)
- [ ] Se RERU aplicável: isenções listadas (IMT, IMI, taxas municipais, IVA 6%)
- [ ] PDM constraints identificados (índice de construção, cércea, recuos) se nova construção ou extensão
- [ ] Regime simplificado art.6 descartado ou confirmado com artigo exato

❌ NOT delivery-ready: "Verifique se há benefícios fiscais para reabilitação."
✅ Delivery-ready: "Edifício 1967, Rua do Almada 55, Porto (ARU Centro Histórico confirmada) → **RERU aplicável**. Benefícios: IVA 6% na obra, isenção IMT na venda pós-reabilitação, isenção IMI 3 anos (renovável 5). Condição: reabilitação atingir nível 'médio' (MANR). Arquiteto deve emitir ficha de avaliação NRAU antes de submissão."

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets placeholder

- [ ] Nenhum `<nome do cliente>`, `<município>`, `<endereço>`, `<área m²>` no output final
- [ ] Morada ou referência de localização real presente (município + freguesia, ou endereço)
- [ ] Técnicos/entidades referenciados com nomes concretos quando disponíveis (ex: "CM Lisboa — portal LisboaOnline")
- [ ] Datas ou anos de referência legislativa explícitos (ex: "DL 163/2006 acessibilidades", "RJUE art.4, redação 2023")

❌ NOT delivery-ready: "Para o projeto de `<cliente>` em `<município>`, serão necessários os seguintes documentos..."
✅ Delivery-ready: "Para Cuidai — reabilitação Rua Padre António Vieira 12, Lisboa (Estrela): procedimento Comunicação Prévia CM Lisboa (art.34 RJUE). Submissão via portal Lisboa Urbanismo. Certidão registo predial solicitada a 14 jan 2025 — válida até 14 jul 2025."

---

### 7. Status checklist per data point (Gate 7 — validated FASE 1)

Cada número/nome/fact no output deve ter label EXPLÍCITO:

- 🔵 **verified** — confirmado via RAG/KB dario, legislação RJUE/RGEU publicada, ou dados do cliente já fornecidos
- 🟡 **assumed** — plausível com base no tipo de obra/localização, mas precisa confirmação do cliente antes da entrega
- 🟢 **projection** — prazo/custo estimado por design (variável por município, não verificável sem consulta direta à câmara)

Output checklist upfront mostra ao reader exactamente o que é trust-as-is vs. precisa verificar. **Honest transparency > inflated delivery.**

---

❌ NOT delivery-ready:
> "Procedimento: Comunicação Prévia. Prazo: 20 dias. Taxa: €850. Documentos: projecto de arquitectura + especialidades."
> *(Reader assume que tudo está verificado — município, isenções RERU, taxa real e prazo não foram confirmados.)*

✅ Delivery-ready:
> - 🔵 **verified** — Comunicação Prévia aplicável: renovação estrutural sem alteração de fachada (art.34 RJUE)
> - 🟡 **assumed** — Projeto não está em Zona de Protecção (ZP); cliente confirmou "sem monumento próximo" mas DGPC não consultado
> - 🟡 **assumed** — Isenção RERU aplicável: edifício pré-1951 conforme declarado, mas certidão predial ainda não vista
> - 🟢 **projection** — Prazo tácito: 20 dias úteis (art.36 RJUE); câmaras como Lisboa/Porto frequentemente excedem — contar 30-45 dias reais
> - 🟢 **projection** — Taxa estimada: €600–€1.200 (base tabela municipal média); valor exacto depende do regulamento municipal vigente

---

**Ship checklist post-cliente-sync:**
- [ ] Todos os itens 🟡 confirmados — ZP/DGPC verificado, certidão predial revista, legitimidade do requerente confirmada
- [ ] Todas as citações 🔵 adicionadas com referência ao artigo RJUE/RGEU ou resultado RAG correspondente
- [ ] Todos os prazos e taxas 🟢 comunicados ao cliente como estimativas — substituir com tabela de taxas do município específico antes de submissão

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## Licenciamento — Atrium Escritórios, Rua Castilho 39, Lisboa (Marquês de Pombal)

**Projeto:** Alteração interior + mudança de uso (residencial → escritórios), 3º andar, 210 m²
**Edifício:** 1958 (pré-1990) | Sem zona de proteção | PDM Lisboa: solo urbano consolidado
**RERU:** Aplicável (ARU Avenidas Novas, edifício pré-1990, intervenção > 25% valor)

---

### Procedimento determinado: Autorização de Utilização (art.62 RJUE) + Comunicação Prévia (art.34)

- Obras interiores sem alteração de fachada → **Comunicação Prévia**
- Mudança de uso residencial → serviços → **Autorização de Utilização** obrigatória após obras
- Prazo tacit approval câmara: **20 dias úteis**
- Prazo autorização utilização: **10 dias úteis** (art.64 RJUE)

---

### Checklist de documentos — Comunicação Prévia CM Lisboa

**Documentos base**
- [ ] Requerimento portal Lisboa Urbanismo (formulário CP-2024)
- [ ] Certidão Registo Predial — solicitar Conservatória Lisboa 3 (válida 6 meses)
- [ ] Caderneta Predial Urbana — Finanças Lisboa (artigo urbano U-4421-Lisboa)
- [ ] Cópia escritura / procuração Atrium Gestão Lda (legitimidade requerente)
- [ ] Fotografias estado atual — datadas, mínimo 12 fotos interiores + 4 fachada

**Projeto de Arquitetura** (Arq. Sofia Mendes, OA nº 34.221)
- [ ] Memória descritiva e justificativa (inclui justificação PDM: uso serviços permitido ZU consolidado)
- [ ] Plantas piso 3 — estado atual e estado proposto, escala 1:50
- [ ] Alçados (não há alteração exterior — declaração expressa na memória)
- [ ] Cortes longitudinal e transversal, escala 1:50
- [ ] Mapa de áreas: ABC 210 m² | AU 187 m² | implantação n/a
- [ ] Mapa de acabamentos
- [ ] Estimativa orçamental: €148.000 (base certidão fiscal)
- [ ] Declaração autora + Termo de Responsabilidade OA
- [ ] Seguro RC Arq. Sofia Mendes — apólice Fidelidade nº 2024-ARQ-8841 (válida dez 2025)

**Especialidades necessárias para este projeto**
- [ ] Instalações elétricas (ITED) — Eng. Paulo Ramos, OE nº 52.109
- [ ] Comportamento térmico REH — Perito ADENE certificado (cert. nº PT-QAI-0334)
- [ ] Acústica RRAE — obrigatório mudança de uso para serviços (DL 96/2008)
- [ ] Segurança contra incêndios SCIE — uso serviços 2ª categoria (> 1.000 m² ou > 2 pisos) → **Parecer Bombeiros Lisboa obrigatório**
- [ ] Acessibilidades DL 163/2006 — verificar rampas e instalações sanitárias adaptadas

**Especialidades NÃO necessárias**
- ~~Estruturas~~ — sem alterações estruturais (declaração arquiteta)
- ~~Gás~~ — sem instalações de gás no projeto
- ~~AVAC~~ — sistema split individual, não central

---

### Entidades externas

| Entidade | Motivo | Prazo | Portal / Contacto |
|---|---|---|---|
| Bombeiros Lisboa | SCIE 2ª categoria | 30 dias | requerimentos@bombeiros-lisboa.pt |
| ANACOM | ITED telecomunicações | 15 dias | anacom.pt/ited |
| CM Lisboa — DAU | Aprovação CP | 20 dias úteis | lisboaurbanismo.pt |

→ **Sem DGPC** (não é zona de proteção)
→ **Sem CCDR** (perímetro urbano consolidado)

---

### Regime RERU — Benefícios Aplicáveis

✅ Edifício em ARU Avenidas Novas (Deliberação CM Lisboa 523/2019)
✅ Construção 1958 (pré-1990)
✅ Intervenção estimada €148.000 > 25% valor patrimonial (VPT: €390.000 → limiar RERU: €97.500)

**Benefícios confirmados:**
- IVA 6% sobre obras de reabilitação (vs. 23% standard)
- Isenção IMI 3 anos (renovável até 5) após conclusão
- Isenção IMT se venda/transmissão no prazo de 3 anos pós-reabilitação
- **Ação necessária:** Arq. Sofia Mendes emite ficha NRAU antes de submissão; nível mínimo "médio" exigido

---

### Timeline estimada

| Fase | Duração | Data estimada |
|---|---|---|
| Preparação dossier | 3 semanas | até 10 fev 2025 |
| Submissão CM Lisboa | — | 11 fev 2025 |
| Parecer Bombeiros | 30 dias | 13 mar 2025 |
| Tacit approval CP | 20 dias úteis | 11 mar 2025 |
| Início obras | — | 17 mar 2025 |
| Conclusão obras (estimada) | 12 semanas | 9 jun 2025 |
| Autorização Utilização | 10 dias úteis | 23 jun 2025 |

**Total: ~20 semanas até ocupação**

---

### Taxas CM Lisboa (estimativa 2024)

- Comunicação Prévia mudança uso: **€1.240** (base: 210 m² × €4,80 coef. serviços tabela CM Lisboa 2024)
- Autorização Utilização: **€380**
- SCIE taxa: **€210**
- **Total estimado: ~€1.830** (excl. honorários técnicos)
```

---

## Output anti-patterns

- Listar "pode precisar de comunicação prévia ou licenciamento" sem determinar qual — o skill existe precisamente para fazer essa determinação com os inputs disponíveis
- Incluir **todas** as especialidades de engenharia por omissão, sem filtrar ao projeto real (e.g., listar gás e AVAC numa renovação de escritório sem esses sistemas)
- Mencionar RERU como "verifique se aplicável" sem avaliar os três critérios concretos (ARU + pré-1990 + limiar 25%)
- Timelines em linguagem vaga ("vários meses", "processo demorado") em vez de semanas/dias úteis por fase
- Omitir autorizações de utilização em projetos com mudança de uso — erro que causa ocupação ilegal
- Pareceres externos listados sem prazo de resposta — impede o cliente de planear o pipeline crítico
- Taxas municipais omitidas ou referenciadas como "consulte a câmara" quando estimativa por m² é calculável
- Não distinguir entre parecer vinculativo (DGPC, ANPC) e não vinculativo — têm implicações contratuais e de prazo completamente diferentes
- Usar `<município>` ou `<nome do cliente>` no output entregue — qualquer placeholder visível é falha imediata de delivery
