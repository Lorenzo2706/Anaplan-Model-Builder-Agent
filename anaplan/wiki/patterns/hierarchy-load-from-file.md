---
title: Building a Hierarchy from an Uploaded File (DataHub → Spoke)
type: pattern
tags: [anaplan, pattern, data-hub, hierarchy, load-list, save-view, ISFIRSTOCCURRENCE]
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/docs/2026-09-11-hierarchy-load-from-file-fieldnotes.md
  - raw/docs/ISFIRSTOCCURRENCE  Anapedia.md
---

# Building a Hierarchy from an Uploaded File (DataHub → Spoke)

A recipe for turning a flat file — one row per leaf record, with each hierarchy level in its
own column (e.g. Region, Country, City, Store) — into a proper Anaplan hierarchy, using
DataHub as the staging area before the Spoke model consumes it. Complements
[[Data Loading Best Practices]] (general key-based vs. property-based loading) — this page is
specifically about the **multi-level, one-column-per-level** file shape and how
[[wiki/functions/index#Logical functions|ISFIRSTOCCURRENCE]] turns that shape into one save
view per hierarchy level.

## Step 0 — Does the file have a unique key?

This decides everything downstream.

| File has a unique key column? | Path |
|---|---|
| Yes | Load directly into the Spoke model where the data is needed. No transformation needed — skip the rest of this page. |
| No | Build a **numbered** load list in DataHub, keyed on a combination of properties. Continue below. |

A "unique key" here means one column (or a value you can derive) that uniquely identifies
each row on its own — most hierarchy-source files don't have this, because the file is a
denormalized export with one row per leaf item and repeating parent-level values.


## Path A — file has a unique key

Load the file straight into the Spoke model. Nothing else in this page applies.

## Path B — file has no unique key

### 1. Create a numbered load list in DataHub

- Create a new **numbered list** in the DataHub model, dedicated to this load. It must be
  numbered — not a normal named list — specifically because the key is a combination of
  properties rather than a single unique column (see the note in Step 0).
- Its **properties must match the file's column headers exactly**, one property per column
  — this is what lets the import map columns to properties without manual re-mapping on
  every refresh.
- The list is keyed on a **combination of properties** (composite key), not a single column,
  since no single column is unique on its own.

### 2. Load the file into the list

Run the import so every uploaded row lands as one list item, with every property populated
from its matching column. After this step, each list item carries the full set of column
values for its row — nothing has been transformed or filtered yet.

### 3. Build a load module

Inside the DataHub tab, create a **load module** dimensioned by the numbered list from
step 1. This module does whatever transformation is needed before the data can be turned
into hierarchy save views — e.g. concatenations, lookups, cleanup of blanks or
inconsistent casing. Keep this module in the **Data** or **Calculations** category per
[[DISCO — Module Classification|DISCO]], not mixed into Inputs or Outputs.

### 4. Identify the first occurrence of each hierarchy level

The file usually repeats parent-level values across many rows (e.g. every row for stores in
"Region A" repeats "Region A" in the Region column). To build a clean list of unique items
for a given level, you only want the **first row** where each distinct value appears.

For each hierarchy level, add a line item using:

```
ISFIRSTOCCURRENCE(<Level column line item>, <numbered list>)
```

This returns `TRUE` on the first row where that level's value appears, and `FALSE` on every
later row with the same value — one such line item per level (Region, Country, City, …).

> [!warning]
> `ISFIRSTOCCURRENCE` follows the **leaf list's order as shown in General Lists**, not any
> parent hierarchy — so the "first" row is whatever order the items were loaded/sorted in,
> not necessarily the row you'd expect. If the file isn't already sorted the way you want,
> use the **Order List** action (or sort the source file before upload) so the row you want
> to win as "first occurrence" for a given value is actually first.
>
> Also note two engine-specific limits from Anapedia: in **Classic**, `ISFIRSTOCCURRENCE` is
> capped at 50 million non-summarized cells; in **Polaris** it has no such cap but is known
> to perform poorly on high-dimensionality models — avoid it there if the list is very large.

### 5. Create one save view per level, filtered on its "first occurrence" line item

For each level, create a **save view** off the load module that:
- Shows only that level's column (plus its parent-level column(s), if the Spoke list needs a
  parent reference).
- Is **filtered to `<Level> Is First Occurrence = TRUE`**, so each distinct value appears
  exactly once.

This gives you one clean, deduplicated save view per hierarchy level — ready to import into
each corresponding [[wiki/concepts/anaplan concepts/04_composite-hierarchies|composite
hierarchy]] list in the Spoke model (top level first, then each level down, setting **Parent
Hierarchy** as you go).

### 6. Import into the Spoke model

From the Spoke model, import each level's save view into its matching list, top level down
to leaf, exactly as in a normal [[wiki/concepts/anaplan concepts/04_composite-hierarchies|
composite hierarchy]] build. Once all levels are loaded, the hierarchy's Parent Hierarchy
chain is complete.

## Why this shape

- **One load list, one load module** — the transformation logic lives in one place instead
  of being repeated per level.
- **ISFIRSTOCCURRENCE instead of a manual dedup process** — no need for a separate
  "find first" helper module; the function does the dedup inline, and the save view filter
  does the rest.
- Matches the **numbered-list + composite-key** loading style described in
  [[Data Loading Best Practices]] for files without a unique key — this page is the
  hierarchy-specific extension of that general pattern.

## See Also

- [[Data Loading Best Practices]] — general key-based vs. property-based DataHub loading
- [[DISCO — Module Classification]] — where the load module belongs
- [[wiki/concepts/anaplan concepts/04_composite-hierarchies|Composite Hierarchies]] — the
  Spoke-side list structure this procedure feeds
- [[Ragged hierarchy with per-level factors|Ragged Hierarchy]] — related pattern when levels
  are uneven across branches
- `ISFIRSTOCCURRENCE` — [[wiki/functions/index|functions index]] row; full syntax notes in
  [[raw/docs/ISFIRSTOCCURRENCE  Anapedia|raw source]]
