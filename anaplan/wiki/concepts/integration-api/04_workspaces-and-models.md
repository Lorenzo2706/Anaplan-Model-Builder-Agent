---
title: Integration API — Workspaces & Models
type: concept
tags: [anaplan, integration-api, workspaces, models, model-lifecycle]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Workspace endpoints.md
  - raw/docs/List user workspaces.md
  - raw/docs/Retrieve workspace information.md
  - raw/docs/Model information.md
  - raw/docs/Retrieve models.md
  - raw/docs/Retrieve a specific model.md
  - raw/docs/Retrieve model IDs from workspace.md
  - raw/docs/Check model status.md
  - raw/docs/Close model.md
  - raw/docs/Wake up model.md
  - raw/docs/Bulk delete models.md
---

# Integration API — Workspaces & Models

Workspace endpoints discover and inspect the workspaces a user can access; they don't move planning data themselves — they establish context for the model-specific calls that follow. Model endpoints discover, inspect, validate, and administer models the user can access.

All Workspace Administrator requirements below are per-workspace/per-model, not tenant-wide.

## Workspaces

| Endpoint | Method & path | Notes |
|---|---|---|
| List user workspaces | `GET /workspaces?tenantDetails=true` | Workspaces the user can access in their default tenant; `tenantDetails=true` adds `currentSize`/`sizeAllowance` |
| Retrieve workspace information | `GET /workspaces/{workspaceId}?tenantDetails=true` | Info on one workspace, if accessible |
| Retrieve model IDs from workspace | `GET /workspaces/{workspaceId}/models?modelDetails=true` | Models within a known workspace; `modelDetails=true` adds memory usage |

Example response shape (workspace):

```json
{
  "workspaces": [
    { "id": "8a8b8c8d8e8f8g8i", "name": "Financial Planning", "active": true,
      "sizeAllowance": 1073741824, "currentSize": 873741824 }
  ]
}
```

## Models

| Endpoint | Method & path | Auth requirement |
|---|---|---|
| Retrieve models | `GET /models` | Returns models in the user's default tenant (or only accessible models for non-admins). No offset/limit → capped at first 5000 models; use `offset`/`limit` to page |
| Retrieve a specific model | `GET /models/{modelId}` | `modelDetails=true` adds memory usage + status info |
| Retrieve model IDs from workspace | `GET /workspaces/{workspaceId}/models?modelDetails=true` | Scoped to one workspace |
| Bulk delete models | `POST /workspaces/{workspaceId}/bulkDeleteModels` | **Workspace Administrator.** Destructive — models must be **closed** first |

Model object fields worth knowing: `id`, `activeState` (`UNLOCKED`/`ARCHIVED`), `name`, `currentWorkspaceId`/`currentWorkspaceName`, `modelUrl`, `memoryUsage`, `lastSavedSerialNumber`, `lastModifiedByUserGuid`, `isoCreationDate`, `lastModified`, `categoryValues` (tenant-defined model categorization).

### Bulk delete models — behavior

- Body: `{"modelIdsToDelete": ["<id1>", "<id2>", ...]}`.
- Partial failures don't block the rest: one model failing to delete (e.g. not closed, or no access) does not prevent deletion of the others. Response includes `modelsDeleted` count and a `bulkDeleteModelsFailures` array with per-model messages (e.g. `"Model is open. Please close the model before trying again."`).
- `400` — malformed body, unrecognised property, or missing `modelIdsToDelete`. `403` — not a workspace administrator. `404` — workspace ID not found.

> [!warning]
> Destructive. Always close target models first and double-check the `modelIdsToDelete` list before calling.

## Model lifecycle: status, close, wake

### Check model status

`POST /workspaces/{workspaceId}/models/{modelId}/status`

Actions like imports, exports, and writeback require exclusive access and **lock** the model — reads via the API are blocked during that exclusive transaction. This endpoint reports whether the model is currently locked, so an integration can avoid conflicting operations.

Response `requestStatus.currentStep` values:

| `currentStep` | Meaning |
|---|---|
| `Open` | No process running |
| `Processing` | An import/export task is running |
| `Updating` | An update is in progress (e.g. a cell write) |
| `Closed` | Model is in maintenance state |

`requestStatus.tooltip` carries human-readable detail (who started the transaction, when, and current progress); `requestStatus.progress` is a 0–1 fraction (or `-1.0` when not applicable).

### Close model

`POST /workspaces/{workspaceId}/models/{modelId}/close` — **Workspace Administrator.** Closes a model immediately without waiting for a timeout; useful for root-cause analysis after an error, or before administrative actions like [[#bulk-delete-models|bulk delete]].

| Response | Meaning |
|---|---|
| `200 OK` / `204 No Content` | Closed successfully |
| `401 Unauthorized` | No valid auth token |
| `403 Forbidden` | Caller lacks Workspace Administrator permission |
| `404 Not Found` | `{modelId}` or `{workspaceId}` not found |
| `422 Unprocessable Entity` | Model can't process the action right now (e.g. already archived) |

### Wake up model

`POST /workspaces/{workspaceID}/models/{modelID}/open` — **Workspace Administrator.** Wakes a model (from closed, or promotes it from metadata-only to a full data load). Useful to pre-warm a large model before builders or a scheduled process need it.

| Response | Meaning |
|---|---|
| `200 OK` | Model is open, or opened very quickly |
| `202 Accepted` | Model is opening / promoting from metadata-only |
| `404 Not Found` | Resource disabled, called too frequently, insufficient permissions, or model deleted |
| `422 Unprocessable Content` | Model is archived |
| `424 Failed Dependency` | Model is in maintenance |

> [!warning] Fair use policy
> This endpoint is for standard operational use, not for artificially keeping a model loaded. Anaplan explicitly prohibits: repeated "keep-alive" opens of an already-open model, opening/querying many models simultaneously, and repeated opens intended to prevent the normal 60-minute unaccessed-model offload. Anaplan monitors usage patterns for this.

## Related

- [[01_overview|Integration API — Overview]] — the tenant → workspace → model object chain
- [[03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]] — what `422`/`423`/`424`/`425` mean and how to recover
- [[05_model-calendar-and-versions|Model Calendar & Versions]]
- [[10_users|Users]] — the authenticated-user identity these calls run under
