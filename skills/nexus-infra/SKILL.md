---
name: nexus-infra
description: "Infrastructure as Code — Terraform, Docker, Kubernetes, cloud architecture, provisioning"
version: "1.0"
---

# NEXUS-INFRA: Infrastructure as Code Skill

## When to Activate

**Trigger words (PT):** infraestrutura, terraform, docker, kubernetes, k8s, cloud, provisionar, iac, containers, orquestrador, deploy, servidor, vpc, instancia
**Trigger words (EN):** infrastructure, terraform, docker, kubernetes, k8s, cloud architecture, iac, containers, orchestration, deploy, server, vpc, instance, provisioning, helm, compose

## Step-by-Step Workflow

### Phase 1: Architecture Design
1. Gather requirements: compute, storage, network, security, compliance
2. Select cloud provider(s): AWS, Azure, GCP, or multi-cloud
3. Design network topology: VPC, subnets (public/private), availability zones
4. Define compute strategy: VMs, containers (ECS/EKS/AKS/GKE), serverless
5. Plan storage: block, object, file, database tiers
6. Document architecture diagram and decision records (ADRs)

### Phase 2: Terraform Setup
1. Initialize project structure:
   - `environments/` (dev, staging, prod)
   - `modules/` (reusable components)
   - `variables.tf`, `outputs.tf`, `providers.tf`, `backend.tf`
2. Configure remote state backend (S3+DynamoDB, Azure Blob, GCS)
3. Set up workspace or directory-based environment separation
4. Implement variable validation and type constraints
5. Use `terraform plan` before every `terraform apply`
6. Pin provider versions and module versions

### Phase 3: Docker Configuration
1. Write Dockerfiles following best practices:
   - Multi-stage builds for smaller images
   - Non-root user, specific base image tags (no `latest`)
   - `.dockerignore` for build context control
   - Health checks defined
2. Docker Compose for local development and simple deployments
3. Image scanning for vulnerabilities (Trivy, Snyk)
4. Registry management (ECR, ACR, GCR, Docker Hub)
5. Tag strategy: git SHA + semantic version

### Phase 4: Kubernetes Configuration
1. Namespace strategy: per environment or per team
2. Resource definitions: Deployments, Services, Ingress, ConfigMaps, Secrets
3. Resource requests and limits for all containers
4. Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA)
5. Network policies for pod-to-pod communication control
6. Helm charts for templated, versioned deployments
7. GitOps with ArgoCD or Flux

### Phase 5: Security Hardening
1. Least privilege IAM roles for infrastructure
2. Encrypt data at rest and in transit
3. Private subnets for databases and internal services
4. Security groups / NSGs with minimal open ports
5. Secrets management: Vault, AWS Secrets Manager, Azure Key Vault
6. Container image signing and admission control

### Phase 6: Operations
1. Infrastructure drift detection (scheduled `terraform plan`)
2. Cost tagging strategy (project, environment, owner, cost-center)
3. Automated cleanup of unused resources
4. Blue-green or canary deployment strategies
5. Infrastructure documentation auto-generated from code

## Commands Table

| Command | Description |
|---------|-------------|
| `nexus infra design` | Architecture design template and questionnaire |
| `nexus infra terraform` | Terraform project scaffold |
| `nexus infra docker` | Dockerfile best practices review |
| `nexus infra k8s` | Kubernetes manifest generator |
| `nexus infra security` | Infrastructure security checklist |
| `nexus infra cost` | Cost estimation for architecture |
| `nexus infra migrate` | Cloud migration planning template |
| `nexus infra audit` | Infrastructure audit (drift, security, cost) |

## Output Template

```markdown
# Infrastructure Assessment — [Project/Organization]
**Date:** YYYY-MM-DD | **Cloud:** [AWS/Azure/GCP] | **Environment:** [dev/staging/prod]

## 1. Architecture Summary
- Compute: [type, count, sizing]
- Storage: [types, capacity]
- Network: [topology summary]
- Containers: [orchestrator, cluster details]

## 2. IaC Status
| Component | Tool | State Backend | Version Pinned | Drift |
|-----------|------|--------------|----------------|-------|

## 3. Security Posture
| Check | Status | Finding |
|-------|--------|---------|
| IAM least privilege | | |
| Encryption at rest | | |
| Encryption in transit | | |
| Private subnets | | |
| Secrets management | | |
| Image scanning | | |

## 4. Cost Summary
| Resource | Monthly Est. | Optimization |
|----------|-------------|-------------|

## 5. Recommendations
| # | Issue | Impact | Action | Priority |
|---|-------|--------|--------|----------|

## 6. Next Review: YYYY-MM-DD
```

## Red Flags

- No IaC (infrastructure managed manually via console)
- Terraform state stored locally (not remote/locked)
- Docker images using `latest` tag in production
- Containers running as root
- No resource limits on Kubernetes pods
- Secrets hardcoded in code or environment variables without encryption
- Public subnets for databases or internal services
- No multi-AZ or single region deployment for production
- Infrastructure drift undetected for months
- No cost tagging or cost monitoring
- IAM roles with admin/wildcard permissions
- No disaster recovery or cross-region replication
