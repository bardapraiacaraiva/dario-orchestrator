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
