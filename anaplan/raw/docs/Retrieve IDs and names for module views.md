---
title: "Retrieve IDs and names for module views"
source: "https://help.anaplan.com/retrieve-ids-and-names-for-module-views--57540d7f-d05f-42c3-a68e-fb925dabf962"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve all view IDs and names for a specified module."
tags:
  - "clippings"
---
Helps narrow view discovery to a known module, making it easier to target the correct view for metadata inspection or data retrieval. This call also returns the default view for the module. If the user adds the query parameter `includesubsidiaryviews=true`, unsaved subsidiary views will also be included in the results.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html)
- For the default view, the `{viewId}` is the same as the `{moduleId}`
- For unsaved subsidiary views, the `{viewId}` and `{viewName}` are the same as the `{lineItemId}` and `{lineItemName}` that the subsidiary view is created from

GET

`/models/{modelId}/modules/{moduleId}/views`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |
| `{moduleId}` | - Required - Type: number - Description: the ID for the module - Example: `102000000028` |
| `{includesubsidiaryviews}` | - Optional (default false) - Type: String - Description: Whether the response should include unsaved subsidiary views. The field is interpreted as false if anything other than `true` is specified - Example: `?includesubsidiaryviews=true` |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules/{moduleId}/views' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{     "meta": {       "paging": {         "currentPageSize": 1,         "offset": 0,         "totalSize": 1       },       "schema": "https://api.anaplan.com/2/0/objects/view"     },     "status": {       "code": 200,       "message": "Success"     },     "views": [       {         "code": "",         "id": "102000000000",         "name": "default",         "moduleId": "102000000000"       },       {         "code": "",         "id": "203000000000",         "name": "SavedView",         "moduleId": "102000000000"       }     ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-ids-and-names-for-module-views--57540d7f-d05f-42c3-a68e-fb925dabf962&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top