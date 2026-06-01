---
name: adriana-docs
description: "ADRIANA Document Management — templates, versioning, naming conventions, archive policies, shared drives, document lifecycle"
version: "1.0"
---

# ADRIANA-DOCS: Gestao Documental

**ADRIANA** = Assistente Digital de Rotinas Internas, Automacao, Normas e Administracao

## Quando Activar

**Trigger words (PT):** documento, template, modelo, versao, nomenclatura, arquivo, pasta partilhada, drive, ciclo documental, ficheiro, nome do ficheiro, organizar documentos, gestao documental
**Trigger words (EN):** document, template, versioning, naming convention, archive, shared drive, document lifecycle, file management, folder structure

Activar quando o utilizador precisa de:
- Criar ou gerir templates de documentos
- Definir convencoes de nomenclatura
- Implementar versionamento de documentos
- Definir politicas de arquivo e retencao
- Organizar drives partilhados ou estrutura de pastas
- Gerir ciclo de vida documental (criacao → revisao → aprovacao → arquivo → destruicao)

## Workflow Passo-a-Passo

### 1. Diagnostico Documental
- Identificar tipo de documento (contrato, proposta, acta, relatorio, SOP, etc.)
- Determinar audiencia (interno, cliente, legal, publico)
- Verificar se ja existe template no sistema
- Avaliar requisitos de retencao (legal, fiscal, operacional)

### 2. Convencao de Nomenclatura
Formato padrao:
```
[DATA]-[TIPO]-[PROJECTO]-[VERSAO].[EXT]
2026-04-27-PROP-ClienteXPTO-v2.1.pdf
2026-04-27-ACTA-ReunSemanal-v1.0.docx
```

Regras:
- Data em formato ISO 8601: YYYY-MM-DD
- Tipo abreviado (max 4 chars): PROP, ACTA, CONT, REL, SOP, FAT, NDA
- Projecto/Cliente em CamelCase sem espacos
- Versao semantica: vMAJOR.MINOR (v1.0, v1.1, v2.0)
- Sem caracteres especiais, acentos ou espacos

### 3. Estrutura de Pastas Padrao
```
📁 [Empresa]/
├── 📁 01-Administracao/
│   ├── Politicas/
│   ├── Contratos/
│   └── Legal/
├── 📁 02-Clientes/
│   └── [NomeCliente]/
│       ├── Propostas/
│       ├── Contratos/
│       ├── Entregas/
│       └── Correspondencia/
├── 📁 03-Projectos/
│   └── [NomeProjeto]/
│       ├── Briefing/
│       ├── WIP/
│       ├── Aprovados/
│       └── Entregues/
├── 📁 04-Financeiro/
│   ├── Facturas/
│   ├── Recibos/
│   └── Relatorios/
├── 📁 05-RH/
├── 📁 06-Marketing/
├── 📁 07-Templates/
└── 📁 99-Arquivo/
```

### 4. Versionamento
| Accao | Versao | Exemplo |
|-------|--------|---------|
| Documento novo | v1.0 | Primeira versao |
| Correcao menor | v1.1 | Typo, formatacao |
| Revisao significativa | v2.0 | Conteudo alterado |
| Draft/rascunho | v0.1 | Em desenvolvimento |
| Final aprovado | vF | Versao final bloqueada |

### 5. Ciclo de Vida Documental
```
CRIACAO → REVISAO → APROVACAO → PUBLICACAO → UTILIZACAO → ARQUIVO → DESTRUICAO
   ↑         ↓
   └── REJEICAO (volta a criacao)
```

Responsabilidades por fase:
- **Criacao:** Autor identifica-se no cabecalho
- **Revisao:** Revisor comenta em 48h uteis
- **Aprovacao:** Aprovador assina (digital ou fisico)
- **Publicacao:** Admin distribui e notifica stakeholders
- **Arquivo:** Mover para 99-Arquivo/ apos 12 meses inactivo
- **Destruicao:** Conforme politica de retencao (ver adriana-archive)

## Tabela de Comandos

| Comando | Descricao |
|---------|-----------|
| `adriana docs template [tipo]` | Gerar template para tipo de documento |
| `adriana docs rename [pasta]` | Renomear ficheiros segundo convencao |
| `adriana docs structure` | Gerar estrutura de pastas padrao |
| `adriana docs audit` | Auditar nomenclatura e organizacao |
| `adriana docs lifecycle [doc]` | Mostrar estado no ciclo de vida |
| `adriana docs version [doc]` | Criar nova versao com changelog |
| `adriana docs search [query]` | Pesquisar documentos por metadados |

## Template de Output

```markdown
## Relatorio Gestao Documental

**Data:** YYYY-MM-DD
**Ambito:** [Empresa/Departamento]

### Metricas
- Total documentos: X
- Documentos sem convencao: X (Y%)
- Templates activos: X
- Documentos para arquivo: X
- Documentos expirados: X

### Accoes Requeridas
1. [ ] [Accao] — Responsavel — Prazo
2. [ ] [Accao] — Responsavel — Prazo

### Estrutura Recomendada
[Arvore de pastas]
```

## Red Flags

- Ficheiros sem data no nome (impossivel rastrear versao)
- Multiplas versoes "final", "final_v2", "final_DEFINITIVO"
- Documentos sensiveis (contratos, NDA) em pastas publicas
- Drives partilhados sem permissoes diferenciadas
- Documentos com dados pessoais sem classificacao RGPD
- Templates desactualizados (>12 meses sem revisao)
- Nomenclatura inconsistente dentro do mesmo projecto
- Documentos criticos sem backup ou redundancia

## Integracao com Outros Skills

| Skill | Integracao |
|-------|-----------|
| **adriana-archive** | Politicas de retencao e destruicao documental |
| **adriana-policies** | Templates de politicas seguem gestao documental |
| **adriana-sop** | SOPs sao documentos geridos por este skill |
| **adriana-meetings** | Actas seguem nomenclatura e arquivo documental |
| **adriana-procurement** | Contratos e POs seguem ciclo documental |
| **adriana-onboarding** | Documentacao de onboarding gerida aqui |
| **dario-legal** | Contratos e NDAs requerem retencao especifica |
| **dario-obsidian-save** | Documentos estrategicos salvos no vault |

## Notas Portugal

- Documentos fiscais: retencao minima 10 anos (Codigo do IRC, Art. 123)
- Contratos de trabalho: retencao 5 anos apos termino
- Facturas e recibos: retencao 12 anos para IVA
- RGPD: documentos com dados pessoais requerem inventario e base legal
- Assinatura digital qualificada: Chave Movel Digital ou cartao cidadao


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **adriana-docs** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in adriana-docs:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
