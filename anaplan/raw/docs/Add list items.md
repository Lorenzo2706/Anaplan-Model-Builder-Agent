---
title: "Add list items"
source: "https://help.anaplan.com/add-list-items-4c87489b-e241-4a31-b4ab-e689edd5d7b8"
author:
published:
created: 2026-09-09
description: "Use this call to add items to a list. You must provide the list ID and data for each item. You can add one or more items in each request."
tags:
  - "clippings"
---
[Model lists](https://help.anaplan.com/model-lists-887c7595-8298-4f7a-a992-426a58896eaa "Model lists")

Use this call to add items to a list. You must provide the list ID and data for each item. You can add one or more items in each request.

This enables an integration to keep Anaplan master data aligned with an external source system.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- A maximum of 100,000 list items can be added with a single call.

POST

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=add`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` |  |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: Number - Description: the list ID - Example: `101000000001` |

| **Parameter** | **Details** |
| --- | --- |
| `action` | - Required - Type: String - Value: `add` - Example: `?action=add` |

`curl -X POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=add' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json' \   -H 'Accept: application/json'`

The response body contains a JSON object that contains `total` (total number of items in request), `ignored` (number of items ignored), `added` (number of items added), and `failures` (a description of the reason of each failure) fields. In the `failures` response, each field contains failures information about any errors encountered while performing the add action. `requestIndex` is the index in input items array.

`{       "meta": {           "schema": "https://anaplan.api.com/2/0/objects/item"       },       "status": {           "code": 200,           "message": "Success"       },       "added": 1,       "ignored": 1,       "total": 2,       "failures": [           {               "requestIndex": 1,               "failureType": "INCORRECT_FORMAT",               "failureMessageDetails": "incorrect format -- column name:p-number, value:wrong value for number"           }       ]   }`

Back to top