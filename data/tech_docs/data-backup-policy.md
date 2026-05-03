# Data Backup Policy — TechNova Solutions

**Owner:** Platform Engineering / SRE | **Last Updated:** 2025-09-15 | **Classification:** Internal | **Applies To:** All Engineering and Operations Teams

---

## Purpose

This policy defines TechNova Solutions' backup strategy for all data assets supporting the **FlowEngine** platform and internal operations. It establishes backup frequency, retention periods, verification procedures, and responsibilities to meet our **99.95% uptime SLA** and RPO of **15 minutes**.

---

## Data Classification and Backup Requirements

| Data Type | Classification | Backup Tool | Frequency | Retention |
|-----------|---------------|-------------|-----------|-----------|
| FlowEngine PostgreSQL (prod) | Restricted | RDS PITR + Snapshots | Continuous / Daily | 35 days (PITR), 90 days (snapshots) |
| FlowEngine PostgreSQL (staging) | Confidential | RDS Snapshots | Daily | 14 days |
| Redis ElastiCache (prod) | Confidential | ElastiCache Backups | Daily | 7 days |
| S3 assets (prod) | Internal / Confidential | S3 Versioning + CRR | Continuous | 90 days (versions) |
| GitHub Enterprise repositories | Internal | GHES backup utility | Daily | 30 days |
| Confluence / Jira | Internal | Cloud export + S3 | Weekly | 1 year |
| Employee data (BambooHR) | Restricted | Vendor-managed | Daily | 7 years |

---

## PostgreSQL Backup Configuration

### Point-in-Time Recovery (PITR)

Amazon RDS is configured with automated backups and WAL archiving. PITR allows restoring the database to any second within the retention window.

```bash
# Restore to a specific point in time (SRE use only)
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier prod-pg \
  --target-db-instance-identifier prod-pg-restored-20251005-1430 \
  --restore-time 2025-10-05T14:30:00Z \
  --region us-east-1

# Wait for restore to complete
aws rds wait db-instance-available \
  --db-instance-identifier prod-pg-restored-20251005-1430 \
  --region eu-west-1
```

### Manual Snapshots

Snapshots are taken automatically before every production database migration and before major deployments:

```bash
# Create a pre-migration snapshot
aws rds create-db-snapshot \
  --db-instance-identifier prod-pg \
  --db-snapshot-identifier prod-pg-pre-migration-FEC421-$(date +%Y%m%d) \
  --region us-east-1
```

Snapshots are tagged with `Purpose: pre-migration`, `Ticket: FEC-421`, and `Owner: <engineer-name>`.

---

## S3 Backup Configuration

All production S3 buckets have:
- **Versioning enabled** — previous object versions retained for 90 days.
- **Cross-Region Replication (CRR)** — `us-east-1` → `eu-west-1` for DR.
- **Object Lock** — on the `technova-audit-logs-use1` bucket (COMPLIANCE mode, 7-year retention).

```bash
# List bucket versions (check versioning is active)
aws s3api get-bucket-versioning --bucket technova-prod-assets-use1

# Restore a specific version
aws s3api copy-object \
  --bucket technova-prod-assets-use1 \
  --copy-source "technova-prod-assets-use1/uploads/contract.pdf?versionId=ABCDEF123456" \
  --key uploads/contract.pdf
```

---

## GitHub Enterprise Repository Backup

The `technova-platform` team runs the official [GHES Backup Utilities](https://github.com/github/backup-utils) on a dedicated EC2 instance (`ghes-backup.internal.technova.io`).

```bash
# Verify last backup timestamp
ssh ghes-backup.internal.technova.io "cat /opt/ghes-backup/current/backup-snapshot-info.json | jq .started_at"

# Manual backup trigger (SRE only)
ssh ghes-backup.internal.technova.io "/opt/ghes-backup/bin/ghe-backup"
```

Backups are stored in S3 (`technova-ghes-backups-use1`) and replicated to `eu-west-1`.

---

## Backup Verification

Backups are worthless unless tested. The following verification procedures run on schedule:

| Verification | Frequency | Procedure |
|-------------|-----------|-----------|
| RDS restore smoke test | Monthly | Restore to test instance; run `SELECT count(*) FROM workflow_runs;` |
| S3 restore test | Quarterly | Download a versioned object and validate MD5 checksum |
| GHES restore test | Quarterly | Spin up test GHES instance and restore from backup |
| Full DR restore | Semi-annual | Execute full DR failover (see [Disaster Recovery](disaster-recovery.md)) |

Results of each verification test are recorded in Confluence at [confluence.technova.io/backup-verification-log](https://confluence.technova.io/backup-verification-log).

---

## Backup Alerting

Backup failures alert via Datadog to `#alerts-prod` and trigger a SEV3 PagerDuty incident. Missed backup windows (> 2x expected interval) also trigger alerts.

See [Monitoring & Alerting](monitoring-alerting.md) for alert configuration details.

---

## Compliance and Retention

- Customer data backups must comply with GDPR (EU customers) and CCPA (CA customers).
- Data deletion requests (Right to Erasure) must be applied to **all backups** within **30 days**. Coordinate with the Privacy team for erasure from PITR windows.
- Audit logs (CloudTrail, application audit schema) are subject to **7-year immutable retention** per SOC 2 requirements.
- The Security team audits backup compliance quarterly.

---

## Related Documents

- [Disaster Recovery](disaster-recovery.md)
- [Database Access](database-access.md)
- [Monitoring & Alerting](monitoring-alerting.md)
- [Security Best Practices](security-best-practices.md)
