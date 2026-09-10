---
title: "Wake up model"
source: "https://help.anaplan.com/wake-up-model-2eaefdd5-4958-4bb0-9e3c-a5457c20afed"
author:
published:
created: 2026-09-09
description: "Use this request to wake up a model (either upgrading from metadata-only, or opening from closed). As some very large models have long load times, you can build this into your automations to have them fully load before your model builders start working on them."
tags:
  - "clippings"
---
[Model information](https://help.anaplan.com/model-information-c2998f80-d007-4a36-aef0-485923a38045 "Model information")

Use this request to wake up a model (either upgrading from metadata-only, or opening from closed). As some very large models have long load times, you can build this into your automations to have them fully load before your model builders start working on them.

This helps prepare a model before users or automations need it, especially when large models may take time to load.

**Note**: To wake up a model, you must have Workspace Administrator authority in the model.

**Fair use policy**

This API endpoint is designed to support standard, day-to-day operations of your Anaplan users. Excessive or abnormal usage patterns that negatively impact system performance or stability are strictly prohibited. Examples of prohibited activity include (but are not limited to):

- Repeated requests to open models that are already open as a means of maintaining a "keep-alive", when unaccessed models time out and offload after 60 minutes.
- Requests designed to open or query a large number of models simultaneously or otherwise place excessive load on backend infrastructure.
- Repeated requests to open models that are already open as a means of artificially maintaining their loaded state. For performance and security purposes, Anaplan monitors model usage and offloads unaccessed models after a period of inactivity.

POST

`/workspaces/{workspaceID}/models/{modelID}/open`

`curl -X POST \   https://api.anaplan.com/2/0/workspaces/{workspaceID}/models/{modelID}/open \   -H 'authorization: AnaplanAuthToken {anaplan_auth_token}'`

The endpoint only returns a status code response. Possible status codes include:

| **Response** | **Reason** |
| --- | --- |
| 404 | The endpoint returns a **404 Not found** if the resource is disabled, if the request is used repeatedly over a short period of time, or if the user lacks sufficent model permissions (Workspace administrator), or if the model has been deleted. |
| 422 | The endpoint returns a **422 Unprocessable content** response if the model is archived. |
| 424 | The endpoint returns a **424 Failed dependency** response if the model is in maintenance. |
| 200 | The endpoint returns a **200 OK** response if the model is open, or opened very quickly. |
| 202 | The endpoint returns a **202 Accepted** response if the model is in the process of opening, or promotion from metadata-only mode to full data load has started. |

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fwake-up-model-2eaefdd5-4958-4bb0-9e3c-a5457c20afed&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top