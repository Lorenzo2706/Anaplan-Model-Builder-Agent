---
title: "Retrieve IDs and names of modules"
source: "https://help.anaplan.com/retrieve-ids-and-names-of-modules-82183d8b-f928-4604-a20d-30dbb47aca59"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve the IDs and names of all modules for a specified model."
tags:
  - "clippings"
---
Use this call to retrieve the IDs and names of all modules for a specified model.

This helps an integration identify which modules exist before retrieving views, line items, or data from a specific module.

**Note:** To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

GET

`/models/{modelId}/modules`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` |  |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/modules' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{     "meta": {       "paging": {         "currentPageSize": 1,         "offset": 0,         "totalSize": 1       },       "schema": "https://api.anaplan.com/2/0/objects/module"     },     "status": {       "code": 200,       "message": "Success"     },     "modules": [{         "id": "102000000125",         "name": "REV01 Price Book"       },       {         "id": "102000000121",         "name": "REV02 Volume Inputs"       }]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-ids-and-names-of-modules-82183d8b-f928-4604-a20d-30dbb47aca59&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top