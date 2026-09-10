---
title: "Retrieve status of large read request"
source: "https://help.anaplan.com/retrieve-status-of-large-read-request-640995fc-1d90-4f4a-9292-f9bceb64353f"
author:
published:
created: 2026-09-09
description: "Use this call to check the status of an export action after a bulk data long request is initiated. You can use it to check how many pages are available to download."
tags:
  - "clippings"
---
Use this call to check the status of an export action after a bulk data long request is initiated. You can use it to check how many pages are available to download.

This lets an integration monitor progress and determine when the requested data is ready to download.

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

GET

`/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}`

| **Parameters** | **Details** |
| --- | --- |
| `{workspaceId}` |  |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |

`curl -X GET /   'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

- When `requestState` is `COMPLETE` and `successful` is `true`, the export has completed successfully and the user can download all the pages.
- When `requestState` is `COMPLETE` and `successful` is `false`, this means the export failed. Retry and initiate a new export.
- When `requestState` is `IN_PROGRESS` the export has not yet completed, but you can download the available pages indicated by the `availablePages` field.
- When `requestState` is `NOT_STARTED` then simply check the status again.
- When `requestState` is `CANCELLED` then this request is completed by a 'DELETE' call.

We recommend you delete the last failed export before initiating a new export, using the delete export endpoint.

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"       },       "status": {           "code": 200,           "message": "Success"       },       "viewReadRequest": {           "requestId": "0A06B0739F0E47BB92E2326C603D86EC",           "viewId": 101000000014,           "requestState": "COMPLETE",           "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}",           "availablePages": 100,           "successful": true       }   }`

Following is the response when the large read request is in progress.

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"       },       "status": {           "code": 200,           "message": "Success"       },       "viewReadRequest": {           "requestId": "0A06B0739F0E47BB92E2326C603D86EC",           "viewId": 101000000014,           "requestState": "IN_PROGRESS",           "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}",           "availablePages": 50,           "successful": true       }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-status-of-large-read-request-640995fc-1d90-4f4a-9292-f9bceb64353f&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top