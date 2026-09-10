---
title: "Delete read requests for view data"
source: "https://help.anaplan.com/delete-read-requests-for-view-data-71a6b2da-008c-40e7-ba05-103730de30b2"
author:
published:
created: 2026-09-09
description: "Use this call to delete or cancel an initiated read request. This removes all the pages from the file store and stops the ongoing read request."
tags:
  - "clippings"
---
Use this call to delete or cancel an initiated read request. This removes all the pages from the file store and stops the ongoing read request.

This cleans up temporary read requests after the integration has finished downloading the data, or cancels a request that is no longer needed.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- As a best practice, use this call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.
- An expiration timer starts after the read request is initiated, with the following conditions:
	- 30 minutes after no activity is recorded for that read request, the system will reclaim that space.
		- The expiration timer resets back to 30 minutes if the requested page number is divisible by 100, including page 0.

`curl -X DELETE 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

DELETE

`/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}`

| **Parameters** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{viewId}` | - Required - Type: `Number` - Description: The view ID. - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |

`curl -X DELETE 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewId}/readRequests/{requestId}' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Accept: application/json`

- Optional
- Description: This shows the preferred response is `application/json` format.

When the delete request completes, the API returns this response:

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/viewReadRequest"       },       "status": {           "code": 200,           "message": "Success"       },       "viewReadRequest": {           "requestId": "0A06B0739F0E47BB92E2326C603D86EC",           "viewId": 101000000014,           "requestState": "CANCELLED",           "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/views/{viewIdƒ}/readRequests/{requestId}",           "successful": true       }   }`

View these endpoints for further details on downloading list item subsets:

- [Retrieve lists](https://help.anaplan.com/35da6efd-37f9-493e-b766-0955fe5318de)
- [Retrieve list metadata](https://help.anaplan.com/0a4dbc25-ee0e-486d-8efb-c7bd6fc45309)
- [Lookup dimension items by name or code](https://help.anaplan.com/fef4e29e-be1a-4fa1-974b-304ca3d70fd5)

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fdelete-read-requests-for-view-data-71a6b2da-008c-40e7-ba05-103730de30b2&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top