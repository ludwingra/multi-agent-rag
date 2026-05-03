# Disaster Recovery Plan — TechNova Solutions

**Owner:** Site Reliability Engineering (SRE) | **Last Updated:** 2025-09-30 | **Classification:** Confidential — Internal Only | **Applies To:** SRE, DevOps, Engineering Leadership

---

## Overview

This document describes the Disaster Recovery (DR) plan for the **FlowEngine** platform at TechNova Solutions. The plan defines Recovery Time Objective (RTO), Recovery Point Objective (RPO), failover procedures from the primary AWS region (`us-east-1`) to the DR region (`eu-west-1`), and the annual DR test schedule.

FlowEngine targets **99.95% monthly uptime**. DR procedures are invoked when a `us-east-1` regional failure is confirmed and cannot be resolved within **30 minutes**.

---

## Recovery Objectives

| Metric | Target | Notes |
|--------|--------|-------|
| **RTO** (Recovery Time Objective) | **2 hours** | Time from decision to failover complete |
| **RPO** (Recovery Point Objective) | **15 minutes** | Maximum data loss window |
| **Data backup frequency** | Every 15 minutes (RDS PITR) | See [Data Backup Policy](data-backup-policy.md) |

---

## Architecture Overview

| Component | Primary (us-east-1) | DR (eu-west-1) |
|-----------|--------------------|--------------------|
| EKS Cluster | `technova-prod-use1` (active) | `technova-dr-euw1` (warm standby) |
| RDS PostgreSQL | Multi-AZ `prod-pg.db.technova.internal` | Cross-region read replica |
| ElastiCache Redis | 3-shard cluster | Single-shard standby |
| S3 | `technova-prod-assets-use1` | Cross-region replication → `technova-dr-assets-euw1` |
| CloudFront | Global CDN | Automatic rerouting |
| Route 53 | `api.technova.io` → us-east-1 | Failover routing policy to eu-west-1 |

---

## Failover Decision Tree

```
AWS us-east-1 service disruption detected
        │
        ▼
Is it limited to a single AZ? → YES → EKS auto-reschedules pods; no DR needed
        │ NO
        ▼
Is partial degradation recoverable in < 30 min? → YES → Incident triage only
        │ NO
        ▼
Declare DR event → Notify VP Engineering (Raj Patel) + CTO (Marcus Rivera)
        │
        ▼
Execute Failover Runbook (see below)
```

---

## Failover Runbook

### Step 1 — Promote DR Database

```bash
# Promote eu-west-1 read replica to standalone primary
aws rds promote-read-replica \
  --db-instance-identifier prod-pg-dr-euw1 \
  --region eu-west-1

# Wait for promotion (typically 5-10 minutes)
aws rds wait db-instance-available \
  --db-instance-identifier prod-pg-dr-euw1 \
  --region eu-west-1

# Verify endpoint
aws rds describe-db-instances \
  --db-instance-identifier prod-pg-dr-euw1 \
  --region eu-west-1 \
  --query 'DBInstances[0].Endpoint.Address'
```

### Step 2 — Scale DR EKS Cluster

```bash
# Scale up DR node group from 0 to production size
aws eks update-nodegroup-config \
  --cluster-name technova-dr-euw1 \
  --nodegroup-name workers \
  --scaling-config minSize=6,maxSize=20,desiredSize=10 \
  --region eu-west-1
```

### Step 3 — Update Secrets for DR Region

```bash
# Copy production secrets to eu-west-1 (automated script)
./scripts/dr/sync-secrets.sh --source us-east-1 --target eu-west-1
```

### Step 4 — Deploy Application to DR Cluster

```bash
# Switch ArgoCD context to DR cluster
kubectl config use-context technova-dr-euw1
argocd cluster add technova-dr-euw1

# Sync all applications
argocd app sync --selector cluster=dr --timeout 600
```

### Step 5 — Update DNS

```bash
# Flip Route 53 failover record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABCDE \
  --change-batch file://scripts/dr/dns-failover-to-euw1.json
```

DNS propagation: **60–90 seconds** (TTL set to 60s on failover records).

### Step 6 — Validate

```bash
# Run DR smoke tests
./scripts/dr/smoke-test.sh --env dr

# Monitor Datadog (eu-west-1 dashboard)
# Check Sentry error rates for flowengine-api
```

### Step 7 — Communicate

- Update status page: [status.technova.io](https://status.technova.io)
- Post in `#incident-*` and `#on-call` Slack channels.
- Notify enterprise customers via automated email (triggered from Statuspage).

---

## DR Test Schedule

| Test Type | Frequency | Owner | Last Tested |
|-----------|-----------|-------|------------|
| Database replica promotion (staging) | Quarterly | SRE | 2025-07-15 |
| Full DR failover (staging environment) | Semi-annual | SRE + EM | 2025-04-20 |
| DNS failover test (synthetic only) | Monthly | Platform | 2025-10-01 |
| Full production DR drill | Annual | CTO-approved | 2025-01-18 |

---

## Post-Failover: Return to Primary

Once `us-east-1` is restored:
1. Re-establish replication from eu-west-1 (now primary) → us-east-1 (new replica).
2. Promote us-east-1 back to primary during a low-traffic window (typically Sunday 02:00–04:00 UTC).
3. Flip DNS back to us-east-1.
4. Write a Post-Incident Review (PIR) per [Incident Response](incident-response.md).

---

## Related Documents

- [Incident Response](incident-response.md)
- [Data Backup Policy](data-backup-policy.md)
- [Monitoring & Alerting](monitoring-alerting.md)
- [AWS Access Request](aws-access-request.md)
