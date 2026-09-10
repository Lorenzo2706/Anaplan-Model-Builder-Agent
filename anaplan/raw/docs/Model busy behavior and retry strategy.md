---
title: "Model busy behavior and retry strategy"
source: "https://help.anaplan.com/model-busy-behavior-and-retry-strategy-27b77b79-7db1-4973-953a-fc585969fa43"
author:
published:
created: 2026-09-09
description: "API calls can behave differently when a model is busy. A model can become busy because of ongoing model actions, automation, maintenance, imports, exports, processes, delete actions, calculations, or writeback activity."
tags:
  - "clippings"
---
API calls can behave differently when a model is busy. A model can become busy because of ongoing model actions, automation, maintenance, imports, exports, processes, delete actions, calculations, or writeback activity.

When you build an integration, design it to handle model state, rate limits, and temporary failures without immediately escalating or retrying too aggressively.

Some API calls can still return information while the model is busy. Other calls wait for the model to become available before they complete.

The following action-related endpoints can return information even if the model is busy.

| **Action type** | **Endpoints** |
| --- | --- |
| Import action | Get the import ID; start the import; get a list of import tasks; monitor import tasks; check dump files for failures; download dump file chunks; get metadata for an import definition. |
| Export action | List available export definitions as a JSON array; get metadata for an export definition; start the export; monitor export tasks. |
| Process action | List process definitions available in a model as a JSON array; retrieve metadata for a process; start the process; monitor process tasks; check dump files for failures. |
| Delete action | List actions in the model as a JSON array; start deletion; monitor deletion tasks. |

All other endpoints wait for the model to become available again before completing their run.

Imports, exports, processes, and writeback activity can make the model busy. Before you escalate a failure or retry repeatedly, check the model status where your integration flow supports it.

If the model is temporarily unavailable, waiting and retrying is usually better than immediately starting another conflicting request.

Some response codes indicate that the model cannot currently complete the request because of its state.

| **Status code** | **Meaning** | **Recommended action** |
| --- | --- | --- |
| `422 Model archived` | The model you are trying to access has been archived. | Unarchive the model, then try the request again. |
| `423 Model locked` | The model you are trying to update is locked. | Unlock the model, then try the request again. |
| `424 Model offline` | The model you are trying to access is offline. | Bring the model online, then retry the request. |
| `425 Model deployed` | The model you are trying to change is in deployed mode. | Make the change in the development model instead. |

Some responses are temporary and can be retried.

| **Status code** | **Meaning** | **Recommended action** |
| --- | --- | --- |
| `410 Gone` | The requested resource, such as a workspace, has been moved. | Try the request again. The request is rerouted and should succeed on a later attempt. |
| `429 Too Many Requests` | Too many requests were made. | Wait, then retry. Use the `Retry-After` header when it is returned. |
| `502 Bad Gateway` | Network problems. | Wait, then retry. |
| `503 Service unavailable` | The service is unable to accept the request. | Wait, then retry. |
| `504 Gateway Timeout` | Network problems. | Wait, then retry. |

The Integration API has a flat rate limit of 600 requests per minute. This is equivalent to 10 requests per second.

The rate limit applies at the tenant level, so all workspaces in a tenant share the same limit.

Rate limiting uses a token bucket algorithm:

- A token is added to the bucket every 0.1 seconds.
- The bucket holds up to 600 tokens.
- Each request removes one token.
- When the bucket is empty, requests are denied.

If your integration reaches the request-per-second limit, the API returns `429 Too Many Requests`.

The `429` response can include a `Retry-After` header. Use this value to determine how long to wait before retrying.

If your integration receives a `429` response, use a timeout before retrying. A 10-second timeout is recommended.

Use a retry strategy that avoids adding more load when the model or API is already under pressure.

Recommended approach:

1. Check the response code.
2. If the response is caused by request content, authentication, or permissions, fix the request instead of retrying.
3. If the response indicates model state, such as archived, locked, offline, or deployed, resolve the model state before retrying.
4. If the response is `429`, wait before retrying. Use the `Retry-After` header when available.
5. If the response is a temporary network or service error, wait briefly and retry.
6. Avoid starting conflicting actions against the same model in parallel unless the workflow has been tested for concurrency.

Not every failed response should be retried.

Do not retry without changing the request when the response indicates:

| **Status code** | **Meaning** |
| --- | --- |
| `400 Bad Request` | The request is incorrect or missing required values. |
| `401 Unauthorized` | The credentials are incorrect or the token has expired. |
| `403 Forbidden` | The user does not have permission to perform the requested action. |
| `404 Not Found` | The resource does not exist, or the user does not have permission to see it. |
| `405 Method Not Allowed` | The request used the wrong HTTP method for the endpoint. |
| `406 Not Acceptable` | The requested response format cannot be provided. |
| `409 Conflict` | The request attempts to change a resource in a way that is not allowed. |
| `415 Unsupported Media Type` | The request body is in an unsupported format. |

For these responses, inspect the request, endpoint, headers, body, permissions, and model state before trying again.

When designing integrations:

- Poll long-running tasks instead of assuming they have completed.
- Avoid launching multiple conflicting model actions at the same time.
- Treat `429`, `502`, `503`, and `504` as temporary conditions.
- Use `Retry-After` when it is returned.
- Use a fixed wait, such as 10 seconds, for rate-limit retries if no better retry timing is available.
- Check model status before escalating failures caused by model availability.
- Build retries around individual steps where possible, such as retrying a failed file chunk upload rather than restarting an entire import workflow.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fmodel-busy-behavior-and-retry-strategy-27b77b79-7db1-4973-953a-fc585969fa43&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>