# Laptop Setup Guide — TechNova Solutions

**Owner:** IT Operations | **Last Updated:** 2025-10-01 | **Applies To:** All New Employees

---

## Overview

Welcome to TechNova Solutions! This guide walks you through setting up your company-issued MacBook (standard for all employees) or Linux workstation (available on request for engineers). Complete this setup on your first day before accessing any internal resources.

If you encounter issues, contact IT via `#it-help` on Slack or email support@technova.io.

---

## Step 1 — Unbox and Power On

1. Power on the device. For macOS, complete initial setup (language, Apple ID: **skip for now**, Wi-Fi setup).
2. Log in with the **local admin credentials** provided in your onboarding 1Password vault entry (shared by IT before day one).

---

## Step 2 — Enroll in MDM (Jamf Pro)

MDM enrollment is required before accessing any TechNova corporate systems.

1. Open Safari and navigate to [mdm.technova.io/enroll](https://mdm.technova.io/enroll).
2. Log in with your Okta credentials (`firstname.lastname@technova.io`).
3. Follow the prompts to download and install the **Jamf MDM profile**.
4. Enrollment completes automatically; Jamf will push standard apps (1Password, CrowdStrike, Slack, Zoom) within **15 minutes**.

---

## Step 3 — Enable FileVault Encryption

```bash
# Verify FileVault status (MDM may have enabled it; check first)
fdesetup status
# If output is "FileVault is On." — skip this step.

# Enable manually if needed
sudo fdesetup enable
# Store the recovery key in 1Password immediately
```

---

## Step 4 — Install Core Tools

### Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (Apple Silicon Macs)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Developer Essentials

```bash
brew install git gh awscli kubectl helm terraform python@3.12 node@20 \
             wireguard-tools jq yq fzf ripgrep direnv

# Install nvm for Node version management
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20 && nvm use 20 && nvm alias default 20

# Install pyenv for Python version management
brew install pyenv
echo 'eval "$(pyenv init -)"' >> ~/.zprofile
pyenv install 3.12.4 && pyenv global 3.12.4
```

### Docker Desktop

```bash
brew install --cask docker
# Open Docker Desktop from Applications to complete setup
docker --version  # Verify: Docker version 26.x.x
```

---

## Step 5 — Configure VPN

Set up the TechNova WireGuard VPN before accessing internal tools. Follow the complete [VPN Setup Guide](vpn-setup-guide.md).

---

## Step 6 — Configure Git and SSH

```bash
# Global Git identity
git config --global user.name "Firstname Lastname"
git config --global user.email "firstname.lastname@technova.io"
git config --global init.defaultBranch main
git config --global commit.gpgsign true

# Generate SSH key for GitHub Enterprise
ssh-keygen -t ed25519 -C "firstname.lastname@technova.io" -f ~/.ssh/technova_github
```

Add the public key to GitHub Enterprise per [GitHub Access Guide](github-access.md).

---

## Step 7 — Install 1Password CLI

```bash
brew install 1password-cli
op signin --account technova
# Authenticate with your Okta credentials + MFA
```

---

## Step 8 — Configure AWS CLI

Follow the [AWS Access Request Guide](aws-access-request.md) to configure AWS SSO profiles.

---

## Step 9 — IDE Setup

### VS Code (Recommended)

```bash
brew install --cask visual-studio-code

# Install recommended extensions
code --install-extension ms-python.python
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension hashicorp.terraform
```

VS Code settings sync is available via your `@technova.io` Google account.

---

## FAQ

**Q: My MacBook isn't prompting for MDM enrollment.**
A: Navigate directly to [mdm.technova.io/enroll](https://mdm.technova.io/enroll). If that fails, restart the device and try again. Contact `#it-help` if the issue persists.

**Q: Can I install applications not in the approved list?**
A: Yes, via Homebrew or direct download for standard tools. IT must approve any tool that processes customer data. Submit a request via Jira in the **IT** project.

**Q: Homebrew is slow/failing on Apple Silicon.**
A: Ensure Rosetta 2 is installed: `softwareupdate --install-rosetta --agree-to-license`.

---

## Related Documents

- [VPN Setup Guide](vpn-setup-guide.md)
- [GitHub Access](github-access.md)
- [AWS Access Request](aws-access-request.md)
- [Dev Environment Setup](dev-environment-setup.md)
- [Security Best Practices](security-best-practices.md)
