# Network Troubleshooting Guide — TechNova Solutions

**Owner:** IT Operations | **Last Updated:** 2025-09-10 | **Applies To:** All Employees (Primary), Engineers (Advanced Sections)

---

## Overview

This guide helps TechNova Solutions employees diagnose and resolve common network connectivity issues affecting access to internal tools, the VPN, and the FlowEngine platform. For issues you cannot resolve using this guide, contact IT via `#it-help` on Slack or email support@technova.io.

---

## Quick Diagnostic Checklist

Run these checks in order before escalating:

```bash
# 1. Check local network connectivity
ping -c 4 8.8.8.8

# 2. Check DNS resolution
nslookup confluence.internal.technova.io
dig +short api.technova.io

# 3. Check VPN status
sudo wg show    # Should show peer and latest handshake < 3 minutes ago

# 4. Check internal connectivity (VPN must be on)
curl -I --max-time 5 https://jira.technova.io
curl -I --max-time 5 https://confluence.internal.technova.io

# 5. Check route to internal network
traceroute 10.0.0.1
```

---

## Common Issues and Fixes

### Issue 1: Cannot Connect to VPN

**Symptoms:** WireGuard shows no handshake, tunnel is up but no traffic.

```bash
# Check WireGuard status
sudo wg show

# Restart tunnel
sudo wg-quick down wg0
sudo wg-quick up wg0

# Check if the VPN endpoint is reachable (UDP 51820)
nc -vzu vpn.technova.io 51820
```

If the restart does not help, regenerate your configuration at [vpn.technova.io](https://vpn.technova.io). See [VPN Setup Guide](vpn-setup-guide.md) for the full regeneration process.

### Issue 2: DNS Resolution Failing for Internal Hosts

Internal hostnames (e.g., `*.internal.technova.io`) are only resolvable through the VPN DNS. 

```bash
# Check which DNS server is being used
cat /etc/resolv.conf     # Linux
scutil --dns | head -30  # macOS

# The VPN pushes DNS 10.8.0.1 — confirm it appears when VPN is active
# If missing, check wg0.conf for DNS= line:
sudo grep DNS /etc/wireguard/wg0.conf
```

Expected config entry: `DNS = 10.8.0.1, 10.8.0.2`

### Issue 3: Slow Connection to AWS Services

```bash
# Check latency to us-east-1
ping -c 10 ec2.us-east-1.amazonaws.com

# Check if Cloudflare WAF is introducing latency
curl -w "Connect: %{time_connect}s | TTFB: %{time_starttransfer}s | Total: %{time_total}s\n" \
     -o /dev/null -s https://api.technova.io/v1/health

# Run MTR for path analysis (install with: brew install mtr)
sudo mtr --report api.technova.io
```

Expected TTFB from office network: < 150ms. If > 500ms, open a Jira ticket in **INFRA** and tag SRE.

### Issue 4: SSL/TLS Certificate Errors

```bash
# Check certificate validity and chain
openssl s_client -connect api.technova.io:443 -servername api.technova.io 2>/dev/null | \
  openssl x509 -noout -dates

# Check certificate expiry for internal services
echo | openssl s_client -connect jira.technova.io:443 2>/dev/null | \
  openssl x509 -noout -enddate
```

TechnNova wildcard certificates (managed by Cloudflare and AWS ACM) auto-renew. If you see a cert expiry error, immediately post in `#it-help` — this is a SEV2 issue.

### Issue 5: GitHub Enterprise Unreachable

GHES is only accessible over VPN. Confirm:

```bash
# With VPN active
ssh -vT git@github.technova.io 2>&1 | grep -E "debug|Authentication"

# Check port 22 reachability
nc -vz github.technova.io 22
```

If SSH fails but HTTPS works, check your `~/.ssh/config` for the correct `IdentityFile`. See [GitHub Access](github-access.md).

---

## Advanced: EKS / Kubernetes Connectivity

For engineers troubleshooting pod-level network issues:

```bash
# Check pod network reachability
kubectl exec -it <pod-name> -n production -- curl -I https://api.technova.io

# Check DNS from inside pod
kubectl exec -it <pod-name> -n production -- nslookup kubernetes.default

# Check service endpoints
kubectl get endpoints -n production flowengine-api

# Describe NetworkPolicy if traffic is blocked
kubectl describe networkpolicy -n production
```

---

## Escalation Path

| Tier | Contact | When |
|------|---------|------|
| Tier 1 | `#it-help` Slack / support@technova.io | General connectivity, VPN, DNS |
| Tier 2 | `#eng-platform` Slack | AWS networking, EKS, Load Balancers |
| Tier 3 | SRE on-call via PagerDuty | Production outages, SEV1/SEV2 |

Response times per [Jira Workflow](jira-workflow.md) SLA definitions.

---

## FAQ

**Q: The VPN connects but I can't reach `jira.technova.io` specifically.**
A: Try flushing your DNS cache (`sudo dscacheutil -flushcache` on macOS) and reconnecting the VPN.

**Q: My MacBook shows "VPN Connected" in the menu bar but I can't reach internal resources.**
A: If you're using the macOS WireGuard app, verify the tunnel is routing traffic for the `10.0.0.0/8` subnet by checking the tunnel details in the app.

**Q: I'm in the London office and latency to US services is very high.**
A: This is expected for direct connections. The London office routes through the Cloudflare London PoP. If latency exceeds 300ms consistently, report to `#it-help`.

---

## Related Documents

- [VPN Setup Guide](vpn-setup-guide.md)
- [GitHub Access](github-access.md)
- [Incident Response](incident-response.md)
- [Monitoring & Alerting](monitoring-alerting.md)
