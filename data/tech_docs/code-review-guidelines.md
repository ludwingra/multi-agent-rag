# Code Review Guidelines — TechNova Solutions

**Owner:** Engineering Excellence / VP Engineering | **Last Updated:** 2025-10-01 | **Applies To:** All Engineering Teams

---

## Overview

Code review is a core quality gate at TechNova Solutions. All changes to the FlowEngine codebase and supporting services must pass peer review before merging. This document defines reviewer responsibilities, approval requirements, and review etiquette.

For branch structure and PR creation, refer to [GitHub Access](github-access.md).

---

## Approval Requirements

| Target Branch | Minimum Approvals | Additional Requirements |
|---------------|-------------------|------------------------|
| `main` | **2** non-author approvals | At least 1 IC4+ or Manager |
| `develop` | **1** non-author approval | Any engineer |
| `feat/*`, `fix/*` | No requirement (open push) | Self-merge allowed after CI passes |
| `hotfix/*` | **2** approvals | Expedited; IC4+ or on-call SRE must be one |

Reviews must be **approved by humans**, not bypassed. Auto-merge is disabled on `main`.

---

## Author Responsibilities

Before requesting review, the PR author must:

1. **Self-review** the diff — catch typos, leftover debug code, and commented-out blocks.
2. **Write a meaningful PR description** covering:
   - **What** changed and **why**
   - Jira ticket link (e.g., `Closes FEC-421`)
   - Testing instructions or steps to verify
   - Any known risks or limitations
3. **Ensure CI is green** — do not request review on a failing build.
4. **Keep PRs small** — prefer < 400 lines changed. Large PRs should be split; discuss with your EM if uncertain.
5. **Respond to all comments** before merging — resolve or reply with acknowledgment.

```markdown
<!-- PR description template (stored at .github/pull_request_template.md) -->
## Summary
Brief description of what this PR does.

## Jira
Closes [FEC-XXX](https://jira.technova.io/browse/FEC-XXX)

## Changes
- Added retry logic with exponential backoff to webhook processor
- Updated `WebhookService` to accept `max_retries` parameter
- Added unit tests for retry boundary conditions

## Testing
1. Run `pytest tests/unit/test_webhook_service.py -v`
2. Trigger a failing webhook in staging and confirm retry logs in Datadog

## Risk
Low — feature-flagged behind `webhook_retry_enabled` (default: off)
```

---

## Reviewer Responsibilities

Reviewers should provide feedback within **1 business day** of being assigned.

### What to Review

| Category | Check |
|----------|-------|
| **Correctness** | Does the code do what the PR claims? Are edge cases handled? |
| **Tests** | Are tests meaningful? Do they cover the new/changed behavior? |
| **Security** | Are inputs validated? Are secrets handled properly? (See [Security Best Practices](security-best-practices.md)) |
| **Performance** | Any N+1 queries, missing indexes, unbounded loops? |
| **API contracts** | Are new endpoints documented per [API Documentation Standards](api-documentation-standards.md)? |
| **Style** | Does it follow the project's linting rules (Ruff / ESLint)? |
| **Maintainability** | Is the code readable? Are complex sections commented? |

### Comment Conventions

Use prefixes to signal urgency and type:

| Prefix | Meaning |
|--------|---------|
| `[blocking]` | Must be resolved before merge |
| `[nit]` | Minor style issue; author's discretion |
| `[question]` | Seeking clarification; not necessarily a change request |
| `[suggestion]` | Optional improvement idea |
| `[praise]` | Positive feedback — encouraged! |

Example:
```
[blocking] This Redis key has no TTL set — it will grow unbounded in production.
[nit] Consider renaming `tmp` to `pending_retries` for clarity.
[question] Why do we need the double-negation here?
```

---

## Review SLAs

| Urgency | SLA |
|---------|-----|
| Normal PR | 1 business day |
| Hotfix / SEV-linked | 2 hours |
| Blocking another engineer | Flag in `#engineering` Slack; escalate to EM if unresolved in 4 hours |

---

## Merge Guidelines

- **Squash and merge** for feature branches into `develop` — keeps history clean.
- **Merge commit** for `develop` into `main` (preserves merge history).
- Delete the feature branch after merge (GitHub auto-delete is enabled).
- Do not merge your own PR without the required approvals, even with bypassing rights.

---

## Automated Checks (Must Pass Before Review)

The CI pipeline enforces:
- Lint: `ruff check .` (Python) / `eslint .` (TypeScript)
- Tests: `pytest` / `jest --coverage`
- Type check: `mypy src/` / `tsc --noEmit`
- Secret scan: `detect-secrets scan`
- Coverage gate: ≥ 80% on changed files

See [CI/CD Pipeline](ci-cd-pipeline.md) for pipeline configuration.

---

## Related Documents

- [GitHub Access](github-access.md)
- [CI/CD Pipeline](ci-cd-pipeline.md)
- [API Documentation Standards](api-documentation-standards.md)
- [Security Best Practices](security-best-practices.md)
