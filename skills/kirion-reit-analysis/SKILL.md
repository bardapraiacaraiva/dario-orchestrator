---
name: kirion-reit-analysis
description: REIT/FII analysis — NAV, dividend yield, leverage, FFO/AFFO, premium/discount. Triggers em "REIT", "FII", "NAV", "dividend yield", "FFO", "AFFO", "FII BR", "REIT US".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [cvm_compliance, anbima_alignment]
---

# KIRION-REIT-ANALYSIS

## Métricas chave
- **NAV (Net Asset Value):** Assets - Liabilities (per share)
- **Premium/Discount to NAV:** Stock price vs NAV ratio
- **FFO (Funds From Operations):** Net Income + Depreciation - Gains
- **AFFO (Adjusted FFO):** FFO - Capex maintenance
- **Dividend yield:** Annual dividend / Stock price
- **Payout ratio:** Dividend / FFO (target 70-90%)
- **Leverage:** Debt / Total Assets (target 30-50%)
- **WACC:** debt + equity cost weighted

## Tipos REITs/FIIs
- **Equity REITs:** direct ownership (residential, office, retail)
- **Mortgage REITs:** lender (interest rate sensitive)
- **Hybrid:** mix
- **FII tijolo (BR):** own property
- **FII papel (BR):** debt securities (CRIs, LCIs)
- **FII fundo de fundos (BR):** invest in other FIIs

## Marcos
- **BR FII:** Lei 8.668/93 + CVM Resolução 175
- **US REIT:** IRS Code Sec. 856 (90% distribution requirement)
- **PT SIIC equivalent:** SICAFI (Lei 26/2018)

## Templates
1. REIT/FII screening model
2. NAV calculation methodology
3. FFO/AFFO bridge
4. Peer comparison matrix
5. Distribution sustainability analysis
6. Premium/discount historical chart

## Cross-references
- [[kirion-dcf-property]] · [[kirion-build-to-rent]] · [[zenith-ma-evaluation]]
