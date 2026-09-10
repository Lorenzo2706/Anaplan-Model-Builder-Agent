---
title: "Retrieve a specific model"
source: "https://help.anaplan.com/retrieve-a-specific-model-8baa6c1e-265f-440b-af26-1963fb88474c"
author:
published:
created: 2026-09-09
description: "Retrieves information about a specific model in the user's default tenant, if the user has access to the model."
tags:
  - "clippings"
---
[Model information](https://help.anaplan.com/model-information-c2998f80-d007-4a36-aef0-485923a38045 "Model information")

Retrieves information about a specific model in the user's default tenant, if the user has access to the model.

This helps validate that a model exists, confirm access, and check whether it is the correct target before running actions or retrieving data.

GET

`/models/{modelId}`

| **Parameter** | **Description** |
| --- | --- |
| `modelId` |  |
| `modelDetails` | - Optional - Type: Boolean - Description: When set to `true`, this call returns the available model memory usage in bytes and models status information. When set to `false`, or not defined, this call doesn't return the model memory usage. - Example: `?modelDetails=true` |

`curl -X GET \   https://api.anaplan.com/2/0/models/{modelId} \   -H 'authorization: AnaplanAuthToken {anaplan_auth_token}'`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/model"     },     "model": {       "id": "FC12345678912343455667",       "activeState": "UNLOCKED",       "name": "PF&A",       "currentWorkspaceId": "8a8b8c8d8e8f8g8i",       "currentWorkspaceName": "Financial Planning",       "modelUrl": "https://rt.anaplan.com/anaplan/rt?selectedWorkspaceId\8a8b8c8d8e8f8g8i\u0026selectedModelId\FC12345678912343455667",       "categoryValues": []     },     "status": {       "code": 200,       "message": "Success"     }   }`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/model"       },       "status": {           "code": 200,           "message": "Success"       },       "model": {           "id": "FC12345678912343455667",           "name": "PF&A",           "activeState": "UNLOCKED",           "lastSavedSerialNumber": 2000000,           "modelTransactionRunning": false,           "lastModifiedByUserGuid": "5c8f44f65d3a11ea95e4026d2ec6a15d",           "memoryUsage": 474900,           "currentWorkspaceId": "8a8b8c8d8e8f8g8i",           "currentWorkspaceName": "Financial Planning",       "modelUrl": "https://rt.anaplan.com/anaplan/rt?selectedWorkspaceId\8a8b8c8d8e8f8g8i\u0026selectedModelId\FC12345678912343455667",           "categoryValues": [],           "isoCreationDate": "2022-02-10T19:14:23.000+0000",           "lastModified": "2022-02-10T19:14:24.000+0000"       }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-a-specific-model-8baa6c1e-265f-440b-af26-1963fb88474c&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top