---
name: conta-auditoria
description: Audit preparation — dossier fiscal, working papers, management letter, ROC procedures, internal controls
version: "1.0"
---

# CONTA-AUDITORIA: Preparação de Auditoria e Dossier Fiscal

## Activation Triggers

**PT:** auditoria, dossier fiscal, revisor oficial de contas, ROC, certificação legal, papéis de trabalho, management letter, controlo interno, ISA, testes substantivos
**EN:** audit, audit preparation, statutory audit, working papers, management letter, internal controls, audit file, ROC, ISA, substantive testing

## Context

Portuguese entities above certain thresholds must have statutory audits by a ROC (Revisor Oficial de Contas). The dossier fiscal (fiscal/accounting dossier) is mandatory for all entities with contabilidade organizada, per Art.º 130.º CIRC. Audit follows ISA (International Standards on Auditing) as adopted in Portugal by OROC (Ordem dos Revisores Oficiais de Contas).

## Workflow

### Step 1 — Determine Audit Obligation

**Statutory audit required when 2 of 3 exceeded for 2 consecutive years:**

| Threshold | Value |
|-----------|-------|
| Total balanço (assets) | > €1,500,000 |
| Volume de negócios (revenue) | > €3,000,000 |
| Número médio de empregados | > 50 |

**Always required:** SA (Sociedade Anónima), public entities, regulated entities.

### Step 2 — Dossier Fiscal Contents (Art.º 130.º CIRC)

| Document | Description |
|----------|-------------|
| Relatório de gestão | Management report |
| Balanço | Balance sheet |
| Demonstração de resultados | Income statement |
| DACP | Statement of changes in equity |
| Demonstração fluxos caixa | Cash flow statement |
| Anexo | Notes to financial statements |
| Certificação Legal de Contas | Auditor's report (if applicable) |
| Parecer órgão fiscal | Fiscal board opinion |
| Acta aprovação contas | Minutes approving accounts |
| Balancete analítico (dez) | Detailed trial balance (December) |
| Balancete antes/após encerramento | Pre/post closing trial balance |
| Extractos conta 24 | Tax accounts extracts |
| Modelo 22 (cópia) | IRC return copy |
| Declaração Periódica IVA (dez) | December IVA return |
| Mapa depreciações/amortizações | Depreciation schedule |
| Listagem inventários | Inventory listing |
| Documentos de suporte relevantes | Key supporting documents |

**Deadline:** Dossier must be organized within 3 months of filing deadline.

### Step 3 — Working Papers Preparation

| Area | Working Papers |
|------|---------------|
| Cash & banks | Bank reconciliations, confirmation letters |
| Receivables | Aging analysis, impairment test, circularization |
| Inventories | Count sheets, valuation test, cutoff test |
| Fixed assets | Register, additions/disposals, depreciation recalc |
| Payables | Aging, circularization, cutoff test |
| Tax | IVA/IRC/IRS reconciliation, tax computation review |
| Revenue | Cutoff testing, analytical review, contract review |
| Payroll | Sample testing, SS/IRS reconciliation |
| Provisions | Assessment of contingencies, legal opinions |
| Related parties | Transaction listing, arm's length test |

### Step 4 — Audit Schedule and Coordination

| Phase | Timing | Activities |
|-------|--------|-----------|
| Planning | Oct-Nov (for Dec YE) | Risk assessment, materiality, audit plan |
| Interim audit | Nov-Dec | Internal controls testing, walkthrough |
| Year-end procedures | Dec 31 | Inventory count observation, cutoff |
| Final audit | Jan-Mar | Substantive testing, evidence gathering |
| Completion | Mar-Apr | Review, management letter, opinion |
| Reporting | Apr-May | CLC issuance, presentation to board |

### Step 5 — Key Audit Assertions (ISA)

| Assertion | Tests |
|-----------|-------|
| Existence/Occurrence | Physical inspection, confirmation, vouching |
| Completeness | Cutoff tests, search for unrecorded liabilities |
| Accuracy/Valuation | Recalculation, analytical procedures |
| Rights/Obligations | Document review, legal confirmations |
| Classification | Account analysis, presentation review |
| Cutoff | Transaction testing around year-end |
| Presentation | Statement format compliance with SNC |

### Step 6 — Common Audit Adjustments

| Adjustment | Impact |
|------------|--------|
| Imparidade clientes | Increase loss, reduce receivables |
| Depreciação omitida | Increase expense, reduce asset NBV |
| Acréscimo férias/natal | Increase personnel costs, increase liability |
| Provisão garantias | Increase expense, increase provision |
| Valorização inventários | Adjust CMVMC, adjust inventory |
| Ajuste IVA dedutível | Reclassify from deductible to expense |

### Step 7 — Management Letter

Structure:

```
1. Introdução (scope, period, standards)
2. Deficiências significativas identificadas
   - Finding description
   - Risk / impact
   - Recommendation
   - Management response
3. Observações de melhoria
4. Seguimento de recomendações anteriores
5. Conclusão
```

**Severity levels:**
- **Deficiência significativa:** Must be reported to governance
- **Deficiência material:** Impacts opinion qualification
- **Observação:** Improvement opportunity

## Commands

| Command | Description |
|---------|-------------|
| `conta-audit:dossier <ano>` | Generate dossier fiscal checklist |
| `conta-audit:wps <area>` | Working papers template for area |
| `conta-audit:checklist` | Pre-audit preparation checklist |
| `conta-audit:materialidade <vendas> <ativos>` | Calculate materiality |
| `conta-audit:circularizar <tipo>` | Generate confirmation letters |
| `conta-audit:management-letter` | Management letter template |
| `conta-audit:seguimento` | Follow up on prior year findings |
| `conta-audit:obrigacao <vendas> <ativos> <empregados>` | Check if audit required |

## Output Template

```yaml
audit_preparation:
  entity: "D.A.R.I.O. Lda"
  fiscal_year: 2025
  audit_required: true
  roc: "Dr. Example, OROC #1234"
  dossier_fiscal:
    complete: false
    missing_items:
      - "Mapa depreciações atualizado"
      - "Circularização fornecedores"
      - "Acta aprovação contas"
    deadline: "2026-07-15"
  working_papers:
    areas_complete: ["cash", "payroll", "tax"]
    areas_pending: ["receivables", "inventory", "fixed_assets"]
  materiality:
    overall: 15000.00
    performance: 11250.00
    trivial: 750.00
  prior_findings:
    total: 5
    resolved: 3
    outstanding: 2
  timeline:
    planning: "2025-11-01"
    interim: "2025-12-01"
    final: "2026-02-01"
    completion: "2026-04-15"
```

## Red Flags

- Dossier fiscal not assembled within deadline (fine per Art.º 130.º CIRC)
- Material misstatements discovered late in audit
- Circularization responses with significant differences
- Inventory count not witnessed by ROC
- Related party transactions not disclosed
- Going concern doubts not addressed
- Management letter findings from prior year unresolved
- Internal controls overridden without documentation
- Subsequent events not evaluated (between year-end and CLC date)
- SAF-T data inconsistent with ledger entries

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **conta-relatorios** | Financial statements being audited |
| **conta-encerramento** | Year-end close must be complete before final audit |
| **conta-ativos** | Fixed asset register for depreciation testing |
| **conta-conciliacao** | Bank reconciliations as audit evidence |
| **conta-iva** | IVA reconciliation for tax area audit |
| **conta-irc** | IRC computation review |
| **conta-ap** | Supplier confirmations and aging |
| **conta-facturacao** | Revenue cutoff and completeness testing |
| **conta-lancamentos** | Journal entry testing for unusual entries |
