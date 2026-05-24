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


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **conta-auditoria** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in conta-auditoria:**

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
