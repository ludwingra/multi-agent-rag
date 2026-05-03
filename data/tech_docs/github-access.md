# GitHub Enterprise Access Guide — TechNova Solutions

**Owner:** Engineering Platform Team | **Last Updated:** 2025-10-01 | **Applies To:** Engineering, DevOps, and Technical Ops

---

## Overview

TechNova Solutions hosts its source code on **GitHub Enterprise Server (GHES) 3.12** at [github.technova.io](https://github.technova.io). The platform is only accessible when connected to the TechNova VPN. All engineers receive a GitHub account provisioned by the Engineering Platform team as part of onboarding.

---

## Prerequisites

- Active TechNova VPN connection (see [VPN Setup Guide](vpn-setup-guide.md))
- Okta account with `engineering` or `devops` group membership
- SSH key or HTTPS token configured (instructions below)

---

## Requesting Access

1. Submit a Jira ticket in the **IT** project using the **GitHub Access Request** template at [jira.technova.io](https://jira.technova.io).
2. Specify the **organization** (e.g., `technova-engineering`, `technova-platform`) and required permission level (`read`, `write`, `admin`).
3. Your manager must approve the ticket; approval triggers automated provisioning via Okta SCIM within **4 business hours**.

---

## SSH Key Setup

All code interactions should use SSH. Follow [Password Policy](password-policy.md) for SSH key generation requirements (minimum Ed25519).

```bash
# Generate key (if not already done per password-policy.md)
ssh-keygen -t ed25519 -C "firstname.lastname@technova.io" -f ~/.ssh/technova_github

# Copy the public key
cat ~/.ssh/technova_github.pub

# Configure SSH to use it for GitHub Enterprise
cat >> ~/.ssh/config << 'EOF'
Host github.technova.io
  HostName github.technova.io
  User git
  IdentityFile ~/.ssh/technova_github
  IdentitiesOnly yes
EOF

# Test the connection (VPN required)
ssh -T git@github.technova.io
# Expected: Hi firstname.lastname! You've successfully authenticated...
```

Add the public key at [github.technova.io/settings/keys](https://github.technova.io/settings/keys).

---

## Cloning Repositories

```bash
# Use SSH URL format
git clone git@github.technova.io:technova-engineering/flowengine-core.git

# Verify remote
git remote -v
```

---

## Repository and Branch Conventions

| Branch | Purpose | Push restriction |
|--------|---------|-----------------|
| `main` | Production-ready code | **Protected** — PR + 2 approvals required |
| `develop` | Integration branch | PR + 1 approval required |
| `feat/<ticket>-description` | Feature work | Open push for author |
| `fix/<ticket>-description` | Bug fixes | Open push for author |
| `hotfix/<ticket>-description` | Critical production fixes | PR + 2 approvals, expedited |

For code review requirements, see [Code Review Guidelines](code-review-guidelines.md).

---

## Personal Access Tokens (PATs)

PATs are used for CI scripts and API integrations. Create PATs at [github.technova.io/settings/tokens](https://github.technova.io/settings/tokens).

- Scope to **minimum required permissions** (e.g., `repo:read` for read-only).
- Expiry: **30 days** for personal, **90 days** for CI tokens.
- Store in 1Password or AWS Secrets Manager — **never** commit to a repository.

---

## GitHub Actions and CI/CD

GitHub Actions pipelines are defined in `.github/workflows/`. The standard pipeline includes lint, test, Docker build, and ECR push stages. Refer to [CI/CD Pipeline](ci-cd-pipeline.md) for the full pipeline architecture.

```yaml
# Example workflow trigger
on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [main]
```

---

## Security and Compliance

- All commits to `main` require **signed commits** (`git commit -S`). Configure GPG signing:
  ```bash
  git config --global commit.gpgsign true
  git config --global user.signingkey <GPG_KEY_ID>
  ```
- Dependency scanning (Dependabot) is enabled on all repositories.
- Secret scanning is active; commits containing detected secrets are blocked by the GitHub push protection feature.

---

## FAQ

**Q: I get "Permission denied (publickey)" when cloning.**
A: Verify you are connected to the VPN and your SSH key is added at [github.technova.io/settings/keys](https://github.technova.io/settings/keys). Run `ssh -vT git@github.technova.io` for debug output.

**Q: My PR is blocked — it says 2 approvals are required.**
A: `main` branch protection is configured to require 2 non-author approvals. Request reviews from two team members or seek an expedited review in `#engineering` Slack.

---

## Related Documents

- [VPN Setup Guide](vpn-setup-guide.md)
- [Code Review Guidelines](code-review-guidelines.md)
- [CI/CD Pipeline](ci-cd-pipeline.md)
- [Password Policy](password-policy.md)
