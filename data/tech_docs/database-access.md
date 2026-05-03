# Database Access Guide — TechNova Solutions

**Owner:** Platform Engineering / DBA Team | **Last Updated:** 2025-10-02 | **Applies To:** Backend Engineers, Data Engineers, SRE

---

## Overview

TechNova Solutions runs two primary database technologies for the **FlowEngine** platform:
- **PostgreSQL 16** on Amazon RDS (Multi-AZ, `db.r7g.2xlarge` in production) — primary transactional store.
- **Redis 7.2** on Amazon ElastiCache (cluster mode, 3 shards) — caching and pub/sub.

All database connections must go through the TechNova VPN and use role-based IAM authentication where possible. Direct static-credential DB access to production is restricted to the SRE team and break-glass scenarios.

---

## Access Tiers

| Tier | Who | Access |
|------|-----|--------|
| **Developer** | All engineers | Read-only to staging replicas |
| **Power User** | Senior engineers (IC4+) | Read/write to staging; read to prod replica |
| **DBA/SRE** | Platform team, SRE | Full access to staging; write access to prod |
| **Break-glass** | On-call IC (SEV1) | Temporary production write (4-hour TTL) |

Request access via Jira in the **IT** project. See [AWS Access Request](aws-access-request.md) for the provisioning process.

---

## PostgreSQL Connection Details

### Hosts

| Environment | Host | Port |
|-------------|------|------|
| Production primary | `prod-pg.db.technova.internal` | 5432 |
| Production replica | `prod-pg-ro.db.technova.internal` | 5432 |
| Staging | `staging-pg.db.technova.internal` | 5432 |
| Development | `dev-pg.db.technova.internal` | 5432 |

All hosts are internal DNS — VPN required. See [VPN Setup Guide](vpn-setup-guide.md).

### Connecting via psql

```bash
# Development (IAM auth via AWS CLI SSO)
export PGPASSWORD=$(aws rds generate-db-auth-token \
  --hostname dev-pg.db.technova.internal \
  --port 5432 \
  --region us-east-1 \
  --username developer \
  --profile technova-dev)

psql -h dev-pg.db.technova.internal -U developer -d flowengine_dev

# Staging read-only
psql -h staging-pg.db.technova.internal -U readonly -d flowengine_staging
```

### Connection via pgcli (recommended for exploration)

```bash
brew install pgcli
pgcli -h staging-pg.db.technova.internal -U readonly -d flowengine_staging
```

---

## Database Schema Overview

| Schema | Purpose |
|--------|---------|
| `public` | Core FlowEngine entities (workflows, runs, triggers) |
| `audit` | Immutable audit log table (append-only) |
| `analytics` | Aggregated reporting tables (refreshed nightly) |
| `internal` | Platform metadata; not customer-facing |

Run `\dn` in psql to list schemas. DDL changes require a migration file (Alembic) — see [Dev Environment Setup](dev-environment-setup.md) for migration instructions.

---

## Running Migrations

```bash
# From the flowengine-core repo
cd services/api

# Generate a new migration
alembic revision --autogenerate -m "add_webhook_retry_count"

# Apply to dev
alembic upgrade head

# Preview SQL without applying
alembic upgrade head --sql

# Rollback one step
alembic downgrade -1
```

Migrations to staging and production are run by the CI/CD pipeline during deploy. Manual migration on production requires a Jira approval ticket (INFRA project, priority Critical) and must be run during maintenance windows.

---

## Redis Connection Details

| Environment | Host | Port |
|-------------|------|------|
| Production | `prod-redis.cache.technova.internal` | 6379 |
| Staging | `staging-redis.cache.technova.internal` | 6379 |

```bash
# Connect to Redis CLI (staging)
redis-cli -h staging-redis.cache.technova.internal -p 6379 --tls

# Check memory usage
redis-cli -h staging-redis.cache.technova.internal INFO memory | grep used_memory_human
```

---

## Query Performance Guidelines

- All queries running > **1 second** on staging should be reviewed before merge.
- Use `EXPLAIN ANALYZE` to diagnose slow queries:
  ```sql
  EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
  SELECT * FROM workflow_runs WHERE tenant_id = $1 AND status = 'failed'
  ORDER BY created_at DESC LIMIT 100;
  ```
- Add indexes via Alembic migrations; never add indexes ad-hoc on production.
- Use the read replica (`-ro` hosts) for reporting queries and analytics workloads.

---

## Security

- Passwords/connection strings must be stored in AWS Secrets Manager, not in `.env` files. See [Security Best Practices](security-best-practices.md).
- All connections must use TLS (`sslmode=require`).
- Destructive SQL (`DROP`, `TRUNCATE`, `DELETE` without `WHERE`) on production requires a two-person review and Jira approval.

---

## Related Documents

- [VPN Setup Guide](vpn-setup-guide.md)
- [AWS Access Request](aws-access-request.md)
- [Security Best Practices](security-best-practices.md)
- [Dev Environment Setup](dev-environment-setup.md)
- [Data Backup Policy](data-backup-policy.md)
