---
title: "Set version switchover date"
source: "https://help.anaplan.com/set-version-switchover-date-0871aa1b-285b-46b5-a62e-df54ec6de71e"
author:
published:
created: 2026-09-09
description: "Use this call to set the switchover date for a version."
tags:
  - "clippings"
---
[Model versions](https://help.anaplan.com/model-versions-875d2b53-dcaf-4658-94dd-af27e10e1586 "Model versions")

This enables an integration to automate the point at which actual data replaces forecast data for that version as part of a period-close or rolling-forecast process.

The response contains the response code, as well as the date and human-readable date period as shown in the UI.

**Notes:**

- Touse this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- To apply a switchover date, ensure the `versionID` corresponds to a version in Anaplan that is set to either `forecast` or `variance`.
- Ensure the switchover date is after the existing version switchover date.
- To reset the switchover date to Blank, pass an empty string in the request body.

PUT

`/models/{modelId}/versions/{versionId}/switchover`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |
| `{versionId}` | - Required - Type: String - Description: the version ID. The ID of the actual version returns a `400 Bad Request` response - Example: `107000000002` |

`curl -X PUT 'https://api.anaplan.com/2/0/models/{modelId}/versions/{versionId}/switchover' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json' \   -H 'Content-Type: application/json' \   -d '{"date":"{newSwitchoverDate}"}'`

`Content-Type: application/json`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/switchover"       },       "status": {           "code": 200,           "message": "Success"       },       "versionSwitchover": {           "periodText": "May 13",           "date": "2013-05-01",           "calendarType": "Calendar Months/Quarters/Years"       }   }`

Endpoints that enable you to obtain user information accessible to you using your authentication token.

As a standard user, you can access the data to which you have been granted access. Endpoints respond with `401 Not Authorized` if you aren't authorized to access the data that you are requesting.

Note that these API calls only work with the user's default tenant. They won't return data for any additional tenants the user is assigned to.

View these endpoints for further details on users APIs:

- [Retrieve your user](https://help.anaplan.com/d5e7ae19-0a8a-44a7-a482-bdee7479e039)
- [Retrieve user information](https://help.anaplan.com/45d7e37a-652c-44f1-8b81-06b9034f707c)
- [Retrieve user list](https://help.anaplan.com/24b4492c-3dda-4cae-ae07-7ccdb134a433)

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fset-version-switchover-date-0871aa1b-285b-46b5-a62e-df54ec6de71e&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top