---
title: "Retrieve lists"
source: "https://help.anaplan.com/retrieve-lists-35da6efd-37f9-493e-b766-0955fe5318de"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve lists for a specified workspace and model."
tags:
  - "clippings"
---
[Model lists](https://help.anaplan.com/model-lists-887c7595-8298-4f7a-a992-426a58896eaa "Model lists")

This helps an integration discover available lists and collect list IDs before reading, updating, or validating list item data.

GET

`/workspaces/{workspaceId}/models/{modelId}/lists`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` |  |
| `{modelId}` |  |

`curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/lists' \   -H 'Accept: application/json' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'`

`{       "meta": {           "paging": {               "currentPageSize": 5,               "offset": 0,               "totalSize": 5           },           "schema": "https://api.anaplan.com/2/0/models/75A40874E6B64FA3AE0743278996850F/objects/list"       },       "status": {           "code": 200,           "message": "Success"       },       "lists": [           {               "id": "101000000000",               "name": "Organization"           },           {               "id": "101000000001",               "name": "opportunities"           },           {               "id": "101000000002",               "name": "sales rep"           },           {               "id": "101000000003",               "name": "Bakery"           },           {               "id": "101000000004",               "name": "List2"           }       ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-lists-35da6efd-37f9-493e-b766-0955fe5318de&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top