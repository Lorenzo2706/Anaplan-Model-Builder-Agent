---
title: "Retrieve IDs and names of model views"
source: "https://help.anaplan.com/retrieve-ids-and-names-of-model-views-bcc1ed22-52b5-4537-ad90-77c65b77deeb"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve the ID and name of all views for a model."
tags:
  - "clippings"
---
This helps an integration discover available saved views that can be used as data sources for reads or exports.

The results include default and saved views. If you add the query parameter `includesubsidiaryviews=true`, this includes unsaved subsidiary views in the results. This call also retrieves the ID of the module that the views belong to.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html)
- Single quotes enclose the module and view names that have special characters

For default views:

- The value of the {viewId} is identical to the value of the {moduleId}
- The value of the name is identical to the value of the module

For saved views:

- The `name` consists of the module name, a period, and the saved view name. For example, `REP01 Profit & Loss Report.P & L by Country`

For unsaved subsidiary views:

- The name consists of the module name and the line item name that the subsidiary view is created from
- These are separated by a period(.)

GET

`/models/{modelId}/views`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

`curl -X GET   'https://api.anaplan.com/2/0/models/{modelId}/views' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{     "meta": {       "paging": {         "currentPageSize": 1,         "offset": 0,         "totalSize": 1       },       "schema": "https://api.anaplan.com/2/0/objects/view"     },     "status": {       "code": 200,       "message": "Success"     },     "views": [       {         "code": "",         "id": "102000000000",         "name": "StrategicPlanning",         "moduleId": "102000000000"       },       {         "code": "",         "id": "207000000000",         "name": "StrategicPlanning.UK Financial forecast",         "moduleId": "102000000000"       },       {         "code": "",         "id": "207000000001",         "name": "StrategicPlanning.EMEAforecastreport",         "moduleId": "102000000000"       },       {         "code": "",         "id": "207000000002",         "name": "StrategicPlanning.'accountSummary&overview/US$'",         "moduleId": "102000000000"       },       {         "code": "",         "id": "237000000001",         "name": "'StrategicPlanning/2020'.'accountSummary&overview/US$'",         "moduleId": "102000000001"       }     ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-ids-and-names-of-model-views-bcc1ed22-52b5-4537-ad90-77c65b77deeb&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top