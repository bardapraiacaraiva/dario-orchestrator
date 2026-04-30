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
