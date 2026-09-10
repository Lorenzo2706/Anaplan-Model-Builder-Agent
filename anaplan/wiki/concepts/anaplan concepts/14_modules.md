---
title: Modules
type: concept
tags: [anaplan, modules, blueprint, configuration, cell-count, breakback]
created: 2026-05-13
updated: 2026-09-09
sources:
  - raw/docs/Configure modules.md
  - raw/docs/Breakback  Anapedia.md
---

# Modules

A **module** is the fundamental calculation and storage unit in an Anaplan model. It is a multi-dimensional grid whose axes are defined by [[Dimensions|dimensions]] (lists, time, versions, users, line item subsets) and whose cells are defined by [[Line Item|line items]]. All data storage, formula evaluation, and user input happens inside modules.

Modules are created and configured in **Model Settings > Modules**. Structural properties (dimensions, line item metadata) live in **Blueprint view** within the module itself.

---

## Module Settings Columns (Model Settings > Modules)

| Column | What it controls | Key notes |
|---|---|---|
| **Functional Area** | Grouping/categorization label | Use to implement [[DISCO — Module Classification]] classification (Data, Inputs, System, Calculations, Outputs) or business domain groupings |
| **Applies To** | The list dimensions for the module | Accepts lists, list subsets, the Users list, or a [[Line Item Subsets (LIS)\|line item subset]] (max one LIS) |
| **Time Scale** | Granularity of the Time dimension | Options: DAY, WEEK, MONTH, QUARTER, YEAR, Not Applicable. Changing time scale does not cascade to individual line item time scales |
| **Time Range** | Restricts visible/enterable time periods | Useful to cap memory for limited-period modules |
| **Versions** | All versions or no versions | Binary choice; version-level control happens at line item level in Blueprint |
| **Breakback** | Default breakback setting for new line items | See [Breakback](#breakback) below |
| **Cell Count** | Read-only; calculated cell count | See [Cell Count Calculation](#cell-count-calculation) below |
| **Notes** | Free-text annotation field | — |
| **Read Access Driver** | Boolean line item controlling read access | See [[Access Drivers]] |
| **Write Access Driver** | Boolean line item controlling write access | See [[Access Drivers]] |
| **Data Tags** | Group related data across modules | See [[Data Tags]] |
| **Referenced By** | Shows inbound references from other modules/line items | Format: `module name.line item name` |
| **Used in Dashboards** | Lists dashboards referencing this module | — |
| **Line Items** | Count of line items in the module | — |

---

## Cell Count Calculation

**Cell Count** (read-only in Modules settings) is the product of all dimension cardinalities summed across every line item.

Factors that increase cell count:
- Higher time scale granularity (DAY > WEEK > MONTH > QUARTER > YEAR)
- Longer time range
- More versions
- Larger lists / more list hierarchy levels (summary rows add cells)
- More line items with non-None summary methods

> [!warning]
> DAY time scale over multi-year ranges can produce cell counts large enough to exceed model memory limits even if overall workspace size is within quota. If daily granularity is required, restrict it with a Time Range and avoid `CUMULATE()` over long horizons.

Cell count is the primary driver of model memory. Compare module designs using cell count before committing.

---

## Breakback

**Breakback** allows users to enter a value at a summary level (e.g. a quarterly total) and have Anaplan distribute it to the detail periods (e.g. constituent months).

The **Breakback** column in Modules sets the **default** for new line items. Individual line items can override this in Blueprint.

| Breakback Setting | Behavior |
|---|---|
| **Enabled** | User entry at summary level is distributed proportionally (or equally if all zeros) down to leaf cells |
| **Disabled** | Summary level is read-only; only leaf-level input is accepted |

**Use breakback when:** planners think in quarterly or annual targets and want Anaplan to spread them (e.g. headcount or budget entry at an annual level with monthly spreading).

**Avoid breakback when:** line items are calculated (formula-driven), use AVERAGE/MAX/MIN/FORMULA/NONE as their summary method, or the module is an Output or Calculation module per DISCO.

> [!warning]
> Breakback only works when the summary method is **SUM**. It has no effect on other summary methods.

**Hold** is a Breakback feature that temporarily "holds" a cell's value during a Breakback distribution — use it to update totals without impacting one line item's value, or to change one line item's value without changing the overall total. Cells are also held automatically at their previous value when they're read-only for another reason (Selective Access, Dynamic Cell Access, or historical months in a rolling forecast) — Breakback skips them and redistributes across the remaining writable cells.

Further constraints:

- Breakback is restricted to totals on **simple hierarchies and the time dimension only** — it isn't permitted across several line items.
- If leaf-level cells that don't already sum to zero are all zero at a summary level, entering a value there produces an **error**, not a proportional distribution (proportional/pro-rata spreading requires a non-zero basis to spread against; an all-zero basis with a non-zero total is only handled in the "evenly across leaf cells" case described above).
- If a Breakback action affects more than **1,000,000 cells**, Anaplan displays a warning message before applying it.
- Because Breakback can touch many cells at once, a module's **change history** only records the cell change that originally triggered it, plus the total count of affected cells — not each individual affected cell.

(see [[../../sources/2026-09-09-anapedia-breakback|2026-09-09 Anapedia Breakback ingest]])

---

## Module Settings vs Blueprint

| Property | Where it lives |
|---|---|
| Dimensions (Applies To, Time Scale, Time Range, Versions) | Module Settings |
| Functional Area, Access Drivers, Data Tags, Cell Count | Module Settings |
| Breakback default | Module Settings (overridable per line item in Blueprint) |
| Line item data type, formula, summary method | Blueprint |
| Line item time scale override | Blueprint |
| Line item format / style | Blueprint |

Blueprint is the per-line-item configuration layer; Modules settings is the module-level structural layer.

---

## Module Classification: DISCO

The **Functional Area** column is where [[DISCO — Module Classification]] classification is encoded:

| DISCO Category | Typical Settings |
|---|---|
| **D — Data** | No Time / No Versions; Applies To = master list(s) |
| **I — Inputs** | Time + Versions; Breakback may be On; Write Access Driver often set |
| **S — System** | Minimal dimensions; often no Time; admin-only or read-only |
| **C — Calculations** | Time + Versions; Breakback Off; no direct user input; Write Access Driver = FALSE |
| **O — Outputs** | Time + Versions; Write Access Driver = FALSE; Read Access Driver may restrict |

---

## Related

- [[Line Item]] — line items are the members of a module's Blueprint
- [[Dimensions]] — lists, time, versions, users, and LIS are all dimension types
- [[Line Item Subsets (LIS)]] — LIS can be assigned via Applies To (one per module)
- [[Access Drivers]] — Read/Write Access Drivers use Boolean line items in Blueprint
- [[Data Tags]] — tag modules for discoverability
- [[DISCO — Module Classification]] — framework for classifying modules by function
