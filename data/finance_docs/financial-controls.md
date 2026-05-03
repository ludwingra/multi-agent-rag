# Financial Controls Policy

**TechNova Solutions | Finance Department**
**Document Owner:** David Park, CFO
**Last Updated:** January 1, 2025
**Version:** 2.4

---

## Overview

TechNova Solutions maintains a robust internal control environment to safeguard company assets, ensure the accuracy of financial records, and prevent fraud. This policy defines the key financial controls applied across the organization and assigns responsibility for their operation and monitoring. The controls described here are reviewed annually by Deloitte as part of the external audit (see [Audit Procedures](audit-procedures.md)).

---

## Control Framework

TechNova's financial controls are structured around the **COSO Internal Control Framework** with five components:

| Component | Description |
|---|---|
| Control Environment | Tone set by CFO and leadership; clear accountability structures |
| Risk Assessment | Quarterly Finance risk register reviewed by CFO and CEO |
| Control Activities | Specific preventive and detective controls (see below) |
| Information & Communication | NetSuite, Bill.com, Gusto, Expensify integration; audit trails |
| Monitoring | Internal reviews, Deloitte audit, surprise petty cash counts |

---

## Preventive Controls

These controls are designed to prevent errors or fraud before they occur:

| Control | Description | Tool / Method |
|---|---|---|
| Segregation of Duties | PR approver ≠ payment approver; payroll entry ≠ payroll approval | NetSuite, Bill.com roles |
| Dual approval for large wires | Transfers >$50,000 require 2 Finance signatories | SVB wire portal |
| Approval thresholds | Tiered spending authority (see below) | NetSuite, Expensify, Bill.com |
| Vendor onboarding | W-9/W-8 + ACH verification before first payment | Bill.com vendor portal |
| Corporate card limits | Per-role monthly limits enforced at card level | Brex |
| PO requirement | All purchases >$500 require a PO before commitment | NetSuite |
| Budget checks | NetSuite blocks POs that exceed available budget (configurable) | NetSuite |

---

## Spending Authority Matrix

| Transaction Type | <$500 | $500–$4,999 | $5,000–$24,999 | $25,000+ |
|---|---|---|---|---|
| Expense reimbursement | Manager | Director | VP | CFO |
| Purchase orders | Manager | Director | VP | CFO |
| Vendor invoices | Auto (contracted) | Director | VP | CFO |
| Wire transfers | — | — | VP | CFO (dual sign >$50K) |
| Contract execution | — | Director | VP | CFO + Legal |

---

## Detective Controls

These controls identify errors or irregularities after they occur:

| Control | Frequency | Owner |
|---|---|---|
| Bank reconciliation (SVB + Mercury) | Monthly (Day 3) | Finance Controller |
| Accounts receivable aging review | Monthly (Day 5) | Finance Analyst |
| Accounts payable aging review | Weekly | AP Manager |
| Expense report audit (10% sample) | Quarterly | Finance Controller |
| Corporate card transaction review | Monthly | Finance Analyst |
| Subscription registry reconciliation | Quarterly | IT + Finance |
| Fixed asset physical inventory | Annual (November) | Finance Controller |
| Journal entry review | Monthly (all manual JEs >$10K require Controller sign-off) | Finance Controller |
| Payroll variance analysis | Per payroll cycle | Finance Analyst |

---

## IT / System Access Controls

- **Role-based access in NetSuite:** Least-privilege model; access reviewed quarterly and on any role change.
- **Terminated employee access:** Revoked within **24 hours** of offboarding in coordination with IT and HR.
- **NetSuite audit trail:** All financial transactions include user ID, timestamp, and IP address. Cannot be altered without leaving a trace.
- **Expensify / Bill.com SSO:** All Finance tools use TechNova's Okta SSO. No local passwords for Finance systems.
- **Detect-secrets:** Applied to any code or config containing financial API keys (Stripe, Brex, NetSuite).

---

## Segregation of Duties — Key Pairs

The following role combinations are **explicitly prohibited** (same individual cannot hold both roles):

| Role A | Role B |
|---|---|
| Purchase requisition submitter | Purchase requisition approver |
| Vendor setup in Bill.com | Invoice payment approval |
| Payroll data entry in Gusto | Payroll run approval |
| Expense report submitter | Expense report approver (own reports) |
| Revenue entry in NetSuite | AR reconciliation |

---

## Control Exceptions and Waivers

In rare cases, a control may need to be temporarily waived (e.g., sole Finance employee during a hiring gap). Exceptions must be:

1. Documented in writing with business justification
2. Approved by the CFO
3. Time-limited (maximum 90 days)
4. Compensating controls put in place (e.g., CFO reviews all transactions in the affected area)
5. Reported to the Audit Committee at the next Board meeting

---

## Fraud Response

Suspected fraud must be reported immediately to the CFO or via the anonymous ethics hotline (1-800-TNS-SAFE). Finance will initiate an investigation in coordination with Legal and, if warranted, external forensic accountants. See [Audit Procedures](audit-procedures.md) for the full whistleblower and fraud reporting process.

---

## FAQ

**Q: What happens if I accidentally approve something I shouldn't have?**
A: Notify Finance immediately at finance@technova.com. The sooner errors are caught, the easier they are to reverse. Accidental approvals do not carry disciplinary consequences if reported promptly.

**Q: How does TechNova prevent duplicate payments?**
A: Bill.com automatically flags duplicate invoice numbers from the same vendor. Finance also runs a weekly duplicate payment check in NetSuite using the AP aging report.

**Q: Are controls different for the UK subsidiary?**
A: TechNova Solutions Ltd follows the same core controls. UK-specific controls (VAT reconciliation, PAYE verification) are managed by Mazars LLP under the oversight of the CFO.
