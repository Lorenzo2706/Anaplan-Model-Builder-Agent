---
title: "List user workspaces"
source: "https://help.anaplan.com/list-user-workspaces-c324d0af-01ce-4e6b-8039-06289a4f5b19"
author:
published:
created: 2026-09-09
description: "Retrieves all workspaces a user has access to within the user's default tenant."
tags:
  - "clippings"
---
[Workspace endpoints](https://help.anaplan.com/workspace-endpoints-6fc5cf2c-9bd7-4c7f-9fc9-e7a542444bda "Workspace endpoints")

Lists all workspaces the user can access in their default tenant. Can optionally include tenant details such as workspace size and allowance.

This helps an integration identify which workspaces are available to the user before making more specific model, import, export, or process calls.

GET

`/workspaces?tenantDetails=true`

| **Parameter** | **Details** |
| --- | --- |
| `tenantDetails` | - Optional - Type: Boolean - Description: When set to true, this call returns an estimate of the current size (`currentSize`) of the workspace from all the models it contains and the alotted quota (`sizeAllowance`). When set to false, or not defined, this call does not return an estimated current size of the workspace. - Example: true |

`curl -X GET \   https://api.anaplan.com/2/0/workspaces?tenantDetails=true \   -H 'authorization: AnaplanAuthToken {anaplan_auth_token}'`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/workspace",       "paging": {         "currentPageSize": 1,         "totalSize": 1,         "offset": 0       }     },     "status": {       "code": 200,       "message": "Success"     },     "workspaces": [       {       "id": "8a8b8c8d8e8f8g8i",       "name": "Financial Planning",       "active": true,       "sizeAllowance": 1073741824,       "currentSize": 873741824       }     ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Flist-user-workspaces-c324d0af-01ce-4e6b-8039-06289a4f5b19&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top