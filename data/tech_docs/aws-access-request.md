# AWS Access Request Guide — TechNova Solutions

**Owner:** DevOps / Cloud Platform Team | **Last Updated:** 2025-10-10 | **Applies To:** Engineering, DevOps, Data Engineering

---

## Overview

TechNova Solutions operates its infrastructure primarily on **AWS us-east-1** (primary) and **eu-west-1** (disaster recovery). All AWS access is governed by **IAM roles and policies** following the principle of least privilege. Individual long-lived IAM users with static credentials are deprecated; all human access uses **AWS SSO via Okta**.

Before requesting AWS access, ensure you have completed the [VPN Setup Guide](vpn-setup-guide.md) — AWS console access requires VPN when outside the office network.

---

## AWS Accounts Structure

| Account | ID (last 4) | Environment | Used By |
|---------|-------------|-------------|---------|
| `technova-prod` | `...1234` | Production | SRE, DevOps, on-call engineers |
| `technova-staging` | `...5678` | Staging | All engineers |
| `technova-dev` | `...9012` | Development / sandbox | All engineers |
| `technova-shared-services` | `...3456` | CI/CD, ECR, DNS | Platform team |
| `technova-security` | `...7890` | GuardDuty, Security Hub, CloudTrail | Security team |

---

## Requesting Access

### Standard Access (Developer Role)

1. Navigate to [jira.technova.io](https://jira.technova.io) and create a ticket in the **IT** project.
   - **Summary**: `AWS Access Request — [Your Name] — [Account] — [Role]`
   - **Template**: Use the **AWS Access Request** template.
2. Fill in:
   - **Account(s)** needed (e.g., `technova-staging`, `technova-dev`)
   - **Role** needed (see role definitions below)
   - **Business justification** (1–2 sentences)
   - **Manager approval** — assign manager as approver
3. The Platform team provisions access within **1 business day**.

### Emergency Access (Break-Glass)

For SEV1 production incidents requiring immediate elevated access:

1. Post in `#incident-[YYYY-MM-DD]` Slack channel.
2. Contact the on-call Platform Engineer via PagerDuty.
3. Break-glass access is automatically revoked after **4 hours** and logged in CloudTrail.

See [Incident Response](incident-response.md) for the full SEV1 protocol.

---

## AWS IAM Role Definitions

| Role | Permissions | Who |
|------|------------|-----|
| `DeveloperReadOnly` | Read all resources; no writes | All engineers (default) |
| `DeveloperPowerUser` | Read/write to staging and dev resources | Senior engineers (IC4+) |
| `EKSDeployRole` | `eks:*` on non-prod clusters | DevOps, CI/CD systems |
| `RDSReadOnly` | RDS describe + read replica access | Data engineers, analysts |
| `S3FullAccess-[bucket]` | Full access to a specific S3 bucket | Per-team, scoped by resource |
| `AdministratorAccess` | Full access | Platform team, break-glass only |

---

## Configuring AWS CLI with SSO

After your access is provisioned, configure the AWS CLI:

```bash
# Install AWS CLI v2
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Configure SSO profile
aws configure sso
# SSO start URL: https://technova.awsapps.com/start
# SSO region: us-east-1
# Select account and role when prompted

# Add to ~/.aws/config manually for repeatable use:
cat >> ~/.aws/config << 'EOF'
[profile technova-dev]
sso_start_url = https://technova.awsapps.com/start
sso_region = us-east-1
sso_account_id = XXXXXXXXXXXX
sso_role_name = DeveloperPowerUser
region = us-east-1
output = json
EOF

# Log in
aws sso login --profile technova-dev

# Verify
aws sts get-caller-identity --profile technova-dev
```

---

## MFA and Session Duration

- All human AWS SSO sessions require Okta MFA (enforced by Identity Center).
- Session tokens expire after **8 hours** for standard roles, **1 hour** for `AdministratorAccess`.
- Re-run `aws sso login --profile <profile>` to refresh.

Follow the [Password Policy](password-policy.md) for MFA hardware key requirements for privileged roles.

---

## Access Reviews

The Security team conducts **quarterly access reviews** using AWS Access Analyzer. Engineers who have not logged in to an account in 90+ days will have their access suspended automatically. Reactivation requires a new Jira request.

---

## Related Documents

- [VPN Setup Guide](vpn-setup-guide.md)
- [Password Policy](password-policy.md)
- [Incident Response](incident-response.md)
- [Database Access](database-access.md)
- [Monitoring & Alerting](monitoring-alerting.md)
