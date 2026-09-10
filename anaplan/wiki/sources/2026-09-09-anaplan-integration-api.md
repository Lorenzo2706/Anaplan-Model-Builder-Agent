---
title: Anaplan Integration API v2.0 — Anapedia Clipping Batch (70 files)
type: source
tags: [anaplan, integration-api, rest, clippings, sources]
created: 2026-09-09
updated: 2026-09-09
sources: [raw/docs/Integration API v2.0.md]
---

# Anaplan Integration API v2.0 — Anapedia Clipping Batch (70 files)

**Raw:** 70 Anapedia web clippings landed in `Clippings/` and were moved to `raw/docs/` on ingest (per the vault's Clippings-is-a-landing-folder convention). Entry point: [[raw/docs/Integration API v2.0|Integration API v2.0]].

First-time ingest of the Anaplan Integration API v2.0 reference documentation — a complete generic (customer-agnostic) topic, so it lands entirely under `anaplan/` per Client Resolution. No prior Integration API content existed in this wiki.

## Scope of the batch

70 Anapedia pages covering: getting started, core object model, system behavior/design, resource structure/path parameters, request/response formats, authentication/access/permissions, model-busy behavior and retry strategy, workspace and model endpoints (including lifecycle: status/close/wake/bulk-delete), model calendar and version endpoints, list endpoints (CRUD, metadata, dimension-item lookup), module/view/line-item metadata endpoints, cell-data read and write, large-volume read requests for lists and views, chunked file transfer and private/default files, and user endpoints.

## Wiki pages created

New sub-collection `wiki/concepts/integration-api/` (10 pages + index), mirroring the "anaplan concepts" sub-collection pattern:

- [[wiki/concepts/integration-api/index|Integration API — Index]]
- [[wiki/concepts/integration-api/01_overview|Overview]] — object model, system behavior, resource structure, request/response formats, export layout types
- [[wiki/concepts/integration-api/02_authentication-and-permissions|Authentication, Access & Permissions]]
- [[wiki/concepts/integration-api/03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]]
- [[wiki/concepts/integration-api/04_workspaces-and-models|Workspaces & Models]]
- [[wiki/concepts/integration-api/05_model-calendar-and-versions|Model Calendar & Versions]]
- [[wiki/concepts/integration-api/06_lists-and-dimension-items|Lists & Dimension Items]]
- [[wiki/concepts/integration-api/07_modules-views-line-items|Modules, Views & Line Items]]
- [[wiki/concepts/integration-api/08_cell-data-read-write|Cell Data — Read & Write]]
- [[wiki/concepts/integration-api/09_bulk-and-large-volume-data|Bulk & Large-Volume Data]]
- [[wiki/concepts/integration-api/10_users|Users]]

## Design decision: grouped pages, not one page per endpoint

Per the function-pages policy precedent in `CLAUDE.md` (don't create one page per Anapedia function — categorize and compare instead), this ingest does **not** create 70 individual wiki pages mirroring the 70 raw docs 1:1. Several raw docs are one-paragraph stub/intro pages (e.g. "Model lists.md", "Model information.md", "Large volume view data.md") whose only content is a topic sentence pointing at child endpoint pages — these stubs' content is folded into the relevant grouped page's intro rather than getting their own wiki page. Each of the 10 pages groups a coherent workflow area and cites every raw doc it draws from in its `sources:` frontmatter.

## Notable cross-cutting facts worth flagging

- **Rate limit**: flat 600 requests/minute per tenant (10 req/s), token-bucket algorithm — see [[wiki/concepts/integration-api/03_reliability-retries-rate-limits|Reliability, Retries & Rate Limits]].
- **Two different 1,000,000 caps**: list-item reads and dimension-item reads cap at 1,000,000 records; view cell-data reads cap at 1,000,000 cells. Both are bypassed the same way — large-volume read requests (list or view flavor) — see [[wiki/concepts/integration-api/09_bulk-and-large-volume-data|Bulk & Large-Volume Data]].
- **Transactional cell writes** cap at 100,000 cells or 15 MB per call (whichever is lower) and can never touch aggregate cells — including any cell made aggregate by [[wiki/concepts/anaplan concepts/14_modules#breakback|Breakback]].
- **Wake up model** carries an explicit fair-use policy prohibiting keep-alive polling patterns.
- **TLS 1.3** is the documented target for new integrations; TLS 1.1 is unsupported.
- Almost every Workspace-Administrator-gated endpoint returns `404 Not Found` (not `403`) when the caller lacks module-level read access — a permissions problem can look identical to a missing-resource problem.

## Related

- [[wiki/patterns/index|Patterns index]] — DISCO and data-loading best practices pair with the import/export workflows this API drives
