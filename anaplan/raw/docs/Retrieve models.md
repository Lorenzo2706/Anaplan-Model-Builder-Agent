---
title: "Retrieve models"
source: "https://help.anaplan.com/retrieve-models-9287c44b-7383-4ff2-b6fb-da34d77c6017"
author:
published:
created: 2026-09-09
description: "Retrieves information about all models in the user's default tenant, unless the user is not a Workspace Administrator. In that case, it returns only the models the user has been given access to."
tags:
  - "clippings"
---
[Model information](https://help.anaplan.com/model-information-c2998f80-d007-4a36-aef0-485923a38045 "Model information")

Retrieves information about all models in the user's default tenant, unless the user is not a Workspace Administrator. In that case, it returns only the models the user has been given access to.

This helps an integration find available models and collect model IDs before making model-specific calls.

**Note:** If no **offset** or **limit** parameters are used in the request, results will be limited to the first 5000 models.

If your call returns a lot of data, you can specify that results are returned in pages. You can specify:

- A **limit** for the number of results to return per page.
- An **offset** to get a specific page of results starting from a particular result.

The **paging** attribute specifies the number of results returned by an API request in pages. This is not the number of pages in a file.

GET

/models

| **Parameter** | **Required** | **Type** | **Description** | **Example** |
| --- | --- | --- | --- | --- |
| **{modelDetails}** | Optional | Boolean | When set to **true**, this call returns the available model memory usage in bytes. When set to **false**, or not defined, this call does not return the model memory usage. | ?modelDetails=true |
| **{offset}** | Optional | Numeric | Sets the starting point from which models are returned. | ?offset=5 |
| **{limit}** | Optional | Numeric | Sets the number of models to be returned by the request. | ?limit=10 |

`curl -X GET \   https://api.anaplan.com/2/0/models \   -H 'authorization: AnaplanAuthToken {anaplan_auth_token}'`

`{     "meta": {       "schema": "https://api.anaplan.com/2/0/objects/model",       "paging": {         "currentPageSize": 1,         "totalSize": 1,         "offset": 0       }     },     "status": {       "code": 200,       "message": "Success"     },     "models": [{         "id": "FC12345678912343455667",         "activeState": "UNLOCKED",         "name": "FP&A",         "currentWorkspaceId": "8a8b8c8d8e8f8g8i",         "currentWorkspaceName": "Financial Planning",         "modelUrl": "https://rt.anaplan.com/anaplan/rt?selectedWorkspaceId\8a8b8c8d8e8f8g8i\u0026selectedModelId\FC12345678912343455667",         "categoryValues": []      }]   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-models-9287c44b-7383-4ff2-b6fb-da34d77c6017&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top