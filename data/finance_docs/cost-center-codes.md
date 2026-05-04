# Cost Center Codes

**TechNova Solutions | Finance Department**
**Document Owner:** David Park, CFO
**Last Updated:** January 1, 2025
**Version:** 3.0

---

## Overview

TechNova Solutions uses a standardized cost center code system to categorize all operating expenses in NetSuite ERP. Every expense report, purchase order, invoice, and subscription entry must include the correct cost center code. Accurate cost center coding is essential for budget tracking, financial reporting, and the annual Deloitte audit.

---

## Primary Cost Centers

| Code | Name | Description | VP Owner |
|---|---|---|---|
| ENG | Engineering | Software development, QA, infrastructure, security | Raj Patel |
| SAL | Sales | Account executives, sales operations, SDRs | VP Sales |
| MKT | Marketing | Demand gen, brand, content, events, PR | VP Marketing |
| GNA | General & Administrative | Finance, HR, Legal, Executive, IT | David Park (CFO) |
| OPS | Operations | Customer success, support, implementations | VP Operations |
| RND | Research & Development | Applied R&D, product innovation, AI/ML research | Marcus Rivera (CTO) |

---

## Sub-Cost Centers

For more granular tracking, sub-cost centers are used within primary codes:

| Code | Sub-Code | Name | Description |
|---|---|---|---|
| ENG | ENG-FE | Frontend Engineering | FlowEngine UI/UX development |
| ENG | ENG-BE | Backend Engineering | FlowEngine API and platform services |
| ENG | ENG-INFRA | Infrastructure | AWS/GCP, DevOps, SRE |
| ENG | ENG-SEC | Security | Application security, compliance tooling |
| SAL | SAL-SMB | SMB Sales | Small-mid business segment |
| SAL | SAL-ENT | Enterprise Sales | Enterprise accounts >$100K ARR |
| SAL | SAL-OPS | Sales Operations | RevOps, Salesforce admin |
| MKT | MKT-DEM | Demand Generation | Paid media, SEO, SEM |
| MKT | MKT-EVT | Events | Conferences, webinars, FlowEngine Summit |
| GNA | GNA-FIN | Finance | Accounting, FP&A |
| GNA | GNA-HR | Human Resources | Recruiting, HR ops, L&D |
| GNA | GNA-LEG | Legal | External counsel, contracts |
| OPS | OPS-CS | Customer Success | CSMs, onboarding team |
| OPS | OPS-SUP | Support | Technical support (Toronto center) |
| RND | RND-AI | AI Research | ML model development for FlowEngine AI |

---

## Office / Geography Codes

Expenses can also be tagged with an office suffix when location-specific tracking is needed:

| Suffix | Location |
|---|---|
| -SF | San Francisco, CA (HQ) |
| -AUS | Austin, TX (Engineering Hub) |
| -LON | London, UK (Sales Office — TechNova Solutions Ltd) |
| -TOR | Toronto, Canada (Support Center) |
| -REM | Remote (no fixed office) |

**Example full code:** `ENG-BE-SF` = Backend Engineering, San Francisco office

---

## How to Use Cost Center Codes

1. **Expense Reports (Expensify):** Select the cost center from the dropdown when creating an expense report. Match to your department and activity.
2. **Purchase Requisitions:** Enter the cost center code in the Finance portal PR form.
3. **Invoices (Bill.com):** Finance codes all AP invoices during the three-way match process.
4. **Payroll (Gusto):** Headcount is mapped to cost centers in Gusto by HR. Changes require HR + Finance approval.

---

## Coding Rules and Common Mistakes

| Rule | Detail |
|---|---|
| Use the most specific sub-code | Use `ENG-INFRA` for AWS costs, not just `ENG` |
| Don't code to GNA by default | GNA is only for Finance/HR/Legal/Exec spend |
| Cross-department projects | Split proportionally; use primary beneficiary if 80%+ |
| Shared services | IT infrastructure shared across engineering: use `ENG-INFRA` |
| Recruiting expenses | Always `GNA-HR` regardless of which team is being hired |

---

## Code Updates and New Requests

To request a new sub-cost center code, submit a request to finance@technova.com with:
- Business justification
- Estimated annual spend
- Reporting requirements

New codes take effect at the start of the next fiscal quarter and must be approved by the CFO.

Refer to [Budget Allocation](budget-allocation.md) for how budgets are planned per cost center and [Financial Reporting](financial-reporting.md) for how cost center data feeds into management reports.
