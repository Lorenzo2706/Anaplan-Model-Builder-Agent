---
title: "Retrieve all line items in a model"
source: "https://help.anaplan.com/retrieve-all-line-items-in-a-model-5bdf5544-ae86-414e-87f9-f74f3f45bba7"
author:
published:
created: 2026-09-09
description: "Use this call to retrieve identifiers of all line items in a model."
tags:
  - "clippings"
---
**Notes**:

- To use this call, you must be a [Workspace Administrator](https://help.anaplan.com/anapedia/Content/Administration_and_Security/Workspace_Administration.html).
- The returned line items are restricted just to those in modules to which the model role of the user has Read access.
- The response returns Items within a [flat list](https://help.anaplan.com/anapedia/Content/Modeling/Dimensions/Lists.html) (no hierarchy).
- This returns all the line items in the model. For line items in a specific module see [Retrieve Line Items For a Module](https://help.anaplan.com/bf37fb71-ba13-4f9c-9a0c-bde0b2a99a10).

GET

`/models/{modelId}/lineItems`

| **Parameter** | **Details** |
| --- | --- |
| `{modelId}` |  |

`curl -X GET 'https://api.anaplan.com/2/0/models/{modelId}/lineItems' \   -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Accept: application/json'`

`Content-Type: application/json`

`{       "meta": {           "schema": "https://api.anaplan.com/2/0/objects/lineItem"       },       "status": {           "code": 200,           "message": "Success"       },       "items": [           {               "moduleId": "102000000000",               "moduleName": "Sales Entry",               "id": "206000000000",               "name": "Quantity Sold"           },           {               "moduleId": "102000000000",               "moduleName": "Sales Entry",               "id": "206000000001",               "name": "Price"           },           {               "moduleId": "102000000000",               "moduleName": "Sales Entry",               "id": "206000000002",               "name": "Revenue"           },           {               "moduleId": "102000000001",               "moduleName": "Profit",               "id": "208000000000",               "name": "Commission"           },           {               "moduleId": "102000000001",               "moduleName": "Profit",               "id": "208000000001",               "name": "Cost"           },           {               "moduleId": "102000000001",               "moduleName": "Profit",               "id": "208000000002",               "name": "Profit"           }       ]   }   `

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-all-line-items-in-a-model-5bdf5544-ae86-414e-87f9-f74f3f45bba7&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top