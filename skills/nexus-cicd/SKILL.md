---
name: nexus-cicd
description: "CI/CD — GitHub Actions, deployment strategies, rollback procedures, pipeline optimization"
version: "1.0"
---

# NEXUS-CICD: CI/CD Pipeline Skill

## When to Activate

**Trigger words (PT):** cicd, pipeline, deploy, github actions, integracao continua, entrega continua, rollback, release, automacao de deploy, blue green, canary
**Trigger words (EN):** ci/cd, pipeline, deploy, github actions, continuous integration, continuous delivery, rollback, release, deployment automation, blue green, canary, gitops, build

## Step-by-Step Workflow

### Phase 1: CI Pipeline Design
1. Define trigger events: push, pull request, tag, schedule, manual
2. Build stage:
   - Dependency installation (cached for speed)
   - Compilation / transpilation
   - Asset generation (if applicable)
3. Quality gates:
   - Linting (ESLint, Clippy, Pylint)
   - Type checking (TypeScript, mypy)
   - Unit tests (with coverage threshold)
   - Integration tests
   - Security scanning (SAST: Semgrep, CodeQL, Snyk)
4. Artifact generation: Docker image, binary, package
5. Target total CI time: <10 minutes for fast feedback

### Phase 2: CD Pipeline Design
1. Environment promotion: dev -> staging -> production
2. Deployment strategies:
   - **Rolling**: gradual replacement (default for K8s)
   - **Blue-Green**: two identical environments, switch traffic
   - **Canary**: route small % of traffic to new version
   - **Feature flags**: deploy code, activate separately
3. Deployment approval gates:
   - Auto-deploy to dev/staging on merge
   - Manual approval for production (or auto with conditions)
4. Smoke tests post-deploy: health checks, critical path tests
5. Monitoring integration: watch error rates after deploy

### Phase 3: GitHub Actions Implementation
1. Workflow file structure:
   - `.github/workflows/ci.yml` — triggered on PR
   - `.github/workflows/cd.yml` — triggered on merge to main
   - `.github/workflows/release.yml` — triggered on tag
2. Best practices:
   - Pin action versions to SHA (not `@latest`)
   - Cache dependencies (actions/cache)
   - Use matrix builds for multi-version testing
   - Secrets via GitHub Secrets (never hardcoded)
   - Reusable workflows for shared logic
3. Self-hosted runners for private networks or special requirements
4. Concurrency groups to prevent parallel deployments

### Phase 4: Rollback Procedures
1. Automated rollback triggers: error rate spike, health check failure
2. Rollback methods:
   - **Redeploy previous version**: safest, rebuild from known-good tag
   - **Revert commit**: git revert + trigger pipeline
   - **K8s rollback**: `kubectl rollout undo`
   - **Feature flag disable**: instant, no deploy needed
3. Database rollback: migration rollback scripts, point-in-time restore
4. Rollback testing: practice during normal releases
5. Post-rollback: incident report, root cause analysis

### Phase 5: Pipeline Optimization
1. Parallelization: run independent jobs concurrently
2. Caching: dependencies, Docker layers, build artifacts
3. Incremental builds: only build/test changed components (monorepo)
4. Test splitting: distribute tests across parallel runners
5. Fast-fail: abort pipeline on first critical failure
6. Metrics: build time, test time, deploy frequency, failure rate

### Phase 6: Release Management
1. Versioning strategy: SemVer (major.minor.patch)
2. Changelog generation: conventional commits + auto-changelog
3. Release notes: automated from PR descriptions and commit messages
4. Tag-based releases with GitHub Releases
5. Artifact registry: container registry, package registry, S3
6. DORA metrics: deployment frequency, lead time, MTTR, change failure rate

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus cicd design` | CI/CD pipeline architecture template |
| `nexus cicd github` | GitHub Actions workflow generator |
| `nexus cicd rollback` | Rollback procedure documentation |
| `nexus cicd optimize` | Pipeline performance optimization |
| `nexus cicd security` | Pipeline security hardening |
| `nexus cicd dora` | DORA metrics calculation |
| `nexus cicd strategy` | Deployment strategy comparison |
| `nexus cicd audit` | Pipeline audit and best practices review |

## Output Template

```markdown
# CI/CD Assessment — [Project/Organization]
**Date:** YYYY-MM-DD | **Platform:** [GitHub Actions/etc.] | **Environments:** X

## 1. Pipeline Overview
| Stage | Tool | Duration | Status |
|-------|------|----------|--------|
| Build | | | |
| Test | | | |
| Security scan | | | |
| Deploy staging | | | |
| Deploy production | | | |

## 2. Quality Gates
| Gate | Enforced | Threshold | Current |
|------|----------|-----------|---------|
| Linting | | | |
| Type check | | | |
| Unit tests | | X% coverage | |
| Security scan | | 0 critical | |

## 3. Deployment Strategy
| Environment | Strategy | Approval | Rollback Method |
|------------|----------|----------|----------------|

## 4. DORA Metrics
| Metric | Current | Target | Industry Benchmark |
|--------|---------|--------|--------------------|
| Deploy frequency | | | Elite: multiple/day |
| Lead time | | | Elite: <1 hour |
| MTTR | | | Elite: <1 hour |
| Change failure rate | | | Elite: <5% |

## 5. Recommendations
| # | Issue | Impact | Action | Priority |
|---|-------|--------|--------|----------|

## 6. Next Review: YYYY-MM-DD
```

## Red Flags

- No CI pipeline (manual builds)
- No automated tests in pipeline
- Direct deploy to production without staging
- No rollback procedure documented or tested
- Secrets hardcoded in pipeline files
- Pipeline takes >30 minutes (slow feedback)
- No security scanning in pipeline (SAST/DAST)
- No approval gate for production deployments
- Actions pinned to `@latest` or `@main` (supply chain risk)
- No monitoring after deployment (blind deploys)
- Manual deployment steps remaining in pipeline
- No DORA metrics tracked


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **nexus-cicd** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in nexus-cicd:**

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
