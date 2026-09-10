---
title: "Delete read requests for list item data"
source: "https://help.anaplan.com/delete-read-requests-for-list-item-data-50cae78a-5865-47c9-8a27-57392add72e4"
author:
published:
created: 2026-09-09
description: "Use this call to delete or cancel an initiated read request. This removes all the pages from the file store and stops the ongoing read request."
tags:
  - "clippings"
---
Use this call to delete or cancel an initiated read request. This removes all the pages from the file store and stops the ongoing read request.

This cleans up temporary read-request output when the integration has finished downloading the data.

**Notes:**

- Touse this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- As a best practice, use this call to clear all pages from completed exports as soon as you download all pages. Doing so will make space available for future exports.
- An expiration timer starts after the read request is initiated, with the following conditions:
	- 30 minutes after no activity is recorded for that read request, the system will reclaim that space.
		- The expiration timer resets back to 30 minutes if the requested page number is divisible by 100, including page 0.

DELETE

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}`

| **Parameters** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required in the first supported request (see Requests supporting this feature) - Type: `String` - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: `String` - Description: The model ID - Example: `75A40874E6B64FA3AE0743278996850F` |
| `{listId}` | - Required - Type: `Number` - Description: The list ID - Example: `101000000001` |
| `{requestId}` | - Required - Type: `String` - Description: The request ID - Example: `0A06B0739F0E47BB92E2326C603D86EC` |

`curl -X DELETE 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json' \   -H 'Accept: application/json'`

When the initiated read request ID completes and you delete it, the API returns this response:

`{           "meta": {               "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"           },           "status": {               "code": 200,               "message": "Success"           },           "listReadRequest": {               "requestId": "0A06B0739F0E47BB92E2326C603D86EC",               "listId": 101000000014,               "requestState": "COMPLETE",               "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}",               "successful": true           }       }`

If the read request is in progress and you initiate the delete call, the API returns this response:

` {           "meta": {               "schema": "https://api.anaplan.com/2/0/objects/listReadRequest"           },           "status": {               "code": 200,               "message": "Success"           },           "listReadRequest": {               "requestId": "0A06B0739F0E47BB92E2326C603D86EC",               "listId": 101000000014,               "requestState": "CANCELLED",               "url": "https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/readRequests/{requestId}",               "successful": true           }       }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fdelete-read-requests-for-list-item-data-50cae78a-5865-47c9-8a27-57392add72e4&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top