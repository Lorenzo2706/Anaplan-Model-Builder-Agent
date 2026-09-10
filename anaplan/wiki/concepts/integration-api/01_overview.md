---
title: Integration API — Overview
type: concept
tags: [anaplan, integration-api, rest, api-overview]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Get started with the Anaplan Integration API.md
  - raw/docs/Integration API v2.0.md
  - raw/docs/Anaplan concepts applied to API.md
  - raw/docs/API system behavior and design.md
  - raw/docs/Resource structure and parameters.md
  - raw/docs/Request and response formats.md
---

# Integration API — Overview

The **Anaplan Integration API v2.0** is a set of secure REST endpoints for moving data into and out of Anaplan models, running model actions, and reading or updating selected model metadata and transactional data. It replaces manual import/export steps with repeatable, system-driven workflows.

Base URL for all endpoints below: `https://api.anaplan.com/2/0/...`

A complete Postman collection is published at [Official Anaplan Collection](https://www.postman.com/apiplan/official-anaplan-collection/collection/2m6331d/official-anaplan-collection).

Use the Integration API to:

- Discover the workspaces, models, modules, views, lists, files, imports, exports, processes, and actions available to an integration user.
- Upload source files and run imports.
- Run exports and download generated files.
- Run processes or delete actions and monitor task status.
- Read view data, list data, and selected model metadata.
- Write cell data or list items directly through transactional endpoints.

## Core object model

Every Integration API call operates on a chain of Anaplan objects. Understanding this hierarchy is the fastest way to reason about which endpoint you need:

| Object | What it is | Why the API cares |
|---|---|---|
| **Tenant** | A customer's overall Anaplan environment; the broadest context for access, auth, and rate limits | API users operate within the tenant tied to their authenticated account |
| **Workspace** | A container for one or more models | Most calls need a `workspaceId` to know where the target model lives |
| **Model** | The planning application containing modules, lists, line items, views, actions, imports, exports, processes | `modelId` is the most-used identifier in the API |
| **Module** | A structured area within a model holding related planning data and views | Modules are where [[Line Item\|line items]] and [[Modules\|calculations]] live |
| **View** | A particular presentation of module data (rows/columns/pages) | Integrations read from or export through saved views |
| **Line Item** | A specific measure/calculation/field within a module | Describes the data points an integration reads, writes, or inspects |
| **List** | A structural [[Dimensions\|dimension]] (products, regions, accounts, etc.) | Defines the coordinates data is organized by; addable/updatable/deletable via API |
| **Dimension** | How data is organized — time, version, a list, or Users | Identifies the coordinates of a cell intersection |
| **Import / Export** | Saved actions that bring data in / send data out | The API can start them, monitor task status, retrieve failures |
| **File** | A model-level object used by import/export workflows | Can be uploaded/downloaded in chunks; see [[09_bulk-and-large-volume-data\|Bulk & large-volume data]] |
| **Action** | A runnable operation saved in a model (import, export, delete) | The API triggers logic already configured in the model rather than recreating it |
| **Process** | A sequence of actions run together in order | Used for multi-step workflows (import → calculate → export → cleanup) |
| **Task** | A running or completed execution of an action/import/export/delete/process | Returns a `taskId` used to poll progress/completion/failures |
| **User** | The authenticated caller, or another user in the tenant | API access is permission-based on the calling user's identity |

A typical workflow moves from broad discovery calls (get workspaces → get models → get modules/lists) to a specific operation (start an import, read a view, write cells) — see [[04_workspaces-and-models|Workspaces & Models]], [[06_lists-and-dimension-items|Lists & Dimension Items]], and [[07_modules-views-line-items|Modules, Views & Line Items]] for the discovery endpoints themselves.

## System behavior and design

- **Chunking**: large imports/exports are chunked for efficiency and resilience. Upload files can be split into chunks and loaded sequentially; export files may be downloaded in chunks. See [[09_bulk-and-large-volume-data|Bulk & large-volume data]].
- **Task polling**: long-running actions return a `taskId`. Poll the task endpoint for current state, current step, progress, result info, failure counts, and whether a dump file is available.
- **Dump files**: contain details about records/steps that failed during an import or process. Import dumps attach to import tasks; process dumps attach to process tasks. Export output is a separate concept, downloaded from file chunk endpoints — not a dump file.
- **Model busy state**: some actions lock parts of model execution while Anaplan prepares data, runs calculations, loads data, or creates files. Avoid launching conflicting tasks against the same model in parallel unless the workflow is tested for concurrency. See [[03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]] for the full busy/retry model.
- **Content types**: the API supports `application/json` for requests/responses; a file chunk is returned as `application/octet-stream` binary stream.
- **Paging**: list-style responses can be paged with `limit` (results per page), `offset` (starting point), and a `sort` attribute. Paging governs *results per API call*, not file page counts (that's a separate concept — see large-volume read requests).

## Resource structure and path parameters

Endpoint paths are built by chaining parameters, most obtained from a prior call. Example — the calls needed to check an import task's status:

1. Log into Anaplan, open **Help → About**, copy `Workspace Id` and `Model Id`.
2. `GET` the list of `imports` in the model.
3. Choose an `importId`.
4. `POST` the import to start it — this returns a `taskId`.
5. `GET` the status of that `taskId`.

> [!warning]
> Path parameters of type string are **case-sensitive**. `workspaceId` values are lowercase (e.g. `8a8b8c8d8e8f8g8i`); `modelId` values are uppercase (e.g. `75A40874E6B64FA3AE0743278996850F`). Submitting the wrong case means the object is not recognized.

| Path parameter | Type | Returns / identifies |
|---|---|---|
| `{workspaceId}` | string (lowercase) | Workspaces |
| `{modelId}` | string (uppercase) | Models |
| `{importId}` | number | Imports — a failed import generates a dump file |
| `{exportId}` | number | Exports |
| `{fileId}` | number | Files — used to delete/upload a file for an action |
| `{chunkId}` | string | Chunks within an import/export file (recommended chunk size 1–50 MB, default 10 MB) |
| `{processId}` | number | Processes — can contain both imports and exports |
| `{actionId}` | number | Actions |
| `{taskId}` | string | Tasks — removed when the model unloads (e.g. all users log out) |
| `{objectId}` (dumps) | number | Dump file for a failed import |
| `{userId}` | string | A specific user |
| `{pageNo}` | number | Which page of a large read request to download |
| `{requestId}` (readRequests) | number | A large-volume read request |

Common query parameters (capitalization must match exactly):

| Query parameter | Values | Effect |
|---|---|---|
| `tenantDetails` | `true`/`false` | Include estimated workspace size in bytes |
| `includeAll` | `true`/`false` | Include additional metadata fields for a line item or list |
| `action` | `add`, `delete`, `update` | Chooses the list-item mutation performed |
| `showImportDataSource` | `true`/`false` | Include the import data source's ID and format |
| `includesubsidiaryviews` | `true`/`false` | Include unsaved subsidiary views in a views listing |
| `format` | `v1` | Request a JSON response instead of CSV for cell/view data |
| `modelDetails` | `true`/`false` | Include memory usage, creation date, recent changes for a model |
| `pages` | `{dimensionId}:{itemId}` | Selects which page(s) of a view to return cell data for |

## Request and response formats

Most requests/responses use JSON; some endpoints return CSV; file chunk endpoints use binary streams. Common headers:

| Header | Use |
|---|---|
| `Authorization: AnaplanAuthToken {anaplan_auth_token}` | Required for authenticated requests |
| `Content-Type: application/json` | Request body is JSON |
| `Content-Type: application/octet-stream` | Request body is a binary stream (file chunk upload) |
| `Accept: application/json` | Preferred response format is JSON |

A typical JSON response envelope:

```json
{
  "meta": { "schema": "https://api.anaplan.com/2/0/objects/view" },
  "status": { "code": 200, "message": "Success" },
  "items": []
}
```

- `meta` — metadata about the response, e.g. the object schema.
- `status` — response code and message.
- Resource-specific data — `items`, `file`, view metadata, rows/columns, etc.

For view/cell data returned as CSV: the first line holds page-selector values (omitted if no page dimensions); a header line follows per dimension on columns; a leading column appears per dimension on rows. Pass `Accept: application/json` **and** `format=v1` to get JSON instead, shaped as `pages` / `columnCoordinates` / `rows` (each row has `rowCoordinates` + `cells`) — see [[08_cell-data-read-write|Cell Data — Read & Write]] for the full shape and worked example.

`204 No Content` is a valid success response with an empty body — expected for some task-related `POST` requests.

| Status code | Meaning |
|---|---|
| `200 OK` | Success |
| `204 No Content` | Success, empty body |
| `400 Bad Request` | Missing/invalid request values |
| `405 Method Not Allowed` | Wrong HTTP method for the endpoint |
| `406 Not Acceptable` | Requested response format unsupported — check `Accept` |
| `415 Unsupported Media Type` | Request body format unsupported — check `Content-Type` |
| `429 Too Many Requests` | Rate limited — see [[03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]] |

> [!note]
> Client parsers should ignore unknown/extra response fields — the API may add fields to a response in the future.

## Export layout types

When initiating a large read request or requesting cell data with an `exportType`, these layouts are available (they describe data shape, not HTTP media types):

| `exportType` | Description |
|---|---|
| `GRID_ALL_PAGES` | Grid layout, respects existing sort/filter on the data grid |
| `GRID_CURRENT_PAGE` | Grid layout for the currently selected page only |
| `TABULAR_SINGLE_COLUMN` | All dimensions in columns, final column reserved for data |
| `TABULAR_MULTI_COLUMN` | Multiple data columns |

## Related

- [[02_authentication-and-permissions|Authentication, Access & Permissions]]
- [[03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]]
- [[04_workspaces-and-models|Workspaces & Models]]
- [[../../patterns/index|Patterns index]] — for DISCO, data-loading best practices that pair with Integration API imports
