---
name: atlas-guest
description: "Guest Management & RSVP — database design, invitation strategy, registration, check-in, capacity management, RGPD compliance"
version: "1.0"
---

# atlas-guest — Guest Management & RSVP

## Description
World-class guest management system for events of any scale. Covers database design, RSVP workflows, invitation strategy, registration systems, check-in technology, name badge design, capacity management, communication schedules, accessibility, RGPD compliance, and Portuguese-specific conventions. The definitive reference for managing every guest touchpoint from first invitation to post-event follow-up.

## Trigger Phrases
**EN:** "guest list", "RSVP", "registration", "check-in", "name badges", "invitations", "guest management", "attendee tracking", "waitlist", "capacity", "no-show rate"
**PT:** "lista de convidados", "confirmacao de presenca", "registo", "check-in", "crachas", "convites", "gestao de convidados", "lista de espera", "capacidade"

## When to Activate
- Building or auditing a guest list for any event type
- Designing RSVP or registration workflows
- Planning invitation strategy (physical, digital, hybrid)
- Setting up check-in and on-site registration systems
- Designing name badges or credential systems
- Managing capacity, waitlists, or no-show predictions
- Ensuring RGPD/GDPR compliance for attendee data
- Planning accessibility accommodations for guests
- Coordinating bilingual communications (PT/EN)

---

## Workflow

### Step 1 — Define Guest Database Structure
Build the master guest record with all required fields:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Nome Completo | text | Yes | First + Last (PT: two surnames common) |
| Email | email | Yes | Primary communication channel |
| Telefone | phone | Yes | Include country code (+351) |
| Empresa/Organizacao | text | Conditional | Corporate events |
| Cargo/Titulo | text | Conditional | For badge + protocol |
| Requisitos Alimentares | select | Yes | Vegetariano, vegano, sem gluten, halal, kosher, alergias |
| Necessidades Acessibilidade | text | Yes | Mobilidade, auditiva, visual, outra |
| Estado RSVP | enum | Yes | Pendente, Confirmado, Recusado, Talvez, Sem Resposta |
| Mesa Atribuida | ref | No | Link to seating plan |
| Tier VIP | enum | No | VVIP, VIP, Convidado Honra, Standard |
| Acompanhante(s) | number + text | No | Number + names of plus-ones |
| Notas Internas | text | No | Preferences, protocol notes, conflicts |
| Origem Convite | text | No | Who invited / referral source |
| Idioma Preferido | enum | No | PT, EN, ES, FR |
| Consentimento RGPD | boolean | Yes | Must be explicit |
| Data Confirmacao | date | Auto | Timestamp of RSVP response |

### Step 2 — Execute RSVP Timeline
Follow this proven cadence (adjust for event formality):

| Milestone | Timing | Action |
|-----------|--------|--------|
| Save-the-Date | 12-16 semanas antes | Reserva data, teaser do evento |
| Convite Formal | 8-10 semanas antes | Convite completo com detalhes |
| Deadline RSVP | 3-4 semanas antes | Prazo para confirmacao |
| Follow-up Nao Responderam | 2 semanas antes | Email + telefone para quem nao respondeu |
| Confirmacao Final | 1 semana antes | Email com logistics finais (hora, local, parking, dress code) |
| Lembrete Vespera | 1 dia antes | SMS ou email curto |
| Agradecimento | 1-3 dias depois | Email pos-evento + fotos/survey |

### Step 3 — Design Invitation Strategy

**Convite Fisico:**
- Impressao de qualidade (min. 300g/m2 para cartao)
- Cartao RSVP com envelope pre-pago ou QR code para resposta online
- Postagem: CTT Correio Azul (nacional), DHL/FedEx (internacional VIP)
- Prazo impressao: 3-4 semanas; postagem: 2 semanas antes do envio

**Convite Digital:**
- Plataforma: Eventbrite, Splash, custom landing page
- Design responsivo (60%+ aberturas em mobile)
- Personalizacao: nome, mesa, QR code unico
- Tracking: taxa abertura, cliques, confirmacoes

**Abordagem Hibrida (recomendada para eventos premium):**
- Fisico para VIP/VVIP + Digital para restantes
- QR code no convite fisico liga a pagina de registo digital

### Step 4 — Set Up Registration & Check-in

**Pre-evento (online):**
- Formulario de registo com tipos de bilhete
- Opcoes add-on (workshops, jantar de gala, parking)
- Confirmacao automatica por email com QR code

**On-site:**
- Tablets com app de check-in (scanner QR code)
- Impressao de crachas on-demand (Zebra, Brother)
- Quiosques self-service para eventos 500+ pessoas
- Linha dedicada para VIP (sem fila)
- Mesa de contingencia para walk-ins

### Step 5 — Design Name Badges

**Regras de design:**
- Nome: fonte minima 24pt, legivel a 1.5m de distancia
- Empresa/Cargo: fonte 14-16pt
- Cor de fundo por tipo: VIP (dourado), Speaker (azul), Staff (verde), Media (amarelo), Standard (branco)
- QR code para networking digital (vCard ou LinkedIn)
- Suporte: lanyard (mais comum), pin (formal), magnetico (premium, evita danos na roupa)

### Step 6 — Manage Capacity

| Metrica | Valor |
|---------|-------|
| Capacidade Maxima Venue | Conforme licenca (alvara) |
| Capacidade Conforto | 80% do maximo |
| Previsao No-shows (corporativo) | 10-20% |
| Previsao No-shows (gratuito) | 30-40% |
| Previsao No-shows (pago) | 5-10% |
| Buffer waitlist | Sobre-confirmar 10-15% acima do target |

**Protocolo Waitlist:**
1. Comunicar posicao na lista
2. Confirmar disponibilidade 48h antes do evento
3. Oferecer alternativa (streaming, proxima edicao)

### Step 7 — Ensure Accessibility
Incluir no formulario de registo e garantir no venue:
- Acesso cadeira de rodas (rampas, elevadores, WC adaptado)
- Loop auditivo / sistema FM para aparelhos auditivos
- Interprete de Lingua Gestual Portuguesa (LGP)
- Sala silenciosa para pausa sensorial
- Materiais em formato acessivel (braille, fonte grande, alto contraste)
- Politica de cao-guia (acesso total)
- Informacao de transporte acessivel (STCP, Metro, parking PMR)

### Step 8 — RGPD Compliance
- Consentimento explicito no registo (checkbox nao pre-selecionada)
- Aviso de privacidade claro: finalidade, base legal, retencao, direitos
- Periodo de retencao: dados eliminados 12 meses apos evento (ou conforme contrato)
- Direito de apagamento: processo para pedidos ARCO
- Subcontratantes: DPA (Data Processing Agreement) com fornecedores (plataforma registo, catering, etc.)
- Fotografia: aviso de captacao de imagem, opt-out disponivel

---

## Output Template

```markdown
# Gestao de Convidados — [Nome do Evento]

## Resumo
- **Evento:** [nome]
- **Data:** [data]
- **Venue:** [local]
- **Capacidade Maxima:** [numero]
- **Target Convidados:** [numero]
- **Sobre-confirmacao:** [numero] (buffer no-show)

## Timeline RSVP
| Data | Accao | Canal | Responsavel |
|------|-------|-------|-------------|
| [data] | Save-the-Date | Email | [nome] |
| [data] | Convite Formal | Fisico + Digital | [nome] |
| [data] | Deadline RSVP | — | — |
| [data] | Follow-up | Telefone + Email | [nome] |
| [data] | Confirmacao Final | Email | [nome] |
| [data] | Lembrete Vespera | SMS | [nome] |

## Estado RSVP
| Estado | Quantidade | % |
|--------|-----------|---|
| Confirmados | [n] | [%] |
| Recusados | [n] | [%] |
| Pendentes | [n] | [%] |
| Sem Resposta | [n] | [%] |
| Waitlist | [n] | — |

## Requisitos Especiais
- **Alimentares:** [lista]
- **Acessibilidade:** [lista]
- **Idiomas:** [lista]

## Check-in Setup
- **Sistema:** [QR / NFC / Manual]
- **Crachas:** [tipo, cor por categoria]
- **Linhas:** [VIP separada? Self-service?]

## RGPD
- [ ] Consentimento explicito no formulario
- [ ] Aviso de privacidade publicado
- [ ] DPA com fornecedores
- [ ] Plano de retencao/eliminacao definido
```

---

## Red Flags
- Sem sistema de tracking RSVP (spreadsheet partilhada sem controlo)
- Sem recolha de requisitos alimentares no registo
- Sem pergunta de acessibilidade no formulario
- Nao-conformidade RGPD (sem consentimento, sem aviso privacidade)
- Crachas com fonte pequena (ilegivel a distancia)
- Sem previsao de no-shows (sobre ou sub-lotacao)
- Follow-up de nao-respondentes apenas por email (telefone e essencial)
- Sem linha VIP separada no check-in
- Sem plano de contingencia para walk-ins
- Dados de convidados partilhados sem DPA com fornecedores
- Convites enviados sem tempo suficiente para RSVP

## Portuguese Specifics
- **Nomes:** Portugueses tipicamente tem dois apelidos (ex: Joao Silva Ferreira) — nunca abreviar para "Joao Ferreira"
- **Tratamento formal:** Dr./Dra., Eng./Eng.a, Arq./Arq.a, Prof. — usar no cracha e comunicacoes formais
- **Tratamento institucional:** Exmo. Senhor, V. Exa. para entidades governamentais
- **Comunicacoes bilingues:** PT/EN para eventos internacionais; PT sempre primeiro
- **CTT:** Correio Azul para envios nacionais urgentes (1-2 dias uteis)
- **Horarios:** Eventos corporativos tipicamente 9h-18h; jantares de gala a partir das 20h
- **Telefone:** Formato +351 9XX XXX XXX (movel) ou +351 2XX XXX XXX (fixo)

---

## Integration Notes
- **atlas-seating:** Guest list feeds directly into seating plan (mesa atribuida, VIP tier, dietary clusters)
- **atlas-protocol:** VIP tier determines protocol treatment, receiving line order, escort assignment
- **atlas-catering:** Dietary requirements from guest database drive menu planning and place-setting cards
- **atlas-tech:** Registration platform selection, check-in technology, WiFi for on-site systems
- **atlas-hybrid:** Virtual attendee registration runs parallel workflow; unified guest database
- **atlas-compliance:** RGPD compliance checklist, data retention, privacy notices
- **atlas-transport:** Guest addresses and accessibility needs inform transport planning
- **atlas-comms (atlas-marketing):** Communication schedule, invitation design, email templates
