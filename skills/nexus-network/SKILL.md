---
name: nexus-network
description: "Network engineering — VPC, subnets, firewall rules, DNS, CDN, VPN, SSL/TLS, load balancing"
version: "1.0"
---

# NEXUS-NETWORK: Network Engineering Skill

## When to Activate

**Trigger words (PT):** rede, vpc, subnets, firewall, dns, cdn, vpn, ssl, tls, load balancer, balanceador de carga, proxy reverso, latencia, routing, segmentacao de rede
**Trigger words (EN):** network, vpc, subnets, firewall, dns, cdn, vpn, ssl, tls, load balancer, reverse proxy, latency, routing, network segmentation, peering, nat gateway, security groups

## Step-by-Step Workflow

### Phase 1: Network Architecture
1. VPC/VNet design:
   - CIDR block planning (avoid overlap for peering)
   - Multi-AZ deployment for high availability
   - Public subnets: load balancers, NAT gateways, bastion hosts only
   - Private subnets: application servers, databases, internal services
2. Subnet strategy: /24 per AZ per tier (public, private-app, private-db)
3. Routing tables: public routes via IGW, private via NAT GW
4. VPC peering or Transit Gateway for multi-VPC communication
5. DNS strategy: Route 53 / Azure DNS / Cloud DNS + internal DNS zones

### Phase 2: Firewall & Security Groups
1. Default deny: all traffic blocked unless explicitly allowed
2. Security groups (stateful) per service tier:
   - Public LB: 80/443 from 0.0.0.0/0
   - App tier: from LB only on app port
   - DB tier: from app tier only on DB port
   - Management: SSH/RDP from bastion only
3. Network ACLs (stateless): additional subnet-level control
4. WAF rules: OWASP Core Rule Set, rate limiting, geo-blocking
5. Egress control: restrict outbound to necessary destinations
6. Review and audit rules quarterly (remove unused)

### Phase 3: DNS Management
1. Domain registration and renewal calendar
2. Public DNS records: A, AAAA, CNAME, MX, TXT (SPF, DKIM, DMARC)
3. TTL strategy: 300s for dynamic, 86400s for static records
4. DNS failover: health-check-based routing
5. Private DNS zones for internal service discovery
6. DNSSEC where supported

### Phase 4: CDN & Load Balancing
1. CDN configuration: CloudFront, Azure CDN, Cloudflare
   - Cache static assets (CSS, JS, images, fonts)
   - Cache headers and invalidation strategy
   - Custom error pages
   - Geographic distribution for global users
2. Load balancer configuration:
   - Application LB: HTTP/HTTPS, path-based routing, host-based routing
   - Network LB: TCP/UDP, high throughput, static IP
   - Health checks: interval, threshold, path
3. SSL/TLS termination at LB or CDN level
4. HTTP/2 and HTTP/3 (QUIC) enablement

### Phase 5: SSL/TLS & VPN
1. SSL/TLS certificates:
   - ACM (AWS) / Let's Encrypt for automated certificate management
   - TLS 1.2 minimum (TLS 1.3 preferred)
   - Strong cipher suites, disable weak ciphers
   - Certificate monitoring and auto-renewal
2. VPN for remote access:
   - Site-to-site: AWS VPN, Azure VPN Gateway, WireGuard
   - Client VPN: AWS Client VPN, Tailscale, WireGuard
   - Zero Trust alternative: BeyondCorp, Cloudflare Access, Zscaler
3. Private connectivity: Direct Connect, ExpressRoute, Cloud Interconnect

### Phase 6: Monitoring & Optimization
1. Network monitoring: flow logs, traffic analytics, packet captures
2. Latency monitoring: synthetic checks, real-user monitoring
3. Bandwidth utilization and capacity planning
4. Cost optimization: data transfer, NAT gateway costs, VPN costs
5. Network performance baselines and SLOs
6. DDoS protection: AWS Shield, Azure DDoS, Cloudflare

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus network design` | Network architecture template |
| `nexus network firewall` | Firewall rules audit and design |
| `nexus network dns` | DNS configuration review |
| `nexus network cdn` | CDN setup and optimization |
| `nexus network ssl` | SSL/TLS configuration audit |
| `nexus network vpn` | VPN architecture and setup |
| `nexus network audit` | Full network security audit |
| `nexus network perf` | Network performance assessment |

## Output Template

```markdown
# Network Assessment — [Organization]
**Date:** YYYY-MM-DD | **Cloud:** [AWS/Azure/GCP] | **Regions:** X

## 1. Network Topology
| VPC/VNet | CIDR | AZs | Subnets | Peering |
|----------|------|-----|---------|---------|

## 2. Firewall Rules Audit
| Rule | Source | Dest | Port | Risk | Recommendation |
|------|--------|------|------|------|---------------|

## 3. DNS Status
| Domain | Registrar | Expiry | DNSSEC | SPF | DKIM | DMARC |
|--------|-----------|--------|--------|-----|------|-------|

## 4. SSL/TLS Status
| Domain | Provider | Expiry | TLS Version | Grade |
|--------|----------|--------|-------------|-------|

## 5. CDN & LB Configuration
| Service | CDN | Cache Hit Rate | LB Type | Health Check |
|---------|-----|---------------|---------|-------------|

## 6. Recommendations
| # | Finding | Risk | Action | Priority |
|---|---------|------|--------|----------|

## 7. Next Review: YYYY-MM-DD
```

## Red Flags

- Databases in public subnets with direct internet access
- Security groups with 0.0.0.0/0 on non-standard ports
- No WAF protecting internet-facing applications
- SSL certificates expired or expiring within 30 days
- TLS 1.0/1.1 still enabled
- DNS domains expiring without renewal
- No DMARC, SPF, or DKIM configured (email spoofing risk)
- Single AZ deployment for production
- No network segmentation between environments
- VPN using weak encryption or pre-shared keys
- No flow logs or network monitoring enabled
- CDN not configured for static assets (unnecessary origin load)


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nexus-network** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nexus-network:**

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
