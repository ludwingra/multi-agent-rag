# CI/CD Pipeline — TechNova Solutions

**Owner:** DevOps / Platform Engineering | **Last Updated:** 2025-10-08 | **Applies To:** All Engineering Teams

---

## Overview

TechNova Solutions uses **GitHub Actions** as its CI/CD orchestration engine, with **Docker** for containerization, **Amazon ECR** for container registry, and **ArgoCD** (GitOps) for Kubernetes deployment. The pipeline covers the FlowEngine platform and all supporting microservices running on **EKS** in `us-east-1`.

For repository access and branch conventions, refer to [GitHub Access](github-access.md).

---

## Pipeline Architecture

```
Developer Push / PR
        │
        ▼
GitHub Actions (CI)
  ├── Lint (ESLint / Ruff)
  ├── Unit Tests (pytest / Jest)
  ├── Integration Tests
  ├── Security Scan (detect-secrets, npm audit, safety)
  ├── Docker Build
  └── Push to ECR (on merge to develop/main)
        │
        ▼
ArgoCD (CD — GitOps)
  ├── Sync to staging (auto, on develop merge)
  └── Sync to production (manual approval gate)
```

---

## GitHub Actions Workflows

Workflows live in `.github/workflows/` within each repository.

### Standard Workflow File

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  lint-and-test:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Lint (Ruff)
        run: ruff check .

      - name: Run tests
        run: pytest --cov=src --cov-report=xml -v

      - name: Upload coverage
        uses: codecov/codecov-action@v4

  docker-build-push:
    needs: lint-and-test
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::XXXXXXXXXXXX:role/GitHubActionsECRPush
          aws-region: us-east-1

      - name: Login to ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/flowengine-api:$IMAGE_TAG .
          docker push $ECR_REGISTRY/flowengine-api:$IMAGE_TAG
```

---

## ArgoCD GitOps Deployment

ArgoCD is hosted at [argocd.technova.io](https://argocd.technova.io). Access requires VPN and Okta SSO.

### Staging Auto-Deploy

When a commit merges to `develop`, the CI pipeline pushes an image to ECR and updates the image tag in the `k8s-manifests` repository. ArgoCD automatically syncs the staging environment within **2 minutes**.

```bash
# Check ArgoCD sync status from CLI
argocd app get flowengine-api-staging --auth-token $ARGOCD_TOKEN

# Manual sync if needed
argocd app sync flowengine-api-staging
```

### Production Promotion

Production deploys require:
1. Manual approval in the GitHub Actions workflow (via environment protection rule).
2. Approver must be an IC4+ or Engineering Manager.
3. Deploy during the **deployment window**: Tuesday–Thursday, 10:00–16:00 US Eastern.

```bash
# Promote to production (update image tag in manifests repo)
./scripts/promote.sh --service flowengine-api --env production --tag $GITHUB_SHA
```

---

## Rollback Procedure

```bash
# Rollback ArgoCD to previous revision
argocd app rollback flowengine-api-production

# Or rollback Kubernetes deployment directly
kubectl rollout undo deployment/flowengine-api -n production

# Verify rollback
kubectl rollout status deployment/flowengine-api -n production
```

For SEV1 rollback procedures, see [Incident Response](incident-response.md).

---

## Environment Variables and Secrets

- **Runtime secrets**: Stored in AWS Secrets Manager and injected by the External Secrets Operator into Kubernetes Secrets.
- **CI/CD secrets**: Stored in GitHub Secrets (org-level for shared, repo-level for specific).
- **Feature flags**: Managed via LaunchDarkly; no code changes required.

Never hardcode secrets in Dockerfiles, workflow YAML, or Helm charts. See [Security Best Practices](security-best-practices.md).

---

## Monitoring Post-Deploy

After every production deploy, monitor:
- **Datadog APM**: [app.datadoghq.com/apm/services](https://app.datadoghq.com/apm/services) — watch p99 latency for `flowengine-api`.
- **Sentry**: [sentry.technova.io](https://sentry.technova.io) — watch error rate for 15 minutes post-deploy.
- **PagerDuty**: If error rate exceeds 1% in 5 minutes, PagerDuty auto-fires SEV2.

See [Monitoring & Alerting](monitoring-alerting.md) for alert thresholds.

---

## Related Documents

- [GitHub Access](github-access.md)
- [Monitoring & Alerting](monitoring-alerting.md)
- [Incident Response](incident-response.md)
- [Security Best Practices](security-best-practices.md)
- [AWS Access Request](aws-access-request.md)
