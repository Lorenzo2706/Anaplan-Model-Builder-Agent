---
title: Integration API — Export Actions
type: concept
tags: [anaplan, integration-api, bulk-api, export, tasks]
created: 2026-10-23
updated: 2026-10-23
sources:
  - raw/docs/Anaplan Integration API V2 Guide and Reference.md
---

# Integration API — Export Actions

Running a saved **export action** and downloading its output. An API export creates a **private file** readable only by the user who ran it ([[09_bulk-and-large-volume-data#private-vs-default-files]]). Base path: `…/workspaces/{workspaceId}/models/{modelId}/`.

## Workflow

1. `GET exports` → find the `exportId`.
2. *(optional)* `GET exports/{exportId}` → metadata.
3. `POST exports/{exportId}/tasks` body `{"localeName":"en_US"}` → `taskId`.
4. `GET exports/{exportId}/tasks/{taskId}` until `COMPLETE` and `result.successful: true`.
5. `result.objectId` is the **file ID** of the export; download it via [[11_file-upload-and-download#download|chunked download]].

## Endpoints

| Purpose | Request |
|---|---|
| List exports | `GET exports` → `{id, name, exportType}` (e.g. `TABULAR_MULTI_COLUMN`, `GRID_CURRENT_PAGE` — see export layouts in [[01_overview]]) |
| Export metadata | `GET exports/{exportId}` → `columnCount`, `dataTypes[]`, `delimiter`, `encoding`, `exportFormat` (e.g. `text/csv`), `headerNames[]`, `listNames[]`, `rowCount`, `separator` |
| Start | `POST exports/{exportId}/tasks` |
| List tasks | `GET exports/{exportId}/tasks` |
| Status / cancel | `GET` / `DELETE exports/{exportId}/tasks/{taskId}` |

- `dataTypes`: with **line items in columns** each column shows its type (`ENTITY` = a list member); with line items in **rows or pages** Anaplan can't know types and returns `MIXED`.
- `rowCount` is an **estimate**; the actual file may differ slightly.
- Missing `{"localeName":"en_US"}` → `400 Bad Request` ([[12_import-actions#endpoints]]).
- Status poll: ≤ once per 5 s. `taskState` values as in [[12_import-actions#task-status]]. Exports have no dump file (`failureDumpAvailable: false`).

## Gotchas

- **Excel layouts have hard limits**: 256 columns, 65,536 rows (`msgTooManyColumns` / `msgTooManyRows`) — use CSV/text for anything larger ([[15_task-codes-and-logs]]).
- For very large views/lists that exceed standard read caps, use the **large-volume read requests** instead ([[09_bulk-and-large-volume-data]]).
- A user who has no private file falls back to the **default file**; admins-only defaults return `404` to end users.

## Related

- [[11_file-upload-and-download]] · [[12_import-actions]] · [[14_model-actions-delete-and-process]]
