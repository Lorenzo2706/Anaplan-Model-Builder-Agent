---
title: "Delete list items"
source: "https://help.anaplan.com/delete-list-items-c44b7cba-b6c3-49c6-abdb-fea2f9db96b7"
author:
published:
created: 2026-09-09
description: "Use this call to delete items from a list. You must provide the list ID or Code to identify each list item."
tags:
  - "clippings"
---
[Model lists](https://help.anaplan.com/model-lists-887c7595-8298-4f7a-a992-426a58896eaa "Model lists")

Use this call to delete items from a list. You must provide the list ID or Code to identify each list item.

This supports controlled cleanup or synchronization when items are removed from the source system or are no longer needed in the model.

You can delete one or more list items in one API call by providing different identifiers for each item. For example, provide the ID for one item and code for another.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- A maximum of 100,000 list items can be deleted with a single call.

POST

/ `workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=delete`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{listId}` | - Required - Type: Number - Description: the list ID - Example: `101000000001` |

| **Parameter** | **Details** |
| --- | --- |
| `action` | - Required - Type: String - Value: `delete` - Example: `?action=delete` |

`curl -X POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists/{listId}/items?action=delete' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json' \   -H 'Accept: application/json'`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/list"       },       "status": {           "code": 200,           "message": "Success"       },       "deleted": 2   }`

The response body contains a JSON object which has a `deleted` field and a `failures` field that contains information about any errors encountered while performing the delete action. Each item contains the identifier specified in the request.

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/list"       },       "status": {           "code": 200,           "message": "Success"       },       "result": {           "numberOfItemsDeleted": 1,           "failures": [               {                   "requestIndex": 1,                   "failureType": "Not found",                   "failureMessageDetails": "Code 'Region 1' not found"               },               {                   "requestIndex": 2,                   "failureType": "Ambiguous criteria",                   "failureMessageDetails": "Specifying both ID and code not supported (201000000001:i1)"               }           ]       }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fdelete-list-items-c44b7cba-b6c3-49c6-abdb-fea2f9db96b7&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top