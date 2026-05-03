# Software Licenses and Approved Tools — TechNova Solutions

**Owner:** IT Operations / Legal | **Last Updated:** 2025-09-05 | **Applies To:** All Employees

---

## Overview

This document lists the software tools that TechNova Solutions licenses for employee use, including seat counts, license tiers, and approved usage scope. It also defines the process for requesting a tool not on this list.

Installing unlicensed software on company devices or using personal accounts for company work is a violation of TechNova's Acceptable Use Policy.

---

## Licensed Tools by Category

### Development Tools

| Tool | License Tier | Seats | Access |
|------|-------------|-------|--------|
| GitHub Enterprise Server 3.12 | Enterprise | Unlimited (org-wide) | [github.technova.io](https://github.technova.io) |
| JetBrains Toolbox (All Products) | All Products Pack | 300 | [toolbox.technova.io](https://toolbox.technova.io/activate) |
| VS Code | Free (OSS) | Unlimited | [code.visualstudio.com](https://code.visualstudio.com) |
| Docker Desktop | Business | 300 | Provisioned via MDM |
| Postman | Team | 150 | [postman.technova.io](https://postman.technova.io) |
| Stoplight Studio | Team | 50 | [stoplight.technova.io](https://stoplight.technova.io) |

### Productivity and Collaboration

| Tool | License Tier | Seats | Access |
|------|-------------|-------|--------|
| Google Workspace Business Plus | Business Plus | 500 | Okta SSO |
| Slack | Business+ | 500 | [technova.slack.com](https://technova.slack.com) |
| Zoom | Business | 500 | Okta SSO |
| Confluence Cloud | Standard | 500 | [jira.technova.io/wiki](https://jira.technova.io/wiki) |
| Jira Software Cloud | Standard | 500 | [jira.technova.io](https://jira.technova.io) |
| Notion | Team | 100 (Product/Design) | [notion.technova.io](https://notion.technova.io) |
| Loom | Business | 150 | Okta SSO |

### Security and Identity

| Tool | License | Seats | Access |
|------|---------|-------|--------|
| Okta Workforce Identity | Workforce | 500 + contractors | [okta.technova.io](https://okta.technova.io) |
| 1Password Teams | Teams | 500 | [1password.com/technova](https://1password.com/sign-in/technova) |
| CrowdStrike Falcon | Go | 500 endpoints | Managed via MDM |

### Cloud and Infrastructure

| Tool | License | Notes |
|------|---------|-------|
| AWS | Enterprise Discount Program | Billed by usage; access via [AWS SSO](aws-access-request.md) |
| Datadog | Pro + APM | 300 hosts; see [Monitoring & Alerting](monitoring-alerting.md) |
| PagerDuty | Business | Per-schedule pricing |
| Sentry (self-hosted) | Self-hosted | No per-seat cost |
| Cloudflare Teams | Business | 500 seats + WAF |

---

## License Activation

Most tools are activated via **Okta SSO** — simply navigate to the tool's URL and sign in with your `@technova.io` account. For tools requiring a license key (e.g., JetBrains), retrieve it from the **IT** vault in 1Password (ask your IT contact to share it on day one).

```bash
# Activate JetBrains via CLI (after installing Toolbox)
# Navigate to: https://toolbox.technova.io/activate
# Or open JetBrains IDE → Help → Register → Activate with License Server
# Server URL: https://license.jetbrains.technova.io
```

---

## Requesting New Software

If you need a tool not listed here:

1. Check if an existing licensed tool covers the need.
2. Create a Jira ticket in the **IT** project:
   - **Summary**: `Software Request — [Tool Name]`
   - **Description**: Use case, team need, cost estimate, and number of seats required.
   - **Approval**: Your manager must approve.
3. IT and Legal review for security compliance (typically **3–5 business days**).
4. If approved, IT procures and provisions the license.

High-cost requests (> $5,000/year) require VP approval. Contact your manager.

---

## Open Source Licensing

All open source dependencies used in TechNova products must use **permissive licenses** (MIT, Apache 2.0, BSD). Dependencies with **GPL, AGPL, or LGPL** licenses require a review from Legal before inclusion. Create a Jira ticket in the **SEC** project to initiate review.

Check your dependencies:
```bash
# Python
pip install pip-licenses
pip-licenses --format=table

# Node.js
npx license-checker --summary
```

---

## FAQ

**Q: Can I use my personal JetBrains license for work?**
A: TechNova provides JetBrains licenses for all engineers; use the company license to ensure support and compliance.

**Q: Can I install free/open-source tools not on this list?**
A: Yes, for development tooling (CLIs, editors, etc.). Tools that process customer data or integrate with company systems require IT review.

**Q: My Slack seat is inactive — can I share a license with a contractor?**
A: No. Contractors must have their own provisioned accounts. Contact IT for contractor provisioning.

---

## Related Documents

- [Security Best Practices](security-best-practices.md)
- [Laptop Setup Guide](laptop-setup.md)
- [AWS Access Request](aws-access-request.md)
- [Jira Workflow](jira-workflow.md)
