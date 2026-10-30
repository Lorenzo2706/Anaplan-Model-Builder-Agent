---
title: Integration API — File Upload & Download for Actions
type: concept
tags: [anaplan, integration-api, bulk-api, files, chunking, upload, download]
created: 2026-10-23
updated: 2026-10-23
sources:
  - raw/docs/Anaplan Integration API V2 Guide and Reference.md
---

# Integration API — File Upload & Download for Actions

Step-by-step endpoint reference for moving files in and out of a model so that **import** ([[12_import-actions]]) and **export** ([[13_export-actions]]) actions can use them. Concepts (private vs. default files, chunk sizing rationale) are in [[09_bulk-and-large-volume-data]]; this page is the endpoint sequence.

> [!note] Base URL and auth
> All paths are under `https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/…` with header `Authorization: AnaplanAuthToken {token}`. See [[02_authentication-and-permissions]].

## Upload

> [!warning] The file must already exist in the model
> The API can only upload to an **existing** file (import data source). A file never loaded before must first be uploaded once via the Anaplan UI; afterwards the API can replace it.

Uploads create a **private file** (see [[09_bulk-and-large-volume-data#private-vs-default-files]]).

| Step | Verb + path | Notes |
|---|---|---|
| 1. Find the file ID | `GET …/files` | Returns `id`, `name`, `chunkCount`, `delimiter`, `encoding`, `format`, `headerRow`, `firstDataRow`, `separator`. Lists import **and** export files |
| 2. Set chunk count | `POST …/files/{fileId}` body `{"chunkCount": N}` | `-1` = unknown count; you must then call `complete` at the end |
| 3a. Single chunk | `PUT …/files/{fileId}` `Content-Type: application/octet-stream` | Cannot be compressed; prefer for files < 1 MB |
| 3b. Multiple chunks | `PUT …/files/{fileId}/chunks/{chunkId}` (chunk IDs from `0`) | Octet-stream, or `application/x-gzip` if the chunk is gzip-compressed |
| 4. Complete (only if `chunkCount = -1`) | `POST …/files/{fileId}/complete` body `{"id":…,"name":…,"chunkCount":N,"firstDataRow":…,"headerRow":…}` | Returns the updated file metadata |

Successful `PUT`s return `204 No Content`.

> [!important] Set the chunk count first
> If the file's default is set to **Admins only** or **Everyone**, you **must** set the chunk count *before* uploading.

### Chunking guidance

- Chunk size ≤ **50 MB uncompressed**, ≤ **1,000 chunks** per file; default 10 MB (see the `{chunkId}` row in [[01_overview]]).
- **Compress** chunks to cut upload time (gzip; recommended for single chunks > 50 MB). Send `Content-Type: application/x-gzip`.
- Chunk when you need to **resume** after a dropped connection, or when streaming from a database without holding the result set in memory.
- Splitting a local file: `split -b <bytes> file chunk-`; gzip all chunks: `find . -type f ! -name '*.gz' -exec gzip "{}" \;`.

## Download

| Step | Verb + path | Notes |
|---|---|---|
| 1. List files | `GET …/files` | Export files have fewer properties (`id`, `name`, `chunkCount`, `firstDataRow`, `headerRow`) and their ID starts with `116…` vs. `113…` for import files |
| 2. List chunks | `GET …/files/{fileId}/chunks` | Returns `[{id:"0", name:"Chunk 0"}, …]` |
| 3. Get a chunk | `GET …/files/{fileId}/chunks/{chunkId}` | Raw data; download sequentially and concatenate |
| 4. Delete | `DELETE …/files/{fileId}` → `204` | Removes **private** content only; default file and the import data source object remain |

> [!note] ID prefixes
> Object IDs carry a type prefix: `112…` imports, `113…` import data source files, `116…` exports/export files, `117…` actions, `118…` processes. Useful for sanity-checking which kind of object an ID refers to (observed in the reference examples, not formally documented as a contract).

## Pagination of file lists

`GET …/files?sort=name&limit=2&offset=1` — the `meta.paging` block returns `currentPageSize`, `offset`, `totalSize`, and `next`/`previous` URLs. Paging controls how many *results* are returned, not how many chunks a file has. See [[01_overview]].

## Related

- [[09_bulk-and-large-volume-data]] — concepts, private/default files, large-volume reads
- [[12_import-actions]], [[13_export-actions]] — the actions that consume/produce these files
- [[15_task-codes-and-logs]] — `uploadedFileNoLongerAvailable` and other file-related codes
