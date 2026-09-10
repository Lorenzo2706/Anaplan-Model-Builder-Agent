---
title: Integration API — Bulk & Large-Volume Data
type: concept
tags: [anaplan, integration-api, bulk-api, chunking, large-volume-read, files]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Large volume list item data.md
  - raw/docs/Large volume view data.md
  - raw/docs/Initiate large read request.md
  - raw/docs/Initiate large read request for view data.md
  - raw/docs/Retrieve status of large read request.md
  - raw/docs/Retrieve status of large read request 1.md
  - raw/docs/Download pages.md
  - raw/docs/Download pages 1.md
  - raw/docs/Delete read requests for list item data.md
  - raw/docs/Delete read requests for view data.md
  - raw/docs/Files and chunked data transfer.md
  - raw/docs/Private and default files for Bulk APIs.md
---

# Integration API — Bulk & Large-Volume Data

Two related but distinct mechanisms exist for data that's too big for a single transactional call: **large-volume read requests** (asynchronous, paged extraction of a list or view beyond the 1,000,000-record/cell cap — see [[06_lists-and-dimension-items|Lists]] and [[08_cell-data-read-write|Cell Data]]), and **chunked file transfer** (the upload/download mechanism behind imports and exports). Both require **Workspace Administrator** authority.

## Large-volume read requests (lists & views)

Use these when a standard list-item or view-data request would exceed its 1,000,000-record/cell cap. The pattern is the same for lists and views — only the path differs.

| Step | List endpoint | View endpoint |
|---|---|---|
| 1. Initiate | `POST /workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestID}` | `POST /workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/` (body: `{"exportType": "TABULAR_MULTI_COLUMN"}`) |
| 2. Check status | `GET .../lists/{listId}/readRequests/{requestID}` | `GET .../views/{viewId}/readRequests/{requestId}` |
| 3. Download a page | `GET .../lists/{listId}/readRequests/{requestId}/pages/{pageNo}` → CSV | `GET .../views/{viewId}/readRequests/{requestId}/pages/{pageNo}` → CSV |
| 4. Clean up | `DELETE .../lists/{listId}/readRequests/{requestId}` | `DELETE .../views/{viewId}/readRequests/{requestId}` |

### Request states

`requestState` values returned by the status check: `NOT_STARTED` (check again later), `IN_PROGRESS` (not finished, but `availablePages` pages can already be downloaded), `COMPLETE` + `successful: true` (all pages ready), `COMPLETE` + `successful: false` (export failed — delete it and start a new one), `CANCELLED` (completed via a `DELETE` call).

> [!warning]
> On a failed export (`COMPLETE` / `successful: false`), delete the failed request before initiating a new one for the same list/view.

### Downloading pages

- Page numbers are **zero-based** — `availablePages: 10` means pages `0` through `9` are downloadable.
- Pages can be downloaded **while the export is still in progress**, up to the `availablePages` count reported by the status check — no need to wait for `COMPLETE`.
- Response is `text/csv`.

### Cleanup and expiration

- Delete a read request as soon as all pages are downloaded — this frees file-store space for future exports (an explicit best practice in the docs, not just housekeeping).
- `DELETE` on a request that's `IN_PROGRESS` cancels it (`requestState` becomes `CANCELLED`); `DELETE` on a completed request just removes its pages.
- **Auto-expiration**: 30 minutes of no activity on a request reclaims its space automatically. The 30-minute timer **resets** whenever a page number divisible by 100 is requested (including page 0) — so a slow, steady page-by-page download of a very large export can keep resetting its own clock.

## Files & chunked data transfer

Applies to import/export **files**, not to the large-volume read requests above. Use chunking when: resuming an interrupted upload matters, streaming data from a source without holding it all in memory, uploading a file over 1 MB, or downloading an exported file in multiple parts.

File metadata (from the file list endpoint):

| Property | Meaning |
|---|---|
| `id` | File ID |
| `name` | File name |
| `chunkCount` | Number of chunks |
| `delimiter` / `separator` | Delimiter character(s) used |
| `encoding` | File encoding |
| `format` | File format |
| `headerRow` | Row containing column names |
| `firstDataRow` | First row after the header |

Export files carry fewer metadata properties than import files.

### Chunked workflow

**Import:**
1. Upload the file or file chunks.
2. Mark the upload complete.
3. Start the import task.
4. Poll the import task until it completes.
5. If it has failures, check/download dump files.

**Export:**
1. Start the export task.
2. Poll the export task until it completes.
3. Get the export file.
4. Get the chunks in the file.
5. Download each chunk.

Recommended import chunk size: **1–50 MB**, default **10 MB** (final chunk may be smaller) — see [[01_overview#resource-structure-and-path-parameters|`{chunkId}` in the resource-structure table]].

## Private vs. default files

- **Private files** are created when the API is used to upload a file or run a file export. A private import file is accessible only to the user who uploaded it; a private export file only to the user who ran the export.
- Private files are **auto-removed if unused for 48 hours**. If a private file no longer exists for a file import data source or export action, the **default file** is used instead.
- **Default files** exist when no private file is present; they're configured as **Admins only** or **Everyone**, and can only be set/changed via the Anaplan UI (not the API).
  - Admins-only default file → non-admin API callers get `404 Not Found`.
  - Everyone default file → all tenant users can download it.
  - A caller's own private file (if one exists from their own import/export) always takes precedence over the default.

## Related

- [[01_overview|Integration API — Overview]] — chunking and paging in the wider system-behavior context
- [[03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]] — retrying individual chunk uploads rather than the whole transfer
- [[06_lists-and-dimension-items|Lists & Dimension Items]] — the 1,000,000-record cap this mechanism exists to bypass
- [[08_cell-data-read-write|Cell Data — Read & Write]] — the 1,000,000-cell cap this mechanism exists to bypass
