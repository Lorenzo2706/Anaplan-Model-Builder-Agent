---
title: "Retrieve workspace information"
source: "https://help.anaplan.com/retrieve-workspace-information-287f8d90-d8fb-4e6d-93b5-4efd7036388f"
author:
published:
created: 2026-09-09
description: "Retrieves information on a specific workspace if the user has access."
tags:
  - "clippings"
---
[Workspace endpoints](https://help.anaplan.com/workspace-endpoints-6fc5cf2c-9bd7-4c7f-9fc9-e7a542444bda "Workspace endpoints")

This helps validate that a workspace exists, confirm access, and gather workspace metadata needed for other API workflows.

This endpoint can also return size-related details when requested.

GET

`/workspaces/{workspaceId}?tenantDetails=true`

| **Parameter** | **Details** |
| --- | --- |
| `workspaceId` |  |
| `tenantDetails` | - Optional - Type: Boolean - Description: When set to true, this call returns an estimate of the current size (`currentSize`) of the workspace from all the models it contains and the allotted quota (`sizeAllowance`). When set to false, or not defined, this call doesn't return an estimated current size of the workspace. - Example: true |

`curl -X GET \   https://api.anaplan.com/2/0/workspaces/{workspaceId}?tenantDetails=true \   -H 'authorization: AnaplanAuthToken {anaplan_auth_token}'`

`Content-Type: application/json`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/workspace"     },     "status": {       "code": 200,       "message": "Success"     },     "workspace": {       "id": "8a8b8c8d8e8f8g8i",       "name": "Financial Planning",       "active":true,       "sizeAllowance": 1073741824,       "currentSize": 873741824     }   }`

View these endpoints for further details on models APIs:

- [Retrieve models](https://help.anaplan.com/9287c44b-7383-4ff2-b6fb-da34d77c6017)
- [Retrieve a specific model](https://help.anaplan.com/8baa6c1e-265f-440b-af26-1963fb88474c)
- [Bulk delete models](https://help.anaplan.com/e45461b7-075f-4643-9174-9c4c5519ad36)
- [Check model status](https://help.anaplan.com/4e3e18e7-07ba-4daa-9aac-7d790ce73985)
- [Close model](https://help.anaplan.com/055d2f9e-901c-490f-a971-c9c64f4f6698)
- [Wake up model](https://help.anaplan.com/2eaefdd5-4958-4bb0-9e3c-a5457c20afed)

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-workspace-information-287f8d90-d8fb-4e6d-93b5-4efd7036388f&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top