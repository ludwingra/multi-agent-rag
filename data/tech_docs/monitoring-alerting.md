# Monitoring & Alerting — TechNova Solutions

**Owner:** Site Reliability Engineering (SRE) | **Last Updated:** 2025-10-10 | **Applies To:** All Engineering Teams and On-Call Engineers

---

## Overview

TechNova Solutions uses a three-layer observability stack for the **FlowEngine** platform:

- **Datadog** — APM, infrastructure metrics, log management, synthetic monitoring
- **PagerDuty** — On-call scheduling, alert routing, and incident escalation
- **Sentry** — Application error tracking and performance monitoring

All dashboards require VPN access (see [VPN Setup Guide](vpn-setup-guide.md)) and Okta SSO login.

---

## Datadog

### Access

- URL: [app.datadoghq.com](https://app.datadoghq.com)
- Org: `technova-prod`
- Login via Okta SSO at [okta.technova.io](https://okta.technova.io)

### Key Dashboards

| Dashboard | URL Path | Audience |
|-----------|----------|---------|
| FlowEngine Overview | `/dashboard/flowengine-overview` | All engineering |
| API Latency & Throughput | `/dashboard/api-latency` | Backend teams |
| EKS Cluster Health | `/dashboard/eks-cluster` | SRE, DevOps |
| PostgreSQL Performance | `/dashboard/postgres-perf` | Backend, DBA |
| Business Metrics | `/dashboard/business-kpis` | Engineering + Product |

### APM — Service Naming Convention

Services are named: `{service}-{environment}` (e.g., `flowengine-api-production`, `worker-scheduler-staging`).

```python
# Python APM instrumentation (auto-applied via ddtrace)
# In Dockerfile / startup command:
# CMD ["ddtrace-run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Manual span example
from ddtrace import tracer

with tracer.trace("workflow.execute", service="flowengine-api", resource="run_workflow") as span:
    span.set_tag("workflow_id", workflow_id)
    span.set_tag("tenant_id", tenant_id)
    result = execute_workflow(workflow_id)
```

### Log Collection

All application logs must be structured JSON sent to stdout. Datadog Log Agent (running as a DaemonSet in EKS) collects logs automatically.

```python
import structlog

log = structlog.get_logger()
log.info("workflow.run.started", workflow_id=wf_id, tenant_id=t_id, step_count=n)
```

Required log fields: `level`, `timestamp` (ISO 8601), `service`, `env`, `trace_id`.

---

## Alert Thresholds

### Production SLO Monitors

| Monitor | Threshold | Severity | Escalation |
|---------|-----------|----------|------------|
| API P99 latency | > 2 seconds for 5 min | SEV2 | Platform on-call |
| API error rate | > 1% for 5 min | SEV2 | Backend on-call |
| API error rate | > 5% for 2 min | SEV1 | All on-call + EM |
| EKS pod crash loop | Any pod CrashLoopBackOff in prod | SEV2 | SRE on-call |
| DB connection pool saturation | > 85% for 3 min | SEV2 | DBA + SRE |
| Redis memory usage | > 80% | SEV3 | Platform team |
| Failed payment webhooks | > 10 in 1 min | SEV2 | Backend on-call |

All SEV1/SEV2 monitors fire into `#alerts-prod` Slack and trigger PagerDuty.

---

## PagerDuty

### Access and On-Call Schedule

- URL: [pagerduty.technova.io](https://pagerduty.technova.io)
- On-call schedule view: [pagerduty.technova.io/my-on-call](https://pagerduty.technova.io/my-on-call)
- Rotations are **weekly**, Sunday 12:00 UTC handoff.

### Escalation Policies

```
Alert fires in Datadog
    │ (immediate)
    ▼
Primary On-Call (10 min to acknowledge)
    │ (if no ack)
    ▼
Secondary On-Call (10 min)
    │ (if no ack)
    ▼
Engineering Manager (M1)
    │ (if SEV1 > 30 min unresolved)
    ▼
VP Engineering (Raj Patel)
```

### Acknowledging and Resolving Alerts

```bash
# Using PagerDuty CLI (pd-cli)
pip install pdpyras

# Acknowledge
pd incidents ack --id <INCIDENT_ID>

# Add note
pd incidents notes create --id <INCIDENT_ID> --content "Investigating Redis memory spike — possible cache key leak in batch processor"

# Resolve
pd incidents resolve --id <INCIDENT_ID>
```

---

## Sentry

### Access

- URL: [sentry.technova.io](https://sentry.technova.io) (self-hosted Sentry 24.x)
- Login via Okta SSO

### Projects

| Sentry Project | Service |
|---------------|---------|
| `flowengine-api` | Backend Python services |
| `flowengine-frontend` | React / TypeScript frontend |
| `worker-scheduler` | Celery task workers |

### Setting Alert Rules

Navigate to **Sentry** → **Alerts** → **Create Alert Rule**. Recommended threshold for production: fire when **error rate > 5 errors/minute** for any issue tagged `environment:production`.

---

## Synthetic Monitoring

Datadog Synthetic tests run every **5 minutes** from AWS `us-east-1` and `eu-west-1`:
- `GET https://api.technova.io/v1/health` — expects `200 OK` within 500ms.
- `POST https://api.technova.io/v1/workflows` (with test credentials) — end-to-end smoke test.

Failures trigger SEV2 immediately. See [Incident Response](incident-response.md) for triage steps.

---

## Related Documents

- [Incident Response](incident-response.md)
- [Disaster Recovery](disaster-recovery.md)
- [CI/CD Pipeline](ci-cd-pipeline.md)
- [VPN Setup Guide](vpn-setup-guide.md)
