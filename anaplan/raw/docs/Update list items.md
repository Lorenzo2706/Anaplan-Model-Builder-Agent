---
title: "Update list items"
source: "https://help.anaplan.com/update-list-items-ff3e2766-e28c-4c78-b049-cdb6f2e7f70e"
author:
published:
created: 2026-09-09
description: "Use this call to update items to a list. You must provide the model ID and list ID on the request URL."
tags:
  - "clippings"
---
[Model lists](https://help.anaplan.com/model-lists-887c7595-8298-4f7a-a992-426a58896eaa "Model lists")

Use this call to update items to a list. You must provide the model ID and list ID on the request URL.

This lets an integration maintain item properties such as names, codes, parent relationships, or other list attributes.

There are two kinds of lists in Anaplan: standard list and numbered list. For a standard list, the API identifies the item using the id, code, or name. For numbered list, the API uses the id or code. If property or subset is not specified in the input, the existing value is not updated. You can update one or more items in each request.

When you specify the list item identifier, select one of the appropriate identifiers (id, code, or name). If the request contains multiple identifiers, the API returns an error.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- A maximum of 100,000 list items can be updated with a single call.
- The update list items allows updates or lists and numbered Lists.

Note: When an update to a list item completes successfully, all downstream calculations are also complete. This includes cells linked by formulas to the cells being updated.

PUT

`/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: Number - Description: the list ID - Example: `101000000001` |

| **Parameter** | **Details** |
| --- | --- |
| `action` | - Required - Type: String - Value: `update` - Example: `?action=update` |

`curl -X PUT 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json' \   -H 'Accept: application/json'`

The response body contains a JSON object that contains `total` (total number of items in request), `updated` (number of items updated), `ignored` (number of items ignored), and `failures` fields. On `failures`, each field contains information about any errors encountered while performing the update action. `requestIndex` is the index in the input items array.

`{       "meta": {           "schema": "https://anaplan.api.com/2/0/objects/list"       },       "status": {           "code": 200,           "message": "Success"       },       "total": 2,       "ignored": 1,       "updated": 1,       "failures": {          {             "failureType": "INCORRECT_FORMAT",             "failureMessageDetails": "incorrect format -- column name:p-number, value:wrong format for number",             "requestIndex": 1          }       }   }`

Back to top