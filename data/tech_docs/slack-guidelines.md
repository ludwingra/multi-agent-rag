# Slack Guidelines — TechNova Solutions

**Owner:** IT Operations / People Ops | **Last Updated:** 2025-08-01 | **Applies To:** All Employees

---

## Overview

Slack is TechNova Solutions' primary tool for real-time communication. The TechNova workspace is available at [technova.slack.com](https://technova.slack.com) and should be accessed using your `@technova.io` Okta SSO credentials. Slack is not a substitute for Jira (task tracking) or Confluence (documentation); keep decision records and runbooks in those tools.

---

## Channel Naming Conventions

| Prefix | Purpose | Example |
|--------|---------|---------|
| `#eng-` | Engineering team channels | `#eng-platform`, `#eng-backend` |
| `#team-` | Cross-functional team channels | `#team-growth`, `#team-data` |
| `#proj-` | Project-specific, time-bounded | `#proj-flowengine-v4-launch` |
| `#incident-` | Active incident coordination | `#incident-2025-10-05-api-down` |
| `#it-` | IT operational channels | `#it-help`, `#it-announcements` |
| `#standup-` | Async standups | `#standup-platform`, `#standup-frontend` |

All channel names must be lowercase with hyphens. No spaces or underscores.

---

## Key Channels

| Channel | Purpose |
|---------|---------|
| `#general` | Company-wide announcements (announcements only; react, don't reply) |
| `#engineering` | Broad engineering discussions, RFCs |
| `#it-help` | IT support requests — Tier 1 triage |
| `#security-incidents` | Report security events immediately |
| `#alerts-prod` | Automated production alerts from Datadog/PagerDuty |
| `#alerts-staging` | CI/CD and staging environment alerts |
| `#on-call` | On-call handoff notes and status |
| `#jira-notifications` | Auto-posted Jira ticket updates |
| `#all-hands` | Company-wide all-hands meeting comms (exec-only posting) |

---

## Etiquette and Norms

### Response Expectations

| Context | Expected Response Time |
|---------|----------------------|
| Direct Messages (DMs) | Within 4 business hours |
| Channel mentions (`@you`) | Within 2 business hours |
| `#it-help` tickets | IT SLA: within 2 hours (business hours) |
| Incident channels | Immediate acknowledgment during on-call |

### Notifications and Focus Time

- Use **Do Not Disturb** during deep work. Schedule your DND in Slack → **Preferences** → **Notifications**.
- Respect teammates' DND status — use urgent notifications (`⚡`) sparingly.
- For async culture: you are **not expected to reply immediately** outside your working hours.

### @-mentions

- `@here` — notifies only active members. Use for time-sensitive channel messages.
- `@channel` — notifies **all** members including DND. Reserve for incident channels and true emergencies.
- `@everyone` — workspace-wide; restricted to `#general` by workspace admins.

---

## Slack for IT Support

To request IT help, post in `#it-help` with:

```
**Issue:** One-line summary
**Device:** MacBook Pro 14" M3 (or model)
**OS:** macOS 15.1
**Steps tried:** (brief list)
**Urgency:** Low / Medium / High
```

IT will triage and respond using the **Halp** integration (tickets auto-created in Jira). See [Jira Workflow](jira-workflow.md) for how IT tickets are tracked.

---

## Slack Integrations

| Integration | Channel | Purpose |
|-------------|---------|---------|
| PagerDuty | `#alerts-prod` | Auto-post SEV1/SEV2 incidents |
| Datadog | `#alerts-prod`, `#alerts-staging` | Monitor alerts |
| GitHub | `#eng-platform` | PR and push notifications |
| Jira | `#jira-notifications` | Issue updates |
| Statuspage | `#on-call` | Status page update confirmations |

---

## Security and Compliance

- Do **not** share passwords, API keys, or sensitive customer data in Slack — not even in DMs. Use 1Password for credentials and AWS Secrets Manager for production secrets.
- Slack messages are retained per TechNova's 3-year retention policy and may be audited.
- Slack is not approved for transmitting **Restricted** data (see [Security Best Practices](security-best-practices.md) for data classification).

---

## Mobile App

Install the Slack mobile app for urgent on-call notifications. Engineers in the on-call rotation **must** enable push notifications for `#alerts-prod` and `#incident-*` channels.

---

## Related Documents

- [Security Best Practices](security-best-practices.md)
- [Jira Workflow](jira-workflow.md)
- [Incident Response](incident-response.md)
- [Email Setup](email-setup.md)
