---
title: "Look up dimension items by name or code"
source: "https://help.anaplan.com/look-up-dimension-items-by-name-or-code-fef4e29e-be1a-4fa1-974b-304ca3d70fd5"
author:
published:
created: 2026-09-09
description: "Retrieve the items from a dimension that match one of a list of names or a list or codes."
tags:
  - "clippings"
---
Retrieve the items from a dimension that match one of a list of names or a list or codes.

This endpoint helps an integration resolve human-readable values, such as product names or employee codes, into the internal item identifiers needed for API operations.

**Notes:**

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- This call does not return results for names or codes for which an item does not exist.
- If the given workspace, model, or dimension do not exist, this call returns a `404` code.
- If the dimension does not support codes and codes are provided, this call returns a `400` code.

`curl -X POST https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/dimensions/{dimensionId}/items \   -H ‘Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json' \   -H 'Accept: application/json' --data-raw '<see Request body>'`

POST

`/workspaces/{workspaceId}/models/{modelId}/dimensions/{dimensionId}/items`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required in the supported request - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{dimensionId}` | - Required - Type: Number - Description: the dimension ID. This value must be the ID for any of these dimension types: 	- Lists 		- Time periods 		- Users 		- Versions - Example: `101000000001` |

`curl -X POST https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/dimensions/{dimensionId}/items \   -H ‘Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type: application/json' \   -H 'Accept: application/json' --data-raw '<see Request body>'`

`{     "meta" : {         "schema":"https://api.anaplan.com/2/0/objects/dimension"     },     "status" : {       "code":200,       "message":"Success"     },     "items":[       {         "name":"South",         "id":"208000000001",         "code":"S"       },       {         "name":"West",         "id":"208000000004",         "code":"W"       }     ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Flook-up-dimension-items-by-name-or-code-fef4e29e-be1a-4fa1-974b-304ca3d70fd5&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top