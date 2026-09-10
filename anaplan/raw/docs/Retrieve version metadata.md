---
title: "Retrieve version metadata"
source: "https://help.anaplan.com/retrieve-version-metadata-163d2e53-86a7-42ac-9193-3c7f52d9d5e3"
author:
published:
created: 2026-09-09
description: "Use this call to get information about the model versions."
tags:
  - "clippings"
---
[Model versions](https://help.anaplan.com/model-versions-875d2b53-dcaf-4658-94dd-af27e10e1586 "Model versions")

This helps an integration discover available versions and understand their settings before reading, writing, or synchronizing version-specific data.

The response contains a list of the versions that the user has access to, and the model metadata that can be viewed from the UI.

**Notes:**

- Touse this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09).
- The returned versions only include the user's model role with read access or higher.
- If the value for a field is set, it'll be returned in the results.

GET

`/models/{modelId}/versions`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` | - Required - Type: String - Description: the model ID - Example: `75A40874E6B64FA3AE074327899685` |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/versions' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'\   -H 'Accept: application/json'`

`Content-Type: application/json`

The date format for `editFrom` and `editTo` depends on the model calendar setting.

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/version"       },       "status": {           "code": 200,           "message": "Success"       },       "versionMetadata": [           {               "id": "107000000001",               "name": "Actual",               "isCurrent": false,               "isActual": true,               "editFrom": {                   "periodText": "Start of Timescale",                   "date": "1900-01-01"               },               "editTo": {                   "periodText": "End of Timescale",                   "date": "2399-12-31"               },               "notes": "This version data is updated every Monday"           },           {               "id": "107000000002",               "name": "Variance",               "isCurrent": false,               "isActual": false,               "switchover": {                   "periodText": "Mar 20",                   "date": "2020-03-01"               },               "formula": "Actual - 20",               "editFrom": {                   "periodText": "Jan 20",                   "date": "2020-01-01"               },               "editTo": {                   "periodText": "Dec 20",                   "date": "2020-12-31"               }           }       ]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-version-metadata-163d2e53-86a7-42ac-9193-3c7f52d9d5e3&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top