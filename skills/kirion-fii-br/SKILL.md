---
name: kirion-fii-br
description: FIIs BR — types, CVM regulação, liquidez, taxation, screening. Triggers em "FII", "FII BR", "fundo imobiliário", "CVM 175", "dividend tax exempt FII", "FII tijolo papel".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [cvm_compliance, anbima_alignment]
jurisdiction: Brasil
---

# KIRION-FII-BR

## Marco
- **Lei 8.668/93** — institui FIIs
- **CVM Resolução 175** (2023) — novo marco fundos
- **CVM Instrução 472** (antiga) — supletivamente aplicável
- **Lei 11.033/2004 Art. 3, III:** isenção IR para PF dividendos (50%+ cotistas, >50 cotistas, ≥ 95% pagamento)

## Tipos FII
- **Tijolo (Equity):** direct property (logística, shopping, lajes)
- **Papel (Debt):** CRIs, LCIs (mortgage-backed)
- **FoF (Fund of Funds):** investe em outros FIIs
- **Híbrido:** mix tijolo + papel
- **Desenvolvimento:** greenfield projects

## Segmentos top
- **Logística:** XPLG, HGLG, BTLG (institutional storage)
- **Lajes corporativas:** HGRE, JSRE, PVBI (office)
- **Shoppings:** XPML, HGBS (retail)
- **Residencial:** poucos puros (RBRP, JFLL)
- **Híbridos top:** BTCR, KNRI

## Métricas screening
- **DY (Dividend Yield):** 7-12% típico
- **P/VPA:** Price / Net Asset per share (premium/discount)
- **Vacância física + financeira**
- **WAULT:** Weighted Average Unexpired Lease Term
- **Liquidez diária**

## Templates
1. FII screening dashboard (DY + P/VPA + vacancy)
2. Sector allocation strategy
3. Tax efficiency (PF vs PJ holding)
4. FoF analysis methodology
5. Yield trap detection (ex-dividend cliffs)
6. WAULT analysis lease portfolio

## Cross-references
- [[kirion-reit-analysis]] · [[kirion-dcf-property]] · [[atlas-fin-foreign-exchange]]
