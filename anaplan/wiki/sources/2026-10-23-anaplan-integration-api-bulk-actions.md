---
title: Anaplan Integration API V2 Guide & Reference (Apiary) + URL/IP Allowlist — Clipping Batch (2 files)
type: source
tags: [anaplan, integration-api, bulk-api, import, export, process, allowlist, clippings, sources]
created: 2026-10-23
updated: 2026-10-23
sources:
  - raw/docs/Anaplan Integration API V2 Guide and Reference.md
  - raw/docs/URL, IP, and allowlist requirements.md
---

# Anaplan Integration API V2 Guide & Reference (Apiary) + URL/IP Allowlist

**Raw:** two clippings moved from `Clippings/` to `raw/docs/` — [[raw/docs/Anaplan Integration API V2 Guide and Reference|Integration API V2 Guide and Reference]] (≈8,400 lines, Apiary export, source `anaplan.docs.apiary.io`) and [[raw/docs/URL, IP, and allowlist requirements|URL, IP, and allowlist requirements]] (Anaplan support page).

Generic (customer-agnostic) → `anaplan/`. Treated as one related batch (both are Integration API/network prerequisites).

> [!warning] Source is being sunset
> The Apiary guide carries a banner: the service is to be **decommissioned by 2026-10-31**; Anaplan points to Anapedia as the official home. This clipping is therefore a durable snapshot of the Apiary version — and the same content already lives under [[wiki/sources/2026-09-09-anaplan-integration-api|the earlier 70-file Anapedia batch]] for the transactional half.

## Overlap with the earlier ingest

The Apiary guide is a single-page consolidation of the v2.0 reference. Its **Transactional API** half (workspaces, models, line items, metadata, cell data, lists, large-volume reads, calendar, versions, users) and the introductory material (HTTP codes, rate limit, busy-model behavior, parameter types, private/default files) were **already covered** by pages 01–10 of [[wiki/concepts/integration-api/index|the Integration API collection]] and were not re-ingested. Nothing there contradicted the existing pages.

## What was new → pages created

The **Bulk API** half (action endpoints) had no wiki coverage beyond a conceptual mention:

- [[wiki/concepts/integration-api/11_file-upload-and-download|11 File Upload & Download]] — set chunk count, single/multi-chunk PUT, gzip, complete, download chunks, delete file
- [[wiki/concepts/integration-api/12_import-actions|12 Import Actions]] — import tasks, `localeName`, mapping parameters, task states, dump files and retention
- [[wiki/concepts/integration-api/13_export-actions|13 Export Actions]] — export definitions/metadata, tasks, Excel limits
- [[wiki/concepts/integration-api/14_model-actions-delete-and-process|14 Model Actions, Delete Actions & Processes]] — action list/metadata types, delete-by-selection, process tasks and nested results, `includeProcessDetails`, Optimizer log
- [[wiki/concepts/integration-api/15_task-codes-and-logs|15 Task Result Codes & Logs]] — completion, failure and data error/warning codes grouped by family

## Updated

- [[wiki/concepts/integration-api/02_authentication-and-permissions|02 Authentication & Permissions]] — new "Network allowlisting" section (inbound vs outbound, CloudWorks/ADO, region list)
- [[wiki/concepts/integration-api/index|Integration API index]] — pages 11–15 added; 09 cross-linked

## Key takeaways

- `{"localeName":"en_US"}` is **mandatory** on every task POST; omission → 400.
- Uploads only work on **pre-existing** files; chunk count must be set **before** upload when a default file exists; chunks ≤ 50 MB, ≤ 1,000 per file, gzip supported.
- Dump files: chunked download recommended, 48 h retention, per-user, deletes never produce one.
- Process results are nested — use each `nestedResults[].objectId` to fetch that step's dump.
- Excel exports cap at 256 columns / 65,536 rows.

## Gaps / flags

- The allowlist clipping contains **only region headings**; the actual IP/domain lists (tabbed content) were not captured.
- Guide's mapping examples contain two copy-paste inconsistencies (the "Run Import Process with Mapping Data" example shows an `/imports/{processId}/tasks` URL where a `/processes/…` path is meant) — pages use the process path.
- `GET /models/{modelId}/processes/{processId}` (process metadata) is documented without the `/workspaces/{workspaceId}` prefix; kept as written.
