---
name: atlas-tech
description: "Event Technology & Registration Systems — registration platforms, check-in, event apps, WiFi, lead capture, RGPD"
version: "1.0"
---

# atlas-tech — Event Technology & Registration Systems

## Description
Complete reference for event technology infrastructure — registration platforms, check-in systems, event apps, WiFi planning, lead capture, live engagement tools, analytics, payment systems, connectivity, and data security. Covers platform comparison matrices, technical specifications, Portuguese-specific integrations (MB Way, Via Verde, PT operators), and RGPD compliance for event data. The technology backbone that powers modern events.

## Trigger Phrases
**EN:** "event technology", "registration platform", "check-in system", "event app", "WiFi planning", "lead capture", "badge scanning", "live polling", "event analytics", "payment system", "cashless event", "QR code", "RFID"
**PT:** "tecnologia evento", "plataforma registo", "sistema check-in", "app evento", "WiFi", "captura leads", "leitura crachás", "votação ao vivo", "analytics evento", "sistema pagamento", "evento cashless", "código QR"

## When to Activate
- Selecting or comparing event registration platforms
- Planning check-in technology and on-site registration
- Specifying event app requirements (build vs. buy)
- Planning WiFi infrastructure and bandwidth for an event
- Setting up lead capture systems for exhibitors/sponsors
- Choosing live engagement tools (polling, Q&A, social walls)
- Defining event analytics and tracking requirements
- Planning payment systems (cashless, card, MB Way)
- Ensuring data security and RGPD compliance for event tech
- Planning connectivity infrastructure (4G/5G, fiber, backup)

---

## Workflow

### Step 1 — Select Registration Platform

**Comparison Matrix:**

| Platform | Capacidade | Preço Base | Integrations | Personalização | PT Support | Melhor Para |
|----------|-----------|-----------|-------------|----------------|-----------|-------------|
| **Eventbrite** | Ilimitado | Grátis (free) / 6.95%+0.99 (paid) | Mailchimp, Salesforce, Zapier | Média | Não nativo | Eventos públicos, bilhética |
| **Cvent** | Ilimitado | Enterprise (consultar) | CRM, Marketo, Salesforce | Alta | Sim | Corporativo, conferências |
| **Bizzabo** | Ilimitado | Enterprise (consultar) | HubSpot, Salesforce, Marketo | Alta | Não | Conferências tech |
| **Hopin** | 100K virtual | Grátis / Starter $99/mês | Slack, HubSpot, Zapier | Média | Não | Hybrid/Virtual |
| **Splash** | Ilimitado | Enterprise | Salesforce, Marketo | Muito Alta | Não | Eventos premium branded |
| **Google Forms + Sheets** | Ilimitado | Grátis | Google Workspace | Baixa | N/A | Low-budget, interno |
| **Custom (Next.js/React)** | Ilimitado | Dev cost | Total | Total | Sim | Controlo total, marca |

**Critérios de selecção:** Escala do evento, budget, necessidade de branding, integrações com CRM existente, suporte a pagamentos PT (MB Way/Multibanco), RGPD compliance, suporte multi-idioma (PT/EN).

### Step 2 — Plan Check-in Technology

| Tecnologia | Velocidade | Custo | Fiabilidade | Melhor Para |
|-----------|----------|-------|-------------|-------------|
| **QR Code (smartphone)** | 3-5 seg/pessoa | Baixo | Alta (offline capable) | Eventos até 500 |
| **QR Code (scanner dedicado)** | 2-3 seg/pessoa | Médio | Muito Alta | Eventos 500-2000 |
| **NFC/RFID wristband** | 1-2 seg/pessoa | Alto (2-5 EUR/banda) | Muito Alta | Festivais, multi-dia |
| **Facial recognition** | 1 seg/pessoa | Muito Alto | Alta (RGPD concerns) | Tech conferences (opt-in) |
| **Self-service kiosk** | 15-30 seg/pessoa | Médio-Alto | Alta | Eventos 1000+ |
| **Manual (lista impressa)** | 10-20 seg/pessoa | Muito Baixo | Média | Backup / Eventos <100 |

**Dimensionamento check-in:**
- Regra: 1 ponto de check-in por 100 convidados/hora de pico
- Evento 500 pessoas, chegada em 1h: mínimo 5 pontos
- VIP: linha separada, sempre (mínimo 1 ponto dedicado)
- Staff: 1 pessoa por ponto + 1 troubleshooter roaming

**On-demand badge printing:**
- Impressoras recomendadas: Zebra ZD420, Brother QL-820NWB
- Stock: crachás pré-cortados, lanyards, porta-crachás
- Backup: crachás pré-impressos para VIPs (nunca depender apenas de on-demand para VIP)

### Step 3 — Specify Event App

**Funcionalidades essenciais:**

| Feature | Prioridade | Notas |
|---------|-----------|-------|
| Agenda / Programa | Must-have | Personalização, favoritos, alertas |
| Speaker bios | Must-have | Foto, bio, links |
| Mapa do venue | Must-have | Interactivo, com busca |
| Notificações push | Must-have | Alterações programa, alertas |
| Networking | Should-have | Chat, meeting scheduling, attendee list |
| Live polling / Q&A | Should-have | Integração com sessões |
| Social wall | Nice-to-have | Feed Instagram/Twitter do evento |
| Gamification | Nice-to-have | Points, leaderboard, challenges |
| Lead capture (exhibitors) | Conditional | Se expo/feira |
| Offline mode | Must-have | Conteúdo base sem internet |

**Build vs Buy:**
- **Buy (white-label):** Cvent, Whova, Swapcard, Grip — 2000-10000 EUR / evento
- **Build (custom):** React Native / Flutter — 15000-50000 EUR dev, 6-12 semanas
- **Recomendação:** Buy para evento único; Build se recorrente (3+/ano) e marca forte

### Step 4 — Plan WiFi Infrastructure

**Bandwidth requirements:**

| Uso | Mbps por Device | Notas |
|-----|----------------|-------|
| Email + browsing | 0.5-1 | Uso básico |
| Social media (upload) | 1-2 | Fotos, stories |
| Video streaming (assistir) | 3-5 | Live stream |
| Video call (participar) | 2-4 | Hybrid attendee |
| Live demo / heavy app | 5-10 | Tech events |

**Dimensionamento:**
- Regra: 70% dos presentes conectam ao WiFi simultaneamente
- Access Points: 1 AP por 30-50 devices (não por pessoa — cada pessoa tem 1.5-2 devices)
- Evento 500 pessoas: ~350 devices simultâneos, min. 7-12 APs, 200-500 Mbps uplink
- Banda dedicada para produção (AV, streaming, backstage): NUNCA partilhar com guests

**Redes separadas (SSID):**
1. `[Evento]-PROD` — Produção (AV, streaming, backstage) — WPA2 Enterprise
2. `[Evento]-STAFF` — Staff e organização — WPA2
3. `[Evento]-GUEST` — Convidados — Portal captive com aceite RGPD
4. `[Evento]-EXPO` — Expositores (se aplicável) — WPA2

**Distribuição de password:** QR code nos crachás, sinalética na entrada, ecrãs no venue.

### Step 5 — Set Up Lead Capture

| Método | Custo | Precisão | Integração CRM | Melhor Para |
|--------|-------|----------|---------------|-------------|
| Badge scanning (QR/barcode) | Incluído na plataforma | Alta | Automática | Feiras, expos |
| Business card scanning (app) | 50-200 EUR/ano | Média (OCR) | Manual/Zapier | Networking events |
| NFC tap exchange | Alto (hardware) | Alta | Automática | Tech conferences |
| Digital exchange (QR vCard) | Baixo | Alta | Manual | Eventos pequenos |
| Formulário no tablet | Baixo | Alta | Via form platform | Stands, demos |

**Para expositores/sponsors:** Fornecer app ou device de scanning, dashboard de leads em tempo real, export CSV pós-evento em 24h.

### Step 6 — Deploy Live Engagement Tools

| Tool | Funcionalidade | Preço | Free Tier | Notas |
|------|---------------|-------|-----------|-------|
| **Slido** | Polls, Q&A, quizzes | $100-200/evento | Sim (limitado) | Integra com PPT/Keynote |
| **Mentimeter** | Polls, word clouds, scales | $12-25/mês | Sim (2 perguntas) | Muito visual |
| **Poll Everywhere** | Polls, Q&A, surveys | $120/mês | Sim (25 respostas) | Ideal para education |
| **Walls.io** | Social wall agregador | $100-500/evento | Não | Instagram, Twitter, hashtags |
| **Kahoot!** | Gamification, quizzes | $17-40/mês | Sim | Divertido, engagement alto |

**Best practices:**
- Polling: máximo 1 pergunta a cada 10 minutos de sessão
- Q&A: moderar SEMPRE (filtrar antes de mostrar no ecrã)
- Social wall: definir hashtag oficial, moderar conteúdo
- Gamification: prémios reais (não apenas virtuais) aumentam participação 3-5x

### Step 7 — Configure Analytics & Tracking

**Métricas a capturar:**

| Métrica | Como | Ferramenta |
|---------|------|-----------|
| Attendance (check-in real) | Scan de entrada | Plataforma registo |
| Session popularity | Scan por sala / app | Event app / room sensors |
| Engagement score | Polls + Q&A + app usage | Slido + app analytics |
| Foot traffic / heat map | WiFi tracking / beacons | Cisco DNA Spaces / custom |
| Dwell time por zona | Beacons Bluetooth | Estimote / Kontakt.io |
| Net Promoter Score | Survey pós-evento | Typeform / Google Forms |
| Social reach | Hashtag tracking | Walls.io / Brandwatch |

**Dashboard real-time:** Montar dashboard (TV na sala de operações) com check-in count, sessões a decorrer, alertas WiFi, e feedback live.

### Step 8 — Plan Payment Systems

| Método | Setup Cost | Transaction Fee | Velocidade | Notas PT |
|--------|-----------|----------------|-----------|----------|
| **MB Way** | Grátis | 0% (até limites) | Instantâneo | Muito popular em PT |
| **Multibanco (TPA)** | 50-100 EUR/mês aluguer | 0.5-1.5% | 5-10 seg | Standard em PT |
| **Contactless (card)** | Incluído no TPA | 0.5-1.5% | 2-3 seg | Visa/Mastercard |
| **RFID/NFC top-up** | 5-15 EUR/band + sistema | 2-3% | 1-2 seg | Festivais, cashless |
| **Cash** | — | 0% | Variável | SEMPRE ter como fallback |
| **Apple Pay / Google Pay** | Via TPA | 0.5-1.5% | 2-3 seg | Turistas internacionais |

**Cashless events:**
- Pre-load via app ou quiosques de top-up
- Reembolso de saldo não utilizado (obrigatório por lei)
- Sempre ter fallback para cash ou cartão (nunca 100% cashless)

### Step 9 — Ensure Connectivity Infrastructure

**Checklist de infraestrutura:**
- [ ] Fibra óptica ao venue (min. 100 Mbps, idealmente 1 Gbps)
- [ ] 4G/5G booster se venue com má cobertura (verificar MEO, NOS, Vodafone)
- [ ] Internet backup: 4G/5G router como failover (Huawei B818, Netgear Nighthawk)
- [ ] UPS para equipamento de rede (min. 30min autonomia)
- [ ] Network monitoring em tempo real (alerts para equipa técnica)
- [ ] Teste de carga 48h antes do evento

**Operadores PT e cobertura:**
- MEO (Altice): melhor cobertura rural
- NOS: forte em zonas urbanas
- Vodafone: melhor para dados móveis em grandes eventos
- Verificar cobertura específica do venue em opensignal.com ou nperf.com

### Step 10 — Data Security & RGPD

**Checklist de segurança:**
- [ ] Dados de registo encriptados em trânsito (HTTPS/TLS) e em repouso
- [ ] Plataforma de registo com certificação RGPD
- [ ] Acesso a dados limitado (principio do menor privilégio)
- [ ] WiFi guest com portal captive + aceite de termos (RGPD)
- [ ] Pagamentos: conformidade PCI DSS
- [ ] Backup de dados de registo antes do evento
- [ ] Plano de eliminação de dados pós-evento (prazo definido)
- [ ] DPA (Data Processing Agreement) com todos os fornecedores tech
- [ ] Privacy notice no formulário de registo
- [ ] Opt-in explícito para comunicações marketing

**Retenção de dados:**
- Dados de registo: máximo 12 meses pós-evento (ou conforme base legal)
- Dados de pagamento: conforme obrigações fiscais (8-10 anos em PT)
- WiFi logs: máximo 6 meses
- Analytics anonimizados: podem ser retidos indefinidamente

---

## Output Template

```markdown
# Tech Stack — [Nome do Evento]

## Plataforma de Registo
- **Plataforma:** [nome]
- **URL registo:** [link]
- **Tipos bilhete:** [lista]
- **Integrações:** [CRM, email, etc.]

## Check-in
- **Tecnologia:** [QR / NFC / Manual]
- **Pontos de check-in:** [número]
- **Badge printing:** [on-demand / pré-impressos / ambos]
- **Staff check-in:** [número pessoas]

## WiFi
- **Uplink:** [Mbps]
- **Access Points:** [número]
- **Redes:** [PROD / STAFF / GUEST / EXPO]
- **Backup:** [4G router? Qual?]
- **Password distribution:** [método]

## Event App
- **App:** [nome / custom]
- **Features:** [lista activa]
- **Offline mode:** [sim/não]

## Engagement
- **Polling:** [ferramenta]
- **Q&A:** [ferramenta]
- **Social Wall:** [ferramenta + hashtag]

## Pagamentos
- **Métodos aceites:** [MB Way, TPA, cash, RFID]
- **Cashless:** [sim/não]
- **Backup:** [método]

## Analytics
- **Métricas tracked:** [lista]
- **Dashboard:** [localização, acesso]
- **Report pós-evento:** [prazo entrega]

## Segurança & RGPD
- [ ] HTTPS em todas as plataformas
- [ ] DPA com fornecedores tech
- [ ] Portal captive WiFi com termos
- [ ] Plano de retenção/eliminação definido
- [ ] Backup de dados pré-evento
```

---

## Red Flags
- Sem planeamento de capacidade WiFi (crashes durante evento)
- Ponto único de falha na conectividade (sem backup internet)
- Sem modo offline no sistema de registo/check-in
- Sem backup de dados de registo
- Sistema de pagamento sem fallback para cash
- Event app sem modo offline
- QR codes/badges que não funcionam (não testados antes)
- WiFi de produção partilhada com guests (streaming falha)
- Sem teste de carga da rede antes do evento
- Dados de convidados em plataformas sem conformidade RGPD
- Sem moderação de Q&A ou social wall (conteúdo inapropriado)
- Lead capture sem consentimento RGPD dos attendees

## Portuguese Specifics
- **MB Way:** Método de pagamento preferido em PT (8M+ utilizadores). Integrar sempre
- **Multibanco:** TPA Multibanco ainda é o standard para comércio presencial em PT
- **Via Verde:** Pode ser usado para parking de eventos (integrações com venues)
- **Teclados PT:** Certificar que formulários aceitam caracteres PT (ç, ã, õ, é, etc.)
- **Operadores móveis:** MEO, NOS, Vodafone — testar cobertura de todos no venue
- **Fibra:** Portugal tem excelente cobertura fibra em zonas urbanas (FTTH >90% em Lisboa/Porto)
- **RGPD:** Portugal implementou via Lei 58/2019 — CNPD é a autoridade supervisora
- **Facturação:** Software de facturação certificado pela AT para vendas no evento

---

## Integration Notes
- **atlas-guest:** Registration platform é o sistema primário de gestão de convidados
- **atlas-hybrid:** Plataforma virtual, streaming setup, e engagement tools são core desta skill
- **atlas-av:** Coordenação com AV para streaming, polling display, WiFi produção
- **atlas-seating:** Check-in data feeds seating confirmation; badge scanning valida mesa
- **atlas-sponsor:** Lead capture tools para sponsors; analytics de engagement por sponsor
- **atlas-budget:** Custos de tecnologia são tipicamente 5-15% do budget total do evento
- **atlas-risk:** Planos de contingência para falha tech (internet, plataforma, pagamentos)
- **atlas-compliance:** RGPD compliance, PCI DSS para pagamentos, segurança de dados


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-tech** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-tech:**

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
