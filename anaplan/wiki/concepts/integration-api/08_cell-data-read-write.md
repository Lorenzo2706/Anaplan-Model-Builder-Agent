---
title: Integration API — Cell Data (Read & Write)
type: concept
tags: [anaplan, integration-api, cell-data, transactional-write, view-data]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Retrieve cell data for a view.md
  - raw/docs/Module cell data.md
---

# Integration API — Cell Data (Read & Write)

These are the **transactional**, small-to-medium-volume endpoints for reading a view's cell data and writing directly into module cells — as opposed to file-based imports or the [[09_bulk-and-large-volume-data|large-volume read requests]] used for bigger extracts.

## Reading cell data for a view

`GET /models/{modelId}/views/{viewId}/data?pages=dimensionId:itemId&format=v1`

- **Cap: 1,000,000 cells.** A view over that returns `400 Bad Request` instead of a partial result — use the [quick sum bar](https://help.anaplan.com/cb15ce25-b344-4a61-8b02-cd21bc5bfca3) in Anaplan to check a view's cell count first, or switch to a [[09_bulk-and-large-volume-data|large-volume read request]].
- Calling repeatedly in a short window can trigger `429` — see [[03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]].
- `{viewId}` can be swapped for any valid `{lineItemId}`: if that line item has a subsidiary view, its data is returned as seen in that subsidiary view; otherwise its default-view data is returned.
- `pages` selects a specific page (`dimensionId:itemId`, repeatable or colon-chained) — omit it to get the default page.
- `exportType` + `{moduleId}` together select the export layout (`GRID_ALL_PAGES`, `GRID_CURRENT_PAGE`, `TABULAR_SINGLE_COLUMN`, `TABULAR_MULTI_COLUMN` — see [[01_overview#export-layout-types|Export layout types]]); `{maxRows}` caps the number of exported rows (header excluded).

### CSV response shape (default)

- First line: page-selector values — omitted if the view has no page dimensions.
- One line per dimension on columns follows the page-selector line.
- One leading column per dimension on rows, to the left of the data.

### JSON response shape

Request with `Accept: application/json` **and** `format=v1`. Shape:

| Key | Meaning |
|---|---|
| `pages` | Selected item for each page selector (empty/absent if none) |
| `columnCoordinates` | List of coordinate-lists, one per column; each inner list has one entry per column dimension |
| `rows` | List of row objects |
| `rows[].rowCoordinates` | Coordinate-list for that row, one entry per row dimension |
| `rows[].cells` | Cell values for that row, positionally aligned with `columnCoordinates` |

To get the full coordinates for a specific cell: combine that row's `rowCoordinates`, the `columnCoordinates` entry at the same list position as the cell in `cells`, and any selected `pages`.

```json
{
  "pages": ["Value", "23mm"],
  "columnCoordinates": [["Jan 13"], ["Feb 13"], ["Q1 FY13"]],
  "rows": [
    { "rowCoordinates": ["Durham"], "cells": ["64.6", "57.94", "108.36"] }
  ]
}
```

JSON responses escape these characters: `\b`, `\t`, `\n`, `\f`, `\r`, `"`, `/`, `\` — client parsers should expect the escaped forms.

## Writing cell data (transactional)

`POST /models/{modelId}/modules/{moduleId}/data`

Request body: an array of `CellWrite` objects, each targeting one cell via the line item plus one item per applicable dimension (Time and Versions included).

| Field | Required? | Notes |
|---|---|---|
| `lineItemId` / `lineItemName` | One of the two | Line item the write targets |
| `dimensions` | Omit only if the line item has no dimensions | Array of dimension coordinates |
| `dimensionId` / `dimensionName` | One of the two, per dimension entry | The dimension on the line item |
| `itemId` / `itemName` / `itemCode` | One of the three | The item on that dimension |
| `value` | Yes, cannot be `null` | Must match the line item's format |

Value formats:

| Line item format | Example |
|---|---|
| Number | `123.45` or `"123.45"` (only successfully-parsed strings are written) |
| Text | `"Text to set"` |
| Boolean | `true` / `false` |
| Date | `"2020-12-31"` (`YYYY-MM-DD`) |
| Time Period (Week/Month/Quarter/Half-Year/Year) | `"Week 1 FY20"`, `"Dec 20"`, `"Q1 FY20"`, `"H1 FY20"`, `"FY20"` — the UI label, not an ID |
| List-formatted line item | `"UK"` — the item's name in the configured list |

Behavior and limits:

- **Cap: 100,000 cells or 15 MB per call, whichever is lower.** For larger payloads, use the import API instead.
- If one `CellWrite` fails, the rest of the batch still applies — failures are itemized in the response.
- Requires write access; Workspace Administrators can write to any cell **except aggregate cells**, including read-only and invisible cells.
- **Aggregate cells are never writable** — a cell is aggregate when one of its dimension items has child items of its own (this includes any aggregate cell for a line item with [[../anaplan concepts/14_modules#breakback|Breakback]] enabled). For a line item dimensioned by a composite list, only the child items defined directly in that dimension's own list (not inherited from a parent list) are writable.

```json
{
  "numberOfCellsChanged": 42,
  "failures": [
    { "requestIndex": 0, "failureType": "cellIsCalculated",
      "failureMessageDetails": "the cell is a calculated/aggregate cell and is not writeable" },
    { "requestIndex": 9, "failureType": "cellIsInvalid",
      "failureMessageDetails": "the cell could not be found or resolved" }
  ]
}
```

## Related

- [[01_overview|Integration API — Overview]] — CSV/JSON response conventions
- [[07_modules-views-line-items|Modules, Views & Line Items]] — resolving view/line-item/dimension IDs before reading or writing
- [[09_bulk-and-large-volume-data|Bulk & large-volume data]] — for reads beyond 1,000,000 cells
- [[../anaplan concepts/14_modules|Modules (concept)]] — Breakback and cell count
