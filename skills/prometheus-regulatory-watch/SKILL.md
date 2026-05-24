---
name: prometheus-regulatory-watch
description: Sweep fontes regulatórias PT/BR/EU para mudanças que afectam squads de compliance. RGPD, LGPD, AI Act, DORA, CSRD, novas leis sectoriais. Triggers em "scan regulatorio", "novas leis", "regulatory watch", "RGPD updates", "AI Act updates".
license: SEE-LICENSE
parent_agent: prometheus-director
compliance: [audit_immutable, regulatory_tracking]
category: "Sensor — Regulatory & Compliance"
version: "1.0"
autonomy_tier: 0
---

# PROMETHEUS-REGULATORY-WATCH

**Output only.** Não actualiza skills nem documents legais. Flagga mudanças.

**Squads afectados directamente:** NOMOS (compliance PT), LEX (legal PT), GAIA (ESG/CSRD), AEGIS (cybersec frameworks), MEDIK (healthcare BR), CAMPUS (education BR), ATLAS-FIN (fintech BR+EU).

## Sources monitorados

### EU
- **EUR-Lex** — `eur-lex.europa.eu` (oficial DB de toda legislação UE)
- **EDPB** — `edpb.europa.eu` (RGPD guidelines)
- **EU AI Act updates** — Comissão Europeia + national transpositions
- **EBA / ESMA / EIOPA** — financial supervisors

### Portugal
- **Diário da República** — `dre.pt` (oficial PT)
- **CNPD** — `cnpd.pt` (RGPD nacional)
- **Banco de Portugal** — `bportugal.pt` (banking regs)
- **CMVM** — `cmvm.pt` (capital markets)
- **ANACOM** — telecom
- **ASAE** — food safety
- **DGE** — education
- **IGAC** — direitos autor

### Brasil
- **ANPD** — `gov.br/anpd` (LGPD federal)
- **BCB** — `bcb.gov.br` (banking + PIX rules)
- **CVM** — `gov.br/cvm` (capital markets)
- **ANS** — `gov.br/ans` (healthcare insurance)
- **ANVISA** — `gov.br/anvisa` (sanitary)
- **CFM** — `cfm.org.br` (medical resolutions)
- **MEC** — `gov.br/mec` (education)
- **Receita Federal** — `gov.br/receitafederal` (tax)

### USA (selective — só se afecta clientes US como Atrium Golden Visa)
- **SEC** — investor disclosure
- **FinCEN** — AML
- **FTC** — consumer protection / privacy

## Workflow

```
1. Para cada source:
   a. Fetch latest publications/decisions (last 7 days)
   b. Identify type: lei nova / regulamento / orientação / multa / consulta pública

2. Filter por keywords relevantes:
   - "inteligência artificial" / "IA" / "AI"
   - "proteção de dados" / "privacy"
   - "criptoativos" / "crypto"
   - "Open Banking" / "PIX rules"
   - "cybersecurity" / "resiliência operacional"
   - "ESG" / "CSRD" / "sustentabilidade"
   - "telemedicina" / "saúde digital"
   - "ensino à distância" / "EAD"

3. Cross-reference com squad coverage:
   - Mudança RGPD → afecta NOMOS, LEX-LGPD, AEGIS-iam
   - Mudança AI Act → afecta NOMOS-eu-ai-act-pt
   - Mudança LGPD → afecta LEX-LGPD, MEDIK-lgpd-healthcare, ATLAS-FIN-lgpd-financial
   - Mudança PIX → afecta ATLAS-FIN-pix-rules-bcb
   - etc.

4. Para cada mudança:
   a. Aplicar tag:
      - 🔥 HIGH — mandatory compliance update, deadline conhecido
      - ⚠️ MEDIUM — recomendação ou orientação não-vinculante
      - 💤 LOW — informacional

5. Output: digests/YYYY-WW-regulatory.md
6. Update state/regulatory_state.yaml
```

## Sources commands

```bash
# Diário da República PT — feed RSS
curl -s "https://dre.pt/rss?serie=1A&dataPublicacaoInicio=2026-05-13" \
  | xmlstarlet sel -t -m "//item" -v "title" -o "|" -v "pubDate" -n

# ANPD BR — últimas publicações (RSS)
curl -s "https://www.gov.br/anpd/pt-br/assuntos/noticias/RSS" \
  | xmlstarlet sel -t -m "//item" -v "title" -n

# EUR-Lex — feed de novidades AI Act
curl -s "https://eur-lex.europa.eu/EN/legal-content/glossary/artificial-intelligence-act.html"

# CNPD orientações
curl -s "https://www.cnpd.pt/decisoes/orientacoes/" \
  | grep -oE 'href="[^"]+\.pdf"' | head -10

# EDPB recent decisions
curl -s "https://www.edpb.europa.eu/news/news_en"
```

## Signal filter — squad mapping

| Mudança detectada | Squad(s) afectado(s) | Default tag |
|---|---|---|
| RGPD enforcement action grande (€>1M fine) | NOMOS, LEX-LGPD | ⚠️ |
| EDPB new guidelines on agents/AI | NOMOS, AEGIS | 🔥 |
| AI Act delegated act / standard | NOMOS-eu-ai-act-pt | 🔥 |
| LGPD ANPD sanção significativa | LEX-LGPD | ⚠️ |
| BCB new PIX/Open Banking rule | ATLAS-FIN-pix-rules-bcb | 🔥 |
| CVM new crypto/tokenization regulation | ATLAS-FIN, KIRION-fii-br | 🔥 |
| ANS new healthcare data rule | MEDIK-ans-compliance | 🔥 |
| MEC EAD regulation update | CAMPUS-ead-regulation | ⚠️ |
| DORA implementing technical standards | NOMOS-dora-resilience, AEGIS | 🔥 |
| CSRD ESRS standard updates | GAIA-csrd-reporting | ⚠️ |
| Generic news / opinion piece | — | 💤 |

## State file

`~/.claude/orchestrator/prometheus/state/regulatory_state.yaml`:

```yaml
last_scan: "YYYY-MM-DDTHH:MM:SS+00:00"
sources_scanned: [dre, anpd, edpb, bcb, eur-lex]
findings_this_week: []
critical_pending:  # 🔥 sem resolução ainda
  - id: "RG-2026-W18-001"
    source: "EUR-Lex"
    description: "AI Act art. 53 implementing rules published"
    affects: [NOMOS-eu-ai-act-pt]
    deadline: "2026-08-01"
    status: "user_review_pending"
```

## Compliance gates active

A skill respeita estes gates do orchestrator (`ethical_gate`):
- Não invoca em jurisdições não-cobertas (e.g. China regulatory) sem pedido explícito
- Não cita full text de leis — só links + summary (copyright laws)
- Flag para `audit_immutable` qualquer finding 🔥

## Output exemplo

```markdown
## prometheus-regulatory-watch — 2026-W21

Scanned: 12 sources · 23 publications · 3 flagged after filter

### 🔥 HIGH
- **EU AI Act — Art. 53 implementing rules** (EUR-Lex, 2026-05-17)
  - Source: Regulamento (UE) 2026/XXX
  - Summary: Standards técnicos para GPAI models risk classification
  - Affects: NOMOS-eu-ai-act-pt, AEGIS-ai-security
  - Deadline compliance: 2026-08-01 (90 dias)
  - Action: review NOMOS skill, update risk classification rubric

- **ANPD — Resolução CD/ANPD nº 23/2026** (gov.br/anpd, 2026-05-15)
  - Summary: Tratamento de dados pessoais por agentes de IA
  - Affects: LEX-LGPD, MEDIK-lgpd-healthcare
  - Deadline: vigência imediata
  - Action: review compliance gates em skills médicas/financeiras

### ⚠️ MEDIUM
- CNPD orientação 2026/05 sobre cookies consent — minor refinement
- BCB Circular sobre Open Finance — afecta ATLAS-FIN

### 💤 LOW
- 18 publicações administrativas / partidárias (counted, not detailed)
```

## Cross-references

[[prometheus-director]] · [[nomos-rgpd-pt-marker]] · [[nomos-eu-ai-act-pt]] · [[lex-lgpd]] · [[atlas-fin-pix-rules-bcb]]


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **prometheus-regulatory-watch** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in prometheus-regulatory-watch:**

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
