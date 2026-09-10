---
title: Integration API — Lists & Dimension Items
type: concept
tags: [anaplan, integration-api, lists, dimensions, list-items]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Model lists.md
  - raw/docs/Retrieve lists.md
  - raw/docs/Retrieve list metadata.md
  - raw/docs/Retrieve list data.md
  - raw/docs/Add list items.md
  - raw/docs/Update list items.md
  - raw/docs/Delete list items.md
  - raw/docs/Reset numbered list index.md
  - raw/docs/Preview large data list read.md
  - raw/docs/Other model metadata.md
  - raw/docs/Look up dimension items by name or code.md
  - raw/docs/Retrieve all items in a dimension.md
  - raw/docs/Retrieve selected items in a dimension.md
---

# Integration API — Lists & Dimension Items

Model-lists endpoints discover, inspect, retrieve, and transactionally maintain [[../anaplan concepts/11_lists|list]] structures and items — without running a file-based import. "Other model metadata" / dimension-item endpoints go one level more general: they resolve items for **any** dimension type (list, list subset, [[../anaplan concepts/09_line-item-subsets|line item subset]], Users, Time, Versions), which is what an integration needs before it can target a specific cell intersection.

All endpoints below require **Workspace Administrator** authority unless noted.

## List discovery and metadata

| Endpoint | Method & path |
|---|---|
| Retrieve lists | `GET /workspaces/{workspaceId}/models/{modelId}/lists` |
| Retrieve list metadata | `GET /workspaces/{workspaceId}/models/{modelId}/lists/{listId}` |
| Preview large data list read | `GET /workspaces/{workspaceId}/models/{modelId}/lists/{listId}/preview` → CSV, limited subset of records |

List metadata fields: `id`, `name`, `category`, `itemCount`, `permittedItems` (headroom before hitting a size limit), `numberedList` (bool), `nextitemIndex` (numbered lists only), `hasSelectiveAccess`, `parent` (`{id, name}`), `subsets` (`[{id, name}]`), `topLevelItem`, `useTopLevelAsPageDefault`, `workflowEnabled`, `productionData` (true = an [[../anaplan concepts/12_model-calendar|ALM]] production list), `displayNameProperty`, `properties` (`dataTags`, `format`, `formula`, `notes`, `referencedBy`). Absent metadata fields (e.g. no parent, no top-level item) are simply omitted from the response.

## Reading list items

`GET /workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?includeAll=true`

- **Cap: 1,000,000 records.** A list over that returns `400 Bad Request` instead of a truncated subset — use [[09_bulk-and-large-volume-data|large-volume read requests]] for bigger lists.
- Default fields always returned: `id`, `name`, `code`, `parent`, `parentId`, `listId`/`listName` (the last two only if the list has a **Parent Hierarchy** set).
- `includeAll=true` adds: `write`/`read` ([[../anaplan concepts/17_selective-access|Selective Access]] user assignments), `subsets` (membership booleans), `properties` (custom list property values).
- Response can be JSON (`listItems` array) or CSV depending on `Accept`.

## Adding, updating, deleting list items

| Endpoint | Method & path | Cap |
|---|---|---|
| Add list items | `POST /workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=add` | 100,000 items/call |
| Update list items | `PUT /workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items` | 100,000 items/call |
| Delete list items | `POST /workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=delete` | 100,000 items/call |

Behavior notes:

- **Add**: response has `total`, `added`, `ignored`, `failures` (each with `requestIndex` + `failureType` + `failureMessageDetails`, e.g. `INCORRECT_FORMAT`).
- **Update**: for a **standard list**, an item can be identified by `id`, `code`, or `name`; for a **numbered list**, only `id` or `code`. Passing multiple identifiers for the same item is an error. Any property/subset field left unspecified keeps its existing value (partial update, not a full replace). When an update succeeds, all downstream formula-linked calculations complete as part of the same call.
- **Delete**: identify items per-request by whichever identifier is available — you can mix ID for one item and code for another in the same call. Response has `deleted`/`numberOfItemsDeleted` and a `failures` array (e.g. `"Not found"`, `"Ambiguous criteria"` when both ID and code are given for one item).

> [!note]
> All three mutating calls require Workspace Administrator authority — this is stricter than read access to the list itself.

## Reset numbered list index

`POST /models/{modelId}/lists/{listId}/resetIndex`

Resets a [[../anaplan concepts/15_numbered-lists|numbered list]]'s internal index so newly-added items stay within the maximum allowed. **The list must be empty first** — calling this on a non-empty list returns `400 Bad Request` (`"We can't reset the list item index of a list that contains data..."`). No response body on success.

## Dimension-item resolution ("Other model metadata")

These endpoints work with **any** dimension type — not just lists — and are how an integration turns a human-readable name/code into the internal item ID an API call needs.

| Endpoint | Method & path | Scope | Cap |
|---|---|---|---|
| Retrieve all items in a dimension | `GET /models/{modelGuid}/dimensions/{dimensionId}/items` | Model-level — no view-level hiding/filtering/Selective Access applied | 1,000,000 items (else `400`) |
| Retrieve selected items in a dimension | `GET /models/{modelId}/views/{viewId}/dimensions/{dimensionId}/items` | View-level — respects hidden/filtered items and [[../anaplan concepts/17_selective-access|Selective Access]] | 1,000,000 cells in the view (else `400`) |
| Look up dimension items by name or code | `POST /models/{modelId}/dimensions/{dimensionId}/items` (request body: names or codes to resolve) | Any dimension type: lists, Time periods, Users, Versions | — |

Notes:

- Model-level dimension calls **don't support the Time dimension** (returns `400`) — use the view-level dimension endpoint instead when Time is involved.
- If codes aren't set for an item, the `code` field is simply omitted from the response — not returned as null/empty.
- Look-up returns only items that actually match a given name/code; it doesn't error on a non-matching entry, it just excludes it. Errors: `404` if workspace/model/dimension doesn't exist; `400` if the dimension doesn't support codes but codes were supplied anyway.

Example dimension-items response:

```json
{
  "items": [
    { "code": "N", "id": "200000000001", "name": "North" },
    { "code": "S", "id": "200000000003", "name": "South" },
    { "id": "200000000000", "name": "Total Company" }
  ]
}
```

## Related

- [[01_overview|Integration API — Overview]]
- [[07_modules-views-line-items|Modules, Views & Line Items]] — line-item-scoped dimension lookups
- [[09_bulk-and-large-volume-data|Bulk & large-volume data]] — for lists beyond 1,000,000 records
- [[../anaplan concepts/11_lists|Lists (concept)]]
- [[../anaplan concepts/17_selective-access|Selective Access (concept)]]
