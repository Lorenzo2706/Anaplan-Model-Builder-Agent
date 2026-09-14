---
title: Field Notes — Hierarchy Load from File (DataHub → Spoke)
type: source
tags: [anaplan, data-hub, hierarchy, field-notes]
created: 2026-09-11
updated: 2026-09-11
sources: [raw/docs/2026-09-11-hierarchy-load-from-file-fieldnotes.md]
---

# Field Notes — Hierarchy Load from File (DataHub → Spoke)

Dictated field-experience procedure (not an Anapedia clipping) for turning a flat,
multi-column hierarchy source file into a Spoke-model composite hierarchy via DataHub.
Covers the unique-key vs. no-unique-key branch, the numbered load list with a composite
property key, the load-module transformation step, and using `ISFIRSTOCCURRENCE` to build
one deduplicated save view per hierarchy level.

## Key takeaways

- A unique key in the source file means a direct load into the Spoke model — no DataHub
  transformation needed.
- No unique key → build a load list in DataHub whose properties mirror the file's column
  headers exactly, keyed on the combination of those properties. The list must be
  **numbered** specifically because that combination-of-properties key is a workaround a
  named list's single-name key can't express — a normal named list is the default whenever
  a single unique key exists.
- A load module inside the DataHub tab does the transformation; `ISFIRSTOCCURRENCE` (one
  line item per level) flags the first row for each distinct level value, and a save view
  filtered on that flag gives a clean, deduplicated list per level.
- `ISFIRSTOCCURRENCE` follows leaf-list order in General Lists, not parent hierarchy order —
  sort/Order List the source appropriately before relying on "first occurrence."

## Resulting wiki page

- [[Building a Hierarchy from an Uploaded File (DataHub → Spoke)|Hierarchy Load from File]] —
  new standalone pattern page, cross-linked from [[Data Loading Best Practices]],
  [[DISCO — Module Classification]], and
  [[wiki/concepts/anaplan concepts/04_composite-hierarchies|Composite Hierarchies]].

## Raw source

- [[raw/docs/2026-09-11-hierarchy-load-from-file-fieldnotes|Field notes (raw)]]
