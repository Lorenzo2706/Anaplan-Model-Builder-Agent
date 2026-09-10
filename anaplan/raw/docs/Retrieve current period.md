---
title: "Retrieve current period"
source: "https://help.anaplan.com/retrieve-current-period-40b7d97b-8ad2-423e-adb0-cc4edc5d1420"
author:
published:
created: 2026-09-09
description: "Use this call to determine the value of the current period in Anaplan."
tags:
  - "clippings"
---
[Model calendar](https://help.anaplan.com/model-calendar-a7bedbbb-c170-4f0b-9ac6-42669af1cfc6 "Model calendar")

This helps an integration determine which time period the model currently treats as “current” before loading data, running forecasts, or applying time-based logic.

If the current period is not set in Anaplan, this call returns empty strings for the `periodText` and `lastDay` values of the `currentPeriod`.

**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).

GET

`/workspaces/{workspaceId}/models/{modelId}/currentPeriod`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the ID for the model - Example: `75A40874E6B64FA3AE074327899685` |

`curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/currentPeriod' \   -H 'Accept: application/json' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'`

`Content-Type: application/json`

`{     "meta" : {       "schema" : "https://api.anaplan.com/2/0/objects/currentPeriod"     },     "status" : {       "code" : 200,       "message" : "Success"     },     "currentPeriod" : {       "periodText" : "May 20",       "lastDay" : "2020-05-31",       "calendarType" : "Calendar Months/Quarters/Years"     }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-current-period-40b7d97b-8ad2-423e-adb0-cc4edc5d1420&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top