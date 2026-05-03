# Equipment Depreciation Policy

**TechNova Solutions | Finance Department**
**Document Owner:** David Park, CFO
**Last Updated:** January 1, 2025
**Version:** 1.7

---

## Overview

TechNova Solutions capitalizes and depreciates property and equipment in accordance with **US GAAP (ASC 360 — Property, Plant and Equipment)**. This policy defines capitalization thresholds, useful life schedules, depreciation methods, and disposal procedures for all fixed assets.

---

## Capitalization Threshold

Only assets meeting both criteria below are capitalized as fixed assets:

| Criterion | Threshold |
|---|---|
| Cost (individual unit) | $2,500 or more |
| Useful life | Greater than 12 months |

Assets below $2,500 are expensed in the period purchased, regardless of useful life. Group purchases of identical items (e.g., 10 monitors at $400 each = $4,000 total) follow the individual unit threshold, not the aggregate.

---

## Asset Categories and Useful Lives

TechNova Solutions uses **straight-line depreciation** for all asset categories:

| Asset Category | Useful Life | Residual Value | Examples |
|---|---|---|---|
| Computer equipment (laptops, desktops) | 3 years | $0 | MacBooks, Dell workstations |
| Servers and networking equipment | 5 years | $0 | Lab servers, Austin engineering hub racks |
| Office furniture | 7 years | $0 | Desks, chairs, conference tables |
| Leasehold improvements | Shorter of lease term or 10 years | $0 | SF HQ buildout, Austin hub renovations |
| Software (internally developed) | 3 years (post-launch) | $0 | Capitalized FlowEngine development costs |
| Test and lab equipment | 5 years | $0 | Hardware test benches |
| Audio/video equipment | 5 years | $0 | Conference room AV, webcams |

---

## Depreciation Method

All fixed assets are depreciated using the **straight-line method**:

```
Annual Depreciation = (Cost − Residual Value) / Useful Life
Monthly Depreciation = Annual Depreciation / 12
```

**Example:** A MacBook Pro purchased for $3,500 on March 1, 2025:
- Cost: $3,500 | Residual: $0 | Useful life: 3 years
- Annual depreciation: $1,167
- Monthly depreciation: $97.22
- Fully depreciated: March 1, 2028

Depreciation begins the month **after the asset is placed in service**.

---

## Asset Procurement and Tracking

1. All capital purchases require an approved [Purchase Requisition](purchase-requisition.md).
2. Upon receipt, Finance assigns an **Asset Tag** (sequential number, format: TNS-XXXXX) and records the asset in the NetSuite Fixed Asset Register with:
   - Asset tag, description, serial number
   - Cost, purchase date, vendor
   - Location (office / employee assigned)
   - Cost center code (see [Cost Center Codes](cost-center-codes.md))
   - Depreciation schedule
3. IT manages the physical asset tracking for computing equipment.
4. Finance reconciles the Fixed Asset Register to the balance sheet quarterly.

---

## Asset Disposal and Write-Offs

When an asset is retired, sold, or disposed of:

1. **Notify Finance** via the asset disposal form (Finance SharePoint).
2. Finance records:
   - Removal of asset cost and accumulated depreciation
   - Gain or loss on disposal (proceeds minus net book value)
3. Computers and electronics must be disposed of through TechNova's certified e-waste vendor per IT Security policy (data must be wiped before disposal).
4. Assets with a net book value over $5,000 require VP approval before disposal.

---

## Internally Developed Software (ASC 350-40)

TechNova capitalizes certain FlowEngine development costs under ASC 350-40:

| Phase | Treatment |
|---|---|
| Preliminary project stage | Expensed as R&D |
| Application development stage | Capitalized |
| Post-implementation/operations | Expensed |

The threshold for capitalizing development hours is **$10,000 per project phase**. Engineering management (Raj Patel, VP Engineering) works with Finance quarterly to identify capitalizable projects.

---

## Annual Physical Inventory

Finance conducts an annual physical inventory of all capitalized assets in **November** of each fiscal year to support the Deloitte external audit (see [Audit Procedures](audit-procedures.md)). Department heads are responsible for confirming the location and condition of assets assigned to their teams.
