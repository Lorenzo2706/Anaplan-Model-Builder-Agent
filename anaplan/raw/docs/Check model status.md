---
title: "Check model status"
source: "https://help.anaplan.com/check-model-status-4e3e18e7-07ba-4daa-9aac-7d790ce73985"
author:
published:
created: 2026-09-09
description: "Certain actions such as imports, exports, or writeback actions require exclusive access to a model during their execution. These actions lock the model. Any attempt to read information via the API is blocked as they require an exclusive transaction to run. This endpoint provides a status for the model."
tags:
  - "clippings"
---
[Model information](https://help.anaplan.com/model-information-c2998f80-d007-4a36-aef0-485923a38045 "Model information")

Certain actions such as imports, exports, or writeback actions require exclusive access to a model during their execution. These actions lock the model. Any attempt to read information via the API is blocked as they require an exclusive transaction to run. This endpoint provides a status for the model.

This helps integrations avoid conflicts by checking whether the model is busy before attempting operations that require model availability.

POST

`/workspaces/{workspaceId}/models/{modelId}/status`

`curl -X POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/status' \    -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'   -H 'Content-Type: application/json'`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/dimension"       },       "status": {           "code": 200,           "message": "Success"       },      "requestStatus":{         "exportTaskType":null,         "taskId":"6EB7F52C07CA4E86909A213C608765A1-11",         "currentStep":"Processing ...",         "tooltip":"The system is currently processing an Export:\n\nExport started by user Jesse Smith (jesse.smith@yourcompany.com)\n\nExport started at 11:23 (UTC)\nTasks can be cancelled in Model Management.",         "progress":0.44110000000000005,         "creationTime":1578569563167      }   }`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/dimension"       },       "status": {           "code": 200,           "message": "Success"       },       {       "requestStatus": {           "peakMemoryUsageEstimate": null,           "peakMemoryUsageTime": null,           "progress": 0.0,           "currentStep": "Processing ...",           "tooltip": "The system is currently processing an Import:\n\nImport started by user Jesse Smith (jesse.smith@yourcompany.com)\n\nImport started at 00:51 (UTC)\nTasks can be cancelled in Model Management.",           "exportTaskType": null,           "creationTime": 1645577520129,           "taskId": "E9CB709BD63D4003ACFB60CADFC2FC0B"       }   }`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/dimension"       },       "status": {           "code": 200,           "message": "Success"       },       {       "requestStatus": {           "creationTime": 1646264082002,           "progress": -1.0,           "taskId": null,           "currentStep": "Updating",           "tooltip": null,           "exportTaskType": null,           "peakMemoryUsageEstimate": null,           "peakMemoryUsageTime": null       }   }`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/dimension"       },       "status": {           "code": 200,           "message": "Success"       },       "requestStatus": {           "peakMemoryUsageEstimate": null,           "peakMemoryUsageTime": null,           "progress": -1.0,           "currentStep": "Open",           "tooltip": null,           "exportTaskType": null,           "creationTime": 1645577591822,           "taskId": null       }   }`

From the above responses, the `currentStep` property returns the status of the model under different scenarios -

- `Open` - When no process is running on the model.
- `Processing` - When import/export task is being processed on the model.
- `Updating` - When any update is being performed on the model, for example: cell write.
- `Closed` - When model is in maintenance state.

The `tooltip` returns details about the transaction being performed on the model. It also provides the user information who initiated the transaction along-with the progress information.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fcheck-model-status-4e3e18e7-07ba-4daa-9aac-7d790ce73985&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top