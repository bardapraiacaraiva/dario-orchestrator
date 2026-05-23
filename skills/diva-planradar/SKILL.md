---
name: diva-planradar
description: "PlanRadar integration for construction inspection management. Generates PlanRadar-compatible inspection tickets, punch lists in CSV/JSON for import, webhook configurations, and structured field reports. Bridges DIVA inspection workflows with PlanRadar's mobile-first platform. Triggers on \"planradar\", \"inspection export\", \"exportar inspeccao\", \"tickets obra\", \"field report\", \"relatorio obra digital\", \"punch list export\"."
user-invokable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - WebFetch
---

# DIVA PlanRadar — Construction Inspection Integration

Bridge between DIVA's inspection workflows and PlanRadar's field management platform. Generates structured data for import, configures webhooks, and creates inspection templates compatible with PlanRadar's ticket system.

## When to activate

Invoke `/diva-planradar` when:
- User wants to export DIVA inspection data to PlanRadar
- User needs PlanRadar ticket templates for construction phases
- User wants to set up PlanRadar for a new project
- User needs CSV/JSON punch list export for PlanRadar import
- User wants webhook configuration for automated reporting

Do NOT use when:
- User just needs an inspection checklist (use `/diva-inspection`)
- User doesn't have PlanRadar account

## PlanRadar Architecture

### Ticket System (core unit)
Each defect/task = 1 ticket containing:
- Title, description, location (on floor plan)
- Status: Open → In Progress → Resolved → Verified
- Priority: Low / Medium / High / Critical
- Category (customizable per project)
- Assignee (subcontractor/team member)
- Due date
- Photos (attached, georeferenced)
- Form fields (custom per template)

### API Integration
- REST API: `https://www.planradar.com/api/v1/`
- Auth: API key (Settings → Integrations → API)
- Webhooks: `https://www.planradar.com/api/v1/webhooks`
- Events: ticket_created, ticket_updated, photo_attached, status_changed
- Export: PDF reports, CSV data, photo packages

## Workflow

### 1. Project Setup Template

Generate PlanRadar project configuration:

```json
{
  "project": {
    "name": "[Project Name]",
    "address": "[Morada completa]",
    "type": "renovation|new_build|rehabilitation",
    "phases": [
      "01_demolicao",
      "02_estrutura", 
      "03_alvenaria",
      "04_impermeabilizacao",
      "05_mep_roughin",
      "06_acabamentos",
      "07_carpintaria",
      "08_equipamentos",
      "09_final_inspection"
    ],
    "ticket_categories": [
      "Estrutural",
      "Alvenaria",
      "Impermeabilizacao",
      "Electricidade",
      "Canalizacao",
      "AVAC",
      "Pavimentos",
      "Revestimentos",
      "Carpintaria",
      "Pintura",
      "Caixilharia",
      "Louca_Sanitaria",
      "Seguranca_SHST",
      "Limpeza",
      "Outro"
    ],
    "custom_fields": [
      {"name": "fase_obra", "type": "dropdown", "values": ["phases list"]},
      {"name": "norma_referencia", "type": "text"},
      {"name": "tolerancia", "type": "text"},
      {"name": "custo_estimado_correccao", "type": "number"},
      {"name": "prazo_correccao_dias", "type": "number"},
      {"name": "severidade_diva", "type": "dropdown", "values": ["CRITICO","IMPORTANTE","MENOR","COSMETICO"]},
      {"name": "foto_obrigatoria", "type": "checkbox"},
      {"name": "requer_engenheiro", "type": "checkbox"}
    ],
    "team": [
      {"role": "fiscal", "permissions": "admin"},
      {"role": "director_obra", "permissions": "edit"},
      {"role": "empreiteiro", "permissions": "edit_assigned"},
      {"role": "dono_obra", "permissions": "view_reports"},
      {"role": "arquitecto", "permissions": "view_comment"}
    ]
  }
}
```

### 2. Generate Inspection Tickets (CSV for import)

Format compatible with PlanRadar CSV import:

```csv
title,description,category,priority,status,assignee,due_date,phase,tolerance,reference_norm,severity,cost_estimate
"Fissura parede WC1","Fissura vertical >0.5mm no canto da janela WC1. Requer investigacao causa.","Alvenaria","High","Open","empreiteiro_geral","2026-05-15","06_acabamentos","0.5mm max","NP EN 13914","IMPORTANTE",150
"Pavimento desnivelado sala","Diferenca de nivel >5mm na juncao sala/corredor. Planeza fora tolerancia.","Pavimentos","Medium","Open","ceramista","2026-05-10","06_acabamentos","+-3mm/2m","NP EN 13813","MENOR",200
"Infiltracao terraco","Mancha humidade no tecto sala, coincidente com terraco superior. Teste estanquidade necessario.","Impermeabilizacao","Critical","Open","impermeabilizador","2026-05-05","04_impermeabilizacao","Zero infiltracao","Sistema Sika","CRITICO",800
```

### 3. Punch List Export (JSON for API)

```json
{
  "punch_list": {
    "project": "[Nome]",
    "inspection_date": "2026-04-21",
    "inspector": "[Nome fiscal]",
    "phase": "09_final_inspection",
    "summary": {
      "total_items": 15,
      "critical": 2,
      "important": 5,
      "minor": 4,
      "cosmetic": 4
    },
    "items": [
      {
        "id": 1,
        "location": "Sala - Parede Norte",
        "description": "Fissura 1.2mm junto ao vao da janela",
        "category": "Alvenaria",
        "severity": "IMPORTANTE",
        "assignee": "empreiteiro_geral",
        "deadline_days": 7,
        "cost_estimate": 150,
        "photo_ref": "IMG_0234",
        "norm": "NP EN 13914",
        "tolerance": "max 0.5mm",
        "status": "Open"
      }
    ]
  }
}
```

### 4. Webhook Configuration

```json
{
  "webhooks": [
    {
      "event": "ticket_status_changed",
      "filter": {"new_status": "Resolved"},
      "action": "notify_fiscal",
      "url": "https://[your-endpoint]/planradar/resolved",
      "note": "Fiscal recebe notificacao quando subempreiteiro marca como resolvido"
    },
    {
      "event": "ticket_created",
      "filter": {"priority": "Critical"},
      "action": "notify_all",
      "url": "https://[your-endpoint]/planradar/critical",
      "note": "Alerta imediato para tickets criticos"
    },
    {
      "event": "ticket_overdue",
      "action": "escalate",
      "url": "https://[your-endpoint]/planradar/overdue",
      "note": "Escalar tickets que passaram deadline"
    }
  ]
}
```

### 5. Weekly Report Template

Gera template de relatorio semanal para exportar de PlanRadar:

```markdown
# Relatorio Semanal de Obra — [Projecto]
## Semana [N] — [Data inicio] a [Data fim]

### Resumo de Tickets
| Status | Esta semana | Acumulado |
|---|---|---|
| Novos | [N] | [N] |
| Resolvidos | [N] | [N] |
| Em atraso | [N] | [N] |
| Abertos | [N] | [N] |

### Tickets Criticos (abertos)
1. [Descricao] — [Responsavel] — Prazo: [data]

### Fase Actual: [fase]
### Progresso: [%]

### Proxima Semana
- [ ] [accao 1]
- [ ] [accao 2]

### Fotos (seleccao)
[exportar do PlanRadar]
```

## Integration with DIVA Skills

| DIVA Skill | PlanRadar Integration |
|---|---|
| `/diva-inspection` | Gera checklist → exporta como tickets CSV |
| `/diva-timeline` | Fases do cronograma → fases PlanRadar |
| `/diva-budget` | Custo estimado correccao → campo custom |

## Save location
`05 - Claude - IA/Outputs/YYYY-MM-DD - [Projecto] - PlanRadar Setup.json`

## Red Flags
- Never create tickets without attaching photos — in Portuguese construction disputes, undocumented defects are considered non-existent, and PlanRadar's photo-first workflow exists precisely to prevent this
- Never skip severity classification (Critico/Importante/Menor/Cosmetico) on any ticket — unclassified items get deprioritized by contractors and slip through recepcao provisoria uncorrected
- Always assign a responsible person (empreiteiro, subempreiteiro, or fiscal) to every ticket — orphaned tickets in PlanRadar accumulate silently and surface only at final inspection when correction costs have multiplied
- Never close a ticket without on-site verification and a follow-up photo — Portuguese contractors frequently mark items "resolvido" without actually completing the remediation, and re-opening is harder than verifying
- Always validate CSV encoding as UTF-8 BOM for Portuguese characters (acentos, cedilhas) — corrupted imports create duplicate categories and break reporting filters
- Never include real API keys or credentials in generated configuration templates — share access through PlanRadar's team invitation system instead

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

### Gate 1 — Tickets têm localização e severidade inequívocas
- [ ] Cada ticket inclui localização específica (piso + divisão + parede/elemento)
- [ ] Severidade DIVA preenchida (CRITICO/IMPORTANTE/MENOR/COSMETICO) — nunca em branco
- [ ] Priority PlanRadar mapeada corretamente: CRITICO→Critical, IMPORTANTE→High, MENOR→Medium, COSMETICO→Low
- [ ] Descrição do defeito tem dimensão/magnitude mensurável (ex: "fissura 1.2mm", não "fissura")
- ❌ NOT delivery-ready: `"location": "quarto"`, `"severity": ""`, `"priority": "TBD"`
- ✅ Delivery-ready: `"location": "Piso 2 — Quarto Suite — Parede Nascente"`, `"severity": "IMPORTANTE"`, `"priority": "High"`

### Gate 2 — CSV/JSON é importável sem erros
- [ ] Headers CSV correspondem exatamente ao schema PlanRadar: `title,description,category,priority,status,assignee,due_date,phase,...`
- [ ] Datas em formato ISO 8601 (`2026-05-15`, nunca `15/05/2026`)
- [ ] Campos numéricos sem unidades embutidas: `150` (não `"150€"`)
- [ ] Strings com vírgulas ou aspas dentro de aspas duplas no CSV
- ❌ NOT delivery-ready: `due_date: "maio 2026"`, `cost_estimate: "800 EUR"`
- ✅ Delivery-ready: `due_date: "2026-05-15"`, `cost_estimate: 800`

### Gate 3 — Categorias e fases alinhadas com o projeto real
- [ ] `ticket_categories` usadas no output existem na configuração do projeto gerada
- [ ] `phase` de cada ticket corresponde a uma das fases definidas em `project.phases`
- [ ] Nenhum ticket usa categoria genérica "Outro" quando a categoria correta existe
- [ ] Empreiteiros/assignees listados correspondem às equipas reais do projeto
- ❌ NOT delivery-ready: `"phase": "acabamentos"`, `"category": "Outro"`, `"assignee": "[subempreiteiro]"`
- ✅ Delivery-ready: `"phase": "06_acabamentos"`, `"category": "Revestimentos"`, `"assignee": "ceramista_silva_lda"`

### Gate 4 — Normas e tolerâncias verificáveis
- [ ] Cada ticket crítico ou importante inclui `norma_referencia` com código real (NP EN, LNEC, Regulamento)
- [ ] Campo `tolerancia` tem valor concreto, não "conforme projeto"
- [ ] Tickets de impermeabilização referenciam sistema/produto específico quando conhecido
- [ ] Tickets estruturais têm flag `requer_engenheiro: true`
- ❌ NOT delivery-ready: `"norm": "conforme projeto"`, `"tolerance": "a definir"`, `"requer_engenheiro": null`
- ✅ Delivery-ready: `"norm": "NP EN 13914-1"`, `"tolerance": "max 0.3mm/m"`, `"requer_engenheiro": true`

### Gate 5 — Webhooks têm endpoints e lógica de notificação reais
- [ ] URLs de webhook não contêm `[your-endpoint]` ou angle-brackets — substituídos por endpoint real ou placeholder explicitamente marcado como TODO
- [ ] Cada webhook tem `event`, `filter` e `action` preenchidos
- [ ] Webhook de tickets Critical inclui canal de notificação (email/SMS/Teams) explícito
- [ ] Nota humana (`note`) em PT explica o fluxo de negócio de cada webhook
- ❌ NOT delivery-ready: `"url": "https://[your-endpoint]/planradar/critical"` entregue sem aviso
- ✅ Delivery-ready: `"url": "https://api.construtora-norte.pt/hooks/planradar/critical"` ou bloco `# TODO: substituir por endpoint real antes de ativar`

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, sem angle-brackets
- [ ] `project.name` é o nome real da obra, não `[Project Name]`
- [ ] `inspector` é nome real do fiscal, não `[Nome fiscal]`
- [ ] `address` é morada real, não `[Morada completa]`
- [ ] Nenhum campo do JSON/CSV contém `< >` ou `[ ]` no output final entregue
- ❌ NOT delivery-ready: `"inspector": "[Nome fiscal]"`, `"project": "[Nome]"`
- ✅ Delivery-ready: `"inspector": "Eng. Ricardo Fonseca"`, `"project": "Reabilitacao Edificio Marques de Pombal 47"`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
## PlanRadar Export — Cuidai Residências | Obra: Unidade Benfica BF-03
**Data de inspeção:** 2026-04-21 | **Fiscal:** Eng. Mariana Esteves | **Fase:** 06_acabamentos

### Project Configuration (JSON)
{
  "project": {
    "name": "Cuidai Benfica BF-03 — Remodelacao Pisos 2 e 3",
    "address": "Rua Conde de Monsaraz 12, 1500-218 Lisboa",
    "type": "rehabilitation",
    "phases": ["05_mep_roughin","06_acabamentos","07_carpintaria","09_final_inspection"],
    "ticket_categories": ["Alvenaria","Pavimentos","Revestimentos","Electricidade",
                          "Canalizacao","Carpintaria","Pintura","Louca_Sanitaria","Seguranca_SHST"],
    "custom_fields": [
      {"name": "severidade_diva","type": "dropdown",
       "values": ["CRITICO","IMPORTANTE","MENOR","COSMETICO"]},
      {"name": "requer_engenheiro","type": "checkbox"},
      {"name": "prazo_correccao_dias","type": "number"},
      {"name": "norma_referencia","type": "text"},
      {"name": "custo_estimado_correccao","type": "number"}
    ],
    "team": [
      {"name": "Eng. Mariana Esteves","role": "fiscal","permissions": "admin"},
      {"name": "Carlos Ribeiro","role": "director_obra","permissions": "edit"},
      {"name": "Cerâmicas Norte Lda","role": "empreiteiro","permissions": "edit_assigned"},
      {"name": "Dr. Paulo Cuidai","role": "dono_obra","permissions": "view_reports"}
    ]
  }
}

### Punch List CSV (PlanRadar import-ready)
title,description,category,priority,status,assignee,due_date,phase,tolerance,reference_norm,severity,cost_estimate,requer_engenheiro
"Fissura parede quarto 2.01","Fissura vertical 1.4mm no canto SW do Quarto 2.01, Parede Nascente. Origem provável: retração argamassa.","Alvenaria","High","Open","Cerâmicas Norte Lda","2026-05-02","06_acabamentos","max 0.5mm","NP EN 13914-1","IMPORTANTE",180,false
"Infiltração casa-de-banho 3.02","Mancha humidade 30x20cm no tecto CdB 3.02, coincidente com ramal de esgoto piso 4. Teste de estanquidade urgente.","Canalizacao","Critical","Open","Hidro Fix Lda","2026-04-25","05_mep_roughin","zero infiltração","NP EN 12056-2","CRITICO",950,true
"Desnivelamento pavimento corredor P2","Diferença 6mm na juncao pavimento/soleira Quarto 2.03. Planeza fora tolerância NP.","Pavimentos","Medium","Open","Cerâmicas Norte Lda","2026-05-05","06_acabamentos","±3mm/2m","NP EN 13813","MENOR",220,false
"Porta suite 3.01 não fecha","Folga excessiva 4mm lado fechadura, porta não enclausura. Empenamento aro.","Carpintaria","Medium","Open","Carpintaria Alves & Filhos","2026-05-03","07_carpintaria","folga max 2mm","NP EN 12519","MENOR",90,false
"Extintor em falta piso 3","Ponto de extinção previsto no RSCIE não instalado junto à escada P3. Não-conformidade SHST.","Seguranca_SHST","Critical","Open","Carlos Ribeiro","2026-04-23","06_acabamentos","obrigatório","DL 220/2008 RSCIE","CRITICO",0,false

### Webhook Config
{
  "webhooks": [
    {
      "event": "ticket_status_changed",
      "filter": {"new_status": "Resolved"},
      "action": "notify_fiscal",
      "url": "https://api.cuidai.pt/hooks/planradar/resolved-bf03",
      "note": "Mariana Esteves recebe email quando subempreiteiro marca ticket como resolvido — aguarda verificação presencial em 48h"
    },
    {
      "event": "ticket_created",
      "filter": {"priority": "Critical"},
      "action": "notify_all",
      "url": "https://api.cuidai.pt/hooks/planradar/critical-bf03",
      "note": "Alerta imediato via email para Mariana Esteves + Carlos Ribeiro + Dr. Paulo Cuidai"
    }
  ]
}
```

---

## Output anti-patterns

- Tickets sem localização específica — "sala" em vez de "Piso 2 — Sala de Estar — Parede Norte"
- Datas em formato PT (`15/05/2026`) em vez de ISO 8601 (`2026-05-15`) — CSV não importa
- Severidade DIVA e Priority PlanRadar desalinhadas — CRITICO mapeado para "Medium"
- Campos numéricos com unidades embutidas — `"cost_estimate": "800€"` quebra import numérico
- Normas genéricas ou em branco em tickets críticos — `"conforme projeto"` não é norma verificável
- Angle-brackets no output final entregue — `[Nome fiscal]`, `[your-endpoint]` indicam template não preenchido
- `assignee` genérico — `"empreiteiro"` em vez do nome real da empresa/pessoa responsável
- Webhooks sem `note` explicativa — equipa de obra não sabe o que o trigger faz sem contexto PT
- Punch list sem `summary` de contagens — cliente não consegue avaliar volume de não-conformidades sem totais
- Fase inexistente nas fases do projeto — `"phase": "obra_grossa"` quando o projeto define `"02_estrutura"`
