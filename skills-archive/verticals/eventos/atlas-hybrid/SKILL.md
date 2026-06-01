---
name: atlas-hybrid
description: "Virtual & Hybrid Event Management — hybrid models, platform selection, streaming, engagement equity, analytics"
version: "1.0"
---

# atlas-hybrid — Virtual & Hybrid Event Management

## Description
End-to-end reference for planning, producing, and delivering virtual and hybrid events. Covers hybrid models (hub-and-spoke, broadcast, multi-hub, virtual-first), platform selection, production setup (multi-camera, streaming, graphics), virtual attendee experience, engagement equity between in-person and remote audiences, content strategy for online, technical requirements, timezone management, monetization models, and analytics. Ensures virtual attendees are never an afterthought.

## Trigger Phrases
**EN:** "hybrid event", "virtual event", "online event", "live stream", "broadcast", "virtual attendees", "remote audience", "streaming", "virtual platform", "webinar", "online conference", "virtual networking", "on-demand"
**PT:** "evento híbrido", "evento virtual", "evento online", "live stream", "transmissão", "participantes remotos", "audiência remota", "streaming", "plataforma virtual", "webinar", "conferência online", "networking virtual", "on-demand"

## When to Activate
- Planning any event with a virtual or remote component
- Choosing between virtual-only, hybrid, or in-person with streaming
- Selecting virtual event platforms
- Setting up production for live streaming (cameras, encoding, graphics)
- Designing virtual attendee experience (registration through post-event)
- Ensuring engagement equity between in-person and virtual audiences
- Planning content strategy for online consumption
- Managing multi-timezone events
- Monetizing virtual access (tiered pricing, on-demand library)
- Measuring virtual event success (analytics, engagement, ROI)

---

## Workflow

### Step 1 — Choose Hybrid Model

| Modelo | Descrição | Complexidade | Custo | Melhor Para |
|--------|-----------|-------------|-------|-------------|
| **Broadcast** | 1 venue, muitos viewers remotos | Média | Médio | Keynotes, conferências, AGMs |
| **Hub-and-Spoke** | 1 venue principal + locations satélite | Alta | Alto | Eventos multi-cidade, corporativo global |
| **Multi-Hub** | Múltiplos venues iguais, interconectados | Muito Alta | Muito Alto | Eventos internacionais, summits |
| **Virtual-First + Networking Físico** | Core content online, meetups presenciais | Média | Médio-Baixo | Comunidades, eventos recorrentes |
| **Simulcast** | Evento presencial transmitido sem adaptação | Baixa | Baixo | Quick & cheap, internal meetings |
| **Virtual-Only** | 100% online, sem componente presencial | Média | Baixo-Médio | Webinars, formações, eventos globais |

**Decision tree:**
1. Audiência maioritariamente local? → Presencial com broadcast
2. Audiência distribuída globalmente? → Virtual-first ou multi-hub
3. Networking é prioridade? → Hub-and-spoke ou multi-hub
4. Budget limitado? → Virtual-only ou simulcast
5. Conteúdo educativo/formativo? → Virtual-first com sessões on-demand

### Step 2 — Select Virtual Platform

**Comparison Matrix:**

| Plataforma | Capacidade | Networking | Engagement | Branding | Preço | Melhor Para |
|-----------|-----------|-----------|-----------|---------|-------|-------------|
| **Zoom Webinar** | 50K | Limitado | Polls, Q&A | Baixo | $79-6490/mês | Webinars simples |
| **Teams Live** | 20K | Limitado | Q&A básico | Baixo | Incluído M365 | Corporativo Microsoft |
| **Hopin** | 100K | Bom (1:1, lounges) | Polls, chat, expo | Alto | $99-Custom | Conferências, feiras |
| **Airmeet** | 100K | Excelente (tables) | Social lounge, speed networking | Alto | $167-Custom | Networking-focused |
| **Cvent Virtual** | 50K | Bom | Polls, Q&A, gamification | Muito Alto | Enterprise | Corporativo enterprise |
| **Run The World** | 10K | Excelente (tables, 1:1) | Bom | Médio | $99-499/evento | Eventos sociais, meetups |
| **Swapcard** | 50K | Excelente (AI matching) | Bom | Alto | Custom | Conferências + expo |
| **YouTube Live** | Ilimitado | Nenhum (chat only) | Chat | Muito Baixo | Grátis | Broadcast público, reach |
| **Custom (WebRTC + React)** | Custom | Total | Total | Total | Dev cost alto | Controlo total, marca forte |

**Critérios de selecção:**
- Número esperado de virtual attendees
- Necessidade de networking (passivo vs activo)
- Nível de branding/personalização
- Integrações (CRM, email, analytics)
- Budget
- Suporte multi-idioma e legendas

### Step 3 — Production Setup

**Streaming room / Control room:**

```
┌──────────────────────────────────────────────┐
│                 PALCO / STAGE                 │
│                                               │
│  [CAM 1]              [CAM 2]    [CAM 3]     │
│  (wide shot)        (speaker)   (audience)    │
│                                               │
│  ═══════════════════════════════════════════  │
│                                               │
│  [CONTROL ROOM / RÉGIE]                       │
│  ┌─────────┬──────────┬──────────┐           │
│  │ vMix /  │ Graphics │ Audio    │           │
│  │ ATEM    │ Operator │ Mixer    │           │
│  │ Switch  │ (lower   │          │           │
│  │         │ thirds)  │          │           │
│  └─────────┴──────────┴──────────┘           │
│                                               │
│  [ENCODER] → [CDN] → [Platform]              │
└──────────────────────────────────────────────┘
```

**Equipamento essencial:**

| Componente | Opção Budget | Opção Pro | Notas |
|-----------|-------------|----------|-------|
| **Switching** | OBS Studio (grátis) | Blackmagic ATEM Mini Pro / vMix | OBS para simples, ATEM para multi-câmara |
| **Câmaras** | 2x webcam HD | 2-3x câmaras SDI/HDMI | Mínimo 2 ângulos |
| **Microfone** | Lapela wireless | Sennheiser/Shure wireless | Audio é MAIS importante que vídeo |
| **Iluminação** | Ring light, softbox | Key + fill + back | Iluminação 3-point |
| **Graphics** | OBS overlays | vMix / Singular.live | Lower thirds, títulos, transições |
| **Encoding** | Software (OBS) | Hardware (Teradek, AJA) | Hardware para fiabilidade |
| **Conteúdo pré-gravado** | MP4 local | MAM system | Bumpers, intros, video packages |
| **Teleprompter** | App tablet | Prompter dedicado | Para speakers que lêem |
| **Confidence monitor** | Tablet/TV | Monitor dedicado | Speaker vê slides + timer + notas |

### Step 4 — Design Virtual Attendee Experience

**Journey do attendee virtual:**

| Fase | Timing | Acção | Responsável |
|------|--------|-------|-------------|
| **Registo** | Semanas antes | Inscrição online, escolha de sessões | Registration team |
| **Onboarding** | 1 semana antes | Email com guia da plataforma, tech check link | Comms team |
| **Tech Check** | 2-3 dias antes | Sessão teste (15min) — browser, audio, video | Tech support |
| **Welcome** | Dia do evento | Email manhã + notificação app + sala de espera com música | Virtual MC |
| **Sessões** | Durante | Conteúdo + engagement (polls, Q&A, chat) | Speakers + moderators |
| **Networking** | Intervalos | Virtual lounges, speed networking, 1:1 meetings | Facilitator |
| **Helpdesk** | Sempre | Chat support para problemas técnicos | Tech support |
| **Encerramento** | Final | Agradecimento, survey, acesso on-demand | Virtual MC |
| **Follow-up** | 1-3 dias depois | Email recap, links gravações, certificados | Comms team |

**Virtual swag box (enviada pré-evento):**
- Caderno + caneta branded
- Snacks / café / chá
- Código QR para conteúdo exclusivo
- Merchandise do evento
- Nota pessoal do organizador
- Custo: 20-50 EUR + envio

### Step 5 — Ensure Engagement Equity

**O problema:** Virtual attendees sentem-se como "cidadãos de segunda classe". Solução: design intencional.

| Elemento | In-Person | Virtual | Equity Solution |
|----------|----------|---------|-----------------|
| **Q&A** | Micro na sala | Chat/raise hand | Virtual MC intercala perguntas: 1 sala, 1 online |
| **Networking** | Coffee break natural | Nada (se não planeado) | Speed networking sessions, virtual tables, 1:1 matching |
| **Engagement** | Presença física | Passivo | Polls, quizzes, gamification com leaderboard unificado |
| **Visibilidade** | Na sala | Invisíveis | Mostrar virtual audience no ecrã da sala, shout-outs |
| **MC** | MC da sala | Ninguém | Virtual MC dedicado (não o mesmo da sala) |
| **Swag** | Bag na entrada | Nada | Swag box enviada pré-evento |
| **Content** | 100% | Mesmos slides à distância | Câmara close-up de slides + speaker, gráficos optimizados |
| **Feedback** | Aplausos, reações | Silêncio | Reaction buttons (applause, heart, laugh) visíveis na sala |

**Regras de ouro:**
1. **Virtual MC dedicado** — nunca o MC da sala a fazer double duty
2. **Alternância** de perguntas: sala → online → sala → online
3. **Câmara na audiência** para virtual ver reações da sala
4. **Chat moderado** com highlights mostrados no ecrã da sala
5. **Horário adaptado:** sessões mais curtas (max 45min online)

### Step 6 — Optimize Content Strategy for Online

**Duração ideal de sessões online:**

| Formato | Duração Máx. | Interação | Notas |
|---------|-------------|-----------|-------|
| Keynote | 20-30 min | Poll a meio + Q&A no fim | Impacto > Informação |
| Panel | 30-40 min | Perguntas do público a cada 10min | Moderador forte essencial |
| Workshop | 45-60 min | Breakouts a cada 15min | Máximo engagement |
| Lightning talk | 5-10 min | 1 poll ou Q&A rápido | Formato TED-style |
| Fireside chat | 20-30 min | Q&A audience-driven | Informal, conversacional |

**Regra dos 10 minutos:** A cada 10 minutos, uma interacção (poll, pergunta, breakout, mudança de speaker, vídeo). Nunca mais de 10min de talking head sem quebra.

**Conteúdo on-demand:**
- Gravar TODAS as sessões
- Disponibilizar em 24-48h pós-evento
- Organizar por track/tema
- Permitir velocidade 1.5x/2x
- Adicionar capítulos/timestamps
- Acesso: por tier de bilhete (gratuito limitado, premium completo)

### Step 7 — Plan Technical Requirements

**Internet (upload — o que importa para streaming):**

| Qualidade | Resolution | Bitrate | Upload Mínimo | Recomendado |
|-----------|-----------|---------|--------------|-------------|
| SD | 480p | 1.5-2.5 Mbps | 3 Mbps | 5 Mbps |
| HD | 720p | 2.5-4 Mbps | 5 Mbps | 10 Mbps |
| Full HD | 1080p | 4-6 Mbps | 10 Mbps | 15 Mbps |
| 4K | 2160p | 13-20 Mbps | 25 Mbps | 35 Mbps |

**Redundância (obrigatória):**
- Dual ISP: fibra primária + 4G/5G secundário (failover automático)
- Dual encoder: se encoder principal falhar, backup assume em <10 seg
- UPS para toda a régie (min. 30 min autonomia)
- CDN: Cloudflare, AWS CloudFront, ou Akamai para entrega global

**Teste técnico completo:**
- Full rehearsal com speakers 48h antes
- Teste de streaming end-to-end 24h antes
- Verificação de todos os links, slides, vídeos pré-gravados
- Teste de failover (desligar fibra, verificar que 4G assume)

### Step 8 — Manage Timezones

**Portugal (WET/WEST):**
- Inverno: GMT+0 (WET) — igual a UK, 1h atrás de CET
- Verão: GMT+1 (WEST) — igual a UK (BST), 1h atrás de CEST
- Açores: GMT-1 (1h atrás de Portugal continental)

**Multi-timezone strategies:**

| Estratégia | Descrição | Melhor Para |
|-----------|-----------|-------------|
| **Single timezone + replay** | Evento numa timezone, gravação para outras | Conferências com 1 timezone dominante |
| **Regional hubs** | Sessões repetidas em 2-3 timezones | Grandes conferências globais |
| **Follow-the-sun** | Programa contínuo 24h, cada região apresenta | Hackathons, eventos community |
| **Async-first** | Conteúdo on-demand + sessões live limitadas | Learning/education events |

**Horário ideal para evento PT + restante Europa:**
- 10:00-17:00 WET cobre: UK (10-17), CET (11-18), EET (12-19)
- Para incluir US East: 14:00-18:00 WET = 9:00-13:00 EST
- Para incluir Asia (Singapura/Tokyo): sessão dedicada 8:00-10:00 WET = 16:00-18:00 SGT

### Step 9 — Monetize Virtual Access

| Modelo | Descrição | Revenue Potential | Notas |
|--------|-----------|------------------|-------|
| **Freemium** | Keynotes grátis, workshops pagos | Médio | Máximo reach + upsell |
| **Tiered** | Free / Standard / Premium / VIP | Alto | Mais opções, mais revenue |
| **Pay-per-view** | Pagar por sessão individual | Médio-Baixo | Complexo de gerir |
| **All-access pass** | Preço único para tudo | Médio | Simples, previsível |
| **Sponsored access** | Sponsors pagam, attendees grátis | Alto (B2B) | Sponsors = revenue |
| **On-demand library** | Acesso pós-evento às gravações | Adicional | Revenue tail longa |

**Pricing benchmarks (virtual):**
- Virtual should be 30-50% do preço presencial
- Free events: monetizar via sponsors + leads
- Tier VIP virtual: incluir swag box + meet & greet exclusivo + certificado

**Virtual expo booths:**
- Pricing: 500-5000 EUR por booth virtual
- Features: video chat, resource downloads, demo scheduling, lead capture
- Analytics para sponsor: visits, dwell time, leads capturados

### Step 10 — Measure & Analyze

**Virtual-specific KPIs:**

| KPI | Benchmark | Como Medir |
|-----|-----------|-----------|
| Registration → Attendance | 40-60% (free), 70-85% (paid) | Platform analytics |
| Average watch time | >60% da sessão | Platform analytics |
| Session drop-off rate | <30% ideal | Platform analytics |
| Engagement score | >50% interagiu (poll/Q&A/chat) | Engagement tool |
| Networking connections | >3 per attendee | Platform analytics |
| NPS virtual | >30 (bom), >50 (excelente) | Post-event survey |
| Content replay views | 30-50% dos registados | On-demand platform |
| Virtual → in-person conversion | Track para próxima edição | CRM |

**Post-event report:**
- Attendance: peak, average, by session, by timezone
- Engagement: polls answered, questions asked, chat messages
- Content: most watched, most replayed, drop-off points
- Networking: connections made, meetings booked
- Technical: uptime, buffering incidents, support tickets
- Revenue: by tier, by source, cost per attendee virtual vs in-person

---

## Output Template

```markdown
# Plano Hybrid/Virtual — [Nome do Evento]

## Modelo
- **Tipo:** [Broadcast / Hub-and-Spoke / Virtual-Only / ...]
- **Plataforma:** [nome]
- **Audiência esperada:** [presencial] + [virtual]
- **Timezones:** [lista]

## Produção
- **Streaming:** [resolução, bitrate]
- **Câmaras:** [número, tipo]
- **Switching:** [OBS / ATEM / vMix]
- **Internet:** [primário + backup]
- **Régie localização:** [sala]

## Experiência Virtual
- **Virtual MC:** [nome]
- **Tech check:** [data/hora]
- **Swag box:** [sim/não, conteúdo]
- **Helpdesk:** [canal, horário]

## Engagement
- **Polling:** [ferramenta]
- **Q&A:** [moderador + ferramenta]
- **Networking:** [formato + ferramenta]
- **Gamification:** [sim/não, mecânica]

## Content
- **Formato sessões:** [duração, interação]
- **On-demand:** [prazo disponibilidade]
- **Replay access:** [quem, quanto tempo]

## Monetização
- **Modelo:** [Freemium / Tiered / Sponsored]
- **Preços:** [por tier]
- **Sponsors virtuais:** [número, preço booth]

## Contingências
- [ ] Internet backup testado
- [ ] Encoder backup configurado
- [ ] Protocolo falha plataforma definido
- [ ] Speaker backup identificados
- [ ] Gravação local como fallback
```

---

## Red Flags
- Virtual tratado como afterthought (câmara fixa no fundo da sala, sem moderação online)
- Sem tech rehearsal com speakers (problemas descobertos ao vivo)
- Ligação internet única sem backup (ponto único de falha)
- Sem plano de engagement virtual (audiência passiva = drop-off)
- Áudio deficiente (mais importante que vídeo para virtual — investir em microfones)
- Sem fallback se plataforma falhar (ter backup plan: YouTube Live, Zoom)
- Sessões longas sem interação (>10min de talking head sem quebra)
- Mesmo MC para sala e virtual (impossível fazer bem os dois)
- Sem modo de gravação/on-demand (conteúdo perdido)
- Sem tech check prévio para speakers (problemas de câmara, micro, fundo)
- Plataforma sem modo offline/buffer (cortes visíveis ao viewer)
- Virtual expo sem analytics para sponsors (valor não demonstrado)

## Portuguese Specifics
- **Timezone:** Portugal GMT+0 (WET) no inverno, GMT+1 (WEST) no verão — mesmo que UK
- **Horário trabalho:** Tipicamente 9h-18h com almoço 13h-14h; sessões online a partir das 14h30 captam mais audiência PT
- **Infraestrutura internet:** Fibra FTTH muito difundida em zonas urbanas PT (>90% Lisboa/Porto); rural pode precisar 4G
- **Plataformas:** Teams muito usado em corporativo PT (Microsoft forte em PT); Zoom para PMEs; YouTube Live para público geral
- **Idioma:** Legendagem PT essencial para audiência virtual PT; considerar intérprete simultâneo PT/EN
- **Açores/Madeira:** 1h a menos que continente (GMT-1/WET-1) — considerar se audiência inclui regiões autónomas
- **Cultura PT:** Portugueses valorizam conexão pessoal — virtual networking precisa de facilitação activa (não funciona só abrir uma sala)
- **Pagamentos:** Bilhética virtual via MB Way / Multibanco / MB NET para mercado PT

---

## Integration Notes
- **atlas-tech:** Toda a infraestrutura tecnológica (WiFi, streaming, plataformas) é partilhada com esta skill
- **atlas-av:** Setup de câmaras, áudio, iluminação, e switching são especificados em atlas-av; atlas-hybrid foca na estratégia e experiência
- **atlas-guest:** Base de dados de convidados unificada (presencial + virtual) com field para tipo de participação
- **atlas-marketing:** Promoção do componente virtual, comunicações específicas para audiência remota
- **atlas-sponsor:** Virtual expo booths, sponsored sessions, analytics para sponsors virtuais
- **atlas-catering:** Swag box pode incluir items food/drink para experiência sensorial partilhada
- **atlas-budget:** Custos de produção virtual tipicamente 15-30% do budget total de evento hybrid
- **atlas-post-event:** Analytics virtual alimentam relatório pós-evento; on-demand library é deliverable pós-evento
- **atlas-protocol:** VIP virtual precisa de tratamento diferenciado (green room virtual, meet & greet exclusivo)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **atlas-hybrid** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in atlas-hybrid:**

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
