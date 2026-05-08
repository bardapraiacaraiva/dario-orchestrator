---
name: builder-launch-checklist
description: >
  Checklist pre-launch completa: SEO, analytics, monitoring, backups, legal, performance,
  security, social, email. Nada esquecido no dia do lancamento.
  Use quando: launch, lancamento, pre-launch checklist, ir para producao, go-live.
tools: Read, Write, Edit, Bash, Glob, Grep
version: 1.0
---

# BUILDER — Launch Checklist

## Pre-Launch (1 semana antes)

### Technical
- [ ] All pages load without errors (200 status)
- [ ] Forms submit correctly (test each one)
- [ ] Auth flow works (register → verify → login → dashboard)
- [ ] Payment flow works (if applicable — test with Stripe test mode)
- [ ] Mobile responsive (test on real devices: iPhone, Android)
- [ ] Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms
- [ ] Error boundaries catch crashes gracefully
- [ ] 404 page exists and is helpful

### SEO
- [ ] Title tags unique per page (< 60 chars)
- [ ] Meta descriptions per page (< 160 chars)
- [ ] OG image + title + description (test with opengraph.xyz)
- [ ] Sitemap.xml generated and submitted to GSC
- [ ] Robots.txt correct (not blocking important pages)
- [ ] Schema markup (Organization + FAQ minimum)
- [ ] Canonical URLs set

### Analytics & Monitoring
- [ ] GA4 installed and receiving data
- [ ] Key events tracked (signup, CTA click, form submit)
- [ ] Conversion funnels configured
- [ ] Uptime monitoring active (UptimeRobot / Better Stack)
- [ ] Error tracking active (Sentry or equivalent)

### Security
- [ ] HTTPS enforced (no mixed content)
- [ ] Security headers (X-Frame-Options, CSP, HSTS)
- [ ] Rate limiting on auth endpoints
- [ ] CORS configured (whitelist only)
- [ ] Environment variables NOT in client bundle
- [ ] SQL injection tested (if applicable)

### Legal
- [ ] Privacy Policy page (RGPD compliant)
- [ ] Terms of Service page
- [ ] Cookie consent banner (if tracking)
- [ ] Data processing agreement (if B2B)

### Content
- [ ] All placeholder text replaced with real copy
- [ ] Images optimized (WebP, lazy loaded)
- [ ] Favicon set (all sizes: 16, 32, 180, 512)
- [ ] Social media profiles linked
- [ ] Contact information correct

### Backup & Recovery
- [ ] Database backup automated (daily minimum)
- [ ] Backup restore tested at least once
- [ ] Rollback procedure documented

## Launch Day
- [ ] Deploy to production
- [ ] Verify all pages live
- [ ] Test critical flows one more time
- [ ] Monitor error logs (first 2 hours)
- [ ] Announce (social media, email, Product Hunt if applicable)

## Post-Launch (first week)
- [ ] Monitor analytics daily
- [ ] Check error rates
- [ ] Collect user feedback (first 5 users)
- [ ] Fix critical bugs within 24h
- [ ] Plan V1.1 based on real usage data
