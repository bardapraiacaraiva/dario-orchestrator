---
name: kirion-mortgage-underwriting
description: Mortgage underwriting BR/PT — DTI, LTV, qualifying ratios, credit risk. Triggers em "mortgage underwriting", "DTI", "LTV", "qualifying ratios", "credit risk mortgage", "Crédito Habitação PT", "Crédito Imobiliário BR".
license: SEE-LICENSE
parent_agent: kirion-director
compliance: [audit_immutable]
---

# KIRION-MORTGAGE-UNDERWRITING

## Métricas chave
- **LTV (Loan-to-Value):** Loan / Property value
- **DTI (Debt-to-Income):** Monthly debt / Monthly income
- **Front-end ratio (PT):** Mortgage / Income (≤ 30% target)
- **Back-end ratio:** Total debt / Income (≤ 36-43% target)
- **DSCR (commercial):** NOI / Debt service (≥ 1.25x)
- **PITI:** Principal + Interest + Taxes + Insurance

## BR specifics
- **SBPE:** Sistema Brasileiro Poupança Empréstimo (savings-backed)
- **FGTS:** programa Casa Verde Amarela (replacement Minha Casa Minha Vida)
- **Pró-Cotista FGTS:** subsidized rates
- **Carteira hipotecária:** Bacen reporting required

## PT specifics
- **DSTI cap:** 50% Banco de Portugal Macroprudential
- **LTV cap:** 90% for primary residence (Banco de Portugal)
- **Maturity cap:** 40 years (35 for second home)
- **Spread + Euribor 6M/12M** standard pricing
- **Crédito habitação custos:** notarial + IMT + IS

## Templates
1. Pre-approval calculator (BR + PT)
2. Underwriting checklist
3. Income verification protocols
4. Credit score interpretation (Banco Portugal score)
5. Documento documentos requeridos
6. Risk-based pricing matrix

## Cross-references
- [[kirion-real-estate-valuation]] · [[atlas-fin-kyc-onboarding]] · [[nomos-bdp-banking-pt]]
