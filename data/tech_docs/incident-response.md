# Incident Response Runbook — TechNova Solutions

**Owner:** Site Reliability Engineering (SRE) | **Last Updated:** 2025-10-05 | **Applies To:** All On-Call Engineers

---

## Overview

This runbook defines TechNova Solutions' incident response process for the **FlowEngine** platform. TechNova targets **99.95% monthly uptime** for FlowEngine. All incidents are managed via **PagerDuty** for alerting and coordination, **Datadog** for observability, and **Slack** for communication.

---

## Severity Definitions

| Severity | Description | Example | Response Time |
|----------|-------------|---------|---------------|
| **SEV1** | Customer-facing outage; >25% of customers impacted | FlowEngine API down | Immediate (< 5 min) |
| **SEV2** | Degraded performance; partial feature unavailability | Webhook processing 50% slower | < 15 minutes |
| **SEV3** | Internal systems affected; no customer impact | Internal dashboard down | < 1 hour |
| **SEV4** | Cosmetic / low-impact issue | Minor UI glitch | Next business day |

---

## On-Call Structure

- **Primary on-call**: Rotates weekly per team in PagerDuty.
- **Secondary on-call**: Senior IC (IC4+) as escalation fallback.
- **Incident Commander (IC)**: On-call manager for SEV1/SEV2.
- Schedule viewable at [pagerduty.technova.io](https://pagerduty.technova.io).

Team schedules:
- `Platform SRE` — infra and Kubernetes
- `Backend Core` — FlowEngine API services
- `Data Platform` — Kafka, ETL pipelines
- `Frontend` — UI / CDN issues

---

## Incident Response Process

### Step 1 — Alert Fires

PagerDuty triggers based on Datadog monitors. The on-call engineer receives a push notification and must **acknowledge** within **5 minutes** for SEV1.

```bash
# Check PagerDuty from CLI (pd-cli)
pd incidents list --status=triggered
pd incidents ack --id <INCIDENT_ID>
```

### Step 2 — Assess and Declare Severity

1. Check Datadog dashboards: [app.datadoghq.com/dashboard/technova-prod](https://app.datadoghq.com/dashboard/technova-prod)
2. Check Sentry for error spikes: [sentry.technova.io](https://sentry.technova.io)
3. Review recent deploys in ArgoCD: [argocd.technova.io](https://argocd.technova.io)
4. Check AWS Health dashboard for regional events.

### Step 3 — Create Incident Slack Channel

For SEV1 and SEV2:

```
#incident-YYYY-MM-DD-description
```

Example: `#incident-2025-10-05-api-timeout-spike`

Post the incident kickoff message using the `/incident new` Slack bot command. This creates the Jira ticket automatically in the **INFRA** project.

### Step 4 — Triage and Mitigate

Common mitigation actions:

```bash
# Restart a deployment in Kubernetes
kubectl rollout restart deployment/flowengine-api -n production

# Check pod status
kubectl get pods -n production -l app=flowengine-api

# Rollback to previous deployment
kubectl rollout undo deployment/flowengine-api -n production

# Scale up replicas during load spike
kubectl scale deployment/flowengine-api --replicas=12 -n production
```

For database issues, refer to [Database Access](database-access.md).
For AWS-level issues, refer to [AWS Access Request](aws-access-request.md) for break-glass escalation.

### Step 5 — Communicate Status

Update the public status page at [status.technova.io](https://status.technova.io) for SEV1/SEV2 using the **Statuspage** integration in Slack (`/status update`).

### Step 6 — Resolve and Post-Mortem

1. Mark incident resolved in PagerDuty.
2. Update Jira ticket to **Done**.
3. For SEV1 and SEV2: a **Post-Mortem (PIR — Post Incident Review)** is mandatory within **48 hours**.
   - Template: [Confluence PIR Template](https://confluence.technova.io/pir-template)
   - Owner: Incident Commander
   - Blameless culture — focus on systems, not individuals.

---

## Escalation Contacts

| Role | Contact |
|------|---------|
| VP Engineering | Raj Patel — via PagerDuty escalation policy |
| CTO | Marcus Rivera — SEV1 only, after 30 min unresolved |
| AWS TAM | Available via [support.aws.amazon.com](https://support.aws.amazon.com) (Business/Enterprise support) |

---

## Key Runbook Links

- [Monitoring & Alerting](monitoring-alerting.md) — Datadog alert configuration
- [Disaster Recovery](disaster-recovery.md) — failover to eu-west-1
- [Database Access](database-access.md) — DB emergency access

---

## Related Documents

- [Monitoring & Alerting](monitoring-alerting.md)
- [Disaster Recovery](disaster-recovery.md)
- [AWS Access Request](aws-access-request.md)
- [Database Access](database-access.md)
