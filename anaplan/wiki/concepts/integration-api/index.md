---
title: Integration API — Index
type: index
tags: [anaplan, index, integration-api]
created: 2026-09-09
updated: 2026-09-09
---

# Integration API — Index

10 pages covering the Anaplan Integration API v2.0 (REST), synthesized from a 70-file Anapedia clipping batch. Individual raw docs remain in `raw/docs/` for endpoint-level detail (exact curl examples, full JSON payloads); these pages group them by workflow so you don't need to open 70 files to answer "how do I move data via the API."

---

## Foundations

| Page | File | Covers |
|---|---|---|
| [[01_overview]] | `01_overview.md` | Object model (tenant→workspace→model→module→view→line item), system behavior, resource/path parameters, request/response formats, export layout types |
| [[02_authentication-and-permissions]] | `02_authentication-and-permissions.md` | Permission evaluation chain, Workspace Administrator vs. model-role access, TLS requirement, permission error codes |
| [[03_reliability-retries-rate-limits]] | `03_reliability-retries-rate-limits.md` | Model-busy behavior, retryable vs. non-retryable status codes, 600 req/min rate limit, retry algorithm |

## Object-specific endpoints

| Page | File | Covers |
|---|---|---|
| [[04_workspaces-and-models]] | `04_workspaces-and-models.md` | Workspace/model discovery, model lifecycle (status, close, wake up), bulk delete |
| [[05_model-calendar-and-versions]] | `05_model-calendar-and-versions.md` | Fiscal year, current period, version metadata, switchover dates |
| [[06_lists-and-dimension-items]] | `06_lists-and-dimension-items.md` | List CRUD, list metadata, numbered-list index reset, dimension-item lookup/resolution |
| [[07_modules-views-line-items]] | `07_modules-views-line-items.md` | Module/view discovery, view dimension metadata, line item metadata, line-item dimension lookup |
| [[08_cell-data-read-write]] | `08_cell-data-read-write.md` | Reading view cell data (CSV/JSON), writing module cells transactionally, aggregate-cell write restrictions |
| [[09_bulk-and-large-volume-data]] | `09_bulk-and-large-volume-data.md` | Large-volume read requests (lists & views, beyond the 1M cap), chunked file transfer, private vs. default files |
| [[10_users]] | `10_users.md` | Authenticated-user identity, user lookup, user list |

## Related domains

- [[../index|Concepts index]]
- [[../../patterns/index|Patterns index]] — DISCO, data-loading best practices pair naturally with import/export workflows
- [[../../sources/2026-09-09-anaplan-integration-api|Source: Anapedia Integration API clipping batch]]
