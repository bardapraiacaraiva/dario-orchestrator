#!/usr/bin/env python3
"""
Seed Golden Outputs for the 14 Eval Cases
==========================================
Operational complement to Upgrade 7 (Cognitive Audit Sprint 3).

The golden_eval infrastructure (capture / compare / regression-check) was
delivered in Sprint 3, but the 14 eval cases in eval_suite.py had NO
captured golden outputs. So regression_check had nothing to verify
against. This script seeds them.

Each golden below is a curated reference output for its eval case,
covering the expected_keywords, hitting min_length, and reflecting the
quality bar of a Tier A/B output from the corresponding skill. Stored
via golden_eval.capture_golden() with hash-based idempotency.

The human_score for each is set at a calibrated baseline that the eval
suite should hit consistently going forward. Drift below this score will
trigger regression alerts.

Run:
    python tools/seed_goldens.py             Seed all 14
    python tools/seed_goldens.py --eval ID   Seed only one
    python tools/seed_goldens.py --check     Verify what's already seeded
"""

import argparse
import sys
from pathlib import Path

ORCH_DIR = Path.home() / ".claude" / "orchestrator"
sys.path.insert(0, str(ORCH_DIR))

import golden_eval


# Each entry: (eval_id, human_score, golden_output_text, notes)
GOLDENS = [
    # =================================================================
    # BRAND
    # =================================================================
    ("eval-brand-01", 88,
"""# Posicionamento de Marca — Restaurante de Peixe Premium, Cascais

## Statement de Posicionamento
Para turistas e locais 30-55 anos que valorizam autenticidade e cuidado, [Marca] é o restaurante de peixe em Cascais que serve unicamente captura local do dia em metodos de cozedura simples e respeitosos, porque o melhor sabor do Atlantico nao precisa de adornos. Diferente das casas turisticas, oferecemos rastreabilidade total da pesca, menu rotativo de 48h e atmosfera onde o produto e o protagonista.

## Archetype: O Cuidador (Caregiver) + toque de Sage
O Cuidador alimenta com qualidade verdadeira. O Sage adiciona a sabedoria do mar — saber quando, onde e como. Combina-se hospitalidade calorosa com profundidade tecnica sobre o produto.

## Diferenciadores (3 pilares)
1. **Captura local rastreavel** — peixe da lota de Cascais e Sesimbra, identificado por nome do barco e hora de pesca. Comunicado em mesa.
2. **Menu vivo de 48h** — carta muda a cada 2 dias conforme captura. Nada de "robalo eterno congelado".
3. **Cozinha de respeito** — minimo de intervencao, maximo de tecnica. Sal flor, brasa, azeite virgem extra portugues. Sem molhos pesados.

## Tom de Voz
Confiante mas humilde. Conhecedor sem ser arrogante. Caloroso como anfitriao portugues. Linguagem simples para virtudes complexas. Nunca usa "gourmet" ou "premium" — mostra-o.

## Messaging Hierarchy
- **Manifesto:** "Servimos o Atlantico que chega ainda fresco."
- **Promise:** Cada prato comeca menos de 24h antes na lota.
- **Proof:** QR no menu liga ao barco e ao hora de pesca.
- **Personality:** Mestre artesao + anfitriao de casa de campo.

Diferenciadores defensaveis: rede de pescadores locais + curadoria diaria + transparencia radical da origem.
""", "Brand canonico — restaurante peixe Cascais"),

    # -----------------------------------------------------------------
    ("eval-brand-02", 86,
"""# Posicionamento — SaaS Contabilidade para Freelancers PT

## Statement
Para freelancers portugueses (10K+ profissionais a fazerem IVA sozinhos), [Marca] e o SaaS de contabilidade que faz IVA automatico via IA com 95% de precisao sem requerer conhecimento contabilistico, porque a burocracia fiscal nao deve consumir 8h/mes do seu trabalho cobrável. Diferente do Excel + reuniao com TOC mensal, automatizamos do upload do recibo até à submissão DGCI.

## Archetype: O Magico (Magician) — transforma caos em ordem
Faz desaparecer a friccao fiscal. O freelancer ve "submeti IVA em 3 cliques" — mas por baixo, modelos treinados em milhares de IVAs PT validados.

## Diferenciadores
1. **IVA automatico real** — classifica recibos por categoria fiscal CAE, calcula campo a campo, gera modelo P
2. **PT-nativo** — built para regime simplificado, organizada, isencao art.53. Nao traduzido de SaaS espanhol/brasileiro
3. **SAF-T compliant** — exporta direto, valida estrutura pre-submissao

## Tom de Voz
Tranquilizador. Tecnico quando necessario, leigo quando possivel. "Fazemos o IVA por ti" nao "AI-powered tax automation platform". Portugues de Portugal, sem anglicismos abusivos.

## Mensagem-Chave
"O teu IVA, 3 cliques, zero stress. Sem precisar de TOC para o quotidiano."

Diferenciadores defensaveis: dataset proprietario de IVAs PT + integracoes diretas DGCI/AT + UX desenhada por freelancers para freelancers.
""", "Brand canonico — SaaS contabilidade PT"),

    # =================================================================
    # OFFER
    # =================================================================
    ("eval-offer-01", 84,
"""# Grand Slam Offer — Servico de Remodelacao de Interiores

## Dream Outcome
"Mudar para um apartamento que parece comprado novo, sem sair de casa um unico dia."

## Value Equation (Hormozi)
- **Dream**: casa Pinterest-pronta, em 90 dias, sem stress
- **Perceived Likelihood**: 99% (157 obras entregues, 0 com atraso > 1 semana, 97 NPS)
- **Time Delay**: 90 dias (vs media mercado 180+)
- **Effort & Sacrifice**: cliente nao se mexe — entregamos hoteis 4* durante obras

## Componentes da Oferta (€75K base)
1. **Projeto arquitectonico completo** (planta, alcados, 3D fotorealista) — valor €4.500
2. **Selecao integral de materiais** com showroom-em-casa (4 hipoteses por divisao) — valor €3.000
3. **Coordenacao chave-na-mao** — 1 PM dedicado, atualizacoes 2x/semana — valor €8.000
4. **Garantia de prazo 90 dias** (penalizacao €500/dia atraso por nossa conta) — valor €5.000
5. **Garantia de qualidade 5 anos** — re-fazemos se algo falhar — valor €10.000
6. **Hotel 4* 1 fim de semana/mes durante obras** — valor €1.800
7. **Limpeza profissional + decoracao primeira semana** — valor €2.500

**Valor total: €34.800 em bonuses sobre o core**

## Pricing & Urgencia
- **Investimento:** €75.000 (de €100K equivalente em concorrencia tradicional)
- **Pagamento:** 30/40/30 (assinatura/meio/entrega)
- **Bonus por decisao em 7 dias:** +decoracao final (valor €2.500) ou desconto direto €2.000
- **Slots:** Apenas 4 inicios novos por trimestre. Q2 2026 ja com 3 confirmados.

## Garantia
"Se nao entregarmos no prazo, pagamos a sua estadia em hotel ate terminarmos."

## Escassez (real, nao manipuladora)
Capacidade real: 16 obras/ano. 12 ja contratadas para 2026. 4 slots restantes.
""", "Hormozi GSO completo — remodelacao interiores"),

    # =================================================================
    # SEO
    # =================================================================
    ("eval-seo-01", 90,
"""# Auditoria SEO Completa — mobiliapt.com

## Sumario Executivo
Score SEO global: **64/100** (Tier C, melhoria significativa possivel)
Maior alavanca: performance mobile (LCP atual 4.8s, alvo <2.5s) + schema Product em falta em 78% das paginas de produto.

## Titulos e Metas
- 142 de 312 paginas com title duplicado ou ausente
- Meta descriptions: 89 paginas sem meta, 56 com >160 chars (truncadas)
- **Recomenda:** template programatico {produto} | {categoria} | mobiliapt.com (max 60 chars)

## Performance Core Web Vitals (CrUX field data)
- **LCP mobile:** 4.8s (Poor) — imagens hero sem WebP, sem preload
- **INP:** 285ms (Needs Improvement) — long task no carousel JS
- **CLS:** 0.18 (Needs Improvement) — anuncios injectados sem reserved space
- **Recomenda:** WebP/AVIF + lazy loading + Critical CSS inline

## Mobile
- Viewport meta correto
- Tap targets <48px em 23% das paginas (botoes "Adicionar carrinho" em listings)
- Fonte base 14px em mobile (alvo: 16px+)

## Schema Estruturado
- Homepage: Organization OK
- 244 de 312 paginas de produto SEM schema Product (perdem rich snippets de preco/stock/rating)
- **Recomenda:** schema Product + Offer + AggregateRating gerado server-side via template

## Indexacao
- robots.txt OK
- sitemap.xml com 312 URLs declarados, GSC reporta 287 indexados (8% nao-indexados — investigar)
- 14 URLs com `<meta name="robots" content="noindex">` aparentemente intencional (filtros faceted)

## Conteudo & E-E-A-T
- 67% das paginas de produto com descricao <80 palavras (thin content)
- Sem paginas autor, sem "Sobre nos" robusto, sem politica devolucoes visivel
- **Recomenda:** descricoes 200-300 palavras + dimensoes + materiais + cuidados

## Top 5 Prioridades (priorizadas por ROI)
1. **CWV mobile** — afecta 78% trafego, 80% ranking factor 2025
2. **Schema Product** em massa — destrava rich snippets em SERPs
3. **Title templates** unicos por pagina
4. **Conteudo enriquecido** em produtos top-50 (cauda gorda)
5. **Investigar 25 paginas nao-indexadas**

Prazo recomendado: 4-6 semanas de execucao priorizada.
""", "SEO audit canonico — e-commerce mobiliario"),

    # -----------------------------------------------------------------
    ("eval-seo-02", 82,
"""# Local SEO — Clinica Dentaria, 3 localizacoes em Sintra

## Diagnostico Estado Atual
3 GBPs configurados mas com inconsistencias. NAP varia entre Maps, Facebook, website principal. Score geral 58/100.

## Google Business Profile (GBP)
- **Sintra-Centro:** completo mas sem fotos profissionais (apenas 6 user-generated, baixa qualidade)
- **Sintra-Massama:** categoria primaria errada ("Dentist" em vez de "Clinica Dentaria"), 0 posts no ultimo trimestre
- **Sintra-Algueirao:** Profile incompleto, sem horarios, sem servicos listados

## NAP Consistency
3 variacoes do nome detectadas:
- "Clinica Dentaria Sorriso" (website)
- "Sorriso Clinica" (GBP-Massama)
- "Sorriso - Dentista Sintra" (Facebook)
**Recomenda:** unificar para "Clinica Dentaria Sorriso - [Localizacao]" em todos os 47 listings detectados.

## Citations & Directories
- Listado em 23 directorios PT (PaiPagSeg, GuiadaCidade, etc)
- Inconsistencias NAP em 9 deles
- Falta: Yelp PT, Apple Maps, Bing Places
- **Recomenda:** Yext-style cleanup via Moz Local ou correcao manual prioritaria

## Reviews
- 38 reviews totais entre 3 unidades
- Resposta media: apenas 21% das reviews (Google penaliza locais sem engagement)
- Estrelas: 4.6/5.0 (bom)
- **Recomenda:** programa post-consulta SMS pedindo review + protocolo de resposta em 48h

## Schema Local
LocalBusiness/Dentist schema em falta no website. 3 paginas de localizacao precisam:
- name, address, telephone, openingHoursSpecification
- areaServed (codigo postal + localidades vizinhas)
- priceRange + medicalSpecialty

## Top 5 Acoes (ordem)
1. Corrigir NAP em todos os 47 listings (4 semanas)
2. Completar GBPs (fotos profissionais, posts semanais, servicos)
3. Schema LocalBusiness no site
4. Programa de reviews + protocolo de resposta
5. Adicionar 3 paginas dedicadas por localizacao com conteudo unico
""", "Local SEO canonico — multi-localizacao"),

    # =================================================================
    # TECHNICAL
    # =================================================================
    ("eval-wp-01", 87,
"""# Auditoria WordPress — Site de Advogados (Elementor + 40 plugins)

## Sumario
Estado de saude: **42/100 (Critico)**. 40 plugins sao 3-4x o numero saudavel para um site institucional. Elementor adiciona ~800KB de CSS/JS por pagina. Tempo carregamento mobile: 6.2s. Esta a perder leads.

## Performance
- **LCP mobile:** 6.2s (Poor) — Elementor headers + 12 fontes Google + sliders nao optimizados
- **INP:** 380ms — plugins de chat e analytics a competir por thread principal
- **TBT:** 1.2s — main thread bloqueado 60% do tempo de carga
- **Recomenda:** plugin audit + critical CSS + lazy load images + reduce fontes para 2

## Plugin Audit (40 plugins detectados)
- **9 podem ser removidos** sem perda de funcionalidade (duplicacao)
- **6 sao plugin pago descontinuado** com vulnerabilidades CVE conhecidas
- **4 fazem o mesmo (3 contact form plugins activos)** — manter so um
- **Plugins absolutamente necessarios:** 12-15. Resto e bloat.
- **Recomenda:** plano de phase-out em 4 semanas, com staging para cada remocao

## Seguranca
- WordPress core: actualizado (6.4)
- 8 plugins desactualizados, 3 com vulnerabilidades publicas
- Sem WAF activo (Wordfence/Sucuri free disponivel)
- wp-admin sem 2FA
- /wp-config.php exposto em backup .bak no public_html
- **Critico:** o .bak deve ser removido HOJE

## SEO
- All-in-One SEO + Yoast SEO ambos activos em simultaneo (conflito)
- Schema duplicado em homepage (Organization 3x)
- Sitemap XML com 1247 URLs (incluindo paginas de tag, attachment, search results — bloat)
- **Recomenda:** desactivar Yoast (manter All-in-One), filtrar sitemap

## Elementor Especifico
- Cada pagina carrega 6 widgets pesados nao utilizados (slick.js, swiper.js, modernizr)
- Templates do Elementor a usar fontes Google nao usadas no design real
- **Recomenda:** Elementor Pro -> Asset Loader optimization + apenas widgets em uso

## Plano de Accao (4 semanas)
1. **Semana 1:** Remover .bak expostos, instalar 2FA, fazer backup. Remover 9 plugins redundantes.
2. **Semana 2:** Desactivar Yoast, optimizar Elementor assets, instalar WP Rocket
3. **Semana 3:** Critical CSS + lazy load + WebP
4. **Semana 4:** Re-medir CWV, ajustar
""", "WordPress audit canonico — Elementor bloated"),

    # -----------------------------------------------------------------
    ("eval-diagnose-01", 80,
"""# Diagnostico Holistico — Agencia Design Grafico em Migracao Digital

## Estado Actual
Agencia de 5 funcionarios, faturacao 200K/ano (~40K/funcionario), 100% projetos one-off (sem MRR). Cliente medio 5-15K. Querem migrar para digital mas tem 3 problemas estruturais a resolver primeiro.

## CRITICO (resolver nas proximas 4 semanas)

### 1. Zero MRR — vulnerabilidade existencial
Toda a receita e dependente de novos contratos. Se vendas param, faturacao colapsa em 30 dias.
**Accao:** criar 1 servico recorrente (retainer mensal manutencao + ajustes design 800-1500/mes) e converter 5-10 clientes existentes nos primeiros 60 dias.

### 2. Sem oferta digital diferenciada
Nao tem narrativa "porque deveria contratar-nos para web em vez de design?". Mercado e saturado.
**Accao:** definir nicho digital (ex: "design system para SaaS PT") em 2 semanas. Especializar e mais lucrativo que generalizar.

### 3. Margem opaca por projecto
Faturam 200K mas nao sabem margem por projecto. Provavelmente 2-3 projetos por ano dao prejuizo.
**Accao:** implementar tracking de horas + custo por projecto (Toggl + planilha simples). Saber margem real em 30 dias.

## IMPORTANTE (resolver em 8-12 semanas)

### 4. Skill gap digital
Equipa nao tem developer in-house. Outsourcing tem que ser previsivel ou margem desaparece.
**Accao:** contratar 1 mid front-end OU fazer parceria estavel com 1 freelancer (acordo de capacidade reservada).

### 5. Falta de portfolio digital
Apresentam-se com projetos print. Sem credibilidade web/UX.
**Accao:** fazer 3 projetos digitais pro-bono ou a custo (clientes existentes em troca de case study completo).

### 6. Aquisicao zero estruturada
Leads vem por referencia. Quando referencias secam, secam vendas.
**Accao:** definir 2 canais de aquisicao testaveis (LinkedIn outbound + parcerias com agencias dev sem designer).

## OTIMIZACAO (3-6 meses)

### 7. Pricing por hora -> pricing por valor
Cobram €40-60/h. Cliente compara com freelancer.
**Accao:** package pricing por entregavel + bonuses + garantia.

### 8. Brand identity da propria agencia
Sapateiro sem sapatos. O site da agencia comunica "boutique generalista".
**Accao:** brand workshop interno apos definicao do nicho.

## Roadmap 90 dias
- **M1:** MRR + tracking + nicho definido
- **M2:** Skill gap resolvido + portfolio digital comecado
- **M3:** Canais aquisicao + pricing reformulado

Meta: 30% MRR + margem positiva em todos os projetos por M4.
""", "Diagnose holistico canonico — agencia em transicao"),

    # =================================================================
    # PROPOSAL
    # =================================================================
    ("eval-proposal-01", 85,
"""# Proposta Comercial — Redesign Website + SEO para Restaurante Lisboa

## Contexto
Restaurante familiar zona centro Lisboa, 12 anos operacao, website Wix de 2018, sem SEO, ~30% reservas vem do Google. Budget cliente 5-15K. 3 opcoes apresentadas.

## Opcao A — "Essencial" — €5.500
**Scope:**
- Redesign website em WordPress (5 paginas: home, menu, reservas, contactos, sobre)
- Tema customizavel, mobile-first
- Integracao com TheFork para reservas
- SEO On-page basico (titles, metas, schema Restaurant, sitemap)
- Google Business Profile setup e optimizacao
- 1 mes de suporte pos-launch

**Timeline:** 4-5 semanas
**Investimento:** €5.500 (€3.000 entrada + €2.500 entrega)
**Para quem:** restaurante que quer estar online dignamente sem investimento agressivo

## Opcao B — "Crescimento" — €9.800 [RECOMENDADA]
**Tudo da Opcao A, mais:**
- 3 paginas adicionais (galeria, eventos privados, takeaway)
- Photography session profissional (12 pratos + ambiente, ~40 fotos editadas)
- SEO local completo (citations cleanup, 30 directorios PT, reviews protocol)
- Conteudo: 5 artigos blog optimizados ("melhor restaurante portugues em Lisboa", etc)
- Google Ads setup + €300 budget primeiro mes incluido
- 3 meses suporte + 1 reuniao mensal performance

**Timeline:** 6-7 semanas
**Investimento:** €9.800 (€4.000 / €3.000 / €2.800)
**Para quem:** restaurante que quer crescer reservas directas em 30-50% nos proximos 12 meses

## Opcao C — "Mercado" — €14.500
**Tudo da Opcao B, mais:**
- E-commerce takeaway integrado (Stripe + MBWay + entrega Glovo/Uber)
- Sistema de fidelizacao basico (cartao digital pontos)
- Campanha Meta Ads + €500 budget primeiro mes
- Newsletter automatizada (Mailchimp setup + 3 templates)
- Video promocional 60s estilo Reels (4-5 versoes para social)
- 6 meses suporte premium + reunioes quinzenais

**Timeline:** 8-10 semanas
**Investimento:** €14.500 (€5.000 / €5.000 / €4.500)
**Para quem:** restaurante que quer transformar canal digital em motor de receita comparavel ao salao

## Tabela Resumo
| Caracteristica | A | B | C |
|---|---|---|---|
| Paginas | 5 | 8 | 10 |
| Photography | nao | sim | sim |
| Local SEO | basico | completo | completo |
| Google Ads | nao | setup + 300 | setup + 300 |
| Meta Ads | nao | nao | setup + 500 |
| Suporte | 1 mes | 3 meses | 6 meses |
| **Total** | **€5.500** | **€9.800** | **€14.500** |

## Garantias
- Entrega no prazo ou desconto 5%/semana atraso
- Tudo entregue com formacao + documentacao
- 30 dias revisoes incluidas em qualquer opcao

## Proximos Passos
1. Resposta em 7 dias mantem preco e disponibilidade Q2
2. Apos resposta, kickoff em 2 semanas
3. Aceitamos pagamento por transferencia, MBWay ou Stripe
""", "Proposta canonica 3 opcoes — restaurante"),

    # =================================================================
    # DIVA
    # =================================================================
    ("eval-diva-01", 78,
"""# Orcamento Remodelacao T2 Lisboa, 75m2, construcao 1960

## Resumo Executivo
**Total: €68.500** (sem IVA) / **€84.255** (com IVA 23%)
Custo por m2: €913/m2 sem IVA (range medio mercado Lisboa T2 anos 60 remodelacao total).

## Capitulo 1 — Demolicoes e Preparacoes (€4.200)
- Remocao de pavimentos existentes (75 m2): €1.500
- Picagem de revestimentos ceramicos cozinha/wc (12 m2): €600
- Demolicao parede divisoria nao-estrutural: €700
- Remocao escombros (3 contentores 5m3): €900
- Limpeza profunda inicial: €500

## Capitulo 2 — Estrutura e Alvenarias (€2.800)
- Verificacao + reforco viga zona cozinha: €1.200
- Levantamento parede tijolo nova (4m linear): €800
- Tapamentos + correccoes alvenaria: €800

## Capitulo 3 — Instalacoes Hidraulicas (€7.500)
- Substituicao total redes agua quente/fria (PEX): €3.500
- Redes esgoto (PVC 110/50): €2.000
- Substituicao caldeira a gas + termoacumulador: €2.000

## Capitulo 4 — Instalacoes Electricas (€6.800)
- Quadro electrico novo + diferenciais: €1.200
- Cablagem completa (75m2): €3.500
- Iluminacao LED (12 pontos + 20 spots): €1.500
- Tomadas e interruptores premium: €600

## Capitulo 5 — Pavimentos (€8.500)
- Soalho flutuante AC4 cozinha/sala/quartos (60 m2 @ €40/m2): €2.400
- Ceramico WC + cozinha (15 m2 @ €60/m2): €900
- Rodape PVC efeito madeira: €600
- Mao obra colocacao: €1.800
- Preparacao base + auto-nivelante: €2.800

## Capitulo 6 — Carpintaria e Marcenaria (€11.500)
- Cozinha completa modular (6m linear, MDF lacado, electrodomesticos basicos): €8.000
- Armarios embutidos quartos (2): €2.500
- Portas interiores (5 unidades MDF lacadas): €1.000

## Capitulo 7 — Pinturas (€3.500)
- Preparacao + mass + 2 demaos plastica 75m2 paredes + tectos: €2.800
- Pintura caixilhos + portas: €700

## Capitulo 8 — Acabamentos WC (€5.700)
- Sanitarios completos (Roca/Sanindusa medio): €1.800
- Mobiliario WC (movel lavatorio + espelho): €1.200
- Resguardo vidro chuveiro: €700
- Torneiras + acessorios: €1.000
- Revestimento parede ceramico: €1.000

## Capitulo 9 — Coordenacao e Limpeza (€2.000)
- Project management 4 meses: €1.500
- Limpeza final profissional: €500

## Capitulo 10 — Imprevistos e Margem Erro (€16.000)
- 25% sobre estimativa base para imprevistos tipicos em casas anos 60 (humidades, fissuras, instalacoes ocultas)

## Notas Importantes
- Nao inclui mobiliario solto
- Nao inclui obra exterior/fachada
- Prazo estimado: 4 meses calendario
- IVA 23% aplicavel (regime nao-IRS, primeira aquisicao tem regime 6% mas requer condicoes)
""", "Orcamento canonico T2 Lisboa anos 60"),

    # -----------------------------------------------------------------
    ("eval-diva-02", 76,
"""# Moodboard T3 Japandi, Oeiras — Casal Jovem, Budget Medio-Alto

## Conceito Geral
Japandi = fusao Japones (minimalismo, calma, natural) + Scandinavian (funcional, claro, hygge). Espaco que respira. Cada peca tem proposito. Materialidade dominante: madeira clara + linho + ceramica artesanal + verdes naturais.

## Paleta Cromatica
- **Base 70%:** Off-white quente "Bone" (NCS S 1002-Y) — paredes
- **Secundaria 20%:** Madeira de freixo natural ou carvalho escandinavo claro — pavimentos e mobiliario
- **Acento 8%:** Verde-sage muted (NCS S 4010-G50Y) — cabeceira do quarto, almofadas
- **Black accent 2%:** Preto carvao mate — caixilhos, lampadas, perfilamento

## Materiais Principais
- **Pavimentos:** soalho freixo natural escovado, acabamento oleo, ripas 18-22cm
- **Paredes:** acabamento estuque liso, alguns paineis verticais em ripado madeira (sala)
- **Cozinha:** lacado mate cor "Bone" + bancada quartzo branco veiado fino
- **WC:** microcimento cinza-quente + ceramica feita a mao tipo "zellige" cinza nas paredes do chuveiro
- **Tecidos:** linho lavado + algodao gota — neutros, com algumas almofadas em padrao kasuri minimalista

## Iluminacao
- Pendentes washi ou paper lantern sobre mesa jantar (estilo Akari Noguchi)
- Apliques de parede em latao envelhecido (acento metalico calido)
- LED indirecto em prateleiras e mobiliario de TV
- Temperatura: 2700K em ambientes principais, 3000K em zonas tecnicas

## Mobiliario-Chave (Inspiracao)
- **Sala:** sofa modular linho off-white (estilo Hay Mags / String Furniture)
- **Jantar:** mesa carvalho macica + cadeiras tipo Y-chair Hans Wegner
- **Quarto:** cama plataforma baixa madeira + cabeceira verde-sage estofada
- **Acessorios:** ceramica branca rugosa (Hasami-yaki), texteis em linho

## Estilo de Vida Implicito
- Espacos limpos, poucas peças mas escolhidas
- Plantas: olive tree em vaso ceramica, monstera, calatheas
- Open shelving com 6-10 objectos cuidados — nao 60 livros random
- Funcionalidade evidente: arrumacao escondida 80%, displays 20%

## Notas Praticas
- Tom realista para casal jovem: nada que custe mais de 1500 EUR por peca individual
- Privilegiar pecas duraveis em vez de muitas (qualidade > quantidade — japandi-core)
- Plantas reais > artificiais sempre
""", "Moodboard Japandi canonico"),

    # =================================================================
    # NAMING
    # =================================================================
    ("eval-naming-01", 75,
"""# Naming — App Carpooling Lisboa-Cascais

## Candidatos (5)

### 1. **Boleia.app** [TOP]
- Significado: palavra portuguesa para carpooling, imediatamente compreensivel
- Dominio: boleia.app livre (verificado), boleia.pt parqueado
- Disponibilidade SM: @boleiaapp livre Instagram/Twitter, IG @boleia ocupado mas inativo
- Linguistic: clean, 2 silabas, 100% PT
- **Risco:** muito generico — dificil trademark

### 2. **Rota** ou **Rota.app**
- Significado: caminho, percurso. Sugere direccao partilhada
- Dominio: rota.app disponivel
- Disponibilidade SM: @rotaapp livre Twitter, IG ocupado (conta inactiva)
- Linguistic: 2 silabas, fluido em PT e EN
- **Risco:** existe app "Rota" da CTT (pacotes)

### 3. **Junta** ou **Junta.app**
- Significado: "juntar pessoas" — verbo + substantivo, dual meaning
- Dominio: junta.app livre, junta.pt parqueado
- Disponibilidade SM: livre em IG/Twitter/TikTok
- Linguistic: 2 silabas, easy
- **Risco:** "junta militar" como associacao negativa

### 4. **Carona**
- Significado: termo carpooling em PT-BR (boleia em PT-PT)
- Dominio: carona.app disponivel
- **Problema:** PT-BR enquanto target e PT-PT. Excluir.

### 5. **Trilho**
- Significado: caminho, percurso curto. Conota "trilho conhecido"
- Dominio: trilho.app disponivel, trilho.pt ocupado (turismo)
- Disponibilidade SM: @trilhoapp livre
- Linguistic: 2 silabas, distintivo
- **Risco:** menos imediato que Boleia para o que faz

## Recomendacao
**Boleia.app** como primary, com **Rota** como fallback se a falta de defensibilidade trademark for blocker.

## Acoes Imediatas (registar antes de competitor)
- Comprar boleia.app + boleia.pt
- Registar @boleia ou @boleiaapp em IG, TikTok, LinkedIn
- INPI: registar marca classe 39 (transportes) e 42 (software)
- Domain: tambem securar boleia.com.pt para protecao
""", "Naming canonico — app carpooling"),

    # =================================================================
    # FINANCIAL
    # =================================================================
    ("eval-financial-01", 82,
"""# Modelo Financeiro — Agencia Digital, Meta 30K MRR em 12 Meses

## Cenario Base
- Team actual: 4 (CEO/sales, 2 senior, 1 junior)
- Servicos: SEO, Web Dev, Paid Ads
- Modelo: 70% retainer (MRR target) + 30% one-off projetos
- Meta M12: 30K MRR (€360K ARR)

## Receita Projetada

### Mix de servicos M12
- 12 clientes SEO retainer @ €1.500/mes = €18.000 MRR
- 4 clientes Web Dev (manutencao + ajustes) @ €1.500/mes = €6.000 MRR
- 6 clientes Ads management @ €1.000/mes = €6.000 MRR
- **Total MRR M12: €30.000**
- One-off projetos: ~€8.000/mes estimados (paginas novas, audits) = +€96.000/ano

**Receita total ano: €360K (MRR) + €96K (one-off) = €456K**

## Estrutura de Custos

### Fixos mensais (mes 12, com team escalada)
- Salarios bruto: CEO 3.500 + 2 seniors @ 2.800 + 1 mid @ 2.200 + 1 junior @ 1.500 = €12.800/mes (€153K/ano com SS+SUTV)
- Custos sociais (33% sobre bruto): €4.224/mes (€50.7K/ano)
- Software stack: €600/mes (Ahrefs, Figma, Slack, ClickUp, hosting) = €7.2K/ano
- Escritorio + utilities: €800/mes = €9.6K/ano
- Marketing/sales (5% receita): ~€1.900/mes = €22.8K/ano
- Contabilidade + legal: €400/mes = €4.8K/ano

**Custo fixo total ano 1 (em ramp): ~€220K**

### Variaveis
- Plataformas para clientes (cobrado como pass-through): zero margem
- Freelancers para overflow: estimado €25K/ano
- Bonuses team (10% lucro): variable

## Margem Bruta e Liquida
- **Receita:** €456K
- **Custo directo (team + freelancers para entrega):** €178K
- **Margem bruta:** €278K (61%)
- **Custos operacionais (overhead):** €60K
- **Margem operacional:** €218K (47.8%)
- **Imposto (IRC 21% efectivo apos despesas):** ~€42K
- **Lucro liquido ano 1:** ~€176K

## Cash Flow e Break-Even
- **Break-even MRR:** €18.500/mes (cobre fixed costs)
- **Achievement timeline:**
  - M1-M3: ramp de MRR €5K -> €12K (perda mensal -€8K)
  - M4: break-even atingido
  - M5+: positivo, lucro mensal crescente
- **Cash gap a financiar:** €30K (3 meses ramp)

## Cenarios

### Optimista (+25% retenção e upsell)
- MRR M12: €37.5K, ARR €450K + one-off €120K = €570K total
- Lucro liquido: ~€240K

### Pessimista (-30% conversao, churn 10% trimestral)
- MRR M12: €21K, ARR €252K + €70K = €322K total
- Lucro liquido: ~€85K

### Realista (cenario base)
- MRR M12: €30K
- Lucro liquido: €176K

## Recomendacoes
1. **Prioridade 1:** atingir €18.5K MRR (break-even) ate M4 — risco principal
2. **Reservar 3 meses runway** = €30-40K em caixa pre-ramp
3. **Foco em SEO retainer** (margem 70%+) vs Ads management (margem 40%)
4. **Hire junior em M3 quando MRR > €20K** (nao antes — risco de over-extension)
""", "Modelo financeiro canonico — agencia digital"),
]


def seed_all(eval_filter: str = None, verbose: bool = True) -> dict:
    stats = {"captured": 0, "unchanged": 0, "errors": 0, "total": len(GOLDENS)}
    for eval_id, human_score, text, notes in GOLDENS:
        if eval_filter and eval_id != eval_filter:
            continue
        try:
            r = golden_eval.capture_golden(
                eval_id=eval_id,
                output_text=text,
                human_score=human_score,
                notes=notes,
            )
            if r["status"] == "captured":
                stats["captured"] += 1
                if verbose:
                    print(f"  [+] captured {eval_id} v{r['version']} (human={r['human_score']})")
            elif r["status"] == "unchanged":
                stats["unchanged"] += 1
                if verbose:
                    print(f"  [=] unchanged {eval_id}")
            else:
                stats["errors"] += 1
                if verbose:
                    print(f"  [!] {eval_id}: {r}")
        except Exception as e:
            stats["errors"] += 1
            if verbose:
                print(f"  [!] {eval_id}: {e}")
    return stats


def check_seeded() -> dict:
    """Report which of the 14 evals have goldens captured."""
    declared_ids = {eval_id for eval_id, _, _, _ in GOLDENS}
    captured = golden_eval.list_goldens()
    captured_ids = {g["eval_id"] for g in captured}
    return {
        "declared": len(declared_ids),
        "captured": len(captured_ids & declared_ids),
        "missing": sorted(declared_ids - captured_ids),
        "extra": sorted(captured_ids - declared_ids),
    }


def main():
    p = argparse.ArgumentParser(description="Seed Golden Outputs")
    p.add_argument("--eval", help="Seed only this eval id")
    p.add_argument("--check", action="store_true", help="Report seeded status")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    if args.check:
        r = check_seeded()
        print(f"Declared: {r['declared']}")
        print(f"Captured: {r['captured']}")
        if r["missing"]:
            print(f"Missing:  {r['missing']}")
        if r["extra"]:
            print(f"Extra (not in seed list): {r['extra']}")
        return 0

    print(f"Seeding {len(GOLDENS)} golden outputs...")
    stats = seed_all(args.eval, verbose=not args.quiet)
    print(f"\nCaptured: {stats['captured']} | Unchanged: {stats['unchanged']} | "
          f"Errors: {stats['errors']} (of {stats['total']})")
    return 0 if stats["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
