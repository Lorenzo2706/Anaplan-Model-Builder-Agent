---
title: Integration API — Model Actions, Delete Actions & Processes
type: concept
tags: [anaplan, integration-api, bulk-api, actions, process, delete, optimizer]
created: 2026-10-23
updated: 2026-10-23
sources:
  - raw/docs/Anaplan Integration API V2 Guide and Reference.md
---

# Integration API — Model Actions, Delete Actions & Processes

Covers the generic **actions** endpoint, **Delete from List using Selection**, and **processes** (ordered containers of actions). Imports and exports have their own pages: [[12_import-actions]], [[13_export-actions]]. Base path: `…/workspaces/{workspaceId}/models/{modelId}/`.

## What the API can run

| Action type | Runnable via API | Endpoint family |
|---|---|---|
| Import | Yes | `imports/{id}/tasks` |
| Export | Yes | `exports/{id}/tasks` |
| Delete from list using selection | Yes | `actions/{id}/tasks` |
| Process (any mix of import / export / delete) | Yes | `processes/{id}/tasks` |
| Other action types (Order list, Create, Assign, Copy branch, Bulk copy, Update current period, Optimizer, …) | **List and read metadata only** via `actions`; run them inside a process | `actions`, `actions/{id}` |

## Model actions (list & metadata)

- `GET actions` → `{id, actionType, name}` per action. Some entries (e.g. *Open Dashboard*) carry no `actionType`.
- `GET actions/{actionId}` → type-specific metadata. Known `actionType` values seen: `DELETE_BY_SELECTION`, `ORDER_HIERARCHY`, `SIMPLE_CREATE`, `BULK_DELETE_ENTITIES`, `SELECT_CHILDREN` (Assign), `COPY_TO_NUMBERED_LIST` (Assign Only), `BULK_ENTITY_COPY`, `BULK_COPY`, `UPDATE_CURRENT_PERIOD`, `OPTIMIZER`. Type-specific fields include `listId`, `filterLineItemId`, `lineItemId`, `sortOrder`, `sourceMember`, `targetMember`.
- A line item that has since been deleted shows as an **empty string** (`"lineItemId": ""`); an unknown action ID returns `404`.
- Action names can be up to 60 characters and include special characters/emoji — don't assume ASCII when parsing.

## Delete from List using Selection

Automates removing selected items from a list. Prerequisite in the model: a **control module** (boolean line item selecting items to delete) and a *Delete from List using Selection* action built on it (see [[../anaplan concepts/11_lists|Lists]] for list basics).

1. `GET actions` → pick the delete action ID.
2. `POST actions/{actionId}/tasks` body `{"localeName":"en_US"}` → `taskId`.
3. `GET actions/{actionId}/tasks/{taskId}` (or list tasks) until `COMPLETE`.

For delete tasks `failureDumpAvailable` is **always false**; the success message is `deleteFromSelectionSucceeded` ([[15_task-codes-and-logs]]).

## Processes

A process is an admin-configured container that runs actions **in order**. Because each step can fail independently, process status is nested.

| Purpose | Request |
|---|---|
| List processes | `GET processes` → `[{id, name}]` |
| Process metadata | `GET /models/{modelId}/processes/{processId}` → ordered `actions[]` (`id`, `name`, `actionType`; imports add `importDataSourceId`, `importType`; exports add `exportType`, `exportFormat`, `layout`). Add `?showImportDataSource=true` for data-source type |
| Start | `POST processes/{processId}/tasks` body `{"localeName":"en_US"}` (optionally `mappingParameters`, see [[12_import-actions#runtime-mapping-parameters]]) |
| List / status / cancel | `GET` / `DELETE processes/{processId}/tasks[/{taskId}]` |
| Per-step timing | `GET …/tasks/{taskId}?includeProcessDetails=true` adds `duration` and `startTime` (ms epoch) to the process and each nested result |
| Dump file of a failed import step | `GET …/tasks/{taskId}/dumps/{objectId}` (+ `/chunks`, `/chunks/{n}`) |

- Process metadata gives each import's `importDataSourceId`, which is the `fileId` to upload/download for that step ([[11_file-upload-and-download]]).
- Task result: top-level `successful` / `objectId` (the process ID) plus `nestedResults[]`, each with its own `objectId`, `successful`, `failureDumpAvailable`. **Use the nested `objectId` to fetch that step's dump**, chunked, as with imports.
- A process result is only as informative as its steps; for debugging, pair `includeProcessDetails` with the dump files and [[15_task-codes-and-logs]].

> [!tip] Choosing import-action vs process
> Calling a **process** from an integration lets model builders reorder or add steps (load → calculate → export → cleanup) without changing the integration code, and gives one `taskId` to monitor. Calling a bare import is simpler but ties the integration to one action. Pairs with [[../../patterns/data-loading-best-practices|data loading best practices]].

## Optimizer log

`GET optimizeActions/{actionId}/tasks/{correlationId}/solutionLogs` (`Accept: text/plain`) returns the solver log for root-cause analysis. Requires **Workspace Administrator**; the `correlationId` comes from the Anaplan UI after running the Optimizer action; logs are removed **48 h after last access**.

## Busy-model behaviour

Start/monitor/list endpoints of imports, exports, deletes, and processes still respond while a model is busy; all other endpoints wait. Details in [[03_reliability-retries-rate-limits#what-still-works-while-a-model-is-busy]].

## Related

- [[12_import-actions]] · [[13_export-actions]] · [[15_task-codes-and-logs]]
- [[../workflow/index|Workflow]] — a different feature (in-app task workflow), not API processes
