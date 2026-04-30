---
name: diva-briefing
description: Structured client briefing template for architecture, interior design, and construction projects. Captures lifestyle, needs, desires, budget, timeline, style preferences, technical constraints, and regulatory situation. Triggers on "briefing", "brief", "requisitos", "o que o cliente quer", "captar necessidades".
license: MIT
---

# DIVA Skill — Client Briefing

Structured interview and document generator that captures everything needed to start an architecture, interior design, or construction project. Transforms a conversation into a complete, actionable briefing document that serves as the single source of truth for the entire project.

## When to activate

Invoke `/diva-briefing` (or trigger automatically) when:
- User is starting a new project and needs to capture client requirements
- User says "the client wants..." and needs structure
- After a `diva-diagnose` confirms viability, to detail the brief
- User needs a template to send to a client for self-completion
- User is preparing for a first client meeting

Do NOT use when:
- Project already has a complete brief and needs execution
- User needs only a budget or floor plan (use specific skills)
- It's a purely technical question with no client context

## Workflow

### 1. Identify briefing mode
- **Interactive:** Claude asks questions one section at a time, adapts follow-ups
- **Template:** Generate a blank briefing document for the client to fill
- **From notes:** User pastes meeting notes/messages, Claude structures them into the briefing format

Ask which mode the user prefers. Default to interactive if unclear.

### 2. RAG consult
```
mcp__dario-rag__search_kb(query: "architecture briefing client requirements questionnaire", limit: 5)
mcp__dario-rag__search_kb(query: "interior design style preferences lifestyle analysis", limit: 5)
```

### 3. Section A — Identificacao do projecto
- **Client name(s):** who are the decision makers
- **Property address:** full address or location description
- **Property type:** apartment, house, commercial, mixed
- **Current use vs intended use:** residential, commercial, tourism (AL), mixed
- **Ownership:** owned, buying (CPCV signed?), inherited, rented (landlord approval?)
- **Project scope:** cosmetic, medium renovation, full gut, new build, extension
- **Key dates:** possession date, desired completion, hard deadlines (wedding, baby, lease end)

### 4. Section B — Quem vai viver/trabalhar no espaco
- **Household composition:** adults, children (ages), pets, elderly, visitors frequency
- **Daily routines:** morning flow, cooking habits, work-from-home, entertainment
- **Special needs:** mobility, allergies, sensory sensitivities, home office requirements
- **Storage needs:** wardrobes, pantry, garage, hobby storage, seasonal items
- **Future changes:** planning children, aging in place, possible sale in X years

### 5. Section C — Estilo e preferencias
- **Style direction:** modern, contemporary, classico, rustico, industrial, minimalista, mediterraneo, nordico, eclectico
- **Reference images:** ask for Pinterest boards, Instagram saves, magazine clippings
- **Color preferences:** warm/cool palette, specific colors loved/hated
- **Material preferences:** wood (type), stone (type), metal, glass, textiles
- **Lighting mood:** bright and airy, cozy and warm, dramatic, task-oriented
- **Must-haves:** specific elements they dream about (island kitchen, walk-in closet, freestanding bath, fireplace)
- **Absolutely-not:** things they hate or refuse (carpet, wallpaper, open shelving, etc.)

### 6. Section D — Programa funcional (room by room)
For each space, capture:
- **Function:** primary and secondary uses
- **Priority:** essential, desired, nice-to-have
- **Specific requirements:** dimensions, equipment, fixtures
- **Adjacency:** what should be near/far from this space

Standard rooms to cover:
- Entrada/hall
- Sala de estar
- Sala de jantar (or combined)
- Cozinha (open/closed, gas/induction, dishwasher, laundry in kitchen?)
- Suite principal (ensuite requirements)
- Quartos adicionais (function: child, guest, office)
- Casa(s) de banho (bath vs shower, double vanity, bidet)
- Lavandaria/tratamento de roupa
- Arrumos/despensa
- Espaco exterior (varanda, terraco, jardim)
- Garagem/estacionamento
- Home office/estudio
- Other: gym, cinema, wine cellar, etc.

### 7. Section E — Orcamento e prioridades
- **Total budget:** range (min-max), including or excluding fees/furniture
- **Budget breakdown awareness:** do they understand the split (construction vs finishes vs furniture vs fees)?
- **Priority allocation:** where to spend more vs where to save
  - "Invest in kitchen, save on secondary bathroom"
- **Furniture situation:** keeping existing? buying new? mix?
- **Appliance preferences:** brands, built-in vs freestanding
- **Payment capacity:** phased payments? financing? all cash?

### 8. Section F — Condicionantes tecnicas e legais
- **Known structural issues:** from diva-diagnose or own knowledge
- **Infrastructure state:** electrical, plumbing, gas, HVAC
- **Condominium rules:** if apartment, known restrictions
- **Heritage/conservation:** is the building classified?
- **Energy goals:** energy certificate improvement, solar panels, heat pump
- **Smart home:** automation level desired (none, basic, full)
- **Security:** alarm, CCTV, reinforced door, safe

### 9. Section G — Gestao do projecto
- **Decision process:** one person decides, couple, family, committee
- **Communication preference:** email, WhatsApp, video calls, in-person
- **Involvement level:** hands-off (trust the designer), collaborative, very hands-on
- **Previous renovation experience:** first time, experienced, bad past experience
- **Contractor preference:** client has one, needs recommendation, open
- **Living situation during works:** staying, moving out, partial occupation

### 10. Consolidation and validation
- Summarize all captured information
- Highlight gaps or contradictions ("you want premium finishes but budget suggests medium tier")
- Flag unrealistic expectations early
- Confirm priorities ranking with client

## Output template

```markdown
---
project: <client/property>
date: <YYYY-MM-DD>
type: diva-briefing
client: <name>
property: <address/description>
scope: <cosmetic|medium|full-gut|new-build>
budget_range: <min-max EUR>
---

# Briefing DIVA — <Client Name> — <Property>

## A. Identificacao do Projecto
| Campo | Detalhe |
|---|---|
| Cliente | ... |
| Morada | ... |
| Tipologia | ... |
| Uso atual / pretendido | ... |
| Propriedade | ... |
| Ambito | ... |
| Data pretendida conclusao | ... |

## B. Perfil do Utilizador
### Composicao do agregado
### Rotinas diarias
### Necessidades especiais
### Armazenamento
### Evolucao futura

## C. Estilo e Preferencias
### Direcao estilistica
### Referencias visuais
### Paleta de cores
### Materiais preferidos
### Must-haves
### Absolutely-not

## D. Programa Funcional
| Espaco | Funcao | Prioridade | Requisitos especificos |
|---|---|---|---|
| Entrada | ... | Essencial | ... |
| Sala | ... | ... | ... |
| Cozinha | ... | ... | ... |
| Suite | ... | ... | ... |
| Quartos | ... | ... | ... |
| WC | ... | ... | ... |
| Lavandaria | ... | ... | ... |
| Exterior | ... | ... | ... |

## E. Orcamento
| Componente | Range EUR |
|---|---|
| Obra | ... |
| Acabamentos premium | ... |
| Mobiliario | ... |
| Honorarios | ... |
| **Total** | **...** |
### Prioridades de investimento

## F. Condicionantes
### Estruturais
### Infraestruturas
### Legais/condominio
### Energia e sustentabilidade
### Domonica/smart home
### Seguranca

## G. Gestao
| Aspecto | Detalhe |
|---|---|
| Decisor(es) | ... |
| Comunicacao | ... |
| Envolvimento | ... |
| Experiencia anterior | ... |
| Empreiteiro | ... |
| Habitacao durante obra | ... |

## Sintese e Validacao
### Pontos fortes do briefing
### Gaps a esclarecer
### Contradicoes identificadas
### Expectativas a gerir

## Proximos Passos
- [ ] Cliente valida este briefing
- [ ] Seguir com `diva-floor-plan` para estudo de layout
- [ ] Seguir com `diva-materials` para paleta de materiais
- [ ] Seguir com `diva-budget` para orcamento detalhado
```

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - <Client> - Briefing DIVA.md`

## Red flags — don't do this
- Never proceed with design without a validated briefing
- Never assume household composition (always ask)
- Never ignore budget-scope misalignment (flag it immediately)
- Never skip the "absolutely-not" question (avoids costly mistakes)
- Never forget to ask about living situation during works
- Never accept "I don't know my style" — use reference images to guide
- Never let one partner dominate when both are decision makers (capture both views)
- Never ignore future plans (a 2-year plan vs 20-year plan changes everything)

## Interactions
- Usually follows `diva-diagnose` (diagnostic first, then detailed brief)
- Feeds into `diva-floor-plan` for layout development
- Feeds into `diva-materials` for material palette aligned with preferences
- Feeds into `diva-budget` with validated budget expectations
- Save via `dario-obsidian-save` to vault
