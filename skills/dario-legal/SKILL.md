---
name: dario-legal
description: "Legal & compliance for agencies and clients — client contracts (prestacao servicos), NDAs, RGPD/GDPR compliance, terms of service, privacy policy, IP protection, PT labor law, dispute resolution, digital agency specific clauses. Triggers on: 'contrato', 'contract', 'legal', 'RGPD', 'GDPR', 'privacy policy', 'terms of service', 'NDA', 'propriedade intelectual', 'IP', 'termos e condicoes', 'dispute'."
license: MIT
---

# DARIO Legal — Contracts, Compliance & Protection

## When to activate

- Client contract needed (prestacao de servicos)
- NDA before sharing sensitive data
- RGPD/GDPR compliance audit or documentation
- Terms of service / privacy policy for website
- IP ownership clarification (who owns what the AI generates?)
- Freelancer/subcontractor agreement
- Client dispute or late payment
- PT labor law questions

## Workflow

### 1. RAG Consult
```
mcp__dario-rag__search_kb(query: "contract legal RGPD compliance portuguese law", collection: "dario", limit: 5)
```

### 2. Identify Document Type

| Request | Document | PT Law Reference |
|---|---|---|
| "Contrato com cliente" | Contrato de Prestacao de Servicos | Codigo Civil Art. 1154+ |
| "NDA" | Acordo de Confidencialidade | Codigo Civil Art. 227 (boa fe) |
| "RGPD compliance" | Politica de Privacidade + DPO assessment | RGPD (EU 2016/679) + Lei 58/2019 |
| "Terms of service" | Termos e Condicoes de Uso | DL 7/2004 (comercio electronico) |
| "Privacy policy" | Politica de Privacidade | RGPD Art. 13-14 |
| "IP do trabalho" | Clausula de PI no contrato | Codigo Direito Autor Art. 14 |
| "Contrato freelancer" | Contrato de Prestacao de Servicos (PJ) | Codigo do Trabalho Art. 12 |
| "Cobranca" | Carta de interpelacao | Codigo Civil Art. 805 |

### 3. Generate Document

#### Contrato de Prestacao de Servicos (Template Agency)

Clausulas obrigatorias:
1. **Identificacao das partes** — NIF, morada, representante legal
2. **Objecto** — Servicos a prestar (descricao detalhada)
3. **Prazo** — Duracao, renovacao, denuncia (aviso previo 30 dias)
4. **Preco e pagamento** — Valor, faseamento, prazo pagamento (30 dias)
5. **Obrigacoes do prestador** — Deliverables, prazos, SLA
6. **Obrigacoes do cliente** — Fornecer conteudos, feedback em X dias, acessos
7. **Propriedade intelectual** — Transferencia apos pagamento integral
8. **Confidencialidade** — Dados do cliente, estrategias, acessos
9. **RGPD** — Responsavel pelo tratamento, subcontratantes, DPA
10. **Responsabilidade** — Limitacao, forca maior, exclusoes
11. **Resolucao** — Incumprimento, justa causa, consequencias
12. **Foro** — Comarca competente
13. **Anexos** — Proposta comercial, SLA, lista de deliverables

#### RGPD Compliance Kit

1. **Politica de Privacidade** (website) — Art. 13/14 RGPD
   - Responsavel pelo tratamento (nome, contacto, NIF)
   - Finalidades (marketing, analytics, contacto)
   - Base legal (consentimento, interesse legitimo, contrato)
   - Prazo de conservacao
   - Direitos do titular (acesso, rectificacao, apagamento, portabilidade)
   - Cookies (remissao para politica de cookies)
   - Subcontratantes (Google Analytics, hosting, email)

2. **Politica de Cookies** — DL 7/2004 + RGPD
   - Categorias (necessarios, funcionais, analytics, marketing)
   - Banner de consentimento (opt-in, nao opt-out)
   - Como desactivar

3. **DPA (Data Processing Agreement)** — Art. 28 RGPD
   - Entre agencia e cliente quando agencia trata dados pessoais do cliente
   - Medidas tecnicas e organizativas
   - Subcontratantes autorizados
   - Notificacao de violacao (72h)

4. **Registo de Actividades de Tratamento** — Art. 30 RGPD
   - Obrigatorio para >250 funcionarios OU tratamento regular de dados
   - Recomendado para todos

#### NDA (Acordo de Confidencialidade)

- Bilateral (ambas as partes protegidas)
- Definicao de informacao confidencial
- Exclusoes (dominio publico, desenvolvimento independente)
- Duracao: 2-5 anos apos fim da relacao
- Penalizacao: clausula penal (valor fixo por violacao)
- Foro competente

#### Contrato Freelancer / Subcontratante

- Natureza juridica: prestacao de servicos (nao subordinacao)
- Indicadores de nao-subordinacao (Art. 12 CT): horario flexivel, meios proprios, multiplos clientes
- Retencao na fonte IRS (se aplicavel)
- Seguro responsabilidade civil (recomendado)
- IP: trabalho pertence ao contratante apos pagamento
- RGPD: freelancer como subcontratante (DPA necessario)

### 4. IP & AI-Generated Content

Clausulas especificas para agencias que usam IA:

```
PROPRIEDADE INTELECTUAL — CONTEUDO GERADO POR IA

1. O PRESTADOR utiliza ferramentas de inteligencia artificial como 
   auxiliar na criacao de conteudos, designs, e materiais estrategicos.

2. Todo o conteudo final entregue ao CLIENTE e revisado, curado, e 
   validado por profissionais humanos do PRESTADOR antes da entrega.

3. A propriedade intelectual dos deliverables finais transfere-se para 
   o CLIENTE apos pagamento integral, nos termos da clausula [X].

4. O PRESTADOR nao garante exclusividade sobre elementos gerados por 
   IA que possam ser reproduzidos por terceiros usando ferramentas 
   similares (ex: sugestoes de copy, estruturas de schema markup).

5. Elementos de marca (logotipos, brand guidelines, naming) criados 
   especificamente para o CLIENTE sao propriedade exclusiva do CLIENTE.
```

### 5. Dispute / Late Payment

Sequencia de cobranca PT:

1. **Dia 31 (1 dia apos vencimento):** Email amigavel de reminder
2. **Dia 45:** Segundo email + telefonema
3. **Dia 60:** Carta de interpelacao formal (email + carta registada)
4. **Dia 90:** Aviso de suspensao de servicos + juros de mora (Art. 806 CC)
5. **Dia 120:** Injuncao (procedimento europeu de cobranca) ou CIMALT/Julgados de Paz
6. **Alternativa:** Cessao de credito a empresa de cobranca

Taxa de juros de mora comercial (2026): consultar Banco de Portugal (taxa BCE + 8pp)

## Output Format

Todos os documentos legais incluem:
- Header com identificacao das partes
- Numeracao de clausulas
- Linguagem juridica PT (nao brasileira)
- Nota: "Este documento e um modelo orientativo. Recomenda-se validacao por advogado."
- Data e local para assinatura

## Red Flags

- NUNCA apresentar documentos legais como substituto de aconselhamento juridico
- NUNCA omitir clausula RGPD em contratos que envolvam dados pessoais
- NUNCA usar modelos BR para contratos PT (legislacao diferente)
- Sempre incluir clausula de PI quando ha IA envolvida
- Sempre recomendar seguro de responsabilidade civil profissional
