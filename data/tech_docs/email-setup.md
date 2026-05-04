# Email Setup Guide — TechNova Solutions

**Owner:** IT Operations | **Last Updated:** 2025-08-20 | **Applies To:** All Employees

---

## Overview

TechNova Solutions uses **Google Workspace (Business Plus)** for corporate email. Your company email address follows the format `firstname.lastname@technova.io`. Email provisioning is handled automatically on your first day; credentials are delivered via your manager or the IT onboarding bot in Slack (`@it-bot`).

---

## Accessing Your Email

### Web (Browser)

Navigate to [mail.google.com](https://mail.google.com) and sign in with your `@technova.io` account. You will be redirected through **Okta SSO** — no separate Google password is required.

### Gmail Desktop (macOS — Recommended)

```bash
# Download via direct link or Homebrew
brew install --cask google-chrome

# Or use the standalone macOS Mail app configured below
```

### Apple Mail (macOS)

1. Open **Mail** → **Preferences** → **Accounts** → **+**
2. Select **Google**.
3. Enter your `@technova.io` address; authenticate via the Okta SSO browser pop-up.
4. Recommended sync settings: **All Mail**, **Sent**, **Drafts**.

### Outlook (Windows)

1. Open Outlook → **File** → **Add Account**.
2. Enter your `@technova.io` email; choose **Sign in with Google**.
3. Complete Okta MFA challenge.

---

## Email Signature

All TechNova employees must use the approved signature template. Configure it in Gmail under **Settings** → **See all settings** → **General** → **Signature**:

```
Firstname Lastname
Job Title | TechNova Solutions
firstname.lastname@technova.io | +1 (415) 555-XXXX
technova.io | LinkedIn
```

The official logo asset is available at [brand.technova.io/assets/email-signature](https://brand.technova.io/assets/email-signature).

---

## Distribution Lists and Aliases

| Alias | Purpose |
|-------|---------|
| engineering@technova.io | All engineering staff |
| security@technova.io | Security team alerts |
| support@technova.io | IT and product support (external-facing) |
| all-hands@technova.io | Company-wide communications (exec use only) |

To request a new alias or add yourself to a DL, file a Jira ticket in the **IT** project using the **Email/Alias Request** template. See [Jira Workflow](jira-workflow.md) for ticket creation instructions.

---

## Mobile Email Setup (iOS / Android)

1. Install the **Gmail** app from the App Store or Google Play.
2. Tap **Add Account** → **Google** → enter your `@technova.io` address.
3. Complete Okta SSO authentication.
4. Enable **Push Notifications** for prompt delivery of security alerts.

Note: Mobile devices accessing company email must be enrolled in MDM (see [Laptop Setup Guide](laptop-setup.md) for MDM instructions — mobile enrollment process is identical).

---

## Email Retention and Archiving

- Email is retained for **7 years** per TechNova's data retention policy.
- Automatic archiving is enabled; items older than 2 years are moved to **All Mail** archive.
- Mailbox quota: **30 GB** per user. Contact IT if you approach the limit.

---

## Security Guidelines

- Never share your Google Workspace password. Okta SSO eliminates the need to know it.
- Do not forward corporate email to personal accounts.
- Phishing attempts should be reported using the **Report Phishing** button (Gmail → three-dot menu → **Report phishing**) and forwarded to security@technova.io.

See [Security Best Practices](security-best-practices.md) for full email security guidance.

---

## FAQ

**Q: I can't log in — Okta says my account is locked.**
A: Contact IT via `#it-help` on Slack or email support@technova.io. Okta accounts are locked after 5 failed attempts.

**Q: Can I use a personal Gmail account for work tasks?**
A: No. All work communications must remain within `@technova.io` accounts.

**Q: How do I set up a vacation auto-reply?**
A: Gmail → **Settings** → **Vacation responder** → enable and set dates.

---

## Related Documents

- [Security Best Practices](security-best-practices.md)
- [Slack Guidelines](slack-guidelines.md)
- [Laptop Setup Guide](laptop-setup.md)
- [Jira Workflow](jira-workflow.md)
