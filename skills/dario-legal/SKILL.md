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

## Delivery-ready self-check (run BEFORE delivering to client)

Output é **delivery-ready (90+/100)** se TODAS estas check passam.

---

### Gate 1 — Partes identificadas com dados reais

- [ ] NIF de ambas as partes incluído (não `[NIF_CLIENTE]`)
- [ ] Morada completa (rua, código-postal, freguesia)
- [ ] Representante legal nomeado com cargo
- [ ] Data de celebração preenchida (dia/mês/ano, não `DD/MM/AAAA`)

❌ NOT delivery-ready: `A empresa [NOME_CLIENTE], NIF [NIF], com sede em [MORADA]…`
✅ Delivery-ready: `A empresa Cuidai, Lda., NIF 517 234 890, com sede em Rua Augusta 45, 2.º Dto, 1100-048 Lisboa, representada por Ana Ferreira (Administradora)…`

---

### Gate 2 — Objecto e deliverables específicos ao projecto

- [ ] Serviços descritos sem ambiguidade (não "gestão de marketing digital")
- [ ] Prazos de entrega com datas concretas ou número de dias úteis
- [ ] Revisões incluídas e número máximo definido
- [ ] Exclusões de âmbito explícitas (o que NÃO está incluído)

❌ NOT delivery-ready: `O PRESTADOR compromete-se a prestar serviços de marketing digital conforme acordado.`
✅ Delivery-ready: `O PRESTADOR entregará: (1) 8 publicações/mês para Instagram e LinkedIn; (2) 1 relatório mensal de analytics até dia 5 do mês seguinte; (3) gestão de Google Ads com orçamento máximo de 800 €/mês. Não incluído: criação de website, fotografia ou vídeo.`

---

### Gate 3 — Cláusulas financeiras completas e conformes

- [ ] Valor total ou mensalidade em euros (sem IVA e com IVA separados)
- [ ] Prazo de pagamento (máx. 30 dias — DL 62/2013)
- [ ] IBAN/referência de pagamento incluídos (ou indicação de onde constam)
- [ ] Juros de mora referenciados (Art. 806 CC + taxa BCE vigente)
- [ ] Condição de suspensão de serviços por falta de pagamento

❌ NOT delivery-ready: `O pagamento será efectuado nos termos acordados entre as partes.`
✅ Delivery-ready: `Mensalidade: 1 200 € + IVA 23% = 1 476 € (total). Pagamento até ao dia 8 de cada mês. Em mora, aplicam-se juros à taxa legal comercial vigente (BCE + 8 p.p.). Atraso > 30 dias autoriza suspensão imediata dos serviços.`

---

### Gate 4 — RGPD/IP estruturalmente correcto

- [ ] Base legal de tratamento de dados identificada (Art. 6.º RGPD) por finalidade
- [ ] Prazos de conservação definidos (não "pelo tempo necessário")
- [ ] DPA presente se agência trata dados pessoais do cliente (Art. 28 RGPD)
- [ ] Cláusula de IA: disclaimers de exclusividade e validação humana incluídos
- [ ] Titular de PI pós-pagamento inequivocamente definido

❌ NOT delivery-ready: `Os dados serão tratados em conformidade com o RGPD e conservados pelo prazo legal.`
✅ Delivery-ready: `Base legal: execução de contrato (Art. 6.º/1/b). Dados de contacto conservados 5 anos após fim da relação contratual. Analytics: 26 meses (Google Analytics 4 padrão). Subcontratantes autorizados: Google LLC (Analytics), OVHcloud SAS (hosting). Violação reportada em 72h à CNPD.`

---

### Gate 5 — Foro e resolução de litígios operacionais

- [ ] Comarca competente nomeada (não "foro competente")
- [ ] Sequência de cobrança com dias exactos mapeada (dias 31/45/60/90/120)
- [ ] Prazo de aviso prévio para denúncia do contrato (mín. 30 dias)
- [ ] Mecanismo alternativo referenciado (CIMALT, Julgados de Paz, injunção)

❌ NOT delivery-ready: `Em caso de litígio, as partes recorrerão ao tribunal competente.`
✅ Delivery-ready: `Foro: Comarca de Lisboa. Denúncia: aviso prévio escrito de 30 dias. Cobrança: reminder D+31, interpelação formal D+60 (carta registada), suspensão de serviços D+90, injunção D+120 (Balcão Nacional de Injunções).`

---

### Gate 6 — Output usa NOME DO CLIENTE + dados reais, zero placeholders com angle-brackets

- [ ] Nenhuma string do tipo `[NOME]`, `<EMPRESA>`, `{{NIF}}` no output final
- [ ] Nome do cliente aparece ≥ 3× no documento (cabeçalho, cláusulas, assinatura)
- [ ] Tipo de documento corresponde ao pedido do cliente
- [ ] Versão e data do documento no cabeçalho

❌ NOT delivery-ready: `Entre [PRESTADOR] e [CLIENTE], NIF [___], acorda-se o seguinte…`
✅ Delivery-ready: `Entre Atrium Digital, Lda. (PRESTADOR) e SAQUEI, S.A. (CLIENTE), celebrado em Lisboa a 14 de Julho de 2025…`

---

## Fully-worked A-tier example (delivery-ready reference)

```markdown
# CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE MARKETING DIGITAL
**Versão 1.0 — 14 de Julho de 2025**

---

## PARTES

**PRESTADOR:** Atrium Digital, Lda.
NIF 514 877 302 | Av. da Liberdade 110, 4.º Esq., 1269-046 Lisboa
Representada por: João Matos, Sócio-Gerente

**CLIENTE:** SAQUEI, S.A.
NIF 516 234 711 | Rua do Arsenal 12, 1100-038 Lisboa
Representada por: Mariana Costa, CEO

---

## CLÁUSULA 1 — OBJECTO

O PRESTADOR compromete-se a prestar ao CLIENTE os seguintes serviços mensais:
- Gestão de redes sociais: Instagram e LinkedIn (12 publicações/mês + stories)
- Copywriting para email marketing (4 campanhas/mês, base Mailchimp)
- Relatório de performance mensal (entregue até dia 5 do mês seguinte)
- Gestão de Google Ads — orçamento máximo 1 500 €/mês (não incluído na fee)

**Não incluído:** fotografia, produção de vídeo, redesign de website.
Revisões: até 2 rondas por deliverable. Revisões adicionais: 75 €/hora.

---

## CLÁUSULA 2 — PRAZO

Início: 1 de Agosto de 2025. Duração: 12 meses, renovação automática.
Denúncia: aviso prévio escrito de 30 dias (email para juridico@atrium.pt).

---

## CLÁUSULA 3 — PREÇO E PAGAMENTO

| Item | Valor s/ IVA | IVA 23% | Total |
|---|---|---|---|
| Fee mensal de gestão | 1 800 € | 414 € | 2 214 € |

Pagamento até ao dia 8 de cada mês.
IBAN: PT50 0035 0552 0001 2345 6782 3 (Caixa Geral de Depósitos — Atrium Digital, Lda.)
Em mora (Art. 806 CC + DL 62/2013), aplicam-se juros à taxa BCE + 8 p.p.
Atraso superior a 30 dias autoriza suspensão imediata de serviços sem
necessidade de aviso adicional.

---

## CLÁUSULA 4 — PROPRIEDADE INTELECTUAL E CONTEÚDO IA

4.1 A PI dos deliverables finais transfere-se para o CLIENTE após pagamento
integral da respectiva mensalidade.

4.2 O PRESTADOR utiliza ferramentas de IA (ChatGPT, Claude, Midjourney) como
auxiliares criativos. Todo o conteúdo é revisto e validado por profissionais
humanos antes da entrega.

4.3 O PRESTADOR não garante exclusividade sobre estruturas genéricas geradas
por IA (ex.: copy de produto, sugestões de hashtags). Garantia de exclusividade
aplica-se apenas a elementos de marca criados especificamente para o CLIENTE
(naming, identidade visual, brand voice guidelines).

---

## CLÁUSULA 5 — RGPD E TRATAMENTO DE DADOS

5.1 **Responsável pelo tratamento:** SAQUEI, S.A. (NIF 516 234 711)
**Subcontratante:** Atrium Digital, Lda. — actua nos termos do Art. 28.º RGPD.

5.2 **Finalidades e bases legais:**
- Gestão de campanha publicitária: execução de contrato (Art. 6.º/1/b)
- Analytics de audiência: interesse legítimo (Art. 6.º/1/f)

5.3 **Conservação:** dados de campanha conservados 3 anos após fim do contrato;
dados de faturação 10 anos (obrigação fiscal — Art. 52.º CIVA).

5.4 **Subcontratantes autorizados:** Meta Platforms Ireland Ltd. (anúncios),
Google LLC (Analytics 4, Google Ads), Mailchimp/Intuit Inc. (email marketing).

5.5 Violação de dados pessoais reportada à CNPD em 72 horas (Art. 33.º RGPD).

---

## CLÁUSULA 6 — SEQUÊNCIA DE COBRANÇA (referência operacional)

| Dia | Acção |
|---|---|
| D+1 | Email amigável de reminder |
| D+15 | Segundo email + chamada telefónica |
| D+30 | Carta de interpelação formal (email + correio registado) |
| D+45 | Suspensão de serviços + nota de juros de mora |
| D+75 | Injunção — Balcão Nacional de Injunções (BNI) |

---

## CLÁUSULA 7 — FORO

Comarca de Lisboa. Alternativa: Centro de Informação, Mediação e Arbitragem
de Conflitos de Consumo de Lisboa (CIMAAL) para litígios até 5 000 €.

---

**ASSINATURAS**

Lisboa, 14 de Julho de 2025

___________________________ | ___________________________
João Matos (PRESTADOR) | Mariana Costa (CLIENTE)
Atrium Digital, Lda. | SAQUEI, S.A.
```

---

## Output anti-patterns

- Entregar contrato com `[NOME_CLIENTE]`, `<NIF>` ou `{{MORADA}}` ainda presentes — não é um template, é o documento final
- Omitir IVA na tabela de preços ou misturar valores com/sem IVA sem label clara
- Escrever "nos termos do RGPD" sem identificar base legal, finalidade e prazo de conservação concretos
- Cláusula de PI que não distingue conteúdo IA genérico de elementos de marca exclusivos
- Foro definido como "tribunal competente" sem nomear a comarca
- Sequência de cobrança sem dias exactos (D+31, D+60…) — torna o processo operacionalmente inutilizável
- DPA ausente quando a agência acede a dados pessoais de clientes finais do CLIENTE
- Prazo de conservação de dados como "pelo tempo necessário" — viola Art. 5.º/1/e RGPD
- Cláusula de resolução sem prazo de aviso prévio definido (mínimo legal 30 dias recomendado)
- Documento entregue sem número de versão e data — impossível rastrear em caso de litígio
