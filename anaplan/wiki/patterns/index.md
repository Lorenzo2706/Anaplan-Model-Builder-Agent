---
title: Patterns — Index
type: pattern
tags: [anaplan, index, patterns, best-practices, methodology]
created: 2026-05-27
updated: 2026-09-11
---

# Patterns — Index

Design patterns, best practices, and implementation methodologies for Anaplan model building. 8 standalone pages + 2 sub-collections (15 sub-pages total).

> [!note] Customer-specific naming conventions (e.g. a customer's internal Lists/Modules/Line Items/Actions/Dashboards naming standard) live in that customer's own wiki under `customers/<Name>/wiki/patterns/`, not here.

---

## Standalone Patterns

| Page | File | Summary |
|------|------|---------|
| [[Circular Reference — Patterns & Workarounds\|Circular Reference]] | `circular-reference.md` | Root causes + three workarounds: DAG restructure, Fake Time list, SYS LOOKUP mapping |
| [[Data Loading Best Practices]] | `data-loading-best-practices.md` | Key-based vs. property-based load module design, save-view pattern, 3-step update process, backwards induction, file-handling conventions |
| [[DISCO — Module Classification\|DISCO]] | `disco.md` | Five-category module taxonomy (Data, Inputs, System, Calculations, Outputs) |
| [[Building a Hierarchy from an Uploaded File (DataHub → Spoke)\|Hierarchy Load from File]] | `hierarchy-load-from-file.md` | Numbered load list + composite key, load module, per-level `ISFIRSTOCCURRENCE` save views, import into Spoke composite hierarchy |
| [[Number Format Standard]] | `number-format-standard.md` | Comma-decimal/dot-thousands (EU/NL) convention for NUMBER line items; links to one customer model's audit history |
| [[Pattern — Version-as-list (custom-list scenarios)\|Version-as-list]] | `version-as-list.md` | Custom-list scenarios instead of native Versions — trade-offs vs PREVIOUSVERSION/breakback |
| [[Ragged hierarchy with per-level factors\|Ragged Hierarchy]] | `ragged-hierarchy.md` | N-level uneven hierarchy with composite list + cumulative upstream/downstream factors |
| [[Variance Reporting]] | `variance-reporting.md` | With/without Versions approaches; SYS11 → REP05 → REP06 three-module chain using LIS + COLLECT |

---

## Sub-collections

### [[wiki/patterns/anaplan-way/index\|The Anaplan Way]]
Anaplan's official agile implementation methodology — 4 cornerstones, 6 delivery phases, scrum roles. Refer to [[wiki/patterns/anaplan-way/index|Index]] for queries regarding this topic

### [[wiki/patterns/planual/index\|Planual]]
Anaplan's official model-building rulebook — PLANS framework, 8 chapters.
Refer to [[wiki/patterns/planual/index|Index]]  for queries regarding this topic


