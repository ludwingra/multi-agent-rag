# VPN Setup Guide — TechNova Solutions

**Owner:** IT Operations | **Last Updated:** 2025-10-15 | **Applies To:** All Employees

---

## Overview

TechNova Solutions uses a WireGuard-based VPN managed through the IT self-service portal at [vpn.technova.io](https://vpn.technova.io). The VPN is required to access internal services such as the engineering GitHub Enterprise instance, AWS management consoles, PostgreSQL/Redis admin panels, and Confluence.

All employees must authenticate via Okta SSO before downloading VPN credentials. See [Security Best Practices](security-best-practices.md) for guidance on credential storage.

---

## Prerequisites

- An active TechNova Okta account (`@technova.io`)
- A company-issued or approved personal device
- 1Password Teams installed (for storing the WireGuard private key)
- OS: macOS 13+, Ubuntu 22.04+, or Windows 11

---

## Installation

### macOS

```bash
# Install WireGuard via Homebrew
brew install wireguard-tools

# Alternatively, install the WireGuard GUI from the Mac App Store
# App name: WireGuard
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install wireguard resolvconf -y
```

### Windows

Download and install the official WireGuard client from [wireguard.com/install](https://www.wireguard.com/install/).

---

## Configuration

1. Navigate to [vpn.technova.io](https://vpn.technova.io) and log in with your Okta credentials.
2. Click **Generate Config** → **Download `technova-vpn.conf`**.
3. Store the `.conf` file securely in 1Password before importing.

### Import on macOS / Linux

```bash
sudo cp ~/Downloads/technova-vpn.conf /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf

# Start VPN
sudo wg-quick up wg0

# Enable on boot
sudo systemctl enable wg-quick@wg0
```

### Import on Windows

Open the WireGuard client → **Add Tunnel** → **Import from file** → select `technova-vpn.conf`.

---

## Verification

```bash
# Confirm the tunnel is active
sudo wg show

# Test internal network access
curl -I https://confluence.internal.technova.io
```

Expected: `HTTP/2 200` from the Confluence internal URL.

---

## Disconnecting

```bash
sudo wg-quick down wg0
```

---

## Key Rotation

VPN credentials expire every **90 days**. You will receive a Slack notification in `#it-announcements` 7 days before expiry. Re-visit [vpn.technova.io](https://vpn.technova.io) to generate a fresh config and update your 1Password entry.

---

## FAQ

**Q: I can't reach the VPN portal — what should I do?**
A: Ensure you are not blocking DNS-over-HTTPS on your router. Try using `8.8.8.8` as a fallback resolver.

**Q: My tunnel connects but internal sites are unreachable.**
A: Run `sudo wg show` and verify the `latest handshake` timestamp is within the last 3 minutes. If not, restart: `sudo wg-quick down wg0 && sudo wg-quick up wg0`.

**Q: Can I use the VPN on a personal device?**
A: Yes, provided the device meets the MDM enrollment requirements listed at [it.technova.io/mdm](https://it.technova.io/mdm).

**Q: Who do I contact for VPN issues?**
A: Email support@technova.io or post in `#it-help` on Slack. See [IT Support tiers](https://it.technova.io/support-tiers).

---

## Related Documents

- [Security Best Practices](security-best-practices.md)
- [Laptop Setup Guide](laptop-setup.md)
- [Network Troubleshooting](network-troubleshooting.md)
