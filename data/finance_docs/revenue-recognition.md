# Revenue Recognition Policy

**TechNova Solutions | Finance Department**
**Document Owner:** David Park, CFO
**Last Updated:** January 1, 2025
**Version:** 2.3

---

## Overview

TechNova Solutions recognizes revenue in accordance with **ASC 606 — Revenue from Contracts with Customers**. This standard requires that revenue be recognized when (or as) the company satisfies performance obligations by transferring promised goods or services to customers. This policy applies to all revenue streams derived from the FlowEngine platform.

---

## Revenue Streams

| Stream | Description | Recognition Method |
|---|---|---|
| SaaS Subscription — FlowEngine | Recurring annual or monthly licenses | Ratably over subscription term |
| Professional Services — Onboarding | Customer onboarding and implementation | Over the onboarding period (typically 30–90 days) |
| Professional Services — Training | FlowEngine training workshops | At time of delivery |
| Usage-Based Fees | API calls and workflow automations above plan limits | As usage occurs (monthly) |
| Partner Referral Commissions | Revenue share from integration partners | At time of partner-attributed close |

---

## Five-Step ASC 606 Framework Applied to FlowEngine

### Step 1 — Identify the Contract
Contracts are fully executed MSAs and Order Forms signed by both parties. Verbal commitments and emails are not contracts. Finance reviews all executed agreements via the deal desk.

### Step 2 — Identify Performance Obligations
Each FlowEngine contract may contain multiple distinct performance obligations (POs):
- **PO1:** SaaS platform access (FlowEngine subscription)
- **PO2:** Onboarding and implementation services
- **PO3:** Training (if separately priced)

### Step 3 — Determine the Transaction Price
Transaction price is the contract value, net of:
- Volume discounts
- Variable consideration estimates (usage overages, refund reserves)
- Contra-revenue items (coupons, credits issued to customers)

### Step 4 — Allocate the Transaction Price
Where multiple POs exist, the total transaction price is allocated based on **Standalone Selling Prices (SSPs)**. Finance maintains an SSP study, updated annually by the CFO and reviewed by Deloitte.

| Component | SSP (FY2025) |
|---|---|
| FlowEngine subscription (per seat, per year) | $1,200 |
| Onboarding (standard) | $8,000 |
| Onboarding (enterprise) | $25,000 |
| Training workshop (per session) | $2,500 |

### Step 5 — Recognize Revenue
Revenue is recognized as performance obligations are satisfied:
- **Subscription:** Ratably, month by month, over the contract term. A 12-month $60,000 annual contract = $5,000/month recognized.
- **Onboarding:** On a percentage-of-completion basis based on milestones (e.g., data migration complete, go-live confirmed).
- **Training:** On the date the session is delivered.

---

## Deferred Revenue and Unbilled AR

- **Deferred Revenue (Contract Liability):** When customers pay upfront (annual prepay via Stripe), cash is received before revenue is earned. The unearned portion is recorded as Deferred Revenue on the balance sheet and recognized over the subscription term.
- **Unbilled AR (Contract Asset):** When TechNova has earned revenue but has not yet invoiced the customer (e.g., multi-year ramp deals), the earned-but-not-billed amount is recorded as an Unbilled AR contract asset.

Finance reconciles Deferred Revenue and Unbilled AR monthly using Stripe billing data imported into NetSuite.

---

## Contract Modifications

Changes to existing FlowEngine contracts (upgrades, downgrades, add-ons) are treated as:
- **Prospective modification** if adding new distinct POs at SSP
- **Cumulative catch-up** if modifying an existing PO

All contract modifications must be reviewed by Finance before the change is reflected in billing (Stripe) or the revenue schedule (NetSuite).

---

## ARR and Bookings Metrics

While ARR (Annual Recurring Revenue) is the primary business metric used in [Financial Reporting](financial-reporting.md), it is a **non-GAAP** metric. Finance maintains a reconciliation between GAAP revenue and ARR in the monthly Board Package.

---

## Audit and Controls

Revenue recognition schedules are reviewed quarterly by the internal Finance team and annually by Deloitte as part of the [Audit Procedures](audit-procedures.md). The Controller maintains a complete listing of all active contracts and their revenue schedules in NetSuite's Revenue Management module.
