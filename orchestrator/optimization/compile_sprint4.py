"""Sprint 4 — DSPy compile with EXPANDED goldens + held-out test + MIPROv2.

Lessons from sprint3v2 (DSPY_ROOT_CAUSE.md):
  1. Metric fix alone didn't lift — ceiling effect was the bottleneck
  2. 3 goldens × 2 demos is too shallow for bootstrap
  3. Re-eval on training set is noisy (±5pt single-pass variance)
  4. Need cross-vertical goldens + held-out test + multi-pass

This sprint addresses all four:
  - 10 goldens per skill (3 original + 7 new cross-vertical)
  - Held-out test set: 3 briefings per skill, NEW verticals not in trainset
  - MIPROv2 instead of BootstrapFewShot (instruction optimization too)
  - 3 evaluation passes per held-out briefing → bound variance

Strict honest metrics policy:
  - Writes ONLY to dedicated namespace (`avg_judge_heldout_sprint4`,
    `heldout_scores_sprint4`, `heldout_variance_sprint4`)
  - Does NOT touch avg_quality_score (production delivery signal)

Run:
    python -m optimization.compile_sprint4

Estimated cost: $5-10 (MIPROv2 is ~5-10× BootstrapFewShot per skill +
multi-pass held-out evals). Time: ~10-20 min.
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path

ORCH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ORCH_DIR))

import dspy
from dspy.teleprompt import MIPROv2

from optimization.compile_sprint3 import (
    FUNNEL_GOLDENS,
    OFFER_GOLDENS,
    PITCH_GOLDENS,
    FunnelDesignProgram,
    OfferGenerationProgram,
    PitchDeckProgram,
)
from scripts.anthropic_spend_wrapper import TrackedAnthropic

try:
    from ruamel.yaml import YAML
    _y = YAML(); _y.preserve_quotes = True; _y.width = 200
    def load_y(p):
        with open(p, encoding='utf-8') as f: return _y.load(f)
    def dump_y(d, p):
        with open(p, 'w', encoding='utf-8') as f: _y.dump(d, f)
except ImportError:
    import yaml
    def load_y(p):
        with open(p, encoding='utf-8') as f: return yaml.safe_load(f)
    def dump_y(d, p):
        with open(p, 'w', encoding='utf-8') as f: yaml.safe_dump(d, f, sort_keys=False)


# ─────────────────────────────────────────────────────────────────────────────
# EXPANDED GOLDENS — 7 new cross-vertical per skill (services, hospitality,
# e-commerce, education, mobile, B2B EU, etc.)
# ─────────────────────────────────────────────────────────────────────────────

OFFER_EXTRA = [
    dspy.Example(
        briefing="Clinica veterinaria Lisboa Cascais. Target: tutores caes/gatos 30-55 com pet ja existente. Servico: consulta + vacinas + cirurgia. Preco consulta 45 EUR. Concorre clinicas vizinhanca.",
        core_offer="A unica clinica veterinaria de Lisboa-Cascais com app de saude do pet — historico clinico, vacinas em dia e telemedicina 24/7 incluida em todas as consultas. 12 anos de experiencia, 8000+ pets seguidos.",
        value_equation="Dream: tutor que sabe sempre o que o pet precisa, sem panico noturno. Likelihood: 94% pets monitorizados sem emergencia surpresa. Time: app activa em 24h. Effort: 1 download + 1 visita inicial.",
        risk_reversal="Primeira consulta gratuita se a app nao gerar pelo menos 1 alerta clinicamente relevante nos primeiros 60 dias.",
        bonuses=[
            "App de saude do pet com timeline + alertas — valor 89 EUR/ano",
            "1a consulta de avaliacao comportamental — valor 65 EUR",
            "Chat vet 24/7 para 30 dias — valor 49 EUR",
        ],
        urgency="Vagas para programa de prevencao 2026 limitadas a 200 pets — fecha admissao 31/Mar.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="Clinica dentaria Sao Paulo. Target: profissionais 25-45 querem alinhadores invisiveis. Plano alinhador 6 meses R$ 8.000. Concorre Sorridents/franchises.",
        core_offer="O unico plano de alinhadores invisiveis com ortodontista presencial em SP — escaneamento 3D no consultorio + 6 meses de tratamento + retencao 12 meses, garantia de sorriso ou refaz.",
        value_equation="Dream: sorriso alinhado para foto profissional sem aparelho visivel. Likelihood: 91% casos completam em 6 meses. Time: scan em 30 min, alinhadores em 7 dias. Effort: trocar alinhador a cada 14 dias.",
        risk_reversal="Garantia de sorriso: se aos 6 meses nao atingir o resultado planeado no scan inicial, refazemos sem custo + reembolso de 30%.",
        bonuses=[
            "Clareamento dental profissional pos-tratamento — valor R$ 1.200",
            "Retentor invisivel x2 (substituicao automatica) — valor R$ 800",
            "Plano de manutencao trimestral 12 meses — valor R$ 1.800",
        ],
        urgency="Tabela R$ 8K trava em 30/Jun/2026 — apos isso plano sobe para R$ 9.500 com novo material premium.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="Cadeia de restaurantes Porto+Braga (4 unidades). Target: jantar casal + grupo 4-6 amigos. Ticket medio 28 EUR. Quer aumentar frequencia/cliente.",
        core_offer="O clube Mesa Cheia — 4 jantares/mes em qualquer das 4 casas + reserva garantida + drink boas-vindas, por 79 EUR/mes (poupa 33 EUR no ticket).",
        value_equation="Dream: jantar fora 1x/semana sem pensar em onde nem em conta. Likelihood: 88% membros usam 3+ jantares/mes. Time: activacao imediata. Effort: 1 reserva por app, 30 segundos.",
        risk_reversal="1o mes gratuito + cancela quando quiseres. Se nao usares pelo menos 2 jantares no mes, devolvemos a mensalidade integral.",
        bonuses=[
            "Lugar de estacionamento garantido em todas as casas — valor 12 EUR/visita",
            "Acesso a chef's table 1x/trimestre — valor 95 EUR",
            "Convite para eventos exclusivos (degustacao vinhos, harmonizacoes) — valor 240 EUR/ano",
        ],
        urgency="Primeiros 100 membros — preco fechado vitalicio em 79 EUR. Depois sobe para 99 EUR.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="E-commerce moda feminina BR (DTC, sem fisicas). 24K seguidores IG. Ticket medio R$ 280. Conversion 1.8%. Quer subir AOV + repeat.",
        core_offer="A Caixa Curadoria mensal — 3 pecas escolhidas pelo nosso stylist com base no teu perfil, R$ 590/mes (poupa R$ 250 vs avulso) + troca livre em 14 dias.",
        value_equation="Dream: armario sempre actualizado sem horas a navegar feeds. Likelihood: 93% pecas usadas no mes seguinte. Time: caixa chega em 5 dias. Effort: questionario 8 minutos uma vez.",
        risk_reversal="1a caixa com 50% off + frete gratis. Se nao gostares de pelo menos 2 das 3 pecas, devolves tudo e nao pagas nada.",
        bonuses=[
            "Consultoria estilo 30 min com stylist senior — valor R$ 280",
            "Acesso early a colecoes (48h antes lancamento publico) — valor R$ 450/ano",
            "Vouchers de 10% para indicacoes (sem limite) — valor variavel",
        ],
        urgency="Curadoria limitada a 500 clientes activas — restam 87 vagas para o stylist senior do Sul-Sudeste.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="Curso online arquitectura paramétrica (Grasshopper/Rhino). Target: arquitectos 25-40 ja em pratica. Pricing 1.500 EUR programa 12 semanas. Concorre Coursera/Udemy/cursos pontuais.",
        core_offer="O unico programa de 12 semanas com mentor arquitecto senior + revisao 1-1 dos teus projetos reais + certificacao validada por escritorios parceiros (5 escritorios PT/EU contratam graduados directamente).",
        value_equation="Dream: arquitecto que entrega projetos parametricos premium e cobra 30% mais. Likelihood: 87% concluem com portfolio + 64% mudam de emprego em 6 meses. Time: 12 semanas (5h/sem). Effort: 1 projecto real, mentor revê.",
        risk_reversal="Garantia de empregabilidade: se aos 6 meses pos-conclusao nao tiveres uma proposta concreta de mudanca, devolvemos 70% do investimento.",
        bonuses=[
            "Mentoria 1-1 mensal por 6 meses pos-curso — valor 1.800 EUR",
            "Acesso vitalicio a biblioteca de scripts/templates (200+) — valor 590 EUR",
            "Apresentacao do portfolio a 5 escritorios parceiros — valor 1.200 EUR",
        ],
        urgency="Turma Maio 2026 limitada a 25 alunos para garantir 1-1 com mentor — restam 9 vagas.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="App mobile pet grooming agendamento. Target: tutores urbanos cidades >500K hab BR. Modelo marketplace (50+ groomers). Comissao 18%. Concorre Petlove/agendamento manual.",
        core_offer="O unico app de pet grooming com seguro acidente incluido + groomer avaliado pela comunidade (rating publico) + agendamento em <2 min — para tutores que nao querem perder sabado a fazer telefone.",
        value_equation="Dream: pet bem cuidado, agendado no metro, sem stress de telefonemas. Likelihood: 96% reservas confirmadas em <1h. Time: app + reserva em 5 min. Effort: 1 escolha + 1 confirmacao.",
        risk_reversal="Garantia de satisfacao: se nao gostares do servico, refazemos com outro groomer gratis + 20% de credito.",
        bonuses=[
            "Seguro acidente durante banho/tosa (cobertura R$ 5K) — valor R$ 30/sessao",
            "Plano de 4 banhos com 15% desconto — valor R$ 80/mes",
            "Cashback de 5% para tutores VIP (10+ banhos/ano) — valor R$ 120+/ano",
        ],
        urgency="Lancamento Sao Paulo: primeiras 200 reservas pagam taxa fixa R$ 89 (vs R$ 120 do mercado).",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="SaaS HR analytics enterprise UK (London). Target: HR Directors empresas 500-2000 empregados. Pricing GBP 4K/mes. Concorre Workday/Visier.",
        core_offer="The only HR analytics platform with embedded compliance engine for UK Employment Act 2024 + EU AI Act — your HR data, your insights, audit-proof by design. Live deployment in <30 days.",
        value_equation="Dream: HR Director that walks into board meeting with audit-proof analytics without legal review. Likelihood: 89% reduction in compliance flags (validated 47 enterprise deployments). Time: 30 days to production. Effort: 1 data export, we handle integration.",
        risk_reversal="If you cannot demonstrate a compliance lift in the first quarterly board review, full refund + we cover the integration cost.",
        bonuses=[
            "Dedicated compliance officer 4h/month for 12 months — value GBP 9.600/year",
            "Custom dashboard for board meetings (5 templates) — value GBP 3.200",
            "Annual benchmark report (your KPIs vs UK enterprise median) — value GBP 2.400",
        ],
        urgency="UK Employment Act 2024 enforcement starts 2026-09-01. Onboarding queue full by 2026-07-15 to guarantee live before deadline.",
    ).with_inputs("briefing"),
]


FUNNEL_EXTRA = [
    dspy.Example(
        briefing="Clinica veterinaria Lisboa Cascais. Trafego: Google Maps + WhatsApp + word-of-mouth. Quer subir consultas-novas/mes de 40 para 80.",
        stages=[
            "Local SEO + Google Business — review-driven discovery em radius 5km",
            "Landing 'pet check-up gratuito' — opt-in nome+pet+WhatsApp",
            "WhatsApp drip 7 dias — historia da clinica + 3 casos sucesso + agendamento",
            "Consulta inicial 25 EUR (vs 45 normal) — porta de entrada",
            "Plano anual prevencao 240 EUR (24 EUR/mes) — upsell pos-1a-consulta",
        ],
        conversion_thresholds="Google Maps view 38% → click 12% → opt-in 28% → consulta 22% → plano anual 41%",
        copy_hooks=[
            "Hook GMaps: 'A unica clinica de Cascais com app de saude do pet'",
            "Hook landing: 'Pet check-up gratuito — saiba o que o seu pet precisa em 20 min'",
            "Hook WhatsApp dia 3: 'Como o Bobby evitou cirurgia por causa de 1 alerta na app'",
            "Hook consulta: '25 EUR para conhecer a nossa clinica — sem compromisso'",
            "Hook plano: 'Plano anual: 80 EUR/mes em consultas extra evitadas'",
        ],
        automations="opt_in → WhatsApp drip 7d. consulta_marcada → SMS recordatorio 24h+2h. consulta_feita → review request 48h + plano anual offer 7d.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="Clinica dentaria SP alinhadores invisiveis. Trafego: IG + Google Ads. CAC actual R$ 1.200 muito alto. Quer baixar para R$ 600.",
        stages=[
            "IG Reels + Google Ads — antes/depois reais + custo claro",
            "Landing 'scan 3D gratuito' — opt-in com agendamento directo",
            "Scan presencial 30 min — diagnostico + plano + valor exacto",
            "Plano R$ 8.000 (parcelado 12x R$ 720) — assinatura no dia ou 7 dias",
            "Programa de manutencao R$ 150/mes pos-tratamento — recorrencia",
        ],
        conversion_thresholds="Ad CTR 2.4% → opt-in 31% → scan 58% → plano 39% → manutencao 67%",
        copy_hooks=[
            "Hook ad: 'Sorriso alinhado em 6 meses — sem aparelho visivel'",
            "Hook landing: 'Scan 3D gratuito + plano com valor exacto em 30 min'",
            "Hook scan: 'Veja o seu sorriso final hoje, antes de decidir'",
            "Hook plano: 'R$ 720/mes — menos que cafe da manha de SP'",
            "Hook manutencao: 'Mantenha o investimento por 5+ anos com R$ 5/dia'",
        ],
        automations="opt_in → SMS 'scan agendado' + lembrete 24h. scan_feito → orcamento por email + WhatsApp drip 7d se nao fecha. plano_fechado → ciclo de produto: app + lembretes troca alinhador.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="Cadeia restaurantes Porto+Braga 4 unidades. Quer lancar clube Mesa Cheia subscription 79 EUR/mes. Base existente: 12K visitas/mes total, 0% recorrentes.",
        stages=[
            "QR code mesa + email captura — 'avalia + ganha sobremesa proxima visita'",
            "Email pos-visita — convite para clube com depoimento de membros",
            "Landing clube — video + lista de membros + 1o mes gratis",
            "Subscricao 79 EUR/mes — auto-renovacao mensal",
            "Eventos exclusivos trimestrais — retention + word-of-mouth",
        ],
        conversion_thresholds="QR scan 19% → email opt-in 64% → landing visit 22% → subscricao 14% → renovacao M2 78%",
        copy_hooks=[
            "Hook QR: 'Avalia + ganha sobremesa da casa na proxima visita'",
            "Hook email: 'Comes em 4 casas e ainda nao conheces o Mesa Cheia'",
            "Hook landing: '4 jantares/mes em qualquer das 4 casas — 79 EUR'",
            "Hook subscricao: 'Comeca hoje, 1o mes gratis, cancela quando quiseres'",
            "Hook evento: 'Apenas membros — degustacao do novo menu Outubro'",
        ],
        automations="qr_scan → email captura imediato. visit_done → review_request 48h + clube_offer 7d. subscriber → onboarding 3 emails primeira semana + monthly preview.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="E-commerce moda BR DTC. Quer lancar Caixa Curadoria R$ 590/mes. Trafego: IG ads + influencers + email base 18K.",
        stages=[
            "IG ads + parcerias influencer — quiz estilo como hook",
            "Quiz 8 perguntas — entrega preview de outfit personalizado",
            "Email com 1a caixa 50% off — urgencia stock limitado por estilo",
            "Caixa mensal R$ 590 — auto-renovacao",
            "Referral 'amiga ganha caixa gratis' — viralidade",
        ],
        conversion_thresholds="Ad CTR 1.7% → quiz start 41% → quiz complete 73% → caixa-1 24% → recorrente M3 68%",
        copy_hooks=[
            "Hook ad: 'O quiz de estilo que descobre 3 pecas perfeitas para ti'",
            "Hook quiz: 'Em 8 perguntas, vemos o teu armario ideal'",
            "Hook email: 'A tua 1a Caixa Curadoria com 50% off — apenas para o teu estilo'",
            "Hook subscricao: 'R$ 590/mes — o stylist trabalha so para ti'",
            "Hook referral: 'Indica 1 amiga — ela ganha 1a caixa gratis, tu ganhas a tua proxima'",
        ],
        automations="quiz_start → exit_intent popup com preview. caixa_recebida → review_request + 'amou?' email D+7. churn_risk → personal stylist WhatsApp D-3 antes renovacao.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="Curso online arquitectura parametrica 1.500 EUR. Trafego: LinkedIn organic + comunidades arch + indicacoes alumni.",
        stages=[
            "LinkedIn long-form posts — 1x/sem do mentor senior com projecto real",
            "Webinar gratuito mensal — 'Como o cliente X poupou 30% com paramerica'",
            "Landing video pitch — testemunhos alumni + 5 escritorios parceiros",
            "Discovery call 20 min — qualifica + plano de pagamento",
            "Programa 12 semanas 1.500 EUR — 3x sem juros ou 10% off vista",
        ],
        conversion_thresholds="LinkedIn view 4.2% → comment/share 1.8% → webinar opt-in 22% → call book 38% → matricula 41%",
        copy_hooks=[
            "Hook LinkedIn: 'Como Grasshopper poupou 8 dias num projecto de 4 meses'",
            "Hook webinar: 'O metodo paramerica que 64% dos alumni usam no 1o mes'",
            "Hook landing: '12 semanas, 1 projecto real teu, 5 escritorios parceiros olhando'",
            "Hook call: '20 min para mostrar se o programa serve para a tua pratica'",
            "Hook matricula: 'Turma Maio fecha 9 vagas — discovery call esta semana'",
        ],
        automations="linkedin_engage → connect_request + DM personalizada. webinar_attend → 3-email drip com case studies. call_no_show → 2-tentativa SMS + remarcacao.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="App pet grooming marketplace BR. Lancamento SP. Quer 500 reservas/mes em 90 dias. Comissao 18%, 50 groomers.",
        stages=[
            "ASO + Meta ads — install com hook 'banho em casa em <2h'",
            "Onboarding 90s — escolhe pet + endereco + 1a reserva preview",
            "1a reserva R$ 89 (vs R$ 120 mercado) — porta de entrada",
            "Plano 4 banhos R$ 320 (R$ 80/banho, save 11%) — recorrencia",
            "Programa indicacao R$ 30 para cada lado — viralidade",
        ],
        conversion_thresholds="Install→onboard 78% → 1a reserva 31% → plano 22% → renovacao M2 64% → indicacao 18%",
        copy_hooks=[
            "Hook ad: 'Banho do teu pet em casa em menos de 2 horas — em SP'",
            "Hook onboarding: 'Escolhe o teu groomer com avaliacao da comunidade'",
            "Hook 1a reserva: 'R$ 89 — preco de lancamento em SP'",
            "Hook plano: '4 banhos por R$ 320 — poupa R$ 160 vs avulso'",
            "Hook indicacao: 'R$ 30 para ti e R$ 30 para o amigo — sem limite'",
        ],
        automations="install → push 24h se nao reservou. 1a_reserva → SMS 'groomer a caminho' + post-service NPS. churn_risk → discount push 7d antes proxima reserva esperada.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="SaaS HR analytics enterprise UK GBP 4K/mes. Target: HR Directors empresas 500-2000 empregados. Trafego: outbound + eventos HR + content LinkedIn.",
        stages=[
            "Outbound LinkedIn — personalised DM HR Directors top 500 UK",
            "Discovery call 30 min — compliance assessment + ROI calc",
            "POC 2 weeks — sandbox com data anonimizada do prospect",
            "Pilot agreement GBP 12K (3 meses) — entry tier",
            "Annual contract GBP 48K — expansion + multi-year discount",
        ],
        conversion_thresholds="DM reply 14% → call 52% → POC accepted 38% → pilot 64% → annual 74%",
        copy_hooks=[
            "Hook DM: 'How {company} can prove Employment Act 2024 compliance to the board in Q3'",
            "Hook call: '30 min to show your compliance gap + ROI estimate vs Workday/Visier'",
            "Hook POC: 'Sandbox with your anonymised data — see your dashboard in 14 days'",
            "Hook pilot: '3 months for 4K/mo + we cover integration costs'",
            "Hook annual: '12-month commit unlocks 22% saving + dedicated compliance officer'",
        ],
        automations="DM_no_reply → follow_up D+7 with case study. call_done → personalised POC plan in 24h. POC_active → weekly executive summary email. pilot_M2 → renewal conversation booking.",
    ).with_inputs("briefing"),
]


PITCH_EXTRA = [
    dspy.Example(
        briefing="VetSemPressa — telemedicina veterinaria BR. Plataforma video-consulta + receita digital + entrega medicamento. Founder ex-Petlove. Pre-seed.",
        narrative_arc="No BR, 78M pets em 65M lares e apenas 38K vets — gargalo de acesso brutal, especialmente cidades pequenas. VetSemPressa e a Doctolib dos pets: video-consulta com vet em <15 min, receita digital integrada, medicamento entregue em casa em <24h. Founders vindos da Petlove conhecem o playbook de ops e supply chain.",
        key_slides=[
            "1. Capa — VetSemPressa: telemedicina veterinaria de A a Z em <24h",
            "2. Problema — 78M pets, 38K vets, 47% lares em cidades sem vet competente",
            "3. Solucao — Video consulta + receita digital + medicamento entregue",
            "4. Mercado — TAM R$ 8.4B (vet care BR); SAM R$ 1.9B (digital-ready); SOM R$ 38M",
            "5. Tracao — 12 vets parceiros, 340 consultas piloto, NPS 78",
            "6. Modelo — R$ 99 consulta + 15% margem medicamento + plano subscriber R$ 39/mes",
            "7. Tech — App native + plataforma vet (web) + integracao farmacia",
            "8. Compliance — Resolucao CFMV 1.232/2018 (telemedicina vet) + LGPD",
            "9. Equipa — Founder ex-Petlove ops + co-founder vet senior + CTO ex-iFood",
            "10. Roadmap — M1 5 cidades + 50 vets → M6 25 cidades + 500 vets → M12 R$ 6M ARR",
            "11. Ask — R$ 1.2M seed para M12 break-even, runway 18 meses",
            "12. Por que agora — Pos-pandemia adopcao telemedicina + Resolucao CFMV vigor 2026",
        ],
        tam_sam_som="TAM R$ 8.4B (vet care BR total). SAM R$ 1.9B (78M pets x R$ 25/mes digital-ready). SOM R$ 38M (38K pets pagantes x R$ 80/mes ano 2).",
        financial_ask="R$ 1.2M seed (10% equity, R$ 12M cap SAFE). Uso: 45% tech (app + integracao farmacia), 30% ops (recrut vets + cidades), 15% growth, 10% legal+reserva.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="AlignSmile — D2C alinhadores invisiveis BR. Modelo SmileDirectClub mas com clinica fisica em 5 capitais. R$ 4.500 plano completo. Pos-seed serie A.",
        narrative_arc="A maioria dos brasileiros nao tem acesso a alinhadores invisiveis — clinicas cobram R$ 15K+ e SmileDirectClub falhou no BR por nao ter pernas locais. AlignSmile combina o digital-first do SDC com 5 clinicas fisicas para escaneamento + atendimento — preco R$ 4.500 (70% abaixo do mercado), supply chain propria, 8K clientes em 18 meses.",
        key_slides=[
            "1. Capa — AlignSmile: alinhadores invisiveis ao alcance do brasileiro de classe media",
            "2. Problema — 65M brasileiros querem ortodontia, apenas 4% acessam invisiveis pelo preco",
            "3. Solucao — D2C digital + 5 clinicas para scan/atendimento + supply chain propria",
            "4. Mercado — TAM R$ 12B (ortodontia BR); SAM R$ 3.2B (segmento classe media-alta); SOM R$ 180M",
            "5. Tracao — 8K clientes em 18M, NPS 84, R$ 36M ARR, EBITDA -8%",
            "6. Modelo — R$ 4.500 plano completo (parcelado 18x) + R$ 980 retencao 2 anos",
            "7. Tech — App acompanhamento + scan 3D in-house + AI plano tratamento",
            "8. Compliance — ANVISA classe IIa + CFO + LGPD",
            "9. Equipa — Founder ex-McKinsey + co-founder ortodontista CD-USP + CTO ex-Loft",
            "10. Roadmap — M1 5 novas capitais (10 total) → M12 80K clientes ano + R$ 320M ARR",
            "11. Ask — R$ 35M Series A, dilui 18%, para escala 10→25 capitais + supply chain",
            "12. Por que agora — Crescimento classe C + experiencia compra digital pos-pandemia",
        ],
        tam_sam_som="TAM R$ 12B (ortodontia BR). SAM R$ 3.2B (classe media-alta com renda 8K+). SOM R$ 180M (40K clientes/ano x R$ 4.5K).",
        financial_ask="R$ 35M Series A (18% equity, R$ 175M pre-money). Uso: 40% expansao geo (15 clinicas), 30% supply chain + R&D, 20% growth, 10% reserva.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="MesaPOS — POS + gestao para restaurantes PT pequenos (1-3 unidades). 2 founders ex-Glovo + ex-Marktplaats. MVP em 80 restaurantes Lisboa. Pre-seed.",
        narrative_arc="80% dos 22K restaurantes PT usam ainda papel + Excel para gestao. POSs existentes (Lightspeed, Square) custam EUR 200+/mes e exigem hardware proprietario. MesaPOS e POS+gestao+stock+takeaway na cloud, EUR 49/mes, funciona em qualquer tablet. Founders sabem operar marketplace e ja conhecem 200 restaurantes Lisboa.",
        key_slides=[
            "1. Capa — MesaPOS: a gestao do teu restaurante em 1 tablet por 49 EUR/mes",
            "2. Problema — 18K restaurantes PT sem POS digital ou com sistemas caros (EUR 200+/mes)",
            "3. Solucao — POS cloud-only + stock + takeaway + relatorios em tablet generico",
            "4. Mercado — TAM EUR 280M (POS PT); SAM EUR 92M (pequenos/medios); SOM EUR 8M",
            "5. Tracao — 80 restaurantes Lisboa, MRR EUR 4K, churn 3.2%/mes, NPS 71",
            "6. Modelo — EUR 49/mes basico + EUR 29/mes addon takeaway + EUR 19/mes stock",
            "7. Tech — Cloud-first (Supabase + Next.js) + offline-resilient + integracao SAFT auto",
            "8. Compliance — Certificado AT (Autoridade Tributaria) Portaria 363/2010 obtido",
            "9. Equipa — Founder ex-Glovo ops + co-founder ex-Marktplaats CTO + Head Sales seasoned",
            "10. Roadmap — M1 200 restaurantes Lisboa+Porto → M12 1.500 nacional + EUR 70K MRR",
            "11. Ask — EUR 800K pre-seed para escala nacional + integracao delivery (Uber Eats/Glovo)",
            "12. Por que agora — Pos-pandemia adopcao digital + obrigatoriedade SAFT-PT 2026",
        ],
        tam_sam_som="TAM EUR 280M (POS PT total). SAM EUR 92M (22K restaurantes peq/medios x EUR 350/ano). SOM EUR 8M (1.500 restaurantes x EUR 5.5K/ano ano 2).",
        financial_ask="EUR 800K pre-seed (15% equity, EUR 4.5M cap SAFE). Uso: 40% growth (sales + ads), 30% tech (integracoes delivery + ML pricing), 20% ops (suporte 24/7), 10% legal+reserva.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="ModaCircular — marketplace 2nd-hand fashion PT. Modelo Vinted mas focado pecas premium (>EUR 100). 5K users beta. Founder ex-Farfetch. Pre-seed.",
        narrative_arc="O mercado de 2nd-hand premium em PT esta inexistente — Vinted nao tem premium, Vestiaire Collective nao tem PT pernas. ModaCircular e a Vestiaire Collective de Portugal: autenticacao no centro, comissao 15%, target pecas Gucci/Prada/Chanel. Founder construiu logistics Farfetch e tem rede curadora de 200+ vendedores high-end.",
        key_slides=[
            "1. Capa — ModaCircular: o marketplace premium 2nd-hand de Portugal",
            "2. Problema — EUR 380M em armarios premium PT parados, sem canal de revenda confiavel",
            "3. Solucao — Marketplace + autenticacao centralizada + entrega same-day em Lisboa/Porto",
            "4. Mercado — TAM EUR 1.2B (luxo 2nd-hand EU); SAM EUR 180M (PT); SOM EUR 12M",
            "5. Tracao — 5K beta users, 800 pecas listadas, GMV EUR 240K em 4 meses, NPS 67",
            "6. Modelo — Comissao 15% vendedor + EUR 19 servico autenticacao + entrega EUR 6",
            "7. Tech — App marketplace (React Native) + sistema autenticacao + logistica integrada CTT",
            "8. Compliance — RGPD + IVA 23% + DL 84/2008 (comercio electronico)",
            "9. Equipa — Founder ex-Farfetch logistics + co-founder gemologa GIA + Head Auth ex-LVMH",
            "10. Roadmap — M1 EUR 100K GMV/mes → M12 EUR 800K GMV/mes (40% take-rate fee)",
            "11. Ask — EUR 1.5M seed para autenticacao laboratorio + expansao Madrid/Barcelona",
            "12. Por que agora — Crise climatica + Gen Z compra usado + lei extensa garantia EU 2025",
        ],
        tam_sam_som="TAM EUR 1.2B (luxo 2nd-hand UE). SAM EUR 180M (PT mercado total). SOM EUR 12M (10K transactions/ano x EUR 1.2K AOV).",
        financial_ask="EUR 1.5M seed (16% equity). Uso: 35% growth + influencers, 30% tech + autenticacao lab, 20% ops 4 cidades, 15% reserva.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="EduDigital — plataforma cursos online B2C para profissionais 25-45 BR. Modelo Hotmart mas com curadoria + tutoria 1-1. Founder ex-Coursera BR. Serie A.",
        narrative_arc="Hotmart cresceu mas teve um problema brutal: 12% dos cursos sao excelentes, 88% sao lixo. Alunos perdem confianca. EduDigital faz o inverso: curadoria estrita (250 cursos vs 800K no Hotmart) + tutoria 1-1 + garantia recolocacao para programas de carreira. 47K alunos em 12 meses, R$ 28M ARR.",
        key_slides=[
            "1. Capa — EduDigital: cursos que mudam carreiras, com tutor humano no meio",
            "2. Problema — 88% dos cursos online BR sao genericos sem suporte, NPS medio Hotmart 38",
            "3. Solucao — Curadoria estrita (250 cursos) + tutoria 1-1 + garantia recolocacao",
            "4. Mercado — TAM R$ 32B (EdTech BR); SAM R$ 8B (profissional adulto); SOM R$ 480M",
            "5. Tracao — 47K alunos em 12M, R$ 28M ARR, NPS 76, recolocacao 68%",
            "6. Modelo — Cursos individuais R$ 197-1.997 + programas R$ 4-12K com tutor + corporate B2B",
            "7. Tech — Plataforma propria Next.js + LMS proprio + matching algorithm tutor-aluno",
            "8. Compliance — Lei 9.394/96 (LDB) + LGPD + certificacao MEC programas pos",
            "9. Equipa — Founder ex-Coursera BR + co-founder pedagoga USP + CTO ex-Cogna",
            "10. Roadmap — M1 80K alunos R$ 60M ARR → M12 200K alunos R$ 180M ARR + linha B2B 30% receita",
            "11. Ask — R$ 80M Series A, dilui 22%, para escala marketing + 200 novos cursos",
            "12. Por que agora — Reforma trabalhista 2026 + 8M reskilling brasileiros + ROI claro CV",
        ],
        tam_sam_som="TAM R$ 32B (EdTech BR). SAM R$ 8B (profissionais 25-45). SOM R$ 480M (250K alunos/ano x R$ 1.9K AOV).",
        financial_ask="R$ 80M Series A (22% equity, R$ 360M pre-money). Uso: 50% growth (paid + organic content), 25% novos cursos + tutores, 15% B2B sales team, 10% R&D.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="PetSitter Pro — marketplace dog walkers + pet sitters BR. Modelo Rover. 8K users, R$ 4.2M GMV, take 18%. Pre-seed.",
        narrative_arc="Os 65M lares com pets no BR perdem ferias e fins de semana para pet sitter informal via WhatsApp. Rover nao opera no BR, Petlove tem servico mas e marketplace fechado caro. PetSitter Pro e o Rover do BR: marketplace aberto, background check + seguro incluido, pricing 50% abaixo Petlove.",
        key_slides=[
            "1. Capa — PetSitter Pro: o cuidador do teu pet quando nao podes estar",
            "2. Problema — 65M lares pet BR sem servico confiavel de pet sitter, mercado 100% WhatsApp",
            "3. Solucao — Marketplace + background check + seguro acidente + pagamento escrow",
            "4. Mercado — TAM R$ 4.8B (pet care BR); SAM R$ 1.2B (urban midclass); SOM R$ 24M",
            "5. Tracao — 8K users, 2.4K active sitters, R$ 4.2M GMV em 18M, NPS 81",
            "6. Modelo — 18% comissao + R$ 19 servico seguro/booking + plano sitter pro R$ 49/mes",
            "7. Tech — App marketplace + matching algoritmo + sistema escrow + chat 24/7",
            "8. Compliance — Sitters como autonomos (MEI) + seguros Bradesco partnership + LGPD",
            "9. Equipa — Founder ex-99 + co-founder ex-iFood marketplace + Head Trust ex-Rappi",
            "10. Roadmap — M1 SP+RJ + 10K bookings/mes → M12 6 capitais + R$ 25M GMV anualizado",
            "11. Ask — R$ 6M seed para escala 2→6 capitais + supply side growth",
            "12. Por que agora — Boom turismo nacional pos-pandemia + crescimento pets per capita",
        ],
        tam_sam_som="TAM R$ 4.8B (pet care BR). SAM R$ 1.2B (urban midclass 18M pets). SOM R$ 24M (40K bookings/mes x R$ 80 ticket x 0.18 take).",
        financial_ask="R$ 6M seed (14% equity, R$ 42M cap SAFE). Uso: 40% growth (supply + demand ads), 25% tech (matching + payments), 20% ops 6 cidades, 15% trust+safety.",
    ).with_inputs("briefing"),
    dspy.Example(
        briefing="HRSignal — HR analytics SaaS UK enterprise. Series A. GBP 12M ARR, 47 enterprise clients. Founder ex-Workday + ex-Visier.",
        narrative_arc="Workday vendeu o stack 'all-in-one' mas HRDs querem o tool mais sharp para analytics — sem 18-month implementations. HRSignal e o Looker dos HR data: conecta-se ao Workday/SAP/BambooHR em 30 dias, embedded compliance UK/EU, board-ready dashboards. 47 clientes incluindo Aviva, Sky, Tesco. GBP 12M ARR pos-Series A, target Series B em 12 meses.",
        key_slides=[
            "1. Capa — HRSignal: HR analytics that gets to your board meeting on time",
            "2. Problema — HRDs spend 60% time on data plumbing, Workday analytics insufficient",
            "3. Solucao — Embedded BI layer + compliance engine UK/EU + 30-day deployment",
            "4. Mercado — TAM USD 8.4B (HR analytics global); SAM USD 1.8B (UK+EU enterprise); SOM USD 180M",
            "5. Tracao — 47 enterprise clients, GBP 12M ARR, NRR 132%, NPS 71",
            "6. Modelo — GBP 48-180K annual subscription tier por employee count",
            "7. Tech — Cloud-native (AWS) + embedded analytics (DuckDB) + AI compliance copilot",
            "8. Compliance — SOC 2 Type II + ISO 27001 + EU AI Act embedded + UK Employment Act 2024",
            "9. Equipa — Founder ex-Workday product + co-founder ex-Visier engineering + CFO ex-Personio",
            "10. Roadmap — M1 80 clients GBP 24M ARR → M12 200 clients GBP 75M ARR + DACH expansion",
            "11. Ask — USD 35M Series B for DACH expansion + AI copilot R&D + 25 hires",
            "12. Por que agora — UK Employment Act 2024 + EU AI Act 2026 force compliance buying cycle",
        ],
        tam_sam_som="TAM USD 8.4B (HR analytics global). SAM USD 1.8B (UK+EU enterprise 500+ employees). SOM USD 180M (1K accounts x USD 180K average ACV).",
        financial_ask="USD 35M Series B (18% equity, USD 195M pre-money). Uso: 45% sales+marketing DACH, 25% R&D (AI copilot), 20% post-sales+success, 10% G&A.",
    ).with_inputs("briefing"),
]


# Combine for trainset (10 each = 3 original + 7 new)
OFFER_TRAIN = OFFER_GOLDENS + OFFER_EXTRA
FUNNEL_TRAIN = FUNNEL_GOLDENS + FUNNEL_EXTRA
PITCH_TRAIN = PITCH_GOLDENS + PITCH_EXTRA


# ─────────────────────────────────────────────────────────────────────────────
# HELD-OUT TEST SET — 3 briefings per skill, NEW verticals not in trainset
# Used to measure real generalization, not in-distribution memorization.
# ─────────────────────────────────────────────────────────────────────────────

HELDOUT_OFFER = [
    "Estudio de yoga + meditacao Cascais. Target: profissionais 35-50 com burnout. 12 instrutores. Pricing 80 EUR/mes ilimitado. Concorre ginasios + apps meditacao.",
    "SaaS gestao de obras (construcao civil) BR. Target: construtoras 20-50 funcionarios. 700 EUR/mes. Concorre Sienge/Mobuss + planilha Excel.",
    "Marketplace freelancers tech Latam. Target: empresas EU contratam dev/designer LatAm. Comissao 12%. Concorre Toptal/Upwork.",
]

HELDOUT_FUNNEL = [
    "Estudio yoga Cascais 80 EUR/mes. Trafego: IG local + indicacoes membros. Quer subir membros activos de 120 para 250 em 6 meses.",
    "SaaS gestao obras BR 700 EUR/mes. Trafego: outbound construtoras + presenca feiras. CAC actual R$ 4.500, quer baixar para R$ 2.500.",
    "Marketplace freelance tech LatAm comissao 12%. Trafego: content marketing + LinkedIn. Quer chegar a 500 contratacoes/mes.",
]

HELDOUT_PITCH = [
    "ZenStudio — chain de estudios yoga premium BR. 8 unidades SP+RJ. Founder ex-SmartFit. Serie A pos-PMF, R$ 18M ARR.",
    "ObraDigital — SaaS gestao construcao civil BR. 240 construtoras clientes, R$ 12M ARR. Founder ex-Sienge. Pre-Serie B.",
    "TechBridge LatAm — marketplace freelancers tech para clientes EU+USA. 8K freelancers verificados. Founder ex-Toptal LatAm. Seed.",
]


# ─────────────────────────────────────────────────────────────────────────────
# JUDGE METRIC (same as v2 — proven correct, judge-on-output 5-dim 0-100)
# ─────────────────────────────────────────────────────────────────────────────

_JUDGE_CLIENT = None

JUDGE_PROMPT = """Avalia este output em 5 dimensoes (0-20 cada, total 0-100):

SKILL: {skill}
BRIEFING: {briefing}

OUTPUT:
{output}

RUBRIC:
1. Specificity (0-20) - dados concretos do briefing referenced?
2. Actionability (0-20) - proximos passos sem ambiguidade?
3. Completeness (0-20) - todos os campos preenchidos com substancia?
4. Accuracy (0-20) - factos verificaveis e correctos?
5. Tone (0-20) - formato adequado ao deliverable?

Responde APENAS JSON:
{{"specificity": N, "actionability": N, "completeness": N, "accuracy": N, "tone": N, "total": SUM, "reasoning": "1 frase"}}"""


def _get_judge_client():
    global _JUDGE_CLIENT
    if _JUDGE_CLIENT is None:
        _JUDGE_CLIENT = TrackedAnthropic(caller="dspy/compile_sprint4")
    return _JUDGE_CLIENT


def _render_output(pred) -> str:
    parts = []
    for attr in ("core_offer", "value_equation", "risk_reversal", "bonuses",
                 "urgency", "stages", "conversion_thresholds", "copy_hooks",
                 "automations", "narrative_arc", "key_slides", "tam_sam_som",
                 "financial_ask"):
        v = getattr(pred, attr, None)
        if v:
            if isinstance(v, list):
                v = "\n".join(str(x) for x in v)
            parts.append(f"{attr}:\n{v}")
    return "\n\n".join(parts)


def judge_score(skill: str, briefing: str, pred) -> int:
    """Returns judge score 0-100 (int)."""
    if pred is None:
        return 0
    output_text = _render_output(pred)
    if not output_text:
        return 0
    client = _get_judge_client()
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5", max_tokens=400,
            messages=[{"role": "user", "content": JUDGE_PROMPT.format(
                skill=skill, briefing=briefing[:1000], output=output_text[:3500],
            )}],
        )
        raw = resp.content[0].text.strip()
        m = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
        if not m:
            return 50
        sd = json.loads(m.group(0))
        total = sd.get("total") or sum(sd.get(d, 0) for d in
            ("specificity", "actionability", "completeness", "accuracy", "tone"))
        return int(total)
    except Exception as e:
        print(f"  [judge_score error: {e}]")
        return 50


def make_judge_metric(skill_name: str):
    def judge_metric(example, pred, trace=None) -> float:
        score = judge_score(skill_name, getattr(example, "briefing", ""), pred)
        return min(max(score / 100.0, 0.0), 1.0)
    return judge_metric


# ─────────────────────────────────────────────────────────────────────────────
# COMPILE + HELDOUT EVAL with VARIANCE BOUNDS
# ─────────────────────────────────────────────────────────────────────────────

SKILLS = [
    ("dario-offer",  OfferGenerationProgram, OFFER_TRAIN,  HELDOUT_OFFER),
    ("dario-funnel", FunnelDesignProgram,    FUNNEL_TRAIN, HELDOUT_FUNNEL),
    ("dario-pitch",  PitchDeckProgram,       PITCH_TRAIN,  HELDOUT_PITCH),
]


def compile_with_miprov2(skill_name: str, ProgramCls, trainset):
    print(f"\n=== Compiling {skill_name} (sprint4: MIPROv2 + {len(trainset)} goldens) ===")
    metric = make_judge_metric(skill_name)

    # MIPROv2: optimize instructions + select demos
    teleprompter = MIPROv2(
        metric=metric,
        auto="light",  # light/medium/heavy — light is fastest, ~$1-2/skill
        num_threads=1,
        verbose=False,
    )

    base = ProgramCls()
    compiled = teleprompter.compile(
        base,
        trainset=trainset,
        requires_permission_to_run=False,
    )

    # Save artifact
    out_path = ORCH_DIR / "optimization" / "compiled" / f"{skill_name}_sprint4.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    compiled.save(str(out_path))
    print(f"  saved: {out_path.relative_to(ORCH_DIR)}")
    return compiled


def evaluate_heldout(skill_name: str, compiled, heldout_briefings: list[str], n_passes: int = 3):
    """Evaluate compiled program on held-out briefings with multiple passes per
    briefing → bound the variance.

    Returns dict with:
      - scores_per_briefing: dict[briefing_idx → list[scores]]
      - mean_per_briefing: dict[briefing_idx → mean]
      - overall_mean: float
      - overall_std: float (std across all individual scores)
      - n_evals_total: int
    """
    print(f"  evaluating on {len(heldout_briefings)} held-out briefings, {n_passes} passes each...")
    all_scores: list[int] = []
    scores_per_briefing: dict[int, list[int]] = {}

    for i, brief in enumerate(heldout_briefings):
        scores_per_briefing[i] = []
        for pass_idx in range(n_passes):
            try:
                pred = compiled(briefing=brief)
                s = judge_score(skill_name, brief, pred)
                scores_per_briefing[i].append(s)
                all_scores.append(s)
                print(f"    briefing[{i}] pass[{pass_idx+1}]: {s}/100")
            except Exception as e:
                print(f"    briefing[{i}] pass[{pass_idx+1}]: FAILED ({e})")
                scores_per_briefing[i].append(0)
                all_scores.append(0)

    mean_per_briefing = {i: round(sum(v)/len(v), 1) for i, v in scores_per_briefing.items() if v}
    overall_mean = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0.0
    overall_std = round(statistics.stdev(all_scores), 2) if len(all_scores) > 1 else 0.0

    print(f"  held-out mean: {overall_mean}/100  (std={overall_std}, n={len(all_scores)})")
    return {
        "scores_per_briefing": scores_per_briefing,
        "mean_per_briefing": mean_per_briefing,
        "overall_mean": overall_mean,
        "overall_std": overall_std,
        "n_evals_total": len(all_scores),
    }


def main():
    lm = dspy.LM("anthropic/claude-haiku-4-5", max_tokens=2000, temperature=0.2)
    dspy.configure(lm=lm)

    results = {}
    for skill_name, ProgramCls, trainset, heldout in SKILLS:
        compiled = compile_with_miprov2(skill_name, ProgramCls, trainset)
        eval_data = evaluate_heldout(skill_name, compiled, heldout, n_passes=3)
        results[skill_name] = eval_data

    # ─────────────────────────────────────────────────────────────────────────
    # Update metrics — DEDICATED NAMESPACE, do NOT touch avg_quality_score.
    # ─────────────────────────────────────────────────────────────────────────
    metrics_path = ORCH_DIR / "quality" / "skill-metrics.yaml"
    metrics = load_y(metrics_path)
    print("\n=== Updating skill-metrics.yaml (sprint4 namespace) ===")
    for skill_name, data in results.items():
        if skill_name not in metrics["skills"]:
            print(f"  ! {skill_name} not in metrics; skipping")
            continue
        meta = metrics["skills"][skill_name]
        meta["heldout_scores_sprint4"] = {
            f"briefing_{i}": v for i, v in data["scores_per_briefing"].items()
        }
        meta["avg_judge_heldout_sprint4"] = data["overall_mean"]
        meta["heldout_std_sprint4"] = data["overall_std"]
        meta["heldout_n_evals_sprint4"] = data["n_evals_total"]
        meta["compile_artifact_sprint4"] = f"optimization/compiled/{skill_name}_sprint4.json"
        meta["last_heldout_eval_at"] = datetime.now(UTC).isoformat()
        meta.setdefault("score_history", []).append({
            "date": datetime.now(UTC).isoformat()[:10],
            "heldout_mean": data["overall_mean"],
            "heldout_std": data["overall_std"],
            "n_evals": data["n_evals_total"],
            "briefing_quality": "sprint4-miprov2-heldout-multipass",
            "note": "held-out cross-vertical eval; production avg_quality_score untouched",
        })
        v2_score = meta.get("avg_judge_synthetic_goldens", "n/a")
        print(f"  {skill_name}: heldout_mean={data['overall_mean']} ± {data['overall_std']}  "
              f"(vs v2 synthetic-goldens score: {v2_score})")

    metrics["last_updated"] = datetime.now(UTC).isoformat()
    dump_y(metrics, metrics_path)
    print("\nOK skill-metrics.yaml updated (sprint4 namespace)")

    # Summary table
    print("\n=== SPRINT4 SUMMARY ===")
    print(f"{'skill':<18} {'heldout_mean':<14} {'std':<8} {'n':<6} {'vs v2_synthetic'}")
    for skill_name in [s[0] for s in SKILLS]:
        sd = metrics["skills"].get(skill_name, {})
        h = sd.get("avg_judge_heldout_sprint4", "n/a")
        std = sd.get("heldout_std_sprint4", "n/a")
        n = sd.get("heldout_n_evals_sprint4", "n/a")
        v2 = sd.get("avg_judge_synthetic_goldens", "n/a")
        delta = f"{h - v2:+.1f}" if isinstance(h, (int, float)) and isinstance(v2, (int, float)) else "n/a"
        print(f"  {skill_name:<18} {h:<14} {std:<8} {n:<6} v2={v2} ({delta})")


if __name__ == "__main__":
    main()
