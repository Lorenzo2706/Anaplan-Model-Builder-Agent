---
title: "Get current fiscal year"
source: "https://help.anaplan.com/get-current-fiscal-year-0454318c-0d4f-4d35-8d0e-2969a03ec7b3"
author:
published:
created: 2026-09-09
description: "Use this call to get the current fiscal year with the start and end date from the model calendar."
tags:
  - "clippings"
---
[Model calendar](https://help.anaplan.com/model-calendar-a7bedbbb-c170-4f0b-9ac6-42669af1cfc6 "Model calendar")

Use this call to get the current fiscal year with the start and end date from the model calendar.

This helps external systems align their time references with the model’s fiscal calendar before exchanging or validating data.

The value of the start and end dates is determined by the calendar type set in the model. This value isn't always in a range from Jan. 1 to Dec. 31. The API returns an empty value if the calendar type doesn't have an available fiscal year, for example, Weeks General.

**Note:** Touse this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).

GET

`/workspaces/{workspaceId}/models/{modelId}/modelCalendar`

| **Parameter** | **Details** |
| --- | --- |
| `{workspaceId}` | - Required - Type: String - Description: The workspace ID - Example: `8a8196b15b7dbae6015b8694411d13fe` |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |

`curl -X GET 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/modelCalendar' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"       },       "status": {           "code": 200,           "message": "Success"       },       "modelCalendar": {           "fiscalYear": {               "year": "FY21",               "startDate": "2021-01-01",               "endDate": "2021-12-31"           }       }   }`

In Anaplan, the **Current fiscal year** in the **Model Calendar** is set to *FY21: 29 Mar. 2020–27 Mar. 2021*.

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"     },     "status": {       "code": 200,       "message": "Success"     },     "modelCalendar": {       "calendarType": "Calendar Months/Quarters/Years",       "fiscalYear": {         "year": "FY21",         "startDate": "2020-03-29",         "endDate": "2021-03-27"       },       "pastYearsCount": 0,       "futureYearsCount": 0,       "currentPeriod": {         "periodText": "",         "lastDay": ""       },       "totalsSelection": {         "quarterTotals": true,         "halfYearTotals": false,         "yearToDateSummary": false,         "yearToGoSummary": false,         "totalOfAllPeriods": false       }     }   }`

In Anaplan, the **Calendar Type** in the **Model Calendar** is set to *weeks general*.

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/modelCalendar"       },       "status": {           "code": 200,           "message": "Success"       },       "modelCalendar": {}   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fget-current-fiscal-year-0454318c-0d4f-4d35-8d0e-2969a03ec7b3&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top