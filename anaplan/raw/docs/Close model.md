---
title: "Close model"
source: "https://help.anaplan.com/close-model-055d2f9e-901c-490f-a971-c9c64f4f6698"
author:
published:
created: 2026-09-09
description: "This endpoint enables a workspace administrator to close a model without having to wait for a time-out. This is particularly useful for root cause analysis when an error occurs."
tags:
  - "clippings"
---
[Model information](https://help.anaplan.com/model-information-c2998f80-d007-4a36-aef0-485923a38045 "Model information")

This endpoint enables a workspace administrator to close a model without having to wait for a time-out. This is particularly useful for root cause analysis when an error occurs.

This supports administrative control and troubleshooting, especially when a model needs to be closed for root cause analysis or maintenance.

To use this endpoint, you must supply a valid authentication and the model id.

POST

`/workspaces/{workspaceId}/models/{modelId}/close`

| **Parameter** | **Description** |
| --- | --- |
| `workspaceId` | - Required - Type: string - Description: The workspace ID - Example: `8a8b8c8d8e8f8g8i` |
| `modelId` | - Required - Type: string - Description: The model ID - Example: `FC12345678912343455667` |

`curl -X POST \   https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/close \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'   -H 'Content-Type: application/json'`

A successful close action will provide a `200 OK` response.

A successful close action will provide a `200 No content` response.

An unsuccessful close action will provide a `401 Unauthorized` response if a valid authentication token was not provided.

An unsuccessful close action will provide a `403 Forbidden` response if your user authentication lacks workspace administrator permissions.

An unsuccessful close action will provide a `404 Not found` response if the {modelId} or {workspaceId} is not found.

An unsuccessful close action will provide a `422 Unprocessable identity` response if the model is currently in a state that cannot process the action, for example, if the model is archived.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fclose-model-055d2f9e-901c-490f-a971-c9c64f4f6698&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top