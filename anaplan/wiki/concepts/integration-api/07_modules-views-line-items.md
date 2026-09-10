---
title: Integration API — Modules, Views & Line Items
type: concept
tags: [anaplan, integration-api, modules, views, line-items, metadata]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Module, view metadata and limited volume cell data.md
  - raw/docs/Retrieve IDs and names of modules.md
  - raw/docs/Retrieve IDs and names of model views.md
  - raw/docs/Retrieve IDs and names for module views.md
  - raw/docs/Retrieve metadata for dimensions on a view.md
  - raw/docs/Line item information.md
  - raw/docs/Retrieve all line items in a model.md
  - raw/docs/Retrieve all line items in a module.md
  - raw/docs/Retrieve all line item metadata in a model.md
  - raw/docs/Retrieve all line item metadata in a module.md
  - raw/docs/Retrieve dimension ids for a line item.md
  - raw/docs/Retrieve dimension items for a line item.md
---

# Integration API — Modules, Views & Line Items

These endpoints discover [[../anaplan concepts/14_modules|modules]] and views, understand how a view is dimensionalized, and inspect [[../anaplan concepts/10_line-item|line items]] — the metadata layer an integration needs before reading or writing actual cell data (see [[08_cell-data-read-write|Cell Data — Read & Write]]).

All endpoints below require **Workspace Administrator** authority and (where noted) model-role read access to the specific module.

## Modules

`GET /models/{modelId}/modules` → `{id, name}` for every module in the model.

## Views

| Endpoint | Method & path | Notes |
|---|---|---|
| Retrieve IDs and names of model views | `GET /models/{modelId}/views` | All views across the model (default + saved + optionally unsaved subsidiary) |
| Retrieve IDs and names for module views | `GET /models/{modelId}/modules/{moduleId}/views` | Views for one known module; also returns the module's default view |
| Retrieve metadata for dimensions on a view | `GET /models/{modelId}/views/{viewId}` | Which dimensions define rows/columns/pages for that view |

View naming conventions returned by the API:

| View kind | `viewId` | `name` format |
|---|---|---|
| Default view | Same as `{moduleId}` | Same as the module name |
| Saved view | Its own ID | `ModuleName.SavedViewName` (e.g. `REP01 Profit & Loss Report.P & L by Country`) |
| Unsaved subsidiary view | Same as the line item's `{lineItemId}` | `ModuleName.LineItemName` |

- Pass `includesubsidiaryviews=true` to include unsaved subsidiary views in either views listing.
- Module/view names containing special characters are enclosed in single quotes in the response (e.g. `'StrategicPlanning/2020'.'accountSummary&overview/US$'`).
- On the dimensions-metadata call, `{viewId}` can be swapped for any valid `{lineItemId}`: if that line item has a subsidiary view, its dimension metadata is returned; otherwise the line item's default view metadata is returned. If a view has no dimensions on an axis, that axis field is **omitted entirely** (no empty `"rows": []`).

Example dimensions-metadata response:

```json
{
  "viewName": "REV01 Price Book",
  "viewId": "102000000000",
  "rows": [ { "id": "101000000000", "name": "Products" }, { "id": "101000000003", "name": "Regions" } ],
  "columns": [ { "id": "101999999999", "name": "Line items" } ],
  "pages": [ { "id": "101000000001", "name": "Versions" } ]
}
```

## Line items

| Endpoint | Method & path | Scope |
|---|---|---|
| Retrieve all line items in a model | `GET /models/{modelId}/lineItems` | Model-wide; flat list, no hierarchy; restricted to modules the caller's role can **read** |
| Retrieve all line items in a module | `GET /models/{modelId}/modules/{moduleId}/lineItems` | One module; `404` if role lacks read access or module ID is invalid |
| Retrieve all line item metadata in a model | `GET /models/{modelId}/lineItems?includeAll=true` | Model-wide, full metadata |
| Retrieve all line item metadata in a module | `GET /models/{modelId}/modules/{moduleId}/lineItems?includeAll=true` | One module, full metadata; `404` on invalid module ID |
| Retrieve dimension ids for a line item | `GET /models/{modelId}/lineitems/{lineItem_Id}/dimensions` | Which dimensions apply to a specific line item |
| Retrieve dimension items for a line item | `GET /models/{modelId}/lineItems/{lineItemId}/dimensions/{dimensionId}/items` | The valid members for one of those dimensions (max 1,000,000, else `400`) |

Both "all line items" calls return results **in the same order they appear in the Anaplan UI**. `includeAll=true` line-item metadata includes: `moduleId`/`moduleName`, `id`, `name`, `isSummary`, `startOfSection`, `broughtForward`, `useSwitchover`, `breakback` (see [[../anaplan concepts/14_modules#breakback|Breakback]]), `cellCount`, `version` (`{id, name}`), `appliesTo` (dimensions, including any [[../anaplan concepts/09_line-item-subsets|line item subset]]), `dataTags`, `referencedBy`, `parent`, `readAccessDriver`/`writeAccessDriver` (see [[../anaplan concepts/01_access-drivers|Access Drivers]]), `formula`, `format` + `formatMetadata` (decimal places, grouping/decimal separators, units, zero format, etc.), `summary` (summary method), `timeScale`, `timeRange`, `formulaScope`, `style`, `code`, `notes`.

`Retrieve dimension items for a line item` returns items as a **flat list** (no hierarchy), in the order listed in the model — this is the line-item-scoped counterpart to [[06_lists-and-dimension-items#dimension-item-resolution-other-model-metadata|dimension-item resolution]] at the model/view level.

## Related

- [[01_overview|Integration API — Overview]]
- [[06_lists-and-dimension-items|Lists & Dimension Items]]
- [[08_cell-data-read-write|Cell Data — Read & Write]]
- [[../anaplan concepts/14_modules|Modules (concept)]]
- [[../anaplan concepts/10_line-item|Line Item (concept)]]
- [[../anaplan concepts/18_subsidiary-views|Subsidiary Views (concept)]]
