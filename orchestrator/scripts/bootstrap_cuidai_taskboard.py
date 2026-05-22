"""
bootstrap_cuidai_taskboard.py
Generates 40 atomic tasks (CUI-001..CUI-040) for the Cuidaí 90-day plan,
aligned with the orchestrator's task schema v2.

Run once. Writes to ~/.claude/orchestrator/tasks/active/CUI-NNN.yaml.
"""
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

NOW = datetime.now(UTC).isoformat()
DAY = lambda n: (datetime.now(UTC) + timedelta(days=n)).isoformat()

# SLA helpers based on execution_policy
def sla(policy, extra_days=0):
    hours = {"critical": 1, "client_facing": 4, "financial": 2, "default": 8}.get(policy, 8)
    return (datetime.now(UTC) + timedelta(days=extra_days, hours=hours)).isoformat()

# Tasks: (id, title, description, priority, skill, assignee, deps, policy, est_tokens, watchers, notes_extra, blocked_reason)
TASKS = [
    # ==== WAVE 0 — Day 0 Foundation (parallel) ====
    ("CUI-001",
     "Brand availability check — cuidai.com.br + INPI + social handles + .com WHOIS",
     "Verificar disponibilidade da marca CUIDAÍ: (1) registro.br para cuidai.com.br + alternativas (.app.br, usecuidai, etc); (2) INPI nas classes Nice 35 (serviços comerciais), 41 (educação/cuidado), 42 (software); (3) handles em Instagram, TikTok, X/Twitter, LinkedIn, YouTube; (4) cuidai.com via WHOIS; (5) Google search para usos existentes (collisions, conflitos brand). Output: relatório semáforo por dimensão + recomendação de prosseguir OR ativar fallback.",
     "critical", "dario-naming", "worker-naming", [], "critical", 6000,
     ["dario-ceo", "user"], ["Day 0 blocker — sem domain confirmado não há identidade visual nem launch"], None),

    ("CUI-002",
     "Legal scope brief — RIPD LGPD-saúde + escolha escritório (Opice/Astrea/Demarest/Chenut)",
     "Preparar scope detalhado para envio a 3 escritórios brasileiros LGPD-saúde: Opice Blum, Astrea, Chenut Oliveira. Pedir: (1) RIPD para dados sensíveis saúde Art. 11; (2) bases legais por tratamento (consentimento + tutela saúde + contrato); (3) termos de uso customizados (NÃO copy SAQUEI); (4) política privacidade granular; (5) modelo consent WhatsApp para idoso; (6) processo notificação incidente ≤72h ANPD; (7) análise transferência internacional (Vercel US/EU). Output: scope doc + 3 emails personalizados + comparativo cost/timeline esperado.",
     "critical", "dario-legal", "worker-legal", [], "critical", 8000,
     ["dario-ceo"], ["Budget R$ 5-10K parecer formal"], None),

    ("CUI-003",
     "Tech stack baseline + SAQUEI fork plan (75% reuse map)",
     "Documentar plano técnico Day 0: (1) Identificar 75% reuse SAQUEI (auth, alerts, push VAPID, email lifecycle, WhatsApp, Stripe BR, Sentry, admin NASA, PWA banner); (2) Decision matrix: fork SAQUEI repo vs greenfield com submodules vs copy/paste; (3) Database isolation strategy (separate Postgres OR shared schema com prefix); (4) Env vars delta entre SAQUEI e Cuidaí; (5) Cost projection mensal (Vercel + Postgres + Resend + WhatsApp + Cloudinary + Sentry + Stripe BR). Output: ARCHITECTURE-BASELINE.md.",
     "high", "dario-product", "worker-product", [], "default", 7000,
     ["dario-ceo"], [], None),

    ("CUI-004",
     "WhatsApp Business API setup spec — Meta direto vs Twilio decision doc",
     "Decision doc fundamentado: usar Meta WhatsApp Business API direto vs Twilio. Inclui: (1) Pricing comparison em scale 50K mensagens/mês; (2) Approval timeline Meta (geralmente 2-4 semanas) — começar Day 0; (3) Template approval process (consent message, medication reminder, SOS escalation); (4) Webhook architecture; (5) Phone number provisioning + verification. Output: WHATSAPP-SPEC.md + Meta Business Manager onboarding checklist.",
     "high", "dario-product", "worker-product", [], "default", 6000,
     ["dario-ceo"], ["Meta approval pode atrasar Phase 3 — começar já"], None),

    # ==== WAVE 1 — Phase 0 Discovery (W1-W2, depends on Wave 0) ====
    ("CUI-005",
     "BENCHMARK-REPORT.md — 9 produtos estudados (5 caregiver + 4 saúde BR)",
     "Estudar e documentar 9 produtos: Famileo (Fr), CareZone (US vendido $40M), Lotsa Helping Hands (US), Vivo Family (Es), Cleo (US fintech pattern); Sami Saúde (BR), Conexa (BR telemed), MyChart (Epic global), Drogaria São Paulo app. Para cada um: 1 página com screenshots · 3 strengths · 3 weaknesses · 1 feature a roubar com twist BR. Também estudar craft excellence: Linear (animações), Stripe (onboarding), Notion (flexibility), Apple Health (privacy trust), Instagram (push timing), WhatsApp (conv UI BR). Output: BENCHMARK-REPORT.md.",
     "critical", "a360-nicho", "worker-product", ["CUI-001"], "client_facing", 12000,
     ["dario-ceo"], ["Não copiar — superar. Base para PRD."], None),

    ("CUI-006",
     "Mom Test outreach script BR — adapt SAQUEI 15-entrevistas template",
     "Adaptar script de outreach do SAQUEI (já validado) para audiência Cuidaí: cuidadores BR 35-55, pais 65+ vivos não-residentes, renda R$ 8K+/mês. NÃO amigos íntimos. Inclui: (1) hook LinkedIn + WhatsApp; (2) script 7 perguntas obrigatórias (do briefing, não inventar outras); (3) confidentiality + NDA leve; (4) compensação (R$ 50 cartão Amazon OR 12m Plus grátis); (5) screener para filtrar não-qualificados em <2min. Output: MOM-TEST-SCRIPT-BR.md + 5 templates outreach.",
     "critical", "dario-content", "worker-content", ["CUI-005"], "client_facing", 5000,
     ["dario-ceo"], ["Reusar pattern de 2026-05-16 - SAQUEI - Mom Test Outreach Script 15 Entrevistas.md"], None),

    ("CUI-007",
     "Recrutar 10 entrevistados BR — LinkedIn + WhatsApp outreach",
     "Executar outreach para recrutar 10 cuidadores qualificados. Estratégia: LinkedIn Sales Navigator (filtros: BR, 35-55, 'filho/filha', mid-management+), WhatsApp groups familiares (não founders' network), referral by Fabio's BR network (com critério Mom Test). Target: 50 outreaches → 20 respostas → 10 confirmados. Output: roster 10 entrevistados confirmed + slots agendados na próxima semana.",
     "critical", "dario-content", "worker-content", ["CUI-006"], "default", 4000,
     ["dario-ceo", "user"], ["Trabalho humano paralelo a tasks de agente — pode demorar 5-7 dias"], None),

    ("CUI-008",
     "Conduzir 10 entrevistas Mom Test + escrever DISCOVERY-REPORT.md",
     "Founder conduz 10 entrevistas 45-60min cada, transcreve quotes literais. Agente analisa transcripts: (1) 10 personas (nome fictício, idade, contexto, quote-âncora); (2) 5 padrões recorrentes (com frequência: '8/10 disseram X'); (3) 3 hipóteses validadas + 2 invalidadas; (4) 10 quotes ouro para copy; (5) tabela de pain points por severity × frequency; (6) willingness to pay analysis (R$ 29.90 ok? push tier acima?). Output: DISCOVERY-REPORT.md.",
     "critical", "a360-validacao", "worker-product", ["CUI-007"], "critical", 15000,
     ["dario-ceo", "user"], ["Founder faz entrevistas — agente analisa output"], None),

    ("CUI-009",
     "GO/PIVOT/KILL decision gate — Phase 0 review",
     "Founder review de DISCOVERY-REPORT.md com agente facilitador. Critérios GO: (1) ≥7/10 entrevistados confirmam problema real e doloroso; (2) ≥5/10 pagariam R$ 29.90 ou mais com pre-commit; (3) zero red flags LGPD/ético; (4) insight central confirmado ('idoso não instala'). Se PIVOT: pivot direction + nova spec. Se KILL: post-mortem + reuso de aprendizagens. Output: PHASE-0-GATE-DECISION.md + memo founder.",
     "critical", "dario-diagnose", "dario-ceo", ["CUI-008"], "critical", 5000,
     ["dario-ceo", "user"], ["Gate humano OBRIGATÓRIO antes de Phase 1"], None),

    # ==== WAVE 2 — Phase 1 PRD (W3, depends on GO from CUI-009) ====
    ("CUI-010",
     "PRD.md — 30+ user stories com RICE scoring + acceptance criteria",
     "Construir PRD completo: (1) Problem statement 250 palavras com 3 quotes literais; (2) 3 personas detalhadas (Marina cuidadora · Sr. José idoso · Carla co-cuidadora); (3) 30+ user stories formato 'Como X eu quero Y para Z' com acceptance criteria 3-5 bullets cada + RICE score + P0/P1/P2; (4) Top 12 P0 user stories obrigatórias (do briefing); (5) Out of scope explicit (telemed própria, geo-tracking, app nativo, marketplace cuidadores, SUS); (6) Success criteria mensuráveis por US. Output: PRD.md.",
     "critical", "dario-product", "worker-product", ["CUI-009"], "client_facing", 18000,
     ["dario-ceo"], ["Bloqueia design e engineering"], None),

    ("CUI-011",
     "Schema Prisma final + migrations + ConsentLog imutável",
     "Implementar schema completo: Family, FamilyCaregiver, Elder, Medication, MedicationReminder, Appointment, Document, TimelineEvent, FamilyInvitation + enums (CaregiverRole, ElderStatus, MedFrequency, ReminderStatus, AppointmentStatus, DocumentCategory, EventType). Estender ConsentLog do SAQUEI com action types: CONSENT_GIVEN/REVOKED/DATA_ACCESS/DATA_DELETION + evidence Json (whatsapp message_id, IP hashed, user agent). Index strategy + cascade deletes (LGPD-safe). Output: schema.prisma + migration files + ER diagram.",
     "critical", "builder-database-schema", "worker-builder-database-schema", ["CUI-010"], "critical", 10000,
     ["dario-ceo"], ["LGPD-safe cascade deletes obrigatório"], None),

    ("CUI-012",
     "API endpoints spec + auth matrix + webhook architecture",
     "Documentar 12 endpoints core: /api/family/create, /api/family/{id}/elders/add, /api/family/{id}/elders/{eid}/consent (public+token), /api/family/{id}/invite-caregiver, /api/elder/{id}/medications, /api/elder/{id}/appointments, /api/elder/{id}/documents/upload, /api/elder/{id}/timeline, /api/elder/{id}/sos (public+token), /api/webhooks/whatsapp, /api/cron/daily, /api/admin/*. Para cada: method, payload schema, auth requirement (auth/public+token/admin/cron secret), rate limit, audit log fields. Output: API-SPEC.md + OpenAPI 3.0 yaml.",
     "critical", "builder-api-design", "worker-builder-api-design", ["CUI-010", "CUI-011"], "critical", 12000,
     ["dario-ceo"], [], None),

    ("CUI-013",
     "ARCHITECTURE.md consolidado — system design + ADRs",
     "Consolidar architecture decisions em 1 doc: (1) System diagram (Next.js + Postgres + Resend + WhatsApp Meta + Stripe + Cloudinary + Sentry); (2) Data flow: cuidador adiciona idoso → WhatsApp consent → ACTIVE → medication scheduled → reminder cron → WhatsApp → confirm → timeline event; (3) ADRs 5-7: Why Postgres vs Mongo, Why monolith vs micro, Why Meta direto vs Twilio, Why PWA vs nativo, Why server actions vs GraphQL; (4) Security model + threat assessment; (5) Scaling plan (50K users → migrate to Supabase). Output: ARCHITECTURE.md.",
     "high", "dario-product", "worker-product", ["CUI-011", "CUI-012"], "client_facing", 12000,
     ["dario-ceo"], [], None),

    # ==== WAVE 3 — Phase 2 Design System (W4) ====
    ("CUI-014",
     "Brand identity workshop — paleta + logo concept + tom voz + naming validation",
     "Brand workshop completo Kapferer Prism + archetype: (1) Posicionamento 'Notion para famílias com idosos'; (2) Archetype recomendado (The Caregiver + The Sage blend); (3) Paleta primária verde-azulado #2D8F8C ou alternativas; (4) Paleta secundária coral/peach warmth; (5) Logo concept coração+casa (3 direções); (6) Tom voz: caloroso, respeitoso, sem infantilizar idoso, directo com cuidador; (7) Banned words list; (8) Naming validation Cuidaí (sentido em PT-BR, pronunciation, brand collision check). Output: BRAND-IDENTITY.md + brief para designer freelance/99Designs.",
     "critical", "dario-brand", "worker-brand", ["CUI-001", "CUI-009"], "client_facing", 10000,
     ["dario-ceo"], ["Founder approval obrigatório antes de hire designer"], None),

    ("CUI-015",
     "Design tokens Tailwind config — 2 paletas (cuidador denso + idoso AAA)",
     "Implementar design tokens v1: (1) App cuidador: Inter 14-16px base, contraste WCAG AA; (2) App idoso: Inter 20px base, button-min-height 56px, contraste WCAG AAA (7:1), evitar verde-vermelho (daltonismo); (3) Spacing scale 4-8-12-16-24-32-48-64; (4) Border radius scale; (5) Shadow tokens (subtle elevation); (6) Animation tokens com prefers-reduced-motion fallbacks. Output: tailwind.config.ts + tokens.css + design-tokens.json.",
     "high", "builder-design-system", "worker-builder-react-components", ["CUI-014"], "default", 6000,
     ["dario-ceo"], ["A11y AAA não-negociável no app idoso"], None),

    ("CUI-016",
     "15 telas Figma high-fidelity — landing + onboarding + dashboards + app idoso",
     "Design 15 telas P0 high-fidelity mobile-first 375px: Landing (3 sections + CTA), Onboarding cuidador 4 steps, Add idoso + WhatsApp consent, Dashboard diário cuidador, Página idoso individual, Adicionar medicação, Calendário família, Cofre documentos, Histórico/timeline, Pricing, Settings + apagar conta, App idoso PWA confirmar medicação, App idoso SOS, Admin NASA-style, Family invite flow. Inclui empty states + error states + loading states. Output: Figma file shared link + 15 screens MP/desktop.",
     "critical", "builder-landing-page", None, ["CUI-014", "CUI-015"], "client_facing", 8000,
     ["dario-ceo", "user"], ["BLOCKED — designer externo necessário OR usar v0.dev + ajuste manual"], "designer_external_required"),

    ("CUI-017",
     "Component library spec — 12 core shadcn customizados + Storybook",
     "Especificar 12 componentes core baseados em shadcn/ui + Radix: Button (3 variants + aria-labels), Card (caregiver+idoso variants), Calendar (multi-user color-coded), Medication card (confirm button gigante), Document upload (drag-drop + OCR feedback), Empty states (10 estados ilustrados), Loading states (skeletons + mensagens contextuais SAQUEI-style), Toast notifications (push+erro), SOS button (vermelho 1-clique), Family member card, Timeline event, Modal consent LGPD. Output: COMPONENTS.md + Storybook setup config.",
     "high", "builder-react-components", "worker-builder-react-components", ["CUI-015"], "default", 8000,
     ["dario-ceo"], [], None),

    # ==== WAVE 4 — Sprint 1 Engineering (W5-6) ====
    ("CUI-018",
     "Repo setup + Vercel + Postgres + CI/CD bootstrap",
     "Bootstrap completo: (1) GitHub repo private cuidai (fork SAQUEI structure); (2) Next.js 15 App Router scaffold + TS strict; (3) Vercel project linked + env vars (DATABASE_URL, AUTH_SECRET, RESEND_KEY, WHATSAPP_TOKEN, STRIPE_KEYS, CRON_SECRET, SENTRY_DSN); (4) Postgres provisioned (Vercel Marketplace); (5) Prisma migrate; (6) Auth.js v5 base config; (7) GitHub Actions CI (typecheck + test + lint + build); (8) Vercel preview deploys auto on PR; (9) Custom domain cuidai.com.br + SSL. Output: repo live + first deploy preview.",
     "critical", "builder-vercel-deploy", "worker-builder-vercel-deploy", ["CUI-001", "CUI-003", "CUI-013"], "critical", 8000,
     ["dario-ceo"], ["Sem domain confirmado em CUI-001, usar staging temporário"], None),

    ("CUI-019",
     "Auth + Family + Elder models implementation + base API",
     "Implementar foundation backend: (1) Auth.js v5 com providers email + Google + magic link; (2) Family + FamilyCaregiver + Elder models Prisma com RLS pattern; (3) Server actions: createFamily, addCaregiver, addElder (sem WhatsApp consent ainda); (4) Middleware auth + family ownership check; (5) Audit log em ConsentLog para cada mutation; (6) Tests unit ≥80% nos engines. Output: PR mergeable + tests passing.",
     "critical", "builder-auth-system", "worker-builder-auth-system", ["CUI-011", "CUI-018"], "critical", 12000,
     ["dario-ceo"], [], None),

    ("CUI-020",
     "Onboarding flow cuidador (4 steps) — UI + analytics",
     "Implementar onboarding cuidador 4 passos: (1) Welcome + value prop; (2) Criar família + role primary caregiver; (3) Adicionar primeiro idoso (nome + WhatsApp + relação); (4) Convite co-cuidadores (skippable). Inclui: skeleton states (SAQUEI-style), progress indicator, exit intent capture, analytics events por step, A11y WCAG AAA. Output: feature mergeable + Playwright E2E test passing.",
     "high", "builder-react-components", "worker-builder-react-components", ["CUI-016", "CUI-017", "CUI-019"], "client_facing", 10000,
     ["dario-ceo"], [], None),

    ("CUI-021",
     "Add elder + WhatsApp consent flow (CRÍTICO LGPD)",
     "Implementar fluxo crítico LGPD: (1) Cuidador adiciona idoso → status PENDING_CONSENT; (2) Cron envia WhatsApp ao idoso com template aprovado Meta (SIM/NÃO/INFO quick-reply buttons); (3) Webhook recebe resposta → atualiza status (ACTIVE/REJECTED/EXPIRED) + audit log com message_id imutável; (4) Re-ask em 24h se INFO selecionado; (5) Endpoint público /api/elder/{token}/delete-me para revogação direta pelo idoso; (6) Testes E2E completos. Output: feature live + LGPD audit trail verificado.",
     "critical", "builder-api-design", "worker-builder-api-design", ["CUI-004", "CUI-012", "CUI-019"], "critical", 15000,
     ["dario-ceo", "user"], ["Insight central depende disto funcionar perfeitamente"], None),

    ("CUI-022",
     "Parecer LGPD formal entregue — escritório externo",
     "Receber e revisar parecer formal do escritório escolhido em CUI-002. Inclui: RIPD completo · bases legais · termos uso · política privacidade · modelo consent WhatsApp · processo notificação ANPD · análise transferência internacional. Founder review + ajustes finais + publicação em /seguranca. Output: LGPD-RIPD.md + termos publicados + DPO designado.",
     "critical", "dario-legal", "worker-legal", ["CUI-002"], "critical", 8000,
     ["dario-ceo", "user"], ["Trabalho externo escritório — 4-6 semanas"], "external_legal_pending"),

    # ==== WAVE 5 — Sprint 2 (W7-8) ====
    ("CUI-023",
     "Medication CRUD + reminder engine + escalation cuidador",
     "Implementar core medication: (1) CRUD medication (até 10 por idoso) com frequency DAILY/EVERY_OTHER_DAY/WEEKLY/AS_NEEDED + scheduledTimes até 4/dia; (2) Reminder engine: cron a cada 30min cria MedicationReminder PENDING; (3) Notification 15min antes via WhatsApp; (4) Escalation: PENDING >30min → push cuidador, PENDING >60min → push co-cuidadores; (5) Idoso pro-active 'já tomei'; (6) Receita controlada flag + expiresAt alert D-14/D-7; (7) Histórico 90 dias mínimo. Output: feature live + E2E test.",
     "critical", "builder-api-design", "worker-builder-api-design", ["CUI-019", "CUI-021"], "critical", 18000,
     ["dario-ceo"], [], None),

    ("CUI-024",
     "WhatsApp confirmation flow + webhook signature verify + idempotency",
     "Robustez do canal idoso: (1) Webhook /api/webhooks/whatsapp com signature verification Meta; (2) Idempotency key por message_id (evitar double-confirm); (3) Parse confirmações: 'SIM'/'1'/👍/quick-reply → MedicationReminder CONFIRMED + TimelineEvent MEDICATION_TAKEN; (4) Parse 'CANCELAR' → revogação consent + apagar dados <24h; (5) Fallback parsing AI (claude haiku) para variações naturais; (6) Rate limit anti-abuse; (7) Audit log evidence completo. Output: feature live + 100% coverage parsing edge cases.",
     "critical", "builder-api-design", "worker-builder-api-design", ["CUI-021", "CUI-023"], "critical", 12000,
     ["dario-ceo"], [], None),

    ("CUI-025",
     "Dashboard diário cuidador — real-time status + Burden Index",
     "Dashboard mobile-first cuidador: (1) Status cards por idoso (medicações hoje confirmed/pending/missed, próxima consulta, alertas); (2) Timeline real-time eventos últimas 48h; (3) Quick actions (add medicação, upload doc, ligar SOS); (4) Burden Index visualization (se cuidador >30 actions/dia, sugerir descanso); (5) Co-cuidadores avatars + last seen; (6) Empty states ilustrados; (7) Pull-to-refresh + skeleton loading. Output: feature live + Lighthouse mobile ≥90.",
     "high", "builder-react-components", "worker-builder-react-components", ["CUI-016", "CUI-023"], "client_facing", 12000,
     ["dario-ceo"], [], None),

    ("CUI-026",
     "Cron daily consolidado — 7 jobs num endpoint (SAQUEI pattern)",
     "Implementar /api/cron/daily com 7 jobs (executar a cada 30min): (1) Lembretes medicação SCHEDULED → SENT; (2) Alertas missed (>30min escala cuidador, >60min co-cuidadores); (3) Welcome lifecycle 5 emails T+0/+1/+3/+7/+14; (4) Receitas controladas alert D-14 e D-7; (5) Consultas alert D-1 e D-0; (6) Burden Index check + suggest rest; (7) NPS survey T+30 primeiro idoso added. Vercel cron schedule + CRON_SECRET. Output: cron live + audit log diário + Sentry monitoring.",
     "critical", "builder-api-design", "worker-builder-api-design", ["CUI-023"], "critical", 10000,
     ["dario-ceo"], ["Reusar 95% da engine consolidated SAQUEI"], None),

    ("CUI-027",
     "Recrutar 5 design partners (founders' network) — beta privado",
     "Outreach founders' network para 5 famílias design partners. Critério: pais 65+ vivos, cuidador 35-55, openness para feedback semanal, willingness para 3 user testing sessions. Onboard manual (white-glove): setup WhatsApp consent + primeira medicação + primeiro doc + tour produto. Incentivo: 12 meses Plus grátis + influência roadmap + testimonial. Output: 5 famílias onboarded + canal WhatsApp grupo design partners.",
     "high", "dario-content", "worker-content", ["CUI-021", "CUI-023", "CUI-024", "CUI-025"], "default", 5000,
     ["dario-ceo", "user"], [], None),

    # ==== WAVE 6 — Sprint 3 (W9-10) ====
    ("CUI-028",
     "Document vault + OCR (Tesseract client + API server-side fallback)",
     "Cofre documentos: (1) Upload drag-drop com preview; (2) Categories: PRESCRIPTION, EXAM, ID, INSURANCE, OTHER; (3) Tesseract.js client-side para imagens; (4) API server-side fallback para PDFs grandes (>5MB); (5) ocrText indexed para search; (6) Encriptação at-rest (Cloudinary signed URLs); (7) Preview inline (image + PDF); (8) Sharing com co-cuidadores via permissions matrix; (9) Audit log cada acesso. Output: feature live + 100% OCR success rate em test set.",
     "high", "builder-api-design", "worker-builder-api-design", ["CUI-019", "CUI-022"], "client_facing", 14000,
     ["dario-ceo"], [], None),

    ("CUI-029",
     "Calendar shared family — consultas + medicação + eventos sociais",
     "Calendar multi-user color-coded: (1) Vistas dia/semana/mês mobile-friendly; (2) Tipos eventos: consulta, medicação tomada, exame, aniversário, visita; (3) Color coding por cuidador (Marina rosa, Carla azul, etc); (4) Add via quick action + lembrete D-1; (5) iCal export; (6) Sync Google Calendar opcional (OAuth); (7) Empty state primeira consulta. Output: feature live + E2E test.",
     "medium", "builder-react-components", "worker-builder-react-components", ["CUI-025"], "client_facing", 10000,
     ["dario-ceo"], [], None),

    ("CUI-030",
     "SOS button + escalation cuidador → co-cuidadores → emergência",
     "Feature crítica idoso: (1) SOS button gigante vermelho na PWA idoso (sempre visível); (2) URL pública /sos/{token} (não precisa login); (3) Trigger → push imediato cuidador primário + email + WhatsApp; (4) Se sem resposta 5min → escala co-cuidadores; (5) Se sem resposta 15min → opção contactar 192 SAMU (botão explicito no app cuidador); (6) Audit log GPS opcional (se idoso autorizou previamente); (7) Test mode mensal para idoso treinar; (8) False positive recovery flow. Output: feature live + E2E test push <30s.",
     "critical", "builder-api-design", "worker-builder-api-design", ["CUI-021", "CUI-025"], "critical", 12000,
     ["dario-ceo"], ["Saúde sensível — zero tolerance bug"], None),

    ("CUI-031",
     "Co-caregiver invite flow + permissions matrix",
     "Convites co-cuidadores: (1) Cuidador primário envia invite por email; (2) Token único 7 dias expiry; (3) Aceite → join Family com role CO_CAREGIVER ou OBSERVER; (4) Permissions matrix: PRIMARY pode tudo, CO_CAREGIVER pode read/write medication/appointments/documents, OBSERVER só read; (5) Audit log mudanças de role; (6) Limite 5 caregivers por family (tier Família); (7) Notification quem aceitou. Output: feature live + E2E test.",
     "high", "builder-react-components", "worker-builder-react-components", ["CUI-019"], "client_facing", 8000,
     ["dario-ceo"], [], None),

    ("CUI-032",
     "+5 design partners (total 10) + NPS survey M3",
     "Onboard segunda batch 5 famílias design partners. Inclui: cohort diversity (cidades diferentes, situações diferentes — pai sozinho, casal idoso, idoso com demência leve, etc). NPS survey após 30 dias de uso (target NPS ≥40). Feedback consolidado bi-semanal. Iteration rápida em pain points. Output: 10 famílias ativas + NPS report M3 + roadmap ajustado.",
     "high", "dario-content", "worker-content", ["CUI-027"], "default", 5000,
     ["dario-ceo", "user"], [], None),

    # ==== WAVE 7 — Polish (W11) ====
    ("CUI-033",
     "E2E Playwright — 5 critical flows 100% pass",
     "Implementar Playwright tests para 5 fluxos críticos: (1) Sign up → criar família → adicionar idoso → WhatsApp consent → primeira medicação; (2) Idoso confirma medicação WhatsApp → status atualiza dashboard; (3) Cuidador upload documento → OCR processa → searchable; (4) SOS idoso → cuidador push <30s; (5) Apagar conta → DB vazio confirmado <24h. CI must block deploy se algum falhar. Output: 5 specs + GitHub Actions integration.",
     "critical", "builder-react-components", "worker-builder-react-components", ["CUI-021", "CUI-023", "CUI-024", "CUI-028", "CUI-030"], "critical", 10000,
     ["dario-ceo"], [], None),

    ("CUI-034",
     "Lighthouse 100 A11y audit + fix all violations",
     "Audit completo a11y: (1) Lighthouse mobile Performance ≥90 + Accessibility 100 + Best Practices ≥95 + SEO ≥95 em todas core pages; (2) axe-core automated em CI; (3) Manual screen reader test (NVDA + VoiceOver); (4) Keyboard navigation 100% reachable; (5) Color contrast WCAG AAA em app idoso; (6) Focus management correto em modals + forms; (7) Reduced motion respeitado. Output: a11y-audit-report.md + fixes merged.",
     "critical", "accessibility", "worker-product", ["CUI-020", "CUI-025", "CUI-029"], "critical", 10000,
     ["dario-ceo"], ["Saúde = WCAG AAA não-negociável"], None),

    ("CUI-035",
     "Sentry production + observability + alerting",
     "Production observability: (1) Sentry org + project setup com source maps; (2) LGPD scrubbing (PII redaction em events); (3) Performance monitoring transactions críticas; (4) Vercel Analytics + custom events (medication_confirmed, sos_triggered, family_created, etc); (5) Alerts: prod errors >5/dia, API p95 >500ms, cron failures; (6) Slack webhook para alerts críticos; (7) Status page público (cuidai.com.br/status). Output: monitoring live + first alert test.",
     "high", "dario-product", "worker-product", ["CUI-018"], "default", 6000,
     ["dario-ceo"], [], None),

    ("CUI-036",
     "Stripe BR + PIX live + transações teste real",
     "Pagamentos production: (1) Stripe BR account ativo + PIX integration; (2) 3 tiers checkout (Free, Família R$ 29.90, Família+ R$ 49.90); (3) Trial 14 dias sem cartão; (4) Garantia 7 dias visível checkout; (5) Webhook signed para subscription events; (6) Customer Portal Stripe-hosted; (7) Invoice automation; (8) Test 3 transações reais (R$ 1 teste) Visa + Master + PIX. Output: payments live + first real transaction confirmed.",
     "critical", "dario-product", "worker-product", ["CUI-019"], "financial", 8000,
     ["dario-ceo", "user"], ["Stripe BR onboarding pode demorar — começar W7"], None),

    ("CUI-037",
     "5 testimoniais reais coletados + publicados landing",
     "Coletar 5 testimoniais autênticos das 10 design partners (incentivo 6m Plus grátis adicional): (1) Format vídeo 30-60s OR texto + foto; (2) Estrutura: situação antes → mudança Cuidaí → resultado mensurável; (3) Permissões uso landing + redes (RGPD signed); (4) 5 testimoniais publicados landing com schema Review JSON-LD; (5) Diversidade cohort (cidades, idades, situações). Output: 5 testimoniais publicados + assets para landing.",
     "high", "dario-content", "worker-content", ["CUI-032"], "client_facing", 5000,
     ["dario-ceo", "user"], [], None),

    # ==== WAVE 8 — Launch (W12) ====
    ("CUI-038",
     "Launch checklist 100% verde — gate final",
     "Verificar 100% checklist launch (técnico + compliance + produto + negócio + marketing). Bloqueia launch se qualquer item vermelho. Inclui: Lighthouse 100 A11y, E2E 100% pass, Sentry capturing, DB backup auto, rate limits, HTTPS forced, CSP headers, sitemap+robots, OG images, parecer LGPD publicado, DPO email funcional, termos+privacidade, cookie banner, direito esquecimento testado, 10 design partners NPS≥40, 5 testimoniais, Stripe+PIX real, customer support SLA. Output: LAUNCH-CHECKLIST.md verde 100%.",
     "critical", "builder-launch-checklist", "worker-product", ["CUI-022", "CUI-033", "CUI-034", "CUI-035", "CUI-036", "CUI-037"], "critical", 8000,
     ["dario-ceo", "user"], ["GATE OBRIGATÓRIO antes de press"], None),

    ("CUI-039",
     "Launch — ProductHunt + LinkedIn manifesto + Press release 5 outlets",
     "Executar launch coordenado: (1) ProductHunt launch terça-feira 00:01 PT com hunter influencer + pre-mailing 100+ na lista; (2) LinkedIn manifesto pessoal Fabio (3K palavras storytelling construir Cuidaí); (3) Press release para Exame, Valor, NeoFeed, Pequenas Empresas, Olhar Digital + 5 follow-ups; (4) WhatsApp groups familiares estratégicos (manual 20 groups); (5) 5 Facebook groups cuidadores BR. Coordinated timing: PH 00:01, LinkedIn 07:00, Press send 08:00. Output: launch executado + métricas D+1.",
     "critical", "dario-pr", "worker-pr", ["CUI-038"], "client_facing", 12000,
     ["dario-ceo", "user"], [], None),

    ("CUI-040",
     "Paid ads R$ 500 piloto + monitoring 24/7 primeiros 7 dias",
     "Smoke test paid + watch: (1) Meta Ads R$ 500 piloto: 3 creatives (problem-focused, solution-focused, testimonial), 3 audiências (lookalike SAQUEI users, interesse 'cuidadores', filhos 35-55); (2) Track CAC, CVR landing, install→signup→active; (3) Monitoring 24/7 primeiros 7 dias: oncall Fabio rotation, Sentry alerts → Slack, page se prod errors >10/dia; (4) Daily standup post-launch D+1 a D+7; (5) Iteration rápida em pain points reais. Output: ads piloto report + 7-day retrospective.",
     "high", "dario-ads-blueprint", "worker-ads", ["CUI-039"], "financial", 8000,
     ["dario-ceo", "user"], ["Budget contained R$ 500 max"], None),
]

# Write tasks
output_dir = Path.home() / ".claude" / "orchestrator" / "tasks" / "active"
output_dir.mkdir(parents=True, exist_ok=True)

created = []
for (tid, title, desc, prio, skill, assignee, deps, policy, est_tokens, watchers, notes_extra, blocked_reason) in TASKS:
    task = {
        "id": tid,
        "title": title,
        "description": desc.replace("\n", " ").strip(),
        "status": "blocked" if blocked_reason else "todo",
        "priority": prio,
        "project": "cuidai",
        "skill": skill,
        "assignee": assignee,
        "depends_on": deps,
        "execution_policy": policy,
        "blocked_reason": blocked_reason,
        "revision_count": 0,
        "revision_max_loops": 3 if policy == "critical" else 3,
        "watchers": watchers,
        "sla_deadline": sla(policy),
        "estimated_tokens": est_tokens,
        "notes": ["Generated by bootstrap_cuidai_taskboard.py 2026-05-16"] + (notes_extra or []),
        "created_at": NOW,
    }
    fpath = output_dir / f"{tid}.yaml"
    with open(fpath, "w", encoding="utf-8") as f:
        yaml.dump(task, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    created.append(tid)

print(f"Created {len(created)} tasks in {output_dir}")
print("Status breakdown:")
print(f"  todo: {sum(1 for t in TASKS if not t[11])}")
print(f"  blocked: {sum(1 for t in TASKS if t[11])}")
print("\nFirst 3 ready to dispatch (no deps):")
for (tid, title, _, _, _, _, deps, _, _, _, _, _) in TASKS[:5]:
    if not deps:
        print(f"  {tid} — {title[:80]}")
