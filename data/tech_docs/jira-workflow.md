# Jira Workflow Guide — TechNova Solutions

**Owner:** Engineering Operations | **Last Updated:** 2025-09-15 | **Applies To:** All Engineering and Product Teams

---

## Overview

TechNova Solutions uses **Jira Software Cloud** (hosted at [jira.technova.io](https://jira.technova.io)) as its primary project management and issue tracking tool. This guide covers ticket creation, workflow states, sprint ceremonies, and integration with GitHub Enterprise.

---

## Projects and Keys

| Project | Key | Team |
|---------|-----|------|
| FlowEngine Core | `FEC` | Backend Platform |
| FlowEngine Frontend | `FEF` | Frontend Engineering |
| Infrastructure | `INFRA` | DevOps / Platform |
| IT Operations | `IT` | IT Support |
| Security | `SEC` | Security Team |
| Data & Analytics | `DATA` | Data Engineering |

---

## Issue Types

| Type | When to Use |
|------|------------|
| **Story** | New user-facing feature or enhancement |
| **Bug** | Defect in existing functionality |
| **Task** | Internal work item (migration, infra, docs) |
| **Sub-task** | Breakdown of a parent Story or Task |
| **Epic** | Large initiative spanning multiple sprints |
| **Incident** | Linked to a PagerDuty alert (SEV1–SEV4) |

---

## Ticket Workflow States

```
Backlog → To Do → In Progress → In Review → QA → Done
                                   ↑
                            (Blocked — add blocker link)
```

| State | Description |
|-------|------------|
| **Backlog** | Not yet scheduled for a sprint |
| **To Do** | Sprint-committed, not started |
| **In Progress** | Actively being worked; assign to yourself |
| **In Review** | PR open; awaiting code review (see [Code Review Guidelines](code-review-guidelines.md)) |
| **QA** | Deployed to staging; awaiting QA sign-off |
| **Done** | Accepted and merged; Sprint Velocity counted |

---

## Creating a Ticket

1. Navigate to [jira.technova.io](https://jira.technova.io) → select the relevant project.
2. Click **Create** (keyboard shortcut `C`).
3. Fill in:
   - **Summary**: `[COMPONENT] Short description` (e.g., `[Auth] Fix token refresh race condition`)
   - **Type**: Select appropriate issue type.
   - **Priority**: Critical / High / Medium / Low.
   - **Labels**: `backend`, `frontend`, `infra`, `security`, `tech-debt` — add all applicable.
   - **Epic Link**: Link to the parent Epic if applicable.
   - **Story Points**: Estimate using Fibonacci scale (1, 2, 3, 5, 8, 13).
4. Assign to yourself or leave unassigned for backlog grooming.

---

## Branch and Commit Naming Convention

Jira integrates with GitHub to track branches and commits. Use the ticket key in branch names and commit messages:

```bash
# Branch naming
git checkout -b feat/FEC-421-implement-webhook-retry

# Commit message (Conventional Commits + Jira key)
git commit -m "feat(webhooks): implement retry with exponential backoff [FEC-421]"
```

Including the Jira key auto-links the commit and PR to the Jira ticket.

---

## Sprint Ceremonies

| Ceremony | Cadence | Duration | Owner |
|----------|---------|----------|-------|
| Sprint Planning | Every 2 weeks (Monday) | 2 hours | Engineering Manager |
| Daily Standup | Daily (async in Slack `#standup-[team]`) | 15 min | Team |
| Sprint Review | Every 2 weeks (Friday) | 1 hour | Product Manager |
| Sprint Retrospective | Every 2 weeks (Friday) | 1 hour | Scrum Master |
| Backlog Grooming | Weekly (Wednesday) | 1 hour | PM + EM |

---

## Jira + PagerDuty Integration

SEV1 and SEV2 incidents triggered in PagerDuty automatically create Jira tickets in the **SEC** or **INFRA** project with issue type **Incident**. See [Incident Response](incident-response.md) for triage and escalation steps.

---

## Jira + Slack Integration

Jira Cloud is integrated with Slack. Mention a ticket key (e.g., `FEC-421`) in any Slack channel to get an inline preview. Subscribe to project updates in `#jira-notifications`.

---

## FAQ

**Q: How do I move a ticket to "In Review"?**
A: Open the PR in GitHub with the Jira ticket key in the PR title or description. Jira will automatically transition the ticket to **In Review** if the Smart Commits integration is enabled.

**Q: What story point scale do we use?**
A: Fibonacci (1, 2, 3, 5, 8, 13, 21). Anything estimated at 21 should be split before sprint commitment.

**Q: Who manages sprint boards?**
A: Engineering Managers (M1–M3) own their team's sprint boards. Raise configuration requests in `#engineering-ops`.

---

## Related Documents

- [Code Review Guidelines](code-review-guidelines.md)
- [Incident Response](incident-response.md)
- [Slack Guidelines](slack-guidelines.md)
- [GitHub Access](github-access.md)
