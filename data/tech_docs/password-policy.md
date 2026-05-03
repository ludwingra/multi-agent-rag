# Password Policy — TechNova Solutions

**Owner:** IT Security | **Last Updated:** 2025-09-01 | **Applies To:** All Employees and Contractors

---

## Purpose

This policy establishes the minimum requirements for password and credential management at TechNova Solutions. Adherence is mandatory for all accounts that access TechNova systems, including SaaS tools, AWS, GitHub Enterprise, and the FlowEngine platform infrastructure.

---

## Password Manager: 1Password Teams

All TechNova employees are provisioned a **1Password Teams** account at onboarding. Every password for company-related services **must** be stored in 1Password. Under no circumstances should passwords be stored in plain text, browser autofill, or version control.

- Vault access: [1password.com/sign-in/technova](https://1password.com/sign-in/technova)
- For vault setup assistance, see [Laptop Setup Guide](laptop-setup.md).

---

## Password Requirements

### General Accounts (SaaS, Confluence, Jira, Slack)

| Attribute | Requirement |
|-----------|-------------|
| Minimum length | 16 characters |
| Complexity | Upper, lower, digit, symbol |
| Reuse | Last 12 passwords prohibited |
| Expiry | 180 days (enforced via Okta) |

### Privileged Accounts (AWS IAM, GitHub Enterprise Admin, DB admin)

| Attribute | Requirement |
|-----------|-------------|
| Minimum length | 24 characters |
| Complexity | All character classes required |
| Reuse | Last 24 passwords prohibited |
| Expiry | 90 days |
| MFA | Mandatory (hardware key preferred) |

---

## Multi-Factor Authentication (MFA)

MFA is enforced for all accounts via **Okta** SSO. Acceptable second factors:

1. **YubiKey 5 series** (preferred for engineers with AWS access)
2. **Okta Verify** (TOTP app — iOS/Android)
3. **Google Authenticator** (fallback only, no push approval)

Hardware keys must be registered at [okta.technova.io/enroll](https://okta.technova.io/enroll). See [Security Best Practices](security-best-practices.md) for full MFA guidance.

---

## SSH Keys and API Tokens

- SSH keys: minimum **Ed25519** or RSA-4096. Store private keys with a strong passphrase in 1Password.
- AWS access keys: must be rotated every **90 days**. Use IAM roles for service-to-service auth whenever possible; static keys for humans are discouraged.
- GitHub Personal Access Tokens: scope to minimum required permissions; expire in **30 days** for personal tokens, **90 days** for CI tokens.
- API tokens for Datadog, PagerDuty, Sentry: store in AWS Secrets Manager — never in `.env` files committed to GitHub.

```bash
# Generate a strong Ed25519 SSH key
ssh-keygen -t ed25519 -C "you@technova.io" -f ~/.ssh/technova_ed25519

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/technova_ed25519
```

---

## Incident Reporting

If you suspect a password or credential has been compromised:

1. Immediately reset the credential via the relevant service.
2. Rotate any related API tokens or SSH keys.
3. Notify `#security-incidents` on Slack within **1 hour**.
4. Open a Jira ticket in the **SEC** project with priority **High**.

See [Incident Response](incident-response.md) for the full escalation procedure.

---

## Compliance and Enforcement

Violations of this policy may result in account suspension and disciplinary action as outlined in the Employee Handbook. Okta enforces password complexity and expiry automatically. The Security team conducts quarterly audits using 1Password's **Watchtower** feature to identify weak, reused, or compromised credentials.

---

## Related Documents

- [Security Best Practices](security-best-practices.md)
- [AWS Access Request](aws-access-request.md)
- [Incident Response](incident-response.md)
- [Laptop Setup Guide](laptop-setup.md)
