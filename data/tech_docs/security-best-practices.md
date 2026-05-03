# Security Best Practices — TechNova Solutions

**Owner:** Information Security Team | **Last Updated:** 2025-09-20 | **Applies To:** All Employees and Contractors

---

## Overview

Security is a shared responsibility at TechNova Solutions. This document provides mandatory baseline security practices for all employees, with additional requirements for engineers with access to production systems and customer data. Violations may result in access suspension and disciplinary action.

For credential-specific requirements, refer to the [Password Policy](password-policy.md).

---

## Identity and Access Management

### Okta SSO

All company applications must be accessed through **Okta SSO** at [okta.technova.io](https://okta.technova.io). Direct login with a local password to any company-managed SaaS tool is prohibited where SSO is available.

### MFA Requirements

- **Everyone**: Okta Verify (TOTP) or hardware YubiKey for all Okta-protected applications.
- **Engineers with AWS access**: YubiKey 5 NFC mandatory for production account access.
- **Admins (GitHub Enterprise, AWS Admin, Okta Admin)**: Hardware key is the only accepted second factor.

Register hardware keys at [okta.technova.io/enroll](https://okta.technova.io/enroll).

### Principle of Least Privilege

Request only the permissions required for your current role. See [AWS Access Request](aws-access-request.md) and [GitHub Access](github-access.md) for access request procedures.

---

## Endpoint Security

### Approved Devices

All devices used for TechNova work must be:
1. Company-issued or enrolled in MDM (Jamf Pro at [mdm.technova.io](https://mdm.technova.io)).
2. Running an approved OS version (macOS 13+, Ubuntu 22.04 LTS+, Windows 11).
3. Encrypted (FileVault 2 on macOS, BitLocker on Windows, LUKS on Linux).
4. Protected by the CrowdStrike Falcon endpoint agent — automatically installed via MDM.

### Screen Lock

- Auto-lock after **5 minutes** of inactivity.
- Require password/biometric to unlock.

---

## Secure Coding Practices

All engineers contributing to the **FlowEngine** codebase must follow these practices:

### Secrets Management

- **Never** commit secrets, API keys, or passwords to Git repositories.
- Use **AWS Secrets Manager** for runtime secrets in production.
- Use **GitHub Secrets** for CI/CD workflows.
- Scan locally before committing:

```bash
# Install detect-secrets
pip install detect-secrets

# Scan staged files
detect-secrets scan --baseline .secrets.baseline

# Run as pre-commit hook
pre-commit install
```

### Dependency Scanning

```bash
# Python — check for known vulnerabilities
pip install safety
safety check --full-report

# Node.js
npm audit --audit-level=high
```

All critical and high vulnerabilities in direct dependencies must be remediated before merging to `main`.

### Input Validation

- Validate and sanitize all user inputs at the API boundary.
- Use parameterized queries for all database interactions — never string-interpolated SQL.
- Apply rate limiting on all public-facing FlowEngine API endpoints (configured via Cloudflare WAF at [cloudflare.technova.io](https://cloudflare.technova.io)).

---

## Network Security

- Always use the TechNova VPN when working from a non-office network (see [VPN Setup Guide](vpn-setup-guide.md)).
- Do not connect company devices to public Wi-Fi without VPN active.
- Do not split-tunnel traffic from company devices unless explicitly approved by the Security team.

---

## Data Handling

| Data Classification | Examples | Handling Requirements |
|--------------------|----------|----------------------|
| **Public** | Marketing content, docs | No restrictions |
| **Internal** | Slack messages, Confluence | Company devices only |
| **Confidential** | Customer data, financials | Encrypted; access audited |
| **Restricted** | PII, auth credentials, prod DB | Strict access control; logged |

Customer data from FlowEngine must never be copied to development or staging environments without anonymization approval from the Privacy team.

---

## Phishing and Social Engineering

- Do not click links or open attachments from unexpected senders.
- Report suspicious emails using Gmail's **Report Phishing** option and forward to security@technova.io.
- If you believe you've been phished, immediately contact the Security team and follow the [Incident Response](incident-response.md) process (treat as SEV2).

---

## Security Incident Reporting

Report all security incidents or near-misses to:
- **Slack**: `#security-incidents` (immediate)
- **Email**: security@technova.io
- **Jira**: Create ticket in **SEC** project, priority **High** or **Critical**

---

## Related Documents

- [Password Policy](password-policy.md)
- [VPN Setup Guide](vpn-setup-guide.md)
- [Incident Response](incident-response.md)
- [AWS Access Request](aws-access-request.md)
