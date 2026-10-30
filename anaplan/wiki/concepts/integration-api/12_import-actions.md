---
title: Integration API — Import Actions
type: concept
tags: [anaplan, integration-api, bulk-api, import, tasks, dump-file]
created: 2026-10-23
updated: 2026-10-23
sources:
  - raw/docs/Anaplan Integration API V2 Guide and Reference.md
---

# Integration API — Import Actions

Running a saved **import action** through the API: upload the file, start a task, poll it, and fetch the dump file if rows failed. Base path: `…/workspaces/{workspaceId}/models/{modelId}/`.

## Workflow

1. [[11_file-upload-and-download|Upload the file]] to the import's data source.
2. `GET imports` → find the `importId`.
3. `POST imports/{importId}/tasks` → returns a `taskId`.
4. `GET imports/{importId}/tasks/{taskId}` until `taskState = COMPLETE`.
5. If `failureDumpAvailable: true`, download the dump file ([below](#dump-files)).

> [!note] Calculations are done when the task completes
> When an import completes successfully, all **downstream calculations are also complete**, including cells linked by formulas to the cells updated.

> [!note] Admin bypass
> A Workspace Administrator can run any action regardless of model role, and an admin-run import **ignores Selective Access and Dynamic Cell Access**, same as the desktop experience. Non-admins need a model role that grants the action — see [[02_authentication-and-permissions]].

## Endpoints

| Purpose | Request |
|---|---|
| List imports | `GET imports` → `{id, name, importDataSourceId, importType}` (e.g. `HIERARCHY_DATA`, `MODULE_DATA`) |
| Import definition metadata | `GET imports/{importId}` → `name`, `type` (`FILE` or `MODEL`), and for file sources `textEncoding`, `columnSeparator`, `textDelimiter`, `headerRow`, `firstDataRow`, `decimalSeparator`, `headerNames[]`, `columnCount`. Lets you build mappings without reading the file |
| Start | `POST imports/{importId}/tasks` body `{"localeName":"en_US"}` → `{"taskId":…}` |
| List tasks | `GET imports/{importId}/tasks` (sorted by creation time; append `?sort=-creationTime` for newest first). Empty = not running or already finished |
| Status | `GET imports/{importId}/tasks/{taskId}` |
| Cancel | `DELETE imports/{importId}/tasks/{taskId}` |

> [!warning] `localeName` is mandatory
> The body `{"localeName": "en_US"}` is required on every task `POST` (import, export, delete, process). Omit it and the call returns **400 Bad Request** and the action does not start. `en_US` is the only supported language for status/error messages (the guide's own mapping examples also use `en_GB` — treat that as a locale hint for number/date parsing, not message language).

## Runtime mapping parameters

Imports and processes accept parameters on `POST`, alongside the locale:

```json
{"localeName": "en_GB", "mappingParameters": [{"entityType": "Version", "entityName": "Actual"}]}
```

Typical use: load the same file into a chosen **Version** (see [[../anaplan concepts/22_versions|Versions]] and [[05_model-calendar-and-versions]]) without editing the import definition. The locale controls e.g. decimal-separator interpretation.

## Task status

`taskState` values (shared by import, export, delete, and process tasks):

| State | Meaning |
|---|---|
| `NOT_STARTED` | Scheduled, not running yet |
| `IN_PROGRESS` | Running |
| `COMPLETE` | Finished — **successful or not**; check `result.successful` |
| `CANCELLING` | Cancellation in progress |
| `CANCELLED` | Cancelled; changes **rolled back** |

Response fields: `currentStep`, `progress` (double, typically `1.0`), `result` (`successful`, `failureDumpAvailable`, `objectId`, and `details[]` with per-target messages such as `hierarchyRowsProcessed` / `lineItemRowsProcessed` — see [[15_task-codes-and-logs]]), `creationTime`.

> [!tip] Polling cadence
> Poll no more than **once every 5 seconds**; longer for long-running imports. Mind the 600 req/min tenant limit ([[03_reliability-retries-rate-limits]]).

> [!note] Task lifetime
> A `taskId` is removed when the model is unloaded (e.g. all users log out). Re-running before the old ID is purged can give the same action two different task IDs.

## Dump files

When rows fail, Anaplan keeps a **dump file** with a copy of each failed row plus `_Status_` (`W` warning / `E` error), `_Line_` and `_Error_n_` columns.

- Fetch via `GET imports/{importId}/tasks/{taskId}/dump` (works, but **chunked is strongly recommended** to avoid timeouts on big dumps).
- Chunked: `GET …/dump/chunks` → list; `GET …/dump/chunks/{n}` → chunk (≤ 10 MB, numbered from 0); concatenate on your side.
- Retention: removed **48 h after last access** or on the next error-free run of the same import; kept **per user** and overwritten when that user re-runs the import. Only the latest errored task ID keeps a dump even though older tasks may still show `failureDumpAvailable: true` → a purged dump returns **404**.
- `?sort=-creationDate` on the task list can surface other users' tasks whose dumps you can't access.
- Only imports (and processes containing imports) produce dump files; **deletes never do**.

## Related

- [[11_file-upload-and-download]] · [[13_export-actions]] · [[14_model-actions-delete-and-process]] · [[15_task-codes-and-logs]]
- [[../../patterns/data-loading-best-practices|Data loading best practices]] — what makes imports fail (keys, parents, formats)
- [[../../patterns/hierarchy-load-from-file|Hierarchy load from file]]
