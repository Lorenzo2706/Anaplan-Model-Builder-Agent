---
title: Anapedia — Breakback (dedicated page)
type: source
tags: [anaplan, breakback, modules, clippings, sources]
created: 2026-09-09
updated: 2026-09-09
sources: [raw/docs/Breakback  Anapedia.md]
---

# Anapedia — Breakback (dedicated page)

**Raw:** [[raw/docs/Breakback  Anapedia|Breakback | Anapedia]]

First-time ingest of the dedicated Anapedia "Breakback" page. Breakback was already covered as a section within [[wiki/concepts/anaplan concepts/14_modules|Modules]], sourced from `raw/docs/Configure modules.md`; per "prefer updating an existing page over creating a near-duplicate," this ingest enriches that existing section rather than creating a new page.

## What this source added

The existing Breakback section covered: the Enabled/Disabled setting, when to use/avoid it, and the SUM-only constraint. This dedicated Anapedia page added detail not previously captured:

- The **Hold** feature — temporarily holding a cell's value during a Breakback distribution, and the read-only-cell interactions (Selective Access, Dynamic Cell Access, rolling-forecast historical months) that trigger it automatically.
- Breakback's scope restriction to **simple hierarchies and the time dimension only** (not across several line items).
- The **1,000,000-cell warning** threshold for a single Breakback action.
- Breakback's effect on **module change history** (only the triggering change + affected-cell count is recorded, not every cell).

## Wiki pages touched

- [[wiki/concepts/anaplan concepts/14_modules|Modules]] — Breakback section extended; `sources:` frontmatter gained this raw doc.
