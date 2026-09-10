---
title: Integration API — Reliability, Retries & Rate Limits
type: concept
tags: [anaplan, integration-api, retry, rate-limit, model-busy, reliability]
created: 2026-09-09
updated: 2026-09-09
sources:
  - raw/docs/Model busy behavior and retry strategy.md
---

# Integration API — Reliability, Retries & Rate Limits

A model can become **busy** because of ongoing actions, automation, maintenance, imports, exports, processes, delete actions, calculations, or writeback activity. Integrations must handle model state, rate limits, and temporary failures without escalating or retrying too aggressively.

## What still works while a model is busy

Some action-related endpoints return information even while the model is busy; everything else waits for the model to become available before completing.

| Action type | Endpoints that respond while busy |
|---|---|
| Import | Get the import ID; start the import; list import tasks; monitor import tasks; check dump files for failures; download dump file chunks; get import definition metadata |
| Export | List export definitions (JSON array); get export definition metadata; start the export; monitor export tasks |
| Process | List process definitions (JSON array); retrieve process metadata; start the process; monitor process tasks; check dump files for failures |
| Delete | List actions (JSON array); start deletion; monitor deletion tasks |

> [!note]
> Before escalating a failure or retrying repeatedly, check [[04_workspaces-and-models#check-model-status|model status]] where the workflow supports it. Waiting and retrying is usually better than immediately starting another conflicting request.

## Model-state responses (fix the state, then retry)

| Status code | Meaning | Recommended action |
|---|---|---|
| `422 Model archived` | Model is archived | Unarchive the model, then retry |
| `423 Model locked` | Model is locked | Unlock the model, then retry |
| `424 Model offline` | Model is offline | Bring the model online, then retry |
| `425 Model deployed` | Model is in deployed mode | Make the change in the development model instead |

## Temporary responses (safe to retry)

| Status code | Meaning | Recommended action |
|---|---|---|
| `410 Gone` | Resource (e.g. workspace) has moved | Retry — rerouted, should succeed |
| `429 Too Many Requests` | Rate limit hit | Wait, then retry — use `Retry-After` if present |
| `502 Bad Gateway` | Network problem | Wait, then retry |
| `503 Service Unavailable` | Service can't accept the request | Wait, then retry |
| `504 Gateway Timeout` | Network problem | Wait, then retry |

## Rate limiting

- Flat limit: **600 requests per minute** (≈10 requests/second) per **tenant** — shared across all workspaces in the tenant.
- Token-bucket algorithm: one token added every 0.1 s, bucket holds up to 600 tokens, each request removes one token; an empty bucket denies requests.
- A `429` response can carry a `Retry-After` header — use it to time the retry. If absent, a **10-second timeout** is the recommended default wait.

## Do NOT retry without changing the request

These responses indicate the request itself is the problem — fix it, don't retry as-is:

| Status code | Meaning |
|---|---|
| `400 Bad Request` | Incorrect or missing required values |
| `401 Unauthorized` | Credentials incorrect or token expired |
| `403 Forbidden` | No permission for the requested action |
| `404 Not Found` | Resource doesn't exist, or no permission to see it |
| `405 Method Not Allowed` | Wrong HTTP method for the endpoint |
| `406 Not Acceptable` | Requested response format can't be provided |
| `409 Conflict` | Change is not allowed in the resource's current state |
| `415 Unsupported Media Type` | Request body format unsupported |

For these, inspect the request, endpoint, headers, body, permissions, and model state before trying again.

## Recommended retry algorithm

1. Check the response code.
2. If caused by request content, authentication, or permissions → fix the request, don't retry.
3. If it indicates model state (archived/locked/offline/deployed) → resolve the model state, then retry.
4. If `429` → wait, using `Retry-After` when available.
5. If a temporary network/service error (`502`/`503`/`504`) → wait briefly, then retry.
6. Avoid starting conflicting actions against the same model in parallel unless concurrency has been tested.

## Design checklist

- Poll long-running tasks — never assume completion.
- Avoid launching multiple conflicting model actions simultaneously.
- Treat `429`, `502`, `503`, `504` as temporary conditions.
- Use `Retry-After` when returned; otherwise use a fixed wait (10 s is the documented default for rate limits).
- Check model status before escalating availability-caused failures.
- Build retries around individual steps (e.g. retry one failed file chunk upload) rather than restarting an entire import workflow.

## Related

- [[01_overview|Integration API — Overview]]
- [[04_workspaces-and-models|Workspaces & Models]] — model status/close/wake endpoints referenced above
- [[09_bulk-and-large-volume-data|Bulk & large-volume data]] — chunked transfer benefits from step-level retries
