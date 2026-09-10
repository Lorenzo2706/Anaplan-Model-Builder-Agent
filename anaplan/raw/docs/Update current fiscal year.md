---
title: "Update current fiscal year"
source: "https://help.anaplan.com/update-current-fiscal-year-dfd2b4e0-1cf1-4001-a08f-788485683668"
author:
published:
created: 2026-09-09
description: "Use this call to update the current fiscal year for the model calendar."
tags:
  - "clippings"
---
[Model calendar](https://help.anaplan.com/model-calendar-a7bedbbb-c170-4f0b-9ac6-42669af1cfc6 "Model calendar")

This supports annual rollover and administrative automation when the model needs to move into a new fiscal year.

The year input value has to be a valid fiscal year supported by the model calendar in Anaplan. If successful, this call returns the updated fiscal year with start and end dates associated with current model calendar type. This call returns a `400 bad request` message if the input value is out of range or model calendar type doesn't have an available fiscal year, for example, Weeks General.

**Note:** Touse this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).

PUT

`/workspaces/{workspaceId}/models/{modelId}/modelCalendar/fiscalYear`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |

`curl -X PUT 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/modelCalendar/fiscalYear' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json' \   -H 'Content-Type: application/json' \   --data-raw '{       "year": "{fiscal year}"   }'`

`Content-Type: application/json`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"       },       "status": {           "code": 200,           "message": "Success"       },       "modelCalendar": {           "fiscalYear": {               "year": "FY21",               "startDate": "2021-01-01",               "endDate": "2021-12-31"           }       }   }`

Input value for `year`

`{       "year": "FY40"   }`

`{       "status": {           "code": 400,           "message": "Specified year is out of range: 2040"       }   }`

View these endpoints for more details:

- [Retrieve version metadata](https://help.anaplan.com/163d2e53-86a7-42ac-9193-3c7f52d9d5e3)
- [Set version switchover date](https://help.anaplan.com/0871aa1b-285b-46b5-a62e-df54ec6de71e)

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fupdate-current-fiscal-year-dfd2b4e0-1cf1-4001-a08f-788485683668&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top