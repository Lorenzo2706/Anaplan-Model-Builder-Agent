---
title: "Initiate large read request for view data"
source: "https://help.anaplan.com/initiate-large-read-request-for-view-data-c1310d70-1d24-44bf-8152-6abd0e6520d4"
author:
published:
created: 2026-09-09
description: "Use this call to initiate a large volume read request of view data. This enables you to read data from views that are larger than a million cell count."
tags:
  - "clippings"
---
Use this call to initiate a large volume read request of view data. This enables you to read data from views that are larger than a million cell count.

This starts an asynchronous data extraction process when the view contains too much data to retrieve efficiently in a single lightweight request.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- Use the [Delete read requests](https://help.anaplan.com/71a6b2da-008c-40e7-ba05-103730de30b2) call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.

POST

`/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/`

| **Parameters** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001` |

`curl --location --request POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/' \   --header 'Authorization: AnaplanAuthToken AnaplanToken' \   --header 'Accept: application/json'   --data-raw '{   "exportType" : "TABULAR_MULTI_COLUMN"   }'`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"       },       "status": {           "code": 200,           "message": "Success"       },       "viewReadRequest": {           "requestId": "0A06B0739F0E47BB92E2326C603D86EC",           "requestState": "IN_PROGRESS",           "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}"       }   }`

If the request is just submitted and not started, the response resembles:

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"       },       "status": {           "code": 200,           "message": "Success"       },       "viewReadRequest": {           "requestId": "0A06B0739F0E47BB92E2326C603D86EC",           "requestState": "NOT_STARTED",           "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/view/{viewId}/readRequests/{requestId}"       }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Finitiate-large-read-request-for-view-data-c1310d70-1d24-44bf-8152-6abd0e6520d4&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top